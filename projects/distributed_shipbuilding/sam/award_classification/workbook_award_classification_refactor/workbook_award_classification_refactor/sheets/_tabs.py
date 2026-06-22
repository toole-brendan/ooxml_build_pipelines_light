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
TAB_NAICS_MAP        = "NAICS-6 Archetype Map"
TAB_SWBS_CROSSWALK   = "HII Work-Item SWBS Crosswalk"
# HII-Newport News co-build workshare (issuer-disclosed; excluded from the subaward data)
TAB_HII_CO_BUILD     = "HII Co-Build Workshare"
TAB_DDG_PROGRAM      = "DDG Program Vendors"
TAB_VIRGINIA_PROGRAM = "Virginia Program Vendors"
TAB_COLUMBIA_PROGRAM = "Columbia Program Vendors"
# per-subsystem SWBS roll-up (HII-Ingalls DDG-51 only carries SWBS)
TAB_SWBS_ROLLUP      = "DDG SWBS by Ship-System"
# capability-domain contestability ("where to play") — size x concentration, live
TAB_DOMAIN_CONC      = "Domain Concentration"
# observed reported subawards -> illustrative cumulative co-build scenario (HII co-build add-on)
TAB_MARKET_BRIDGE    = "Market Bridge"
# capability-domain concentration at UEI vs ultimate-parent grain (reviewer finding #6)
TAB_PARENT_CONC      = "Parent Concentration"
# raw transaction fact sheets (one row per subaward report id)
TAB_DDG_TX           = "DDG Subaward Transactions"
TAB_VIRGINIA_TX      = "Virginia Subaward Transactions"
TAB_COLUMBIA_TX      = "Columbia Subaward Transactions"
# supplier dimension + classification (one row per UEI x program; merges the former
# Subawardee UEI Index + Subawardee Parents into one source)
TAB_SUPPLIER_MASTER  = "Supplier Master"
# archetype crosswalk (NAICS-6 default) + the hand-researched (Program, UEI) overrides
TAB_ARCHETYPE_OVERRIDES = "Vendor Archetype Overrides"
# back-of-book price-deflator helper (Green Book Procurement TOA -> constant FY2026$ factor)
TAB_DEFLATORS        = "Deflators"
# semantic-duplicate adjudication: gross vs net-of-candidates by program (reviewer finding #2)
TAB_DUP_AUDIT        = "Duplicate-Report Audit"

# All <= 31 chars (Excel sheet-name limit); the packager re-asserts this.
assert all(len(n) <= 31 for n in (
    TAB_EXEC_SUMMARY,
    TAB_TAXONOMY, TAB_METHODOLOGY, TAB_NAICS_MAP, TAB_SWBS_CROSSWALK, TAB_HII_CO_BUILD,
    TAB_DDG_PROGRAM, TAB_VIRGINIA_PROGRAM, TAB_COLUMBIA_PROGRAM, TAB_SWBS_ROLLUP,
    TAB_DOMAIN_CONC, TAB_MARKET_BRIDGE,
    TAB_DDG_TX, TAB_VIRGINIA_TX, TAB_COLUMBIA_TX,
    TAB_SUPPLIER_MASTER, TAB_ARCHETYPE_OVERRIDES, TAB_DEFLATORS, TAB_DUP_AUDIT,
    TAB_PARENT_CONC,
))
