"""data_pop_corpus - the "POP Corpus" tab (DDG, data group; one module = one sheet).

The place-of-performance evidence table that drives the supplier coefficients. The
former Corpus tab, now its own data tab. The two reconstructed MYP master rows lead
the table (linked from Inputs), followed by the gated disclosed-announcement actions;
a field guide explains the flag fields. Native table: tbl_ddg_pop_parse.

Promoted accessors (POP ranges + row-cell helpers; consumed by tam_build, sam_build,
pop_audit):
  gate_range, gfe_excl_range, confirmed_range, stream_range, scope_class_range,
  program_range, pop_dollar_range, myp_master_range, pct_range, pop_first_data_row,
  pop_last_data_row, pop_row_cell, gated_row_cell, n_gated, n_myp_masters
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT, S_PCT_INPUT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg.inputs_assumptions import myp_master_cell, myp_pop_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG POP Corpus"


def _make_pop_corpus():
    _HEADERS = ["Date", "PIID", "Prime", "Program", "Work Type", "Scope Class", "Stream",
                "Gate", "GFE/Excl", "Confirmed", "MYP master", "$M",
                "BIW %", "Ingalls %", "Other US %", "Foreign %"]
    _N_COLS = len(_HEADERS)
    _GATE_TRUE = {"yes", "y", "true", "1"}
    _COL = {
        "piid": 2, "prime": 3, "program": 4, "work_type": 5,
        "scope_class": 6, "stream": 7, "gate": 8, "gfe_excl": 9,
        "confirmed": 10, "myp_master": 11, "dollar": 12,
        "biw": 13, "ingalls": 14, "other": 15, "foreign": 16,
    }

    def _f(x) -> float:
        try:
            return float(x)
        except (TypeError, ValueError):
            return 0.0

    def _scope_class(gfe: int) -> str:
        return "EXCLUDE_GFE" if gfe else "INCLUDE_BC"

    def _load_disclosed() -> list[dict]:
        out = []
        with (EXTRACTED / "dod_announcement_pop.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                gate = 1 if (r.get("is_ddg_new_construction_tam") or "").strip().lower() in _GATE_TRUE else 0
                if not gate:
                    continue
                program = (r.get("program_refined") or "").strip()
                gfe = 1 if program.startswith("ddg_gfe_") else 0
                out.append({
                    "date":     (r.get("action_date") or "").strip(),
                    "piid":     (r.get("piid") or "").strip() or "-",
                    "prime":    (r.get("prime") or "").strip() or "-",
                    "program":  program,
                    "work_type": (r.get("work_type_primary") or "").strip(),
                    "scope_class": _scope_class(gfe),
                    "stream":   "BC",
                    "gate":     1,
                    "gfe_excl": gfe,
                    "confirmed": 1,
                    "myp_master": 0,
                    "dollar":   _f(r.get("amount_usd")) / 1e6,
                    "biw":      _f(r.get("pop_biw_site_pct")) / 100.0,
                    "ingalls":  _f(r.get("pop_ingalls_site_pct")) / 100.0,
                    "other":    _f(r.get("pop_other_us_pct")) / 100.0,
                    "foreign":  _f(r.get("pop_foreign_pct")) / 100.0,
                })
        out.sort(key=lambda r: r["dollar"], reverse=True)
        return out

    def _master_row(piid: str, prime: str, yard: str) -> dict:
        return {
            "date": "(MYP master)", "piid": piid, "prime": prime,
            "program": "ddg51", "work_type": "construction",
            "scope_class": "INCLUDE_BC", "stream": "BC",
            "gate": 1, "gfe_excl": 0, "confirmed": 1, "myp_master": 1,
            "dollar":  f"={myp_master_cell(yard)}",
            "biw":     f"={myp_pop_cell(yard, 'biw')}",
            "ingalls": f"={myp_pop_cell(yard, 'ingalls')}",
            "other":   f"={myp_pop_cell(yard, 'other_us')}",
            "foreign": f"={myp_pop_cell(yard, 'foreign')}",
        }

    _MASTERS = [
        _master_row("N00024-23-C-2305", "Bath Iron Works", "biw"),
        _master_row("N00024-23-C-2307", "Huntington Ingalls Industries", "ingalls"),
    ]
    _DISCLOSED = _load_disclosed()
    _DATA = _MASTERS + _DISCLOSED

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_N_COLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 POP corpus (native table)
    c.banner("§1 - POP corpus (gated award place-of-performance)", n_cols=_N_COLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header_row = c.write(_HEADERS, styles=[S_HEADER_LEFT] * 7 + [S_HEADER_CENTER] * 9)
    _first_data = c.at()
    for r in _DATA:
        is_link = r["myp_master"] == 1
        num_style = S_LINK_NUM if is_link else S_NUM_INPUT
        pct_style = S_LINK_PCT if is_link else S_PCT_INPUT
        c.write(
            [r["date"], r["piid"], r["prime"], r["program"], r["work_type"],
             r["scope_class"], r["stream"], r["gate"], r["gfe_excl"],
             r["confirmed"], r["myp_master"], r["dollar"],
             r["biw"], r["ingalls"], r["other"], r["foreign"]],
            styles=[S_DEFAULT] * 7 + [S_NUM_INPUT] * 4
                   + [num_style, pct_style, pct_style, pct_style, pct_style],
            outline_level=1)
    _last_data = c.at() - 1
    _table = ExcelTable(name="tbl_ddg_pop_parse",
                        ref=f"B{_header_row}:{col_letter(_N_COLS)}{_last_data}",
                        headers=_HEADERS)
    c.blank(2)

    # §2 Field guide
    c.banner("§2 - Field guide", n_cols=_N_COLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    guide, nxt = build_table(
        c.at(), headers=["Field", "Meaning"],
        data_rows=[
            ["Gate", "1 = DDG new-construction TAM-relevant action"],
            ["GFE/Excl", "1 = GFE / Navy-directed scope (ddg_gfe_*) dropped from the coefficient"],
            ["Confirmed", "1 = manual_review_status confirmed (default 1)"],
            ["MYP master", "1 = a $-redacted MYP master row ($ reconstructed; POP as announced; linked from Inputs)"],
            ["Scope Class", "INCLUDE_BC / EXCLUDE_GFE"],
            ["Stream", "BC (all DDG gated work is Basic Construction stream)"],
        ],
        header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(guide, nxt)

    def render() -> WorksheetSpec:
        ws = worksheet(
            c.rows,
            cols=[12, 18, 20, 18, 18, 14, 8, 7, 9, 11, 11, 11, 9, 10, 10, 10],
            tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=[_table])

    def _rng(key: str) -> str:
        col = col_letter(_COL[key])
        return f"'{_TAB}'!{col}{_first_data}:{col}{_last_data}"

    def gate_range() -> str:        return _rng("gate")
    def gfe_excl_range() -> str:    return _rng("gfe_excl")
    def confirmed_range() -> str:   return _rng("confirmed")
    def stream_range() -> str:      return _rng("stream")
    def scope_class_range() -> str: return _rng("scope_class")
    def program_range() -> str:     return _rng("program")
    def dollar_range() -> str:      return _rng("dollar")
    def myp_master_range() -> str:  return _rng("myp_master")

    def pct_range(which: str) -> str:
        return _rng(which)

    def first_data_row() -> int:    return _first_data
    def last_data_row() -> int:     return _last_data

    def row_cell(i: int, key: str) -> str:
        return f"'{_TAB}'!{col_letter(_COL[key])}{_first_data + i}"

    _GATED_RANK = [i for i, r in enumerate(_DATA) if r["gate"] == 1]

    def gated_row_cell(rank: int, key: str) -> str:
        return row_cell(_GATED_RANK[rank], key)

    def n_gated() -> int:
        return len(_GATED_RANK)

    def n_myp_masters() -> int:
        return len(_MASTERS)

    return (SheetEntry(_TAB, _GROUP, render),
            gate_range, gfe_excl_range, confirmed_range, stream_range,
            scope_class_range, program_range, dollar_range, myp_master_range,
            pct_range, first_data_row, last_data_row, row_cell,
            gated_row_cell, n_gated, n_myp_masters)


(POP_CORPUS, gate_range, gfe_excl_range, confirmed_range, stream_range,
 scope_class_range, program_range, pop_dollar_range, myp_master_range, pct_range,
 pop_first_data_row, pop_last_data_row, pop_row_cell, gated_row_cell, n_gated,
 n_myp_masters) = _make_pop_corpus()
