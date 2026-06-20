"""build_capability_domain_worklists - per-program Capability Domain assignment worklists.

Three SEPARATE, plain (default-Excel-styled) xlsx files - one per program - for a zero-
context AI agent to assign ONE Capability Domain archetype (D1-D10 / D0) to every row that
already carries a Role / Description. Capability Domain is a pure technical-area axis,
inferred from the work description + NAICS, so the worklist carries only those signals.

Each workbook has two sheets:
  <Program>                - the rows to classify: UEI, Vendor Name, NAICS-6 + title,
                            Role / Description, then empty Capability Domain (D) + Basis.
  Capability Domain Codes  - the controlled vocabulary (D1-D10, D0) + boundary tie-breaks,
                            so the prompt can stay short and the agent can't invent codes.

Output (projects/distributed_shipbuilding/sam/award_classification/):
    ddg_capability_domain_worklist.xlsx
    virginia_capability_domain_worklist.xlsx
    columbia_capability_domain_worklist.xlsx
Run: python3 scripts/build_capability_domain_worklists.py
"""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import xlsxwriter

REFACTOR = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light"
                "/projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor")
EXTRACTED = REFACTOR / "extracted"
OUT_DIR = REFACTOR.parent  # projects/research_shared

PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

# import DOMAINS / DOMAIN_TIEBREAKS straight from the taxonomy leaf (single source of
# truth) without triggering the package __init__ / workbook_core.
_spec = importlib.util.spec_from_file_location(
    "_taxonomy_leaf", REFACTOR / "workbook_award_classification_refactor/sheets/_taxonomy.py")
_tax = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tax)
DOMAINS, DOMAIN_TIEBREAKS = _tax.DOMAINS, _tax.DOMAIN_TIEBREAKS

# (worklist header, source col in <program>_program_vendors.csv); "" = empty to fill
COLUMNS = [
    ("Subawardee UEI",          "Subawardee UEI"),
    ("Vendor Name",             "Subawardee Vendor Name"),
    ("NAICS-6",                 "Subawardee NAICS-6 (Primary)"),
    ("NAICS-6 Title / Status",  "Subawardee NAICS-6 Description"),
    ("Role / Description",      "Role / Description"),
    ("Capability Domain (D)",   ""),
    ("Capability Domain Basis", ""),
]


def load_rows(program: str) -> list[dict]:
    with (EXTRACTED / f"{program}_program_vendors.csv").open(encoding="utf-8-sig") as fh:
        rows = [r for r in csv.DictReader(fh) if (r.get("Role / Description") or "").strip()]
    rows.sort(key=lambda r: -float(r["Subaward $M"] or 0))
    return rows


def write_codes_sheet(ws) -> None:
    ws.write(0, 0, "Code")
    ws.write(0, 1, "Capability Domain")
    ws.write(0, 2, "Definition")
    r = 1
    for code, name, defn in DOMAINS:
        ws.write(r, 0, code); ws.write(r, 1, name); ws.write(r, 2, defn)
        r += 1
    r += 1
    ws.write(r, 0, "Boundary tie-breaks"); r += 1
    for situation, rule in DOMAIN_TIEBREAKS:
        ws.write(r, 0, situation); ws.write(r, 2, rule)
        r += 1


def build() -> None:
    for program, label in PROGRAMS:
        rows = load_rows(program)
        path = OUT_DIR / f"{program}_capability_domain_worklist.xlsx"
        wb = xlsxwriter.Workbook(str(path))           # default styling: no formats applied
        ws = wb.add_worksheet(label)
        for c, (header, _src) in enumerate(COLUMNS):
            ws.write(0, c, header)
        for ri, r in enumerate(rows, start=1):
            for c, (_header, src) in enumerate(COLUMNS):
                if src:
                    ws.write(ri, c, r.get(src, ""))
        write_codes_sheet(wb.add_worksheet("Capability Domain Codes"))
        wb.close()
        print(f"wrote {path.name}  ({len(rows)} rows)")


if __name__ == "__main__":
    build()
