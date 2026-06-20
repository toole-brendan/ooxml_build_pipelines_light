"""sam_taxonomy — generated from the DDG slide spec.

Intent: Transition from TAM to SAM by defining the named bucket menu, keeping the unbucketed residual explicit, and showing that the five scenarios are alternative inclusion cuts of the same seven buckets, never additive pools.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'SAM taxonomy'
_TITLE_TOPIC = 'SAM Taxonomy'
_TAKEAWAY = 'SAM is a work-type bucket menu, not a capture forecast'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122'

_CHART_SPECS = []
_TABLES = [{
  'id': 'scenario_membership_1',
  'element': 'e11',
  'role': 'chart_side_evidence',
  'factory': 'house_table',
  'semantic': {'table_name': 'Scenario membership cue',
               'purpose': 'define',
               'reader_takeaway': 'Each scenario is an alternative inclusion cut of the same seven named buckets; do not sum.',
               'row_order': 'structural, machining, castings, piping, electrical, HVAC, coatings',
               'highlight_rows': [],
               'guardrails': ['Scenario definitions overlap; they are not additive.',
                              'Residual remains explicit and outside broad component SAM.']},
  'render': {'table_skin': 'rule',
             'size': 800,
             'column_widths': {'mode': 'ratio',
                               'values': [3.4, 1.0, 1.0, 1.0, 1.0, 1.0],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'ctr', 'ctr', 'ctr', 'ctr', 'ctr'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Bucket', 'Metal', 'HM&E', 'Elec', 'Modular', 'Broad'],
                      ['Structural', 'Yes', 'No', 'No', 'Yes', 'Yes'],
                      ['Machining', 'Yes', 'Yes', 'No', 'No', 'Yes'],
                      ['Castings', 'Yes', 'No', 'No', 'No', 'Yes'],
                      ['Piping', 'No', 'Yes', 'No', 'No', 'Yes'],
                      ['Electrical', 'No', 'No', 'Yes', 'No', 'Yes'],
                      ['HVAC', 'No', 'Yes', 'No', 'No', 'Yes'],
                      ['Coatings', 'No', 'No', 'No', 'Yes', 'Yes']],
             'cell_fills': {'(1,1)': 'BLUE_1', '(1,4)': 'BLUE_1', '(1,5)': 'BLUE_1',
                            '(2,1)': 'BLUE_1', '(2,2)': 'BLUE_1', '(2,5)': 'BLUE_1',
                            '(3,1)': 'BLUE_1', '(3,5)': 'BLUE_1',
                            '(4,2)': 'BLUE_1', '(4,5)': 'BLUE_1',
                            '(5,3)': 'BLUE_1', '(5,5)': 'BLUE_1',
                            '(6,2)': 'BLUE_1', '(6,5)': 'BLUE_1',
                            '(7,4)': 'BLUE_1', '(7,5)': 'BLUE_1'},
             'cell_bold': {'(1,1)': True, '(1,4)': True, '(1,5)': True,
                           '(2,1)': True, '(2,2)': True, '(2,5)': True,
                           '(3,1)': True, '(3,5)': True,
                           '(4,2)': True, '(4,5)': True,
                           '(5,3)': True, '(5,5)': True,
                           '(6,2)': True, '(6,5)': True,
                           '(7,4)': True, '(7,5)': True},
             'cell_text_colors': {},
             'footnotes': ['Blue cells indicate scenario membership. Scenarios overlap and should not be summed.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(text_box(10, "TAMBanner", BODY_X, BODY_Y, BODY_CX, 720_000,
        [p("PORTFOLIO TAM", size=CAP_12PT, bold=True, color=WHITE, align="ctr"),
         p("~$573M per year", size=RIBBON_KPI_18PT, bold=True, color=WHITE, align="ctr"),
         p("(~$3.44B FY22 to FY27 cumulative)", size=LABEL_9PT, italic=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color=BLACK, line_width=STRONG_LINE, insets=INSETS_ANSWER_CARD, anchor="ctr"))
    chip_y0 = BODY_Y + 920_000
    chip_w = int(BODY_CX * 0.295)
    chip_h = 335_000
    col2 = BODY_X + chip_w + GAP
    buckets = [
        ("Structural fabrication", "and pre-outfit"), ("Machining", "precision and mechanical"),
        ("Castings and forgings", "metal components"), ("Piping, valves, and pumps", "HM&E path"),
        ("Electrical and power", "standalone scenario"), ("HVAC and ventilation", "HM&E path"),
        ("Coatings and insulation", "modular path"),
    ]
    coords = [(BODY_X, chip_y0), (col2, chip_y0), (BODY_X, chip_y0+chip_h+GAP), (col2, chip_y0+chip_h+GAP), (BODY_X, chip_y0+2*(chip_h+GAP)), (col2, chip_y0+2*(chip_h+GAP)), (BODY_X, chip_y0+3*(chip_h+GAP))]
    for i, ((cap, body), (x, y)) in enumerate(zip(buckets, coords)):
        out.append(chip(20+i, f"Bucket{i}", x, y, chip_w, chip_h, cap, body, fill=BLUE_1, line_color=BLACK))
    rx = BODY_X + int(BODY_CX * 0.67)
    rw = BODY_R - rx
    out.append(chip(30, "Residual", rx, chip_y0, rw, 590_000, "Unbucketed and ambiguous", "42.9% of TAM", value="~$246M per year", fill=GRAY_3, line_color=BLACK))
    out.append(nofill(31, "SAMNote", rx, chip_y0 + 680_000, rw, 600_000,
        [lead_body("SAM:", "selects from named work-type buckets inside TAM. It does not apply win probability, and scenarios are not additive.", lead_size=FINEPRINT_8_5PT, body_size=LABEL_9PT)], anchor="t"))
    tbl_y = BODY_Y + 2_650_000
    tbl, h = make_table(40, "ScenarioMembership", BODY_X, tbl_y, BODY_CX, _TABLES[0], size_override=820, min_row_h=180_000)
    out.append(tbl)
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
