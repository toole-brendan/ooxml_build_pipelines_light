"""ddg_program_vendors - the refactored DDG-51 program-vendor sheet (trial).

One row per distinct subawardee UEI on the DDG-51 program across all corpus years,
entity-grain (NOT parent-collapsed). The row is almost entirely LIVE formulas; the
only hardcoded leaf cells are the Subawardee UEI key, the four archetype columns
(Capability Domain / Primary Output + their bases, assigned later) and the prose
(Role / Description + Source URLs). Built from extracted/ddg_program_vendors.csv
(scripts/build_program_vendors.py) via the shared flat-table builder.

Two formula families, both keyed on the row's Subawardee UEI (column B):
  - roll-ups over the DDG Subaward Transactions leaf: Subaward $M (SUMIFS), Subaward
    Actions (COUNTIFS), First / Last Subaward (MINIFS / MAXIFS), Domestic or Foreign
    (a foreign-majority IF over the raw Country Code).
  - attribute lookups over the per-UEI dimension sheets (composite key UEI x Program,
    via INDEX/MATCH): Subawardee Vendor Name + Primary NAICS-6 + NAICS-6 Description
    from the Subawardee UEI Index, and the standardized Parent UEI + Parent Vendor
    Name from Subawardee Parents.
This sheet therefore sits in the `model` group (a derived cut over the `data`
transaction spine + dimensions), mirroring award_analysis's model_by_vendor.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import (
    make_flat_sheet, composite_lookup, override_then_map, override_then_map_basis,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_DDG_PROGRAM
from workbook_award_classification_refactor.sheets.ddg_subaward_transactions import (
    ddg_tx_cols,
)
from workbook_award_classification_refactor.sheets.subawardee_uei_index import (
    uei_index_cols,
)
from workbook_award_classification_refactor.sheets.subawardee_parents import (
    parents_cols,
)
from workbook_award_classification_refactor.sheets.naics6_archetype_map import (
    naics_map_cols,
)
from workbook_award_classification_refactor.sheets.vendor_archetype_overrides import (
    overrides_cols,
)
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_NAICS, W_NAICS_DESC, W_VENDOR, W_DOMFOR, W_DOLLAR, W_COUNT,
    W_CONF, W_TEXT_WIDE,
)

# Subawardee UEI | NAICS-6 | NAICS-6 desc | Parent UEI | Parent name | Subawardee name |
# Dom/For | $M | Actions | First | Last | D | D basis | P | P basis | Role
# (Source URLs is folded into hover Notes on Role / Description, not a column.)
_WIDTHS = [W_UEI, W_NAICS, W_NAICS_DESC, W_UEI, W_VENDOR, W_VENDOR, W_DOMFOR,
           W_DOLLAR, W_COUNT, W_CONF, W_CONF, W_CONF, W_DOMFOR, W_CONF, W_DOMFOR,
           W_TEXT_WIDE]

# Live roll-ups over the DDG Subaward Transactions leaf, keyed on Subawardee UEI
# (this sheet's column B). $M sums the raw Subaward Amount ($) and /1e6 to millions;
# each subaward record is one distinct report id, so COUNTIFS == the distinct action
# count; dates are real serials, so MINIFS/MAXIFS give the first/last subaward;
# Domestic or Foreign is the foreign-majority of that UEI's raw Country Code
# (is_foreign: code not USA/blank; ties -> Domestic, matching the prior value).
# --- live roll-ups over the DDG tx leaf (this sheet's $/count/date columns) ---
_UEI = ddg_tx_cols("Subawardee UEI")
_DOL = ddg_tx_cols("Subaward Amount $")
_DATE = ddg_tx_cols("Subaward Date")
_CC = ddg_tx_cols("Country Code")

# --- entity attributes pulled from the dimension sheets (composite key UEI x Program;
# this sheet is DDG, so the second criterion is the literal program label) ---
_LABEL = "DDG"
_IX_UEI, _IX_PROG = uei_index_cols("Subawardee UEI"), uei_index_cols("Program")
_IX_NAME = uei_index_cols("Subawardee Vendor Name")
_IX_CODE = uei_index_cols("Primary NAICS-6")
_IX_DESC = uei_index_cols("NAICS-6 Description")
_PA_UEI, _PA_PROG = parents_cols("Subawardee UEI"), parents_cols("Program")
_PA_PUEI = parents_cols("Parent UEI")
_PA_PNAME = parents_cols("Parent Vendor Name")

# --- archetype resolution: (UEI x Program) override first, then the NAICS-6 crosswalk
# default, then unresolved. The row's resolved NAICS-6 (Primary) is column C. ---
_NAICS_COL = "C"
_MAP_NAICS = naics_map_cols("NAICS-6")
_MAP_D = naics_map_cols("Capability Domain (D)")
_MAP_P = naics_map_cols("Primary Output (P)")
_OV_UEI, _OV_PROG = overrides_cols("Subawardee UEI"), overrides_cols("Program")
_OV_D = overrides_cols("Capability Domain (D)")
_OV_P = overrides_cols("Primary Output (P)")


def _dim(ret, key_range, prog_range):
    """Bind a composite (UEI x Program) dimension lookup to a per-row formula."""
    return lambda r: composite_lookup(ret, key_range, prog_range, _LABEL, f"$B{r}")


def _arch(ov_ret, map_ret, default):
    """Bind an override-first archetype-code resolution to a per-row formula."""
    return lambda r: override_then_map(
        ov_ret, _OV_UEI, _OV_PROG, _LABEL, f"$B{r}",
        map_ret, _MAP_NAICS, f"${_NAICS_COL}{r}", default)


def _arch_basis(ov_ret):
    """Bind the matching override-first basis-tier label to a per-row formula."""
    return lambda r: override_then_map_basis(
        ov_ret, _OV_UEI, _OV_PROG, _LABEL, f"$B{r}", _MAP_NAICS, f"${_NAICS_COL}{r}")


_FORMULAS = {
    "Subaward $M":      lambda r: f"=SUMIFS({_DOL},{_UEI},$B{r})/1000000",
    "Published Subaward Records": lambda r: f"=COUNTIFS({_UEI},$B{r})",
    "First Subaward":   lambda r: f"=_xlfn.MINIFS({_DATE},{_UEI},$B{r})",
    "Last Subaward":    lambda r: f"=_xlfn.MAXIFS({_DATE},{_UEI},$B{r})",
    "Predominant Place of Performance (by records)": lambda r: (
        f'=IF(COUNTIFS({_UEI},$B{r},{_CC},"<>USA",{_CC},"<>")'
        f'>COUNTIFS({_UEI},$B{r},{_CC},"USA"),"Foreign","Domestic")'),
    # NAICS-6 (code + desc, incl. the n/a labels) and the canonical vendor name come
    # from the Subawardee UEI Index; the standardized parent pair from Subawardee Parents.
    "Subawardee Vendor Name":         _dim(_IX_NAME, _IX_UEI, _IX_PROG),
    "Subawardee NAICS-6 (Primary)":   _dim(_IX_CODE, _IX_UEI, _IX_PROG),
    "Subawardee NAICS-6 Description": _dim(_IX_DESC, _IX_UEI, _IX_PROG),
    "Parent UEI":                     _dim(_PA_PUEI, _PA_UEI, _PA_PROG),
    "Parent Vendor Name":             _dim(_PA_PNAME, _PA_UEI, _PA_PROG),
    # Archetypes: override-first (Vendor Archetype Overrides) -> NAICS-6 crosswalk
    # default (NAICS-6 Archetype Map) -> unresolved (D0 / P0); the Basis cell reports
    # which tier fired. The evidence/rationale lives on those two source sheets now.
    "Capability Domain Archetype (D)":     _arch(_OV_D, _MAP_D, "D0"),
    "Capability Domain Archetype Basis":   _arch_basis(_OV_D),
    "Primary Output Archetype (P)":        _arch(_OV_P, _MAP_P, "P0"),
    "Primary Output Archetype Basis":      _arch_basis(_OV_P),
}

DDG_PROGRAM_VENDORS, _ = make_flat_sheet(
    tab=TAB_DDG_PROGRAM, group="model",
    csv_name="ddg_program_vendors", table_name="DdgProgramVendors",
    banner="§1 - DDG-51 subaward recipients",
    intro="Entity-grain roll-up: one row per DDG-51 subawardee UEI, CY2013-2026; nominal dollars. "
          "Scope = subawards under the hull-construction primes (Bath Iron Works, Ingalls); Navy GFE "
          "primes (propulsion, Aegis, guns/VLS) are funded on separate SCN lines and are out of scope.",
    widths=_WIDTHS,
    int_cols=["Published Subaward Records"], float_cols=["Subaward $M"],
    date_cols=["First Subaward", "Last Subaward"], formula_cols=_FORMULAS,
    input_cols=["Subawardee UEI"],   # the hardcoded identity key -> blue input font
    # Green cross-sheet links: COUNTIFS/MINIFS/MAXIFS surface values that live on
    # the tx sheet. $M (SUMIFS, a new aggregate total) and the place-of-performance
    # classifier stay black.
    link_cols=["Published Subaward Records", "First Subaward", "Last Subaward"],
    # Source URLs -> native hover Notes on the Role / Description cell they support;
    # the Source URLs column is dropped from the visible table. (The archetype Basis
    # cells are now override-first formulas, so they no longer carry evidence Notes -
    # that evidence lives on the Vendor Archetype Overrides / NAICS-6 Archetype Map sheets.)
    note_from={"Role / Description": "Source URLs"},
    # Fake spacer cell in column R so Role / Description (column Q) overflow stops
    # instead of running on across the empty grid (no header, no banner extension).
    right_spacer=True,
)
