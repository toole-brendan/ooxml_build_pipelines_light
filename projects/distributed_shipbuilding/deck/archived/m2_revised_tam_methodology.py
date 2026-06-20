"""m2_revised_tam_methodology - explain how raw Navy new-construction
budget is narrowed into average annual outsourced supplier TAM as a top-to-bottom
narrowing tree.

A shape-built narrowing tree occupies the left ~70%; a stacked method-note rail
occupies the right ~30%; a full-width guardrail spans the bottom. The right rail
is preserved from the prior module; the left tree is re-spaced with taller nodes,
shorter copy, and explicit branch/merge connectors so text fits cleanly and the
flow reads as a decision tree rather than a stacked grid.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_5,
    GRAY_1, GRAY_2, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "TAM Build"
_TOPIC            = "TAM Methodology"
_TAKEAWAY = ("Navy budget is narrowed to average annual outsourced supplier "
             "opportunity.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c shipbuilding budget justification, "
            "FY2022–FY2027; (2) DoD contract-announcement place-of-performance "
            "corpus; (3) program AP/LLTM bridge and assumptions register")

# Operator glyphs the diagram is allowed to use (not separators).
_X = "×"

# Raw point sizes with no exact token (style.py says raw sizes are fine with a
# comment): 7.8pt terminal body, 9.0pt terminal title, 10.5pt focal node title.
_BODY_78PT = 780     # 7.8pt, dense terminal body
_LABEL_90  = 900     # 9pt, terminal-decision label
_TITLE_105 = 1050    # 10.5pt, conversion / output title

# Text rhythm and insets tuned so all tree nodes clear a render-time fit check.
_NODE_LNSPC = 108_000
_NODE_INSETS = (100_000, 50_000, 100_000, 50_000)
_NODE_INSETS_FOCAL = (114_300, 60_000, 114_300, 60_000)
_TERMINAL_INSETS = (60_000, 35_000, 60_000, 35_000)

# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_GAP = 120_000

# Caption (top, no-fill) and guardrail (bottom, full width).
_CAP_Y, _CAP_H = BODY_Y, 300_000
_GUARD_H = 600_000
_GUARD_Y = BODY_B - _GUARD_H

# Middle diagram zone, between caption and guardrail.
_MID_TOP = _CAP_Y + _CAP_H + 65_000
_MID_BOT = _GUARD_Y - 80_000

# Left = tree; Right = method-note rail (~70 / 30 split).
_LEFT_W = 8_000_000
_RAIL_X = BODY_X + _LEFT_W + _GAP
_RAIL_W = BODY_R - _RAIL_X
# Rail text left inset; the divider is centered in the whitespace between the tree's
# right edge and where the rail text begins (not the rail box edge).
_RAIL_LINSET = 137_160
_SEP_X = (BODY_X + _LEFT_W + _RAIL_X + _RAIL_LINSET) // 2

# Two-across positions inside the left zone (streams, gates).
_HALF_W = (_LEFT_W - _GAP) // 2
_L_X = BODY_X
_R_X = BODY_X + _HALF_W + _GAP
_CENTER_X = BODY_X + _LEFT_W // 2
_L_C = _L_X + _HALF_W // 2
_R_C = _R_X + _HALF_W // 2

# Four-across positions for the terminal-decision row.
_Q_GAP = 90_000
_Q_W = (_LEFT_W - 3 * _Q_GAP) // 4
_Q_X = [BODY_X + i * (_Q_W + _Q_GAP) for i in range(4)]
_Q_C = [x + _Q_W // 2 for x in _Q_X]

# Narrowing spine nodes (centred, progressively narrower).
_SC_W = 6_200_000
_SC_X = BODY_X + (_LEFT_W - _SC_W) // 2
_OUT_W = 5_000_000
_OUT_X = BODY_X + (_LEFT_W - _OUT_W) // 2

# Row tops + heights. The tree uses slightly taller upstream nodes and shorter
# gaps than the prior module so every two-line node fits without collisions.
_RG = 70_000
_R1_Y, _R1_H = _MID_TOP, 420_000
_R2_Y, _R2_H = _R1_Y + _R1_H + _RG, 440_000
_R3_Y, _R3_H = _R2_Y + _R2_H + _RG, 440_000
_R4_Y, _R4_H = _R3_Y + _R3_H + _RG, 720_000
_R5_Y, _R5_H = _R4_Y + _R4_H + _RG, 460_000
_R6_Y, _R6_H = _R5_Y + _R5_H + _RG, 520_000
_TREE_BOT = _R6_Y + _R6_H

# Connector posture.
_EDGE_W = 9_525
_EDGE = BLACK
_EDGE_SOFT = BLACK


# ── Local helpers ────────────────────────────────────────────────────────────
def _treenode(sp_id, name, x, y, cx, cy, title, body, *, fill, title_size,
              body_size=FINEPRINT_8_5PT, line_width=12_700, fg=BLACK,
              insets=_NODE_INSETS, body_align="ctr"):
    """One tree node: bold centered title plus a smaller body line.
    Shorter paragraph spacing and 108% line spacing avoid visual clipping while
    preserving the source module's filled-rectangle vocabulary."""
    paras = [paragraph([run(title, size=title_size, bold=True, color=fg, font=FONT)],
                       align="ctr", space_after=60, line_spacing=_NODE_LNSPC)]
    if body:
        paras.append(paragraph([run(body, size=body_size, color=fg, font=FONT)],
                               align=body_align, line_spacing=_NODE_LNSPC))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill,
                    line_width=line_width, anchor="ctr", insets=insets)


