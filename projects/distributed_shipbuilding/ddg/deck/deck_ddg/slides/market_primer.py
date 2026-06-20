"""Market primer - shape-built ecosystem map for DDG-51 supplier TAM flows.

Flows are drawn as orthogonal bus-and-drop connectors (short vertical drops,
horizontal buses, terminal vertical drops), with arrowheads reserved for the
terminal drops into the downstream boxes.
"""
from __future__ import annotations

from xml.sax.saxutils import escape as _esc

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R,
    BLUE_1, BLUE_5, GRAY_1, GRAY_2, GRAY_4, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_MESSAGE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CAP_12PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Market Primer"
_TAKEAWAY = "DDG-51 construction dollars flow through yards, Navy-procured GFE primes, and yard-side suppliers"
_SOURCES = "Sources: U.S. Navy FY2027 SCN Justification Book, LI 2122; 48 C.F.R. Part 45 and section 52.245-1; FAR 52.204-10"

# ── Connector grammar ────────────────────────────────────────────────────────
# Bus-and-drop: hairline segments, arrowheads only on terminal drops long
# enough to read. Buses and stubs stay arrowless.
_CONNECTOR_W = 9_525            # 0.75pt hairline
_MIN_ARROW_LEN = 250_000        # ~0.27in - below this, no arrowhead
_CONNECTOR_COLOR = BLACK


def _vline(sp_id, name, x, y1, y2, *, arrow=True, dashed=False,
           color=_CONNECTOR_COLOR):
    """Vertical connector segment. Arrowhead only on a terminal drop at least
    _MIN_ARROW_LEN long; pass arrow=False for a stub that lands on a bus."""
    return connector(
        sp_id, name, x, y1, 0, y2 - y1,
        color=color, width=_CONNECTOR_W,
        arrow=arrow and abs(y2 - y1) >= _MIN_ARROW_LEN, dashed=dashed,
    )


def _hline(sp_id, name, x1, x2, y, *, dashed=False, color=_CONNECTOR_COLOR):
    """Horizontal bus segment. Never carries an arrowhead - a bus routes, it
    does not terminate."""
    return connector(
        sp_id, name, x1, y, x2 - x1, 0,
        color=color, width=_CONNECTOR_W, arrow=False, dashed=dashed,
    )


# ── Body shapes ──────────────────────────────────────────────────────────────


