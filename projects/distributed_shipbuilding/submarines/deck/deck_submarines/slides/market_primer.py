"""Market primer - submarine-construction scope map.

A horizontal counted-path spine (Navy and SCN -> GDEB prime construction ->
counted supplier layer) with chevron transitions, a quiet context lane
beneath it, and a bottom exclusion ledger under a scope-boundary cap. This is
a scope map, not a branching flow: this path counts, nearby layers explain it,
these lanes are excluded.
"""
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
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BLUE_1,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_3,
    GRAY_4,
    GRAY_5,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_CHIP,
    INSETS_ANSWER_CARD,
    CAP_12PT,
    MESSAGE_11PT,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

# Breadcrumb topic is an expanded variant of the visible title topic.
_SECTION = "Market Sizing"
_TOPIC = "Submarine Ecosystem Primer"
_TITLE_TOPIC = "Market Primer"
_TAKEAWAY = "Submarine construction is a layered procurement ecosystem"
_SOURCES = "Sources: U.S. Department of the Navy SCN Justification Books; General Dynamics FY2021 Form 10-K; Huntington Ingalls Columbia-Class product page"

GAP = 91_440
MAIN_GAP = 365_760
CONNECTOR_NORMAL = 12_700
CONNECTOR_HAIRLINE = 9_525
MIN_ARROW_LEN = 250_000          # ~0.27in - below this, no arrowhead


def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w


def _p(
    text: str,
    *,
    size: int,
    color: str = BLACK,
    bold: bool = False,
    italic: bool = False,
    align: str | None = None,
    space_after: int = 0,
) -> str:
    return paragraph(
        [run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)],
        align=align,
        space_after=space_after,
    )


def _node(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    paragraphs_: list[str],
    *,
    fill: str,
    focal: bool = False,
    insets=INSETS_CARD,
    anchor: str = "t",
    line_color: str | None = None,
) -> str:
    """Sharp-rect card. Black border by default (the counted-path family);
    pass line_color=GRAY_3 for a secondary panel (context / exclusion cell)."""
    kwargs = {
        "fill": fill,
        "line_width": 19_050 if focal else 12_700,
        "anchor": anchor,
        "insets": insets,
    }
    if line_color is not None:
        kwargs["line_color"] = line_color
    return text_box(sp_id, name, x, y, cx, cy, paragraphs_, **kwargs)


def _path_chevron(sp_id: int, x: int, y: int, *, fill: str = BLUE_4) -> str:
    """Filled chevron in the whitespace between counted-path cards - the
    approved non-rect flow transition, which avoids the arrowhead-overlap
    problem of a connector running under its destination card."""
    return text_box(
        sp_id,
        "CountedPathChevron",
        x,
        y,
        260_000,
        260_000,
        [paragraph([])],
        fill=fill,
        prst="chevron",
        anchor="ctr",
    )


