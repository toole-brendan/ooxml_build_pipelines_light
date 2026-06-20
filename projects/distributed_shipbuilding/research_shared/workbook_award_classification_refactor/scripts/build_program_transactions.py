"""build_program_transactions - the COMPLETE raw subaward transaction pull per program.

Produces extracted/<program>_subaward_transactions.csv: ONE row per deduped
published subaward record (subAwardReportId) on that program, carrying EVERY data
field that exists on the raw FSRS `published` subaward object - 28 record fields
flattened to 50 leaf columns (nested objects -> one column per leaf; the two array
fields -> their joined leaves). Always-blank fields are kept as columns by design.
Nothing here is SAM-enrichment: the subawardee's NAICS-6 is an entity attribute and
lives on the Subawardee UEI Index, not on the transaction grain.

Scope = the canonical corpus: walk the same in-scope-PIID JSON the corpus walks
(load_scope), DDG restricted to shipbuilder-directed groups, MIB/BlueForge UEIs
stripped, report-id deduped - so the record SET is byte-identical to
_corpus.iter_records (asserted: count + $ reconcile to the cent). Records with a
blank subEntityUei are dropped (they cannot key a vendor row); that count is 0 in
every program today, so the per-UEI roll-up still reconciles exactly.

Run:
    python3 scripts/build_program_transactions.py ddg
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
sys.path.insert(0, str(REPO / "projects/distributed_shipbuilding/research_shared/corpus/scripts"))
from _corpus import PROGRAMS, load_scope, iter_records  # noqa: E402

EXTRACTED = REPO / "projects/distributed_shipbuilding/research_shared/workbook_award_classification_refactor/extracted"


# ---- raw-record helpers ----------------------------------------------------------

def g(r, *path):
    """Nested get -> the leaf value, or '' if any hop is missing/None."""
    cur = r
    for k in path:
        if not isinstance(cur, dict):
            return ""
        cur = cur.get(k)
        if cur is None:
            return ""
    return cur


def jl(r, key, sub):
    """Array-of-objects field -> '; '-joined leaf values (faithful multi-value)."""
    out = []
    for it in (r.get(key) or []):
        if isinstance(it, dict):
            v = it.get(sub)
            if v not in (None, ""):
                out.append(str(v).strip())
    return "; ".join(out)


def t(v):
    return "" if v is None else str(v).strip()


def date10(v):
    return t(v)[:10]


# ---- the 50-column schema (header, extractor) ------------------------------------
# Order: subawardee identity -> the subaward -> subawardee address -> business
# types / exec comp -> prime-contract context. UEI is column B (sort + join key).
COLUMNS = [
    # subawardee entity (as reported on the subaward record)
    ("Subawardee UEI",                    lambda r: t(g(r, "subEntityUei"))),
    ("Subawardee Vendor Name",            lambda r: t(g(r, "subEntityLegalBusinessName"))),
    ("Subawardee DBA Name",               lambda r: t(g(r, "subEntityDoingBusinessAsName"))),
    ("Parent UEI",                        lambda r: t(g(r, "subParentUei"))),
    ("Parent Vendor Name",                lambda r: t(g(r, "subEntityParentLegalBusinessName"))),
    # the subaward
    ("Subaward Report ID",                lambda r: t(g(r, "subAwardReportId"))),
    ("Subaward Report Number",            lambda r: t(g(r, "subAwardReportNumber"))),
    ("Subaward Number",                   lambda r: t(g(r, "subAwardNumber"))),
    ("Subaward Date",                     lambda r: date10(g(r, "subAwardDate"))),
    ("Submitted Date",                    lambda r: date10(g(r, "submittedDate"))),
    ("Subaward Amount $",                 lambda r: t(g(r, "subAwardAmount"))),
    ("Subaward Description",              lambda r: t(g(r, "subawardDescription"))),
    # subawardee physical address
    ("Subawardee Street Address",         lambda r: t(g(r, "entityPhysicalAddress", "streetAddress"))),
    ("Subawardee Street Address 2",       lambda r: t(g(r, "entityPhysicalAddress", "streetAddress2"))),
    ("Subawardee City",                   lambda r: t(g(r, "entityPhysicalAddress", "city"))),
    ("Subawardee Congressional District", lambda r: t(g(r, "entityPhysicalAddress", "congressionalDistrict"))),
    ("Subawardee State Code",             lambda r: t(g(r, "entityPhysicalAddress", "state", "code"))),
    ("Subawardee State Name",             lambda r: t(g(r, "entityPhysicalAddress", "state", "name"))),
    ("Country Code",                      lambda r: t(g(r, "entityPhysicalAddress", "country", "code"))),
    ("Country Name",                      lambda r: t(g(r, "entityPhysicalAddress", "country", "name"))),
    ("Subawardee ZIP",                    lambda r: t(g(r, "entityPhysicalAddress", "zip"))),
    # business types + exec comp (array fields, joined)
    ("Business Type Codes",               lambda r: jl(r, "subBusinessType", "code")),
    ("Business Type Names",               lambda r: jl(r, "subBusinessType", "name")),
    ("Top Pay Salaries",                  lambda r: jl(r, "subTopPayEmployee", "salary")),
    ("Top Pay Employee Names",            lambda r: jl(r, "subTopPayEmployee", "fullname")),
    # prime-contract context (constant per prime PIID)
    ("Prime PIID",                        lambda r: t(g(r, "piid"))),
    ("Prime Contract Key",                lambda r: t(g(r, "primeContractKey"))),
    ("Agency ID",                         lambda r: t(g(r, "agencyId"))),
    ("Referenced IDV PIID",               lambda r: t(g(r, "referencedIDVPIID"))),
    ("Referenced IDV Agency ID",          lambda r: t(g(r, "referencedIDVAgencyId"))),
    ("Prime Award Type",                  lambda r: t(g(r, "primeAwardType"))),
    ("Total Contract Value $",            lambda r: t(g(r, "totalContractValue"))),
    ("Base Award Date Signed",            lambda r: date10(g(r, "baseAwardDateSigned"))),
    ("Prime Entity UEI",                  lambda r: t(g(r, "primeEntityUei"))),
    ("Prime Entity Name",                 lambda r: t(g(r, "primeEntityName"))),
    ("Description of Requirement",        lambda r: t(g(r, "descriptionOfRequirement"))),
    ("Prime NAICS",                       lambda r: t(g(r, "primeNaics", "code"))),
    ("Prime NAICS Description",           lambda r: t(g(r, "primeNaics", "description"))),
    ("Funding Agency Code",               lambda r: t(g(r, "primeOrganizationInfo", "fundingAgency", "code"))),
    ("Funding Agency Name",               lambda r: t(g(r, "primeOrganizationInfo", "fundingAgency", "name"))),
    ("Funding Office Code",               lambda r: t(g(r, "primeOrganizationInfo", "fundingOffice", "code"))),
    ("Funding Office Name",               lambda r: t(g(r, "primeOrganizationInfo", "fundingOffice", "name"))),
    ("Funding Department Code",           lambda r: t(g(r, "primeOrganizationInfo", "fundingDepartment", "code"))),
    ("Funding Department Name",           lambda r: t(g(r, "primeOrganizationInfo", "fundingDepartment", "name"))),
    ("Contracting Agency Code",           lambda r: t(g(r, "primeOrganizationInfo", "contractingAgency", "code"))),
    ("Contracting Agency Name",           lambda r: t(g(r, "primeOrganizationInfo", "contractingAgency", "name"))),
    ("Contracting Office Code",           lambda r: t(g(r, "primeOrganizationInfo", "contractingOffice", "code"))),
    ("Contracting Office Name",           lambda r: t(g(r, "primeOrganizationInfo", "contractingOffice", "name"))),
    ("Contracting Department Code",       lambda r: t(g(r, "primeOrganizationInfo", "contractingDepartment", "code"))),
    ("Contracting Department Name",       lambda r: t(g(r, "primeOrganizationInfo", "contractingDepartment", "name"))),
]
HEADERS = [h for h, _ in COLUMNS]
assert len(HEADERS) == 50, len(HEADERS)


def raw_records(program: str):
    """Yield raw published subaward dicts on `program`, canonical scope + dedup."""
    src = "ddg" if program == "ddg" else "submarines"
    piids, mib = load_scope(src)
    fdir = PROGRAMS[src]["fullhistory"]
    seen: set[str] = set()
    for path in sorted(fdir.glob("N*_subawards.json")):
        piid = path.stem.split("_")[0]
        if piid not in piids:
            continue
        vclass = (piids[piid].get("class") or "").strip().lower()
        if program != "ddg" and vclass != program:
            continue
        # Hull-builder-only scope (see build_program_vendors): submarines keep only the
        # GDEB-directed prime (Basic Construction); GFE primes (BPMI/LM/BAE/RR) excluded.
        group = (piids[piid].get("group") or piids[piid].get("prime") or "").strip()
        if program != "ddg" and group != "GDEB":
            continue
        blob = json.load(path.open(encoding="utf-8"))
        for r in blob.get("published") or []:
            rid = r.get("subAwardReportId") or ""
            if rid and rid in seen:
                continue
            if rid:
                seen.add(rid)
            eu = (r.get("subEntityUei") or "").strip()
            pu = (r.get("subParentUei") or "").strip()
            if eu in mib or pu in mib:
                continue
            yield r


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def build(program: str):
    rows = []
    raw_all_dol = 0.0
    blank_n = blank_dol = 0
    for r in raw_records(program):
        amt_m = _f(r.get("subAwardAmount")) / 1e6
        raw_all_dol += amt_m
        if not (r.get("subEntityUei") or "").strip():
            blank_n += 1
            blank_dol += amt_m
            continue
        rows.append([fn(r) for _, fn in COLUMNS])

    # group by subawardee UEI, then chronological (col 0 = UEI, col 8 = Subaward Date)
    rows.sort(key=lambda x: (x[0], x[8]))

    out_path = EXTRACTED / f"{program}_subaward_transactions.csv"
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        w.writerows(rows)

    # reconcile the raw walk to the canonical corpus (same record set)
    csrc = "ddg" if program == "ddg" else "submarines"
    corpus_dol = sum(rr["dollar_m"] for rr in iter_records(csrc)
                     if program == "ddg" or ((rr["vclass"] or "").lower() == program
                                             and rr["bgroup"] == "GDEB"))
    row_dol = sum(_f(row[10]) for row in rows) / 1e6   # col 10 = Subaward Amount $
    ueis = len({row[0] for row in rows})

    print(f"\n==== {program.upper()} subaward transactions ====")
    print(f"output: {out_path}")
    print(f"columns                           : {len(HEADERS)}")
    print(f"transactions (rows)               : {len(rows)}")
    print(f"distinct subawardee UEIs          : {ueis}")
    print(f"corpus $M (iter_records)          : {corpus_dol:,.6f}")
    print(f"  raw-walk $M (all records)       : {raw_all_dol:,.6f}")
    print(f"  rows $M (keyed UEIs)            : {row_dol:,.6f}")
    print(f"  dropped blank-UEI records       : {blank_n}  (${blank_dol:,.6f}M)")
    delta = abs(corpus_dol - raw_all_dol)
    assert delta < 1e-4, f"SCOPE MISMATCH: corpus {corpus_dol} vs raw {raw_all_dol} (Δ{delta})"
    print(f"  reconcile Δ                     : {delta:.2e}  OK")


if __name__ == "__main__":
    progs = sys.argv[1:] or ["ddg", "virginia", "columbia"]
    for p in progs:
        build(p)
