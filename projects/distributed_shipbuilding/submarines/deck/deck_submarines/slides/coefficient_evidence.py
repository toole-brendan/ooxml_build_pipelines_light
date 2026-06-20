"""Coefficient Evidence - show POP coefficient views and the corpus discipline behind the strict headline coefficient."""
from __future__ import annotations
from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BLUE_2,
    BLUE_3,
    BLUE_5,
    GRAY_1,
    GRAY_3,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    CHART_TITLE_10PT,
    CONNECTOR_NOTE_8_5PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    VALUE_14PT,
)
from deck_core.charts import column_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Coefficient Evidence"
_TITLE_TOPIC = "Coefficient Evidence"
_TAKEAWAY = "POP data supports distributed production, but the headline coefficient remains strict"
_SOURCES = "Sources: (1) U.S. DoD daily Contracts announcements, July 2022-May 2026; (2) DoD Contracts releases dated April 30, 2025 and May 11, 2026; (3) GAO-25-106286"
# SRT bar palette (docs/chart_conversion_spec.md): the applied (strict) coefficient
# is the focal value (hero navy); the higher POP evidence views are neutral.
_CHART = column_chart(
    mode="ranked",
    categories=["POP anchor", "AP/LLTM ref", "Applied BC"],
    series=[
        {
            "name": "Coefficient view",
            "values": [0.518, 0.485, 0.350],
            "data_point_colors": ["79838F", "79838F", "1D4D68"],
        }
    ],
    title=None,
    show_legend=False,
    value_axis_format="0.0%",
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format="0.0%",
    value_label_size_pt=10,
    cat_label_size_pt=9,
    gap_width=80,
    cat_header="Coefficient view",
)
CHARTS = [_CHART]
def _chart_title(sp_id: int, x: int, y: int, cx: int, text: str) -> str:
    return text_box(
        sp_id,
        "ChartTitle",
        x,
        y,
        cx,
        150_000,
        [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _evidence_card(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    *,
    label: str,
    value: str,
    qualifier: str,
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [
            paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=45),
            paragraph([run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=45),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=GRAY_1,
        line_color=GRAY_3,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _chart_note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)], align="l")],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _headline_callout(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "CoefficientReadCallout",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Read: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Evidence supports a large distributed-production layer; the model applies a stricter coefficient.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                ],
                align="l",
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _guardrail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "CoefficientGuardrail",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Guardrail: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Higher POP views are explanatory and sensitivity views; they are not multiplied into headline TAM.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _body() -> str:
    chart_x = BODY_X
    chart_w = 6_250_000
    chart_title_y = BODY_Y + 45_000
    chart_y = BODY_Y + 270_000
    chart_h = 2_760_000
    right_x = BODY_X + chart_w + 410_000
    right_w = BODY_CX - chart_w - 410_000
    card_gap = 90_000
    card_w = (right_w - card_gap) // 2
    card_h = 790_000
    card_y = BODY_Y + 270_000
    row_gap = 115_000
    cards = [
        (30, "POPRowsCard", "POP rows", "658", "screened"),
        (31, "GatedActionsCard", "Gated TAM actions", "43", "TAM-relevant"),
        (32, "GatedCorpusCard", "Gated corpus", "$25.4B", "POP corpus"),
        (33, "InScopeNonGFECard", "In-scope non-GFE", "$19.3B", "screened value"),
        (34, "ConfirmationCoverageCard", "Confirmation", "100%", "of in-scope dollars"),
        (35, "UnparsedShareCard", "Unparsed share", "10.1%", "tracked limitation"),
    ]
    out = []
    out.append(_chart_title(10, chart_x, chart_title_y, chart_w, "Supplier coefficient evidence, %"))
    out.append(graphic_frame(sp_id=20, name="CoefficientEvidenceRankedBarChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"))
    # Notes now sit above their columns (chart is vertical): AP/LLTM ref = middle
    # column, Applied = right (shorter) column. Exact placement needs PowerPoint review.
    out.append(_chart_note(21, "APAndLLTMReferenceNote", chart_x + int(chart_w * 0.36), chart_y + 110_000, 1_500_000, 260_000, "Reference only; additive base = $0"))
    out.append(_chart_note(22, "AppliedCoefficientNote", chart_x + int(chart_w * 0.64), chart_y + 760_000, 1_500_000, 200_000, "Only input to headline TAM"))
    out.append(_headline_callout(23, chart_x, chart_y + chart_h + 140_000, chart_w, 420_000))
    for idx, (sp_id, name, label, value, qualifier) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        out.append(
            _evidence_card(
                sp_id,
                name,
                right_x + col * (card_w + card_gap),
                card_y + row * (card_h + row_gap),
                card_w,
                card_h,
                label=label,
                value=value,
                qualifier=qualifier,
            )
        )
    out.append(_guardrail(50, BODY_X, BODY_Y + 4_075_000, BODY_CX, 260_000))
    return "".join(out)
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
