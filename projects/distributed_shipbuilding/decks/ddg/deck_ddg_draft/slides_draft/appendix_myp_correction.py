"""appendix_myp_correction — generated from the DDG slide spec.

Intent: Show how the BIW and Ingalls FY23-27 multiyear masters are reconstructed, why the disclosed-only outside-yards reading is a redaction artifact, and how folding the masters back corrects outside-yards POP to ~32.8% and underpins the applied BC supplier coefficient.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'MYP correction'
_TITLE_TOPIC = 'MYP Correction'
_TAKEAWAY = 'Folding the redacted $14.58B masters back into the corpus corrects outside-yards POP to about one third'
_SOURCES = 'Sources: (1) DoW DDG-51 contract announcements, Aug. 1 and Aug. 11, 2023; (2) 41 U.S. Code 2101 et seq. and FAR 2.101 and 3.104; (3) USNI News, Navy reporting on the FY23-27 DDG-51 multiyear master awards, 2023'

_CHART_SPECS = []
_TABLES = [{'id': 'myp_reconstruction',
  'element': 'e2',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'MYP reconstruction and POP correction',
               'purpose': 'reconcile',
               'reader_takeaway': 'The reconstructed ~$14.58B masters are ~67% of the gated corpus '
                                  'and pull outside-yards POP down from the disclosed artifact to '
                                  'the ~32.8% MYP-corrected view.',
               'row_order': 'BIW master, Ingalls master, combined masters, disclosed announcement '
                            'corpus, gated corpus incl. masters, corrected outside-yards POP, '
                            'disclosed-only artifact, TAM sensitivity',
               'highlight_rows': ['Combined reconstructed masters', 'Corrected outside-yards POP'],
               'guardrails': ['The disclosed artifact is a trapdoor, not the conclusion.',
                              'Corrected outside-yards POP is the defensible reading.',
                              'The reconstructed master POP weights are analytical, not disclosed '
                              'per hull.']},
  'render': {'table_skin': 'rule',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [2.4, 1.0, 1.7, 2.0, 1.5],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r', 'l', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Item', 'Approx. $M', 'Reconstructed POP', 'Model use', 'Guardrail'],
                      ['BIW FY23-27 MYP master',
                       '6,400',
                       'Bath 86%, supplier 14%',
                       'PIID N00024-23-C-2305',
                       'Redacted dollar value'],
                      ['Ingalls FY23-27 MYP master',
                       '8,180',
                       'Pascagoula 88%, supplier 12%',
                       'PIID N00024-23-C-2307',
                       'Redacted dollar value'],
                      ['Combined reconstructed masters',
                       '14,580',
                       'Yard-heavy',
                       '67.2% of gated corpus',
                       'Too large to ignore'],
                      ['Disclosed announcement corpus',
                       '7,132',
                       '152 gated actions',
                       'Disclosed-only base',
                       'Over-weights GFE'],
                      ['Gated corpus incl. masters',
                       '21,712',
                       'All gated',
                       'Denominator for correction',
                       'Use for the corrected view'],
                      ['Corrected outside-yards POP',
                       'n.a.',
                       '32.8%',
                       'Other-US and foreign',
                       'Defensible reading'],
                      ['Disclosed-only artifact',
                       'n.a.',
                       '73.6%',
                       'Guardrail only',
                       'Do not headline'],
                      ['TAM sensitivity',
                       '1,310',
                       'Uplift',
                       '~$3.44B corrected vs ~$2.13B disclosed-only',
                       'Method swing']],
             'cell_fills': {'(3,0)': 'BLUE_1', '(6,0)': 'BLUE_2', '(7,0)': 'GRAY_2'},
             'cell_bold': {'(3,0)': True, '(6,0)': True},
             'cell_text_colors': {'(7,0)': 'GRAY_5'},
             'footnotes': ['Master dollar values are source-selection redacted (FAR 2.101 and '
                           '3.104); ~$14.58B reconstructed from FPDS obligated amount and '
                           'trade-press totals. POP weights are the analytical reconstruction, not '
                           'disclosed per hull.']},
  'columns': [{'name': 'Item', 'unit': 'name', 'tie_out': 'Inputs §4 / POP Audit §2'},
              {'name': 'Approx. $M',
               'unit': '$M',
               'tie_out': 'Inputs §4 (masters) / POP Audit §2 (corpus)'},
              {'name': 'Reconstructed POP',
               'unit': 'percent or text',
               'tie_out': 'Inputs §4 / TAM Build §3b'},
              {'name': 'Model use', 'unit': 'text', 'tie_out': 'POP Corpus / TAM Build §4'},
              {'name': 'Guardrail', 'unit': 'text', 'tie_out': 'TAM Build §4c'}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    table_w = int(BODY_CX * 0.66)
    out.append(exhibit_title(10, "MYP master reconstruction and outside-yards POP correction", BODY_X, BODY_Y, table_w))
    tbl, h = make_table(20, "MYPReconstruction", BODY_X, BODY_Y + 220_000, table_w, _TABLES[0], size_override=720, min_row_h=178_000)
    out.append(tbl)
    bx = BODY_X + table_w + GAP
    bw = BODY_R - bx
    by = BODY_Y + 230_000
    out.append(text_box(40, "OutsideYardsComparison", bx, by, bw, 1_470_000,
        [p("Outside-yards POP share", size=DENSE_BODY_10PT, bold=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color=BLACK, insets=INSETS_MESSAGE, anchor="t"))
    out.append(hbar(41, bx + 160_000, by + 430_000, bw - 320_000, 360_000, "Disclosed-only artifact", "73.6%", 0.736, fill=GRAY_3))
    out.append(hbar(42, bx + 160_000, by + 850_000, bw - 320_000, 360_000, "MYP-corrected", "32.8%", 0.328, fill=BLUE_5))
    out.append(nofill(50, "Read", bx, by + 1_330_000, bw, 410_000,
        [p("Read: the corrected view is about one third of the gated corpus, corrected to from the artifact.", size=FINEPRINT_8_5PT, italic=True, color=DK, align="l")], anchor="t"))
    out.append(nofill(60, "Guardrail", BODY_X, BODY_B - 430_000, BODY_CX, 380_000,
        [lead_body("Guardrail:", "do not headline the disclosed artifact; the ~32.8% outside-yards POP is not the 12.5% BC supplier coefficient.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT)], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
