"""myp_redaction — generated from the DDG slide spec.

Intent: Explain why the model restores the redacted FY23-27 multiyear master values before using place-of-performance data to estimate outside-yards share, and land that the corrected ~33% (not the ~87% disclosed-only artifact) is what feeds the BC supplier coefficient.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Denominator correction'
_TITLE_TOPIC = 'MYP Redaction'
_TAKEAWAY = 'Restoring the redacted multiyear masters corrects the outside-yards artifact to ~33%'
_SOURCES = 'Sources: (1) DoD daily contract announcements, war.gov articles 3479250 (Aug. 1, 2023) and 3491276 (Aug. 11, 2023); (2) 41 U.S. Code 2101 et seq. and FAR 2.101 and FAR 3.104; (3) U.S. Naval Institute News reporting on the FY23-27 DDG-51 multiyear award'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['Corrected POP distribution'],
           'series': [{'name': 'BIW site', 'values': [0.29], 'data_point_colors': ['BLUE_4']},
                      {'name': 'Ingalls site', 'values': [0.336], 'data_point_colors': ['BLUE_3']},
                      {'name': 'Other-US supplier',
                       'values': [0.315],
                       'data_point_colors': ['BLUE_5']},
                      {'name': 'Foreign', 'values': [0.013], 'data_point_colors': ['GRAY_3']},
                      {'name': 'Unparsed', 'values': [0.045], 'data_point_colors': ['GRAY_1']}]},
  'params': {'mode': 'percent',
             'value_axis_format': '0%',
             'show_legend': True,
             'legend_pos': 'b',
             'show_gridlines': False,
             'show_value_labels': True,
             'value_label_format': '0.0%',
             'value_label_size_pt': 8,
             'cat_label_size_pt': 9,
             'gap_width': 35,
             'cat_header': 'Distribution',
             'title': None},
  'external_title': {'text': 'MYP-corrected place-of-performance distribution',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'Outside both yards, the supplier-addressable share, is Other-US 31.5% '
                           'plus Foreign 1.3% = 32.8%.',
                   'anchor_to': 'e2'}]},
 {'id': 'chart_2',
  'factory': 'bar_chart',
  'chart_index': 1,
  'title_element': 'e3',
  'frame_element': 'e4',
  'data': {'categories': ['MYP-corrected', 'Disclosed-only artifact, do not headline'],
           'series': [{'name': 'Outside-yards share',
                       'values': [0.328, 0.87],
                       'data_point_colors': ['BLUE_5', 'GRAY_3']}]},
  'params': {'mode': 'ranked',
             'value_axis_format': '0%',
             'show_legend': False,
             'show_gridlines': True,
             'major_gridline_color': 'GRAY_1',
             'show_value_labels': True,
             'value_label_format': '0.0%',
             'value_label_size_pt': 9,
             'cat_label_size_pt': 9,
             'gap_width': 50,
             'cat_header': 'View',
             'title': None},
  'external_title': {'text': 'Outside-yards share after restoring redacted MYP masters',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'The ~87% is a disclosed-only artifact, shown as a caveat; do not '
                           'headline it.',
                   'anchor_to': 'e4'}]}]
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    left_w = int(BODY_CX * 0.64)
    rail_x = BODY_X + left_w + GAP
    rail_w = BODY_R - rail_x
    out.append(exhibit_title(10, "MYP-corrected place-of-performance distribution", BODY_X, BODY_Y, left_w))
    out.append(chart(20, "CorrectedPOPChart", BODY_X, BODY_Y + 220_000, left_w, 1_120_000, "rId2"))
    y2 = BODY_Y + 1_620_000
    out.append(exhibit_title(11, "Outside-yards share after restoring redacted MYP masters", BODY_X, y2, left_w))
    out.append(chart(21, "OutsideYardsComparison", BODY_X, y2 + 220_000, left_w, 1_310_000, "rId3"))
    badge_y = BODY_Y + 3_260_000
    bw = (left_w - GAP) // 2
    out.append(chip(40, "MasterBadge", BODY_X, badge_y, bw, 540_000, "Reconstructed FY23-27 MYP masters", "BIW plus Ingalls masters folded back", value="~$14.58B", fill=BLUE_1, line_color=BLACK))
    out.append(chip(41, "CorpusBadge", BODY_X + bw + GAP, badge_y, bw, 540_000, "Gated POP corpus incl. masters", "distribution base for correction", value="~$21.71B", fill=BLUE_1, line_color=BLACK))
    out.append(bullet_rail(50, rail_x, BODY_Y, rail_w, 3_800_000,
        ["The FY23-27 BIW and Ingalls multiyear masters disclose work locations but redact dollar values.",
         "Those masters are large and yard-heavy, so omitting their dollars over-weights disclosed GFE actions.",
         "The model restores ~$14.58B of master value before applying the Basic Construction supplier coefficient.",
         "Use the corrected ~33% outside-yards view going forward, not the disclosed-only artifact."],
        title="What changed", body_size=LABEL_9PT))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
