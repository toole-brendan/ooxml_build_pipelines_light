"""visible_suppliers - Show the largest FFATA-visible suppliers and frame the named list as a visible floor."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.style import *
from deck_core.charts import bar_chart, graphic_frame
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

GAP = 91_440
TITLE_BAND_H = 190_000

# --- chrome (unchanged from the original main module) ---
_SECTION = "Market Sizing"
_BREADCRUMB_TOPIC = "Visible Suppliers"
_TITLE_TOPIC = "Visible Suppliers"
_TAKEAWAY = "The named vendor base is broad but anchored by a few large suppliers"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"


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


def _chart_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_BAND_H,
                    [_txt(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, align="l")],
                    fill=None, line_color=None, insets=INSETS_NONE, anchor="t")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


_CHART = bar_chart(
    mode="ranked",
    categories=["Northrop Grumman Corporation", "Leonardo SpA", "Curtiss-Wright Electro-Mechanical Corp.", "Scot Forge Company", "ESCO Technologies Inc.", "DC Fabricators Inc.", "Rhoads Metal Fabrications, Inc.", "Curtiss-Wright Corporation", "The Graham Corporation", "Austal USA, LLC"],
    series=[{"name": "Visible subaward $M", "values": [1426.6, 490.6, 198.0, 197.5, 188.5, 162.9, 141.9, 110.8, 89.1, 87.6],
             # SRT bar palette (docs/chart_conversion_spec.md): top supplier hero
             # navy, blue ramp down, neutral gray-blue tail. Kept horizontal -
             # 10 long supplier names do not fit a vertical column axis.
             "data_point_colors": ["1D4D68", "486D82", "89A2B0", "89A2B0", "89A2B0", "AFC2CC", "79838F", "79838F", "79838F", "79838F"]}],
    title=None, show_legend=False, value_axis_format='"$"#,##0"M"', show_gridlines=True,
    major_gridline_color=GRAY_1, major_gridline_width=3175, show_value_labels=True,
    value_label_format='"$"#,##0"M"', value_label_size_pt=9, cat_label_size_pt=9,
    gap_width=35, cat_header="Supplier (parent)",
)
CHARTS = [_CHART]
_ROWS = [["Visible-supplier evidence", "Value"], ["Classified subaward recipients", "150"], ["Supplier-addressable visible value", "~$5.46B"], ["Broader FFATA-visible parents", "~759"]]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX*0.64)
    chart_y = BODY_Y + TITLE_BAND_H + 30_000
    note_y = BODY_B - 320_000
    chart_h = note_y - chart_y - 90_000
    out.append(_chart_title(10, "Top 10 FFATA-visible suppliers, cumulative subaward value FY2016-FY2026", BODY_X, BODY_Y, chart_w))
    out.append(graphic_frame(sp_id=20, name="VisibleSuppliersChart", x=BODY_X, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"))
    table_x = BODY_X + chart_w + GAP
    col_w = _widths(BODY_R-table_x, [2.6, 1.0])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, min_row_h=280_000)
    out.append(house_table(30, "EvidenceTable", table_x, chart_y, col_w, _ROWS, row_h=row_h, table_skin="rule", size=900, aligns=["l", "r"]))
    out.append(_note(35, "ReadNote", table_x, chart_y + sum(row_h) + 120_000, BODY_R-table_x, 360_000,
        "Read: the ranked names are the top of a visible first-tier floor, not a complete supplier universe or target list.",
        size=FINEPRINT_8_5PT, bold_lead="Read:", italic=True, align="l"))
    out.append(_note(40, "FloorNote", BODY_X, note_y, BODY_CX, 260_000,
        "Parent-normalized where SAM.gov Entity data supports the relationship. Visible value is a floor: FFATA misses purchased material, lower-tier subcontracts, long-term agreements, and most HII Newport News team-build work.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
