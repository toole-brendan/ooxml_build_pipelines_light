"""data_entity_master - the "Entity Master" tab (DDG, data group; one module = one sheet).

Subaward classification used by the SAM bucket shares. Classification is
REGISTRY-LED: every FFATA subaward record in ``nc_records_long.csv`` is classified by
the operating-entity evidence registry (keyed on sub_entity_uei) FIRST, falling back
to ``_taxonomy.classify(vendor, naics4)`` (NAICS-4 enriched per UEI from
``entity_naics_lookup.csv``) for entities not in the registry. The registry carries
role + bucket + the modular / VLS scenario flags. Records are aggregated to one row
per (vendor, UEI, role, bucket). Excluded roles (mission_systems / service / holding /
foreign_fms / prime / gfe_mib) drop out of the supplier-addressable base. Role and
bucket summaries roll up the table. Native table: tbl_ddg_entity_master.

Promoted accessors (consumed by sam_build + bucket_evidence + sensitivity):
  ent_dollar_range, role_range, bucket_range, country_range, naics_range,
  modular_range, vls_range, ent_first_data_row, ent_last_data_row, ent_row_cell,
  top_vendor_indices, observed_addressable_total
"""
from __future__ import annotations

import csv
import json

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg._taxonomy import classify, BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_master_tam.sheets.ddg._registry import load_registry
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG Entity Master"
_NCOLS = 16
_Q = '"'

# The work-type share gate (rendered as per-entity Yard columns; Worktype by FY
# sums them live): yard construction PIIDs only, FY2022-FY2025 subaward years.
YARD_GROUPS = {"GD-BIW", "HII-Ingalls"}
WT_FY_WINDOW = [2022, 2023, 2024, 2025]


def _piid_groups() -> dict:
    with (EXTRACTED / "nc_scope_summary.json").open(encoding="utf-8") as fh:
        scope = json.load(fh)
    return {p: v["group"] for p, v in scope["in_scope_piids"].items()}


def _f(x) -> float:
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def classified_records():
    """Every FFATA subaward record, classified registry-FIRST (operating-entity
    overrides keyed by sub_entity_uei), falling back to the NAICS/name ladder.
    The single classification pass: the entity table aggregates it by entity;
    Worktype by FY aggregates it by bucket x subaward FY. Yields one dict per
    record: piid, fy, vendor, uei, country, naics4, naics_desc, dollar_m, role,
    bucket, basis, modular, vls."""
    # enrichment: UEI -> NAICS-4 / NAICS desc / country (the 150-vendor lookup)
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
            desc = (r.get("description_of_requirement") or "").strip()
            amt = _f(r.get("subAwardAmount_$")) / 1e6
            reg = REG.get(eu) or REG.get(pu)
            if reg:
                role = reg["role"]
                bucket = reg["bucket"] or (UNBUCKETED if role == "supplier" else "")
                basis = "registry"
                modular, vls = reg["modular"], reg["vls"]
            else:
                role, bucket, basis = classify(vendor, naics4, desc)
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


