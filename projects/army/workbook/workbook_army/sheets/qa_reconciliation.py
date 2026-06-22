"""qa_reconciliation - reconciliation + scope QA (live over Contract Families).

The credibility sheet: every figure is a LIVE COUNTIFS / SUMIFS over the Contract Families
leaf, so it re-computes with the data. Surfaces the things a reader must check before
trusting the model - obligation coverage (incl. the negative/partial reconstructions),
parent-IDV hydration, the Army-vs-USACE segment split, and the historical-obligation total
(an evidence lens, never added to budget). Scope = watercraft families with selected
measure >= $1.0M (the radar universe).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_QA
from workbook_army.sheets.data_contract_families import families_cols

_GROUP = "validation"
_TAB = TAB_QA
_NCOLS = 3
_COLS = [52, 16, 60]
_FLOOR = "1000000"

_SEGMENTS = [
    "Army operational watercraft & bridging",
    "Army logistics / prepositioned / floating",
    "Army experimentation / autonomy / sensors / RDT&E",
    "Maintenance, repair & vessel support",
    "USACE floating plant / civil works",
    "Peripheral / excluded maritime",
]
_COVERAGE = ["complete", "partial", "over", "negative", "no-actions", "no-award-$"]


def _make_qa():
    KEY = families_cols("family_key")
    ISW = families_cols("is_watercraft")
    SEL = families_cols("selected_measure")
    COV = families_cols("coverage_status")
    HYD = families_cols("hydrated")
    SEG = families_cols("customer_segment")
    VT = families_cols("vehicle_type")
    AWO = families_cols("award_reported_obligation")
    REC = families_cols("reconstructed_action_sum")

    radar = f'{ISW},"Y",{SEL},">="&{_FLOOR}'      # the radar universe predicate

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Reconciliation + scope QA over Contract Families. Screened universe = "
             "watercraft families with selected measure >= $1.0M."], styles=[S_ITALIC])
    c.blank(2)

    def metric(label, formula, style, note=""):
        c.write([label, formula, note], styles=[S_DEFAULT, style, S_ITALIC])

    c.banner("§1 - Universe + scope", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value", "Note"], styles=header_styles(["Metric", "Value", "Note"]))
    metric("Families in register (all)", f"=COUNTA({KEY})", S_INT, "every contract family")
    metric("Watercraft-relevant families", f'=COUNTIF({ISW},"Y")', S_INT,
           "PSC 19xx / NAICS 33661x / descriptors / primes")
    metric("Screened universe (watercraft, selected >= $1.0M)", f"=COUNTIFS({radar})", S_INT,
           "the decision set")
    metric("IDV vehicles in screened universe", f'=COUNTIFS({radar},{VT},"IDV vehicle")', S_INT)
    metric("  of which hydrated (parent-IDV end resolved)",
           f'=COUNTIFS({radar},{VT},"IDV vehicle",{HYD},"Y")', S_INT,
           "SAM Contract Awards API ordering-period end")

    c.blank(2)
    c.banner("§2 - Obligation coverage (screened universe)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coverage status", "Families", "Meaning"],
            styles=header_styles(["Coverage status", "Families", "Meaning"]))
    _meaning = {"complete": "action sum ties award-reported (selected on action)",
                "partial": "actions under-reconstruct award (selected on award fallback)",
                "over": "actions exceed award-reported",
                "negative": "net deobligations -> negative actions (award fallback)",
                "no-actions": "no per-mod rows reconstructed",
                "no-award-$": "actions exist but award-level obligation is 0"}
    for st in _COVERAGE:
        metric(st, f'=COUNTIFS({radar},{COV},"{st}")', S_INT, _meaning[st])

    c.blank(2)
    c.banner("§3 - Customer segment split (screened universe)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Segment", "Families", ""], styles=header_styles(["Segment", "Families", ""]))
    for seg in _SEGMENTS:
        metric(seg, f'=COUNTIFS({radar},{SEG},"{seg}")', S_INT)

    c.blank(2)
    c.banner("§4 - Historical obligations", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Lens", "$M", "Note"], styles=header_styles(["Lens", "$M", "Note"]))
    metric("Award-reported obligations (screened universe)",
           f"=SUMIFS({AWO},{radar})/1000000", S_NUM, "cumulative award-level lens")
    metric("Reconstructed per-mod actions (screened universe)",
           f"=SUMIFS({REC},{radar})/1000000", S_NUM, "sum-able per-mod lens")
    metric("Army operational watercraft only (award-reported)",
           f'=SUMIFS({AWO},{radar},{SEG},"Army operational watercraft & bridging")/1000000',
           S_NUM, "the Saronic-relevant operational core")
    c.blank()
    c.write(["Historical contract obligations - a separate lens from the budget-funded "
             "market, never added to budget dollars."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


QA_RECONCILIATION = _make_qa()
