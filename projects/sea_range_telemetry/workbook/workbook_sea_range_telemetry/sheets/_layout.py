"""_layout - a local row cursor for the sea_range_telemetry sheet modules.

Adapted (copy-from, per the workbook_core "snippets stay copy-from" principle) from
the RowCursor snippet in workbook_core/sheet_snippets.md. It lives inside
workbook_sea_range_telemetry so the shared engine stays untouched; it just composes
the workbook_core primitives (banner_row / write_row / total_row).

A cursor tracks the next row as you append, so blocks compose without off-by-one
math and the 1/1/2 spacing rhythm (sheet_guide.md "Row spacing rhythm") reads as
`c.blank()` / `c.blank(2)`. Every emitting method RETURNS the row it wrote, so a
producer captures load-bearing positions straight from the writing call:

    c = RowCursor(4)
    pos["coeff"] = c.write(["BC coeff", f"={x}"], styles=[S_DEFAULT, S_LINK_PCT])
    ...
    def bc_coeff_cell(): return f"'{TAB}'!C{pos['coeff']}"

This keeps the safety invariant "the accessor row derives from the same value used
to write the row" structural - there is no second literal to drift.

Self-referential formulas (a cell whose formula names its own row, e.g.
`=C{r}+D{r}` or `=1-SUM(E47:E53)`) are written by passing a CALLABLE in the values
list; the cursor calls it with the row it just assigned:

    c.write([name, f"={obs}", 0, lambda r: f"=C{r}+D{r}"], styles=[...])

Content lives in columns B+ (gutter mode); start_col defaults to 1 and banners use
with_gutter=True, matching every sea_range_telemetry sheet.
"""
from __future__ import annotations

from workbook_core.primitives import banner_row, write_row, total_row


def _resolve(values: list, r: int) -> list:
    """Replace any callable in `values` with its result called on the row `r`."""
    return [v(r) if callable(v) else v for v in values]


class RowCursor:
    """Tracks the next row as you append. Start at 2 (row 1 is the gutter blank)."""

    def __init__(self, start: int = 2):
        self.r = start
        self.rows: list[str] = []

    def at(self) -> int:
        """The row the next emit will use."""
        return self.r

    def banner(self, text: str, n_cols: int, *, style: int, **kw) -> int:
        """Emit a full-width banner (gutter mode). Returns its row."""
        r0 = self.r
        self.rows.append(banner_row(r0, text, n_cols=n_cols, style=style,
                                    with_gutter=True, **kw))
        self.r += 1
        return r0

    def write(self, values: list, *, styles, start_col: int = 1, **kw) -> int:
        """Emit one content row. Callable values are resolved against the row.

        Returns the row written.
        """
        r0 = self.r
        self.rows.append(write_row(r0, _resolve(values, r0), styles=styles,
                                   start_col=start_col, **kw))
        self.r += 1
        return r0

    def total(self, values: list, *, styles, n_cols: int, start_col: int = 1,
              **kw) -> int:
        """Emit a total/subtotal divider via total_row(). Pass BASE styles.

        Callable values are resolved against the row. Returns the row written.
        """
        r0 = self.r
        self.rows.append(total_row(r0, _resolve(values, r0), styles=styles,
                                   n_cols=n_cols, start_col=start_col, **kw))
        self.r += 1
        return r0

    def feed(self, rows_xml: list[str], next_row: int) -> None:
        """Splice in pre-built rows (e.g. build_table output) and jump to next_row.

        Use when a helper returns (rows_xml, next_row); the cursor adopts the rows
        and continues from next_row so later positions stay consistent.
        """
        self.rows.extend(r for r in rows_xml if r)
        self.r = next_row

    def blank(self, n: int = 1) -> None:
        """Advance past n blank rows (no cells emitted)."""
        self.r += n
