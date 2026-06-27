"""award_data_sourcing — US Defense Market Strategy deck (20260626), source slide 33.

EXHIBIT — "Award Data Sourcing": SAM.gov Contract Awards anchors the data pull;
funding and subaward layers enrich it, and validation precedes any total. The
exhibit is a left-to-right methodology workflow set on a four-stage band —
PULL · ENRICH · VALIDATE · OUTPUTS. President's Budget and SAM.gov Contract
Awards form the funded-demand spine; USAspending, vehicle families, SAM.gov
subawards and entity records enrich it. Numbered step chips (1 Define … 7
Validate) and arrow connectors wire the stages into a validation gate that
feeds three output cards (Market Size · Opportunity Map · End-User Read), with
FPDS Atom and external program evidence drawn dashed as supporting/legacy
inputs. A supporting table restates each source as role / question / caveat /
output. This is a preliminary methodology slide.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............. breadcrumb() + prelim_chip() + title_placeholder()
  • _STAGE_BANDS ....... 3 colour bands behind PULL / ENRICH / VALIDATE
  • _STAGE_LABELS ...... 4 stage names on the band (PULL / ENRICH / VALIDATE / OUTPUTS)
  • anchor note ........ "ModernBaseNote" — modern base pull = SAM.gov Contract Awards
  • _STEP_NUMBERS ...... 7 numbered ellipse chips (1–7) on the workflow
  • _STEP_ACTIONS ...... 7 action verbs beside the chips (Define / Pull / Add / …)
  • ENRICH cards ....... USAspending · Vehicle Family · SAM.gov Subawards · SAM.gov
                        Entity, plus Budget-Bridge / Supplier-Layer caveat cards
  • enrich connectors .. 6 drop/arrow connectors from the cards down to the spine
  • PULL spine ......... President's Budget → SAM.gov Contract Awards + Define arrow
  • VALIDATE gate ...... Validation box + spine→gate arrow
  • FPDS legacy ........ dashed FPDS-Atom note + dashed connector (retiring FY2026)
  • external evidence .. dashed External-Program-Evidence box + 2 dashed connectors
  • OUTPUTS ............ gate → output bus → Market Size / Opportunity Map /
                        End-User Read cards (3 branch arrows)
  • supporting table ... native table(): source × role × question × caveat × output

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=15, connector=16, table=1, chrome_builders=3,
clusters=4 (covering 21 shapes), dropped=1 (think-cell OLE frame).
Post-conversion edit: the source's top-right "WIP" chip — already at the house
position with house styling — was promoted to the house prelim_chip() builder
and relabeled "Preliminary" (the converter had kept it verbatim only because its
"WIP" text didn't match the chrome detector).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, table, trow, tcell,
    breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates; values unchanged from the raw port) ──
_BAND_Y, _BAND_H = IN(1.752), IN(1.91)             # stage-band top / height        [x3]
_STAGE_LBL_Y, _STAGE_LBL_H = IN(1.752), IN(0.14)   # stage-name label top / height  [x4]
_STEP_W, _STEP_H = IN(0.18), IN(0.18)              # numbered step chip (ellipse)   [x7]
_STEP_LBL_W, _STEP_LBL_H = IN(0.82), IN(0.18)      # step action-label box          [x7]
_ENRICH_ROW_Y = IN(2.278)    # enrich source-card top; also external-evidence connector start [x6]
_ENRICH_CARD_W = IN(1.12)    # enrich source-card width                [x4]
_ENRICH_CARD_H = IN(0.335)   # enrich source-card height               [x4]
_ENRICH_DROP_Y = IN(2.613)   # enrich-card bottom edge; drop connectors start here  [x4]
_ARROW_RUN = IN(0.24)        # short horizontal arrow run (Define→spine + 3 bus→output) [x4]
_SHORT_SPAN = IN(0.3)        # heterogeneous: FPDS→gate stub length + 3 output-card heights [x4]
_OUTPUT_COL_X = IN(10.115)   # outputs-column left x (evidence box + 3 output cards) [x4]
_OUTPUT_COL_W = IN(2.639)    # outputs-column card width                [x4]
_OUTPUT_BUS_X = IN(9.875)    # output-bus vertical x + its 3 branch starts          [x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three colour bands behind the PULL / ENRICH / VALIDATE stages (the OUTPUTS
#   stage has no band).
_STAGE_BANDS = [    # (x, cx, fill) x3 — workflow stage background bands
    (0.495, 2.65, "F2F2F2"),   # GRAY_1
    (3.145, 5, "E2E9EF"),   # BLUE_1
    (8.145, 1.55, "B6C8D8"),   # BLUE_2
]

# local_meaning: the four workflow-band stage names (PULL / ENRICH / VALIDATE / OUTPUTS).
_STAGE_LABELS = [    # (x, cx, label) x4 — stage names along the workflow band
    (0.575, 0.65, "PULL"),
    (3.225, 0.75, "ENRICH"),
    (8.225, 0.88, "VALIDATE"),
    (10.125, 0.75, "OUTPUTS"),
]

# local_meaning: the seven numbered step chips (1–7) on the workflow; step 7 is the validation
#   gate. fill is a per-row field.
_STEP_NUMBERS = [    # (x, y, fill, label) x7 — numbered step chips (ellipses)
    (3.375, 2.043, "6E91B1", "3"),   # BLUE_3
    (4.595, 2.043, "6E91B1", "4"),   # BLUE_3
    (5.815, 2.043, "6E91B1", "5"),   # BLUE_3
    (7.035, 2.043, "6E91B1", "6"),   # BLUE_3
    (0.695, 2.838, "6E91B1", "1"),   # BLUE_3
    (2.115, 2.838, "6E91B1", "2"),   # BLUE_3
    (8.335, 2.398, "263746", "7"),   # BLUE_5
]

# local_meaning: the seven action verbs beside the numbered chips (Define / Pull / Add / Link /
#   Resolve / Validate).
_STEP_ACTIONS = [    # (x, y, label) x7 — action label beside each numbered chip
    (3.59, 2.043, "Add"),
    (4.81, 2.043, "Link"),
    (6.03, 2.043, "Pull"),
    (7.25, 2.043, "Resolve"),
    (0.91, 2.838, "Define"),
    (2.33, 2.838, "Pull"),
    (8.55, 2.398, "Validate"),
]

# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome: breadcrumb + Preliminary chip + title ──
    out.append(breadcrumb("Market Sizing", "Sources and Validation"))
    out.append(prelim_chip())
    out.append(title_placeholder("Award Data Sourcing", "SAM.gov Contract Awards anchors the pull; funding and subaward layers enrich it, and validation precedes any total."))
    # ── workflow band: stage background bands ──
    for _x, _cx, _fill in _STAGE_BANDS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _BAND_Y, IN(_cx), _BAND_H, [paragraph([])], fill=_fill, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # ── workflow band: stage names (PULL / ENRICH / VALIDATE / OUTPUTS) ──
    for _x, _cx, _t in _STAGE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _STAGE_LBL_Y, IN(_cx), _STAGE_LBL_H, [paragraph([run(_t, size=PT(8), bold=True, color="000000", font=FONT)])], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # ── anchor note: modern base pull = SAM.gov Contract Awards ──
    out.append(text_box(n(), "ModernBaseNote", IN(0.615), IN(1.932), IN(2.38), IN(0.74), [paragraph([run("The modern base pull is SAM.gov Contract Awards.", size=PT(9), bold=True, color="000000", font=FONT)], line_spacing=102000), paragraph([run("FPDS remains useful for legacy lineage and per-action validation; the workflow does not depend on a feed slated to retire in FY2026.", size=PT(7.5), color="000000", font=FONT)], line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=36576, b_ins=0))   # BLACK
    # ── numbered step chips (1–7) ──
    for _x, _y, _fill, _t in _STEP_NUMBERS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _STEP_W, _STEP_H, [paragraph([run(_t, size=PT(7), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="000000", prst="ellipse", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # ── step action labels (beside the chips) ──
    for _x, _y, _t in _STEP_ACTIONS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _STEP_LBL_W, _STEP_LBL_H, [paragraph([run(_t, size=PT(8), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # ── ENRICH layer: source cards (USAspending / Vehicle Family / Subawards / Entity) ──
    out.append(text_box(n(), "USAspending", IN(3.275), _ENRICH_ROW_Y, _ENRICH_CARD_W, _ENRICH_CARD_H, [paragraph([run("USAspending", size=PT(7.5), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("FY obligations, TAS", size=PT(6.5), color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="B6C8D8", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_2
    out.append(text_box(n(), "VehicleFamilies", IN(4.495), _ENRICH_ROW_Y, _ENRICH_CARD_W, _ENRICH_CARD_H, [paragraph([run("Vehicle Family", size=PT(7.5), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Parent/child orders", size=PT(6.5), color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="E2E9EF", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_1
    out.append(text_box(n(), "Subawards", IN(5.715), _ENRICH_ROW_Y, _ENRICH_CARD_W, _ENRICH_CARD_H, [paragraph([run("SAM.gov Subawards", size=PT(7.5), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("First-tier suppliers", size=PT(6.5), color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="B6C8D8", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_2
    out.append(text_box(n(), "EntityManagement", IN(6.935), _ENRICH_ROW_Y, _ENRICH_CARD_W, _ENRICH_CARD_H, [paragraph([run("SAM.gov Entity", size=PT(7.5), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("UEI / CAGE / NAICS", size=PT(6.5), color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="E2E9EF", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_1
    # ── ENRICH caveat cards (Budget Bridge / Supplier Layer) ──
    out.append(text_box(n(), "USAspendingComment", IN(3.275), IN(2.658), IN(1.55), IN(0.395), [paragraph([run("Budget Bridge", size=PT(7.75), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000), paragraph([run("FY obligations and TAS; reconcile to SAM.gov.", size=PT(6.25), color="000000", font=FONT)], align="l", line_spacing=100000)], fill="E2E9EF", line_color="000000", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_1
    out.append(text_box(n(), "SubawardComment", IN(5.715), IN(2.658), IN(1.55), IN(0.395), [paragraph([run("Supplier Layer", size=PT(6.75), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000), paragraph([run("Lagged first-tier only; never add to primes.", size=PT(6), color="000000", font=FONT)], align="l", line_spacing=100000)], fill="D9D9D9", line_color="000000", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # GRAY_2
    # ── connectors: enrich cards → funded-demand spine ──
    out.append(connector(n(), "USABoxToCard", IN(3.835), _ENRICH_DROP_Y, IN(0), IN(0.045), color="000000", width=6350))   # BLACK
    out.append(connector(n(), "USACardToSpine", IN(3.835), IN(3.053), IN(0), IN(0.02), color="000000", width=6350, arrow=True))   # BLACK
    out.append(connector(n(), "VehicleToSpine", IN(5.055), _ENRICH_DROP_Y, IN(0), IN(0.46), color="000000", width=6350, arrow=True))   # BLACK
    out.append(connector(n(), "SubawardBoxToCard", IN(6.275), _ENRICH_DROP_Y, IN(0), IN(0.045), color="000000", width=6350))   # BLACK
    out.append(connector(n(), "SubawardCardToSpine", IN(6.275), IN(3.053), IN(0), IN(0.02), color="000000", width=6350, arrow=True))   # BLACK
    out.append(connector(n(), "EntityToSpine", IN(7.495), _ENRICH_DROP_Y, IN(0), IN(0.46), color="000000", width=6350, arrow=True))   # BLACK
    # ── PULL spine: President's Budget → SAM.gov Contract Awards ──
    out.append(text_box(n(), "DefineMarketSpine", IN(0.595), IN(3.073), IN(1.18), IN(0.34), [paragraph([run("President's Budget", size=PT(7.5), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("PE/BLI and money color", size=PT(6.5), color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="F2F2F2", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # GRAY_1
    out.append(text_box(n(), "SAMContractAwardsSpine", IN(2.015), IN(3.073), IN(5.78), IN(0.34), [paragraph([run("SAM.gov Contract Awards", size=PT(9), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Primes, IDVs, orders/calls and ceiling", size=PT(7.75), color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="6E91B1", line_color="000000", anchor="ctr", l_ins=60000, t_ins=35000, r_ins=60000, b_ins=35000))   # BLUE_3
    out.append(connector(n(), "DefineToSpine", IN(1.775), IN(3.243), _ARROW_RUN, IN(0), color="000000", width=9525, arrow=True))   # BLACK
    # ── VALIDATE gate ──
    out.append(text_box(n(), "ValidationGate", IN(8.215), IN(2.633), IN(1.48), IN(0.96), [paragraph([run("Validation", size=PT(9), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=95000), paragraph([run("Tag source, vintage, measure, family and confidence", size=PT(5.6), color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="263746", line_color="000000", line_width=19050, anchor="ctr", l_ins=45000, t_ins=22000, r_ins=45000, b_ins=18000))   # BLUE_5
    out.append(connector(n(), "SpineToGate", IN(7.795), IN(3.243), IN(0.42), IN(0), color="000000", width=12700, arrow=True))   # BLACK
    # ── FPDS legacy validation (dashed; retiring FY2026) ──
    out.append(text_box(n(), "FPDSLegacy", IN(5.215), IN(3.423), IN(2.7), IN(0.22), [paragraph([run("FPDS Atom | legacy lineage and validation; retiring FY2026", size=PT(6.5), bold=True, color="7F7F7F", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="000000", dashed_line=True, anchor="ctr", l_ins=35000, t_ins=8000, r_ins=35000, b_ins=8000))   # BLACK
    out.append(connector(n(), "FPDSToGate", IN(7.915), IN(3.533), _SHORT_SPAN, IN(0), color="000000", width=6350, dashed=True, arrow=True))   # BLACK
    # ── external program evidence (dashed) ──
    out.append(text_box(n(), "ExternalProgramEvidence", _OUTPUT_COL_X, IN(2.043), _OUTPUT_COL_W, IN(0.47), [paragraph([run("External Program Evidence", size=PT(7.5), bold=True, font=FONT)], align="l", line_spacing=100000), paragraph([run("Anecdotal color to contextualize data / explain possible gaps.", size=PT(6.5), font=FONT)], align="l", line_spacing=100000)], fill=None, line_color="000000", dashed_line=True, l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLACK
    out.append(connector(n(), "ExternalEvidenceLeft", IN(8.955), _ENRICH_ROW_Y, IN(1.16), IN(0), color="000000", width=6350, dashed=True, flip_h=True))   # BLACK
    out.append(connector(n(), "ExternalEvidenceDown", IN(8.955), _ENRICH_ROW_Y, IN(0), IN(0.355), color="000000", width=6350, dashed=True, arrow=True))   # BLACK
    # ── OUTPUTS: gate → output bus → Market Size / Opportunity Map / End-User Read ──
    out.append(connector(n(), "GateToOutputBus", IN(9.695), IN(3.113), IN(0.18), IN(0), color="000000", width=9525))   # BLACK
    out.append(connector(n(), "OutputBus", _OUTPUT_BUS_X, IN(2.713), IN(0), IN(0.67), color="000000", width=9525))   # BLACK
    out.append(text_box(n(), "MarketOutput", _OUTPUT_COL_X, IN(2.563), _OUTPUT_COL_W, _SHORT_SPAN, [paragraph([run("Market Size", size=PT(7.5), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000), paragraph([run("Funded-demand spine", size=PT(6.5), color="000000", font=FONT)], align="l", line_spacing=100000)], fill="B6C8D8", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_2
    out.append(text_box(n(), "OpportunityOutput", _OUTPUT_COL_X, IN(2.903), _OUTPUT_COL_W, _SHORT_SPAN, [paragraph([run("Opportunity Map", size=PT(7.5), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000), paragraph([run("SAM.gov Opportunities, vehicles and incumbents", size=PT(6.5), color="000000", font=FONT)], align="l", line_spacing=100000)], fill="E2E9EF", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # BLUE_1
    out.append(text_box(n(), "EndUserOutput", _OUTPUT_COL_X, IN(3.233), _OUTPUT_COL_W, _SHORT_SPAN, [paragraph([run("End-User Read", size=PT(7.5), bold=True, color="000000", font=FONT)], align="l", line_spacing=100000), paragraph([run("External evidence, confidence-tagged", size=PT(6.5), color="000000", font=FONT)], align="l", line_spacing=100000)], fill="F2F2F2", line_color="000000", anchor="ctr", l_ins=40000, t_ins=18000, r_ins=40000, b_ins=18000))   # GRAY_1
    out.append(connector(n(), "BusToMarket", _OUTPUT_BUS_X, IN(2.713), _ARROW_RUN, IN(0), color="000000", width=6350, arrow=True))   # BLACK
    out.append(connector(n(), "BusToOpportunity", _OUTPUT_BUS_X, IN(3.053), _ARROW_RUN, IN(0), color="000000", width=6350, arrow=True))   # BLACK
    out.append(connector(n(), "BusToEndUser", _OUTPUT_BUS_X, IN(3.383), _ARROW_RUN, IN(0), color="000000", width=6350, arrow=True))   # BLACK
    # ── supporting table: source × role × question × caveat × output ──
    # Table layout: col_widths fix the five columns (source / role / question /
    # caveat / output) and trow(h=...) each row minimum; cells repeat the
    # L/R-borderless rule convention, and the caveat / output columns carry the
    # F2F2F2 / E2E9EF fills.
    # Rule/text palette: text 000000 (BLACK); all rules 000000 (BLACK), widths 19050 (header) / 12700.
    out.append(table(n(), "SourceRoleLegend", IN(0.495), IN(3.939), IN(12.339), IN(2.67), col_widths=[IN(1.92), IN(1.55), IN(3), IN(3.25), IN(2.619)], rows=[
        trow([tcell("Source", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 19050}}), tcell("Role in workflow", size=PT(8.75), bold=True, color="000000", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 19050}}), tcell("Question being answered", size=PT(8.75), bold=True, color="000000", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 19050}}), tcell("Caveat / rule", size=PT(8.75), bold=True, color="000000", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 19050}}), tcell("Output", size=PT(8.75), bold=True, color="000000", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 19050}})], h=IN(0.246)),
        trow([tcell("President's Budget / justification (P-1, R-1)", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 19050}, "B": {"color": "000000", "width": 12700}}), tcell("Forward funding", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 19050}, "B": {"color": "000000", "width": 12700}}), tcell("Funded by account, PE/BLI, color of money?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 19050}, "B": {"color": "000000", "width": 12700}}), tcell("Budget lines do not map to NAICS/PSC or vendors", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 19050}, "B": {"color": "000000", "width": 12700}}), tcell("Funded-demand spine", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 19050}, "B": {"color": "000000", "width": 12700}})], h=IN(0.392)),   # GRAY_1, BLUE_1
        trow([tcell("SAM Contract Awards", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Prime and vehicle pull", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Awards/IDVs; parent-child structure; ceilings?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Do not double-count vehicle and child orders; tag coverage", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Vehicle, incumbent and capacity map", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}})], h=IN(0.392)),   # GRAY_1, BLUE_1
        trow([tcell("USAspending", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Budget bridge", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Transaction FY obligations; funding TAS?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Reconcile to procurement record; fields differ", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("TAS bridge and FY view", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}})], h=IN(0.246)),   # GRAY_1, BLUE_1
        trow([tcell("SAM Subaward Reporting", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("First-tier supplier layer", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Which reported suppliers sit under a prime?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Lagged/incomplete; separate from prime obligations", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Supplier and workshare map", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}})], h=IN(0.246)),   # GRAY_1, BLUE_1
        trow([tcell("SAM enrichment sources", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Resolve and pipeline", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("UEI/CAGE/NAICS; what is posted pre-award?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Registration/posting does not prove program relevance or award", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Vendor segments and watchlist", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}})], h=IN(0.392)),   # GRAY_1, BLUE_1
        trow([tcell("FPDS Atom feed", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Legacy validation", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("What does the older action feed show?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Not the future base; retiring FY2026", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}}), tcell("Lineage validation", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "000000", "width": 12700}})], h=IN(0.246)),   # GRAY_1, BLUE_1
        trow([tcell("External program evidence", size=PT(8.75), bold=True, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": "none"}), tcell("End-user attribution", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": "none"}), tcell("Who requires, tests, or fields the capability?", size=PT(8.75), color="000000", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": "none"}), tcell("Cite and confidence-tag; place of performance is not proof", size=PT(8.75), color="000000", fill="F2F2F2", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": "none"}), tcell("End-user map", size=PT(8.75), bold=True, color="000000", fill="E2E9EF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": "none"})], h=IN(0.392)),   # GRAY_1, BLUE_1
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
