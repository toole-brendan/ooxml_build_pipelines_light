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
_TOPIC = "Data limits"
_TAKEAWAY = "FFATA captures a visible floor, not the full supplier layer"
_SOURCES = "Sources: (1) FAR 52.204-10; (2) SAM.gov FFATA and FSRS records; (3) General Dynamics and HII Form 10-K filings"


def _ledger(sp_id, x, y, w, title, lines, fill):
    return _card(sp_id, "LedgerPanel", x, y, w, 2_700_000, title, lines, fill=fill,
                 title_size=CAP_12PT, body_size=DENSE_BODY_10PT, title_align="ctr")


def _chip(sp_id, x, y, w, label, body, fill):
    return text_box(sp_id, "GuardrailChip", x, y, w, 500_000,
        [_txt(label, size=FINEPRINT_8_5PT, bold=True, color=DK, align="ctr"),
         _txt(body, size=DENSE_BODY_10PT, bold=True, color=DK, align="ctr")],
        fill=fill, line_color=GRAY_3, insets=INSETS_MICRO_CAP, anchor="ctr")


def _body() -> str:
    out = []
    y = BODY_Y
    w = (BODY_CX - GAP) // 2
    out.append(_ledger(20, BODY_X, y, w, "VISIBLE AND MEASURED LAYER", [
        "FFATA-visible first-tier subawards",
        "Named vendors and parent entities",
        "SAM.gov Entity NAICS enrichment",
        "DoD Contracts POP evidence",
        "SCN P-5c and P-10 budget exhibits",
    ], BLUE_1))
    out.append(_ledger(21, BODY_X+w+GAP, y, w, "UNSEEN OR UNDER-OBSERVED LAYER", [
        "Purchased material booked as direct material",
        "Lower-tier subcontracts",
        "HII Newport News visibility gap",
        "Standing supplier agreements",
        "Reporting lag",
        "Unparsed single-site POP rows",
    ], GRAY_1))
    note_y = y + 2_880_000
    out.append(_note(30, "Interpretation", BODY_X, note_y, BODY_CX, 320_000,
        "Visible data is strong enough to classify and triangulate, not complete enough to equal the whole supplier layer.",
        size=DENSE_BODY_10PT, bold_lead="Visible data", italic=False))
    chip_y = BODY_B - 590_000
    xs, cw = _grid_x(4, start=BODY_X, total=BODY_CX, gap=GAP)
    chips = [
        ("MODEL GUARDRAIL", "No SOM or capture modeled", GRAY_2),
        ("DOUBLE-COUNT CHECK", "AP and LLTM additive base = $0", GRAY_2),
        ("DOLLAR BASIS", "Nominal then-year dollars", GRAY_2),
        ("SUPPLIER VISIBILITY", "FFATA-visible = named floor", BLUE_1),
    ]
    for i,(l,b,f) in enumerate(chips):
        out.append(_chip(40+i, xs[i], chip_y, cw, l, b, f))
    return "".join(out)
