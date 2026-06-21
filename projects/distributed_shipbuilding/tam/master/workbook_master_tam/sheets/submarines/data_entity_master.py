"""data_entity_master - the "Entity Master" tab (one module = one sheet).

Subaward vendor classification (the native table), plus the role / bucket / basis
summaries derived from it. The table also carries the work-type share gate as
per-entity columns (GDEB $ + Virginia/Columbia dollars per FY2022-25 subaward
year), which Worktype by FY sums live into the per-class share vectors. §4's
full-corpus observed bucket shares stay as the reference view; Figure Register's
DO-07 reads addressable_total_cell().

Role meanings (kept here, not as a cell column): supplier = supplier-addressable
(seeds the SAM bucket shares); prime / co_prime = final-assembly yards, not
addressable; gfe_sib = GFE / SIB / Navy-directed, excluded scope; service =
non-component, not addressable.

Promoted accessors: the table ranges (ent_dollar/role/bucket/country/naics/basis,
gdeb_dollar_range / class_fy_range for the gate), classified_records (the single
classification pass), ent_row_cell / top_vendor_indices for Worktype Evidence, and
the corpus observed-bucket reference (observed_bucket_dollar_cell /
observed_bucket_share_cell / addressable_total_cell).
"""
from __future__ import annotations

import csv
import json

from workbook_core.primitives import worksheet, banner_row, write_row, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines.taxonomy import classify, BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_master_tam.sheets.submarines._registry import load_registry
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub Entity Master"
_Q = '"'
_TBL_BASE = 14                                   # title(2) + blank + §1 at-a-glance(4-11) + 2 blanks

# (basis key) - which classification rule fired; order = display order.
_BASIS_KEYS = ["vendor-override", "naics4", "service NAICS", "prime/co-prime name",
               "GFE/SIB name", "holding-co (parent unknown)", "residual"]

# The work-type share gate (rendered as per-entity Va/Col FY columns; Worktype by
# FY sums them live): GDEB construction/LLTM PIIDs only, split by the scope map's
# Virginia/Columbia class, FY2022-FY2025 subaward years.
WT_FY_WINDOW = [2022, 2023, 2024, 2025]
WT_CLASSES = [("va", "Virginia"), ("col", "Columbia")]
_CLS_KEY = {name: key for key, name in WT_CLASSES}


