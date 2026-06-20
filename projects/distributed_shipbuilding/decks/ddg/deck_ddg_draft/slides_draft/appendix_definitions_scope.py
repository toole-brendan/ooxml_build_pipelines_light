"""appendix_definitions_scope — generated from the DDG slide spec.

Intent: Make it impossible to confuse total ship cost, SCN LI 2122 spend, the Basic Construction base, FFATA-visible first-tier flow, and supplier-addressable TAM, and to state the FY2022-27 TAM window, the in-scope new-construction PIID set, and the explicit scope exclusions (Zumwalt, depot sustainment, WPN and OPN weapons, GFE, the IVECO contaminant).
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Definitions and scope'
_TITLE_TOPIC = 'Definitions and Scope'
_TAKEAWAY = 'Total ship cost, SCN, Basic Construction, FFATA-visible flow, and supplier-addressable TAM each do a different job'
_SOURCES = 'Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c; (2) FAR 52.204-10 and 48 C.F.R. Part 45; (3) CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109'

_CHART_SPECS = []
_TABLES = [{'id': 'denominator_ledger',
  'element': 'e2',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'Denominator and scope ledger',
               'purpose': 'define',
               'reader_takeaway': 'Total ship cost, SCN LI 2122, Basic Construction, AP and LLTM, '
                                  'FFATA-visible flow, supplier-addressable TAM, and SAM scenarios '
                                  'serve different jobs and must not be conflated.',
               'row_order': 'total ship cost, SCN LI 2122, Basic Construction base, AP and LLTM '
                            'base, FFATA-visible flow, supplier-addressable TAM, SAM scenarios',
               'highlight_rows': ['Supplier-addressable TAM'],
               'guardrails': ['TAM is not total ship cost.',
                              'FFATA-visible flow is evidence, not the market-size denominator.',
                              'SAM scenarios are not SOM and are not additive totals.']},
  'render': {'table_skin': 'rule',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [1.7, 2.7, 2.3, 2.3, 1.7],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l', 'l', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size',
                       'min_row_h': 274320},
             'rows': [['Denominator',
                       'Definition',
                       'Included examples',
                       'Excluded examples',
                       'Where used'],
                      ['Total ship cost',
                       'P-5c Total Ship Estimate by procurement year',
                       'Basic Construction, Electronics, Ordnance, Plans, HM&E, Other',
                       'WPN and OPN weapons, depot sustainment',
                       'Cost funnel context only'],
                      ['SCN LI 2122',
                       'DDG-51 Class Destroyer line item in the Navy SCN budget books',
                       'DDG-51 Flight IIA and Flight III new construction',
                       'DDG-1000 Zumwalt (LI 2119), cruiser modernization, depot repair',
                       'Scope gate and schedule'],
                      ['Basic Construction base',
                       'Prime construction layer flowing through BIW and Ingalls prime contracts',
                       'Yard work and yard-side supplier work',
                       'Navy-procured Aegis, SPY-6, Mk 41, Mk 45, LM2500, SEWIP',
                       'BC stream TAM'],
                      ['AP and LLTM base',
                       'Current-year advance procurement and long-lead material that is '
                       'supplier-addressable',
                       'Ship-construction EOQ and long-lead material after the non-GFE filter',
                       'AWS EOQ, Other GFE, VLS and weapons AP',
                       'AP and LLTM stream TAM'],
                      ['FFATA-visible flow',
                       'First-tier subawards reported to FSRS and surfaced through SAM.gov',
                       'Reportable first-tier subcontracts above the threshold',
                       'Direct material, lower-tier subs, standing agreements, sub-threshold tail',
                       'Evidence and bucket rules'],
                      ['Supplier-addressable TAM',
                       'BC base times the BC supplier coefficient, plus AP and LLTM base times the '
                       'AP coefficient',
                       'Non-GFE new-construction supplier work away from the prime yards',
                       'GFE, WPN and OPN weapons, sustainment, design-only, SOM and capture',
                       'Headline market size'],
                      ['SAM scenarios',
                       'Selected work-type bucket menus within TAM',
                       'Broad, metal, electrical, modular, HM&E',
                       'Unbucketed residual unless later classified, capture probability',
                       'Where-to-play menu']],
             'cell_fills': {'(6,0)': 'BLUE_1'},
             'cell_bold': {'(6,0)': True},
             'cell_text_colors': {},
             'footnotes': ['Seven distinct denominators. Total ship cost and SCN context the '
                           'scope; the headline market is supplier-addressable TAM after '
                           'exclusions and coefficients.']},
  'columns': [{'name': 'Denominator', 'unit': 'name', 'tie_out': 'deck glossary'},
              {'name': 'Definition',
               'unit': 'text',
               'tie_out': 'TAM Build §2-§5 / SAM Build §4a / FAR 52.204-10'},
              {'name': 'Included examples',
               'unit': 'text',
               'tie_out': 'Scope Exclusions / AP Bridge §3'},
              {'name': 'Excluded examples',
               'unit': 'text',
               'tie_out': 'Scope Exclusions §2 / wiki 01'},
              {'name': 'Where used', 'unit': 'text', 'tie_out': 'deck figure register'}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Denominator and scope ledger, DDG-51 supplier TAM", BODY_X, BODY_Y, BODY_CX))
    tbl, h = make_table(20, "DenominatorLedger", BODY_X, BODY_Y + 220_000, BODY_CX, _TABLES[0], size_override=780, min_row_h=205_000)
    out.append(tbl)
    y = BODY_Y + 220_000 + h + 80_000
    out.append(bullet_rail(40, BODY_X, y, BODY_CX, 520_000,
        [("TAM window:", "FY2022 to FY2027; the wiki framing window is FY2018 to FY2027."),
         ("In scope:", "DDG-51 new-construction PIID set, two prime yards plus major GFE primes."),
         ("Excluded:", "Zumwalt, depot sustainment, WPN and OPN weapons, GFE combat-system content, and contaminants.")], body_size=FINEPRINT_8_5PT, lead_size=FINEPRINT_8_5PT, insets=INSETS_NONE))
    out.append(nofill(50, "BoundaryCue", BODY_X, BODY_B - 300_000, BODY_CX, 280_000,
        [lead_body("Boundary cue:", "the deck sizes non-GFE new-construction supplier work within Basic Construction and AP and LLTM. SAM is a strict subset of TAM, never SOM.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT)], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
