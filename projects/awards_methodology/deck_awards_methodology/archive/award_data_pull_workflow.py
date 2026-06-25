"""award_data_pull_workflow - how an analyst pulls and trusts federal
award data: a seven-step PULL -> ENRICH -> QA workflow above a source-role table
and a money-discipline rail, reframing SAM Contract Awards (not the FPDS Atom
feed) as the modern base pull surface.

Style + chrome rules: deck_core/slide_guide.md. Builders and design tokens are
imported from deck_core (primitives / style / text_metrics); the page design is
local. No chart - process boxes + a native source-role table + a QA rail.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, tcell, trow, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_1, BLUE_5, GRAY_1, GRAY_3, GRAY_4,
    DK, WHITE, BREADCRUMB, BLACK, FONT,
    INSETS_NONE, INSETS_MESSAGE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    blue_pair,
)
from deck_core import text_metrics

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers


# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION  = "Method"
_TOPIC    = "Awards data workflow"                 # breadcrumb topic label
_TITLE    = "How we pull it"                        # title topic
_TAKEAWAY = ("SAM.gov award records, USAspending funding context, and "
             "subaward reporting")
_SOURCES  = ("Sources: (1) SAM.gov Contract Awards, Subaward, Opportunities, "
             "and Entity Management APIs; (2) USAspending API; (3) FPDS Atom "
             "(legacy lineage)")


# ════════════════════════════════════════════════════════════════════════════
# CONTENT
# ════════════════════════════════════════════════════════════════════════════

# Workflow steps: (number+verb, descriptor, phase). Phase drives the blue ramp
# and the PULL / ENRICH / QA grouping. Active verbs only; no endpoint syntax.
_PULL, _ENRICH, _QA = "pull", "enrich", "qa"
_STEPS = [
    ("1 DEFINE",   "Programs, PSC, NAICS, vendors, buyers",     _PULL),
    ("2 PULL",     "Awards, IDVs, vehicles, orders, ceiling",   _PULL),
    ("3 ADD",      "Fiscal-year context, funding TAS",          _ENRICH),
    ("4 HYDRATE",  "Parents to child task and call orders",     _ENRICH),
    ("5 PULL",     "First-tier subawards (supplier layer)",     _ENRICH),
    ("6 RESOLVE",  "UEIs, CAGEs, parents, NAICS, rollups",      _ENRICH),
    ("7 QA",       "Separate money universes, tag confidence",  _QA),
]
# blue_pair(3)=BLUE_4/WHITE, blue_pair(1)=BLUE_2/DK, blue_pair(4)=BLUE_5/WHITE
_PHASE_PAIR = {_PULL: blue_pair(3), _ENRICH: blue_pair(1), _QA: blue_pair(4)}

# Source-role table. Columns sum to BODY_CX. Opportunities + Entity Management
# are folded into one "SAM enrichment sources" row (the spec's fit rule) so the
# table reads as an operating model rather than IT documentation.
_COL_W = [1_750_000, 1_650_000, 2_850_000, 2_850_000, 2_182_362]
_HEADER = ["Source", "Role in workflow", "Best answers",
           "Caveat or QA rule", "Slide output"]
_ROWS = [
    ["President's Budget", "Forward-funded demand",
     "What is funded, by account, PE or BLI, color of money, and FY",
     "Budget lines do not map cleanly to NAICS, PSC, or contractors",
     "Funded-demand spine"],
    ["SAM Contract Awards", "Modern prime and vehicle pull",
     "What awards and IDVs exist; parent-child order and ceiling structure",
     "Do not overcount parent and child awards; mind coverage rules",
     "Vehicle and incumbent map; ceiling and remaining capacity"],
    ["USAspending", "Award enrichment and funding bridge",
     "Obligations by transaction and FY; funding account and TAS",
     "Enriched spending view; reconcile key facts to the award record",
     "TAS bridge, FY obligations, budget intersection"],
    ["SAM Subaward Reporting", "First-tier supplier layer",
     "Which reported first-tier suppliers sit under a prime",
     "Reporting lags and can be incomplete; not the full supply chain",
     "Supplier and workshare map"],
    ["SAM enrichment sources (Opportunities, Entity)",
     "Pre-award pipeline and entity resolution",
     "Posted but not yet awarded work; UEI, CAGE, NAICS, vendor data",
     "Postings are not awarded demand; registration is not relevance",
     "Forward pipeline watchlist; vendor rollups"],
    ["FPDS Atom feed", "Legacy reference and validation",
     "What the older FPDS action feed shows",
     "Do not build the future methodology around Atom as the base",
     "Lineage validation and issue resolution"],
]


# ════════════════════════════════════════════════════════════════════════════
# GEOMETRY
# ════════════════════════════════════════════════════════════════════════════
_GAP = 80_000
_N = len(_STEPS)
_STEP_W = (BODY_CX - (_N - 1) * _GAP) // _N


def _step_x(i: int) -> int:
    return BODY_X + i * (_STEP_W + _GAP)


_PHASE_Y   = BODY_Y                 # phase labels sit on the top edge of BODY
_BRACKET_Y = BODY_Y + 160_000       # thin grouping rule under each phase label
_STEP_Y    = BODY_Y + 205_000
_STEP_CY   = 740_000
_NOTE_Y    = _STEP_Y + _STEP_CY + 60_000
_NOTE_CY   = 360_000
_TABLE_Y   = _NOTE_Y + _NOTE_CY + 60_000
_QA_GAP    = 90_000
_QA_CY     = 430_000


# ── slide-local builders ─────────────────────────────────────────────────────
def _phase(sp_id, x, w, label):
    """Small-caps phase label + a thin GRAY_4 grouping rule beneath it."""
    lab = text_box(
        sp_id, f"PhaseLabel {label}", x, _PHASE_Y, w, 150_000,
        [paragraph([run(label, size=LABEL_9PT, bold=True, color=BREADCRUMB,
                        font=FONT)], align="ctr")],
        anchor="b", insets=INSETS_NONE)
    rule = connector(sp_id + 1, f"PhaseBracket {label}", x, _BRACKET_Y, w, 0,
                     color=GRAY_4, width=9_525)
    return lab + rule


def _step(sp_id, x, label, desc, phase):
    """One workflow box: number+verb cap over a compact descriptor."""
    fill, txt = _PHASE_PAIR[phase]
    return text_box(
        sp_id, f"Step {label}", x, _STEP_Y, _STEP_W, _STEP_CY,
        [paragraph([run(label, size=DENSE_BODY_10PT, bold=True, color=txt,
                        font=FONT)], space_after=200),
         paragraph([run(desc, size=FINEPRINT_8_5PT, color=txt, font=FONT)])],
        anchor="t", fill=fill,
        l_ins=72_000, t_ins=54_000, r_ins=72_000, b_ins=54_000)


def _hcell(t):
    return tcell(t, fill=BLUE_5, color=WHITE, bold=True, size=FINEPRINT_8_5PT,
                 align="l", anchor="ctr",
                 borders={"B": {"color": BLACK, "width": 19_050}})  # 1.5pt rule


def _bcell(t, *, bold=False, italic=False, fill=None, last=False):
    return tcell(
        t, fill=fill, color=DK, bold=bold or None, italic=italic or None,
        size=FINEPRINT_8_5PT, align="l", anchor="t",
        borders=None if last else {"B": {"color": BLACK, "width": 12_700}})


def _source_table(sp_id):
    """Native source-role table with honest, content-fit row heights.

    Source column bold; Caveat column reads as caution (GRAY_1 + italic); Slide
    output reads as payoff (BLUE_1 tint). Cascading bottom borders: 1.5pt under
    the header, 1pt under each body row except the last. Returns (frame_xml,
    bottom_y) so the QA rail can sit just below the real table bottom."""
    rows_text = [_HEADER] + _ROWS
    heights = text_metrics.estimate_row_heights(
        rows_text, _COL_W, size_pt=8.5, header_size_pt=8.5)
    rows = [trow([_hcell(c) for c in _HEADER], h=heights[0])]
    for i, r in enumerate(_ROWS):
        last = (i == len(_ROWS) - 1)
        src, role, best, caveat, out = r
        rows.append(trow([
            _bcell(src, bold=True, last=last),
            _bcell(role, last=last),
            _bcell(best, last=last),
            _bcell(caveat, italic=True, fill=GRAY_1, last=last),
            _bcell(out, fill=BLUE_1, last=last),
        ], h=heights[i + 1]))
    total_h = sum(heights)
    frame = table(sp_id, "SourceRoleTable", BODY_X, _TABLE_Y, BODY_CX, total_h,
                  col_widths=_COL_W, rows=rows)
    return frame, _TABLE_Y + total_h


def _body() -> str:
    parts = []

    # Phase brackets over the step row: PULL (1-2), ENRICH (3-6), QA (7).
    parts.append(_phase(10, _step_x(0), 2 * _STEP_W + _GAP,     "PULL"))
    parts.append(_phase(12, _step_x(2), 4 * _STEP_W + 3 * _GAP, "ENRICH"))
    parts.append(_phase(14, _step_x(6), _STEP_W,                "QA"))

    # Seven workflow step boxes.
    for i, (label, desc, phase) in enumerate(_STEPS):
        parts.append(_step(20 + i, _step_x(i), label, desc, phase))

    # The major reframing, as a bold no-fill note above the table.
    parts.append(text_box(
        30, "CorrectionNote", BODY_X, _NOTE_Y, BODY_CX, _NOTE_CY,
        [paragraph([
            run("Source correction: ", size=MESSAGE_11PT, bold=True, color=DK,
                font=FONT),
            run("the modern base pull is SAM Contract Awards, not FPDS Atom. "
                "The Atom feed is retiring in FY 2026; FPDS now serves only as "
                "legacy lineage and validation.", size=MESSAGE_11PT, color=DK,
                font=FONT),
        ])],
        anchor="t", insets=INSETS_NONE))

    # Source-role table.
    frame, table_bottom = _source_table(40)
    parts.append(frame)

    # QA / money-discipline rail: high-contrast lead-in but visually
    # subordinate (light GRAY_1 panel, secondary GRAY_3 border).
    qa_y = table_bottom + _QA_GAP
    parts.append(text_box(
        50, "QARail", BODY_X, qa_y, BODY_CX, _QA_CY,
        [paragraph([
            run("QA is the method: ", size=LABEL_9PT, bold=True, color=DK,
                font=FONT),
            run("keep budget, obligations, ceiling, outlays, and subawards as "
                "separate money universes; sum action obligations, not restated "
                "totals; roll vehicles and child orders into one opportunity "
                "family; tag source, vintage, measure, and confidence.",
                size=LABEL_9PT, color=DK, font=FONT),
        ])],
        anchor="ctr", fill=GRAY_1, line_color=GRAY_3, line_width=12_700,
        insets=INSETS_MESSAGE))

    return "".join(parts)


def render() -> str:
    """Assemble locked chrome + body into a complete <p:sld>."""
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
