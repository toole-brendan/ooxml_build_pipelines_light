"""build_uei_dimensions - the per-UEI attribute (dimension) pulls.

Produces two (subawardee UEI x program) dimension CSVs that surface, as their own
in-workbook sheets, the SAM/corpus enrichments that back the program-vendor sheets'
hardcoded leaf columns:

    subawardee_uei_index.csv  - UEI | Program | Vendor Name | Primary NAICS-6 | desc
    subawardee_parents.csv    - UEI | Program | Vendor Name | Parent UEI (dollar-modal
                                standardized) | Parent Vendor Name | Parent UEI(s) (raw)

(There is deliberately no domestic/foreign dimension sheet: that flag - and the
country - live per-transaction on the Subaward Transactions sheets, and the
program-vendor sheets derive Domestic or Foreign from them with a live COUNTIFS
majority, so a separate roll-up sheet would just be a stale copy.)

Grain = one row per (subEntityUei, program): a UEI active on two programs appears
once per program (the Program column distinguishes), so the union over the three
program-vendor sheets is reproduced exactly. NAICS-6 uses the SAME precedence as
scripts/build_program_vendors.py (reference is_primary -> SAM fallback -> title
backfill) by importing its loaders, so the value matches the vendor sheets.

Dollars come ONLY from the corpus and are used here solely to pick the dollar-modal
vendor / parent name and to order rows; no dollar column is emitted.

Run:
    python3 scripts/build_uei_dimensions.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
SCRIPTS = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/scripts"
sys.path.insert(0, str(REPO / "projects/distributed_shipbuilding/sam/award_classification/corpus/scripts"))
sys.path.insert(0, str(SCRIPTS))
from _corpus import iter_records  # noqa: E402
from build_program_vendors import (  # noqa: E402  (reuse the exact NAICS precedence)
    load_naics_primary, load_naics_titles, load_research_naics, load_sam_naics,
    load_sam_status, na_label,
)

EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/extracted"

PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

UEI_HEADERS = ["Subawardee UEI", "Program", "Subawardee Vendor Name",
               "Primary NAICS-6", "NAICS-6 Description"]
PARENT_HEADERS = ["Subawardee UEI", "Program", "Subawardee Vendor Name",
                  "Parent UEI", "Parent Vendor Name", "Parent UEI(s)"]


def _aggregate(program: str):
    """{uei: dict} dollar-weighted roll-up for one program (blank UEIs dropped)."""
    src = "ddg" if program == "ddg" else "submarines"
    # Hull-builder-only scope (see build_program_vendors): submarines keep only the
    # GDEB-directed prime (the Basic Construction line); the GFE primes (BPMI naval
    # reactor, LM/BAE/RR) are a separate SCN denominator and are excluded. DDG is
    # already restricted to its two hull builders (GD-BIW/HII-Ingalls) in _corpus.
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
            d["pudol"][r["parent_uei"]] += r["dollar_m"]       # $ per parent UEI
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

    uei_rows, parent_rows = [], []
    for program, label in PROGRAMS:
        g = _aggregate(program)
        research_naics = load_research_naics(program)
        # within a program, biggest vendors first (matches the vendor-sheet order)
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
            # standardized parent = the dollar-modal as-reported parent UEI, paired with
            # the dollar-modal name reported for THAT SAME UEI (kept a consistent pair:
            # the name never bleeds in from a different parent). When the subawardee
            # reports parent names but no parent UEI at all, surface the modal name with
            # a blank UEI. The raw multi-valued set is kept in Parent UEI(s).
            puei = _modal(d["pudol"])
            if puei:
                pname = _modal(d["puname"][puei])   # blank if this parent was never named
            else:
                pname = _modal(d["pnames"])
            parents = "; ".join(sorted(d["parents"]))
            uei_rows.append([eu, label, name, code, desc])
            parent_rows.append([eu, label, name, puei, pname, parents])

    for path, headers, rows in (
        (EXTRACTED / "subawardee_uei_index.csv", UEI_HEADERS, uei_rows),
        (EXTRACTED / "subawardee_parents.csv", PARENT_HEADERS, parent_rows),
    ):
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(headers)
            w.writerows(rows)
        print(f"output: {path}  ({len(rows)} rows)")

    n = len(uei_rows)
    naics_hits = sum(1 for r in uei_rows if r[3])
    puei_hits = sum(1 for r in parent_rows if r[3])
    pname_hits = sum(1 for r in parent_rows if r[4])
    print(f"\n==== UEI dimensions (UEI x program) ====")
    print(f"rows (UEI x program)              : {n}")
    print(f"distinct UEIs                     : {len({r[0] for r in uei_rows})}")
    print(f"NAICS-6 code filled               : {naics_hits}/{n}  ({naics_hits/n*100:.0f}%)")
    print(f"standardized parent UEI filled    : {puei_hits}/{n}  ({puei_hits/n*100:.0f}%)")
    print(f"parent vendor name filled         : {pname_hits}/{n}  ({pname_hits/n*100:.0f}%)")


if __name__ == "__main__":
    build()