def _flow_label(sp_id: int, x: int, y: int, cx: int, text: str) -> str:
    return text_box(
        sp_id, "FlowLabel", x, y, cx, 150_000,
        [paragraph([run(text, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )


def _funding_node(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    # 1pt border (was 1.5pt): the supplier rail is the slide's sole focal
    # anchor, so the funding source reads as a strong identity, not a co-hero.
    return text_box(
        sp_id, "FundingNode", x, y, cx, cy,
        [
            paragraph([run("U.S. NAVY AND SCN LINE ITEM 2122", size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=80),
            paragraph([run("DDG-51 new-construction funding", size=FINEPRINT_8_5PT, italic=True, color=WHITE, font=FONT)], align="ctr"),
        ],
        fill=BLUE_5, anchor="ctr", insets=INSETS_CARD,
    )


def _yard_card(sp_id: int, x: int, y: int, cx: int, title: str, location: str, role: str) -> str:
    return text_box(
        sp_id, "PrimeYardCard", x, y, cx, 1_020_000,
        [
            paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], space_after=80),
            paragraph([run(location, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], space_after=60),
            paragraph([run(role, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)]),
        ],
        fill=GRAY_1, anchor="t", insets=INSETS_CARD,
    )


def _gfe_card(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "GFEPrimesCard", x, y, cx, 1_020_000,
        [
            paragraph([run("Navy-procured GFE primes", size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], space_after=70),
            paragraph([run("Aegis, SPY-6, VLS, Mk 45, LM2500, SEWIP", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], space_after=70),
            paragraph([run("Excluded from non-GFE supplier TAM", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)]),
        ],
        fill=GRAY_2, anchor="t", insets=INSETS_CARD,
    )


def _excluded_tag(sp_id: int, x: int, y: int) -> str:
    """Out-of-scope status badge as a rounded classification tag (roundRect):
    GRAY_5 fill, white text, 1pt black border. Rounded geometry is the
    approved exception for tags / dots / chevrons (never panels or cards)."""
    cx, cy = 1_740_000, 260_000
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="ExcludedTag"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 42000"/></a:avLst></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{GRAY_5}"/></a:solidFill>'
        f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" lIns="45720" tIns="9144" '
        f'rIns="45720" bIns="9144"/><a:lstStyle/><a:p><a:pPr algn="ctr"/>'
        f'<a:r><a:rPr lang="en-US" sz="{LABEL_9PT}" b="1" kern="1200" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{WHITE}"/></a:solidFill>'
        f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
        f'</a:rPr><a:t>{_esc("EXCLUDED FROM TAM")}</a:t></a:r></a:p></p:txBody></p:sp>'
    )


def _supplier_rail(sp_id: int, x: int, y: int, cx: int) -> str:
    cap_h = 360_000
    body_h = 840_000
    return (
        text_box(
            sp_id, "SupplierRailCap", x, y, cx, cap_h,
            [paragraph([run("YARD-SIDE SUPPLIER WORK SIZED IN THIS DECK", size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
            fill=BLUE_5, line_width=19_050, anchor="ctr", insets=INSETS_CARD,
        )
        + text_box(
            sp_id + 1, "SupplierRailBody", x, y + cap_h, cx, body_h,
            [
                paragraph([run("Structural fabrication, machining, electrical and power, piping, HVAC, coatings, castings and forgings", size=LABEL_9PT, color=BLACK, font=FONT)], align="ctr", space_after=90),
                paragraph([run("AP/LLTM supplier-addressable material", size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
            ],
            fill=BLUE_1, anchor="ctr", insets=INSETS_MESSAGE,
        )
    )


def _commentary_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Read:", "the market in layers, not as one gross ship cost."),
        ("Sized market:", "non-GFE new-construction supplier work that sits outside the two assembling yards."),
        ("GFE context:", "critical DDG supplier flow, but outside this TAM definition."),
    ]
    paras = [
        paragraph(
            [run("How to read the flows", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)],
            space_after=160,
        )
    ]
    for i, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120 if i < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id, "CommentaryRail", x, y, cx, cy, paras,
        fill=None, line_color=None, anchor="t", insets=(90_000, 20_000, 30_000, 20_000),
    )


def _body() -> str:
    top_w = 5_300_000
    top_h = 580_000
    top_x = BODY_X + (BODY_CX - top_w) // 2
    top_y = BODY_Y + 60_000
    top_center_x = top_x + top_w // 2
    flow_y = top_y + top_h + 320_000

    card_y = BODY_Y + 1_320_000
    card_h = 1_020_000
    yard_x = BODY_X + 300_000
    yard_gap = 140_000
    yard_w = 3_280_000
    yard2_x = yard_x + yard_w + yard_gap
    gfe_x = BODY_X + 7_400_000
    gfe_w = BODY_R - gfe_x - 250_000

    yard1_center = yard_x + yard_w // 2
    yard2_center = yard2_x + yard_w // 2
    gfe_center = gfe_x + gfe_w // 2

    rail_x = yard_x
    rail_y = BODY_Y + 2_700_000
    rail_w = gfe_x - yard_x - 260_000
    rail_center = rail_x + rail_w // 2

    excluded_y = card_y + card_h + 260_000           # terminal of the GFE flow
    yard_supplier_bus_y = card_y + card_h + 80_000   # short stub below the yard cards

    commentary_x = gfe_x
    commentary_y = excluded_y + 260_000 + 110_000     # clears the excluded tag
    commentary_w = gfe_w
    commentary_h = 1_300_000

    # Orthogonal bus-and-drop flow. Arrowheads on the terminal drops into the
    # downstream boxes; buses and short stubs stay arrowless.
    connectors = (
        # Funding into the split bus - no arrow, it lands on a bus, not a box.
        _vline(10, "FundingToSplit", top_center_x, top_y + top_h, flow_y, arrow=False)

        # One continuous split bus that reaches BIW, Ingalls, and GFE.
        + _hline(11, "SplitBus", yard1_center, gfe_center, flow_y)

        # Terminal drops into the three downstream boxes.
        + _vline(12, "SplitToBIW", yard1_center, flow_y, card_y)
        + _vline(13, "SplitToIngalls", yard2_center, flow_y, card_y)
        + _vline(14, "SplitToGFE", gfe_center, flow_y, card_y)

        # Yard cards converge via an orthogonal bus, not diagonals.
        + _vline(15, "BIWToSupplierBus", yard1_center, card_y + card_h, yard_supplier_bus_y, arrow=False)
        + _vline(16, "IngallsToSupplierBus", yard2_center, card_y + card_h, yard_supplier_bus_y, arrow=False)
        + _hline(17, "YardSupplierBus", yard1_center, yard2_center, yard_supplier_bus_y)
        + _vline(18, "SupplierBusToRail", rail_center, yard_supplier_bus_y, rail_y)

        # Out-of-scope terminal: dashed reads as exclusion / boundary.
        + _vline(19, "GFEToExcluded", gfe_center, card_y + card_h, excluded_y, dashed=True, color=GRAY_4)
    )

    labels = (
        _flow_label(20, yard_x, flow_y - 180_000, rail_w, "IN-PROGRAM CONSTRUCTION FLOW")
        + _flow_label(21, gfe_x, flow_y - 180_000, gfe_w, "NAVY-PROCURED GFE FLOW")
    )

    cards = (
        _funding_node(30, top_x, top_y, top_w, top_h)
        + _yard_card(31, yard_x, card_y, yard_w, "GD Bath Iron Works", "Bath, ME and Brunswick, ME", "Prime yard and DDG-51 design agent")
        + _yard_card(32, yard2_x, card_y, yard_w, "HII Ingalls Shipbuilding", "Pascagoula, MS", "Prime yard and distributed-shipbuilding network")
        + _gfe_card(33, gfe_x, card_y, gfe_w)
        + _excluded_tag(34, gfe_x + (gfe_w - 1_740_000) // 2, excluded_y)
        + _supplier_rail(40, rail_x, rail_y, rail_w)
        + _commentary_rail(50, commentary_x, commentary_y, commentary_w, commentary_h)
    )

    # Paint order = concatenation order: cards first, connectors over them so
    # terminal arrowheads sit on the card edges, no-fill labels on top.
    return cards + connectors + labels


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
