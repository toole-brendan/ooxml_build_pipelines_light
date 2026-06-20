"""Sourcing Priority Board - SLIDE 02 wireframed in the DrawingML canvas layer.

INTENT
    State the answer as an action screen: Columbia is the expansion case, Virginia
    the concentrated-incumbent pocket, DDG-51 the near-term timing pressure. An
    answer-board layout: three program cards on top, a ranked priority-lane bar
    chart in the middle, a full-width priority table below. The whole slide is ONE
    16:9 DrawingML canvas (slide_canvas + CanvasBox / CanvasLine); a slide_frame
    annotation lists layout + objects below it. No commentary rail - cards carry
    the narrative, the chart sizes the lanes, the table is the audit trail. Visible
    copy avoids role labels and self-reference.

OUTLINE (source-only; not emitted)
    - title band (dark, white)            : topic | finding
    - three program cards                 : Columbia / Virginia / DDG-51
    - ranked bar chart                    : priority lanes by recent supplier $M
    - priority table (full width)         : program / PIID / work type / signal / $M
    - source line (small, gray)

DATA NOTE (build, not slide copy): take DDG-51 counts from Re-buy Timing /
    Concentrated Lanes / Source Concentration (Concentration 9, second-source 12,
    re-buy 18), not the Overview cached zeros. Carried in the slide_frame objects.
"""
from __future__ import annotations

from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_SLIDE_16x9_TALL
from docx_core.wireframes import slide_canvas, slide_frame, CanvasBox
from docx_core.style import (
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, GRAY_5, WHITE, BLACK,
)
from doc_distributed_shipbuilding.pages._slidekit import ranked_hbar, rule_table

PAGE_TITLE = "Sourcing Priority Board - slide mock"

W = 12.5
CARD_GAP = 0.20
CARD_W = (W - 2 * CARD_GAP) / 3
CARD_Y, CARD_H = 0.70, 1.65

# Per-bar / per-card signal colors (darkest reserved for timing urgency).
EXPANSION, CONCENTRATION, TIMING = BLUE_2, BLUE_4, BLUE_5


def _card(x, prog, signal, chips, fill, tcol) -> list[str]:
    """One program answer card: filled sharp-rect (1.5pt border, the slide's single
    heavy-border family) with a program cap, a 16pt signal line, and fragment
    chips. Text rides over the fill as no-fill / no-line boxes."""
    return [
        CanvasBox(x, CARD_Y, CARD_W, CARD_H, fill=fill, line=BLACK, line_pt=1.5,
                  name=prog),
        CanvasBox(x + 0.12, CARD_Y + 0.06, CARD_W - 0.24, 0.24, text=prog,
                  fill="none", line="none", align="left", text_size_pt=11,
                  text_color=tcol),
        CanvasBox(x + 0.12, CARD_Y + 0.32, CARD_W - 0.24, 0.52, text=signal,
                  fill="none", line="none", align="left", text_size_pt=16,
                  text_color=tcol),
        CanvasBox(x + 0.12, CARD_Y + 0.88, CARD_W - 0.24, CARD_H - 0.94,
                  text="\n".join(chips), fill="none", line="none", align="left",
                  text_size_pt=9, text_color=tcol),
    ]


def _cards() -> list[str]:
    out = []
    out += _card(0.0, "COLUMBIA", "Expansion screen", [
        "6 second-source / active-incumbent lanes",
        "$2.4B recent supplier $",
        "0 concentration lanes; 0 timing lanes",
    ], BLUE_3, WHITE)
    out += _card(CARD_W + CARD_GAP, "VIRGINIA", "Concentrated incumbent pocket", [
        "9 concentration lanes",
        "$503M largest concentrated lane",
        "3 timing lanes",
    ], BLUE_2, BLACK)
    out += _card(2 * (CARD_W + CARD_GAP), "DDG-51", "Timing pressure", [
        "18 re-buy lanes inside 12 months",
        "$491M largest timing lane",
        "9 concentration lanes",
    ], BLUE_5, WHITE)
    return out


def _ranked_chart() -> list[str]:
    """Middle: single-series ranked bars by recent supplier $M, per-bar color by
    signal type, with an external title and a manual three-item key."""
    out = [
        CanvasBox(0.0, 2.45, 7.0, 0.20, fill="none", line="none", align="left",
                  text_size_pt=10, text_color=GRAY_5,
                  text="Priority lanes by recent supplier $M"),
        CanvasBox(0.0, 2.66, 7.4, 0.18, fill="none", line="none", align="left",
                  text_size_pt=8, text_color=GRAY_5,
                  text="Recent supplier $M; lanes selected from active "
                       "sourcing-signal screens."),
    ]
    # Manual key, right of the title row.
    key = [("Expansion", EXPANSION), ("Concentration", CONCENTRATION),
           ("Timing", TIMING)]
    kx = 8.0
    for label, color in key:
        out.append(CanvasBox(kx, 2.47, 0.16, 0.14, fill=color, line=BLACK,
                             line_pt=0.5))
        out.append(CanvasBox(kx + 0.22, 2.45, 1.05, 0.18, text=label, fill="none",
                             line="none", align="left", text_size_pt=8))
        kx += 1.5
    out += ranked_hbar(0.0, 2.85, W, [
        ("1  Columbia · N0002417C2117 · Electrical", 1138, EXPANSION, "$1,138M"),
        ("2  Virginia · N0002417C2100 · Electrical", 503, CONCENTRATION, "$503M"),
        ("3  Columbia · N0002417C2117 · Piping", 498, EXPANSION, "$498M"),
        ("4  DDG-51 · N0002423C2307 · Machining", 491, TIMING, "$491M"),
        ("5  Columbia · N0002417C2117 · Structural", 416, EXPANSION, "$416M"),
        ("6  DDG-51 · N0002423C2307 · Electrical", 159, TIMING, "$159M"),
    ], name_w=3.6, bar_h=0.18, gap=0.06, max_bar=7.4, value_w=0.95)
    return out


