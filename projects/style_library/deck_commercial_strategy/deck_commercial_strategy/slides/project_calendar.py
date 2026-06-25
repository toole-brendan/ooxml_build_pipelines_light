"""project_calendar - Commercial Strategy deck, source slide 4.

Auto-converted from the source .pptx by _tools/convert_slide.py. The native
<c:chart> exhibit is bundled verbatim with its .xlsb (byte-exact, still "Edit
Data"-editable); shapes are deck_core primitives at the source EMU coordinates.
Standard chrome uses the house builders; repeated shape clusters are data tables
+ loops; think-cell <a:fld> labels are frozen; the OLE frame + EMF preview dropped.

Converter stats: text_box=1, connector=0, chart=0, table=1, chrome_builders=2, clusters=3 (covering 20 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, breadcrumb, title_placeholder,
)
from deck_core.charts import graphic_frame, editable_bundled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_LBL_H = IN(0.4)
_LBL2_H = IN(0.4)
_VAL_W, _VAL_H = IN(0.3), IN(0.3)

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, cx, fill, label) x4
    (4.676, 2.218, 3.689, WHITE, "Define the end-to-end (E2E) commercial maritime value chain, including current revenue potential and profitability "),
    (5.619, 2.696, 2.741, GRAY_1, "Assess demand for US-built ships under current and expected industrial policy (i.e., Jones Act status quo, SHIPS Act, other US-built markets)"),
    (5.619, 3.174, 2.745, GRAY_2, "Compare US shipbuilding costs vs. PRC / ROK / Japan under current and expected industrial policy"),
    (5.617, 4.13, 2.745, "C4DFEF", "Compare US-flagged vs. foreign-flagged vessel costs under current and expected industrial policy"),
]

_LABELS2 = [    # (x, y, cx, fill, label) x6
    (8.434, 6.042, 4.486, "0F2634", "Project OpCo financials given potential industrial policy and automation impact"),
    (3.738, 4.608, 1.804, "89C0DE", "Determine impact of automation on vessel opex and fuel costs"),
    (1.018, 5.086, 11.904, "4EA0CE", "Identify most attractive entry points in existing US-flagged market based on unit economics, incumbent fleet, competition, and our capabilities"),
    (8.434, 6.52, 4.486, BLACK, "Project ComboCo financials under different demand, subsidy, and automation scenarios"),
    (6.552, 3.652, 1.81, "808080", "Project ShipbuilderCo financials given US-built ship demand and shipyard subsidy scenarios"),
    (10.362, 5.564, 2.558, "163A4E", "Identify and assess attractiveness of alternative service models unlocked by automation (i.e., substitute ocean for trucking/rail)"),
]

_VALUE_LABELS = [    # (x, y, label) x10
    (4.315, 2.268, "1"),
    (5.279, 2.746, "2"),
    (5.279, 3.224, "3"),
    (6.22, 3.702, "4"),
    (5.279, 4.18, "5"),
    (3.406, 4.658, "6"),
    (0.668, 5.136, "7"),
    (10.012, 5.627, "8"),
    (8.087, 6.092, "9"),
    (8.087, 6.57, "10"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 10", IN(0.217), IN(1.372), IN(12.868), IN(5.547), col_widths=[IN(0.676), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938), IN(0.938)], rows=[
        trow([tcell("Week of:", size=PT(10), italic=True, color=BLACK, row_span=2, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": DK, "width": 12700}}), tcell("January", size=PT(10), bold=True, color=BLACK, align="ctr", grid_span=4, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": DK, "width": 12700}}), tcell("February", size=PT(10), bold=True, color=BLACK, align="ctr", grid_span=4, anchor="b", l_ins=60960, r_ins=60960, borders={"L": "none", "R": "none", "T": "none", "B": {"color": DK, "width": 12700}}), tcell("March", size=PT(10), bold=True, color=BLACK, align="ctr", grid_span=5, anchor="b", l_ins=60960, r_ins=60960, borders={"L": "none", "R": "none", "T": "none", "B": {"color": DK, "width": 12700}})], h=IN(0)),
        trow([tcell("1/5", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("1/12", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("1/19", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("1/26", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("2/2", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("2/9", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("2/16", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("2/23", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("3/2", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("3/9", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("3/16", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("3/23", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("3/30", size=PT(10), bold=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": "none", "T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0)),
        trow([tcell("Focus Areas", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", borders={"L": "none", "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": DK, "width": 12700}, "B": "none"}), tcell("", l_ins=60960, r_ins=60960, borders={"L": {"color": "808080", "width": 6350}, "R": "none", "T": {"color": DK, "width": 12700}, "B": "none"})], h=IN(4.947)),
    ]))
    out.append(breadcrumb("Commercial Strategy", "Research Overview"))
    out.append(title_placeholder("Project Calendar", "Initial effort to extend through end of March."))
    for _x, _y, _cx, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)])], fill=_fill, line_color=BLACK, anchor="ctr"))
    for _x, _y, _cx, _fill, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL2_H, [paragraph([run(_t, size=PT(8), color=WHITE, font=FONT)])], fill=_fill, line_color=BLACK, anchor="ctr"))
    for _x, _y, _t in _VALUE_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _VAL_W, _VAL_H, [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=BLACK, prst="ellipse", anchor="ctr", l_ins=0, r_ins=0))
    out.append(text_box(n(), "Rectangle 44", IN(9.334), IN(4.608), IN(3.75), IN(1.404), [paragraph([run("Foundational work conducted in initial effort – to test hypotheses in subsequent phases ", size=PT(10), bold=True, color="FB6B3C", font=FONT)], align="ctr")], fill=None, line_color="FB6B3C", line_width=19050, dashed_line=True))
    return "".join(out)


def render() -> str:
    return slide(_body())
