"""data_scn_budget - the "SCN Budget" tab (one module = one sheet).

The P-5c per-FY cost-category breakdown (Virginia + Columbia) with derived BC/GFE
ratios and a portfolio rollup that gives TAM Build a clean budget-base source. Leaf
module (loads its CSV, no cross-sheet dependency).

Promoted accessor: scn_cell(li, fy, metric) -> 'SCN Budget'!... (consumed by TAM
Build's Budget Normalized section). Built at import time so the row positions the
accessor returns derive from the same cursor calls that write the cells.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, banner_row, write_row, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import load_extracted_csv
from workbook_master_tam.sheets.submarines.data_deflators import deflator_factor_cell
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub SCN Budget"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_DETAIL_BASE = 15                       # title(2) + blank + §1 at-a-glance(4-12) + 2 blanks

# detail columns: B=label, C..H = FY22..FY27
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_FY)}
# rollup / at-a-glance columns: + Total in I
_C_FIRST, _C_LAST = col_letter(2), col_letter(1 + len(_FY))     # C..H
_TOTAL_COL = col_letter(2 + len(_FY))                           # I
_HDR_DETAIL = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY)
_HDR_ROLL = [S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_FY) + 1)


def _build_scn_annual(tab: str, base: int):
    n_cols = 1 + len(_FY) + 1                     # full sheet width incl. Total col (matches §4 rollup)
    pos = {2013: {}, 1045: {}}             # then-year (blue) P-5c rows, per class
    pos_const = {2013: {}, 1045: {}}       # constant-FY2026 rows (§Nd), what scn_cell returns

    def _load_p5c():
        headers, data = load_extracted_csv("cost_funnel_with_subawards")
        idx = {h: i for i, h in enumerate(headers)}
        metric_cols = {
            "total": "total_ship_estimate_$M", "plans": "plan_costs_$M",
            "propulsion": "propulsion_$M", "electronics": "electronics_$M",
            "hme": "hme_$M", "ordnance": "ordnance_$M", "other_cost": "other_cost_$M",
            "technology_insertion": "technology_insertion_$M",
            "gfe_sum": "gfe_sum_$M", "change_orders": "change_orders_$M",
            "basic": "basic_construction_$M",
        }
        out = {}
        for r in data:
            li, fy = r[idx["LI"]], r[idx["FY"]]
            if not isinstance(li, int) or not isinstance(fy, int):
                continue
            out[(li, fy)] = {k: r[idx[c]] for k, c in metric_cols.items()}
        return out

    p5c = _load_p5c()
    c = RowCursor(base)

    def _class_block(li: int, sec: int, ship: str):
        c.banner(f"§{sec} - {ship} SCN P-5c per FY ($M)", n_cols,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric"] + list(_FY), styles=_HDR_DETAIL)

        def drow(label, mkey):
            vals = [label] + [p5c.get((li, fy), {}).get(mkey) for fy in _FY]
            pos[li][mkey] = c.write(vals, styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY),
                                    outline_level=1)

        drow("Total Ship Estimate", "total")
        drow("Plans Costs", "plans")
        c.blank()
        c.banner(f"§{sec}a - GFE components", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        drow("Propulsion Equipment", "propulsion")
        drow("Electronics", "electronics")
        drow("Hull, Mechanical, Electrical (HM&E)", "hme")
        drow("Ordnance", "ordnance")
        drow("Other Cost", "other_cost")
        drow("Technology Insertion", "technology_insertion")
        drow("GFE Sum", "gfe_sum")
        c.blank()
        c.banner(f"§{sec}b - Construction", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        drow("Change Orders", "change_orders")
        drow("Basic Construction", "basic")
        c.blank()
        c.banner(f"§{sec}c - Derived ratios", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        rt, rb, rg = pos[li]["total"], pos[li]["basic"], pos[li]["gfe_sum"]

        def pct(label, num_row, mkey):
            vals = [label] + [f'=IF({_FY_COL[fy]}{rt}=0,"",{_FY_COL[fy]}{num_row}/{_FY_COL[fy]}{rt})'
                              for fy in _FY]
            pos[li][mkey] = c.write(vals, styles=[S_BOLD] + [S_PCT] * len(_FY),
                                    outline_level=1)

        pct("BC % of Total", rb, "bc_pct")
        pct("GFE % of Total", rg, "gfe_pct")
        c.blank()

        # §Nd Constant FY2026 $ (then-year x Green Book Procurement deflator). These rows,
        # not the then-year detail above, are what scn_cell returns - so the §1 at-a-glance
        # and §4 portfolio rollup (both built via scn_cell / _portfolio) inherit constant
        # FY2026 dollars automatically. All P-5c categories deflated at the one Procurement
        # factor (GFE included as an approximation; it is removed before TAM).
        c.banner(f"§{sec}d - Constant FY2026 $M (then-year x deflator)", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric"] + list(_FY), styles=_HDR_DETAIL)

        def crow(label, mkey):
            vals = [label] + [f"={_FY_COL[fy]}{pos[li][mkey]}*{deflator_factor_cell(fy)}"
                              for fy in _FY]
            pos_const[li][mkey] = c.write(vals, styles=[S_BOLD] + [S_LINK_NUM] * len(_FY),
                                          outline_level=1)

        for mlabel, mkey in [
            ("Total Ship Estimate", "total"), ("Plans Costs", "plans"),
            ("Propulsion Equipment", "propulsion"), ("Electronics", "electronics"),
            ("Hull, Mechanical, Electrical (HM&E)", "hme"), ("Ordnance", "ordnance"),
            ("Other Cost", "other_cost"), ("Technology Insertion", "technology_insertion"),
            ("GFE Sum", "gfe_sum"), ("Change Orders", "change_orders"),
            ("Basic Construction", "basic"),
        ]:
            crow(mlabel, mkey)

    _class_block(2013, 2, "Virginia (LI 2013)")
    c.blank(2)
    _class_block(1045, 3, "Columbia (LI 1045)")

    _RATIO_METRICS = {"bc_pct", "gfe_pct"}

    def scn_cell(li: int, fy: int, metric: str) -> str:
        if li not in pos:
            raise ValueError(f"Unknown LI {li!r}; expected 2013 or 1045")
        if fy not in _FY_COL:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")
        # dollar metrics -> constant-FY2026 rows (§Nd); ratios -> then-year rows (invariant)
        src = pos[li] if metric in _RATIO_METRICS else pos_const[li]
        if metric not in src:
            raise ValueError(f"Unknown metric {metric!r}")
        return f"'{tab}'!{_FY_COL[fy]}{src[metric]}"

    return c.rows, c.at(), scn_cell


# ── Layout pass: SCN detail first (promotes scn_cell), then rollups ─────────
_detail_rows, _after_detail, scn_cell = _build_scn_annual(_TAB, _DETAIL_BASE)


def _portfolio(fy, metric):
    return f"N({scn_cell(2013, fy, metric)})+N({scn_cell(1045, fy, metric)})"


def _render_scn_annual() -> WorksheetSpec:
    n_cols = 1 + len(_FY) + 1                     # label + 6 FY + Total
    c = RowCursor(2)
    c.banner("SCN Budget", n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 headline
    c.banner("§1 - Basic Construction & GFE by FY ($M)", n_cols,
             style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure"] + list(_FY) + ["Total"], styles=_HDR_ROLL)
    glance = [
        ("Virginia Basic Construction", lambda fy: scn_cell(2013, fy, "basic"), True, False),
        ("Columbia Basic Construction", lambda fy: scn_cell(1045, fy, "basic"), True, False),
        ("Portfolio Basic Construction", lambda fy: _portfolio(fy, "basic"), True, True),
        ("Virginia GFE sum", lambda fy: scn_cell(2013, fy, "gfe_sum"), False, False),
        ("Columbia GFE sum", lambda fy: scn_cell(1045, fy, "gfe_sum"), False, False),
        ("Portfolio GFE sum", lambda fy: _portfolio(fy, "gfe_sum"), False, True),
    ]
    for label, maker, bold, derived in glance:
        num = S_NUM                                # same-sheet refs -> black (not green links)
        vals = ([label] + [f"={maker(fy)}" for fy in _FY]
                + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"])
        c.write(vals, styles=[S_BOLD if bold else S_DEFAULT] + [num] * len(_FY) + [S_NUM])
    c.blank(2)

    # §2 Virginia / §3 Columbia detail (built at import, spliced here)
    assert c.at() == _DETAIL_BASE, f"at-a-glance ends at {c.at()}, expected {_DETAIL_BASE}"
    c.feed(_detail_rows, _after_detail)
    c.blank(2)

    # §4 Portfolio rollup
    c.banner("§4 - Portfolio rollup (Virginia + Columbia, $M by FY)", n_cols,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY) + ["Total"], styles=_HDR_ROLL)
    rollpos = {}
    for label, mkey in [("Total Ship Estimate", "total"), ("GFE Sum", "gfe_sum"),
                        ("Basic Construction", "basic")]:
        vals = ([label] + [f"={_portfolio(fy, mkey)}" for fy in _FY]
                + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"])
        rollpos[mkey] = c.write(vals, styles=[S_BOLD] + [S_NUM] * len(_FY) + [S_NUM],
                                outline_level=1)
    rt = rollpos["total"]
    for label, num_row in [("BC % of Total", rollpos["basic"]), ("GFE % of Total", rollpos["gfe_sum"])]:
        vals = [label] + [f'=IF({_FY_COL[fy]}{rt}=0,"",{_FY_COL[fy]}{num_row}/{_FY_COL[fy]}{rt})'
                          for fy in _FY]
        vals.append(f'=IF({_TOTAL_COL}{rt}=0,"",{_TOTAL_COL}{num_row}/{_TOTAL_COL}{rt})')
        c.write(vals, styles=[S_BOLD] + [S_PCT] * len(_FY) + [S_PCT], outline_level=1)
    c.blank(2)

    # §5 Sources
    c.banner("§5 - Sources", n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Source family", "Source Index ID", "Refresh"], styles=S_HEADER_LEFT)
    c.write(["SCN P-5c (Basic Construction)", "Source Index §2", "FY22-27 PB"],
            styles=S_DEFAULT, outline_level=1)

    ws = worksheet(c.rows, cols=[34, 9, 9, 9, 9, 9, 9, 12],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


SCN_BUDGET = SheetEntry(_TAB, _GROUP, _render_scn_annual)
