"""_validate - canonical dropdown vocabularies + data-validation spec builders.

Centralizes the controlled lists an analyst may enter into the editable (blue) fields, plus
small spec dicts that make_flat_sheet (and the model sheets) turn into worksheet
<dataValidation> blocks via workbook_core.primitives.data_validation. One place to evolve the
vocabularies so every input surface validates the same way.

A spec is just the kwargs for primitives.data_validation MINUS sqref (the sheet builder fills
sqref from the column's data range). Use the DV_* constants or dv_list(...) helper.
"""
from __future__ import annotations

# Fraction / probability (0-1): the market knobs, fits, scores.
DV_FRACTION = dict(kind="decimal", operator="between", formula1="0", formula2="1")
# Any real date (serial >= 1): as-of, deadlines, planned milestones.
DV_DATE = dict(kind="date", operator="greaterThanOrEqual", formula1="1")
# Non-negative whole number: capture-lead override days.
DV_WHOLE_NONNEG = dict(kind="whole", operator="greaterThanOrEqual", formula1="0")


def dv_list(*items: str) -> dict:
    """A dropdown of fixed members (allowBlank stays on, so an empty cell is still legal)."""
    return dict(kind="list", formula1='"' + ",".join(items) + '"')


# Canonical controlled vocabularies (kept small + house-stable).
CONFIRM = ("Y", "N")                                          # analyst_confirmed
ENGAGEMENT = ("Not started", "Identified", "Contacted", "Engaged",
              "Pursuing", "Won", "Lost", "Declined")          # CRM engagement_status
CONFIDENCE = ("High", "Medium", "Low")                        # analyst confidence
PURSUIT_ACCESS = ("Strong", "Moderate", "Limited", "None")    # pursuit access
WINDOW = ("0-12 mo", "12-24 mo", "24-36 mo", "36+ mo", "Expired")  # recompete window override
