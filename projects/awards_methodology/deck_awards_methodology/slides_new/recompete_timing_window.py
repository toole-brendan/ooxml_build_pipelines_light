"""recompete_timing_window — Awards Analysis Market Timing vPrelim deck, source slide 2.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats (original mechanical convert): text_box=25, connector=2, chart=0,
table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=1, dropped=1.

HAND-REWORKED: the lower flow is reframed into three left-railed lanes —
Anchor (baseline date by award type) → Shifts (variables that pull earlier /
push later) → Signals (is the recompete forming?) — built with the _spine() /
_flow_row() helpers; the right-side "when the date misleads" box is collapsed
into one bordered card. The top half (color-of-money bars, Upper Bound +
Funding-read cards, chips) is unchanged. Every font is an integer pt, ≥ 8pt.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_X1 = IN(2.834)    # flow-row left edge (aligns under the color-of-money bars)
_W1 = IN(5.98)     # flow-row width
_Y1 = IN(2.888)    # color-money chip row (top half)
_W2 = IN(0.78)     # color-money chip width
_H1 = IN(0.2)      # color-money chip height / lane-cue length
_X2 = IN(1.419)    # lane-spine left edge
_SPINE_W = IN(1.204)
_ROW_H = 0.355     # flow-row height, inches (lane pitch ≈ 0.388)


def _spine(n: int, y: float, h: float, title: str, sub: str) -> str:
    """Left-rail label for a flow lane: bold title over a small italic sublabel."""
    return text_box(n, "Lane Spine", _X2, IN(y), _SPINE_W, IN(h),
                    [paragraph([run(title, size=PT(10), bold=True, color=BLACK, font=FONT)],
                               align="ctr", line_spacing=100000),
                     paragraph([run(sub, size=PT(8), italic=True, color=BLACK, font=FONT)],
                               align="ctr", line_spacing=100000)],
                    fill=GRAY_2, line_color=BLACK, anchor="ctr",
                    l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288)


def _flow_row(n: int, y: float, label: str, detail: str, *, fill: str, line: str,
              alpha=None, sep: str = "  |  ", detail_color: str = BLACK,
              detail_italic: bool = False, line_w: int = 9525) -> str:
    """One lane row: bold label + separator + detail, kept to a single line."""
    return text_box(n, "Flow Row", _X1, IN(y), _W1, IN(_ROW_H),
                    [paragraph([run(label, size=PT(9), bold=True, color=BLACK, font=FONT),
                                run(sep, size=PT(8), color=GRAY_4, font=FONT),
                                run(detail, size=PT(8), italic=detail_italic, color=detail_color, font=FONT)],
                               align="l", line_spacing=100000)],
                    fill=fill, fill_alpha=alpha, line_color=line, line_width=line_w,
                    anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(title_placeholder("Recompete Timing", "Award type anchors the baseline date, color of money caps how late it can fall, and a handful of variables and signals move it from there."))
    out.append(prelim_chip())
    out.append(text_box(n(), "Upper Bound Card", IN(0.495), IN(1.676), IN(2.128), IN(1.416), [paragraph([run("Upper Bound", size=PT(12), bold=True, italic=True, underline=True, color=BLACK, font=FONT)], align="ctr", space_after=160, line_spacing=100000), paragraph([], align="ctr", space_after=160, line_spacing=100000, end_size=1000), paragraph([run("Color-of-money obligation period", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", space_after=160, line_spacing=100000), paragraph([run("Latest feasible award that can use a given FY’s money — not period of performance.", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=BLACK, anchor="ctr", l_ins=18288, t_ins=36576, r_ins=18288, b_ins=36576))
    out.append(text_box(n(), "Color of Money Bar", _X1, IN(1.676), IN(10), IN(0.38), [paragraph([run("SCN", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  5-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="007770", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Color of Money Bar", _X1, IN(2.194), IN(6), IN(0.38), [paragraph([run("Procurement", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  3-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="447BB2", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Color of Money Bar", IN(2.83), IN(2.712), IN(4), IN(0.38), [paragraph([run("RDT&E", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  2-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="7030A0", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Upper Bound Caption", _X1, IN(3.185), _W1, IN(0.15), [paragraph([run("Bar length = how long that year’s money stays obligable; the cap moves only if a later appropriation funds the award.", size=PT(8), italic=True, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Funding Read Card", IN(9.045), IN(2.261), IN(3.789), IN(0.867), [paragraph([run("Funding read", size=PT(10), bold=True, color=BLACK, font=FONT)], space_after=110, line_spacing=100000), paragraph([run("Which color of money funds it, and how much obligation life remains — that sets the latest feasible award.", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="808080", l_ins=73152, t_ins=36576, r_ins=73152, b_ins=36576))
    out.append(text_box(n(), "Color Money Chip", IN(9.225), _Y1, _W2, _H1, [paragraph([run("O&M", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 1 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_4, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(10.075), _Y1, _W2, _H1, [paragraph([run("RDT&E", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 2 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="7030A0", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(10.925), _Y1, _W2, _H1, [paragraph([run("Proc", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 3 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(11.775), _Y1, _W2, _H1, [paragraph([run("SCN", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 5 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="007770", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Likely Window Output", IN(0.495), IN(3.48), IN(0.827), IN(2.813), [paragraph([run("Likely Window", size=PT(12), bold=True, italic=True, underline=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color=BLACK, anchor="ctr", l_ins=27432, t_ins=36576, r_ins=27432, b_ins=36576))
    # ── Lane 1 — Anchor (baseline date by award type) ──
    out.append(_spine(n(), 3.48, 1.131, "Anchor", "by award type"))
    out.append(_flow_row(n(), 3.48,  "Standalone definitive contract", "ultimate completion + options", fill=GRAY_1, line=BLACK, sep="  —  ", detail_color=DK, detail_italic=True, line_w=6350))
    out.append(_flow_row(n(), 3.868, "Task / delivery order", "order completion + order options", fill=GRAY_1, line=BLACK, sep="  —  ", detail_color=DK, detail_italic=True, line_w=6350))
    out.append(_flow_row(n(), 4.256, "Parent IDIQ / MAC / GWAC", "last date to order + parent options", fill=GRAY_1, line=BLACK, sep="  —  ", detail_color=DK, detail_italic=True, line_w=6350))
    # ── Lane 2 — Shifts (variables that move the date earlier / later) ──
    out.append(_spine(n(), 4.71, 0.743, "Shifts", "pull / push"))
    out.append(_flow_row(n(), 4.71,  "Pull earlier  ↑", "award type, value & complexity, full-and-open, incumbency, scope changes", fill="1B8A57", alpha=16000, line="1B8A57"))
    out.append(_flow_row(n(), 5.098, "Push later  ↓", "options exercised, bridge / sole-source, protest delay, date drift", fill="C00000", alpha=16000, line="C00000"))
    # ── Lane 3 — Signals (is the recompete forming?) ──
    out.append(_spine(n(), 5.55, 0.743, "Signals", "early indicators"))
    out.append(_flow_row(n(), 5.55,  "Buy is forming", "FYDP / obligations, forecast, sources-sought, draft RFP", fill="1B8A57", alpha=16000, line="1B8A57"))
    out.append(_flow_row(n(), 5.938, "Customer intel", "acquisition authority, operational sponsor, PM signal", fill="447BB2", alpha=16000, line="447BB2"))
    # ── right-side caveat note: pale-blue dashed box + soft shadow, bulleted body ──
    _bullet = dict(bullet=True, mar_l=142875, indent=-142875, space_after=80, line_spacing=100000)
    out.append(text_box(n(), "Date Misleads Card", IN(9.045), IN(3.48), IN(3.789), IN(1.95),
        [paragraph([run("When the date misleads", size=PT(11), bold=True, color=BLACK, font=FONT)], space_after=60, line_spacing=100000),
         paragraph([], end_size=800, line_spacing=100000),
         paragraph([run("Options remain: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("may trigger an option, not a recompete", size=PT(9), color=BLACK, font=FONT)], **_bullet),
         paragraph([run("LDO ≠ performance end: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("an ordering deadline, not a PoP", size=PT(9), color=BLACK, font=FONT)], **_bullet),
         paragraph([run("Parent / child mismatch: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("child orders can outlast the parent", size=PT(9), color=BLACK, font=FONT)], **_bullet),
         paragraph([run("Successor early: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("rebuy can land before incumbent LDO", size=PT(9), color=BLACK, font=FONT)], **_bullet),
         paragraph([run("Retention path: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("bridge or in-scope mod can defer it", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=142875, indent=-142875, line_spacing=100000)],
        fill="CEDDEC", line_color="223E59", line_width=12700, dashed_line=True, anchor="t", l_ins=91440, t_ins=73152, r_ins=91440, b_ins=54864,
        effects='<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/></a:prstClr></a:outerShdw></a:effectLst>'))
    # ── lane cues: one short arrow pointing from the rail into each lane ──
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(4.05), _H1, IN(0), color=DK, width=6350, arrow=True))
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(5.08), _H1, IN(0), color=DK, width=6350, arrow=True))
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(5.92), _H1, IN(0), color=DK, width=6350, arrow=True))
    return "".join(out)


def render() -> str:
    return slide(_body())
