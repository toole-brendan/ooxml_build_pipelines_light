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

from deck_core.charts import waterfall_chart, graphic_frame

_SECTION = "Market sizing"
_TOPIC = "AP and LLTM"
_TAKEAWAY = "Gross AP is large but contributes $0 additive TAM"
_SOURCES = "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10; (2) U.S. DoD daily Contracts announcements; (3) CRS RL32418 and CRS R41129"

_CHART = waterfall_chart(
    steps=[
        {"label": "Gross AP top-line", "value": 44.709, "kind": "start"},
        {"label": "GFE design and weapons", "value": -27.273, "kind": "delta"},
        {"label": "Already inside BC", "value": -16.847, "kind": "delta"},
        {"label": "Unitemized overlap", "value": -0.589, "kind": "delta"},
        {"label": "Additive base", "value": 0.000, "kind": "end"},
    ],
    title=None, value_axis_format='"$"0.0"B"', show_value_labels=False, cat_header="Step",
    show_gridlines=True, major_gridline_color=GRAY_1, major_gridline_width=3175, cat_label_size_pt=9,
)
CHARTS = [_CHART]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX * 0.68)
    chart_y = BODY_Y + TITLE_BAND_H + 40_000
    note_y = BODY_B - 320_000
    chart_h = note_y - chart_y - 80_000
    out.append(_chart_title(10, "P-10 AP and LLTM bridge to additive TAM base, FY2022-FY2027, $B", BODY_X, BODY_Y, chart_w))
    out.append(graphic_frame(sp_id=20, name="APWaterfall", x=BODY_X, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"))
    right_x = BODY_X + chart_w + GAP
    right_w = BODY_R - right_x
    out.append(text_box(30, "Warning", right_x, chart_y, right_w, 1_250_000,
        [paragraph([run("$0 additive base. ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
                    run("Do not add P-10 AP to P-5c Basic Construction. P-10 is timing and reference evidence unless the model boundary is rebuilt.", size=DENSE_BODY_10PT, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(text_box(31, "Interpretation", right_x, chart_y+1_420_000, right_w, 700_000,
        [_txt("AP and LLTM are useful evidence of supplier-heavy purchasing, but not additive market size in the headline model.",
              size=DENSE_BODY_10PT, color=DK, align="l")],
        fill=None, line_color=None, insets=INSETS_NONE, anchor="t"))
    out.append(text_box(32, "Endpoint", BODY_X+int(chart_w*0.73), chart_y+int(chart_h*0.58), 1_700_000, 350_000,
        [_txt("$0 additive base", size=VALUE_14PT, bold=True, color=DK, align="ctr")],
        fill=None, line_color=None, insets=INSETS_NONE, anchor="ctr"))
    out.append(_note(40, "ScopeGuardrail", BODY_X, note_y, BODY_CX, 260_000,
        "Large does not mean additive. Adding P-10 AP to P-5c Basic Construction would double count unless the whole boundary changes.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
