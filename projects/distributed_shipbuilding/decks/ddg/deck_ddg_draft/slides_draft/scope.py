"""scope — generated from the DDG slide spec.

Intent: Prevent misinterpretation by defining the bounded market before any denominator or TAM math appears; the deck sizes non-GFE new-construction supplier work outside the two yards, not total ship cost.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Scope'
_TITLE_TOPIC = 'Scope'
_TAKEAWAY = 'The analysis sizes non-GFE new-construction supplier work, not total DDG spend'
_SOURCES = 'Sources: (1) CRS RL32109, Navy DDG-51 and DDG-1000 Destroyer Programs; (2) U.S. Navy FY2027 SCN Justification Book, LI 2122; (3) FAR 52.204-10 and FAR Part 45'

_CHART_SPECS = []
_TABLES = [{'id': 'ledger_1',
  'element': 'e1',
  'role': 'primary',
  'factory': 'house_table',
  'semantic': {'table_name': 'Scope boundary ledger',
               'purpose': 'define',
               'reader_takeaway': 'The deck sizes non-GFE new-construction supplier work; it '
                                  'excludes total DDG spend, GFE-heavy flows, sustainment and '
                                  'depot, weapons procurement, DDG-1000, and contaminants.',
               'row_order': 'program scope, appropriation, Basic Construction, AP and LLTM, '
                            'place-of-performance boundary',
               'highlight_rows': ['IN SCOPE'],
               'guardrails': ['GFE examples belong only in the out-of-scope column.',
                              'The slide is a scope boundary, not a data table; no model dollars.',
                              'Use commas and "and"; no visible slash or plus separators.']},
  'render': {'table_skin': 'light',
             'size': 900,
             'column_widths': {'mode': 'ratio',
                               'values': [1.0, 1.0],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['IN SCOPE\nsized in TAM and SAM', 'OUT OF SCOPE\nnot in TAM'],
                      ['DDG-51 Flight IIA and Flight III new construction',
                       'DDG-1000 Zumwalt (out of class, closed)'],
                      ['SCN Line Item 2122 appropriation', 'WPN and OPN weapons procurement'],
                      ['Basic Construction supplier work',
                       'Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, SEWIP, CIWS, and other GFE-heavy '
                       'prime flows'],
                      ['AP and LLTM supplier-addressable material',
                       'Sustainment, depot, ship repair, design-only, and MIB'],
                      ['Work performed away from BIW, Ingalls, GFE prime sites, and Navy-directed '
                       'flows',
                       'Contaminants such as the IVECO Mk 110 gun and Thales ESSM artifacts']],
             'cell_fills': {'(1,0)': 'BLUE_1',
                            '(2,0)': 'BLUE_1',
                            '(3,0)': 'BLUE_1',
                            '(4,0)': 'BLUE_1',
                            '(5,0)': 'BLUE_1',
                            '(1,1)': 'GRAY_1',
                            '(2,1)': 'GRAY_1',
                            '(3,1)': 'GRAY_1',
                            '(4,1)': 'GRAY_1',
                            '(5,1)': 'GRAY_1'},
             'cell_bold': {},
             'cell_text_colors': {},
             'footnotes': ['Conceptual boundary; the appendix carries the in-scope and excluded '
                           'record audit.']},
  'columns': [{'name': 'In scope',
               'unit': 'text',
               'tie_out': 'Methodology §2 (In TAM)',
               'formula': None},
              {'name': 'Out of scope',
               'unit': 'text',
               'tie_out': 'Methodology §3 / Scope Exclusions',
               'formula': None}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    x = BODY_X + int(BODY_CX * 0.08)
    w = int(BODY_CX * 0.84)
    tbl, h = make_table(20, "ScopeBoundaryLedger", x, BODY_Y + 130_000, w, _TABLES[0], size_override=900, min_row_h=250_000)
    out.append(tbl)
    y = BODY_Y + 130_000 + h + 220_000
    out.append(nofill(40, "BoundaryCue", BODY_X + int(BODY_CX*0.08), y, int(BODY_CX*0.84), 430_000,
        [lead_body("Boundary cue:", "total DDG spend, then non-GFE new-construction base, then supplier-addressable TAM, then the SAM work-type menu.", lead_size=FINEPRINT_8_5PT, body_size=MESSAGE_11PT)], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
