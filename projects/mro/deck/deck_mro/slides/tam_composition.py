"""tam_composition - work-segment x vessel-type composition (v3.3 slide 7).

The work-segment x vessel-type Marimekko is a NATIVE chart (variable-width
percent-stacked columns, column width proportional to FY2025 $M) styled to the
think-cell look; it replaces the earlier static-shape transcription.

Unlike the simpler fleet_mro marimekko (slide 13), the source here SORTS each
column's segments by size (largest at the bottom), so the columns do NOT share a
single segment order — a by-segment native stack (one series per segment) can't
reproduce that. So this is built as POSITIONAL series instead: one series per
stack *layer* (bottom band, 2nd band, ...), with each bin colored individually via
data_point_colors. Layer 1 sits at the bottom of every column, but carries each
column's own bottom segment + color, so every column keeps its exact source
order while the chart stays native and Edit-Data-backed.

The chart is rendered SEAMLESS (no per-bin borders) with the white column/segment
dividers overlaid (computed from the same plot rect). Everything else from the
source exhibit — the legend, the $M / vessel-type headers, the in-cell %s, the
tiny-segment leader chips, and the "Segment composition by hull" rail title — is
kept verbatim from _chart_xml/slide07.xml (the colored cells and the source's own
value axis are filtered; the native chart draws those). The chart caption, the
right-side six-segment commentary rail, and the footer note are deck_core
primitives (they were never part of the extracted exhibit).
"""
from __future__ import annotations

import re
from pathlib import Path

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip,
    run, paragraph, text_box,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    DK, FONT, INSETS_NONE, FINEPRINT_8_5PT, DENSE_BODY_10PT, SOURCES_8PT,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
    CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6,
)

LAYOUT = "slideLayout4"

_SECTION = "TAM"
_TOPIC = "Composition"
_TITLE_TOPIC = "TAM Composition"
_TAKEAWAY = ("Depot ship repair and nuclear and complex overhauls drove ~74% of MRO TAM, led by "
             "DDG and SSN/CVN work.")

_CHART_CAPTION = "FY2025 reconciled FPDS-visible MRO TAM by work segment and vessel type ($M)"
_COMMENTARY = [
    ("Depot work concentrates in DDG and amphibious hulls.",
     "DDG 25% ($1.2B) and LPD 13% ($613M) lead; T-AO, CVN, LSD, and LCS each 6%–7%."),
    ("Nuclear and complex overhauls are submarine-led.",
     "SSN 66% ($1,255M) and CVN 18% ($337M) drive the segment; refueling overhauls at GDEB, "
     "CVN RCOH at HII Newport News."),
    ("HM&E spreads thinly across surface hulls.",
     "DDG 6%; LCS, LPD, T-AO, and CVN at 2%–3% each."),
    ("Combat systems sustainment is SSBN-dominated.",
     "SSBN 55% ($319M); Trident II and VLS sustainment on Ohio-class SSBNs."),
    ("Port and technical work tracks logistics and carrier hulls.",
     "T-AO, DDG, T-AKE, and CVN each 8%–10%; ESB 4%."),
    ("Electronics and C4ISR work is SSBN-led.",
     "SSBN 13% ($42M) Trident II support; CVN, SSN, and DDG trace."),
]
_FOOTER = ("Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; data as "
           "of April 2026")

# ── Marimekko data, transcribed from the source cells. Per column the stack is
# listed BOTTOM->TOP in the source's own (size-sorted) order, each entry an
# (accent-index, cell-height-EMU) pair so proportions reproduce the exhibit
# exactly. Accent index -> segment (from the legend): 1 Depot / 2 Nuclear &
# Complex / 3 HM&E / 4 Combat / 5 Electronics / 6 Port & Technical. ─────────────
_ACCENTS = [CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
            CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6]
