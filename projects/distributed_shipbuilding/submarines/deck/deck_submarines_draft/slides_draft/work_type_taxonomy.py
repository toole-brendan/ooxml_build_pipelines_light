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


_SECTION = "Market sizing"
_TOPIC = "Work-type taxonomy"
_TAKEAWAY = "Seven component buckets define the serviceable market"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

_BUCKETS = [
    ("Structural fabrication and pre-outfit", "hull sections, fabricated structural metal, pre-outfit modules"),
    ("Machining", "machine shops, precision machining, mechanical power transmission"),
    ("Castings and forgings", "iron and steel forging, foundries, cast and forged components"),
    ("Piping, valves, and pumps", "industrial valves, pumps, measuring and dispensing, pipe and fittings"),
    ("Electrical and power", "switchgear, electronic components, propulsion-electronics, power distribution"),
    ("HVAC and ventilation", "air-conditioning, heating, shipboard ventilation systems"),
    ("Coatings and insulation", "rubber and synthetic products, composites, coatings and insulation"),
]


def _bucket_card(sp_id, x, y, w, title, desc):
    return _card(sp_id, "BucketCard", x, y, w, 700_000, title, [desc], fill=BLUE_1,
                 title_size=LABEL_9PT, body_size=FINEPRINT_8_5PT, title_align="l")


def _body() -> str:
    out = []
    out.append(_note(10, "IncludedLabel", BODY_X, BODY_Y, BODY_CX, 200_000,
        "Included in broad component manufacturing", size=DENSE_BODY_10PT, italic=False, align="l"))
    row1_y = BODY_Y + 360_000
    xs4, w4 = _grid_x(4, start=BODY_X, total=BODY_CX, gap=GAP)
    for i, (title, desc) in enumerate(_BUCKETS[:4]):
        out.append(_bucket_card(20+i, xs4[i], row1_y, w4, title, desc))
    row2_y = row1_y + 820_000
    xs3, w3 = _grid_x(3, start=BODY_X, total=BODY_CX, gap=GAP)
    for i, (title, desc) in enumerate(_BUCKETS[4:]):
        out.append(_bucket_card(30+i, xs3[i], row2_y, w3, title, desc))
    label_y = row2_y + 930_000
    out.append(_note(40, "ExcludedLabel", BODY_X, label_y, BODY_CX, 200_000,
        "Outside broad component SAM", size=DENSE_BODY_10PT, italic=False, align="l"))
    res_y = label_y + 260_000
    out.append(text_box(50, "Residual", BODY_X, res_y, BODY_CX, 620_000,
        [paragraph([run("Unbucketed / ambiguous residual: ", size=MESSAGE_11PT, bold=True, color=DK, font=FONT),
                    run("visible vendor flow not confidently assigned to one of the seven buckets. Kept in TAM, excluded from broad component SAM.", size=DENSE_BODY_10PT, color=DK, font=FONT)], align="ctr")],
        fill=GRAY_3, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(_note(60, "Method", BODY_X, BODY_B-320_000, BODY_CX, 260_000,
        "Mapped from FFATA-visible vendors using SAM.gov Entity Management NAICS and manual work-type evidence; NAICS is corporate-primary, not a per-action work description.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
