"""fleet_mro - Marauder-like fleet MRO composition (v3.3 slide 13).

The work-segment x hull Marimekko is a NATIVE marimekko_chart (variable-width
percent-stacked columns, hull width proportional to FY2025 $M) styled to the
think-cell look; it replaces the earlier static-shape transcription. Everything
else from the source exhibit — the legend, the $M / hull column headers, the
in-cell % labels, the right-side commentary callouts, the axis title and footer —
is kept verbatim from _chart_xml/slide13.xml (the colored cells and the source's
own value axis are filtered out; the native chart draws those). The analyst
"DISCUSS" review-sticky stays dropped per the locked content decisions.
"""
from __future__ import annotations

import re
from pathlib import Path

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, text_box, paragraph,
)
from deck_core.charts import marimekko_chart, graphic_frame
from deck_core.style import CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3, INSETS_NONE

LAYOUT = "slideLayout4"

_SECTION = "SAM"
_TOPIC = "Marauder-Like Fleet MRO"
_TAKEAWAY = ("Marauder-comparable fleet MRO totals $758M, with 82% concentrated in depot ship "
             "repair.")

# ── Marimekko data, transcribed from the source cells (values + widths in EMU so
# proportions/widths reproduce the exhibit exactly). Segments bottom->top:
# Depot (accent1) / Port & Technical (accent3) / HM&E (accent2). ───────────────
_COLUMNS = ["T-AO", "T-AKE", "ESB", "T-EPF", "WPC"]
_SEGMENTS = ["Depot Ship Repair", "Port & Technical Services",
             "Hull, Mechanical & Electrical (HM&E)"]
_COLORS = {
    "Depot Ship Repair":                    CHART_ACCENT_1,
    "Port & Technical Services":            CHART_ACCENT_3,
    "Hull, Mechanical & Electrical (HM&E)": CHART_ACCENT_2,
}
_VALUES = {  # per hull: {segment: cell height in EMU} -> exact source proportions
    "T-AO":  {"Depot Ship Repair": 3003550, "Port & Technical Services": 381000,
              "Hull, Mechanical & Electrical (HM&E)": 190500},
    "T-AKE": {"Depot Ship Repair": 2901950, "Port & Technical Services": 606425,
              "Hull, Mechanical & Electrical (HM&E)": 66675},
    "ESB":   {"Depot Ship Repair": 2463800, "Port & Technical Services": 1111250,
              "Hull, Mechanical & Electrical (HM&E)": 0},
    "T-EPF": {"Depot Ship Repair": 2960688, "Port & Technical Services": 503238,
              "Hull, Mechanical & Electrical (HM&E)": 111125},
    "WPC":   {"Depot Ship Repair": 3451225, "Port & Technical Services": 57150,
              "Hull, Mechanical & Electrical (HM&E)": 66675},
}
_WIDTHS = {"T-AO": 3621088, "T-AKE": 1960563, "ESB": 569913,
           "T-EPF": 554038, "WPC": 328613}  # ∝ FY2025 $M (384/208/60/59/35)

# Graphic-frame + inner-plot pin (plot_layout). The marimekko's thin bins would
# show per-bin pinstripes if bordered, so the chart is rendered SEAMLESS
# (seg_line_color=None) and the white column/segment dividers are overlaid below,
# computed from the same plot rect + label_meta so they land on the bin/segment
# boundaries exactly.
_FRAME = {"x": 440000, "y": 1850000, "cx": 7460000, "cy": 3700000}
_PL = {"x": 0.0502, "y": 0.0153, "w": 0.9429, "h": 0.9662}
_PX0 = _FRAME["x"] + _PL["x"] * _FRAME["cx"]
_PX1 = _FRAME["x"] + (_PL["x"] + _PL["w"]) * _FRAME["cx"]
_PY0 = _FRAME["y"] + _PL["y"] * _FRAME["cy"]
_PY1 = _FRAME["y"] + (_PL["y"] + _PL["h"]) * _FRAME["cy"]
_PW, _PH = _PX1 - _PX0, _PY1 - _PY0

_CHART, _LABEL_META = marimekko_chart(
    columns=_COLUMNS, segments=_SEGMENTS, values=_VALUES,
    column_widths=_WIDTHS, colors=_COLORS, total_bins=200,
    show_legend=False,
    seg_line_color=None, axis_line_color="162029",
    value_axis_min=0, value_axis_max=1, value_axis_major_unit=0.05,
    plot_layout=_PL,
)
CHARTS: list[dict] = [_CHART]

