"""Small slide-local helper layer for the generated DDG slide modules.

These helpers compose the uploaded deck_core primitives only; they do not alter
or replace deck_core. They keep the generated modules concise while preserving
native PowerPoint charts/tables and the house chrome/body conventions.
"""
from __future__ import annotations

from typing import Iterable, Sequence

from deck_core.primitives import run, paragraph, text_box, house_table, connector
from deck_core.charts import graphic_frame, bar_chart, column_chart, waterfall_chart
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_CY, BODY_R, BODY_B,
    DK, WHITE, BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5, FONT,
    INSETS_NONE, INSETS_CHIP, INSETS_CARD, INSETS_EVIDENCE,
    INSETS_MESSAGE, INSETS_ANSWER_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CHART_TITLE_10PT,
    MESSAGE_11PT, CAP_12PT, VALUE_14PT, RIBBON_KPI_18PT, ANSWER_KPI_24PT,
    BADGE_16PT,
)
from deck_core.text_metrics import estimate_row_heights

GAP = 91_440
TITLE_H = 180_000
SMALL_TITLE_H = 160_000
NOTE_H = 300_000
TALL_NOTE_H = 430_000
HAIRLINE = 6_350
NORMAL_LINE = 12_700
STRONG_LINE = 19_050

_COLOR_TOKENS = {
    "DK": DK, "WHITE": WHITE, "BLACK": BLACK,
    "BLUE_1": BLUE_1, "BLUE_2": BLUE_2, "BLUE_3": BLUE_3,
    "BLUE_4": BLUE_4, "BLUE_5": BLUE_5,
    "GRAY_1": GRAY_1, "GRAY_2": GRAY_2, "GRAY_3": GRAY_3,
    "GRAY_4": GRAY_4, "GRAY_5": GRAY_5,
}


def C(v):
    """Resolve color-token strings in spec dictionaries to actual hex values."""
    if isinstance(v, str):
        return _COLOR_TOKENS.get(v, v)
    return v


def cell_map(raw: dict | None) -> dict:
    """Convert YAML cell override keys like '(2,3)' into {(2, 3): value}."""
    out = {}
    for k, v in (raw or {}).items():
        if isinstance(k, tuple):
            key = k
        else:
            s = str(k).strip().strip("()").replace(" ", "")
            if not s:
                continue
            a, b = s.split(",")
            key = (int(a), int(b))
        out[key] = C(v)
    return out


def col_widths(total: int, ratios: Sequence[float]) -> list[int]:
    """Integer EMU column widths that sum exactly to total."""
    s = float(sum(ratios))
    vals = [int(total * (float(r) / s)) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


def p(text: str = "", *, size: int = LABEL_9PT, bold: bool = False,
      italic: bool = False, color: str = DK, align: str | None = None,
      space_after: int = 0, bullet: bool = False) -> str:
    return paragraph(
        [run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)],
        align=align, space_after=space_after, bullet=bullet,
    )


def lead_body(lead: str, body: str = "", *, lead_size: int = DENSE_BODY_10PT,
              body_size: int = LABEL_9PT, color: str = DK,
              align: str | None = None, bullet: bool = False,
              space_after: int = 0, italic_body: bool = False) -> str:
    runs = [run(lead, size=lead_size, bold=True, color=color, font=FONT)]
    if body:
        runs.append(run(" " + body, size=body_size, italic=italic_body,
                        color=color, font=FONT))
    return paragraph(runs, align=align, bullet=bullet, space_after=space_after)


def text_lines(text: str, *, first_size: int = LABEL_9PT, body_size: int = FINEPRINT_8_5PT,
               color: str = DK, first_bold: bool = True, align: str = "ctr",
               all_caps_first: bool = False) -> list[str]:
    lines = [ln.strip() for ln in str(text).splitlines() if ln.strip()]
    paras = []
    for i, ln in enumerate(lines):
        if i == 0:
            paras.append(p(ln.upper() if all_caps_first else ln,
                           size=first_size, bold=first_bold, color=color, align=align,
                           space_after=120 if len(lines) > 1 else 0))
        else:
            # Numeric-looking second lines deserve the value scale.
            val = ("$" in ln or "%" in ln or ln.startswith("~"))
            paras.append(p(ln, size=VALUE_14PT if val and i == 1 else body_size,
                           bold=val and i == 1, italic=(not val and i == len(lines)-1),
                           color=color, align=align,
                           space_after=80 if i < len(lines)-1 else 0))
    return paras or [p("")]