_STACKS: dict[str, list[tuple[int, int]]] = {
    "Surface Combatants":       [(1, 2871788), (3, 192088), (4, 192088), (2, 190500), (6, 138113)],
    "Amphibious Warfare Ships": [(1, 3346450), (3, 192088), (6, 46038)],
    "Submarines":               [(2, 2149475), (4, 762000), (3, 319088), (5, 276225), (1, 71438), (6, 6350)],
    "Combat Logistics Ships":   [(1, 2986088), (6, 409575), (3, 188913)],
    "Aircraft Carriers":        [(1, 1720850), (2, 1592263), (6, 160338), (3, 95250), (5, 15875)],
    "Other":                    [(1, 1277938), (3, 1060450), (6, 430213), (2, 415925), (5, 358775), (4, 41275)],
}
_COLUMNS = list(_STACKS)                                  # left -> right
_WIDTHS = {  # EMU, ∝ FY2025 $M (≈790 EMU/$M: 2239/1441/2093/769/759/1667)
    "Surface Combatants": 1768475, "Amphibious Warfare Ships": 1138238, "Submarines": 1652588,
    "Combat Logistics Ships": 608013, "Aircraft Carriers": 600075, "Other": 1316038,
}
_TOTAL_BINS = 200


def _alloc_bins(widths: list[int], total: int) -> list[int]:
    """Largest-remainder split of `total` bins ∝ widths (mirrors
    deck_core.charts._allocate_bins; each column gets at least one bin)."""
    s = sum(widths)
    raw = [w / s * total for w in widths]
    bins = [max(1, int(x)) for x in raw]
    while sum(bins) > total:
        i = max(range(len(bins)), key=lambda j: bins[j] - raw[j])
        if bins[i] > 1:
            bins[i] -= 1
        else:
            break
    while sum(bins) < total:
        i = max(range(len(bins)), key=lambda j: raw[j] - bins[j])
        bins[i] += 1
    return bins


_BINS = _alloc_bins([_WIDTHS[c] for c in _COLUMNS], _TOTAL_BINS)
_NPOS = max(len(s) for s in _STACKS.values())            # 6 stack layers

# Positional series: layer k is the k-th segment from the bottom of whichever
# column a bin belongs to. data_point_colors paints each bin with that segment's
# accent, so each column keeps its own source order. Empty top layers -> 0 height.
_pos_vals: list[list[int]] = [[] for _ in range(_NPOS)]
_pos_cols: list[list[str]] = [[] for _ in range(_NPOS)]
for _col, _nb in zip(_COLUMNS, _BINS):
    _stack = _STACKS[_col]
    for _ in range(_nb):
        for _k in range(_NPOS):
            if _k < len(_stack):
                _pos_vals[_k].append(_stack[_k][1])
                _pos_cols[_k].append(_ACCENTS[_stack[_k][0] - 1])
            else:
                _pos_vals[_k].append(0)
                _pos_cols[_k].append("FFFFFF")
_SERIES = [{"name": f"Layer {k + 1}", "values": _pos_vals[k], "data_point_colors": _pos_cols[k]}
           for k in range(_NPOS)]

# Graphic-frame + inner-plot pin. Plot rect lands on the source bar region:
# x 873125..7956551, y(100%) 2047875 .. y(0%) 5632451.
_FRAME = {"x": 430000, "y": 1860000, "cx": 7740000, "cy": 3900000}
_PL = {"x": 0.057251, "y": 0.048173, "w": 0.915171, "h": 0.919122}
_PX0 = _FRAME["x"] + _PL["x"] * _FRAME["cx"]
_PX1 = _FRAME["x"] + (_PL["x"] + _PL["w"]) * _FRAME["cx"]
_PY0 = _FRAME["y"] + _PL["y"] * _FRAME["cy"]
_PY1 = _FRAME["y"] + (_PL["y"] + _PL["h"]) * _FRAME["cy"]
_PW, _PH = _PX1 - _PX0, _PY1 - _PY0

_CHART = column_chart(
    mode="percent",
    categories=[""] * _TOTAL_BINS,
    series=_SERIES,
    value_axis_format="0%",
    value_axis_min=0, value_axis_max=1, value_axis_major_unit=0.05,
    seg_line_color=None, axis_line_color="162029",
    show_gridlines=False, show_legend=False, show_value_labels=False,
    show_cat_labels=False, gap_width=0, cat_header="Mekko bin",
    plot_layout=_PL,
)
CHARTS: list[dict] = [_CHART]

