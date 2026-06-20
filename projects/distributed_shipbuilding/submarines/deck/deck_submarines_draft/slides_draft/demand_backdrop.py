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


_SECTION = "TAM Build"
_TOPIC = "Demand backdrop"
_TAKEAWAY = "Policy and prime behavior point toward distributed supplier capacity"
_SOURCES = "Sources: (1) U.S. GAO, GAO-21-257, GAO-24-107732, GAO-25-106286, and GAO-26-109068; (2) CRS RL32418 and U.S. Navy FY2027 30-Year Shipbuilding Plan; (3) HII and General Dynamics SEC 10-K filings and earnings calls"


def _event(sp_id, x, y, w, title, body, fill=GRAY_1):
    return _card(sp_id, "TimelineEvent", x, y, w, 1_080_000, title, [body], fill=fill,
                 title_size=LABEL_9PT, body_size=FINEPRINT_8_5PT, title_align="l")


def _rail(sp_id, x, y, w, title, bullets):
    paras = [_txt(title, size=CAP_12PT, bold=True, color=DK, align="l")]
    for b in bullets:
        paras.append(paragraph([run(b, size=LABEL_9PT, color=DK, font=FONT)], bullet=True, space_after=80))
    return text_box(sp_id, "ThemeRail", x, y, w, 1_250_000, paras, fill=None, line_color=None,
                    insets=INSETS_CARD, anchor="t")


def _body() -> str:
    out = []
    axis_y = BODY_Y + 420_000
    left = BODY_X + 300_000
    right = BODY_R - 300_000
    out.append(connector(10, "TimeAxis", left, axis_y, right-left, 0, color=GRAY_4, width=12_700, arrow=False))
    tick_fracs = [0.08, 0.29, 0.50, 0.70, 0.90]
    labels = ["2021", "2024-2025", "Jan 2026", "Jan-Apr 2026", "Apr-May 2026"]
    for i, (f, lab) in enumerate(zip(tick_fracs, labels)):
        x = left + int((right-left)*f)
        out.append(connector(20+i, "Tick", x, axis_y-70_000, 0, 140_000, color=GRAY_4, width=9_525))
        out.append(_note(30+i, "TickLabel", x-360_000, axis_y-280_000, 720_000, 150_000, lab,
                         size=LABEL_9PT, italic=False, align="ctr"))
    y = BODY_Y + 800_000
    xs, ew = _grid_x(5, start=BODY_X, total=BODY_CX, gap=GAP)
    events = [
        ("Jan 2021", "GAO: supplier base roughly 70% smaller than prior booms; outsourcing raises oversight need.", GRAY_1),
        ("2024-2025", "SIB program office stood up; GAO documents outsourcing yard work due to constrained physical space.", GRAY_1),
        ("Jan 2026", "CRS: about 16,000 suppliers; about 70% of critical suppliers sole-source; AUKUS lifts demand.", GRAY_1),
        ("Jan-Apr 2026", "GD: supply chain remains the gating item; sole-source components are a bottleneck.", GRAY_1),
        ("Apr-May 2026", "GAO and Navy plan point to distributed shipbuilding; HII guides to plus 30% outsourcing hours.", BLUE_1),
    ]
    for i, (t,b,f) in enumerate(events):
        out.append(_event(40+i, xs[i], y, ew, t, b, f))
    rail_y = BODY_Y + 2_520_000
    rxs, rw = _grid_x(3, start=BODY_X, total=BODY_CX, gap=GAP)
    out.append(_rail(60, rxs[0], rail_y, rw, "CONSTRAINT SIGNAL", [
        "Supplier base about 70% smaller than prior booms",
        "About 70% of critical suppliers sole-source",
        "AUKUS adds demand toward 2.33 Virginia per year",
    ]))
    out.append(_rail(61, rxs[1], rail_y, rw, "POLICY SIGNAL", [
        "More than $10B DoD submarine industrial-base investment",
        "SIB program office institutionalizes oversight",
        "Navy distributed-shipbuilding policy context",
    ]))
    out.append(_rail(62, rxs[2], rail_y, rw, "PRIME BEHAVIOR SIGNAL", [
        "HII guides to plus 30% YoY outsourcing hours",
        "GD: supply chain is the gating item",
        "Complex components drive bottlenecks",
    ]))
    out.append(_note(80, "Guardrail", BODY_X, BODY_B-330_000, BODY_CX, 260_000,
        "Backdrop signals direction of travel; they do not change the FY2022-FY2027 sizing math or imply immediate addressability.",
        size=FINEPRINT_8_5PT, italic=True, align="ctr"))
    return "".join(out)
