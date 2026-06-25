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

from _paths import REPO  # noqa: E402
sys.path.insert(0, str(REPO / "projects/distributed_shipbuilding/sam/sam_awards_data/corpus/scripts"))
from _corpus import PROGRAMS, load_scope, iter_records  # noqa: E402

EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor/extracted"


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


# Columns that legitimately differ between two reports of the SAME subcontract action:
# the FSRS report identity (Report ID + Report Number). Two rows identical on EVERY OTHER
# field are a semantic-duplicate candidate (reviewer finding #2): the same action reported
# twice. Flagged + logged, never silently deleted - only the prime can adjudicate.
_DUP_IGNORE = {5, 6}   # 5 = Subaward Report ID, 6 = Subaward Report Number
_RID, _RNO, _UEI, _VN, _DATE, _AMT, _PIID = 5, 6, 0, 1, 8, 10, 25


def _dup_key(row):
    return tuple(v for i, v in enumerate(row[:50]) if i not in _DUP_IGNORE)


def find_duplicate_candidates(program: str, rows: list[list[str]]):
    """Return (candidate_records, summary). Within each group of rows identical on all
    non-report-ID fields, the first (earliest, by the existing UEI+date sort) is RETAINED
    and the rest are duplicate CANDIDATES. Nothing is removed."""
    groups: dict[tuple, list[list[str]]] = {}
    for r in rows:
        groups.setdefault(_dup_key(r), []).append(r)
    candidates = []
    cand_dol = 0.0
    for g in groups.values():
        if len(g) < 2:
            continue
        retained = g[0]
        for r in g[1:]:
            cand_dol += _f(r[_AMT])
            candidates.append([
                program, retained[_RID], r[_RID], r[_RNO], r[_UEI], r[_VN],
                r[_PIID], r[_DATE], f"{_f(r[_AMT]) / 1e6:.6f}"])
    gross_dol = sum(_f(r[_AMT]) for r in rows)
    summary = {
        "program": program,
        "gross_rows": len(rows),
        "gross_nominal_m": gross_dol / 1e6,
        "candidate_rows": len(candidates),
        "candidate_nominal_m": cand_dol / 1e6,
        "net_rows": len(rows) - len(candidates),
        "net_nominal_m": (gross_dol - cand_dol) / 1e6,
    }
    return candidates, summary


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

    cands, summary = find_duplicate_candidates(program, rows)
    print(f"  duplicate candidates            : {summary['candidate_rows']}  "
          f"(${summary['candidate_nominal_m']:,.3f}M nominal)")
    return cands, summary


_CAND_HEADERS = ["Program", "Retained Report ID", "Candidate Report ID",
                 "Candidate Report Number", "Subawardee UEI", "Subawardee Vendor Name",
                 "Prime PIID", "Subaward Date", "Subaward Amount $M"]
_AUDIT_HEADERS = ["Program", "Gross Rows", "Gross Nominal $M", "Duplicate-Candidate Rows",
                  "Duplicate-Candidate Nominal $M", "Net Rows", "Net Nominal $M",
                  "Candidate % of Gross"]


def write_audit(results: list[tuple[list, dict]]) -> None:
    """Emit the semantic-duplicate adjudication log + the per-program gross/net summary."""
    all_cands = [c for cands, _ in results for c in cands]
    with (EXTRACTED / "duplicate_candidates.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(_CAND_HEADERS)
        w.writerows(all_cands)

    rows_out = []
    tot = {"gross_rows": 0, "gross_nominal_m": 0.0, "candidate_rows": 0,
           "candidate_nominal_m": 0.0, "net_rows": 0, "net_nominal_m": 0.0}
    for _, s in results:
        for k in tot:
            tot[k] += s[k]
    for _, s in results + [(None, {"program": "TOTAL", **tot})]:
        pct = (s["candidate_nominal_m"] / s["gross_nominal_m"] * 100
               if s["gross_nominal_m"] else 0.0)
        rows_out.append([s["program"], s["gross_rows"], f"{s['gross_nominal_m']:.3f}",
                         s["candidate_rows"], f"{s['candidate_nominal_m']:.3f}",
                         s["net_rows"], f"{s['net_nominal_m']:.3f}", f"{pct:.2f}%"])
    with (EXTRACTED / "duplicate_audit.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(_AUDIT_HEADERS)
        w.writerows(rows_out)
    print(f"\n==== duplicate audit ====\nlog : {EXTRACTED / 'duplicate_candidates.csv'} "
          f"({len(all_cands)} candidates)\nsummary: {EXTRACTED / 'duplicate_audit.csv'}")


if __name__ == "__main__":
    progs = sys.argv[1:] or ["ddg", "virginia", "columbia"]
    results = [build(p) for p in progs]
    write_audit(results)
