"""_flat - shared single-table sheet builder for the flat data/model tabs.

Most tabs are flat tables: a header row + N data rows. They differ only in their
columns, widths, and which columns are numeric / date / derived, so they share one
builder here (one module per tab still declares its own config and calls this). The
result carries the house style: a row-2 title banner (the tab name), a §1 section
banner, an underlined header row, collapsible data rows, sized columns, and a
native filterable Excel table.

Three kinds of column live on these sheets:
  - text (default)  -> raw string (S_DEFAULT); identifiers that merely look numeric
    (Work-type ID "01", CAGE "07482", NAICS "335312") keep their exact string form.
  - hardcoded source -> blue input font. A column named in `input_cols` is a leaf
    SOURCE value: numeric/date -> S_NUM_INPUT / S_INT_INPUT / S_DATE_INPUT; a text
    key (e.g. the Subawardee UEI identity) -> S_TEXT_INPUT (blue text, the one place
    the workbook colors a text cell - see _text_input.py).
  - derived -> a live formula. A column named in `formula_cols` carries a
    `fn(row)->"=..."` callable (resolved per row by the RowCursor) and renders
    black (S_NUM / S_INT / S_DATE) - an aggregation, not a hardcoded value.
    A formula column also named in `link_cols` instead renders GREEN (the
    cross-sheet-link styles S_LINK_INT / S_DATE_LINK): use it for roll-ups that
    surface a value living on another sheet (a count, a min/max date), as opposed
    to a genuinely new aggregate like a SUMIFS total. link_cols applies to numeric
    and date columns only - text columns always render default black.

Column TYPE is declared via int_cols / float_cols / date_cols (controls coercion +
number format). A column with no type is text. `make_flat_sheet` returns
(SheetEntry, cols): `cols(header)` gives the absolute range "'Tab'!$X$f:$X$l" of
that column's data, so a derived sheet's formulas can reference this sheet's leaf
ranges (the data_lane_vendors -> model_by_vendor pattern).
"""
from __future__ import annotations

import re

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_INT_INPUT, S_NUM, S_NUM_INPUT, S_DATE, S_DATE_INPUT,
    S_LINK_INT, S_LINK_NUM, S_DATE_LINK,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_award_classification_refactor.sheets._text_input import S_TEXT_INPUT
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._cuts import (
    load_table, as_int, as_float, cell, date_serial,
)
from workbook_award_classification_refactor.sheets._widths import header_styles

# type key -> (derived/black style, input/blue style, link/green style)
_STYLE_BY_TYPE = {
    "int":   (S_INT, S_INT_INPUT, S_LINK_INT),
    "float": (S_NUM, S_NUM_INPUT, S_LINK_NUM),
    "date":  (S_DATE, S_DATE_INPUT, S_DATE_LINK),
}


def composite_lookup(ret_range: str, key_range: str, second_range: str,
                     second_value: str, key_cell: str, empty: str = "-") -> str:
    """A scalar two-criteria cross-sheet lookup (e.g. Subawardee UEI x Program),
    returned as an OOXML formula string. Implemented with INDEX/MATCH over an
    INDEX-coerced boolean array: ``MATCH(1, INDEX((keys=k)*(2nd=v), 0), 0)`` finds the
    single row matching both criteria, and the outer INDEX returns that row's value.
    The INDEX(...,0) coercion makes the array math evaluate WITHOUT Ctrl+Shift+Enter,
    so the cell stores as an ordinary (non-spilling) formula -- portable to any Excel
    and free of the dynamic-array metadata that would otherwise risk a repair-on-open.

    Yields ``empty`` (default the IB dash "-", per the workbook's zero/blank
    convention) in BOTH degenerate cases: no row matches (IFERROR), or the matched
    dimension cell is itself blank -- without the IF guard, INDEX of an empty cell
    surfaces as 0 in these General-format text columns (Excel's empty-cell-as-zero
    quirk), which is what was rendering missing NAICS codes / parents as "0"."""
    idx = (f'INDEX({ret_range},MATCH(1,INDEX(({key_range}={key_cell})'
           f'*({second_range}="{second_value}"),0),0))')
    return f'=IFERROR(IF({idx}="","{empty}",{idx}),"{empty}")'


def _override_inner(ov_ret: str, ov_key: str, ov_prog: str, prog_value: str,
                    key_cell: str) -> str:
    """The (UEI x Program) override lookup as a bare expression (no leading '='),
    yielding "" when no override row matches - composable inside an IF()."""
    ov = (f'INDEX({ov_ret},MATCH(1,INDEX(({ov_key}={key_cell})'
          f'*({ov_prog}="{prog_value}"),0),0))')
    return f'IFERROR(IF({ov}="","",{ov}),"")'


