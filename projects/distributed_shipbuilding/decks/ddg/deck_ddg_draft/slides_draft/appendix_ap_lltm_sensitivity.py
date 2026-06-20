"""appendix_ap_lltm_sensitivity — generated from the DDG slide spec.

Intent: Show the AP and LLTM stream build (CY AP in-window x 80.0% ship-construction share x 85.0% supplier coefficient = ~$1.25B cumulative, ~$208M per year), document the line-level treatment, and bound the stream against the two editable AP knobs.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'AP and LLTM sensitivity'
_TITLE_TOPIC = 'AP and LLTM Sensitivity'
_TAKEAWAY = 'The AP and LLTM stream is assumption-driven and contributes about 36% of portfolio TAM'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, Line Item 2122; (2) CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; (3) DoD daily contract announcement, DDG 51 FY23-27 multiyear award, Aug. 1, 2023'

_CHART_SPECS = []
_TABLES = [{'id': 'ap_stream_build',
  'element': 'e1',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'AP and LLTM stream build',
               'purpose': 'calculate',
               'reader_takeaway': 'CY AP in-window x 80.0% ship-construction share x 85.0% '
                                  'supplier coefficient yields ~$1.25B cumulative, ~$208M per '
                                  'year, about 36% of portfolio TAM.',
               'row_order': 'CY Advance Procurement in-window, ship-construction share, AP and '
                            'LLTM supplier coefficient, AP and LLTM stream TAM',
               'highlight_rows': ['AP and LLTM stream TAM'],
               'guardrails': ['AP and LLTM is additive only after GFE-heavy and weapons flows are '
                              'excluded.',
                              'The 85.0% supplier coefficient is an Inputs assumption, not '
                              'measured over a POP corpus.',
                              'Use "AP and LLTM", not slash notation, in visible labels.']},
  'render': {'table_skin': 'light',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [2.5, 1.0, 1.0, 1.0, 2.0],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r', 'r', 'ctr', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Step', 'Cum $M', 'Avg $M per year', 'Share or coeff.', 'Treatment note'],
                      ['CY Advance Procurement, in-window',
                       '1,833.2',
                       '305.5',
                       'n.a.',
                       'FY25-27 CY AP base'],
                      ['x ship-construction share',
                       '1,466.6',
                       '244.4',
                       '80.0%',
                       'Strips AWS EOQ and other GFE'],
                      ['x AP and LLTM supplier coefficient',
                       '1,246.6',
                       '207.8',
                       '85.0%',
                       'Inputs assumption (no AP POP corpus)'],
                      ['AP and LLTM stream TAM',
                       '1,246.6',
                       '207.8',
                       '36.3%',
                       'Share of ~$3.44B portfolio TAM']],
             'cell_fills': {'(4,0)': 'BLUE_2', '(4,1)': 'BLUE_1'},
             'cell_bold': {'(4,0)': True, '(4,1)': True},
             'cell_text_colors': {},
             'footnotes': ['In-window CY AP is FY25-27 (FY22-24 AP sits in Prior Years); a lower '
                           'bound.']},
  'columns': [{'name': 'Step', 'unit': 'text', 'tie_out': 'AP Bridge §2', 'formula': None},
              {'name': 'Cum $M',
               'unit': '$M cumulative',
               'tie_out': 'AP Bridge §2',
               'formula': None},
              {'name': 'Avg $M per year',
               'unit': '$M per year',
               'tie_out': 'AP Bridge §2',
               'formula': 'cumulative divided by six'},
              {'name': 'Share or coeff.',
               'unit': 'percent',
               'tie_out': 'Assumptions §5 knobs',
               'formula': None},
              {'name': 'Treatment note',
               'unit': 'text',
               'tie_out': 'AP Bridge §3',
               'formula': None}]},
 {'id': 'ap_sensitivity_matrix',
  'element': 'e4',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'AP and LLTM cumulative TAM sensitivity',
               'purpose': 'sensitivity',
               'reader_takeaway': 'The two editable AP knobs bound the stream between ~$962M and '
                                  '~$1,568M cumulative across the 3x3 grid; the central case is '
                                  '~$1,247M.',
               'row_order': '70% share, 80% share, 90% share',
               'highlight_rows': ['80% share'],
               'guardrails': ['Matrix values are FY22-27 cumulative $M, not annualized.',
                              'Cell = CY AP in-window $1,833.224M x row share x column '
                              'coefficient.',
                              "The 80% row x 85% column central cell ties to the build table's "
                              '~$1,246.6M.']},
  'render': {'table_skin': 'light',
             'size': 900,
             'column_widths': {'mode': 'ratio',
                               'values': [1.2, 1.0, 1.0, 1.0],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r', 'r', 'r'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Share', 'AP coeff 75%', 'AP coeff 85%', 'AP coeff 95%'],
                      ['70%', '962', '1,091', '1,219'],
                      ['80%', '1,100', '1,247', '1,393'],
                      ['90%', '1,237', '1,403', '1,568']],
             'cell_fills': {'(2,0)': 'BLUE_2', '(2,2)': 'BLUE_1'},
             'cell_bold': {'(2,0)': True, '(2,2)': True},
             'cell_text_colors': {},
             'footnotes': ['Matrix values are FY22-27 cumulative $M; central case (80% x 85%) = '
                           '~$1,247M.']},
  'columns': []}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    left_w = int(BODY_CX * 0.53)
    tbl, h = make_table(20, "APStreamBuild", BODY_X, BODY_Y, left_w, _TABLES[0], size_override=820, min_row_h=230_000)
    out.append(tbl)
    y = BODY_Y + h + 140_000
    out.append(bullet_rail(40, BODY_X, y, left_w, 900_000,
        [("Include:", "Ship Construction EOQ and supplier-addressable long-lead material."),
         ("Exclude:", "Aegis Weapon System EOQ, Other GFE, VLS, weapons and ordnance AP, WPN and OPN flows."),
         ("Already in BC:", "Power Conversion Modules moved into Basic Construction in FY23; do not re-add.")],
        body_size=FINEPRINT_8_5PT, lead_size=FINEPRINT_8_5PT, insets=INSETS_NONE))
    rx = BODY_X + left_w + GAP
    rw = BODY_R - rx
    out.append(exhibit_title(50, "AP and LLTM cumulative TAM sensitivity, $M", rx, BODY_Y, rw))
    tbl2, h2 = make_table(60, "APSensitivity", rx, BODY_Y + 260_000, rw, _TABLES[1], size_override=880, min_row_h=230_000)
    out.append(tbl2)
    out.append(sizing_note(70, "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
