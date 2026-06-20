"""z_chart_data - consolidated "z_ChartData" tab.

First of the two chart-data tabs for the consolidated DDG + submarine slide deck;
the Outsourced BC slide blocks (walk, annual outlook, penetration, work type by
program) live on the second tab, z_ChartData_OutsourcedBC. The tab is
intentionally not a model: every value below is hardcoded from the two program
workbooks' final chart-data / model outputs, then arranged into the same pale-yellow
think-cell paste rectangles used by the DDG and submarine z_ChartData tabs.

Dollar basis: constant FY2026 $ (Green Book Procurement deflator, FY2026 = 1.000),
matching the program workbooks' Deflators tabs. TAM streams include the OBBBA
Sec. 20002 mandatory funding: DDG folds Sec. 20002(17) into its BC stream; the
submarine model carries Sec. 20002(16) as a separate toggled stream (on). Award /
subaward evidence dollars (supplier shares, visibility) stay nominal as observed.

Block -> consolidated deck chart/exhibit (slide order):
  §1 Executive TAM/SAM          stacked/comparison column, $B/yr
  §2 DDG cost funnel            waterfall, $B
  §3 Submarine cost funnel      waterfall, $B
  §4 TAM bridge - DDG           waterfall, cumulative $B
  §5 TAM bridge - submarine     dollar summary, cumulative $B
  §6 Supplier-share evidence    ranked column, %
  §7 Annual cadence             stacked column by FY, $B/yr
  §8 Work-type allocation       ranked stacked column + residual, $M/yr
  §9 SAM scenarios              clustered/ranked column, $B/yr
  §10 Supplier visibility       visible-flow / outsourcing evidence, $M

think-cell waterfall convention: every data cell is a STEP, so a computed subtotal
or endpoint is the literal text marker "e". Numeric values are literals; there are
no formulas or cross-sheet links.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, banner_row, write_row
from workbook_core.styles import (
    S_TITLE_SHEET, S_TITLE_SECTION,
    S_PASTE_HEADER_TL, S_PASTE_HEADER_T, S_PASTE_HEADER_TR,
    S_PASTE_LABEL_L, S_PASTE_LABEL_BL,
    S_PASTE_VAL_INT_M, S_PASTE_VAL_R_M, S_PASTE_VAL_B_M, S_PASTE_VAL_BR_M,
    S_PASTE_VAL_INT_B, S_PASTE_VAL_R_B, S_PASTE_VAL_B_B, S_PASTE_VAL_BR_B,
    S_PASTE_VAL_INT_P, S_PASTE_VAL_R_P, S_PASTE_VAL_B_P, S_PASTE_VAL_BR_P,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

TAB_NAME = "z_ChartData"
SHEET_GROUP = "chartdata"
TAB_COLOR = group_color(SHEET_GROUP)

_GROUP = SHEET_GROUP
_TAB = TAB_NAME
_NCOLS = 9                       # widest paste block: corner + 8 work-type categories (§8)


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


def _paste_block(c: RowCursor, title: str, header: list, rows: list, unit: str) -> None:
    """Emit one bordered think-cell paste rectangle.

    header: full top row; header[0] is the blank corner, header[1:] are categories
    or waterfall steps. rows: list of (row_label, [values]), where values align to
    header[1:]. A value may be a float/int, None (blank), or the waterfall marker
    "e".
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

    vs = _VAL_STYLE[unit]
    c.write(header,
            styles=[S_PASTE_HEADER_TL] + [S_PASTE_HEADER_T] * (ncol - 1) + [S_PASTE_HEADER_TR],
            outline_level=1)
    n = len(rows)
    for i, (label, vals) in enumerate(rows):
        last = (i == n - 1)
        styles = [S_PASTE_LABEL_BL if last else S_PASTE_LABEL_L]
        for j in range(1, ncol + 1):
            if last:
                styles.append(vs["BR"] if j == ncol else vs["B"])
            else:
                styles.append(vs["R"] if j == ncol else vs["INT"])
        c.write([label, *vals], styles=styles, outline_level=1)
    c.blank(2)


# --- Hardcoded consolidated values ----------------------------------------
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_HDR = [f"FY{fy}" for fy in _FY]

# Executive summary, average annual $B.
_DDG_TAM_B = 0.6585466942276466
_SUB_TAM_B = 3.53536223644271
_COMBINED_TAM_B = _DDG_TAM_B + _SUB_TAM_B
_BROAD_SAM_B = 3.541282237778322

