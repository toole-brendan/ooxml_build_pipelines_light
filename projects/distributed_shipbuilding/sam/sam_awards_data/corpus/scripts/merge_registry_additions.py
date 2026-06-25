#!/usr/bin/env python3
"""
Validate and append registry_additions_worksheet.csv to the shared vendor registry (B3).

Safety:
  - vocabulary check (role/bucket/confidence/flags) against the registry conventions
  - UEIs already present in the registry are rejected UNLESS the existing row is an
    unresolved placeholder (role=residual, confidence=low) — those are upgraded in
    place, with the prior basis preserved in notes. Real adjudications never move.
  - backs up the registry to vendor_evidence_registry_pre_competability.csv.bak
    (first run only) before writing

The registry is shared with the live submarines/ddg/consolidated workbooks; appends
are additive, so existing classifications can only gain coverage.
"""
from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import EXTRACTED, REGISTRY_CSV

VALID_ROLES = {"supplier", "prime", "co_prime", "gfe", "gfe_sib", "service",
               "holding", "mission_systems", "foreign_fms", "residual"}
VALID_BUCKETS = {"structural", "machining", "castings", "piping", "electrical",
                 "hvac", "coatings", ""}
VALID_CONF = {"high", "med", "low"}


def main() -> int:
    worksheet = EXTRACTED / "registry_additions_worksheet.csv"
    with worksheet.open(encoding="utf-8-sig", newline="") as fh:
        additions = list(csv.DictReader(fh))

    with REGISTRY_CSV.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        existing = list(reader)
    by_uei = {r["uei"]: r for r in existing}

    errors = []
    seen = set()
    upgrades = []
    for i, r in enumerate(additions, start=2):
        uei = (r.get("uei") or "").strip()
        if not uei or len(uei) != 12:
            errors.append(f"row {i}: bad uei {uei!r}")
        if uei in by_uei:
            prior = by_uei[uei]
            if prior.get("role") == "residual" and prior.get("confidence") == "low":
                upgrades.append(uei)
            else:
                errors.append(f"row {i}: uei {uei} already adjudicated "
                              f"(role={prior.get('role')}, conf={prior.get('confidence')})")
        if uei in seen:
            errors.append(f"row {i}: duplicate uei {uei} in worksheet")
        seen.add(uei)
        if r.get("role") not in VALID_ROLES:
            errors.append(f"row {i}: bad role {r.get('role')!r}")
        if r.get("bucket") not in VALID_BUCKETS:
            errors.append(f"row {i}: bad bucket {r.get('bucket')!r}")
        if r.get("confidence") not in VALID_CONF:
            errors.append(f"row {i}: bad confidence {r.get('confidence')!r}")
        missing = [k for k in fields if k not in r]
        if missing:
            errors.append(f"row {i}: missing columns {missing}")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  {e}")
        return 1

    bak = REGISTRY_CSV.with_name("vendor_evidence_registry_pre_competability.csv.bak")
    if not bak.exists():
        shutil.copy2(REGISTRY_CSV, bak)
        print(f"Backed up registry to {bak}")

    upgrade_set = set(upgrades)
    add_rows = []
    for r in additions:
        row = {k: r.get(k, "") for k in fields}
        if r["uei"] in upgrade_set:
            prior = by_uei[r["uei"]]
            note = f"upgraded from residual ({prior.get('basis', '')})"
            row["notes"] = f"{row['notes']}; {note}".strip("; ")
            by_uei[r["uei"]].update(row)   # in-place upgrade
        else:
            add_rows.append(row)

    with REGISTRY_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in existing:
            w.writerow({k: r.get(k, "") for k in fields})
        for r in add_rows:
            w.writerow(r)
    print(f"Registry updated: {len(existing)} rows kept ({len(upgrades)} upgraded "
          f"in place: {', '.join(upgrades)}), {len(add_rows)} appended "
          f"-> {len(existing) + len(add_rows)} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
