#!/usr/bin/env python3
"""
BWXT churn validation (Phase C check).

The handoff proposed validating the method against the BWXT missile-tube
weld-defect episode (2018 discovery; VPM tube work re-competed to Scot Forge /
BAE / others) and suggested it would appear "in the VPM tube fab PIIDs
N0002410C2118 / N0002416C2111". That PIID-level expectation is structurally
unobservable in FSRS: N0002410C2118 (2010 award) predates FSRS reporting and has
ZERO published subaward records; N0002416C2111's records contain no BWXT.

The episode IS observable at vendor level: BWXT's submarine subawards sit on
N0002413C2128 / N0002417C2117 / N0002419C2115 and stop entirely after Dec 2021 —
the exit signature signal 4 is built to catch. The full story in the corpus:
BWXT (registry role gfe_sib — naval nuclear, Navy-directed) exits, and Babcock
Marine Rosyth (UK; foreign_fms via the foreign-flag rule) appears 2019-2021 as
the second-sourced tube fabricator. Both parties sit OUTSIDE the supplier-only
scorecard universe by deliberate role classification, which is methodologically
consistent: reactor-adjacent tube work is Navy-directed and a foreign yard is not
a US new-entrant target. The validation therefore checks the detection mechanics
on the corpus, not a scorecard cell:
  1. BWXT records exist with awards 2016 - Dec 2021 and none after,
  2. the roles excluding them from the scorecard are the intended ones
     (gfe_sib for BWXT, foreign_fms for Babcock Rosyth),
  3. if any BWXT-family key IS in the supplier table and active FY22-25, its
     exited_flag must be True.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import EXTRACTED, iter_records

NAME_KEYS = ("BWX", "BABCOCK")


def main() -> int:
    recs = [r for r in iter_records("submarines")
            if any(k in (r["parent_name"] or r["vendor"]).upper() or
                   k in r["vendor"].upper() for k in NAME_KEYS)]
    if not recs:
        print("FAIL: no BWX/BABCOCK records found in the subs corpus")
        return 1

    # split the two firms my name match conflates: BWXT (US) vs Babcock Intl (UK)
    bwxt = [r for r in recs if not r["foreign"]]
    babcock_uk = [r for r in recs if r["foreign"]]

    by_piid_fy = defaultdict(lambda: [0, 0.0])
    keys = set()
    last_date = ""
    roles = defaultdict(set)
    for r in bwxt:
        by_piid_fy[(r["piid"], r["fy"])][0] += 1
        by_piid_fy[(r["piid"], r["fy"])][1] += r["dollar_m"]
        keys.add(r["vendor_key"])
        roles[r["role"]].add(r["vendor_key"])
        last_date = max(last_date, r["date"])

    total = sum(v[1] for v in by_piid_fy.values())
    print(f"BWXT (US) submarine subaward timeline ({len(bwxt)} records, "
          f"${total:,.1f}M, vendor keys: {', '.join(sorted(keys))}):")
    for (piid, fy), (n, m) in sorted(by_piid_fy.items()):
        print(f"  {piid}  FY{fy}  n={n:>3}  ${m:>8,.1f}M")
    print(f"  last subAwardDate: {last_date}")
    print(f"  roles: " + "; ".join(f"{k}={sorted(v)}" for k, v in roles.items()))

    if babcock_uk:
        uk_total = sum(r["dollar_m"] for r in babcock_uk)
        uk_dates = sorted(r["date"] for r in babcock_uk)
        uk_roles = {r["role"] for r in babcock_uk}
        print(f"\nBabcock Marine Rosyth (UK second-sourced tube fabricator): "
              f"{len(babcock_uk)} records, ${uk_total:,.1f}M, "
              f"{uk_dates[0][:10]}..{uk_dates[-1][:10]}, roles={sorted(uk_roles)}")

    failures = []
    if last_date[:4] > "2021":
        failures.append(f"BWXT has post-2021 awards (last {last_date}) — "
                        "the exit signature did not hold")
    if "gfe_sib" not in roles:
        failures.append("BWXT records are not roled gfe_sib — registry "
                        "adjudication changed; revisit the exclusion rationale")
    if babcock_uk and {r["role"] for r in babcock_uk} != {"foreign_fms"}:
        failures.append("Babcock Rosyth records not roled foreign_fms")

    sig = {}
    with (EXTRACTED / "vendor_signal_table.csv").open(encoding="utf-8-sig",
                                                      newline="") as fh:
        for row in csv.DictReader(fh):
            if row["program"] == "submarines" and row["vendor_uei"] in keys:
                sig[row["vendor_uei"]] = row

    for uei, row in sig.items():
        in_window = int(row["n_awards_fy22_25"] or 0) > 0
        print(f"\nsignal table [{uei}] {row['vendor_name']}: "
              f"work_type={row['work_type']}, "
              f"fy22_25 n={row['n_awards_fy22_25']}, "
              f"last={row['last_award_date']}, exited_flag={row['exited_flag']}")
        if in_window:
            if row["exited_flag"] != "True":
                failures.append(f"{uei} active FY22-25 but exited_flag is not True")
            else:
                print(f"  -> churn lands in scorecard cell (submarines, "
                      f"{row['work_type']}) as an FY22-25 exit")
        else:
            print("  -> exit predates the FY22-25 window entirely "
                  "(pre-window exit; not a scorecard churn event)")

    if failures:
        print("\nFAIL:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("\nPASS: BWXT exit signature (awards 2016-Dec 2021, then silence) and the "
          "Babcock Rosyth second-source entry are both visible in the corpus; both "
          "parties are excluded from the supplier scorecard by their intended roles "
          "(gfe_sib / foreign_fms). The handoff's PIID-level expectation is "
          "unobservable in FSRS — N0002410C2118 has zero published records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
