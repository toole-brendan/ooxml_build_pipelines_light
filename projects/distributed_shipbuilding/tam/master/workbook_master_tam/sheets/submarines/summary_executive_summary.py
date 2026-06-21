"""summary_executive_summary - the "Executive Summary" tab (one module = one sheet).

The reader-facing answer page, first in the workbook. It LINKS to producer cells
(green cross-sheet links) and never recomputes: the headline KPIs, the
TAM bridge (BC / AP-LLTM / OBBBA mandatory / portfolio), TAM by fiscal year, and
the SAM scenario menu. Imports its producers; nothing imports this module.

Note on styling: the per-stream supplier-TAM totals are FY sums (=N(...)+N(...)+...),
so they are derived black S_NUM, not green links; only one-for-one producer-cell
displays stay green.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT, S_LINK_NUM,
    S_LINK_PCT, S_LABEL_INDENT_1, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines.model_tam_build import (
    cumulative_tam_cell, avg_annual_tam_cell, va_bc_supplier_coeff_cell,
    col_bc_supplier_coeff_cell,
    ap_lltm_supplier_coeff_cell, cumulative_bc_base_cell, tam_bc_total_cell,
    tam_ap_total_cell, tam_obbba_total_cell, tam_total_cell,
    cumulative_obbba_base_cell, cumulative_obbba_tam_cell, FY_COLUMNS,
)
from workbook_master_tam.sheets.submarines.data_obbba_funding import obbba_gross_total_cell
from workbook_master_tam.sheets.submarines.model_outlook import (
    penetration_l6y_cell, outyear_low_avg_cell, outyear_high_avg_cell,
    tam_fy2225_avg_cell,
)
from workbook_master_tam.sheets.submarines.model_sam_build import (
    sam_cell, sam_pct_cell, avg_annual_sam_cell, scenario_keys_ordered,
)
from workbook_master_tam.sheets.submarines.data_ap_bridge import (
    ap_bridge_gross_cell, ap_bridge_gfe_removed_cell, ap_bridge_in_bc_removed_cell,
    ap_bridge_residual_cell, ap_bridge_base_cell,
)
from workbook_master_tam.sheets.submarines.inputs_assumptions import (
    scenario_name, obbba_bc_share_cell, obbba_spillover_cell,
)
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "summary"
_TAB = "Sub Executive Summary"

_bc_tam_sum = "+".join(f"N({tam_bc_total_cell(fy)})" for fy in FY_COLUMNS)
_ap_tam_sum = "+".join(f"N({tam_ap_total_cell(fy)})" for fy in FY_COLUMNS)
_INTERP = {"metal": "structural + castings + machining",
           "hme": "machining + piping + electrical + HVAC",
           "electrical": "electrical power / distribution / generation only",
           "modular": "entity-flagged modular assemblers (registry, not a bucket union)",
           "broad": "all seven buckets"}


def _render_executive_summary() -> WorksheetSpec:
    n_cols = 5
    c = RowCursor(2)
    c.banner("Executive Summary", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 Key takeaways
    c.banner("§1 - Key takeaways", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value", "Source"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    _nr = {}
    for label, val, src, lab in [
        ("Average annual portfolio TAM $M", avg_annual_tam_cell(), "TAM Build", S_BOLD),
        ("FY22-FY27 cumulative portfolio TAM $M", cumulative_tam_cell(), "TAM Build", S_BOLD),
        ("incl. OBBBA mandatory TAM $M (Sec. 20002(16), 1 boat)", cumulative_obbba_tam_cell(), "TAM Build", S_DEFAULT),
        ("Average annual broad SAM $M", avg_annual_sam_cell("broad"), "SAM Build", S_BOLD),
        ("FY22-FY27 cumulative broad SAM $M", sam_cell("broad"), "SAM Build", S_DEFAULT),
    ]:
        _nr[label] = c.write([label, f"={val}", src], styles=[lab, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Virginia BC coefficient (Block V announced POP)", f"={va_bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["Columbia BC coefficient (Build I announced POP)", f"={col_bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    _nr["ap_base"] = c.write(["AP/LLTM additive base $M", f"={ap_bridge_base_cell()}", "AP Bridge"],
                             styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Outsourced BC penetration, FY22-27", f"={penetration_l6y_cell()}", "Outlook"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["Implied outyear Outsourced BC, low $M/yr", f"={outyear_low_avg_cell()}", "Outlook"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Implied outyear Outsourced BC, high $M/yr", f"={outyear_high_avg_cell()}", "Outlook"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["FY22-25 average annual TAM $M/yr", f"={tam_fy2225_avg_cell()}", "Outlook"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 TAM bridge
    c.banner("§2 - TAM bridge", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - BC stream", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M / %", "Source"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["BC construction base (FY22-27)", f"={cumulative_bc_base_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["x Virginia BC coefficient (Block V announced POP)", f"={va_bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["x Columbia BC coefficient (Build I announced POP)", f"={col_bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["BC-stream supplier TAM (per-class coeff x per-class base)", f"={_bc_tam_sum}", "TAM Build"],
            styles=[S_BOLD, S_NUM, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2b - AP/LLTM stream", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M / %", "Source"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["P-10 gross AP top-line", f"={ap_bridge_gross_cell()}", "AP Bridge"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    for label, val in [("less GFE / design / weapons", ap_bridge_gfe_removed_cell()),
                       ("less already inside P-5c BC", ap_bridge_in_bc_removed_cell()),
                       ("less un-itemized overlap", ap_bridge_residual_cell())]:
        c.write([label, f"={val}", "AP Bridge"], styles=[S_LABEL_INDENT_1, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["AP/LLTM additive base", f"={ap_bridge_base_cell()}", "AP Bridge"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["AP/LLTM reference coefficient", f"={ap_lltm_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["AP/LLTM-stream supplier TAM", f"={_ap_tam_sum}", "TAM Build"],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2c - OBBBA mandatory (Sec. 20002(16))", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M / %", "Source"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["Gross award (Sec. 20002(16), 2nd FY26 Virginia boat)", f"={obbba_gross_total_cell()}", "OBBBA Mandatory"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["OBBBA BC share of award", f"={obbba_bc_share_cell()}", "Assumptions"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["OBBBA mandatory BC base (FY22-27)", f"={cumulative_obbba_base_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["x Virginia BC coefficient (the OBBBA boat is a Virginia)", f"={va_bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["OBBBA mandatory supplier TAM", f"={cumulative_obbba_tam_cell()}", "TAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["FY2027 execution spillover assumption", f"={obbba_spillover_cell()}", "Assumptions"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2d - Portfolio TAM", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M", "Source"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["BC-stream supplier TAM", f"={_bc_tam_sum}", "TAM Build"],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    c.write(["AP/LLTM-stream supplier TAM", f"={_ap_tam_sum}", "TAM Build"],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    c.write(["OBBBA mandatory supplier TAM", f"={cumulative_obbba_tam_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Total portfolio TAM", f"={cumulative_tam_cell()}", "TAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 TAM by fiscal year
    c.banner("§3 - TAM by fiscal year", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Fiscal year", "BC-stream TAM $M", "AP/LLTM-stream TAM $M", "OBBBA mandatory TAM $M", "Portfolio TAM $M"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    for fy in FY_COLUMNS:
        c.write([f"FY{fy}", f"={tam_bc_total_cell(fy)}", f"={tam_ap_total_cell(fy)}",
                 f"={tam_obbba_total_cell(fy)}", f"={tam_total_cell(fy)}"],
                styles=[S_DEFAULT, S_LINK_NUM, S_LINK_NUM, S_LINK_NUM, S_LINK_NUM], outline_level=1)
    c.total(["Total (FY22-27)", f"={_bc_tam_sum}", f"={_ap_tam_sum}",
             f"={cumulative_obbba_tam_cell()}", f"={cumulative_tam_cell()}"],
            styles=[S_BOLD, S_NUM, S_NUM, S_LINK_NUM, S_LINK_NUM], n_cols=5)
    c.blank(2)

    # §4 SAM scenario menu
    c.banner("§4 - SAM scenario menu", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "Cumulative SAM $M", "% of TAM", "Avg annual SAM $M", "Interpretation"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    for k in scenario_keys_ordered():
        c.write([scenario_name(k), f"={sam_cell(k)}", f"={sam_pct_cell(k)}", f"={avg_annual_sam_cell(k)}",
                 _INTERP.get(k, "")],
                styles=[S_DEFAULT, S_LINK_NUM, S_LINK_PCT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    ws = worksheet(c.rows, cols=[40, 18, 18, 18, 30], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


EXECUTIVE_SUMMARY = SheetEntry(_TAB, _GROUP, _render_executive_summary)
