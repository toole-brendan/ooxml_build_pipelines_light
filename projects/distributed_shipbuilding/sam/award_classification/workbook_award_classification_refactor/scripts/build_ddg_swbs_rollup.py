"""build_ddg_swbs_rollup - the per-subsystem SWBS roll-up spine (one row per ship-system).

The SWBS analogue of a program-vendor sheet: one row per observed SWBS subsystem (plus a
U00 unmapped row), which the DDG SWBS by Ship-System sheet turns into per-FY constant-
FY2026$ roll-ups (date-bounded SUMIFS over the SWBS-tagged DDG transactions, keyed on
SWBS Subsystem, exactly like the program-vendor per-FY columns key on UEI). This script
only emits the row spine + the static ship-system labels; every dollar/count/date column
is a formula on the sheet, so the values stay blank here.

Subsystem universe = the distinct subsystems in the HII Work-Item SWBS Crosswalk (i.e.
every ship-system observed in the DDG-HII data), plus U00 for the unmapped tail.
Output: extracted/ddg_swbs_by_subsystem.csv.

Run (after build_swbs_crosswalk.py):
    python3 scripts/build_ddg_swbs_rollup.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # make sibling scripts importable
from build_swbs_crosswalk import (  # noqa: E402  (reuse the display / bucket logic)
    GROUP_NAME, load_hierarchy, swbs_display, major_bucket,
)

from _paths import REPO  # noqa: E402
EXTRACTED = (REPO / "projects/distributed_shipbuilding/sam/award_classification"
             / "workbook_award_classification_refactor/extracted")
XWALK_CSV = EXTRACTED / "hii_swbs_crosswalk.csv"
OUT_CSV = EXTRACTED / "ddg_swbs_by_subsystem.csv"

# Per-FY split, IN SYNC with the program-vendor sheets: ≤FY12 catch-all + FY2013..FY2026.
FY_COLUMNS = ["≤FY12 $M"] + [f"FY{y % 100} $M" for y in range(2013, 2027)]
HEADERS = ["SWBS Subsystem", "SWBS Major Group", "SWBS", "Subaward $M",
           "Published Subaward Records", "First Subaward", "Last Subaward", *FY_COLUMNS]

# major-group display order: 100..900, then X00, L00, U00
_ORDER = {f"{d}00": i for i, d in enumerate(range(1, 10))}
_ORDER.update({"X00": 9, "L00": 10, "U00": 11})


def build() -> None:
    hier = load_hierarchy()
    subs: list[str] = []
    seen: set[str] = set()
    with XWALK_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            sg = (r.get("SWBS Subsystem") or "").strip()
            if sg and sg not in seen:
                seen.add(sg)
                subs.append(sg)

    blanks = [""] * (4 + len(FY_COLUMNS))   # Subaward $M, Records, First, Last, + per-FY
    rows = []
    for sg in subs:
        mc, mn = major_bucket(sg)
        rows.append([sg, mc, swbs_display(sg, hier), *blanks])
    # the unmapped tail (HII rows whose code is absent from the crosswalk -> SWBS Subsystem "U00")
    rows.append(["U00", "U00", "U00 " + GROUP_NAME["U00"], *blanks])

    rows.sort(key=lambda x: (_ORDER.get(x[1], 99), x[0]))

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        w.writerows(rows)

    print("\n==== DDG SWBS by Ship-System (roll-up spine) ====")
    print(f"output: {OUT_CSV}")
    print(f"rows (subsystems + U00)           : {len(rows)}")
    print("all $/count/date columns are formulas on the sheet (blank here).")


if __name__ == "__main__":
    build()
