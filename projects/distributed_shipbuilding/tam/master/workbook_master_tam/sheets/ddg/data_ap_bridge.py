"""data_ap_bridge - the "AP Bridge" tab (DDG, data group; one module = one sheet).

AP / LLTM / EOQ data support and the TAM-base derivation. The former AP section of
the composite Budget tab, now its own tab - AP/LLTM is a live additive stream in
the DDG TAM bridge, not a footnote. Derives the AP/LLTM stream TAM from the P-10
"Ship Construction EOQ" line (Inputs §3, P-10-cited) x supplier coefficient.

Promoted accessors:
  cy_ap_gross_cell, eoq_gross_cell, cy_ap_inwindow_cell, ap_tam_cell
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_LABEL_INDENT_1, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg.inputs_assumptions import (
    ap_lltm_base_cell as _cp_ap_base,
    ap_gross_then_cell as _cp_ap_gross,
    ap_supplier_coeff_cell as _cp_ap_coeff,
)
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG AP Bridge"
_NCOLS = 11   # label + 10 periods
_LI = 2122
_AP_TOTAL_COL = "L"


def _make_ap_bridge():
    _AP_COLS = [("Prior Years", "Prior"), ("FY 2025", "FY25"), ("FY 2026", "FY26"),
                ("FY 2027 Total", "FY27"), ("FY 2028", "FY28"), ("FY 2029", "FY29"),
                ("FY 2030", "FY30"), ("FY 2031", "FY31"), ("To Complete", "ToCompl"),
                ("Total", "Total")]
    _AP_ROW_LABELS = [
        ("Gross/Weapon System Cost ($ in Millions)",        "Gross / Weapon System Cost"),
        ("Plus CY Advance Procurement ($ in Millions)",     "Plus CY Advance Procurement (AP)"),
        ("Plus EOQ ($ in Millions)",                        "Plus EOQ (Economic Order Qty)"),
        ("Less PY Advance Procurement ($ in Millions)",     "Less PY Advance Procurement"),
        ("Less EOQ ($ in Millions)",                        "Less EOQ"),
        ("Net Procurement (P-1) ($ in Millions)",           "Net Procurement (P-1)"),
        ("Total Obligation Authority ($ in Millions)",      "Total Obligation Authority (TOA)"),
    ]

    def _apnum(x):
        s = (str(x) if x is not None else "").strip().replace(",", "")
        if s in ("", "-"):
            return None
        try:
            return float(s)
        except ValueError:
            return None

    def _ap_load():
        out = {}
        with (EXTRACTED / "scn_li_resource_summary.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                if (r.get("LI") or "").strip() != str(_LI):
                    continue
                out[(r.get("Row Label") or "").strip()] = r
        return out

    _AP = _ap_load()
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Resource summary (AP + EOQ + TOA gross values)
    c.banner("§1 - Resource summary ($M, FY27 PB; P-1/P-10 view)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Row Label"] + [disp for _csv, disp in _AP_COLS],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_AP_COLS))
    pos: dict = {}
    for label, disp in _AP_ROW_LABELS:
        rec = _AP.get(label, {})
        vals = [_apnum(rec.get(csv_col)) for csv_col, _disp in _AP_COLS]
        pos[label] = c.write([disp] + vals,
                             styles=[S_BOLD] + [S_NUM_INPUT] * len(_AP_COLS), outline_level=1)
    c.blank(2)
    _cy_ap_gross_row = pos["Plus CY Advance Procurement ($ in Millions)"]
    _eoq_gross_row = pos["Plus EOQ ($ in Millions)"]

    # §2 TAM-base derivation
    c.banner("§2 - TAM-base derivation",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "Value $M (basis per row)"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _gross = "+".join(f"N({_cp_ap_gross(_LI, fy)})" for fy in range(2022, 2028))
    _cy_inwindow_row = c.write(
        ["CY Advance Procurement gross, in-window (then-year)", f"={_gross}"],
        styles=[S_BOLD, S_NUM], outline_level=1)
    _cy = "+".join(f"N({_cp_ap_base(_LI, fy)})" for fy in range(2022, 2028))
    _ship_base_row = c.write(
        ["of which Ship Construction EOQ = AP/LLTM base (P-10; constant FY2026)", f"={_cy}"],
        styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
    _ap_tam_row = c.total(
        ["x AP/LLTM supplier coeff = AP/LLTM stream TAM", f"=C{_ship_base_row}*{_cp_ap_coeff()}"],
        styles=[S_BOLD, S_NUM], n_cols=2)
    c.blank(2)

    # §3 Line-level classification
    c.banner("§3 - Line-level classification (DDG P-10 structure)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["AP / EOQ line", "TAM treatment", "Rationale"], styles=S_HEADER_LEFT)
    for line, treat, basis in [
        ("Ship Construction EOQ", "INCLUDE", "P-10 EOQ procurements of material items (vendor-purchased); included in full"),
        ("AWS EOQ (Aegis Weapon System)", "EXCLUDE", "GFE-controlled combat system (default out)"),
        ("Other GFE (CBSP / NMT terminals)", "EXCLUDE", "Navy-furnished equipment"),
        ("Congressional adds: shipyard infrastructure / wage enhancements", "EXCLUDE", "FY26 $450.0M + $300.0M; yard capex and wages, not ship material"),
        ("VLS / weapons / ordnance AP", "EXCLUDE", "WPN/OPN appropriation; not SCN ship construction"),
        ("Power Conversion Modules", "IN BC ALREADY", "moved GFE -> Basic Construction in FY23 (no re-add)"),
    ]:
        c.write([line, treat, basis], styles=[S_DEFAULT, S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 Caveats
    c.banner("§4 - Caveats", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    for txt in [
        "AP/LLTM base = the P-10 'Ship Construction EOQ' line per FY (Inputs §3, cited); AWS EOQ, terminal GFE, and congressional adds are excluded at the line level.",
        "No double-count: P-5c BC is net of prior-yr AP, so CY AP is additive (PY-AP-credit in TAM stream bases = 0).",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[40, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def cy_ap_gross_cell() -> str:
        return f"'{_TAB}'!{_AP_TOTAL_COL}{_cy_ap_gross_row}"

    def eoq_gross_cell() -> str:
        return f"'{_TAB}'!{_AP_TOTAL_COL}{_eoq_gross_row}"

    def cy_ap_inwindow_cell() -> str:
        return f"'{_TAB}'!C{_cy_inwindow_row}"

    def ap_tam_cell() -> str:
        return f"'{_TAB}'!C{_ap_tam_row}"

    return (SheetEntry(_TAB, _GROUP, render),
            cy_ap_gross_cell, eoq_gross_cell, cy_ap_inwindow_cell, ap_tam_cell)


(AP_BRIDGE, cy_ap_gross_cell, eoq_gross_cell,
 cy_ap_inwindow_cell, ap_tam_cell) = _make_ap_bridge()