def box(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
        paras: list[str] | None = None, *, text: str | None = None,
        fill: str | None = None, line_color: str | None = None,
        line_width: int = NORMAL_LINE, insets=None, anchor: str = "ctr") -> str:
    if paras is None:
        paras = text_lines(text or "", color=(WHITE if fill in (BLUE_3, BLUE_4, BLUE_5, GRAY_5) else DK))
    # Preserve the deck_core house default: a filled semantic box gets a black
    # exterior border unless the caller intentionally passes a secondary border
    # such as GRAY_3. No-fill boxes remain borderless.
    effective_line = BLACK if line_color is None and fill not in (None, "none") else line_color
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill,
                    line_color=effective_line, line_width=line_width,
                    insets=insets if insets is not None else INSETS_CARD,
                    anchor=anchor)


def nofill(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
           paras: list[str] | None = None, *, text: str | None = None,
           size: int = FINEPRINT_8_5PT, align: str = "l",
           anchor: str = "t", insets=INSETS_NONE) -> str:
    if paras is None:
        paras = [p(text or "", size=size, color=DK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None,
                    line_color=None, insets=insets, anchor=anchor)


def exhibit_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return nofill(sp_id, "ExhibitTitle", x, y, cx, TITLE_H,
                  [p(text, size=CHART_TITLE_10PT, italic=True, color=DK, align="l")],
                  anchor="t", insets=INSETS_NONE)


def sizing_note(sp_id: int, text: str, x: int = BODY_X, y: int | None = None,
                cx: int = BODY_CX, cy: int = NOTE_H) -> str:
    return nofill(sp_id, "SizingNote", x, BODY_B - cy if y is None else y, cx, cy,
                  [p(text, size=FINEPRINT_8_5PT, color=DK, align="l")],
                  anchor="t", insets=INSETS_NONE)


def bullet_rail(sp_id: int, x: int, y: int, cx: int, cy: int,
                bullets: Sequence[tuple[str, str] | str], *, title: str | None = None,
                body_size: int = LABEL_9PT, lead_size: int = DENSE_BODY_10PT,
                insets=INSETS_MESSAGE) -> str:
    paras: list[str] = []
    if title:
        paras.append(p(title, size=LABEL_9PT, bold=True, italic=True, color=DK,
                       align="l", space_after=120))
    for i, b in enumerate(bullets):
        if isinstance(b, tuple):
            paras.append(lead_body(b[0], b[1], lead_size=lead_size, body_size=body_size,
                                   bullet=True, space_after=120 if i < len(bullets)-1 else 0))
        else:
            paras.append(p(str(b), size=body_size, color=DK, align="l", bullet=True,
                           space_after=120 if i < len(bullets)-1 else 0))
    return text_box(sp_id, "CommentaryRail", x, y, cx, cy, paras,
                    fill=None, line_color=None, insets=insets, anchor="t")


def kpi_card(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
             cap: str, value: str, qualifier: str, *, fill: str = BLUE_5) -> str:
    paras = [
        p(cap.upper(), size=CAP_12PT, bold=True, color=WHITE, align="ctr", space_after=160),
        p(value, size=ANSWER_KPI_24PT, bold=True, color=WHITE, align="ctr", space_after=80),
        p(qualifier, size=LABEL_9PT, italic=True, color=WHITE, align="ctr"),
    ]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=BLACK,
                    line_width=STRONG_LINE, insets=INSETS_ANSWER_CARD, anchor="ctr")


def support_kpi(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
                cap: str, value: str, qualifier: str = "", *, fill: str = BLUE_1) -> str:
    paras = [p(cap.upper(), size=CAP_12PT, bold=True, color=DK, align="ctr", space_after=120),
             p(value, size=VALUE_14PT, bold=True, color=DK, align="ctr")]
    if qualifier:
        paras.append(p(qualifier, size=FINEPRINT_8_5PT, italic=True, color=DK, align="ctr"))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=BLACK,
                    insets=INSETS_CARD, anchor="ctr")


