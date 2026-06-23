"""contracts_obligated_vs_unobligated - distinguish contract-value snapshots from additive action obligations.

Drop-in body-slide module for the deck_core raw-OOXML pipeline. The slide uses
only shared primitives, style tokens, and deterministic table sizing; it has no
charts or image relationships.
"""
from __future__ import annotations

from xml.sax.saxutils import escape as _esc

from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
    house_table,
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BLUE_1,
    BLUE_2,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    GRAY_4,
    GRAY_5,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CHIP,
    INSETS_CARD,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_TOPIC = "Obligated vs. Unobligated"             # title topic
_BREADCRUMB_TOPIC = "Obligated and Unobligated Value"   # breadcrumb second half
_TAKEAWAY = (
    "Unobligated ceiling is capacity already inside awarded vehicles, "
    "not unspent budget authority."
)
_SOURCES = (
    "Sources: Ceiling and current value: SAM.gov Contract Awards API; "
    "action-level obligations and outlays: USAspending transactions, reconciled "
    "with FPDS lineage; family roll-up and worked figures: internal Army Market "
    "Mapping workbook | Note: Then-year dollars; figures illustrative of method; "
    "as of 2026-06-22"
)

_EMU = 914_400


def _inch(value: float) -> int:
    return int(round(value * _EMU))


# Visual hierarchy for the nested contract measures. The slide's focal gap is
# ceiling less current value (the unobligated capacity), so it gets the strongest
# hatch; the inner current-less-obligation gap is deliberately quieter.
_UNOBLIGATED_GAP = dict(fg=GRAY_5, bg=BLUE_1, pattern="dkUpDiag")
_CURRENT_VALUE_GAP = dict(fg=GRAY_4, bg=GRAY_1, pattern="ltUpDiag")


def _pattern_rect(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    *,
    fg: str = GRAY_4,
    bg: str = BLUE_1,
    pattern: str = "ltUpDiag",
) -> str:
    """Borderless patterned rectangle used for the unobligated-capacity ring."""
    return (
        '<p:sp><p:nvSpPr>'
        f'<p:cNvPr id="{sp_id}" name="{_esc(name)}"/>'
        '<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm>'
        f'<a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/>'
        '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:pattFill prst="{pattern}">'
        f'<a:fgClr><a:srgbClr val="{fg}"/></a:fgClr>'
        f'<a:bgClr><a:srgbClr val="{bg}"/></a:bgClr>'
        '</a:pattFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>'
    )


def _label_box(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    text: str,
    *,
    size: int = LABEL_9PT,
    bold: bool = True,
    italic: bool = False,
    color: str = BLACK,
    fill: str | None = None,
    align: str = "l",
    anchor: str = "ctr",
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)],
                   align=align, line_spacing=100_000)],
        fill=fill,
        line_color="none",
        anchor=anchor,
        insets=INSETS_CHIP,
    )


def _money_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    segments = [
        ("Sum action obligations only", 1.66),
        ("Never sum cumulative snapshots", 1.92),
        ("Keep obligations, current value, ceiling, outlays, budget demand, and subawards separate", 3.58),
        ("Roll the vehicle and its children into one family", 2.48),
        ("Ceiling and option value are not guaranteed revenue", 2.70),
    ]
    out = text_box(
        sp_id,
        "MoneyDisciplineRail",
        x,
        y,
        cx,
        cy,
        [paragraph([])],
        fill=GRAY_1,
        line_color=BLACK,
        line_width=12_700,
        insets=INSETS_NONE,
    )
    sid = sp_id + 1
    cursor = x
    for idx, (copy, width_in) in enumerate(segments):
        width = _inch(width_in)
        if idx == len(segments) - 1:
            width = x + cx - cursor
        out += text_box(
            sid,
            f"MoneyDiscipline{idx + 1}",
            cursor,
            y,
            width,
            cy,
            [paragraph([run(copy, size=DENSE_BODY_10PT, bold=(idx in (0, 1, 4)),
                                color=BLACK, font=FONT)],
                       align="ctr", line_spacing=100_000)],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=(_inch(0.06), _inch(0.03), _inch(0.06), _inch(0.03)),
        )
        sid += 1
        cursor += width
        if idx < len(segments) - 1:
            out += connector(
                sid,
                f"MoneyDisciplineDivider{idx + 1}",
                cursor,
                y + _inch(0.08),
                1,
                cy - _inch(0.16),
                color=BLACK,
                width=6_350,
            )
            sid += 1
    return out


