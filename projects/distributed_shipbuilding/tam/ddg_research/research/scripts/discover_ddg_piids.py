#!/usr/bin/env python3
"""
Discover candidate DDG-51 prime PIIDs from the FPDS raw pulls.

Reads:  fpds_raw/*_raw.json
Writes: extracted/_discovered_piids.json   (used by pull_sam_subawards.py and
                                            aggregate_new_construction.py)
        extracted/_discovered_piids.csv    (human-readable view)

Logic:
  - For each FPDS record, classify the vendor into a DDG vendor group:
      HII-Ingalls, GD-BIW, LM-Aegis, Raytheon, GE-Propulsion, Rolls-Royce,
      BAE-Guns/VLS, L3Harris, NG, DRS, GD-MissionSys
  - For each PIID, keep the latest-mod (max signed_date) record as the
    representative record (gives best total_obligated estimate).
  - Apply min-dollar floor (default $50M total_obligated) to drop noise.
  - Take top-N per group: 30 for yards (HII-Ingalls / GD-BIW — these are the
    DDG primes), 15 for everyone else (GFE vendors). This biases the seed
    list toward the yard work that's most likely to have substantial subawards.

Output format (compatible with old USAspending-discovery output):
  [
    ["N00024XXC2XXX", "HII-Ingalls: ddg 51 flight iii ...", "HUNTINGTON INGALLS INCORPORATED"],
    ...
  ]
"""
import csv
import json
import os
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
FPDS_DIR = REPO / "fpds_raw"
OUT_DIR = REPO / "extracted"
OUT_DIR.mkdir(exist_ok=True)

# DDG vendor-name patterns. Must match the substrings as they appear in FPDS
# `vendorName` fields. Order matters slightly — more-specific patterns first.
DDG_VENDOR_GROUPS = {
    "HII-Ingalls": ("INGALLS SHIPBUILDING", "HUNTINGTON INGALLS"),
    "GD-BIW": ("BATH IRON WORKS",),
    "LM-Aegis": ("LOCKHEED MARTIN",),
    "Raytheon": ("RAYTHEON", "RTX CORPORATION"),
    "GE-Propulsion": ("GENERAL ELECTRIC", "GE AEROSPACE"),
    "Rolls-Royce": ("ROLLS-ROYCE", "ROLLS ROYCE"),
    "BAE-Guns/VLS": ("BAE SYSTEMS",),
    "L3Harris": ("L3HARRIS", "L3 TECHNOLOGIES"),
    "NG": ("NORTHROP GRUMMAN",),
    "DRS": ("LEONARDO DRS", "DRS SYSTEMS", "DRS LAUREL", "DRS NAVAL"),
    "GD-MissionSys": ("GENERAL DYNAMICS MISSION",),
}

# How many top PIIDs to keep per group. Yards get more because they're the
# in-scope DDG primes; GFE vendors get fewer (we only want their DDG-tagged work).
TOP_N_YARDS = 30
TOP_N_OTHER = 15
MIN_DOLLAR = 50_000_000   # drop sub-$50M total_obligated as noise


def vendor_to_group(vendor_name):
    if not vendor_name:
        return None
    upper = vendor_name.upper()
    for group, patterns in DDG_VENDOR_GROUPS.items():
        for pat in patterns:
            if pat in upper:
                return group
    return None


def main():
    if not FPDS_DIR.is_dir():
        raise SystemExit(f"!! {FPDS_DIR} not present — run pull_fpds_ddg_primes.py first")

    by_piid = {}    # piid → {vendor, group, total_obligated, description, ...}
    for fname in sorted(os.listdir(FPDS_DIR)):
        if not fname.endswith("_raw.json") or fname.startswith("_"):
            continue
        with open(FPDS_DIR / fname) as f:
            data = json.load(f)
        for r in data.get("records", []):
            p = r.get("piid")
            if not p:
                continue
            group = vendor_to_group(r.get("vendor_name"))
            if not group:
                continue
            prev = by_piid.get(p)
            # Keep the latest-mod record per PIID
            if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
                by_piid[p] = {
                    "piid": p,
                    "vendor": r.get("vendor_name"),
                    "group": group,
                    "total_obligated": r.get("total_obligated") or 0,
                    "description": (r.get("description") or "")[:200],
                    "signed_date": r.get("signed_date"),
                    "naics": r.get("naics"),
                    "psc": r.get("psc"),
                    "contracting_office": r.get("contracting_office_id"),
                }

    # Bucket by group, take top-N per group, subject to min dollar
    by_group = {}
    for piid, meta in by_piid.items():
        if (meta["total_obligated"] or 0) < MIN_DOLLAR:
            continue
        by_group.setdefault(meta["group"], []).append(meta)

    seeds = []   # list of [piid, label, vendor]
    long_rows = []
    for group, lst in sorted(by_group.items()):
        lst.sort(key=lambda m: m["total_obligated"], reverse=True)
        cap = TOP_N_YARDS if group in ("HII-Ingalls", "GD-BIW") else TOP_N_OTHER
        for meta in lst[:cap]:
            label = f"{group}: {meta['description'][:120]}"
            seeds.append([meta["piid"], label, meta["vendor"]])
            long_rows.append({
                "group": group,
                "piid": meta["piid"],
                "vendor": meta["vendor"],
                "total_obligated_M": round(meta["total_obligated"] / 1e6, 2),
                "signed_date": meta["signed_date"],
                "naics": meta["naics"],
                "psc": meta["psc"],
                "contracting_office": meta["contracting_office"],
                "description": meta["description"],
            })

    # Write seed PIIDs in the same JSON format the SAM script expects
    seed_path = OUT_DIR / "_discovered_piids.json"
    with open(seed_path, "w") as f:
        json.dump(seeds, f, indent=2)
    print(f"Wrote {seed_path}  ({len(seeds)} PIIDs)")

    # Also write a human-readable CSV
    csv_path = OUT_DIR / "_discovered_piids.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "group", "piid", "vendor", "total_obligated_M", "signed_date",
            "naics", "psc", "contracting_office", "description"
        ])
        w.writeheader()
        for row in long_rows:
            w.writerow(row)
    print(f"Wrote {csv_path}")

    # Print summary per group
    print("\nDiscovered DDG PIIDs by group (top of each list):")
    by_group_summary = {}
    for row in long_rows:
        by_group_summary.setdefault(row["group"], []).append(row)
    for group, rows in by_group_summary.items():
        total = sum(r["total_obligated_M"] for r in rows)
        print(f"\n  [{group}] {len(rows)} PIIDs  total cum-obligated=${total:,.0f}M")
        for r in rows[:5]:
            print(f"    {r['piid']}  ${r['total_obligated_M']:>9,.1f}M  "
                  f"{r['vendor'][:40]:40s}  {r['description'][:60]}")


if __name__ == "__main__":
    main()
