"""Methodology - show the seven-step TAM-to-SAM model logic and the headline formula."""
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
    BLUE_2,
    BLUE_4,
    BLUE_5,
    GRAY_4,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_ANSWER_CARD,
    CAP_12PT,
    CHART_TITLE_10PT,
    MESSAGE_11PT,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    VALUE_14PT,
    RIBBON_KPI_18PT,
    DENSE_BODY_10PT,
)
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Methodology"
_TITLE_TOPIC = "Methodology"
_TAKEAWAY = "TAM is built from Basic Construction, supplier coefficients, and work-type allocation"
_SOURCES = "Sources: U.S. Department of the Navy SCN Justification Books; U.S. DoD daily Contracts announcements; SAM.gov FFATA, FSRS, and Entity Management records"
GAP = 55_000
CONNECTOR_NORMAL = 12_700
def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w
def _step_dot(sp_id: int, x: int, y: int, d: int, n: int) -> str:
    return text_box(
        sp_id,
        f"StepDot{n}",
        x,
        y,
        d,
        d,
        [paragraph([run(str(n), size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5,
        prst="ellipse",
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _step_card(
    sp_id: int,
    x: int,
    y: int,
    cx: int,
    cy: int,
    *,
    title: str,
    cue: str,
    fill: str,
    color: str = BLACK,
    value: str | None = None,
    focal: bool = False,
) -> str:
    paras = [paragraph([run(title, size=LABEL_9PT, bold=True, color=color, font=FONT)], align="ctr", space_after=55)]
    if value:
        paras.append(paragraph([run(value, size=VALUE_14PT, bold=True, color=color, font=FONT)], align="ctr", space_after=55))
    paras.append(paragraph([run(cue, size=FINEPRINT_8_5PT, color=color, font=FONT)], align="ctr"))
    return text_box(
        sp_id,
        f"ProcessStep{sp_id}",
        x,
        y,
        cx,
        cy,
        paras,
        fill=fill,
        line_width=19_050 if focal else 12_700,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _no_fill_text(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    text: str,
    *,
    size: int,
    italic: bool = False,
) -> str:
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        [paragraph([run(text, size=size, italic=italic, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _formula_box(sp_id: int, x: int, y: int, cx: int, cap_h: int, body_h: int) -> str:
    cap = text_box(
        sp_id,
        "FormulaBoxCap",
        x,
        y,
        cx,
        cap_h,
        [paragraph([run("APPLIED HEADLINE FORMULA", size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5,
        anchor="ctr",
        insets=INSETS_CARD,
    )
    body = text_box(
        sp_id + 1,
        "FormulaBoxBody",
        x,
        y + cap_h,
        cx,
        body_h,
        [
            paragraph([run("Average annual TAM = FY2022-FY2027 Basic Construction base multiplied by applied BC supplier coefficient, divided by 6.", size=MESSAGE_11PT, color=BLACK, font=FONT)], align="ctr", space_after=80),
            paragraph([run("$56.647B Basic Construction multiplied by 35.0% = ~$19.840B cumulative TAM", size=RIBBON_KPI_18PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=60),
            paragraph([run("divided by 6 = ~$3.307B average annual", size=RIBBON_KPI_18PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=80),
            paragraph([run("Broad component-manufacturing SAM = ~$16.833B cumulative; ~$2.806B average annual.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=BLUE_1,
        anchor="ctr",
        insets=INSETS_ANSWER_CARD,
    )
    return cap + body
def _scope_notes(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    paras = [
        paragraph([run("Scope notes", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)], space_after=130),
        paragraph([
            run("AP/LLTM: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("gross stream retained as reference evidence; additive headline base = $0.", size=LABEL_9PT, color=BLACK, font=FONT),
        ], bullet=True, space_after=120),
        paragraph([
            run("SAM: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run("scenario inclusion menu only; no SOM, capture, or win-probability haircut is applied.", size=LABEL_9PT, color=BLACK, font=FONT),
        ], bullet=True),
    ]
    return text_box(
        sp_id,
        "ScopeNotesRail",
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(137_160, 80_000, 137_160, 80_000),
    )
def _body() -> str:
    rail_y = BODY_Y + 260_000
    dot_d = 220_000
    dot_y = rail_y - dot_d // 2
    card_y = BODY_Y + 430_000
    card_h = 900_000
    note_y = BODY_Y + 1_400_000
    note_h = 190_000
    formula_y = BODY_Y + 1_710_000
    formula_cap_h = 330_000
    formula_body_h = 1_050_000
    scope_y = BODY_Y + 3_270_000
    scope_h = 900_000
    xs, step_w = _grid_x(7)
    centers = [x + step_w // 2 for x in xs]
    steps = [
        ("Budget base", "P-5c Basic Construction; P-10 reference", BLUE_1, BLACK, None, False),
        ("Remove flows", "GFE, BPMI, SIB, yards, depot, AP overlap", BLUE_1, BLACK, None, False),
        ("Apply coefficient", "POP-derived, non-nuclear, yard-excluded", BLUE_2, BLACK, "35.0%", False),
        ("Calculate TAM", "BC base multiplied by coefficient; AP add = $0", BLUE_1, BLACK, None, False),
        ("Allocate buckets", "FFATA and FSRS; SAM.gov NAICS mapping", BLUE_1, BLACK, None, False),
        ("Apply flags", "scenario inclusion menu, not capture", BLUE_1, BLACK, None, False),
        ("SAM output menu", "broad, electrical, metal, modular, HM&E; no SOM", BLUE_4, WHITE, None, True),
    ]
    out = []
    out.append(connector(10, "ProcessConnectorRail", centers[0], rail_y, centers[-1] - centers[0], 0, color=GRAY_4, width=CONNECTOR_NORMAL, arrow=False))
    for idx, center in enumerate(centers, start=1):
        out.append(_step_dot(20 + idx, center - dot_d // 2, dot_y, dot_d, idx))
    for idx, (x, step) in enumerate(zip(xs, steps), start=1):
        title, cue, fill, color, value, focal = step
        out.append(_step_card(40 + idx, x, card_y, step_w, card_h, title=title, cue=cue, fill=fill, color=color, value=value, focal=focal))
    out.append(_no_fill_text(60, "FormulaLeadIn", BODY_X, note_y, BODY_CX, note_h, "The headline model is intentionally simple; complexity is handled in the evidence and exclusions.", size=CHART_TITLE_10PT, italic=True))
    out.append(_formula_box(70, BODY_X, formula_y, BODY_CX, formula_cap_h, formula_body_h))
    out.append(_scope_notes(90, BODY_X, scope_y, BODY_CX, scope_h))
    return "".join(out)
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
