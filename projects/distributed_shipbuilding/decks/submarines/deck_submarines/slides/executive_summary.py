"""Executive summary - lead with average annual TAM and broad SAM and the key defensibility rules."""
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
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_ANSWER_CARD,
    CAP_12PT,
    ANSWER_KPI_24PT,
    RIBBON_KPI_18PT,
    DENSE_BODY_10PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
)
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Executive Summary"
_TITLE_TOPIC = "Executive Summary"
_TAKEAWAY = "Average annual opportunity is ~$3.3B TAM and ~$2.8B broad SAM"
_SOURCES = "Sources: U.S. Department of the Navy SCN Justification Books; U.S. DoD daily Contracts announcements; SAM.gov FFATA, FSRS, and Entity Management records"
GAP = 91_440
def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w
def _no_fill_text(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str, *, size: int, italic: bool = False) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=size, italic=italic, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _primary_card(
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
    fill: str,
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [
            paragraph([run(label, size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=120),
            paragraph([run(value, size=ANSWER_KPI_24PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=120),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT, italic=True, color=WHITE, font=FONT)], align="ctr"),
        ],
        fill=fill,
        line_width=19_050,
        anchor="ctr",
        insets=INSETS_ANSWER_CARD,
    )
def _secondary_card(
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
    fill: str,
    italic_qualifier: bool = False,
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [
            paragraph([run(label, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=65),
            paragraph([run(value, size=RIBBON_KPI_18PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=65),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT, italic=italic_qualifier, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=fill,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _commentary_rail(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    bullets: list[tuple[str, str]],
    *,
    title: str,
) -> str:
    paras = [
        paragraph(
            [run(title, size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)],
            space_after=160,
        )
    ]
    for idx, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120 if idx < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(137_160, 80_000, 137_160, 80_000),
    )
def _body() -> str:
    subtitle_y = BODY_Y + 20_000
    primary_y = BODY_Y + 300_000
    primary_h = 1_430_000
    secondary_y = BODY_Y + 1_950_000
    secondary_h = 860_000
    note_y = BODY_Y + 2_900_000
    note_h = 180_000
    rail_y = BODY_Y + 3_170_000
    rail_h = 1_170_000
    primary_xs, primary_w = _grid_x(2, gap=GAP)
    secondary_xs, secondary_w = _grid_x(4, gap=GAP)
    bullets = [
        ("Denominator:", "Basic Construction is the denominator; GFE and SIB are excluded."),
        ("Coefficient:", "strict, non-nuclear, BPMI-excluded, yard-excluded."),
        ("SAM:", "scenario menu only; no SOM, capture share, or win probability."),
        ("Cadence:", "annual flow is lumpy, with FY2024 and FY2027 peaks shown later."),
    ]
    return "".join([
        _no_fill_text(10, "SubtitleNote", BODY_X, subtitle_y, BODY_CX, 180_000, "FY2022-FY2027 model-period averages; not a commercial-style steady run-rate.", size=FINEPRINT_8_5PT, italic=True),
        _primary_card(20, "AverageAnnualTAMCard", primary_xs[0], primary_y, primary_w, primary_h, label="AVERAGE ANNUAL TAM", value="~$3.3B", qualifier="FY2022-FY2027 model-period average", fill=BLUE_5),
        _primary_card(21, "AverageAnnualBroadSAMCard", primary_xs[1], primary_y, primary_w, primary_h, label="AVERAGE ANNUAL BROAD SAM", value="~$2.8B", qualifier="Broad component manufacturing", fill=BLUE_4),
        _secondary_card(30, "CumulativeTAMCard", secondary_xs[0], secondary_y, secondary_w, secondary_h, label="Cumulative TAM", value="~$19.8B", qualifier="FY2022-FY2027", fill=BLUE_1),
        _secondary_card(31, "CumulativeBroadSAMCard", secondary_xs[1], secondary_y, secondary_w, secondary_h, label="Cumulative broad SAM", value="~$16.8B", qualifier="FY2022-FY2027", fill=BLUE_1),
        _secondary_card(32, "AppliedBCSupplierCoefficientCard", secondary_xs[2], secondary_y, secondary_w, secondary_h, label="Applied BC supplier coeff.", value="35.0%", qualifier="deliberately strict", fill=GRAY_1, italic_qualifier=True),
        _secondary_card(33, "APAndLLTMAdditiveBaseCard", secondary_xs[3], secondary_y, secondary_w, secondary_h, label="AP/LLTM additive base", value="$0", qualifier="no double count", fill=GRAY_2, italic_qualifier=True),
        _no_fill_text(40, "KPINote", BODY_X, note_y, BODY_CX, note_h, "Headline values are model-derived from budget base, POP coefficient, and SAM work-type allocation.", size=FINEPRINT_8_5PT, italic=True),
        _commentary_rail(50, "FindingsRail", BODY_X, rail_y, BODY_CX, rail_h, bullets, title="What makes the sizing conservative"),
    ])
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
