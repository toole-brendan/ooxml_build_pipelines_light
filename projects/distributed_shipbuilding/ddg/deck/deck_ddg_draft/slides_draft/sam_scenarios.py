"""sam_scenarios — generated from the DDG slide spec.

Intent: Show the five scenario sizes and make obvious that scenarios are alternative serviceable-market definitions, not additive submarkets; land broad as the envelope and metal as the largest single targetable wedge.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'SAM scenarios'
_TITLE_TOPIC = 'SAM Scenarios'
_TAKEAWAY = 'Broad component manufacturing represents ~$327M per year of serviceable market'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['Broad component manufacturing (57.1%)',
                          'Metal components (29.6%)',
                          'Electrical and power (23.0%)',
                          'Modular assemblies (18.2%)',
                          'HM&E components (15.4%)'],
           'series': [{'name': 'Average annual SAM',
                       'values': [327.3, 169.7, 131.8, 104.3, 88.5],
                       'data_point_colors': ['BLUE_5', 'BLUE_4', 'BLUE_3', 'BLUE_2', 'BLUE_1']}]},
  'params': {'mode': 'ranked',
             'value_axis_format': '"$"#,##0"M"',
             'show_legend': False,
             'show_gridlines': True,
             'major_gridline_color': 'GRAY_1',
             'show_value_labels': True,
             'value_label_format': '"$"#,##0"M"',
             'value_label_size_pt': 9,
             'cat_label_size_pt': 9,
             'gap_width': 45,
             'cat_header': 'Scenario',
             'title': None},
  'external_title': {'text': 'SAM scenarios, average annual FY22-27',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': []}]
_TABLES = [{'id': 'matrix_1',
  'element': 'e3',
  'role': 'chart_side_evidence',
  'factory': 'house_table',
  'semantic': {'table_name': 'Scenario inclusion cue',
               'purpose': 'define',
               'reader_takeaway': 'Each scenario is a different inclusion cut of the same seven '
                                  'buckets.',
               'row_order': 'structural, machining, castings, piping, electrical, HVAC, coatings',
               'highlight_rows': [],
               'guardrails': ['Yes/No flags must match the Scenarios tab definitions exactly.',
                              'Scenarios overlap; do not sum.']},
  'render': {'table_skin': 'rule',
             'size': 900,
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
             'cell_fills': {},
             'cell_bold': {'(1,1)': True,
                           '(1,4)': True,
                           '(1,5)': True,
                           '(2,1)': True,
                           '(2,2)': True,
                           '(2,5)': True,
                           '(3,1)': True,
                           '(3,5)': True,
                           '(4,2)': True,
                           '(4,5)': True,
                           '(5,3)': True,
                           '(5,5)': True,
                           '(6,2)': True,
                           '(6,5)': True,
                           '(7,4)': True,
                           '(7,5)': True},
             'cell_text_colors': {},
             'footnotes': ['Scenarios are alternative serviceable-market definitions. Do not sum '
                           'them.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX * 0.60)
    mx = BODY_X + chart_w + GAP
    mw = BODY_R - mx
    out.append(exhibit_title(10, "SAM scenarios, average annual FY22-27", BODY_X, BODY_Y, chart_w))
    out.append(chart(20, "SAMScenarioChart", BODY_X, BODY_Y + 240_000, chart_w, 3_360_000, "rId2"))
    tbl, h = make_table(30, "ScenarioMatrix", mx, BODY_Y + 240_000, mw, _TABLES[0], size_override=830, min_row_h=190_000)
    out.append(tbl)
    out.append(sizing_note(40, "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
