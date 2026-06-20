"""build_research_worklist - per-program AI-deep-research worklists (xlsxwriter).

Three SEPARATE, plain (default-Excel-styled) xlsx files - one per program - listing the
subawardee UEIs that still need an AI deep-research pull to bring each program's
*described* subaward dollars up to the 90%-of-program-$ cutoff. Per program: rank every
UEI by Subaward $M descending, walk the cumulative $ share until it crosses 90% (the
frontier), and list the frontier UEIs that DO NOT yet carry a Role / Description - in
that same $ order. Only the columns requested: UEI, vendor name, parent vendor name,
first/last subaward date, domestic/foreign, current NAICS-6 + title/status.

Output (projects/distributed_shipbuilding/sam/award_classification/):
    ddg_subaward_research_worklist.xlsx
    virginia_subaward_research_worklist.xlsx
    columbia_subaward_research_worklist.xlsx
Run: python3 scripts/build_research_worklist.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import xlsxwriter

REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/extracted"
OUT_DIR = REPO / "projects/research_shared"

PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]
CUTOFF = 0.90

# (output header, source column in <program>_program_vendors.csv)
COLUMNS = [
    ("Subawardee UEI",         "Subawardee UEI"),
    ("Vendor Name",            "Subawardee Vendor Name"),
    ("Parent Vendor Name",     "Parent Vendor Name"),
    ("First Subaward",         "First Subaward"),
    ("Last Subaward",          "Last Subaward"),
    ("Domestic or Foreign",    "Domestic or Foreign"),
    ("Current NAICS-6",        "Subawardee NAICS-6 (Primary)"),
    ("NAICS-6 Title / Status", "Subawardee NAICS-6 Description"),
]


def needs_research(program: str) -> list[dict]:
    """The 90%-frontier UEIs lacking a description, in Subaward $ descending order."""
    with (EXTRACTED / f"{program}_program_vendors.csv").open(encoding="utf-8-sig") as fh:
        rows = sorted(csv.DictReader(fh), key=lambda r: float(r["Subaward $M"]), reverse=True)
    total = sum(float(r["Subaward $M"]) for r in rows) or 1.0
    cum = 0.0
    out = []
    for r in rows:
        cum += float(r["Subaward $M"])
        if not (r.get("Role / Description") or "").strip():
            out.append(r)
        if cum / total >= CUTOFF:
            break
    return out


def build():
    for program, label in PROGRAMS:
        rows = needs_research(program)
        path = OUT_DIR / f"{program}_subaward_research_worklist.xlsx"
        wb = xlsxwriter.Workbook(str(path))           # default styling: no formats applied
        ws = wb.add_worksheet(label)
        for c, (header, _src) in enumerate(COLUMNS):
            ws.write(0, c, header)
        for ri, r in enumerate(rows, start=1):
            for c, (_header, src) in enumerate(COLUMNS):
                ws.write(ri, c, r.get(src, ""))
        wb.close()
        print(f"wrote {path.name}  ({len(rows)} vendors)")


if __name__ == "__main__":
    build()
