"""TAM Bridge - the arithmetic that turns the Basic Construction base into
cumulative and average-annual TAM.

Read it as a formula bridge, not a sourcing map: two inputs multiply into a
cumulative portfolio TAM, which is then divided by the six model years to give
the average-annual headline. The operator is a real mathMultiply shape, the
inputs merge through an orthogonal bus, and the divide-by-six step sits in its
own gap between the cumulative and final cards.
"""
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
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_R,
    BLUE_1,
    BLUE_2,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_3,
    GRAY_4,
    WHITE,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_ANSWER_CARD,
    CAP_12PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    RIBBON_KPI_18PT,
    ANSWER_KPI_24PT,
    HERO_32PT,
)

LAYOUT = "slideLayout4"

# Breadcrumb topic is a more specific variant of the visible title topic.
_SECTION = "Market Sizing"
_TOPIC = "TAM Bridge Calculation"
_TITLE_TOPIC = "TAM Bridge"
_TAKEAWAY = "Applying the strict 35.0% coefficient yields ~$3.3B average annual TAM"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA and FSRS records"

CONNECTOR_NORMAL = 12_700
MIN_ARROW_LEN = 250_000          # ~0.27in - below this, no arrowhead


def _card(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    *,
    cap: str,
    value: str,
    qualifier: str,
    fill: str,
    color: str,
    value_size: int,
    focal: bool = False,
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [
            paragraph([run(cap, size=CAP_12PT, bold=True, color=color, font=FONT)], align="ctr", space_after=80),
            paragraph([run(value, size=value_size, bold=True, color=color, font=FONT)], align="ctr", space_after=80),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT if not focal else LABEL_9PT, italic=not focal, color=color, font=FONT)], align="ctr"),
        ],
        fill=fill,
        line_width=19_050 if focal else 12_700,
        anchor="ctr",
        insets=INSETS_ANSWER_CARD if focal else INSETS_CARD,
    )


def _multiply_symbol(sp_id: int, x: int, y: int, size: int) -> str:
    """The arithmetic operator as a real mathMultiply AutoShape (a symbol, not a
    typed glyph). No text - default insets keep it clear of the inset floor."""
    return text_box(
        sp_id,
        "MathMultiplyOperator",
        x,
        y,
        size,
        size,
        [paragraph([])],
        fill=BLACK,
        line_color=BLACK,
        line_width=12_700,
        anchor="ctr",
        prst="mathMultiply",
        tx_box=False,
    )