def chip(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
         cap: str, body: str = "", *, fill: str = BLUE_1, line_color: str = BLACK,
         body_size: int = FINEPRINT_8_5PT, value: str | None = None) -> str:
    text_color = WHITE if fill in (BLUE_3, BLUE_4, BLUE_5, GRAY_5) else DK
    paras = [p(cap.upper(), size=LABEL_9PT, bold=True, color=text_color, align="ctr",
               space_after=80)]
    if value:
        paras.append(p(value, size=VALUE_14PT, bold=True, color=text_color, align="ctr",
                       space_after=40 if body else 0))
    if body:
        paras.append(p(body, size=body_size, color=text_color, align="ctr"))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    insets=INSETS_CHIP, anchor="ctr")


def make_table(sp_id: int, name: str, x: int, y: int, cx: int, table_spec: dict,
               *, size_override: int | None = None, min_row_h: int | None = None) -> tuple[str, int]:
    r = table_spec["render"]
    rows = r["rows"]
    size = size_override if size_override is not None else int(r.get("size", 900))
    ratios = r["column_widths"].get("values", [1] * len(rows[0]))
    cw = col_widths(cx, ratios)
    row_h_kw = r.get("row_h", {}) or {}
    mrh = min_row_h if min_row_h is not None else int(row_h_kw.get("min_row_h", 274_320))
    heights = estimate_row_heights(rows, cw, size_pt=size / 100.0,
                                   header_size_pt=size / 100.0, min_row_h=mrh)
    tbl = house_table(
        sp_id, name, x, y, cw, rows,
        row_h=heights,
        table_skin=r.get("table_skin", "rule"),
        size=size,
        aligns=r.get("aligns"),
        cell_fills=cell_map(r.get("cell_fills")),
        cell_text_colors=cell_map(r.get("cell_text_colors")),
        cell_bold=cell_map(r.get("cell_bold")),
    )
    return tbl, sum(heights)


def chart(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, rId: str) -> str:
    return graphic_frame(sp_id=sp_id, name=name, x=x, y=y, cx=cx, cy=cy, rId=rId)


def hbar(sp_id: int, x: int, y: int, cx: int, cy: int, label: str, value_label: str,
         frac: float, *, fill: str = BLUE_5, bg: str = GRAY_1) -> str:
    """Shape-built horizontal comparison bar with label/value overlay."""
    label_w = min(1_600_000, int(cx * 0.36))
    bar_x = x + label_w + GAP // 2
    bar_w = cx - label_w - GAP // 2
    fill_w = max(60_000, int(bar_w * max(0.0, min(1.0, frac))))
    out = nofill(sp_id, "BarLabel", x, y, label_w, cy,
                 [p(label, size=LABEL_9PT, color=DK, align="l")], anchor="ctr")
    out += text_box(sp_id + 100, "BarBack", bar_x, y + cy // 4, bar_w, cy // 2,
                    [p("")], fill=bg, line_color=BLACK, insets=INSETS_NONE, anchor="ctr")
    out += text_box(sp_id + 200, "BarFill", bar_x, y + cy // 4, fill_w, cy // 2,
                    [p("")], fill=fill, line_color=BLACK, insets=INSETS_NONE, anchor="ctr")
    out += nofill(sp_id + 300, "BarValue", bar_x + bar_w - 850_000, y, 850_000, cy,
                  [p(value_label, size=VALUE_14PT, bold=True, color=DK, align="r")], anchor="ctr")
    return out



def _resolve_colors(obj):
    if isinstance(obj, dict):
        return {k: _resolve_colors(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_colors(v) for v in obj]
    return C(obj)


def build_chart(chart_spec: dict) -> dict:
    """Build a native chart dict from the slide-spec chart block."""
    factory = chart_spec["factory"]
    data = _resolve_colors(chart_spec.get("data", {}))
    params = _resolve_colors(dict(chart_spec.get("params", {}) or {}))
    params.pop("external_title", None)
    if factory == "bar_chart":
        mode = params.pop("mode", "clustered")
        return bar_chart(mode=mode, categories=data["categories"], series=data["series"], **params)
    if factory == "column_chart":
        mode = params.pop("mode", "clustered")
        return column_chart(mode=mode, categories=data["categories"], series=data["series"], **params)
    if factory == "waterfall_chart":
        return waterfall_chart(steps=data["steps"], **params)
    raise ValueError(f"unsupported chart factory: {factory}")
