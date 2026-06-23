"""build_supplier_master - the single per-(UEI x program) supplier dimension pull.

Produces ONE (subawardee UEI x program) dimension CSV - the Supplier Master - that merges
what used to be two independently-materialized sheets (subawardee_uei_index + subawardee_
parents). Independent refreshes were the cause of the dimension-universe drift, so there is
now one source for the supplier attributes the program-vendor sheets look up:

    supplier_master.csv  - Key (Program|UEI) | Program | UEI | Vendor Name | Primary NAICS-6 |
                           NAICS-6 desc | Parent UEI (dollar-modal standardized) | Parent
                           Vendor Name | Parent UEI(s) (raw set)

(There is deliberately no domestic/foreign column: that flag - and the country - live
per-transaction on the Subaward Transactions sheets; the program-vendor sheets derive
Domestic or Foreign from them with a live COUNTIFS majority.)

Grain = one row per (subEntityUei, program): a UEI active on two programs appears once per
program. NAICS-6 uses the SAME precedence as scripts/build_program_vendors.py (reference
is_primary -> SAM fallback -> title backfill) by importing its loaders, so the value matches
the vendor sheets. Dollars come ONLY from the corpus and are used solely to pick the dollar-
modal vendor / parent name and to order rows; no dollar column is emitted.

The resolved Capability Domain / Primary Output archetypes are NOT emitted here - they are
LIVE formulas on the Supplier Master sheet (override-first over the Vendor Archetype Overrides
sheet, then the NAICS-6 Archetype Map), so editing an override or the crosswalk updates them.

Run:
    python3 scripts/build_supplier_master.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

from _paths import REPO  # noqa: E402
SCRIPTS = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/scripts"
sys.path.insert(0, str(REPO / "projects/distributed_shipbuilding/sam/award_classification/corpus/scripts"))
sys.path.insert(0, str(SCRIPTS))
from _corpus import iter_records  # noqa: E402
from build_program_vendors import (  # noqa: E402  (reuse the exact NAICS + prose precedence)
    load_naics_primary, load_naics_titles, load_research_naics, load_sam_naics,
    load_sam_status, na_label, load_old_prose, load_research_prose,
)

EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/extracted"

PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

HEADERS = ["Key", "Program", "Subawardee UEI", "Subawardee Vendor Name",
           "Primary NAICS-6", "NAICS-6 Description",
           "Parent UEI", "Parent Vendor Name", "Parent UEI(s)",
           "Role / Description", "Source URLs"]


def _aggregate(program: str):
    """{uei: dict} dollar-weighted roll-up for one program (blank UEIs dropped). Hull-builder-
    only scope (see build_program_vendors): submarines keep only the GDEB-directed prime; DDG
    is already restricted to its two hull builders in _corpus."""
    src = "ddg" if program == "ddg" else "submarines"
    recs = [r for r in iter_records(src)
            if program == "ddg" or ((r["vclass"] or "").lower() == program
                                    and r["bgroup"] == "GDEB")]
    g: dict[str, dict] = defaultdict(lambda: {
        "dol": 0.0, "names": defaultdict(float), "pnames": defaultdict(float),
        "parents": set(), "foreign": 0, "dom": 0,
        "pudol": defaultdict(float), "puname": defaultdict(lambda: defaultdict(float))})
    for r in recs:
        eu = r["entity_uei"]
        if not eu:
            continue
        d = g[eu]
        d["dol"] += r["dollar_m"]
        d["names"][r["vendor"]] += r["dollar_m"]
        if r["parent_name"]:
            d["pnames"][r["parent_name"]] += r["dollar_m"]
        if r["parent_uei"]:
            d["parents"].add(r["parent_uei"])
            d["pudol"][r["parent_uei"]] += r["dollar_m"]
            if r["parent_name"]:
                d["puname"][r["parent_uei"]][r["parent_name"]] += r["dollar_m"]
        if r["foreign"]:
            d["foreign"] += 1
        else:
            d["dom"] += 1
    return g


def _modal(counts: dict) -> str:
    """dollar-modal key, ties broken by the key itself so output is deterministic."""
    return max(counts, key=lambda k: (counts[k], k)) if counts else ""


def build():
    naics_primary = load_naics_primary()
    naics_titles = load_naics_titles()
    sam_naics = load_sam_naics()
    sam_status = load_sam_status()

    rows = []
    for program, label in PROGRAMS:
        g = _aggregate(program)
        research_naics = load_research_naics(program)
        old_prose = load_old_prose(program)
        research_prose = load_research_prose(program)
        for eu, d in sorted(g.items(), key=lambda kv: kv[1]["dol"], reverse=True):
            name = _modal(d["names"])
            code, desc = naics_primary.get(eu, ("", ""))
            if not code:
                code = sam_naics.get(eu, "")
                if not code and eu in research_naics:   # gap-fill only; never overwrites
                    code, rtitle = research_naics[eu]
                    desc = desc or rtitle
            if not desc and code:
                desc = naics_titles.get(code, "")
            if not code:  # typed n/a reason in place of a blank description
                desc = na_label(eu, d["foreign"] > d["dom"], sam_status)
            puei = _modal(d["pudol"])
            if puei:
                pname = _modal(d["puname"][puei])   # blank if this parent was never named
            else:
                pname = _modal(d["pnames"])
            parents = "; ".join(sorted(d["parents"]))
            # Role / Description + Source URLs: leaf-UEI research result wins; else direct UEI
            # in the old parent-level sheet; else the dollar-modal parent UEI's prose. This is
            # the SAME precedence + dollar-modal tie-break build_program_vendors uses, so the
            # value matches the program-vendor CSV exactly (the program-vendor sheets now read
            # this prose from here instead of re-deriving it).
            prose = url = ""
            if eu in research_prose:
                prose, url = research_prose[eu]
            elif eu in old_prose:
                prose, url = old_prose[eu]
            else:
                for p in sorted(d["pudol"], key=lambda x: (-d["pudol"][x], x)):
                    if p in old_prose:
                        prose, url = old_prose[p]
                        break
            rows.append([f"{label}|{eu}", label, eu, name, code, desc, puei, pname,
                         parents, prose, url])

    path = EXTRACTED / "supplier_master.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        w.writerows(rows)
    print(f"output: {path}  ({len(rows)} rows)")

    n = len(rows)
    naics_hits = sum(1 for r in rows if r[4])
    puei_hits = sum(1 for r in rows if r[6])
    pname_hits = sum(1 for r in rows if r[7])
    print(f"\n==== Supplier Master (UEI x program) ====")
    print(f"rows (UEI x program)              : {n}")
    print(f"distinct UEIs                     : {len({r[2] for r in rows})}")
    print(f"NAICS-6 code filled               : {naics_hits}/{n}  ({naics_hits/n*100:.0f}%)")
    print(f"standardized parent UEI filled    : {puei_hits}/{n}  ({puei_hits/n*100:.0f}%)")
    print(f"parent vendor name filled         : {pname_hits}/{n}  ({pname_hits/n*100:.0f}%)")


if __name__ == "__main__":
    build()
