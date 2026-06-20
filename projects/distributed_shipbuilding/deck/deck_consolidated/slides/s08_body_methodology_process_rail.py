"""s08_body_methodology_process_rail - the primary method ledger: a six-layer
sizing-chain table (Layer / Governing signal / Treatment / Why it matters) read in
build-sequence order, paired with three bold-led findings and one modeling-boundary
guardrail strip.

Pattern A (table-left ~7.8in, commentary-right ~4.2in, full-width boundary strip
below). The governing-rule grid is the page's one primary table, so it carries the
dark BLUE_5 header; it is built on the low-level table() engine (not house_table)
because the spec calls for per-cell sizes the uniform-size house table can't express:
9pt ALL-CAPS header, 8.5pt body, 9pt bold Layer column, plus a single GRAY_1 fill on
the Exclusions-and-residual row. Horizontal rules only (1.5pt under the header, 1pt
under each body row, none under the last), no vertical borders.

Spec: ds_specs/s08_body_methodology_process_rail.txt (SLIDE 08 - METHODOLOGY).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_5, GRAY_1, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, MESSAGE_11PT, EXHIBIT_HEADER_13PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Sizing Methodology"
_BREADCRUMB_TOPIC = "Sizing Chain"
_TOPIC            = "Methodology"
_TAKEAWAY = ("TAM is budget-led, while SAM mix is allocated through one "
             "entity-resolved supplier registry.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c Basic Construction and AP/LLTM budget "
            "justification, FY2022–FY2027; (2) DoD place-of-performance (POP) award "
            "corpus and parent-prime PIID scope; (3) FFATA/FSRS subaward records and "
            "the operating-entity supplier registry, FY2017–FY2026")

# Raw point size with no exact token (style.py allows raw sizes with a nearby note).
_EVID_95 = 950   # 9.5pt: commentary supporting-evidence text (spec typography)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Exhibit header over the table; table-left / commentary-right aligned at the grid
# top; full-width boundary strip below both.
_EXH_Y, _EXH_H = BODY_Y, 300_000               # 13pt bold exhibit header
_GRID_TOP = _EXH_Y + _EXH_H + 70_000           # 1_741_600 — table grid + commentary top

# Primary table (left). Layer is the narrow scan column; Governing signal and
# Treatment carry the most width; Why it matters is compact.
_TABLE_W = 7_150_000                            # ~7.82in
_COL_W   = [1_150_000, 2_100_000, 2_300_000, 1_600_000]   # sum = _TABLE_W
_HDR_H   = 350_000
_ROW_H   = 440_000                              # every body row is two lines -> even grid
_ROW_HEIGHTS = [_HDR_H] + [_ROW_H] * 6
_GRID_H  = sum(_ROW_HEIGHTS)                     # 2_990_000
_GRID_BOT = _GRID_TOP + _GRID_H                 # 4_731_600

# Commentary (right), top-aligned with the table grid.
_GAP_TC  = 280_000
_COMM_X  = BODY_X + _TABLE_W + _GAP_TC          # 7_883_079
_COMM_W  = BODY_R - _COMM_X                     # 3_852_362 (~4.21in)
_COMM_INSETS = (137_160, 30_000, 137_160, 30_000)

# Boundary strip (full width), under both columns.
_BOUND_Y = _GRID_BOT + 220_000                  # 4_951_600
_BOUND_H = 540_000                              # bottom 5_491_600, clear of Sources

# Per-cell type sizes (spec: 9pt caps header, 8.5pt body, 9pt bold Layer column).
_HDR_SZ   = LABEL_9PT          # 900
_BODY_SZ  = FINEPRINT_8_5PT    # 850
_LAYER_SZ = LABEL_9PT          # 900


# ── Content ──────────────────────────────────────────────────────────────────
_HEADERS = ["LAYER", "GOVERNING SIGNAL", "TREATMENT", "WHY IT MATTERS"]

# Six body rows, in build-sequence order (no step numbers; the order is the chain).
_ROWS = [
    ("Budget TAM",
     "SCN Basic Construction and AP/LLTM stream",
     "Build exogenous TAM by program",
     "Classification does not move headline TAM"),
    ("Supplier share",
     "POP corpus",
     "Strip prime, co-prime, GFE, and excluded scope",
     "Converts the budget base into supplier opportunity"),
    ("Supplier mix",
     "Operating entity, SAM-resolved supplier registry",
     "Role first, then bucket; subawards are mix evidence, not market size",
     "One registry classifies DDG and submarine alike"),
    ("Physical buckets",
     "Seven stable work-type buckets",
     "Structural, machining, castings, piping, electrical power, HVAC, coatings",
     "Keeps the two programs comparable"),
    ("Exclusions and residual",
     "Mission systems, service, holding, foreign/FMS, unresolved tail",
     "Route out, or hold residual explicit",
     "Broad SAM does not auto-equal TAM"),
    ("Scenario SAM",
     "Bucket and entity flags",
     "Overlapping cuts: metal, HM&E, electrical, modular, broad",
     "Scenarios are not additive"),
]
_SHADED_ROW = 4   # Exclusions and residual — light gray hold-out fill (the only one)

# Commentary: (bold finding, figure-tied supporting evidence). No label prefixes.
_FINDINGS = [
    ("TAM is fixed by the budget method, not by supplier reclassification.",
     "Supplier TAM is the budget base multiplied by the place-of-performance "
     "supplier share; re-bucketing suppliers changes mix, not the $4.2B headline."),
    ("The same registry governs both programs after role exclusions.",
     "DDG and submarine dollars are classified at the operating-entity level after "
     "mission systems, services, holding companies, foreign/FMS, primes, and GFE "
     "are removed."),
    ("Residual is a modeled result, not a cleanup item.",
     "Unresolved supplier dollars stay in the denominator and dilute bucket shares, "
     "so broad SAM does not automatically equal total TAM."),
]

_BOUND_LEAD = "Modeling boundary: "
_BOUND_BODY = ("electrical means ship power, distribution, and generation; combat "
               "and mission electronics are excluded in the base case. DDG VLS "
               "launch-control is sensitivity, not base scope.")


# ── Local helpers ────────────────────────────────────────────────────────────
def _method_table(sp_id: int) -> str:
    """Primary governing-rule ledger via the low-level table engine: dark header,
    9pt bold Layer column, 8.5pt body, one gray hold-out row, horizontal rules only
    (1.5pt under header, 1pt under each body row, none under the last)."""
    header = trow([
        tcell(h, fill=BLUE_5, color=WHITE, bold=True, size=_HDR_SZ, align="l",
              anchor="ctr", borders={"B": {"color": BLACK, "width": 19_050}})
        for h in _HEADERS
    ], h=_HDR_H)

    body = []
    for ri, (layer, signal, treatment, why) in enumerate(_ROWS):
        last = ri == len(_ROWS) - 1
        bb = {"B": "none"} if last else {"B": {"color": BLACK, "width": 12_700}}
        fill = GRAY_1 if ri == _SHADED_ROW else None
        cells = [
            tcell(layer, fill=fill, color=BLACK, bold=True, size=_LAYER_SZ,
                  align="l", anchor="ctr", borders=bb),
            tcell(signal, fill=fill, color=BLACK, size=_BODY_SZ,
                  align="l", anchor="ctr", borders=bb),
            tcell(treatment, fill=fill, color=BLACK, size=_BODY_SZ,
                  align="l", anchor="ctr", borders=bb),
            tcell(why, fill=fill, color=BLACK, size=_BODY_SZ,
                  align="l", anchor="ctr", borders=bb),
        ]
        body.append(trow(cells, h=_ROW_H))

    return table(sp_id, "MethodLedger", BODY_X, _GRID_TOP, _TABLE_W, _GRID_H,
                 col_widths=_COL_W, rows=[header] + body)


def _commentary(sp_id: int) -> str:
    """No-fill commentary: bold 9.5pt finding sentence, then a bulleted 9.5pt
    evidence line; hierarchy via bold + bullet, not a larger parent font. Read
    alone, the bold lines are the takeaways."""
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 260)))
    return text_box(sp_id, "Commentary", _COMM_X, _GRID_TOP, _COMM_W, _GRID_H,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=_COMM_INSETS)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    exhibit_header = text_box(
        10, "ExhibitHeader", BODY_X, _EXH_Y, _TABLE_W, _EXH_H,
        [paragraph([run("Sizing chain and governing rules",
                        size=EXHIBIT_HEADER_13PT, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)

    ledger = _method_table(11)
    commentary = _commentary(12)

    boundary = text_box(
        13, "BoundaryStrip", BODY_X, _BOUND_Y, BODY_CX, _BOUND_H,
        [paragraph([
            run(_BOUND_LEAD, size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run(_BOUND_BODY, size=MESSAGE_11PT, color=WHITE, font=FONT)])],
        fill=GRAY_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    return exhibit_header + ledger + commentary + boundary


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
