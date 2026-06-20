"""market_direction - Build the qualitative distributed-shipbuilding evidence timeline slide."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLACK, FONT, INSETS_NONE, INSETS_MESSAGE,
    CHART_TITLE_10PT, LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Market Direction"
_TAKEAWAY = "Distributed shipbuilding points toward more external production capacity"
_SOURCES = "Sources: (1) HII quarterly earnings materials, FY2024 Q3-FY2026 Q1; (2) General Dynamics earnings materials, FY2025 Q4-FY2026 Q1; (3) GAO-25-106286"

GAP = 91_440
TITLE_H = 160_000
TITLE_GAP = 70_000

_ROWS = [
    ["Period",    "Source",           "Signal",                                                                       "Implication"],
    ["FY24 Q3",   "HII",              "Outsourcing over 1 million hours in 2024; planned increase of more than 30% in 2025", "Outsourcing is now a named lever"],
    ["FY25 Q4",   "HII",              "Outsourcing doubled year over year in 2025; 30% planned in 2026; over 23 vendors established", "Supplier network is scaling"],
    ["FY26 Q1",   "HII",              "On track to grow outsourcing hours ~30%; first 2 of 32 units in yard from partners on DDG 137", "Distributed work reaching the DDG line"],
    ["FY25 Q4",   "General Dynamics", "Supply chain remains the gating item in an Electric Boat context; no comparable DDG outsourcing-hours target", "Constraint is broad, not a DDG plan"],
    ["FY25-FY26", "Navy and GAO",     "Shipbuilders already outsource to overcome constrained physical space; distributed production policy", "Directional tailwind"],
]


def _exhibit_title(text: str, x: int, y: int, cx: int, *, sp_id: int) -> str:
    return text_box(sp_id, "ExhibitTitle", x, y, cx, TITLE_H,
                    [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _ratio_widths(total: int, ratios: list[float]) -> list[int]:
    s = sum(ratios)
    widths = [int(total * r / s) for r in ratios[:-1]]
    widths.append(total - sum(widths))
    return widths


def _interpretation_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Direction:", "external production capacity is expanding, especially at HII Ingalls."),
        ("Asymmetry:", "HII has the clearest public commitment; GD signals supplier constraints, submarine-centric."),
        ("Scope:", "directional only; it does not change the FY22-27 TAM math without a refreshed model."),
    ]
    paras = []
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph([
            run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(body, size=LABEL_9PT, color=BLACK, font=FONT),
        ], bullet=True, space_after=110 if i < len(bullets) - 1 else 0))
    return text_box(sp_id, "InterpretationRail", x, y, cx, cy, paras,
                    fill=None, line_color=None, anchor="t", insets=INSETS_MESSAGE)


def _body() -> str:
    title_y = BODY_Y
    table_y = BODY_Y + TITLE_H + TITLE_GAP
    col_w = _ratio_widths(BODY_CX, [1.1, 1.4, 4.3, 2.4])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.5, header_size_pt=9.5, min_row_h=274_320)
    table_h = sum(row_h)
    rail_y = table_y + table_h + GAP
    rail_h = min(1_070_000, BODY_B - rail_y - 60_000)

    title = _exhibit_title("Distributed-shipbuilding signals, FY2024 Q3 to FY2026 Q1", BODY_X, title_y, BODY_CX, sp_id=20)
    table = house_table(21, "MarketDirectionTimeline", BODY_X, table_y, col_w, _ROWS,
                        row_h=row_h, table_skin="rule", size=950,
                        aligns=["l", "l", "l", "l"])
    rail = _interpretation_rail(22, BODY_X, rail_y, BODY_CX, rail_h)
    return title + table + rail


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Market Direction", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
