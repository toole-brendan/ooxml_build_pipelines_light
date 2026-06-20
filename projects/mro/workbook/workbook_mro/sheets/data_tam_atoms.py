"""TAM Atoms

INTENT
    The mutually-exclusive TAM-atom ledger - the substrate of the SAM scenario
    engine. One atom per source row: every services-MRO Awards row (PSC in the 65
    MRO PSCs, Service in {Navy, Coast Guard}) plus every embedded PSC 1905 MRO PIID
    (Central buckets). Each atom carries ONE bucket per axis (work segment / hull /
    buyer-RMC / contractor tier / IDV scope / scope class / service) and a single
    Amount $M. A dollar may carry many tags but lives in exactly one atom, so
    SUM(Amount) ties to the Reconciled FPDS-visible MRO TAM by construction and a
    scenario can include/exclude atoms without ever double-counting.

    Built in Python at import (the DDG data_entity_master.py pattern): dollars come
    from exactly one source table per atom (Awards for services+depot, PSC1905
    Classified for embedded). J998J999Data is used ONLY to attach depot tags (RMC,
    tier, IDV scope, availability) via a left-join on PIID - never as a dollar source
    (Awards is hull-apportioned and TAM-canonical). Depot atoms with no J998J999
    match tag the depot-only axes "unmapped" (distinct from "n/a" on non-depot atoms)
    so the enrichment delta is disclosed, not silently dropped.

    Exposed as the native ``TAMAtoms`` table; inputs_scenarios builds its matrix rows
    from distinct_tags(axis) and model_sam_build runs the SUMIFS/SUMPRODUCT cube over
    the axis tag ranges.

LAYOUT
    row 2   : title
    row 4+  : §1 the atom ledger (native TAMAtoms table)
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.lib import EXTRACTED
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import PSC_CODES
from workbook_mro.sheets import taxonomy_mro as tx

_GROUP = "data"
_TAB = "TAM Atoms"
_TABLE_NAME = "TAMAtoms"   # stable: model_sam_build SUMIFS/SUMPRODUCT reference this

_PSC_SET = set(PSC_CODES)
_CENTRAL_BUCKETS = {"MRO (strong)", "MRO (TAS-confirmed)", "MRO (probable)"}
_SERVICES_UNIVERSE = "Services PSC"

# (header, is_numeric, axis_key|None). Headers are load-bearing.
_COLUMNS = [
    ("Atom ID",          False, None),
    ("Source Universe",  False, None),
    ("Source PIID",      False, None),
    ("Service",          False, "service"),
    ("PSC",              False, None),
    ("Work Segment",     False, "work_segment"),
    ("Hull Program",     False, "hull"),
    ("Hull Group",       False, None),
    ("Buyer / RMC",      False, "buyer_rmc"),
    ("Contractor Tier",  False, "contractor_tier"),
    ("IDV Scope Group",  False, "idv_scope"),
    ("Corporate Parent", False, None),
    ("Scope Class",      False, "scope_class"),
    ("Amount $M",        True,  None),
]
_HEADERS = [h for h, _n, _a in _COLUMNS]
_NCOLS = len(_COLUMNS)
# Content begins at column B (index 1); header[i] sits at column index 1+i.
_COL_LETTER = {h: col_letter(1 + i) for i, (h, _n, _a) in enumerate(_COLUMNS)}
_AXIS_HEADER = {a: h for h, _n, a in _COLUMNS if a}
_AMOUNT_COL = _COL_LETTER["Amount $M"]

# Per-atom cube helper columns sit just to the RIGHT of the ledger table (so the
# native TAMAtoms table stays the clean ledger). One Included flag column per
# scenario (in tx.SCENARIO_KEYS order) + an Included(selected) column.
_INC_FIRST_IDX = _NCOLS + 1                       # content col index after Amount $M
_INC_COL = {k: col_letter(_INC_FIRST_IDX + j) for j, k in enumerate(tx.SCENARIO_KEYS)}
_INC_FIRST_COL = _INC_COL[tx.SCENARIO_KEYS[0]]
_INC_LAST_COL = _INC_COL[tx.SCENARIO_KEYS[-1]]
_INC_SEL_COL = col_letter(_INC_FIRST_IDX + len(tx.SCENARIO_KEYS))
_TOTAL_NCOLS = _INC_FIRST_IDX + len(tx.SCENARIO_KEYS)   # ledger + 9 inc + 1 sel

# Deterministic layout: title(2) blank(3) §1 banner(4) blank(5) header(6) data(7+).
_HDR_ROW = 6
_FIRST_DATA = 7


def _num(x) -> float:
    s = str(x).replace(",", "").strip()
    if s == "":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def _load(name: str) -> list[dict]:
    with (EXTRACTED / name).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _build_atoms() -> tuple[list[dict], dict]:
    """Return (atoms, diagnostics). One dict per atom with every axis tag + amount."""
    # J998J999 depot-tag dictionary, keyed by PIID (one task order per PIID).
    j_by_piid: dict[str, dict] = {}
    j998_total = 0.0
    for r in _load("j998_j999.csv"):
        piid = (r.get("PIID") or "").strip()
        j998_total += _num(r.get("FY2025 Obligation"))
        if piid:
            j_by_piid[piid] = r

    atoms: list[dict] = []
    n_svc = n_emb = 0
    depot_total = depot_unmapped = 0.0

    # Services + depot atoms from Awards (PSC in 65, Service in {Navy, Coast Guard}).
    for r in _load("awards.csv"):
        psc = (r.get("PSC") or "").strip()
        svc = (r.get("Service") or "").strip()
        if psc not in _PSC_SET or svc not in ("Navy", "Coast Guard"):
            continue
        amount = _num(r.get("FY2025 Obligation")) / 1e6
        if amount == 0.0:
            continue
        seg = tx.work_segment_for_psc(psc)
        hp = (r.get("Hull Program") or "").strip()
        is_depot = psc in tx.DEPOT_PSCS
        avail = ""
        if is_depot:
            piid = (r.get("PIID") or "").strip()
            m = j_by_piid.get(piid)
            if m:
                buyer = tx.rmc_bucket(m.get("RMC"))
                tier = (m.get("Contractor Tier") or "").strip() or "Other"
                idv = (m.get("IDV Scope Group") or "").strip() or tx.UNCLASSIFIED
                avail = (m.get("Availability Group") or "").strip()
            else:
                buyer = tier = idv = tx.UNMAPPED
            depot_total += amount
            if not m:
                depot_unmapped += amount
        else:
            buyer = tier = idv = tx.NA
        scope = tx.scope_class_for(source_universe=_SERVICES_UNIVERSE,
                                   ultimate_parent=r.get("Ultimate Parent"),
                                   availability_group=avail)
        n_svc += 1
        atoms.append({
            "atom_id": f"S{n_svc:05d}",
            "source_universe": _SERVICES_UNIVERSE,
            "source_piid": (r.get("PIID") or "").strip(),
            "service": svc,
            "psc": psc,
            "work_segment": seg,
            "hull": tx.hull_program(hp),
            "hull_group": tx.hull_group(hp),
            "buyer_rmc": buyer,
            "contractor_tier": tier,
            "idv_scope": idv,
            "corporate_parent": (r.get("Corporate Parent") or "").strip() or "-",
            "scope_class": scope,
            "amount": amount,
        })

    # Embedded atoms from PSC 1905 Classified (Central MRO buckets).
    for r in _load("psc_1905_classified.csv"):
        if (r.get("bucket") or "").strip() not in _CENTRAL_BUCKETS:
            continue
        amount = _num(r.get("fy2025_obligation")) / 1e6
        if amount == 0.0:
            continue
        hp = (r.get("hull_program") or "").strip()
        scope = tx.scope_class_for(source_universe=tx.EMBEDDED_SEGMENT,
                                   ultimate_parent=r.get("ultimate_parent_name"),
                                   availability_group="")
        n_emb += 1
        atoms.append({
            "atom_id": f"E{n_emb:05d}",
            "source_universe": tx.EMBEDDED_SEGMENT,
            "source_piid": (r.get("piid") or "").strip(),
            "service": (r.get("service") or "").strip() or "Navy",
            "psc": "1905",
            "work_segment": tx.EMBEDDED_SEGMENT,
            "hull": tx.hull_program(hp),
            "hull_group": tx.hull_group(hp),
            "buyer_rmc": tx.NA,
            "contractor_tier": tx.NA,
            "idv_scope": tx.NA,
            "corporate_parent": (r.get("corporate_parent") or "").strip() or "-",
            "scope_class": scope,
            "amount": amount,
        })

    diag = {
        "n_services": n_svc, "n_embedded": n_emb,
        "services_total_m": sum(a["amount"] for a in atoms if a["source_universe"] == _SERVICES_UNIVERSE),
        "embedded_total_m": sum(a["amount"] for a in atoms if a["source_universe"] == tx.EMBEDDED_SEGMENT),
        "depot_total_m": depot_total, "depot_unmapped_m": depot_unmapped,
        "j998_total_m": j998_total,
    }
    return atoms, diag


_ATOMS, _DIAG = _build_atoms()

# Build-time guards (fail the build loudly rather than ship a broken cube).
_ids = [a["atom_id"] for a in _ATOMS]
assert len(_ids) == len(set(_ids)), "TAMAtoms: duplicate Atom ID"
assert 6000 < _DIAG["services_total_m"] < 9000, f"services atom total off: {_DIAG['services_total_m']:.1f}"
assert 1000 < _DIAG["embedded_total_m"] < 3000, f"embedded atom total off: {_DIAG['embedded_total_m']:.1f}"

# Distinct tags per axis (drives the Scenarios matrix + the coverage assertion).
_DISTINCT = {
    axis: sorted({a[tx.AXIS_FIELD[axis]] for a in _ATOMS})
    for axis in tx.AXIS_KEYS
}
_LAST_DATA = _FIRST_DATA + len(_ATOMS) - 1


# ── Accessors (constant positions; available at import for downstream sheets) ──
def atom_first_row() -> int: return _FIRST_DATA
def atom_last_row() -> int: return _LAST_DATA
def n_atoms() -> int: return len(_ATOMS)
def distinct_tags(axis: str) -> list[str]: return list(_DISTINCT[axis])
def diagnostics() -> dict: return dict(_DIAG)


def _rng(col: str) -> str:
    return f"'{_TAB}'!${col}${_FIRST_DATA}:${col}${_LAST_DATA}"


def amount_range() -> str: return _rng(_AMOUNT_COL)
def axis_tag_range(axis: str) -> str: return _rng(_COL_LETTER[_AXIS_HEADER[axis]])
def tag_range(header: str) -> str: return _rng(_COL_LETTER[header])
def atom_id_range() -> str: return _rng(_COL_LETTER["Atom ID"])
def included_range(k: str) -> str: return _rng(_INC_COL[k])
def included_selected_range() -> str: return _rng(_INC_SEL_COL)


def _render() -> WorksheetSpec:
    # Lazy imports break the data<->inputs cycle (Scenarios imports distinct_tags
    # at module load; we only need its ranges here, at render time).
    from workbook_mro.sheets.inputs_scenarios import (
        scenario_keys, flag_axis_range, key_axis_range, scenario_header_range)
    from workbook_mro.sheets.inputs_assumptions import selected_scenario_cell
    scen_keys = scenario_keys()
    assert scen_keys == tx.SCENARIO_KEYS, "scenario key order drift"
    sel = selected_scenario_cell()
    hdr_range = scenario_header_range()

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_TOTAL_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner(f"§1 - TAM atoms ({len(_ATOMS):,} rows; SUM(Amount $M) = Reconciled MRO TAM). "
             "Columns to the right of Amount are the scenario-inclusion cube.",
             n_cols=_TOTAL_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    inc_headers = [f"inc_{k}" for k in scen_keys] + ["inc_selected"]
    hdr_styles = ([S_HEADER_CENTER if is_num else S_HEADER_LEFT for _h, is_num, _a in _COLUMNS]
                  + [S_HEADER_CENTER] * len(inc_headers))
    hdr = c.write(_HEADERS + inc_headers, styles=hdr_styles)
    assert hdr == _HDR_ROW, f"TAM Atoms header at {hdr}, expected {_HDR_ROW}"

    base_styles = [S_DEFAULT] * (_NCOLS - 1) + [S_NUM_INPUT]
    inc_styles = [S_NUM_INPUT] * len(scen_keys) + [S_NUM_INPUT]
    for i, a in enumerate(_ATOMS):
        r = _FIRST_DATA + i
        ledger = [a["atom_id"], a["source_universe"], a["source_piid"], a["service"],
                  a["psc"], a["work_segment"], a["hull"], a["hull_group"], a["buyer_rmc"],
                  a["contractor_tier"], a["idv_scope"], a["corporate_parent"],
                  a["scope_class"], a["amount"]]
        inc = []
        for k in scen_keys:
            factors = [f"SUMIFS({flag_axis_range(k, axis)},{key_axis_range(axis)},"
                       f"${_COL_LETTER[_AXIS_HEADER[axis]]}{r})" for axis in tx.AXIS_KEYS]
            inc.append("=" + "*".join(factors))
        inc.append(f"=INDEX(${_INC_FIRST_COL}{r}:${_INC_LAST_COL}{r},1,"
                   f"MATCH({sel},{hdr_range},0))")
        c.write(ledger + inc, styles=base_styles + inc_styles, outline_level=1)
    last_data = c.at() - 1
    assert last_data == _LAST_DATA, f"TAM Atoms last data {last_data}, expected {_LAST_DATA}"

    tables = [ExcelTable(name=_TABLE_NAME,
                         ref=f"B{_HDR_ROW}:{col_letter(_NCOLS)}{_LAST_DATA}", headers=_HEADERS)]
    cols = ([12, 16, 22, 11, 8, 30, 13, 24, 12, 26, 22, 24, 14, 12]
            + [8] * (len(scen_keys) + 1))
    ws = worksheet(c.rows, cols=cols, tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=tables)


TAM_ATOMS = SheetEntry(_TAB, _GROUP, _render)
