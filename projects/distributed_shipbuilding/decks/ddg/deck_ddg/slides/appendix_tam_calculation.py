"""TAM calculation - reconcile FY22-27 cumulative supplier TAM to the average annual headline."""
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
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_B,
    BLUE_1,
    BLUE_5,
    GRAY_1,
    WHITE,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    MESSAGE_11PT,
    CAP_12PT,
    VALUE_14PT,
)
from deck_core.text_metrics import estimate_row_heights
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "TAM Detail"
_TAKEAWAY = "The annual headline reconciles to the FY22-27 cumulative model"
_SOURCES = (
    "Sources: U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; "
    "DoW DDG-51 contract announcements, July 2022-May 2026; "
    "SAM.gov Acquisition Subaward Reporting Public API"
)
_BREADCRUMB_TOPIC = "TAM Calculation"
GAP = 91_440
_TABLE_W = 7_720_000
_RIGHT_X = BODY_X + _TABLE_W + 250_000
_RIGHT_W = BODY_X + BODY_CX - _RIGHT_X
_TABLE_Y = BODY_Y + 400_000
_ROWS = [
    ["Step", "FY22-27 cumulative $M", "Average annual $M per year", "Applied coefficient or share", "Note"],
    ["Basic Construction base", "17,471.0", "2,911.8", "n.a.", "P-5c BC base"],
    ["MYP-corrected supplier coefficient", "n.a.", "n.a.", "12.5%", "Other-US and foreign POP over non-GFE BC corpus"],
    ["BC-stream supplier TAM", "2,192.0", "365.3", "applied", "Base times coefficient"],
    ["CY AP in-window", "1,833.2", "305.5", "n.a.", "FY25-27 AP base"],
    ["Ship-construction share of CY AP", "1,466.6", "244.4", "80.0%", "Non-GFE share"],
    ["AP/LLTM supplier coefficient", "n.a.", "n.a.", "85.0%", "Input knob"],
    ["AP/LLTM stream TAM", "1,246.6", "207.8", "applied", "Second stream"],
    ["Portfolio supplier TAM", "3,438.6", "573.1", "n.a.", "Headline TAM"],
    ["Average annual convention", "n.a.", "573.1", "divide by six", "Six-year average, not run-rate"],
]
_COL_W = [2_350_000, 1_250_000, 1_380_000, 1_350_000, 1_390_000]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, header_size_pt=9.0)
_TABLE_H = sum(_ROW_H)
_KPI_Y = min(_TABLE_Y + _TABLE_H + 115_000, BODY_B - 855_000)
_SIZING_Y = min(_KPI_Y + 575_000, BODY_B - 230_000)
# Reconciliation evidence -> rule skin so the header stays light; the Portfolio
# supplier TAM row (8) is the lone dark BLUE_5 answer band. Coefficient /
# convention rows (2, 6, 9) muted GRAY_1; stream-TAM rows (3, 7) BLUE_1 + bold.
def _reconciliation_cell_maps():
    cell_fills: dict[tuple[int, int], str] = {}
    cell_text_colors: dict[tuple[int, int], str] = {}
    cell_bold: dict[tuple[int, int], bool] = {}
    for ri in (2, 6, 9):
        for ci in range(len(_COL_W)):
            cell_fills[(ri, ci)] = GRAY_1
    for ri in (3, 7):
        for ci in range(len(_COL_W)):
            cell_fills[(ri, ci)] = BLUE_1
            cell_bold[(ri, ci)] = True
    for ci in range(len(_COL_W)):
        cell_fills[(8, ci)] = BLUE_5
        cell_text_colors[(8, ci)] = WHITE
        cell_bold[(8, ci)] = True
    return cell_fills, cell_text_colors, cell_bold
