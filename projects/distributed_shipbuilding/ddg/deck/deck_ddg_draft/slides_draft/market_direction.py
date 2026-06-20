"""market_direction — generated from the DDG slide spec.

Intent: Present a qualitative evidence timeline of distributed-shipbuilding signals and interpret the direction of travel as more external production capacity, especially at HII Ingalls — directional, not a refreshed TAM.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Market direction'
_TITLE_TOPIC = 'Market Direction'
_TAKEAWAY = 'Distributed shipbuilding points toward more external production capacity'
_SOURCES = 'Sources: (1) HII quarterly earnings materials, FY2024 Q3-FY2026 Q1; (2) General Dynamics earnings materials, FY2025 Q4-FY2026 Q1; (3) GAO-25-106286'

_CHART_SPECS = []
_TABLES = [{'id': 'timeline_1',
  'element': 'e2',
  'role': 'primary',
  'factory': 'house_table',
  'semantic': {'table_name': 'Market direction (evidence)',
               'purpose': 'summarize',
               'reader_takeaway': 'External production capacity is expanding, led by HII; GD '
                                  'signals constraint; policy supports the direction.',
               'row_order': 'chronological by fiscal period, HII first, then GD, then policy',
               'highlight_rows': [],
               'guardrails': ['Use short paraphrases, not long transcript quotes.',
                              'No fabricated numeric index column.']},
  'render': {'table_skin': 'rule',
             'size': 950,
             'column_widths': {'mode': 'ratio',
                               'values': [1.1, 1.4, 4.3, 2.4],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size',
                       'min_row_h': 274320},
             'rows': [['Period', 'Source', 'Signal', 'Implication'],
                      ['FY24 Q3',
                       'HII',
                       'Outsourcing over 1 million hours in 2024; planned increase of more than '
                       '30% in 2025',
                       'Outsourcing is now a named lever'],
                      ['FY25 Q4',
                       'HII',
                       'Outsourcing doubled year over year in 2025; +30% planned in 2026; over 23 '
                       'vendors established',
                       'Supplier network is scaling'],
                      ['FY26 Q1',
                       'HII',
                       'On track to grow outsourcing hours ~30%; first 2 of 32 units in yard from '
                       'partners on DDG 137',
                       'Distributed work reaching the DDG line'],
                      ['FY25 Q4',
                       'General Dynamics',
                       'Supply chain remains the gating item (Electric Boat context); no '
                       'comparable DDG outsourcing-hours target',
                       'Constraint is broad, not a DDG plan'],
                      ['FY25-FY26',
                       'Navy and GAO',
                       'Shipbuilders already outsource to overcome constrained physical space; '
                       'distributed production policy',
                       'Directional tailwind']],
             'cell_fills': {},
             'cell_bold': {},
             'cell_text_colors': {},
             'footnotes': ['Qualitative evidence; paraphrased from earnings materials and GAO. Not '
                           'a numeric index and not a TAM forecast.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Distributed-shipbuilding signals, FY2024 Q3 to FY2026 Q1", BODY_X, BODY_Y, BODY_CX))
    tbl, h = make_table(20, "MarketDirectionTimeline", BODY_X, BODY_Y + 230_000, BODY_CX, _TABLES[0], size_override=920, min_row_h=245_000)
    out.append(tbl)
    y = BODY_Y + 230_000 + h + 120_000
    out.append(bullet_rail(40, BODY_X, y, BODY_CX, 610_000,
        [("Direction:", "external production capacity is expanding, especially at HII Ingalls."),
         ("Asymmetry:", "HII has the clearest public commitment; GD signals supplier constraints, submarine-centric."),
         ("Scope:", "directional only — it does not change the FY22-27 TAM math without a refreshed model.")], body_size=LABEL_9PT, insets=INSETS_NONE))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
