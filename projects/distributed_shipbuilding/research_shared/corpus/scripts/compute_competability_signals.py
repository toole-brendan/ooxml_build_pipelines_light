#!/usr/bin/env python3
"""
Compute competability signals 1-4 per work type per program (Phase C).

Universe: role == "supplier" records only (prime/co_prime/gfe_sib/service/holding/
mission_systems/foreign_fms are outside the competable substrate), in-scope PIIDs,
deduped on subAwardReportId. Vendor key = subParentUei else subEntityUei; each
vendor is assigned its dollar-weighted modal work type (vendors are classified at
the entity level, so bucket splits within one key are registry-vs-fallback edge
cases — the modal assignment keeps one lane per vendor).

Windows: FY22-25 (subAwardDate) for levels; FULL HISTORY for first-ever-award
dating (signal 3) and cadence (signal 4) — this is why the fullhistory corpora are
the substrate.

Documented parameter defaults (also surfaced in the findings memo):
  - New entrant = vendor whose first-ever subaward in THIS program falls in
    FY22-25. `also_active_other_program` flags cross-program incumbents.
  - Exit = vendor active in FY22-25, >=2 lifetime awards, whose last award is
    >= EXIT_TRAILING_MONTHS (18) before the program corpus end date. FFATA filing
    lag (6-18 months) means recent "exits" can be reporting lag — floors caveat.
  - HHI on FY22-25 dollar shares within (program, work_type); top-1/top-3 share
    reported alongside (HHI is floor-biased by FSRS undercount).

Outputs (extracted/): vendor_signal_table.csv, worktype_scorecard.csv,
entrant_cohorts.csv. Signal-5 columns (barrier, seeding) join from
barrier_scores.csv / seeding_evidence.csv when present (Phase D).
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import (BUCKET_KEYS, EXTRACTED, FY22_25, OUT_DIR, UNBUCKETED,
                     in_window, iter_records, load_enrichment, load_registry)

EXIT_TRAILING_MONTHS = 18
# Headline (2022, 2025); COMP_WINDOW overrides for sensitivity runs. Column
# names stay fy22_25/pre_fy22 regardless — under an override they mean
# "window" / "pre-window".
FY_LO, FY_HI = FY22_25
LANES = BUCKET_KEYS + [UNBUCKETED]

# A "first award in FY22-25" vendor with more than this in window dollars is far
# more likely a reporting onset (or rename/novation) of a long-time incumbent than
# a true entrant — GE first-reports on DDG machining in FY22 at $333M; Timken Gears
# & Services is Philadelphia Gear renamed. The credible-entrant signal counts only
# first-reporters at or under the cap.
ENTRANT_CREDIBILITY_CAP_M = 25.0


def _d(s):
    try:
        return date.fromisoformat(s[:10])
    except (ValueError, TypeError):
        return None


def collect(program: str, registry, vendors_other: set | None):
    """Per-vendor rollup for one program. Returns (vendor dicts, corpus_end)."""
    v = {}
    corpus_end = None
    for rec in iter_records(program, registry=registry):
        if rec["role"] != "supplier":
            continue
        d = _d(rec["date"])
        if d and (corpus_end is None or d > corpus_end):
            corpus_end = d
        key = rec["vendor_key"]
        g = v.get(key)
        if g is None:
            g = v[key] = {
                "vendor_uei": key, "names": defaultdict(float),
                "bucket_dollars": defaultdict(float),
                "dates": [], "dollars_all": 0.0, "n_all": 0, "n_pre22": 0,
                "dollars_w": 0.0, "n_w": 0, "piids": set(), "basis": rec["basis"],
            }
        name = rec["parent_name"] or rec["vendor"]
        g["names"][name.upper()] += rec["dollar_m"]
        g["bucket_dollars"][rec["bucket"]] += rec["dollar_m"]
        if d:
            g["dates"].append(d)
        g["dollars_all"] += rec["dollar_m"]
        g["n_all"] += 1
        g["piids"].add(rec["piid"])
        if rec["fy"] is not None and rec["fy"] < FY_LO:
            g["n_pre22"] += 1
        if in_window(rec, FY_LO, FY_HI):
            g["dollars_w"] += rec["dollar_m"]
            g["n_w"] += 1
    return v, corpus_end


def fy_of_date(d: date) -> int:
    return d.year + 1 if d.month >= 10 else d.year


def main() -> int:
    registry = load_registry()
    per_program = {}
    for program in ("submarines", "ddg"):
        per_program[program] = collect(program, registry, None)

    vendor_rows = []
    cohort = defaultdict(lambda: [0, 0.0])  # (program, lane, fy) -> [n, $]
    score = {}

    for program, (vendors, corpus_end) in per_program.items():
        other = set(per_program["ddg" if program == "submarines" else "submarines"][0])
        exit_cutoff = corpus_end - timedelta(days=EXIT_TRAILING_MONTHS * 30)
        # lane aggregates
        lane = {ln: {"pool": 0.0, "vendors": [], "entrants": 0, "entrant_$": 0.0,
                     "entrants_cred": 0, "entrant_$_cred": 0.0,
                     "exits": 0, "cadences": [], "n_pre22": 0, "n_recs": 0}
                for ln in LANES}

        for g in vendors.values():
            lane_key = max(g["bucket_dollars"].items(), key=lambda kv: kv[1])[0]
            dates = sorted(g["dates"])
            first, last = (dates[0], dates[-1]) if dates else (None, None)
            first_fy = fy_of_date(first) if first else None
            gaps = [(b - a).days for a, b in zip(dates, dates[1:]) if (b - a).days > 0]
            med_gap = statistics.median(gaps) if gaps else None
            max_gap = max(gaps) if gaps else None
            is_entrant = first_fy is not None and FY_LO <= first_fy <= FY_HI
            active = g["dollars_w"] > 0 or g["n_w"] > 0
            exited = (active and g["n_all"] >= 2 and last is not None
                      and last < exit_cutoff)
            name = max(g["names"].items(), key=lambda kv: kv[1])[0]

            vendor_rows.append({
                "program": program, "work_type": lane_key,
                "vendor_uei": g["vendor_uei"], "vendor_name": name,
                "basis": g["basis"],
                "n_awards_fy22_25": g["n_w"],
                "dollars_fy22_25_$M": round(g["dollars_w"], 3),
                "n_awards_all": g["n_all"],
                "dollars_all_$M": round(g["dollars_all"], 3),
                "first_award_date": first.isoformat() if first else "",
                "first_award_fy": first_fy or "",
                "last_award_date": last.isoformat() if last else "",
                "is_new_entrant_fy22_25": is_entrant,
                "also_active_other_program": g["vendor_uei"] in other,
                "median_interaward_days": med_gap if med_gap is not None else "",
                "max_gap_days": max_gap if max_gap is not None else "",
                "exited_flag": exited,
                "n_piids": len(g["piids"]),
                "piids": ";".join(sorted(g["piids"])),
            })

            L = lane[lane_key]
            L["n_pre22"] += g["n_pre22"]
            L["n_recs"] += g["n_all"]
            if active:
                L["pool"] += g["dollars_w"]
                L["vendors"].append(g["dollars_w"])
                if is_entrant:
                    L["entrants"] += 1
                    L["entrant_$"] += g["dollars_w"]
                    if g["dollars_w"] <= ENTRANT_CREDIBILITY_CAP_M:
                        L["entrants_cred"] += 1
                        L["entrant_$_cred"] += g["dollars_w"]
                if exited:
                    L["exits"] += 1
                if med_gap is not None:
                    L["cadences"].append(med_gap)

        for ln, L in lane.items():
            shares = sorted((x / L["pool"] for x in L["vendors"] if x > 0),
                            reverse=True) if L["pool"] > 0 else []
            n_active = len([x for x in L["vendors"] if x > 0])
            score[(program, ln)] = {
                "program": program, "work_type": ln,
                "pool_dollars_fy22_25_$M": round(L["pool"], 1),
                "n_active_vendors": n_active,
                "hhi_fy22_25": round(sum(s * s for s in shares), 4) if shares else "",
                "top1_share": round(shares[0], 4) if shares else "",
                "top3_share": round(sum(shares[:3]), 4) if shares else "",
                "n_new_entrants_fy22_25": L["entrants"],
                "new_entrant_dollars_$M": round(L["entrant_$"], 1),
                "entrant_rate": round(L["entrant_$"] / L["pool"], 4) if L["pool"] else "",
                "n_credible_entrants": L["entrants_cred"],
                "credible_entrant_dollars_$M": round(L["entrant_$_cred"], 1),
                "credible_entrant_rate": round(L["entrant_$_cred"] / L["pool"], 4)
                    if L["pool"] else "",
                "median_cadence_days": round(statistics.median(L["cadences"]))
                    if L["cadences"] else "",
                "n_exits_fy22_25": L["exits"],
                "churn_ratio": round((L["entrants"] + L["exits"]) / n_active, 4)
                    if n_active else "",
                # entrant-signal censoring diagnostic: share of lane records dated
                # before FY22. Thin pre-window history means "first award FY22-25"
                # cannot distinguish a true entrant from a newly-reported incumbent.
                "n_records_pre_fy22": L["n_pre22"],
                "pre_fy22_record_share": round(L["n_pre22"] / L["n_recs"], 4)
                    if L["n_recs"] else "",
            }

    # entrant cohorts: per (program, lane, entry FY) vendor counts; dollars column
    # carries window dollars for in-window entrants only (per-award first-FY dollars
    # would need amounts threaded by date, which the signal table doesn't carry)
    for r in vendor_rows:
        fy = r["first_award_fy"]
        if not fy:
            continue
        key = (r["program"], r["work_type"], fy)
        cohort[key][0] += 1
        if r["is_new_entrant_fy22_25"]:
            cohort[key][1] += r["dollars_fy22_25_$M"]

    # ---- signal 5 join (Phase D files, when present) -------------------------
    barrier = {}
    bpath = EXTRACTED / "barrier_scores.csv"
    if bpath.exists():
        with bpath.open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                barrier[r["work_type"]] = r["barrier_score"]
    seeding = defaultdict(int)
    spath = EXTRACTED / "seeding_evidence.csv"
    if spath.exists():
        with spath.open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                seeding[(r["program"], r["work_type"])] += 1
    for (program, ln), row in score.items():
        row["barrier_score"] = barrier.get(ln, "")
        row["seeding_evidence_count"] = (seeding.get((program, ln), 0)
                                         + seeding.get(("both", ln), 0)) if seeding else ""

    # ---- write ----------------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    vendor_rows.sort(key=lambda r: (r["program"], r["work_type"],
                                    -r["dollars_fy22_25_$M"]))
    with (OUT_DIR / "vendor_signal_table.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(vendor_rows[0].keys()))
        w.writeheader()
        w.writerows(vendor_rows)

    srows = [score[k] for k in sorted(score)]
    with (OUT_DIR / "worktype_scorecard.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(srows[0].keys()))
        w.writeheader()
        w.writerows(srows)

    with (OUT_DIR / "entrant_cohorts.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["program", "work_type", "first_award_fy", "n_first_time_vendors",
                    "entrant_window_dollars_$M"])
        for (program, ln, fy), (n, dollars) in sorted(cohort.items()):
            w.writerow([program, ln, fy, n, round(dollars, 3)])

    # ---- console summary + reconciliation --------------------------------------
    for program in ("submarines", "ddg"):
        tot = sum(r["pool_dollars_fy22_25_$M"] for (p, ln), r in score.items()
                  if p == program)
        print(f"\n[{program}] FY{FY_LO % 100}-{FY_HI % 100} supplier pool ${tot:,.0f}M  "
              f"(corpus end {per_program[program][1]})")
        for ln in LANES:
            r = score[(program, ln)]
            if not r["n_active_vendors"]:
                continue
            print(f"  {ln:<12} ${r['pool_dollars_fy22_25_$M']:>7,.1f}M  "
                  f"vendors={r['n_active_vendors']:>3}  hhi={r['hhi_fy22_25']:<7} "
                  f"top1={r['top1_share']:<7} entrants={r['n_new_entrants_fy22_25']:>2} "
                  f"(${r['new_entrant_dollars_$M']:,.1f}M)  exits={r['n_exits_fy22_25']:>2}  "
                  f"cadence={r['median_cadence_days']}d")
    print(f"\nWrote vendor_signal_table.csv ({len(vendor_rows)} rows), "
          f"worktype_scorecard.csv ({len(srows)} rows), entrant_cohorts.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
