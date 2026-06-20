"""topdown_detail - top-down budget-anchored MRO composition (v3.3 slide 8).

The left-side stacked bar is a NATIVE column_chart (single stacked column, six
budget-source segments shown as % share) styled to the think-cell look; it
replaces the earlier static-shape transcription of the source exhibit (same
conversion done for slide 6 / ``work_segments.py``). The right-side rollup table
stays transcribed VERBATIM from the v3.3 slide:
  * ``_chart_xml/slide08_table.xml`` - the native <a:tbl> (exact source row
    heights / insets / per-cell borders + the grey bg1-lumMod50 total row); its
    custom tableStyleId is swapped for the built-in no-grid style and the dsbld
    cellmeta stripped. It positions itself via its own graphicFrame xfrm.
The chart caption, the column total, the vertical color key, and the footer note
are the rebuilt deck_core primitives.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip,
    run, paragraph, text_box,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    DK, BLACK, FONT, INSETS_NONE, SOURCES_8PT,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
    CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6,
)

LAYOUT = "slideLayout4"

_SECTION = "TAM Sizing"
_TOPIC = "Top-Down Detail"
_TITLE_TOPIC = "Top-Down Composition"
_TAKEAWAY = ("Public Naval Shipyard labor leads the $17.0B budget-anchored MRO at 44%, ahead of "
             "OMN 1B4B private availabilities at 25%.")

_CHART_CAPTION = "FY2025 budget-anchored MRO funding by source ($M)"
_FOOTER = ("Sources: (1) PB26 OMN OP-5; (2) PB26 SCN P-40 LI 2086 and OPN BA-1 P-40 LI 1000; "
           "(3) PB26 USCG Justification; data as of April 2026")

_XML = Path(__file__).parent / "_chart_xml"
# Verbatim native rollup table (positions itself via its own graphicFrame xfrm).
_TABLE = (_XML / "slide08_table.xml").read_text(encoding="utf-8")

# Native stacked-column reproduction of the v3.3 think-cell exhibit. Single fat
# column; the six segments stack bottom->top in pure source accent order (no
# accent swap here, unlike slide 6). Values are the % shares the source labels
# show; the theme accent hexes equal deck_core CHART_ACCENT_*, so the fills are
# pixel-faithful. Segment names populate only the (hidden) embedded data.
_SEG = [  # (series name, fill, % share, force white in-bar label, chip) — bottom->top
    ("Public NSY",          CHART_ACCENT_1, 44, True,  False),
    ("1B4B Private avails", CHART_ACCENT_2, 25, True,  False),
    ("OPN LI 1000",         CHART_ACCENT_3, 14, True,  False),
    ("SCN LI 2086 RCOH",    CHART_ACCENT_4,  9, True,  False),  # accent4 (borderline-bright -> force white)
    ("MSC M&R",             CHART_ACCENT_5,  7, False, False),  # accent5 light -> auto-black label
    ("USCG ISVS",           CHART_ACCENT_6,  1, False, True),   # 1% sliver too thin for an in-bar label:
                                                               # native label suppressed, overlaid as a chip
]
_CHART = column_chart(
    mode="stacked",
    categories=["Total FY2025"],
    series=[{"name": n, "values": [p], "color": c,
             **({"label_color": "FFFFFF"} if w else {}),
             **({"hide_labels": True} if chip else {})}
            for (n, c, p, w, chip) in _SEG],
    value_axis_format='0"%"', value_label_format='0"%"',
    value_axis_min=0, value_axis_max=100, value_axis_major_unit=5,
    seg_line_color="FFFFFF", seg_line_width=9525, axis_line_color="162029",
    show_gridlines=False, show_legend=False,
    value_label_size_pt=8, cat_label_size_pt=8,
    gap_width=0, cat_header="Budget source",
    # Inner plot pinned to the source bar/axis rectangle within the graphic_frame
    # below (all four edges land on the transcribed exhibit's bar/axis lines).
    plot_layout={"x": 0.0833, "y": 0.0187, "w": 0.9155, "h": 0.9441},
)
CHARTS: list[dict] = [_CHART]

# Vertical color key, transcribed from the source exhibit (the native chart has no
# legend). Each entry: (fill, label, swatch_y, label_y); swatch x=4540250, label
# x=4733925. Order top->bottom mirrors the source (USCG ISVS -> Public NSY).
_LEG = [
    (CHART_ACCENT_6, "USCG ISVS",          1747838, 1743075),
    (CHART_ACCENT_5, "MSC M&R",            1920875, 1916113),
    (CHART_ACCENT_4, "SCN LI 2086 RCOH",   2093913, 2089150),
    (CHART_ACCENT_3, "OPN LI 1000",        2266950, 2262188),
    (CHART_ACCENT_2, "1B4B Private avails", 2439988, 2435225),
    (CHART_ACCENT_1, "Public NSY",         2613025, 2608263),
]


def _legend() -> str:
    parts = []
    sid = 110
    for fillc, label, sy, ly in _LEG:
        parts.append(text_box(
            sid, "LegendSwatch", 4540250, sy, 142875, 106362, [paragraph([])],
            fill=fillc, line_color="FFFFFF", line_width=9525, insets=INSETS_NONE))
        parts.append(text_box(
            sid + 1, "LegendLabel", 4733925, ly, 1750000, 122238,
            [paragraph([run(label, size=SOURCES_8PT, color=BLACK, font=FONT)], align="l")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        sid += 2
    return "".join(parts)


def _body() -> str:
    caption = text_box(
        100, "ChartCaption", 403013, 1298363, 3622253, 275434,
        [paragraph([run(_CHART_CAPTION, size=SOURCES_8PT, italic=True, color=BLACK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
    footer = text_box(
        101, "FooterNote", 457200, 6037783, 11308384, 502920,
        [paragraph([run(_FOOTER, size=SOURCES_8PT, color=DK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
    # Native chart placed in the static exhibit's footprint (rId2 = this slide's
    # first chart). The catAx renders the "Total FY2025" category label; only the
    # column total can't be a native stacked-chart element, so keep it as overlay.
    chart = graphic_frame(
        sp_id=102, name="TopDownStackedColumn",
        x=465138, y=1660000, cx=3946525, cy=4180000, rId="rId2",
    )
    total = text_box(
        103, "ChartTotal", 2359025, 1574800, 484188, 122238,
        [paragraph([run("$16,996M", size=SOURCES_8PT, color=BLACK, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE,
    )
    # The 1% USCG ISVS sliver (accent6) is too thin for an in-bar label, so the
    # source bumps "1%" above the bar on a chip filled with the segment's own
    # accent6 (keeps it legible / tied to its color). Its native label is hidden
    # (hide_labels above); this overlay reproduces the chip at the source x/y.
    chip = text_box(
        104, "OnePctChip", 2513013, 1697038, 176213, 122238,
        [paragraph([run("1%", size=SOURCES_8PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
        fill=CHART_ACCENT_6, line_color="none", anchor="ctr", insets=INSETS_NONE,
    )
    return caption + _TABLE + footer + chart + total + chip + _legend()


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
    )
