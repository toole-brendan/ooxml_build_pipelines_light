#!/usr/bin/env python3
"""
New-construction-only aggregator.

Filters existing SAM.gov subaward JSON pulls down to:
  - the 15 in-scope new-construction PIIDs (drops Hartford EOH + Va Tech Instr)
  - excludes MIB / workforce pass-throughs (BlueForge, Training Modernization Group, IALR)

Outputs:
  extracted/nc_annual_by_piid.csv     -- per FY × PIID, with FY totals
  extracted/nc_annual_by_vendor.csv   -- per FY top vendors (parent-UEI rolled)
  extracted/nc_lifetime_vendors.csv   -- top vendors across whole window
  extracted/nc_records_long.csv       -- one row per subaward action (for the workbook)
  extracted/nc_scope_summary.json     -- audit trail: what was kept / excluded
"""
import csv
import glob
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Optional, Dict, Tuple, List

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
OUT = REPO / "extracted"
OUT.mkdir(exist_ok=True)

# 15 in-scope new-construction PIIDs
IN_SCOPE_PIIDS = {
    "N0002417C2100": ("GDEB", "Virginia",  "Va Block V/VI master"),
    "N0002417C2117": ("GDEB", "Columbia",  "Col Build I/II master"),
    "N0002424C2110": ("GDEB", "Virginia",  "Va Block VI LLTM"),
    "N0002412C2115": ("GDEB", "Virginia",  "Va Block IV MYP"),
    "N0002409C2104": ("GDEB", "Virginia",  "Va Block II residual"),
    "N0002413C2128": ("GDEB", "Columbia",  "Col Design Drawings"),
    "N0002411C2109": ("GDEB", "Columbia",  "SSBN-R concept formulation"),
    "N0002416C2111": ("GDEB", "Virginia",  "VPM Vent Valve (Block V)"),
    "N0002410C2118": ("GDEB", "Virginia",  "VPM Tube Fabrication"),
    "N0002419C2114": ("BPMI", "Columbia",  "Naval Reactor Components"),
    "N0002419C2115": ("BPMI", "Columbia",  "Col Class IBI"),
    "N0002424C2114": ("BPMI", "Virginia",  "S9G reactor"),
    "N0002410C6266": ("LM",   "Virginia",  "Va Combat Systems HW/SW"),
    "N0002421C4106": ("BAE",  "Virginia",  "SSN 812 Forward Subassembly"),
    "N0002421C4111": ("RR",   "Virginia",  "Va Class Submarine Rotor"),
}

OUT_OF_SCOPE_PIIDS = {
    "N0002420C4312": ("GDEB", "EXCLUDED: Hartford (SSN-768) EOH — overhaul of existing boat"),
    "N0002419C2125": ("GDEB", "EXCLUDED: Va Tech Instructions / HPAD backfit — upgrades to existing boats"),
}

# MIB / workforce / training pass-throughs to exclude on the recipient side
MIB_EXCLUDED_UEIS = {
    "F8PEZKXES8B1": "BLUEFORGE ALLIANCE",
    "QLJZVM6XKR71": "TRAINING MODERNIZATION GROUP, INC.",
    "TCM3R4JPRKY4": "INSTITUTE FOR ADVANCED LEARNING AND RESEARCH",
}


def fy_of(date_str):
    """Fed FY: Oct 1 of prior year through Sep 30 of FY year. Returns None on bad input."""
    if not date_str or len(date_str) < 10:
        return None
    y, m = int(date_str[:4]), int(date_str[5:7])
    return y + 1 if m >= 10 else y


def recipient_uei(rec: dict) -> str:
    return (rec.get("subParentUei") or rec.get("subEntityUei") or "").strip()


def recipient_name(rec: dict) -> str:
    return ((rec.get("subEntityParentLegalBusinessName") or
             rec.get("subEntityLegalBusinessName") or "UNKNOWN")
            .upper().strip())


def is_foreign(rec: dict) -> bool:
    addr = rec.get("entityPhysicalAddress") or {}
    country = (addr.get("country") or {}).get("code", "") or ""
    return country.upper() not in ("USA", "")


