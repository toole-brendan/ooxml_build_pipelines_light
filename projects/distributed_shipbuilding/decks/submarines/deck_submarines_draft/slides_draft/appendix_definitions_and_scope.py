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

from deck_core.text_metrics import estimate_row_heights

_SECTION = "Appendix"
_TOPIC = "Definitions and scope"
_TAKEAWAY = "Key terms define the model boundary and prevent double counting"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books; (2) FAR 52.204-10; (3) FAR Part 45"

_ROWS = [
    ["Term", "Model role", "Treatment", "Guardrail"],
    ["TAM", "Non-GFE, non-SIB new-construction supplier opportunity", "In model", "Inside P-5c Basic Construction; opportunity ceiling, not forecast"],
    ["SAM", "Portion of TAM in targeted work-type buckets", "In model", "Scenario menu, not capture share or SOM"],
    ["Basic Construction", "P-5c construction-contract denominator (GFE-free)", "In model", "Not total ship cost"],
    ["GFE and GFP", "Government-furnished equipment and property", "Excluded", "Do not add to component TAM"],
    ["SIB", "Submarine industrial base capacity grants and workforce funding", "Excluded", "Context only; not current component delivery"],
    ["AP and LLTM", "Advance procurement and long-lead-time material reference stream", "Reference", "Additive base = $0; already inside Basic Construction"],
    ["FFATA and FSRS", "First-tier subaward visibility under FAR 52.204-10", "Evidence", "Named-vendor floor, not the full supplier layer"],
    ["POP", "Place-of-performance evidence", "Evidence", "Drives the supplier coefficient"],
]


def _body() -> str:
    out = []
    out.append(_note(10, "Setup", BODY_X, BODY_Y, BODY_CX, 260_000,
        "Scope anchor: these definitions mirror the model's Methodology boundary; they are an interpretation aid, not a new boundary.",
        size=DENSE_BODY_10PT, bold_lead="Scope anchor:", italic=False, align="l"))
    table_y = BODY_Y + 340_000
    guard_y = BODY_B - 530_000
    col_w = _widths(BODY_CX, [1.2, 2.6, 1.4, 2.7])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=274_320)
    fills = {(1,0): BLUE_1, (2,0): BLUE_1, (3,0): BLUE_1, (4,0): GRAY_2, (5,0): GRAY_2, (6,0): GRAY_1, (7,0): GRAY_1, (8,0): GRAY_1}
    bold = {(r,0): True for r in range(1,9)}
    out.append(house_table(20, "GlossaryMatrix", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="dark", size=900,
                           aligns=["l", "l", "l", "l"], cell_fills=fills, cell_bold=bold))
    out.append(text_box(30, "Guardrail", BODY_X, guard_y, BODY_CX, 460_000,
        [paragraph([run("NO SOM IS MODELED. ", size=CAP_12PT, bold=True, color=DK, font=FONT),
                    run("SAM is a scenario menu, not capture share or revenue forecast. AP and LLTM additive base = $0.", size=MESSAGE_11PT, color=DK, font=FONT)], align="ctr")],
        fill=GRAY_2, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    return "".join(out)
