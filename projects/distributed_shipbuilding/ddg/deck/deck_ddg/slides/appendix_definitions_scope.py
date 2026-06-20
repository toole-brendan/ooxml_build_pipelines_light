"""Definitions and scope - clarify which denominators are evidence, context, TAM, and SAM."""
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
    GRAY_1,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    LABEL_9PT,
    CHART_TITLE_10PT,
    DENSE_BODY_10PT,
)
from deck_core.text_metrics import estimate_row_heights
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "Definitions"
_TAKEAWAY = "Four denominators need to stay separate"
_SOURCES = (
    "Sources: CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; "
    "U.S. Navy FY2027 SCN Justification Book, LI 2122; FAR 52.204-10 and 48 C.F.R. Part 45"
)
_BREADCRUMB_TOPIC = "Definitions and Scope"
_ROWS = [
    ["Denominator", "Definition", "Included examples", "Excluded examples", "Where used"],
    [
        "Total ship cost",
        "P-5c Total Ship Estimate by procurement year",
        "Basic Construction; Electronics; Ordnance; Plans; HM&E; Other",
        "WPN missiles; OPN sustainment",
        "Cost funnel context only",
    ],
    [
        "SCN LI 2122",
        "DDG-51 Class Destroyer line item in Navy SCN budget books",
        "DDG-51 Flight III new construction",
        "DDG-1000, cruiser modernization, sustainment, depot repair",
        "Scope gate and production schedule",
    ],
    [
        "Basic Construction base",
        "Construction layer flowing through BIW and Ingalls prime contracts",
        "Yard work and yard-side supplier work",
        "Navy-procured Aegis, SPY-6, Mk 41, Mk 45, LM2500, SEWIP",
        "BC stream TAM",
    ],
    [
        "AP/LLTM base",
        "Advance procurement and long-lead material considered supplier-addressable",
        "Ship Construction EOQ and long-lead material after non-GFE filter",
        "Aegis Weapon System EOQ, Other GFE, VLS and weapons AP",
        "AP/LLTM stream TAM",
    ],
    [
        "FFATA-visible flow",
        "First-tier subawards reported to FSRS and surfaced through SAM.gov",
        "Reportable subcontracts above the reporting threshold",
        "Direct material purchases, lower-tier subcontracts, standing agreements, sub-threshold long tail",
        "Evidence, bucket rules, supplier landscape",
    ],
    [
        "Supplier-addressable TAM",
        "BC stream plus AP/LLTM stream after supplier coefficients",
        "Non-GFE new-construction supplier work away from prime yards and excluded flows",
        "GFE, weapons, sustainment, MIB, design-only, SOM",
        "Headline market size",
    ],
    [
        "SAM scenarios",
        "Work-type bucket menus selected from TAM",
        "Broad component, metal, electrical, modular, HM&E scenarios",
        "Unbucketed residual unless later classified; capture probability",
        "Target-market menu, not a forecast",
    ],
]
_COL_W = [2_050_000, 2_260_000, 2_520_000, 2_580_000, 1_872_362]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, header_size_pt=9.0)
_TABLE_Y = BODY_Y + 240_000
_TABLE_H = sum(_ROW_H)
_BOUNDARY_Y = min(_TABLE_Y + _TABLE_H + 110_000, BODY_B - 455_000)
# Dense definitions/crosswalk ledger -> light skin. Row highlights kept via
# cell_fills / cell_bold: BLUE_1 first column, the FFATA-visible row (5) muted
# GRAY_1, and the supplier-addressable TAM row (6) emphasized BLUE_1 + bold.
def _ledger_cell_maps():
    cell_fills: dict[tuple[int, int], str] = {}
    cell_bold: dict[tuple[int, int], bool] = {}
    for ri in range(1, len(_ROWS)):
        cell_fills[(ri, 0)] = BLUE_1
    for ci in range(len(_COL_W)):
        cell_fills[(5, ci)] = GRAY_1
        cell_fills[(6, ci)] = BLUE_1
        cell_bold[(6, ci)] = True
    return cell_fills, cell_bold
def _ledger_table() -> str:
    cell_fills, cell_bold = _ledger_cell_maps()
    return house_table(
        20,
        "DenominatorLedger",
        BODY_X,
        _TABLE_Y,
        _COL_W,
        _ROWS,
        row_h=_ROW_H,
        table_skin="light",
        aligns=["l", "l", "l", "l", "l"],
        size=LABEL_9PT,
        cell_fills=cell_fills,
        cell_bold=cell_bold,
    )
def _body() -> str:
    label = text_box(
        10,
        "ExhibitTitle",
        BODY_X,
        BODY_Y,
        BODY_CX,
        150_000,
        [
            paragraph(
                [run("Denominator ledger", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)],
                align="l",
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    boundary = text_box(
        11,
        "BoundaryCommentary",
        BODY_X + 5_650_000,
        _BOUNDARY_Y,
        BODY_CX - 5_650_000,
        500_000,
        [
            paragraph(
                [
                    run("Boundary: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(
                        "The deck keeps GFE-heavy prime flows visible as context, but excludes them from non-GFE TAM.",
                        size=LABEL_9PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ],
                align="l",
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_MESSAGE,
    )
    return label + _ledger_table() + boundary
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
