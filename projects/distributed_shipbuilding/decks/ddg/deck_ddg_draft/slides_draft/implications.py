"""implications — generated from the DDG slide spec.

Intent: Leave the reader with usable where-to-play choices via a disciplined scenario scorecard — broad is the envelope, metal the largest targeted scenario, electrical the largest single bucket, modular the distributed-capacity lane, HM&E selective — without adding capture odds or a revenue forecast.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Implications'
_TITLE_TOPIC = 'Implications'
_TAKEAWAY = 'Prioritization depends on product scope, qualification burden, and confidence in bucket visibility'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (3) GAO-25-106286'

_CHART_SPECS = []
_TABLES = [{'id': 'scorecard_1',
  'element': 'e2',
  'role': 'primary',
  'factory': 'house_table',
  'semantic': {'table_name': 'Scenario prioritization scorecard',
               'purpose': 'summarize',
               'reader_takeaway': 'Metal and electrical are the most concrete near-term lanes; '
                                  'broad is the envelope; modular is the strategic distributed '
                                  'lane; HM&E is selective.',
               'row_order': 'by average-annual SAM descending (broad, metal, electrical, modular, '
                            'HM&E)',
               'highlight_rows': ['Metal components', 'Electrical and power'],
               'guardrails': ['Broad is labeled an envelope, not a wedge.',
                              'No capture / win-probability / revenue-forecast column.',
                              'Priority-read cells fold qualification difficulty + strategic fit; '
                              'they are deck judgment.']},
  'render': {'table_skin': 'dark',
             'size': 950,
             'column_widths': {'mode': 'ratio',
                               'values': [2.6, 1.5, 1.4, 1.1, 1.5, 3.2],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r', 'r', 'ctr', 'ctr', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Scenario',
                       'Avg annual',
                       'Cumulative',
                       'TAM share',
                       'Confidence',
                       'Priority read'],
                      ['Broad component manufacturing',
                       '~$327M per year',
                       '~$1.96B',
                       '57.1%',
                       'Medium',
                       'Envelope, not a single wedge'],
                      ['Metal components',
                       '~$170M per year',
                       '~$1.02B',
                       '29.6%',
                       'Medium-high',
                       'Largest targeted scenario; high if fabrication or machining scope fits'],
                      ['Electrical and power',
                       '~$132M per year',
                       '~$791M',
                       '23.0%',
                       'Medium',
                       'Largest single named bucket; high but qualification-heavy'],
                      ['Modular assemblies',
                       '~$104M per year',
                       '~$626M',
                       '18.2%',
                       'Medium',
                       'Strategic distributed-capacity lane; smaller in the current model'],
                      ['HM&E components',
                       '~$89M per year',
                       '~$531M',
                       '15.4%',
                       'Medium-low',
                       'Selective, product-by-product; evidence-dependent']],
             'cell_fills': {'(2,5)': 'BLUE_1', '(3,5)': 'BLUE_1'},
             'cell_bold': {},
             'cell_text_colors': {},
             'footnotes': ['Where-to-play screen, not SOM. No capture probability is applied.']},
  'columns': [{'name': 'Scenario', 'unit': 'name', 'tie_out': 'inputs_scenarios.SCENARIOS'},
              {'name': 'Avg annual',
               'unit': '$M/yr',
               'tie_out': 'SAM Build §4a',
               'formula': 'cumulative SAM / 6 years'},
              {'name': 'Cumulative', 'unit': '$B', 'tie_out': 'SAM Build §4a'},
              {'name': 'TAM share',
               'unit': 'percent',
               'tie_out': 'scenario cumulative SAM / portfolio TAM'},
              {'name': 'Confidence',
               'unit': 'qualitative',
               'tie_out': 'deck judgment (Bucket Evidence)'},
              {'name': 'Priority read', 'unit': 'qualitative', 'tie_out': 'deck judgment'}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Scenario prioritization scorecard, average annual FY22-27", BODY_X, BODY_Y, BODY_CX))
    tbl, h = make_table(20, "ImplicationsScorecard", BODY_X, BODY_Y + 230_000, BODY_CX, _TABLES[0], size_override=930, min_row_h=245_000)
    out.append(tbl)
    y = BODY_Y + 230_000 + h + 140_000
    out.append(nofill(40, "ClosingNote", BODY_X, y, BODY_CX, 560_000,
        [lead_body("Where-to-play screen, not SOM.", "Prioritization depends on product scope, qualification burden, and confidence in bucket visibility.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT),
         p("Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture.", size=FINEPRINT_8_5PT, color=DK, align="l")], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
