"""customer_anatomy - the federal customer is three customers: the org that funds,
the org that buys, and the org that uses a capability are usually three different
organizations, and they are not equally recoverable from awards data.

Style + chrome rules: deck_core/slide_guide.md. Builders imported from deck_core
(primitives + style + text_metrics); no per-slide copies.

Visual read: a thin, muted org-chain relationship band on top (operational user ->
requirement -> program/acquisition -> contracting), a one-line lead finding rail,
then the dominant exhibit - a rule-skin triad table (roles as rows) whose Role
column carries the WHO FUNDS / WHO BUYS / WHO USES chips and whose Visibility
column is the color-graded scan column. Two commentary cards close the page: a
focal "BD doors" card (lower-left) and a muted data-observability note (right).

Palette note: the spec calls for traffic-light High(green)/Medium(amber)/Low(red)
visibility cells. The deck palette (slide_guide.md -> Color) is locked to the
blue/gray ramps with no green/amber/red, so visibility is graded on the BLUE ramp
instead - darker fill = more recoverable from the data (HIGH=BLUE_5, MEDIUM=BLUE_3,
LOW=BLUE_1). Swap in literal traffic-light hexes only if house style is overridden.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun,
    connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_3, BLUE_5, GRAY_1, GRAY_3, GRAY_4,
    DK, WHITE, BLACK, FONT,
    INSETS_CARD,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
    MESSAGE_11PT, BODY_12PT, CAP_12PT,
    blue_pair,
)
from deck_core import text_metrics

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers

# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION          = "Federal Market Mapping"
_BREADCRUMB_TOPIC = "Who funds, buys, and uses"
_TOPIC            = "The federal customer is three customers"
_TAKEAWAY         = ("money, decision authority, and end-user rarely sit in one "
                     "organization")
_SOURCES = ("Sources: (1) Buyer and payer fields: FPDS, SAM.gov Contract Awards, "
            "USAspending awarding office and funding TAS; (2) Entity resolution: "
            "SAM.gov Entity Management; (3) End-user: external program reporting, "
            "not the contract APIs. Worked example: internal Army Market Mapping "
            "workbook (Customer Map)")


# ════════════════════════════════════════════════════════════════════════════
# BUILD SLIDE BODY
# ════════════════════════════════════════════════════════════════════════════

# -- Vertical bands within BODY (EMU). Reading order top-to-bottom. -----------
_ZONE_Y,  _ZONE_H  = BODY_Y, 470_000                 # pale grouping band
_NODE_Y,  _NODE_H  = BODY_Y + 55_000, 360_000        # org-chain nodes (rich)
_LEAD_Y,  _LEAD_H  = 1_905_000, 405_000              # one-line lead finding rail
_TBL_Y             = 2_440_000                        # triad table top
_CMT_H             = 900_000                           # bottom commentary row
_CMT_Y             = BODY_B - _CMT_H                   # -> bottom flush with BODY_B

# -- Triad table column widths (EMU, sum == BODY_CX). Army example + Where are
#    widest; Visibility narrow but bold; What-it-is is the first to shorten. ---
_COL_ROLE  = 1_500_000
_COL_WHAT  = 2_100_000
_COL_ARMY  = 3_300_000
_COL_VIS   = 1_182_362
_COL_WHERE = 3_200_000
_COL_W = [_COL_ROLE, _COL_WHAT, _COL_ARMY, _COL_VIS, _COL_WHERE]
assert sum(_COL_W) == BODY_CX, sum(_COL_W)

# -- Row data (funds -> buys -> uses). Hyphen/slash separators removed per the
#    guide (no "/", "+", "->" as separators; no em dashes). -------------------
_HEADER = ["Role", "What it is (DoD)", "Army watercraft example",
           "Awards-data visibility", "Where we get it"]

_ROWS = [
    {   # WHO FUNDS
        "role": ("WHO FUNDS", "the money"),
        "what": ("Appropriation, color of money, and program element or budget "
                 "line."),
        "army": ("OPA line 8211R01001 (MSV(L)) and RDT&E PE 0603804A-526, "
                 "programmed by PM Transportation Systems under CPE Combat "
                 "Sustainment."),
        "vis": "MEDIUM", "vis_i": 2,   # BLUE_3 / WHITE
        "where": ("USAspending funding endpoint (TAS); President's Budget P-1 "
                  "and R-1."),
    },
    {   # WHO BUYS
        "role": ("WHO BUYS", "the decision"),
        "what": ("Contracting office (DODAAC) plus the milestone and "
                 "source-selection authority."),
        "army": ("ACC-Detroit Arsenal (DODAAC W56HZV) runs and awards; ASA(ALT) "
                 "is the milestone decision authority."),
        "vis": "HIGH", "vis_i": 4,     # BLUE_5 / WHITE
        "where": ("FPDS, SAM Contract Awards, and USAspending awarding-office "
                  "fields."),
    },
    {   # WHO USES
        "role": ("WHO USES", "the capability"),
        "what": "The operational command or unit that fields the capability.",
        "army": ("USARPAC, 8th Theater Sustainment Command, and the 569th Dive "
                 "Detachment (INDOPACOM)."),
        "vis": "LOW", "vis_i": 0,      # BLUE_1 / DK
        "where": ("Sourced externally (2025 autonomous ship-to-shore demo), not "
                  "the contract APIs."),
    },
]


def _band() -> str:
    """Muted org-chain band: a pale grouping zone unifies four information-rich
    nodes (bold org name + italic role-mapping) joined by thin arrows. Read first
    but visually subordinate to the table - the zone + node text carry the
    band->table bridge so no separate caption row is needed."""
    nodes = [
        ("Operational user",                "maps to WHO USES"),
        ("Requirement and experimentation", "shapes the requirement"),
        ("Program and acquisition",         "maps to WHO FUNDS and WHO BUYS"),
        ("Contracting",                     "maps to WHO BUYS"),
    ]
    n = len(nodes)
    gap = 360_000                                   # > 0.27in so arrowheads read
    node_w = (BODY_CX - (n - 1) * gap) // n
    cy = _NODE_Y + _NODE_H // 2

    # Pale grouping zone behind the row (the "relationship band" itself).
    xml = [text_box(
        10, "BandZone", BODY_X, _ZONE_Y, BODY_CX, _ZONE_H, [paragraph([])],
        fill=GRAY_1, line_color=GRAY_3, line_width=9_525)]

    for i, (name, mapping) in enumerate(nodes):
        x = BODY_X + i * (node_w + gap)
        # Rich node: bold name + muted italic role-mapping, on the pale zone.
        xml.append(text_box(
            11 + i, f"BandNode{i+1}", x, _NODE_Y, node_w, _NODE_H,
            [paragraph([run(name, size=LABEL_9PT, bold=True, color=DK, font=FONT)],
                       align="ctr", space_after=200),
             paragraph([run(mapping, size=FINEPRINT_8_5PT, italic=True,
                            color=GRAY_4, font=FONT)], align="ctr")],
            anchor="ctr", fill=WHITE, line_color=GRAY_3, line_width=9_525,
            insets=(45_720, 18_000, 45_720, 18_000)))
        # Muted arrow into the next node.
        if i < n - 1:
            xml.append(connector(
                15 + i, f"BandArrow{i+1}", x + node_w, cy, gap, 0,
                color=GRAY_4, width=9_525, arrow=True))
    return "".join(xml)


def _lead() -> str:
    """Commentary 1 - lead finding as a no-fill rail above the exhibit:
    bold one-liner + a single regular explanatory line."""
    paras = [
        paragraph([run("Payer is not buyer is not user.",
                       size=BODY_12PT, bold=True, color=DK, font=FONT)],
                  space_after=300),
        paragraph([run("The appropriation that funds a program, the contracting "
                       "office that awards it, and the unit that fields it answer "
                       "to different commands and live in different places.",
                       size=DENSE_BODY_10PT, color=DK, font=FONT)]),
    ]
    return text_box(21, "LeadFinding", BODY_X, _LEAD_Y, BODY_CX, _LEAD_H, paras,
                    anchor="t", fill=None, insets=(0, 0, 0, 0))


def _triad_table() -> str:
    """The dominant exhibit: roles as rows, rule-skin borders (1.5pt black header
    underline, thin GRAY_3 between body rows, no vertical gridlines). Role column
    carries the WHO chips; Visibility is the color-graded scan column."""
    # Honest per-row heights from the shared text model (size_pt=11 covers the
    # 11pt visibility word - the conservative driver the probe's --table-fit uses).
    rows_text = [_HEADER] + [
        [f"{r['role'][0]} {r['role'][1]}", r["what"], r["army"], r["vis"], r["where"]]
        for r in _ROWS
    ]
    row_h = text_metrics.estimate_row_heights(
        rows_text, _COL_W, size_pt=11.0, header_size_pt=10.0, min_row_h=300_000)
    # Equalize the three data rows so the Role and Visibility emphasis cells read
    # as matching chips; give them a little headroom above the content floor.
    body_h = max(640_000, max(row_h[1:]))
    row_h = [row_h[0], body_h, body_h, body_h]

    def _b(side_b):
        # All cells: no L/R/T rule; bottom per the rule skin.
        return {"L": "none", "R": "none", "T": "none", "B": side_b}

    hdr_b = {"color": BLACK, "width": 19_050}        # 1.5pt black underline
    mid_b = {"color": GRAY_3, "width": 9_525}        # thin inter-row rule
    no_b  = "none"

    # Header row (rule skin: no fill; the underline carries it).
    header_cells = [
        tcell(h, bold=True, size=DENSE_BODY_10PT, color=DK,
              align=("ctr" if i == 3 else "l"), anchor="ctr",
              borders=_b(hdr_b))
        for i, h in enumerate(_HEADER)
    ]
    rows = [trow(header_cells, h=row_h[0])]

    for ri, r in enumerate(_ROWS):
        body_b = no_b if ri == len(_ROWS) - 1 else mid_b
        fill, txt = blue_pair(r["vis_i"])
        role_cell = tcell_rich(
            [tpara([trun(r["role"][0], size=DENSE_BODY_10PT, bold=True, color=DK)]),
             tpara([trun(r["role"][1], size=FINEPRINT_8_5PT, italic=True, color=DK)])],
            fill=BLUE_1, anchor="ctr", borders=_b(body_b))
        cells = [
            role_cell,
            tcell(r["what"], size=DENSE_BODY_10PT, color=DK, align="l",
                  anchor="t", borders=_b(body_b)),
            tcell(r["army"], size=DENSE_BODY_10PT, color=DK, align="l",
                  anchor="t", borders=_b(body_b)),
            tcell(r["vis"], size=MESSAGE_11PT, bold=True, color=txt, fill=fill,
                  align="ctr", anchor="ctr", borders=_b(body_b)),
            tcell(r["where"], size=DENSE_BODY_10PT, color=DK, align="l",
                  anchor="t", borders=_b(body_b)),
        ]
        rows.append(trow(cells, h=row_h[ri + 1]))

    return table(30, "TriadTable", BODY_X, _TBL_Y, BODY_CX, sum(row_h),
                 col_widths=_COL_W, rows=rows)


def _commentary() -> str:
    """Commentary 2 (focal filled BD-doors card, lower-left) + Commentary 3
    (muted data-observability note, right)."""
    gap = 200_000
    left_w = 6_400_000
    right_x = BODY_X + left_w + gap
    right_w = BODY_R - right_x

    # Commentary 2 - the one focal filled callout (soft BLUE_1, 1pt black border).
    c2 = text_box(
        40, "BDDoorsCard", BODY_X, _CMT_Y, left_w, _CMT_H,
        [paragraph([run("Each “who” is a different door for business "
                        "development.",
                        size=MESSAGE_11PT, bold=True, color=DK, font=FONT)],
                   space_after=400),
         paragraph([run("Shape the requirement with the user and requirements side "
                        "(theater commands, Futures Command CFTs); win the award "
                        "through the contracting office and its OTA and CSO "
                        "pathways; confirm the money in the program office's budget "
                        "lines.",
                        size=LABEL_9PT, color=DK, font=FONT)])],
        anchor="t", fill=BLUE_1, line_color=BLACK, line_width=12_700,
        insets=INSETS_CARD)

    # Commentary 3 - muted note tied to the Visibility column (GRAY_1 + GRAY_3).
    c3 = text_box(
        41, "DataObservabilityNote", right_x, _CMT_Y, right_w, _CMT_H,
        [paragraph([run("The three are not equally observable in the data.",
                        size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT)],
                   space_after=300),
         paragraph([run("The buyer falls straight out of the contract number; the "
                        "payer is recoverable to the appropriation account via the "
                        "Treasury Account Symbol; the end-user usually is not in "
                        "contract data at all and must be sourced externally (open "
                        "program reporting, demos, requirements docs).",
                        size=FINEPRINT_8_5PT, color=DK, font=FONT)])],
        anchor="t", fill=GRAY_1, line_color=GRAY_3, line_width=9_525,
        insets=(120_000, 90_000, 120_000, 90_000))

    return c2 + c3


def _body() -> str:
    return _band() + _lead() + _triad_table() + _commentary()


def render() -> str:
    """Assemble chrome + body into a complete <p:sld> (no page number; auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
