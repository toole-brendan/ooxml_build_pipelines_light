"""award_data_sourcing_updated — US Defense Market Strategy deck.

EXHIBIT — "Award Data Sourcing & Validation": SAM.gov Contract Awards is the
modern transaction base; budget, supplier, and entity layers enrich the pull,
and every record passes through a validation gate before it becomes a market,
opportunity, or end-user output.

REDESIGN RATIONALE
  • The workflow is the primary exhibit, so it now occupies ~3.7 inches of body
    height rather than sharing equal visual weight with a redundant source table.
  • Source cards, step chips, connector runs, the validation gate, and output
    cards were enlarged together so the diagram reads at normal presentation
    distance without changing the underlying methodology.
  • The detailed source-by-source table was replaced by a compact four-card
    "Key source rules" strip. The workflow already names every source; the strip
    preserves only the decision-useful rules that govern counting and validation.
  • The title head was revised to the deck's standard topic + takeaway pattern:
    a concise title-cased topic followed by an insight-led sentence.

CODE MAP (body follows paint order; headers mark roles in place):
  • chrome .............. breadcrumb() + prelim_chip() + title_placeholder()
  • stage bands ......... PULL / ENRICH / VALIDATE backgrounds and labels
  • PULL ................. modern-base note + steps 1–2 + budget / award spine
  • ENRICH ............... steps 3–6 + four source cards + two caveat cards
  • VALIDATE ............. step 7 gate + FPDS legacy validation input
  • OUTPUTS .............. external evidence + three output cards and output bus
  • key source rules ..... four compact bottom cards replacing the dense table
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector,
    breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import (
    IN, PT, BLACK, WHITE,
    BLUE_1, BLUE_2, BLUE_3, BLUE_5,
    GRAY_1, GRAY_2, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── enlarged workflow geometry ────────────────────────────────────────────────
_BAND_Y, _BAND_H = IN(1.52), IN(3.72)
_STAGE_LBL_Y, _STAGE_LBL_H = IN(1.56), IN(0.18)

_STEP_W, _STEP_H = IN(0.24), IN(0.24)
_STEP_LBL_W, _STEP_LBL_H = IN(0.94), IN(0.24)

_ENRICH_ROW_Y = IN(2.24)
_ENRICH_CARD_W, _ENRICH_CARD_H = IN(1.16), IN(0.62)
_ENRICH_CAVEAT_Y, _ENRICH_CAVEAT_H = IN(3.02), IN(0.72)

_SPINE_Y, _SPINE_H = IN(4.05), IN(0.58)
_FPDS_Y, _FPDS_H = IN(4.68), IN(0.30)

_OUTPUT_COL_X, _OUTPUT_COL_W = IN(10.10), IN(2.65)
_OUTPUT_BUS_X = IN(9.86)
_OUTPUT_CARD_H = IN(0.56)

_RULE_LABEL_Y, _RULE_Y, _RULE_H = IN(5.38), IN(5.62), IN(1.15)


# ── repeated-shape data ───────────────────────────────────────────────────────
_STAGE_BANDS = [
    (0.495, 2.65, GRAY_1),
    (3.145, 5.00, BLUE_1),
    (8.145, 1.55, BLUE_2),
]

_STAGE_LABELS = [
    (0.575, 0.70, "PULL"),
    (3.225, 0.82, "ENRICH"),
    (8.225, 0.98, "VALIDATE"),
    (10.125, 0.94, "OUTPUTS"),
]

# x, y, fill, step number, action
_STEP_HEADERS = [
    (0.70, 3.62, BLUE_3, "1", "Define"),
    (2.12, 3.62, BLUE_3, "2", "Pull"),
    (3.34, 1.88, BLUE_3, "3", "Add"),
    (4.58, 1.88, BLUE_3, "4", "Link"),
    (5.82, 1.88, BLUE_3, "5", "Pull"),
    (7.06, 1.88, BLUE_3, "6", "Resolve"),
    (8.32, 1.92, BLUE_5, "7", "Validate"),
]

# x, fill, title, subtitle
_ENRICH_SOURCES = [
    (3.26, BLUE_2, "USAspending", "FY obligations / TAS"),
    (4.50, BLUE_1, "Vehicle Family", "Parent / child orders"),
    (5.74, BLUE_2, "SAM.gov Subawards", "First-tier suppliers"),
    (6.98, BLUE_1, "SAM.gov Entity", "UEI / CAGE / NAICS"),
]

# x, width, fill, title, body
_ENRICH_CAVEATS = [
    (3.26, 1.74, BLUE_1, "Budget Bridge", "Reconcile FY obligations and TAS back to the procurement record."),
    (5.74, 1.74, GRAY_2, "Supplier Layer", "Lagged first-tier reporting; never add subawards to prime obligations."),
]

# y, fill, title, body
_OUTPUT_CARDS = [
    (2.90, BLUE_2, "Market Size", "Validated funded-demand spine"),
    (3.58, BLUE_1, "Opportunity Map", "Vehicles, incumbents and postings"),
    (4.26, GRAY_1, "End-User Read", "External evidence, confidence-tagged"),
]

# x, width, fill, title, body
_RULE_CARDS = [
    (0.495, 2.93, GRAY_1, "BASE PULL", "President's Budget frames funded demand; SAM.gov Contract Awards is the transaction base."),
    (3.55, 2.93, BLUE_1, "ENRICH", "USAspending bridges FY / TAS; entity and subaward records resolve vendors and first-tier suppliers."),
    (6.605, 2.93, GRAY_2, "COUNT ONCE", "Do not add vehicle ceilings, child orders, prime obligations, and subawards into one total."),
    (9.66, 3.175, BLUE_2, "VALIDATE BEFORE OUTPUT", "Tag source, vintage, measure, vehicle family, and confidence before sizing or publishing."),
]


# ── text layout commentary ────────────────────────────────────────────────────
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) controls horizontal alignment. Tight,
# explicit insets are used only for compact exhibit labels; body cards retain
# enough padding to wrap cleanly at presentation size.


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Sources and Validation"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Award Data Sourcing & Validation",
        "SAM.gov Contract Awards is the modern base pull; budget, supplier, and entity layers enrich it before validation and sizing.",
    ))

    # ── stage bands and labels ──
    for _x, _cx, _fill in _STAGE_BANDS:
        out.append(text_box(
            n(), "StageBand", IN(_x), _BAND_Y, IN(_cx), _BAND_H,
            [paragraph([])], fill=_fill, line_color="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
    for _x, _cx, _t in _STAGE_LABELS:
        out.append(text_box(
            n(), "StageLabel", IN(_x), _STAGE_LBL_Y, IN(_cx), _STAGE_LBL_H,
            [paragraph([run(_t, size=PT(9.5), bold=True, color=BLACK, font=FONT)])],
            fill=None, line_color="none", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── PULL: modern-base note ──
    out.append(text_box(
        n(), "ModernBaseNote", IN(0.64), IN(1.92), IN(2.28), IN(1.26),
        [
            paragraph([
                run("SAM.gov Contract Awards is the modern base pull.", size=PT(10.5), bold=True, color=BLACK, font=FONT),
            ], line_spacing=102000, space_after=300),
            paragraph([
                run("President's Budget frames funded demand. FPDS remains useful for legacy lineage and per-action validation, but the workflow does not depend on a feed retiring in FY2026.", size=PT(8.25), color=BLACK, font=FONT),
            ], line_spacing=100000),
        ],
        fill=None, line_color="none",
        l_ins=0, t_ins=0, r_ins=36576, b_ins=0,
    ))

    # ── numbered steps and action labels ──
    for _x, _y, _fill, _num, _action in _STEP_HEADERS:
        out.append(text_box(
            n(), "StepNumber", IN(_x), IN(_y), _STEP_W, _STEP_H,
            [paragraph([run(_num, size=PT(8.5), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=BLACK, prst="ellipse", anchor="ctr",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "StepAction", IN(_x + 0.29), IN(_y), _STEP_LBL_W, _STEP_LBL_H,
            [paragraph([run(_action, size=PT(9.25), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── ENRICH source cards ──
    for _x, _fill, _title, _subtitle in _ENRICH_SOURCES:
        out.append(text_box(
            n(), "EnrichSource", IN(_x), _ENRICH_ROW_Y, _ENRICH_CARD_W, _ENRICH_CARD_H,
            [
                paragraph([run(_title, size=PT(8.75), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
                paragraph([run(_subtitle, size=PT(7.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=_fill, line_color=BLACK, anchor="ctr",
            l_ins=40000, t_ins=24000, r_ins=40000, b_ins=24000,
        ))

    for _x, _cx, _fill, _title, _body in _ENRICH_CAVEATS:
        out.append(text_box(
            n(), "EnrichCaveat", IN(_x), _ENRICH_CAVEAT_Y, IN(_cx), _ENRICH_CAVEAT_H,
            [
                paragraph([run(_title, size=PT(8.75), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000, space_after=200),
                paragraph([run(_body, size=PT(7.25), color=BLACK, font=FONT)], align="l", line_spacing=100000),
            ],
            fill=_fill, line_color=BLACK,
            l_ins=50000, t_ins=28000, r_ins=50000, b_ins=24000,
        ))

    # source-card drops into the funded-demand spine
    out.append(connector(n(), "USABoxToCaveat", IN(3.84), IN(2.86), IN(0), IN(0.16), color=BLACK, width=6350))
    out.append(connector(n(), "USACaveatToSpine", IN(4.13), IN(3.74), IN(0), IN(0.31), color=BLACK, width=6350, arrow=True))
    out.append(connector(n(), "VehicleToSpine", IN(5.08), IN(2.86), IN(0), IN(1.19), color=BLACK, width=6350, arrow=True))
    out.append(connector(n(), "SubawardBoxToCaveat", IN(6.32), IN(2.86), IN(0), IN(0.16), color=BLACK, width=6350))
    out.append(connector(n(), "SubawardCaveatToSpine", IN(6.61), IN(3.74), IN(0), IN(0.31), color=BLACK, width=6350, arrow=True))
    out.append(connector(n(), "EntityToSpine", IN(7.56), IN(2.86), IN(0), IN(1.19), color=BLACK, width=6350, arrow=True))

    # ── PULL spine: President's Budget → SAM.gov Contract Awards ──
    out.append(text_box(
        n(), "DefineMarketSpine", IN(0.595), _SPINE_Y, IN(1.18), _SPINE_H,
        [
            paragraph([run("President's Budget", size=PT(8.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("PE / BLI and color of money", size=PT(7.25), color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=GRAY_1, line_color=BLACK, anchor="ctr",
        l_ins=40000, t_ins=24000, r_ins=40000, b_ins=24000,
    ))
    out.append(text_box(
        n(), "SAMContractAwardsSpine", IN(2.015), _SPINE_Y, IN(5.78), _SPINE_H,
        [
            paragraph([run("SAM.gov Contract Awards", size=PT(11), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("Primes, IDVs, orders / calls and ceiling", size=PT(8.75), color=WHITE, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=BLUE_3, line_color=BLACK, anchor="ctr",
        l_ins=60000, t_ins=42000, r_ins=60000, b_ins=42000,
    ))
    out.append(connector(n(), "DefineToSpine", IN(1.775), IN(4.34), IN(0.24), IN(0), color=BLACK, width=9525, arrow=True))

    # ── VALIDATE gate ──
    out.append(text_box(
        n(), "ValidationGate", IN(8.215), IN(2.28), IN(1.48), IN(2.57),
        [
            paragraph([run("Validation", size=PT(11), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=95000, space_after=400),
            paragraph([run("Tag source, vintage, measure, vehicle family, and confidence before any total is published.", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=BLUE_5, line_color=BLACK, line_width=19050, anchor="ctr",
        l_ins=50000, t_ins=30000, r_ins=50000, b_ins=26000,
    ))
    out.append(connector(n(), "SpineToGate", IN(7.795), IN(4.34), IN(0.42), IN(0), color=BLACK, width=12700, arrow=True))

    # ── FPDS legacy validation input ──
    out.append(text_box(
        n(), "FPDSLegacy", IN(5.13), _FPDS_Y, IN(2.86), _FPDS_H,
        [paragraph([run("FPDS Atom | legacy lineage and action-level validation; retiring FY2026", size=PT(7.25), bold=True, color="7F7F7F", font=FONT)], align="ctr", line_spacing=100000)],
        fill=None, line_color=BLACK, dashed_line=True, anchor="ctr",
        l_ins=35000, t_ins=12000, r_ins=35000, b_ins=12000,
    ))
    out.append(connector(n(), "FPDSToGate", IN(7.99), IN(4.83), IN(0.225), IN(0), color=BLACK, width=6350, dashed=True, arrow=True))

    # ── external program evidence ──
    out.append(text_box(
        n(), "ExternalProgramEvidence", _OUTPUT_COL_X, IN(1.92), _OUTPUT_COL_W, IN(0.72),
        [
            paragraph([run("External Program Evidence", size=PT(9), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000, space_after=200),
            paragraph([run("Contextualizes data gaps and supports end-user attribution; cite and confidence-tag every claim.", size=PT(7.5), color=BLACK, font=FONT)], align="l", line_spacing=100000),
        ],
        fill=None, line_color=BLACK, dashed_line=True,
        l_ins=50000, t_ins=26000, r_ins=50000, b_ins=24000,
    ))
    out.append(connector(n(), "ExternalEvidenceLeft", IN(9.695), IN(2.28), IN(0.405), IN(0), color=BLACK, width=6350, dashed=True, flip_h=True))
    out.append(connector(n(), "ExternalEvidenceDown", IN(9.695), IN(2.28), IN(0), IN(0.36), color=BLACK, width=6350, dashed=True, arrow=True))

    # ── OUTPUTS: gate → bus → three outputs ──
    out.append(connector(n(), "GateToOutputBus", IN(9.695), IN(3.86), IN(0.165), IN(0), color=BLACK, width=9525))
    out.append(connector(n(), "OutputBus", _OUTPUT_BUS_X, IN(3.18), IN(0), IN(1.36), color=BLACK, width=9525))

    for _y, _fill, _title, _body in _OUTPUT_CARDS:
        out.append(text_box(
            n(), "OutputCard", _OUTPUT_COL_X, IN(_y), _OUTPUT_COL_W, _OUTPUT_CARD_H,
            [
                paragraph([run(_title, size=PT(9.25), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000),
                paragraph([run(_body, size=PT(7.5), color=BLACK, font=FONT)], align="l", line_spacing=100000),
            ],
            fill=_fill, line_color=BLACK, anchor="ctr",
            l_ins=50000, t_ins=24000, r_ins=50000, b_ins=24000,
        ))

    for _y in (3.18, 3.86, 4.54):
        out.append(connector(n(), "BusToOutput", _OUTPUT_BUS_X, IN(_y), IN(0.24), IN(0), color=BLACK, width=6350, arrow=True))

    # ── compact source rules strip ──
    out.append(text_box(
        n(), "RulesLabel", IN(0.495), _RULE_LABEL_Y, IN(2.0), IN(0.18),
        [paragraph([run("KEY SOURCE RULES", size=PT(9), bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color="none", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    for _x, _cx, _fill, _title, _body in _RULE_CARDS:
        out.append(text_box(
            n(), "SourceRule", IN(_x), _RULE_Y, IN(_cx), _RULE_H,
            [
                paragraph([run(_title, size=PT(8.75), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000, space_after=300),
                paragraph([run(_body, size=PT(8.25), color=BLACK, font=FONT)], align="l", line_spacing=100000),
            ],
            fill=_fill, line_color=BLACK,
            l_ins=65000, t_ins=48000, r_ins=65000, b_ins=42000,
        ))

    return "".join(out)


def render() -> str:
    return slide(_body())
