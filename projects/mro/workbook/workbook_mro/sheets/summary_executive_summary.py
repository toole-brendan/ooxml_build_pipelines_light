"""Executive Summary

INTENT
    The reader-facing answer page, first in the workbook. It LINKS to producer cells
    (green cross-sheet links) and never recomputes: the headline TAM figures, the
    top-down vs bottom-up reconciliation bridge, and the private-addressable
    convergence. Every $ cell is a pure =accessor() pull into a model producer, so the
    page is a stable summary that follows the model. Nothing imports this module.

LAYOUT
    row 2 : title
    §1 headline TAM · §2 reconciliation bridge · §3 non-public-NSY cross-check
    B..D  : Item, $M, Source
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets.model_reconciliation import (
    reconciled_mro_tam_cell, psc1905_mro_cell, public_shipyard_nwcf_cell,
)
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell
from workbook_mro.sheets.model_tam_bridge import (
    topdown_total_cell, bottomup_total_cell, bridge_gap_cell,
)
from workbook_mro.sheets.model_private_addressable import (
    budget_pot_cell, nonpublic_nsy_crosscheck_cell, crosscheck_delta_cell,
)
from workbook_mro.sheets import taxonomy_mro as tx
from workbook_mro.sheets.model_sam_build import (
    sam_cell, selected_sam_cell, broad_addressable_cell,
)
from workbook_mro.sheets.inputs_assumptions import selected_scenario_cell

_GROUP = "summary"
_TAB = "Executive Summary"
_NCOLS = 3                       # B..D: Item / $M / Source
_COLS = [52, 14, 22]


def _render_executive_summary() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _hdr(first):
        c.write([first, "$M", "Source"],
                styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT], outline_level=1)

    # §1 Headline TAM
    c.banner("§1 - Headline TAM", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _hdr("Item")
    for label, ref, src, bold in [
        ("Reconciled FPDS-visible MRO TAM", reconciled_mro_tam_cell(), "Reconciliation", True),
        ("Navy services-MRO TAM (65 PSCs)", navy_tam_svc_cell(), "Services", False),
        ("USCG services-MRO TAM (65 PSCs)", cg_tam_svc_cell(), "Services", False),
        ("Embedded PSC 1905 MRO", psc1905_mro_cell("EMBEDDED"), "Reconciliation", False),
    ]:
        c.write([label, f"={ref}", src],
                styles=[S_BOLD if bold else S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Reconciliation bridge (top-down budget pot vs bottom-up Reconciled MRO TAM)
    c.banner("§2 - Reconciliation bridge", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    _hdr("Step")
    c.write(["Budget-anchored MRO funding pot (top-down)", f"={topdown_total_cell()}", "TAM Bridge"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Reconciled FPDS-visible MRO TAM (bottom-up)", f"={bottomup_total_cell()}", "TAM Bridge"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["of which Public NSY NWCF (structural, intramural labor)",
             f"={public_shipyard_nwcf_cell()}", "Reconciliation"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Budget pot minus TAM gap", f"={bridge_gap_cell()}", "TAM Bridge"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Non-public-NSY cross-check (a funding-side check, not a market size, not TAM)
    c.banner("§3 - Non-public-NSY cross-check", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    _hdr("Step")
    c.write(["Budget-anchored MRO funding pot", f"={budget_pot_cell()}", "Non-Public-NSY Bridge"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Non-public-NSY funding cross-check (pot less Public NSY)",
             f"={nonpublic_nsy_crosscheck_cell()}", "Non-Public-NSY Bridge"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Reconciled FPDS-visible MRO TAM", f"={bottomup_total_cell()}", "TAM Bridge"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Cross-check delta (~$540M, ~6%)",
             f"={crosscheck_delta_cell()}", "Non-Public-NSY Bridge"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 SAM scenario menu (scenario-selected subsets of TAM atoms; a MENU - never summed)
    c.banner("§4 - SAM scenario menu (subset of TAM atoms; a menu - do NOT sum)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _hdr("Scenario")
    c.write(["Selected SAM scenario", f"={selected_scenario_cell()}", "Inputs"],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Selected SAM", f"={selected_sam_cell()}", "SAM Build"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.write(["Broad Addressable SAM", f"={broad_addressable_cell()}", "SAM Build"],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
    for k in tx.SCENARIO_KEYS:
        c.write([f"  {tx.SCENARIO_NAME[k]}", f"={sam_cell(k)}", "SAM Build"],
                styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


EXECUTIVE_SUMMARY = SheetEntry(_TAB, _GROUP, _render_executive_summary)
