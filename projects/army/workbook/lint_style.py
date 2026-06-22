"""lint_style - build-time house-style invariants over the rendered sheets.

Mirrors verify_timing.py: renders every registered sheet and asserts the workbook_core
presentation rules the audit turned into gates, so a style regression fails like a tab-order
regression rather than slipping through. Exits non-zero on any UNexcepted violation; the
EXCEPTIONS table keeps a deliberate deviation visible instead of silently weakening a rule.

    python3 lint_style.py            # report + non-zero exit on unexcepted violations

Rules:
  TITLE_MISMATCH                       row-2 title banner != tab name
  UNNUMBERED_SECTION                   a section banner without a "§N" number
  VISIBLE_TEXT_OVER_180                a visible cell text longer than 180 chars
  COLUMN_WIDTH_OVER_LIMIT              a configured column wider than 50 chars
  PERCENT_HEADER_USING_NUM_STYLE       a "%" header whose column uses a non-percent style
  BLUE_INPUT_OUTSIDE_INPUTS_GROUP      a blue input cell on a non-inputs / non-data sheet
  MODEL_NATIVE_TABLE                   a native table on a model sheet (use a styled range)
  CATEGORICAL_INPUT_WITHOUT_VALIDATION a categorical input column with no data validation
"""
import re
import sys
from xml.etree import ElementTree as ET

import workbook_army  # noqa: F401  (puts workbook_army + workbook_core on sys.path)
from workbook_core.sheet_probe import inspect_worksheet_xml
from workbook_core.ooxml import NS_SS
from workbook_army.sheets import SHEETS
from workbook_army.sheets._text_input import S_TEXT_INPUT

WIDTH_LIMIT = 50
TEXT_LIMIT = 180

# Deliberate, documented deviations: {tab_name: {rule codes allowed on that sheet}}.
EXCEPTIONS = {
    # The filterable decision screens legitimately keep native tables (audit: "continue
    # using native tables for the timing and queue screens").
    # The editable As-of master clock is a deliberate blue input on the screen.
    "Timing & Incumbent Screen": {"MODEL_NATIVE_TABLE", "BLUE_INPUT_OUTSIDE_INPUTS_GROUP"},
    "Recompete Research Queue": {"MODEL_NATIVE_TABLE", "BLUE_INPUT_OUTSIDE_INPUTS_GROUP"},
    "Timing Detail": {"MODEL_NATIVE_TABLE"},
    # "Incumbent since" is a build-baked chain-root start the multi-hop walk can't express as
    # a formula - a hardcoded value, legitimately blue (handled via the rule code above).
}

_TITLE = "S_TITLE_SHEET"
_SECTION = "S_TITLE_SECTION"
_HEADERS = {"S_HEADER_LEFT", "S_HEADER_CENTER"}
_PCT = {"S_PCT", "S_PCT_INPUT", "S_LINK_PCT", "S_PCT_TOTAL", "S_PCT_INPUT_TOTAL",
        "S_LINK_PCT_TOTAL"}
_NUMERIC_NONPCT = {"S_NUM", "S_NUM_INPUT", "S_LINK_NUM", "S_NUM_TOTAL", "S_NUM_INPUT_TOTAL",
                   "S_LINK_NUM_TOTAL", "S_INT", "S_INT_INPUT", "S_LINK_INT", "S_INT_TOTAL"}
# Blue inputs: the numeric/date input styles by S_* name + the scoped blue-text style (which
# sheet_probe renders as "#<index>" since it lives outside workbook_core.styles).
_INPUT = {"S_NUM_INPUT", "S_PCT_INPUT", "S_INT_INPUT", "S_DATE_INPUT",
          "S_NUM_INPUT_TOTAL", "S_PCT_INPUT_TOTAL", "S_INT_INPUT_TOTAL",
          "S_DATE_INPUT_TOTAL", f"#{S_TEXT_INPUT}"}
# Categorical fields that must carry a dropdown when rendered as an editable input.
_CATEGORICAL = {"Engagement status", "Confidence", "Pursuit access", "Window",
                "analyst_confirmed"}


def _col(ref):
    m = re.match(r"^([A-Z]+)\d+$", ref or "")
    return m.group(1) if m else None


