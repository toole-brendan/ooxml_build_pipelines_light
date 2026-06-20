"""supplier_landscape — generated from the DDG slide spec.

Intent: Rank the top visible first-tier suppliers by lifetime flow and frame them as a concentrated landscape of specialized manufacturers, engineering-services firms, and GFE-adjacent suppliers — evidence of the visible base, not the full true market.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Supplier landscape'
_TITLE_TOPIC = 'Supplier Landscape'
_TAKEAWAY = 'Visible supplier flow is concentrated among specialized defense manufacturers'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) SAM.gov Entity Management API; (3) FAR 52.204-10'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['Leonardo SpA',
                          'Arctic Slope Regional Corp',
                          'Major Tool and Machine',
                          'General Dynamics Corp',
                          'General Electric Co',
                          'Rolls-Royce Holdings plc',
                          'Northrop Grumman Corp',
                          'Johnson Controls Navy Systems',
                          'Advanced Sciences and Technologies',
                          'CAES Systems LLC'],
           'series': [{'name': 'Lifetime visible flow',
                       'values': [1810.3,
                                  987.4,
                                  816.1,
                                  372.0,
                                  335.6,
                                  257.2,
                                  249.3,
                                  178.2,
                                  174.0,
                                  169.2],
                       'data_point_colors': ['BLUE_5',
                                             'BLUE_4',
                                             'BLUE_4',
                                             'BLUE_3',
                                             'BLUE_3',
                                             'BLUE_2',
                                             'BLUE_2',
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
             'gap_width': 40,
             'cat_header': 'Supplier (parent)',
             'title': None},
  'external_title': {'text': 'Top visible first-tier suppliers by lifetime flow, $M',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': []}]
_TABLES = [{'id': 'supplier_evidence_1',
  'element': 'e3',
  'role': 'chart_side_evidence',
  'factory': 'house_table',
  'semantic': {'table_name': 'Supplier role and caveat cue',
               'purpose': 'classify',
               'reader_takeaway': 'Top visible suppliers include product manufacturers, services, '
                                  'and prime-affiliated parents; the chart is a floor, not a '
                                  'target list.',
               'row_order': 'highest-risk interpretation caveats first',
               'highlight_rows': [],
               'guardrails': ['Names only, no logos.',
                              'Parent-level Vendors tab, not bucket-split CD09.',
                              'Evidence table is not a target-account list.']},
  'render': {'table_skin': 'rule',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [1.4, 1.4, 2.6],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Example', 'Role', 'Caveat'],
                      ['Leonardo via DRS', 'Electrical and VLS', 'Foreign parent, U.S. work sites'],
                      ['Arctic Slope', 'Engineering services', 'Not a pure component manufacturer'],
                      ['Major Tool', 'Machining', 'Clean physical-components proof point'],
                      ['General Dynamics', 'Prime-affiliated', 'Do not read as third-party wedge'],
                      ['GE and Rolls-Royce',
                       'Propulsion',
                       'Visible flow can understate vertical integration']],
             'cell_fills': {},
             'cell_bold': {},
             'cell_text_colors': {},
             'footnotes': ['Supplier evidence is visible first-tier parent flow; a floor, not the '
                           'full supplier base.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX * 0.61)
    tx = BODY_X + chart_w + GAP
    tw = BODY_R - tx
    out.append(exhibit_title(10, "Top visible first-tier suppliers by lifetime flow, $M", BODY_X, BODY_Y, chart_w))
    out.append(chart(20, "TopSupplierChart", BODY_X, BODY_Y + 240_000, chart_w, 3_300_000, "rId2"))
    tbl, h = make_table(30, "SupplierEvidenceTable", tx, BODY_Y + 240_000, tw, _TABLES[0], size_override=820, min_row_h=215_000)
    out.append(tbl)
    out.append(nofill(40, "VisibleFloor", BODY_X, BODY_B - 360_000, chart_w, 300_000,
        [p("Lifetime visible first-tier subaward flow per parent vendor; a floor, not the full supplier base. Names only, no logos.", size=FINEPRINT_8_5PT, color=DK, align="l")], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
