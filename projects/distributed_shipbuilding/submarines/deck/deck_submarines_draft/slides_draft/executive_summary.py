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


_SECTION = "Market and Scope"
_TOPIC = "Executive summary"
_TAKEAWAY = "Average annual opportunity is about $3.3B TAM and $2.8B broad SAM"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA/FSRS records and Entity Management API"


def _support(sp_id, x, y, w, label, value, qual, fill):
    return _kpi(sp_id, "Support", x, y, w, 780_000, label, value, qual,
                fill=fill, color=DK, line_color=GRAY_3, line_width=12_700,
                value_size=RIBBON_KPI_18PT, label_size=LABEL_9PT, qualifier_size=FINEPRINT_8_5PT,
                insets=INSETS_CARD)


def _body() -> str:
    out = []
    out.append(_note(10, "AverageNote", BODY_X, BODY_Y, BODY_CX, 240_000,
        "FY2022-FY2027 model-period averages; not a commercial-style steady run-rate.", size=FINEPRINT_8_5PT, italic=True))
    y = BODY_Y + 520_000
    hero_h = 1_230_000
    w = (BODY_CX - GAP) // 2
    out.append(_kpi(20, "TAMHero", BODY_X, y, w, hero_h, "AVERAGE ANNUAL TAM", "~$3.3B",
                    "FY2022-FY2027 model-period average", fill=BLUE_5, color=WHITE))
    out.append(_kpi(21, "BroadSAMHero", BODY_X + w + GAP, y, w, hero_h, "AVERAGE ANNUAL BROAD SAM", "~$2.8B",
                    "Broad component-manufacturing scenario", fill=BLUE_4, color=WHITE))
    sy = y + hero_h + 310_000
    xs, sw = _grid_x(4, start=BODY_X, total=BODY_CX, gap=GAP)
    out.append(_support(30, xs[0], sy, sw, "Cumulative TAM", "~$19.8B", "FY2022-FY2027", BLUE_1))
    out.append(_support(31, xs[1], sy, sw, "Cumulative broad SAM", "~$16.8B", "FY2022-FY2027", BLUE_1))
    out.append(_support(32, xs[2], sy, sw, "Applied BC supplier coefficient", "35.0%", "strict, non-nuclear, yard-excluded", GRAY_1))
    out.append(_support(33, xs[3], sy, sw, "AP and LLTM additive base", "$0", "no double count", GRAY_1))
    rail_y = sy + 1_000_000
    paras = [_txt("KEY FINDINGS", size=CAP_12PT, bold=True, color=DK, align="l")]
    for line in [
        "1. Basic Construction is the denominator; GFE and SIB capacity grants are excluded.",
        "2. The supplier coefficient is deliberately strict: non-nuclear, BPMI-excluded, yard-excluded.",
        "3. Broad SAM is a scenario menu; no SOM, capture share, or win probability is modeled.",
        "4. Annual flow is lumpy, with FY2024 and FY2027 peaks shown later in the deck.",
    ]:
        paras.append(_txt(line, size=LABEL_9PT, color=DK, align="l"))
    out.append(text_box(40, "FindingsRail", BODY_X, rail_y, BODY_CX, BODY_B - rail_y - 60_000, paras,
                        fill=None, line_color=None, insets=INSETS_MESSAGE, anchor="t"))
    return "".join(out)
