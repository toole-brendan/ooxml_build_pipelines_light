"""validation_sib_excluded - the "SIB Excluded" tab (one module = one sheet).

The SIB (Submarine Industrial Base) exclusion trail: BlueForge Alliance, Training
Modernization Group, and IALR are capacity grants / workforce support, NOT
construction outsourcing, so their subaward $ is excluded from the SAM (Sec. 8
guardrail). Leaf module (loads its CSV/JSON). Produces sib_total_cell (consumed by
Figure Register DO-08 and QA Reconciliation); mib_total_cell stays as a
backward-compatible alias.

Terminology: visible text says SIB (Submarine Industrial Base). Earlier source
files use MIB / Maritime Industrial Base; the one glossary note explaining that
lives on Methodology & Scope. The module filename stays mib_excluded.py to avoid
import churn; the source-data JSON key (dollars_excluded_mib_$M) is the external
file's key and is read as-is.

Treatment rationale (kept here, not as cell prose): capacity grants fund shipyard
capacity, workforce/training programs, and industrial-base R&D - none is a
construction subaward Saronic could win; only outsourced new-construction supplier
work counts in TAM. The SIB total ties to nc_scope_summary.dollars_excluded_mib_$M
and feeds Figure Register DO-08 + QA Reconciliation (anchor $4,251.8M).
"""
from __future__ import annotations

import csv
import json

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "validation"
_TAB = "Sub SIB Excluded"
_BASE = 11                                       # title(2) + blank + §1 at-a-glance(4-8) + 2 blanks

_UEI_ORDER = [
    ("F8PEZKXES8B1", "BlueForge Alliance"),
    ("QLJZVM6XKR71", "Training Modernization Group, Inc."),
    ("TCM3R4JPRKY4", "Institute for Advanced Learning and Research"),
]


def _build_sib_excluded(tab: str, base: int):
    def _load():
        out = {}
        with (EXTRACTED / "sam_subaward_top_parents.csv").open(encoding="utf-8-sig", newline="") as fh:
            rdr = csv.reader(fh); next(rdr)
            for r in rdr:
                if r[0] in {e[0] for e in _UEI_ORDER}:
                    out[r[0]] = {"total_$M": float(r[2]), "action_count": int(r[3])}
        with (EXTRACTED / "nc_scope_summary.json").open(encoding="utf-8") as fh:
            sib_total = float(json.load(fh)["dollars_excluded_mib_$M"])
        bf, tmg = out["F8PEZKXES8B1"]["total_$M"], out["QLJZVM6XKR71"]["total_$M"]
        out["TCM3R4JPRKY4"] = {"total_$M": sib_total - bf - tmg, "action_count": 1}
        return out

    totals = _load()
    c = RowCursor(base)
    c.banner("§2 - SIB exclusion (capacity grants, not construction outsourcing)", n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["UEI", "Display name", "Total $M", "Action count", "% of SIB total"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    first = c.at()
    total_row_n = first + len(_UEI_ORDER)
    for uei, name in _UEI_ORDER:
        v = totals[uei]
        c.write([uei, name, v["total_$M"], v["action_count"], lambda r: f"=D{r}/D{total_row_n}"],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_DEFAULT, S_PCT], outline_level=1)
    assert c.at() == total_row_n
    last = total_row_n - 1
    c.total(["", "Total (SIB exclusion)", f"=SUM(D{first}:D{last})",
             f"=SUM(E{first}:E{last})", f"=SUM(F{first}:F{last})"],
            styles=[S_DEFAULT, S_BOLD, S_NUM, S_DEFAULT, S_PCT], n_cols=5)

    def entity_dollar_cell(i):
        return f"'{tab}'!D{first + i}"

    return c.rows, c.at(), dict(sib_total_cell=lambda: f"'{tab}'!D{total_row_n}",
                                entity_dollar_cell=entity_dollar_cell)


# ── Layout pass: detail first (promotes sib_total_cell), then at-a-glance ────
_rows, _after, _acc = _build_sib_excluded(_TAB, _BASE)
sib_total_cell = _acc["sib_total_cell"]
mib_total_cell = sib_total_cell           # backward-compatible alias (old name)
sib_entity_dollar_cell = _acc["entity_dollar_cell"]    # i-th SIB entity $ (Chart Data)
SIB_ENTITY_NAMES = [name for _uei, name in _UEI_ORDER]
_LARGEST = _UEI_ORDER[0][1]


def _render_sib_excluded() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("SIB Excluded", n_cols=5, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - SIB exclusion", n_cols=5, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _tot_row = c.write(["Total SIB exclusion $M", f"={sib_total_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["Number of SIB entities", len(_UEI_ORDER)],
            styles=[S_DEFAULT, S_DEFAULT])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[16, 40, 14, 14, 16],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


SIB_EXCLUDED = SheetEntry(_TAB, _GROUP, _render_sib_excluded)
