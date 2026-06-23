"""build_program_vendors - entity-grain subaward-recipient roll-up per program.

Produces extracted/<program>_program_vendors.csv for the refactored program-vendor
sheets: ONE row per distinct subawardee UEI (subEntityUei) that received a subaward
on that program across all years in the corpus, with SAM NAICS-6 enrichment, the
domestic/foreign flag, dollar + action + first/last-date roll-ups, blank archetype
columns (Capability Domain / Primary Output, assigned later), and the AI prose +
source URLs from the old top-vendor sheet joined in where the UEI (or its raw parent
UEI) matches.

Spine = the canonical corpus (_corpus.iter_records), so in-scope-PIID filtering,
DDG shipbuilder-directed restriction, MIB/BlueForge exclusion and report-id dedup
are already applied. Dollars come ONLY from the corpus; the SAM enrichment files are
used solely as per-UEI attribute lookups.

Column order (locked with the user):
    Subawardee UEI | Subawardee NAICS-6 (primary) | Subawardee NAICS-6 description |
    Parent UEI (blank) | Parent vendor name (raw as-reported) |
    Subawardee vendor name | Domestic or Foreign | Subaward $M | Subaward Actions |
    First Subaward | Last Subaward | <=FY12 $M .. FY26 $M (per-FY Subaward $M split) |
    Capability Domain (D) | Capability Domain Basis |
    Primary Output (P) | Primary Output Basis | Role / Description | Source URLs

Run:
    python3 scripts/build_program_vendors.py ddg
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

from _paths import REPO  # noqa: E402
sys.path.insert(0, str(REPO / "projects/distributed_shipbuilding/sam/award_classification/corpus/scripts"))
from _corpus import iter_records  # noqa: E402

NAICS_REF = REPO / "projects/distributed_shipbuilding/sam/award_classification/submarine_subaward_code_package/vendor_naics_reference.csv"
SAM_ENRICH = REPO / "projects/distributed_shipbuilding/sam/award_classification/sam_entity_enrichment/unique_uei_sam_enrichment.csv"
REFACTOR = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor"
EXTRACTED = REFACTOR / "extracted"

# Official NAICS-6 titles for codes that reach a vendor only via the SAM fallback and
# are absent from vendor_naics_reference.csv (so the title harvest below can't backfill
# their description). Values are taken from the entity's SAM `naicsList` description,
# which matches the official Census 2022 NAICS title. The reference harvest still wins
# where it has the code; these only fill codes it lacks.
NAICS_TITLE_OVERRIDES = {
    "424710": "Petroleum Bulk Stations and Terminals",     # Martin Energy Services, LLC
    "424410": "General Line Grocery Merchant Wholesalers",  # Sysco USA II LLC
}

# old top-vendor sheets: (csv, uei col, prose col, source-url col)
OLD_SHEETS = {
    "ddg": (EXTRACTED / "ddg_top_vendors.csv", "Vendor UEI",
            "DDG-51 new-construction role / work description", "Source URLs"),
    "virginia": (EXTRACTED / "virginia_top_vendors.csv", "vendor_uei",
                 "submarine_construction_role_summary", "source_urls_used"),
    "columbia": (EXTRACTED / "columbia_top_vendors.csv", "Vendor UEI",
                 "submarine_construction_work_description", "source_urls"),
}

# AI deep-research result CSVs (normalized from research_pulls/ by
# extract_research_results.py). Keyed directly on the LEAF subawardee UEI - one row per
# UEI - so this prose takes precedence over the parent-level OLD_SHEETS join, and its
# NAICS-6 is used only to gap-fill a UEI that has no reference/SAM code.
RESEARCH_RESULTS = {
    "ddg": EXTRACTED / "ddg_subaward_research_results.csv",
    "virginia": EXTRACTED / "virginia_subaward_research_results.csv",
    "columbia": EXTRACTED / "columbia_subaward_research_results.csv",
}

# The per-program archetype classifications (merge_archetype_pulls.py output) are no
# longer consumed here: the workbook resolves D / P as override-first formulas, so those
# overrides are emitted to their own table by scripts/build_archetype_overrides.py.

_NAICS6 = re.compile(r"^\d{6}$")

# Per-FY Subaward $M split. These columns are rendered on the program-vendor sheets as
# date-bounded SUMIFS formulas (the calendar Subaward Date -> federal FY conversion happens
# in the formula, NOT in the raw data), so the values written here are blank placeholders -
# they exist only so the columns are present on the sheet. Uniform axis: a <=FY12 open-below
# catch-all (captures the lone pre-FY2013 DDG record) + FY2013..FY2026. Keep these header
# strings IN SYNC with _FY_HEADERS in {ddg,virginia,columbia}_program_vendors.py.
FY_COLUMNS = ["≤FY12 $M"] + [f"FY{y % 100} $M" for y in range(2013, 2027)]

HEADERS = [
    "Subawardee UEI", "Subawardee NAICS-6 (Primary)", "Subawardee NAICS-6 Description",
    "Parent UEI", "Parent Vendor Name", "Subawardee Vendor Name",
    "Predominant Place of Performance (by records)", "Subaward $M",
    "Published Subaward Records",
    "First Subaward", "Last Subaward",
    # Per-FY Subaward $M split (blank placeholders; rendered as SUMIFS formulas on the sheet).
    *FY_COLUMNS,
    # The four archetype cells are placeholders here: the workbook renders them as
    # override-first formulas (Vendor Archetype Overrides -> NAICS-6 Archetype Map ->
    # unresolved), so the values written below are blank and ignored. The headers must
    # remain so the columns exist on the sheet.
    "Capability Domain Archetype (D)", "Capability Domain Archetype Basis",
    "Primary Output Archetype (P)", "Primary Output Archetype Basis",
    "Role / Description", "Source URLs",
]


def load_naics_primary() -> dict[str, tuple[str, str]]:
    """uei -> (naics6, naics_desc) for the is_primary='Y' row."""
    out: dict[str, tuple[str, str]] = {}
    with NAICS_REF.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("is_primary") or "").strip().upper() == "Y":
                uei = (r.get("uei") or "").strip()
                if uei and uei not in out:
                    out[uei] = ((r.get("naics6") or "").strip(),
                                (r.get("naics_desc") or "").strip())
    return out


def load_naics_titles() -> dict[str, str]:
    """naics6 code -> official title, harvested from every row of the reference
    (used to backfill descriptions for codes sourced from the SAM fallback)."""
    out: dict[str, str] = {}
    with NAICS_REF.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("naics6") or "").strip()
            desc = (r.get("naics_desc") or "").strip()
            if code and desc and code not in out:
                out[code] = desc
    for code, desc in NAICS_TITLE_OVERRIDES.items():
        out.setdefault(code, desc)   # fill only codes the reference harvest lacks
    return out


def load_sam_naics() -> dict[str, str]:
    """uei -> primary_naics_6 (code only) fallback from the SAM entity enrichment."""
    out: dict[str, str] = {}
    with SAM_ENRICH.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            code = (r.get("primary_naics_6") or "").strip()
            if uei and code:
                out[uei] = code
    return out


def load_old_prose(program: str) -> dict[str, tuple[str, str]]:
    """old parent-first UEI -> (prose, source_urls) from the old top-vendor sheet."""
    path, ucol, pcol, scol = OLD_SHEETS[program]
    out: dict[str, tuple[str, str]] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get(ucol) or "").strip()
            if uei:
                out[uei] = ((r.get(pcol) or "").strip(), (r.get(scol) or "").strip())
    return out


def load_research_prose(program: str) -> dict[str, tuple[str, str]]:
    """leaf subawardee UEI -> (role, source_urls) from the AI deep-research results.
    Keyed on the subawardee UEI itself (not a parent), so it overrides the parent-level
    OLD_SHEETS prose for any UEI that was researched."""
    path = RESEARCH_RESULTS.get(program)
    out: dict[str, tuple[str, str]] = {}
    if not path or not path.exists():
        return out
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("Subawardee UEI") or "").strip()
            role = (r.get("Role / Description") or "").strip()
            if uei and role:
                out[uei] = (role, (r.get("Source URLs") or "").strip())
    return out


def load_research_naics(program: str) -> dict[str, tuple[str, str]]:
    """leaf subawardee UEI -> (naics6, title) from the research results, accepting ONLY a
    valid 6-digit code (drops 'Not confirmed' and blanks). Used to gap-fill a UEI that the
    reference and SAM both lack; it never overwrites an existing code (lowest precedence)."""
    path = RESEARCH_RESULTS.get(program)
    out: dict[str, tuple[str, str]] = {}
    if not path or not path.exists():
        return out
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("Subawardee UEI") or "").strip()
            code = (r.get("NAICS-6 code") or "").strip()
            if uei and _NAICS6.match(code):
                out[uei] = (code, (r.get("NAICS-6 title") or "").strip())
    return out


def load_sam_status() -> dict[str, str]:
    """uei -> the reason it has no SAM-sourced NAICS-6, used to fill the (otherwise
    blank) NAICS-6 description with a typed n/a. Only the two failure modes are
    recorded: 'NO_RECORD' (queried, no SAM entity for that UEI) and 'NO_NAICS' (a SAM
    record exists but lists no primary NAICS). A UEI absent from the map was never
    pulled, so the caller treats it as the un-researched long tail."""
    out: dict[str, str] = {}
    with SAM_ENRICH.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            if not uei:
                continue
            if (r.get("sam_match") or "").strip() == "NO_RECORD":
                out[uei] = "NO_RECORD"
            elif not (r.get("primary_naics_6") or "").strip():
                out[uei] = "NO_NAICS"
    return out


def na_label(uei: str, foreign: bool, sam_status: dict[str, str]) -> str:
    """Typed 'n/a (reason)' shown in the NAICS-6 description when a UEI has no code, so
    a blank reads as adjudicated rather than forgotten. The no-SAM-record bucket is
    split foreign/domestic (foreign entities are the dominant reason a UEI is absent
    from SAM); the other two buckets are not, since foreignness is already its own
    column. These resolve to a real code/title if the research pass later fills them."""
    st = sam_status.get(uei)
    if st == "NO_RECORD":
        return "n/a (foreign, no SAM record)" if foreign else "n/a (no SAM record)"
    if st == "NO_NAICS":
        return "n/a (SAM record, no NAICS)"
    return "n/a (long-tail, not researched)"


def build(program: str):
    src = "ddg" if program == "ddg" else "submarines"
    # Hull-builder-only scope: this workbook measures what the hull-construction PRIME
    # outsources (the Basic Construction line, appropriated to the prime). For
    # submarines that prime is GDEB; the GFE primes catalogued in the submarine scope
    # (BPMI naval reactor, LM combat systems, BAE ordnance/deck modules, RR propulsion)
    # are a SEPARATE SCN denominator and are excluded here so the three programs are
    # comparable. DDG is already restricted to its two hull builders (GD-BIW /
    # HII-Ingalls) upstream in _corpus.load_scope, so the bgroup test is sub-only.
    # NOTE: the submarine cut still excludes the HII-NNS team-build workshare, which
    # flows through GDEB as vendor of record and is largely unreported (the "Newport
    # News gap"); hull/structural archetypes are understated on the submarine side.
    recs = [r for r in iter_records(src)
            if program == "ddg" or ((r["vclass"] or "").lower() == program
                                    and r["bgroup"] == "GDEB")]

    naics_primary = load_naics_primary()
    naics_titles = load_naics_titles()
    sam_naics = load_sam_naics()
    sam_status = load_sam_status()
    old_prose = load_old_prose(program)
    research_prose = load_research_prose(program)
    research_naics = load_research_naics(program)

    g: dict[str, dict] = defaultdict(lambda: {
        "dol": 0.0, "n": 0, "first": "", "last": "",
        "names": defaultdict(float), "pnames": defaultdict(float),
        "foreign": 0, "dom": 0, "pdol": defaultdict(float)})
    blank_dol = 0.0
    blank_n = 0
    corpus_dol = 0.0

    for r in recs:
        corpus_dol += r["dollar_m"]
        eu = r["entity_uei"]
        if not eu:
            blank_dol += r["dollar_m"]
            blank_n += 1
            continue
        d = g[eu]
        d["dol"] += r["dollar_m"]
        d["n"] += 1
        d["names"][r["vendor"]] += r["dollar_m"]
        if r["parent_name"]:
            d["pnames"][r["parent_name"]] += r["dollar_m"]
        dt = (r["date"] or "")[:10]
        if dt:
            if not d["first"] or dt < d["first"]:
                d["first"] = dt
            if dt > d["last"]:
                d["last"] = dt
        if r["foreign"]:
            d["foreign"] += 1
        else:
            d["dom"] += 1
        if r["parent_uei"]:
            d["pdol"][r["parent_uei"]] += r["dollar_m"]

    rows = []
    naics_ref_hits = naics_any_hits = desc_hits = desc_backfilled = 0
    foreign_rows = prose_rows = pname_rows = 0
    research_naics_hits = research_prose_hits = 0
    matched_old = set()
    for eu, d in g.items():
        name = max(d["names"].items(), key=lambda kv: kv[1])[0]
        pname = max(d["pnames"].items(), key=lambda kv: kv[1])[0] if d["pnames"] else ""
        if pname:
            pname_rows += 1
        # NAICS-6: prefer the reference (code+desc), fall back to SAM code-only,
        # then backfill a missing description from the code->title harvest.
        code, desc = naics_primary.get(eu, ("", ""))
        if code:
            naics_ref_hits += 1
        else:
            code = sam_naics.get(eu, "")
            if not code and eu in research_naics:   # gap-fill only; never overwrites
                code, rtitle = research_naics[eu]
                desc = desc or rtitle
                research_naics_hits += 1
        if code:
            naics_any_hits += 1
        if not desc and code:
            desc = naics_titles.get(code, "")
            if desc:
                desc_backfilled += 1
        if desc:
            desc_hits += 1
        domforeign = "Foreign" if d["foreign"] > d["dom"] else "Domestic"
        if domforeign == "Foreign":
            foreign_rows += 1
        if not code:  # no NAICS-6 -> typed n/a reason in place of a blank description
            desc = na_label(eu, domforeign == "Foreign", sam_status)
        # prose: leaf-UEI research result wins; else direct UEI match in the old
        # parent-level sheet; else any raw parent UEI match (dollar-modal).
        prose = url = ""
        if eu in research_prose:
            prose, url = research_prose[eu]
            research_prose_hits += 1
        elif eu in old_prose:
            prose, url = old_prose[eu]
            matched_old.add(eu)
        else:
            # A subawardee can carry several as-reported parent UEIs, and more than one
            # may have prose. Pick the dollar-modal parent's prose (the parent that took
            # the most subaward $ for this subawardee; ties broken by UEI) so the result
            # is deterministic and consistent with the standardized-parent rule -- a set
            # iteration here made the build non-reproducible run to run.
            for p in sorted(d["pdol"], key=lambda x: (-d["pdol"][x], x)):
                if p in old_prose:
                    prose, url = old_prose[p]
                    matched_old.add(p)
                    break
        if prose:
            prose_rows += 1
        # Archetype cells are left blank: the workbook computes D / P + their Basis as
        # override-first formulas (the hand-researched overrides now live in their own
        # Vendor Archetype Overrides table; see scripts/build_archetype_overrides.py).
        rows.append([
            eu, code, desc, "", pname, name, domforeign,
            round(d["dol"], 6), d["n"], d["first"], d["last"],
            *[""] * len(FY_COLUMNS),   # per-FY $M placeholders (SUMIFS formulas on the sheet)
            "", "", "", "", prose, url,
        ])

    rows.sort(key=lambda x: x[7], reverse=True)

    out_path = EXTRACTED / f"{program}_program_vendors.csv"
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        w.writerows(rows)

    # ---- coverage report ----
    n = len(rows)
    row_dol = sum(r[7] for r in rows)
    old_total = len(old_prose)
    old_unmatched = sorted(set(old_prose) - matched_old)
    print(f"\n==== {program.upper()} program-vendor roll-up ====")
    print(f"output: {out_path}")
    print(f"rows (distinct subawardee UEIs)   : {n}")
    print(f"corpus $M total                   : {corpus_dol:,.3f}")
    print(f"  rows $M total                   : {row_dol:,.3f}  (delta {corpus_dol-row_dol:+.6f})")
    print(f"  dropped blank-UEI records       : {blank_n}  (${blank_dol:,.3f}M)")
    print(f"NAICS-6 fill (reference, code+desc): {naics_ref_hits}/{n}  ({naics_ref_hits/n*100:.0f}%)")
    print(f"NAICS-6 fill (incl SAM fallback)  : {naics_any_hits}/{n}  ({naics_any_hits/n*100:.0f}%)")
    print(f"  description filled (post-backfill): {desc_hits}/{n}  ({desc_hits/n*100:.0f}%)  [+{desc_backfilled} backfilled]")
    print(f"parent vendor name filled (raw)   : {pname_rows}/{n}  ({pname_rows/n*100:.0f}%)")
    print(f"foreign rows                      : {foreign_rows}/{n}")
    print(f"rows with prose joined            : {prose_rows}/{n}")
    print(f"  from leaf-UEI research result   : {research_prose_hits}")
    print(f"  from old parent-level join      : {prose_rows - research_prose_hits}")
    print(f"NAICS-6 gap-filled from research  : {research_naics_hits}")
    print(f"old top-vendors matched to >=1 row: {len(matched_old)}/{old_total}")
    if old_unmatched:
        print(f"old top-vendors with NO match ({len(old_unmatched)}):")
        for u in old_unmatched:
            print(f"    {u}  {old_prose[u][0][:60]}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "ddg")
