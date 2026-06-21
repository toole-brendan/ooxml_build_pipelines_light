"""summary_overview - the "Overview" tab (summary group): the answer page.

Nothing hardcoded - every headline is a cross-sheet link into Ceiling Model /
Headroom. Per class and portfolio: core %, structural ceiling % (p=1 upper bound),
the selected pass-through case % (p=50%), ceiling $M, and the headroom multiple
over today's outsourcing.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling.model_ceiling import (
    core_pct_cell, ceiling_pct_cell, ceiling_dollar_cell,
)
from workbook_master_tam.sheets.ceiling.model_bridge import active_share_cell
from workbook_master_tam.sheets.ceiling.model_headroom import headroom_mult_cell

_GROUP = "summary"
_TAB = "Ceiling Overview"

NAMES = ["Virginia", "Columbia", "DDG-51", "Portfolio"]
_NCOLS = 1 + len(NAMES)


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Scope
    c.banner("§1 - Scope", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Question", "Theoretical ceiling on new-construction outsourcing $ "
             "(and the irreducible core)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Programs", "Virginia, Columbia, DDG-51"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Window / units", "FY2022-2027 - then-year $M (P-5c); ratios unit-invariant"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Frame", "POP / distributed leads; make/buy = reference (Headroom)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Headline
    c.banner("§2 - Headline (share of Basic Construction)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure"] + NAMES,
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(NAMES))
    c.write(["Irreducible core %"]
            + [f"={core_pct_cell(n)}" for n in NAMES],
            styles=[S_DEFAULT] + [S_LINK_PCT] * len(NAMES), outline_level=1)
    c.write(["Structural ceiling % (p=1 upper bound)"]
            + [f"={ceiling_pct_cell(n)}" for n in NAMES],
            styles=[S_DEFAULT] + [S_LINK_PCT] * len(NAMES), outline_level=1)
    c.write(["Selected pass-through case % (p=50%)"]
            + [f"={active_share_cell(n)}" for n in NAMES],
            styles=[S_DEFAULT] + [S_LINK_PCT] * len(NAMES), outline_level=1)
    c.write(["Ceiling $M (FY22-27)"]
            + [f"={ceiling_dollar_cell(n)}" for n in NAMES],
            styles=[S_DEFAULT] + [S_LINK_NUM] * len(NAMES), outline_level=1)
    c.write(["Headroom x vs current outsourcing"]
            + [f"={headroom_mult_cell(n)}" for n in NAMES],
            styles=[S_DEFAULT] + [S_LINK_NUM] * len(NAMES), outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[42, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


OVERVIEW = _make()
