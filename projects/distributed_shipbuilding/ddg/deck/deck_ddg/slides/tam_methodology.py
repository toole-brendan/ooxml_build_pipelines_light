"""TAM methodology - shape-built two-stream equation and guardrail."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_3, BLUE_4, BLUE_5, GRAY_4,
    BLACK, WHITE, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_MESSAGE, INSETS_ANSWER_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, MESSAGE_11PT, BODY_12PT, CAP_12PT,
    VALUE_14PT, ANSWER_KPI_24PT,
)
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Method"
_TAKEAWAY = "TAM combines Basic Construction supplier work with AP/LLTM supplier material"
_SOURCES = "Sources: U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; DoW DDG-51 contract announcements, July 2022-May 2026; SAM.gov Acquisition Subaward Reporting Public API"
_SIZING_NOTE = "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
_CONNECTOR_W = 9_525
def _equation_banner(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id, "HeroEquationBanner", x, y, cx, cy,
        [
            paragraph(
                [
                    run("Supplier TAM is ", size=BODY_12PT, color=WHITE, font=FONT),
                    run("Basic Construction base", size=BODY_12PT, bold=True, color=WHITE, font=FONT),
                    run(" times ", size=BODY_12PT, color=WHITE, font=FONT),
                    run("MYP-corrected supplier coefficient", size=BODY_12PT, bold=True, color=WHITE, font=FONT),
                    run(" plus ", size=BODY_12PT, color=WHITE, font=FONT),
                    run("AP/LLTM base", size=BODY_12PT, bold=True, color=WHITE, font=FONT),
                    run(" times ", size=BODY_12PT, color=WHITE, font=FONT),
                    run("AP supplier coefficient", size=BODY_12PT, bold=True, color=WHITE, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=BLUE_5,
        line_width=19_050,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _stream_card(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cap: str,
    cap_fill: str,
    paragraphs: list[str],
) -> str:
    cap_h = 360_000
    body_h = 1_260_000
    body_paras = []
    for i, item in enumerate(paragraphs):
        if "|" in item:
            lead, value = item.split("|", 1)
            body_paras.append(
                paragraph(
                    [
                        run(lead, size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                        run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT),
                    ],
                    space_after=80 if i < len(paragraphs) - 1 else 0,
                )
            )
        elif item.startswith("("):
            body_paras.append(
                paragraph(
                    [run(item, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)],
                    space_after=80 if i < len(paragraphs) - 1 else 0,
                )
            )
        else:
            body_paras.append(
                paragraph(
                    [run(item, size=DENSE_BODY_10PT, color=BLACK, font=FONT)],
                    space_after=80 if i < len(paragraphs) - 1 else 0,
                )
            )
    return (
        text_box(
            sp_id, "StreamCardCap", x, y, cx, cap_h,
            [paragraph([run(cap, size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
            fill=cap_fill,
            anchor="ctr",
            insets=INSETS_CARD,
        )
        + text_box(
            sp_id + 1, "StreamCardBody", x, y + cap_h, cx, body_h,
            body_paras,
            fill=BLUE_1,
            anchor="t",
            insets=INSETS_CARD,
        )
    )
def _output_card(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id, "PortfolioOutputCard", x, y, cx, cy,
        [
            paragraph([run("PORTFOLIO SUPPLIER TAM", size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=70),
            paragraph([run("~$573M per year", size=ANSWER_KPI_24PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=45),
            paragraph([run("(~$3.44B FY22-27 cumulative)", size=FINEPRINT_8_5PT, italic=True, color=WHITE, font=FONT)], align="ctr"),
        ],
        fill=BLUE_5,
        line_width=19_050,
        anchor="ctr",
        insets=(160_000, 45_000, 160_000, 45_000),
    )
def _connector_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ConnectorNote", x, y, cx, 150_000,
        [paragraph([run("two supplier-addressable streams", size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _guardrail_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "GuardrailNote", x, y, cx, 250_000,
        [
            paragraph(
                [
                    run("Guardrail: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("BC coefficient uses the MYP-corrected non-GFE corpus. It is not the disclosed-only artifact.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _sizing_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "SizingNote", x, y, cx, 190_000,
        [paragraph([run(_SIZING_NOTE, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    eq_x = BODY_X + 180_000
    eq_y = BODY_Y + 70_000
    eq_w = BODY_CX - 360_000
    eq_h = 620_000
    card_gap = 300_000
    card_side = 440_000
    card_w = (BODY_CX - 2 * card_side - card_gap) // 2
    card_y = eq_y + eq_h + 350_000
    card_h = 1_620_000
    left_x = BODY_X + card_side
    right_x = left_x + card_w + card_gap
    out_w = 4_950_000
    out_h = 900_000
    out_x = BODY_X + (BODY_CX - out_w) // 2
    out_y = card_y + card_h + 300_000
    left_center = left_x + card_w // 2
    right_center = right_x + card_w // 2
    out_center = out_x + out_w // 2
    card_bottom = card_y + card_h
    connectors = (
        connector(10, "BCToPortfolio", left_center, card_bottom, out_center - left_center, out_y - card_bottom, color=GRAY_4, width=_CONNECTOR_W)
        + connector(11, "APToPortfolio", right_center, card_bottom, out_center - right_center, out_y - card_bottom, color=GRAY_4, width=_CONNECTOR_W)
    )
    return (
        connectors
        + _equation_banner(20, eq_x, eq_y, eq_w, eq_h)
        + _stream_card(
            30, left_x, card_y, card_w,
            "BASIC CONSTRUCTION STREAM",
            BLUE_4,
            [
                "BC base |~$17.47B cumulative",
                "Times |12.5% supplier coefficient",
                "Equals |~$365M per year",
                "(~$2.19B cumulative)",
            ],
        )
        + _stream_card(
            40, right_x, card_y, card_w,
            "AP/LLTM STREAM",
            BLUE_3,
            [
                "AP/LLTM base after share |~$1.47B cumulative",
                "Ship-construction share |80.0%",
                "Times |85.0% supplier coefficient",
                "Equals |~$208M per year",
                "(~$1.25B cumulative)",
            ],
        )
        + _connector_note(50, out_x, out_y - 210_000, out_w,)
        + _output_card(60, out_x, out_y, out_w, out_h)
        + _guardrail_note(70, BODY_X + 400_000, out_y + out_h + 60_000, BODY_CX - 800_000)
        + _sizing_note(80, BODY_X, BODY_B - 220_000, BODY_CX)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("TAM Methodology", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
