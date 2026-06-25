"""_tabs - canonical worksheet (tab) names, in one place.

Local non-sheet helper (like _layout / _cuts / _widths). Tab names are
load-bearing: the packager rejects duplicates rather than renaming, and a native
table sits on a named sheet. Centralizing the names here means a rename happens in
exactly one place.

Tab structure (group-contiguous, canonical guide -> model -> data order):
  [guide] Taxonomy · Methodology
  [model] DDG Program Vendors · Virginia Program Vendors · Columbia Program Vendors
  [data]  DDG/Virginia/Columbia Subaward Transactions (the fact spine; each row
          carries its own domestic/foreign flag + country) ·
          Subawardee UEI Index · Subawardee Parents
"""
from __future__ import annotations

TAB_EXEC_SUMMARY     = "Executive Summary"
TAB_TAXONOMY         = "Taxonomy"
TAB_METHODOLOGY      = "Methodology"
TAB_NAICS_MAP        = "Mapping - NAICS Defaults"
TAB_SWBS_CROSSWALK   = "Mapping - HII Code to SWBS"
TAB_DDG_PROGRAM      = "DDG Program Vendors"
TAB_VIRGINIA_PROGRAM = "Virginia Program Vendors"
TAB_COLUMBIA_PROGRAM = "Columbia Program Vendors"
# per-subsystem SWBS roll-up (HII-Ingalls DDG-51 only carries SWBS)
TAB_SWBS_ROLLUP      = "DDG SWBS by Ship-System"
# lifetime capability-domain structure ("observed structure") — size x concentration, live
TAB_DOMAIN_CONC      = "Domain Concentration"
# annual Program x Archetype x FY "where to play" scorecard (over Supplier-Year Activity)
TAB_WHERE_TO_PLAY    = "Where to Play"
# observed reported subawards -> illustrative cumulative co-build scenario (HII co-build add-on)
TAB_MARKET_BRIDGE    = "Market Bridge"
# observed subaward reporting activity per (UEI x prime PIID): reports, action span, $
TAB_SUBAWARD_ACTIVITY = "Subaward Activity"
# raw transaction fact sheets (one row per subaward report id)
TAB_DDG_TX           = "DDG Subaward Transactions"
TAB_VIRGINIA_TX      = "Virginia Subaward Transactions"
TAB_COLUMBIA_TX      = "Columbia Subaward Transactions"
# in-scope prime contracts (USAspending award detail: authoritative prime PoP + obligations)
TAB_PRIME_AWARDS     = "Prime Awards"
# supplier dimension + classification (one row per UEI x program; merges the former
# Subawardee UEI Index + Subawardee Parents into one source)
TAB_SUPPLIER_MASTER  = "Supplier Master"
# annual supplier activity model (one row per Program x UEI x Federal FY; status + concentration)
TAB_SUPPLIER_YEAR    = "Supplier-Year Activity"
# archetype crosswalk (NAICS-6 default) + the hand-researched (Program, UEI) overrides
TAB_ARCHETYPE_OVERRIDES = "Mapping - Vendor Overrides"
# back-of-book price-deflator helper (Green Book Procurement TOA -> constant FY2026$ factor)
TAB_DEFLATORS        = "Deflators"

# All <= 31 chars (Excel sheet-name limit); the packager re-asserts this.
assert all(len(n) <= 31 for n in (
    TAB_EXEC_SUMMARY,
    TAB_TAXONOMY, TAB_METHODOLOGY, TAB_NAICS_MAP, TAB_SWBS_CROSSWALK,
    TAB_DDG_PROGRAM, TAB_VIRGINIA_PROGRAM, TAB_COLUMBIA_PROGRAM, TAB_SWBS_ROLLUP,
    TAB_DOMAIN_CONC, TAB_WHERE_TO_PLAY, TAB_MARKET_BRIDGE,
    TAB_DDG_TX, TAB_VIRGINIA_TX, TAB_COLUMBIA_TX,
    TAB_SUPPLIER_MASTER, TAB_SUPPLIER_YEAR, TAB_ARCHETYPE_OVERRIDES, TAB_DEFLATORS,
    TAB_SUBAWARD_ACTIVITY, TAB_PRIME_AWARDS,
))
