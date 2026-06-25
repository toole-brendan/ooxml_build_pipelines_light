"""OT Layer — USV-vendor prime awards from SAM Contract Awards, pulled by awardee UEI.

The Finding 2 recovery: one row per award family per vendor, with the OT flag that
separates Other Transactions (where the USV production money lives) from
conventional A-D/IDV awards. Obligated and ceiling are in $M. Source:
extracted/ota_layer.csv (pull_ota_layer.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "vendor",       "show": "Vendor",        "type": "text", "w": 24},
    {"csv": "piid",         "show": "PIID",          "type": "text", "w": 18},
    {"csv": "is_ot",        "show": "OT",            "type": "text", "w": 6},
    {"csv": "award_type",   "show": "Award Type",    "type": "text", "w": 26},
    {"csv": "base_signed",  "show": "Base Signed",   "type": "text", "w": 13},
    {"csv": "last_signed",  "show": "Last Signed",   "type": "text", "w": 13},
    {"csv": "ceiling_$m",   "show": "Ceiling $M",    "type": "num",  "w": 13},
    {"csv": "obligated_$m", "show": "Obligated $M",  "type": "num",  "w": 14},
]

OT_LAYER, ot_cols = flat_sheet(
    tab="OT Layer", csv_name="ota_layer", table_name="OTLayer",
    banner="§1 - USV vendor prime awards, SAM Contract Awards by awardee UEI",
    intro=("One row per award family; obligated and ceiling in $M. OT marks an Other "
           "Transaction, which a standard FPDS pull drops."),
    columns=_COLUMNS,
)
