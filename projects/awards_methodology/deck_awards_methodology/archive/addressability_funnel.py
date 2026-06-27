"""slide_01_addressability_funnel — Addressability (Generalized Decision Cascade), slide 01.

EXHIBIT — "Addressability | A large award isn't an opportunity until it clears five
gates — and the gate it fails as prime names the route in." The method opener for the
worked instances on slides 02 (supply the prime) and 03 (become a holder).

A left-of-centre VERTICAL CASCADE walks seven stacked elements top-to-bottom, wired by
down-arrow connectors: a Precondition (classify the record), Gate 1 (Demand, not
capacity), the ADDRESSABLE MARKET waypoint (focal light-blue band), Gate 2 (Access —
the pivot, accent fill), then Gates 3-5 (Timing / Ability / Economics). Each gate carries
a bold title, its criterion, and an italic pass/redirect verdict. The cascade fans out
into a row of FOUR ROUTE LEAVES (the second focal stop) — Bid the recompete · On-ramp ·
Subcontract/teaming · Consortium/OT — each tagged with the posture that leads to it. Two
dashed ANNOTATION callouts sit in the lane right of the cascade (closed prime != closed
market; enter early or the follow-on closes). A set-apart italic PORTAL-VISIBILITY note
sits beneath the leaves. A RIGHT RAIL carries a bold finding + non-bold support. No
dataset figures on the face — this is the generalized method read.

CODE MAP (body in paint order; headers mark roles in place):
  • chrome ............. breadcrumb() + title_placeholder()
  • framing one-liner .. event-probability vs. addressability band (top-left)
  • _CASCADE ........... the 7 stacked cascade elements (loop): precondition, Gate 1,
                         ADDRESSABLE waypoint, Gate 2 pivot, Gates 3-5
  • _ARROWS ............ vertical down-arrow connectors between cascade elements (loop)
  • route header ....... "Route leaves — the payoff" band + 4 fan-out arrows (loop)
  • _LEAVES ............ the 4 route-leaf boxes, posture-tagged (loop)
  • annotations ........ two dashed reframe callouts (closed-prime / enter-early)
  • portal overlay ..... set-apart italic note beneath the leaves (not a gate)
  • right rail ......... title-band table() + bold finding box + support bullets
  • footnote ........... method/authorities/sources Note line
  • logo ............... picture() top-right (IMAGES rId2)

Authored to the deck_core house style (slideLayout4, breadcrumb/title chrome, native
table title band, dashed callouts, focal light-blue fills) — geometry is original to
this slide; content, order, the access->route mapping, the emphasis intent (the
ADDRESSABLE waypoint and the ROUTE LEAVES are the focal pair; Access is the pivot) and
the accuracy guardrails follow the content brief.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break,
    table, trow, tcell_rich, tpara, trun, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates) ──────────────────────────────────────
_CAS_X, _CAS_W = 1.50, 4.45        # cascade-box column (gate/precondition boxes)
_WP_X, _WP_W = 1.30, 4.85          # ADDRESSABLE waypoint band (wider; the focal stop)
_CAS_MID = 3.72                    # cascade centre-line (down-arrows ride this x)
_ANN_X, _ANN_W = 6.30, 3.02        # annotation lane (dashed reframe callouts)
_RAIL_X, _RAIL_W = 9.55, 3.30      # right-rail commentary column
_GRAY = GRAY_3                     # receding (upstream filtering) fill
_HAIR = "808080"                   # hairline rule colour
_FOCAL = "CEDDEC"                  # focal light-blue (waypoint glow)
_PIVOT = "447BB2"                  # access-pivot accent fill
_LEAF = "99B9D8"                   # route-leaf fill

# ── the cascade — 7 stacked elements, top to bottom ──────────────────────────
#   keys: y,h = box geom; fill/line/lw = styling; tc = text colour; vc = verdict
#   colour; align/ts = title align + size; title/crit/verdict = the three lines.
_CASCADE = [
    {"y": 1.52, "h": 0.42, "fill": _GRAY, "line": _HAIR, "lw": 3175, "tc": BLACK, "vc": DK, "align": "l", "ts": 9,
     "title": "Precondition  ·  Classify the record",
     "crit": "Definitive contract · IDV (IDIQ/BPA/BOA/FSS) · order · mod/option · 1st-tier subaward · OT",
     "verdict": "Mislabel the record and every gate below is wrong"},
    {"y": 2.02, "h": 0.48, "fill": _GRAY, "line": _HAIR, "lw": 3175, "tc": BLACK, "vc": DK, "align": "l", "ts": 9,
     "title": "Gate 1  ·  Demand, not capacity",
     "crit": "Obligated orders + quantity-adding mods = demand;  ceiling / TBAOV / unexercised options = capacity",
     "verdict": "Fail \u2192 a ceiling or empty BPA isn\u2019t revenue yet \u2014 track for actual orders"},
    {"y": 2.58, "h": 0.42, "fill": _FOCAL, "line": DK, "lw": 12700, "tc": BLACK, "vc": DK, "align": "ctr", "ts": 11,
     "title": "ADDRESSABLE MARKET",
     "crit": "Real, in-scope, committed demand \u2014 the denominator and first focal stop",
     "verdict": ""},
    {"y": 3.08, "h": 0.52, "fill": _PIVOT, "line": DK, "lw": 12700, "tc": WHITE, "vc": _FOCAL, "align": "l", "ts": 9,
     "title": "Gate 2  ·  Access \u2014 the pivot",
     "crit": "Who may legally compete? extentCompeted · single- vs. multiple-award · FAR 16.505 fair opportunity",
     "verdict": "Fail as prime \u2192 redirect to a non-prime route    ·    Pass \u2192 open recompete, be prime"},
    {"y": 3.68, "h": 0.48, "fill": _GRAY, "line": _HAIR, "lw": 3175, "tc": BLACK, "vc": DK, "align": "l", "ts": 9,
     "title": "Gate 3  ·  Timing",
     "crit": "Upcoming contracting action? period of performance vs. ordering-period end vs. option dates",
     "verdict": "Fail \u2192 option exercise or mid-ordering-period: monitor.  A bridge is delayed, not abandoned"},
    {"y": 4.24, "h": 0.44, "fill": _GRAY, "line": _HAIR, "lw": 3175, "tc": BLACK, "vc": DK, "align": "l", "ts": 9,
     "title": "Gate 4  ·  Ability to perform",
     "crit": "Responsibility · past performance · facility clearance (FCL) · CAS/DCAA accounting · flowdowns",
     "verdict": "Fail \u2192 not yet qualified: qualify, team, or subcontract"},
    {"y": 4.76, "h": 0.46, "fill": _GRAY, "line": _HAIR, "lw": 3175, "tc": BLACK, "vc": DK, "align": "l", "ts": 9,
     "title": "Gate 5  ·  Economics",
     "crit": "Contract type & payment risk · financing · data rights (DFARS -7013 / -7014) · compliance burden",
     "verdict": "Fail \u2192 economics don\u2019t fit: pass, or pursue a different tier"},
]

# ── down-arrow connectors between consecutive cascade elements (top y, gap) ──
_ARROWS = [
    (1.94, 0.08), (2.50, 0.08), (3.00, 0.08), (3.60, 0.08), (4.16, 0.08), (4.68, 0.08),
]

# ── the four route leaves (the second focal stop) ────────────────────────────
_LEAVES = [    # (x, route, posture, detail)
    (0.50, "Bid the recompete", "Open standalone / full-and-open", "Compete as prime"),
    (2.70, "On-ramp", "Multiple-award IDIQ", "Seat as a holder at the next pool   \u203a  slide 03"),
    (4.90, "Subcontract / teaming", "Closed prime · single-award · sole-source", "FAR 9.6 CTA or prime-sub; MYP/block enterable below the prime   \u203a  slide 02"),
    (7.10, "Consortium / OT", "Innovation pathway", "Enter at the prototype / consortium stage"),
]
_LEAF_W, _LEAF_Y, _LEAF_H = 2.08, 5.46, 0.96

# ── the two dashed reframe annotations ───────────────────────────────────────
_ANNOTATIONS = [    # (y, h, head, body)
    (2.04, 1.32, "Closed prime \u2260 closed market   \u203a  feeds the subcontract leaf (slide 02)",
     "When the prime role is committed years ahead \u2014 multiyear procurement (FAR 17.1), block/lot buy, or a "
     "major quantity-adding mod \u2014 demand sits below the prime: components, castings, electronics, software, "
     "sustainment. It releases as AP/LLTM and EOQ buys, bought by the prime, not the Government. FFATA first-tier "
     "subaward reporting is a floor, not a census."),
    (3.50, 1.46, "Enter early or the follow-on closes   \u203a  feeds the consortium / OT leaf",
     "OT and SBIR/STTR are entry authorities, not pricing types. A competitively awarded prototype OT can lead to a "
     "production follow-on with no new competition (DFARS 206.001-70); an SBIR/STTR Phase III can be sole-source to "
     "the firm whose earlier work it derives from. Enter at the topic, prototype, consortium, BAA, or CSO stage \u2014 "
     "before the production follow-on closes to later entrants."),
]

# ── right-rail support bullets (lead clause bold, remainder plain) ───────────
_SUPPORT = [    # (lead, rest)
    ("The upper gates are hard data", " \u2014 object type, obligations vs. ceiling, extent of competition \u2014 and decide quickly; the lower gates (timing, ability to perform) are judgment."),
    ("The decision is route, not bid/no-bid", " \u2014 bid the recompete, on-ramp onto the vehicle, subcontract/team to a holder, or join the consortium/OT."),
    ("A closed prime is not a closed market", " \u2014 multiyear and block buys release demand below the prime (AP/LLTM, EOQ, first-tier subcontracts)."),
    ("Single-award \u2260 sole-source", " \u2014 a fully competed vehicle can have one winner; an order under a competed multiple-award vehicle can still be directed to one holder."),
    ("Most addressable awards were never on SAM.gov Contract Opportunities", " \u2014 the work is in Contract Awards / USAspending / FPDS."),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Addressability", "Decision Cascade (1/3)"))
    out.append(title_placeholder(
        "Addressability",
        "A large award isn\u2019t an opportunity until it clears five gates \u2014 and the gate it fails as prime names the route in.",
    ))

    # ── framing one-liner: event probability vs. addressability ──
    out.append(text_box(n(), "Framing", IN(0.50), IN(1.12), IN(8.70), IN(0.34), [paragraph([
        run("Event probability", size=PT(10), bold=True, color=BLACK, font=FONT),
        run(" \u2014 will the Government buy this again?     ", size=PT(10), italic=True, color=BLACK, font=FONT),
        run("\u2260  ", size=PT(10), bold=True, color=DK, font=FONT),
        run("Addressability", size=PT(10), bold=True, color=DK, font=FONT),
        run(" \u2014 can this company reach and win the action?", size=PT(10), italic=True, color=BLACK, font=FONT),
    ], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))

    # ── the cascade: 7 stacked elements ──
    for g in _CASCADE:
        _x = _WP_X if g["fill"] == _FOCAL else _CAS_X
        _w = _WP_W if g["fill"] == _FOCAL else _CAS_W
        runs = [run(g["title"], size=PT(g["ts"]), bold=True, color=g["tc"], font=FONT)]
        if g["crit"]:
            runs += [line_break(), run(g["crit"], size=PT(7.5), color=g["tc"], font=FONT)]
        if g["verdict"]:
            runs += [line_break(), run(g["verdict"], size=PT(7.5), italic=True, color=g["vc"], font=FONT)]
        out.append(text_box(n(), "Gate", IN(_x), IN(g["y"]), IN(_w), IN(g["h"]),
                            [paragraph(runs, align=g["align"], line_spacing=100000)],
                            fill=g["fill"], line_color=g["line"], line_width=g["lw"], anchor="ctr",
                            l_ins=54000, r_ins=54000, t_ins=18000, b_ins=18000))

    # ── down-arrow connectors riding the cascade centre-line ──
    for _y, _gap in _ARROWS:
        out.append(connector(n(), "Cascade Arrow", IN(_CAS_MID), IN(_y), IN(0.003), IN(_gap),
                             color=DK, width=12700, arrow=True))

    # ── route header band + arrow from Gate 5 into it ──
    out.append(connector(n(), "To Leaves", IN(_CAS_MID), IN(5.22), IN(0.003), IN(0.14),
                         color=DK, width=12700, arrow=True))
    out.append(text_box(n(), "Route Header", IN(0.50), IN(5.16), IN(8.68), IN(0.26), [paragraph([
        run("Route leaves \u2014 the payoff", size=PT(10), bold=True, color=DK, font=FONT),
        run("   (what survives is named by route)", size=PT(9), italic=True, color=BLACK, font=FONT),
    ], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))

    # ── four fan-out arrows (header -> each leaf) ──
    for _lx, _r, _p, _d in _LEAVES:
        out.append(connector(n(), "Fan Arrow", IN(_lx + _LEAF_W / 2.0), IN(5.40), IN(0.003), IN(0.06),
                             color=DK, width=12700, arrow=True))

    # ── the four route leaves ──
    for _lx, _route, _posture, _detail in _LEAVES:
        out.append(text_box(n(), "Leaf", IN(_lx), IN(_LEAF_Y), IN(_LEAF_W), IN(_LEAF_H), [paragraph([
            run(_route, size=PT(10), bold=True, color=BLACK, font=FONT),
            line_break(), run(_posture, size=PT(7.5), italic=True, color=DK, font=FONT),
            line_break(), run(_detail, size=PT(7.5), color=BLACK, font=FONT),
        ], align="ctr", line_spacing=100000)], fill=_LEAF, line_color=DK, line_width=3175, anchor="ctr",
            l_ins=45720, r_ins=45720))

    # ── two dashed reframe annotations (right of the cascade) ──
    for _y, _h, _head, _bodytext in _ANNOTATIONS:
        out.append(text_box(n(), "Annotation", IN(_ANN_X), IN(_y), IN(_ANN_W), IN(_h), [
            paragraph([run(_head, size=PT(8.5), bold=True, color=DK, font=FONT)], line_spacing=100000, space_after=4),
            paragraph([run(_bodytext, size=PT(8), color=BLACK, font=FONT)], line_spacing=100000),
        ], fill=WHITE, line_color=DK, line_width=12700, dashed_line=True, anchor="ctr",
            l_ins=63500, r_ins=63500, t_ins=36000, b_ins=36000))

    # ── portal-visibility overlay (a property of the set, not a gate) ──
    out.append(text_box(n(), "Portal Overlay", IN(0.50), IN(6.50), IN(8.68), IN(0.44), [paragraph([
        run("Portal visibility ", size=PT(8.5), bold=True, italic=True, color=DK, font=FONT),
        run("(a property of the set, not a gate): ", size=PT(8.5), italic=True, color=DK, font=FONT),
        run("most addressable awards were never advertised on SAM.gov Contract Opportunities \u2014 award-data "
            "analysis runs on SAM.gov Contract Awards, USAspending, and FPDS, not the opportunities portal.",
            size=PT(8.5), color=BLACK, font=FONT),
    ], line_spacing=100000)], fill=None, line_color=DK, line_width=6350, dashed_line=True, anchor="ctr",
        l_ins=63500, r_ins=63500))

    # ── right-rail commentary: title band ──
    out.append(table(n(), "Rail Title", IN(_RAIL_X), IN(1.10), IN(_RAIL_W), IN(0.30), col_widths=[IN(_RAIL_W)], rows=[
        trow([tcell_rich([tpara([trun("What to take away", size=PT(11), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)],
                         l_ins=41564, r_ins=41564,
                         borders={"L": "none", "R": "none", "T": {"color": WHITE, "width": 12700}, "B": {"color": BLACK, "width": 12700}})], h=IN(0.30)),
    ]))

    # ── right-rail: bold finding ──
    out.append(text_box(n(), "Finding", IN(_RAIL_X), IN(1.52), IN(_RAIL_W), IN(1.05), [paragraph([
        run("A large award is not an opportunity \u2014 it is a posture to classify. Walk the gates; the gate it "
            "fails as prime names the route in.", size=PT(10), bold=True, color=BLACK, font=FONT),
    ], line_spacing=104000)], fill=None, line_color="none", anchor="t"))

    # ── right-rail: non-bold support bullets ──
    _support_paras = []
    for _lead, _rest in _SUPPORT:
        _support_paras.append(paragraph(
            [run(_lead, size=PT(9), bold=True, color=BLACK, font=FONT), run(_rest, size=PT(9), color=BLACK, font=FONT)],
            bullet=True, mar_l=148113, indent=-148113, line_spacing=102000, space_after=6))
    out.append(text_box(n(), "Support", IN(_RAIL_X), IN(2.62), IN(_RAIL_W), IN(4.30),
                        _support_paras, fill=None, line_color="none", anchor="t"))

    # ── footnote: method / authorities / sources ──
    out.append(text_box(n(), "Footnote", IN(0.495), IN(7.04), IN(12.40), IN(0.34), [paragraph([
        run("Generalized method \u2014 no dataset figures on the face; named vehicles and market sizing live on slides "
            "02\u201303 and the wiki.   ", size=PT(7), italic=True, color=DK, font=FONT),
        run("Authorities: FAR 16.5 / 17.1 / 17.2 / 9.6 / 6.302 / 52.217-8; DFARS 206.001-70 / 252.227-7013 / -7014; "
            "15 U.S.C. 638.   Sources: SAM.gov Contract Awards; USAspending; FPDS; SAM.gov Contract Opportunities.",
            size=PT(7), color=BLACK, font=FONT),
    ], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))

    # ── logo (top-right) ──
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