_DIV_W = 9525  # 0.75pt white divider, matching the source cell borders


def _xfracs() -> list[tuple[float, float]]:
    """(x0_frac, x1_frac) per column from the bin allocation."""
    out, cum = [], 0
    for nb in _BINS:
        out.append((cum / _TOTAL_BINS, (cum + nb) / _TOTAL_BINS))
        cum += nb
    return out


def _dividers() -> str:
    """White column + segment dividers (the seamless chart draws none)."""
    parts, sid = [], 60
    spans = _xfracs()
    for i in range(len(_COLUMNS) - 1):                     # vertical, between columns
        x = _PX0 + spans[i][1] * _PW
        parts.append(text_box(
            sid, "VDiv", round(x - _DIV_W / 2), round(_PY0), _DIV_W, round(_PH),
            [paragraph([])], fill="FFFFFF", line_color="none", insets=INSETS_NONE))
        sid += 1
    for col, (x0f, x1f) in zip(_COLUMNS, spans):           # horizontal, between segments
        x0 = round(_PX0 + x0f * _PW)
        x1 = round(_PX0 + x1f * _PW)
        stack = _STACKS[col]
        tot = sum(h for _, h in stack)
        cum = 0
        for k in range(len(stack) - 1):
            cum += stack[k][1]
            y = _PY1 - (cum / tot) * _PH
            parts.append(text_box(
                sid, "HDiv", x0, round(y - _DIV_W / 2), x1 - x0, _DIV_W,
                [paragraph([])], fill="FFFFFF", line_color="none", insets=INSETS_NONE))
            sid += 1
    return "".join(parts)


# ── Source overlay: keep every shape EXCEPT the colored marimekko cells and the
# source's own value axis (the 0..100% labels + tick/spine connectors) — the
# native chart draws those. Everything else (legend, $M + vessel headers, in-cell
# %s, leader chips, rail title) is reproduced verbatim. ─────────────────────────
_COL_X = {"873125", "2641600", "3779838", "5432425", "6040438", "6640513"}
_AXIS_CXN_X = {"839788", "868363", "873125"}


def _overlay() -> str:
    xml = (Path(__file__).parent / "_chart_xml" / "slide07.xml").read_text(encoding="utf-8")
    shapes = re.findall(r'<p:sp>.*?</p:sp>|<p:cxnSp>.*?</p:cxnSp>', xml, re.S)
    kept = []
    for sp in shapes:
        m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', sp)
        x = m.group(1) if m else None
        is_cell = x in _COL_X and 'schemeClr val="accent' in sp
        is_axis_label = bool(re.search(r'<a:t>\d+%</a:t>', sp)) and x is not None and int(x) < 900000
        is_axis_line = sp.startswith("<p:cxnSp") and x in _AXIS_CXN_X
        if is_cell or is_axis_label or is_axis_line:
            continue
        kept.append(sp)
    return "".join(kept)


def _body() -> str:
    caption = text_box(
        10, "ChartCaption", 511175, 1585116, 4000000, 240000,
        [paragraph([run(_CHART_CAPTION, size=FINEPRINT_8_5PT, italic=True, color=DK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
    paras = []
    for i, (label, text) in enumerate(_COMMENTARY):
        paras.append(paragraph([run(label, size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT)],
                               space_after=20))
        paras.append(paragraph([run(text, size=DENSE_BODY_10PT, color=DK, font=FONT)],
                               space_after=0 if i == len(_COMMENTARY) - 1 else 110))
    rail = text_box(
        20, "SegmentCommentary", 8145755, 2044628, 3535070, 3477875, paras,
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
    footer = text_box(
        30, "FooterNote", 457200, 6008287, 11308384, 502920,
        [paragraph([run(_FOOTER, size=SOURCES_8PT, color=DK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
    chart = graphic_frame(
        sp_id=40, name="TamCompositionMarimekko",
        x=_FRAME["x"], y=_FRAME["y"], cx=_FRAME["cx"], cy=_FRAME["cy"], rId="rId2",
    )
    return caption + rail + footer + chart + _dividers() + _overlay()


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
    )