def main():
    in_records = []   # records kept after filtering
    excluded_piid_records = 0
    excluded_mib_records = 0
    excluded_mib_dollars = 0.0

    for f in sorted(glob.glob(str(REPO / "sam_subawards" / "N*.json"))):
        piid_file = Path(f).stem.split("_")[0]
        if piid_file not in IN_SCOPE_PIIDS:
            d = json.load(open(f))
            excluded_piid_records += len(d.get("published", []))
            continue
        d = json.load(open(f))
        for r in d.get("published", []):
            uei = recipient_uei(r)
            if uei in MIB_EXCLUDED_UEIS:
                excluded_mib_records += 1
                excluded_mib_dollars += float(r.get("subAwardAmount") or 0)
                continue
            in_records.append(r)

    print(f"Kept: {len(in_records):,} records "
          f"(after filtering {excluded_piid_records:,} out-of-scope PIID records + "
          f"{excluded_mib_records:,} MIB vendor records = ${excluded_mib_dollars/1e6:,.1f}M)",
          flush=True)

    # ---- Build per-FY × PIID table -------------------------------------------
    by_fy_piid_amt = defaultdict(float)
    by_fy_piid_cnt = defaultdict(int)
    fys = set()
    for r in in_records:
        fy = fy_of(r.get("subAwardDate"))
        if fy is None:
            continue
        amt = float(r.get("subAwardAmount") or 0)
        piid = r["piid"]
        by_fy_piid_amt[(fy, piid)] += amt
        by_fy_piid_cnt[(fy, piid)] += 1
        fys.add(fy)

    piids_sorted = sorted(IN_SCOPE_PIIDS.keys())
    fys_sorted = sorted(fys)

    with open(OUT / "nc_annual_by_piid.csv", "w", newline="") as fout:
        w = csv.writer(fout)
        w.writerow(["FY"] + [f"{p}_$M" for p in piids_sorted] + ["FY_TOTAL_$M"] +
                   [f"{p}_count" for p in piids_sorted] + ["FY_TOTAL_count"])
        for fy in fys_sorted:
            amts = [by_fy_piid_amt[(fy, p)] / 1e6 for p in piids_sorted]
            cnts = [by_fy_piid_cnt[(fy, p)] for p in piids_sorted]
            w.writerow([fy] + [f"{a:.2f}" for a in amts] + [f"{sum(amts):.2f}"] +
                       cnts + [sum(cnts)])

    # ---- Build per-FY × vendor table -----------------------------------------
    by_fy_vendor = defaultdict(
        lambda: {"name": "", "amt": 0.0, "n": 0, "foreign": False, "naics_seen": set()}
    )
    for r in in_records:
        fy = fy_of(r.get("subAwardDate"))
        if fy is None:
            continue
        uei = recipient_uei(r)
        v = by_fy_vendor[(fy, uei)]
        if not v["name"]:
            v["name"] = recipient_name(r)
        v["amt"] += float(r.get("subAwardAmount") or 0)
        v["n"] += 1
        if is_foreign(r):
            v["foreign"] = True

    rows_by_vendor = []
    for (fy, uei), v in by_fy_vendor.items():
        rows_by_vendor.append({
            "fy": fy, "uei": uei, "vendor": v["name"],
            "foreign": "Yes" if v["foreign"] else "",
            "amount_M": v["amt"] / 1e6, "records": v["n"],
        })
    rows_by_vendor.sort(key=lambda r: (r["fy"], -r["amount_M"]))

    with open(OUT / "nc_annual_by_vendor.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy", "uei", "vendor", "foreign",
                                              "amount_M", "records"])
        w.writeheader()
        for row in rows_by_vendor:
            row["amount_M"] = f"{row['amount_M']:.4f}"
            w.writerow(row)

    # ---- Lifetime top-vendor rollup ------------------------------------------
    lifetime = defaultdict(
        lambda: {"name": "", "amt": 0.0, "n": 0, "fys": set(), "piids": set(),
                 "foreign": False}
    )
    for r in in_records:
        uei = recipient_uei(r)
        v = lifetime[uei]
        if not v["name"]:
            v["name"] = recipient_name(r)
        v["amt"] += float(r.get("subAwardAmount") or 0)
        v["n"] += 1
        fy = fy_of(r.get("subAwardDate"))
        if fy:
            v["fys"].add(fy)
        v["piids"].add(r["piid"])
        if is_foreign(r):
            v["foreign"] = True

    lifetime_rows = sorted(
        ({"rank": 0, "uei": uei, "vendor": v["name"],
          "foreign": "Yes" if v["foreign"] else "",
          "amount_M_lifetime": v["amt"] / 1e6,
          "records": v["n"],
          "fy_count": len(v["fys"]),
          "fys": ",".join(str(y) for y in sorted(v["fys"])),
          "piid_count": len(v["piids"]),
          "piids": ",".join(sorted(v["piids"])),
         } for uei, v in lifetime.items()),
        key=lambda x: -x["amount_M_lifetime"],
    )
    for i, row in enumerate(lifetime_rows, start=1):
        row["rank"] = i

    with open(OUT / "nc_lifetime_vendors.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["rank", "uei", "vendor", "foreign",
                                              "amount_M_lifetime", "records",
                                              "fy_count", "fys",
                                              "piid_count", "piids"])
        w.writeheader()
        for row in lifetime_rows:
            row["amount_M_lifetime"] = f"{row['amount_M_lifetime']:.4f}"
            w.writerow(row)

    # ---- Long-form record table (for the workbook + audit) -------------------
    with open(OUT / "nc_records_long.csv", "w", newline="") as fout:
        w = csv.writer(fout)
        w.writerow(["piid", "fy", "subAwardDate", "subAwardAmount_$",
                    "subAwardReportId", "subAwardNumber",
                    "sub_parent_uei", "sub_entity_uei", "sub_name", "foreign",
                    "prime_entity_name", "prime_naics_code", "prime_naics_desc",
                    "description_of_requirement"])
        for r in in_records:
            fy = fy_of(r.get("subAwardDate"))
            pnaics = r.get("primeNaics") or {}
            w.writerow([
                r.get("piid"), fy, r.get("subAwardDate"),
                f"{float(r.get('subAwardAmount') or 0):.2f}",
                r.get("subAwardReportId"), r.get("subAwardNumber"),
                r.get("subParentUei") or "", r.get("subEntityUei") or "",
                recipient_name(r), "Yes" if is_foreign(r) else "",
                r.get("primeEntityName") or "",
                pnaics.get("code") or "", pnaics.get("description") or "",
                r.get("descriptionOfRequirement") or "",
            ])

    # ---- Audit / scope summary -----------------------------------------------
    summary = {
        "in_scope_piids": {p: {"prime": pr, "class": cl, "label": lbl}
                            for p, (pr, cl, lbl) in IN_SCOPE_PIIDS.items()},
        "out_of_scope_piids": {p: {"prime": pr, "reason": lbl}
                                for p, (pr, lbl) in OUT_OF_SCOPE_PIIDS.items()},
        "excluded_mib_ueis": MIB_EXCLUDED_UEIS,
        "records_kept": len(in_records),
        "records_excluded_out_of_scope_piids": excluded_piid_records,
        "records_excluded_mib": excluded_mib_records,
        "dollars_excluded_mib_$M": excluded_mib_dollars / 1e6,
        "fy_range": [min(fys_sorted), max(fys_sorted)] if fys_sorted else None,
        "total_dollars_in_scope_$M": sum(r.get("subAwardAmount") and float(r["subAwardAmount"]) or 0
                                          for r in in_records) / 1e6,
        "unique_parent_ueis_in_scope": len({recipient_uei(r) for r in in_records}),
    }
    with open(OUT / "nc_scope_summary.json", "w") as fout:
        json.dump(summary, fout, indent=2, default=str)

    print()
    print(f"Records kept (in-scope, MIB stripped): {summary['records_kept']:,}")
    print(f"Dollars kept: ${summary['total_dollars_in_scope_$M']:,.1f}M")
    print(f"Unique parent UEIs: {summary['unique_parent_ueis_in_scope']:,}")
    print(f"FY range: {summary['fy_range']}")
    print()
    print("Per-FY totals (in scope, MIB stripped):")
    for fy in fys_sorted:
        total = sum(by_fy_piid_amt[(fy, p)] for p in piids_sorted) / 1e6
        cnt = sum(by_fy_piid_cnt[(fy, p)] for p in piids_sorted)
        print(f"  FY{fy}: ${total:>9,.1f}M   ({cnt:>5,} records)")

    print()
    print("Top 10 vendors lifetime (in scope, MIB stripped):")
    for row in lifetime_rows[:10]:
        print(f"  {row['rank']:>2}. {row['vendor'][:50]:<50}  "
              f"${float(row['amount_M_lifetime']):>8,.1f}M   "
              f"FYs={row['fy_count']}  PIIDs={row['piid_count']}")


if __name__ == "__main__":
    main()
