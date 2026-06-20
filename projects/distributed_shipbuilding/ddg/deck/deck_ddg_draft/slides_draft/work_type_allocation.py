"""work_type_allocation — generated from the DDG slide spec.

Intent: Rank portfolio TAM by work type, identify the largest named buckets, and keep the unbucketed residual visible and visually distinct so the reader does not mistake it for a named target lane.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Work-type allocation'
_TITLE_TOPIC = 'Work-Type Allocation'
_TAKEAWAY = 'Residual ambiguity is the largest line, while electrical and structural are the largest named buckets'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['Unbucketed / ambiguous (42.9%)',
                          'Electrical and power (23.0%)',
                          'Structural fabrication and pre-outfit (17.7%)',
                          'Machining (11.4%)',
                          'Piping, valves, and pumps (2.3%)',
                          'HVAC and ventilation (1.7%)',
                          'Coatings and insulation (0.5%)',
                          'Castings and forgings (0.5%)'],
           'series': [{'name': 'Average annual TAM',
                       'values': [245.8, 131.8, 101.4, 65.6, 13.0, 9.9, 2.8, 2.7],
                       'data_point_colors': ['GRAY_3',
                                             'BLUE_5',
                                             'BLUE_4',
                                             'BLUE_3',
                                             'BLUE_1',
                                             'BLUE_1',
                                             'BLUE_1',
                                             'BLUE_1']}]},
  'params': {'mode': 'ranked',
             'value_axis_format': '"$"#,##0"M"',
             'show_legend': False,
             'show_gridlines': True,
             'major_gridline_color': 'GRAY_1',
             'show_value_labels': True,
             'value_label_format': '"$"#,##0"M"',
             'value_label_size_pt': 9,
             'cat_label_size_pt': 9,
             'gap_width': 50,
             'cat_header': 'Work type',
             'title': None},
  'external_title': {'text': 'Portfolio TAM allocation by work type, average annual FY22-27',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'Residual is evidence ambiguity; keep it visually distinct from named '
                           'buckets.',
                   'anchor_to': 'e2'}]}]
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Portfolio TAM allocation by work type, average annual FY22-27", BODY_X, BODY_Y, BODY_CX))
    out.append(chart(20, "WorkTypeAllocation", BODY_X, BODY_Y + 220_000, BODY_CX, 3_360_000, "rId2"))
    out.append(chip(30, "ResidualCue", BODY_X, BODY_B - 720_000, BODY_CX, 330_000,
        "Residual is evidence ambiguity", "The seven named buckets sum to broad component SAM; the gray residual remains in TAM but outside broad SAM.", fill=GRAY_1, line_color=BLACK))
    out.append(sizing_note(31, "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
