#!/usr/bin/env python3
"""
Build the ranked vendor/award target list from the scorecard + signal table (Phase E).

Lane gates (explicit, simple, documented in the memo):
  COMPETABLE       hhi < 0.15 (prime demonstrably multi-sources) OR
                   credible_entrant_rate > 0.03 (door demonstrably open). The
                   credible rate counts only first-reporters at or under $25M of
                   window dollars — larger "entrants" (GE $333M, Timken $169M on
                   DDG machining) are reporting onsets or renames of incumbents,
                   not entries. Also requires pre_fy22_record_share >= 0.15 (thin
                   pre-window history censors first-award dating entirely).
  SEEDED           barrier_score == 5 AND seeding_evidence_count >= 1
                   (locked today; active seeding = long qualification path)
  COMPONENT-TIER   hhi >= 0.30 but with an entrant cohort (n_new_entrants >= 5):
                   top tier locked, component tier moving
  LOCKED           everything else
The unbucketed lane is never gated competable (registry-cleanup queue).

Within gated lanes, vendors rank by FY22-25 dollars. Each vendor row carries its
award history shape (n awards, cadence, first/last dates, PIIDs) — the PIID list
IS the named-competable-awards column. status: entrant (first award FY22-25),
exited (active in window, silent >= 18 trailing months), else incumbent.

Output: extracted/target_list.csv + console summary of lane gates.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import OUT_DIR, UNBUCKETED

TOP_N_PER_LANE = 10


def gate(row) -> str:
    if row["work_type"] == UNBUCKETED:
        return "LOCKED"
    hhi = float(row["hhi_fy22_25"] or 1)
    cred_rate = float(row["credible_entrant_rate"] or 0)
    barrier = int(row["barrier_score"]) if row["barrier_score"] else 0
    seeding = int(row["seeding_evidence_count"] or 0)
    cred_entrants = int(row["n_credible_entrants"] or 0)
    censored = float(row["pre_fy22_record_share"] or 0) < 0.15
    # ordering matters: a concentrated lane never reads plain COMPETABLE off the
    # entrant arm alone — it lands SEEDED (hard-barrier lanes under active seeding)
    # or COMPONENT-TIER (top tier locked, component tier moving) instead.
    if hhi < 0.15 or (cred_rate > 0.03 and hhi < 0.30 and not censored):
        return "COMPETABLE"
    if barrier == 5 and seeding >= 1:
        return "SEEDED"
    if hhi >= 0.30 and not censored and (cred_entrants >= 5 or cred_rate > 0.03):
        return "COMPONENT-TIER"
    return "LOCKED"


def why(row, lane_gate) -> str:
    bits = []
    hhi = float(row["hhi_fy22_25"] or 0)
    if hhi and hhi < 0.15:
        bits.append(f"fragmented lane (HHI {hhi:.2f})")
    er = float(row["credible_entrant_rate"] or 0)
    censored = float(row["pre_fy22_record_share"] or 0) < 0.15
    if er > 0.03 and not censored:
        bits.append(f"{row['n_credible_entrants']} credible entrants took "
                    f"{er:.0%} of FY22-25 lane dollars")
    elif er > 0.03 and censored:
        bits.append("entrant signal censored (thin pre-FY22 history)")
    if lane_gate == "SEEDED":
        bits.append("locked incumbents but active Navy/BFA seeding "
                    f"({row['seeding_evidence_count']} evidence items)")
    if lane_gate == "COMPONENT-TIER":
        bits.append("top tier locked; component tier shows entry "
                    f"({row['n_new_entrants_fy22_25']} entrants)")
    if row["median_cadence_days"]:
        bits.append(f"median re-buy {row['median_cadence_days']}d")
    return "; ".join(bits)


def main() -> int:
    with (OUT_DIR / "worktype_scorecard.csv").open(encoding="utf-8-sig", newline="") as fh:
        scorecard = list(csv.DictReader(fh))
    with (OUT_DIR / "vendor_signal_table.csv").open(encoding="utf-8-sig", newline="") as fh:
        vendors = list(csv.DictReader(fh))

    gates = {(r["program"], r["work_type"]): gate(r) for r in scorecard}
    score_by = {(r["program"], r["work_type"]): r for r in scorecard}

    print("Lane gates:")
    for r in scorecard:
        g = gates[(r["program"], r["work_type"])]
        if r["work_type"] != UNBUCKETED:
            print(f"  {r['program']:<11} {r['work_type']:<12} {g:<15} "
                  f"pool=${float(r['pool_dollars_fy22_25_$M']):>7,.1f}M  "
                  f"hhi={r['hhi_fy22_25']:<7} entrant_rate={r['entrant_rate']}")

    out_rows = []
    for (program, ln), g in gates.items():
        if g == "LOCKED":
            continue
        lane_vendors = [v for v in vendors
                        if v["program"] == program and v["work_type"] == ln
                        and float(v["dollars_fy22_25_$M"] or 0) > 0]
        lane_vendors.sort(key=lambda v: -float(v["dollars_fy22_25_$M"]))
        srow = score_by[(program, ln)]
        for rank, v in enumerate(lane_vendors[:TOP_N_PER_LANE], start=1):
            if v["is_new_entrant_fy22_25"] == "True":
                status = ("entrant" if float(v["dollars_fy22_25_$M"]) <= 25.0
                          else "reported-entrant (likely incumbent)")
            elif v["exited_flag"] == "True":
                status = "exited"
            else:
                status = "incumbent"
            out_rows.append({
                "program": program, "work_type": ln, "lane_gate": g, "rank": rank,
                "vendor_name": v["vendor_name"], "vendor_uei": v["vendor_uei"],
                "status": status,
                "dollars_fy22_25_$M": v["dollars_fy22_25_$M"],
                "n_awards_fy22_25": v["n_awards_fy22_25"],
                "median_interaward_days": v["median_interaward_days"],
                "first_award_fy": v["first_award_fy"],
                "last_award_date": v["last_award_date"],
                "also_active_other_program": v["also_active_other_program"],
                "piids": v["piids"],
                "why_competable": why(srow, g),
            })

    out = OUT_DIR / "target_list.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nWrote {out} ({len(out_rows)} rows across "
          f"{len({(r['program'], r['work_type']) for r in out_rows})} gated lanes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
