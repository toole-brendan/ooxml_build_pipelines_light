"""appendix_tam_calculation — generated from the DDG slide spec.

Intent: Show the full FY22-27 cumulative TAM calculation, the per-FY profile, and the six-year average-annual convention behind the ~$573M per year headline, plus the BC-base to supplier-TAM bridge and the per-hull view.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'TAM calculation'
_TITLE_TOPIC = 'TAM Calculation'
_TAKEAWAY = 'The annual headline is the FY22-27 cumulative two-stream model divided by six'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122, Exhibit P-5c; (2) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-40; (3) DoW DDG-51 contract announcements, July 2022 to May 2026'

_CHART_SPECS = []
_TABLES = [{'id': 'tam_reconciliation',
  'element': 'e2',
  'role': 'appendix_detail',
  'factory': 'house_table',
  'semantic': {'table_name': 'FY22-27 supplier-TAM reconciliation',
               'purpose': 'reconcile',
               'reader_takeaway': 'Portfolio supplier TAM equals the BC stream plus the AP and '
                                  'LLTM stream, then divided by six fiscal years for the annual '
                                  'headline.',
               'row_order': 'Basic Construction base, BC supplier coefficient, BC-stream supplier '
                            'TAM, CY AP in-window, ship-construction share, non-GFE AP base, AP '
                            'and LLTM coefficient, AP and LLTM stream TAM, portfolio supplier TAM, '
                            'average-annual convention',
               'highlight_rows': ['BC-stream supplier TAM',
                                  'AP and LLTM stream TAM',
                                  'Portfolio supplier TAM',
                                  'Average annual convention'],
               'guardrails': ['Annual values are average annual, not a run-rate.',
                              'AP and LLTM values must remain labeled as the second stream.',
                              'No SOM or capture language.']},
  'render': {'table_skin': 'rule',
             'size': 850,
             'column_widths': {'mode': 'ratio',
                               'values': [3.0, 1.2, 1.1, 1.1, 2.4],
                               'builder_resolves_to_emu': True,
                               'sum_to_region_width': True},
             'col_w_emu_override': [],
             'aligns': ['l', 'r', 'r', 'ctr', 'l'],
             'row_h': {'fn': 'estimate_row_heights',
                       'size_pt_from': 'size',
                       'header_size_pt_from': 'size'},
             'rows': [['Step',
                       'FY22-27 cumulative $M',
                       'Avg $M per year',
                       'Coefficient',
                       'Model source or note'],
                      ['Basic Construction base',
                       '17,471.0',
                       '2,911.8',
                       'n.a.',
                       'P-5c BC base, LI 2122'],
                      ['BC supplier coefficient (MYP-corrected)',
                       'n.a.',
                       'n.a.',
                       '12.5%',
                       'Other-US and foreign POP'],
                      ['BC-stream supplier TAM',
                       '2,192.0',
                       '365.3',
                       'applied',
                       'Base times coefficient'],
                      ['CY AP in-window (FY25 to FY27)',
                       '1,833.2',
                       '305.5',
                       'n.a.',
                       'FY22-24 sit in Prior Years'],
                      ['Ship-construction share of CY AP',
                       '1,466.6',
                       '244.4',
                       '80.0%',
                       'Non-GFE share'],
                      ['Non-GFE AP base', '1,466.6', '244.4', 'n.a.', 'AP base after the share'],
                      ['AP and LLTM supplier coefficient',
                       'n.a.',
                       'n.a.',
                       '85.0%',
                       'Inputs assumption knob'],
                      ['AP and LLTM stream TAM', '1,246.6', '207.8', 'applied', 'Second stream'],
                      ['Portfolio supplier TAM', '3,438.6', '573.1', 'n.a.', 'Headline TAM'],
                      ['Average annual convention',
                       '3,438.6',
                       '573.1',
                       'divide by 6',
                       'Not a steady run-rate']],
             'cell_fills': {'(3,0)': 'BLUE_1',
                            '(8,0)': 'BLUE_1',
                            '(9,0)': 'BLUE_2',
                            '(10,0)': 'GRAY_1'},
             'cell_bold': {'(3,0)': True, '(8,0)': True, '(9,0)': True, '(10,0)': True},
             'cell_text_colors': {},
             'footnotes': ['Average annual = FY22-27 cumulative divided by six fiscal years; an '
                           'average, not a steady run-rate. The per-FY TAM profile is lumpy: '
                           '~$245M FY22, ~$1,225M FY26.']},
  'columns': [{'name': 'Step', 'unit': 'text', 'tie_out': 'TAM Build §5 and AP Bridge §2'},
              {'name': 'FY22-27 cumulative $M',
               'unit': '$M',
               'tie_out': 'TAM Build §5a/§5e source outputs'},
              {'name': 'Avg $M per year',
               'unit': '$M per year',
               'tie_out': 'cumulative divided by six'},
              {'name': 'Coefficient',
               'unit': 'percent or treatment',
               'tie_out': 'TAM Build §3a / Inputs §5'},
              {'name': 'Model source or note', 'unit': 'text', 'tie_out': 'source tabs'}]}]
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(nofill(10, "AnnualizationHeader", BODY_X, BODY_Y, BODY_CX, 320_000,
        [lead_body("Average annual:", "FY22-27 cumulative divided by six; not a steady run-rate. The per-FY TAM profile is lumpy, with a FY26 AP spike.", lead_size=FINEPRINT_8_5PT, body_size=MESSAGE_11PT)], anchor="t"))
    table_w = int(BODY_CX * 0.67)
    tbl, h = make_table(20, "TAMReconciliation", BODY_X, BODY_Y + 420_000, table_w, _TABLES[0], size_override=760, min_row_h=190_000)
    out.append(tbl)
    bx = BODY_X + table_w + GAP
    bw = BODY_R - bx
    by = BODY_Y + 420_000
    out.append(text_box(40, "MiniBridge", bx, by, bw, 1_350_000,
        [p("CUMULATIVE BRIDGE, $M", size=DENSE_BODY_10PT, bold=True, color=DK, align="ctr"),
         p("BC-stream supplier TAM: ~2,192.0", size=LABEL_9PT, color=DK, align="l"),
         p("AP and LLTM stream TAM: ~1,246.6", size=LABEL_9PT, color=DK, align="l"),
         p("Portfolio supplier TAM: ~3,438.6", size=VALUE_14PT, bold=True, color=DK, align="l"),
         p("Divide by 6: ~573.1 per year", size=VALUE_14PT, bold=True, color=DK, align="l")],
        fill=BLUE_1, line_color=BLACK, insets=INSETS_MESSAGE, anchor="t"))
    out.append(nofill(50, "PerHull", BODY_X, BODY_B - 680_000, BODY_CX, 330_000,
        [p("13 in-window hulls (award FY22-27). Supplier TAM per hull ~$265M; BC TAM per hull ~$169M. BC base ~$17.47B less POP removal leaves the ~$2.19B BC stream.", size=FINEPRINT_8_5PT, color=DK, align="l")], anchor="t"))
    out.append(sizing_note(51, "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
