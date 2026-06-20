"""implications - Build the closing scenario prioritization scorecard slide."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_1, BLACK, FONT, INSETS_NONE,
    CHART_TITLE_10PT, FINEPRINT_8_5PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Implications"
_TAKEAWAY = "Prioritization depends on product scope, qualification burden, and confidence in bucket visibility"
_SOURCES = "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (3) GAO-25-106286"

GAP = 91_440
TITLE_H = 160_000
TITLE_GAP = 70_000

_ROWS = [
    ["Scenario",                    "Avg annual",     "Cumulative", "TAM share", "Confidence",  "Priority read"],
    ["Broad component manufacturing", "~$327M per year", "~$1.96B",   "57.1%",     "Medium",      "Envelope, not a single wedge"],
    ["Metal components",            "~$170M per year", "~$1.02B",    "29.6%",     "Medium-high", "Largest targeted scenario; high if fabrication or machining scope fits"],
    ["Electrical and power",        "~$132M per year", "~$791M",     "23.0%",     "Medium",      "Largest single named bucket; high but qualification-heavy"],
    ["Modular assemblies",          "~$104M per year", "~$626M",     "18.2%",     "Medium",      "Strategic distributed-capacity lane; smaller in the current model"],
    ["HM&E components",             "~$89M per year",  "~$531M",     "15.4%",     "Medium-low",  "Selective, product-by-product; evidence-dependent"],
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


def _note(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(sp_id, "WhereToPlayNote", x, y, cx, cy,
                    [
                        paragraph([run("Where-to-play screen, not SOM. ", size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT),
                                   run("Prioritization depends on product scope, qualification burden, and confidence in bucket visibility.", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)]),
                        paragraph([run("Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture.", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)]),
                    ],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _body() -> str:
    title_y = BODY_Y
    table_y = BODY_Y + TITLE_H + TITLE_GAP
    col_w = _ratio_widths(BODY_CX, [2.6, 1.5, 1.4, 1.1, 1.5, 3.2])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.5, header_size_pt=9.5, min_row_h=274_320)
    table_h = sum(row_h)
    note_y = table_y + table_h + GAP
    note_h = max(430_000, BODY_B - note_y - 120_000)

    title = _exhibit_title("Scenario prioritization scorecard, average annual FY22-27", BODY_X, title_y, BODY_CX, sp_id=20)
    table = house_table(21, "ScenarioPrioritizationScorecard", BODY_X, table_y, col_w, _ROWS,
                        row_h=row_h, table_skin="dark", size=950,
                        aligns=["l", "r", "r", "ctr", "ctr", "l"],
                        cell_fills={(2, 5): BLUE_1, (3, 5): BLUE_1})
    note = _note(22, BODY_X, note_y, BODY_CX, note_h)
    return title + table + note


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Implications", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
