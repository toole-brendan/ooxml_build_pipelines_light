"""Local builders for the Saronic mini-workbook — composed only from workbook_core.

Three things live here:
  - S_ITALIC: a black-italic caption style (workbook_core ships only a gray italic);
    registered once into the style table at import, the same scoping trick the
    distributed-shipbuilding workbook uses.
  - RowCursor: a tiny next-row tracker so a sheet body composes without off-by-one
    math and the 1/1/2 spacing rhythm reads as c.blank() / c.blank(2). Copied-from
    the house RowCursor; trimmed to what this workbook needs.
  - flat_sheet(): turns one extracted/<csv>.csv into a house-styled data tab (row-2
    title banner, §1 section banner, underlined header, native filterable table)
    and returns (SheetEntry, Cols). Cols(header) -> "'Tab'!$C$first:$C$last" so the
    Summary's formulas reference each data tab's columns by NAME, never a hardcoded
    letter.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import (
    col_letter, worksheet, banner_row, write_row,
)
from workbook_core.primitives import row as _blank_row
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NUM, S_INT, S_PCT, S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from .paths import EXTRACTED

# ── S_ITALIC: black-italic caption (font id 5 = italic black; numFmt 0) ─────────
# workbook_core's only italic body font is S_NOTE's gray; the house captions read
# as black italic, so register one once into CELL_XFS (build_styles_xml reads that
# list at build time, so appending at import is enough — same per-process scoping
# the shipbuilding workbook's _italic.py uses).
import workbook_core.styles as _styles
if not getattr(_styles, "_saronic_italic", None):
    _styles._saronic_italic = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        '<xf numFmtId="0" fontId="5" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
    )
S_ITALIC = _styles._saronic_italic


# ── CSV loader (raw strings; per-column casting happens in flat_sheet) ──────────
def load_csv(name: str) -> tuple[list[str], list[list[str]]]:
    """(headers, data_rows) of extracted/<name>.csv as raw strings ('' for blank)."""
    with (EXTRACTED / f"{name}.csv").open(encoding="utf-8-sig", newline="") as fh:
        grid = [list(r) for r in csv.reader(fh)]
    return (grid[0], grid[1:]) if grid else ([], [])


# ── Per-type cast + style ───────────────────────────────────────────────────────
_NUM_STYLE = {"num": S_NUM, "int": S_INT, "pct": S_PCT}


def _cast(raw: str, kind: str, scale: float):
    """Coerce a raw CSV string to its typed value; '' -> None (a real empty cell)."""
    s = (raw or "").strip()
    if s == "":
        return None
    if kind == "text":
        return s
    if kind == "int":
        return int(float(s))
    # num / pct
    return float(s) * scale


class Cols:
    """Column accessor for a flat sheet's DATA region (header row excluded).

    Cols(header) -> "'Tab'!$C$first:$C$last" (the full data range, for SUMIFS /
    COUNTIF). .cell(header,row) / .letter(header) give a single ref / bare letter.
    Keyed by the CSV header name, so a consuming sheet names the column, never a
    letter that could drift.
    """
    __slots__ = ("_tab", "_headers", "first", "last")

    def __init__(self, tab: str, headers: list[str], first: int, last: int):
        self._tab, self._headers, self.first, self.last = tab, headers, first, last

    def letter(self, header: str) -> str:
        return col_letter(self._headers.index(header) + 1)   # +1 for the gutter (A)

    def __call__(self, header: str) -> str:
        c = self.letter(header)
        return f"'{self._tab}'!${c}${self.first}:${c}${self.last}"

    def cell(self, header: str, row: int) -> str:
        return f"'{self._tab}'!${self.letter(header)}${row}"


def flat_sheet(*, tab: str, csv_name: str, table_name: str, banner: str,
               intro: str, columns: list[dict], group: str = "data"):
    """Build one data tab from extracted/<csv_name>.csv.

    columns: ordered list of {csv, show, type, w[, scale]} dicts, where
      type in {text, num, int, pct} and scale (default 1.0) multiplies a numeric
      column (e.g. 1e-6 to render raw dollars as $M). `w` is the column width.

    Returns (SheetEntry, Cols). The cols accessor is built eagerly from the row
    count, so the Summary can import it at module load.
    """
    headers, rows = load_csv(csv_name)
    by_csv = {h: i for i, h in enumerate(headers)}
    show = [c["show"] for c in columns]
    n = len(columns)

    # Row layout: gutter row 1 (worksheet injects it) · row 2 title · row 3 caption
    # · row 4 blank · row 5 §1 banner · row 6 blank · row 7 header · row 8+ data.
    hdr_row = 7
    first, last = hdr_row + 1, hdr_row + len(rows)

    body: list[str] = []
    body.append(banner_row(2, tab, n, style=S_TITLE_SHEET, with_gutter=True))
    body.append(write_row(3, [intro], styles=[S_ITALIC], start_col=1))
    body.append(banner_row(5, banner, n, style=S_TITLE_SECTION, with_gutter=True))
    hdr_styles = [S_HEADER_CENTER if c["type"] != "text" else S_HEADER_LEFT
                  for c in columns]
    body.append(write_row(hdr_row, show, styles=hdr_styles, start_col=1))
    cell_styles = [_NUM_STYLE.get(c["type"], S_DEFAULT) for c in columns]
    for ri, raw in enumerate(rows):
        vals = [_cast(raw[by_csv[c["csv"]]] if by_csv[c["csv"]] < len(raw) else "",
                      c["type"], c.get("scale", 1.0)) for c in columns]
        body.append(write_row(hdr_row + 1 + ri, vals, styles=cell_styles, start_col=1))

    cols_spec = [c["w"] for c in columns]
    table_ref = f"B{hdr_row}:{col_letter(n)}{last}"   # content cols B..; gutter A excluded

    def render() -> WorksheetSpec:
        ws = worksheet(body, cols=cols_spec, tab_color=group_color(group),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name=table_name, ref=table_ref, headers=show)])

    cols = Cols(tab, [c["csv"] for c in columns], first, last)
    return SheetEntry(tab, group, render), cols


# ── RowCursor (trimmed copy of the house cursor) ────────────────────────────────
def _resolve(values: list, r: int) -> list:
    return [v(r) if callable(v) else v for v in values]


class RowCursor:
    """Tracks the next row as you append. Start at 2 (row 1 is the gutter blank)."""

    def __init__(self, start: int = 2):
        self.r = start
        self.rows: list[str] = []

    def banner(self, text: str, n_cols: int, *, style: int) -> int:
        r0 = self.r
        self.rows.append(banner_row(r0, text, n_cols=n_cols, style=style,
                                    with_gutter=True))
        self.r += 1
        return r0

    def title(self, text: str, n_cols: int) -> int:
        return self.banner(text, n_cols, style=S_TITLE_SHEET)

    def section(self, text: str, n_cols: int) -> int:
        return self.banner(text, n_cols, style=S_TITLE_SECTION)

    def caption(self, text: str, *, start_col: int = 1) -> int:
        return self.write([text], styles=[S_ITALIC], start_col=start_col)

    def write(self, values: list, *, styles, start_col: int = 1) -> int:
        r0 = self.r
        self.rows.append(write_row(r0, _resolve(values, r0), styles=styles,
                                   start_col=start_col))
        self.r += 1
        return r0

    def blank(self, n: int = 1) -> None:
        self.r += n