_DIV_W = 9525  # 0.75pt white divider, matching the source cell borders


def _dividers() -> str:
    """White column + segment dividers (the seamless chart draws none)."""
    parts, sid = [], 60
    for i in range(len(_COLUMNS) - 1):                     # vertical, between columns
        x = _PX0 + _LABEL_META[i]["x1_frac"] * _PW
        parts.append(text_box(
            sid, "VDiv", round(x - _DIV_W / 2), round(_PY0), _DIV_W, round(_PH),
            [paragraph([])], fill="FFFFFF", line_color="none", insets=INSETS_NONE))
        sid += 1
    for i, col in enumerate(_COLUMNS):                     # horizontal, between segments
        x0 = round(_PX0 + _LABEL_META[i]["x0_frac"] * _PW)
        x1 = round(_PX0 + _LABEL_META[i]["x1_frac"] * _PW)
        vals = [_VALUES[col][s] for s in _SEGMENTS]
        tot = sum(vals)
        if tot <= 0:
            continue
        cum = 0
        for j in range(len(vals) - 1):
            cum += vals[j]
            if vals[j] > 0 and vals[j + 1] > 0:           # skip boundaries by a zero segment
                y = _PY1 - (cum / tot) * _PH
                parts.append(text_box(
                    sid, "HDiv", x0, round(y - _DIV_W / 2), x1 - x0, _DIV_W,
                    [paragraph([])], fill="FFFFFF", line_color="none", insets=INSETS_NONE))
                sid += 1
    return "".join(parts)

# ── Source overlay: keep every shape EXCEPT the colored marimekko cells and the
# source's own value axis (labels + tick/spine connectors) — the native chart
# draws those. Everything else (legend, headers, in-cell %s, callouts, footer,
# axis title, tiny-segment leader chips) is reproduced verbatim. ───────────────
_COL_X = {"814387", "4435475", "6396038", "6965950", "7519988"}
_AXIS_CXN_X = {"781050", "809626", "814387", "814388"}


def _overlay() -> str:
    xml = (Path(__file__).parent / "_chart_xml" / "slide13.xml").read_text(encoding="utf-8")
    # Bottom band carries sources only: collapse the column-blank caveat footer to the source line.
    xml = xml.replace(
        '<a:r><a:rPr sz="800" b="0" i="0" dirty="0"><a:solidFill><a:srgbClr val="162029"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>Note: Nuclear &amp; Complex Overhauls column is blank because embedded MRO covers only CVN, SSN, SSBN, and surface-combatant programs</a:t></a:r><a:r><a:rPr lang="en-US" sz="800" b="0" i="0" dirty="0"><a:solidFill><a:srgbClr val="162029"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>,</a:t></a:r><a:r><a:rPr sz="800" b="0" i="0" dirty="0"><a:solidFill><a:srgbClr val="162029"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t> not MSC auxiliaries or USCG cutters. Source: FPDS FY2025 contract obligations. Data as of April 2026.</a:t></a:r>',
        '<a:r><a:rPr sz="800" b="0" i="0" dirty="0"><a:solidFill><a:srgbClr val="162029"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>Sources: (1) FPDS FY2025 contract obligations; data as of April 2026</a:t></a:r>',
    )
    xml = xml.replace("J998 / J999", "J998/J999")
    shapes = re.findall(r'<p:sp>.*?</p:sp>|<p:cxnSp>.*?</p:cxnSp>', xml, re.S)
    kept = []
    for sp in shapes:
        m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', sp)
        x = m.group(1) if m else None
        is_cell = x in _COL_X and 'schemeClr val="accent' in sp
        is_axis_label = bool(re.search(r'<a:t>\d+%</a:t>', sp)) and x is not None and int(x) < 700000
        is_axis_line = sp.startswith("<p:cxnSp") and x in _AXIS_CXN_X
        if is_cell or is_axis_label or is_axis_line:
            continue
        kept.append(sp)
    return "".join(kept)


def _body() -> str:
    chart = graphic_frame(
        sp_id=40, name="FleetMroMarimekko",
        x=_FRAME["x"], y=_FRAME["y"], cx=_FRAME["cx"], cy=_FRAME["cy"], rId="rId2",
    )
    return chart + _dividers() + _overlay()


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
    )
