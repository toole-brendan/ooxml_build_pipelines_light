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

from deck_core.charts import bar_chart, graphic_frame

_SECTION = "Market sizing"
_TOPIC = "Bucket TAM"
_TAKEAWAY = "Electrical and power, structural fabrication, and piping lead the opportunity"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

_CHART = bar_chart(
    mode="ranked",
    categories=[
        "Electrical and power (38.0%)",
        "Structural fabrication and pre-outfit (18.9%)",
        "Piping, valves, and pumps (15.7%)",
        "Castings and forgings (4.3%)",
        "Coatings and insulation (3.1%)",
        "Machining (3.0%)",
        "HVAC and ventilation (1.9%)",
    ],
    series=[{"name": "Average annual TAM", "values": [1257.1, 624.5, 519.6, 142.8, 101.5, 98.1, 61.9],
             "data_point_colors": [BLUE_5, BLUE_4, BLUE_3, BLUE_1, BLUE_1, BLUE_1, BLUE_1]}],
    title=None, show_legend=False, value_axis_format='"$"#,##0"M"',
    show_gridlines=True, major_gridline_color=GRAY_1, major_gridline_width=3175,
    show_value_labels=True, value_label_format='"$"#,##0"M"', value_label_size_pt=9,
    cat_label_size_pt=9, gap_width=40, cat_header="Work-type bucket",
)
CHARTS = [_CHART]


def _body() -> str:
    out = []
    chart_y = BODY_Y + TITLE_BAND_H + 30_000
    chart_h = 2_700_000
    out.append(_chart_title(10, "Average annual TAM by work-type bucket, FY2022-FY2027", BODY_X, BODY_Y, BODY_CX))
    out.append(graphic_frame(sp_id=20, name="BucketTAMChart", x=BODY_X, y=chart_y, cx=int(BODY_CX*0.88), cy=chart_h, rId="rId2"))
    res_y = chart_y + chart_h + 220_000
    out.append(text_box(30, "ResidualStrip", BODY_X, res_y, BODY_CX, 580_000,
        [paragraph([run("Unbucketed / ambiguous residual: ", size=MESSAGE_11PT, bold=True, color=DK, font=FONT),
                    run("~$501M per year (~$3.01B cumulative). Tracked in TAM, excluded from broad component SAM.", size=DENSE_BODY_10PT, color=DK, font=FONT)], align="ctr")],
        fill=GRAY_3, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(_note(40, "Note", BODY_X, BODY_B-310_000, BODY_CX, 240_000,
        "Values are average annual FY2022-FY2027; cumulative shown for context. Average annual is not a run-rate.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
