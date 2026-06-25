"""Recompete Radar — vehicles surfaced by the recompete clock, re-based on FPDS.

Mechanism 1: each row is a vehicle, clocked by its ordering-period end. The clock
is the authoritative FPDS field — `lastDateToOrder` for an IDV, `ultimateCompletionDate`
for a standalone — not the Stage-2 max-order-PoP, which ran early or late on 33 of 52
vehicles (see clock_basis / prev_clock). 12 ordering periods have already closed
(overdue, no successor seen). Incumbent, access gate, and the portal notice (all NONE)
follow. Obligated in $M. Source: extracted/recompete_radar.csv
(build_recompete_radar.py, re-clocked by reclock_radar_fpds.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "vehicle_piid",    "show": "Vehicle PIID",   "type": "text", "w": 16},
    {"csv": "tier",            "show": "Tier",           "type": "text", "w": 12},
    {"csv": "vehicle_type",    "show": "Type",           "type": "text", "w": 11},
    {"csv": "incumbent",       "show": "Incumbent",      "type": "text", "w": 30},
    {"csv": "naics",           "show": "NAICS",          "type": "text", "w": 8},
    {"csv": "psc",             "show": "PSC",            "type": "text", "w": 7},
    {"csv": "obligated_$m",    "show": "Obligated $M",   "type": "num",  "w": 13},
    {"csv": "n_orders",        "show": "Orders",         "type": "int",  "w": 8},
    {"csv": "recompete_clock", "show": "Recompete Clock", "type": "text", "w": 14},
    {"csv": "months_to_clock", "show": "Months to Clock", "type": "num",  "w": 13},
    {"csv": "state",           "show": "State",          "type": "text", "w": 34},
    {"csv": "access_gate",     "show": "Access Gate",    "type": "text", "w": 22},
    {"csv": "portal_notice",   "show": "Portal Notice",  "type": "text", "w": 12},
    {"csv": "last_activity",   "show": "Last Activity",  "type": "text", "w": 13},
    {"csv": "clock_basis",     "show": "Clock Basis",    "type": "text", "w": 20},
    {"csv": "prev_clock",      "show": "Prev Clock (S2)", "type": "text", "w": 15},
]

RECOMPETE_RADAR, radar_cols = flat_sheet(
    tab="Recompete Radar", csv_name="recompete_radar", table_name="RecompeteRadar",
    banner="§1 - Vehicles surfaced by the recompete clock (FPDS ordering-period end)",
    intro=("Clock is the FPDS ordering-period end (lastDateToOrder for an IDV, "
           "ultimateCompletionDate for a standalone); an indicator, not a guaranteed "
           "date. Clock Basis and Prev Clock show the re-base off the Stage-2 order-PoP. "
           "Portal Notice is the matching SAM Opportunities notice."),
    columns=_COLUMNS,
)
