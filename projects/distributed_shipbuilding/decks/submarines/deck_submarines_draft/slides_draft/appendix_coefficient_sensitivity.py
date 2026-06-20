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
from deck_core.text_metrics import estimate_row_heights

_SECTION = "Appendix"
_TOPIC = "Coefficient sensitivity"
_TAKEAWAY = "The strict 35.0% supplier coefficient feeds TAM; broader POP views are sensitivity"
_SOURCES = "Sources: (1) U.S. DoD daily Contracts announcements; (2) GAO-25-106286; (3) FAR 52.204-10"

_CHART = bar_chart(
    mode="ranked",
    categories=["Distributed, incl. unparsed (78%)", "Outsourced band, high (65%)", "BC stream incl-GFE (61%)", "All-gated, GFE-excluded (54.5%)", "All-gated POP anchor (51.8%)", "Outsourced band, low (50%)", "AP and LLTM reference (48.5%)", "Applied non-nuclear supplier coefficient (35.0%)"],
    series=[{"name": "Coefficient view", "values": [0.780,0.650,0.610,0.545,0.518,0.500,0.485,0.350], "data_point_colors": [BLUE_2, BLUE_2, BLUE_2, BLUE_3, BLUE_3, BLUE_2, BLUE_2, BLUE_5]}],
    title=None, show_legend=False, value_axis_format="0%", show_gridlines=True,
    major_gridline_color=GRAY_1, major_gridline_width=3175, show_value_labels=True,
    value_label_format="0.0%", value_label_size_pt=9, cat_label_size_pt=9,
    gap_width=50, cat_header="Coefficient and place-of-performance view",
)
CHARTS = [_CHART]
_ROWS = [["Corpus control", "Value"], ["POP rows screened", "658"], ["Gated TAM-relevant actions", "43"], ["Gated POP corpus", "$25.4B"], ["In-scope non-GFE corpus", "$19.3B"], ["Confirmation coverage", "100%"], ["Unparsed share", "10.1%"]]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX*0.58)
    chart_y = BODY_Y + TITLE_BAND_H + 35_000
    guard_y = BODY_B - 460_000
    chart_h = guard_y - chart_y - 80_000
    out.append(_chart_title(10, "Supplier coefficient and place-of-performance views, percent of relevant corpus", BODY_X, BODY_Y, chart_w))
    out.append(graphic_frame(sp_id=20, name="SensitivityChart", x=BODY_X, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"))
    table_x = BODY_X + int(BODY_CX*0.62)
    col_w = _widths(BODY_R-table_x, [2.5, 1.0])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=280_000)
    out.append(house_table(30, "CorpusControls", table_x, BODY_Y, col_w, _ROWS, row_h=row_h, table_skin="rule", size=900, aligns=["l", "r"]))
    out.append(text_box(40, "Guardrail", BODY_X, guard_y, BODY_CX, 400_000,
        [paragraph([run("Only the strict 35.0% ", size=MESSAGE_11PT, bold=True, color=DK, font=FONT),
                    run("non-nuclear Basic Construction supplier coefficient feeds headline TAM; the broader place-of-performance views are sensitivity and evidence.", size=DENSE_BODY_10PT, color=DK, font=FONT)], align="ctr")],
        fill=GRAY_2, line_color=GRAY_3, insets=INSETS_MESSAGE, anchor="ctr"))
    return "".join(out)
