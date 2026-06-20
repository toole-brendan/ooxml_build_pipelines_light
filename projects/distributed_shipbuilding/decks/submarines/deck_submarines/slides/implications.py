"""implications - close with a work-type priority scorecard for diligence focus."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.style import *
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# --- chrome (unchanged from the original main module) ---
_SECTION = "Market Sizing"
_TOPIC = "Implications"
_TAKEAWAY = "Priority areas are electrical and power, structural fabrication, and piping"
_SOURCES = "Sources: (1) SAM.gov FFATA, FSRS, and Entity Management records; (2) GAO-25-106286; (3) HII and General Dynamics earnings calls"


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = BLACK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=BLACK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=BLACK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=BLACK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


_ROWS = [
    ["Bucket", "Avg TAM", "Addressability", "Qual. burden", "Evidence", "Pri."],
    ["Electrical and power", "$1,257M", "Medium", "High", "High", "1"],
    ["Structural fab and pre-outfit", "$625M", "High", "Med-high", "High", "2"],
    ["Piping, valves, and pumps", "$520M", "High", "High", "Med-high", "3"],
    ["Castings and forgings", "$143M", "Medium", "Very high", "Medium", "4"],
    ["Machining", "$98M", "High", "Medium", "Medium", "5"],
    ["Coatings and insulation", "$101M", "Medium", "High", "Medium", "6"],
    ["HVAC and ventilation", "$62M", "Medium", "Medium", "Medium", "7"],
]


def _body() -> str:
    out = []
    note_y = BODY_B - 320_000
    table_y = BODY_Y
    table_w = BODY_CX
    col_w = _widths(table_w, [3.7, 1.0, 1.25, 1.35, 1.0, 0.55])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=315_000)
    fills = {}
    bold = {}
    for r in [1, 2, 3]:
        for c in range(6):
            fills[(r, c)] = BLUE_1
        bold[(r, 5)] = True
    out.append(house_table(20, "PriorityScorecard", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="dark", size=900,
                           aligns=["l", "ctr", "ctr", "ctr", "ctr", "ctr"], cell_fills=fills, cell_bold=bold))
    out.append(_note(30, "ClosingNote", BODY_X, note_y, BODY_CX, 260_000,
        "Read: the scorecard is a diligence priority view, not SOM. Test supplier availability, qualification paths, capacity, concentration, and make-or-buy posture by bucket.",
        size=FINEPRINT_8_5PT, bold_lead="Read:", italic=True))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
