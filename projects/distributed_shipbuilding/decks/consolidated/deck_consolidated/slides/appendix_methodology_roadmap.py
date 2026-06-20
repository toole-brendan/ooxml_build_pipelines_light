"""appendix_methodology_roadmap - the appendix opener: a shape-built roadmap that
orients the reader before the detailed method pages.

One left-to-right calculation chain - Retained Budget Base -> Supplier-Share
Conversion -> the FIXED SUPPLIER TAM handoff -> Evidence Classifier -> Allocation
and Scenario Views - with two chapter bands (TAM chapter builds the fixed dollar
pool; SAM chapter allocates it) above the nodes. Below the rail: three reader-key
/ formula chips that define the vocabulary once, two no-fill bold-led commentary
findings, and a full-width dark guardrail strip. No chart, no native table - the
audit ledgers live on the later method pages. This is the reader's map for the
appendix.

Spec: specs/distributed_shipbuilding/methodology/alternative_v3/
appendix_methodology_roadmap_spec.md (APPENDIX M1 - METHODOLOGY ROADMAP).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CAP_12PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Methodology Roadmap"
_TOPIC            = "Methodology (1/5)"
_TAKEAWAY = ("TAM creates the fixed supplier pool; SAM slices it without "
             "resizing the market.")
_SOURCES = ("Sources: (1) Navy SCN budget justification books, FY2022–FY2027; "
            "(2) DoD/DoW contract-announcement POP corpus, CY2022–CY2026; "
            "(3) SAM.gov FSRS / FFATA subawards and SAM.gov / USAspending "
            "UEI / NAICS enrichment, FY2017–FY2026")

# Raw point sizes with no exact token (style.py allows raw sizes with a nearby note).
_EVID_95  = 950    # 9.5pt: commentary finding sentence (spec typography)
_CHAP_SZ  = 1000   # 10pt: chapter-band cap (spec: white Arial 10pt bold)

# Intra-shape paragraph spacing (1/100 pt). Generous gaps so the distinct lines
# inside a node / chip / commentary block read as separate, not crowded.
_GAP_HEAD = 300    # 3.0pt: header line -> body block
_GAP_ITEM = 240    # 2.4pt: between stacked body items
_GAP_CHIP = 320    # 3.2pt: chip body -> formula line
_GAP_FIND = 300    # 3.0pt: commentary finding -> supporting bullet
_GAP_CAP  = 360    # 3.6pt: handoff cap -> subline


# ── Roadmap horizontal geometry (all EMU) ────────────────────────────────────
# One left-to-right chain of five slots: M2, M3, [handoff], M4, M5. Four equal
# connector gaps carry the arrows; the central handoff slot is wider so it reads
# as the dominant node. Slot lefts are derived so the last node closes on BODY_R.
_GAP_C        = 300_000      # horizontal arrow gap between adjacent nodes (~0.33in)
_HAND_EXTRA_W = 600_000      # handoff node is this much wider than a regular node
_W_N = (BODY_CX - 4 * _GAP_C - _HAND_EXTRA_W) // 5   # regular node width
_W_H = _W_N + _HAND_EXTRA_W                          # handoff node width

_SLOT_W = [_W_N, _W_N, _W_H, _W_N, _W_N]
_LEFTS: list[int] = []
_cur = BODY_X
for _w in _SLOT_W:
    _LEFTS.append(_cur)
    _cur += _w + _GAP_C
# Close any integer-division drift onto the final node so M5 ends exactly at BODY_R.
_SLOT_W[-1] = BODY_R - _LEFTS[-1]
_HAND_X = _LEFTS[2]


# ── Roadmap vertical geometry (all EMU) ──────────────────────────────────────
# Five stacked bands inside BODY with intentional whitespace between them:
# caption, roadmap rail, reader-key chips, commentary, guardrail (pinned bottom).
_CAP_Y, _CAP_H = BODY_Y, 240_000                     # italic evidence-window caption

_CH_Y, _CH_H = 1_701_600, 300_000                    # two chapter bands (above nodes)

_NODE_Y, _NODE_H = 2_151_600, 860_000                # the four regular nodes
_HAND_OVER = 110_000                                 # handoff overhang above/below
_HAND_Y = _NODE_Y - _HAND_OVER                       # handoff is taller, vertically centered
_HAND_H = _NODE_H + 2 * _HAND_OVER
_HAND_B = _HAND_Y + _HAND_H
_CONN_Y = _NODE_Y + _NODE_H // 2                     # connector + handoff vertical center

_CAP2_Y, _CAP2_H = _HAND_B + 24_000, 200_000         # "TAM ends here; SAM starts here."

_FORM_Y, _FORM_H = 3_455_600, 980_000                # three reader-key / formula chips
_CHIP_GAP = 100_000
_CHIP_W = (BODY_CX - 2 * _CHIP_GAP) // 3

_COMM_Y, _COMM_H = 4_545_600, 620_000                # two no-fill commentary findings
_COMM_GAP = 260_000
_COMM_W = (BODY_CX - _COMM_GAP) // 2

_GUARD_H = 500_000                                   # full-width dark guardrail strip
_GUARD_Y = BODY_B - _GUARD_H


# ── Content ──────────────────────────────────────────────────────────────────
# Regular milestone nodes: (id, slot, header, [body lines], fill). Pale BLUE_1 and
# mid BLUE_2 fills alternate; the central handoff (slot 2) is rendered apart. The
# step numbers (M2-M5) are internal slide notations, so they stay out of the copy.
_NODES = [
    (20, 0, "Retained budget base",
     ["Budget streams + scope gates",
      "Basic Construction and AP/LLTM treatment"], BLUE_1),
    (21, 1, "Supplier-share conversion",
     ["POP evidence estimates outsourced share",
      "Program-specific TAM build"], BLUE_2),
    (22, 3, "Evidence classifier",
     ["FFATA / FSRS → PIID scope → UEI entity",
      "Role filter + work-type home"], BLUE_1),
    (23, 4, "Allocation + scenarios",
     ["Fixed TAM × bucket share",
      "Scenario views from one pool"], BLUE_2),
]

# Reader-key chips: (id, header, body, formula). Fills alternate GRAY_1 / BLUE_1 /
# GRAY_1 so the chips clarify the rail without competing with the handoff.
_CHIPS = [
    (50, "Supplier-share factor",
     "Conversion rate showing how many cents of each retained budget dollar "
     "become outsourced supplier work.",
     "Retained budget base × supplier-share factor = fixed supplier TAM", GRAY_1),
    (51, "Work-type home",
     "One mutually exclusive classification for each retained supplier dollar; "
     "unresolved supplier work stays residual.",
     "Fixed TAM × bucket share = work-type TAM", BLUE_1),
    (52, "Scenario view",
     "An overlapping leadership lens on the same fixed TAM pool; broad, HM&E, "
     "metal, electrical, and modular should not be added.",
     "Scenario SAM = SUMPRODUCT(bucket TAM, inclusion flag)", GRAY_1),
]

# Commentary: (id, x, finding, supporting bullet). Award evidence moves allocation,
# not headline size - the two questions TAM and SAM answer.
_FINDINGS = [
    (60, BODY_X,
     "TAM and SAM answer different questions.",
     "TAM sizes how much outsourced supplier-addressable new-construction work "
     "exists; SAM identifies which work-type slices are serviceable inside that "
     "fixed pool."),
    (61, BODY_X + _COMM_W + _COMM_GAP,
     "Award evidence moves allocation, not headline size.",
     "PIID, UEI, registry, role filters, residual treatment, and scenario flags "
     "can move bucket shares and scenario SAM, but not budget-derived TAM."),
]

_GUARD_LEAD = "Guardrails: "
_GUARD_BODY = ("POP evidence creates supplier-share factors, not a summed award "
               "numerator. FFATA / FSRS evidence creates mix percentages, not "
               "market size. Scenario views overlap and should not be added.")


# ── Local helpers ────────────────────────────────────────────────────────────
def _node(sp_id: int, x: int, header: str, lines: list[str], fill: str) -> str:
    """A filled milestone node: 9pt bold header line over 8.5pt body lines, top
    anchored, with clear gaps between the header and each body item. Every filled
    shape carries the house 1pt black border."""
    paras = [paragraph([run(header, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                       space_after=_GAP_HEAD, line_spacing=108_000)]
    for i, ln in enumerate(lines):
        paras.append(paragraph(
            [run(ln, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
            space_after=(0 if i == len(lines) - 1 else _GAP_ITEM), line_spacing=105_000))
    return text_box(sp_id, "MethodNode", x, _NODE_Y, _W_N, _NODE_H, paras,
                    fill=fill, line_width=12_700, anchor="t",
                    insets=(80_000, 72_000, 80_000, 60_000))


def _handoff(sp_id: int) -> str:
    """Central handoff node - the darkest and largest object: 12pt bold all-caps
    cap over a 10pt body, white on BLUE_5, with the one 1.5pt focal border."""
    return text_box(
        sp_id, "FixedSupplierTAM", _HAND_X, _HAND_Y, _W_H, _HAND_H,
        [paragraph([run("FIXED SUPPLIER TAM", size=CAP_12PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr", space_after=_GAP_CAP),
         paragraph([run("The only dollar pool SAM can slice", size=DENSE_BODY_10PT,
                        color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, line_width=19_050, anchor="ctr", insets=INSETS_CARD)


def _chapter_band(sp_id: int, x: int, w: int, text: str) -> str:
    """Chapter cap above a pair of nodes: white 10pt bold on BLUE_4, 1pt border."""
    return text_box(
        sp_id, "ChapterBand", x, _CH_Y, w, _CH_H,
        [paragraph([run(text, size=_CHAP_SZ, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_4, line_width=12_700, anchor="ctr",
        insets=(120_000, 40_000, 120_000, 40_000))


def _formula_paragraph(text: str) -> str:
    """Formula line: 8.5pt, with the bare × / = operators bolded inline (the spec's
    optional operator emphasis, kept as text runs rather than separate shapes)."""
    toks = text.split(" ")
    runs = []
    for i, tok in enumerate(toks):
        is_op = tok in ("×", "=")
        suffix = "" if i == len(toks) - 1 else " "
        runs.append(run(tok + suffix, size=FINEPRINT_8_5PT, bold=is_op,
                        color=BLACK, font=FONT))
    return paragraph(runs, line_spacing=110_000)


def _chip(sp_id: int, x: int, header: str, body: str, formula: str, fill: str) -> str:
    """Reader-key chip: 9pt bold header, 8.5pt definition body, 8.5pt formula line,
    with clear gaps separating the three blocks."""
    return text_box(
        sp_id, "ReaderKeyChip", x, _FORM_Y, _CHIP_W, _FORM_H,
        [paragraph([run(header, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=_GAP_HEAD, line_spacing=112_000),
         paragraph([run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
                   space_after=_GAP_CHIP, line_spacing=110_000),
         _formula_paragraph(formula)],
        fill=fill, line_width=12_700, anchor="t",
        insets=(110_000, 90_000, 110_000, 80_000))


def _commentary(sp_id: int, x: int, finding: str, bullet: str) -> str:
    """No-fill / no-border commentary: 9.5pt bold finding over a 9pt supporting
    bullet. Read alone, the bold lines are the page's two takeaways."""
    return text_box(
        sp_id, "Commentary", x, _COMM_Y, _COMM_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=_GAP_FIND, line_spacing=110_000),
         paragraph([run(bullet, size=LABEL_9PT, color=BLACK, font=FONT)],
                   bullet=True, line_spacing=108_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 20_000, 40_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(
            "TAM sizing window FY2022–FY2027; SAM evidence window FY2017–FY2026. "
            "Budget and POP evidence size the dollar pool; award evidence "
            "allocates the pool.",
            size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Horizontal arrows along the chain (painted first, behind the nodes).
    arrows = []
    for i in range(4):
        x_start = _LEFTS[i] + _SLOT_W[i]
        arrows.append(connector(40 + i, f"Arrow{i + 1}", x_start, _CONN_Y,
                                _LEFTS[i + 1] - x_start, 0,
                                color=BLACK, width=12_700, arrow=True))

    # Chapter bands: TAM chapter spans M2+M3; SAM chapter spans M4+M5.
    tam_w = (_LEFTS[1] + _W_N) - _LEFTS[0]
    sam_w = BODY_R - _LEFTS[3]
    chapters = (
        _chapter_band(11, _LEFTS[0], tam_w, "TAM CHAPTER — BUILD THE FIXED DOLLAR POOL")
        + _chapter_band(12, _LEFTS[3], sam_w, "SAM CHAPTER — ALLOCATE THE FIXED POOL")
    )

    # Regular nodes, then the handoff on top.
    nodes = "".join(_node(sp_id, _LEFTS[slot], header, lines, fill)
                    for (sp_id, slot, header, lines, fill) in _NODES)
    handoff = _handoff(30)
    handoff_caption = text_box(
        31, "HandoffCaption", _HAND_X, _CAP2_Y, _W_H, _CAP2_H,
        [paragraph([run("TAM ends here; SAM starts here.", size=FINEPRINT_8_5PT,
                        italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    chips = "".join(_chip(sp_id, BODY_X + i * (_CHIP_W + _CHIP_GAP),
                          header, body, formula, fill)
                    for i, (sp_id, header, body, formula, fill) in enumerate(_CHIPS))

    commentary = "".join(_commentary(sp_id, x, finding, bullet)
                         for (sp_id, x, finding, bullet) in _FINDINGS)

    guardrail = text_box(
        70, "Guardrails", BODY_X, _GUARD_Y, BODY_CX, _GUARD_H,
        [paragraph([
            run(_GUARD_LEAD, size=DENSE_BODY_10PT, bold=True, color=WHITE, font=FONT),
            run(_GUARD_BODY, size=DENSE_BODY_10PT, color=WHITE, font=FONT)])],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Paint order: arrows behind, then chapter bands, nodes, handoff, then the
    # subordinate caption / chips / commentary / guardrail.
    return ("".join(arrows) + chapters + nodes + handoff
            + caption + handoff_caption + chips + commentary + guardrail)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
