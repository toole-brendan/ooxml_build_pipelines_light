"""Demand backdrop - show converging oversight, policy, and prime behavior signals for distributed supplier capacity."""
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
    BODY_R,
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_4,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    CAP_12PT,
    CHART_TITLE_10PT,
    DENSE_BODY_10PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
)
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Demand Backdrop"
_TITLE_TOPIC = "Demand Backdrop"
_TAKEAWAY = "Policy and prime behavior point toward distributed supplier capacity"
_SOURCES = "Sources: GAO-21-257, GAO-25-106286, and GAO-26-109068; CRS RL32418 and U.S. Navy FY2027 30-Year Shipbuilding Plan; HII and General Dynamics earnings calls"
GAP = 91_440
TIMELINE_GAP = 60_000
CONNECTOR_HAIRLINE = 9_525
CONNECTOR_NORMAL = 12_700
def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w
def _no_fill_label(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    text: str,
    *,
    size: int,
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
        [paragraph([run(text, size=size, bold=bold, italic=italic, color=BLACK, font=FONT)], align=align)],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _timeline_dot(sp_id: int, x: int, y: int, d: int) -> str:
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="TimelineDot{sp_id}"/>'
        f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
        f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{BLUE_5}"/></a:solidFill>'
        f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill></a:ln>'
        f'</p:spPr></p:sp>'
    )
def _milestone_card(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    *,
    date: str,
    actor: str,
    body: str,
    fill: str = BLUE_1,
) -> str:
    return text_box(
        sp_id,
        f"MilestoneCard{sp_id}",
        x,
        y,
        cx,
        cy,
        [
            paragraph([run(date, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=40),
            paragraph([run(actor, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=60),
            paragraph([run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=fill,
        anchor="t",
        insets=INSETS_CARD,
    )
def _theme_card(
    base_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cap_h: int,
    body_h: int,
    *,
    cap: str,
    cap_fill: str,
    bullets: list[str],
) -> str:
    cap_box = text_box(
        base_id,
        f"{name}Cap",
        x,
        y,
        cx,
        cap_h,
        [paragraph([run(cap, size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=cap_fill,
        anchor="ctr",
        insets=INSETS_CARD,
    )
    body_paras = [
        paragraph([run(item, size=DENSE_BODY_10PT, color=BLACK, font=FONT)], bullet=True, space_after=120 if idx < len(bullets) - 1 else 0)
        for idx, item in enumerate(bullets)
    ]
    body_box = text_box(
        base_id + 10,
        f"{name}Body",
        x,
        y + cap_h,
        cx,
        body_h,
        body_paras,
        fill=GRAY_1,
        anchor="t",
        insets=INSETS_CARD,
    )
    return cap_box + body_box
def _body() -> str:
    headline_y = BODY_Y + 20_000
    headline_h = 230_000
    date_y = BODY_Y + 330_000
    date_h = 180_000
    axis_y = BODY_Y + 640_000
    dot_d = 130_000
    dot_y = axis_y - dot_d // 2
    card_y = BODY_Y + 880_000
    card_h = 1_120_000
    evidence_y = BODY_Y + 2_390_000
    evidence_cap_h = 350_000
    evidence_body_h = 1_430_000
    card_xs, card_w = _grid_x(6, gap=TIMELINE_GAP)
    evidence_xs, evidence_w = _grid_x(3, gap=GAP)
    axis_start = BODY_X + 160_000
    axis_end = BODY_R - 160_000
    span = axis_end - axis_start
    centers = [axis_start + int(i * span / 5) for i in range(6)]
    dates = ["2021", "2024 and 2025", "Jan 2026", "Jan-Apr 2026", "Apr-May 2026", "May 2026"]
    milestones = [
        ("Jan 2021", "GAO-21-257", "Supplier base roughly 70% smaller; outsourcing oversight becomes critical.", BLUE_1),
        ("2024 and 2025", "SIB institutionalized", "GAO documents integrator role and yard outsourcing due to constrained space.", BLUE_1),
        ("Jan 2026", "CRS RL32418", "16,000 suppliers; about 70% critical sole-source; AUKUS ramps demand.", BLUE_1),
        ("Jan-Apr 2026", "General Dynamics", "Supply chain remains the gating item; complex components bottleneck.", BLUE_1),
        ("Apr-May 2026", "GAO and Navy", "More than $10B invested; Navy plan points to distributed capacity.", BLUE_1),
        ("May 2026", "HII", "+30% outsourcing-hours guidance and distributed shipbuilding strategy language.", BLUE_2),
    ]
    out = []
    out.append(_no_fill_label(10, "TimelineHeadline", BODY_X, headline_y, BODY_CX, headline_h, "The constraint is no longer only yard throughput; it is supplier capacity and supplier qualification.", size=CHART_TITLE_10PT, italic=True))
    out.append(connector(11, "TimelineRule", axis_start, axis_y, span, 0, color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False))
    for i, center in enumerate(centers):
        out.append(connector(12 + i, f"TimelineTickConnector{i + 1}", center, axis_y + dot_d // 2, 0, card_y - (axis_y + dot_d // 2), color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False))
    for i, (center, label) in enumerate(zip(centers, dates)):
        out.append(_no_fill_label(30 + i, f"TimelineDateLabel{i + 1}", card_xs[i], date_y, card_w, date_h, label, size=LABEL_9PT, bold=True, align="ctr"))
        out.append(_timeline_dot(40 + i, center - dot_d // 2, dot_y, dot_d))
    for i, (date, actor, body, fill) in enumerate(milestones):
        out.append(_milestone_card(50 + i, card_xs[i], card_y, card_w, card_h, date=date, actor=actor, body=body, fill=fill))
    out.append(_theme_card(
        70,
        "ConstraintSignal",
        evidence_xs[0],
        evidence_y,
        evidence_w,
        evidence_cap_h,
        evidence_body_h,
        cap="CONSTRAINT SIGNAL",
        cap_fill=BLUE_5,
        bullets=["Atrophied supplier base", "70% critical suppliers sole-source", "AUKUS adds demand"],
    ))
    out.append(_theme_card(
        72,
        "PolicySignal",
        evidence_xs[1],
        evidence_y,
        evidence_w,
        evidence_cap_h,
        evidence_body_h,
        cap="POLICY SIGNAL",
        cap_fill=BLUE_4,
        bullets=[">$10B DoD submarine industrial-base investment", "SIB program office", "Distributed sites target"],
    ))
    out.append(_theme_card(
        74,
        "PrimeBehaviorSignal",
        evidence_xs[2],
        evidence_y,
        evidence_w,
        evidence_cap_h,
        evidence_body_h,
        cap="PRIME BEHAVIOR SIGNAL",
        cap_fill=BLUE_3,
        bullets=["HII +30% outsourcing-hours guidance", "GD supply-chain gating", "EB capex and throughput"],
    ))
    return "".join(out)
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
