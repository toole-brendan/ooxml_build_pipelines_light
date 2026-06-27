"""supplier_lane_method_part1 - methodology flow, part 1: build the lane, then
make the concentration-first split.

A WORKING / SME-REVIEW slide (the evidence build + primary split; the next slide
is the interpretation engine). The left pane builds the analytical unit, attaches
vendor-by-FY history, and asks ONE first routing question - recent vendor
concentration in the lane:

  BUILD  : FSRS subaward data -> in-scope PIIDs -> classify each subaward ->
           SUPPLIER LANE (Program x PIID x Work type) -> attach vendor-by-FY history.
  SPLIT  : "What is the recent vendor concentration in this lane?" (recent
           top-vendor share)
             HIGH share          -> Track A: more concentrated / incumbent-heavy
             LOWER share + active -> Track B: more diverse / multi-source
             LOW / no signal      -> Monitor, evidence-only
           Both tracks continue on the next slide; source diversification is NOT
           the first decision - it lives inside Track A as the weakening read.

The right pane carries the per-stage SME-challenge questions. Flow logic is
conceptual; live thresholds stay in the workbook. Pure deck_core primitives via
_lane_method_kit; no chart.
"""
from __future__ import annotations

from itertools import count

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, connector,
)
from deck_core.style import BLUE_1, BLUE_2, BLUE_3, WHITE

from ._lane_method_kit import (
    SECTION, PANE_X, PANE_CX, PANE_R,
    CONTEXT_FILL, CONN_PT, TITLE_STRIP_Y,
    node, title_strip, arrow, divider, sme_rail, edge_chip, legend,
)

LAYOUT = "slideLayout4"

_TOPIC = "SAM Methodology (1/2)"
_TAKEAWAY = ("Each supplier lane is built from subaward and vendor history, then "
             "split first on recent top-vendor share.")
_TOPIC_LABEL = "Building the Lane"            # breadcrumb topic (non-bold second part)

_TRACK_FILL = BLUE_2          # the two live routing tracks (continue next slide)

# Vertical gap between stacked build stages — sized so each spine connector is
# long enough to carry an arrowhead (kit MIN_ARROW = 250_000).
_SPINE_GAP = 250_000

# ── Build strip (top, left to right) ─────────────────────────────────────────
_STRIP_Y = 1_530_000
_STRIP_H = 470_000
_STRIP_B = _STRIP_Y + _STRIP_H            # 2_000_000
_STRIP_MID = _STRIP_Y + _STRIP_H // 2
_STRIP_GAP = 250_000
_STRIP_N = 3
_STRIP_W = (PANE_CX - (_STRIP_N - 1) * _STRIP_GAP) // _STRIP_N
_STRIP_PITCH = _STRIP_W + _STRIP_GAP
_PANE_MID_X = PANE_X + PANE_CX // 2

_STRIP = [
    ("FSRS subaward data", "One record = one award event"),
    ("In-scope PIIDs", "Virginia, Columbia, DDG-51"),
    ("Classify each subaward",
     "Supplier-role only; drop prime, GFE, services; assign work type"),
]

# ── Supplier-lane core band + vendor history band ────────────────────────────
_LANE_Y = _STRIP_B + _SPINE_GAP           # 2_230_000
_LANE_H = 530_000
_LANE_B = _LANE_Y + _LANE_H               # 2_760_000

_VEND_Y = _LANE_B + _SPINE_GAP            # 3_010_000
_VEND_H = 420_000
_VEND_B = _VEND_Y + _VEND_H               # 3_430_000

# ── First routing question (concentration) + three regime bands ──────────────
_GATE_Y = _VEND_B + _SPINE_GAP            # 3_680_000
_GATE_H = 410_000
_GATE_B = _GATE_Y + _GATE_H               # 4_090_000

# Left routing bus + an inset outcome stack: the gap between them is a labeled
# channel that carries each branch chip (the share condition) clear of the bands.
_BUS_X = PANE_X + 130_000                  # 583_079  (left routing rail)
_BAND_X = 1_500_000                        # outcomes inset to open the channel
_BAND_W = PANE_R - _BAND_X                 # 7_230_441
_CHIP_X = (_BUS_X + _BAND_X) // 2          # branch-chip center, in the channel

# Bands tightened (the share condition moved to the branch chip, so each band is
# a cap + one line): less box height, less dead vertical padding.
_BAND_H = 460_000
_BAND_GAP = 80_000
_BAND1_Y = _GATE_B + 100_000               # 4_190_000
_BAND2_Y = _BAND1_Y + _BAND_H + _BAND_GAP  # 4_730_000
_BAND3_Y = _BAND2_Y + _BAND_H + _BAND_GAP  # 5_270_000
_BAND3_H = 420_000                          # → 5_690_000


def _band_mid(y: int, h: int) -> int:
    return y + h // 2


