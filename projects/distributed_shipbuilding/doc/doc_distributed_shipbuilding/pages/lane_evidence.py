"""Lane Evidence System - SLIDE 01 wireframed in the DrawingML canvas layer.

INTENT
    Show how the supplier-record corpus becomes lane-level sourcing signals as
    auditable infrastructure, not a process narrative. A method-board layout: a
    full-width five-stage method rail on top, then a coverage chart (lower-left)
    and a signal-test table (lower-right). The whole slide is ONE 16:9 DrawingML
    canvas (slide_canvas + CanvasBox / CanvasLine); a slide_frame annotation lists
    layout + objects below it. No prose commentary rail - the title, rail, chart,
    and table carry the read. Visible copy avoids self-reference / process talk.

OUTLINE (source-only; not emitted)
    - title band (dark, white)            : topic | finding
    - method rail (5 stages + arrows)     : scope -> grain -> controls -> signals
    - chart (lower-left)                   : 100% stacked coverage by program
    - signal-test table (lower-right)      : signal / trigger / read / evidence
    - caveat chip + source line (small, gray)
"""
from __future__ import annotations

from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_SLIDE_16x9_TALL
from docx_core.wireframes import slide_canvas, slide_frame, CanvasBox
from docx_core.style import (
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, GRAY_1, GRAY_2, GRAY_5, WHITE, BLACK,
)
from doc_distributed_shipbuilding.pages._slidekit import (
    stage_rail, stacked_hbar, rule_table,
)

PAGE_TITLE = "Lane Evidence System - slide mock"

W = 12.5                         # slide region width (see _slidekit / doc_guide)
LX, LW = 0.0, 6.1                # lower-left chart column
RX, RW = 6.4, 6.1                # lower-right table column


def _method_rail() -> list[str]:
    """Five stage cards (blue ramp BLUE_1 -> BLUE_5), white text on the dark ones,
    joined by thin black arrows. The final SOURCING SIGNALS card carries the one
    1.5pt heavy border."""
    stages = [
        ("SCOPE",
         ["39 shipbuilder-directed PIIDs", "≤FY12–FY26 supplier records"],
         BLUE_1, BLACK, 1.0),
        ("SUPPLIER RECORDS",
         ["18,747 reported records", "$10.8B supplier $M"],
         BLUE_2, BLACK, 1.0),
        ("LANE GRAIN",
         ["132 PIID and work-type lanes", "2,897 vendor-lane rows"],
         BLUE_3, WHITE, 1.0),
        ("LIVE CONTROLS",
         ["FY22–FY26 recent window", "75% top-1 cutoff; 12-mo horizon"],
         BLUE_4, WHITE, 1.0),
        ("SOURCING SIGNALS",
         ["Timing, concentration, 2nd-source entry", "reconciled across $M and "
          "records"],
         BLUE_5, WHITE, 1.5),
    ]
    return stage_rail(0.0, 0.72, W, 1.00, stages)


def _coverage_chart() -> list[str]:
    """Lower-left: 100% stacked horizontal coverage bars by program, ordered by
    coverage share, with 'x of y' end labels - plus an external title, units
    caption, a two-item legend, and the data-floor caveat chip."""
    out = [
        CanvasBox(LX, 1.90, LW, 0.20, fill="none", line="none", align="left",
                  text_size_pt=10, text_color=GRAY_5,
                  text="PIIDs with reported supplier records, count of in-scope "
                       "PIIDs"),
        CanvasBox(LX, 2.12, LW, 0.18, fill="none", line="none", align="left",
                  text_size_pt=8, text_color=GRAY_5,
                  text="Count of in-scope PIIDs; supplier-record coverage, not "
                       "program value."),
    ]
    out += stacked_hbar(LX, 2.40, LW, [
        ("Columbia", [(4, BLUE_5, WHITE), (1, GRAY_2, BLACK)], "4 of 5"),
        ("Virginia", [(6, BLUE_5, WHITE), (4, GRAY_2, BLACK)], "6 of 10"),
        ("DDG-51", [(11, BLUE_5, WHITE), (13, GRAY_2, BLACK)], "11 of 24"),
    ], name_w=1.25, max_bar=3.0, end_w=0.95)
    # Legend (two swatches).
    out.append(CanvasBox(LX, 3.70, 0.16, 0.14, fill=BLUE_5, line=BLACK,
                         line_pt=0.5))
    out.append(CanvasBox(LX + 0.22, 3.68, 1.4, 0.18, text="With records",
                         fill="none", line="none", align="left", text_size_pt=8))
    out.append(CanvasBox(LX + 1.70, 3.70, 0.16, 0.14, fill=GRAY_2, line=BLACK,
                         line_pt=0.5))
    out.append(CanvasBox(LX + 1.92, 3.68, 2.0, 0.18, text="No supplier records",
                         fill="none", line="none", align="left", text_size_pt=8))
    # Data-floor caveat chip.
    out.append(CanvasBox(LX, 4.02, 3.9, 0.36, fill=BLUE_1, line=BLACK,
                         line_pt=1.0, align="center", text_size_pt=9,
                         text="FSRS levels are floors; FY26 is partial."))
    return out


