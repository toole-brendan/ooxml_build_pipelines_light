"""recompete_cadence_supply_chain — Recompete On-Ramps deck, slide 02.

EXHIBIT — "Recompete Cadence -> Supply-Chain Entry": the DDG-51 prime is a
closed two-yard duopoly you can't win (it re-ups to Huntington Ingalls + Bath
Iron Works), but it re-buys on a fixed ~5-year multi-year-procurement (MYP)
cadence, and each block sub-contracts ~$1B+ to a visible first-tier supplier
base. The cadence is the timing engine; the addressable move is to supply the
NEXT block's sourcing wave (FY28-32, due ~2028), positioned years ahead.

COMPOSITION (top -> bottom; the slide reads as a three-beat argument):
  • chrome ............ breadcrumb() + title_placeholder() + prelim_chip()
  • timing engine ..... a section cap + a 4-node cadence ribbon (FY13-17 / FY18-22
                        / FY23-27 / FY28-32), each node a cap+body card carrying
                        the award year, the block's first-tier subaward $, and its
                        supplier count; right-arrow connectors form the spine, and
                        the FY28-32 "next wave" node is focal (draft-yellow, 1.5pt
                        border). A one-line cadence caption sits under the ribbon.
  • WHERE to enter .... lower-left house table() — reported $, supplier HHI, and a
                        plain-English read per ship system; the Auxiliary "open
                        lane" row is highlighted.
  • WHEN to enter ..... lower-right native column_chart() (CHARTS[0], rId2) of the
                        cumulative first-tier-subaward-$ share by years after the
                        prime award (front-loaded: ~80% within four years), with a
                        caption dating the FY28-32 supplier window (~2028-2031).
  • sources_line ...... honest-floor caveat (FFATA is first-tier only / lagged /
                        under-reported; BIW chain dark) + provenance.

Shape fills use the BLUE_*/GRAY_*/PRELIM ramps (deck_core.style); the column
chart uses the CHART_ACCENT_* palette (charts only), per the house rules.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector,
    table, trow, tcell,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
)
from deck_core.charts import graphic_frame, column_chart, THINKCELL_BARS
from deck_core.style import (
    IN, PT, BLACK, WHITE, DK,
    BLUE_1, BLUE_4, BLUE_5, GRAY_5, PRELIM, FONT,
    CHART_ACCENT_2,
)

LAYOUT = "slideLayout4"

# ── Layout anchors (inches) ────────────────────────────────────────────────
_LM = 0.495                 # left margin (flush with chrome)
_W = 12.336                 # content width

# Cadence ribbon: 4 cards + 3 arrow gaps spanning the full content width.
_CARD_W, _GAP = 2.78, 0.405
_CARD_X = [round(_LM + i * (_CARD_W + _GAP), 3) for i in range(4)]   # 0.495 .. 10.05
_CAP_Y, _CAP_H = 1.92, 0.34
_BODY_Y, _BODY_H = 2.26, 1.18
_ARROW_Y = 2.83

# ── Cadence cards (the timing engine) ──────────────────────────────────────
# (block, award line, headline $, sub-line, focal?)  — FY11 single-ship and the
# full prime-$ detail live in the provenance CSV; here only the dated MYP spine.
_CARDS = [
    ("FY13\u201317 MYP", "Awarded 2013", "$942M",  "320 first-tier suppliers", False),
    ("FY18\u201322 MYP", "Awarded 2018", "$1,327M", "344 first-tier suppliers", False),
    ("FY23\u201327 MYP", "Awarded 2023", "$1,145M", "89 suppliers (ramping)",   False),
    ("FY28\u201332 MYP", "~2028 (forecast)", "~$1B+", "next wave \u2014 be early", True),
]

# ── WHERE table: concentration by ship system (reported $, HHI) ─────────────
# (system, $M, HHI, read, highlight?)
_WHERE_ROWS = [
    ("Auxiliary systems",            "948", "683",   "Open lane \u2014 no supplier >16%", True),
    ("Propulsion plant",            "958", "1,905", "Entrenched (GE 35%) \u2014 team",  False),
    ("Electric plant",              "751", "2,106", "Entrenched (RR 43%) \u2014 team",  False),
    ("Command & surveillance",       "48", "2,188", "Concentrated, small",             False),
    ("Armament",                      "2", "6,561", "Locked (Lake Shore 78%)",         False),
]

# ── WHEN chart: cumulative first-tier subaward $ by years after prime award ──
_WHEN_CATS = ["Yr 0", "+1", "+2", "+3", "+4"]
_WHEN_CUM = [26, 42, 58, 69, 79]   # %, front-loaded -> ~80% within four years

CHARTS = [
    column_chart(
        categories=_WHEN_CATS,
        series=[{"name": "Cumulative subaward $ (%)", "values": _WHEN_CUM,
                 "color": CHART_ACCENT_2, "label_color": BLACK}],
        value_axis_format='0"%"',
        value_label_format='0"%"',
        value_axis_max=100,
        show_value_axis_labels=False,
        gap_width=55,
        cat_header="Years after prime award",
        **THINKCELL_BARS,
    )
]


def _card(n, x, cap, awarded, headline, subline, focal):
    """One cadence node: a dark cap over a body card (award / $ / suppliers)."""
    cap_fill = BLUE_4 if focal else BLUE_5
    body_fill = PRELIM if focal else BLUE_1
    body_border = 19050 if focal else 12700   # 1.5pt focal vs 1pt house
    head_color = BLACK if focal else BLUE_5
    cap_sp = text_box(
        n(), "CadenceCap", IN(x), IN(_CAP_Y), IN(_CARD_W), IN(_CAP_H),
        [paragraph([run(cap, size=PT(11), bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=100000)],
        fill=cap_fill, line_color="none", anchor="ctr")
    body_sp = text_box(
        n(), "CadenceBody", IN(x), IN(_BODY_Y), IN(_CARD_W), IN(_BODY_H),
        [paragraph([run(awarded, size=PT(9), color=GRAY_5, font=FONT)],
                   align="ctr", line_spacing=100000, space_after=300),
         paragraph([run(headline, size=PT(18), bold=True, color=head_color, font=FONT)],
                   align="ctr", line_spacing=100000, space_after=300),
         paragraph([run(subline, size=PT(8.5), italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100000)],
        fill=body_fill, line_width=body_border, anchor="ctr")
    return cap_sp + body_sp


def _mini_header(n, text, x, cx, *, y=3.92):
    """A small bold section cap with a thin blue rule beneath it."""
    hdr = text_box(
        n(), "MiniHeader", IN(x), IN(y), IN(cx), IN(0.24),
        [paragraph([run(text, size=PT(10), bold=True, color=DK, font=FONT)],
                   line_spacing=100000)],
        fill=None, line_color="none", anchor="b", l_ins=0, r_ins=0, t_ins=0, b_ins=0)
    rule = connector(n(), "HeaderRule", IN(x), IN(y + 0.27), IN(cx), IN(0),
                     color=BLUE_4, width=12700)
    return hdr + rule


def _where_table(n):
    """Lower-left house table: ship-system concentration (reported $, HHI, read)."""
    hdr_fill = BLUE_5
    cw = [IN(2.45), IN(0.72), IN(0.78), IN(2.10)]   # sums to 6.05
    rows = [
        trow([
            tcell("Ship system", size=PT(9), bold=True, color=WHITE, fill=hdr_fill,
                  borders={"L": "none", "R": "none", "T": "none", "B": "none"}),
            tcell("$M", size=PT(9), bold=True, color=WHITE, fill=hdr_fill, align="r",
                  borders={"L": "none", "R": "none", "T": "none", "B": "none"}),
            tcell("HHI", size=PT(9), bold=True, color=WHITE, fill=hdr_fill, align="r",
                  borders={"L": "none", "R": "none", "T": "none", "B": "none"}),
            tcell("Read", size=PT(9), bold=True, color=WHITE, fill=hdr_fill,
                  borders={"L": "none", "R": "none", "T": "none", "B": "none"}),
        ], h=IN(0.30)),
    ]
    for sysname, dollars, hhi, read, hot in _WHERE_ROWS:
        fill = PRELIM if hot else None
        rule = {"L": "none", "R": "none", "T": "none",
                "B": {"color": "D9D9D9", "width": 9525}}
        rows.append(trow([
            tcell(sysname, size=PT(9), bold=hot, color=BLACK, fill=fill, borders=rule),
            tcell(dollars, size=PT(9), color=BLACK, fill=fill, align="r", borders=rule),
            tcell(hhi, size=PT(9), color=BLACK, fill=fill, align="r", borders=rule),
            tcell(read, size=PT(8.5), italic=True, color=BLACK, fill=fill, borders=rule),
        ], h=IN(0.31)))
    return table(n(), "WhereTable", IN(_LM), IN(4.26), IN(6.05), IN(1.85),
                 col_widths=cw, rows=rows)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 4000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Recompete On-Ramps", "Supply the Prime"))
    out.append(title_placeholder(
        "Recompete Cadence",
        "The DDG-51 prime is a closed two-yard duopoly \u2014 but its ~5-year re-buy "
        "opens a datable $1B+ first-tier supplier wave; position ahead of the "
        "FY28\u201332 buy (~2028)."))

    # ── beat 1: the timing engine (cadence ribbon) ──
    out.append(text_box(
        n(), "EngineCap", IN(_LM), IN(1.50), IN(_W), IN(0.26),
        [paragraph([run("THE TIMING ENGINE", size=PT(10), bold=True, color=DK, font=FONT),
                    run("  \u2014  DDG-51 is re-bought as sequential ~5-year multi-year "
                        "procurements (MYPs); each block re-opens ~$1B of first-tier demand",
                        size=PT(10), color=DK, font=FONT)],
                   line_spacing=100000)],
        fill=None, line_color="none", anchor="b", l_ins=0, r_ins=0, t_ins=0, b_ins=0))

    for x, (cap, awarded, headline, subline, focal) in zip(_CARD_X, _CARDS):
        out.append(_card(n, x, cap, awarded, headline, subline, focal))
    # spine arrows between the four nodes
    for i in range(3):
        ax = _CARD_X[i] + _CARD_W + 0.045
        out.append(connector(n(), f"CadenceArrow{i}", IN(ax), IN(_ARROW_Y),
                             IN(_GAP - 0.09), IN(0), color=BLUE_4, width=22225, arrow=True))

    # cadence caption under the ribbon
    out.append(text_box(
        n(), "CadenceCaption", IN(_LM), IN(3.52), IN(_W), IN(0.30),
        [paragraph([
            run("Award cadence 2013 \u2192 2018 \u2192 2023 (~5 FY) \u2192 next buy ~2028. ",
                size=PT(8.5), bold=True, color=BLACK, font=FONT),
            run("$3.47B reported across 521 first-tier suppliers to date (266 recur across "
                "\u22652 blocks). The prime route is closed; the route in is to supply a holder.",
                size=PT(8.5), italic=True, color=BLACK, font=FONT)],
            line_spacing=100000)],
        fill=None, line_color="none", anchor="t", l_ins=0, r_ins=0, t_ins=0, b_ins=0))

    # ── beat 2 + 3: WHERE (table) and WHEN (chart) ──
    out.append(_mini_header(n, "WHERE TO ENTER \u2014 concentration by ship system "
                            "(reported $, supplier HHI)", _LM, 6.05))
    out.append(_mini_header(n, "WHEN TO ENTER \u2014 subaward $ is front-loaded off "
                            "each prime award", 6.78, 6.05))

    out.append(_where_table(n))

    # WHEN: chart context line + native column chart + dated-window caption
    out.append(text_box(
        n(), "WhenContext", IN(6.78), IN(4.24), IN(6.05), IN(0.22),
        [paragraph([run("Cumulative share of reported first-tier subaward $, by years "
                        "after the prime award", size=PT(8), italic=True, color=GRAY_5,
                        font=FONT)], line_spacing=100000)],
        fill=None, line_color="none", anchor="b", l_ins=0, r_ins=0, t_ins=0, b_ins=0))
    out.append(graphic_frame(sp_id=n(), name="WhenChart",
                             x=IN(6.72), y=IN(4.52), cx=IN(6.13), cy=IN(1.30), rId="rId2"))
    out.append(text_box(
        n(), "WhenCaption", IN(6.78), IN(5.86), IN(6.05), IN(0.50),
        [paragraph([
            run("~80% lands within four years \u2192 ", size=PT(8.5), bold=True,
                color=BLACK, font=FONT),
            run("the FY28\u201332 award (~2028) opens a dated supplier window "
                "~2028\u20132031. Be sourced before it opens, not chasing the surge.",
                size=PT(8.5), italic=True, color=BLACK, font=FONT)],
            line_spacing=100000)],
        fill=None, line_color="none", anchor="t", l_ins=0, r_ins=0, t_ins=0, b_ins=0))

    # ── chrome: draft chip + sources ──
    out.append(prelim_chip())
    out.append(sources_line(
        "Note: First-tier (FFATA) subaward reporting is a floor, not a census \u2014 "
        "first-tier only, 6\u201318-mo lag, and under-reported (Bath Iron Works files "
        "<5% of Huntington Ingalls on the same block, so its chain is dark in FFATA); "
        "the HHI / where-to-enter read is on reported dollars. The supplier "
        "\u201Crecompete\u201D is a forecastable demand surge on the prime's cadence, "
        "not a date-certain ordering-period end. | "
        "Source: SAM.gov Contract Awards + USAspending (prime cadence & dollars; "
        "multiyear basis 10 U.S.C. 3501 / FAR Subpart 17.1); SAM.gov Subaward "
        "Reporting (FFATA) first-tier base, SWBS ship-system crosswalk from the "
        "program workbook. As of 2026-06-24."))
    return "".join(out)


def render() -> str:
    return slide(_body())
