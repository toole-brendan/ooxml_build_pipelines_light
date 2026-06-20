"""s06_body_demand_backdrop - establish the demand and industrial-base direction of
travel (policy, prime behavior, supplier-base pressure) WITHOUT implying that future
distributed-production targets alter the historical FY2022-FY2027 sizing math.

Layout (no chart, no table): a horizontal five-milestone timeline across the top
(date chips on a black axis, milestone cards hanging below), three no-fill theme
rails reading the timeline as interpretation, a no-fill commentary block with two
bold-led findings, and one focal callout strip pinned to the bottom.

Spec: ds_specs/s06_body_demand_backdrop.txt (SLIDE 06 - DEMAND BACKDROP). Program
treatment is fused, with DDG-specific (HII) and submarine-specific (GD/AUKUS)
evidence carried in the milestone and commentary copy.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector, picture,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_4, BLUE_5,
    WHITE, BLACK, FONT,
    INSETS_CHIP, INSETS_CARD, INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT, BADGE_16PT,
)

# One supporting photograph anchors this otherwise text/diagram deck in the physical
# product. No charts on this slide, so the image rId starts at rId2. The file is a
# pre-cropped submarine-construction image in deck_consolidated/images/.
IMAGES = [{"rId": "rId2", "file": "virginia_construction.jpg"}]

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Context"
_BREADCRUMB_TOPIC = "Demand Signals"
_TOPIC            = "Demand Backdrop"
_TAKEAWAY = ("Policy, prime behavior, and industrial-base pressure point toward "
             "more distributed supplier capacity.")
_SOURCES = ("Sources: (1) Navy and OSD shipbuilding and industrial-base policy and "
            "budget materials, FY2021–FY2026; (2) GAO shipbuilding and submarine "
            "industrial-base reports; (3) HII and General Dynamics public "
            "disclosures and earnings commentary, 2024–2026; (4) submarine "
            "construction photograph, illustrative")

# Raw point size with no exact token (style.py allows raw sizes with a nearby note).
_EVID_95 = 950   # 9.5pt: commentary supporting-evidence text (spec typography)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Four stacked bands inside BODY: timeline, theme rails, commentary, focal callout.
# Heights are tuned so the four bands plus their gaps exactly fill BODY_CY.

# Band 1 — timeline. The axis line threads through the vertical centre of the date
# chips (hidden behind each filled chip, visible in the gaps, like a real timeline);
# short ticks drop from the chip bottoms to a milestone card in each column.
_TL_TOP  = BODY_Y                       # 1_371_600
_CHIP_H  = 330_000
_AXIS_Y  = _TL_TOP + _CHIP_H            # 1_701_600 — chip bottom (tick start / card ref)
_AXIS_LINE_Y = _TL_TOP + _CHIP_H // 2   # 1_536_600 — timeline thread, centred on the chips
_TICK_H  = 150_000
_CARD_Y  = _AXIS_Y + _TICK_H            # 1_851_600
_CARD_H  = 560_000
_TL_BOT  = _CARD_Y + _CARD_H            # 2_411_600

# Five evenly spaced timeline columns across the content width.
_COL_GAP = 110_000
_COL_W   = (BODY_CX - 4 * _COL_GAP) // 5          # 2_168_472
_COL_X   = [BODY_X + i * (_COL_W + _COL_GAP) for i in range(5)]
# Widen the card text box vs. the roomy INSETS_CARD so each milestone holds at two
# lines (the default card inset pushes the longest milestone to three).
_CARD_INSETS = (80_000, 60_000, 80_000, 60_000)

# Band 2 — three no-fill theme rails, each under a thin black top rule.
_RAILS_TOP = _TL_BOT + 230_000          # 2_641_600
_RAILS_H   = 640_000
_RAIL_GAP  = 140_000
_RAIL_W    = (BODY_CX - 2 * _RAIL_GAP) // 3        # 3_667_454
_RAIL_X    = [BODY_X + i * (_RAIL_W + _RAIL_GAP) for i in range(3)]
_RAILS_BOT = _RAILS_TOP + _RAILS_H      # 3_281_600
_RAIL_INSETS = (40_000, 55_000, 40_000, 30_000)   # top inset clears the rule

# Band 3 — commentary block (two bold-led findings, no fill / no border).
_COMM_TOP = _RAILS_BOT + 230_000        # 3_511_600
_COMM_H   = 1_340_000
_COMM_BOT = _COMM_TOP + _COMM_H         # 4_851_600
_COMM_INSETS = (137_160, 40_000, 137_160, 40_000)

# Band 3 is split into a narrowed commentary column (left) and a supporting
# submarine-construction photo (right). The two short findings reflow into the
# left column; the photo fills the right column down to just above the callout.
# Its box aspect (W/H) matches the pre-cropped file exactly so it never distorts.
_COMM_W_L  = 6_300_000                          # narrowed commentary width (~6.9in)
_PHOTO_GUT = 320_000
_PHOTO_X   = BODY_X + _COMM_W_L + _PHOTO_GUT     # 7_073_079
_PHOTO_W   = BODY_R - _PHOTO_X                   # 4_662_362
_PHOTO_Y   = _COMM_TOP - 150_000                 # nudged up so the caption clears the callout
_PHOTO_H   = 1_670_000                           # aspect 2.79 == crop; bottom 5_031_600
_PCAP_Y    = _PHOTO_Y + _PHOTO_H + 16_000        # caption under the photo (~5_047_600)
_PCAP_H    = 95_000
_PHOTO_CAPTION = "Virginia-class submarine under construction"

# Band 4 — focal callout strip, pinned to the body floor.
_CALL_H = 560_000
_CALL_Y = BODY_B - _CALL_H              # 5_310_000


# ── Content ──────────────────────────────────────────────────────────────────
# Timeline: date is the scan anchor (16pt bold chip); milestone phrase is the
# evidence text (9pt card). Each milestone is kept to two lines.
_MILESTONES = [
    ("2021",          "Supplier-base constraint and industrial-base concern"),
    ("2024–2025",     "Industrial-base capacity funding and yard-space outsourcing context"),
    ("Jan 2026",      "Submarine requirement and AUKUS demand context"),
    ("Jan–Apr 2026",  "GD commentary: supply chain is a gating item, submarine-centric"),
    ("Apr–May 2026",  "Navy, GAO, and HII distributed-shipbuilding signals"),
]

# Theme rails: a bold label before the colon, then regular evidence; interpretation
# of the timeline, not additional chronology.
_RAILS = [
    ("Supplier-base constraint:",
     "capacity, long-lead items, sole-source exposure, and industrial-base atrophy."),
    ("Policy and funding tailwind:",
     "Navy distributed-production direction and capacity investment."),
    ("Prime behavior:",
     "HII public distributed-work commitments; GD supply-chain pressure signals."),
]

# Commentary: each (bold finding, supporting evidence). No label prefixes.
_FINDINGS = [
    ("Demand signals support more external capacity, but not a larger sizing numerator.",
     "Policy, oversight, and prime commentary point toward more distributed supplier "
     "work; the FY2022–FY2027 model still sizes from SCN Basic Construction and "
     "strict supplier coefficients."),
    ("DDG and submarine signals support the same direction for different reasons.",
     "HII carries the clearer DDG distributed-production signal; GD's public signal "
     "is more submarine-centric, with margin pressure consistent with an outsourcing "
     "premium."),
]

_CALLOUT_LEAD = "The model sizes the current opportunity; "
_CALLOUT_BODY = ("future distributed work for new entrants is a diligence question, "
                 "not a modeled input.")


# ── Local helpers ────────────────────────────────────────────────────────────
def _date_chip(sp_id: int, x: int, date: str) -> str:
    """Timeline date anchor: BLUE_4 fill, white 16pt bold, 1pt black border."""
    return text_box(
        sp_id, f"DateChip {date}", x, _TL_TOP, _COL_W, _CHIP_H,
        [paragraph([run(date, size=BADGE_16PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_4, line_width=12_700, anchor="ctr", insets=INSETS_CHIP)


def _milestone_card(sp_id: int, x: int, text: str) -> str:
    """Timeline milestone card: one consistent BLUE_1 fill, black 9pt, 1pt border."""
    return text_box(
        sp_id, "MilestoneCard", x, _CARD_Y, _COL_W, _CARD_H,
        [paragraph([run(text, size=LABEL_9PT, color=BLACK, font=FONT)], align="ctr")],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=_CARD_INSETS)


def _theme_rail(sp_id: int, x: int, label: str, evidence: str) -> str:
    """No-fill / no-border theme rail: bold 10pt label, regular 9pt evidence."""
    return text_box(
        sp_id, "ThemeRail", x, _RAILS_TOP, _RAIL_W, _RAILS_H,
        [paragraph([
            run(label + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(evidence, size=LABEL_9PT, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=_RAIL_INSETS)


def _commentary(sp_id: int) -> str:
    """No-fill commentary: bold 9.5pt finding sentence, then a bulleted 9.5pt
    evidence line; hierarchy via bold + bullet, not a larger parent font. Read
    alone, the bold lines are the takeaways."""
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 300)))
    return text_box(sp_id, "Commentary", BODY_X, _COMM_TOP, _COMM_W_L, _PHOTO_H,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=_COMM_INSETS)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    # Timeline axis + per-column ticks (drawn first so chips/cards paint on top).
    axis = connector(10, "TimelineAxis", BODY_X, _AXIS_LINE_Y, BODY_CX, 0,
                     color=BLACK, width=12_700)
    ticks = "".join(
        connector(16 + i, f"TimelineTick{i}", _COL_X[i] + _COL_W // 2, _AXIS_Y,
                  0, _TICK_H, color=BLACK, width=12_700)
        for i in range(5))

    chips = "".join(_date_chip(11 + i, _COL_X[i], _MILESTONES[i][0])
                    for i in range(5))
    cards = "".join(_milestone_card(21 + i, _COL_X[i], _MILESTONES[i][1])
                    for i in range(5))

    # Thin black top rule above each theme rail (separator, not a shape border).
    rail_rules = "".join(
        connector(26 + i, f"RailRule{i}", _RAIL_X[i], _RAILS_TOP, _RAIL_W, 0,
                  color=BLACK, width=9_525)
        for i in range(3))
    rails = "".join(_theme_rail(31 + i, _RAIL_X[i], _RAILS[i][0], _RAILS[i][1])
                    for i in range(3))

    commentary = _commentary(40)

    # Supporting submarine-construction photo (right of the commentary) + caption.
    photo = picture(50, "SubmarineConstructionPhoto", "rId2",
                    _PHOTO_X, _PHOTO_Y, _PHOTO_W, _PHOTO_H)
    photo_caption = text_box(
        51, "PhotoCaption", _PHOTO_X, _PCAP_Y, _PHOTO_W, _PCAP_H,
        [paragraph([run(_PHOTO_CAPTION, size=FINEPRINT_8_5PT, italic=True,
                        color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    callout = text_box(
        45, "FocalCallout", BODY_X, _CALL_Y, BODY_CX, _CALL_H,
        [paragraph([
            run(_CALLOUT_LEAD, size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run(_CALLOUT_BODY, size=MESSAGE_11PT, color=WHITE, font=FONT)],
            align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Paint order: connectors behind, then chips/cards/rails, commentary, photo, callout.
    return (axis + ticks + rail_rules
            + chips + cards + rails + commentary + photo + photo_caption + callout)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
