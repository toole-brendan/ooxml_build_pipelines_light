"""_integrity - build-stopping cross-CSV universe checks (non-sheet helper).

The program-vendor sheets, the per-UEI dimension sheets, and the transaction fact
sheets must ALL describe the same (Program x UEI) universe. An independent CSV
refresh that updates one pull but not another silently strips the orphaned rows to
dash / D0 / P0: the program-vendor dimension lookups find no matching dimension row,
so the supplier name / NAICS / parent resolve to "-" and the archetype falls to the
unresolved default. That is exactly the 2026-06 Virginia drift - the
N00024-20-C-2120 prime was added to the transaction + program-vendor pulls but not
the dimension pulls, leaving 36 Virginia UEIs unresolved (that prime has since been
removed from scope - 2026-06-21 - but the guard remains the structural guarantee).

`assert_universes_aligned()` is called from lib.build() so `python build_workbook.py`
fails LOUDLY (with the offending keys) rather than shipping a silently drifted
workbook. It is the structural guarantee behind "regenerate the dimensions" - the
re-sync can never quietly come undone again.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from workbook_award_classification_refactor.sheets._cuts import load_table

# (csv stem prefix, Program label) for the per-program single-program CSVs.
_PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

# Versioned prime-contract scope manifest, at the workbook root (two levels up from sheets/).
_SCOPE_MANIFEST = Path(__file__).resolve().parents[2] / "prime_contract_scope.csv"


def _single_program_keys(suffix: str) -> set[tuple[str, str]]:
    """{(Program, UEI)} union over the three <prog>_<suffix>.csv files - Program from
    the file, UEI from the 'Subawardee UEI' column."""
    keys: set[tuple[str, str]] = set()
    for stem, label in _PROGRAMS:
        headers, rows = load_table(f"{stem}_{suffix}")
        j = headers.index("Subawardee UEI")
        for r in rows:
            u = (r[j] if j < len(r) else "").strip()
            if u:
                keys.add((label, u))
    return keys


def _dimension_keys(stem: str) -> set[tuple[str, str]]:
    """{(Program, UEI)} from a dimension CSV that carries its own 'Program' column."""
    headers, rows = load_table(stem)
    jp, ju = headers.index("Program"), headers.index("Subawardee UEI")
    keys: set[tuple[str, str]] = set()
    for r in rows:
        u = (r[ju] if ju < len(r) else "").strip()
        if u:
            keys.add(((r[jp] if jp < len(r) else "").strip(), u))
    return keys


def _diff(a: set, b: set, a_name: str, b_name: str) -> str:
    parts = []
    if a - b:
        parts.append(f"{len(a - b)} in {a_name} not in {b_name} (e.g. {sorted(a - b)[:5]})")
    if b - a:
        parts.append(f"{len(b - a)} in {b_name} not in {a_name} (e.g. {sorted(b - a)[:5]})")
    return "; ".join(parts)


def _tx_piids() -> dict[str, set[str]]:
    """{Program label -> {Prime PIID}} over the three transaction CSVs."""
    out: dict[str, set[str]] = {}
    for stem, label in _PROGRAMS:
        headers, rows = load_table(f"{stem}_subaward_transactions")
        j = headers.index("Prime PIID")
        out[label] = {(r[j] if j < len(r) else "").strip()
                      for r in rows if j < len(r) and (r[j] or "").strip()}
    return out


def _load_manifest() -> dict[str, str]:
    """{PIID -> include flag (Y/N)} from the scope manifest."""
    with _SCOPE_MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        return {(r["piid"] or "").strip(): (r.get("include") or "").strip().upper()
                for r in csv.DictReader(fh) if (r.get("piid") or "").strip()}


def assert_piids_in_manifest() -> None:
    """Fail the build unless every prime PIID in the transaction CSVs is present in the
    versioned scope manifest with include=Y, and no include=N prime leaked through. Warns
    (does not fail) when an include=Y prime returned zero transactions, so an omitted query
    cannot quietly masquerade as a genuine zero (reviewer finding #1)."""
    assert _SCOPE_MANIFEST.exists(), f"scope manifest missing: {_SCOPE_MANIFEST}"
    manifest = _load_manifest()
    present = set().union(*_tx_piids().values())

    missing = sorted(p for p in present if p not in manifest)
    assert not missing, f"transaction PIIDs absent from scope manifest: {missing}"

    leaked = sorted(p for p in present if manifest.get(p) == "N")
    assert not leaked, f"include=N PIIDs leaked into transactions (exclusion not applied): {leaked}"

    zero_rows = sorted(p for p, inc in manifest.items() if inc == "Y" and p not in present)
    if zero_rows:
        print(f"[scope] note: {len(zero_rows)} include=Y prime(s) returned zero subawards "
              f"(queried, accounted): {zero_rows}")


# Warn if semantic duplicate candidates exceed this share of the gross reported total.
_DUP_WARN_PCT = 2.0


def assert_duplicate_audit_recorded() -> None:
    """Reviewer build-stopping test #3: there must be no semantic duplicate candidates without
    an adjudication record. Reads the build-time audit summary + log; asserts the per-row log
    accounts for every candidate, and warns when candidate $ exceeds _DUP_WARN_PCT of gross."""
    ah, arows = load_table("duplicate_audit")
    total = next((r for r in arows if (r[ah.index("Program")] or "").strip() == "TOTAL"), None)
    assert total is not None, "duplicate_audit.csv missing TOTAL row (run build_program_transactions)"
    cand_rows = int(float(total[ah.index("Duplicate-Candidate Rows")] or 0))

    _, log = load_table("duplicate_candidates")
    assert len(log) >= cand_rows, (
        f"duplicate adjudication log incomplete: audit reports {cand_rows} candidates, "
        f"log has {len(log)} rows")

    pct = float(str(total[ah.index("Candidate % of Gross")]).rstrip("%") or 0)
    if pct > _DUP_WARN_PCT:
        print(f"[dedup] WARNING: duplicate candidates are {pct:.2f}% of gross reported "
              f"(> {_DUP_WARN_PCT}% threshold) - review extracted/duplicate_candidates.csv")
    else:
        print(f"[dedup] note: {cand_rows} duplicate candidates ({pct:.2f}% of gross), logged + reported")


def assert_archetype_codes_valid() -> None:
    """Every D/P code in the editable inputs (Vendor Archetype Overrides + NAICS-6 Archetype
    Map) must be a valid taxonomy code OR blank. Combined with the axis-specific override-or-
    blank resolution and the valid D0/P0 default, this guarantees every RESOLVED D in D0..D11
    and P in P0..P6 - no blank or numeric-zero archetype can survive (reviewer finding #3)."""
    from workbook_award_classification_refactor.sheets import _taxonomy
    valid_d = {t[0] for t in _taxonomy.DOMAINS} | {""}
    valid_p = {t[0] for t in _taxonomy.OUTPUTS} | {""}
    bad: list[str] = []
    for stem in ("vendor_archetype_overrides", "naics6_archetype_map"):
        headers, rows = load_table(stem)
        jd, jp = headers.index("Capability Domain (D)"), headers.index("Primary Output (P)")
        for i, r in enumerate(rows, start=2):
            d = (r[jd] if jd < len(r) else "").strip()
            p = (r[jp] if jp < len(r) else "").strip()
            if d not in valid_d:
                bad.append(f"{stem} row {i}: D={d!r}")
            if p not in valid_p:
                bad.append(f"{stem} row {i}: P={p!r}")
    assert not bad, "invalid archetype codes (not in D0..D11 / P0..P6 or blank): " + "; ".join(bad[:20])


def assert_naics_rationale_aligned() -> None:
    """Every NAICS-6 D-Rationale that ends in a terminal 'Dxx' code must agree with the assigned
    Capability Domain (D). Stops the auditability drift the reviewer flagged (finding #5) - a note
    concluding '-> D0' while the row is assigned D11 - from recurring after a refresh. Rationales
    with no explicit terminal code (e.g. 'no defensible single D') are skipped."""
    headers, rows = load_table("naics6_archetype_map")
    jd = headers.index("Capability Domain (D)")
    jr = headers.index("D Rationale")
    bad: list[str] = []
    for r in rows:
        d = (r[jd] if jd < len(r) else "").strip()
        ms = re.findall(r"D(\d+)", r[jr] if jr < len(r) else "")
        if ms and f"D{ms[-1]}" != d:
            bad.append(f"NAICS {r[headers.index('NAICS-6')]}: assigned {d}, rationale ends D{ms[-1]}")
    assert not bad, "NAICS D-rationale vs assigned-code drift: " + "; ".join(bad[:20])


def assert_universes_aligned() -> None:
    """Fail the build unless program-vendor == transaction == Supplier Master on the
    (Program x UEI) universe."""
    pv = _single_program_keys("program_vendors")
    tx = _single_program_keys("subaward_transactions")
    sm = _dimension_keys("supplier_master")

    assert pv == tx, "program-vendor vs transaction (Program x UEI) drift: " + _diff(
        pv, tx, "program-vendor", "transaction")
    assert pv == sm, "program-vendor vs Supplier Master drift: " + _diff(
        pv, sm, "program-vendor", "Supplier Master")
