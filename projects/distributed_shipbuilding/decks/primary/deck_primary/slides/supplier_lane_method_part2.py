"""supplier_lane_method_part2 - methodology flow, part 2: downstream logic for
both concentration tracks (the interpretation engine).

A WORKING / SME-REVIEW slide. The previous slide split lanes on recent top-vendor
concentration; this one reads what each track means:

  TRACK A (concentrated): test historical DIRECTION
     A1 maintained  -> Entrenched incumbent lane (harder displacement; monitor)
     A2 weakening   -> Concentrated but diversifying (prior single -> recent
                       multi, incumbent active) - this is where source
                       diversification lives, as a sub-case of concentration.
  TRACK B (diverse): test subaward CADENCE
     B1 discrete waves -> forecast window:
            overlaps horizon -> Periodic Sourcing Opening
            not yet          -> Monitor future periodic
     B2 continuous     -> still buying and material:
            yes -> Active Continuous Sourcing Opening
            no  -> Diagnostic monitor

The right pane carries the per-stage SME-challenge questions. Flow logic is
conceptual; live thresholds stay in the workbook. Pure deck_core primitives via
_lane_method_kit; no chart.
"""
from __future__ import annotations

from itertools import count

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, connector,
)
from deck_core.style import BLUE_1, BLUE_2

from ._lane_method_kit import (
    SECTION, PANE_X, PANE_R,
    CONTEXT_FILL, CONN_PT, TITLE_STRIP_Y,
    node, title_strip, arrow, divider, sme_rail, edge_chip, legend, orthogonal_fork,
)

LAYOUT = "slideLayout4"

_TOPIC = "SAM Methodology (2/2)"
_TAKEAWAY = ("Each track is refined by a second test — direction or cadence — "
             "into a specific opening or monitor read.")
_TOPIC_LABEL = "Concentration Tracks"        # breadcrumb topic (non-bold second part)

_TRACK_FILL = BLUE_2          # the two routing tracks (carried in from part 1)

# ── Enter banner (full width) ────────────────────────────────────────────────
_PANE_MID_X = PANE_X + (PANE_R - PANE_X) // 2     # 4_591_760
_ENTER_Y = 1_580_000
_ENTER_H = 400_000
_ENTER_B = _ENTER_Y + _ENTER_H                    # 1_980_000
_ENTER_FORK_Y = 2_070_000                         # Enter → headers rail (orthogonal)

# ── Two track columns ────────────────────────────────────────────────────────
_TA_X = PANE_X                                     # 453_079
_TA_W = 3_620_000
_TA_R = _TA_X + _TA_W                              # 4_073_079
_TA_MID = _TA_X + _TA_W // 2                       # 2_263_079

_TB_X = _TA_R + 250_000                            # 4_323_079
_TB_W = PANE_R - _TB_X                             # 4_407_362
_TB_MID = _TB_X + _TB_W // 2                       # 6_526_760

_SPINE_GAP = 250_000          # header → test gap, long enough for an arrowhead

_HDR_Y = 2_190_000
_HDR_H = 440_000
_HDR_B = _HDR_Y + _HDR_H                           # 2_630_000

_TEST_Y = _HDR_B + _SPINE_GAP                       # 2_880_000
_TEST_H = 440_000
_TEST_B = _TEST_Y + _TEST_H                        # 3_320_000

# Track A: left bus -> two stacked outcomes, inset right to open a labeled chip
# channel (the direction condition rides the tap, clear of the outcome boxes).
_A_BUS_X = _TA_X + 120_000                          # 573_079
_A_OUT_X = _TA_X + 980_000                          # 1_433_079
_A_OUT_W = _TA_R - _A_OUT_X                         # 2_640_000
_A_CHIP_X = (_A_BUS_X + _A_OUT_X) // 2              # direction chip, in the channel
_A1_Y, _A1_H = 3_480_000, 900_000                  # entrenched   -> 4_380_000
_A2_Y, _A2_H = 4_460_000, 1_020_000                # diversifying -> 5_480_000
_A1_MID = _A1_Y + _A1_H // 2                        # 3_930_000
_A2_MID = _A2_Y + _A2_H // 2                        # 4_970_000

# Track B: cadence fork -> two sub-columns, each a bus -> two stacked outcomes
_BSUB_GAP = 40_000
_BSUB_W = (_TB_W - _BSUB_GAP) // 2                  # 2_183_681
_B1_X = _TB_X                                        # 4_323_079
_B1_MID = _B1_X + _BSUB_W // 2                       # 5_414_919
_B2_X = _TB_X + _BSUB_W + _BSUB_GAP                 # 6_546_760
_B2_MID = _B2_X + _BSUB_W // 2                       # 7_638_600

