"""Cost funnel - native ranked bar chart and no-fill commentary rail for DDG-51 Basic Construction denominator."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R,
    BLUE_5, GRAY_1, GRAY_2, GRAY_4,
    BLACK, WHITE, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_CHIP,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CHART_TITLE_10PT,
    MESSAGE_11PT, VALUE_14PT,
)
from deck_core.charts import waterfall_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Cost Funnel"
_TAKEAWAY = "Basic Construction is the supplier-addressable base after excluding GFE-heavy cost categories"
_SOURCES = "Sources: U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c; CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; 48 C.F.R. Part 45 and section 52.245-1"
# Decreasing waterfall: total ship estimate ($5,492M) narrows to the
# supplier-addressable Basic Construction base ($3,322M) by removing GFE-heavy
# and other cost categories. SRT bar palette (docs/chart_conversion_spec.md):
# total pillars hero navy, excluded steps gray.
_CHART = waterfall_chart(
    steps=[
        {"label": "Total ship", "value": 5492, "kind": "start"},
        {"label": "Less GFE", "value": -1807, "kind": "delta"},
        {"label": "Less other", "value": -363, "kind": "delta"},
        {"label": "Basic Construction", "value": None, "kind": "end"},
    ],
    title=None,
    value_axis_format='"$"#,##0"M"',
    increase_color="486D82",
    decrease_color="A1A1A1",
    total_color="1D4D68",
    show_value_labels=True,
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    cat_label_size_pt=9,
    cat_header="Step",
)
CHARTS: list[dict] = [_CHART]
def _chart_title(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ChartTitle", x, y, cx, 150_000,
        [paragraph([run("FY24 DDG-51 cost categories, both ships", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
def _denominator_reference(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "DenominatorReference", x, y, cx, 250_000,
        [
            paragraph(
                [
                    run("Total Ship Estimate: ", size=LABEL_9PT, italic=True, color=BLACK, font=FONT),
                    run("~$5,492M", size=VALUE_14PT, bold=True, color=BLACK, font=FONT),
                    run(" denominator reference", size=LABEL_9PT, italic=True, color=BLACK, font=FONT),
                ]
            )
        ],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
def _scope_chip(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ScopeBoundaryChip", x, y, cx, 430_000,
        [paragraph([run("Total ship cost is not supplier TAM.", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
        fill=GRAY_2, anchor="ctr", insets=INSETS_CHIP,
    )
def _commentary_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Basic Construction:", "largest cost category and the starting base for the BC supplier stream."),
        ("GFE-heavy categories:", "Electronics and Ordnance are excluded from the non-GFE supplier TAM."),
        ("Next step:", "correct the supplier coefficient before applying it to the Basic Construction base."),
    ]
    paras = []
    for i, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=135 if i < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id, "CommentaryRail", x, y, cx, cy,
        paras, fill=None, line_color=None, anchor="t", insets=(60_000, 20_000, 20_000, 20_000),
    )
def _granular_caption(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "GranularCaption", x, y, cx, 190_000,
        [paragraph([run("Plans $83M | Change Orders $92M | HM&E $101M | Other Cost $88M", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
def _body() -> str:
    chart_x = BODY_X + 20_000
    chart_w = 7_330_000
    rail_x = BODY_X + 7_720_000
    rail_w = BODY_R - rail_x
    title_y = BODY_Y + 50_000
    denom_y = title_y + 210_000
    rule_y = denom_y + 250_000
    chart_y = rule_y + 120_000
    chart_h = 2_760_000
    caption_y = chart_y + chart_h + 170_000
    chip_y = BODY_Y + 280_000
    rail_y = chip_y + 610_000
    rail_h = 2_160_000
    return (
        _chart_title(10, chart_x, title_y, chart_w)
        + _denominator_reference(11, chart_x, denom_y, chart_w)
        + connector(12, "DenominatorRule", chart_x, rule_y, chart_w, 0, color=GRAY_4, width=6_350)
        + graphic_frame(sp_id=20, name="CostFunnelChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2")
        + _granular_caption(30, chart_x, caption_y, chart_w)
        + _scope_chip(40, rail_x, chip_y, rail_w)
        + _commentary_rail(41, rail_x, rail_y, rail_w, rail_h)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Cost Funnel", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
