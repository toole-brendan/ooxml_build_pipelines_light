"""MYP redaction - native-chart correction exhibit for reconstructed FY23-27 multiyear masters.

The left-side data is carried by two native, editable PowerPoint charts rather
than hand-built shapes: a one-row 100% stacked place-of-performance strip
(rId2) and a two-row outside-yards comparison "progress bar" (rId3). The two
evidence chips stay as shapes because they are semantic evidence, not plotted
data, and the right rail is no-fill interpretive commentary.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_5,
    BLACK, FONT,
    INSETS_NONE, INSETS_BADGE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
    CHART_TITLE_10PT, MESSAGE_11PT, VALUE_14PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Denominator Correction"
_TAKEAWAY = "Restoring the redacted multiyear masters corrects the outside-yards artifact to ~33%"
_SOURCES = "Sources: DoW contract announcements, Aug. 1, Aug. 11, and Sept. 6, 2023; USNI News, Navy Reveals Contract Costs of Latest 10-Hull Destroyer Deal, Sept. 6, 2023; NAVSEA, Navy Awards DDG 51 FY23-27 Multiyear Procurement Contracts, Aug. 1, 2023"


# ── Native charts ────────────────────────────────────────────────────────────
# Two editable charts replace the former shape-built strip + comparison bars.
# CHARTS order maps to slide rels: rId2 = distribution, rId3 = comparison.
# Values are decimals because the label/axis format is a "0.0%" / "0%" percent
# code (the percent factory normalizes the stack to 100%).

# Distribution: one 100% stacked column (place-of-performance mix).
# SRT bar palette (docs/chart_conversion_spec.md): the Other-US supplier share
# (the supplier-addressable slice) is hero navy; yard sites and unparsed are grays.
_DISTRIBUTION_CHART = column_chart(
    mode="percent",
    categories=[""],
    series=[
        {"name": "BIW site",          "values": [0.290], "color": "A1A1A1"},
        {"name": "Ingalls site",      "values": [0.336], "color": "BEBEBE"},
        {"name": "Other-US supplier", "values": [0.315], "color": "1D4D68"},
        {"name": "Foreign",           "values": [0.013], "color": "89A2B0", "hide_labels": True},
        {"name": "Unparsed",          "values": [0.045], "color": "DBDBDB", "hide_labels": True},
    ],
    title=None,
    show_legend=True,
    legend_pos="b",
    value_axis_format="0%",
    show_gridlines=False,
    show_value_labels=True,
    value_label_format="0.0%",
    value_label_size_pt=8,
    cat_label_size_pt=8,
    gap_width=25,
    cat_header="Place of performance",
)

# Comparison: two stacked columns ("progress bar"). The visible series is the
# outside-yards share; a hidden no-fill remainder scales each column to 100%.
# SRT bar palette: corrected view hero navy, disclosed artifact gray.
_COMPARISON_CHART = column_chart(
    mode="stacked",
    categories=[
        "MYP-corrected",
        "Disclosed artifact",
    ],
    series=[
        {
            "name": "Outside-yards share",
            "values": [0.328, 0.736],
            "data_point_colors": ["1D4D68", "A1A1A1"],
        },
        {
            "name": "Remainder",
            "values": [0.672, 0.264],
            "no_fill": True,
            "hide_labels": True,
        },
    ],
    title=None,
    show_legend=False,
    value_axis_format="0%",
    show_gridlines=False,
    show_value_labels=True,
    value_label_format="0.0%",
    value_label_size_pt=11,
    cat_label_size_pt=9,
    gap_width=80,
    cat_header="View",
)

CHARTS: list[dict] = [_DISTRIBUTION_CHART, _COMPARISON_CHART]


def _exhibit_title(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ExhibitTitle", x, y, cx, 150_000,
        [paragraph([run("MYP-corrected place-of-performance distribution", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )


def _data_badge(sp_id: int, x: int, y: int, cx: int, label: str, value: str, *, fill: str) -> str:
    return text_box(
        sp_id, "EvidenceBadge", x, y, cx, 620_000,
        [
            paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=55),
            paragraph([run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=fill, anchor="ctr", insets=INSETS_BADGE,
    )


def _explanation_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Master awards:", "FY23-27 BIW and Ingalls MYP masters disclose work locations but not dollar values."),
        ("Artifact:", "omitting large yard-heavy master dollars over-weights disclosed GFE actions."),
        ("Correction:", "restore ~$14.58B of master value before applying the Basic Construction supplier coefficient."),
        ("Carry-forward:", "use the corrected ~33% outside-yards view going forward."),
    ]
    paras = [
        paragraph(
            [run("What Changed", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
            space_after=150,
        )
    ]
    for i, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120 if i < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id, "ExplanationRail", x, y, cx, cy,
        paras, fill=None, line_color=None, anchor="ctr", insets=(70_000, 20_000, 30_000, 20_000),
    )


def _body() -> str:
    main_x = BODY_X + 20_000
    main_w = 7_250_000

    rail_x = BODY_X + 7_720_000
    rail_w = BODY_R - rail_x

    title_y = BODY_Y + 50_000
    dist_y = BODY_Y + 300_000
    dist_h = 1_040_000

    comp_y = BODY_Y + 1_560_000
    comp_h = 1_390_000

    badge_gap = 150_000
    badge_y = BODY_Y + 3_240_000
    badge_w = (main_w - badge_gap) // 2

    left_top = title_y
    left_bottom = badge_y + 620_000
    rail_y = left_top
    rail_h = left_bottom - left_top

    return (
        _exhibit_title(10, main_x, title_y, main_w)
        + graphic_frame(
            sp_id=20,
            name="DistributionChart",
            x=main_x,
            y=dist_y,
            cx=main_w,
            cy=dist_h,
            rId="rId2",
        )
        + graphic_frame(
            sp_id=40,
            name="OutsideYardsComparisonChart",
            x=main_x,
            y=comp_y,
            cx=main_w,
            cy=comp_h,
            rId="rId3",
        )
        + _data_badge(50, main_x, badge_y, badge_w, "Reconstructed masters", "~$14.58B", fill=BLUE_1)
        + _data_badge(51, main_x + badge_w + badge_gap, badge_y, badge_w, "Gated corpus incl. masters", "~$21.71B", fill=GRAY_1)
        + _explanation_rail(60, rail_x, rail_y, rail_w, rail_h)
    )


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("MYP Redaction", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
