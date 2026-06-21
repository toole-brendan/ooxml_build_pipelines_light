"""data_pop_corpus - the "POP Corpus" tab (one module = one sheet).

The 658-row place-of-performance corpus, as a native Excel table, behind a compact
at-a-glance rollup. This sheet is the source of the per-stream POP coefficients
(consumed by TAM Build) and the confirmation audit (POP Source Audit). It is a leaf:
it loads its CSV and depends on no other sheet module.

Promoted accessors (consumed elsewhere): the dollar-weighted SUMPRODUCT ranges
(gate / gfe_excl / confirmed / stream / scope_class / program / dollar / pct) plus
the gated-row register helpers. Names are unchanged from the former corpus_sheets so
TAM Build, Sensitivity, and POP Source Audit are unaffected. Column semantics
(Gate / GFE-Excl / Confirmed / Stream) are documented here, not in cell prose.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_PCT_INPUT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub POP Corpus"
_BASE = 14                              # title(2) + blank + §1 at-a-glance(4-11) + 2 blanks
_HEADERS = ["Date", "PIID", "Program", "Work Type", "Scope Class", "Stream",
            "Gate", "GFE/Excl", "Confirmed", "$M",
            "EB %", "HII %", "Other US %", "Foreign %"]
_HDR_STYLES = [S_HEADER_LEFT] * 6 + [S_HEADER_CENTER] * 8   # 6 text, then flags/$/% centered


def _build_pop_location_parse(tab: str, base: int):
    _GFE_PROGRAMS = {"sub_gfe_electronics", "sub_gfe_components"}
    _NUCLEAR_GFE_PROGRAMS = {"bpmi_nuclear"}
    _AP_LLTM_WORKTYPES = {"lltm_early_mfg", "advance_procurement"}
    _BC_WORKTYPES = {"construction", "component_procurement"}
    _GATE_TRUE = {"yes", "y", "true", "1"}
    _COL = {"piid": 2, "program": 3, "work_type": 4, "scope_class": 5, "stream": 6,
            "gate": 7, "gfe_excl": 8, "confirmed": 9, "dollar": 10,
            "eb": 11, "hii": 12, "other": 13, "foreign": 14}

    def _f(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return 0.0

    def _stream(wt): return "AP_LLTM" if wt in _AP_LLTM_WORKTYPES else "BC"

    def _scope_class(program, wt, gfe):
        if program in _NUCLEAR_GFE_PROGRAMS:
            return "EXCLUDE_GFE_NUCLEAR"
        if gfe:
            return "EXCLUDE_GFE"
        if wt in _AP_LLTM_WORKTYPES:
            return "INCLUDE_AP_LLTM"
        if wt in _BC_WORKTYPES:
            return "INCLUDE_BC"
        return "EXCLUDE_REVIEW"

    def _load_rows():
        out = []
        with (EXTRACTED / "dod_announcement_pop.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                program = (r.get("program_refined") or "").strip()
                wt = (r.get("work_type_primary") or "").strip()
                gate = 1 if (r.get("is_sub_new_construction_tam") or "").strip().lower() in _GATE_TRUE else 0
                gfe = 1 if (program in _GFE_PROGRAMS or program in _NUCLEAR_GFE_PROGRAMS) else 0
                out.append({
                    "date": (r.get("action_date") or "").strip(),
                    "piid": (r.get("piid") or "").strip() or "-",
                    "program": program, "work_type": wt,
                    "scope_class": _scope_class(program, wt, gfe), "stream": _stream(wt),
                    "gate": gate, "gfe_excl": gfe, "confirmed": 1,
                    "dollar_m": _f(r.get("amount_usd")) / 1e6,
                    "eb": _f(r.get("pop_eb_site_pct")) / 100.0,
                    "hii": _f(r.get("pop_hii_site_pct")) / 100.0,
                    "other": _f(r.get("pop_other_us_pct")) / 100.0,
                    "foreign": _f(r.get("pop_foreign_pct")) / 100.0,
                })
        out.sort(key=lambda r: r["dollar_m"], reverse=True)
        return out

    rows_data = _load_rows()
    c = RowCursor(base)
    c.banner("§2 - POP corpus (658-row place-of-performance gate)", n_cols=14,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    header_row = c.write(_HEADERS, styles=_HDR_STYLES)
    first_data = c.at()
    row_styles = [S_DEFAULT] * 6 + [S_NUM_INPUT] * 4 + [S_PCT_INPUT] * 4
    for r in rows_data:
        c.write([r["date"], r["piid"], r["program"], r["work_type"], r["scope_class"], r["stream"],
                 r["gate"], r["gfe_excl"], r["confirmed"], r["dollar_m"],
                 r["eb"], r["hii"], r["other"], r["foreign"]],
                styles=row_styles, outline_level=1)
    last_data = c.at() - 1

    table = ExcelTable(name="tbl_sub_pop_parse",
                       ref=f"B{header_row}:{col_letter(len(_HEADERS))}{last_data}",
                       headers=_HEADERS)

    def _rng(key):
        cc = col_letter(_COL[key])
        return f"'{tab}'!{cc}{first_data}:{cc}{last_data}"

    def row_cell(i, key): return f"'{tab}'!{col_letter(_COL[key])}{first_data + i}"

    _GATED_RANK = [i for i, r in enumerate(rows_data) if r["gate"] == 1]

    acc = dict(
        gate_range=lambda: _rng("gate"), gfe_excl_range=lambda: _rng("gfe_excl"),
        confirmed_range=lambda: _rng("confirmed"), stream_range=lambda: _rng("stream"),
        scope_class_range=lambda: _rng("scope_class"), program_range=lambda: _rng("program"),
        pop_dollar_range=lambda: _rng("dollar"), pct_range=lambda which: _rng(which),
        pop_first_data_row=lambda: first_data, pop_last_data_row=lambda: last_data,
        pop_row_cell=row_cell,
        gated_row_cell=lambda rank, key: row_cell(_GATED_RANK[rank], key),
        n_gated=lambda: len(_GATED_RANK), n_rows=lambda: len(rows_data))
    return c.rows, c.at(), [table], acc


# ── Layout pass: corpus first (promotes the ranges), at-a-glance wraps it ────
_rows, _after, _tables, _acc = _build_pop_location_parse(_TAB, _BASE)

gate_range = _acc["gate_range"]; gfe_excl_range = _acc["gfe_excl_range"]
confirmed_range = _acc["confirmed_range"]; stream_range = _acc["stream_range"]
scope_class_range = _acc["scope_class_range"]; program_range = _acc["program_range"]
pop_dollar_range = _acc["pop_dollar_range"]; pct_range = _acc["pct_range"]
pop_first_data_row = _acc["pop_first_data_row"]; pop_last_data_row = _acc["pop_last_data_row"]
pop_row_cell = _acc["pop_row_cell"]; gated_row_cell = _acc["gated_row_cell"]; n_gated = _acc["n_gated"]
_n_rows = _acc["n_rows"]


def _render_pop_location_parse() -> WorksheetSpec:
    g, x, c_rng, dol = gate_range(), gfe_excl_range(), confirmed_range(), pop_dollar_range()

    def _sp(*m): return f"SUMPRODUCT({'*'.join(m)})"

    c = RowCursor(2)
    c.banner("POP Corpus", n_cols=14, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Gated POP corpus", n_cols=14, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Rows in corpus", _n_rows()],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Gated TAM actions", f"={_sp(g)}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Gated TAM corpus $M", f"={_sp(g, dol)}"],
            styles=[S_BOLD, S_NUM])
    c.write(["In-scope non-GFE $M", f"={_sp(g, f'(1-{x})', dol)}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Confirmed in-scope $M", f"={_sp(g, f'(1-{x})', c_rng, dol)}"],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[22, 18, 18, 20, 18, 10, 7, 9, 11, 11, 9, 9, 11, 11],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=_tables)


POP_CORPUS = SheetEntry(_TAB, _GROUP, _render_pop_location_parse)
