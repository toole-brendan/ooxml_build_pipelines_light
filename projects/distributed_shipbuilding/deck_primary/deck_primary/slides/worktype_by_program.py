"""worktype_by_program — deck_primary slide 2 (outsourced BC by capability domain, by program).

EXHIBIT — outsourced Basic Construction spend apportioned by vendor Capability
Domain, by program: a native stacked-column chart (3 program bars — DDG-51,
Columbia, Virginia) split across the 12 Capability-Domain archetypes (D1–D11, D0),
with a right-side legend. Each bar totals that program's cumulative outsourced-BC
TAM (FY22–27, FY26$); the within-bar split is the program's SAM subaward
Capability-Domain mix.

REBUILD (2026-06-26): re-pointed to the updated SAM classification workbook
(workbook_award_classification_refactor). The old 7-NAICS-work-type exhibit (a
bundled think-cell chart + verbatim legend/label overlay) is replaced by a native
deck_core column_chart driven by a Python DATA literal — the 12 Capability Domains
are now the published axis. Values = each program's SAM Capability-Domain share
(recalced Domain Concentration sheet, FY26$) × that program's cumulative
outsourced-BC TAM ($6.42B DDG-51 / $4.51B Columbia / $13.64B Virginia), so the
column totals are unchanged from the prior exhibit. Title/subtitle are neutral
(per the rebuild brief). The prior bundled chart, its .xlsb, the verbatim
legend/label overlay (slide02.xml) and the 7-stage NAICS methodology ledger
(slide02_tables.xml) are retired here; if a methodology ledger is wanted back it
must be re-authored to the new D/P archetype method.

CODE MAP:
  • chrome ..... breadcrumb() + prelim_chip() + title_placeholder()
  • chart ...... CHARTS[0] = column_chart(stacked) placed by graphic_frame() (rId2)
  • data ....... DOMAIN_SERIES — (code, legend label, fill, [DDG, Columbia, Virginia] $B)
  • sources .... one text_box()
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, run, paragraph, text_box, breadcrumb, prelim_chip, title_placeholder,
)
from deck_core.charts import graphic_frame, column_chart
from deck_core.style import IN, PT, DK, FONT

LAYOUT = "slideLayout4"

# Categories = program bars; column total = program cumulative outsourced-BC TAM ($B).
CATEGORIES = ["DDG-51", "Columbia", "Virginia"]

# (code, legend label, fill hex, [DDG-51, Columbia, Virginia] $B)
# value = SAM Capability-Domain share (recalced Domain Concentration, FY26$) × program TAM cumulative.
DOMAIN_SERIES: list[tuple[str, str, str, list[float]]] = [
    ("D1",  "D1 · Hull & structures",       "1D4D68", [0.1730, 0.6539, 1.4284]),
    ("D2",  "D2 · Propulsion machinery",    "6E91B1", [1.8948, 0.8547, 5.5385]),
    ("D3",  "D3 · Electrical power",        "486D82", [0.8650, 0.3181, 0.3627]),
    ("D4",  "D4 · Fluid & piping",          "89A2B0", [0.7859, 0.5628, 2.1187]),
    ("D5",  "D5 · Thermal / HVAC",          "3D5972", [1.0267, 0.1553, 0.8552]),
    ("D6",  "D6 · Mission & combat",        "B6C8D8", [0.2846, 1.0329, 0.1790]),
    ("D7",  "D7 · Electronic components",   "AFC2CC", [0.1465, 0.1105, 0.7115]),
    ("D8",  "D8 · Mechanical handling",     "263746", [0.2753, 0.0612, 0.0292]),
    ("D9",  "D9 · Specialty materials",     "79838F", [0.2549, 0.3387, 1.3147]),
    ("D10", "D10 · Interiors & outfitting", "D8E3EB", [0.1382, 0.0051, 0.1579]),
    ("D11", "D11 · Services",               "7F7F7F", [0.0502, 0.0708, 0.0968]),
    ("D0",  "D0 · Unresolved",              "D9D9D9", [0.5266, 0.3430, 0.8439]),
]

CHARTS = [column_chart(
    mode="stacked",
    categories=CATEGORIES,
    series=[{"name": lbl, "values": vals, "color": col} for (_c, lbl, col, vals) in DOMAIN_SERIES],
    show_legend=True, legend_pos="r",
    show_value_labels=False, show_cat_labels=True,
    show_value_axis_labels=False, show_gridlines=False,
    gap_width=140,
)]

_SRC_NOTE = (
    "Capability-Domain shares from FFATA/FSRS first-tier subawards on hull-builder new-construction "
    "PIIDs (GDEB; BIW + Ingalls), classified per vendor; applied to each program's cumulative "
    "outsourced-BC TAM (FY22–27, FY26$). Bars total the program TAM "
    "($6.4B DDG-51 / $4.5B Columbia / $13.6B Virginia)."
)


def _body() -> str:
    out: list[str] = []
    out.append(breadcrumb("Executive Summary", "Supplier TAM and SAM"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Outsourced spend by capability domain, by program",
        "Cumulative outsourced Basic Construction TAM (FY22–27, FY26$), apportioned by vendor Capability Domain."))
    out.append(graphic_frame(sp_id=352, name="DomainByProgram",
                             x=IN(0.5), y=IN(1.6), cx=IN(12.33), cy=IN(4.3), rId="rId2"))
    out.append(text_box(900, "Sources", IN(0.5), IN(6.55), IN(12.33), IN(0.6),
                        [paragraph([run(_SRC_NOTE, size=PT(8), color=DK, font=FONT)], line_spacing=100000)],
                        fill=None, line_color="none", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    return "".join(out)


def render() -> str:
    return slide(_body())
