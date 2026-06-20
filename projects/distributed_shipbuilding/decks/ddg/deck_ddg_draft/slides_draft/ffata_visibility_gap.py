"""ffata_visibility_gap — generated from the DDG slide spec.

Intent: Show the visible FFATA flow against the estimated yard-side outsourcing band and land that visible subawards are a floor (evidence), not the denominator; the deck's TAM does not come from summing FFATA.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Visibility gap'
_TITLE_TOPIC = 'FFATA Visibility Gap'
_TAKEAWAY = 'FFATA is evidence, not the market-size denominator'
_SOURCES = 'Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) HII and General Dynamics Form 10-K filings; (3) U.S. BLS OEWS, NAICS 336611'

_CHART_SPECS = [{'id': 'chart_1',
  'factory': 'bar_chart',
  'chart_index': 0,
  'title_element': 'e1',
  'frame_element': 'e2',
  'data': {'categories': ['FFATA-visible yard-side flow (~$2.73B)',
                          'Estimated outsourcing, low (~$11.31B)',
                          'Estimated outsourcing, midpoint (~$13.57B)',
                          'Estimated outsourcing, high (~$16.16B)'],
           'series': [{'name': 'Cumulative FY2016-FY2027',
                       'values': [2728.6, 11311.4, 13573.7, 16159.2],
                       'data_point_colors': ['BLUE_5', 'GRAY_2', 'GRAY_4', 'GRAY_2']}]},
  'params': {'mode': 'clustered',
             'value_axis_format': '"$"#,##0"M"',
             'show_legend': False,
             'show_gridlines': True,
             'major_gridline_color': 'GRAY_1',
             'show_value_labels': True,
             'value_label_format': '"$"#,##0"M"',
             'value_label_size_pt': 9,
             'cat_label_size_pt': 9,
             'gap_width': 60,
             'cat_header': 'Measure',
             'title': None},
  'external_title': {'text': 'Cumulative FFATA-visible flow vs estimated yard-side outsourcing, $M',
                     'size': 'CHART_TITLE_10PT',
                     'italic': True,
                     'color': 'DK'},
  'annotations': [{'text': 'Implied visible share at midpoint ~20.1%; a floor, not a denominator.',
                   'anchor_to': 'e4'}]}]
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    chart_w = int(BODY_CX * 0.60)
    rx = BODY_X + chart_w + GAP
    rw = BODY_R - rx
    out.append(exhibit_title(10, "Cumulative FFATA-visible flow vs estimated yard-side outsourcing, $M", BODY_X, BODY_Y, chart_w))
    out.append(chart(20, "VisibilityGapChart", BODY_X, BODY_Y + 240_000, chart_w, 3_100_000, "rId2"))
    out.append(exhibit_title(30, "What public FFATA misses", rx, BODY_Y + 240_000, rw))
    chip_h = 435_000
    y = BODY_Y + 570_000
    missed = [
        ("Direct material", "Booked as direct cost, not a subcontract"),
        ("Lower tiers", "A sub's sub is outside FFATA visibility"),
        ("Standing agreements", "Long-term supplier deals may not sit under a prime PIID"),
        ("Threshold and lag", "Sub-$30,000 actions plus 12-30 month reporting lag"),
        ("Reporting gap", "BIW under-reporting is acute but not the whole gap"),
    ]
    for i, (cap, body) in enumerate(missed):
        out.append(chip(31+i, f"Miss{i}", rx, y+i*(chip_h+GAP//2), rw, chip_h, cap, body, fill=GRAY_1, line_color=BLACK))
    out.append(text_box(50, "VisibleShareCallout", BODY_X + 650_000, BODY_Y + 650_000, 3_300_000, 520_000,
        [p("Visible flow is ~20.1%", size=MESSAGE_11PT, bold=True, color=DK, align="ctr"),
         p("of the midpoint estimate on a cumulative basis", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color=BLACK, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(nofill(60, "EvidenceNote", BODY_X, BODY_B - 360_000, chart_w, 300_000,
        [p("FFATA provides public evidence of the supplier base; it does not capture the full true flow. Values are cumulative FY2016-FY2027.", size=FINEPRINT_8_5PT, color=DK, align="l")], anchor="t"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
