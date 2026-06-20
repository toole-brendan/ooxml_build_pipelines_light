"""data_limits - distinguish FFATA-visible evidence from the larger under-observed supplier layer."""
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
    GRAY_1,
    GRAY_2,
    BLACK,
    FONT,
    INSETS_CARD,
    INSETS_NONE,
    INSETS_MICRO_CAP,
    FINEPRINT_8_5PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    CAP_12PT,
)
LAYOUT = "slideLayout4"
# _TOPIC is title-cased because title_placeholder uses it for the visible title.
_SECTION = "Market Sizing"
_TOPIC = "Data Limits"
_TAKEAWAY = "FFATA captures a visible floor, not the full supplier layer"
_SOURCES = "Sources: (1) FAR 52.204-10; (2) SAM.gov FFATA and FSRS records; (3) General Dynamics and HII Form 10-K filings"
_GAP = 160_000
_PANEL_H = 2_800_000
_PANEL_W = (BODY_CX - _GAP) // 2
_CALLOUT_Y = BODY_Y + _PANEL_H + 120_000
_CALLOUT_H = 350_000
_GUARD_Y = _CALLOUT_Y + _CALLOUT_H + 120_000
_GUARD_H = 950_000
def _ledger_panel(sp_id: int, x: int, title: str, bullets: list[str], *, fill: str) -> str:
    paras = [
        paragraph(
            [run(title, size=CAP_12PT, bold=True, color=BLACK, font=FONT)],
            space_after=180,
        )
    ]
    for i, bullet in enumerate(bullets):
        paras.append(
            paragraph(
                [run(bullet, size=DENSE_BODY_10PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=95 if i < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id,
        title.title().replace(" ", ""),
        x,
        BODY_Y,
        _PANEL_W,
        _PANEL_H,
        paras,
        fill=fill,
        anchor="t",
        insets=INSETS_CARD,
    )
def _guardrail_chip(sp_id: int, x: int, cx: int, label: str, text: str, *, fill: str) -> str:
    return text_box(
        sp_id,
        "GuardrailChip",
        x,
        _GUARD_Y,
        cx,
        _GUARD_H,
        [
            paragraph(
                [run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)],
                align="ctr",
                space_after=90,
            ),
            paragraph(
                [run(text, size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)],
                align="ctr",
            ),
        ],
        fill=fill,
        anchor="ctr",
        insets=INSETS_MICRO_CAP,
    )
def _body() -> str:
    left_bullets = [
        "FFATA-visible first-tier subawards",
        "Named vendors and parent entities",
        "SAM.gov Entity NAICS enrichment",
        "DoD Contracts POP evidence",
        "SCN P-5c and P-10 budget exhibits",
    ]
    right_bullets = [
        "Purchased material booked as direct material",
        "Lower-tier subcontracts",
        "HII Newport News visibility gap",
        "Standing supplier agreements",
        "Reporting lag",
        "Unparsed single-site POP rows",
    ]
    guard_gap = 80_000
    guard_w = (BODY_CX - 3 * guard_gap) // 4
    guard_xs = [BODY_X + i * (guard_w + guard_gap) for i in range(4)]
    return (
        _ledger_panel(10, BODY_X, "VISIBLE AND MEASURED LAYER", left_bullets, fill=BLUE_1)
        + _ledger_panel(11, BODY_X + _PANEL_W + _GAP, "UNSEEN OR UNDER-OBSERVED LAYER", right_bullets, fill=GRAY_1)
        + text_box(
            20,
            "MainCallout",
            BODY_X,
            _CALLOUT_Y,
            BODY_CX,
            _CALLOUT_H,
            [
                paragraph(
                    [
                        run("Visible data ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                        run(
                            "is strong enough to classify and triangulate, not complete enough to equal the whole supplier layer.",
                            size=DENSE_BODY_10PT,
                            color=BLACK,
                            font=FONT,
                        ),
                    ],
                    align="ctr",
                )
            ],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
        )
        + _guardrail_chip(30, guard_xs[0], guard_w, "MODEL GUARDRAIL", "No SOM or capture modeled", fill=GRAY_2)
        + _guardrail_chip(31, guard_xs[1], guard_w, "DOUBLE-COUNT CHECK", "AP/LLTM additive base = $0", fill=GRAY_2)
        + _guardrail_chip(32, guard_xs[2], guard_w, "DOLLAR BASIS", "Nominal then-year dollars", fill=GRAY_2)
        + _guardrail_chip(33, guard_xs[3], BODY_X + BODY_CX - guard_xs[3], "SUPPLIER VISIBILITY", "FFATA-visible = named floor", fill=BLUE_1)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
