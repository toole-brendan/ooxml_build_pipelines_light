"""coefficient_sensitivity - compare POP-derived coefficient views with the strict applied input."""
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
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_EVIDENCE,
    INSETS_MESSAGE,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
    MESSAGE_11PT,
    VALUE_14PT,
)
from deck_core.charts import column_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "Coefficient Sensitivity"
_TAKEAWAY = "Higher POP views are evidence, not the headline input"
_SOURCES = "Sources: (1) U.S. DoD daily Contracts announcements; (2) GAO-25-106286; (3) FAR 52.204-10"
# SRT bar palette (docs/chart_conversion_spec.md): the applied (strict) coefficient
# is the focal value (hero navy); the higher POP evidence views are neutral.
_CHART = column_chart(
    mode="ranked",
    categories=["POP anchor", "AP/LLTM ref", "Applied BC"],
    series=[
        {
            "name": "Supplier coefficient",
            "values": [0.518, 0.485, 0.350],
            "data_point_colors": ["79838F", "79838F", "1D4D68"],
        }
    ],
    title=None,
    show_legend=False,
    value_axis_format="0%",
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
CHARTS: list[dict] = [_CHART]
_CHART_X = BODY_X
_CHART_Y = BODY_Y + 280_000
_CHART_W = 6_520_000
_CHART_H = 3_050_000
_RIGHT_X = BODY_X + _CHART_W + 280_000
_RIGHT_W = BODY_CX - _CHART_W - 280_000
_CARD_GAP = 100_000
_CARD_W = (_RIGHT_W - _CARD_GAP) // 2
_CARD_H = 560_000
_CARD_Y = BODY_Y + 180_000
_GUARD_Y = BODY_Y + 3_620_000
_GUARD_H = 620_000
def _chart_title() -> str:
    return text_box(
        10,
        "ChartTitle",
        _CHART_X,
        BODY_Y,
        _CHART_W,
        170_000,
        [paragraph([run("Supplier coefficient views, percent", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _evidence_card(sp_id: int, x: int, y: int, value: str, label: str, *, fill: str = GRAY_1) -> str:
    return text_box(
        sp_id,
        "EvidenceCard",
        x,
        y,
        _CARD_W,
        _CARD_H,
        [
            paragraph([run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=35),
            paragraph([run(label, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=fill,
        anchor="ctr",
        insets=INSETS_EVIDENCE,
    )
def _evidence_grid() -> str:
    cards = [
        ("658", "POP rows screened", GRAY_1),
        ("43", "Gated TAM-relevant actions", GRAY_1),
        ("$25.4B", "Gated POP corpus", BLUE_1),
        ("$19.3B", "In-scope non-GFE corpus", BLUE_1),
        ("100%", "Confirmation coverage", GRAY_1),
        ("10.1%", "Unparsed share", GRAY_1),
    ]
    parts: list[str] = []
    for i, (value, label, fill) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = _RIGHT_X + col * (_CARD_W + _CARD_GAP)
        y = _CARD_Y + row * (_CARD_H + _CARD_GAP)
        parts.append(_evidence_card(30 + i, x, y, value, label, fill=fill))
    return "".join(parts)
def _chart_notes() -> str:
    return text_box(
        20,
        "AppliedCoefficientNote",
        _CHART_X,
        _CHART_Y + _CHART_H + 55_000,
        _CHART_W,
        300_000,
        [
            paragraph(
                [
                    run("Applied BC supplier: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("only coefficient multiplied into headline TAM.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _guardrail() -> str:
    return text_box(
        50,
        "CoefficientGuardrail",
        BODY_X,
        _GUARD_Y,
        BODY_CX,
        _GUARD_H,
        [
            paragraph(
                [
                    run("Guardrail: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("only the strict 35.0% Basic Construction supplier coefficient feeds headline TAM; ", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                    run("higher POP views are sensitivity and evidence.", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=GRAY_2,
        line_width=19_050,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    return (
        _chart_title()
        + graphic_frame(sp_id=11, name="CoefficientSensitivityChart", x=_CHART_X, y=_CHART_Y, cx=_CHART_W, cy=_CHART_H, rId="rId2")
        + _chart_notes()
        + _evidence_grid()
        + _guardrail()
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
