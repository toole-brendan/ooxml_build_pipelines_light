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

from deck_core.charts import column_chart, graphic_frame

_SECTION = "Market sizing"
_TOPIC = "Budget denominator"
_TAKEAWAY = "The FY2022-FY2027 denominator averages ~$9.4B annually"
_SOURCES = "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-5c; (2) CRS RL32418; (3) CRS R41129"

_CHART = column_chart(
    mode="stacked",
    categories=["FY22", "FY23", "FY24", "FY25", "FY26", "FY27"],
    series=[
        {"name": "Virginia", "values": [4.758, 5.095, 9.071, 5.327, 3.137, 8.889], "color": BLUE_4},
        {"name": "Columbia", "values": [0.000, 0.000, 6.356, 0.000, 7.160, 6.854], "color": BLUE_2,
         "label_colors": [WHITE, WHITE, DK, WHITE, DK, DK]},
    ],
    title=None, show_legend=True, legend_pos="b", value_axis_format='"$"0.0"B"',
    show_gridlines=True, major_gridline_color=GRAY_1, major_gridline_width=3175,
    show_value_labels=True, value_label_format='"$"0.0"B"', value_label_size_pt=9,
    cat_label_size_pt=9, gap_width=90, cat_header="FY",
)
CHARTS = [_CHART]


def _body() -> str:
    out = []
    chart_x, title_y = BODY_X, BODY_Y
    chart_w = int(BODY_CX * 0.70)
    chart_y = BODY_Y + TITLE_BAND_H + 40_000
    note_y = BODY_B - 320_000
    chart_h = note_y - chart_y - 70_000
    out.append(_chart_title(10, "Basic Construction by fiscal year and class, $B", chart_x, title_y, chart_w))
    out.append(graphic_frame(sp_id=20, name="BasicConstructionChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"))
    rail_x = chart_x + chart_w + GAP
    paras = [_txt("How to read the denominator", size=LABEL_9PT, bold=True, italic=True, color=DK, align="l")]
    for lead, body in [
        ("Total:", "FY2022-FY2027 Basic Construction totals ~$56.6B."),
        ("Average:", "the denominator averages ~$9.4B annually across six years."),
        ("Cadence:", "FY2024 and FY2027 are peak years when both classes contribute."),
        ("Scope:", "BC includes yards, team-build work, purchased material, first-tier subs, and lower-tier flow."),
    ]:
        paras.append(_line(lead, body, lead_size=DENSE_BODY_10PT, body_size=LABEL_9PT, bullet=True, space_after=100))
    out.append(text_box(30, "Rail", rail_x, chart_y, BODY_R-rail_x, 1_600_000, paras,
                        fill=None, line_color=None, insets=INSETS_NONE, anchor="t"))
    out.append(_note(40, "FY2024Peak", chart_x + int(chart_w*0.38), chart_y + 80_000, 1_800_000, 300_000,
        "FY2024 peak, Virginia and Columbia Basic Construction", size=CONNECTOR_NOTE_8_5PT, italic=True))
    out.append(connector(41, "PeakLeader2024", chart_x + int(chart_w*0.47), chart_y+370_000, 0, 470_000, color=BLACK, width=6_350, arrow=True))
    out.append(_note(42, "FY2027Peak", chart_x + int(chart_w*0.72), chart_y + 80_000, 1_900_000, 300_000,
        "FY2027 peak, two-boat Virginia plus Columbia", size=CONNECTOR_NOTE_8_5PT, italic=True))
    out.append(connector(43, "PeakLeader2027", chart_x + int(chart_w*0.84), chart_y+370_000, 0, 470_000, color=BLACK, width=6_350, arrow=True))
    out.append(_note(50, "UnitNote", BODY_X, note_y, chart_w, 260_000,
        "AP-only Columbia years contribute no Basic Construction to this denominator. Average annual BC is a six-year average, not a smooth run-rate.",
        size=FINEPRINT_8_5PT, italic=True, align="l"))
    return "".join(out)