def _operator_caption(sp_id: int, x: int, y: int, cx: int) -> str:
    """Quiet italic caption under the operator - same treatment as a connector
    note (no fill, no border)."""
    return text_box(
        sp_id,
        "MultiplyOperatorCaption",
        x,
        y,
        cx,
        140_000,
        [paragraph([run("multiplied by", size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )


def _vline(
    sp_id: int,
    name: str,
    x: int,
    y1: int,
    y2: int,
    *,
    arrow: bool = True,
    color: str = GRAY_4,
    width: int = CONNECTOR_NORMAL,
) -> str:
    return connector(
        sp_id,
        name,
        x,
        y1,
        0,
        y2 - y1,
        color=color,
        width=width,
        arrow=arrow and abs(y2 - y1) >= MIN_ARROW_LEN,
    )


def _hline(
    sp_id: int,
    name: str,
    x1: int,
    x2: int,
    y: int,
    *,
    color: str = GRAY_4,
    width: int = CONNECTOR_NORMAL,
) -> str:
    return connector(
        sp_id,
        name,
        x1,
        y,
        x2 - x1,
        0,
        color=color,
        width=width,
        arrow=False,
    )


def _connector_note(sp_id: int, x: int, y: int, cx: int, cy: int, text: str) -> str:
    return text_box(
        sp_id,
        "DivideBySixConnectorNote",
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )


def _secondary_bridge(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "SecondaryBridgeStrip",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Subtraction check: ", size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT),
                    run("$56.647B BC base minus ", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                    run("$36.807B", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(" prime, co-prime, and excluded share equals ", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                    run("$19.840B TAM", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(".", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=GRAY_1,
        line_color=GRAY_3,
        anchor="ctr",
        insets=(160_000, 50_000, 160_000, 50_000),
    )


def _guardrail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "StrictCoefficientGuardrail",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Guardrail: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Only the strict 35.0% BC coefficient feeds headline TAM; broader POP views are sensitivity.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
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
    input_w = 3_450_000
    input_h = 880_000
    input_y = BODY_Y + 290_000
    left_x = BODY_X + 680_000
    right_x = BODY_R - 680_000 - input_w
    center_x = BODY_X + BODY_CX // 2

    left_center = left_x + input_w // 2
    right_center = right_x + input_w // 2

    cum_w = 4_700_000
    cum_h = 840_000
    cum_x = center_x - cum_w // 2
    cum_y = BODY_Y + 1_560_000        # raised so the divide step gets real space
    cum_center = cum_x + cum_w // 2

    final_w = 5_200_000
    final_h = 1_060_000
    final_x = center_x - final_w // 2
    final_y = BODY_Y + 2_660_000      # lowered to open the cumulative-to-final gap

    # Bottom band trimmed slightly to absorb the lowered final card.
    strip_y = BODY_Y + 3_800_000
    strip_h = 360_000
    guard_y = BODY_Y + 4_220_000
    guard_h = 210_000

    # Operator: mathMultiply symbol centered between the inputs at value height,
    # with the quiet caption just below it.
    op_size = 340_000
    op_x = center_x - op_size // 2
    op_y = input_y + input_h // 2 - op_size // 2
    cap_w = 1_400_000
    cap_x = center_x - cap_w // 2
    cap_y = op_y + op_size + 20_000

    # Merge bus: short input drops -> horizontal bus -> one arrow into cum TAM.
    # +140_000 keeps the bus-to-cum drop at the 250_000 arrow floor.
    merge_y = input_y + input_h + 140_000

    # Divide-by-six step lives in the real gap below the cumulative card.
    divide_gap_y = cum_y + cum_h
    divide_note_y = divide_gap_y + (final_y - divide_gap_y - 150_000) // 2

    cards = [
        _card(20, "BasicConstructionBaseCard", left_x, input_y, input_w, input_h,
              cap="BASIC CONSTRUCTION BASE", value="$56.647B", qualifier="FY2022-FY2027 P-5c",
              fill=BLUE_1, color=BLACK, value_size=RIBBON_KPI_18PT),
        _multiply_symbol(21, op_x, op_y, op_size),
        _card(22, "AppliedBCSupplierCoefficientCard", right_x, input_y, input_w, input_h,
              cap="APPLIED BC SUPPLIER COEFFICIENT", value="35.0%", qualifier="strict, non-nuclear, yard-excluded",
              fill=BLUE_4, color=WHITE, value_size=RIBBON_KPI_18PT),
        _card(30, "CumulativePortfolioTAMCard", cum_x, cum_y, cum_w, cum_h,
              cap="CUMULATIVE PORTFOLIO TAM", value="$19.840B", qualifier="FY2022-FY2027",
              fill=BLUE_2, color=BLACK, value_size=ANSWER_KPI_24PT),
        _card(40, "AverageAnnualTAMCard", final_x, final_y, final_w, final_h,
              cap="AVERAGE ANNUAL TAM", value="~$3.307B", qualifier="FY2022-FY2027 model-period average",
              fill=BLUE_5, color=WHITE, value_size=HERO_32PT, focal=True),
    ]

    connectors = [
        _vline(10, "BCInputDropToMergeBus", left_center, input_y + input_h, merge_y, arrow=False),
        _vline(11, "CoefficientInputDropToMergeBus", right_center, input_y + input_h, merge_y, arrow=False),
        _hline(12, "InputMergeBus", left_center, right_center, merge_y),
        _vline(13, "MergeBusToCumulativeTAM", cum_center, merge_y, cum_y),
        _vline(14, "CumulativeToAverageAnnualTAM", center_x, cum_y + cum_h, final_y),
    ]

    labels = [
        _operator_caption(23, cap_x, cap_y, cap_w),
        _connector_note(31, center_x + 190_000, divide_note_y, 1_450_000, 150_000, "divide by 6 years"),
    ]

    strip = _secondary_bridge(50, BODY_X, strip_y, BODY_CX, strip_h)
    guardrail = _guardrail(60, BODY_X, guard_y, BODY_CX, guard_h)

    return "".join(cards + connectors + labels + [strip, guardrail])


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