def _rail(sp_id, x, y, cx, cy, title, bullets):
    """No-fill / no-border method-note rail: preserved from the prior module."""
    paras = [paragraph([run(title, size=LABEL_9PT, bold=True, italic=True,
                            color=BLACK, font=FONT)], space_after=160)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph(
            [run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
             run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
            bullet=True, space_after=(120 if i < len(bullets) - 1 else 0)))
    return text_box(sp_id, "MethodRail", x, y, cx, cy, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(_RAIL_LINSET, 50_000, 50_000, 50_000))


def _v(sp_id, name, x, y1, y2, *, color=_EDGE, width=_EDGE_W, dashed=False):
    return connector(sp_id, name, x, y1, 0, y2 - y1, color=color,
                     width=width, dashed=dashed)


def _h(sp_id, name, x1, x2, y, *, color=_EDGE, width=_EDGE_W, dashed=False):
    return connector(sp_id, name, x1, y, x2 - x1, 0, color=color,
                     width=width, dashed=dashed)


def _branch_connectors() -> str:
    """Quiet connectors behind nodes. Drawn before the shapes so edges never
    cover labels; no arrowheads because all node gaps are short."""
    parts = []

    # Top input split into the two budget streams.
    y_split = _R1_Y + _R1_H + _RG // 2
    parts += [
        _v(50, "InputToSplit", _CENTER_X, _R1_Y + _R1_H, y_split),
        _h(51, "SplitBar", _L_C, _R_C, y_split),
        _v(52, "SplitToBasic", _L_C, y_split, _R2_Y),
        _v(53, "SplitToApLltm", _R_C, y_split, _R2_Y),
    ]

    # Streams drop into their gates.
    parts += [
        _v(54, "BasicToScope", _L_C, _R2_Y + _R2_H, _R3_Y),
        _v(55, "ApLltmToIncrementality", _R_C, _R2_Y + _R2_H, _R3_Y),
    ]

    # Each gate resolves into two terminal decisions.
    y_scope_split = _R3_Y + _R3_H + _RG // 2
    parts += [
        _v(56, "ScopeGateToSplit", _L_C, _R3_Y + _R3_H, y_scope_split),
        _h(57, "ScopeSplitBar", _Q_C[0], _Q_C[1], y_scope_split),
        _v(58, "ScopeToIncluded", _Q_C[0], y_scope_split, _R4_Y),
        _v(59, "ScopeToExcluded", _Q_C[1], y_scope_split, _R4_Y),
        _v(60, "IncrementalityGateToSplit", _R_C, _R3_Y + _R3_H, y_scope_split),
        _h(61, "IncrementalitySplitBar", _Q_C[2], _Q_C[3], y_scope_split),
        _v(62, "IncrementalityToAdditive", _Q_C[2], y_scope_split, _R4_Y),
        _v(63, "IncrementalityToReference", _Q_C[3], y_scope_split, _R4_Y),
    ]

    # Only the blue included/additive paths feed supplier conversion; gray
    # terminal cards are boundary/reference decisions and do not merge.
    y_merge = _R4_Y + _R4_H + _RG // 2
    parts += [
        _v(64, "IncludedFeed", _Q_C[0], _R4_Y + _R4_H, y_merge),
        _v(65, "AdditiveFeed", _Q_C[2], _R4_Y + _R4_H, y_merge),
        _h(66, "SupplierMergeBar", _Q_C[0], _Q_C[2], y_merge),
        _v(67, "MergeToSupplierConversion", _CENTER_X, y_merge, _R5_Y),
        _v(68, "SupplierToPortfolio", _CENTER_X, _R5_Y + _R5_H, _R6_Y),
        # Subtle dead-end ticks make the off-spine terminal decisions read as
        # boundaries without visually joining them to the supplier path.
        _v(69, "ExcludedBoundaryTick", _Q_C[1], _R4_Y + _R4_H, y_merge,
           color=_EDGE_SOFT, width=6_350, dashed=True),
        _v(70, "ReferenceBoundaryTick", _Q_C[3], _R4_Y + _R4_H, y_merge,
           color=_EDGE_SOFT, width=6_350, dashed=True),
    ]
    return "".join(parts)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    # Caption with the TAM(FY) formula.
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_R - BODY_X, _CAP_H,
        [paragraph([
            run("Sizing window FY2022–FY2027, nominal then-year. ",
                size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT),
            run(f"TAM(FY) = Basic Construction base {_X} supplier coefficient, "
                "with incremental AP/LLTM added only where the program boundary allows. ",
                size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT),
            run("Programs are computed separately; dollar outputs are summed.",
                size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Row 1 — top node (full width, BLUE_5, white, 1pt border).
    top = _treenode(
        20, "TopNode", BODY_X, _R1_Y, _LEFT_W, _R1_H,
        "NAVY NEW-CONSTRUCTION BUDGET INPUTS",
        "SCN and P-5c construction streams for DDG and submarine programs.",
        fill=BLUE_5, title_size=MESSAGE_11PT, body_size=FINEPRINT_8_5PT,
        line_width=12_700, fg=WHITE, insets=_NODE_INSETS_FOCAL, body_align="ctr")

    # Row 2 — two stream branches.
    streams = (
        _treenode(21, "BasicConstructionStream", _L_X, _R2_Y, _HALF_W, _R2_H,
                  "BASIC CONSTRUCTION STREAM",
                  "Primary new-construction budget base.",
                  fill=BLUE_2, title_size=DENSE_BODY_10PT,
                  insets=_NODE_INSETS, body_align="ctr")
        + _treenode(22, "ApLltmEoqStream", _R_X, _R2_Y, _HALF_W, _R2_H,
                    "AP/LLTM STREAM",
                    "Advance procurement, long-lead material, and EOQ; add only if incremental.",
                    fill=BLUE_1, title_size=DENSE_BODY_10PT,
                    insets=_NODE_INSETS, body_align="ctr"))

    # Row 3 — one gate on each branch (GRAY_1).
    gates = (
        _treenode(23, "ScopeGate", _L_X, _R3_Y, _HALF_W, _R3_H,
                  "SCOPE GATE",
                  "Keep supplier-addressable work inside new construction.",
                  fill=GRAY_1, title_size=DENSE_BODY_10PT,
                  insets=_NODE_INSETS, body_align="ctr")
        + _treenode(24, "IncrementalityGate", _R_X, _R3_Y, _HALF_W, _R3_H,
                    "INCREMENTALITY GATE",
                    "Avoid double-counting dollars already in Basic Construction.",
                    fill=GRAY_1, title_size=DENSE_BODY_10PT,
                    insets=_NODE_INSETS, body_align="ctr"))

    # Row 4 — terminal decisions. Included / additive feed the spine (BLUE_2);
    # excluded / reference-only are quieter, off-spine boundaries (GRAY_2).
    terminal = (
        _treenode(25, "IncludedSupplierPath", _Q_X[0], _R4_Y, _Q_W, _R4_H,
                  "INCLUDED SUPPLIER PATH",
                  "Outsourced component work outside prime, co-prime, and GFE footprint.",
                  fill=BLUE_2, title_size=_LABEL_90, body_size=_BODY_78PT,
                  insets=_TERMINAL_INSETS, body_align="l")
        + _treenode(26, "ExcludedScopePath", _Q_X[1], _R4_Y, _Q_W, _R4_H,
                    "EXCLUDED SCOPE",
                    "Prime and co-prime self-perform; GFE and GFP; mission systems, "
                    "weapons, nuclear plant, sustainment, design, services, and FMS.",
                    fill=GRAY_2, title_size=_LABEL_90, body_size=_BODY_78PT,
                    insets=_TERMINAL_INSETS, body_align="l")
        + _treenode(27, "AdditivePath", _Q_X[2], _R4_Y, _Q_W, _R4_H,
                    "ADDITIVE WHERE INCREMENTAL",
                    "DDG: filtered AP/LLTM can feed TAM where outside Basic Construction.",
                    fill=BLUE_2, title_size=_LABEL_90, body_size=_BODY_78PT,
                    insets=_TERMINAL_INSETS, body_align="l")
        + _treenode(28, "ReferenceOnlyPath", _Q_X[3], _R4_Y, _Q_W, _R4_H,
                    "REFERENCE ONLY",
                    "Submarine: AP/LLTM is timing and supplier evidence; additive base remains zero.",
                    fill=GRAY_2, title_size=_LABEL_90, body_size=_BODY_78PT,
                    insets=_TERMINAL_INSETS, body_align="l"))

    # Row 5 — supplier conversion (centred, narrower, BLUE_1).
    supplier_conv = _treenode(
        29, "SupplierConversion", _SC_X, _R5_Y, _SC_W, _R5_H,
        "SUPPLIER CONVERSION",
        "DDG: MYP-corrected POP. Submarine: strict non-nuclear, yard-excluded POP.",
        fill=BLUE_1, title_size=_TITLE_105, body_size=FINEPRINT_8_5PT,
        insets=_NODE_INSETS, body_align="ctr")

    # Row 6 — program-specific build merges into the portfolio output (narrowest,
    # BLUE_5, white, 1pt border): sum outputs, not inputs.
    output = _treenode(
        31, "PortfolioSupplierTam", _OUT_X, _R6_Y, _OUT_W, _R6_H,
        "PORTFOLIO SUPPLIER TAM",
        "Build DDG and submarine separately; sum outputs to average annual outsourced supplier opportunity.",
        fill=BLUE_5, title_size=_TITLE_105, body_size=FINEPRINT_8_5PT,
        line_width=12_700, fg=WHITE, insets=_NODE_INSETS_FOCAL, body_align="ctr")

    # Thin separator between the tree and the method-note rail.
    sep = connector(75, "RailSeparator", _SEP_X, _MID_TOP,
                    0, _TREE_BOT - _MID_TOP, color=BLACK, width=9_525)

    # Right rail — TAM method notes and audit points (commentary, not a column).
    rail = _rail(
        80, _RAIL_X, _MID_TOP, _RAIL_W, _TREE_BOT - _MID_TOP,
        "TAM audit points",
        [("Budget anchor:",
          "SCN and P-5c Basic Construction anchor the denominator; total ship "
          "cost and TOA are context."),
         ("Supplier conversion:",
          "POP-derived supplier-location share converts gated non-GFE budget "
          "dollars into outsourced supplier opportunity."),
         ("Program asymmetries:",
          "DDG uses MYP-corrected POP and additive AP/LLTM. Submarine uses a "
          "strict non-nuclear coefficient and AP/LLTM reference-only."),
         ("AP/LLTM boundary:",
          "Additive only where outside Basic Construction; otherwise timing "
          "evidence, not a second numerator."),
         ("Do not confuse:",
          "POP is coefficient evidence; FFATA/FSRS is mix evidence; neither is "
          "the TAM numerator."),
         ("Diligence items:",
          "Supplier coefficient, MYP reconstruction, AP/LLTM treatment, scope "
          "exclusions, and stream toggles.")])

    # Bottom guardrail strip — GRAY_5, white, 1pt black.
    guardrail = text_box(
        90, "Guardrails", BODY_X, _GUARD_Y, BODY_R - BODY_X, _GUARD_H,
        [paragraph([
            run("TAM guardrail: ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run("TAM is the outsourced supplier-addressable new-construction "
                "dollar pool. It is not total ship cost, total Navy budget, "
                "visible award flow, demand forecast, SOM, capture rate, win "
                "probability, pricing haircut, or expected revenue.",
                size=DENSE_BODY_10PT, color=WHITE, font=FONT)])],
        fill=GRAY_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Paint order: connectors + separator behind the nodes; guardrail last.
    return (_branch_connectors() + sep
            + caption + top + streams + gates + terminal + supplier_conv + output
            + rail + guardrail)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
