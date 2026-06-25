"""PoP Timeline — the point-in-time clock history behind the backtest.

The no-look-ahead evidence: for each vehicle in the backtest, the sequence of
distinct FPDS lastDateToOrder values with the date a contract action first recorded
each. Shows the recompete clock was on record years before it closed, and flags the
rows where a later mod EXTENDED it (the date-slip case). Source:
extracted/backtest_pop_timeline.csv (backtest_recompete.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "vehicle_piid",       "show": "Vehicle PIID",       "type": "text", "w": 16},
    {"csv": "role",               "show": "Role",               "type": "text", "w": 12},
    {"csv": "clock_set",          "show": "Clock Recorded",     "type": "text", "w": 14},
    {"csv": "mod",                "show": "Mod",                "type": "text", "w": 22},
    {"csv": "last_date_to_order", "show": "Last Date To Order", "type": "text", "w": 18},
    {"csv": "event",              "show": "Event",              "type": "text", "w": 18},
]

POP_TIMELINE, timeline_cols = flat_sheet(
    tab="PoP Timeline", csv_name="backtest_pop_timeline", table_name="PopTimeline",
    banner="§1 - Ordering-period clock history (point-in-time, per FPDS action)",
    intro=("Each row is a distinct lastDateToOrder value and the date a contract action "
           "first recorded it; the clock was on record years ahead, and a later mod "
           "extending it shows as EXTENDED."),
    columns=_COLUMNS, group="validation",
)
