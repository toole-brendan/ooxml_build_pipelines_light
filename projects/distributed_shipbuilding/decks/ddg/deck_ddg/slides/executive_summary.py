"""Executive summary - answer-first KPI cards with a small native stream-split chart."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    BLACK, WHITE, FONT,
    INSETS_NONE, INSETS_ANSWER_CARD,
    FINEPRINT_8_5PT, DENSE_BODY_10PT, CHART_TITLE_10PT,
    MESSAGE_11PT, CAP_12PT, ANSWER_KPI_24PT,
)
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "TAM Answer"
_TAKEAWAY = "Supplier TAM averages ~$573M per year, with ~$327M in broad component SAM"
_SOURCES = "Sources: U.S. Navy FY2022–FY2027 SCN Justification Books, LI 2122; DoW DDG-51 contract announcements, July 2022–May 2026; SAM.gov Acquisition Subaward Reporting Public API"

# This slide is a KPI answer board; its slide-spec carries charts: []. The former
# stream-split chart was removed in the SRT chart-pattern conversion
# (docs/chart_conversion_spec.md) - the four KPI cards already carry the answer.
CHARTS: list[dict] = []
def _kpi_card(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    cap: str,
    value: str,
    qualifier: str,
    *,
    fill: str,
    color: str,
    focal: bool = False,
) -> str:
    return text_box(
        sp_id, "KPICard", x, y, cx, cy,
        [
            paragraph([run(cap, size=CAP_12PT, bold=True, color=color, font=FONT)], align="ctr", space_after=90),
            paragraph([run(value, size=ANSWER_KPI_24PT, bold=True, color=color, font=FONT)], align="ctr", space_after=80),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT, italic=True, color=color, font=FONT)], align="ctr"),
        ],
        fill=fill,
        line_width=19_050 if focal else 12_700,
        anchor="ctr",
        insets=INSETS_ANSWER_CARD,
    )
def _answer_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ([
            run("Supplier TAM: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("~$573M per year", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
            run(", or ~$3.44B across FY22–27.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
        ]),
        ([
            run("Broad component SAM: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("~$327M per year", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
            run(" and 57.1% of TAM.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
        ]),
        ([
            run("TAM build: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("Basic Construction supplier work plus AP/LLTM supplier material.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
        ]),
        ([
            run("SAM read: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("a work-type menu, not a probability-weighted capture forecast.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
        ]),
    ]
    paras = [
        paragraph(
            [run("Answer at a Glance", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
            space_after=130,
        )
    ]
    paras += [
        paragraph(runs, bullet=True, space_after=135 if i < len(bullets) - 1 else 0)
        for i, runs in enumerate(bullets)
    ]
    return text_box(
        sp_id, "AnswerRail", x, y, cx, cy, paras,
        fill=None, line_color=None, anchor="ctr", insets=(70_000, 20_000, 90_000, 20_000),
    )
def _sizing_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "SizingNote", x, y, cx, 270_000,
        [paragraph([run("Nominal $M per year; average annual FY22–27 unless noted. Cumulative FY22–27 values shown in parentheses. Excludes SOM and capture.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
def _body() -> str:
    left_x = BODY_X
    left_w = 4_620_000

    right_x = BODY_X + 4_920_000
    right_w = BODY_R - right_x

    gap = 120_000
    card_w = (right_w - gap) // 2
    card_h = 880_000
    row_gap = 120_000

    card_y1 = BODY_Y + 80_000
    card_y2 = card_y1 + card_h + row_gap
    # Left rail spans exactly the two-row KPI-card block, so its centered text
    # sits against the cards instead of drifting in an oversized invisible box.
    card_block_y = card_y1
    card_block_h = (card_y2 + card_h) - card_y1

    note_y = BODY_B - 380_000

    return (
        _answer_rail(10, left_x, card_block_y, left_w, card_block_h)
        + _kpi_card(20, right_x, card_y1, card_w, card_h, "SUPPLIER TAM", "~$573M", "per year ($3.44B FY22–27)", fill=BLUE_5, color=WHITE, focal=True)
        + _kpi_card(21, right_x + card_w + gap, card_y1, card_w, card_h, "BROAD SAM", "~$327M", "per year ($1.96B FY22–27)", fill=BLUE_4, color=WHITE)
        + _kpi_card(22, right_x, card_y2, card_w, card_h, "BROAD SAM SHARE", "57.1%", "of TAM", fill=BLUE_3, color=WHITE)
        + _kpi_card(23, right_x + card_w + gap, card_y2, card_w, card_h, "PER-HULL KPI", "~$265M", "per in-window hull", fill=BLUE_1, color=BLACK)
        + _sizing_note(40, right_x, note_y, right_w)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Executive Summary", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
