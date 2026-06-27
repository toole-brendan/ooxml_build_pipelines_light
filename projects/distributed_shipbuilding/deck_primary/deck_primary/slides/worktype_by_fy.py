"""worktype_by_fy — deck_primary slide 5 (outsourced BC capability-domain mix by FY).

EXHIBIT — Capability-Domain COMPOSITION of outsourced Basic Construction subaward
dollars by program and fiscal year: a native percent-stacked column chart, 12
program-year bars (DDG-51 / Virginia / Columbia × FY2022–25), each normalized to
100% and split across the 12 Capability-Domain archetypes (D1–D11, D0), with a
right-side legend. Shows how each program's domain mix shifts year to year.

REBUILD (2026-06-26): re-pointed to the updated SAM classification workbook
(workbook_award_classification_refactor). The old 7-NAICS-work-type exhibit (a
bundled think-cell chart + verbatim overlay with a penetration strip) is replaced
by a native deck_core column_chart (percent mode) driven by a Python DATA literal —
the 12 Capability Domains are the published axis. Series values are net subaward $M
per (program, FY, domain) from the recalced Supplier-Year Activity sheet (federal FY
of the subaward action); the factory normalizes each bar to 100%. All three programs
have real FY22–25 subaward data (DDG-51 included); DDG-51's subawards also span
FY13–21, not shown here. Title/subtitle are neutral (per the rebuild brief). The
prior bundled chart, its .xlsb, and the verbatim overlay (slide05.xml, incl. the $
total + penetration annotations) are retired; the per-bar $ total and penetration-%
annotations can be re-added as an overlay if wanted.

CODE MAP:
  • chrome ..... breadcrumb() + prelim_chip() + title_placeholder()
  • chart ...... CHARTS[0] = column_chart(percent) placed by graphic_frame() (rId2)
  • data ....... DOMAIN_SERIES — (code, legend label, fill, [12 program-year $M])
  • sources .... one text_box()
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, run, paragraph, text_box, breadcrumb, prelim_chip, title_placeholder,
)
from deck_core.charts import graphic_frame, column_chart
from deck_core.style import IN, PT, DK, FONT

LAYOUT = "slideLayout4"

# 12 program-year bars; program shown once per group, FY on each.
CATEGORIES = ["DDG-51 FY22", "FY23", "FY24", "FY25",
              "Virginia FY22", "FY23", "FY24", "FY25",
              "Columbia FY22", "FY23", "FY24", "FY25"]

# (code, legend label, fill hex, [net $M per (program, FY, domain) across the 12 bars])
# Source: recalced SAM Supplier-Year Activity sheet (federal FY); percent mode normalizes each bar.
DOMAIN_SERIES: list[tuple[str, str, str, list[float]]] = [
    ("D1",  "D1 · Hull & structures",       "1D4D68", [10.8, 7.9, 10.5, 36.1, 40.0, 141.4, 62.9, 46.2, 32.3, 229.7, 84.9, 30.1]),
    ("D2",  "D2 · Propulsion machinery",    "6E91B1", [49.4, 118.7, 140.9, 295.2, 74.8, 472.8, 126.1, 31.4, 30.7, 309.6, 241.0, 21.4]),
    ("D3",  "D3 · Electrical power",        "486D82", [15.5, 15.8, 122.5, 74.4, 3.7, 12.9, 20.4, 15.8, 45.3, 67.4, 67.7, 31.8]),
    ("D4",  "D4 · Fluid & piping",          "89A2B0", [20.7, 32.6, 70.7, 82.0, 31.2, 90.7, 137.2, 70.6, 57.2, 121.7, 125.5, 43.2]),
    ("D5",  "D5 · Thermal / HVAC",          "3D5972", [16.4, 68.0, 72.2, 131.3, 10.4, 97.0, 8.7, 25.5, 15.2, 29.2, 29.9, 20.9]),
    ("D6",  "D6 · Mission & combat",        "B6C8D8", [1.5, 4.8, 54.7, 5.9, 15.0, 2.2, 0.7, 0.3, 7.1, 285.9, 199.8, 276.9]),
    ("D7",  "D7 · Electronic components",   "AFC2CC", [19.4, 5.4, 5.8, 4.0, 16.1, 24.1, 11.4, 14.0, 6.0, 34.2, 12.3, 4.8]),
    ("D8",  "D8 · Mechanical handling",     "263746", [9.2, 6.3, 38.8, 19.8, 0.3, 1.0, 3.3, 0.2, 36.4, 0.0, 2.9, 7.8]),
    ("D9",  "D9 · Specialty materials",     "79838F", [9.7, 3.6, 35.5, 29.8, 35.8, 94.7, 57.4, 41.0, 45.1, 42.5, 43.0, 56.3]),
    ("D10", "D10 · Interiors & outfitting", "D8E3EB", [3.6, 8.2, 5.1, 3.9, 6.8, 3.9, 3.5, 0.4, 0.6, 0.5, 0.5, 0.1]),
    ("D11", "D11 · Services",               "7F7F7F", [3.1, 4.7, 3.7, 3.7, 2.4, 4.6, 6.7, 3.1, 9.9, 12.8, 9.9, 1.1]),
    ("D0",  "D0 · Unresolved",              "D9D9D9", [3.8, 13.5, 7.2, 12.0, 27.4, 56.4, 43.2, 13.7, 35.4, 56.2, 56.4, 11.7]),
]

CHARTS = [column_chart(
    mode="percent",
    categories=CATEGORIES,
    series=[{"name": lbl, "values": vals, "color": col} for (_c, lbl, col, vals) in DOMAIN_SERIES],
    show_legend=True, legend_pos="r",
    show_value_labels=False, show_cat_labels=True,
    show_value_axis_labels=False, show_gridlines=False,
    gap_width=40,
)]

_SRC_NOTE = (
    "Capability-Domain composition of FFATA/FSRS first-tier subawards on hull-builder new-construction "
    "PIIDs (GDEB; BIW + Ingalls), by program and federal fiscal year of the subaward action (net $, each "
    "bar normalized to 100%). DDG-51 subawards also span FY13–21 (not shown)."
)


def _body() -> str:
    out: list[str] = []
    out.append(breadcrumb("Executive Summary", "Supplier TAM and SAM"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Outsourced spend mix by capability domain, by fiscal year",
        "Capability-Domain composition of program-year subaward dollars (FY22–25, each bar = 100%)."))
    out.append(graphic_frame(sp_id=843, name="DomainByFY",
                             x=IN(0.5), y=IN(1.6), cx=IN(12.33), cy=IN(4.3), rId="rId2"))
    out.append(text_box(900, "Sources", IN(0.5), IN(6.55), IN(12.33), IN(0.6),
                        [paragraph([run(_SRC_NOTE, size=PT(8), color=DK, font=FONT)], line_spacing=100000)],
                        fill=None, line_color="none", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    return "".join(out)


def render() -> str:
    return slide(_body())
