"""tam_timing — generated from the DDG slide spec.

Intent: Show the fiscal-year supplier TAM profile by stream and make obvious that FY26 is a one-year AP and LLTM material spike, not the ongoing run-rate, while the average-annual headline stays the sizing convention.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Timing'
_TITLE_TOPIC = 'TAM Timing'
_TAKEAWAY = 'Annual supplier TAM is lumpy, with the FY26 spike driven by AP and LLTM'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'column_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['FY22', 'FY23', 'FY24', 'FY25', 'FY26', 'FY27'],
           'series': [{'name': 'BC stream',
                       'values': [245.9, 571.9, 416.9, 580.7, 35.5, 341.2],
                       'color': 'BLUE_3'},
                      {'name': 'AP and LLTM stream',
                       'values': [0, 0, 0, 56.6, 1190.0, 0],
                       'color': 'BLUE_5'}]},
  'params': {'mode': 'stacked',
             'value_axis_format': '"$"#,##0"M"',
             'show_legend': True,
             'legend_pos': 'b',
             'show_gridlines': True,
             'major_gridline_color': 'GRAY_1',
             'show_value_labels': False,
             'cat_label_size_pt': 9,
             'gap_width': 80,
             'cat_header': 'Fiscal year',
             'title': None},
  'external_title': {'text': 'Supplier TAM by fiscal year and stream',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'FY26 peak is almost entirely AP and LLTM material.', 'anchor_to': 'e2'},
                  {'text': 'Average-annual values size the market; supplier demand is fiscally '
                           'lumpy.',
                   'anchor_to': 'e2'}]}]
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Supplier TAM by fiscal year and stream", BODY_X, BODY_Y, BODY_CX))
    out.append(chart(20, "TimingChart", BODY_X, BODY_Y + 240_000, BODY_CX, 3_060_000, "rId2"))
    y = BODY_Y + 3_420_000
    w = int(BODY_CX * 0.34)
    out.append(nofill(30, "AvgKPI", BODY_X + int(BODY_CX*0.14), y, w, 530_000,
        [p("Average-annual convention", size=LABEL_9PT, italic=True, color=DK, align="ctr"),
         p("~$573M per year", size=RIBBON_KPI_18PT, bold=True, color=DK, align="ctr")], anchor="ctr"))
    out.append(nofill(31, "FY26KPI", BODY_X + int(BODY_CX*0.52), y, int(BODY_CX*0.40), 530_000,
        [p("FY26 is not the run-rate", size=LABEL_9PT, italic=True, color=DK, align="ctr"),
         p("~$1.23B, driven by AP and LLTM", size=RIBBON_KPI_18PT, bold=True, color=DK, align="ctr")], anchor="ctr"))
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
