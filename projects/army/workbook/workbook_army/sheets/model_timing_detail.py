"""model_timing_detail - the provenance companion to the Timing & Incumbent Screen.

The detail columns moved off the narrowed screen (audit #5): relevance basis, PSC/NAICS,
cohort structure, the reconciliation lenses (award-reported vs reconstructed actions +
coverage), the four end-date lenses, lineage candidates, action counts and the anomaly flag.
One row per screened family in the SAME Saronic-first order as the screen (it reuses the
screen's shared selection), so row N lines up between the two sheets. Every analytic column is
the SAME live formula the screen used; nothing is baked.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, cf_rule
from workbook_core.styles import (
    S_BOLD, S_DATE, S_DATE_LINK, S_DEFAULT, S_INT, S_NUM, S_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET, DXF_ANOMALY, DXF_COVERAGE,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_TIMING_DETAIL, AS_OF_CELL
from workbook_army.sheets._radar_formulas import family_formulas
from workbook_army.sheets.model_recompete_radar import (
    SCREENED, SUCC_OF, family_link_builder,
)

_GROUP = "model"
_TAB = TAB_TIMING_DETAIL

_HEADERS = [
    "Family (vehicle PIID)", "Relevance basis", "PSC", "NAICS", "Last competition",
    "Predecessor vehicle", "Successor vehicle",
    "Vehicle type", "Agreement type", "Award structure", "Cohort", "Cohort role",
    "Cohort size", "Task orders",
    "Award-reported $M", "Recon. $M (actions)", "Coverage", "Materiality basis", "Actions",
    "Decision date", "Date basis", "Date confidence",
    "Current end", "Potential end", "Parent/vehicle end", "Latest task-order end",
    "Option headroom (mo)", "Anomaly flag", "Lineage status",
]
_NCOLS = len(_HEADERS)
_COLS = [22, 18, 7, 9, 24, 18, 18,
         13, 15, 16, 22, 18, 11, 11,
         16, 17, 10, 16, 9,
         15, 34, 13,
         13, 13, 15, 16,
         14, 34, 24]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Cohort size", "Task orders", "Award-reported $M", "Recon. $M (actions)",
           "Coverage", "Actions", "Decision date", "Current end", "Potential end",
           "Parent/vehicle end", "Latest task-order end", "Option headroom (mo)"}
_STYLE = {
    "Cohort size": S_INT, "Task orders": S_INT, "Actions": S_INT,
    "Option headroom (mo)": S_INT,
    "Award-reported $M": S_NUM, "Recon. $M (actions)": S_NUM, "Coverage": S_PCT,
    "Decision date": S_DATE_LINK, "Latest task-order end": S_DATE_LINK,
    "Current end": S_DATE, "Potential end": S_DATE, "Parent/vehicle end": S_DATE,
}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}


def _make_detail():
    selected, succ_of = SCREENED, SUCC_OF
    ASOF = AS_OF_CELL                       # the screen's editable C6; detail re-clocks with it

    FB = _CL["Family (vehicle PIID)"]
    DD, PE = _CL["Decision date"], _CL["Potential end"]
    AR, RC = _CL["Award-reported $M"], _CL["Recon. $M (actions)"]
    fam = lambda r: f"${FB}{r}"

    F = family_formulas(fam, ASOF)
    cur_end_f, pot_end_f, parent_end_f = F["cur_end"], F["pot_end"], F["parent_end"]
    vtype_f, tos_f, obl_f, acts_f = F["vtype"], F["tos"], F["obl"], F["acts"]
    obl_award_f = F["obl_award"]
    coverage_f = lambda r: (f'=IF(${AR}{r}=0,"n/a",ROUND(${RC}{r}/${AR}{r},2))')

    _link, _ = family_link_builder(fam)
    decision_f = _link("effective_decision_date")
    latest_to_f = _link("latest_task_order_end")

    head_f = lambda r: (f'=IF(OR(${DD}{r}="",${PE}{r}=""),"",'
                        f'ROUND((${PE}{r}-${DD}{r})/30.44,0))')
    # Lineage status off the (live) decision date: an expired tail with no CONFIRMED successor
    # is "Expired - successor unresolved", not a verdict; a confirmed-superseded row is static.
    status_f = lambda r: (f'=IF(${DD}{r}="","",IF(${DD}{r}<{ASOF},'
                          f'"Expired - successor unresolved","Active"))')

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Provenance for the Timing & Incumbent Screen: reconciliation, end-date lenses, "
             "cohort, lineage and anomalies. Same row order as the screen."],
            styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Timing & reconciliation detail", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    f = hdr + 1
    styles = [_STYLE.get(h, S_DEFAULT) for h in _HEADERS]
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)
    for d in selected:
        lineage = "Superseded" if d["key"] in succ_of else status_f
        c.write([d["key"], d["reason"], d["psc"], d["naics"], d["comp"],
                 d.get("cand_pred"), d.get("cand_succ"),
                 vtype_f, d["agreement_type"], d["award_structure"], d["cohort_id"],
                 d["cohort_role"], d["cohort_size"], tos_f,
                 obl_award_f, obl_f, coverage_f, d["materiality_basis"], acts_f,
                 decision_f, d["date_basis"], d["date_confidence"],
                 cur_end_f, pot_end_f, parent_end_f, latest_to_f,
                 head_f, d["date_anomaly"], lineage],
                styles=styles, outline_level=1)
    last = hdr + len(selected)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    c.blank(2)
    c.write(["Award-reported $M = award-level obligation; Recon. $M (actions) = per-mod sum; "
             "Coverage = Recon / Award-reported."], styles=[S_DEFAULT])
    c.write(["Anomaly flag marks implausible inputs; Lineage status = Superseded only when an "
             "analyst confirms the successor. Historical obligations, not TAM/SAM."],
            styles=[S_DEFAULT])

    CV, AN = _CL["Coverage"], _CL["Anomaly flag"]
    cfmt = [
        cf_rule(f"${AN}${f}:${AN}${last}", DXF_ANOMALY, f'${AN}{f}<>""', priority=1),
        cf_rule(f"${CV}${f}:${CV}${last}", DXF_COVERAGE,
                f'AND(${CV}{f}<>"",${CV}{f}<1)', priority=2),
    ]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, conditional_formatting=cfmt)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="TimingDetail", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


TIMING_DETAIL = _make_detail()