def _piid_meta() -> dict:
    with (EXTRACTED / "nc_scope_summary.json").open(encoding="utf-8") as fh:
        scope = json.load(fh)
    return {p: (v["prime"], v["class"]) for p, v in scope["in_scope_piids"].items()}


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def classified_records():
    """Every FFATA subaward record, classified registry-FIRST (operating-entity
    overrides keyed by sub_entity_uei), falling back to the NAICS/name ladder.
    The single classification pass: the entity table aggregates it by entity;
    Worktype by FY aggregates it by class/bucket/subaward FY. Yields one dict per
    record: piid, fy, vendor, uei, country, naics4, naics_desc, dollar_m, role,
    bucket, basis, modular, vls. SIGNED dollars (de-obligations net out)."""
    # enrichment: UEI -> NAICS-4 / NAICS desc / country (the top-150 lookup)
    enr: dict[str, dict] = {}
    with (EXTRACTED / "entity_naics_lookup.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            if uei:
                enr[uei] = {"naics4": (r.get("naics_4digit") or "").strip(),
                            "naics_desc": (r.get("naics_desc") or "").strip(),
                            "country": (r.get("country") or "").strip()}
    REG = load_registry()
    with (EXTRACTED / "nc_records_long.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            vendor = (r.get("sub_name") or "").strip()
            eu = (r.get("sub_entity_uei") or "").strip()
            pu = (r.get("sub_parent_uei") or "").strip()
            er = enr.get(eu) or enr.get(pu) or {}
            naics4 = er.get("naics4", "")
            amt = _f(r.get("subAwardAmount_$")) / 1e6
            reg = REG.get(eu) or REG.get(pu)
            if reg:
                role = reg["role"]
                bucket = reg["bucket"] or (UNBUCKETED if role == "supplier" else "")
                basis = "registry"
                modular, vls = reg["modular"], reg["vls"]
            else:
                role, bucket, basis = classify(vendor, naics4)
                if (role == "supplier" and bucket == UNBUCKETED and not naics4
                        and (r.get("foreign") or "").strip()):
                    role, bucket, basis = "foreign_fms", "", "foreign flag"
                modular = vls = False
            country = er.get("country") or ("Foreign" if (r.get("foreign") or "").strip() else "-")
            yield {"piid": (r.get("piid") or "").strip(), "fy": int(r["fy"]),
                   "vendor": vendor, "uei": eu or pu or "-", "country": country,
                   "naics4": naics4, "naics_desc": er.get("naics_desc", ""),
                   "dollar_m": amt, "role": role, "bucket": bucket, "basis": basis,
                   "modular": modular, "vls": vls}


def _build_entity_table(tab: str, base: int):
    _HEADERS = (["Vendor", "UEI", "Country", "NAICS-4", "NAICS desc", "$M", "Role", "Bucket",
                 "Class rule", "Modular", "VLS", "GDEB $M"]
                + [f"Va FY{fy % 100}" for fy in WT_FY_WINDOW]
                + [f"Col FY{fy % 100}" for fy in WT_FY_WINDOW])
    _COL = {"vendor": 1, "uei": 2, "country": 3, "naics4": 4, "naics_desc": 5,
            "dollar": 6, "role": 7, "bucket": 8, "basis": 9, "modular": 10, "vls": 11,
            "gdeb": 12,
            **{f"vafy{fy}": 13 + i for i, fy in enumerate(WT_FY_WINDOW)},
            **{f"colfy{fy}": 13 + len(WT_FY_WINDOW) + i for i, fy in enumerate(WT_FY_WINDOW)}}

    def _load_rows():
        # aggregate the classified record stream by (vendor, uei, role, bucket); the
        # GDEB / Va / Col columns split each entity's dollars by the work-type gate
        meta = _piid_meta()
        groups: dict[tuple, dict] = {}
        for rec in classified_records():
            key = (rec["vendor"], rec["uei"], rec["role"], rec["bucket"])
            g = groups.get(key)
            if g is None:
                g = groups[key] = {
                    "vendor": rec["vendor"] or "-", "uei": rec["uei"],
                    "country": rec["country"] or "-",
                    "naics4": rec["naics4"] or "-", "naics_desc": rec["naics_desc"] or "-",
                    "dollar_m": 0.0, "role": rec["role"], "bucket": rec["bucket"] or "-",
                    "modular": 1 if rec["modular"] else 0, "vls": 1 if rec["vls"] else 0,
                    "gdeb_m": 0.0,
                    "cls_fy": {(ck, fy): 0.0 for ck, _n in WT_CLASSES for fy in WT_FY_WINDOW},
                    "_basis": {}}
            g["dollar_m"] += rec["dollar_m"]
            prime, cls = meta.get(rec["piid"], ("", ""))
            if prime == "GDEB":
                g["gdeb_m"] += rec["dollar_m"]
                ck = _CLS_KEY.get(cls)
                if ck and rec["fy"] in WT_FY_WINDOW:
                    g["cls_fy"][(ck, rec["fy"])] += rec["dollar_m"]
            g["_basis"][rec["basis"]] = g["_basis"].get(rec["basis"], 0) + 1
        # 3. one row per group; basis = the dominant arbiter (+N when records mixed)
        out = []
        for g in groups.values():
            bset = g.pop("_basis")
            dom = max(bset, key=bset.get)
            g["basis"] = dom + (f" +{len(bset) - 1}" if len(bset) > 1 else "")
            out.append(g)
        out.sort(key=lambda r: r["dollar_m"], reverse=True)
        return out

    rows_data = _load_rows()
    n_gate_cols = 1 + 2 * len(WT_FY_WINDOW)
    c = RowCursor(base)
    c.banner("§2 - Entity classification (registry/NAICS-led; GDEB/Va/Col columns = gated work-type evidence, see Worktype by FY)",
             n_cols=11 + n_gate_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = ([S_HEADER_LEFT] * 5 + [S_HEADER_CENTER] + [S_HEADER_LEFT] * 3
           + [S_HEADER_CENTER] * (2 + n_gate_cols))
    header_row = c.write(_HEADERS, styles=hdr)
    first_data = c.at()
    row_styles = ([S_DEFAULT] * 5 + [S_NUM_INPUT] + [S_DEFAULT] * 3
                  + [S_NUM_INPUT] * (2 + n_gate_cols))
    for r in rows_data:
        c.write([r["vendor"], r["uei"], r["country"], r["naics4"], r["naics_desc"],
                 r["dollar_m"], r["role"], r["bucket"], r["basis"], r["modular"], r["vls"],
                 r["gdeb_m"]]
                + [r["cls_fy"][("va", fy)] for fy in WT_FY_WINDOW]
                + [r["cls_fy"][("col", fy)] for fy in WT_FY_WINDOW],
                styles=row_styles, outline_level=1)
    last_data = c.at() - 1

    table = ExcelTable(name="tbl_sub_entity_master",
                       ref=f"B{header_row}:{col_letter(len(_HEADERS))}{last_data}",
                       headers=_HEADERS)

    def _rng(key):
        cc = col_letter(_COL[key])
        return f"'{tab}'!{cc}{first_data}:{cc}{last_data}"

    def row_cell(i, key): return f"'{tab}'!{col_letter(_COL[key])}{first_data + i}"

    def top_vendor_indices(bucket, n):
        return [i for i, r in enumerate(rows_data)
                if r["role"] == "supplier" and r["bucket"] == bucket][:n]

    def top_supplier_indices(n):
        return [i for i, r in enumerate(rows_data) if r["role"] == "supplier"][:n]

    def unbucketed_vendor_indices(n):
        return [i for i, r in enumerate(rows_data)
                if r["role"] == "supplier" and r["bucket"] == UNBUCKETED][:n]

    def class_fy_range(cls, fy):
        if cls not in ("va", "col"):
            raise ValueError(f"Unknown class {cls!r}; expected 'va' or 'col'")
        if fy not in WT_FY_WINDOW:
            raise ValueError(f"FY {fy!r} outside {WT_FY_WINDOW!r}")
        return _rng(f"{cls}fy{fy}")

    acc = dict(ent_dollar_range=lambda: _rng("dollar"), role_range=lambda: _rng("role"),
               bucket_range=lambda: _rng("bucket"), country_range=lambda: _rng("country"),
               naics_range=lambda: _rng("naics4"), basis_range=lambda: _rng("basis"),
               modular_range=lambda: _rng("modular"), vls_range=lambda: _rng("vls"),
               gdeb_dollar_range=lambda: _rng("gdeb"), class_fy_range=class_fy_range,
               ent_first_data_row=lambda: first_data, ent_last_data_row=lambda: last_data,
               ent_row_cell=row_cell, top_vendor_indices=top_vendor_indices,
               top_supplier_indices=top_supplier_indices,
               unbucketed_vendor_indices=unbucketed_vendor_indices,
               observed_addressable_total=lambda: sum(r["dollar_m"] for r in rows_data if r["role"] == "supplier"),
               n_entities=lambda: len(rows_data))
    return c.rows, c.at(), [table], acc


def _build_summaries(tab: str, base: int, tab_acc):
    _role, _bkt, _dol, _basis = (tab_acc["role_range"], tab_acc["bucket_range"],
                                 tab_acc["ent_dollar_range"], tab_acc["basis_range"])
    _mod, _vls = tab_acc["modular_range"], tab_acc["vls_range"]

    def _sp(*m): return f"SUMPRODUCT({'*'.join(m)})"
    def _rmask(role): return f"({_role()}={_Q}{role}{_Q})"
    def _bmask(b): return f"({_bkt()}={_Q}{b}{_Q})"
    def _basmask(b): return f"({_basis()}={_Q}{b}{_Q})"
    def _flag(rng): return f"({rng()}=1)"
    bucket_name = {k: name for k, name, _ in BUCKETS}

    c = RowCursor(base)

    # §3 Role summary (supplier = addressable; everything else excluded by market definition)
    c.banner("§3 - Role summary ($ by role; only 'supplier' is addressable)", n_cols=11,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Role", "$M", "% of total"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    role_keys = ["supplier", "mission_systems", "service", "holding", "foreign_fms",
                 "prime", "co_prime", "gfe_sib"]
    role_first = c.at()
    grand_row = role_first + len(role_keys)
    grand = f"$C${grand_row}"
    role_pos = {}
    for rk in role_keys:
        r = c.at()
        role_pos[rk] = c.write([rk, f"={_sp(_rmask(rk), _dol())}", f"=C{r}/{grand}"],
                               styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    assert c.at() == grand_row
    c.total(["Grand total (all recipients)", f"={_sp(_dol())}", None],
            styles=[S_BOLD, S_NUM, S_DEFAULT], n_cols=3)
    c.blank(2)

    # §4 Bucket summary - full-corpus reference (the applied per-class shares live
    # on Worktype by FY / SAM Build)
    c.banner("§4 - Bucket summary (observed supplier $ + share; full corpus reference)", n_cols=11,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Supplier $M", "Observed share"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    bucket_first = c.at()
    unb_row = bucket_first + len(BUCKET_KEYS)
    addr_row = unb_row + 1
    addr = f"$C${addr_row}"
    bucket_pos = {}
    for k in BUCKET_KEYS:
        r = c.at()
        bucket_pos[k] = c.write([bucket_name[k], f"={_sp(_rmask('supplier'), _bmask(k), _dol())}", f"=C{r}/{addr}"],
                                styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    assert c.at() == unb_row
    unb_pos = c.write(["Unbucketed / ambiguous", f"={_sp(_rmask('supplier'), _bmask(UNBUCKETED), _dol())}",
                       f"=C{unb_row}/{addr}"], styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    assert c.at() == addr_row
    c.total(["Supplier-addressable total", f"={_sp(_rmask('supplier'), _dol())}", f"=C{addr_row}/{addr}"],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=3)
    c.blank(2)

    # §4b Scenario-tag observations (entity-flagged; not buckets)
    c.banner("§4b - Entity-flagged scenario tags (modular assembly; VLS launch-control boundary)",
             n_cols=11, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Tag", "$M", "Share of addressable"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    mod_row = c.write(["Modular assemblies (entity-flagged)",
                       f"={_sp(_rmask('supplier'), _flag(_mod), _dol())}", f"=C{c.at()}/{addr}"],
                      styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    vls_row = c.write(["VLS launch-control (sensitivity boundary; excluded base case)",
                       f"={_sp(_flag(_vls), _dol())}", f"=C{c.at()}/{addr}"],
                      styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    c.blank(2)

    # §5 Classification basis
    c.banner("§5 - Classification rule (which rule fired)", n_cols=11,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class rule", "Entity count", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    for bkey in _BASIS_KEYS:
        c.write([bkey, f"={_sp(_basmask(bkey))}", f"={_sp(_basmask(bkey), _dol())}"],
                styles=[S_DEFAULT, S_NUM, S_NUM], outline_level=1)

    acc = dict(
        role_dollar_cell=lambda role: f"'{tab}'!C{role_pos[role]}",
        grand_total_cell=lambda: f"'{tab}'!C{grand_row}",
        observed_bucket_dollar_cell=lambda b: f"'{tab}'!C{bucket_pos[b] if b in bucket_pos else unb_pos}",
        observed_bucket_share_cell=lambda b: f"'{tab}'!D{bucket_pos[b] if b in bucket_pos else unb_pos}",
        addressable_total_cell=lambda: f"'{tab}'!C{addr_row}",
        observed_modular_dollar_cell=lambda: f"'{tab}'!C{mod_row}",
        observed_modular_share_cell=lambda: f"'{tab}'!D{mod_row}",
        vls_boundary_dollar_cell=lambda: f"'{tab}'!C{vls_row}")
    return c.rows, c.at(), acc


# ── Layout pass ──────────────────────────────────────────────────────────────
_tbl_rows, _after_tbl, _tables, _tbl_acc = _build_entity_table(_TAB, _TBL_BASE)
_SUM_BASE = _after_tbl + 2                        # 2 blanks between the table and §3
_sum_rows, _after_sum, _sum_acc = _build_summaries(_TAB, _SUM_BASE, _tbl_acc)

ent_dollar_range = _tbl_acc["ent_dollar_range"]; role_range = _tbl_acc["role_range"]
bucket_range = _tbl_acc["bucket_range"]; country_range = _tbl_acc["country_range"]
naics_range = _tbl_acc["naics_range"]; basis_range = _tbl_acc["basis_range"]
gdeb_dollar_range = _tbl_acc["gdeb_dollar_range"]; class_fy_range = _tbl_acc["class_fy_range"]
ent_first_data_row = _tbl_acc["ent_first_data_row"]; ent_last_data_row = _tbl_acc["ent_last_data_row"]
ent_row_cell = _tbl_acc["ent_row_cell"]; top_vendor_indices = _tbl_acc["top_vendor_indices"]
top_supplier_indices = _tbl_acc["top_supplier_indices"]
unbucketed_vendor_indices = _tbl_acc["unbucketed_vendor_indices"]
observed_addressable_total = _tbl_acc["observed_addressable_total"]; _n_entities = _tbl_acc["n_entities"]
modular_range = _tbl_acc["modular_range"]; vls_range = _tbl_acc["vls_range"]
role_dollar_cell = _sum_acc["role_dollar_cell"]; grand_total_cell = _sum_acc["grand_total_cell"]
observed_bucket_dollar_cell = _sum_acc["observed_bucket_dollar_cell"]
observed_bucket_share_cell = _sum_acc["observed_bucket_share_cell"]
addressable_total_cell = _sum_acc["addressable_total_cell"]
observed_modular_dollar_cell = _sum_acc["observed_modular_dollar_cell"]
observed_modular_share_cell = _sum_acc["observed_modular_share_cell"]
vls_boundary_dollar_cell = _sum_acc["vls_boundary_dollar_cell"]


def _render_entity_master() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("Entity Master", n_cols=11, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Supplier-addressable base", n_cols=11, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "$M / count"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Total entities", _n_entities()],
            styles=[S_DEFAULT, S_DEFAULT])
    c.write(["Supplier-addressable subaward total $M", f"={addressable_total_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["Prime / co-prime total $M", f"={role_dollar_cell('prime')}+{role_dollar_cell('co_prime')}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["GFE / SIB total $M", f"={role_dollar_cell('gfe_sib')}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Unbucketed supplier $M", f"={observed_bucket_dollar_cell(UNBUCKETED)}"],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _TBL_BASE, f"at-a-glance ends at {c.at()}, expected {_TBL_BASE}"
    c.feed(_tbl_rows, _after_tbl)
    c.blank(2)
    c.feed(_sum_rows, _after_sum)

    ws = worksheet(c.rows, cols=[40, 22, 12, 12, 30, 11, 11, 12, 22, 9, 7,
                                 12, 11, 11, 11, 11, 11, 11, 11, 11],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=_tables)


ENTITY_MASTER = SheetEntry(_TAB, _GROUP, _render_entity_master)
