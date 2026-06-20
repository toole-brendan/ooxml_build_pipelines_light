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
_TOPIC = "Boundary"
_TAKEAWAY = "The model sizes non-nuclear supplier opportunity, excluding GFE, SIB, yards, and SOM"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) FAR 52.204-10 and FAR Part 45; (3) GAO-25-106286"


def _body() -> str:
    out = []
    out.append(_note(10, "BoundaryNote", BODY_X, BODY_Y, BODY_CX, 260_000,
        "A narrower answer is more defensible than a larger, double-counted market.", size=FINEPRINT_8_5PT, italic=True))
    y = BODY_Y + 520_000
    h = 2_650_000
    xs, w = _grid_x(3, start=BODY_X, total=BODY_CX, gap=GAP)
    out.append(_card(20, "Included", xs[0], y, w, h, "INCLUDED IN TAM", [
        "P-5c Basic Construction base for Virginia and Columbia new construction",
        "Non-nuclear supplier component manufacturing inside that base",
        "Purchased material, subcontracts, and lower-tier supplier flow where supported",
        "Work-type buckets used for scenario SAM",
    ], fill=BLUE_1, title_align="ctr", body_size=DENSE_BODY_10PT))
    out.append(_card(21, "Excluded", xs[1], y, w, h, "EXCLUDED FROM TAM", [
        "GFE and GFP: reactor plant, combat systems, sonar, weapons, ordnance",
        "BPMI nuclear reactor work",
        "SIB capacity-development grants and pass-throughs",
        "Prime and co-prime yard work at GDEB and HII",
        "Depot, sustainment, overhauls, design-only, classified payloads",
        "AP and LLTM already inside Basic Construction; additive base is $0",
    ], fill=GRAY_2, title_align="ctr", body_size=LABEL_9PT))
    out.append(_card(22, "Context", xs[2], y, w, h, "CONTEXT ONLY", [
        "Total Ship Estimate and TOA as top-of-funnel context",
        "Gross AP and LLTM reference stream; additive base is $0",
        "FFATA and FSRS visible first-tier vendor floor",
        "DoD place-of-performance evidence behind the supplier coefficient",
        "HII Newport News visibility gap and unseen-layer limitations",
    ], fill=GRAY_1, title_align="ctr", body_size=LABEL_9PT))
    warn_y = BODY_Y + 3_520_000
    out.append(text_box(30, "WarningRail", BODY_X, warn_y, BODY_CX, 720_000,
        [paragraph([run("Boundary warning: ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
                    run("No SOM is modeled. SAM is a scenario menu, not market share, capture, win probability, or revenue forecast.", size=DENSE_BODY_10PT, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    return "".join(out)