def _colnum(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n


def _table_rects(tables):
    """[(c1, r1, c2, r2), ...] for each native table ref - the raw-data ranges where long
    SOURCE text is faithful evidence, not an authored caption."""
    out = []
    for t in tables:
        m = re.match(r"^([A-Z]+)(\d+):([A-Z]+)(\d+)$", t.ref)
        if m:
            out.append((_colnum(m.group(1)), int(m.group(2)),
                        _colnum(m.group(3)), int(m.group(4))))
    return out


def _dv_columns(xml):
    """Column letters covered by any <dataValidation sqref>."""
    cols = set()
    for dv in ET.fromstring(xml).iter(f"{{{NS_SS}}}dataValidation"):
        for rng in (dv.get("sqref") or "").split():
            m = re.match(r"^([A-Z]+)\d+(?::([A-Z]+)\d+)?$", rng)
            if m:
                cols.add(m.group(1))
    return cols


def _lint_sheet(entry, violations):
    tab, group = entry.tab_name, entry.group
    spec = entry.render()
    inv = inspect_worksheet_xml(spec.xml)
    add = lambda code, detail: violations.append((tab, code, detail))

    # column letter -> [data-cell style names] and header value -> column letter
    col_styles, header_col = {}, {}
    for cell in inv["cells"]:
        col = _col(cell["ref"])
        if not col:
            continue
        style = cell["style"]
        if style in _HEADERS and cell.get("value"):
            header_col[cell["value"].strip()] = col
        elif style not in (_TITLE, _SECTION) and style not in _HEADERS:
            col_styles.setdefault(col, []).append(style)

    # TITLE_MISMATCH
    titles = [b for b in inv["banners"] if b["style"] == _TITLE]
    if titles and titles[0]["text"].strip() != tab:
        add("TITLE_MISMATCH", f"{titles[0]['text']!r} != tab {tab!r}")

    # UNNUMBERED_SECTION
    for b in inv["banners"]:
        if b["style"] == _SECTION and not b["text"].lstrip().startswith("§"):
            add("UNNUMBERED_SECTION", b["text"])

    # VISIBLE_TEXT_OVER_180 (authored captions/footers only; raw table data is exempt - long
    # source descriptions are faithful evidence, and the no-wrap rule lets them overflow)
    rects = _table_rects(spec.tables)

    def _in_table(ref):
        m = re.match(r"^([A-Z]+)(\d+)$", ref or "")
        if not m:
            return False
        cc, rr = _colnum(m.group(1)), int(m.group(2))
        return any(c1 <= cc <= c2 and r1 <= rr <= r2 for c1, r1, c2, r2 in rects)

    for cell in inv["cells"]:
        v = cell.get("value")
        if isinstance(v, str) and len(v) > TEXT_LIMIT and not _in_table(cell["ref"]):
            add("VISIBLE_TEXT_OVER_180", f"{cell['ref']} ({len(v)} chars)")

    # COLUMN_WIDTH_OVER_LIMIT
    for c in inv["cols"]:
        w = c.get("width")
        if w and float(w) > WIDTH_LIMIT:
            add("COLUMN_WIDTH_OVER_LIMIT", f"width {w}")

    # PERCENT_HEADER_USING_NUM_STYLE
    for header, col in header_col.items():
        if "%" in header:
            bad = [s for s in col_styles.get(col, []) if s in _NUMERIC_NONPCT]
            if bad:
                add("PERCENT_HEADER_USING_NUM_STYLE", f"{header!r} ({col}) -> {set(bad)}")

    # BLUE_INPUT_OUTSIDE_INPUTS_GROUP (data leaves carry blue SOURCE values - exempt)
    if group not in ("inputs", "data"):
        n = sum(1 for cell in inv["cells"] if cell["style"] in _INPUT)
        if n:
            add("BLUE_INPUT_OUTSIDE_INPUTS_GROUP", f"{n} blue input cell(s)")

    # MODEL_NATIVE_TABLE
    if group == "model" and spec.tables:
        add("MODEL_NATIVE_TABLE", ", ".join(t.name for t in spec.tables))

    # CATEGORICAL_INPUT_WITHOUT_VALIDATION (only when the column is an editable input)
    dv_cols = _dv_columns(spec.xml)
    for header, col in header_col.items():
        if header in _CATEGORICAL and any(s in _INPUT for s in col_styles.get(col, [])):
            if col not in dv_cols:
                add("CATEGORICAL_INPUT_WITHOUT_VALIDATION", f"{header!r} ({col})")


def main():
    violations = []
    for entry in SHEETS:
        _lint_sheet(entry, violations)

    failures, excepted = [], []
    for tab, code, detail in violations:
        (excepted if code in EXCEPTIONS.get(tab, set()) else failures).append(
            (tab, code, detail))

    if excepted:
        print(f"Excepted ({len(excepted)}):")
        for tab, code, detail in excepted:
            print(f"  ~ {tab}: {code} - {detail}")
    if failures:
        print(f"\nSTYLE LINT FAILED - {len(failures)} violation(s):")
        for tab, code, detail in failures:
            print(f"  x {tab}: {code} - {detail}")
        return 1
    print(f"\nSTYLE LINT PASSED ({len(SHEETS)} sheets, {len(excepted)} excepted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
