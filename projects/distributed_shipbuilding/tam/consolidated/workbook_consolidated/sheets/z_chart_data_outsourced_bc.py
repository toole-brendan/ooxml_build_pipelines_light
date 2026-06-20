"""z_chart_data_outsourced_bc - consolidated "z_ChartData_OutsourcedBC" tab.

Second chart-data tab for the consolidated deck: the paste blocks behind the
Outsourced Basic Construction front-row slides, split out of z_ChartData so the
first tab keeps the core deck exhibits. ONE paste rectangle per think-cell
chart/element, in slide order, and nothing else - the tab exists to be
copy-pasted from. Values are hardcoded from the two program workbooks' final
chart-data / model outputs (the z_ChartData convention).

Dollar basis: constant FY2026 $ (Green Book Procurement deflator, FY2026 =
1.000) with the OBBBA Sec. 20002 mandatory funding included. Supplier
coefficients are the 2026-06-10 announced-POP restates: DDG 25.29% FY23-27 /
22.00% FY2022 vintage; submarines per class - Virginia 34% (Block V announced
POP), Columbia 22% (Build I announced POP), with the OBBBA boat riding
Virginia. The DDG AP/LLTM stream is the P-10 Ship Construction EOQ line at
coefficient 1.00 (vendor material by exhibit classification), so no prime
AP/LLTM removal remains in the walk. Submarine series split Virginia / Columbia
where the slide draws them per class.

Block -> consolidated deck chart/element (slide order; one block per chart):
  §1  DDG outsourced BC walk          waterfall, cumulative $B (slide 2)
  §2  Submarine outsourced BC walk    waterfall, cumulative $B (slide 2)
  §3  Outsourced BC by work type (per program/class)  stacked column, cumulative $B (slide 3; columns DDG-51, Columbia, Virginia)
  §4  Outsourced BC annual TAM with outlook  clustered stacked columns FY22-31, $B/yr (slide 4; one datasheet column per bar - DDG/Va/Col per FY, no spacer columns; FOUR rows per class grouped Columbia / Virginia / DDG-51: outsourced (FY22-27), outsourced low (FY28-31), outsourced high (FY28-31 increment, own color), retained spend (one row, both eras) - every bar tops out at total spend / FYDP gross)
  §4b Annual TAM, ramped upper bound         same chart, manual think-cell variant: FY28-31 penetration ramps ~6.8% p.a. from the FY22-25 avg (anchored FY27) to x1.30 at FY31; ONE high segment per forecast bar (no low split) + retained-to-gross
  §5  FY22-25 average annual TAM      dashed reference-line level, $B/yr (slide 4)
  §6  DDG penetration strip           % of total ship spend by FY (slide 4)
  §7  Submarine penetration strip     % of total ship spend by FY, per class: Virginia, Columbia (slide 4)
  §8  Work-type mix by FY             ONE 100%-stacked chart: 9 bars vessel-grouped (DDG-51 FY22-25 | Virginia FY22-25 | Columbia FY2024 only - unfunded years omitted), blank spacer column between groups; rows = the eight buckets in absolute $B (think-cell 100% mode normalizes; the unhighlighted side table carries the bar $B totals for column labels) (slide 5)

Outlook basis (§4-§7, from the program workbooks' Outlook tabs): penetration =
Outsourced BC TAM (all streams) / (P-5c Total Ship Estimate + OBBBA gross),
constant FY2026 $, measured per class for the submarines. Implied FY2028-FY2031
= each class's PB2027 FYDP gross x its penetration assumption: low = the class
FY22-25 average (complete historical years), high = low x (1 + the stated
outsourcing-intent uplift, 30%). The §4 retained-spend rows are each program's
denominator minus its outsourced TAM - the no-fill outlined extension above the
filled bars on slide 4. The FYDP outyears are the PB2027 request, not
appropriation. Work-type shares (§3, §8) are the gated yard/GDEB FY22-25
vectors applied per FY and per class (SAM Build).

think-cell waterfall convention: every data cell is a STEP, so a computed
subtotal or endpoint is the literal text marker "e". Numeric values are
literals; there are no formulas or cross-sheet links.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, banner_row, write_row
from workbook_core.styles import (
    S_DEFAULT, S_BOLD,
    S_TITLE_SHEET, S_TITLE_SECTION,
    S_PASTE_HEADER_TL, S_PASTE_HEADER_T, S_PASTE_HEADER_TR,
    S_PASTE_LABEL_L, S_PASTE_LABEL_BL,
    S_PASTE_VAL_INT_M, S_PASTE_VAL_R_M, S_PASTE_VAL_B_M, S_PASTE_VAL_BR_M,
    S_PASTE_VAL_INT_B, S_PASTE_VAL_R_B, S_PASTE_VAL_B_B, S_PASTE_VAL_BR_B,
    S_PASTE_VAL_INT_P, S_PASTE_VAL_R_P, S_PASTE_VAL_B_P, S_PASTE_VAL_BR_P,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

# Shared with the first chart-data tab (single source, no drift): the FY header
# and the work-type bucket order. The annual-TAM actuals are NO LONGER imported
# from z_chart_data - the first tab's §7 cadence block predates the 2026-06-10
# coefficient restates and the per-class split; the restated per-class series
# live here until the back-catalog sweep restates tab 1.
from .z_chart_data import _FY_HDR, _WORKTYPE_HDR

TAB_NAME = "z_ChartData_OutsourcedBC"
SHEET_GROUP = "chartdata"
TAB_COLOR = group_color(SHEET_GROUP)

_GROUP = SHEET_GROUP
_TAB = TAB_NAME
_NCOLS = 31                      # widest paste block: corner + 30 cluster slots (§4)


class RowCursor:
    """Small local cursor so this module has no dependency on a program package."""
    def __init__(self, start: int = 2):
        self.r = start
        self.rows: list[str] = []

    def banner(self, text: str, n_cols: int, *, style: int,
               mark_collapsible: bool = False) -> int:
        r0 = self.r
        self.rows.append(banner_row(r0, text, n_cols=n_cols, style=style,
                                    with_gutter=True,
                                    mark_collapsible=mark_collapsible))
        self.r += 1
        return r0

    def write(self, values: list, *, styles, outline_level: int = 0) -> int:
        r0 = self.r
        self.rows.append(write_row(r0, values, styles=styles, start_col=1,
                                   outline_level=outline_level))
        self.r += 1
        return r0

    def blank(self, n: int = 1) -> None:
        self.r += n


# --- think-cell paste-range emitter ---------------------------------------
# Per unit, the value-cell styles for {interior, right edge, bottom edge,
# bottom-right corner}. The left column is always a label (S_PASTE_LABEL_*),
# the top row always a header (S_PASTE_HEADER_*), so values never sit on the
# top or left edge.
_VAL_STYLE = {
    "M": {"INT": S_PASTE_VAL_INT_M, "R": S_PASTE_VAL_R_M, "B": S_PASTE_VAL_B_M, "BR": S_PASTE_VAL_BR_M},
    "B": {"INT": S_PASTE_VAL_INT_B, "R": S_PASTE_VAL_R_B, "B": S_PASTE_VAL_B_B, "BR": S_PASTE_VAL_BR_B},
    "P": {"INT": S_PASTE_VAL_INT_P, "R": S_PASTE_VAL_R_P, "B": S_PASTE_VAL_B_P, "BR": S_PASTE_VAL_BR_P},
}


def _paste_block(c: RowCursor, title: str, header: list, rows: list, unit: str,
                 annex: list | None = None, annex_gap: int = 2) -> None:
    """Emit one bordered think-cell paste rectangle.

    header: full top row; header[0] is the blank corner, header[1:] are categories
    or waterfall steps. rows: list of (row_label, [values]), where values align to
    header[1:]. A value may be a float/int, None (blank), or the waterfall marker
    "e".

    annex: optional UNHIGHLIGHTED side table written annex_gap blank columns
    right of the rectangle - a list aligned to [header line, *data lines];
    each entry is None or a list of plain cells (first non-None entry renders
    bold as the side table's header line, the rest default-styled).
    """
    c.banner(title, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    ncol = len(header) - 1
    if ncol < 1:
        raise ValueError(f"{title}: paste block needs at least one data column")
    for label, vals in rows:
        if len(vals) != ncol:
            raise ValueError(
                f"{title}: row {label!r} has {len(vals)} values but header has {ncol}"
            )
    annex = annex or []

    def _with_annex(values: list, styles: list, li: int) -> tuple[list, list]:
        side = annex[li] if li < len(annex) else None
        if side is None:
            return values, styles
        first = next(i for i, a in enumerate(annex) if a is not None)
        s = S_BOLD if li == first else S_DEFAULT
        return (values + [None] * annex_gap + side,
                styles + [S_DEFAULT] * annex_gap + [s] * len(side))

    vs = _VAL_STYLE[unit]
    hv, hs = _with_annex(
        header,
        [S_PASTE_HEADER_TL] + [S_PASTE_HEADER_T] * (ncol - 1) + [S_PASTE_HEADER_TR],
        0)
    c.write(hv, styles=hs, outline_level=1)
    n = len(rows)
    for i, (label, vals) in enumerate(rows):
        last = (i == n - 1)
        styles = [S_PASTE_LABEL_BL if last else S_PASTE_LABEL_L]
        for j in range(1, ncol + 1):
            if last:
                styles.append(vs["BR"] if j == ncol else vs["B"])
            else:
                styles.append(vs["R"] if j == ncol else vs["INT"])
        rv, rs = _with_annex([label, *vals], styles, i + 1)
        c.write(rv, styles=rs, outline_level=1)
    c.blank(2)


# --- Hardcoded consolidated values ----------------------------------------
# Outsourced BC walk (deck slide 2), FY2022-FY2027 cumulative constant FY2026 $B.
# Total Ship Spend = P-5c TSE + OBBBA Sec. 20002 gross; the GFE step carries
# the OBBBA non-BC remainder; the endpoint is the program supplier TAM (DDG
# 6.4217, sub 18.1338). Steps follow the think-cell convention (removals
# negative, computed subtotal / endpoint = "e"). The DDG walk is TWO series
# rows so the P-10 Ship Construction EOQ AP/LLTM base (1.04233 constant) rides
# the Total Ship Spend column as its own stacked segment (the slide's hatched
# slice, recolorable in think-cell) with the in-year base adjusted down -
# 36.5920922 + 1.04233 = 37.6344222; the "e" subtotals cumulate both rows, so
# Basic Construction (22.5907) and the endpoint (6.4217) are unchanged. The
# Prime AP/LLTM step is blank for BOTH programs: the DDG AP/LLTM base is the
# P-10 EOQ line at coefficient 1.00 (vendor material by classification - none
# retained by the primes); the submarines carry no AP/LLTM stream (single-row
# walk). Component provenance lives in the program workbooks (SCN Budget /
# OBBBA Mandatory / Assumptions §3 / TAM Build).
_WALK_HDR = ["Total Ship Spend", "Less GFE", "Less other non-BC",
             "Basic Construction", "Less prime BC", "Less prime AP/LLTM",
             "Outsourced BC"]
_DDG_WALK_INYEAR_B = [36.5920922, -12.76808724, -2.27568007, "e",
                      -16.16892521, None, "e"]
_DDG_WALK_APLLTM_B = [1.04233, None, None, None, None, None, None]
_SUB_WALK_B = [90.22347197, -19.1685053510754, -10.48950382, "e",
               -42.431616267, None, "e"]

# Outsourced BC by work type (§3, deck slide 3): one stacked column per program
# / submarine class, cumulative FY2022-FY2027 constant FY2026 $B. Values are
# the program workbooks' SAM Build allocations (annual TAM x per-FY modeled
# share, per class for the submarines); Residual is each column's unbucketed /
# ambiguous remainder, so each column sums to its supplier TAM (DDG = the §1
# walk endpoint; Virginia + Columbia = the §2 endpoint). Bucket order follows
# _WORKTYPE_HDR.
_DDG_WT_B = [0.687840132, 0.603915665, 0.37146878, 2.260781875,
             0.009666927, 0.146559104, 0.984150038, 1.357347159]
_VA_WT_B = [3.579611972, 2.79263306, 2.925105325, 0.6001458,
            0.894591879, 0.607109542, 0.104599769, 2.122962685]
_COL_WT_B = [2.015264257, 0.918962976, 0.691126691, 0.10813464,
             0.06840629, 0.178717817, 0.086917623, 0.439556207]

# Outsourced BC annual TAM with outlook (§4-§7), constant FY2026 $B. Actuals
# and denominators from each program's Outlook §2 (per class for submarines;
# Columbia's FY22/23/25 are genuinely zero - P-5c full funding lands biennially);
# implied FY28-31 from Outlook §4 (class FYDP gross x class assumption). The
# remainder rows = denominator - outsourced TAM (slide 4's no-fill outline
# extension; none drawn on the FY28-31 estimate bars).
_OY = [2028, 2029, 2030, 2031]
_FY_HDR_EXT = _FY_HDR + [f"FY{fy}" for fy in _OY]
_VA_ANNUAL_TAM_B = [1.779597842, 1.853723982, 3.207421443, 1.847245459, 1.976853214, 2.961918092]
_COL_ANNUAL_TAM_B = [0, 0, 1.454272706, 0, 1.57514896, 1.477664835]
_DDG_ANNUAL_TAM_B = [0.474364998, 1.233631888, 0.873986645, 1.236388123, 1.929240094, 0.674117932]
_VA_REMAINDER_B = [5.827734858, 5.904395548, 8.625327277, 7.843299221, 8.012255786, 8.246377188]
_COL_REMAINDER_B = [0, 0, 9.662090734, 0, 9.16916804, 8.798976785]
_DDG_REMAINDER_B = [4.005805202, 7.272375912, 4.838036555, 6.779602157, 3.776884906, 3.497657788]
_VA_OUTYEAR_LO_B = [2.551475393, 2.457053457, 2.20937342, 2.245625171]
_COL_OUTYEAR_LO_B = [1.27311354, 1.274126532, 1.256646369, 1.259008095]
_DDG_OUTYEAR_LO_B = [0.552462556, 0.565572572, 0.869625827, 0.895882451]
_VA_OUTYEAR_HI_B = [3.316918011, 3.194169494, 2.872185446, 2.919312723]
_COL_OUTYEAR_HI_B = [1.655047603, 1.656364492, 1.633640279, 1.636710524]
_DDG_OUTYEAR_HI_B = [0.718201322, 0.735244344, 1.130513575, 1.164647186]
# §4 cluster layout: ONE datasheet column per bar - [DDG-51, Virginia, Columbia]
# per FY, no spacer columns (cluster gaps are set in think-cell, not the data);
# columns = bars, rows = stacked series bottom -> top. 10 FYs x 3 classes = 30
# slots; the FY label sits over each cluster's middle (Virginia) column. Class
# fill rows carry the FY22-27 actuals only; each FY28-31 estimate is ONE chunk
# valued at the class's HIGH bound (the "lo-hi" range renders as that chunk's
# label in think-cell, not as a second stacked segment), with a rest-of-FYDP-
# gross segment above it. Columbia's unfunded FY22/23/25 are blank.
_N_FY_EXT = 10
_NSLOT = 3 * _N_FY_EXT
_DDG_SLOT = [3 * k for k in range(_N_FY_EXT)]
_VA_SLOT = [3 * k + 1 for k in range(_N_FY_EXT)]
_COL_SLOT = [3 * k + 2 for k in range(_N_FY_EXT)]


def _cluster_slots(pairs: dict) -> list:
    """Expand {slot index: value} into the 39-slot row (blanks elsewhere)."""
    return [pairs.get(i) for i in range(_NSLOT)]


_CLUSTER_HDR = [h if h is not None else ""
                for h in _cluster_slots({_VA_SLOT[k]: fy
                                         for k, fy in enumerate(_FY_HDR_EXT)})]

# Penetration (outsourced BC TAM / class total ship spend), per class - the §4
# constants' own ratio fill/(fill + remainder); Columbia's unfunded years are
# blank. Assumed low = the class FY22-25 dollar-weighted average (sum of fills
# / sum of denominators over the complete historical years); high = low x 1.30
# (the stated outsourcing-intent uplift).
_DDG_PEN = [0.105881022, 0.145030656, 0.153008245, 0.154240222, 0.338099865, 0.161590166]
_DDG_PEN_LO, _DDG_PEN_HI = 0.142934202470808, 0.185814463212051   # FY22-25 avg / x1.30 intent
_VA_PEN = [0.233931907, 0.238939858, 0.271063091, 0.190623491, 0.197900855, 0.264261247]
_VA_PEN_LO, _VA_PEN_HI = 0.235518681, 0.306174286                 # FY22-25 avg / x1.30 intent
_COL_PEN = [None, None, 0.130822702, None, 0.146602986, 0.14378869]
_COL_PEN_LO, _COL_PEN_HI = 0.130822702, 0.170069513               # FY24 only in window / x1.30

# FY28-31 FYDP gross per class, recovered from the outlook's own identity
# (implied low = FYDP gross x assumed-low penetration); the rest-of-gross rows
# subtract the HIGH bound so an outyear bar stacks low + range + rest = gross
# and tops out at the class's FYDP gross, full-height like the historicals.
_VA_OUTYEAR_REST_B = [lo / _VA_PEN_LO - hi
                      for lo, hi in zip(_VA_OUTYEAR_LO_B, _VA_OUTYEAR_HI_B)]
_COL_OUTYEAR_REST_B = [lo / _COL_PEN_LO - hi
                       for lo, hi in zip(_COL_OUTYEAR_LO_B, _COL_OUTYEAR_HI_B)]
_DDG_OUTYEAR_REST_B = [lo / _DDG_PEN_LO - hi
                       for lo, hi in zip(_DDG_OUTYEAR_LO_B, _DDG_OUTYEAR_HI_B)]


def _rng(lo: float, hi: float) -> str:
    return f"{lo:.1f}–{hi:.1f}"


# §4 side table (unhighlighted, right of the paste rectangle): the "lo–hi"
# label strings for the FY28-31 estimate chunks, $B to one decimal (the
# slide's estimate-label convention). Outsourced = implied low to high;
# retained spend = the complement against the class FYDP gross (gross minus
# high, to gross minus low).
_S4_ANNEX = [
    ["FY28–31 label ranges ($B)", "FY2028", "FY2029", "FY2030", "FY2031"],
    ["Columbia outsourced",
     *(_rng(l, h) for l, h in zip(_COL_OUTYEAR_LO_B, _COL_OUTYEAR_HI_B))],
    ["Columbia retained spend",
     *(_rng(r, r + h - l) for r, l, h in
       zip(_COL_OUTYEAR_REST_B, _COL_OUTYEAR_LO_B, _COL_OUTYEAR_HI_B))],
    ["Virginia outsourced",
     *(_rng(l, h) for l, h in zip(_VA_OUTYEAR_LO_B, _VA_OUTYEAR_HI_B))],
    ["Virginia retained spend",
     *(_rng(r, r + h - l) for r, l, h in
       zip(_VA_OUTYEAR_REST_B, _VA_OUTYEAR_LO_B, _VA_OUTYEAR_HI_B))],
    ["DDG-51 outsourced",
     *(_rng(l, h) for l, h in zip(_DDG_OUTYEAR_LO_B, _DDG_OUTYEAR_HI_B))],
    ["DDG-51 retained spend",
     *(_rng(r, r + h - l) for r, l, h in
       zip(_DDG_OUTYEAR_REST_B, _DDG_OUTYEAR_LO_B, _DDG_OUTYEAR_HI_B))],
]

# FY22-25 average annual TAM (the slide's dashed reference line is the combined
# level only; per-program averages render in the program workbooks' chartdata).
_DDG_AVG_2225_B = 0.954592913
_SUB_AVG_2225_B = 2.535565358

# Work type by FY (§8-§10, deck slide 5), FY2022-FY2025 constant FY2026 $B:
# each class's annual TAM x its own FY's gated share vector (SAM Build §3/§4).
# Rows follow _WORKTYPE_HDR; columns FY2022-FY2025. Columbia funds biennially -
# only FY2024 carries TAM inside the window.
_FY_HDR_2225 = _FY_HDR[:4]
_VA_WT_FY_B = [
    [0.368495986, 0.865859642, 0.736346985, 0.035197415],
    [0.272449311, 0.167845438, 0.942754177, 0.547155952],
    [0.513513635, 0.34467773, 0.556551769, 0.492813685],
    [0.108315223, 0.01499292, 0.194228613, 0.113847585],
    [0.076693549, 0.136814098, 0.229244033, 0.115541509],
    [0.046084466, 0.047195813, 0.083546914, 0.235329835],
    [0.003747833, 0.031124026, 0.002703856, 0.016739738],
    [0.39029784, 0.24521617, 0.462048303, 0.290617892],
]
_COL_WT_FY_B = [
    [0, 0, 0.628862421, 0],
    [0, 0, 0.350632421, 0],
    [0, 0, 0.204411117, 0],
    [0, 0, 0.04539076, 0],
    [0, 0, 0.025676639, 0],
    [0, 0, 0.039021045, 0],
    [0, 0, 0.016820118, 0],
    [0, 0, 0.143458185, 0],
]
_DDG_WT_FY_B = [
    [0.027222384, 0.056467032, 0.191894256, 0.10630836],
    [0.050574424, 0.087536052, 0.122911364, 0.090768198],
    [0.01663598, 0.043558308, 0.064574503, 0.086383965],
    [0.149893173, 0.407928757, 0.237555688, 0.540793692],
    [0.002434441, 0.003243218, 0.000790084, 0],
    [0, 0, 0.050453501, 0.026375868],
    [0.047756222, 0.255730657, 0.087605799, 0.207467163],
    [0.179848848, 0.37916663, 0.118202324, 0.178292113],
]


def _render_outsourced_bc() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1-§2 - Outsourced BC walk (deck slide 2): one waterfall per program, from
    # total ship spend to the outsourced BC endpoint. The DDG block stacks the
    # AP/LLTM EOQ segment on the Total Ship Spend column (own row, own color).
    _paste_block(c, "§1 - DDG outsourced BC walk (waterfall)",
                 ["", *_WALK_HDR],
                 [("In-year", _DDG_WALK_INYEAR_B),
                  ("AP/LLTM (P-10 EOQ)", _DDG_WALK_APLLTM_B)],
                 "B")

    _paste_block(c, "§2 - Submarine outsourced BC walk (waterfall)",
                 ["", *_WALK_HDR],
                 [("", _SUB_WALK_B)],
                 "B")

    # §3 - Outsourced BC by work type (deck slide 3): one stacked column per
    # program / class, in slide column order DDG-51, Columbia, Virginia;
    # Residual rides each stack (hatched on the slide), so each column sums to
    # its supplier TAM.
    _paste_block(c, "§3 - Outsourced BC by work type (per program/class, stacked column)",
                 ["", "DDG-51", "Columbia", "Virginia"],
                 [(name, [d, cl, v]) for name, d, v, cl in
                  zip(_WORKTYPE_HDR, _DDG_WT_B, _VA_WT_B, _COL_WT_B)],
                 "B")

    # §4 - Outsourced BC annual TAM with outlook (deck slide 4): one datasheet
    # column per bar - DDG-51, Virginia, Columbia per FY cluster, no spacer
    # columns (see the _cluster_slots note). FOUR rows per class, grouped by
    # class with Columbia first; per column the stack follows row order:
    #   outsourced        FY22-27 actuals (bottom of the historical bars)
    #   outsourced low    FY28-31 implied low (bottom of the forecast bars)
    #   outsourced high   FY28-31 INCREMENT (high - low) riding the low chunk
    #                     - its own color-codable segment; suppress its data
    #                     label (it would read the increment) and use the side
    #                     table's lo-hi strings instead
    #   retained spend    both eras in one row: FY22-27 remainder + FY28-31
    #                     rest to FYDP gross, capping every bar at full height
    # If think-cell renders the stack inverted, reverse the rows within each
    # class block; do NOT use think-cell segment sorting.
    def _class_rows(name: str, slot: list, actual: list, rem: list,
                    lo: list, hi: list, rest: list) -> list:
        blank_ok = name == "Columbia"          # unfunded years stay blank
        def _v(x): return (x or None) if blank_ok else x
        return [
            (f"{name} outsourced", _cluster_slots(
                {slot[k]: _v(v) for k, v in enumerate(actual)})),
            (f"{name} outsourced low", _cluster_slots(
                {slot[6 + j]: v for j, v in enumerate(lo)})),
            (f"{name} outsourced high", _cluster_slots(
                {slot[6 + j]: h - l for j, (l, h) in enumerate(zip(lo, hi))})),
            (f"{name} retained spend", _cluster_slots(
                {**{slot[k]: _v(v) for k, v in enumerate(rem)},
                 **{slot[6 + j]: v for j, v in enumerate(rest)}})),
        ]

    _paste_block(c, "§4 - Outsourced BC annual TAM with outlook (clustered stacked columns)",
                 ["", *_CLUSTER_HDR],
                 _class_rows("Columbia", _COL_SLOT, _COL_ANNUAL_TAM_B,
                             _COL_REMAINDER_B, _COL_OUTYEAR_LO_B,
                             _COL_OUTYEAR_HI_B, _COL_OUTYEAR_REST_B)
                 + _class_rows("Virginia", _VA_SLOT, _VA_ANNUAL_TAM_B,
                               _VA_REMAINDER_B, _VA_OUTYEAR_LO_B,
                               _VA_OUTYEAR_HI_B, _VA_OUTYEAR_REST_B)
                 + _class_rows("DDG-51", _DDG_SLOT, _DDG_ANNUAL_TAM_B,
                               _DDG_REMAINDER_B, _DDG_OUTYEAR_LO_B,
                               _DDG_OUTYEAR_HI_B, _DDG_OUTYEAR_REST_B),
                 "B", annex=_S4_ANNEX)

    # §4b - Same chart, RAMPED upper bound, single high segment (manual
    # think-cell rebuild; ADDITIVE - §4 stays the deck's source). Instead of
    # the flat x1.30 bound, penetration grows ~6.8% p.a. (1.30^(1/4)-1) from
    # the class FY22-25 average anchored at FY27, reaching x1.30 at FY31 -
    # the band commentary's "~7% p.a. towards target" read literally. Each
    # forecast bar carries ONE outsourced chunk valued at the ramped high
    # (no low segment - the pre-split §4 idiom) plus retained-to-gross, so
    # every bar still tops out at the class FYDP gross. FY31 ties to §4's
    # flat high by construction (lo x 1.30).
    _RAMP = [1.30 ** ((j + 1) / 4) for j in range(4)]   # FY28..FY31 factors

    def _ramp_rows(name: str, slot: list, actual: list, rem: list,
                   lo: list, pen_lo: float) -> list:
        blank_ok = name == "Columbia"          # unfunded years stay blank
        def _v(x): return (x or None) if blank_ok else x
        hi_ramp = [l * f for l, f in zip(lo, _RAMP)]
        rest = [l / pen_lo - h for l, h in zip(lo, hi_ramp)]
        return [
            (f"{name} outsourced", _cluster_slots(
                {slot[k]: _v(v) for k, v in enumerate(actual)})),
            (f"{name} outsourced high (ramped)", _cluster_slots(
                {slot[6 + j]: v for j, v in enumerate(hi_ramp)})),
            (f"{name} retained spend", _cluster_slots(
                {**{slot[k]: _v(v) for k, v in enumerate(rem)},
                 **{slot[6 + j]: v for j, v in enumerate(rest)}})),
        ]

    _S4B_ANNEX = [
        ["Ramped high penetration", "FY2028", "FY2029", "FY2030", "FY2031"],
        ["Columbia", *(f"{_COL_PEN_LO * f:.1%}" for f in _RAMP)],
        ["Virginia", *(f"{_VA_PEN_LO * f:.1%}" for f in _RAMP)],
        ["DDG-51", *(f"{_DDG_PEN_LO * f:.1%}" for f in _RAMP)],
        ["Growth", "~6.8% p.a. = 1.30^(1/4) - 1, FY22-25 avg anchored at FY27"],
    ]

    _paste_block(c, "§4b - Annual TAM, ramped upper bound (single high segment; manual think-cell)",
                 ["", *_CLUSTER_HDR],
                 _ramp_rows("Columbia", _COL_SLOT, _COL_ANNUAL_TAM_B,
                            _COL_REMAINDER_B, _COL_OUTYEAR_LO_B, _COL_PEN_LO)
                 + _ramp_rows("Virginia", _VA_SLOT, _VA_ANNUAL_TAM_B,
                              _VA_REMAINDER_B, _VA_OUTYEAR_LO_B, _VA_PEN_LO)
                 + _ramp_rows("DDG-51", _DDG_SLOT, _DDG_ANNUAL_TAM_B,
                              _DDG_REMAINDER_B, _DDG_OUTYEAR_LO_B, _DDG_PEN_LO),
                 "B", annex=_S4B_ANNEX)

    # §5 - FY22-25 average annual TAM: the dashed reference line.
    _paste_block(c, "§5 - FY22-25 average annual TAM (reference line)",
                 ["", "Combined"],
                 [("", [_DDG_AVG_2225_B + _SUB_AVG_2225_B])],
                 "B")

    # §6-§7 - Penetration strips: Outsourced BC / total ship spend per FY,
    # per class (the slide draws one oval row per class); FY28-31 carry the
    # assumed low/high (low = class FY22-25 dollar-weighted average, high =
    # low x 1.30 intent uplift). Columbia's unfunded FY22/23/25 are blank.
    _paste_block(c, "§6 - DDG penetration strip",
                 ["", *_FY_HDR_EXT],
                 [("Actual", _DDG_PEN + [None] * 4),
                  ("Assumed low", [None] * 6 + [_DDG_PEN_LO] * 4),
                  ("Assumed high", [None] * 6 + [_DDG_PEN_HI] * 4)],
                 "P")

    _paste_block(c, "§7 - Submarine penetration strip (per class)",
                 ["", *_FY_HDR_EXT],
                 [("Virginia actual", _VA_PEN + [None] * 4),
                  ("Virginia assumed low", [None] * 6 + [_VA_PEN_LO] * 4),
                  ("Virginia assumed high", [None] * 6 + [_VA_PEN_HI] * 4),
                  ("Columbia actual", _COL_PEN + [None] * 4),
                  ("Columbia assumed low", [None] * 6 + [_COL_PEN_LO] * 4),
                  ("Columbia assumed high", [None] * 6 + [_COL_PEN_HI] * 4)],
                 "P")

    # §6b/§7b - Penetration strips for the §4b RAMPED variant (additive):
    # the lower bound stays flat (reversion to the FY22-25 mean applies every
    # year) but the assumed HIGH ramps per FY with the §4b path, so the
    # per-FY range narrows early (e.g. DDG FY28 14-15%) and only reaches the
    # §6/§7 envelope (14-19%) at FY31.
    _paste_block(c, "§6b - DDG penetration strip (ramped variant)",
                 ["", *_FY_HDR_EXT],
                 [("Actual", _DDG_PEN + [None] * 4),
                  ("Assumed low", [None] * 6 + [_DDG_PEN_LO] * 4),
                  ("Assumed high (ramped)",
                   [None] * 6 + [_DDG_PEN_LO * f for f in _RAMP])],
                 "P")

    _paste_block(c, "§7b - Submarine penetration strip (ramped variant, per class)",
                 ["", *_FY_HDR_EXT],
                 [("Virginia actual", _VA_PEN + [None] * 4),
                  ("Virginia assumed low", [None] * 6 + [_VA_PEN_LO] * 4),
                  ("Virginia assumed high (ramped)",
                   [None] * 6 + [_VA_PEN_LO * f for f in _RAMP]),
                  ("Columbia actual", _COL_PEN + [None] * 4),
                  ("Columbia assumed low", [None] * 6 + [_COL_PEN_LO] * 4),
                  ("Columbia assumed high (ramped)",
                   [None] * 6 + [_COL_PEN_LO * f for f in _RAMP])],
                 "P")

    # §8 - Work-type mix by FY (deck slide 5): ONE 100%-stacked chart / one
    # table. The story is each vessel's work-type MIX and its year-to-year
    # shift (the slide's segment labels are % of that year's TAM), and the
    # vessels' dollar scales differ 3-6x - so the bars are vessel-grouped and
    # think-cell's 100% mode does the normalizing: paste the absolute $B
    # below, every bar renders full height with % segment labels, and the $B
    # totals ride each column as labels (the side table carries them).
    # 9 bars: DDG-51 FY22-25 | Virginia FY22-25 | Columbia FY2024 only -
    # Columbia's unfunded years are OMITTED (no placeholder holes; the slide's
    # em-dash note covers the biennial cadence). One blank spacer column
    # between vessel groups. Zero cells (sparse DDG buckets) are blank, not 0.
    def _wt_row(b: int) -> list:
        return ([v or None for v in _DDG_WT_FY_B[b]] + [None]
                + [v or None for v in _VA_WT_FY_B[b]] + [None]
                + [_COL_WT_FY_B[b][2] or None])

    def _wt_totals(wt: list) -> list:
        return [sum(wt[b][k] for b in range(8)) for k in range(4)]

    wt_annex = [
        ["Bar $B totals (column labels)", *_FY_HDR_2225],
        ["DDG-51", *_wt_totals(_DDG_WT_FY_B)],
        ["Virginia", *_wt_totals(_VA_WT_FY_B)],
        ["Columbia", None, None, _wt_totals(_COL_WT_FY_B)[2], None],
    ]
    # Row order = stack order (first datasheet row renders as the BOTTOM
    # segment, per the manager's vDraft chart internals): the seven named
    # buckets descend by their total dollars across all nine bars - biggest
    # at the bottom, smaller rising - and Residual is pinned LAST so it caps
    # every column. One global order for the chart (a stacked series cannot
    # re-sort per column); do NOT use think-cell segment sorting.
    def _bucket_total(b: int) -> float:
        return sum(v or 0 for v in _wt_row(b))

    wt_order = sorted(range(7), key=_bucket_total, reverse=True) + [7]
    _paste_block(c, "§8 - Outsourced BC work-type mix by FY (100% stacked "
                    "columns: DDG-51 FY22-25 | Virginia FY22-25 | Columbia FY24)",
                 ["", *_FY_HDR_2225, "", *_FY_HDR_2225, "", "FY2024"],
                 [(_WORKTYPE_HDR[b], _wt_row(b)) for b in wt_order],
                 "B", annex=wt_annex)

    # Trailing widths cover the §4 side table (2 gap cols + label + 4 FYs).
    ws = worksheet(c.rows, cols=[40] + [18] * (_NCOLS - 1) + [4, 4, 26, 11, 11, 11, 11],
                   tab_color=TAB_COLOR, with_gutter=True)
    return WorksheetSpec(ws)


def render() -> WorksheetSpec:
    """Module-first registry path: SHEETS = [z_chart_data_outsourced_bc]."""
    return _render_outsourced_bc()


# Entry-style registry path, matching z_chart_data:
# SHEETS = [..., z_chart_data_outsourced_bc.CHART_DATA_OUTSOURCED_BC]
CHART_DATA_OUTSOURCED_BC = SheetEntry(_TAB, _GROUP, _render_outsourced_bc)
