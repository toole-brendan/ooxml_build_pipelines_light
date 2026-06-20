"""Sizing boundary - define included, excluded, and context-only streams for the supplier TAM and scenario SAM model."""
from __future__ import annotations
from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BLUE_1,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    GRAY_4,
    GRAY_5,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_MESSAGE,
    CAP_12PT,
    CHART_TITLE_10PT,
    DENSE_BODY_10PT,
    FINEPRINT_8_5PT,
    MESSAGE_11PT,
)
LAYOUT = "slideLayout4"
# The spec uses a breadcrumb topic distinct from the visible title topic.
_SECTION = "Market Sizing"
_TOPIC = "Boundary"
_TITLE_TOPIC = "Sizing Boundary"
_TAKEAWAY = "The model sizes non-nuclear supplier opportunity, excluding GFE, SIB, yards, and SOM"
_SOURCES = "Sources: U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; FAR 52.204-10 and FAR Part 45; GAO-25-106286"
GAP = 91_440
def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w
def _simple_text(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    text: str,
    *,
    size: int,
    color: str = BLACK,
    bold: bool = False,
    italic: bool = False,
    align: str = "l",
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _bullet_paragraphs(items: list[str | tuple[str, str]], *, body_size: int = DENSE_BODY_10PT) -> list[str]:
    paras: list[str] = []
    for idx, item in enumerate(items):
        space_after = 95 if idx < len(items) - 1 else 0
        if isinstance(item, tuple):
            lead, body = item
            runs_ = [
                run(lead + " ", size=body_size, bold=True, color=BLACK, font=FONT),
                run(body, size=body_size, color=BLACK, font=FONT),
            ]
        else:
            runs_ = [run(item, size=body_size, color=BLACK, font=FONT)]
        paras.append(paragraph(runs_, bullet=True, space_after=space_after))
    return paras
def _column(
    base_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cap_h: int,
    body_h: int,
    title: str,
    bullets: list[str | tuple[str, str]],
    *,
    cap_fill: str,
    body_fill: str,
) -> str:
    cap = text_box(
        base_id,
        f"{name}Header",
        x,
        y,
        cx,
        cap_h,
        [paragraph([run(title, size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=cap_fill,
        anchor="ctr",
        insets=INSETS_CARD,
    )
    body = text_box(
        base_id + 10,
        f"{name}Body",
        x,
        y + cap_h,
        cx,
        body_h,
        _bullet_paragraphs(bullets),
        fill=body_fill,
        anchor="t",
        insets=INSETS_CARD,
    )
    return cap + body
def _warning_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "BoundaryWarningRail",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Boundary warning: ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
                    run("No SOM is modeled. SAM is a scenario menu, not market share, capture, win probability, or revenue forecast.", size=MESSAGE_11PT, color=WHITE, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=BLUE_5,
        line_width=19_050,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    note_y = BODY_Y + 30_000
    note_h = 190_000
    cols_y = BODY_Y + 310_000
    cap_h = 330_000
    body_h = 2_590_000
    warning_y = BODY_Y + 3_520_000
    warning_h = 650_000
    xs, col_w = _grid_x(3, gap=GAP)
    included = [
        ("P-5c Basic Construction", "and Conversion base for Virginia and Columbia new construction."),
        ("Non-nuclear supplier", "component manufacturing inside the construction base."),
        ("Purchased material", "first-tier subcontracts and supported lower-tier supplier flow."),
        ("Work-type buckets", "structural, machining, castings, piping, valves, electrical, HVAC, coatings."),
    ]
    excluded = [
        ("GFE and GFP", "nuclear reactor plant, combat systems, sonar, weapons, and ordnance."),
        ("BPMI nuclear", "reactor work and naval nuclear GFE."),
        ("SIB capacity", "grants and BlueForge-type pass-through funding."),
        ("Yards", "prime and co-prime work at GDEB and HII Newport News."),
        ("Depot and sustainment", "overhauls, design-only work, program-office labor, and classified payloads."),
        ("AP overlap", "already inside Basic Construction; additive base is $0."),
    ]
    context = [
        ("Total Ship Estimate", "and TOA context from P-5c and P-40."),
        ("AP/LLTM", "gross reference stream for cadence; additive base is $0."),
        ("FFATA and FSRS", "visible first-tier subaward stream as a named-vendor floor."),
        ("POP evidence", "supports the supplier coefficient."),
        ("HII visibility gap", "and unseen layer are limitations, not extra add-ons."),
    ]
    return "".join([
        _simple_text(10, "BoundarySubtitle", BODY_X, note_y, BODY_CX, note_h, "A narrower answer is more defensible than a larger, double-counted market.", size=CHART_TITLE_10PT, italic=True),
        _column(20, "IncludedInTAM", xs[0], cols_y, col_w, cap_h, body_h, "INCLUDED IN TAM", included, cap_fill=BLUE_5, body_fill=BLUE_1),
        _column(21, "ExcludedFromTAM", xs[1], cols_y, col_w, cap_h, body_h, "EXCLUDED FROM TAM", excluded, cap_fill=GRAY_5, body_fill=GRAY_2),
        _column(22, "ContextOnly", xs[2], cols_y, col_w, cap_h, body_h, "CONTEXT ONLY", context, cap_fill=GRAY_4, body_fill=GRAY_1),
        _warning_rail(50, BODY_X, warning_y, BODY_CX, warning_h),
        _simple_text(60, "APAndLLTMNote", BODY_X, warning_y + warning_h + 110_000, BODY_CX, 170_000, "AP/LLTM are timing mechanisms; do not add P-10 to P-5c Basic Construction without changing the boundary.", size=FINEPRINT_8_5PT, italic=True),
    ])
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
