"""portfolio_summary - the master TAM answer page (summary group).

The one cross-program page: Virginia | Columbia | DDG-51 | Total. Nothing is
hardcoded - every headline is a cross-sheet link into the per-program model tabs
and the ceiling layer.

TAM and the ceiling metrics split cleanly per program. The submarine SAM model
only exposes the Va+Col *combined* broad SAM, so the per-class broad SAM here is
recomputed from the submarine per-class bucket allocation x the broad scenario
flags:  Va_broad = sum_b ClassBucketTAM(va,b) * BroadFlag(b). By construction
Va_broad + Col_broad == the Sub SAM Build portfolio broad SAM; the §3 tie-out
row asserts exactly that so the recompute cannot silently drift.
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

# --- submarine model (already Virginia/Columbia-aware) ---
from workbook_master_tam.sheets.submarines.model_tam_build import (
    cumulative_tam_cell as sub_cum_tam, n_years_cell as sub_n_years,
)
from workbook_master_tam.sheets.submarines.model_sam_build import (
    class_tam_total_cell, class_bucket_tam_cell, sam_cell as sub_sam_cell,
)
from workbook_master_tam.sheets.submarines.inputs_assumptions import scenario_flag_cell
from workbook_master_tam.sheets.submarines.taxonomy import BUCKET_KEYS

# --- DDG model ---
from workbook_master_tam.sheets.ddg.model_tam_build import (
    avg_annual_tam_cell as ddg_avg_tam, portfolio_tam_cell as ddg_cum_tam,
)
from workbook_master_tam.sheets.ddg.model_sam_build import (
    sam_cell as ddg_sam_cell, sam_avg_annual_cell as ddg_avg_sam,
)

# --- ceiling layer (per-program + Portfolio columns) ---
from workbook_master_tam.sheets.ceiling.model_ceiling import (
    core_pct_cell, ceiling_pct_cell, ceiling_dollar_cell,
)
from workbook_master_tam.sheets.ceiling.model_headroom import headroom_mult_cell

_GROUP = "summary"
_TAB = "Portfolio Summary"

NAMES = ["Virginia", "Columbia", "DDG-51", "Total"]
_NCOLS = 1 + len(NAMES)


def _class_broad_sam(ck: str) -> str:
    """Cumulative per-class broad SAM = sum_b ClassBucketTAM(ck,b) * BroadFlag(b).
    Ties out to the Sub SAM Build portfolio broad SAM by construction."""
    terms = [f"{class_bucket_tam_cell(ck, b)}*{scenario_flag_cell('broad', b)}"
             for b in BUCKET_KEYS]
    return "(" + "+".join(terms) + ")"


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Scope
    c.banner("§1 - Scope", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Question", "Outsourced new-construction TAM & SAM across the portfolio"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Programs", "Virginia + Columbia (submarines) and DDG-51; Total = sum"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Window / units", "FY2022-2027 - then-year $M; ceiling ratios unit-invariant"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Per-program detail", "see Sub/DDG TAM Build, SAM Build, Outlook; Ceiling Model/Headroom"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Headline TAM / SAM
    c.banner("§2 - Outsourced TAM & SAM", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure"] + NAMES, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(NAMES))

    _total = lambda r: f"=SUM(C{r}:E{r})"
    # Cumulative TAM (FY22-27): Va, Col per class; DDG portfolio; Total = sum
    c.write(["Outsourced TAM, FY22-27 cumulative $M",
             f"={class_tam_total_cell('va')}", f"={class_tam_total_cell('col')}",
             f"={ddg_cum_tam()}", _total],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 4, outline_level=1)
    # Avg annual TAM = per-class cumulative / submarine n_years; DDG has its own avg
    c.write(["Outsourced TAM, avg annual $M/yr",
             f"={class_tam_total_cell('va')}/{sub_n_years()}",
             f"={class_tam_total_cell('col')}/{sub_n_years()}",
             f"={ddg_avg_tam()}", _total],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 4, outline_level=1)
    # Broad SAM cumulative: Va/Col recomputed per class; DDG portfolio; Total = sum
    c.write(["Broad component-mfg SAM, FY22-27 cumulative $M",
             f"={_class_broad_sam('va')}", f"={_class_broad_sam('col')}",
             f"={ddg_sam_cell('broad')}", _total],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 4, outline_level=1)
    # Broad SAM avg annual
    c.write(["Broad component-mfg SAM, avg annual $M/yr",
             f"={_class_broad_sam('va')}/{sub_n_years()}",
             f"={_class_broad_sam('col')}/{sub_n_years()}",
             f"={ddg_avg_sam('broad')}", _total],
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

    # §4 Tie-outs (the per-class SAM recompute cannot drift)
    c.banner("§4 - Tie-outs", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _va = _class_broad_sam('va')
    _col = _class_broad_sam('col')
    c.write(["Va + Col broad SAM = Sub SAM Build portfolio broad SAM",
             f'=IF(ABS(({_va}+{_col})-{sub_sam_cell("broad")})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Va + Col cumulative TAM = Sub TAM Build portfolio TAM",
             f'=IF(ABS(({class_tam_total_cell("va")}+{class_tam_total_cell("col")})-{sub_cum_tam()})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 13, 13, 13, 13],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


PORTFOLIO_SUMMARY = _make()
