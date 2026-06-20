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
_TOPIC = "Top visible suppliers"
_TAKEAWAY = "The extended FFATA-visible list is a named-vendor floor, not the full supplier layer"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

_ROWS = [
    ["Rank", "Supplier (parent legal entity)", "$M", "Rank", "Supplier (parent legal entity)", "$M"],
    ["1", "Northrop Grumman Corporation", "1,426.6", "14", "W International SC, LLC", "74.1"],
    ["2", "Leonardo SpA", "490.6", "15", "Oil States International, Inc.", "71.5"],
    ["3", "Curtiss-Wright Electro-Mechanical Corp.", "198.0", "16", "Precision Custom Components, LLC", "68.8"],
    ["4", "Scot Forge Company", "197.5", "17", "Goodrich Corp. (RTX Collins Aerospace)", "64.9"],
    ["5", "ESCO Technologies Inc.", "188.5", "18", "Johnson Controls Navy Systems, LLC", "58.7"],
    ["6", "DC Fabricators Inc.", "162.9", "19", "Globe Composite Solutions, LLC", "57.3"],
    ["7", "Rhoads Metal Fabrications, Inc.", "141.9", "20", "CIRCOR International, Inc.", "53.0"],
    ["8", "Curtiss-Wright Corporation", "110.8", "21", "L3Harris Technologies, Inc.", "52.3"],
    ["9", "The Graham Corporation", "89.1", "22", "BWX Technologies, Inc.", "51.8"],
    ["10", "Austal USA, LLC", "87.6", "23", "Advance Mfg. Co., Inc.", "51.2"],
    ["11", "Rosyth Royal Dockyard Ltd. (Babcock)", "84.0", "24", "Pegasus Steel, LLC", "48.9"],
    ["12", "W International, LLC", "82.6", "25", "Portland Valve LLC", "48.1"],
    ["13", "Curtiss-Wright Flow Control Corp.", "74.7", "", "", ""],
]


def _evidence_chip(sp_id, x, y, w, value, qualifier):
    return text_box(sp_id, "EvidenceChip", x, y, w, 380_000,
        [_txt(value, size=VALUE_14PT, bold=True, color=DK, align="ctr"),
         _txt(qualifier, size=FINEPRINT_8_5PT, color=DK, align="ctr")],
        fill=BLUE_1, line_color=GRAY_3, insets=INSETS_EVIDENCE, anchor="ctr")


def _body() -> str:
    out = []
    chip_y = BODY_Y
    out.append(_evidence_chip(10, BODY_X, chip_y, int(BODY_CX*0.26), "150", "classified subaward recipients"))
    out.append(_evidence_chip(11, BODY_X+int(BODY_CX*0.26)+GAP, chip_y, int(BODY_CX*0.34), "~$5.46B", "supplier-addressable visible value"))
    out.append(_note(12, "ReadNote", BODY_X+int(BODY_CX*0.60)+2*GAP, chip_y, BODY_R-(BODY_X+int(BODY_CX*0.60)+2*GAP), 380_000,
        "Read: this is a named-vendor evidence ledger; values are visible cumulative filings, not annual market size.",
        size=FINEPRINT_8_5PT, bold_lead="Read:", italic=True, align="l"))
    table_y = BODY_Y + 430_000
    note_y = BODY_B - 210_000
    col_w = _widths(BODY_CX, [0.55, 3.55, 0.75, 0.55, 3.55, 0.75])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=8.5, header_size_pt=8.5, min_row_h=274_320)
    fills = {}; colors = {}; bold = {}
    for c in range(6):
        fills[(0,c)] = BLUE_5; colors[(0,c)] = WHITE; bold[(0,c)] = True
    for r in range(1,6):
        for c in range(3):
            fills[(r,c)] = BLUE_1
    out.append(house_table(20, "Top25Ledger", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="rule", size=850,
                           aligns=["ctr", "l", "r", "ctr", "l", "r"], cell_fills=fills, cell_text_colors=colors, cell_bold=bold))
    out.append(_note(30, "FloorCaveat", BODY_X, note_y, BODY_CX, 200_000,
        "Visible does not mean complete: FFATA names first-tier filings above the $30,000 per-action threshold and should be treated as a floor, not the full supplier layer. Across the fifteen in-scope new-construction PIIDs there are ~759 FFATA-visible parents; the 25 shown are the largest.",
        size=FINEPRINT_8_5PT, italic=True))
    return "".join(out)