# ── SME-challenge rail (right pane): per-stage question banks 1-7 ─────────────
_RAIL_GROUPS = [
    ("1. PIID scope", [
        "Right PIIDs for shipbuilder-directed work?",
        "Any submarine or DDG supplier work missing outside this lens?"]),
    ("2. Classification", [
        "Are vendor-based work-type buckets directionally fair?",
        "Should any submarine or DDG vendors be classified differently?"]),
    ("3. Lane grain", [
        "Is PIID and work type the right competitive unit?",
        "Should some lanes split by block, hull, yard, or class?"]),
    ("4. Vendor-share logic", [
        "Is dollar share the right signal of practical control?",
        "Does the recent window match how these programs buy?"]),
    ("5. Concentration cutoff", [
        "Where should high concentration begin?",
        "Is one cutoff fair across Virginia, Columbia, and DDG?"]),
    ("6. Track assignment", [
        "Does the split reflect how these lanes actually behave?",
        "Which lanes warrant a manual override?"]),
]


def _body() -> str:
    sid = count(10)
    parts: list[str] = []

    # -- connectors first (paint behind the nodes) ----------------------------
    for i in range(_STRIP_N - 1):
        x = PANE_X + i * _STRIP_PITCH + _STRIP_W
        parts.append(arrow(next(sid), f"BuildArrow{i + 1}", x, _STRIP_MID,
                           _STRIP_GAP, 0))
    # the build stack, top to bottom — each link is a flow step, so it is arrowed
    for nm, y0, y1 in [("StripToLane", _STRIP_B, _LANE_Y),
                       ("LaneToVendor", _LANE_B, _VEND_Y),
                       ("VendorToGate", _VEND_B, _GATE_Y)]:
        parts.append(arrow(next(sid), nm, _PANE_MID_X, y0, 0, y1 - y0))
    # routing rail: a bus down the left from the gate, an arrow into each band
    bands = [(_BAND1_Y, _BAND_H), (_BAND2_Y, _BAND_H), (_BAND3_Y, _BAND3_H)]
    last_mid = _band_mid(*bands[-1])
    parts.append(connector(next(sid), "RouteBus", _BUS_X, _GATE_B, 0,
                           last_mid - _GATE_B, arrow=False, color="000000",
                           width=CONN_PT))
    for i, (by, bh) in enumerate(bands):
        parts.append(arrow(next(sid), f"RouteDrop{i + 1}", _BUS_X,
                           _band_mid(by, bh), _BAND_X - _BUS_X, 0))

    # -- title strip ----------------------------------------------------------
    parts.append(title_strip(next(sid), "BuildCap", PANE_X, TITLE_STRIP_Y,
                             PANE_CX, "Build the lane, then split on concentration"))

    # -- build strip ----------------------------------------------------------
    for i, (cap, sub) in enumerate(_STRIP):
        x = PANE_X + i * _STRIP_PITCH
        parts.append(node(next(sid), f"Build{i + 1}", x, _STRIP_Y, _STRIP_W,
                          _STRIP_H, cap, sub, fill=BLUE_1))

    # -- supplier-lane core band (focal by dark BLUE_3 fill + white text; 1pt border) --
    parts.append(node(next(sid), "SupplierLane", PANE_X, _LANE_Y, PANE_CX,
                      _LANE_H, "SUPPLIER LANE",
                      ["Program × PIID × Work type",
                       "Shorthand PIID × Work type, since PIID carries program "
                       "relevance"],
                      fill=BLUE_3, txt=WHITE))

    # -- vendor-by-FY history band --------------------------------------------
    parts.append(node(next(sid), "VendorHistory", PANE_X, _VEND_Y, PANE_CX,
                      _VEND_H, "Attach vendor-by-FY history",
                      "Dollars and records by vendor; prior vs recent mix; "
                      "first and last award; active vendors; recent top-vendor "
                      "share", fill=BLUE_1))

    # -- first routing question (concentration) -------------------------------
    parts.append(node(next(sid), "ConcentrationGate", PANE_X, _GATE_Y, PANE_CX,
                      _GATE_H, "Recent vendor concentration in the lane?",
                      "The first routing split, on recent top-vendor share",
                      fill=BLUE_1))

    # -- three regime bands ---------------------------------------------------
    parts.append(node(next(sid), "TrackA", _BAND_X, _BAND1_Y, _BAND_W, _BAND_H,
                      "Track A: more concentrated, incumbent-heavy",
                      "Continues on the next slide, Track A", fill=_TRACK_FILL))
    parts.append(node(next(sid), "TrackB", _BAND_X, _BAND2_Y, _BAND_W, _BAND_H,
                      "Track B: more diverse, multi-source",
                      "Continues on the next slide, Track B", fill=_TRACK_FILL))
    parts.append(node(next(sid), "MonitorBand", _BAND_X, _BAND3_Y, _BAND_W,
                      _BAND3_H, "Monitor, evidence-only",
                      "Useful context, not a current jump-ball",
                      fill=CONTEXT_FILL))

    # -- branch chips: the share condition rides each routing tap (painted last
    #    so the white fill masks the connector under it) -----------------------
    _BRANCH = ["High share", "Lower share", "Low / none"]
    for i, (by, bh) in enumerate(bands):
        parts.append(edge_chip(next(sid), f"BranchChip{i + 1}", _CHIP_X,
                               _band_mid(by, bh), _BRANCH[i]))

    # -- pane divider + SME rail + legend -------------------------------------
    parts.append(divider(next(sid)))
    parts.append(sme_rail(sid, "SMERail", _RAIL_GROUPS))
    parts.append(legend(next(sid)))

    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
    )
