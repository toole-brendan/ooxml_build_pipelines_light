"""contracts_recompete_timing - Show how vehicle structure sets the recompete clock and why an expiring clock still must clear successor and access gates before it becomes addressable.

The five parent-term bars are rendered as one native, editable stacked horizontal
bar chart (``CHARTS``/``rId2``); the vehicle-type lane labels, trigger ticks,
child-order tails, today / decision guides, routes, and the addressability gate
remain slide-shape overlays pinned to the chart's inner plot via
``_plot_geom``/``_x_at``/``_row_center``.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector, esc,
)
from deck_core.charts import bar_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CHIP, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT,
    DENSE_BODY_10PT, MESSAGE_11PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_TOPIC = "Recompete Timing"                 # title topic
_BREADCRUMB_TOPIC = "Recompete Addressability"   # breadcrumb second half
_TAKEAWAY = (
    "A vehicle's last date to order sets the recompete clock, not its last task "
    "order's end date."
)
_SOURCES = (
    "Sources: SAM.gov Contract Awards API; FAR 16.505, 16.703, 17.207; "
    "FPDS and internal Army Market Mapping workbook. Figures illustrative of method; "
    "as of 2026-06-22"
)

_EMU_PER_IN = 914_400


def _in(v: float) -> int:
    return int(round(v * _EMU_PER_IN))


def _label(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
           *, size: int = LABEL_9PT, bold: bool = False, italic: bool = False,
           color: str = BLACK, align: str = "l", anchor: str = "ctr") -> str:
    return text_box(
        sp_id, name, x, y, cx, cy,
        [paragraph([run(text, size=size, bold=bold, italic=italic,
                        color=color, font=FONT)], align=align, line_spacing=105_000)],
        fill=None, line_color=None, anchor=anchor, insets=INSETS_NONE,
    )


def _outline_bar(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
                 *, dashed: bool = False, color: str = BLACK,
                 width: int = 12_700, text: str | None = None) -> str:
    if text:
        return text_box(
            sp_id, name, x, y, cx, cy,
            [paragraph([run(text, size=750, color=color, font=FONT)],
                       align="ctr", line_spacing=100_000)],
            fill=None, line_color=color, line_width=width, dashed_line=dashed,
            anchor="ctr", insets=INSETS_NONE,
        )
    dash = '<a:prstDash val="dash"/>' if dashed else ''
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
        f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:noFill/><a:ln w="{width}"><a:solidFill>'
        f'<a:srgbClr val="{color}"/></a:solidFill>{dash}</a:ln>'
        f'</p:spPr></p:sp>'
    )


def _trigger(sp_id: int, x: int, y: int, *, name: str = "RecompeteTrigger") -> str:
    return connector(
        sp_id, name, x, y, 1, _in(0.43),
        color=BLUE_3, width=25_400,
    )


def _route_to_gate(sp_id: int, x: int, y: int, gate_x: int,
                   *, name: str = "RouteToAddressableGate") -> str:
    return connector(
        sp_id, name, x, y, gate_x - x, 1,
        color=BLACK, width=9_525, arrow=True,
    )


# ── Timeline model ───────────────────────────────────────────────────────────
# Relative units are inches measured from the timeline origin (TODAY). These
# preserve the prior hand-drawn bar lengths exactly: an axis x of 0.312 puts the
# native plot-left at BODY_X + 1.94in (the old timeline origin) and 1 unit == 1in.
# _VEHICLES is the single source for chart lengths, trigger positions, child
# tails, and the in-bar / category labels, so chart data and overlay geometry
# cannot drift apart.
_AXIS_MAX = 4.25

_VEHICLES = [
    {
        "key": "Definitive", "axis": "Definitive contract",
        "lane_label": "Standalone definitive\ncontract",
        "base": 2.16, "extension": 1.30, "trigger": 2.16,
        "bar_label": "base term", "ext_label": "option capacity",
        "child_label": None, "children": [],
    },
    {
        "key": "SA_IDIQ", "axis": "Single-award IDIQ",
        "lane_label": "Single-award\nIndefinite-Delivery/\nIndefinite-Quantity (IDIQ)",
        "base": 2.01, "extension": 1.10, "trigger": 3.11,
        "bar_label": "parent ordering period", "ext_label": None,
        "child_label": "orders", "children": [(0.52, 3.08), (1.72, 2.33)],
    },
    {
        "key": "MA_IDIQ", "axis": "Multiple-award IDIQ",
        "lane_label": "Multiple-award\nIndefinite-Delivery/\nIndefinite-Quantity (IDIQ)",
        "base": 1.71, "extension": 1.01, "trigger": 2.72,
        "bar_label": "parent vehicle", "ext_label": None,
        "child_label": "orders", "children": [(0.45, 2.85), (1.40, 2.71), (2.13, 2.00)],
    },
    {
        "key": "BPA", "axis": "BPA",
        "lane_label": "Blanket Purchase Agreement\n(BPA)",
        "base": 1.54, "extension": 0.94, "trigger": 2.48,
        "bar_label": "agreement / call period", "ext_label": None,
        "child_label": "calls", "children": [(0.62, 2.76), (1.60, 2.43)],
    },
    {
        "key": "OT", "axis": "OT",
        "lane_label": "Other Transaction (OT)\nagreement",
        "base": 2.11, "extension": 1.22, "trigger": 3.33,
        "bar_label": "agreement-specific term", "ext_label": None,
        "child_label": "orders", "children": [(1.05, 3.20)],
    },
]

_GATE_X = BODY_X + _in(6.32)

_CHART_X = BODY_X
_CHART_Y = BODY_Y + _in(0.95)
_CHART_W = _in(6.22)
_CHART_H = _in(3.14)

# Inner-plot fractions (pinned via plot_layout) reused below to land every
# overlay on the rendered bars. Tune only these four after a render.
_PLOT_LAYOUT = {
    "x": 0.312,   # leaves room for native abbreviated category labels
    "y": 0.089,
    "w": 0.682,
    "h": 0.898,
}

_TIMELINE_CHART = bar_chart(
    mode="stacked",
    categories=[v["axis"] for v in _VEHICLES],
    series=[
        {
            "name": "Active / base term",
            "values": [v["base"] for v in _VEHICLES],
            "no_fill": True,
            "hide_labels": True,
            "line": {"color": BLACK, "width": 12_700},
        },
        {
            "name": "Option / extension capacity",
            "values": [v["extension"] for v in _VEHICLES],
            "no_fill": True,
            "hide_labels": True,
            "line": {"color": BLACK, "width": 12_700, "dash": "dash"},
        },
    ],
    title=None,
    show_legend=False,
    show_value_labels=False,
    show_gridlines=False,
    show_value_axis_labels=False,
    value_axis_min=0,
    value_axis_max=_AXIS_MAX,
    show_cat_labels=False,  # manual lane labels are drawn as overlay text boxes
    cat_label_size_pt=8,   # chart API uses points, not hundredths of a point
    cat_label_bold=True,   # bold the vehicle-type axis labels
    gap_width=300,
    seg_line_color=None,
    axis_line_color=WHITE,  # suppress native spines; retain the manual top time axis
    plot_layout=_PLOT_LAYOUT,
    cat_header="Vehicle type",
)

CHARTS: list[dict] = [_TIMELINE_CHART]


def _plot_geom() -> tuple[int, int, int, int]:
    """(px, py, pw, ph) of the chart's pinned inner plot, in slide EMU."""
    px = _CHART_X + int(_CHART_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_H * _PLOT_LAYOUT["y"])
    pw = int(_CHART_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_H * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _x_at(value: float) -> int:
    px, _, pw, _ = _plot_geom()
    return px + int(pw * value / _AXIS_MAX)


def _row_center(index: int) -> int:
    _, py, _, ph = _plot_geom()
    count = len(_VEHICLES)
    return py + ph * (2 * index + 1) // (2 * count)


def _lane_label(sp_id: int, index: int, text: str) -> str:
    row_y = _row_center(index)
    return _label(
        sp_id, f"LaneLabel_{index + 1}",
        BODY_X, row_y - _in(0.25),
        _in(1.78), _in(0.50),
        text,
        size=FINEPRINT_8_5PT,
        bold=True,
        align="l",
        anchor="ctr",
    )


_GATE_BADGE_INSETS = (
    _in(0.04),  # left
    _in(0.01),  # top
    _in(0.04),  # right
    _in(0.01),  # bottom
)


def _body() -> str:
    parts: list[str] = []
    sid = 10

    # Page grid. The right-rail table is stretched leftward (smaller right_x);
    # the gate narrows and the top commentary trims to clear its new left edge.
    left_w = _in(7.84)
    right_x = BODY_X + _in(8.04)
    right_w = BODY_R - right_x
    gate_x = _GATE_X
    gate_w = _in(1.58)
    rail_y = _in(5.90)

    px, py, pw, ph = _plot_geom()
    timeline_x = px                       # value 0 == TODAY / timeline origin
    timeline_end = _x_at(_AXIS_MAX)
    decision_x = _x_at(3.62)
    bar_half = _in(0.075)

    # Native stacked timeline chart (base term + option / extension capacity and
    # the vehicle-type category labels). Painted first so every overlay lands on
    # top of it.
    parts.append(graphic_frame(
        sp_id=sid, name="RecompeteTimelineChart",
        x=_CHART_X, y=_CHART_Y, cx=_CHART_W, cy=_CHART_H, rId="rId2",
    )); sid += 1

    # Manual lane labels match the original swim-lane text treatment.
    # Native chart cat labels are hidden above; categories remain in the embedded data.
    for i, v in enumerate(_VEHICLES):
        parts.append(_lane_label(sid, i, v["lane_label"]))
        sid += 1

    # Commentary 1: the key reframe.
    parts.append(text_box(
        sid, "ClockReframe", BODY_X, BODY_Y, left_w, _in(0.69),
        [
            paragraph([
                run(
                    "Recompete is when authority to place new orders ends, not when "
                    "the latest task order ends.",
                    size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT,
                )
            ], line_spacing=108_000),
            paragraph([
                run(
                    "For an Indefinite Delivery Vehicle (IDV), the parent's last date "
                    "to order controls; orders placed during the ordering period can "
                    "keep performing after it. Reading the latest child-order end as "
                    "the recompete date is the common false signal.",
                    size=LABEL_9PT, color=BLACK, font=FONT,
                )
            ], line_spacing=108_000),
        ],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )); sid += 1

    # Separation between schematic and right rail.
    parts.append(connector(
        sid, "SectionDivider", right_x - _in(0.09), BODY_Y,
        1, _in(4.22), color=GRAY_3, width=6_350,
    )); sid += 1

    # Timeline legend and axis labels.
    legend_y = BODY_Y + _in(0.78)
    parts.append(connector(
        sid, "TriggerLegendTick", BODY_X + _in(3.42), legend_y + _in(0.01),
        1, _in(0.18), color=BLUE_3, width=25_400,
    )); sid += 1
    parts.append(_label(
        sid, "TriggerLegend", BODY_X + _in(3.52), legend_y - _in(0.04),
        _in(1.17), _in(0.28), "last date to order\n(recompete trigger)",
        size=800, italic=True, align="l", anchor="ctr",
    )); sid += 1
    parts.append(_label(
        sid, "TailLegend", BODY_X + _in(4.70), legend_y - _in(0.04),
        _in(1.58), _in(0.36),
        "child-order performance tail\n(continues past the trigger)",
        size=750, italic=True, color=GRAY_4, align="l", anchor="ctr",
    )); sid += 1

    axis_y = BODY_Y + _in(1.12)
    parts.append(connector(
        sid, "TimeAxis", timeline_x, axis_y, timeline_end - timeline_x, 1,
        color=BLACK, width=9_525, arrow=True,
    )); sid += 1
    parts.append(connector(
        sid, "TodayLine", timeline_x, axis_y - _in(0.03), 1, _in(3.24),
        color=GRAY_3, dashed=True, width=6_350,
    )); sid += 1
    parts.append(connector(
        sid, "DecisionHorizonLine", decision_x, axis_y - _in(0.03), 1, _in(3.24),
        color=GRAY_3, dashed=True, width=6_350,
    )); sid += 1
    parts.append(_label(
        sid, "TodayLabel", timeline_x - _in(0.26), axis_y - _in(0.24),
        _in(0.58), _in(0.18), "TODAY", size=800, bold=True, align="ctr",
    )); sid += 1
    parts.append(_label(
        sid, "DecisionHorizonLabel", decision_x - _in(0.46), axis_y + _in(0.02),
        _in(0.92), _in(0.14), "decision horizon", size=750, italic=True,
        color=GRAY_4, align="ctr",
    )); sid += 1

    # Per-vehicle overlays, all pinned to the chart's inner plot: the in-bar
    # phrase, the child-order label + performance tails, the recompete trigger,
    # and the route into the addressability gate.
    for i, v in enumerate(_VEHICLES):
        row_y = _row_center(i)
        base_l = timeline_x
        base_r = _x_at(v["base"])
        trig_x = _x_at(v["trigger"])

        # In-bar phrase centered on the base segment.
        if v.get("bar_label"):
            parts.append(_label(
                sid, f"BarLabel_{v['key']}", base_l, row_y - bar_half,
                base_r - base_l, _in(0.15), v["bar_label"],
                size=750, align="ctr", anchor="ctr",
            )); sid += 1

        # Extension-segment phrase (standalone option capacity only).
        if v.get("ext_label"):
            ext_r = _x_at(v["base"] + v["extension"])
            parts.append(_label(
                sid, f"ExtLabel_{v['key']}", base_r, row_y - bar_half,
                ext_r - base_r, _in(0.15), v["ext_label"],
                size=700, italic=True, color=GRAY_4, align="ctr", anchor="ctr",
            )); sid += 1

        # Child-order row label at the timeline origin.
        if v.get("child_label"):
            parts.append(_label(
                sid, f"ChildLabel_{v['key']}", base_l, row_y + _in(0.07),
                _in(0.48), _in(0.13), v["child_label"],
                size=750, italic=True, color=GRAY_4, align="l",
            )); sid += 1

        # Child-order performance tails (continue past the trigger).
        for j, (start, dur) in enumerate(v["children"]):
            cx0 = _x_at(start)
            cx1 = _x_at(start + dur)
            parts.append(_outline_bar(
                sid, f"ChildTail_{v['key']}_{j + 1}",
                cx0, row_y + _in(0.08 + j * 0.10), cx1 - cx0, _in(0.06),
                color=GRAY_4, width=9_525,
            )); sid += 1

        # Recompete trigger tick.
        parts.append(_trigger(
            sid, trig_x, row_y - _in(0.20), name=f"Trigger_{v['key']}",
        )); sid += 1

        # Route from the trigger to the gate. When the option extends past the
        # trigger (standalone), drop below the bar first so the arrow does not
        # cross the dashed extension box.
        if v["trigger"] < v["base"] + v["extension"] - 0.001:
            parts.append(connector(
                sid, f"TriggerDrop_{v['key']}", trig_x, row_y + bar_half,
                1, _in(0.21), color=BLACK, width=9_525,
            )); sid += 1
            parts.append(_route_to_gate(
                sid, trig_x, row_y + bar_half + _in(0.21), gate_x,
                name=f"RouteToGate_{v['key']}",
            )); sid += 1
        else:
            parts.append(_route_to_gate(
                sid, trig_x, row_y, gate_x, name=f"RouteToGate_{v['key']}",
            )); sid += 1

    # Standalone-specific below-bar annotations (option decision at the trigger,
    # ultimate end at the option-capacity end).
    row0 = _row_center(0)
    parts.append(_label(
        sid, "StandaloneDecisionLabel",
        _x_at(_VEHICLES[0]["trigger"]) - _in(0.41), row0 + _in(0.02),
        _in(0.82), _in(0.14), "option decision",
        size=700, italic=True, color=GRAY_4, align="ctr",
    )); sid += 1
    parts.append(_label(
        sid, "StandaloneUltimateLabel",
        _x_at(_VEHICLES[0]["base"] + _VEHICLES[0]["extension"]) - _in(0.46),
        row0 + _in(0.02), _in(0.92), _in(0.14), "ultimate end",
        size=700, italic=True, color=GRAY_4, align="ctr",
    )); sid += 1

    # Commentary 2: the addressability gate. Painted after lane routes so every
    # arrow visibly terminates at the gate edge.
    gate_y = BODY_Y + _in(1.08)
    parts.append(text_box(
        sid, "AddressableBadge", gate_x, gate_y, gate_w, _in(0.40),
        [paragraph([
            run("ADDRESSABLE?", size=1300, bold=True,
                color=WHITE, font=FONT)
        ], align="ctr", line_spacing=100_000)],
        fill=BLUE_4, line_color=BLACK, line_width=19_050,
        anchor="ctr", insets=_GATE_BADGE_INSETS, wrap="none",
    )); sid += 1
    parts.append(text_box(
        sid, "AddressableGuardrail", gate_x, gate_y + _in(0.40), gate_w, _in(2.64),
        [
            paragraph([
                run("Expired does not mean addressable.",
                    size=LABEL_9PT, bold=True, color=BLACK, font=FONT)
            ], space_after=400, line_spacing=105_000),
            paragraph([
                run("1  SUCCESSOR CHECK", size=FINEPRINT_8_5PT, bold=True,
                    color=BLACK, font=FONT)
            ], line_spacing=105_000),
            paragraph([
                run("Has a follow-on already been awarded? If yes, classify it as "
                    "superseded, not overdue.", size=FINEPRINT_8_5PT,
                    color=BLACK, font=FONT)
            ], space_after=300, line_spacing=105_000),
            paragraph([
                run("2  ACCESS CHECK", size=FINEPRINT_8_5PT, bold=True,
                    color=BLACK, font=FONT)
            ], line_spacing=105_000),
            paragraph([
                run("Can the company compete? FAR 16.505 may limit the next order "
                    "to existing vehicle holders.", size=FINEPRINT_8_5PT,
                    color=BLACK, font=FONT)
            ], line_spacing=105_000),
        ],
        fill=BLUE_2, line_color=BLACK, anchor="t", insets=INSETS_CARD,
    )); sid += 1

    # Per-vehicle clock-rule table in the upper-right rail. Full vehicle names in
    # the first column; the column widths grow to hold them.
    table_rows = [
        ["Vehicle type", "Recompete clock", "Confidence", "Note"],
        ["Standalone definitive contract",
         "Current and ultimate completion",
         "High",
         "Current may be an option decision; ultimate is the outer horizon."],
        ["Indefinite-delivery / indefinite-quantity (IDIQ), "
         "single- or multiple-award",
         "Parent last date to order; child end for holders-only work",
         "High (parent)",
         "Parent governs vehicle; child follow-on may be holders-only."],
        ["Task order or delivery order",
         "Child ultimate completion",
         "Medium",
         "Follow-on may be holders-only."],
        ["Blanket Purchase Agreement (BPA)",
         "Agreement or call-period logic",
         "Medium",
         "Inspect parent and call rules."],
        ["Basic Ordering Agreement (BOA)",
         "Nominal agreement end",
         "Low",
         "Not a contract; not a guaranteed recompete."],
        ["Other Transaction (OT) agreement or order",
         "Agreement-specific terms",
         "Variable",
         "Read governing agreement; validate externally."],
    ]
    col_w = [
        _in(1.15),                 # full vehicle names
        _in(1.05),                 # clock rule
        _in(0.72),                 # confidence
        right_w - _in(2.92),       # note
    ]
    row_h = estimate_row_heights(
        table_rows, col_w, size_pt=7.5, header_size_pt=7.5,
        min_row_h=_in(0.25),
    )
    row_h[0] = max(row_h[0], _in(0.30))
    cell_fills = {
        (1, 2): BLUE_3,
        (2, 2): BLUE_3,
        (3, 2): BLUE_2,
        (4, 2): BLUE_2,
        (5, 2): BLUE_1,
        (6, 2): GRAY_1,
    }
    cell_text_colors = {
        (1, 2): WHITE,
        (2, 2): WHITE,
        (3, 2): BLACK,
        (4, 2): BLACK,
        (5, 2): BLACK,
        (6, 2): BLACK,
    }
    parts.append(house_table(
        sid, "VehicleClockRules", right_x, BODY_Y, col_w, table_rows,
        row_h=row_h, table_skin="rule", aligns=["l", "l", "ctr", "l"],
        size=750,
        cell_fills=cell_fills,
        cell_text_colors=cell_text_colors,
    )); sid += 1

    # State classification block, pinned just above the caveat rail. OOXML row
    # heights are minimums and the estimator can under-count wrapped lines, so the
    # spelled-out table renders taller than sum(row_h); anchoring the state block
    # to the bottom (not to table_bottom) keeps the two from ever colliding.
    chip_gap = _in(0.06)
    chip_w = (right_w - 2 * chip_gap) // 3
    chip_h = _in(0.22)
    chip_step = _in(0.25)
    state_header_h = _in(0.22)
    chip_y = rail_y - _in(0.06) - chip_step - chip_h     # top of first chip row
    state_y = chip_y - _in(0.06) - state_header_h        # header just above chips

    parts.append(connector(
        sid, "GateToStateClassification", gate_x + gate_w,
        state_y + _in(0.11), right_x - (gate_x + gate_w), 1,
        color=BLACK, width=9_525, arrow=True,
    )); sid += 1
    parts.append(text_box(
        sid, "StateHeader", right_x, state_y, right_w, state_header_h,
        [paragraph([
            run("OPPORTUNITY STATE, AFTER BOTH GATES",
                size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)
        ], align="ctr", line_spacing=100_000)],
        fill=GRAY_1, line_color=BLACK, anchor="ctr", insets=INSETS_NONE,
    )); sid += 1

    states = [
        "Open now", "Option decision", "Likely upcoming",
        "Holders-only", "Superseded", "Research required",
    ]
    for i, state in enumerate(states):
        row, col = divmod(i, 3)
        x = right_x + col * (chip_w + chip_gap)
        y = chip_y + row * chip_step
        parts.append(text_box(
            sid, f"StateChip{i+1}", x, y, chip_w, chip_h,
            [paragraph([
                run(state, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)
            ], align="ctr", line_spacing=100_000)],
            fill=GRAY_1, line_color=BLACK, anchor="ctr", insets=INSETS_CHIP,
        )); sid += 1

    # Bottom caveat rail: Commentary 3 plus vehicle-type caveats.
    parts.append(connector(
        sid, "CaveatRailRule", BODY_X, rail_y, BODY_CX, 1,
        color=BLACK, width=9_525,
    )); sid += 1
    parts.append(text_box(
        sid, "CaveatRail", BODY_X, rail_y + _in(0.03), BODY_CX, _in(0.48),
        [
            paragraph([
                run("Timing is one of four reads; ", size=DENSE_BODY_10PT,
                    bold=True, color=BLACK, font=FONT),
                run("recurrence, authority, competition route, and bidder "
                    "eligibility remain separate.", size=DENSE_BODY_10PT,
                    color=BLACK, font=FONT),
            ], line_spacing=100_000),
            paragraph([
                run(
                    "Timing confidence varies by vehicle type | A Basic Ordering Agreement "
                    "(BOA) nominal end is not a guaranteed recompete | A later Procurement "
                    "Instrument Identifier (PIID) may already be the successor | Option "
                    "value is capacity, not guaranteed revenue",
                    size=750, color=GRAY_4, font=FONT,
                )
            ], line_spacing=100_000),
        ],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )); sid += 1

    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