def _scope_boundary(sp_id: int, x: int, y: int, cx: int) -> str:
    """Dark cap over the exclusion ledger so the cells read as scope carve-outs
    under a shared label, not a downstream flow."""
    return text_box(
        sp_id,
        "ExclusionBoundary",
        x,
        y,
        cx,
        260_000,
        [paragraph([run("OUTSIDE COUNTED SUPPLIER LAYER", size=LABEL_9PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=GRAY_5,
        anchor="ctr",
        insets=INSETS_CHIP,
    )


def _scope_key(sp_id: int, x: int, y: int, cx: int) -> str:
    """No-fill read key - maps the color treatments without adding a box."""
    return text_box(
        sp_id,
        "ScopeKey",
        x,
        y,
        cx,
        260_000,
        [
            paragraph([
                run("Read: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                run("blue marks the counted sizing path; light gray cards are related context; cells under the dark cap are excluded from the count.", size=LABEL_9PT, color=BLACK, font=FONT),
            ])
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _body() -> str:
    main_y = BODY_Y + 150_000
    main_h = 880_000
    context_y = BODY_Y + 1_300_000
    context_h = 850_000
    boundary_y = BODY_Y + 2_480_000
    excl_y = BODY_Y + 2_820_000
    excl_h = 640_000
    key_y = BODY_Y + 3_620_000

    main_xs, main_w = _grid_x(3, gap=MAIN_GAP)
    excl_xs, excl_w = _grid_x(4, gap=GAP)

    y_mid = main_y + main_h // 2
    node1_r = main_xs[0] + main_w
    node2_l = main_xs[1]
    node2_r = main_xs[1] + main_w
    node3_l = main_xs[2]
    gdeb_cx = main_xs[1] + main_w // 2
    counted_cx = main_xs[2] + main_w // 2

    chev_w = 260_000
    chev_y = y_mid - chev_w // 2
    gap_12 = node2_l - node1_r
    gap_23 = node3_l - node2_r

    decomp_cy = context_y - (main_y + main_h)   # gap below the main row

    out: list[str] = []

    # ── Counted-path family: cards + chevron transitions (black borders) ──
    out.append(_node(
        20,
        "NavyAndSCNNode",
        main_xs[0],
        main_y,
        main_w,
        main_h,
        [
            _p("NAVY AND SCN", size=CAP_12PT, bold=True, color=BLACK, align="ctr", space_after=80),
            _p("budget authority", size=LABEL_9PT, color=BLACK, align="ctr"),
            _p("P-5c and P-10", size=FINEPRINT_8_5PT, italic=True, color=BLACK, align="ctr"),
        ],
        fill=BLUE_1,
        anchor="ctr",
    ))
    out.append(_node(
        21,
        "GDEBPrimeConstructionNode",
        main_xs[1],
        main_y,
        main_w,
        main_h,
        [
            _p("GDEB PRIME CONSTRUCTION", size=CAP_12PT, bold=True, color=BLACK, align="ctr", space_after=80),
            _p("contracts", size=LABEL_9PT, color=BLACK, align="ctr"),
            _p("Basic Construction", size=LABEL_9PT, bold=True, color=BLACK, align="ctr"),
            _p("Prime of record for Virginia and Columbia construction", size=FINEPRINT_8_5PT, italic=True, color=BLACK, align="ctr"),
        ],
        fill=BLUE_1,
        anchor="ctr",
    ))
    out.append(_node(
        22,
        "CountedSupplierLayerNode",
        main_xs[2],
        main_y,
        main_w,
        main_h,
        [
            _p("COUNTED SUPPLIER LAYER", size=CAP_12PT, bold=True, color=WHITE, align="ctr", space_after=80),
            _p("components and subcontracts", size=MESSAGE_11PT, color=WHITE, align="ctr"),
            _p("In TAM and SAM candidate", size=FINEPRINT_8_5PT, italic=True, color=WHITE, align="ctr"),
        ],
        fill=BLUE_5,
        focal=True,
        insets=INSETS_ANSWER_CARD,
        anchor="ctr",
    ))
    out.append(_path_chevron(10, node1_r + (gap_12 - chev_w) // 2, chev_y, fill=BLUE_4))
    out.append(_path_chevron(11, node2_r + (gap_23 - chev_w) // 2, chev_y, fill=BLUE_5))

    # ── Context lane: secondary panels, light gray borders ──
    out.append(_node(
        30,
        "HIINewportNewsContextNode",
        main_xs[1],
        context_y,
        main_w,
        context_h,
        [
            _p("HII Newport News", size=LABEL_9PT, bold=True, color=BLACK, align="ctr", space_after=60),
            _p("team-build workshare", size=FINEPRINT_8_5PT, color=BLACK, align="ctr"),
            _p("Context and yard layer; not treated as open supplier SAM", size=FINEPRINT_8_5PT, italic=True, color=BLACK, align="ctr"),
        ],
        fill=GRAY_1,
        line_color=GRAY_3,
        anchor="ctr",
    ))
    # Decomposition strip, aligned under the counted supplier node so the
    # decomposition drop lands on its center and the right edge stays at BODY_R.
    out.append(_node(
        31,
        "SupplierWorkTypesStrip",
        main_xs[2],
        context_y,
        main_w,
        context_h,
        [
            _p("Supplier work types", size=LABEL_9PT, bold=True, color=BLACK, align="ctr", space_after=60),
            _p("structural, electrical, piping, machining, castings and forgings, valves, pumps, HVAC, coatings", size=FINEPRINT_8_5PT, color=BLACK, align="ctr"),
        ],
        fill=BLUE_1,
        line_color=GRAY_3,
        anchor="ctr",
    ))

    # ── Exclusion ledger: dark boundary cap + compact cells ──
    out.append(_scope_boundary(35, BODY_X, boundary_y, BODY_CX))
    exclusions = [
        (40, "GFEAndGFPExclusionCell", "GFE and GFP", "combat systems, sonar, weapons"),
        (41, "NuclearAndBPMIExclusionCell", "Nuclear and BPMI", "reactor plant"),
        (42, "SIBCapacityExclusionCell", "SIB capacity", "grants and BlueForge-type pass-throughs"),
        (43, "DepotAndSustainmentExclusionCell", "Depot and sustainment", "non-new-construction flows"),
    ]
    for x, (sp_id, name, title, body) in zip(excl_xs, exclusions):
        out.append(_node(
            sp_id,
            name,
            x,
            excl_y,
            excl_w,
            excl_h,
            [
                _p(title, size=LABEL_9PT, bold=True, color=BLACK, align="ctr", space_after=60),
                _p(body, size=FINEPRINT_8_5PT, color=BLACK, align="ctr"),
            ],
            fill=GRAY_1,
            line_color=GRAY_3,
            anchor="ctr",
        ))

    # ── Quiet guides, painted over the cards so the decomposition arrow shows ──
    # Context is a dashed hairline (not a primary procurement step); the
    # work-type drop is a solid decomposition arrow (gap clears the arrow floor).
    out.append(connector(
        12,
        "ContextGDEBToHII",
        gdeb_cx,
        main_y + main_h,
        0,
        decomp_cy,
        color=GRAY_4,
        width=CONNECTOR_HAIRLINE,
        dashed=True,
        arrow=False,
    ))
    out.append(connector(
        13,
        "WorkTypeDecomposition",
        counted_cx,
        main_y + main_h,
        0,
        decomp_cy,
        color=BLUE_4,
        width=CONNECTOR_NORMAL,
        arrow=decomp_cy >= MIN_ARROW_LEN,
    ))

    # ── No-fill read key ──
    out.append(_scope_key(50, BODY_X, key_y, BODY_CX))

    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
