"""build_description_rerun_worklists - two plain xlsx files for a re-research pass.

Two SEPARATE, plain (default-Excel-styled) xlsx files - to be attached to a deep-research
AI agent with zero project context (the framing/instructions live in the prompt, not the
file). Each file spans all three programs in one sheet, with a leading Program column.

File 1 - weak / hedged descriptions: rows whose current Role / Description hedges instead
  of asserting a real role ("Likely...", "most plausibly tied", "Parent-company entry...",
  "no direct deliverable resolved", "input row names X while public traces...", etc.),
  EXCLUDING any row already captured by File 2 (clean partition, no UEI researched twice).
  Sorted by Program, then Subaward $ descending.

File 2 - duplicated shared-parent descriptions: every row in a group of >=2 subawardee-UEIs
  (same program) that carry byte-identical Role / Description text inherited from a shared
  parent corporation. Sorted by Program -> Parent Vendor Name -> Subaward $ descending so
  each shared-parent cluster sits together.

Output (projects/distributed_shipbuilding/sam/award_classification/):
    weak_description_research_worklist.xlsx
    duplicate_parent_description_research_worklist.xlsx
Run: python3 scripts/build_description_rerun_worklists.py
"""
from __future__ import annotations

import collections
import csv
from pathlib import Path

import xlsxwriter

from _paths import REPO  # noqa: E402
EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/extracted"
OUT_DIR = REPO / "projects/research_shared"

PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

# Hedge markers that signal "weak / I don't know / can't really say" prose.
HEDGES = [
    "likely", "most plausibly", "plausibly tied", "plausibly", "parent-company entry",
    "input row names", "public traces", "presumably", "appears to", "uncertain",
    "unclear", "cannot", "could not", "no public", "not clear", "unable",
    "best guess", "may supply", "might", "probably", "no specific", "no direct",
    "insufficient", "speculativ",
]

# (output header, source column in <program>_program_vendors.csv) - "Program" is injected.
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


def has_hedge(text: str) -> bool:
    t = text.lower()
    return any(h in t for h in HEDGES)


def load(program: str) -> list[dict]:
    with (EXTRACTED / f"{program}_program_vendors.csv").open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def classify(program: str) -> tuple[list[dict], list[dict]]:
    """Return (weak_not_dup, duplicated) row lists for one program."""
    rows = load(program)
    prose = [r for r in rows if (r.get("Role / Description") or "").strip()]

    # File 2: rows sharing byte-identical prose with >=1 sibling (shared parent).
    by_desc: dict[str, list[dict]] = collections.defaultdict(list)
    for r in prose:
        by_desc[r["Role / Description"].strip()].append(r)
    dup_ids: set[int] = set()
    duplicated: list[dict] = []
    for rs in by_desc.values():
        if len(rs) > 1:
            duplicated.extend(rs)
            dup_ids.update(id(r) for r in rs)

    # File 1: hedged prose NOT already captured by File 2.
    weak_not_dup = [
        r for r in prose
        if has_hedge(r["Role / Description"]) and id(r) not in dup_ids
    ]
    return weak_not_dup, duplicated


def write_workbook(path: Path, rows: list[dict]) -> None:
    wb = xlsxwriter.Workbook(str(path))           # default styling: no formats applied
    ws = wb.add_worksheet("Worklist")
    ws.write(0, 0, "Program")
    for c, (header, _src) in enumerate(COLUMNS, start=1):
        ws.write(0, c, header)
    for ri, r in enumerate(rows, start=1):
        ws.write(ri, 0, r["_program"])
        for c, (_header, src) in enumerate(COLUMNS, start=1):
            val = r.get(src, "")
            if src == "Subaward $M" and str(val).strip():
                ws.write_number(ri, c, round(float(val), 1))
            else:
                ws.write(ri, c, val)
    wb.close()


def build() -> None:
    weak_all: list[dict] = []
    dup_all: list[dict] = []
    for program, label in PROGRAMS:
        weak, dup = classify(program)
        for r in weak:
            r["_program"] = label
        for r in dup:
            r["_program"] = label
        # File 1 sort: Program, then $ desc.
        weak.sort(key=lambda r: -float(r["Subaward $M"] or 0))
        # File 2 sort: keep each shared-text cluster contiguous (the true grouping
        # invariant - a few siblings carry a blank/variant Parent Vendor Name string).
        # Order clusters by their largest member $ desc; rows within a cluster by $ desc.
        cluster_max: dict[str, float] = {}
        for r in dup:
            d = r["Role / Description"].strip()
            cluster_max[d] = max(cluster_max.get(d, 0.0), float(r["Subaward $M"] or 0))
        dup.sort(key=lambda r: (
            -cluster_max[r["Role / Description"].strip()],     # biggest clusters first
            r["Role / Description"].strip(),                   # determinism across ties
            -float(r["Subaward $M"] or 0),                     # $ desc within cluster
            r["Subawardee UEI"],                               # determinism
        ))
        weak_all.extend(weak)
        dup_all.extend(dup)

    f1 = OUT_DIR / "weak_description_research_worklist.xlsx"
    f2 = OUT_DIR / "duplicate_parent_description_research_worklist.xlsx"
    write_workbook(f1, weak_all)
    write_workbook(f2, dup_all)
    print(f"wrote {f1.name}  ({len(weak_all)} rows)")
    print(f"wrote {f2.name}  ({len(dup_all)} rows)")


if __name__ == "__main__":
    build()