_B_FORK_Y = 3_420_000                               # cadence-test → sub-headers rail
_SUB_Y = 3_700_000
_SUB_H = 380_000
_SUB_B = _SUB_Y + _SUB_H                             # 4_080_000

_BOUT_H = 640_000
_BOUT1_Y = 4_180_000                                # -> 4_820_000
_BOUT2_Y = 4_900_000                                # -> 5_540_000
_BOUT1_MID = _BOUT1_Y + _BOUT_H // 2               # 4_500_000
_BOUT2_MID = _BOUT2_Y + _BOUT_H // 2               # 5_220_000


def _sub_bus_x(col_x: int) -> int:
    return col_x + 120_000


def _sub_out_x(col_x: int) -> int:
    return col_x + 370_000


def _sub_out_w(col_x: int) -> int:
    return (col_x + _BSUB_W) - _sub_out_x(col_x)    # 1_451_181


# ── SME-challenge rail (right pane): question banks A-I ───────────────────────
_RAIL_GROUPS = [
    ("1. Overall reasonableness", [
        "Does concentration-first feel like the right organizing logic?",
        "Is this the best way to frame the opportunity?"]),
    ("2. Concentrated track", [
        "Does high reported share mean lock-up, or normal specialization?"]),
    ("3. Maintained dominance", [
        "A real opening, or just an incumbent map? What moves it to pursue?"]),
    ("4. Weakening dominance", [
        "Declining share: buyer diversification, or program phase and mix?"]),
    ("5. Diversification proof", [
        "A true split, or a rename or FSRS artifact? Does incumbent-active "
        "prove it?"]),
    ("6. Diverse track", [
        "Substitutable competition, or work split by component or yard?"]),
    ("7. Periodic cadence", [
        "Real sourcing waves, and is the forecast window useful for planning?"]),
    ("8. Continuous sourcing", [
        "Always-on lanes easier to enter, or harder with embedded incumbents?"]),
]


