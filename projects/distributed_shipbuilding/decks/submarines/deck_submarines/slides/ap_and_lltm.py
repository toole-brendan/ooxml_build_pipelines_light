"""AP/LLTM - reconcile gross P-10 AP to a zero additive TAM base."""
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
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    CHART_TITLE_10PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    CAP_12PT,
    RIBBON_KPI_18PT,
)
from deck_core.charts import waterfall_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "AP/LLTM"
_TITLE_TOPIC = "AP/LLTM"
_TAKEAWAY = "Gross AP is large but contributes $0 additive TAM"
_SOURCES = "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10; (2) U.S. DoD daily Contracts announcements; (3) CRS RL32418 and CRS R41129"
_CHART = waterfall_chart(
    steps=[
        {"label": "Gross AP", "value": 44.709, "kind": "start"},
        {"label": "GFE design weapons", "value": -27.273, "kind": "delta"},
        {"label": "Inside BC", "value": -16.847, "kind": "delta"},
        {"label": "Overlap", "value": -0.589, "kind": "delta"},
        {"label": "Additive base", "value": None, "kind": "end"},
    ],
    title=None,
    value_axis_format='"$"0.0"B"',
    # SRT bar palette (docs/chart_conversion_spec.md).
    increase_color="486D82",
    decrease_color="A1A1A1",
    total_color="1D4D68",
    show_value_labels=False,
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    cat_label_size_pt=9,
    cat_header="Step",
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
def _waterfall_value(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str, *, color: str = BLACK) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=LABEL_9PT, bold=True, color=color, font=FONT)], align="ctr")],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _final_zero_tag(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "FinalZeroAdditiveTAMTag",
        x,
        y,
        cx,
        cy,
        [paragraph([run("$0 additive TAM", size=RIBBON_KPI_18PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5,
        anchor="ctr",
        insets=(80_000, 30_000, 80_000, 30_000),
    )
def _warning_card(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "DoNotAddP10APWarningCard",
        x,
        y,
        cx,
        cy,
        [
            paragraph([run("DO NOT ADD P-10 AP", size=CAP_12PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=100),
            paragraph(
                [
                    run("Double-counting risk: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Adding P-10 AP to P-5c Basic Construction would double count unless the model boundary is rebuilt.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            ),
        ],
        fill=GRAY_2,
        line_width=19_050,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _interpretation_note(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    paras = [
        paragraph([run("Interpretation", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)], space_after=150),
        paragraph(
            [
                run("Evidence: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                run("AP/LLTM are useful evidence of supplier-heavy purchasing.", size=LABEL_9PT, color=BLACK, font=FONT),
            ],
            bullet=True,
            space_after=115,
        ),
        paragraph(
            [
                run("Boundary: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                run("they are not additive market size under the current P-5c Basic Construction boundary.", size=LABEL_9PT, color=BLACK, font=FONT),
            ],
            bullet=True,
            space_after=115,
        ),
        paragraph(
            [
                run("Read: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                run("large does not mean additive.", size=LABEL_9PT, italic=True, color=BLACK, font=FONT),
            ],
            bullet=True,
        ),
    ]
    return text_box(
        sp_id,
        "APAndLLTMInterpretationNote",
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(100_000, 60_000, 90_000, 60_000),
    )
def _caption(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "APBoundaryCaption",
        x,
        y,
        cx,
        cy,
        [paragraph([run("Gross AP remains useful reference evidence; current boundary assigns zero additive TAM to AP/LLTM.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    chart_x = BODY_X
    chart_w = 7_240_000
    chart_title_y = BODY_Y + 40_000
    chart_y = BODY_Y + 265_000
    chart_h = 3_360_000
    right_x = BODY_X + chart_w + 450_000
    right_w = BODY_CX - chart_w - 450_000
    warning_y = BODY_Y + 310_000
    warning_h = 1_370_000
    note_y = BODY_Y + 1_900_000
    note_h = 1_230_000
    return "".join(
        [
            _chart_title(10, chart_x, chart_title_y, chart_w, "AP/LLTM reconciliation to additive TAM, $B"),
            graphic_frame(sp_id=20, name="APAndLLTMReconciliationWaterfallChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"),
            _waterfall_value(30, "GrossAPValueLabel", chart_x + 460_000, chart_y + 210_000, 1_150_000, 160_000, "$44.7B", color=BLACK),
            _waterfall_value(31, "GFEDesignWeaponsDecreaseLabel", chart_x + 2_070_000, chart_y + 1_390_000, 1_250_000, 160_000, "($27.3B)", color=BLACK),
            _waterfall_value(32, "AlreadyInsideBCDecreaseLabel", chart_x + 3_600_000, chart_y + 2_210_000, 1_250_000, 160_000, "($16.8B)", color=BLACK),
            _waterfall_value(33, "UnItemizedOverlapDecreaseLabel", chart_x + 5_030_000, chart_y + 2_740_000, 1_200_000, 160_000, "($0.6B)", color=BLACK),
            _final_zero_tag(34, chart_x + 5_260_000, chart_y + 2_940_000, 1_950_000, 430_000),
            _warning_card(40, right_x, warning_y, right_w, warning_h),
            _interpretation_note(50, right_x, note_y, right_w, note_h),
            _caption(60, chart_x, chart_y + chart_h + 160_000, chart_w, 190_000),
        ]
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