# Cost funnels, FY2022-FY2027 cumulative constant FY2026 $B. Waterfall endpoint is
# "e". Both programs are on the same FY2022-FY2027 portfolio basis. DDG totals = SUM
# of the SCN Budget §3 portfolio producer constant rows (Total 31.192092, GFE
# 10.759287, other non-BC 2.275680 -> Basic Construction 18.157125). The funnels
# stay P-5c-scope: the OBBBA mandatory awards enter at the TAM bridge, not here.
_DDG_COST_FUNNEL_B = [31.1920922, -10.75928724, -2.27568007, "e"]
_SUB_COST_FUNNEL_B = [85.62347197, -17.24598751, -10.48950382, "e"]

# TAM bridge, cumulative $B. DDG BC construction base = P-5c constant BC + the
# OBBBA Sec. 20002(17) mandatory BC base (folded into the BC stream, per the DDG
# workbook). Submarine carries its OBBBA Sec. 20002(16) BC base as its own element
# so base x coefficient still reproduces the supplier TAM.
_DDG_TAM_BRIDGE_B = [21.5483248900, -18.844768891734, "e", 1.2477241664, "e"]
_SUB_TAM_BRIDGE_B = [57.88798064, 2.6774821589246, 21.2121734186562, 0.0]
_COMBINED_TAM_CUM_B = 25.163453584022198

# Supplier-share evidence, %.
_DDG_APPLIED_BC_SHARE = 0.125464787266162
_DDG_CORRECTED_POP = 0.32839487515574817
_DDG_DISCLOSED_ARTIFACT = 0.73644244876732046
_SUB_APPLIED_BC_SHARE = 0.35023547147786133
_SUB_POP_ANCHOR = 0.51756127773687943
_SUB_AP_LLTM_REF = 0.48486094882578951

# Annual cadence, $B by FY (DDG = BC stream + AP/LLTM; FY2026 carries the OBBBA
# two-ship BC add and the AP/LLTM spike on the DDG side, and the OBBBA second
# Virginia boat on the submarine side). z_chart_data_outsourced_bc imports these
# actuals (and _FY_HDR) for its §2 outlook block.
_DDG_ANNUAL_TAM_B = [
    0.270500701233185,
    0.611921177697855,
    0.433525545617588,
    0.650015481056835,
    1.650933037317575,
    0.334384221742955,
]
_SUB_ANNUAL_TAM_B = [
    1.8331714389231,
    1.90952909695789,
    5.61915092225009,
    1.90285554217133,
    4.54396977250461,
    5.40349664584922,
]

# Work-type allocation, average annual $M in the slide's ranked category order.
# z_chart_data_outsourced_bc imports _WORKTYPE_HDR (§5 bucket order).
_WORKTYPE_HDR = [
    "Electrical and power",
    "Piping, valves, and pumps",
    "Structural fabrication and pre-outfit",
    "Machining",
    "Coatings and insulation",
    "Castings and forgings",
    "HVAC and ventilation",
    "Residual",
]
_SUB_WORKTYPE_M = [
    1314.84531886375,
    675.178728542329,
    596.592286553305,
    116.596076476217,
    189.129612911059,
    151.044869525244,
    60.8275759543346,
    None,
]
_DDG_WORKTYPE_M = [
    37.9029717726373,
    34.8783669127747,
    36.42351659956,
    258.766620524605,
    16.9830967067049,
    11.1399226196339,
    40.9732738161658,
    None,
]
_RESIDUAL_M = [None, None, None, None, None, None, None,
               _COMBINED_TAM_B * 1000 - _BROAD_SAM_B * 1000]

# Scenario SAM, average annual $B.
_SCENARIO_HDR = [
    "Broad mfg (envelope)",
    "HM&E",
    "Electrical/power",
    "Metal components",
    "Modular assy",
]
_SCENARIO_SAM_B = [
    _BROAD_SAM_B,
    (2167.44769983663 + 372.521233026183) / 1000,
    (1314.84531886375 + 37.9029717726373) / 1000,
    (864.233232554766 + 306.330059743799) / 1000,
    (400.743857021115 + 7.66313205877709) / 1000,
]

# Visibility / evidence floor, $M. DDG bands are from the DDG FFATA-gap block;
# submarine visible flow is the supplier-addressable visible value from the
# submarine Entity Master roll-up.
_VISIBILITY_HDR = [
    "DDG visible flow",
    "DDG outsourced low",
    "DDG outsourced mid",
    "DDG outsourced high",
    "Sub visible flow",
]
_VISIBILITY_M = [2728.6, 11311.4, 13573.7, 16159.2, 5451.121335849999]


