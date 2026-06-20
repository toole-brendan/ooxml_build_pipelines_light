"""SAM taxonomy - shape-built work-type bucket menu and scenario membership cue."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_5, GRAY_1, GRAY_3,
    BLACK, WHITE, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_MESSAGE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    CAP_12PT, VALUE_14PT, RIBBON_KPI_18PT,
)
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "SAM Taxonomy"
_TAKEAWAY = "SAM is a work-type bucket menu, not a capture forecast"
_SOURCES = "Sources: SAM.gov Acquisition Subaward Reporting Public API; FAR 52.204-10; SAM.gov Subcontract Reports Help"
def _tam_banner(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id, "PortfolioTAMBanner", x, y, cx, cy,
        [
            paragraph([run("PORTFOLIO TAM", size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=40),
            paragraph([run("~$573M per year", size=RIBBON_KPI_18PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=35),
            paragraph([run("(~$3.44B FY22-27 cumulative)", size=FINEPRINT_8_5PT, italic=True, color=WHITE, font=FONT)], align="ctr"),
        ],
        fill=BLUE_5,
        line_width=19_050,
        anchor="ctr",
        insets=(120_000, 5_000, 120_000, 5_000),
    )
def _main_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "MainSAMNote", x, y, cx, 285_000,
        [
            paragraph(
                [
                    run("SAM selects from named work-type buckets inside TAM. ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("It does not apply win probability, capture probability, or SOM.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _group_label(sp_id: int, x: int, y: int, cx: int, text: str) -> str:
    return text_box(
        sp_id, "GroupLabel", x, y, cx, 150_000,
        [paragraph([run(text, size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _bucket_chip(sp_id: int, x: int, y: int, cx: int, cy: int, title: str, body: str) -> str:
    return text_box(
        sp_id, "NamedBucketChip", x, y, cx, cy,
        [
            paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], space_after=40),
            paragraph([run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)]),
        ],
        fill=BLUE_1,
        anchor="t",
        insets=INSETS_CARD,
    )
def _residual_chip(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id, "ResidualChip", x, y, cx, cy,
        [
            paragraph([run("UNBUCKETED AND AMBIGUOUS", size=CAP_12PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=55),
            paragraph([run("~$246M per year", size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=45),
            paragraph([run("42.9% of TAM; ~$1.47B cumulative", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=GRAY_3,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _residual_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ResidualNote", x, y, cx, 840_000,
        [
            paragraph(
                [
                    run("Unbucketed and ambiguous remains explicit. ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("It is real evidence ambiguity, not zero market.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=110,
            ),
            paragraph(
                [
                    run("Boundary: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run("parent-unknown, GFE-adjacent specialty, or no clean description cue.", size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
            ),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=(70_000, 20_000, 20_000, 20_000),
    )
def _scenario_title(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ScenarioCueTitle", x, y, cx, 150_000,
        [paragraph([run("Scenario membership cue: overlapping definitions, not additive", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _scenario_cell(sp_id: int, x: int, y: int, cx: int, cy: int, title: str, body: str) -> str:
    return text_box(
        sp_id, "ScenarioMembershipCell", x, y, cx, cy,
        [
            paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=45),
            paragraph([run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=GRAY_1,
        anchor="ctr",
        insets=(60_000, 45_720, 60_000, 45_720),
    )
def _bucket_grid(sp_id: int, x: int, y: int, cx: int) -> str:
    buckets = [
        ("Structural fabrication and pre-outfit", "Hull sections, deckhouse, modules"),
        ("Machining", "Machine shops, gears, shafts, bearings"),
        ("Castings and forgings", "Forging, foundries, cast components"),
        ("Piping, valves, and pumps", "Valves, pumps, manifolds, fittings"),
        ("Electrical and power", "Switchgear, cable, distribution, motors"),
        ("HVAC and ventilation", "Chilled water, air handling, ductwork"),
        ("Coatings and insulation", "Paint, deck covering, non-skid"),
    ]
    gap_x = 120_000
    gap_y = 90_000
    chip_w = (cx - gap_x) // 2
    chip_h = 420_000
    parts = []
    for i, (title, body) in enumerate(buckets):
        row = i // 2
        col = i % 2
        parts.append(
            _bucket_chip(
                sp_id + i,
                x + col * (chip_w + gap_x),
                y + row * (chip_h + gap_y),
                chip_w,
                chip_h,
                title,
                body,
            )
        )
    return "".join(parts)
def _scenario_rail(sp_id: int, x: int, y: int, cx: int) -> str:
    cells = [
        ("Metal components", "structural, machining, castings"),
        ("HM&E components", "machining, piping, HVAC"),
        ("Electrical and power", "electrical only"),
        ("Modular assemblies", "structural, coatings"),
        ("Broad component manufacturing", "all seven named buckets"),
    ]
    gap = 90_000
    cell_w = (cx - (len(cells) - 1) * gap) // len(cells)
    cell_y = y + 190_000
    return _scenario_title(sp_id, x, y, cx) + "".join(
        _scenario_cell(sp_id + 1 + i, x + i * (cell_w + gap), cell_y, cell_w, 610_000, title, body)
        for i, (title, body) in enumerate(cells)
    )
def _body() -> str:
    side = 180_000
    banner_x = BODY_X + side
    banner_y = BODY_Y + 40_000
    banner_w = BODY_CX - 2 * side
    banner_h = 730_000
    note_y = banner_y + banner_h + 90_000
    label_y = note_y + 360_000
    chips_y = label_y + 210_000
    right_w = 3_360_000
    right_x = BODY_R - side - right_w
    left_x = BODY_X + side
    left_w = right_x - left_x - 320_000
    scenario_y = BODY_B - 1_090_000
    return (
        _tam_banner(10, banner_x, banner_y, banner_w, banner_h)
        + _main_note(20, BODY_X + 650_000, note_y, BODY_CX - 1_300_000)
        + _group_label(30, left_x, label_y, left_w, "Named work-type buckets included in scenarios")
        + _group_label(31, right_x, label_y, right_w, "Residual shown, not hidden")
        + _bucket_grid(40, left_x, chips_y, left_w)
        + _residual_chip(60, right_x, chips_y, right_w, 980_000)
        + _residual_note(61, right_x, chips_y + 1_120_000, right_w)
        + _scenario_rail(80, BODY_X + side, scenario_y, BODY_CX - 2 * side)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("SAM Taxonomy", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
