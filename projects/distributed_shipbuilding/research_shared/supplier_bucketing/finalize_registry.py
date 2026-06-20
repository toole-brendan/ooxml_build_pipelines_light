#!/usr/bin/env python3
"""Task C (data) - build the extended evidence registry.

Upgrades the owner-accepted 45-row registry to the full Task-C schema, normalizes
the role vocabulary, recomputes scenario_flags to the Task-D definitions
(HM&E += electrical; modular = structural + EXPLICIT modular flags, drop coatings),
and folds in the >=$20M tail entities from tail_resolved.csv with §4 judgment
overrides. Writes projects2/vendor_evidence_registry.csv (the v1 backup is kept).
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path("/Users/brendantoole/projects2")
HERE = ROOT / "ooxml_build_pipelines_light/projects/distributed_shipbuilding/research_shared/supplier_bucketing"
OLD = ROOT / "vendor_evidence_registry_v1_45.csv.bak"
OUT = ROOT / "vendor_evidence_registry.csv"
TAIL = HERE / "tail_resolved.csv"

NEW_COLS = ["uei", "entity_name", "parent_or_display_name", "platform",
            "ddg_signed_$M", "subs_signed_$M", "role", "bucket", "in_physical_base",
            "scenario_flags", "confidence", "basis", "evidence_source",
            "override_grain", "notes"]

# bucket -> base scenario flags (Task D). modular is added separately for module assemblers.
BASE_FLAGS = {
    "structural": ["metal", "broad"],
    "machining": ["metal", "hme", "broad"],
    "castings": ["metal", "broad"],
    "piping": ["hme", "broad"],
    "electrical": ["electrical", "hme", "broad"],
    "hvac": ["hme", "broad"],
    "coatings": ["broad"],
}


def flags_for(bucket, modular, vls_boundary):
    if vls_boundary:
        return "vls_boundary"
    if bucket not in BASE_FLAGS:
        return ""
    f = list(BASE_FLAGS[bucket])
    if modular and bucket == "structural":
        f.insert(1, "modular")
    return ",".join(f)


def platform(ddg, subs):
    d, s = float(ddg or 0), float(subs or 0)
    if d and s:
        return "both"
    return "subs" if s else "ddg"


# ── 1. upgrade the accepted 45 rows ──────────────────────────────────────────
def upgrade_existing():
    rows = []
    with OLD.open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            role = (r.get("role") or "").strip()
            old_flags = (r.get("scenario_flags") or "").strip()
            bucket = (r.get("bucket") or "").strip()
            modular = "modular" in old_flags
            vls = role == "mission_vls"
            # normalize role vocabulary
            if role == "mission":
                role = "mission_systems"
            elif role == "mission_vls":
                role = "mission_systems"
            elif role == "foreign":
                role = "foreign_fms"
            # Arctic Slope (5511) is a holding, not a service
            if "arctic slope" in (r.get("entity_name") or "").lower():
                role = "holding"
            rows.append({
                "uei": r["uei"], "entity_name": r["entity_name"],
                "parent_or_display_name": r["entity_name"],
                "platform": platform(r.get("ddg_$M"), r.get("subs_$M")),
                "ddg_signed_$M": r.get("ddg_$M", "0"),
                "subs_signed_$M": r.get("subs_$M", "0"),
                "role": role, "bucket": bucket,
                "in_physical_base": "yes" if role == "supplier" else "no",
                "scenario_flags": flags_for(bucket, modular, vls),
                "confidence": r.get("confidence", ""),
                "basis": r.get("basis", ""),
                "evidence_source": r.get("evidence_source", ""),
                "override_grain": r.get("override_grain", "firm_entity"),
                "notes": "vls launch-control boundary (sensitivity-in only)" if vls else "",
            })
    return rows


# ── 2. §4 judgment overrides for the tail (uei -> (role, bucket, conf, note)) ──
OVERRIDE = {
    "WMXDDH6HJNA5": ("prime", "", "high", "HII Newport News - prime yard"),
    "CMT4S6G76QB5": ("gfe", "", "high", "BWXT - naval nuclear reactor plant (NNPP/Navy-directed)"),
    "YNJNTZWVC3H6": ("mission_systems", "", "med", "BAE Land & Armaments - naval gun/combat systems"),
    "HLVNZXU8EAM1": ("mission_systems", "", "med", "L-3 Communications - comms/EW (parent holding)"),
    "H9DTZCLEYHD5": ("mission_systems", "", "med", "Teledyne Defense Electronics"),
    "CPHLNLBGWFN5": ("supplier", "electrical", "high", "DRS Naval Power - ship power equipment (§4)"),
    "WQ6KK3G6K2M1": ("supplier", "machining", "med", "Arconic/RTI Remmele - precision machining"),
    "JA2KCX21NL48": ("supplier", "machining", "med", "Wartsila Defense - waterjets/propulsion"),
    "L4UCL5K5H5J9": ("supplier", "machining", "med", "Woodward - engine fuel/actuation controls"),
    "TFJMUN5RL718": ("supplier", "machining", "med", "Barnes Group - aerospace precision components"),
    "N5KMLMXEPFM5": ("supplier", "piping", "med", "Parker Hannifin - hydraulics/fluid power"),
    "M6N8EM57NLL3": ("supplier", "piping", "med", "Parker Hannifin - seals/sealing devices"),
    "J645RTMFWMW1": ("supplier", "piping", "med", "Maxim Evaporators - shipboard distilling plants"),
    "JW6PXX1WALN4": ("supplier", "hvac", "med", "Howden - marine fans/ventilation"),
    "M1LQD44NEJ56": ("supplier", "coatings", "med", "Applied Composite Structures - composites"),
    # bucket-precision fixes (4-digit too coarse)
    "XYNDM1Y7XGG7": ("supplier", "machining", "med", "American Metal Bearing - bearings"),
}

# explicit single-name fixes by sam_legal substring (applied after uei overrides)
LEGAL_FIX = {
    "DRS NAVAL POWER": ("supplier", "electrical", "high", "DRS Naval Power - ship power equipment (§4)"),
    "RICHLIND METAL FABRICATORS": ("supplier", "structural", "med", "Richlind - metal fabrication"),
}


def fold_tail(existing_ueis):
    rows = []
    with TAIL.open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            uei = r["uei"].strip()
            if uei in existing_ueis:
                continue
            role = r["role"]; bucket = r["bucket"]; conf = r["confidence"]; note = ""
            if uei in OVERRIDE and OVERRIDE[uei]:
                role, bucket, conf, note = OVERRIDE[uei]
            else:
                for sub, fix in LEGAL_FIX.items():
                    if sub in (r["sam_legal"] or "").upper():
                        role, bucket, conf, note = fix
                        break
            legal = (r["sam_legal"] or "").strip()
            brand = (r["entity_name"] or "").strip()
            rows.append({
                "uei": uei,
                "entity_name": legal or brand,
                "parent_or_display_name": brand,
                "platform": platform(r["ddg_signed_$M"], r["subs_signed_$M"]),
                "ddg_signed_$M": r["ddg_signed_$M"],
                "subs_signed_$M": r["subs_signed_$M"],
                "role": role, "bucket": bucket,
                "in_physical_base": "yes" if role == "supplier" else "no",
                "scenario_flags": flags_for(bucket, False, False),
                "confidence": conf,
                "basis": (note or r["basis"]),
                "evidence_source": f"SAM {r['primary_naics']} (tail pass)" if r["primary_naics"] else "tail pass (no SAM NAICS)",
                "override_grain": "firm_entity",
                "notes": note,
            })
    return rows


def main():
    existing = upgrade_existing()
    existing_ueis = {r["uei"] for r in existing}
    tail = fold_tail(existing_ueis)
    allrows = existing + tail
    # sort by combined signed $ desc
    def comb(r):
        return float(r["ddg_signed_$M"] or 0) + float(r["subs_signed_$M"] or 0)
    allrows.sort(key=comb, reverse=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=NEW_COLS)
        w.writeheader()
        w.writerows(allrows)
    print(f"registry written: {len(allrows)} rows ({len(existing)} upgraded + {len(tail)} tail) -> {OUT}")
    # tally
    from collections import defaultdict
    t = defaultdict(lambda: [0, 0.0])
    for r in allrows:
        t[r["role"]][0] += 1
        t[r["role"]][1] += comb(r)
    print("role tally (registry):")
    for role, (n, d) in sorted(t.items(), key=lambda kv: -kv[1][1]):
        print(f"  {role:16} {n:3}  ${d:9.1f}M")


if __name__ == "__main__":
    main()
