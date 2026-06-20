"""_corpus - shared loader for the competability analysis.

Loads the SAM.gov full-history subaward corpora for both programs, filters to the
in-scope new-construction PIIDs, strips MIB/BlueForge vendors, and classifies every
record registry-FIRST with the consolidated taxonomy as fallback — replicating
`workbook_submarines/sheets/data_entity_master.classified_records()` exactly, but
reading the raw research JSONs instead of the workbook's windowed nc_records_long.csv
(full history is needed for first-ever-award dating and cadence).

Differences vs the workbook corpus, by design:
  - Source = research/sam_subawards_fullhistory/ (the workbook extraction predates
    the fullhistory pulls and used the windowed cache), so record counts here are
    >= the workbook's for any window.
  - DDG scope = the 24 shipbuilder-directed PIIDs only (groups GD-BIW + HII-Ingalls);
    Navy-directed GFE primes are outside the competable pool (handoff decision #3).

Pure stdlib. Import from sibling scripts via `from _corpus import ...`.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
from pathlib import Path

REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
TAXONOMY_PY = REPO / "projects/distributed_shipbuilding/tam/consolidated/workbook_consolidated/sheets/_taxonomy.py"
REGISTRY_CSV = REPO / "projects/distributed_shipbuilding/sam/award_classification/supplier_bucketing/vendor_evidence_registry.csv"
EXTRACTED = REPO / "projects/distributed_shipbuilding/sam/award_classification/corpus/extracted"

PROGRAMS = {
    "submarines": {
        "fullhistory": REPO / "projects/distributed_shipbuilding/tam/submarines/research/sam_subawards_fullhistory",
        "scope_json": REPO / "projects/distributed_shipbuilding/tam/submarines/extracted/nc_scope_summary.json",
        "naics_csv": REPO / "projects/distributed_shipbuilding/tam/submarines/research/extracted/entity_naics_lookup.csv",
        "groups": None,                      # all in-scope PIIDs (GDEB shipbuilder-directed)
    },
    "ddg": {
        "fullhistory": REPO / "projects/distributed_shipbuilding/tam/ddg/research/sam_subawards_fullhistory",
        "scope_json": REPO / "projects/distributed_shipbuilding/tam/ddg/extracted/nc_scope_summary.json",
        "naics_csv": REPO / "projects/distributed_shipbuilding/tam/ddg/research/extracted/entity_naics_lookup.csv",
        "groups": {"GD-BIW", "HII-Ingalls"},  # shipbuilder-directed only
    },
}

def _window_from_env() -> tuple[int, int]:
    """Analysis window (fy_lo, fy_hi). Headline default is the deck's FY22-25
    basis; sensitivity runs override with e.g. COMP_WINDOW=2019:2025."""
    raw = os.environ.get("COMP_WINDOW", "").strip()
    if not raw:
        return (2022, 2025)
    lo, hi = (int(x) for x in raw.split(":"))
    if lo > hi:
        raise ValueError(f"COMP_WINDOW lo > hi: {raw!r}")
    return (lo, hi)


FY22_25 = _window_from_env()

# Window-dependent CSVs land here. Sensitivity runs point COMP_OUTDIR at a
# scratch dir so the headline extracted/ files stay untouched.
OUT_DIR = Path(os.environ["COMP_OUTDIR"]) if os.environ.get("COMP_OUTDIR") else EXTRACTED


# ---- taxonomy (importlib: _taxonomy.py is a dependency-free leaf) ----------------

def load_taxonomy():
    spec = importlib.util.spec_from_file_location("_taxonomy", TAXONOMY_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_TAX = load_taxonomy()
classify = _TAX.classify
BUCKET_KEYS = _TAX.BUCKET_KEYS
BUCKETS = _TAX.BUCKETS
UNBUCKETED = _TAX.UNBUCKETED


# ---- registry (inlined from workbook_submarines/sheets/_registry.py) -------------

_ROLE_MAP = {"gfe": "gfe_sib", "residual": "supplier"}


def load_registry() -> dict[str, dict]:
    """uei -> {role, bucket, modular, vls}. Empty dict if the file is absent."""
    out: dict[str, dict] = {}
    if not REGISTRY_CSV.exists():
        return out
    with REGISTRY_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            if not uei:
                continue
            role = (r.get("role") or "").strip()
            role = _ROLE_MAP.get(role, role)
            flags = (r.get("scenario_flags") or "")
            out[uei] = {
                "role": role,
                "bucket": (r.get("bucket") or "").strip(),
                "modular": "modular" in flags,
                "vls": "vls_boundary" in flags,
            }
    return out


# ---- helpers (mirroring aggregate_new_construction.py) ---------------------------

def fy_of(date_str):
    """Fed FY: Oct 1 of prior year through Sep 30 of FY year. None on bad input."""
    if not date_str or len(date_str) < 10:
        return None
    try:
        y, m = int(date_str[:4]), int(date_str[5:7])
    except ValueError:
        return None
    return y + 1 if m >= 10 else y


def is_foreign(rec: dict) -> bool:
    addr = rec.get("entityPhysicalAddress") or {}
    country = (addr.get("country") or {}).get("code", "") or ""
    return country.upper() not in ("USA", "")


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def load_enrichment(program: str) -> dict[str, dict]:
    """uei -> {naics4, naics_desc, country} from the per-program top-N SAM lookup."""
    enr: dict[str, dict] = {}
    path = PROGRAMS[program]["naics_csv"]
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            if uei:
                enr[uei] = {"naics4": (r.get("naics_4digit") or "").strip(),
                            "naics_desc": (r.get("naics_desc") or "").strip(),
                            "country": (r.get("country") or "").strip()}
    return enr


def load_scope(program: str) -> tuple[dict[str, dict], set[str]]:
    """(in_scope_piids meta, excluded MIB UEI set), restricted to shipbuilder groups
    for DDG."""
    cfg = PROGRAMS[program]
    with cfg["scope_json"].open(encoding="utf-8") as fh:
        scope = json.load(fh)
    piids = scope.get("in_scope_piids") or {}
    if cfg["groups"] is not None:
        piids = {p: v for p, v in piids.items() if v.get("group") in cfg["groups"]}
    mib = set((scope.get("excluded_mib_ueis") or {}).keys())
    return piids, mib


def scope_meta(program: str) -> dict[str, dict]:
    """piid -> scope meta (class, prime/group, label) for the in-corpus PIIDs."""
    return load_scope(program)[0]


# ---- the classified record stream -------------------------------------------------

def iter_records(program: str, registry: dict | None = None,
                 enrichment: dict | None = None):
    """Yield one classified dict per deduped in-scope published subaward record.

    Classification precedence = data_entity_master.classified_records():
    registry by entity UEI then parent UEI -> classify(vendor, naics4) ladder ->
    foreign-flag special case for unenriched unbucketed suppliers.

    Fields: program, piid, fy, date, vendor (entity legal name), parent_name,
    entity_uei, parent_uei, vendor_key (parent-first), dollar_m, foreign, country,
    naics4, naics_desc, role, bucket, basis, report_id, vclass (vessel class from
    scope meta), bgroup (builder group/prime from scope meta).
    """
    REG = load_registry() if registry is None else registry
    enr = load_enrichment(program) if enrichment is None else enrichment
    piids, mib = load_scope(program)
    fdir = PROGRAMS[program]["fullhistory"]

    seen_ids: set[str] = set()
    for path in sorted(fdir.glob("N*_subawards.json")):
        piid = path.stem.split("_")[0]
        if piid not in piids:
            continue
        pm = piids[piid]
        vclass = (pm.get("class") or "").strip()
        bgroup = (pm.get("group") or pm.get("prime") or "").strip()
        with path.open(encoding="utf-8") as fh:
            blob = json.load(fh)
        for r in blob.get("published") or []:
            rid = r.get("subAwardReportId") or ""
            if rid and rid in seen_ids:
                continue
            if rid:
                seen_ids.add(rid)

            eu = (r.get("subEntityUei") or "").strip()
            pu = (r.get("subParentUei") or "").strip()
            if eu in mib or pu in mib:
                continue

            vendor = (r.get("subEntityLegalBusinessName") or "").strip()
            parent_name = (r.get("subEntityParentLegalBusinessName") or "").strip()
            er = enr.get(eu) or enr.get(pu) or {}
            naics4 = er.get("naics4", "")
            foreign = is_foreign(r)

            reg = REG.get(eu) or REG.get(pu)
            if reg:
                role = reg["role"]
                bucket = reg["bucket"] or (UNBUCKETED if role == "supplier" else "")
                basis = "registry"
            else:
                role, bucket, basis = classify(vendor, naics4)
                if (role == "supplier" and bucket == UNBUCKETED and not naics4
                        and foreign):
                    role, bucket, basis = "foreign_fms", "", "foreign flag"

            date = (r.get("subAwardDate") or "").strip()
            yield {
                "program": program,
                "piid": piid,
                "fy": fy_of(date),
                "date": date,
                "vendor": vendor or "-",
                "parent_name": parent_name,
                "entity_uei": eu,
                "parent_uei": pu,
                "vendor_key": pu or eu or "-",
                "dollar_m": _f(r.get("subAwardAmount")) / 1e6,
                "foreign": foreign,
                "country": er.get("country") or ("Foreign" if foreign else "-"),
                "naics4": naics4,
                "naics_desc": er.get("naics_desc", ""),
                "role": role,
                "bucket": bucket,
                "basis": basis,
                "report_id": rid,
                "vclass": vclass,
                "bgroup": bgroup,
            }


def in_window(rec: dict, lo: int = FY22_25[0], hi: int = FY22_25[1]) -> bool:
    return rec["fy"] is not None and lo <= rec["fy"] <= hi
