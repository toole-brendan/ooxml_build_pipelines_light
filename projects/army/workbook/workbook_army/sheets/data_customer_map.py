"""data_customer_map - the customer / acquisition relationship GRAPH (analyst).

The Army autonomous-surface-logistics stakeholder landscape behind the evidence chain
(operational user -> requirement / experimentation -> program / acquisition -> contracting),
from the durable analyst/customer_org_map.csv. Wired as a graph via parent_org_id, with each
org's decision rights, current nomenclature, acquisition pathways (FAR/OTA/CSO/prototype/
experiment), geography and the opportunity ids it touches. Editable analyst reference
(seeded), not mined facts - so the org fields render as blue text inputs.

One DERIVED column is appended (live, not stored): "Screened vehicles at office" = a COUNTIFS
over Contract Families keyed on contracting_office AND filtered to the screened universe
(is_watercraft="Y" and selected_measure >= the $1M floor) - the live join from the org layer
to the fact layer, so an acquisition office shows how many SCREENED vehicles it owns (the
same universe as the Timing & Incumbent Screen, not the full 1,688-row register).

Promoted accessor: customer_map_cols(header) -> "'Customer Map'!$X$first:$X$last".
"""
from __future__ import annotations

import csv

from workbook_core.primitives import col_letter
from workbook_army.sheets import _flat
from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_CUSTOMER_MAP
from workbook_army.sheets._widths import contract_width
from workbook_army.sheets._analyst import ANALYST_DIR
from workbook_army.sheets.data_contract_families import families_cols
from workbook_army.sheets._validate import DV_DATE, dv_list, ENGAGEMENT
from workbook_army.sheets import config as CFG

# The analyst tables live in workbook/analyst/, not workbook/extracted/. Temporarily point
# the flat builder's loader (bound in _flat's namespace) at the analyst copy for this sheet.
_orig = _flat.load_table


def _load_analyst_csv(name):
    with open(ANALYST_DIR / f"{name}.csv", newline="") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


# contracting_office column letter (gutter +1) for the derived COUNTIFS, computed from the
# analyst CSV header order so it tracks any reordering; the derived column is appended AFTER
# it, so this index holds. families_cols joins the org layer to the canonical fact layer.
_OH, _ = _load_analyst_csv("customer_org_map")
_OFF = col_letter(_OH.index("contracting_office") + 1)
_FAM_OFFICE = families_cols("contracting_office")
# Count only the SCREENED universe (watercraft AND selected_measure >= the $1M materiality
# floor), NOT all 1,688 register families - the register includes sub-floor / non-watercraft
# rows, so an unqualified COUNTIFS overstated the office's footprint (audit #5c).
_FAM_WC = families_cols("is_watercraft")
_FAM_SEL = families_cols("selected_measure")
_FLOOR = int(CFG.MIN_OBLIG)
_vehicles_fn = lambda r: (f'=IF(${_OFF}{r}="","",'
                          f'COUNTIFS({_FAM_OFFICE},${_OFF}{r},'
                          f'{_FAM_WC},"Y",{_FAM_SEL},">="&{_FLOOR}))')

# Blue = ONLY the fields an analyst actively maintains (the CRM layer): owner, status,
# next action, as-of, notes, and the opportunity attribution. Organization identity, command
# structure, geography, decision rights, pathways and source are reference facts -> black, so
# the eye separates "maintain this" from "read this" (audit #7).
_INPUT = ["associated_opportunity_ids", "saronic_relationship_owner",
          "engagement_status", "next_action", "as_of", "notes"]
# Humanize the machine column names for this input/decision tab (audit #7).
_LABELS = {
    "org_id": "Org ID", "parent_org_id": "Parent org", "name": "Organization",
    "current_official_name": "Current official name", "role": "Role",
    "decision_rights": "Decision rights", "command": "Command", "echelon": "Echelon",
    "portfolio_program": "Portfolio / program", "associated_opportunity_ids": "Opportunities",
    "customer_segment": "Customer segment", "geography": "Geography",
    "contracting_office": "Contracting office", "available_pathways": "Pathways",
    "saronic_relationship_owner": "Relationship owner", "engagement_status": "Engagement status",
    "next_action": "Next action", "as_of": "As-of", "notes": "Notes", "source": "Source",
}

_flat.load_table = lambda name: (_load_analyst_csv(name) if name == "customer_org_map"
                                 else _orig(name))
try:
    CUSTOMER_MAP, customer_map_cols = make_flat_sheet(
        tab=TAB_CUSTOMER_MAP, group="inputs",
        csv_name="customer_org_map", table_name="CustomerMap",
        banner="§1 - Customer / acquisition relationship map",
        intro="Army autonomous-surface-vessel stakeholders: operational user -> requirement "
              "-> program / acquisition -> contracting, with each office's screened vehicles.",
        width_fn=contract_width, header_labels=_LABELS,
        date_cols=["as_of"], input_cols=_INPUT,
        validations=[("engagement_status", dv_list(*ENGAGEMENT)), ("as_of", DV_DATE)],
        derived_cols=[("Screened vehicles at office (wc >= $1M)", "int", _vehicles_fn)],
    )
finally:
    _flat.load_table = _orig
