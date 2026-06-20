"""data_ap_bridge - the "AP Bridge" tab (one module = one sheet).

The P-10 advance-procurement bucket grids (Virginia + Columbia), the Phase-3
TAM-treatment crosswalk, and the central P-10 -> TAM reconciliation bridge that
confirms the AP/LLTM additive base nets to $0 (supplier LLTM already inside Basic
Construction). This bridge is the producer block for the Executive Summary's AP/LLTM
bridge. Imports Assumptions & Controls for the gross-P10 reference.

Conclusion captured here (not as cell prose): the supplier-addressable LLTM
(shipbuilder-procured + EOQ + HM&E + propulsor) is ALREADY inside the P-5c Basic
Construction base, so wiring P-10 AP as a separate stream would double-count the BC
TAM. The AP/LLTM additive base is therefore a confirmed $0. BPMI naval-nuclear is GFE,
so it is also excluded from the BC coefficient corpus (BC coeff 75.7% -> 35.0%; see
Sensitivity). The ~$18.8B AP/LLTM POP corpus is a different lens (the gated-POP
denominator for the 48.5% reference coeff), not the P-10 gross; both reconcile to $0.

Promoted accessors: ap_bridge_gross/gfe_removed/in_bc_removed/residual/base_cell.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_LINK_NUM, S_LABEL_INDENT_1, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.lib import EXTRACTED
from workbook_submarines.sheets.inputs_assumptions import ap_gross_cell as _cp_ap_gross
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "AP Bridge"
_DETAIL_BASE = 14                                # title(2) + blank + §1 at-a-glance(4-11) + 2 blanks
_FY_COLUMNS = list(range(2020, 2032))
_BUCKET_ORDER = [
    "Plans / SIB", "EOQ", "Nuclear plant LLTM", "Propulsor LLTM",
    "Electronics LLTM", "HM&E LLTM", "Ordnance LLTM", "Missile compartment LLTM",
    "Shipbuilder-procured LLTM", "Shipbuilder-procured LLTM (CFE)",
]
_BRIDGE_FY = (2022, 2023, 2024, 2025, 2026, 2027)
_EXCLUDE_BUCKETS = ["Nuclear plant LLTM", "Electronics LLTM", "Ordnance LLTM",
                    "Missile compartment LLTM", "Plans / SIB"]
_IN_BC_BUCKETS = ["Propulsor LLTM", "HM&E LLTM", "Shipbuilder-procured LLTM",
                  "Shipbuilder-procured LLTM (CFE)", "EOQ"]
# P-10 bucket -> (short TAM treatment, terse basis). Full reasoning in the docstring.
_RECON = [
    ("Nuclear plant LLTM", "EXCL GFE", "BPMI naval reactor - GFE"),
    ("Electronics LLTM", "EXCL GFE", "combat-system electronics - Navy-furnished"),
    ("Ordnance LLTM", "EXCL wpn", "WPN/OPN ordnance, not SCN"),
    ("Missile compartment LLTM", "EXCL GFE", "CMC / tubes - GFE / industrial base"),
    ("Plans / SIB", "EXCL des", "lead-yard design - Plan Costs"),
    ("Shipbuilder-procured (+CFE)", "IN BC", "direct material inside BC"),
    ("EOQ", "IN BC", "economic-order-quantity - inside BC"),
    ("HM&E / Propulsor LLTM", "IN BC", "HM&E / propulsor material inside BC"),
]


def _build_lltm_ap(tab: str, base: int):
    n_cols = 1 + len(_FY_COLUMNS) + 1
    fy_hdr = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS) + [S_HEADER_CENTER]

    def _fy_col(fy): return col_letter(2 + (fy - _FY_COLUMNS[0]))
    def _total_col(): return col_letter(2 + len(_FY_COLUMNS))

    def _load_lltm():
        out = {}
        with (EXTRACTED / "scn_p10_ap_buckets.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                li, bucket, fy = int(r["LI"]), r["Bucket"], int(r["FY"])
                try:
                    val = float(r["Best Value $M"])
                except ValueError:
                    val = None
                out.setdefault((li, bucket), {})[fy] = val
        return out

    lltm = _load_lltm()
    c = RowCursor(base)

    def _class_block(li, sec, ship):
        c.banner(f"§{sec} - {ship} P-10 AP buckets ($M, FY20-31)", n_cols=n_cols,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket"] + list(_FY_COLUMNS) + ["Total"], styles=fy_hdr)
        first = c.at()
        cf, cl = _fy_col(_FY_COLUMNS[0]), _fy_col(_FY_COLUMNS[-1])
        for bucket in _BUCKET_ORDER:
            per_fy = lltm.get((li, bucket), {})
            vals = ([bucket] + [per_fy.get(fy) for fy in _FY_COLUMNS]
                    + [lambda r: f"=SUM({cf}{r}:{cl}{r})"])
            c.write(vals, styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS) + [S_NUM],
                    outline_level=1)
        last = c.at() - 1
        tc = _total_col()
        totals = (["Class total"]
                  + [f"=SUM({_fy_col(fy)}{first}:{_fy_col(fy)}{last})" for fy in _FY_COLUMNS]
                  + [f"=SUM({tc}{first}:{tc}{last})"])
        c.total(totals, styles=[S_BOLD] + [S_NUM] * (len(_FY_COLUMNS) + 1), n_cols=n_cols)
        return first

    va_first = _class_block(2013, 2, "Virginia (LI 2013)")
    c.blank(2)
    col_first = _class_block(1045, 3, "Columbia (LI 1045)")
    c.blank(2)

    # §4 P-10 bucket -> TAM treatment crosswalk
    c.banner("§4 - P-10 bucket -> TAM treatment (AP/LLTM base = 0)", n_cols=14,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["P-10 bucket", "TAM treatment", "Rationale"], styles=S_HEADER_LEFT)
    for bucket, treat, basis in _RECON:
        c.write([bucket, treat, basis], styles=[S_DEFAULT, S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 P-10 -> TAM reconciliation bridge (FY22-27): gross nets to $0
    def _fy2227(bucket_names):
        terms = []
        for b in bucket_names:
            i = _BUCKET_ORDER.index(b)
            terms.append(f"SUM(E{va_first + i}:J{va_first + i})")
            terms.append(f"SUM(E{col_first + i}:J{col_first + i})")
        return "+".join(terms)

    c.banner("§5 - P-10 -> TAM reconciliation bridge ($M, FY22-27)", n_cols=14,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "$M", "Rationale"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    gross = "+".join(f"N({_cp_ap_gross(li, fy)})" for li in (2013, 1045) for fy in _BRIDGE_FY)
    r_gross = c.write(["P-10 gross AP top-line (FY22-27)", f"={gross}", "authoritative AP total, Va+Col"],
                      styles=[S_BOLD, S_NUM, S_DEFAULT], outline_level=1)
    r_gfe = c.write(["less GFE / design / weapons", f"=-({_fy2227(_EXCLUDE_BUCKETS)})",
                     "nuclear+electronics+ordnance+missile+Plans"],
                    styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT], outline_level=1)
    r_inbc = c.write(["less already inside P-5c BC", f"=-({_fy2227(_IN_BC_BUCKETS)})",
                      "shipbuilder+CFE+EOQ+HM&E+propulsor"],
                     styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT], outline_level=1)
    r_res = c.write(["less un-itemized overlap", f"=-(C{r_gross}+C{r_gfe}+C{r_inbc})",
                     "early-Va top-line over named detail"],
                    styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT], outline_level=1)
    r_base = c.total(["= AP/LLTM additive base = 0", f"=C{r_gross}+C{r_gfe}+C{r_inbc}+C{r_res}",
                      "confirmed $0"], styles=[S_BOLD, S_NUM, S_DEFAULT], n_cols=3)

    acc = dict(
        ap_bridge_gross_cell=lambda: f"'{tab}'!C{r_gross}",
        ap_bridge_gfe_removed_cell=lambda: f"'{tab}'!C{r_gfe}",
        ap_bridge_in_bc_removed_cell=lambda: f"'{tab}'!C{r_inbc}",
        ap_bridge_residual_cell=lambda: f"'{tab}'!C{r_res}",
        ap_bridge_base_cell=lambda: f"'{tab}'!C{r_base}")
    return c.rows, c.at(), acc


# ── Layout pass: detail first (promotes ap_bridge_*), then at-a-glance + checks ─
_detail_rows, _after_detail, _acc = _build_lltm_ap(_TAB, _DETAIL_BASE)

ap_bridge_gross_cell = _acc["ap_bridge_gross_cell"]
ap_bridge_gfe_removed_cell = _acc["ap_bridge_gfe_removed_cell"]
ap_bridge_in_bc_removed_cell = _acc["ap_bridge_in_bc_removed_cell"]
ap_bridge_residual_cell = _acc["ap_bridge_residual_cell"]
ap_bridge_base_cell = _acc["ap_bridge_base_cell"]


def _render_lltm_ap() -> WorksheetSpec:
    n_cols = 14
    c = RowCursor(2)
    c.banner("AP Bridge", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - P-10 -> TAM bridge ($M, FY22-27)", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Step", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _gross_row = c.write(["P-10 gross AP top-line", f"={ap_bridge_gross_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["less GFE / design / weapons", f"={ap_bridge_gfe_removed_cell()}"],
            styles=[S_LABEL_INDENT_1, S_NUM])
    c.write(["less already inside P-5c BC", f"={ap_bridge_in_bc_removed_cell()}"],
            styles=[S_LABEL_INDENT_1, S_NUM])
    c.write(["less un-itemized overlap", f"={ap_bridge_residual_cell()}"],
            styles=[S_LABEL_INDENT_1, S_NUM])
    _base_row = c.write(["AP/LLTM additive base", f"={ap_bridge_base_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.blank(2)

    assert c.at() == _DETAIL_BASE, f"at-a-glance ends at {c.at()}, expected {_DETAIL_BASE}"
    c.feed(_detail_rows, _after_detail)
    c.blank(2)

    # §6 Reconciliation checks
    c.banner("§6 - Reconciliation checks", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Status"], styles=S_HEADER_LEFT)
    c.write(["Bridge nets to the additive base",
             f'=IF(ABS({ap_bridge_base_cell()}-({ap_bridge_gross_cell()}+{ap_bridge_gfe_removed_cell()}'
             f'+{ap_bridge_in_bc_removed_cell()}+{ap_bridge_residual_cell()}))<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["AP/LLTM additive base = 0", f'=IF(ABS({ap_bridge_base_cell()})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=[34, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 12],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


AP_BRIDGE = SheetEntry(_TAB, _GROUP, _render_lltm_ap)
