"""name_map - the Phase-4 replacement for the workbook's defined-name table.

Through Phase 3 the four model producers (Reconciliation, Services, OP-5, MSC/SCN/
USCG) re-published their ~88 v4.33 defined names (the "bridge") at their new native
cells so qa/tie_out.py could validate the model figures *by name* against a soffice
recompute. Phase 4 drops those bridge names entirely - the workbook now ships ZERO
defined names - so the tie-out's Invariant B no longer has a workbook definedName
table to read from. This module supplies that table instead: ``NAME_TO_ACCESSOR``
maps each legacy v4.33 name to a zero-arg callable that returns the producer
accessor's ``'Sheet'!Cell`` ref. tie_out reads the recomputed value at that cell and
asserts it equals the frozen baseline value for the name (Invariant B).

The map is built from the SAME closure accessors the consumer sheets use, so a wrong
captured row breaks both the live model and this gate identically - the map cannot
"agree with itself" against a broken build.

Two of the 88 v4.33 names are formula-defined date constants (FY25_START / FY25_END =
DATE(...)) with NO cell target; they were never consumed cross-sheet (no formula
references them) and are simply dropped in Phase 4. So this map covers the 86
cell-anchored model figures; the date names are intentionally absent (see
``_DROPPED_FORMULA_NAMES``).
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
sys.path.insert(0, str(_HERE.parents[1]))          # projects/mro/workbook/ -> workbook_mro
sys.path.insert(0, str(_HERE.parents[5]))          # workspace root        -> workbook_core

from workbook_mro.sheets.model_reconciliation import (   # noqa: E402
    reconciled_mro_tam_cell, public_shipyard_nwcf_cell,
    hii_mt_rev_cell, hii_mt_oi_cell, hii_mt_svc_mix_cell,
    psc1905_mro_cell, mro_tas_cell, omn_cell, scn_cell, uscg_isvs_cell,
)
from workbook_mro.sheets.model_services import (         # noqa: E402
    navy_tam_svc_cell, cg_tam_svc_cell,
)
from workbook_mro.sheets.model_op5_navy_topdown import (  # noqa: E402
    op5_cell, op5_private_cell, op5_public_nsy_cell, op5_total_cell,
)
from workbook_mro.sheets.model_msc_scn_uscg_topdown import (  # noqa: E402
    msc_mr_fy25_transfer_cell, msc_mr_fy26_mta_cell, msc_mr_fy26_roh_cell,
    msc_mr_fy26_other_cell, msc_mr_fy26_total_cell,
    scn_cvn74_rcoh_cell, scn_cvn75_rcoh_fy26_cell, scn_cvn_rcoh_li2086_cell,
    uscg_isvs_floor_cell, uscg_os_memo_fy25_cell, opn_li1000_cell,
)

# The two formula-defined date names carried no cell target and are referenced by no
# formula; Phase 4 drops them. Recorded here so the coverage self-check can account for
# the full 88-name baseline (86 cell-anchored here + these 2 dropped).
_DROPPED_FORMULA_NAMES = ("FY25_START", "FY25_END")

# Key families for the parameterized Reconciliation accessors (mirrors the producer).
_PSC1905_BUCKETS = (
    "EMBEDDED", "SUBS", "CARRIERS", "SURFCOMBS", "UNCL", "SSN", "CVN", "DDG", "LCS",
    "TIER0", "GD", "HII", "BAE", "OTHER_PRIMES",
)
_MRO_TAS_KEYS = (
    "OMN", "OPN", "OPN_BA7", "OPN_BA8", "OPN_BAOTHER", "RDTE_DW", "DW_OTHER",
    "NAVY_OTHER", "SCN", "AIR_FORCE", "USCG", "ARMY", "OTHER_AGENCY", "TOTAL",
)
_OMN_KEYS = (
    "1B1B_TOTAL", "1B1B_CONTRACT", "1B2B_TOTAL", "1B2B_CONTRACT",
    "1B4B_TOTAL", "1B4B_CONTRACT", "1B5B_TOTAL", "1B5B_CONTRACT",
    "SHIPOPS_BA1_TOTAL", "SHIPOPS_BA1_CONTRACT",
)
_SCN_KEYS = ("COLUMBIA", "VIRGINIA", "CVN_RCOH", "CVN_REPL", "CVN81")
_USCG_ISVS_KEYS = ("TOTAL", "47MLB", "WMEC", "HEALY")

# OP-5 FY25-Current availability codes (private + public NSY).
_OP5_CODES = (
    "OH", "SRA", "SIA", "PIA", "PMA", "CIA", "SCO", "ERATA", "ORATA", "CM", "IL",
    "NNSY", "PNSY", "PSNSY", "PHNSY",
)


def _build() -> dict:
    """name -> zero-arg callable returning the accessor's 'Sheet'!Cell ref."""
    m: dict[str, callable] = {}

    # ---- Reconciliation (52) ----
    m["RECONCILED_MRO_TAM"] = reconciled_mro_tam_cell
    m["PUBLIC_SHIPYARD_NWCF"] = public_shipyard_nwcf_cell
    m["HII_MT_FY25_REV"] = hii_mt_rev_cell
    m["HII_MT_FY25_OI"] = hii_mt_oi_cell
    m["HII_MT_FY25_SVC_MIX_PCT"] = hii_mt_svc_mix_cell
    for b in _PSC1905_BUCKETS:
        m[f"PSC1905_MRO_{b}"] = (lambda bb=b: psc1905_mro_cell(bb))
    for k in _MRO_TAS_KEYS:
        m[f"MRO_TAS_{k}_FY25"] = (lambda kk=k: mro_tas_cell(kk))
    for k in _OMN_KEYS:
        m[f"OMN_{k}_FY25"] = (lambda kk=k: omn_cell(kk))
    for k in _SCN_KEYS:
        m[f"SCN_{k}_FY25"] = (lambda kk=k: scn_cell(kk))
    for k in _USCG_ISVS_KEYS:
        m[f"USCG_ISVS_{k}_FY25"] = (lambda kk=k: uscg_isvs_cell(kk))

    # ---- Services (2) ----
    m["NAVY_TAM_SVC"] = navy_tam_svc_cell
    m["CG_TAM_SVC"] = cg_tam_svc_cell

    # ---- OP-5 Navy Top-Down (18) ----
    for code in _OP5_CODES:
        m[f"OP5_{code}_FY25"] = (lambda cc=code: op5_cell(cc))
    m["OP5_PRIVATE_FY25"] = op5_private_cell
    m["OP5_PUBLIC_NSY_FY25"] = op5_public_nsy_cell
    m["OP5_TOTAL_FY25"] = op5_total_cell

    # ---- MSC / SCN / USCG / OPN Top-Down (14) ----
    m["MSC_MR_FY25_1B1B_TRANSFER"] = msc_mr_fy25_transfer_cell
    m["MSC_MR_FY26_MTA"] = msc_mr_fy26_mta_cell
    m["MSC_MR_FY26_ROH"] = msc_mr_fy26_roh_cell
    m["MSC_MR_FY26_OTHER"] = msc_mr_fy26_other_cell
    m["MSC_MR_FY26_TOTAL"] = msc_mr_fy26_total_cell
    m["SCN_CVN74_RCOH_FY25"] = (lambda: scn_cvn74_rcoh_cell(2025))
    m["SCN_CVN74_RCOH_FY26"] = (lambda: scn_cvn74_rcoh_cell(2026))
    m["SCN_CVN75_RCOH_FY26"] = scn_cvn75_rcoh_fy26_cell
    m["SCN_CVN_RCOH_LI2086_FY25"] = (lambda: scn_cvn_rcoh_li2086_cell(2025))
    m["SCN_CVN_RCOH_LI2086_FY26"] = (lambda: scn_cvn_rcoh_li2086_cell(2026))
    m["USCG_ISVS_FY25_FLOOR"] = uscg_isvs_floor_cell
    m["USCG_OS_MEMO_FY25"] = uscg_os_memo_fy25_cell
    m["OPN_LI1000_FY25"] = (lambda: opn_li1000_cell(2025))
    m["OPN_LI1000_FY26"] = (lambda: opn_li1000_cell(2026))

    return m


NAME_TO_ACCESSOR = _build()

assert len(NAME_TO_ACCESSOR) == 86, (
    f"name_map should cover 86 cell-anchored names, got {len(NAME_TO_ACCESSOR)}")


def coverage_report(oracle_names: set[str]) -> tuple[list[str], list[str]]:
    """Diff this map against a baseline name set.

    Returns (uncovered, stale): legacy oracle names NOT in this map (excluding the
    intentionally-dropped date names), and map names absent from the oracle.
    """
    mapped = set(NAME_TO_ACCESSOR)
    droppable = set(_DROPPED_FORMULA_NAMES)
    uncovered = sorted((oracle_names - mapped) - droppable)
    stale = sorted(mapped - oracle_names)
    return uncovered, stale


if __name__ == "__main__":
    for nm in sorted(NAME_TO_ACCESSOR):
        print(f"{nm:32s} -> {NAME_TO_ACCESSOR[nm]()}")
    print(f"\n{len(NAME_TO_ACCESSOR)} cell-anchored names; "
          f"dropped formula names: {', '.join(_DROPPED_FORMULA_NAMES)}")
