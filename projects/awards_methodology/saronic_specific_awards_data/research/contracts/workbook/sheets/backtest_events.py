"""Backtest Events — the Phase-2 historical replay, one row per recompete pair.

Tests, point-in-time (FPDS lastDateToOrder as known at each freeze, no look-ahead),
whether the radar would have flagged each predecessor->successor recompete at
t-6/12/18 months before the successor award. Event Class separates true turnovers
(predecessor closed around the successor) from parallel vehicles a builder held at
once - the crude hit-rate is dragged down by the latter, which are not recompetes.
Source: extracted/backtest_results.csv (backtest_recompete.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "builder",                  "show": "Builder",            "type": "text", "w": 12},
    {"csv": "predecessor",              "show": "Predecessor",        "type": "text", "w": 15},
    {"csv": "successor",                "show": "Successor",          "type": "text", "w": 15},
    {"csv": "succ_award",               "show": "Succ Award",         "type": "text", "w": 12},
    {"csv": "pred_final_close",          "show": "Pred Close",         "type": "text", "w": 13},
    {"csv": "pred_close_vs_succ_mo",     "show": "Close vs Succ (mo)", "type": "num",  "w": 16},
    {"csv": "event_class",               "show": "Event Class",        "type": "text", "w": 14},
    {"csv": "anticipable_t6",            "show": "t-6",                "type": "text", "w": 6},
    {"csv": "anticipable_t12",           "show": "t-12",               "type": "text", "w": 6},
    {"csv": "anticipable_t18",           "show": "t-18",               "type": "text", "w": 6},
    {"csv": "ldo_known_at_t12",          "show": "Clock Known @ t-12", "type": "text", "w": 17},
    {"csv": "lead_months",               "show": "Lead (mo)",          "type": "num",  "w": 10},
    {"csv": "clock_extended_after_t12",  "show": "Clock Extended",     "type": "text", "w": 13},
]

BACKTEST_EVENTS, bt_cols = flat_sheet(
    tab="Backtest Events", csv_name="backtest_results", table_name="BacktestEvents",
    banner="§1 - Recompete events: would the radar have flagged each, point-in-time?",
    intro=("Each row is a predecessor-successor recompete pair. t-6/12/18 = whether the "
           "predecessor's then-known FPDS clock put it in the 36-month horizon at that "
           "freeze (no look-ahead). Event Class separates true turnovers from parallel "
           "vehicles a builder held at once."),
    columns=_COLUMNS, group="validation",
)
