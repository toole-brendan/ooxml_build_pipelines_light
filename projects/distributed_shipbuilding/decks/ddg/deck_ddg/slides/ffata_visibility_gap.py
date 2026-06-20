"""ffata_visibility_gap - Build the FFATA-visible versus estimated outsourcing comparison slide."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_1, BLUE_5, GRAY_1, GRAY_2, GRAY_3, GRAY_4,
    BLACK, FONT, INSETS_NONE, INSETS_MESSAGE,
    CHART_TITLE_10PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Visibility Gap"
_TAKEAWAY = "FFATA is evidence, not the market-size denominator"
_SOURCES = "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) HII and General Dynamics Form 10-K filings; (3) U.S. BLS OEWS, NAICS 336611"

GAP = 91_440
TITLE_H = 160_000
TITLE_GAP = 70_000
NOTE_H = 410_000

_CATEGORIES = [
    "Visible flow",
    "Outsourcing low",
    "Outsourcing mid",
    "Outsourcing high",
]
_VALUES = [2728.6, 11311.4, 13573.7, 16159.2]

# SRT bar palette (docs/chart_conversion_spec.md): the visible-flow column is the
# focal value (hero navy); the three outsourcing estimates are neutral context.
_CHART = column_chart(
    mode="clustered",
    categories=_CATEGORIES,
    series=[{"name": "Cumulative FY2016-FY2027", "values": _VALUES,
             "data_point_colors": ["1D4D68", "79838F", "79838F", "79838F"]}],
    title=None,
    show_legend=False,
    value_axis_format='"$"#,##0"M"',
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format='"$"#,##0"M"',
    value_label_size_pt=10,
    cat_label_size_pt=9,
    gap_width=80,
    cat_header="Measure",
)
CHARTS = [_CHART]


def _chart_title(text: str, x: int, y: int, cx: int, *, sp_id: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_H,
                    [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _explanation_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Direct material:", "purchased material booked as direct cost, not a subcontract."),
        ("Lower tiers:", "FFATA reaches only one tier below the prime."),
        ("Standing agreements:", "long-term supplier deals not subordinated to the prime."),
        ("Threshold and lag:", "sub-$30,000 actions and 12-30 month reporting lag."),
        ("Compliance:", "under-reporting, acute at BIW."),
    ]
    paras = [paragraph([run("Why visible is not the full market", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)], space_after=170)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph([
            run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(body, size=LABEL_9PT, color=BLACK, font=FONT),
        ], bullet=True, space_after=110 if i < len(bullets) - 1 else 0))
    return text_box(sp_id, "ExplanationRail", x, y, cx, cy, paras, fill=None, line_color=None,
                    anchor="t", insets=INSETS_MESSAGE)


def _pointer_callout(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
                     text: str, *, tip_x: int, tip_y: int) -> str:
    adj1 = round(((tip_x - (x + cx / 2)) / cx) * 100_000)
    adj2 = round(((tip_y - (y + cy / 2)) / cy) * 100_000)
    return text_box(sp_id, f"PointerCallout {name}", x, y, cx, cy,
                    [paragraph([run(text, size=DENSE_BODY_10PT, color=BLACK, font=FONT)], align="ctr")],
                    prst="wedgeRectCallout", geom_adj={"adj1": adj1, "adj2": adj2},
                    tx_box=False, fill=BLUE_1, line_color=GRAY_3, line_width=12_700,
                    anchor="ctr", insets=INSETS_MESSAGE)


def _body() -> str:
    chart_w = int(BODY_CX * 0.64)
    chart_x = BODY_X
    title_y = BODY_Y
    frame_y = BODY_Y + TITLE_H + TITLE_GAP
    note_y = BODY_B - NOTE_H
    frame_h = note_y - frame_y - 90_000
    rail_x = chart_x + chart_w + GAP
    rail_w = BODY_X + BODY_CX - rail_x

    title = _chart_title("Cumulative FFATA-visible flow vs estimated yard-side outsourcing, $M", chart_x, title_y, chart_w, sp_id=20)
    chart = graphic_frame(sp_id=21, name="FFATAVisibilityGapChart", x=chart_x, y=frame_y,
                          cx=chart_w, cy=frame_h, rId="rId2")
    rail = _explanation_rail(22, rail_x, frame_y, rail_w, 2_300_000)
    # Overlay points at the leftmost (visible-flow) column - short, near the axis.
    # Chart annotation, not a page callout; exact tip needs PowerPoint review.
    callout_x = chart_x + int(chart_w * 0.10)
    callout_y = frame_y + 90_000
    callout_w = int(chart_w * 0.46)
    callout_h = 560_000
    tip_x = chart_x + int(chart_w * 0.14)
    tip_y = frame_y + int(frame_h * 0.74)
    callout = _pointer_callout(23, "VisibleShare", callout_x, callout_y, callout_w, callout_h,
                               "Visible flow is ~20.1% of the midpoint estimate (cumulative basis).",
                               tip_x=tip_x, tip_y=tip_y)
    note = text_box(24, "EvidenceDenominatorNote", BODY_X, note_y, chart_w, NOTE_H,
                    [paragraph([run("FFATA provides public evidence of the supplier base; it does not capture the full true flow. Values are cumulative FY2016-FY2027.",
                                    size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="l")],
                    fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    return title + chart + rail + callout + note


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("FFATA Visibility Gap", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
