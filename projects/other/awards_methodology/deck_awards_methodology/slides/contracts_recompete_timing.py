"""contracts_recompete_timing - Show how vehicle structure sets the recompete clock and why an expiring clock still must clear successor and access gates before it becomes addressable."""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector, esc,
)
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


def _empty_paragraph() -> str:
    return paragraph([])


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


def _lane_label(sp_id: int, y: int, text: str) -> str:
    return _label(
        sp_id, "LaneLabel", BODY_X, y, _in(1.78), _in(0.50), text,
        size=FINEPRINT_8_5PT, bold=True, align="l", anchor="ctr",
    )


def _trigger(sp_id: int, x: int, y: int) -> str:
    return connector(
        sp_id, "RecompeteTrigger", x, y, 1, _in(0.43),
        color=BLUE_3, width=25_400,
    )


def _route_to_gate(sp_id: int, x: int, y: int, gate_x: int) -> str:
    return connector(
        sp_id, "RouteToAddressableGate", x, y, gate_x - x, 1,
        color=BLACK, width=9_525, arrow=True,
    )


def _body() -> str:
    parts: list[str] = []
    sid = 10

    # Page grid.
    left_w = _in(8.10)
    right_x = BODY_X + _in(8.28)
    right_w = BODY_R - right_x
    gate_x = BODY_X + _in(6.32)
    gate_w = _in(1.78)
    timeline_x = BODY_X + _in(1.94)
    timeline_end = gate_x - _in(0.14)
    decision_x = BODY_X + _in(5.56)
    rail_y = _in(5.90)

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
    ))
    sid += 1

    # Separation between schematic and right rail.
    parts.append(connector(
        sid, "SectionDivider", right_x - _in(0.09), BODY_Y,
        1, _in(4.22), color=GRAY_3, width=6_350,
    ))
    sid += 1

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

    lane_y = [BODY_Y + _in(v) for v in (1.26, 1.83, 2.40, 2.97, 3.54)]
    lane_h = _in(0.50)

    # Faint lane separators are drawn first, then bars/labels, then the gate on top.
    for ly in lane_y:
        parts.append(connector(
            sid, "LaneSeparator", BODY_X, ly + lane_h,
            gate_x - BODY_X, 1, color=GRAY_2, width=3_175,
        )); sid += 1

    # Lane 1: standalone contract. The current end is an option decision; the
    # outer completion horizon can extend beyond it.
    ly = lane_y[0]
    parts.append(_lane_label(sid, ly, "Standalone definitive\ncontract")); sid += 1
    tick = BODY_X + _in(4.10)
    parts.append(_outline_bar(
        sid, "StandaloneBase", timeline_x, ly + _in(0.10), tick - timeline_x,
        _in(0.15), text="base term",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "StandaloneOptions", tick, ly + _in(0.10), _in(1.30),
        _in(0.15), dashed=True, text="option capacity",
    )); sid += 1
    parts.append(_trigger(sid, tick, ly + _in(0.03))); sid += 1
    parts.append(_label(
        sid, "StandaloneDecisionLabel", tick - _in(0.38), ly + _in(0.27),
        _in(0.82), _in(0.14), "option decision",
        size=700, italic=True, color=GRAY_4, align="ctr",
    )); sid += 1
    parts.append(_label(
        sid, "StandaloneUltimateLabel", tick + _in(0.48), ly + _in(0.27),
        _in(0.92), _in(0.14), "ultimate end",
        size=700, italic=True, color=GRAY_4, align="ctr",
    )); sid += 1
    # Route beneath the option span so the trigger, not the ultimate end, feeds the gate.
    parts.append(connector(
        sid, "StandaloneDrop", tick, ly + _in(0.25), 1, _in(0.21),
        color=BLACK, width=9_525,
    )); sid += 1
    parts.append(_route_to_gate(sid, tick, ly + _in(0.46), gate_x)); sid += 1

    # Lane 2: single-award IDIQ.
    ly = lane_y[1]
    parts.append(_lane_label(
        sid, ly,
        "Single-award\nIndefinite-Delivery/\nIndefinite-Quantity (IDIQ)",
    )); sid += 1
    base_end = BODY_X + _in(3.95)
    tick = BODY_X + _in(5.05)
    parts.append(_outline_bar(
        sid, "SAIDIQBase", timeline_x, ly + _in(0.08), base_end - timeline_x,
        _in(0.14), text="parent ordering period",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "SAIDIQOptions", base_end, ly + _in(0.08), tick - base_end,
        _in(0.14), dashed=True,
    )); sid += 1
    parts.append(_label(
        sid, "SAIDIQChildLabel", timeline_x, ly + _in(0.28), _in(0.48),
        _in(0.13), "orders", size=750, italic=True, color=GRAY_4,
        align="l",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "SAIDIQChild1", timeline_x + _in(0.52), ly + _in(0.27),
        _in(3.08), _in(0.07), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_outline_bar(
        sid, "SAIDIQChild2", timeline_x + _in(1.72), ly + _in(0.38),
        _in(2.33), _in(0.07), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_trigger(sid, tick, ly + _in(0.02))); sid += 1
    parts.append(_route_to_gate(sid, tick, ly + _in(0.15), gate_x)); sid += 1

    # Lane 3: multiple-award IDIQ.
    ly = lane_y[2]
    parts.append(_lane_label(
        sid, ly,
        "Multiple-award\nIndefinite-Delivery/\nIndefinite-Quantity (IDIQ)",
    )); sid += 1
    base_end = BODY_X + _in(3.65)
    tick = BODY_X + _in(4.66)
    parts.append(_outline_bar(
        sid, "MAIDIQBase", timeline_x, ly + _in(0.06), base_end - timeline_x,
        _in(0.14), text="parent vehicle",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "MAIDIQOptions", base_end, ly + _in(0.06), tick - base_end,
        _in(0.14), dashed=True,
    )); sid += 1
    parts.append(_label(
        sid, "MAIDIQChildLabel", timeline_x, ly + _in(0.25), _in(0.48),
        _in(0.13), "orders", size=750, italic=True, color=GRAY_4,
        align="l",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "MAIDIQChild1", timeline_x + _in(0.45), ly + _in(0.24),
        _in(2.85), _in(0.06), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_outline_bar(
        sid, "MAIDIQChild2", timeline_x + _in(1.40), ly + _in(0.33),
        _in(2.71), _in(0.06), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_outline_bar(
        sid, "MAIDIQChild3", timeline_x + _in(2.13), ly + _in(0.42),
        _in(2.00), _in(0.06), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_trigger(sid, tick, ly + _in(0.01))); sid += 1
    parts.append(_route_to_gate(sid, tick, ly + _in(0.13), gate_x)); sid += 1

    # Lane 4: BPA.
    ly = lane_y[3]
    parts.append(_lane_label(
        sid, ly, "Blanket Purchase Agreement\n(BPA)",
    )); sid += 1
    base_end = BODY_X + _in(3.48)
    tick = BODY_X + _in(4.42)
    parts.append(_outline_bar(
        sid, "BPABase", timeline_x, ly + _in(0.08), base_end - timeline_x,
        _in(0.14), text="agreement / call period",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "BPAOptions", base_end, ly + _in(0.08), tick - base_end,
        _in(0.14), dashed=True,
    )); sid += 1
    parts.append(_label(
        sid, "BPAChildLabel", timeline_x, ly + _in(0.28), _in(0.48),
        _in(0.13), "calls", size=750, italic=True, color=GRAY_4,
        align="l",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "BPAChild1", timeline_x + _in(0.62), ly + _in(0.27),
        _in(2.76), _in(0.07), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_outline_bar(
        sid, "BPAChild2", timeline_x + _in(1.60), ly + _in(0.38),
        _in(2.43), _in(0.07), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_trigger(sid, tick, ly + _in(0.02))); sid += 1
    parts.append(_route_to_gate(sid, tick, ly + _in(0.15), gate_x)); sid += 1

    # Lane 5: OT agreement.
    ly = lane_y[4]
    parts.append(_lane_label(
        sid, ly, "Other Transaction (OT)\nagreement",
    )); sid += 1
    base_end = BODY_X + _in(4.05)
    tick = BODY_X + _in(5.27)
    parts.append(_outline_bar(
        sid, "OTBase", timeline_x, ly + _in(0.08), base_end - timeline_x,
        _in(0.14), text="agreement-specific term",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "OTOptions", base_end, ly + _in(0.08), tick - base_end,
        _in(0.14), dashed=True,
    )); sid += 1
    parts.append(_label(
        sid, "OTChildLabel", timeline_x, ly + _in(0.30), _in(0.48),
        _in(0.13), "orders", size=750, italic=True, color=GRAY_4,
        align="l",
    )); sid += 1
    parts.append(_outline_bar(
        sid, "OTChild1", timeline_x + _in(1.05), ly + _in(0.29),
        _in(3.20), _in(0.07), color=GRAY_4, width=9_525,
    )); sid += 1
    parts.append(_trigger(sid, tick, ly + _in(0.02))); sid += 1
    parts.append(_route_to_gate(sid, tick, ly + _in(0.15), gate_x)); sid += 1

    # Commentary 2: the addressability gate. It is painted after lane routes so
    # every arrow visibly terminates at the gate edge.
    gate_y = BODY_Y + _in(1.08)
    parts.append(text_box(
        sid, "AddressableBadge", gate_x, gate_y, gate_w, _in(0.40),
        [paragraph([
            run("ADDRESSABLE?", size=1600, bold=True,
                color=WHITE, font=FONT)
        ], align="ctr", line_spacing=100_000)],
        fill=BLUE_4, line_color=BLACK, line_width=19_050,
        anchor="ctr", insets=INSETS_NONE, wrap="none",
    )); sid += 1
    parts.append(text_box(
        sid, "AddressableGuardrail", gate_x, gate_y + _in(0.40), gate_w, _in(2.64),
        [
            paragraph([
                run("An expiring vehicle is not automatically an opportunity.",
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

    # Per-vehicle clock-rule table in the upper-right rail. IDIQ rows are merged
    # per the spec's fit behavior; BOA remains explicit.
    table_rows = [
        ["Vehicle type", "Recompete clock", "Confidence", "Note"],
        ["Standalone definitive contract",
         "Current and ultimate completion",
         "High",
         "Current may be an option decision; ultimate is the outer horizon."],
        ["IDIQ, single or multiple award",
         "Parent last date to order; child end for holders-only work",
         "High (parent)",
         "Parent governs vehicle; child follow-on may be holders-only."],
        ["Task or delivery order",
         "Child ultimate completion",
         "Medium",
         "Follow-on may be holders-only."],
        ["BPA",
         "Agreement or call-period logic",
         "Medium",
         "Inspect parent and call rules."],
        ["BOA",
         "Nominal agreement end",
         "Low",
         "Not a contract; not a guaranteed recompete."],
        ["OT agreement or order",
         "Agreement-specific terms",
         "Variable",
         "Read governing agreement; validate externally."],
    ]
    col_w = [_in(0.90), _in(1.03), _in(0.78), right_w - _in(2.71)]
    row_h = estimate_row_heights(
        table_rows, col_w, size_pt=8.0, header_size_pt=8.0,
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
        size=800,
        cell_fills=cell_fills,
        cell_text_colors=cell_text_colors,
    )); sid += 1
    table_bottom = BODY_Y + sum(row_h)

    # The gate flows into a classification strip, then the muted state chips.
    state_y = table_bottom + _in(0.03)
    parts.append(connector(
        sid, "GateToStateClassification", gate_x + gate_w,
        state_y + _in(0.09), right_x - (gate_x + gate_w), 1,
        color=BLACK, width=9_525, arrow=True,
    )); sid += 1
    parts.append(text_box(
        sid, "StateHeader", right_x, state_y, right_w, _in(0.18),
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
    chip_gap = _in(0.06)
    chip_w = (right_w - 2 * chip_gap) // 3
    chip_h = _in(0.20)
    chip_y = state_y + _in(0.23)
    for i, state in enumerate(states):
        row, col = divmod(i, 3)
        x = right_x + col * (chip_w + chip_gap)
        y = chip_y + row * _in(0.21)
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
        sid, "CaveatRail", BODY_X, rail_y + _in(0.03), BODY_CX, _in(0.43),
        [
            paragraph([
                run("Timing is one of four reads. ", size=DENSE_BODY_10PT,
                    bold=True, color=BLACK, font=FONT),
                run("Requirement recurrence, authority lapse, competition route, and "
                    "eligible bidder set are separate questions; the clock answers only "
                    "the second.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
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