def override_then_map(ov_ret: str, ov_key: str, ov_prog: str, prog_value: str,
                      key_cell: str, map_ret: str, map_key: str, naics_cell: str,
                      default: str) -> str:
    """Override-first archetype CODE as one OOXML formula:
        IF a (UEI x Program) research override exists -> that code,
        else IF the row's NAICS-6 (naics_cell) is in the crosswalk -> the mapped code,
        else `default` (the unresolved code D0 / P0).
    The override is the same composite (UEI x Program) INDEX/MATCH used for the
    dimension lookups; the crosswalk is a single-key INDEX/MATCH on NAICS-6."""
    ov = _override_inner(ov_ret, ov_key, ov_prog, prog_value, key_cell)
    mp = f'INDEX({map_ret},MATCH({naics_cell},{map_key},0))'
    return f'=IF({ov}<>"",{ov},IFERROR({mp},"{default}"))'


def override_then_map_basis(ov_ret: str, ov_key: str, ov_prog: str, prog_value: str,
                            key_cell: str, map_key: str, naics_cell: str) -> str:
    """The basis-tier label paired with override_then_map: 'Research override' when a
    (UEI x Program) override exists, else 'NAICS-6 map' when the row's NAICS-6 is in the
    crosswalk, else 'Unresolved'."""
    ov = _override_inner(ov_ret, ov_key, ov_prog, prog_value, key_cell)
    mapped = f'ISNUMBER(MATCH({naics_cell},{map_key},0))'
    return (f'=IF({ov}<>"","Research override",'
            f'IF({mapped},"NAICS-6 map","Unresolved"))')


_NOTE_SPLIT = re.compile(r"[\s|;]+")


def _note_text(raw: str) -> str:
    """Normalize a Source-URLs cell into one URL per line for a hover Note.

    The CSV mixes separators (newline, ' | ', '; '), so split on any whitespace /
    pipe / semicolon run, keep the http(s) tokens, and strip trailing punctuation.
    When a cell carries no URL but does hold text (e.g. a 'No reliable public source
    located' annotation), fall back to that text verbatim so the value is not lost
    when the Source-URLs column is dropped. Returns "" only for an empty cell."""
    s = str(raw or "").strip()
    urls = [t.rstrip(".,);") for t in _NOTE_SPLIT.split(s) if t.startswith("http")]
    if urls:
        return "\n".join(urls)
    return " ".join(s.split())


def _note_verbatim(raw: str) -> str:
    """Note text used as-is (internal newlines preserved, ends trimmed) — for a
    pre-composed note like the archetype Basis evidence (reasoning + sources already
    laid out by build_program_vendors). Returns "" for an empty cell."""
    return str(raw or "").strip()


