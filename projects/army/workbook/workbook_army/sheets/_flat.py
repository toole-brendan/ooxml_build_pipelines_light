"""_flat - shared single-table sheet builder for the flat raw-data tabs.

Most data tabs are flat tables: a header row + N data rows. They differ only in their
columns, widths, and which columns are numeric / date, so they share one builder here
(one module per tab still declares its own config and calls this). The result carries
the house style: a row-2 title banner (the tab name), an optional italic intro
caption, a §1 section banner, an underlined header row, collapsible data rows, sized
columns, and a native filterable Excel table.

Copy-from workbook_award_classification_refactor/sheets/_flat.py, trimmed to the
generic builder (the archetype-specific INDEX/MATCH override helpers were dropped) and
given a `width_fn` so a raw pull can auto-size every column from its header instead of
a hand-counted widths list.

Three kinds of column live on these sheets:
  - text (default)  -> raw string (S_DEFAULT); identifiers that merely look numeric
    (PSC "1940", NAICS "336611", a TAS "021-2035") keep their exact string form.
  - hardcoded source -> blue input font. A column named in `input_cols` is a leaf
    SOURCE value: numeric/date -> S_NUM_INPUT / S_INT_INPUT / S_DATE_INPUT; a text key
    -> S_TEXT_INPUT (blue text, the one place the workbook colors a text cell).
  - derived -> a live formula. A column named in `formula_cols` carries a
    `fn(row)->"=..."` callable (resolved per row by the RowCursor) and renders black
    (S_NUM / S_INT / S_DATE) - an aggregation, not a hardcoded value. A formula column
    also named in `link_cols` instead renders GREEN (cross-sheet-link styles): use it
    for roll-ups that surface a value living on another sheet.

Column TYPE is declared via int_cols / float_cols / date_cols / pct_cols (controls
coercion + number format). A pct column is a fraction (0-1) coerced like a float but
rendered with the italic percent styles (S_PCT / S_PCT_INPUT / S_LINK_PCT) so a stored
0.85 reads "85.0%". A column with no type is text. `make_flat_sheet` returns
(SheetEntry, cols): `cols(header)` gives the absolute range "'Tab'!$X$f:$X$l" of that
column's data, so a derived sheet's live formulas can reference this sheet's leaf
ranges (the data-leaf -> model pattern; here, the future recompete radar).
"""
from __future__ import annotations

import re

from workbook_core.primitives import col_letter, worksheet, data_validation
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_INT_INPUT, S_NUM, S_NUM_INPUT, S_DATE, S_DATE_INPUT,
    S_LINK_INT, S_LINK_NUM, S_DATE_LINK, S_PCT, S_PCT_INPUT, S_LINK_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_army.sheets._text_input import S_TEXT_INPUT
from workbook_army.sheets._italic import S_ITALIC
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import (
    load_table, as_int, as_float, cell, date_serial,
)
from workbook_army.sheets._widths import header_styles

# type key -> (derived/black style, input/blue style, link/green style)
_STYLE_BY_TYPE = {
    "int":   (S_INT, S_INT_INPUT, S_LINK_INT),
    "float": (S_NUM, S_NUM_INPUT, S_LINK_NUM),
    "date":  (S_DATE, S_DATE_INPUT, S_DATE_LINK),
}

_NOTE_SPLIT = re.compile(r"[\s|;]+")


def _note_text(raw: str) -> str:
    """Normalize a Source-URLs cell into one URL per line for a hover Note.

    The CSV mixes separators (newline, ' | ', '; '), so split on any whitespace /
    pipe / semicolon run, keep the http(s) tokens, and strip trailing punctuation.
    When a cell carries no URL but does hold text, fall back to that text verbatim so
    the value is not lost. Returns "" only for an empty cell."""
    s = str(raw or "").strip()
    urls = [t.rstrip(".,);") for t in _NOTE_SPLIT.split(s) if t.startswith("http")]
    if urls:
        return "\n".join(urls)
    return " ".join(s.split())


def _note_verbatim(raw: str) -> str:
    """Note text used as-is (internal newlines preserved, ends trimmed)."""
    return str(raw or "").strip()


