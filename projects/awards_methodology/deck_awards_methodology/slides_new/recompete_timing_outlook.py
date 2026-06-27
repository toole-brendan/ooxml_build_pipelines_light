"""recompete_timing_outlook — Awards Methodology deck, "Recompete Timing and Outlook".

EXHIBIT — a single-program recompete-timing timeline on a shared fiscal-year axis
(FY21–FY31) with three stacked swim-lanes — the visual form of the playbook's
three-layer model:
  • What program needs (Requirement) — planned procurement units across the years.
  • Funding — appropriations colour-coded by color of money, with bar LENGTH = the
    obligation window (RDT&E,N 2-yr · OPN 3-yr · SCN 5-yr).
  • Contracting — the existing vehicle's Active Ordering Period (ordering-period start
    → common last date to order), then a dashed Likely Recompete Window bounded by
    when the follow-on funding's obligation window completes.
The thesis: the recompete window is LOCATED by the contracting lane (last date to
order) and BOUNDED by the funding lane (obligation window).

DATA — instantiated with AN/SLQ-25 "Nixie" (surface-ship torpedo countermeasure):
  • Contracting lane is LIVE: parent IDIQ N0025321D0002 (Ultra Electronics Ocean
    Systems; NUWC; PSC 5865; full-and-open). Ordering period 2020-12-15 →
    2025-12-16 (common last date to order); 26 delivery orders, $103.1M realized
    (ceiling $537.0M); orders perform to ~2027-02. Recompete is OPEN NOW (the last
    date to order passed ~2025-12) with no successor IDIQ visible in the data.
    Source: USAspending widened-Navy pull (navy_lane_autonomy_sensors_families.csv).
  • Funding and Requirement lanes are ILLUSTRATIVE, clearly labelled, and swap-ready:
    real color-of-money / obligation windows await a File-C (TAS) pull; planned
    units await the President's-Budget P-1 line.

Hand-built in the house style (recoloured off the raw-converted wireframe's purple
onto the house BLUE_*/GRAY_* ramps; copy tightened to the gold-standard budget; all
font sizes integer). This is a Preliminary slide.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell,
    breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_3, BLUE_4, BLUE_5, GRAY_1, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── FY-axis geometry (shared x-mapping so the floating ink registers with the table) ──
_LEFT, _SPINE_W = 0.495, 1.16
_X0 = _LEFT + _SPINE_W          # 1.655 — left edge of the FY21 column
_COL_W = 1.016                  # one fiscal-year column (matches the table grid)
_FY = list(range(21, 32))       # FY21 … FY31  (11 columns)
_TABLE_W = _SPINE_W + _COL_W * len(_FY)   # 12.336

_T_Y = 2.05                     # table top (shifted down to clear the program title)
_H_HDR, _H_L1, _H_L2, _H_L3 = 0.28, 0.56, 1.35, 2.10
_L1_Y = _T_Y + _H_HDR           # Requirement lane top
_L2_Y = _L1_Y + _H_L1           # Funding lane top
_L3_Y = _L2_Y + _H_L2           # Contracting lane top


def _fyx(fy):              # left edge of a 2-digit fiscal-year column
    return _X0 + (fy - 21) * _COL_W


def _fyspan(a, b):         # (x, cx) covering FY a .. FY b inclusive
    return _fyx(a), (b - a + 1) * _COL_W


def _datex(y, m, d=15):    # sub-year x for a calendar date (fiscal-year aware)
    fy, fmo = (y + 1, m - 9) if m >= 10 else (y, m + 3)
    pos = (fmo - 1 + d / 30.0) / 12.0
    return _X0 + ((fy - 2000 - 21) + pos) * _COL_W


# key contracting anchors (LIVE Nixie data)
_ORD_START = _datex(2020, 12, 15)   # ordering-period start
_LDO = _datex(2025, 12, 16)         # common last date to order
_OBLIG = _datex(2029, 9, 30)        # follow-on obligation window complete (illustrative)
_RECOMP_END = _datex(2028, 3, 31)   # end of the likely recompete window


# ── table kit (local; renders identically to tcell — separates content from mechanics) ──
def edge(color, w=12700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


_GREY = lambda: edge("808080", 6350)   # noqa: E731 — inner fiscal-year rule


def _grid_cells(label, *, top=None, bottom=None, hdr=False):
    """One table row: spine label + 11 empty FY cells with the inner/section rules."""
    cells = [cell(label, size=PT(10), bold=True, align="ctr", anchor="ctr", T=top, B=bottom)]
    for i, fy in enumerate(_FY):
        L = _GREY() if i else None
        R = _GREY() if i < len(_FY) - 1 else None
        if hdr:
            cells.append(cell(f"FY{fy}", size=PT(10), bold=True, align="ctr", anchor="b",
                              L=L, R=R, B=edge(BLACK)))
        else:
            cells.append(cell("", L=L, R=R, T=top, B=bottom))
    return cells


# ── Funding lane bars (ILLUSTRATIVE color-of-money: fill = appropriation, length = obligation window) ──
_FUND_BARS = [    # (x, cx, y, fill, label)
    (*_fyspan(21, 23), 3.12, BLUE_4, "OPN base · $XXM"),                 # 3-yr production money (current contract)
    (_datex(2027, 1, 15), _OBLIG - _datex(2027, 1, 15), 3.12, BLUE_4, "Follow-on OPN · $XXM (illus.)"),
    (*_fyspan(21, 25), 3.57, BLUE_5, "SCN forward-fit · $XXM"),          # 5-yr new-construction install money
]

# ── color-of-money legend ──
_LEGEND = [    # (swatch x, fill, caption) — packed tight
    (1.70, BLUE_3, "RDT&E,N · 2-yr"),
    (2.80, BLUE_4, "OPN · 3-yr"),
    (3.70, BLUE_5, "SCN · 5-yr"),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(title_placeholder("Recompete Timing and Outlook",
                                 "Ordering window closed FY26, recompete now open, no successor visible."))
    out.append(prelim_chip())
    # ── "Illustrative" chip — clones the Preliminary chip (dims/border/font), medium-gray fill ──
    out.append(text_box(n(), "Illustrative chip", IN(9.524), IN(0.122), IN(1.605), IN(0.317),
        [paragraph([run("Illustrative", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
        fill="A6A6A6", line_color=BLACK, line_width=19050, anchor="ctr",
        l_ins=45720, t_ins=9144, r_ins=45720, b_ins=9144))
    # ── program / award title (top-left; no-fill, extended, single font size) ──
    out.append(text_box(n(), "Program", IN(_LEFT), IN(1.54), IN(9.30), IN(0.30),
        [paragraph([run("AN/SLQ-25 Nixie", size=PT(12), bold=True, color=BLACK, font=FONT),
                    run("   ·   IDIQ N0025321D0002   ·   Ultra Electronics Ocean Systems", size=PT(12), color=BLACK, font=FONT)],
                   align="l", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    # ── scaffold table: FY axis + three lane rows (the grid; bars/markers float on top) ──
    out.append(table(n(), "FY Lane Grid", IN(_LEFT), IN(_T_Y), IN(_TABLE_W),
                     IN(_H_HDR + _H_L1 + _H_L2 + _H_L3),
                     col_widths=[IN(_SPINE_W)] + [IN(_COL_W)] * len(_FY), rows=[
        trow(_grid_cells("", bottom=edge(BLACK), hdr=True), h=IN(_H_HDR)),
        trow(_grid_cells("What program needs", bottom=_GREY()), h=IN(_H_L1)),
        trow(_grid_cells("Funding", bottom=_GREY()), h=IN(_H_L2)),
        trow(_grid_cells("Contracting", bottom=edge(BLACK)), h=IN(_H_L3)),
    ]))
    # ── Lane 1 · Requirement (illustrative, swap-ready) ──
    out.append(text_box(n(), "Planned procurement", IN(_fyx(21)), IN(2.47), IN(_COL_W * 11), IN(0.30),
        [paragraph([run("Planned procurement (units)", size=PT(9), bold=True, color=BLACK, font=FONT),
                    run("   illustrative, pending P-1", size=PT(9), italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000)],
        fill=GRAY_1, line_color=DK, dashed_line=True, anchor="ctr"))
    # ── Lane 2 · Funding (illustrative color-of-money bars; right edge ties to the obligation marker) ──
    for _x, _cx, _y, _fill, _t in _FUND_BARS:
        out.append(text_box(n(), "Funding bar", IN(_x), IN(_y), IN(_cx), IN(0.30),
            [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=WHITE, line_width=6350, anchor="ctr",
            l_ins=45720, t_ins=18000, r_ins=45720, b_ins=18000))
    # tie line: follow-on funding obligation end → obligation-complete marker (the thesis)
    out.append(connector(n(), "Obligation tie", IN(_OBLIG), IN(3.42), IN(0), IN(1.36),
                         color=GRAY_4, width=6350, dashed=True))
    # ── Lane 3 · Contracting (LIVE) — active ordering band + recompete window ──
    out.append(text_box(n(), "Active Ordering Period", IN(_ORD_START), IN(4.36), IN(_LDO - _ORD_START), IN(0.50),
        [paragraph([run("Active Ordering Period", size=PT(11), bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000),
         paragraph([run("26 orders · $103.1M realized", size=PT(9), italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000)],
        fill=GRAY_1, line_color=DK, anchor="ctr"))
    out.append(text_box(n(), "Likely Recompete Window", IN(_LDO), IN(4.36), IN(_RECOMP_END - _LDO), IN(0.50),
        [paragraph([run("Likely Recompete Window", size=PT(11), bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000),
         paragraph([run("open now · no successor in data", size=PT(9), italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000)],
        fill=WHITE, line_color=GRAY_4, dashed_line=True, anchor="ctr"))
    # marker dots (observed = black) + obligation-complete tick (inferred = grey triangle)
    out.append(text_box(n(), "Start marker", IN(_ORD_START - 0.08), IN(4.80), IN(0.16), IN(0.16),
        [paragraph([], line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="ellipse", anchor="ctr"))
    out.append(text_box(n(), "Last-order marker", IN(_LDO - 0.08), IN(4.80), IN(0.16), IN(0.16),
        [paragraph([], line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="ellipse", anchor="ctr"))
    out.append(text_box(n(), "Obligation marker", IN(_OBLIG - 0.09), IN(4.78), IN(0.18), IN(0.20),
        [paragraph([], line_spacing=100000)], fill=GRAY_4, line_color=DK, prst="triangle", anchor="ctr"))
    # milestone dates (bold) + descriptions — left-aligned from the spine edge for the leftmost milestone
    out.append(text_box(n(), "Start date", IN(1.66), IN(4.96), IN(1.05), IN(0.22),
        [paragraph([run("2020-12-15", size=PT(9), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Last-order date", IN(_LDO - 0.45), IN(4.96), IN(0.90), IN(0.22),
        [paragraph([run("2025-12-16", size=PT(9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Start desc", IN(1.66), IN(5.19), IN(2.00), IN(0.22),
        [paragraph([run("Ordering period starts", size=PT(9), color=BLACK, font=FONT)], align="l", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Last-order desc", IN(_LDO - 0.70), IN(5.19), IN(1.40), IN(0.22),
        [paragraph([run("Common last date to order", size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Obligation desc", IN(_OBLIG - 1.85), IN(5.05), IN(2.00), IN(0.22),
        [paragraph([run("Obligation window complete", size=PT(9), italic=True, color=BLACK, font=FONT)], align="r", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    # ── color-of-money legend ──
    out.append(text_box(n(), "Legend label", IN(_LEFT), IN(6.52), IN(1.20), IN(0.22),
        [paragraph([run("Color of money:", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    for _x, _fill, _cap in _LEGEND:
        out.append(text_box(n(), "Legend swatch", IN(_x), IN(6.54), IN(0.18), IN(0.18),
            [paragraph([], line_spacing=100000)], fill=_fill, line_color=WHITE, line_width=6350, anchor="ctr"))
        out.append(text_box(n(), "Legend caption", IN(_x + 0.22), IN(6.52), IN(1.45), IN(0.22),
            [paragraph([run(_cap, size=PT(9), color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Legend note", IN(4.75), IN(6.52), IN(2.70), IN(0.22),
        [paragraph([run("bar length = obligation window", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Legend key", IN(9.60), IN(6.52), IN(3.24), IN(0.22),
        [paragraph([run("Solid: contract data  ·  Dashed: inferred", size=PT(9), italic=True, color=BLACK, font=FONT)], align="r", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, r_ins=0))
    return "".join(out)


def render() -> str:
    return slide(_body())