def _body() -> str:
    sid = count(10)
    parts: list[str] = []

    # -- connectors first (paint behind the nodes) ----------------------------
    # Enter -> the two track headers: a right-angled fan-out (never diagonal)
    parts.extend(orthogonal_fork(sid, "EnterFork", _PANE_MID_X, _ENTER_B,
                                 _ENTER_FORK_Y, [_TA_MID, _TB_MID], _HDR_Y))
    # header -> test, each column — arrowed flow step
    for nm, mid in [("AHdrToTest", _TA_MID), ("BHdrToTest", _TB_MID)]:
        parts.append(arrow(next(sid), nm, mid, _HDR_B, 0, _TEST_Y - _HDR_B))
    # Track A test -> bus -> A1 / A2
    parts.append(connector(next(sid), "ABus", _A_BUS_X, _TEST_B, 0,
                           _A2_MID - _TEST_B, arrow=False, color="000000",
                           width=CONN_PT))
    parts.append(arrow(next(sid), "ABusToA1", _A_BUS_X, _A1_MID,
                       _A_OUT_X - _A_BUS_X, 0))
    parts.append(arrow(next(sid), "ABusToA2", _A_BUS_X, _A2_MID,
                       _A_OUT_X - _A_BUS_X, 0))
    # Track B test -> the two sub-headers: another right-angled fan-out
    parts.extend(orthogonal_fork(sid, "BFork", _TB_MID, _TEST_B, _B_FORK_Y,
                                 [_B1_MID, _B2_MID], _SUB_Y))
    # each B sub-column: bus -> two stacked outcomes
    for tag, col_x in [("B1", _B1_X), ("B2", _B2_X)]:
        bx = _sub_bus_x(col_x)
        ox = _sub_out_x(col_x)
        parts.append(connector(next(sid), f"{tag}Bus", bx, _SUB_B, 0,
                               _BOUT2_MID - _SUB_B, arrow=False, color="000000",
                               width=CONN_PT))
        parts.append(arrow(next(sid), f"{tag}BusToOut1", bx, _BOUT1_MID,
                           ox - bx, 0))
        parts.append(arrow(next(sid), f"{tag}BusToOut2", bx, _BOUT2_MID,
                           ox - bx, 0))

    # -- title strip ----------------------------------------------------------
    parts.append(title_strip(next(sid), "FlowCap", PANE_X, TITLE_STRIP_Y,
                             PANE_R - PANE_X, "What each concentration track means"))

    # -- enter banner ---------------------------------------------------------
    parts.append(node(next(sid), "Enter", PANE_X, _ENTER_Y, PANE_R - PANE_X,
                      _ENTER_H, "Enter from the previous slide",
                      "Recent top-vendor concentration set the track",
                      fill=CONTEXT_FILL))

    # -- Track A: header, direction test, two outcomes ------------------------
    parts.append(node(next(sid), "TrackAHdr", _TA_X, _HDR_Y, _TA_W, _HDR_H,
                      "Track A: concentrated, incumbent-heavy",
                      "High recent top-vendor share", fill=_TRACK_FILL))
    parts.append(node(next(sid), "ATest", _TA_X, _TEST_Y, _TA_W, _TEST_H,
                      "Test historical direction", "Maintained, or weakening?",
                      fill=BLUE_1))
    parts.append(node(next(sid), "A1Entrenched", _A_OUT_X, _A1_Y, _A_OUT_W,
                      _A1_H, "A1. Entrenched incumbent",
                      ["Same supplier dominant; no credible second source",
                       "Harder displacement; useful for targeting, not proof "
                       "the door is open"], fill=CONTEXT_FILL))
    parts.append(node(next(sid), "A2Diversifying", _A_OUT_X, _A2_Y, _A_OUT_W,
                      _A2_H, "A2. Concentrated but diversifying",
                      ["Share declining; prior single → recent multi, incumbent "
                       "active", "Better than pure dominance: supplier-base "
                       "movement already visible"], fill=CONTEXT_FILL))

    # -- Track B: header, cadence test, two sub-branches ----------------------
    parts.append(node(next(sid), "TrackBHdr", _TB_X, _HDR_Y, _TB_W, _HDR_H,
                      "Track B: diverse, multi-source",
                      "Lower top-vendor share; enough active vendors",
                      fill=_TRACK_FILL))
    parts.append(node(next(sid), "BTest", _TB_X, _TEST_Y, _TB_W, _TEST_H,
                      "Test subaward cadence", "Periodic, or continuous?",
                      fill=BLUE_1))
    parts.append(node(next(sid), "B1Hdr", _B1_X, _SUB_Y, _BSUB_W, _SUB_H,
                      "B1. Discrete waves", "Forecast window from quiet gaps",
                      fill=BLUE_1))
    parts.append(node(next(sid), "B2Hdr", _B2_X, _SUB_Y, _BSUB_W, _SUB_H,
                      "B2. Continuous stream", "Activity over a forecast date",
                      fill=BLUE_1))
    # B1 outcomes
    parts.append(node(next(sid), "PeriodicOpening", _sub_out_x(_B1_X), _BOUT1_Y,
                      _sub_out_w(_B1_X), _BOUT_H, "Periodic Sourcing Opening",
                      "Window overlaps the horizon", fill=CONTEXT_FILL))
    parts.append(node(next(sid), "MonitorPeriodic", _sub_out_x(_B1_X), _BOUT2_Y,
                      _sub_out_w(_B1_X), _BOUT_H, "Monitor future periodic",
                      "Good lane, not timed yet", fill=CONTEXT_FILL))
    # B2 outcomes
    parts.append(node(next(sid), "ContinuousOpening", _sub_out_x(_B2_X), _BOUT1_Y,
                      _sub_out_w(_B2_X), _BOUT_H, "Active Continuous Opening",
                      "Ongoing access, not scheduled", fill=CONTEXT_FILL))
    parts.append(node(next(sid), "DiagnosticMonitor", _sub_out_x(_B2_X), _BOUT2_Y,
                      _sub_out_w(_B2_X), _BOUT_H, "Diagnostic monitor",
                      "Pattern exists, opening weak", fill=CONTEXT_FILL))

    # -- branch chips: direction (Track A) and cadence (Track B) ride the edges;
    #    painted last so the white fill masks the connector under them ----------
    parts.append(edge_chip(next(sid), "AChipMaintained", _A_CHIP_X, _A1_MID,
                           "Maintained", w=800_000, place="above"))
    parts.append(edge_chip(next(sid), "AChipWeakening", _A_CHIP_X, _A2_MID,
                           "Weakening", w=800_000, place="above"))
    _B_FORK_MID_Y = (_B_FORK_Y + _SUB_Y) // 2
    parts.append(edge_chip(next(sid), "BChipPeriodic", _B1_MID, _B_FORK_MID_Y,
                           "Periodic"))
    parts.append(edge_chip(next(sid), "BChipContinuous", _B2_MID, _B_FORK_MID_Y,
                           "Continuous"))

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
