"""sam_bucket_crosswalk - map classified work-type buckets into overlapping SAM scenario cuts."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.style import *
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

TITLE_BAND_H = 190_000

# --- chrome (unchanged from the original main module) ---
_SECTION = "Appendix"
_TOPIC = "SAM Bucket Crosswalk"
_TAKEAWAY = "NAICS and vendor evidence map TAM into scenario cuts"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API"


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = BLACK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=BLACK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=BLACK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=BLACK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _chart_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_BAND_H,
                    [_txt(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, align="l")],
                    fill=None, line_color=None, insets=INSETS_NONE, anchor="t")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


_ROWS = [
    ["Bucket", "Evidence cues (NAICS-4; example vendor)", "Broad", "Metal", "Modular", "HM&E", "Elec"],
    ["Structural fab / pre-outfit", "3323, 3324, 3366, 3369; e.g. DC Fabricators, Rhoads", "Yes", "Yes", "Yes", "No", "No"],
    ["Machining", "3327, 3336; e.g. Advance Mfg., B. & F. Machine", "Yes", "Yes", "No", "Yes", "No"],
    ["Castings and forgings", "3321, 3315, 3312; e.g. Scot Forge", "Yes", "Yes", "No", "No", "No"],
    ["Piping / valves / pumps", "3329, 3339, 4235; e.g. Curtiss-Wright, CIRCOR", "Yes", "No", "No", "Yes", "No"],
    ["Electrical / power", "3353, 3344, 3359, 3364; e.g. Northrop Grumman, Leonardo", "Yes", "No", "No", "No", "Yes"],
    ["HVAC / ventilation", "3334; e.g. Johnson Controls Navy Systems", "Yes", "No", "No", "Yes", "No"],
    ["Coatings / insulation", "3252, 3259, 3262; e.g. Globe Composite", "Yes", "No", "Yes", "No", "No"],
    ["Residual (Unbucketed / ambiguous)", "no clean NAICS bucket; e.g. ESCO, L3Harris, BWX", "No", "No", "No", "No", "No"],
]


def _body() -> str:
    out = []
    out.append(_chart_title(10, "Work-type bucket to SAM scenario crosswalk", BODY_X, BODY_Y, BODY_CX))
    note_y = BODY_B - 300_000
    table_y = BODY_Y + TITLE_BAND_H + 35_000
    col_w = _widths(BODY_CX, [2.6, 3.6, 0.85, 0.85, 0.95, 0.85, 0.85])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=274_320)
    fills = {}
    for c in range(7):
        fills[(8, c)] = GRAY_3
    bold = {(8, 0): True}
    out.append(house_table(20, "Crosswalk", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="light", size=900,
                           aligns=["l", "l", "ctr", "ctr", "ctr", "ctr", "ctr"], cell_fills=fills, cell_bold=bold))
    out.append(_note(30, "NoSum", BODY_X, note_y, BODY_CX, 240_000,
        "Scenario cuts overlap; do not sum scenarios (machining is in both Metal and HM&E). Broad SAM excludes the unbucketed / ambiguous residual. No SOM is modeled.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