def make_flat_sheet(*, tab: str, group: str, csv_name: str, table_name: str,
                    banner: str, widths: list, intro=None, int_cols=(),
                    float_cols=(), date_cols=(), input_cols=(), formula_cols=None,
                    link_cols=(), note_from=None, note_from_verbatim=None,
                    right_spacer=False):
    """Build a single-table sheet from extracted/<csv_name>.csv.

    Returns (SheetEntry, cols) where cols(header) -> "'Tab'!$Col$first:$Col$last".

    intro: optional italic one-line orientation caption written immediately under
    the row-2 title banner (the Taxonomy-tab house pattern: title banner -> italic
    caption -> two blank rows -> §1 section banner). When omitted the sheet keeps
    the bare title-banner -> one-blank -> banner spacing.

    note_from: optional {anchor_header: source_header} map. Each source column is
    DROPPED from the visible table and its per-row value is normalized (one URL per
    line) into a native Excel Note anchored on the anchor column's cell — used to
    fold a Source-URLs column into hover notes on the prose it supports. Rows whose
    source cell is empty get no note. `widths` must match the columns that REMAIN
    after the source columns are dropped.

    note_from_verbatim: same contract as note_from, but the note text is used
    as-is (newlines preserved, no URL extraction) — for pre-composed evidence notes
    like the archetype Basis reasoning + sources. Source columns named here are also
    dropped; an anchor must not appear in both maps (one Note per cell).

    right_spacer: when True, write a single-space cell in the column immediately
    right of the table on every DATA row (no header, no banner extension, not part
    of the table). It is a fake spacer column whose only job is to clip a long final
    text column (e.g. Role / Description) so its overflow stops instead of running
    on across the empty grid.
    """
    note_from = dict(note_from or {})
    note_from_verbatim = dict(note_from_verbatim or {})
    # (anchor header, source header, mode): URL-normalized vs verbatim note text.
    note_specs = ([(a, s, "url") for a, s in note_from.items()]
                  + [(a, s, "verbatim") for a, s in note_from_verbatim.items()])
    headers, rows = load_table(csv_name)
    # Columns consumed into Notes are dropped from the visible table; capture their
    # original positions first so each row's source value can be read after the drop.
    for anchor, src, _mode in note_specs:
        if anchor not in headers:
            raise ValueError(f"{csv_name}: note anchor column {anchor!r} not found")
        if src not in headers:
            raise ValueError(f"{csv_name}: note source column {src!r} not found")
    drop = {src for _a, src, _m in note_specs}
    src_orig = {src: headers.index(src) for src in drop}
    keep = [j for j, h in enumerate(headers) if h not in drop]
    headers = [headers[j] for j in keep]
    ncols = len(headers)
    if len(widths) != ncols:
        raise ValueError(
            f"{csv_name}: {len(widths)} widths != {ncols} columns ({headers})")
    int_cols, float_cols, date_cols = set(int_cols), set(float_cols), set(date_cols)
    input_cols = set(input_cols)
    link_cols = set(link_cols)
    formula_cols = dict(formula_cols or {})
    numeric = int_cols | float_cols | date_cols   # centered headers

    def _type(h: str):
        if h in int_cols:
            return "int"
        if h in float_cols:
            return "float"
        if h in date_cols:
            return "date"
        return None

    def _style(h: str) -> int:
        t = _type(h)
        if t is None:
            # text: blue when it is a hardcoded source key (input_cols), else black
            return S_TEXT_INPUT if h in input_cols else S_DEFAULT
        derived, inp, link = _STYLE_BY_TYPE[t]
        if h in link_cols:
            return link             # cross-sheet link surfaced green (override)
        if h in formula_cols:
            return derived          # live aggregation -> black
        if h in input_cols:
            return inp              # hardcoded source -> blue
        return derived             # typed leaf without an input flag -> black

    col_styles = [_style(h) for h in headers]

    def convert(j: int, raw: str):
        h = headers[j]
        if h in formula_cols:
            return formula_cols[h]   # callable; RowCursor.write resolves per row
        t = _type(h)
        if t == "int":
            return as_int(raw)
        if t == "float":
            return as_float(raw)
        if t == "date":
            return date_serial(raw)
        return cell(raw)

    # anchor header -> its spreadsheet column letter (gutter at A, so +1)
    anchor_letter = {a: col_letter(headers.index(a) + 1)
                     for a, _s, _m in note_specs}
    notes: list[ExcelNote] = []

    c = RowCursor(2)
    c.banner(tab, n_cols=ncols, style=S_TITLE_SHEET)
    if intro:
        c.write([intro], styles=[S_ITALIC])
        c.blank(2)
    else:
        c.blank()
    c.banner(banner, n_cols=ncols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    # Fake spacer column (one cell right of the table) appended to data rows only -
    # no header cell, so the banner/header still span B..last and the table_ref does
    # not include it.
    spacer_vals = [" "] if right_spacer else []
    spacer_sty = [S_DEFAULT] if right_spacer else []

    hdr = c.write(headers, styles=header_styles(headers, center_headers=numeric))
    for row in rows:
        vals = [convert(j, row[keep[j]] if keep[j] < len(row) else "")
                for j in range(ncols)]
        rownum = c.write(vals + spacer_vals, styles=col_styles + spacer_sty,
                         outline_level=1)
        for anchor, src, mode in note_specs:
            j = src_orig[src]
            raw = row[j] if j < len(row) else ""
            text = _note_verbatim(raw) if mode == "verbatim" else _note_text(raw)
            if text:
                notes.append(
                    ExcelNote(ref=f"{anchor_letter[anchor]}{rownum}", text=text))
    first, last = hdr + 1, hdr + len(rows)
    table_ref = f"B{hdr}:{col_letter(ncols)}{last}"

    def cols(header: str) -> str:
        col = col_letter(headers.index(header) + 1)   # +1 for the gutter (A)
        return f"'{tab}'!${col}${first}:${col}${last}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=widths, tab_color=group_color(group),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name=table_name, ref=table_ref, headers=headers)],
            notes=notes)

    return SheetEntry(tab, group, render), cols
