"""appendix_ffata_limitations — generated from the DDG slide spec.

Intent: Defend the use of FFATA as evidence rather than as the market-size denominator, listing the categories FFATA structurally misses and showing the visible flow as a minority share (~20.1%) of the estimated yard-side outsourcing midpoint.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'FFATA limitations'
_TITLE_TOPIC = 'FFATA Limitations'
_TAKEAWAY = 'Visible first-tier subawards are a floor and evidence base, not the market denominator'
_SOURCES = 'Sources: (1) FAR 52.204-10; (2) SAM.gov Acquisition Subaward Reporting Public API; (3) GAO-25-106286'

_CHART_SPECS = []
_TABLES = [{'id': 'ffata_evidence_ledger',
  'element': 'e1',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'FFATA evidence and limitations ledger',
               'purpose': 'summarize',
               'reader_takeaway': 'FFATA is useful for supplier names, bucket evidence, and '
                                  'concentration, but structurally misses parts of the supplier '
                                  'flow; it is a floor, not the denominator.',
               'row_order': 'FFATA first-tier subawards, SAM.gov published and deleted records, '
                            'Yard-prime PIID filings, Vendor and description fields, SAM.gov '
                            'Entity Management enrichment, USAspending cross-validation',
               'highlight_rows': ['FFATA first-tier subawards'],
               'guardrails': ['FFATA is the observable floor, not the full market denominator.',
                              'Structural misses are broader than non-compliance.']},
  'render': {'table_skin': 'light',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [1.7, 2.1, 2.1, 2.2],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Public-data element',
                       'What it captures',
                       'What it misses',
                       'Implication for deck use'],
                      ['FFATA first-tier subawards',
                       'Direct prime-to-sub subcontracts above the $30,000 threshold',
                       'Lower-tier suppliers and sub-threshold actions',
                       'Visible floor and evidence base'],
                      ['SAM.gov published and deleted records',
                       'FSRS records surfaced through the SAM.gov API (no per-PIID cap)',
                       'Reporting lag of 12 to 30 months and late corrections',
                       'Longitudinal evidence with a timing caveat'],
                      ['Yard-prime PIID filings',
                       'Yard-side filings by BIW and Ingalls',
                       'Direct material booked as direct cost and standing agreements',
                       'Supports the supplier landscape, not the denominator'],
                      ['Vendor and description fields',
                       'Visible supplier names and award descriptions',
                       'Incomplete NAICS and UEI resolution',
                       'Bucket evidence for SAM classification'],
                      ['SAM.gov Entity Management enrichment',
                       'Entity attributes, country, and validation support',
                       'Corporate-primary NAICS, not action-level work type',
                       'Useful for cleaning and enrichment'],
                      ['USAspending cross-validation',
                       'A cross-check against the federal spending view',
                       'Truncation at about 2,500 records per PIID and timing differences',
                       'Triangulation only; SAM.gov is canonical']],
             'cell_fills': {'(1,0)': 'BLUE_1'},
             'cell_bold': {'(1,0)': True},
             'cell_text_colors': {},
             'footnotes': ['FFATA is the legal reporting framework (FAR 52.204-10); SAM.gov FSRS '
                           'is the public access path.']},
  'columns': [{'name': 'Public-data element',
               'unit': 'text',
               'tie_out': 'wiki 05/16',
               'formula': None},
              {'name': 'What it captures', 'unit': 'text', 'tie_out': 'wiki 05', 'formula': None},
              {'name': 'What it misses', 'unit': 'text', 'tie_out': 'wiki 05/12', 'formula': None},
              {'name': 'Implication for deck use',
               'unit': 'text',
               'tie_out': 'wiki 05',
               'formula': None}]},
 {'id': 'cumulative_range_cue',
  'element': 'e2',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'Cumulative yard-side view',
               'purpose': 'compare',
               'reader_takeaway': 'FFATA-visible flow is only ~20.1% of the estimated yard-side '
                                  'outsourcing midpoint on a cumulative basis.',
               'row_order': 'FFATA visible, estimated low, estimated midpoint, estimated high, '
                            'visible share at midpoint',
               'highlight_rows': ['Estimated midpoint', 'Visible share at midpoint'],
               'guardrails': ['Values are cumulative FY2016-FY2027.',
                              'Do not place annualized values in this matrix unless fully '
                              'relabeled.']},
  'render': {'table_skin': 'rule',
             'size': 900,
             'column_widths': {'mode': 'ratio',
                               'values': [2.0, 1.2],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Cumulative yard-side view', 'Value'],
                      ['FFATA visible', '~$2.73B'],
                      ['Estimated low', '~$11.31B'],
                      ['Estimated midpoint', '~$13.57B'],
                      ['Estimated high', '~$16.16B'],
                      ['Visible share at midpoint', '20.1%']],
             'cell_fills': {'(1,0)': 'GRAY_1', '(3,0)': 'BLUE_1', '(5,0)': 'BLUE_2'},
             'cell_bold': {'(3,0)': True, '(5,0)': True},
             'cell_text_colors': {},
             'footnotes': ['Cumulative FY2016-FY2027. Annual view (off-slide): ~$455M per year '
                           'visible vs ~$2.26B per year midpoint.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    left_w = int(BODY_CX * 0.63)
    tbl, h = make_table(20, "FFATAEvidenceLedger", BODY_X, BODY_Y, left_w, _TABLES[0], size_override=760, min_row_h=190_000)
    out.append(tbl)
    rx = BODY_X + left_w + GAP
    rw = BODY_R - rx
    tbl2, h2 = make_table(40, "CumulativeRangeCue", rx, BODY_Y, rw, _TABLES[1], size_override=880, min_row_h=235_000)
    out.append(tbl2)
    out.append(nofill(60, "LimitationsRail", BODY_X, BODY_B - 430_000, BODY_CX, 390_000,
        [lead_body("What FFATA misses:", "direct material booked as direct cost (~$400 to 700M per year), lower-tier subcontracts, BIW under-reporting, long-term supplier agreements, sub-$30,000 tail, and 12 to 30 month reporting lag.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT)], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
