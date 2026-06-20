"""appendix_bucket_rules_supplier_evidence — generated from the DDG slide spec.

Intent: Show the rules that convert visible subaward evidence into work-type buckets, the per-bucket supplier proof points, the residual logic, and the SAM scenario-membership inputs.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Bucket rules'
_TITLE_TOPIC = 'Bucket Rules and Supplier Evidence'
_TAKEAWAY = 'Description-led classification maps subawards into seven target work types, with an explicit residual'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) SAM.gov Entity Management API; (3) FAR 52.204-10'

_CHART_SPECS = []
_TABLES = [{'id': 'bucket_rules_1',
  'element': 'e2',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'Bucket definitions, scale, and supplier evidence',
               'purpose': 'define',
               'reader_takeaway': 'Seven named buckets are classified by description, vendor '
                                  'override, then NAICS fallback; the residual (~42.9% of TAM) '
                                  'stays explicit and outside broad SAM until evidence supports '
                                  'assignment.',
               'row_order': 'structural, machining, castings, piping, electrical, HVAC, coatings, '
                            'residual',
               'highlight_rows': ['Unbucketed / ambiguous residual'],
               'guardrails': ['The residual stays explicit and is not hidden in broad component '
                              'SAM.',
                              'Scenario membership must match the scenario flags exactly.',
                              'Supplier evidence is parent-level (Vendors tab), not bucket-split '
                              'CD09.']},
  'render': {'table_skin': 'rule',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [1.7, 2.8, 1.2, 1.2, 2.5, 1.4],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'l', 'r', 'r', 'l', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Bucket',
                       'Inclusion rule',
                       'Avg annual',
                       'FY22-27 cum.',
                       'Supplier evidence',
                       'Scenarios'],
                      ['Structural fab and pre-outfit',
                       'Hull sections, fabricated structural metal, deckhouse, pre-outfit modules',
                       '~$101M',
                       '~$608M',
                       'Major Tool and Machine; Superior Electromechanical; Leonardo via DRS',
                       'metal, modular, broad'],
                      ['Machining',
                       'Machine shops, precision machining, mechanical power transmission',
                       '~$66M',
                       '~$394M',
                       'Major Tool and Machine; Rolls-Royce; Timken Gears and Services',
                       'metal, HM&E, broad'],
                      ['Castings and forgings',
                       'Iron and steel forging, steel foundries, cast components',
                       '~$3M',
                       '~$16M',
                       'Ellwood Group',
                       'metal, broad'],
                      ['Piping, valves, and pumps',
                       'Industrial valves, pumps, manifolds, pipe and fittings, hydraulics',
                       '~$13M',
                       '~$78M',
                       'Curtiss-Wright; CIRCOR; Leslie Controls (vendor overrides)',
                       'HM&E, broad'],
                      ['Electrical and power',
                       'Switchgear, switchboards, cable, generators, motors, power distribution',
                       '~$132M',
                       '~$791M',
                       'Leonardo via DRS; General Electric; DRS Naval',
                       'electrical, broad'],
                      ['HVAC and ventilation',
                       'Air-conditioning, chilled water, warm-air heating, shipboard ventilation',
                       '~$10M',
                       '~$59M',
                       'Johnson Controls Navy Systems',
                       'HM&E, broad'],
                      ['Coatings and insulation',
                       'Coatings, paint, deck covering, insulation, rubber and synthetic',
                       '~$3M',
                       '~$17M',
                       'M.S.M. Industries; Espey Mfg. and Electronics',
                       'modular, broad'],
                      ['Unbucketed / ambiguous residual',
                       'Insufficient description, ambiguous scope, or evidence too thin to '
                       'classify; do not force-classify',
                       '~$246M',
                       '~$1.47B',
                       'Held explicit; not assigned to a named bucket',
                       'excluded from broad']],
             'cell_fills': {'(8,0)': 'GRAY_2',
                            '(8,1)': 'GRAY_2',
                            '(8,2)': 'GRAY_2',
                            '(8,3)': 'GRAY_2',
                            '(8,4)': 'GRAY_2',
                            '(8,5)': 'GRAY_2'},
             'cell_bold': {'(8,0)': True, '(8,2)': True, '(8,3)': True, '(8,5)': True},
             'cell_text_colors': {},
             'footnotes': ['Classification arbiter: description keyword, then vendor override, '
                           'then NAICS-4 fallback, then residual.',
                           'Broad component manufacturing is the seven named buckets (~57.1% of '
                           'TAM), not the residual. Avg annual = FY22-27 cumulative divided by '
                           'six.']},
  'columns': [{'name': 'Bucket', 'unit': 'text', 'tie_out': '_taxonomy BUCKETS', 'formula': None},
              {'name': 'Inclusion rule',
               'unit': 'text',
               'tie_out': '_taxonomy BUCKETS definition + DESC_BUCKET keywords',
               'formula': None},
              {'name': 'Avg annual',
               'unit': '$M per year',
               'tie_out': 'SAM Build §3 bucket TAM / 6',
               'formula': 'cumulative divided by six'},
              {'name': 'FY22-27 cum.',
               'unit': '$M',
               'tie_out': 'SAM Build §3 bucket TAM',
               'formula': 'portfolio TAM x modeled bucket share'},
              {'name': 'Supplier evidence',
               'unit': 'text',
               'tie_out': 'Vendors tab / nc_lifetime_vendors.csv; Worktype Evidence §2',
               'formula': None},
              {'name': 'Scenarios',
               'unit': 'text',
               'tie_out': 'inputs_scenarios scenario flags',
               'formula': None}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(exhibit_title(10, "Bucket definitions, scale, and supplier evidence", BODY_X, BODY_Y, BODY_CX))
    tbl, h = make_table(20, "BucketRules", BODY_X, BODY_Y + 220_000, BODY_CX, _TABLES[0], size_override=720, min_row_h=178_000)
    out.append(tbl)
    out.append(nofill(40, "RuleCue", BODY_X, BODY_B - 430_000, BODY_CX, 380_000,
        [lead_body("Arbiter:", "description keyword, then vendor override, then NAICS-4 fallback, then residual.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT),
         lead_body("Scenarios:", "broad component manufacturing is the seven named buckets; the residual is excluded until evidence assigns a named bucket.", lead_size=FINEPRINT_8_5PT, body_size=FINEPRINT_8_5PT)], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
