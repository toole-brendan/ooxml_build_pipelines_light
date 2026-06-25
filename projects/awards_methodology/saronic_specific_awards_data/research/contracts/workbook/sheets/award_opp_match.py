"""Award-Opportunity Match — addressable awards matched to SAM Opportunities notices.

The incompleteness evidence (Metric B): each of the 2,048 addressable awards and
whether a matching notice exists. The Summary's coverage gap (share of in-window
addressable dollars that were dark) is SUMIFS off In Window + Match Level. Obligation
in $M. Source: extracted/award_opp_match.csv (match_awards_to_opps.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "piid",                     "show": "PIID",           "type": "text", "w": 16},
    {"csv": "parent_idv",               "show": "Parent IDV",     "type": "text", "w": 16},
    {"csv": "tier",                     "show": "Tier",           "type": "text", "w": 12},
    {"csv": "recipient",                "show": "Recipient",      "type": "text", "w": 30},
    {"csv": "award_type",               "show": "Award Type",     "type": "text", "w": 22},
    {"csv": "obligation",               "show": "Obligation $M",  "type": "num",  "w": 14, "scale": 1e-6},
    {"csv": "date_signed",              "show": "Date Signed",    "type": "text", "w": 12},
    {"csv": "in_opps_window",           "show": "In Window",      "type": "text", "w": 10},
    {"csv": "solicitation_identifier",  "show": "Solicitation",   "type": "text", "w": 16},
    {"csv": "match_level",              "show": "Match Level",    "type": "text", "w": 12},
    {"csv": "matched_notice_type",      "show": "Matched Notice", "type": "text", "w": 16},
]

AWARD_OPP_MATCH, match_cols = flat_sheet(
    tab="Award-Opportunity Match", csv_name="award_opp_match", table_name="AwardOppMatch",
    banner="§1 - Addressable awards matched to SAM Opportunities notices (incompleteness)",
    intro=("Each addressable award and whether a matching notice exists. In Window flags "
           "the portal's 12-month posting window; Match Level NONE = dark (no notice)."),
    columns=_COLUMNS,
)
