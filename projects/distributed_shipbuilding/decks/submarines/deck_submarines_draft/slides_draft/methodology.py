from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector,
)
from deck_core.style import *

LAYOUT = "slideLayout4"

GAP = 91_440
TITLE_BAND_H = 190_000
NOTE_H = 360_000
CAVEAT_H = 520_000


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = DK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _line(lead: str, body: str = "", *, lead_size: int = DENSE_BODY_10PT,
          body_size: int = LABEL_9PT, lead_color: str = DK, body_color: str = DK,
          align: str = "l", space_after: int = 0, bullet: bool = False,
          italic_body: bool = False) -> str:
    runs = [run(lead, size=lead_size, bold=True, color=lead_color, font=FONT)]
    if body:
        runs.append(run(" " + body, size=body_size, italic=italic_body, color=body_color, font=FONT))
    return paragraph(runs, align=align, space_after=space_after, bullet=bullet)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=DK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=DK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=DK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _card(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, title: str,
          lines: list[str], *, fill: str = BLUE_1, color: str = DK,
          line_color=GRAY_3, line_width: int = 12_700,
          title_size: int = CAP_12PT, body_size: int = DENSE_BODY_10PT,
          title_align: str = "ctr", body_bullets: bool = False,
          insets=INSETS_CARD, anchor: str = "t") -> str:
    paras = [_txt(title, size=title_size, bold=True, color=color, align=title_align)]
    for i, line in enumerate(lines):
        paras.append(_txt(line, size=body_size, color=color, align="l"))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor=anchor)


def _kpi(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
         label: str, value: str, qualifier: str, *, fill: str, color: str,
         line_color=BLACK, line_width: int = 19_050, value_size: int = HERO_32PT,
         label_size: int = CAP_12PT, qualifier_size: int = LABEL_9PT,
         insets=INSETS_ANSWER_CARD) -> str:
    paras = [
        _txt(label, size=label_size, bold=True, color=color, align="ctr"),
        _txt(value, size=value_size, bold=True, color=color, align="ctr"),
        _txt(qualifier, size=qualifier_size, italic=True, color=color, align="ctr"),
    ]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor="ctr")


def _chart_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_BAND_H,
                    [_txt(text, size=CHART_TITLE_10PT, italic=True, color=DK, align="l")],
                    fill=None, line_color=None, insets=INSETS_NONE, anchor="t")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    w = (total - (n - 1) * gap) // n
    return [start + i * (w + gap) for i in range(n)], w


def _grid_y(n: int, *, start: int = BODY_Y, total: int = BODY_CY, gap: int = GAP):
    h = (total - (n - 1) * gap) // n
    return [start + i * (h + gap) for i in range(n)], h


def _render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )

render = _render


_SECTION = "TAM Build"
_TOPIC = "Methodology"
_TAKEAWAY = "TAM is built from Basic Construction, supplier coefficients, and work-type allocation"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA/FSRS and Entity Management records"


def _dot(sp_id, x, y, n, fill, color):
    d = 330_000
    return text_box(sp_id, "StepDot", x-d//2, y-d//2, d, d,
                    [_txt(str(n), size=LABEL_9PT, bold=True, color=color, align="ctr")],
                    fill=fill, line_color=BLACK if fill==DK else GRAY_3, insets=INSETS_NONE,
                    prst="ellipse", anchor="ctr")


def _body() -> str:
    out = []
    out.append(_note(10, "Thesis", BODY_X, BODY_Y, BODY_CX, 230_000,
        "The headline model is intentionally simple; complexity is handled in the evidence and exclusions.",
        size=FINEPRINT_8_5PT, italic=True))
    axis_y = BODY_Y + 780_000
    left = BODY_X + 500_000
    right = BODY_R - 500_000
    out.append(connector(20, "ProcessAxis", left, axis_y, right-left, 0, color=BLACK, width=12_700, arrow=True))
    steps = [
        (1, "Build budget base", "P-5c Basic Construction; P-10 AP and LLTM reference"),
        (2, "Remove non-addressable", "GFE, BPMI, SIB, yards, design-only, depot"),
        (3, "Apply supplier coefficient", "POP evidence; strict 35.0% feeds headline TAM"),
        (4, "Calculate portfolio TAM", "Basic Construction base times coefficient; AP and LLTM base is $0"),
        (5, "Allocate work-type buckets", "FFATA, FSRS, SAM.gov entity data, NAICS mapping"),
        (6, "Apply scenario flags", "Bucket inclusion menus; SAM scenario, not SOM"),
        (7, "Output SAM menu", "Broad, electrical, metal, modular, HM&E; no SOM"),
    ]
    for i, (n, title, body) in enumerate(steps):
        x = left + int((right-left)*(0.03 + i*0.94/6))
        fill = DK if n == 3 else BLUE_1
        color = WHITE if n == 3 else DK
        out.append(_dot(30+i, x, axis_y, n, fill, color))
        out.append(text_box(40+i, "StepLabel", x-610_000, axis_y+260_000, 1_220_000, 650_000,
            [_txt(title, size=LABEL_9PT, bold=True, color=DK, align="ctr"),
             _txt(body, size=FINEPRINT_8_5PT, color=DK, align="ctr")],
            fill=None, line_color=None, insets=INSETS_NONE, anchor="t"))
    formula_y = BODY_Y + 2_520_000
    formula_w = 7_550_000
    out.append(text_box(60, "FormulaBox", BODY_X, formula_y, formula_w, 1_310_000,
        [_txt("AVERAGE ANNUAL TAM", size=CAP_12PT, bold=True, color=DK, align="ctr"),
         _txt("$56.647B × 35.0% = ~$19.840B cumulative TAM", size=RIBBON_KPI_18PT, bold=True, color=DK, align="ctr"),
         _txt("over 6 years = ~$3.307B average annual", size=MESSAGE_11PT, color=DK, align="ctr")],
        fill=BLUE_1, line_color=BLACK, line_width=19_050, insets=INSETS_ANSWER_CARD, anchor="ctr"))
    rail_x = BODY_X + formula_w + GAP
    out.append(_card(70, "ScopeNotes", rail_x, formula_y, BODY_R-rail_x, 1_310_000,
        "Scope notes", [
            "AP and LLTM gross is reference evidence; additive base is $0.",
            "SAM scenarios are bucket inclusion menus; no SOM or win-probability haircut.",
            "Detailed coefficient evidence belongs on the coefficient slide.",
        ], fill=GRAY_1, title_size=LABEL_9PT, body_size=LABEL_9PT, title_align="l"))
    out.append(_note(80, "NoSOM", BODY_X, BODY_B-330_000, BODY_CX, 260_000,
        "Method note: SAM is a scenario menu, not SOM, capture share, win probability, or company revenue forecast.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
