"""work_type_taxonomy - Define the seven component buckets used to translate TAM into serviceable component-manufacturing scenarios."""
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
    BODY_R,
    BODY_B,
    BLUE_1,
    GRAY_3,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_MESSAGE,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_BREADCRUMB_TOPIC = "Work-Type Taxonomy"
_TITLE_TOPIC = "Work-Type Taxonomy"
_TAKEAWAY = "Seven component buckets define the serviceable market"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

GAP = 91_440
NOTE_H = 360_000

_BUCKETS: list[tuple[str, str]] = [
    (
        "Structural fabrication and pre-outfit",
        "hull sections, fabricated structural metal, pre-outfit modules",
    ),
    (
        "Machining",
        "machine shops, precision machining, mechanical power transmission",
    ),
    (
        "Castings and forgings",
        "iron and steel forging, foundries, cast and forged components",
    ),
    (
        "Piping, valves, and pumps",
        "industrial valves, pumps, measuring and dispensing, pipe and fittings",
    ),
    (
        "Electrical and power",
        "switchgear, electronic components, propulsion-electronics, power distribution",
    ),
    (
        "HVAC and ventilation",
        "air-conditioning, heating, shipboard ventilation systems",
    ),
    (
        "Coatings and insulation",
        "rubber and synthetic products, composites, coatings and insulation",
    ),
]


def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP) -> tuple[list[int], int]:
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w


def _section_label(sp_id: int, y: int, text: str) -> str:
    return text_box(
        sp_id,
        "SectionLabel",
        BODY_X,
        y,
        int(BODY_CX * 0.70),
        190_000,
        [paragraph([run(text, size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _bucket_card(sp_id: int, x: int, y: int, cx: int, cy: int, title: str, definition: str) -> str:
    return text_box(
        sp_id,
        f"BucketCard {title}",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                align="ctr",
                space_after=100,
            ),
            paragraph(
                [run(definition, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
                align="ctr",
            ),
        ],
        fill=BLUE_1,
        line_color=GRAY_3,
        anchor="ctr",
        insets=INSETS_CARD,
    )


def _residual_card() -> str:
    return text_box(
        40,
        "ResidualCard",
        BODY_X,
        BODY_Y + 3_075_000,
        BODY_CX,
        645_000,
        [
            paragraph(
                [
                    run(
                        "Unbucketed / ambiguous residual: ",
                        size=DENSE_BODY_10PT,
                        bold=True,
                        color=BLACK,
                        font=FONT,
                    ),
                    run(
                        "visible vendor flow not confidently assigned to one of the seven buckets. Kept in TAM, excluded from broad component SAM.",
                        size=DENSE_BODY_10PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ],
                align="ctr",
            )
        ],
        fill=GRAY_3,
        line_color=BLACK,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )


def _method_note() -> str:
    return text_box(
        41,
        "MethodNote",
        BODY_X,
        BODY_B - NOTE_H,
        BODY_CX,
        NOTE_H,
        [
            paragraph(
                [
                    run(
                        "Mapped from FFATA-visible vendors using SAM.gov Entity Management NAICS and manual work-type evidence; NAICS is corporate-primary, not a per-action work description.",
                        size=FINEPRINT_8_5PT,
                        italic=True,
                        color=BLACK,
                        font=FONT,
                    )
                ],
                align="l",
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _body() -> str:
    top_row_y = BODY_Y + 405_000
    card_h = 830_000
    row_gap = 130_000
    row_1_x, row_1_w = _grid_x(4)
    row_2_x, row_2_w = _grid_x(3)

    parts: list[str] = []
    parts.append(_section_label(10, BODY_Y, "Included in broad component manufacturing"))
    for i, (title, definition) in enumerate(_BUCKETS[:4]):
        parts.append(_bucket_card(20 + i, row_1_x[i], top_row_y, row_1_w, card_h, title, definition))
    for i, (title, definition) in enumerate(_BUCKETS[4:]):
        parts.append(_bucket_card(30 + i, row_2_x[i], top_row_y + card_h + row_gap, row_2_w, card_h, title, definition))
    parts.append(_section_label(39, BODY_Y + 2_800_000, "Outside broad component SAM"))
    parts.append(_residual_card())
    parts.append(_method_note())
    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
