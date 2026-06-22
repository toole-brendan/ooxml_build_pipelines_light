"""input_recompete_reviews - the per-family analyst judgment surface (one editable tab).

The recompete reviews an analyst maintains per contract family - confidence, pursuit access,
window override, program / capability node, the planned RFI / solicitation / award milestones,
a capture-lead override and notes - gathered on ONE inputs-group tab (mirrors the durable
recompete_reviews.csv, keyed by family_key). The Timing & Incumbent Screen and the Recompete
Research Queue LINK to these cells (black) instead of embedding editable inputs. Dropdowns +
date / number validation keep entries canonical.

Promoted accessor: recompete_reviews_cols(header) -> "'Recompete Reviews'!$X$f:$X$l",
keyed on the canonical (machine) column names.
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_RECOMPETE_REVIEWS
from workbook_army.sheets._widths import contract_width
from workbook_army.sheets._validate import (
    DV_DATE, DV_WHOLE_NONNEG, dv_list, CONFIDENCE, PURSUIT_ACCESS, WINDOW,
)

# Editable analyst fields (everything but the family key). Dates + the override are typed.
_DATE = ["review_date", "planned_rfi_date", "planned_solicitation_date", "planned_award_date"]
_INT = ["capture_lead_override_days"]
_INPUT = ["window_override", "confidence", "pursuit_access", "program", "capability_node",
          "notes", "milestone_source"] + _DATE + _INT
_LABELS = {
    "family_key": "Family (vehicle PIID)", "window_override": "Window",
    "confidence": "Confidence", "pursuit_access": "Pursuit access", "program": "Program",
    "capability_node": "Capability node", "notes": "Notes", "review_date": "Reviewed",
    "planned_rfi_date": "Planned RFI", "planned_solicitation_date": "Planned solicitation",
    "planned_award_date": "Planned award", "capture_lead_override_days": "Capture lead (days)",
    "milestone_source": "Milestone source",
}
_VALIDATIONS = [
    ("window_override", dv_list(*WINDOW)),
    ("confidence", dv_list(*CONFIDENCE)),
    ("pursuit_access", dv_list(*PURSUIT_ACCESS)),
    ("review_date", DV_DATE), ("planned_rfi_date", DV_DATE),
    ("planned_solicitation_date", DV_DATE), ("planned_award_date", DV_DATE),
    ("capture_lead_override_days", DV_WHOLE_NONNEG),
]

RECOMPETE_REVIEWS, recompete_reviews_cols = make_flat_sheet(
    tab=TAB_RECOMPETE_REVIEWS, group="inputs",
    csv_name="recompete_reviews", table_name="RecompeteReviews",
    banner="§1 - Recompete reviews (per family)",
    intro="Analyst judgment per contract family; the Timing Screen and Research Queue link "
          "to it. Blank until the analyst pass.",
    width_fn=contract_width, header_labels=_LABELS,
    date_cols=_DATE, int_cols=_INT, input_cols=_INPUT, validations=_VALIDATIONS,
)
