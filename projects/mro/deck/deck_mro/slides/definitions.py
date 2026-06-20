"""definitions - five sizing levels: nested rings + Level/Definition table (v3.3 slide 3).

Faithful port: chrome via deck_core builders, five concentric ellipses (blue ramp)
with centered level labels on the left, and a Level/Definition house_table on the
right with the Company TCV / Company ACV rows greyed as 'Future effort'.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip,
    run, paragraph, text_box, house_table,
)
from deck_core.style import (
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, GRAY_1, GRAY_4,
    BLACK, WHITE, FONT, INSETS_NONE,
    VALUE_14PT,
)

LAYOUT = "slideLayout4"

_SECTION = "TAM"
_TOPIC = "Definitions"
_TAKEAWAY = "Sizing breaks the MRO market into five nested levels."

_RING_BORDER = "C0C0C0"

# (fill, x, y, cx, cy) — concentric ellipses, outermost first
_RINGS = [
    (BLUE_1, 436168, 1195120, 5212080, 5212080),
    (BLUE_2, 847648, 2018080, 4389120, 4389120),
    (BLUE_3, 1259128, 2841040, 3566160, 3566160),
    (BLUE_4, 1624888, 3664000, 2834640, 2743200),
    (BLUE_5, 2082088, 4486960, 1920240, 1920240),
]
# (label, fill, text color, y)
_LABELS = [
    ("Total Funding", BLUE_1, BLACK, 1430121),
    ("TAM", BLUE_2, BLACK, 2253081),
    ("SAM", BLUE_3, WHITE, 3161080),
    ("Saronic TCV", BLUE_4, WHITE, 4069080),
    ("Saronic ACV", BLUE_5, WHITE, 5303520),
]
_LABEL_X, _LABEL_W, _LABEL_H = 2150668, 1782165, 352958

# Level/Definition table (right). rows[0] = header.
_TBL_X, _TBL_Y = 6096304, 1559966
_COL_W = [1575511, 4063593]
_ROW_H = [366674, 822960, 822960, 822960, 822960, 822960]
_TABLE = [
    ["Level", "Definition"],
    ["Total Funding", "All Service-PSC code award spending for US Navy and US Coast Guard in FY2025"],
    ["Total Addressable Market (TAM)", "Reconciled FPDS-visible MRO TAM: 65 services-PSC MRO + embedded PSC 1905 MRO (~$9.0B)"],
    ["Serviceable Addressable Market (SAM)", "Scenario-selected subset of TAM atoms; Broad Addressable (~$7.1B, TAM less captive SUPSHIP & FMS) narrowing to Depot Ship Repair on Marauder-type platforms"],
    ["Saronic TCV", "Share of SAM that Saronic can likely capture"],
    ["Saronic ACV", "Portion of TCV expected to convert into annual contract value"],
]


def _body() -> str:
    out = []
    # nested rings
    for i, (fill, x, y, cx, cy) in enumerate(_RINGS):
        out.append(text_box(
            20 + i, f"Ring{i}", x, y, cx, cy, [paragraph([])],
            fill=fill, line_color=_RING_BORDER, line_width=3175, prst="ellipse",
        ))
    # ring labels (centered, on top of the rings)
    for i, (text, fill, color, y) in enumerate(_LABELS):
        out.append(text_box(
            30 + i, f"RingLabel{i}", _LABEL_X, y, _LABEL_W, _LABEL_H,
            [paragraph([run(text, size=VALUE_14PT, bold=True, color=color, font=FONT)], align="ctr")],
            fill=fill, line_color="none", anchor="ctr", insets=INSETS_NONE,
        ))

    # Level / Definition table — grey the two future-effort rows
    grey_cells = {(r, c): GRAY_1 for r in (4, 5) for c in (0, 1)}
    grey_text = {(r, c): GRAY_4 for r in (4, 5) for c in (0, 1)}
    bold = {(0, 0): True, (0, 1): True}
    out.append(house_table(
        50, "DefinitionsTable", _TBL_X, _TBL_Y, _COL_W, _TABLE,
        row_h=_ROW_H, table_skin="rule", aligns=["l", "l"], size=1100,
        cell_fills=grey_cells, cell_text_colors=grey_text, cell_bold=bold,
    ))
    # "Future effort" tag at the bottom-left of the greyed rows
    out.append(text_box(
        60, "FutureEffort", _TBL_X, _TBL_Y + sum(_ROW_H) + 30_000, 2_400_000, 250_000,
        [paragraph([run("Future capture layer", size=1000, bold=True, italic=True, color=BLACK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    ))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
    )