def _render_chart_data() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Executive TAM/SAM: one stacked TAM column and one SAM comparison column.
    _paste_block(c, "§1 - Executive TAM/SAM (stacked/comparison column)",
                 ["", "Combined supplier TAM", "Broad component SAM"],
                 [("Submarine", [_SUB_TAM_B, None]),
                  ("DDG", [_DDG_TAM_B, None]),
                  ("Broad component SAM", [None, _BROAD_SAM_B])],
                 "B")

    # §2-§3 - Scope and cost funnel small multiples (FY2022-FY2027 cumulative). Same
    # top-level buckets on both programs so the slide doesn't imply identical cost-
    # category composition; per-program detail lives in the slide's interpretation cards.
    _paste_block(c, "§2 - DDG cost funnel (waterfall)",
                 ["", "Total ship estimate", "Less GFE / directed equipment",
                  "Less other non-BC", "Basic Construction"],
                 [("", _DDG_COST_FUNNEL_B)],
                 "B")

    _paste_block(c, "§3 - Submarine cost funnel (waterfall)",
                 ["", "Total ship estimate", "Less GFE / directed equipment",
                  "Less other non-BC", "Basic Construction"],
                 [("", _SUB_COST_FUNNEL_B)],
                 "B")

    # §4-§5 - Program-specific TAM bridge evidence.
    _paste_block(c, "§4 - TAM bridge - DDG (waterfall)",
                 ["", "BC construction base (P-5c + OBBBA)", "Less prime/co-prime/GFE", "BC supplier stream", "AP/LLTM stream", "DDG TAM"],
                 [("", _DDG_TAM_BRIDGE_B)],
                 "B")

    _paste_block(c, "§5 - TAM bridge - submarine (dollar summary)",
                 ["", "BC construction base", "OBBBA mandatory BC base", "Submarine supplier TAM", "AP/LLTM additive base"],
                 [("", _SUB_TAM_BRIDGE_B)],
                 "B")

    # §6 - Supplier-share evidence: keep program inputs separate; do not blend.
    _paste_block(c, "§6 - Supplier-share evidence (ranked column)",
                 ["", "DDG applied", "DDG corrected POP", "DDG disclosed artifact",
                  "Sub applied", "Sub POP anchor", "Sub AP/LLTM ref"],
                 [("", [_DDG_APPLIED_BC_SHARE, _DDG_CORRECTED_POP,
                        _DDG_DISCLOSED_ARTIFACT, _SUB_APPLIED_BC_SHARE,
                        _SUB_POP_ANCHOR, _SUB_AP_LLTM_REF])],
                 "P")

    # §7 - Annual cadence: DDG is the lighter base segment, submarine the upper segment.
    _paste_block(c, "§7 - Annual cadence (stacked column)",
                 ["", *_FY_HDR],
                 [("DDG", _DDG_ANNUAL_TAM_B),
                  ("Submarine", _SUB_ANNUAL_TAM_B)],
                 "B")

    # §8 - Work-type allocation: named buckets stacked by program; residual separate.
    _paste_block(c, "§8 - Work-type allocation (ranked stacked column)",
                 ["", *_WORKTYPE_HDR],
                 [("Submarine", _SUB_WORKTYPE_M),
                  ("DDG", _DDG_WORKTYPE_M),
                  ("Residual", _RESIDUAL_M)],
                 "M")

    # §9 - SAM scenarios: overlapping cuts of one TAM; do not stack or sum.
    _paste_block(c, "§9 - SAM scenarios (clustered/ranked column)",
                 ["", *_SCENARIO_HDR],
                 [("", _SCENARIO_SAM_B)],
                 "B")

    # §10 - Supplier visibility: evidence floor and DDG outsourcing band.
    _paste_block(c, "§10 - Supplier visibility (evidence floor)",
                 ["", *_VISIBILITY_HDR],
                 [("", _VISIBILITY_M)],
                 "M")

    ws = worksheet(c.rows, cols=[40] + [18] * (_NCOLS - 1),
                   tab_color=TAB_COLOR, with_gutter=True)
    return WorksheetSpec(ws)


def render() -> WorksheetSpec:
    """Module-first registry path: SHEETS = [z_chart_data]."""
    return _render_chart_data()


# Entry-style registry path used by the DDG/submarine chartdata modules:
# SHEETS = [z_chart_data.CHART_DATA]
CHART_DATA = SheetEntry(_TAB, _GROUP, _render_chart_data)
