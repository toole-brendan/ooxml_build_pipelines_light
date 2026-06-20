"""RowCursor - a local row cursor for the MRO sheet modules.

Copy-from from workbook_core/sheet_snippets.md, kept identical to the DDG/submarines
_layout.py. Content lives in column B+ (gutter mode); the 1/1/2 spacing rhythm
(sheet_guide.md "Row spacing rhythm") reads as c.blank() / c.blank(2).

Every emitting method RETURNS the row it wrote, so a producer captures load-bearing
positions straight from the writing call - there is no second literal to drift:

    pos["coeff"] = c.write(["BC coeff", f"={x}"], styles=[S_DEFAULT, S_LINK_PCT])
    def bc_coeff_cell(): return f"'{TAB}'!C{pos['coeff']}"

Self-referential formulas (a cell whose formula names its own row, e.g. =C{r}+D{r})
are written by passing a CALLABLE in the values list; the cursor calls it with the
row it just assigned.
"""
from __future__ import annotations

from workbook_core.primitives import banner_row, write_row, total_row


def _resolve(values: list, r: int) -> list:
    """Replace any callable in `values` with its result called on the row `r`."""
    return [v(r) if callable(v) else v for v in values]


class RowCursor:
    """Tracks the next row as you append. Start at 2 (row 1 is the gutter blank)."""

    def __init__(self, start: int = 2, outline_default: int = 0):
        self.r = start
        self.rows: list[str] = []
        # When > 0, write()/total() default content rows to this outline level (so a
        # section's rows form a collapsible group under its mark_collapsible banner)
        # unless an explicit outline_level is passed. banner() is unaffected (level 0).
        self.outline_default = outline_default

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
        kw.setdefault("outline_level", self.outline_default)
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
        kw.setdefault("outline_level", self.outline_default)
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
