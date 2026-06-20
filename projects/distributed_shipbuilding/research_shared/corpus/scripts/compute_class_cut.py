#!/usr/bin/env python3
"""
Descriptive class/builder cuts of the competability corpus (no gates).

Cuts: submarines by vessel class (Virginia / Columbia); DDG by builder group
(GD-BIW / HII-Ingalls) — DDG-51 is single-class, and FSRS visibility differs
sharply by builder, so the group cut is the DDG analog. Per the handoff, gates
stay at the program level: these outputs carry pools / vendor counts / HHI /
overlap only, with a thin-lane flag where the cut is too small to read.

Universe and conventions match compute_competability_signals.py: supplier-role
records only, vendor key = parent-first UEI, FY22-25 window dollars (COMP_WINDOW
overrides), modal work type by all-time dollars — here computed per (vendor,
cut) so lanes don't bleed across cuts.

Outputs (extracted/ or COMP_OUTDIR):
  class_cut_scorecard.csv   one row per (program, cut, work_type)
  vendor_class_matrix.csv   one row per (program, vendor) with per-cut dollars,
                            first-award dates, and cut_profile (X-only / both)
  piid_profile.csv          one row per in-corpus PIID with data-thinness status
                            (zero-record PIIDs included)
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import (BUCKET_KEYS, FY22_25, OUT_DIR, UNBUCKETED, in_window,
                     iter_records, load_registry, scope_meta)

FY_LO, FY_HI = FY22_25
LANES = BUCKET_KEYS + [UNBUCKETED]
CUTS = {
    "submarines": ("vclass", ["Virginia", "Columbia"], ("virginia", "columbia")),
    "ddg": ("bgroup", ["GD-BIW", "HII-Ingalls"], ("biw", "ingalls")),
}
THIN_VENDORS, THIN_POOL_M = 5, 20.0


def _new_cut():
    return {"bucket_all": defaultdict(float), "w_$": 0.0, "n_w": 0,
            "n_all": 0, "n_pre": 0, "first": ""}


def collect(program: str, registry):
    """Returns (vendors, piid_stats). vendors: vendor_key -> rollup with per-cut
    sub-rollups; piid_stats seeded from scope so zero-record PIIDs appear."""
    cut_field, cut_names, _ = CUTS[program]
    piid_stats = {p: {"meta": m, "n_all": 0, "sup_w_$": 0.0,
                      "sup_vendors": set(), "lane_$": defaultdict(float)}
                  for p, m in scope_meta(program).items()}
    vendors = {}
    for rec in iter_records(program, registry=registry):
        P = piid_stats[rec["piid"]]
        P["n_all"] += 1
        if rec["role"] != "supplier":
            continue
        in_w = in_window(rec, FY_LO, FY_HI)
        if in_w:
            P["sup_w_$"] += rec["dollar_m"]
            P["sup_vendors"].add(rec["vendor_key"])
            P["lane_$"][rec["bucket"]] += rec["dollar_m"]

        g = vendors.get(rec["vendor_key"])
        if g is None:
            g = vendors[rec["vendor_key"]] = {
                "names": defaultdict(float), "bucket_all": defaultdict(float),
                "cuts": {c: _new_cut() for c in cut_names},
            }
        name = (rec["parent_name"] or rec["vendor"]).upper()
        g["names"][name] += rec["dollar_m"]
        g["bucket_all"][rec["bucket"]] += rec["dollar_m"]
        c = g["cuts"].setdefault(rec[cut_field], _new_cut())
        c["bucket_all"][rec["bucket"]] += rec["dollar_m"]
        c["n_all"] += 1
        date = rec["date"][:10]
        if date and (not c["first"] or date < c["first"]):
            c["first"] = date
        if rec["fy"] is not None and rec["fy"] < FY_LO:
            c["n_pre"] += 1
        if in_w:
            c["w_$"] += rec["dollar_m"]
            c["n_w"] += 1
    return vendors, piid_stats


def main() -> int:
    registry = load_registry()
    score_rows, matrix_rows, piid_rows = [], [], []
    recon = {}

    for program in ("submarines", "ddg"):
        cut_field, cut_names, cut_cols = CUTS[program]
        vendors, piid_stats = collect(program, registry)

        # ---- per-(cut, lane) descriptive scorecard -----------------------------
        lane = {(cn, ln): {"pool": 0.0, "vendors": [], "n_recs": 0, "n_pre": 0}
                for cn in cut_names for ln in LANES}
        for g in vendors.values():
            for cn in cut_names:
                c = g["cuts"][cn]
                if not c["n_all"]:
                    continue
                ln = max(c["bucket_all"].items(), key=lambda kv: kv[1])[0]
                L = lane[(cn, ln)]
                L["n_recs"] += c["n_all"]
                L["n_pre"] += c["n_pre"]
                if c["w_$"] > 0 or c["n_w"]:
                    L["pool"] += c["w_$"]
                    L["vendors"].append(c["w_$"])
        for cn in cut_names:
            for ln in LANES:
                L = lane[(cn, ln)]
                if not L["n_recs"]:
                    continue
                shares = sorted((x / L["pool"] for x in L["vendors"] if x > 0),
                                reverse=True) if L["pool"] > 0 else []
                n_active = len([x for x in L["vendors"] if x > 0])
                score_rows.append({
                    "program": program, "cut": cn, "work_type": ln,
                    "pool_dollars_fy22_25_$M": round(L["pool"], 1),
                    "n_active_vendors": n_active,
                    "hhi_fy22_25": round(sum(s * s for s in shares), 4)
                        if shares else "",
                    "top1_share": round(shares[0], 4) if shares else "",
                    "top3_share": round(sum(shares[:3]), 4) if shares else "",
                    "n_records": L["n_recs"],
                    "pre_window_record_share": round(L["n_pre"] / L["n_recs"], 4),
                    "thin_lane": n_active < THIN_VENDORS or L["pool"] < THIN_POOL_M,
                })
        recon[program] = sum(L["pool"] for L in lane.values())

        # ---- vendor cut matrix --------------------------------------------------
        a, b = cut_names
        ca, cb = cut_cols
        for key, g in vendors.items():
            A, B = g["cuts"][a], g["cuts"][b]
            act_a = A["w_$"] > 0 or A["n_w"] > 0
            act_b = B["w_$"] > 0 or B["n_w"] > 0
            profile = ("both" if act_a and act_b
                       else f"{a}-only" if act_a
                       else f"{b}-only" if act_b
                       else "window-inactive")
            matrix_rows.append({
                "program": program,
                "vendor_uei": key,
                "vendor_name": max(g["names"].items(), key=lambda kv: kv[1])[0],
                "work_type": max(g["bucket_all"].items(), key=lambda kv: kv[1])[0],
                f"{ca}_dollars_fy22_25_$M": round(A["w_$"], 3),
                f"{ca}_n_awards_fy22_25": A["n_w"],
                f"{ca}_first_award": A["first"],
                f"{cb}_dollars_fy22_25_$M": round(B["w_$"], 3),
                f"{cb}_n_awards_fy22_25": B["n_w"],
                f"{cb}_first_award": B["first"],
                "cut_profile": profile,
                "_sort": A["w_$"] + B["w_$"],
            })

        # ---- PIID profile -------------------------------------------------------
        for piid, P in piid_stats.items():
            n = P["n_all"]
            status = ("none" if n == 0 else "very-thin" if n < 50
                      else "thin" if n < 300 else "usable" if n < 1500
                      else "robust")
            top = sorted(P["lane_$"].items(), key=lambda kv: -kv[1])[:2]
            m = P["meta"]
            piid_rows.append({
                "program": program, "piid": piid,
                "vessel_class": (m.get("class") or "").strip(),
                "builder": (m.get("group") or m.get("prime") or "").strip(),
                "label": (m.get("label") or "").strip(),
                "n_records_full_history": n,
                "supplier_dollars_fy22_25_$M": round(P["sup_w_$"], 1),
                "n_supplier_vendors_fy22_25": len(P["sup_vendors"]),
                "top_work_types_fy22_25": "; ".join(
                    f"{ln} ${d:,.1f}M" for ln, d in top),
                "data_status": status,
            })

    # ---- write -----------------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "class_cut_scorecard.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(score_rows[0].keys()))
        w.writeheader()
        w.writerows(score_rows)

    matrix_rows.sort(key=lambda r: (r["program"], -r.pop("_sort")))
    fields = []  # union across programs, program-stable order
    for r in matrix_rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    fields.remove("cut_profile")
    fields.append("cut_profile")
    with (OUT_DIR / "vendor_class_matrix.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, restval="")
        w.writeheader()
        w.writerows(matrix_rows)

    piid_rows.sort(key=lambda r: (r["program"], -r["n_records_full_history"]))
    with (OUT_DIR / "piid_profile.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(piid_rows[0].keys()))
        w.writeheader()
        w.writerows(piid_rows)

    # ---- console summary + reconciliation ---------------------------------------
    sc_path = OUT_DIR / "worktype_scorecard.csv"
    for program in ("submarines", "ddg"):
        _, cut_names, _ = CUTS[program]
        print(f"\n[{program}]")
        for cn in cut_names:
            rows = [r for r in score_rows
                    if r["program"] == program and r["cut"] == cn]
            pool = sum(r["pool_dollars_fy22_25_$M"] for r in rows)
            print(f"  {cn:<12} pool ${pool:>7,.1f}M across "
                  f"{len(rows)} lanes ({sum(1 for r in rows if r['thin_lane'])} thin)")
        prof = defaultdict(int)
        for r in matrix_rows:
            if r["program"] == program:
                prof[r["cut_profile"]] += 1
        print("  vendor overlap: "
              + ", ".join(f"{k}={v}" for k, v in sorted(prof.items())))
        if sc_path.exists():
            with sc_path.open(encoding="utf-8-sig", newline="") as fh:
                head = sum(float(r["pool_dollars_fy22_25_$M"] or 0)
                           for r in csv.DictReader(fh) if r["program"] == program)
            delta = recon[program] - head
            tag = "OK" if abs(delta) < 1.0 else "MISMATCH"
            print(f"  reconciliation vs worktype_scorecard: cut sum "
                  f"${recon[program]:,.1f}M vs headline ${head:,.1f}M -> {tag}")

    print(f"\nWrote class_cut_scorecard.csv ({len(score_rows)} rows), "
          f"vendor_class_matrix.csv ({len(matrix_rows)} rows), "
          f"piid_profile.csv ({len(piid_rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
