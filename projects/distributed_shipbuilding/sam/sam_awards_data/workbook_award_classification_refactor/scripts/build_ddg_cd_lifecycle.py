"""build_ddg_cd_lifecycle - the C/D family-level lifecycle CANDIDATE + ROLLUP spines.

For the family-level (grade C / D) DDG subawards - the ~$2.75B that maps only to a 5-7 hull MYP
block, not one ship - this expands each transaction across its full PIID candidate family and uses
the purchase date vs each hull's build windows (scripts/_lifecycle.py) to NARROW the candidate set
and stage-tag it. It never assigns a single hull (that stays the A/B job) and it never splits a
dollar across hulls (that would be allocation, not attribution - the wall, briefing §6).

Emits two materialized spines (every C/D row's hull family is re-derived with the shared
_hull_logic.resolve(); the narrowing with _lifecycle.narrow() - the same rule the lifecycle tagger
uses for the per-row tx columns, so the two are consistent):

  - ddg_cd_lifecycle_candidates.csv : one row per (C/D transaction x candidate hull) - the full
      family, so the kept hulls AND the excluded ones (with the reason) are both visible.
  - ddg_cd_lifecycle_rollup.csv     : one row per C/D transaction - the narrowed candidate set,
      stage consensus, narrowing result, and lifecycle confidence.

Run AFTER tag_ddg_transactions_lifecycle.py (and the SWBS/hull taggers it depends on):
    python3 scripts/tag_ddg_transactions_lifecycle.py
    python3 scripts/build_ddg_cd_lifecycle.py
"""
from __future__ import annotations

import csv
from collections import Counter

from _paths import EXTRACTED  # noqa: E402
from _hull_logic import load_map, hull_set, resolve  # noqa: E402
from _lifecycle import (  # noqa: E402
    load_milestones, narrow, parse_iso, hull_str, _hull_num,
    NR_SINGLE, NR_FEW, NR_FAMILY, NR_EXCEPTION, NR_NODATA,
)

TX_CSV = EXTRACTED / "ddg_subaward_transactions.csv"
CAND_CSV = EXTRACTED / "ddg_cd_lifecycle_candidates.csv"
ROLLUP_CSV = EXTRACTED / "ddg_cd_lifecycle_rollup.csv"

# Constant carried on every rollup row: the attribution-vs-allocation wall, stated in the data.
SCOPE_NOTE = "Evidence-based narrowing, not modeled allocation"

CAND_HEADERS = [
    "Subaward Report ID", "Prime PIID", "Original Hull Confidence", "Candidate Hull", "Builder",
    "Subaward Date", "Candidate Hull Stage on Date", "Window Match Flag", "Date Source Confidence",
    "Lifecycle Confidence", "Include as Timing Candidate?", "Reason",
]
ROLLUP_HEADERS = [
    "Subaward Report ID", "Prime PIID", "Builder", "Original Candidate Hulls", "Timing Candidate Hulls",
    "Timing Candidate Count", "Candidate Stages", "Stage Consensus Flag", "Narrowing Result",
    "Lifecycle Confidence", "Lifecycle Attribution Scope", "Assigned Hull",
]


def _yn(b: bool) -> str:
    return "TRUE" if b else "FALSE"


def build() -> None:
    fam_info = load_map()
    milestones = load_milestones()
    with TX_CSV.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    cand_rows: list[list] = []
    rollup_rows: list[list] = []
    nr_hist: Counter = Counter()
    nominal_by_bucket: Counter = Counter()   # nominal $ by narrowing result (sanity only; $ is live on the sheet)
    n_cd = 0

    for r in rows:
        piid = (r.get("Prime PIID") or "").strip()
        direct = hull_set(r.get("Direct Hull Text", ""))
        req = hull_set(r.get("Prime Requirement Hull Text", ""))
        _assigned, _scope, _basis, conf = resolve(piid, direct, req, fam_info)
        if conf not in ("C", "D"):
            continue
        n_cd += 1
        rid = (r.get("Subaward Report ID") or "").strip()
        builder = (r.get("Builder") or "").strip()
        sub_date = (r.get("Subaward Date") or "").strip()
        d = parse_iso(sub_date)
        family = fam_info.get(piid, {}).get("family", set())
        nr = narrow(family, d, milestones)

        for hull, stage, match, dc, reason in nr.candidates:
            cand_rows.append([
                rid, piid, conf, f"DDG {hull}", builder, sub_date, stage, _yn(match), dc,
                nr.lifecycle_confidence, _yn(match), reason,
            ])

        rollup_rows.append([
            rid, piid, builder, hull_str(family), hull_str(nr.timing_hulls),
            nr.count, " / ".join(nr.stages), _yn(nr.consensus), nr.narrowing_result,
            nr.lifecycle_confidence, SCOPE_NOTE, "",
        ])
        nr_hist[nr.narrowing_result] += 1
        try:
            nominal_by_bucket[nr.narrowing_result] += float((r.get("Subaward Amount $") or "0").replace(",", ""))
        except ValueError:
            pass

    cand_rows.sort(key=lambda x: (x[0], _hull_num(x[3])))
    rollup_rows.sort(key=lambda x: (x[1], x[0]))

    with CAND_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CAND_HEADERS)
        w.writerows(cand_rows)
    with ROLLUP_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(ROLLUP_HEADERS)
        w.writerows(rollup_rows)

    print("\n==== DDG C/D lifecycle candidate + rollup spines ====")
    print(f"candidates : {CAND_CSV}  ({len(cand_rows)} rows = C/D tx x family hull)")
    print(f"rollup     : {ROLLUP_CSV}  ({len(rollup_rows)} C/D transactions)")
    print(f"C/D transactions                  : {n_cd}")
    print("narrowing result (count | nominal $M):")
    for bucket in (NR_SINGLE, NR_FEW, NR_FAMILY, NR_EXCEPTION, NR_NODATA):
        if nr_hist.get(bucket):
            print(f"    {bucket:<28}: {nr_hist[bucket]:>5}  | ${nominal_by_bucket[bucket] / 1e6:>9.1f}M")
    print("(nominal $ is a sanity print; the workbook splits constant FY2026$ live via SUMIFS.)")
    print("No per-hull dollar split is emitted - narrowing is attribution, not allocation (the wall).")


if __name__ == "__main__":
    build()
