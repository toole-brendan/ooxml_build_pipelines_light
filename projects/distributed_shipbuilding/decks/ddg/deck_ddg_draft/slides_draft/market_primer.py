"""market_primer — generated from the DDG slide spec.

Intent: Explain who pays whom and which flows are in scope so the reader does not treat DDG-51 construction as one undifferentiated supplier pool; make the denominator language visual before the cost funnel, MYP correction, and TAM build.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Market primer'
_TITLE_TOPIC = 'Market Primer'
_TAKEAWAY = 'DDG-51 construction dollars flow through prime yards, Navy-procured GFE primes, and yard-side suppliers'
_SOURCES = 'Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122; (2) FAR Part 45 and FAR 52.245-1, Government Property; (3) FAR 52.204-10'

_CHART_SPECS = []
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    # Coordinates
    y0 = BODY_Y
    out.append(nofill(10, "Thesis", BODY_X, y0, BODY_CX, 360_000,
        [lead_body("Read:", "DDG-51 construction is layered: Navy funding, two prime yards, Navy-procured GFE, and the yard-side supplier layer sized in this deck.", lead_size=FINEPRINT_8_5PT, body_size=MESSAGE_11PT)], anchor="t"))

    navy_x, navy_y, navy_w, navy_h = BODY_X + 180_000, BODY_Y + 820_000, 2_350_000, 760_000
    biw_x, biw_y, yard_w, yard_h = BODY_X + 3_600_000, BODY_Y + 620_000, 2_900_000, 610_000
    ing_x, ing_y = biw_x, BODY_Y + 1_460_000
    sup_x, sup_y, sup_w, sup_h = BODY_X + 7_300_000, BODY_Y + 900_000, 3_750_000, 950_000

    # Paint connectors first.
    out.append(connector(20, "NavyToBIW", navy_x + navy_w, navy_y + 200_000, biw_x - (navy_x + navy_w), biw_y + 120_000 - (navy_y + 200_000), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(21, "NavyToIngalls", navy_x + navy_w, navy_y + 520_000, ing_x - (navy_x + navy_w), ing_y + 160_000 - (navy_y + 520_000), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(22, "BIWToSupplier", biw_x + yard_w, biw_y + 300_000, sup_x - (biw_x + yard_w), sup_y + 220_000 - (biw_y + 300_000), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(23, "IngallsToSupplier", ing_x + yard_w, ing_y + 300_000, sup_x - (ing_x + yard_w), sup_y + 640_000 - (ing_y + 300_000), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(24, "NavyToGFE", navy_x + 900_000, navy_y + navy_h, BODY_X + 1_380_000 - (navy_x + 900_000), BODY_Y + 3_250_000 - (navy_y + navy_h), color=BLACK, dashed=True, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(25, "SupplierToFFATA", sup_x + sup_w - 500_000, sup_y + sup_h, BODY_X + 9_700_000 - (sup_x + sup_w - 500_000), BODY_Y + 3_250_000 - (sup_y + sup_h), color=BLACK, dashed=True, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))

    out.append(text_box(30, "NavyNode", navy_x, navy_y, navy_w, navy_h,
        [p("U.S. NAVY SCN", size=CAP_12PT, bold=True, color=WHITE, align="ctr", space_after=90),
         p("Line Item 2122", size=LABEL_9PT, color=WHITE, align="ctr"),
         p("new-construction funding", size=FINEPRINT_8_5PT, italic=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color=BLACK, line_width=STRONG_LINE, insets=INSETS_CARD, anchor="ctr"))
    out.append(box(31, "BIW", biw_x, biw_y, yard_w, yard_h,
        [p("GD Bath Iron Works", size=LABEL_9PT, bold=True, color=DK, align="ctr"),
         p("prime-yard node", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")], fill=GRAY_1, line_color=BLACK))
    out.append(box(32, "Ingalls", ing_x, ing_y, yard_w, yard_h,
        [p("HII Ingalls", size=LABEL_9PT, bold=True, color=DK, align="ctr"),
         p("prime-yard node and distributed-network context", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")], fill=GRAY_1, line_color=BLACK))
    out.append(text_box(33, "SupplierLane", sup_x, sup_y, sup_w, sup_h,
        [p("IN-SCOPE SUPPLIER LANE", size=CAP_12PT, bold=True, color=DK, align="ctr", space_after=100),
         p("yard-side supplier work sized by the deck", size=LABEL_9PT, color=DK, align="ctr"),
         p("non-GFE new-construction supplier TAM", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color=BLACK, insets=INSETS_CARD, anchor="ctr"))

    tag_y = BODY_Y + 2_950_000
    out.append(exhibit_title(40, "Excluded lanes are context, not the sized supplier TAM", BODY_X, tag_y - 250_000, BODY_CX))
    tag_w = (BODY_CX - 3 * GAP) // 4
    tags = [
        ("GFE", "Navy-procured combat-system primes"),
        ("WEAPONS", "WPN and OPN missile and ordnance flows"),
        ("SUSTAINMENT", "depot, repair, modernization"),
        ("FFATA", "evidence source, not definition"),
    ]
    for i, (cap, body) in enumerate(tags):
        out.append(chip(41+i, f"Tag{cap}", BODY_X + i*(tag_w + GAP), tag_y, tag_w, 520_000, cap, body, fill=GRAY_1, line_color=BLACK))

    out.append(nofill(50, "Legend", BODY_X, BODY_Y + 3_630_000, 6_650_000, 480_000,
        [lead_body("Legend:", "blue lane = sized non-GFE supplier work; gray tags = exclusions or evidence lenses; dashed lines = context/evidence only.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT)], anchor="t"))
    out.append(bullet_rail(51, BODY_X + 7_250_000, BODY_Y + 3_550_000, 3_950_000, 700_000,
        [("Market layer:", "the prime yards are pass-through and self-perform nodes, not target suppliers."),
         ("Evidence layer:", "FFATA-visible subawards help classify work, but do not set the denominator.")], body_size=LABEL_9PT, insets=INSETS_NONE))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
