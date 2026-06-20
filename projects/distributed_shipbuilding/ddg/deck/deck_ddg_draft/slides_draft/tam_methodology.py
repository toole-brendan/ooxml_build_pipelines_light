"""tam_methodology — generated from the DDG slide spec.

Intent: Explain the sizing equation clearly enough that a reader understands the two streams and the denominator correction behind the Basic Construction coefficient, before the numeric build.
"""
from __future__ import annotations

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip, sources_line
from ._helpers import *

LAYOUT = "slideLayout4"
_SECTION = 'DDG-51 supplier TAM'
_TOPIC = 'Method'
_TITLE_TOPIC = 'TAM Methodology'
_TAKEAWAY = 'TAM combines Basic Construction supplier work with AP and LLTM supplier material'
_SOURCES = 'Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API'

_CHART_SPECS = []
_TABLES = []
CHARTS = [build_chart(c) for c in _CHART_SPECS]


def _body() -> str:
    out = []
    out.append(nofill(10, "Equation", BODY_X, BODY_Y, BODY_CX, 360_000,
        [lead_body("Method:", "supplier TAM is the sum of two separately gated supplier streams.", lead_size=FINEPRINT_8_5PT, body_size=MESSAGE_11PT)], anchor="t"))
    y = BODY_Y + 620_000
    stream_w = int(BODY_CX * 0.42)
    plus_w = int(BODY_CX * 0.09)
    left_x = BODY_X
    plus_x = BODY_X + stream_w + int(BODY_CX * 0.045)
    right_x = plus_x + plus_w + int(BODY_CX * 0.045)
    right_w = BODY_R - right_x
    stream_h = 1_450_000
    out.append(connector(20, "BCToPlus", left_x + stream_w, y + stream_h//2, plus_x - (left_x+stream_w), 0, color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(21, "APToPlus", right_x, y + stream_h//2, plus_x + plus_w - right_x, 0, color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    output_y = y + stream_h + 720_000
    output_x = BODY_X + int(BODY_CX * 0.29)
    output_w = int(BODY_CX * 0.42)
    out.append(connector(22, "PlusToOutputA", plus_x + plus_w//2, y + stream_h, output_x + output_w//3 - (plus_x+plus_w//2), output_y - (y+stream_h), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(connector(23, "PlusToOutputB", plus_x + plus_w//2, y + stream_h, output_x + 2*output_w//3 - (plus_x+plus_w//2), output_y - (y+stream_h), color=BLACK, width=NORMAL_LINE, arrow=True, prst="bentConnector3"))
    out.append(box(30, "BCStream", left_x, y, stream_w, stream_h,
        [p("BASIC CONSTRUCTION STREAM", size=LABEL_9PT, bold=True, color=DK, align="ctr", space_after=120),
         p("BC base: ~$17.47B cumulative", size=FINEPRINT_8_5PT, color=DK, align="ctr"),
         p("Times 12.5% MYP-corrected supplier coefficient", size=DENSE_BODY_10PT, bold=True, color=DK, align="ctr"),
         p("Equals ~$365M per year (~$2.19B cumulative)", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")], fill=GRAY_1, line_color=BLACK))
    out.append(text_box(31, "Plus", plus_x, y + 290_000, plus_w, 680_000,
        [p("PLUS", size=BADGE_16PT, bold=True, color=DK, align="ctr")], fill=BLUE_1, line_color=BLACK, insets=INSETS_CHIP, anchor="ctr"))
    out.append(box(32, "APStream", right_x, y, right_w, stream_h,
        [p("AP AND LLTM STREAM", size=LABEL_9PT, bold=True, color=DK, align="ctr", space_after=120),
         p("CY AP after 80.0% ship-construction share: ~$1.47B", size=FINEPRINT_8_5PT, color=DK, align="ctr"),
         p("Times 85.0% AP supplier coefficient", size=DENSE_BODY_10PT, bold=True, color=DK, align="ctr"),
         p("Equals ~$208M per year (~$1.25B cumulative)", size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr")], fill=GRAY_1, line_color=BLACK))
    out.append(kpi_card(40, "Output", output_x, output_y, output_w, 800_000, "Portfolio supplier TAM", "~$573M per year", "(~$3.44B FY22-27 cumulative)", fill=BLUE_5))
    out.append(nofill(50, "Guardrail", BODY_X, output_y + 900_000, BODY_CX, 360_000,
        [lead_body("Guardrail:", "the BC coefficient is 12.5% on the MYP-corrected non-GFE corpus. It is not the ~32.8% outside-yards POP share, nor the disclosed-only ~87% artifact.", lead_size=DENSE_BODY_10PT, body_size=LABEL_9PT)], anchor="t"))
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