def make_flat_sheet(*, tab: str, group: str, csv_name: str, table_name: str,
                    banner: str, widths=None, width_fn=None, intro=None,
                    int_cols=(), float_cols=(), date_cols=(), pct_cols=(),
                    input_cols=(),
                    formula_cols=None, link_cols=(), note_from=None,
                    note_from_verbatim=None, right_spacer=False, derived_cols=None,
                    header_labels=None, validations=()):
    """Build a single-table sheet from extracted/<csv_name>.csv.

    Returns (SheetEntry, cols) where cols(header) -> "'Tab'!$Col$first:$Col$last".

    widths: per-column character widths (len == kept column count). Omit and pass
    `width_fn` instead to auto-size every column from its header name.

    intro: optional italic one-line orientation caption written immediately under the
    row-2 title banner (title banner -> italic caption -> two blank rows -> §1 banner).
    When omitted the sheet keeps the bare title-banner -> one-blank -> banner spacing.

    note_from / note_from_verbatim: optional {anchor_header: source_header} maps; each
    source column is DROPPED from the visible table and folded into a native Excel Note
    anchored on the anchor column's cell (URL-normalized vs verbatim). `widths` (if
    given) must match the columns that REMAIN after the source columns are dropped.

    right_spacer: when True, write a single-space cell one column right of the table on
    every DATA row (no header, not part of the table) to clip a long final text column
    so its overflow stops instead of running on across the empty grid.

    derived_cols: optional [(header, type, fn), ...] of SYNTHETIC columns appended after
    the CSV columns. They have no CSV source - each `fn(row)->"=..."` callable is a live
    formula (resolved per row by the RowCursor), `type` is None (text) / "int" / "float"
    / "date" (controls number format + centering). Use for a derived status column that
    keys off another cell on the row (e.g. a deadline vs the As-of date).

    header_labels: optional {csv_header: display label} map. The CSV/machine column name
    stays the lookup key (int_cols/input_cols/cols(...) all key off it) but the VISIBLE
    header + table column name use the label - so an input/decision tab can read "Org ID"
    while the data stays keyed on "org_id". Raw evidence tabs omit it and keep machine names.
    """
    note_from = dict(note_from or {})
    note_from_verbatim = dict(note_from_verbatim or {})
    derived_cols = list(derived_cols or [])
    note_specs = ([(a, s, "url") for a, s in note_from.items()]
                  + [(a, s, "verbatim") for a, s in note_from_verbatim.items()])
    headers, rows = load_table(csv_name)
    for anchor, src, _mode in note_specs:
        if anchor not in headers:
            raise ValueError(f"{csv_name}: note anchor column {anchor!r} not found")
        if src not in headers:
            raise ValueError(f"{csv_name}: note source column {src!r} not found")
    drop = {src for _a, src, _m in note_specs}
    src_orig = {src: headers.index(src) for src in drop}
    keep = [j for j, h in enumerate(headers) if h not in drop]
    headers = [headers[j] for j in keep]
    base_ncols = len(headers)                      # CSV-sourced columns
    headers = headers + [d[0] for d in derived_cols]
    ncols = len(headers)
    if widths is None:
        if width_fn is None:
            raise ValueError(f"{csv_name}: provide widths or width_fn")
        widths = [width_fn(h) for h in headers]
    if len(widths) != ncols:
        raise ValueError(
            f"{csv_name}: {len(widths)} widths != {ncols} columns ({headers})")
    int_cols, float_cols, date_cols = set(int_cols), set(float_cols), set(date_cols)
    pct_cols = set(pct_cols)
    float_cols |= pct_cols            # pct coerces + centers like a float; styled as percent
    input_cols = set(input_cols)
    link_cols = set(link_cols)
    header_labels = dict(header_labels or {})
    formula_cols = dict(formula_cols or {})
    for _h, _t, _fn in derived_cols:               # register synthetic formula columns
        formula_cols[_h] = _fn
        (int_cols if _t == "int" else float_cols if _t == "float"
         else date_cols if _t == "date" else set()).add(_h)
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
        if h in pct_cols:
            # fraction rendered as a percent: green link / blue input / black derived
            if h in link_cols:
                return S_LINK_PCT
            if h in input_cols and h not in formula_cols:
                return S_PCT_INPUT
            return S_PCT
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
    # Visible header labels (display only); all keying stays on the canonical CSV names.
    display_headers = [header_labels.get(h, h) for h in headers]

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
    spacer_vals = [" "] if right_spacer else []
    spacer_sty = [S_DEFAULT] if right_spacer else []

    hdr = c.write(display_headers, styles=header_styles(headers, center_headers=numeric))
    for row in rows:
        vals = [convert(j, row[keep[j]] if (j < base_ncols and keep[j] < len(row))
                        else "")
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
        # Per-column data validations (sqref = the column's local data range B..last).
        def _local(h: str) -> str:
            cl = col_letter(headers.index(h) + 1)
            return f"{cl}{first}:{cl}{last}"
        dvs = [data_validation(_local(h), **spec) for h, spec in validations] or None
        ws = worksheet(c.rows, cols=widths, tab_color=group_color(group),
                       with_gutter=True, data_validations=dvs)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name=table_name, ref=table_ref, headers=display_headers)],
            notes=notes)

    return SheetEntry(tab, group, render), cols