def _priority_table() -> list[str]:
    """Bottom: the six named lanes (program / PIID / work type / signal / recent
    $M / evidence read), ordered to match the chart. Rule skin; Program column
    carries row-identity fill; Signal in bold; Recent $M right-aligned."""
    def prog(name, fill, color):
        return {"text": name, "fill": fill, "color": color, "align": "center"}

    VA = lambda: prog("Virginia", BLUE_1, BLACK)
    COL = lambda: prog("Columbia", BLUE_3, WHITE)
    DDG = lambda: prog("DDG-51", BLUE_5, WHITE)
    sig = lambda t: {"text": t, "color": BLUE_5}
    money = lambda v: {"text": v, "align": "right"}

    headers = ["Program", "PIID", "Work type", "Signal",
               {"text": "Recent $M", "align": "right"}, "Evidence read"]
    rows = [
        [COL(), "N0002417C2117",
         "Electrical power / distribution / generation", sig("Expansion"),
         money("$1,138M"),
         "29 active vendors; top-1 54%; FY22 second-source entry"],
        [VA(), "N0002417C2100",
         "Electrical power / distribution / generation", sig("Concentration"),
         money("$503M"),
         "Top-1 93%; Northrop Grumman; 23 active vendors"],
        [COL(), "N0002417C2117", "Piping / fluid handling", sig("Expansion"),
         money("$498M"),
         "69 active vendors; top-1 29%; FY22 second-source entry"],
        [DDG(), "N0002423C2307", "Machining / mechanical / propulsion",
         sig("Timing"), money("$491M"),
         "Next re-buy 2026-06-19; 6 active vendors; top-1 54%"],
        [COL(), "N0002417C2117", "Structural fabrication & modules",
         sig("Expansion"), money("$416M"),
         "45 active vendors; top-1 30%; FY22 second-source entry"],
        [DDG(), "N0002423C2307",
         "Electrical power / distribution / generation", sig("Timing"),
         money("$159M"),
         "Next re-buy 2026-07-14; 10 active vendors; top-1 25%"],
    ]
    return rule_table(0.0, 4.45, W, headers, rows,
                      col_w=[1.2, 1.7, 2.95, 1.6, 1.1, 3.95],
                      header_h=0.28, row_h=0.30, body_pt=8.0, header_pt=8.5)


def _slide() -> str:
    ch: list[str] = []
    ch.append(CanvasBox(0.0, 0.0, W, 0.58, fill=BLUE_5, text_color=WHITE,
                        align="left", text_size_pt=13,
                        text="Sourcing Priorities  |  Columbia points to expansion, "
                             "Virginia to concentration, and DDG-51 to timing "
                             "pressure."))
    ch += _cards()
    ch += _ranked_chart()
    ch += _priority_table()
    ch.append(CanvasBox(0.0, 6.72, W, 0.30, fill="none", line="none",
                        align="left", text_size_pt=7.5, text_color=GRAY_5,
                        text="Sources: attached workbook tabs Overview, Re-buy "
                             "Timing, Concentrated Lanes, Source Concentration, PIID "
                             "× Work Type; FSRS supplier-role subaward records, "
                             "recent window FY22–FY26, as of 2026-05-22. "
                             "Sheet-module basis: Indicators stack recompete-timing, "
                             "concentration, and source-diversification screens; "
                             "Market Views and Detail Tables provide sizing and leaf "
                             "evidence."))
    return slide_canvas(ch, ratio="16:9", w_in=W)


def render() -> PageModuleSpec:
    return PageModuleSpec(
        page_setup=PAGE_SLIDE_16x9_TALL, title=PAGE_TITLE,
        body=slide_frame(
            _slide(),
            layout=[
                "Answer-board: three program cards on top, a ranked priority-lane "
                "bar chart in the middle, a full-width priority table below.",
                "Title band across the top (dark fill, white text).",
                "No commentary rail; cards carry the narrative, the chart sizes the "
                "lanes, the table is the audit trail.",
                "Source line along the bottom edge.",
            ],
            objects=[
                "Title: topic | finding.",
                "Cards (top): Columbia / Virginia / DDG-51, program cap + 16pt "
                "signal line + fragment chips; blue ramp Columbia BLUE_3, Virginia "
                "BLUE_2, DDG-51 BLUE_5 (white text on dark); 1.5pt card borders are "
                "the single heavy-border family.",
                "Chart (middle): single-series ranked horizontal bars by recent "
                "supplier $M, per-bar color by signal (Expansion / Concentration / "
                "Timing) with a manual key; direct end labels.",
                "Table (bottom): program / PIID / work type / signal / recent $M / "
                "evidence read; rule skin, program-column row-identity fill, signal "
                "in bold, $M right-aligned; rows ordered to match the chart.",
                "DATA NOTE (build, not slide copy): take DDG-51 counts from Re-buy "
                "Timing / Concentrated Lanes / Source Concentration (Concentration "
                "9, second-source 12, re-buy 18), not the Overview cached zeros.",
            ],
        ),
    )
