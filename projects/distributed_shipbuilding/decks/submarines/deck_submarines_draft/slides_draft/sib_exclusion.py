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

from deck_core.text_metrics import estimate_row_heights

_SECTION = "Market sizing"
_TOPIC = "SIB exclusion"
_TAKEAWAY = "Capacity-development pass-throughs are material but outside component TAM"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) GAO-25-106286"

_ROWS = [
    ["Entity", "Amount $M", "Treatment", "Rationale"],
    ["BlueForge Alliance", "4,173.3", "Exclude", "Capacity development (nonprofit integrator)"],
    ["Training Modernization Group, Inc.", "77.0", "Exclude", "Workforce and training"],
    ["Institute for Advanced Learning and Research", "1.5", "Exclude", "Industrial-base support, applied R&D"],
    ["Total excluded SIB pass-throughs", "4,251.8", "Exclude", "Outside component TAM and SAM"],
]


def _body() -> str:
    out = []
    table_w = int(BODY_CX*0.62)
    table_y = BODY_Y + 300_000
    col_w = _widths(table_w, [2.8, 1.0, 1.1, 2.5])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, min_row_h=300_000)
    fills = {}
    colors = {}
    for c in range(4):
        fills[(0,c)] = GRAY_5; colors[(0,c)] = WHITE
        fills[(1,c)] = GRAY_2
        fills[(2,c)] = GRAY_1
        fills[(3,c)] = GRAY_1
        fills[(4,c)] = GRAY_5; colors[(4,c)] = WHITE
    bold = {(4,0): True, (4,1): True}
    out.append(house_table(20, "SIBLedger", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="rule", size=900,
                           aligns=["l", "r", "l", "l"], cell_fills=fills, cell_text_colors=colors, cell_bold=bold))
    right_x = BODY_X + table_w + GAP
    out.append(text_box(30, "Treatment", right_x, table_y, BODY_R-right_x, 1_520_000,
        [_txt("EXCLUDE FROM COMPONENT TAM AND SAM", size=CAP_12PT, bold=True, color=DK, align="ctr"),
         _txt("SIB dollars fund supplier development, workforce, capacity expansion, qualification, and infrastructure rather than current components delivered into a hull. Material to the industrial-base story, not additive component TAM.", size=MESSAGE_11PT, color=DK, align="ctr")],
        fill=GRAY_2, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(_note(40, "Total", BODY_X, table_y + sum(row_h) + 180_000, table_w, 260_000,
        "Total excluded SIB pass-throughs: ~$4,252M", size=MESSAGE_11PT, bold_lead="Total excluded SIB pass-throughs:", italic=False, align="l"))
    out.append(_note(50, "Terminology", BODY_X, BODY_B-310_000, BODY_CX, 240_000,
        "Deck standardizes on SIB (Submarine Industrial Base); earlier source files may use MIB (Maritime Industrial Base).",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
