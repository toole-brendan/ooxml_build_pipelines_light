"""AP/LLTM sensitivity - show second-stream build, exclusions, and AP knob sensitivity."""
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
    house_table,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_B,
    BLUE_1,
    BLUE_5,
    GRAY_1,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
)
from deck_core.text_metrics import estimate_row_heights
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "AP/LLTM"
_TAKEAWAY = "The second stream contributes ~36% of portfolio TAM"
_SOURCES = (
    "Sources: U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; "
    "CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; "
    "NAVSEA, DDG 51 FY23-27 MYP award release, Aug. 1, 2023"
)
GAP = 300_000
_LEFT_W = 6_200_000
_RIGHT_X = BODY_X + _LEFT_W + GAP
_RIGHT_W = BODY_X + BODY_CX - _RIGHT_X
_LEFT_Y = BODY_Y + 80_000
_MATRIX_TITLE_Y = BODY_Y + 80_000
_MATRIX_Y = _MATRIX_TITLE_Y + 260_000
_AP_ROWS = [
    ["Step", "Cum $M", "Avg $M per year", "Share or coefficient", "Treatment"],
    ["CY Advance Procurement", "1,833.2", "305.5", "n.a.", "starting AP base"],
    ["Ship-construction share", "1,466.6", "244.4", "80.0%", "non-GFE share"],
    ["AP/LLTM supplier coefficient", "n.a.", "n.a.", "85.0%", "input knob"],
    ["AP/LLTM stream TAM", "1,246.6", "207.8", "applied", "contributes 36.3% of TAM"],
]
_AP_COL_W = [2_100_000, 1_070_000, 1_180_000, 1_160_000, 690_000]
_AP_ROW_H = estimate_row_heights(_AP_ROWS, _AP_COL_W, size_pt=9.0, header_size_pt=9.0)
_AP_TABLE_H = sum(_AP_ROW_H)
_CUE_Y = _LEFT_Y + _AP_TABLE_H + 220_000
_SIZING_Y = BODY_B - 250_000
_MATRIX_ROWS = [
    ["Ship-construction share", "75% AP coeff.", "85% AP coeff.", "95% AP coeff."],
    ["70%", "~$962M", "~$1,091M", "~$1,219M"],
    ["80%", "~$1,100M", "~$1,247M", "~$1,393M"],
    ["90%", "~$1,237M", "~$1,403M", "~$1,568M"],
]
_MATRIX_COL_W = [1_360_000, 1_140_000, 1_140_000, _RIGHT_W - 3_640_000]
_MATRIX_ROW_H = estimate_row_heights(_MATRIX_ROWS, _MATRIX_COL_W, size_pt=9.0, header_size_pt=9.0)
# Left AP-stream build -> dark skin (the one primary table here); the final
# "AP/LLTM stream TAM" row is the dark answer band, coefficient rows (2, 3)
# muted GRAY_1. (Replaces the old hand-rolled fills + focal bottom rule.)
_AP_OUTPUT = len(_AP_ROWS) - 1
_AP_CELL_FILLS = {(ri, ci): GRAY_1 for ri in (2, 3) for ci in range(len(_AP_COL_W))}
_AP_CELL_FILLS.update({(_AP_OUTPUT, ci): BLUE_5 for ci in range(len(_AP_COL_W))})
_AP_CELL_TEXT_COLORS = {(_AP_OUTPUT, ci): WHITE for ci in range(len(_AP_COL_W))}
_AP_CELL_BOLD = {(_AP_OUTPUT, ci): True for ci in range(len(_AP_COL_W))}
# Right sensitivity matrix -> light skin (dense crosspoints). The row-label
# column keeps a GRAY_1 fill; the 80% / 85%-coeff. crosspoint is the focal cell.
_MATRIX_FOCAL = (2, 2)
_MATRIX_CELL_FILLS = {(ri, 0): GRAY_1 for ri in range(1, len(_MATRIX_ROWS))}
_MATRIX_CELL_FILLS[_MATRIX_FOCAL] = BLUE_1
_MATRIX_CELL_BOLD = {_MATRIX_FOCAL: True}
def _ap_build_table() -> str:
    return house_table(
        20,
        "APStreamBuildTable",
        BODY_X,
        _LEFT_Y,
        _AP_COL_W,
        _AP_ROWS,
        row_h=_AP_ROW_H,
        table_skin="dark",
        aligns=["l", "r", "r", "ctr", "l"],
        size=LABEL_9PT,
        cell_fills=_AP_CELL_FILLS,
        cell_text_colors=_AP_CELL_TEXT_COLORS,
        cell_bold=_AP_CELL_BOLD,
    )
def _matrix_table() -> str:
    return house_table(
        50,
        "APSensitivityMatrix",
        _RIGHT_X,
        _MATRIX_Y,
        _MATRIX_COL_W,
        _MATRIX_ROWS,
        row_h=_MATRIX_ROW_H,
        table_skin="light",
        aligns=["ctr", "ctr", "ctr", "ctr"],
        size=LABEL_9PT,
        cell_fills=_MATRIX_CELL_FILLS,
        cell_bold=_MATRIX_CELL_BOLD,
    )
def _line_treatment_cue() -> str:
    return text_box(
        70,
        "LineLevelTreatmentCue",
        BODY_X,
        _CUE_Y,
        _LEFT_W,
        1_650_000,
        [
            paragraph(
                [
                    run("INCLUDE: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("Ship Construction EOQ and supplier-addressable long-lead material.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120,
            ),
            paragraph(
                [
                    run("EXCLUDE: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("Aegis Weapon System EOQ; Other GFE; VLS, weapons, and ordnance AP; WPN and OPN-funded flows.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120,
            ),
            paragraph(
                [
                    run("ALREADY IN BC: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("Power Conversion Modules moved into Basic Construction in FY23.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
            ),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    matrix_title = text_box(
        40,
        "SensitivityMatrixTitle",
        _RIGHT_X,
        _MATRIX_TITLE_Y,
        _RIGHT_W,
        170_000,
        [paragraph([run("AP/LLTM cumulative TAM sensitivity, $M", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    sizing_note = text_box(
        90,
        "SizingNote",
        BODY_X,
        _SIZING_Y,
        BODY_CX,
        220_000,
        [
            paragraph(
                [
                    run(
                        "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture.",
                        size=FINEPRINT_8_5PT,
                        italic=True,
                        color=BLACK,
                        font=FONT,
                    )
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    return _ap_build_table() + matrix_title + _matrix_table() + _line_treatment_cue() + sizing_note
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
