"""portfolio_summary - the master TAM answer page (summary group).

The one cross-program page: Virginia | Columbia | DDG-51 | Total. Nothing is
hardcoded - every headline links into the per-program TAM model tabs and the
ceiling layer. TAM splits per class (Virginia = LI 2013, Columbia = LI 1045 on
Sub TAM Build, where tam_cell(li, fy) is the all-streams per-class TAM and the
portfolio total is exactly their sum; DDG-51 from DDG TAM Build). The ceiling
metrics come straight from the cross-program ceiling layer. The §4 tie-out
asserts Va + Col cumulative TAM equals the Sub TAM Build portfolio total.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._layout import RowCursor

# submarine TAM (already Virginia/Columbia-aware): per-class TAM via tam_cell(li, fy)
from workbook_master_tam.sheets.submarines.model_tam_build import (
    tam_cell, cumulative_tam_cell as sub_cum_tam, n_years_cell as sub_n_years,
    FY_COLUMNS,
)
# DDG TAM
from workbook_master_tam.sheets.ddg.model_tam_build import (
    avg_annual_tam_cell as ddg_avg_tam, portfolio_tam_cell as ddg_cum_tam,
)
# ceiling layer (per-program + Portfolio columns)
from workbook_master_tam.sheets.ceiling.model_ceiling import (
    core_pct_cell, ceiling_pct_cell, ceiling_dollar_cell,
)
from workbook_master_tam.sheets.ceiling.model_headroom import headroom_mult_cell

_GROUP = "summary"
_TAB = "Portfolio Summary"

NAMES = ["Virginia", "Columbia", "DDG-51", "Total"]
_NCOLS = 1 + len(NAMES)

_VA_LI, _COL_LI = 2013, 1045


def _class_tam_cumul(li):
    """Per-class FY22-27 cumulative TAM (all streams) summed from Sub TAM Build."""
    return "(" + "+".join(f"N({tam_cell(li, fy)})" for fy in FY_COLUMNS) + ")"


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Scope
    c.banner("§1 - Scope", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Question", "Outsourced new-construction TAM across the portfolio"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Programs", "Virginia + Columbia (submarines) and DDG-51; Total = sum"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Window / units", "FY2022-2027 - then-year $M; ceiling ratios unit-invariant"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Per-program detail", "see Sub/DDG TAM Build & Outlook; Ceiling Model / Headroom"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Outsourced TAM
    c.banner("§2 - Outsourced TAM", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure"] + NAMES, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(NAMES))
    _total = lambda r: f"=SUM(C{r}:E{r})"
    c.write(["Outsourced TAM, FY22-27 cumulative $M",
             f"={_class_tam_cumul(_VA_LI)}", f"={_class_tam_cumul(_COL_LI)}",
             f"={ddg_cum_tam()}", _total],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 4, outline_level=1)
    c.write(["Outsourced TAM, avg annual $M/yr",
             f"={_class_tam_cumul(_VA_LI)}/{sub_n_years()}",
             f"={_class_tam_cumul(_COL_LI)}/{sub_n_years()}",
             f"={ddg_avg_tam()}", _total],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 4, outline_level=1)
    c.blank(2)

    # §3 Structural ceiling (from the cross-program ceiling layer)
    c.banner("§3 - Structural outsourcing ceiling (share of Basic Construction)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _C = ["Virginia", "Columbia", "DDG-51", "Portfolio"]   # ceiling's own column keys (Total -> Portfolio)
    c.write(["Measure"] + NAMES, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(NAMES))
    c.write(["Irreducible core %"] + [f"={core_pct_cell(n)}" for n in _C],
            styles=[S_DEFAULT] + [S_LINK_PCT] * len(_C), outline_level=1)
    c.write(["Structural ceiling % (p=1 upper bound)"] + [f"={ceiling_pct_cell(n)}" for n in _C],
            styles=[S_DEFAULT] + [S_LINK_PCT] * len(_C), outline_level=1)
    c.write(["Ceiling $M (FY22-27)"] + [f"={ceiling_dollar_cell(n)}" for n in _C],
            styles=[S_DEFAULT] + [S_LINK_NUM] * len(_C), outline_level=1)
    c.write(["Headroom x vs current outsourcing"] + [f"={headroom_mult_cell(n)}" for n in _C],
            styles=[S_DEFAULT] + [S_LINK_NUM] * len(_C), outline_level=1)
    c.blank(2)

    # §4 Tie-out
    c.banner("§4 - Tie-out", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Va + Col cumulative TAM = Sub TAM Build portfolio TAM",
             f'=IF(ABS(({_class_tam_cumul(_VA_LI)}+{_class_tam_cumul(_COL_LI)})-{sub_cum_tam()})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 13, 13, 13, 13],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


PORTFOLIO_SUMMARY = _make()
