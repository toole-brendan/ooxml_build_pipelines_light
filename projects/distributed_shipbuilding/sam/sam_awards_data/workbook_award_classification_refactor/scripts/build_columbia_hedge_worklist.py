"""build_columbia_hedge_worklist - 2nd-pass re-research worklist for Columbia.

A single plain (default-Excel-styled) xlsx listing the Columbia rows whose first AI
deep-research pull came back HEDGED - it gives a generic company capability but states the
specific Columbia-class deliverable could not be confirmed ("A specific Columbia ... could
not be confirmed", "public sources do not identify the exact Columbia ..."). Scope is
restricted to UEIs that came from the Columbia research pull (extracted/columbia_subaward_
research_results.csv), so this set is disjoint from the cross-program weak/duplicate
worklists built earlier from the pre-ingest prose.

Columns are the same bare-bones identity set used by the earlier worklists, plus the
Current Role / Description (the hedged text to be replaced). Sorted by Subaward $ desc.

Output (projects/distributed_shipbuilding/sam/sam_awards_data/):
    columbia_hedge_rerun_worklist.xlsx
Run: python3 scripts/build_columbia_hedge_worklist.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import xlsxwriter

from _paths import REPO  # noqa: E402
EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor/extracted"
OUT_DIR = REPO / "projects/research_shared"

# Markers of an unconfirmed Columbia-specific deliverable in the research prose. These
# capture both the leading punt ("...could not be confirmed") and the appended caveat
# ("...do not identify the exact/specific Columbia ..."). The clean rows assert a concrete
# Columbia role and match none of these.
HEDGES = [
    "could not be confirmed", "cannot be confirmed", "could not confirm",
    "could not be determined", "do not identify", "does not identify",
    "does not publicly identify", "not publicly identify", "no confirmed",
]

COLUMNS = [
    ("Subawardee UEI",          "Subawardee UEI"),
    ("Vendor Name",             "Subawardee Vendor Name"),
    ("Parent Vendor Name",      "Parent Vendor Name"),
    ("Current NAICS-6",         "Subawardee NAICS-6 (Primary)"),
    ("NAICS-6 Title / Status",  "Subawardee NAICS-6 Description"),
    ("Subaward $M",             "Subaward $M"),
    ("First Subaward",          "First Subaward"),
    ("Last Subaward",           "Last Subaward"),
    ("Domestic or Foreign",     "Domestic or Foreign"),
    ("Current Role / Description", "Role / Description"),
]


def is_hedged(text: str) -> bool:
    t = text.lower()
    return any(h in t for h in HEDGES)


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def build() -> None:
    research_ueis = {r["Subawardee UEI"] for r in load(EXTRACTED / "columbia_subaward_research_results.csv")}
    rows = load(EXTRACTED / "columbia_program_vendors.csv")
    hedged = [
        r for r in rows
        if r["Subawardee UEI"] in research_ueis and is_hedged(r.get("Role / Description") or "")
    ]
    hedged.sort(key=lambda r: -float(r["Subaward $M"] or 0))

    path = OUT_DIR / "columbia_hedge_rerun_worklist.xlsx"
    wb = xlsxwriter.Workbook(str(path))           # default styling: no formats applied
    ws = wb.add_worksheet("Columbia")
    for c, (header, _src) in enumerate(COLUMNS):
        ws.write(0, c, header)
    for ri, r in enumerate(hedged, start=1):
        for c, (_header, src) in enumerate(COLUMNS):
            val = r.get(src, "")
            if src == "Subaward $M" and str(val).strip():
                ws.write_number(ri, c, round(float(val), 1))
            else:
                ws.write(ri, c, val)
    wb.close()
    print(f"wrote {path.name}  ({len(hedged)} rows)")


if __name__ == "__main__":
    build()
