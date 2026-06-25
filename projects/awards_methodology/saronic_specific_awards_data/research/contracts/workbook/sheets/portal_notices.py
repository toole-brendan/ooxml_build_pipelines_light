"""Portal Notices — the SAM Opportunities notices on hand, categorized (Finding 1).

The 669 maritime notices the portal showed over 12 months, tagged by what is actually
being bought. The Summary's portal-coverage figures (~2% USV, ~65% recurring
sustainment) are COUNTIF off the Subject column. Source: extracted/portal_content.csv
(analyze_opportunities.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "notice_id",            "show": "Notice ID",    "type": "text", "w": 18},
    {"csv": "type",                 "show": "Type",         "type": "text", "w": 14},
    {"csv": "posted",               "show": "Posted",       "type": "text", "w": 12},
    {"csv": "_buyer",               "show": "Buyer",        "type": "text", "w": 13},
    {"csv": "_subject",             "show": "Subject",      "type": "text", "w": 22},
    {"csv": "naics",                "show": "NAICS",        "type": "text", "w": 8},
    {"csv": "psc",                  "show": "PSC",          "type": "text", "w": 7},
    {"csv": "title",                "show": "Title",        "type": "text", "w": 42},
    {"csv": "solicitation_number",  "show": "Solicitation", "type": "text", "w": 18},
]

PORTAL_NOTICES, portal_cols = flat_sheet(
    tab="Portal Notices", csv_name="portal_content", table_name="PortalNotices",
    banner="§1 - SAM Opportunities notices on hand, by subject (Finding 1)",
    intro=("The 669 maritime notices the portal showed, categorized by what is being "
           "bought. Subject usv_autonomy is ~2%; recurring sustainment (ship repair and "
           "parts) is ~65%."),
    columns=_COLUMNS,
)
