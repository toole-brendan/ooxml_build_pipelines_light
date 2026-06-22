#!/usr/bin/env python3
"""mapping_rules - deterministic, documented classification for the contract families.

Two faithful, rule-derived classifications used when aggregate builds contract_families.csv:
  * watercraft_relevance(...) -> short basis string or None (mirrors the radar's old
    _wc_reason; near-saturating because discovery was already PSC/NAICS-scoped).
  * customer_segment(...)     -> a market segment, so the workbook never reports Army
    operational watercraft and USACE civil works as one homogeneous market (review #5).

These are RULES, not analyst judgment: an analyst override lives in the analyst layer
(customer_org_map.csv / opportunities), never edited into the mechanical aggregate.
"""
from __future__ import annotations

import config as C


def watercraft_relevance(psc, naics, recipient, naics_desc, psc_desc):
    psc = (psc or "").strip()
    naics = (naics or "").strip()
    name = (recipient or "").upper()
    nd = (naics_desc or "").upper()
    pd = (psc_desc or "").upper()
    if psc in C.WC_PSC:
        return f"PSC {psc}"
    if naics in C.WC_NAICS:
        return f"NAICS {naics}"
    for p in C.WC_PRIMES:
        if p in name:
            return f"prime: {p.title()}"
    for t in C.WC_DESC:
        if t in nd or t in pd:
            return f"desc: {t.lower()}"
    return None


def saronic_tier(segment):
    """Re-group a customer_segment into a Saronic priority tier (Core / Adjacent /
    Peripheral) so the timing screens default Saronic-first. Pure derivation - no new
    judgment; unknown segments fall to Peripheral."""
    return C.SARONIC_TIER_BY_SEGMENT.get(segment, C.SARONIC_TIER_PERIPHERAL)


# Raw FPDS idv_type / award_type_description -> a normalized agreement type. A BOA/BPA is
# NOT a guaranteed-recompete contract (FAR 16.703/16.702); its nominal end is a weaker
# signal than an IDC ordering-period end or a standalone contract PoP end.
_AGREEMENT_NORM = {
    "IDC": "IDC", "BOA": "BOA", "BPA": "BPA", "FSS": "FSS",
    "IDV (hydrated)": "Hydrated-IDV",
}

# Position 9 of a legacy 13-char DoD PIID is the authoritative instrument-type code (DFARS
# PGI 204.16). It SURVIVES hydration, which blanks idv_type to "IDV (hydrated)" on the
# synthetic base record - so it's the only place a BOA (G) or BPA (A) can still be recovered
# (e.g. BOA W912BU07G0001, whose 2050 nominal end must read as a weak signal, not a vehicle
# recompete). D = IDC, F = order against a vehicle.
_PIID_TYPE9 = {"A": "BPA", "G": "BOA", "D": "IDC"}


def _piid_instrument(piid):
    """Decode position 9 of a standard legacy DoD PIID (DoDAAC + 2-digit FY + type letter +
    4-char serial). Returns the normalized type or None when the PIID isn't that shape."""
    p = (piid or "").strip()
    if len(p) == 13 and p[6:8].isdigit() and p[8:9].isalpha():
        return _PIID_TYPE9.get(p[8:9].upper())
    return None


def agreement_type(idv_type, is_idv, piid=None):
    """Normalized agreement type. The PIID position-9 code is authoritative for the BOA/BPA
    distinction (it survives hydration, which idv_type does not); otherwise normalize the
    dominant award's idv_type. Blank idv_type -> Standalone (a definitive contract / purchase
    order), or IDC if the family nonetheless has task orders under it (an IDV whose base
    record lacks an explicit idv_type)."""
    code = _piid_instrument(piid)
    if code in ("BOA", "BPA"):           # distinctions idv_type loses post-hydration
        return code
    raw = (idv_type or "").strip()
    if raw in _AGREEMENT_NORM:
        return _AGREEMENT_NORM[raw]
    if code == "IDC":
        return "IDC"
    return "IDC" if is_idv else "Standalone"


def _has(blob, *terms):
    return any(t in blob for t in terms)


def customer_segment(psc, naics, office, recipient, description, department):
    """Classify a family into one market segment (first match wins). Inputs are the
    dominant award's fields. office = contracting office code (e.g. W56HZV, W912xx)."""
    psc = (psc or "").strip()
    naics = (naics or "").strip()
    office = (office or "").upper()
    dep = (department or "").upper()
    blob = " ".join(str(x or "") for x in (recipient, description, psc, naics)).upper()

    usace_office = office.startswith("W912") or office.startswith("W071") or \
        office.startswith("W074") or office.startswith("W2S") or "ENGINEER" in blob
    is_usace = ("CORPS OF ENGINEERS" in dep) or usace_office

    # 1) Army experimentation / autonomy / sensors / RDT&E (cross-cuts; check first so an
    #    autonomy award under a watercraft office is not mislabeled operational).
    if _has(blob, "UNMANNED", "AUTONOM", "USV", "PROTOTYPE", "EXPERIMENT", "RDT&E",
            "RESEARCH AND DEVELOP", "SCIENCE AND TECHNOLOGY", " AOA", "TRADE STUD") \
            or naics in {"541715", "541330", "541714"}:
        return C.SEG_ARMY_RDTE

    # 2) USACE floating plant / civil works (dredges, survey boats, civil-works barges).
    if is_usace:
        return C.SEG_USACE

    # 3) Army operational watercraft & bridging (TACOM watercraft office or operational
    #    descriptors / PSCs).
    army_ops_office = office.startswith("W56HZV") or office.startswith("W4GG")
    if army_ops_office or psc in {"1905", "1925", "1940"} or _has(
            blob, "LANDING CRAFT", "MANEUVER SUPPORT VESSEL", "MSV", "LCU", "LSV",
            "WATERCRAFT", "CAUSEWAY", "LIGHTER", "BRIDG", "PONTOON", "FERRY", "MODULAR CAUSEWAY"):
        return C.SEG_ARMY_OPS

    # 4) Army logistics / prepositioned / floating capability.
    if _has(blob, "PREPOSITION", "APS-", "ARMY PREPOSITIONED", "LOGISTIC SUPPORT VESSEL",
            "FLOAT", "BARGE", "WAREHOUSE AFLOAT"):
        return C.SEG_ARMY_LOG

    # 5) Maintenance, repair & vessel support.
    if _has(blob, "REPAIR", "OVERHAUL", "SLEP", "MAINTENANCE", "DRYDOCK", "DRY DOCK",
            "DEPOT", "RESET", "SUSTAIN", "REFURB") or psc.startswith("J"):
        return C.SEG_MRO

    # 6) Everything else maritime that surfaced under the watercraft net.
    return C.SEG_PERIPHERAL
