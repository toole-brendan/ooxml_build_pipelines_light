"""input_market_assumptions - the editable market-sizing knobs (the % levers).

The addressable / fit / timing / pursuit / win levers that size the Saronic-addressable
market, gathered on ONE inputs-group tab so the model sheets only LINK to them (green),
never embed editable cells. Mirrors the durable analyst tables - market_assumptions.csv
(addressable / saronic-fit / timing / pursuit / win, per opportunity) merged with
saronic_relevance.csv (mission / platform / autonomy-C2 fit) - keyed by opportunity name.
Market Size reads each knob via INDEX/MATCH on that name. Seeded illustrations until the
analyst pass sources them.

Promoted accessor: market_assumptions_cols(header) -> "'Market Assumptions'!$X$f:$X$l",
keyed on the canonical (machine) column names below.
"""
from __future__ import annotations

from workbook_army.sheets import _flat
from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_MARKET_ASSUMPTIONS
from workbook_army.sheets._analyst import load_analyst_table, value as a_value
from workbook_army.sheets._validate import DV_FRACTION

# Canonical (machine) headers -> the accessor + style keying; display labels humanize them.
_HEADERS = ["opportunity", "addressable_pct", "saronic_fit_pct", "timing_conf",
            "pursuit_access", "win_prob", "mission_fit", "platform_fit",
            "autonomy_c2_fit", "basis_note", "source"]
_LABELS = {
    "opportunity": "Opportunity", "addressable_pct": "Addressable %",
    "saronic_fit_pct": "Saronic fit %", "timing_conf": "Timing conf",
    "pursuit_access": "Pursuit access", "win_prob": "Win prob",
    "mission_fit": "Mission fit", "platform_fit": "Platform fit",
    "autonomy_c2_fit": "Autonomy/C2 fit", "basis_note": "Basis", "source": "Source",
}
# The eight 0-1 levers -> blue italic percent inputs; source -> blue editable text.
_PCT = ["addressable_pct", "saronic_fit_pct", "timing_conf", "pursuit_access",
        "win_prob", "mission_fit", "platform_fit", "autonomy_c2_fit"]
_WIDTHS = [40, 13, 13, 11, 14, 10, 11, 11, 15, 46, 14]
assert len(_WIDTHS) == len(_HEADERS)


def _merged():
    """market_assumptions x saronic_relevance, one row per opportunity (the build feeds this
    to make_flat_sheet via the load_table override below)."""
    opps = load_analyst_table("opportunities", "opportunity_id")
    ma = load_analyst_table("market_assumptions", "opportunity_id")
    sr = load_analyst_table("saronic_relevance", "opportunity_id")
    rows = []
    for oid, m in ma.items():
        rows.append([
            a_value(opps, oid, "name") or oid,
            m.get("addressable_pct", ""), m.get("saronic_fit_pct", ""),
            m.get("timing_conf", ""), m.get("pursuit_access", ""), m.get("win_prob", ""),
            a_value(sr, oid, "mission_fit") or "", a_value(sr, oid, "platform_fit") or "",
            a_value(sr, oid, "autonomy_c2_fit") or "",
            m.get("basis_note", ""), m.get("source", ""),
        ])
    return _HEADERS, rows


_orig = _flat.load_table
_flat.load_table = lambda name: (_merged() if name == "market_assumptions" else _orig(name))
try:
    MARKET_ASSUMPTIONS, market_assumptions_cols = make_flat_sheet(
        tab=TAB_MARKET_ASSUMPTIONS, group="inputs",
        csv_name="market_assumptions", table_name="MarketAssumptions",
        banner="§1 - Market-sizing knobs (per opportunity)",
        intro="Editable levers that size the Saronic-addressable market; Market Size links "
              "to them. Seeded illustrations - replace in the analyst pass.",
        widths=_WIDTHS, header_labels=_LABELS,
        pct_cols=_PCT, input_cols=_PCT + ["source"],
        validations=[(h, DV_FRACTION) for h in _PCT],
    )
finally:
    _flat.load_table = _orig
