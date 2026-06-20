"""summary_executive_summary - the "Executive Summary" tab (DDG, summary group).

The reader-facing answer page, first in the workbook. It LINKS to producer cells
(green cross-sheet links) and never recomputes: headline KPIs, the TAM bridge, the
SAM scenario menu, and the bucket allocation (with the unbucketed residual visible).
Nothing imports this module.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets._taxonomy import BUCKETS, BUCKET_KEYS
from workbook_ddg.sheets.model_tam_build import (
    portfolio_tam_cell, avg_annual_tam_cell, portfolio_bc_tam_cell,
    portfolio_ap_tam_cell, bc_supplier_coeff_cell, outside_yards_corrected_cell,
    portfolio_bc_base_cell,
)
from workbook_ddg.sheets.model_sam_build import (
    sam_cell, sam_pct_cell, sam_avg_annual_cell, bucket_tam_cell,
    unbucketed_tam_cell, bucketed_total_cell, scenario_keys_ordered,
)
from workbook_ddg.sheets.data_obbba_funding import obbba_bc_base_cell
from workbook_ddg.sheets.model_outlook import (
    penetration_l6y_cell, outyear_low_avg_cell, outyear_high_avg_cell,
    tam_fy2225_avg_cell,
)
from workbook_ddg.sheets.inputs_scenarios import scenario_name
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "summary"
_TAB = "Executive Summary"
_NCOLS = 5


def _render_executive_summary() -> WorksheetSpec:
    bucket_name = {k: name for k, name, _ in BUCKETS}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Key takeaways
    c.banner("§1 - Key takeaways", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value", "Source"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    kpi_row: dict = {}
    for label, ref, src, note, bold, pct in [
        # Annual headline first; FY22-27 cumulative figures as supporting backup.
        ("Average annual TAM $M/yr", avg_annual_tam_cell(), "TAM Build", "FY22-27 cumulative / fiscal years", True, False),
        ("Average annual broad component SAM $M/yr", sam_avg_annual_cell("broad"), "SAM Build", "broad scenario", True, False),
        ("Portfolio TAM $M", portfolio_tam_cell(), "TAM Build", "FY22-27 cumulative", False, False),
        ("Broad component SAM $M", sam_cell("broad"), "SAM Build", "FY22-27 cumulative; all-buckets", False, False),
        ("BC-stream TAM $M", portfolio_bc_tam_cell(), "TAM Build", "Basic Construction supplier TAM", False, False),
        ("AP/LLTM-stream TAM $M", portfolio_ap_tam_cell(), "TAM Build", "advance-procurement supplier TAM", False, False),
        ("BC supplier coefficient (FY23-27)", bc_supplier_coeff_cell(), "TAM Build", "MYP-corrected (other-US + foreign); FY2022 uses the 22.0% FY18-22-master vintage", False, True),
        ("MYP-corrected outside-yards POP", outside_yards_corrected_cell(), "TAM Build", "~42% (vs ~87% disclosed artifact)", False, True),
        ("Broad component SAM / TAM", sam_pct_cell("broad"), "SAM Build", "share of portfolio TAM", False, True),
        ("Outsourced BC penetration, FY22-27", penetration_l6y_cell(), "Outlook", "sum TAM / sum total ship spend incl. OBBBA", False, True),
        ("Implied outyear Outsourced BC, low $M/yr", outyear_low_avg_cell(), "Outlook", "FY28-31 avg; PB2027 FYDP gross x FY22-25 average penetration", False, False),
        ("Implied outyear Outsourced BC, high $M/yr", outyear_high_avg_cell(), "Outlook", "FY28-31 avg; PB2027 FYDP gross x intent-uplifted FY22-25 penetration", False, False),
        ("FY22-25 average annual TAM $M/yr", tam_fy2225_avg_cell(), "Outlook", "pre-OBBBA reference level", False, False),
    ]:
        link = S_LINK_PCT if pct else S_LINK_NUM
        kpi_row[label] = c.write([label, f"={ref}", src],
                styles=[S_BOLD if bold else S_DEFAULT, link, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 TAM bridge
    c.banner("§2 - TAM bridge", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M / %", "Source"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["BC construction base (FY22-27)", f"={portfolio_bc_base_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["incl. OBBBA mandatory BC, FY26 (Sec. 20002(17), 2 ships)",
             f"={obbba_bc_base_cell(2122, 2026)}", "OBBBA Mandatory"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["x BC supplier coefficient", f"={bc_supplier_coeff_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT], outline_level=1)
    c.write(["= BC-stream TAM", f"={portfolio_bc_tam_cell()}", "TAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["+ AP/LLTM-stream TAM", f"={portfolio_ap_tam_cell()}", "TAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["= Portfolio TAM", f"={portfolio_tam_cell()}", "TAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 SAM scenarios
    c.banner("§3 - SAM scenarios", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "SAM $M", "% of TAM", "Avg annual SAM $M/yr", "Interpretation"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    _interp = {"metal": "structural + castings + machining",
               "hme": "machining + piping + electrical + HVAC",
               "electrical": "electrical power / distribution / generation only",
               "modular": "entity-flagged modular assemblers (registry, not a bucket union)",
               "broad": "all seven buckets"}
    for k in scenario_keys_ordered():
        c.write([scenario_name(k), f"={sam_cell(k)}", f"={sam_pct_cell(k)}", f"={sam_avg_annual_cell(k)}",
                 _interp.get(k, "")],
                styles=[S_DEFAULT, S_LINK_NUM, S_LINK_PCT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 Bucket allocation
    c.banner("§4 - Bucket allocation", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Bucket TAM $M", "Source"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    for k in BUCKET_KEYS:
        c.write([bucket_name[k], f"={bucket_tam_cell(k)}", "SAM Build"],
                styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Unbucketed residual (not in scenario SAM)", f"={unbucketed_tam_cell()}", "SAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.total(["Total (7 buckets + unbucketed = TAM)", f"={bucketed_total_cell()}", "SAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], n_cols=3)
    c.blank(2)

    ws = worksheet(c.rows, cols=[44, 18, 14, 20, 30], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


EXECUTIVE_SUMMARY = SheetEntry(_TAB, _GROUP, _render_executive_summary)
