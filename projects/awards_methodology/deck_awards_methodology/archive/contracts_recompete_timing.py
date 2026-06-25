"""contracts_recompete_timing - a vehicle's structure encodes a recompete clock,
and the clock is only the timing leg of re-competability.

Body / schematic slide: a horizontal-time swim-lane map (one lane per vehicle
archetype) whose recompete tick deliberately falls short of the child-order
performance tail, an ADDRESSABLE? gate every expiring lane must pass, a
per-vehicle clock-rule table, opportunity-state chips, and a caveat rail.

Style + chrome rules: deck_core/slide_guide.md. Built from the imported
deck_core builders (text_box / house_table / connector / run / paragraph) plus
slide-local `_`-prefixed helpers; geometry is explicit because the schematic is
hand-laid, not a placeholder grid.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4,
    GRAY_1, GRAY_3, GRAY_4, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_CHIP,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, MESSAGE_11PT, BADGE_16PT,
)
from deck_core import text_metrics

LAYOUT = "slideLayout4"   # body slide; auto-numbers

# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION  = "Contracts"
_TOPIC    = "Recompete Timing"
_TAKEAWAY = ("A vehicle's last date to order sets the recompete clock, not its "
             "last task order's end date.")
_SOURCES  = ("Sources: SAM.gov Contract Awards API (ordering and option dates); "
             "FAR 16.505, 16.703, 17.207; internal Army Market Mapping workbook "
             "(Timing and Incumbent Screen), FPDS for lineage | "
             "Note: figures illustrative of method; as of 2026-06-22")


# ════════════════════════════════════════════════════════════════════════════
# Geometry
# ════════════════════════════════════════════════════════════════════════════
# Vertical bands of BODY, top to bottom: Commentary 1 (left) + table (right) ->
# schematic (left) + ADDRESSABLE gate + guardrail card (right) -> chip row ->
# caveat rail.

_GAP        = 160_000
_RAIL_W     = 3_560_000
_RAIL_X     = BODY_R - _RAIL_W                       # 8_175_441
_LEFT_X     = BODY_X
_LEFT_W     = _RAIL_X - _GAP - _LEFT_X               # 7_562_362

# bottom bands
_CAV_H      = 440_000
_CAV_Y      = BODY_B - _CAV_H                        # 5_430_000
_CHIP_H     = 360_000
_CHIP_Y     = _CAV_Y - 60_000 - _CHIP_H             # 5_010_000
_MAIN_B     = _CHIP_Y - 70_000                       # 4_940_000  main band floor

# left zone: commentary 1 then schematic
_C1_Y       = BODY_Y
_C1_H       = 620_000
_SCH_X      = _LEFT_X
_SCH_Y      = _C1_Y + _C1_H + 40_000                 # 2_031_600

# schematic internals
_LANE_LABEL_W = 1_560_000
_PLOT_X     = _SCH_X + _LANE_LABEL_W                 # 2_013_079
_PLOT_R     = 6_700_000
_PLOT_W     = _PLOT_R - _PLOT_X                       # 4_686_921
_AXIS_Y     = _SCH_Y                                  # axis / TODAY label row
_LANES_Y    = _SCH_Y + 300_000                        # 2_331_600
_LANE_PITCH = (_MAIN_B - _LANES_Y) // 5               # ~521_680

# ADDRESSABLE gate (single dark focal object) - right edge of the left zone
_GATE_W     = 900_000
_GATE_X     = _LEFT_X + _LEFT_W - _GATE_W            # 7_115_441
_GATE_Y     = _LANES_Y
_GATE_H     = _MAIN_B - _LANES_Y

_TODAY_FRAC = 0.18


def _x(frac: float) -> int:
    """Fraction of plot width -> absolute EMU x."""
    return int(_PLOT_X + frac * _PLOT_W)


class _Id:
    def __init__(self, start: int = 10):
        self.n = start

    def __call__(self) -> int:
        v = self.n
        self.n += 1
        return v


# ── slide-local helpers ──────────────────────────────────────────────────────

def _label(gid, x, y, cx, cy, runs, *, align="l", anchor="t", insets=INSETS_NONE):
    """No-fill, no-border text label (commentary / caption / tick note)."""
    return text_box(gid(), "label", x, y, cx, cy,
                    [paragraph(runs, align=align)],
                    anchor=anchor, fill=None, insets=insets)


def _rect(gid, x, y, cx, cy, *, line_color=BLACK, width=12_700, dashed=False,
          fill=None):
    """Outline-only (or filled) rectangle with no text - lane bar geometry."""
    return text_box(gid(), "bar", x, y, cx, cy, [paragraph([])],
                    fill=fill, line_color=line_color, line_width=width,
                    dashed_line=dashed, insets=INSETS_NONE)


# ── lane data ────────────────────────────────────────────────────────────────
# Each lane: parent base + (optional) dashed option span ending at the recompete
# tick; a lighter nested child-order bar whose RIGHT edge runs PAST the tick
# (the gap is the argument). Ticks intentionally do not line up across lanes.
_LANES = [
    # label,                          base,          option,        tick,  child
    ("Standalone definitive contract", (0.04, 0.46), (0.46, 0.60), 0.60, (0.16, 0.66)),
    ("Single-award IDIQ",              (0.04, 0.40), (0.40, 0.52), 0.52, (0.14, 0.62)),
    ("Multiple-award IDIQ",            (0.04, 0.50), (0.50, 0.66), 0.66, (0.22, 0.90)),
    ("BPA",                            (0.04, 0.34), None,         0.34, (0.10, 0.44)),
    ("OT agreement",                   (0.04, 0.28), None,         0.28, (0.08, 0.40)),
]

_CHIPS = ["Open now", "Option decision", "Likely upcoming",
          "Holders-only", "Superseded", "Research required"]


def _commentary_1(gid) -> str:
    finding = run("Recompete is when authority to place new orders ends, not the "
                  "latest task order's end date. ",
                  size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)
    body = run("For an IDV it is the parent's last date to order; orders placed "
               "during the ordering period can keep performing after it. Reading "
               "the latest child-order end as the recompete date is the most "
               "common false signal.",
               size=LABEL_9PT, color=BLACK, font=FONT)
    return text_box(gid(), "commentary1", _LEFT_X, _C1_Y, _LEFT_W, _C1_H,
                    [paragraph([finding, body], line_spacing=112_000)],
                    anchor="t", fill=None, insets=INSETS_NONE)


def _axis(gid) -> list[str]:
    out = []
    # subtle time axis with a right arrow
    ax_y = _AXIS_Y + 205_000
    out.append(connector(gid(), "time-axis", _PLOT_X, ax_y, _PLOT_W + 120_000, 0,
                         color=GRAY_4, width=6_350, arrow=True))
    out.append(_label(gid, _PLOT_X, ax_y + 12_000, 1_400_000, 150_000,
                      [run("time, now to future", size=SOURCES_8PT, italic=True,
                           color=GRAY_5, font=FONT)]))
    # TODAY / decision-horizon reference line across all lanes
    tx = _x(_TODAY_FRAC)
    out.append(connector(gid(), "today-line", tx, _LANES_Y - 30_000, 0,
                         _GATE_H + 30_000, color=GRAY_3, width=6_350, dashed=True))
    out.append(_label(gid, tx - 360_000, _AXIS_Y, 720_000, 150_000,
                      [run("TODAY", size=SOURCES_8PT, bold=True, color=BLACK,
                           font=FONT)], align="ctr"))
    out.append(_label(gid, tx - 520_000, _AXIS_Y + 132_000, 1_040_000, 150_000,
                      [run("decision horizon", size=SOURCES_8PT, italic=True,
                           color=GRAY_5, font=FONT)], align="ctr"))
    return out


def _lanes(gid) -> list[str]:
    out = []
    for i, (label, base, opt, tick, child) in enumerate(_LANES):
        ly = _LANES_Y + i * _LANE_PITCH
        # lane label (left)
        out.append(text_box(gid(), "lane-label", _SCH_X, ly,
                            _LANE_LABEL_W - 70_000, _LANE_PITCH - 40_000,
                            [paragraph([run(label, size=LABEL_9PT, bold=True,
                                            color=BLACK, font=FONT)])],
                            anchor="ctr", fill=None, insets=INSETS_NONE))
        p_y, p_h = ly + 64_000, 118_000          # parent span
        c_y, c_h = ly + 222_000, 118_000          # child span (nested beneath)
        # parent base (solid outline)
        bx0, bx1 = _x(base[0]), _x(base[1])
        out.append(_rect(gid, bx0, p_y, bx1 - bx0, p_h))
        # option span (dashed outline continuation)
        if opt is not None:
            ox0, ox1 = _x(opt[0]), _x(opt[1])
            out.append(_rect(gid, ox0, p_y, ox1 - ox0, p_h, dashed=True))
        # child-order bar (lighter gray; tail runs past the tick)
        cx0, cx1 = _x(child[0]), _x(child[1])
        out.append(_rect(gid, cx0, c_y, cx1 - cx0, c_h, line_color=GRAY_4))
        # recompete tick - the focal mark (heavier, full lane height)
        tx = _x(tick)
        out.append(connector(gid(), "recompete-tick", tx, ly + 44_000, 0,
                             354_000, color=BLACK, width=12_700))
        out.append(_rect(gid, tx - 33_000, ly + 18_000, 66_000, 66_000,
                         line_color=BLACK, fill=BLACK))   # tick cap
        # every lane arrows into the ADDRESSABLE gate
        out.append(connector(gid(), "to-gate", _PLOT_R + 40_000,
                             c_y + c_h // 2, _GATE_X - (_PLOT_R + 40_000), 0,
                             color=BLACK, width=6_350, arrow=True))

    # annotate lane 3 (longest child tail) - the tick-vs-tail gap is the point
    li = 2
    ly = _LANES_Y + li * _LANE_PITCH
    tick_x = _x(_LANES[li][3])
    tail_x1 = _x(_LANES[li][4][1])
    out.append(_label(gid, tick_x - 540_000, ly - 158_000, 1_140_000, 150_000,
                      [run("last date to order (recompete trigger)",
                           size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK,
                           font=FONT)], align="ctr"))
    out.append(connector(gid(), "tick-leader", tick_x, ly - 16_000, 0, 60_000,
                         color=BLACK, width=6_350))
    out.append(_label(gid, tick_x + 20_000, ly + 350_000, tail_x1 - tick_x + 520_000,
                      150_000,
                      [run("child-order performance tail (continues past the "
                           "trigger)", size=CONNECTOR_NOTE_8_5PT, italic=True,
                           color=GRAY_5, font=FONT)]))
    return out


def _gate(gid) -> list[str]:
    out = []
    # single dark focal object: vertical text in an upright tall badge
    out.append(text_box(gid(), "addressable-gate", _GATE_X, _GATE_Y,
                        _GATE_W, _GATE_H,
                        [paragraph([run("ADDRESSABLE?", size=BADGE_16PT, bold=True,
                                        color=WHITE, font=FONT)], align="ctr")],
                        anchor="ctr", fill=BLUE_4, line_width=12_700,
                        body_attrs_extra=' vert="vert270"'))
    # two-gate caption inside the badge (horizontal, small)
    out.append(text_box(gid(), "gate-checks", _GATE_X, _GATE_Y + _GATE_H - 300_000,
                        _GATE_W, 280_000,
                        [paragraph([run("1 successor check", size=SOURCES_8PT,
                                        color=WHITE, font=FONT)], align="ctr"),
                         paragraph([run("2 access category", size=SOURCES_8PT,
                                        color=WHITE, font=FONT)], align="ctr")],
                        anchor="b", fill=None, line_color="none",
                        insets=INSETS_NONE))
    return out


def _rail_table(gid) -> tuple[str, int]:
    header = ["Vehicle type", "Recompete clock", "Conf.", "Note"]
    rows = [
        header,
        ["Standalone definitive contract", "Current and ultimate completion",
         "High", "Current end may be an option decision"],
        ["IDIQ (single or multi-award)", "Parent last date to order",
         "High", "Child-order clock is holders-only work"],
        ["Task or delivery order", "Child ultimate completion",
         "Medium", "Follow-on may be holders-only"],
        ["BPA", "Agreement or call-period logic",
         "Medium", "Inspect parent and call rules"],
        ["BOA", "Nominal agreement end",
         "Low", "Not a contract; not a guaranteed recompete"],
        ["OT agreement or order", "Agreement-specific terms",
         "Variable", "Read governing agreement; validate externally"],
    ]
    # 8pt + a narrow Conf / wide Note split keeps every row <=3 lines, so the
    # table clears room for the guardrail card below it in the rail (BODY_Y..
    # _MAIN_B). At 9pt the table consumed the whole rail and drove _guardrail's
    # height negative -> PowerPoint repair on open.
    col_w = [980_000, 900_000, 500_000, 1_180_000]
    heights = text_metrics.estimate_row_heights(rows, col_w, size_pt=8.0,
                                                min_row_h=240_000)
    # confidence cells: color-graded, darkest = highest
    cell_fills, cell_text = {}, {}
    grade = {"High": (BLUE_3, WHITE), "Medium": (BLUE_2, BLACK),
             "Low": (BLUE_1, BLACK), "Variable": (GRAY_1, BLACK)}
    for ri in range(1, len(rows)):
        f, t = grade[rows[ri][2]]
        cell_fills[(ri, 2)] = f
        cell_text[(ri, 2)] = t
    xml = house_table(gid(), "clock-rule-table", _RAIL_X, BODY_Y, col_w, rows,
                      row_h=heights, table_skin="rule", size=800,
                      aligns=["l", "l", "ctr", "l"],
                      cell_fills=cell_fills, cell_text_colors=cell_text)
    return xml, BODY_Y + sum(heights)


def _guardrail(gid, top: int) -> str:
    y = top + 70_000
    h = _MAIN_B - y
    finding = run("An expiring vehicle is not automatically an opportunity. ",
                  size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)
    body = run("Check two gates. Has a follow-on already been awarded? If so the "
               "vehicle is superseded, not overdue. Can the company actually "
               "compete? Multiple-award fair opportunity under FAR 16.505 can open "
               "the next order only to existing holders.",
               size=FINEPRINT_8_5PT, color=BLACK, font=FONT)
    return text_box(gid(), "guardrail", _RAIL_X, y, _RAIL_W, h,
                    [paragraph([finding, body], line_spacing=110_000)],
                    anchor="t", fill=BLUE_2, line_width=12_700, insets=INSETS_CARD)


def _chips(gid) -> list[str]:
    out = []
    cap = _label(gid, _LEFT_X, _CHIP_Y - 2_000, 2_400_000, 150_000,
                 [run("Opportunity state, once gated:", size=SOURCES_8PT,
                      italic=True, color=GRAY_5, font=FONT)])
    n = len(_CHIPS)
    gap = 110_000
    cap_w = 2_460_000
    row_x = _LEFT_X + cap_w
    row_w = BODY_R - row_x
    chip_w = (row_w - (n - 1) * gap) // n
    out.append(cap)
    for i, c in enumerate(_CHIPS):
        cx = row_x + i * (chip_w + gap)
        out.append(text_box(gid(), "chip", cx, _CHIP_Y + 18_000, chip_w, 240_000,
                            [paragraph([run(c, size=FINEPRINT_8_5PT, color=BLACK,
                                            font=FONT)], align="ctr")],
                            anchor="ctr", fill=GRAY_1, line_width=12_700,
                            insets=INSETS_CHIP))
    return out


def _caveat_rail(gid) -> list[str]:
    out = []
    out.append(connector(gid(), "caveat-rule", _LEFT_X, _CAV_Y, BODY_R - _LEFT_X, 0,
                         color=GRAY_3, width=6_350))
    out.append(text_box(gid(), "caveat-lead", _LEFT_X, _CAV_Y + 24_000,
                        BODY_R - _LEFT_X, 170_000,
                        [paragraph([
                            run("Timing is one of four reads. ", size=LABEL_9PT,
                                bold=True, color=BLACK, font=FONT),
                            run("Whether the requirement recurs, when authority "
                                "lapses, whether the work will be competed, and who "
                                "is allowed to compete are separate questions; the "
                                "clock answers only the second.",
                                size=LABEL_9PT, color=BLACK, font=FONT)])],
                        anchor="t", fill=None, insets=INSETS_NONE))
    out.append(text_box(gid(), "caveat-fragments", _LEFT_X, _CAV_Y + 224_000,
                        BODY_R - _LEFT_X, 160_000,
                        [paragraph([run(
                            "Timing confidence varies by vehicle type   |   "
                            "A BOA nominal end is not a guaranteed recompete   |   "
                            "A later PIID may already be the successor   |   "
                            "Option value is capacity, not guaranteed revenue",
                            size=FINEPRINT_8_5PT, italic=True, color=GRAY_5,
                            font=FONT)])],
                        anchor="t", fill=None, insets=INSETS_NONE))
    return out


def _body() -> str:
    gid = _Id(10)
    parts: list[str] = []
    parts.append(_commentary_1(gid))
    parts += _axis(gid)
    parts += _lanes(gid)
    parts += _gate(gid)
    table_xml, table_bottom = _rail_table(gid)
    parts.append(table_xml)
    parts.append(_guardrail(gid, table_bottom))
    parts += _chips(gid)
    parts += _caveat_rail(gid)
    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
