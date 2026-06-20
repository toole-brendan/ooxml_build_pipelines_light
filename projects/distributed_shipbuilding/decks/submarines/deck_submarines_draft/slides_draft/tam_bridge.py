from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector,
)
from deck_core.style import *

LAYOUT = "slideLayout4"

GAP = 91_440
TITLE_BAND_H = 190_000
NOTE_H = 360_000
CAVEAT_H = 520_000


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = DK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _line(lead: str, body: str = "", *, lead_size: int = DENSE_BODY_10PT,
          body_size: int = LABEL_9PT, lead_color: str = DK, body_color: str = DK,
          align: str = "l", space_after: int = 0, bullet: bool = False,
          italic_body: bool = False) -> str:
    runs = [run(lead, size=lead_size, bold=True, color=lead_color, font=FONT)]
    if body:
        runs.append(run(" " + body, size=body_size, italic=italic_body, color=body_color, font=FONT))
    return paragraph(runs, align=align, space_after=space_after, bullet=bullet)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=DK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=DK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=DK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _card(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, title: str,
          lines: list[str], *, fill: str = BLUE_1, color: str = DK,
          line_color=GRAY_3, line_width: int = 12_700,
          title_size: int = CAP_12PT, body_size: int = DENSE_BODY_10PT,
          title_align: str = "ctr", body_bullets: bool = False,
          insets=INSETS_CARD, anchor: str = "t") -> str:
    paras = [_txt(title, size=title_size, bold=True, color=color, align=title_align)]
    for i, line in enumerate(lines):
        paras.append(_txt(line, size=body_size, color=color, align="l"))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor=anchor)


def _kpi(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
         label: str, value: str, qualifier: str, *, fill: str, color: str,
         line_color=BLACK, line_width: int = 19_050, value_size: int = HERO_32PT,
         label_size: int = CAP_12PT, qualifier_size: int = LABEL_9PT,
         insets=INSETS_ANSWER_CARD) -> str:
    paras = [
        _txt(label, size=label_size, bold=True, color=color, align="ctr"),
        _txt(value, size=value_size, bold=True, color=color, align="ctr"),
        _txt(qualifier, size=qualifier_size, italic=True, color=color, align="ctr"),
    ]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor="ctr")


def _chart_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_BAND_H,
                    [_txt(text, size=CHART_TITLE_10PT, italic=True, color=DK, align="l")],
                    fill=None, line_color=None, insets=INSETS_NONE, anchor="t")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    w = (total - (n - 1) * gap) // n
    return [start + i * (w + gap) for i in range(n)], w


def _grid_y(n: int, *, start: int = BODY_Y, total: int = BODY_CY, gap: int = GAP):
    h = (total - (n - 1) * gap) // n
    return [start + i * (h + gap) for i in range(n)], h


def _render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )

render = _render


_SECTION = "Market Sizing"
_TOPIC = "TAM Bridge Calculation"
_TAKEAWAY = "Applying the strict 35.0% coefficient yields ~$3.3B average annual TAM"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA and FSRS records"


def _bridge_card(sp_id, name, x, y, w, h, label, value, qual, fill, color=DK, line_width=12_700, value_size=RIBBON_KPI_18PT):
    return _kpi(sp_id, name, x, y, w, h, label, value, qual, fill=fill, color=color,
                line_color=BLACK, line_width=line_width, value_size=value_size,
                label_size=CAP_12PT, qualifier_size=FINEPRINT_8_5PT, insets=INSETS_CARD)


def _body() -> str:
    out = []
    base_x, base_y, base_w, card_h = BODY_X + 650_000, BODY_Y + 270_000, 3_300_000, 900_000
    coeff_x, coeff_y, coeff_w = BODY_R - 650_000 - 3_300_000, base_y, 3_300_000
    op_x, op_y, op_w = BODY_X + BODY_CX//2 - 240_000, base_y + 170_000, 480_000
    cum_x, cum_y, cum_w = BODY_X + 3_250_000, BODY_Y + 1_640_000, 4_800_000
    annual_x, annual_y, annual_w = BODY_X + 3_000_000, BODY_Y + 2_820_000, 5_300_000

    # Connectors first: four bridge links behind cards.
    out.append(connector(80, "BaseToOperator", base_x+base_w, base_y+card_h//2, op_x-(base_x+base_w), 0, color=BLACK, width=9_525, arrow=True))
    out.append(connector(81, "CoeffToOperator", coeff_x, coeff_y+card_h//2, (op_x+op_w)-coeff_x, 0, color=BLACK, width=9_525, arrow=True))
    out.append(connector(82, "OperatorToCumulative", op_x+op_w//2, op_y+op_w, 0, cum_y-(op_y+op_w), color=BLACK, width=9_525, arrow=True))
    out.append(connector(83, "CumulativeToAnnual", cum_x+cum_w//2, cum_y+850_000, 0, annual_y-(cum_y+850_000), color=BLACK, width=9_525, arrow=True))

    out.append(_bridge_card(10, "BasicConstructionBase", base_x, base_y, base_w, card_h,
        "BASIC CONSTRUCTION BASE", "$56.647B", "FY2022-FY2027 P-5c", BLUE_1))
    out.append(text_box(11, "Operator", op_x, op_y, op_w, op_w,
        [paragraph([])], fill=BLACK, line_color=BLACK, prst="mathMultiply", insets=INSETS_NONE, anchor="ctr"))
    out.append(_note(12, "OperatorCaption", op_x-230_000, op_y+op_w+10_000, op_w+460_000, 150_000,
        "multiplied by", size=CONNECTOR_NOTE_8_5PT, italic=True))
    out.append(_bridge_card(13, "Coefficient", coeff_x, coeff_y, coeff_w, card_h,
        "APPLIED BC SUPPLIER COEFFICIENT", "35.0%", "strict, non-nuclear, yard-excluded", BLUE_4, WHITE))
    out.append(_kpi(20, "CumulativeTAM", cum_x, cum_y, cum_w, 850_000,
        "CUMULATIVE PORTFOLIO TAM", "$19.840B", "FY2022-FY2027", fill=BLUE_2, color=DK,
        line_color=BLACK, line_width=12_700, value_size=ANSWER_KPI_24PT, insets=INSETS_ANSWER_CARD))
    out.append(_note(21, "Divide", cum_x+cum_w//2+250_000, cum_y+920_000, 1_100_000, 170_000,
        "divide by 6", size=CONNECTOR_NOTE_8_5PT, italic=True, align="l"))
    out.append(_kpi(30, "AnnualTAM", annual_x, annual_y, annual_w, 1_060_000,
        "AVERAGE ANNUAL TAM", "~$3.307B", "FY2022-FY2027 model-period average",
        fill=BLUE_5, color=WHITE, line_color=BLACK, line_width=19_050))
    strip_y = BODY_Y + 4_060_000
    out.append(text_box(40, "SubtractionCheck", BODY_X, strip_y, BODY_CX, 430_000,
        [paragraph([run("Subtraction check: ", size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT),
                    run("$56.647B BC base minus $36.807B prime, co-prime, and excluded share equals $19.840B TAM.", size=DENSE_BODY_10PT, color=DK, font=FONT)], align="ctr")],
        fill=GRAY_1, line_color=GRAY_3, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(_note(50, "Guardrail", BODY_X, BODY_B-310_000, BODY_CX, 240_000,
        "Guardrail: Only the strict 35.0% BC coefficient feeds headline TAM; broader POP views are sensitivity.",
        size=DENSE_BODY_10PT, bold_lead="Guardrail:", italic=False))
    return "".join(out)
