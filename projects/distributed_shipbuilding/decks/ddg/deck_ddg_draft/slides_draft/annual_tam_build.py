"""annual_tam_build — generated from the DDG slide spec.

Intent: Make the average-annual supplier TAM calculation visible without forcing the reader into the workbook, and tie the annual waterfall to the cumulative bridge.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'TAM build'
_TITLE_TOPIC = 'Annual TAM Build'
_TAKEAWAY = 'The corrected model yields ~$573M per year of supplier TAM'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'waterfall_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'steps': [{'label': 'BC construction base', 'value': 2911.8, 'kind': 'start'},
                     {'label': 'Less prime, co-prime, GFE POP', 'value': -2546.5, 'kind': 'delta'},
                     {'label': 'BC-stream supplier TAM', 'value': 365.3, 'kind': 'subtotal'},
                     {'label': 'Add AP and LLTM stream', 'value': 207.8, 'kind': 'delta'},
                     {'label': 'Portfolio supplier TAM', 'value': 573.1, 'kind': 'end'}]},
  'params': {'value_axis_format': '"$"#,##0"M"',
             'show_value_labels': False,
             'cat_header': 'Step',
             'title': None},
  'external_title': {'text': 'Average annual supplier TAM build, FY22-27',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'Waterfall values are average annual; the right-hand bridge is FY22-27 '
                           'cumulative.',
                   'anchor_to': 'e2'}]}]
_TABLES = [{'id': 'bridge_1',
  'element': 'e3',
  'role': 'chart_side_evidence',
  'factory': 'house_table',
  'semantic': {'table_name': 'Cumulative bridge, FY22-27',
               'purpose': 'reconcile',
               'reader_takeaway': 'The annualized waterfall ties back to the cumulative portfolio '
                                  'TAM of ~$3.44B.',
               'row_order': 'BC base, removed, BC stream, AP and LLTM, portfolio TAM',
               'highlight_rows': ['Portfolio TAM'],
               'guardrails': ['Keep this table clearly cumulative so it does not conflict with the '
                              'annualized waterfall.',
                              'Removed row = BC base minus BC stream (~$17.47B minus ~$2.19B = '
                              '~$15.28B).']},
  'render': {'table_skin': 'rule',
             'size': 900,
             'column_widths': {'mode': 'ratio',
                               'values': [2.1, 1.0],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Cumulative bridge', 'FY22-27'],
                      ['BC base', '~$17.47B'],
                      ['Removed', '~$15.28B'],
                      ['BC stream', '~$2.19B'],
                      ['AP and LLTM', '~$1.25B'],
                      ['Portfolio TAM', '~$3.44B']],
             'cell_fills': {},
             'cell_bold': {'(5,0)': True, '(5,1)': True},
             'cell_text_colors': {},
             'footnotes': ['Chart values are average annual; bridge values are cumulative.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX * 0.64)
    table_x = BODY_X + chart_w + GAP
    table_w = BODY_R - table_x
    out.append(exhibit_title(10, "Average annual supplier TAM build, FY22-27", BODY_X, BODY_Y, chart_w))
    out.append(chart(20, "AnnualizedWaterfall", BODY_X, BODY_Y + 240_000, chart_w, 3_560_000, "rId2"))
    tbl, h = make_table(30, "CumulativeBridge", table_x, BODY_Y + 240_000, table_w, _TABLES[0], size_override=900, min_row_h=245_000)
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