def _make_entities():
    _ENT_HEADERS = ["Vendor", "UEI", "Country", "NAICS-4", "NAICS desc", "$M",
                    "Role", "Bucket", "Arbiter", "Modular", "VLS",
                    "Yard $M"] + [f"Yard FY{fy % 100}" for fy in WT_FY_WINDOW]
    _ENT_COL = {"vendor": 1, "uei": 2, "country": 3, "naics4": 4, "naics_desc": 5,
                "dollar": 6, "role": 7, "bucket": 8, "basis": 9, "modular": 10, "vls": 11,
                "yard": 12, **{f"yfy{fy}": 13 + i for i, fy in enumerate(WT_FY_WINDOW)}}
    _bucket_name = {k: name for k, name, _ in BUCKETS}

    def _ent_load():
        # aggregate the classified record stream by (vendor, uei, role, bucket);
        # the Yard columns split each entity's dollars by the work-type share gate
        grp = _piid_groups()
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
                    "yard_m": 0.0, "yfy": {fy: 0.0 for fy in WT_FY_WINDOW}, "_basis": {}}
            g["dollar_m"] += rec["dollar_m"]
            if grp.get(rec["piid"]) in YARD_GROUPS:
                g["yard_m"] += rec["dollar_m"]
                if rec["fy"] in g["yfy"]:
                    g["yfy"][rec["fy"]] += rec["dollar_m"]
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

    _ENT = _ent_load()
    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Entity classification (native table)
    c.banner("§1 - Subaward classification (registry/NAICS-led; Yard columns = yard-construction-PIID $, the Worktype by FY gate)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _ent_header = c.write(_ENT_HEADERS,
                          styles=[S_HEADER_LEFT] * 5 + [S_HEADER_CENTER] + [S_HEADER_LEFT] * 3
                                 + [S_HEADER_CENTER] * (2 + 1 + len(WT_FY_WINDOW)))
    _ent_first = c.at()
    _ent_styles = ([S_DEFAULT] * 5 + [S_NUM_INPUT] + [S_DEFAULT] * 3 + [S_NUM_INPUT] * 2
                   + [S_NUM_INPUT] * (1 + len(WT_FY_WINDOW)))
    for r in _ENT:
        c.write([r["vendor"], r["uei"], r["country"], r["naics4"], r["naics_desc"],
                 r["dollar_m"], r["role"], r["bucket"], r["basis"], r["modular"], r["vls"],
                 r["yard_m"]] + [r["yfy"][fy] for fy in WT_FY_WINDOW],
                styles=_ent_styles, outline_level=1)
    _ent_last = c.at() - 1
    tables.append(ExcelTable(name="tbl_ddg_entity_master",
                             ref=f"B{_ent_header}:{col_letter(len(_ENT_HEADERS))}{_ent_last}",
                             headers=_ENT_HEADERS))

    # accessors (defined now so the summaries below can use them)
    def _ent_rng(key: str) -> str:
        col = col_letter(_ENT_COL[key])
        return f"'{_TAB}'!{col}{_ent_first}:{col}{_ent_last}"

    def ent_dollar_range() -> str: return _ent_rng("dollar")
    def role_range() -> str:       return _ent_rng("role")
    def bucket_range() -> str:     return _ent_rng("bucket")
    def country_range() -> str:    return _ent_rng("country")
    def naics_range() -> str:      return _ent_rng("naics4")
    def modular_range() -> str:    return _ent_rng("modular")
    def vls_range() -> str:        return _ent_rng("vls")
    def yard_dollar_range() -> str: return _ent_rng("yard")

    def yard_fy_range(fy: int) -> str:
        if fy not in WT_FY_WINDOW:
            raise ValueError(f"FY {fy!r} outside {WT_FY_WINDOW!r}")
        return _ent_rng(f"yfy{fy}")

    def ent_first_data_row() -> int: return _ent_first
    def ent_last_data_row() -> int:  return _ent_last

    def ent_row_cell(i: int, key: str) -> str:
        return f"'{_TAB}'!{col_letter(_ENT_COL[key])}{_ent_first + i}"

    def top_vendor_indices(bucket: str, n: int) -> list[int]:
        idx = [i for i, r in enumerate(_ENT) if r["role"] == "supplier" and r["bucket"] == bucket]
        return idx[:n]

    def top_supplier_indices(n: int) -> list[int]:
        """Indices of the top-n supplier rows overall (any bucket), by subaward $."""
        idx = [i for i, r in enumerate(_ENT) if r["role"] == "supplier"]
        return idx[:n]

    def observed_addressable_total() -> float:
        return sum(r["dollar_m"] for r in _ENT if r["role"] == "supplier")

    def _sp(*m): return f"SUMPRODUCT({'*'.join(m)})"
    def _role_mask(rk): return f"({role_range()}={_Q}{rk}{_Q})"
    def _bkt_mask(b): return f"({bucket_range()}={_Q}{b}{_Q})"

    c.blank(2)

    # §2 Role summary (supplier = addressable; everything else excluded by market definition)
    c.banner("§2 - Role summary (signed $; only 'supplier' is addressable)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Role", "$M (signed)"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    for rk, label in [("supplier", "Supplier (addressable)"), ("mission_systems", "Mission systems (excluded)"),
                      ("service", "Service / non-component (excluded)"), ("holding", "Holding / parent unknown (excluded)"),
                      ("foreign_fms", "Foreign / FMS (excluded)"), ("prime", "Prime yard (dropped)"),
                      ("co_prime", "Co-prime yard (dropped)"), ("gfe_mib", "GFE / MIB / Navy-directed (dropped)")]:
        c.write([label, f"={_sp(_role_mask(rk), ent_dollar_range())}"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)

    # §3 Bucket summary
    c.banner("§3 - Bucket summary", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Supplier $M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    for k in BUCKET_KEYS:
        c.write([_bucket_name[k], f"={_sp(_role_mask('supplier'), _bkt_mask(k), ent_dollar_range())}"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[40, 16, 12, 13, 30, 12, 12, 12, 22, 9, 7,
                                     12, 11, 11, 11, 11],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return (SheetEntry(_TAB, _GROUP, render),
            ent_dollar_range, role_range, bucket_range, country_range, naics_range,
            ent_first_data_row, ent_last_data_row, ent_row_cell, top_vendor_indices,
            top_supplier_indices, observed_addressable_total, modular_range, vls_range,
            yard_dollar_range, yard_fy_range)


(ENTITY_MASTER, ent_dollar_range, role_range, bucket_range, country_range,
 naics_range, ent_first_data_row, ent_last_data_row, ent_row_cell,
 top_vendor_indices, top_supplier_indices, observed_addressable_total,
 modular_range, vls_range, yard_dollar_range, yard_fy_range) = _make_entities()
