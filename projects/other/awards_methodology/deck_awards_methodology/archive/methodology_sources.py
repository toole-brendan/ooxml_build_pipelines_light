"""methodology_sources - the credibility slide: where federal award data comes
from (four free government API families across the contract lifecycle), the
triangulation rule (FPDS wins ties), and the honest limits (subaward blindness,
reporting lag, operational gotchas).

Style + chrome rules: deck_core/slide_guide.md. Builders imported from
deck_core.primitives; tokens from deck_core.style.

Read (top -> bottom): lifecycle swim-lane -> API-at-a-glance table ->
triangulation finding + caution card + operational-gotcha chips.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, tcell, trow,
    connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_3, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_5,
    DK, WHITE, BLACK, PRELIM, FONT,
    INSETS_EVIDENCE,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT,
    MESSAGE_11PT,
)
from deck_core import text_metrics as _tm

LAYOUT = "slideLayout4"   # body slide; auto-numbers

# ── chrome text ──────────────────────────────────────────────────────────────
_SECTION  = "Methodology"
_TOPIC    = "Sources and trust"
_TAKEAWAY = "Four free federal APIs, triangulated, with FPDS as ground truth"
_SOURCES  = ("Sources: (1) API docs: open.gsa.gov/api (SAM.gov Contract Awards, "
             "Subawards, Opportunities, Entity), api.usaspending.gov/docs, fpds.gov; "
             "(2) Army Market Mapping workbook (quota tiers, source clocks); "
             "(3) Federal Award API Research Methodology (internal)")


# ── helpers ──────────────────────────────────────────────────────────────────

_INSETS_NONE = (0, 0, 0, 0)   # structural labels carry no inset


def _lane_label(sp_id, name, x, y, cx, cy, stage, lane_title):
    """A swim-lane header: small stage cap (ALL CAPS) over the lane name.
    No fill / no border - it is a structural label, not an object."""
    return text_box(
        sp_id, name, x, y, cx, cy,
        [
            paragraph([run(stage, size=FINEPRINT_8_5PT, bold=True, italic=True,
                           color=GRAY_5, font=FONT)],
                      space_after=200),
            paragraph([run(lane_title, size=LABEL_9PT, bold=True, color=DK,
                           font=FONT)]),
        ],
        fill=None, line_color="none", insets=_INSETS_NONE, anchor="t",
    )


def _api_chip(sp_id, name, x, y, cx, cy, label, *, fill, txt, authoritative=False,
              border_w=12700):
    """A small API chip inside a lane: filled rect, 1pt black border, centered
    label. `authoritative=True` adds a tiny italic tag line under the name."""
    paras = [paragraph([run(label, size=LABEL_9PT, bold=True, color=txt,
                            font=FONT)], align="ctr")]
    if authoritative:
        paras.append(paragraph([run("authoritative", size=SOURCES_8PT,
                                    italic=True, color=txt, font=FONT)],
                               align="ctr", space_after=0))
    return text_box(
        sp_id, name, x, y, cx, cy, paras,
        fill=fill, line_width=border_w, anchor="ctr",
        insets=(45_720, 18_000, 45_720, 18_000),
    )


# ── body ─────────────────────────────────────────────────────────────────────

def _body() -> str:
    out = []
    sp = 10  # body shape ids start at 10

    GAP = 91_440  # 0.10in standard gap

    # ===================================================================
    # BAND 1 — Lifecycle swim-lane (top)
    # ===================================================================
    lane_y = BODY_Y
    lane_label_h = 470_000
    chip_h = 300_000
    chip_top = lane_y + lane_label_h
    band1_b = chip_top + chip_h            # bottom of swim-lane band

    # Four lifecycle lanes, content-weighted widths (Prime award is widest: it
    # carries three chips and sits above the prime-feed table rows). Widths sum
    # to BODY_CX with three inter-lane gaps.
    lane_gap = 110_000
    w_pre   = 1_950_000
    w_sub   = 2_750_000
    w_ent   = 1_950_000
    w_prime = BODY_CX - (w_pre + w_sub + w_ent) - 3 * lane_gap

    x_pre   = BODY_X
    x_prime = x_pre + w_pre + lane_gap
    x_sub   = x_prime + w_prime + lane_gap
    x_ent   = x_sub + w_sub + lane_gap

    lanes = [
        (x_pre,   w_pre,   "PRE-AWARD",        "Pipeline"),
        (x_prime, w_prime, "PRIME AWARD",      "Award actions"),
        (x_sub,   w_sub,   "SUB-TIER",         "Subcontracts"),
        (x_ent,   w_ent,   "ENTITY",           "Resolution"),
    ]
    for (lx, lw, stage, ltitle) in lanes:
        out.append(_lane_label(sp, f"Lane {stage}", lx, lane_y, lw, lane_label_h,
                               stage, ltitle))
        sp += 1

    # thin rule under the lane labels, lane-wide, to carry the swim-lane read
    # without a filled header bar
    rule_y = lane_y + lane_label_h - 40_000
    out.append(connector(sp, "Lane rule", BODY_X, rule_y, BODY_CX, 0,
                         color=GRAY_3, width=9_525))
    sp += 1

    # chips inside each lane
    # Pre-award: 1 chip
    out.append(_api_chip(sp, "Chip SAM Opportunities", x_pre, chip_top, w_pre, chip_h,
                         "SAM Opportunities", fill=GRAY_1, txt=DK))
    sp += 1

    # Prime award: 3 chips (FPDS authoritative, SAM Contract Awards, USAspending)
    cgap = 70_000
    cw = (w_prime - 2 * cgap) // 3
    prime_chips = [
        ("FPDS Atom", BLUE_5, WHITE, True, 19_050),       # authoritative -> focal 1.5pt
        ("SAM Contract Awards", BLUE_3, WHITE, False, 12_700),
        ("USAspending", BLUE_1, DK, False, 12_700),
    ]
    for i, (lbl, fill, txt, auth, bw) in enumerate(prime_chips):
        cx_i = x_prime + i * (cw + cgap)
        out.append(_api_chip(sp, f"Chip {lbl}", cx_i, chip_top, cw, chip_h,
                             lbl, fill=fill, txt=txt, authoritative=auth,
                             border_w=bw))
        sp += 1

    # Sub-tier: 2 chips
    sgap = 70_000
    sw = (w_sub - sgap) // 2
    sub_chips = [("SAM Subaward (FFATA)", GRAY_2, DK), ("USAspending subawards", GRAY_1, DK)]
    for i, (lbl, fill, txt) in enumerate(sub_chips):
        cx_i = x_sub + i * (sw + sgap)
        out.append(_api_chip(sp, f"Chip {lbl}", cx_i, chip_top, sw, chip_h,
                             lbl, fill=fill, txt=txt))
        sp += 1

    # Entity: 1 chip
    out.append(_api_chip(sp, "Chip SAM Entity", x_ent, chip_top, w_ent, chip_h,
                         "SAM Entity Mgmt", fill=GRAY_1, txt=DK))
    sp += 1

    # ===================================================================
    # BAND 2 — API-at-a-glance table (middle)
    # ===================================================================
    tbl_y = band1_b + GAP + 30_000
    col_w = [2_000_000, 3_300_000, 880_000, 1_780_000, 3_322_362]  # sums to BODY_CX

    # Plain-text grid (used only to size rows honestly via the shared estimator;
    # the rendered cells carry the real fills/bold below). The API column and
    # several first cells render at 9pt, so size at 9pt to match the probe.
    grid_text = [
        ["API", "What it gives you", "API key?", "Daily quota", "Best for"],
        ["FPDS Atom feed", "Authoritative prime award actions (XML, per mod)",
         "No", "–", "Ground-truth obligations; discovery by NAICS / PSC / vendor"],
        ["USAspending", "Enriched awards, transactions, funding accounts (JSON)",
         "No", "–", "FY breakdowns; funding TAS; PIID lookups"],
        ["SAM Contract Awards API", "Modern structured prime + IDV awards (JSON / CSV)",
         "Yes", "10 / 1,000 / 10,000 by tier", "Vehicle ceiling + ordering-period; bulk extracts"],
        ["SAM Subaward Reporting", "First-tier subcontracts, FFATA (per prime)",
         "Yes", "(same tiers)", "The supplier layer under a prime"],
        ["SAM Opportunities", "Solicitations / pre-award notices",
         "Yes", "(same tiers)", "The not-yet-awarded pipeline"],
        ["SAM Entity Management", "UEI → NAICS / CAGE / registration",
         "Yes", "(same tiers)", "Enriching / resolving top vendors"],
    ]
    row_h = _tm.estimate_row_heights(grid_text, col_w, size_pt=9.0,
                                     header_size_pt=9.0)

    # cell-builder shortcuts
    def hcell(text, align="l"):
        # header: bold, 1.5pt black bottom rule (cascading-border pattern)
        return tcell(text, size=LABEL_9PT, bold=True, color=DK, align=align,
                     fill=None,
                     borders={"B": {"color": BLACK, "width": 19_050},
                              "T": "none", "L": "none", "R": "none"})

    def bcell(text, *, align="l", bold=False, fill=None, color=DK,
              size=FINEPRINT_8_5PT, last=False):
        b = {"T": "none", "L": "none", "R": "none"}
        b["B"] = "none" if last else {"color": GRAY_3, "width": 9_525}
        return tcell(text, size=size, bold=bold, color=color, align=align,
                     fill=fill, borders=b)

    # "No" is the low-friction case -> soft positive tint (BLUE_1). FPDS row
    # gets a subtle emphasis fill (it is ground truth) on the API + key cells.
    NO_FILL  = BLUE_1
    FPDS_EMPH = GRAY_1

    rows = [
        trow([hcell("API"), hcell("What it gives you"),
              hcell("API key?", align="ctr"), hcell("Daily quota"),
              hcell("Best for")], h=row_h[0]),

        trow([bcell("FPDS Atom feed", bold=True, fill=FPDS_EMPH, size=LABEL_9PT),
              bcell("Authoritative prime award actions (XML, per mod)"),
              bcell("No", align="ctr", fill=NO_FILL, bold=True),
              bcell("–", align="ctr", size=LABEL_9PT),
              bcell("Ground-truth obligations; discovery by NAICS / PSC / vendor")],
             h=row_h[1]),

        trow([bcell("USAspending", bold=True, size=LABEL_9PT),
              bcell("Enriched awards, transactions, funding accounts (JSON)"),
              bcell("No", align="ctr", fill=NO_FILL, bold=True),
              bcell("–", align="ctr", size=LABEL_9PT),
              bcell("FY breakdowns; funding TAS; PIID lookups")],
             h=row_h[2]),

        trow([bcell("SAM Contract Awards API", bold=True, size=LABEL_9PT),
              bcell("Modern structured prime + IDV awards (JSON / CSV)"),
              bcell("Yes", align="ctr"),
              bcell("10 / 1,000 / 10,000 by tier", size=SOURCES_8PT),
              bcell("Vehicle ceiling + ordering-period; bulk extracts")],
             h=row_h[3]),

        trow([bcell("SAM Subaward Reporting", bold=True, size=LABEL_9PT),
              bcell("First-tier subcontracts, FFATA (per prime)"),
              bcell("Yes", align="ctr"),
              bcell("(same tiers)", size=SOURCES_8PT),
              bcell("The supplier layer under a prime")],
             h=row_h[4]),

        trow([bcell("SAM Opportunities", bold=True, size=LABEL_9PT),
              bcell("Solicitations / pre-award notices"),
              bcell("Yes", align="ctr"),
              bcell("(same tiers)", size=SOURCES_8PT),
              bcell("The not-yet-awarded pipeline")],
             h=row_h[5]),

        trow([bcell("SAM Entity Management", bold=True, size=LABEL_9PT, last=True),
              bcell("UEI → NAICS / CAGE / registration", last=True),
              bcell("Yes", align="ctr", last=True),
              bcell("(same tiers)", size=SOURCES_8PT, last=True),
              bcell("Enriching / resolving top vendors", last=True)],
             h=row_h[6]),
    ]
    tbl_h = sum(row_h)
    out.append(table(sp, "API table", BODY_X, tbl_y, BODY_CX, tbl_h,
                     col_widths=col_w, rows=rows))
    sp += 1
    tbl_b = tbl_y + tbl_h

    # ===================================================================
    # BAND 3 — Triangulation finding + caution card + gotcha chips (bottom)
    # ===================================================================
    rail_y = tbl_b + GAP + 20_000
    gotcha_h = 250_000
    gotcha_y = BODY_B - gotcha_h
    rail_b = gotcha_y - 60_000             # rail/card bottom sits above chips
    rail_h = rail_b - rail_y

    # Left: filled caution card (Commentary 2 - the most important limitation).
    card_w = 4_350_000
    out.append(text_box(
        sp, "Caution card", BODY_X, rail_y, card_w, rail_h,
        [
            paragraph([run("A PRIME FEED CANNOT EXPOSE SUBAWARD GAPS",
                           size=LABEL_9PT, bold=True, color=DK, font=FONT)],
                      space_after=300),
            paragraph([
                run("First-tier subcontracts are a separate, lagging universe: "
                    "multi-billion workshare can be structurally invisible in "
                    "prime data (the HII / GDEB submarine co-build is the "
                    "canonical case). ", size=FINEPRINT_8_5PT, color=DK, font=FONT),
                run("Recover it via FFATA subawards and issuer disclosures, not "
                    "the prime feeds.", size=FINEPRINT_8_5PT, bold=True, color=DK,
                    font=FONT),
            ]),
        ],
        fill=PRELIM, line_width=19_050, anchor="t", insets=INSETS_EVIDENCE,
    ))
    sp += 1

    # Right: no-fill triangulation rail (Commentary 1 - bold finding + explain).
    rail_x = BODY_X + card_w + 200_000
    rail_w = BODY_R - rail_x
    out.append(text_box(
        sp, "Triangulation rail", rail_x, rail_y, rail_w, rail_h,
        [
            paragraph([run("Triangulate; FPDS wins ties.", size=MESSAGE_11PT,
                           bold=True, color=DK, font=FONT)],
                      space_after=300),
            paragraph([
                run("FPDS is the authoritative prime-award record and USAspending "
                    "is derived from it, so FPDS is ground truth when they "
                    "disagree. Subawards lag primes 6–18 months with "
                    "compliance gaps; SAM Opportunities covers what is not yet "
                    "awarded. The SAM Contract Awards API (2025) is the modern "
                    "structured replacement for the FPDS Atom feed.",
                    size=FINEPRINT_8_5PT, color=DK, font=FONT)],
                      space_after=250),
            paragraph([
                run("Keep the money universes separate: ", size=FINEPRINT_8_5PT,
                    bold=True, color=DK, font=FONT),
                run("prime obligations, funded budget demand, and subawards are "
                    "distinct, as are obligation / current value / ceiling within "
                    "a contract. Never sum across them.",
                    size=FINEPRINT_8_5PT, italic=True, color=GRAY_5, font=FONT)],
            ),
        ],
        fill=None, line_color="none", anchor="t", insets=(0, 0, 0, 0),
    ))
    sp += 1

    # Bottom: three operational-gotcha chips, small, monospace, subordinate.
    gotchas = [
        "PIID = UPPERCASE, no dashes (reversed 2026-06-21; lowercase returns 0 records)",
        "Sum per-mod obligations, never cumulative totals",
        "Subaward reporting lags 6–18 months",
    ]
    ggap = 80_000
    # weight the first chip wider (it carries the longest note)
    gw0 = 5_350_000
    gw_rest = (BODY_CX - gw0 - 2 * ggap) // 2
    gxs = [BODY_X, BODY_X + gw0 + ggap, BODY_X + gw0 + ggap + gw_rest + ggap]
    gws = [gw0, gw_rest, gw_rest]
    for i, (gt, gx, gw) in enumerate(zip(gotchas, gxs, gws)):
        out.append(text_box(
            sp, f"Gotcha {i+1}", gx, gotcha_y, gw, gotcha_h,
            [paragraph([run(gt, size=SOURCES_8PT, color=DK, font=FONT)],
                       align="l")],
            fill=GRAY_1, line_color=GRAY_3, line_width=9_525, anchor="ctr",
            insets=(91_440, 18_000, 91_440, 18_000),
        ))
        sp += 1

    return "".join(out)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld> (no page number; auto)."""
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