def _body() -> str:
    # Main two-column body above the shared bottom rail.
    gap = _inch(0.18)
    left_w = _inch(7.82)
    right_x = BODY_X + left_w + gap
    right_w = BODY_X + BODY_CX - right_x

    out: list[str] = []
    sid = 10

    # Commentary 1: the governing interpretation above the hero schematic.
    out.append(text_box(
        sid,
        "MoneyMeasuresFinding",
        BODY_X,
        BODY_Y,
        left_w,
        _inch(0.60),
        [
            paragraph([run("Three contract-value measures, never summed.",
                           size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
                      line_spacing=100_000),
            paragraph([run(
                "Obligated, current value, and ceiling restate the same money. "
                "Only the per-action obligation stream is additive; sum it, never the cumulative snapshots.",
                size=LABEL_9PT, color=BLACK, font=FONT)],
                line_spacing=100_000),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    ))
    sid += 1

    # Collapsed vehicle-family frame: parent, children, and modifications counted once.
    frame_x = BODY_X
    frame_y = BODY_Y + _inch(0.68)
    frame_w = _inch(5.90)
    frame_h = _inch(2.42)
    out.append(text_box(
        sid,
        "VehicleFamilyFrame",
        frame_x,
        frame_y,
        frame_w,
        frame_h,
        [paragraph([])],
        fill=None,
        line_color=BLACK,
        line_width=12_700,
        insets=INSETS_NONE,
    ))
    sid += 1
    out.append(_label_box(
        sid,
        "VehicleFamilyCap",
        frame_x + _inch(0.12),
        frame_y + _inch(0.06),
        _inch(3.80),
        _inch(0.27),
        "COLLAPSED VEHICLE FAMILY | parent, child orders, and modifications counted once",
        size=FINEPRINT_8_5PT,
        fill=WHITE,
    ))
    sid += 1

    # Nested money measures. The outer and inner rings are patterned to make the
    # obligated-to-ceiling gap read as optional authority, never booked backlog.
    ceil_x = frame_x + _inch(0.23)
    ceil_y = frame_y + _inch(0.37)
    ceil_w = _inch(5.35)
    ceil_h = _inch(1.55)
    curr_x = ceil_x + _inch(0.36)
    curr_y = ceil_y + _inch(0.31)
    curr_w = ceil_w - _inch(0.72)
    curr_h = ceil_h - _inch(0.58)
    obl_x = curr_x + _inch(0.43)
    obl_y = curr_y + _inch(0.24)
    obl_w = curr_w - _inch(0.94)
    obl_h = curr_h - _inch(0.39)

    out.append(text_box(
        sid,
        "CeilingOutline",
        ceil_x,
        ceil_y,
        ceil_w,
        ceil_h,
        [paragraph([])],
        fill=None,
        line_color=BLACK,
        line_width=12_700,
        insets=INSETS_NONE,
    ))
    sid += 1
    out.append(text_box(
        sid,
        "CurrentValueField",
        curr_x,
        curr_y,
        curr_w,
        curr_h,
        [paragraph([])],
        fill=BLUE_2,
        line_color=BLACK,
        line_width=12_700,
        insets=INSETS_NONE,
    ))
    sid += 1

    # Outer ring: ceiling less current-value rectangle.
    outer_t = curr_y - ceil_y
    outer_b = ceil_y + ceil_h - (curr_y + curr_h)
    outer_l = curr_x - ceil_x
    outer_r = ceil_x + ceil_w - (curr_x + curr_w)
    for name, x, y, w, h in (
        ("CeilingGapTop", ceil_x, ceil_y, ceil_w, outer_t),
        ("CeilingGapBottom", ceil_x, curr_y + curr_h, ceil_w, outer_b),
        ("CeilingGapLeft", ceil_x, curr_y, outer_l, curr_h),
        ("CeilingGapRight", curr_x + curr_w, curr_y, outer_r, curr_h),
    ):
        out.append(_pattern_rect(sid, name, x, y, w, h, **_UNOBLIGATED_GAP))
        sid += 1

    # Inner ring: current value less cumulative obligation.
    inner_t = obl_y - curr_y
    inner_b = curr_y + curr_h - (obl_y + obl_h)
    inner_l = obl_x - curr_x
    inner_r = curr_x + curr_w - (obl_x + obl_w)
    for name, x, y, w, h in (
        ("CurrentGapTop", curr_x, curr_y, curr_w, inner_t),
        ("CurrentGapBottom", curr_x, obl_y + obl_h, curr_w, inner_b),
        ("CurrentGapLeft", curr_x, obl_y, inner_l, obl_h),
        ("CurrentGapRight", obl_x + obl_w, obl_y, inner_r, obl_h),
    ):
        out.append(_pattern_rect(sid, name, x, y, w, h, **_CURRENT_VALUE_GAP))
        sid += 1

    # Layer labels sit on their own fields, not as addable bar labels.
    out.append(_label_box(
        sid,
        "CeilingLabel",
        ceil_x + _inch(0.08),
        ceil_y + _inch(0.03),
        _inch(2.30),
        _inch(0.23),
        "Ceiling | base and all options",
        size=LABEL_9PT,
        fill=WHITE,
    ))
    sid += 1
    out.append(_label_box(
        sid,
        "CurrentValueLabel",
        curr_x + _inch(0.08),
        curr_y + _inch(0.03),
        _inch(2.90),
        _inch(0.22),
        "Current value | base and exercised options",
        size=LABEL_9PT,
        fill=BLUE_2,
    ))
    sid += 1

    # Solid executed core.
    out.append(text_box(
        sid,
        "CumulativeObligationCore",
        obl_x,
        obl_y,
        obl_w,
        obl_h,
        [paragraph([])],
        fill=BLUE_4,
        line_color=BLACK,
        line_width=12_700,
        insets=INSETS_NONE,
    ))
    sid += 1
    out.append(_label_box(
        sid,
        "CumulativeObligationLabel",
        obl_x + _inch(0.08),
        obl_y + _inch(0.02),
        obl_w - _inch(0.16),
        _inch(0.19),
        "Cumulative obligation (award) | executed",
        size=FINEPRINT_8_5PT,
        color=WHITE,
        fill=BLUE_4,
    ))
    sid += 1

    # Per-action tiles: the only additive layer.
    tile_y = obl_y + _inch(0.20)
    tile_h = _inch(0.20)
    tile_gap = _inch(0.05)
    tile_left = obl_x + _inch(0.10)
    tile_total_w = obl_w - _inch(0.20)
    tile_w = (tile_total_w - 4 * tile_gap) // 5
    for idx in range(5):
        tx = tile_left + idx * (tile_w + tile_gap)
        out.append(text_box(
            sid,
            f"ActionObligation{idx + 1}",
            tx,
            tile_y,
            tile_w,
            tile_h,
            [paragraph([run(f"A{idx + 1}", size=LABEL_9PT, bold=True,
                                color=WHITE, font=FONT)], align="ctr",
                       line_spacing=100_000)],
            fill=BLUE_5,
            line_color=WHITE,
            line_width=6_350,
            anchor="ctr",
            insets=INSETS_NONE,
        ))
        sid += 1
    out.append(_label_box(
        sid,
        "ActionStreamLabel",
        obl_x + _inch(0.08),
        obl_y + obl_h - _inch(0.17),
        obl_w - _inch(0.16),
        _inch(0.15),
        "Action obligations (transactions) | ONLY ADDITIVE LAYER",
        size=750,  # 7.5pt, compact in-core label
        color=WHITE,
        fill=BLUE_4,
        align="ctr",
    ))
    sid += 1

    # Gap label and formula caption.
    gap_label_x = frame_x + _inch(4.00)
    gap_label_y = frame_y + _inch(0.05)
    gap_label_w = _inch(1.82)
    gap_label_h = _inch(0.30)
    out.append(text_box(
        sid,
        "UnobligatedCapacityLabel",
        gap_label_x,
        gap_label_y,
        gap_label_w,
        gap_label_h,
        [
            paragraph([run("UNOBLIGATED", size=FINEPRINT_8_5PT, bold=True,
                           color=BLACK, font=FONT)], align="ctr", line_spacing=90_000),
            paragraph([run("= remaining capacity | indicative", size=750, italic=True,
                           color=GRAY_5, font=FONT)], align="ctr", line_spacing=90_000),
        ],
        fill=WHITE,
        line_color=BLACK,
        line_width=12_700,
        anchor="ctr",
        insets=INSETS_CHIP,
    ))
    sid += 1
    out.append(connector(
        sid,
        "UnobligatedCapacityPointer",
        gap_label_x + gap_label_w // 2,
        gap_label_y + gap_label_h,
        1,
        ceil_y - (gap_label_y + gap_label_h),
        color=BLACK,
        width=6_350,
        arrow=True,
    ))
    sid += 1
    out.append(text_box(
        sid,
        "CapacityFormula",
        frame_x + _inch(0.28),
        frame_y + frame_h - _inch(0.37),
        frame_w - _inch(0.56),
        _inch(0.27),
        [paragraph([run(
            "unobligated remaining capacity = parent ceiling minus family obligations (indicative)",
            size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)],
            align="ctr", line_spacing=100_000)],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    ))
    sid += 1

    # Detached chips: separate universes, visually outside the vehicle frame.
    chip_x = BODY_X + _inch(6.12)
    chip_w = left_w - _inch(6.12)
    out.append(text_box(
        sid,
        "SeparateUniversesHeader",
        chip_x,
        frame_y + _inch(0.03),
        chip_w,
        _inch(0.43),
        [
            paragraph([run("SEPARATE UNIVERSES", size=LABEL_9PT, bold=True,
                           color=BLACK, font=FONT)], align="ctr", line_spacing=95_000),
            paragraph([run("not outer rings", size=FINEPRINT_8_5PT, italic=True,
                           color=GRAY_5, font=FONT)], align="ctr", line_spacing=95_000),
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    ))
    sid += 1
    chip_specs = [
        ("Outlay", "cash disbursed"),
        ("Budget demand", "requested or enacted"),
        ("Subaward", "first-tier supplier flow"),
    ]
    chip_y = frame_y + _inch(0.53)
    for idx, (label, definition) in enumerate(chip_specs):
        out.append(text_box(
            sid,
            f"SeparateUniverse{idx + 1}",
            chip_x,
            chip_y + idx * _inch(0.54),
            chip_w,
            _inch(0.46),
            [
                paragraph([run(label, size=LABEL_9PT, bold=True,
                               color=BLACK, font=FONT)], align="ctr", line_spacing=95_000),
                paragraph([run(definition, size=800, color=BLACK, font=FONT)],
                          align="ctr", line_spacing=95_000),
            ],
            fill=GRAY_1,
            line_color=BLACK,
            line_width=12_700,
            anchor="ctr",
            insets=INSETS_CHIP,
        ))
        sid += 1
    out.append(text_box(
        sid,
        "SeparateUniverseCaption",
        chip_x,
        frame_y + _inch(2.19),
        chip_w,
        _inch(0.20),
        [paragraph([run("never summed with the nest", size=800, italic=True,
                           color=GRAY_5, font=FONT)], align="ctr", line_spacing=95_000)],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    ))
    sid += 1

    # Commentary 3: muted note tied to the hatched capacity gap.
    note_y = BODY_Y + _inch(3.23)
    out.append(_pattern_rect(
        sid,
        "CapacityNoteSwatch",
        BODY_X,
        note_y + _inch(0.06),
        _inch(0.20),
        _inch(0.20),
        **_UNOBLIGATED_GAP,
    ))
    sid += 1
    out.append(text_box(
        sid,
        "CapacityInterpretation",
        BODY_X + _inch(0.29),
        note_y,
        left_w - _inch(0.29),
        _inch(0.89),
        [
            paragraph([run("Count the capacity once, and call it indicative.",
                           size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)],
                      line_spacing=100_000),
            paragraph([run(
                "Collapse parent, child orders, and modifications into one family before reading the gap. "
                "A ceiling may be shared across many holders and never used, so the gap is an opportunity "
                "indicator, not pipeline value.",
                size=FINEPRINT_8_5PT, color=GRAY_5, font=FONT)],
                line_spacing=100_000),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    ))
    sid += 1

    # Right rail: anti-misread clarifier card.
    card_y = BODY_Y
    card_h = _inch(1.30)
    out.append(text_box(
        sid,
        "TwoSensesCard",
        right_x,
        card_y,
        right_w,
        card_h,
        [paragraph([])],
        fill=BLUE_1,
        line_color=BLACK,
        line_width=19_050,
        insets=INSETS_NONE,
    ))
    sid += 1
    out.append(text_box(
        sid,
        "TwoSensesHeadline",
        right_x + _inch(0.12),
        card_y + _inch(0.08),
        right_w - _inch(0.24),
        _inch(0.34),
        [paragraph([run('"Unobligated" has two senses; this slide means the contract one.',
                           size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
                   line_spacing=100_000)],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    ))
    sid += 1
    half = (right_w - _inch(0.34)) // 2
    col_y = card_y + _inch(0.50)
    col_h = card_h - _inch(0.60)
    out.append(text_box(
        sid,
        "ContractSense",
        right_x + _inch(0.12),
        col_y,
        half,
        col_h,
        [
            paragraph([run("CONTRACT SENSE (THIS SLIDE)", size=FINEPRINT_8_5PT,
                           bold=True, color=BLACK, font=FONT)], line_spacing=95_000),
            paragraph([run(
                "Vehicle ceiling not yet obligated; capacity already inside an IDIQ.",
                size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], line_spacing=95_000),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    ))
    sid += 1
    divider_x = right_x + _inch(0.17) + half
    out.append(connector(
        sid,
        "TwoSensesDivider",
        divider_x,
        col_y,
        1,
        col_h,
        color=BLACK,
        width=6_350,
    ))
    sid += 1
    out.append(text_box(
        sid,
        "BudgetSense",
        divider_x + _inch(0.10),
        col_y,
        half,
        col_h,
        [
            paragraph([run("BUDGET SENSE (NOT THIS SLIDE)", size=FINEPRINT_8_5PT,
                           bold=True, color=BLACK, font=FONT)], line_spacing=95_000),
            paragraph([run(
                "Appropriated authority not yet placed on contract. Different number, different universe.",
                size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], line_spacing=95_000),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    ))
    sid += 1

    # Four-row glossary. Outlay and Subaward are intentionally kept in the
    # detached chips because the right rail is too narrow for six honest rows.
    glossary_title_y = BODY_Y + _inch(1.43)
    out.append(text_box(
        sid,
        "GlossaryTitle",
        right_x,
        glossary_title_y,
        right_w,
        _inch(0.24),
        [paragraph([run("MONEY-MEASURES GLOSSARY | nested contract measures",
                           size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   line_spacing=100_000)],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    ))
    sid += 1

    glossary_rows = [
        ["Measure", "What it is", "Where it appears", "Common misread"],
        ["Action obligation", "One transaction or modification",
         "Award action and transaction records", "Summing cumulative snapshots"],
        ["Cumulative obligation", "Restated running total to date",
         "Award record", "Treating each restatement as new money"],
        ["Current value", "Base and exercised options",
         "SAM Contract Awards value fields", "Reading it as the ceiling"],
        ["Potential / ceiling", "Base and all options; maximum authority",
         "SAM Contract Awards ceiling fields", "Treating ceiling as funded or guaranteed revenue"],
    ]
    col_w = [_inch(0.90), _inch(1.05), _inch(1.05)]
    col_w.append(right_w - sum(col_w))
    row_h = estimate_row_heights(
        glossary_rows,
        col_w,
        size_pt=8.0,
        header_size_pt=8.0,
        min_row_h=_inch(0.30),
    )
    row_h = [h if i == 0 else h + _inch(0.03) for i, h in enumerate(row_h)]
    glossary_y = BODY_Y + _inch(1.69)
    muted = {(ri, 3): GRAY_5 for ri in range(1, len(glossary_rows))}
    out.append(house_table(
        sid,
        "MoneyMeasuresGlossary",
        right_x,
        glossary_y,
        col_w,
        glossary_rows,
        row_h=row_h,
        table_skin="rule",
        aligns=["l", "l", "l", "l"],
        size=800,
        cell_text_colors=muted,
    ))
    sid += 1

    # Shared money-discipline rail across both zones.
    rail_y = BODY_Y + _inch(4.27)
    out.append(_money_rail(sid, BODY_X, rail_y, BODY_CX, _inch(0.64)))

    return "".join(out)


def render() -> str:
    """Assemble the locked chrome and slide body into one complete p:sld XML part."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
