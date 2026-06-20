#!/usr/bin/env python3
"""
Validate the DDG full-history SAM.gov pull against the windowed corpus.

Checks per PIID:
  1. subAwardReportId dedupe (expect 0 duplicates, matching the submarines corpus).
  2. Reconciliation: every windowed sam_subawards/ subAwardReportId must appear in
     the fullhistory published (or deleted) set. Set-coverage, not date-window
     counts — the API's fromDate/toDate filter on the FILING date (submittedDate),
     not subAwardDate, so windowed pulls legitimately contain pre-window action
     dates. Any truly-missing ID means the piid filter was dropped or the pull
     truncated — hard fail.
  3. Flag 0-record PIIDs (expected for pre-FSRS contracts, ~pre-2011; flag
     N0002423C2305 specifically as FFATA-lag if still 0).

Read-only. Writes sam_subawards_fullhistory/_validation.json and prints a table.
Exit code 1 on any hard failure.
"""
import json
import os
import sys

PROJECT_ROOT = "/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/distributed_shipbuilding/tam/ddg/research"
FULL_DIR = os.path.join(PROJECT_ROOT, "sam_subawards_fullhistory")
WINDOWED_DIR = os.path.join(PROJECT_ROOT, "sam_subawards")
WINDOW_FLOOR = "2017-10-01"  # the windowed pull's fromDate
LAG_WATCH = {"N0002423C2305"}  # BIW FY23 construction — possibly empty from FFATA lag


def main():
    results = {}
    failures = []
    files = sorted(f for f in os.listdir(FULL_DIR)
                   if f.endswith("_subawards.json"))
    if not files:
        print("No fullhistory files found.")
        return 1

    print(f"{'PIID':<16}{'full':>7}{'dupes':>7}{'missing':>9}{'windowed':>10}{'recon':>7}  "
          f"{'$M':>10}  {'date range':<23}")
    for fn in files:
        piid = fn.replace("_subawards.json", "")
        with open(os.path.join(FULL_DIR, fn)) as f:
            full = json.load(f)
        pub = full.get("published") or []
        ids = [r.get("subAwardReportId") for r in pub if r.get("subAwardReportId")]
        dupes = len(ids) - len(set(ids))
        dates = sorted(r.get("subAwardDate") or "" for r in pub if r.get("subAwardDate"))
        total_m = sum(float(r.get("subAwardAmount") or 0) for r in pub) / 1e6
        full_ids = set(ids) | {r.get("subAwardReportId")
                               for r in (full.get("deleted") or [])}

        win_path = os.path.join(WINDOWED_DIR, fn)
        win_count = None
        n_missing = 0
        recon = "n/a"
        if os.path.exists(win_path):
            with open(win_path) as f:
                win = json.load(f)
            win_ids = {r.get("subAwardReportId") for r in (win.get("published") or [])}
            win_count = len(win_ids)
            n_missing = len(win_ids - full_ids)
            recon = "OK" if n_missing == 0 else "FAIL"
            if recon == "FAIL":
                failures.append(f"{piid}: {n_missing} windowed subAwardReportIds absent from fullhistory")

        flags = []
        if dupes:
            flags.append("dupes")
            failures.append(f"{piid}: {dupes} duplicate subAwardReportId")
        if not pub:
            flags.append("FFATA-lag?" if piid in LAG_WATCH else "empty (pre-FSRS?)")

        drange = f"{dates[0][:10]}..{dates[-1][:10]}" if dates else "-"
        print(f"{piid:<16}{len(pub):>7}{dupes:>7}{n_missing:>9}"
              f"{win_count if win_count is not None else '-':>10}{recon:>7}  "
              f"{total_m:>10,.1f}  {drange:<23}"
              + ("  [" + ", ".join(flags) + "]" if flags else ""))

        results[piid] = {
            "published_count": len(pub),
            "duplicate_subAwardReportId": dupes,
            "windowed_ids_missing_from_fullhistory": n_missing,
            "windowed_count": win_count,
            "reconciliation": recon,
            "published_total_$M": round(total_m, 3),
            "date_min": dates[0] if dates else None,
            "date_max": dates[-1] if dates else None,
            "flags": flags,
        }

    out = {"window_floor": WINDOW_FLOOR, "n_piids": len(files),
           "failures": failures, "piids": results}
    with open(os.path.join(FULL_DIR, "_validation.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n{len(files)} PIIDs validated; {len(failures)} hard failure(s).")
    for msg in failures:
        print(f"  FAIL: {msg}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