def _signal_table() -> list[str]:
    """Lower-right: the five sourcing screens (signal / lane trigger / read /
    primary evidence), rule skin, bold first column, pale fill on the Data floor
    row only."""
    def sig(text):
        return {"text": text, "color": BLUE_5, "pt": 9}

    headers = ["Signal", "Lane trigger", "Read", "Primary evidence"]
    rows = [
        [sig("Re-buy timing"),
         "Active multi-source lane; next buy inside the 12-month horizon",
         "Split supplier base with a near-term sourcing window",
         "Lane Vendor FY; lane-signal cadence"],
        [sig("Concentration"),
         "Top-1 recent supplier share ≥75%",
         "Incumbent pocket, even where program-level share is diffuse",
         "Lane Vendor FY; recent top supplier"],
        [sig("Second-source entry"),
         "Recent additional suppliers with incumbent still active",
         "Split underway; expansion path worth tracking",
         "Source Concentration; second-source FY"],
        [{"text": "Data floor", "color": BLUE_5, "pt": 9, "fill": GRAY_1},
         {"text": "FSRS supplier records are incomplete and FY26 is partial",
          "fill": GRAY_1},
         {"text": "Relative signal screen, not full market sizing", "fill": GRAY_1},
         {"text": "Sources; Inputs", "fill": GRAY_1}],
        [sig("Tie-out guardrail"),
         "Supplier $M and records reconcile across independent cuts",
         "Broken formulas or dropped rows surface before reads",
         "Checks; Detail Tables"],
    ]
    out = [CanvasBox(RX, 1.90, RW, 0.22, fill="none", line="none", align="left",
                     text_size_pt=10.5, text_color=BLUE_5,
                     text="Signal tests and live controls")]
    out += rule_table(RX, 2.18, RW, headers, rows,
                      col_w=[1.0, 2.05, 1.95, 1.1],
                      header_h=0.30, row_h=0.72, body_pt=8.5, header_pt=9.0)
    return out


def _slide() -> str:
    ch: list[str] = []
    ch.append(CanvasBox(0.0, 0.0, W, 0.58, fill=BLUE_5, text_color=WHITE,
                        align="left", text_size_pt=13,
                        text="Lane Evidence  |  Supplier records are tested at lane "
                             "grain before sourcing calls."))
    ch += _method_rail()
    ch += _coverage_chart()
    ch += _signal_table()
    ch.append(CanvasBox(0.0, 6.72, W, 0.30, fill="none", line="none",
                        align="left", text_size_pt=7.5, text_color=GRAY_5,
                        text="Sources: attached workbook tabs Overview, PIID × Work "
                             "Type, Lane Vendors, Lane Vendors × FY, Re-buy Timing, "
                             "Concentrated Lanes, Source Concentration, Tie-Outs; "
                             "FSRS supplier-role subaward records, as of 2026-05-22. "
                             "Sheet-module basis: Sources, Inputs, Detail Tables, "
                             "Indicators, Checks."))
    return slide_canvas(ch, ratio="16:9", w_in=W)


def render() -> PageModuleSpec:
    return PageModuleSpec(
        page_setup=PAGE_SLIDE_16x9_TALL, title=PAGE_TITLE,
        body=slide_frame(
            _slide(),
            layout=[
                "Method-board: full-width five-stage method rail on top; a coverage "
                "chart lower-left and a signal-test table lower-right.",
                "Title band across the top (dark fill, white text).",
                "Reads top-to-bottom: scope -> lane grain -> signal tests -> "
                "caveat / checks.",
                "Caveat chip under the chart; source line along the bottom.",
            ],
            objects=[
                "Title: topic | finding.",
                "Method rail: five sharp-rect stages (SCOPE -> SUPPLIER RECORDS -> "
                "LANE GRAIN -> LIVE CONTROLS -> SOURCING SIGNALS), blue ramp "
                "BLUE_1 -> BLUE_5, white text on dark, thin black arrows; the final "
                "stage carries the single 1.5pt heavy border.",
                "Chart (lower-left): 100% stacked horizontal bars, PIID "
                "supplier-record coverage by program, ordered by coverage share, "
                "'x of y' end labels; legend With records / No supplier records.",
                "Table (lower-right): signal x lane trigger / read / primary "
                "evidence; rule skin, bold first column, pale 'Data floor' row.",
                "Caveat chip: 'FSRS levels are floors; FY26 is partial.'; external "
                "italic chart title; source note (small, gray).",
            ],
        ),
    )
