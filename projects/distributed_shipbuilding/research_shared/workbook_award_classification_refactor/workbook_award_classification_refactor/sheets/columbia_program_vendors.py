"""columbia_program_vendors - the refactored Columbia-class program-vendor sheet.

One row per distinct subawardee UEI on the Columbia-class program across all corpus
years (entity-grain); see ddg_program_vendors for the full column rationale and the
live-formula design. The roll-ups (Subaward $M / Actions / First / Last / Domestic or
Foreign) are SUMIFS / COUNTIFS / MINIFS / MAXIFS / IF over the Columbia Subaward
Transactions leaf, and the Subawardee Vendor Name + NAICS-6 + standardized Parent
UEI / Parent Vendor Name are composite (UEI x Program) lookups into the Subawardee
UEI Index / Subawardee Parents dimensions. This sheet sits in the `model` group.
Built from extracted/columbia_program_vendors.csv (scripts/build_program_vendors.py).
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import (
    make_flat_sheet, composite_lookup, override_then_map, override_then_map_basis,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_COLUMBIA_PROGRAM
from workbook_award_classification_refactor.sheets.columbia_subaward_transactions import (
    columbia_tx_cols,
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

# Source URLs is folded into native hover Notes on Role / Description (note_from
# below) and no longer rendered as a column, so its width (W_URL) is dropped.
_WIDTHS = [W_UEI, W_NAICS, W_NAICS_DESC, W_UEI, W_VENDOR, W_VENDOR, W_DOMFOR,
           W_DOLLAR, W_COUNT, W_CONF, W_CONF, W_CONF, W_DOMFOR, W_CONF, W_DOMFOR,
           W_TEXT_WIDE]

# --- live roll-ups over the Columbia tx leaf ---
_UEI = columbia_tx_cols("Subawardee UEI")
_DOL = columbia_tx_cols("Subaward Amount $")
_DATE = columbia_tx_cols("Subaward Date")
_CC = columbia_tx_cols("Country Code")

# --- entity attributes from the dimension sheets (composite key UEI x Program) ---
_LABEL = "Columbia"
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

COLUMBIA_PROGRAM_VENDORS, _ = make_flat_sheet(
    tab=TAB_COLUMBIA_PROGRAM, group="model",
    csv_name="columbia_program_vendors", table_name="ColumbiaProgramVendors",
    banner="§1 - Columbia-class subaward recipients",
    intro="Entity-grain roll-up: one row per Columbia-class subawardee UEI, CY2016-2025; nominal dollars. "
          "Scope = subawards under the hull-construction prime (GDEB Basic Construction); GFE primes "
          "(BPMI reactor, Lockheed, BAE, Rolls-Royce) are out of scope. The HII-Newport News team-build "
          "workshare flows through GDEB as vendor of record and is largely unreported, so hull/structural "
          "content is understated.",
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