def _reconciliation_table() -> str:
    cell_fills, cell_text_colors, cell_bold = _reconciliation_cell_maps()
    return house_table(
        20,
        "TAMReconciliationTable",
        BODY_X,
        _TABLE_Y,
        _COL_W,
        _ROWS,
        row_h=_ROW_H,
        table_skin="rule",
        aligns=["l", "r", "r", "ctr", "l"],
        size=LABEL_9PT,
        cell_fills=cell_fills,
        cell_text_colors=cell_text_colors,
        cell_bold=cell_bold,
    )
def _bridge() -> str:
    x, y, w = _RIGHT_X, _TABLE_Y, _RIGHT_W
    h = 3_105_000
    pad = 150_000
    parts = [
        text_box(
            60,
            "MiniBridgeContainer",
            x,
            y,
            w,
            h,
            [paragraph([])],
            fill=GRAY_1,
            anchor="t",
            insets=INSETS_CARD,
        ),
        text_box(
            61,
            "BridgeCap",
            x + pad,
            y + 120_000,
            w - 2 * pad,
            270_000,
            [paragraph([run("CUMULATIVE BRIDGE", size=CAP_12PT, bold=True, color=BLACK, font=FONT)], align="l")],
            fill=None,
            line_color=None,
            anchor="t",
            insets=INSETS_NONE,
        ),
    ]
    rows = [
        ("BC-stream supplier TAM", "~$2.19B", "cumulative"),
        ("AP/LLTM stream TAM", "~$1.25B", "cumulative"),
        ("Portfolio supplier TAM", "~$3.44B", "cumulative"),
    ]
    row_y = y + 500_000
    for i, (label, value, note) in enumerate(rows):
        parts.append(
            text_box(
                62 + i,
                f"BridgeRow{i+1}",
                x + pad,
                row_y + i * 480_000,
                w - 2 * pad,
                390_000,
                [
                    paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)]),
                    paragraph(
                        [
                            run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT),
                            run(f"  {note}", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT),
                        ]
                    ),
                ],
                fill=None,
                line_color=None,
                anchor="t",
                insets=INSETS_NONE,
            )
        )
    parts.append(connector(70, "BridgeDividerRule", x + pad, y + 2_035_000, w - 2 * pad, 0, color=BLACK, width=9_525))
    parts.append(
        text_box(
            71,
            "BridgeAnnualBand",
            x + pad,
            y + 2_190_000,
            w - 2 * pad,
            730_000,
            [
                paragraph([run("Average annual headline", size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
                paragraph([run("~$573M per year", size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
                paragraph([run("Divide by 6 fiscal years", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr"),
            ],
            fill=BLUE_1,
            anchor="ctr",
            insets=INSETS_CARD,
        )
    )
    return "".join(parts)
def _kpi_chip(sp_id: int, x: int, y: int, cx: int, label: str, value: str) -> str:
    return text_box(
        sp_id,
        "KPIChip",
        x,
        y,
        cx,
        460_000,
        [
            paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
            paragraph([run(value, size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=BLUE_1,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _kpi_strip() -> str:
    chip_w = (_TABLE_W - 2 * GAP) // 3
    return (
        _kpi_chip(80, BODY_X, _KPI_Y, chip_w, "In-window hulls", "13")
        + _kpi_chip(81, BODY_X + chip_w + GAP, _KPI_Y, chip_w, "Supplier TAM per in-window hull", "~$265M")
        + _kpi_chip(82, BODY_X + 2 * (chip_w + GAP), _KPI_Y, chip_w, "BC TAM per in-window hull", "~$169M")
    )
def _body() -> str:
    header_note = text_box(
        10,
        "HeaderNote",
        BODY_X,
        BODY_Y,
        BODY_CX,
        260_000,
        [
            paragraph(
                [
                    run("Average annual convention: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run(
                        "FY22-27 cumulative values are divided by six; they are not a steady run-rate.",
                        size=LABEL_9PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ]
            )
        ],
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
        210_000,
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
    return header_note + _reconciliation_table() + _bridge() + _kpi_strip() + sizing_note
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
