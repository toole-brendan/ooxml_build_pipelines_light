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

_SECTION = "Appendix"
_TOPIC = "AP and LLTM detail"
_TAKEAWAY = "Gross P-10 reference flow reconciles to a $0 additive base"
_SOURCES = "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10; (2) U.S. DoD daily Contracts announcements; (3) CRS RL32418"

_ROWS = [
    ["Step", "Value $B", "Treatment", "Model reason"],
    ["Gross P-10 AP top-line", "44.709", "Reference", "Authoritative AP total, Va and Col"],
    ["Less GFE, design, and weapons", "(27.273)", "Exclude", "Nuclear, electronics, ordnance, missile, plans - outside boundary"],
    ["Less already inside Basic Construction", "(16.847)", "Exclude overlap", "Shipbuilder-procured, CFE, EOQ, HM&E, propulsor"],
    ["Less un-itemized overlap", "(0.589)", "Reconcile", "Early-Virginia top-line over named detail"],
    ["Additive AP and LLTM base", "0.000", "Final", "Do not add to TAM"],
]


def _body() -> str:
    out = []
    left_w = int(BODY_CX*0.70)
    out.append(_note(10, "Formula", BODY_X, BODY_Y, left_w, 260_000,
        "$44.709B gross P-10 AP, less exclusions and overlap, equals $0.000B additive base.",
        size=MESSAGE_11PT, italic=False, align="l"))
    table_y = BODY_Y + 350_000
    col_w = _widths(left_w, [2.8, 1.0, 1.4, 2.4])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=310_000)
    fills = {}
    colors = {}
    for c in range(4):
        fills[(1,c)] = BLUE_1
        fills[(2,c)] = GRAY_1
        fills[(3,c)] = GRAY_2
        fills[(4,c)] = GRAY_1
        fills[(5,c)] = BLUE_5; colors[(5,c)] = WHITE
    bold = {(1,1): True, (5,0): True, (5,1): True, (5,2): True, (5,3): True}
    out.append(house_table(20, "APReconciliation", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="rule", size=900,
                           aligns=["l", "r", "l", "l"], cell_fills=fills, cell_text_colors=colors, cell_bold=bold))
    right_x = BODY_X + left_w + GAP
    right_w = BODY_R - right_x
    out.append(text_box(30, "Warning", right_x, BODY_Y, right_w, 1_150_000,
        [_txt("DO NOT ADD P-10 AP", size=CAP_12PT, bold=True, color=DK, align="ctr"),
         _txt("Adding P-10 AP to P-5c Basic Construction would double count unless the model boundary is rebuilt.", size=MESSAGE_11PT, color=DK, align="ctr")],
        fill=GRAY_2, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    paras = [
        _line("Evidence:", "AP and LLTM show a large, supplier-heavy purchasing cadence years ahead of construction.", lead_size=DENSE_BODY_10PT, body_size=LABEL_9PT, bullet=True),
        _line("Boundary:", "under this model AP and LLTM are reference evidence, not additive TAM.", lead_size=DENSE_BODY_10PT, body_size=LABEL_9PT, bullet=True),
    ]
    out.append(text_box(31, "Interpretation", right_x, BODY_Y+1_330_000, right_w, 1_100_000, paras,
                        fill=None, line_color=None, insets=INSETS_NONE, anchor="t"))
    return "".join(out)
