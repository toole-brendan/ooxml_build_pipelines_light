"""cost_funnel — generated from the DDG slide spec.

Intent: Establish the denominator. Show the FY24 cost-category decomposition with Basic Construction as the largest single category and the starting base for the BC supplier stream; visually de-emphasize the GFE-heavy Electronics and Ordnance block that is excluded from the non-GFE supplier TAM.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Cost funnel'
_TITLE_TOPIC = 'Cost Funnel'
_TAKEAWAY = 'Basic Construction is the supplier-addressable base after excluding GFE-heavy cost categories'
_SOURCES = 'Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c; (2) Congressional Research Service, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; (3) FAR Part 45 and FAR 52.245-1'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['Basic Construction (60.5%)',
                          'Electronics and Ordnance GFE (32.9%)',
                          'Other smaller categories (6.6%)'],
           'series': [{'name': 'FY24 cost category value',
                       'values': [3322, 1807, 363],
                       'data_point_colors': ['BLUE_5', 'GRAY_3', 'GRAY_1']}]},
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
             'cat_header': 'FY24 cost category',
             'title': None},
  'external_title': {'text': 'FY24 DDG-51 cost categories, both ships',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'Total ship estimate is the denominator reference, not a competing bar: '
                           '~$5,492M.',
                   'anchor_to': 'e3'}]}]
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    left_w = int(BODY_CX * 0.64)
    right_x = BODY_X + left_w + GAP
    right_w = BODY_R - right_x
    out.append(exhibit_title(10, "FY24 DDG-51 cost categories, both ships", BODY_X, BODY_Y, left_w))
    out.append(chart(20, "FY24CostCategoryChart", BODY_X, BODY_Y + 260_000, left_w, 3_260_000, "rId2"))
    out.append(chip(30, "TotalShipRef", BODY_X, BODY_B - 420_000, left_w, 350_000,
        "Total ship estimate", "Basic Construction is ~$3,322M, or 60.5% of total.", value="~$5,492M", fill=GRAY_1, line_color=BLACK))
    out.append(exhibit_title(40, "Denominator decision", right_x, BODY_Y + 260_000, right_w))
    step_h = 680_000
    y = BODY_Y + 620_000
    out.append(chip(41, "StepTotal", right_x, y, right_w, step_h, "1. Total ship cost", "Too broad for supplier TAM", fill=GRAY_1, line_color=BLACK))
    out.append(chip(42, "StepBC", right_x, y + step_h + GAP, right_w, step_h, "2. Basic Construction", "Supplier-addressable starting base", fill=BLUE_1, line_color=BLACK))
    out.append(chip(43, "StepNext", right_x, y + 2*(step_h+GAP), right_w, step_h, "3. Next correction", "Apply the MYP-corrected supplier coefficient", fill=GRAY_1, line_color=BLACK))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
