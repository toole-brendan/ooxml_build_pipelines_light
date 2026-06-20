"""executive_summary — generated from the DDG slide spec.

Intent: Give the answer up front while making clear the values are average-annual FY22-27 sizing conventions, not a steady run-rate or a capture forecast.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Answer'
_TITLE_TOPIC = 'Executive Summary'
_TAKEAWAY = 'DDG-51 supplier TAM averages ~$573M per year, with ~$327M per year in broad component SAM'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoW DDG-51 contract announcements, July 2022 to May 2026; (3) SAM.gov Subaward Reporting Public API'

_CHART_SPECS = []
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(nofill(10, "Qualifier", BODY_X, BODY_Y, BODY_CX, 300_000,
        [lead_body("Answer convention:", "headline values are average annual FY22-27; cumulative values are secondary context, not a run-rate.", lead_size=FINEPRINT_8_5PT, body_size=MESSAGE_11PT)], anchor="t"))
    hero_y = BODY_Y + 520_000
    hero_w = (BODY_CX - GAP) // 2
    out.append(kpi_card(20, "SupplierTAM", BODY_X, hero_y, hero_w, 1_130_000, "Supplier TAM", "~$573M per year", "($3.44B FY22-27)", fill=BLUE_5))
    out.append(kpi_card(21, "BroadSAM", BODY_X + hero_w + GAP, hero_y, hero_w, 1_130_000, "Broad SAM", "~$327M per year", "($1.96B FY22-27)", fill=BLUE_4))
    support_y = hero_y + 1_130_000 + GAP
    card_w = (BODY_CX - 3 * GAP) // 4
    cards = [
        ("BC stream", "~$365M per year", "~$2.19B cumulative", BLUE_1),
        ("AP and LLTM", "~$208M per year", "~$1.25B cumulative", BLUE_1),
        ("Broad SAM share", "57.1% of TAM", "scenario, not SOM", GRAY_1),
        ("Per hull", "~$265M", "13 in-window hulls", GRAY_1),
    ]
    for i, (cap, value, qual, fill) in enumerate(cards):
        out.append(support_kpi(30+i, f"Support{i}", BODY_X + i*(card_w+GAP), support_y, card_w, 890_000, cap, value, qual, fill=fill))
    rail_y = support_y + 890_000 + GAP
    out.append(bullet_rail(40, BODY_X, rail_y, BODY_CX, 830_000,
        [("Answer:", "supplier TAM is ~$573M per year after non-GFE and MYP-corrected scope gates."),
         ("Serviceable menu:", "broad component SAM is the largest scenario at ~$327M per year."),
         ("Discipline:", "SAM is not SOM and the scenarios are never summed.")], body_size=LABEL_9PT))
    out.append(sizing_note(50, "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
