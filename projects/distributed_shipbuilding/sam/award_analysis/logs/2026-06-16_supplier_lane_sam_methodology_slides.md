# 2026-06-16 — SAM Methodology slides: supplier-lane screen (2-slide split), concentration-first

Two new working / SME-review slides for the deck_primary deck, plus a shared
helper module; four old slides removed.

Slide modules:
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/supplier_lane_method_part1.py`  (deck slide 11)
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/supplier_lane_method_part2.py`  (deck slide 12)
Shared helper (NOT registered, leading underscore):
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/_lane_method_kit.py`
Deck launcher: `projects/distributed_shipbuilding/deck_primary/build_deck.py`
Deck output:  `projects/distributed_shipbuilding/20260610_Distributed Shipbuilding New Construction_vS.pptx` (12 slides, 6 charts)
Build:  `cd projects/distributed_shipbuilding/deck_primary && python3 build_deck.py`
Probe:  `cd <repo root> && PYTHONPATH=.:projects/distributed_shipbuilding/deck_primary python3 -m deck_core.slide_probe deck_primary.slides.supplier_lane_method_part1 --text-estimate --out-dir /tmp/probe`

Authoring reference: `projects3/deck_primary_module_kit` (README + slide_guide.md +
example_slide.py) and `target_copy.txt` at the repo root. Built with the shared
engine ONLY (`deck_core.primitives` + `deck_core.style` + chrome builders) — the
pre-existing `rebuy_*` modules were the anti-pattern to avoid (they re-implemented
their own OOXML primitives, re-declared the palette, and hand-rolled the chrome).

## Goal

Add a 2-slide methodology explainer for the supplier-lane / re-buy openings
screen (the SAM sizing): a left-pane flow chart + a right-pane column of
discussion questions. Flow logic is CONCEPTUAL; live thresholds and timing
windows stay in the Award Analysis workbook, not on the page (matches the
hand-synced, not-wired pattern). The screen taxonomy maps to the workbook tabs
(Award Events, Lane Detail, Lane Vendor FY, Assumptions + the indicator-screen
tabs).

## Structure (final, concentration-first)

The initial spec was diversification-first and was corrected mid-build to
**concentration-first**: the first routing decision is recent top-vendor share.
Source diversification is NOT a first-class branch — it lives inside the
concentrated track as the "weakening dominance" read.

- **Slide 11 — build + primary split.** Build pipeline (FSRS subaward data →
  in-scope PIIDs → classify) → focal SUPPLIER LANE band (Program × PIID × Work
  type) → attach vendor-by-FY history → concentration gate ("recent vendor
  concentration in the lane?") fanning down a left rail to three regimes:
  Track A (high share, concentrated/incumbent-heavy), Track B (lower share +
  active, diverse/multi-source), Monitor (low/no signal). A/B continue on slide 12.
- **Slide 12 — track interpretation.** Two columns. Track A → direction test →
  A1 Entrenched incumbent (context) / A2 Concentrated but diversifying (opening;
  prior single → recent multi, incumbent active). Track B → cadence test → B1
  Discrete waves → forecast window → Periodic Sourcing Opening / Monitor future
  periodic; B2 Continuous stream → Active Continuous Opening / Diagnostic monitor.

## Shared kit (`_lane_method_kit.py`)

- Two-pane geometry derived from one rail-width constant (`RAIL_CX`), so the flow
  pane auto-resizes when the rail changes.
- Helpers: `node` (cap + italic sublines), `caption`, `arrow` (drops the
  arrowhead under MIN_ARROW ~0.27in), `divider` (vertical rule between panes),
  `sme_rail` (the question column).
- Shared chrome constants: `SECTION="Sourcing Openings"`, `TOPIC_LABEL="SAM
  Methodology"`, `SOURCES` (Note + workbook/FSRS source line), `SOURCES_Y=6_085_448`.
- Semantic fills: `OPENING_FILL=BLUE_2` (sourcing openings), `CONTEXT_FILL=GRAY_1`
  (context/monitor); stages/gates `BLUE_1`; the lane core band `BLUE_3`+white.

## Changes over the session (in order)

- Built the kit + three slides (overview + part1 + part2), registered last, built green.
- Reworked the two split slides to concentration-first (the corrected spec).
- **Deleted** the overview (`supplier_lane_mece_overview.py`) and unregistered +
  deleted the three pre-existing `rebuy_*` modules (`rebuy_openings_method`,
  `rebuy_openings_results`, `rebuy_opening_methodology`). Their charts were native
  in-code, so no orphaned `_chart_xml` sources were left. Deck 16→12 slides, 7→6 charts.
- **Rail width**: narrowed to ~60% then settled at `RAIL_CX = 2_805_000` (right-
  aligned to the body edge); flow pane auto-widened. part2 Track A (the one
  hardcoded width) bumped to 3_620_000 to grow in kind.
- **Rail bullets**: hang-indent under their group header (`mar_l=247_650`,
  `indent=-152_400`) — glyph ~0.10in in, wrapped text ~0.27in.
- **Rail title**: "SME challenges" → **"To discuss:"**, with one blank line
  before the first group.
- **Group numbering**: part2 headers A–I → 1–9; later **deleted** part2 "9. Final
  check" and part1 "7. Sparse or stale lanes".
- **Voice fix**: reworded the three questions that named "SME" (the SME is the
  audience); made them impersonal, not second-person ("Is this the best way to
  frame the opportunity?", "Should any … vendors be classified differently?",
  "Does the split reflect how these lanes actually behave?" / "Which lanes
  warrant a manual override?").
- **Borders**: all filled flow shapes uniform 1pt (dropped the 1.5pt focal
  border on the lane band; it stays distinct via the dark BLUE_3 fill). Only the
  locked Preliminary chip keeps 1.5pt. Connectors stay 0.75pt flow / 0.5pt divider.
- **Titles** (per `target_copy.txt` "Topic | Finding."): topic → `SAM Methodology
  (1/2)` / `(2/2)`; breadcrumb topic label → `SAM Methodology`. Findings:
  "Recent top-vendor concentration sets the first routing split." /
  "Direction and cadence turn each track into a specific opening read."
  The `(x/2)` part-counter is a deliberate, narrow exception to the no-parens-in-
  titles rule (recorded in memory).

## Verification

- Deck **builds green** (12 slides, 6 charts); package validates (zip OK, all 12
  slide XML parts well-formed).
- Slide-probe (`--text-estimate`): every body shape `fits=True` on both slides;
  the only `fits=False` is the Breadcrumb chrome box (pre-existing, shared deck-wide).
- Titles within two lines (11 = 1 line, 12 = 2 lines). Sources at y=6,085,448
  (deck convention). No em dashes; one `→` used as a deliberate flow transition.
- Rails fit with headroom: part1 ~29 wrapped lines / ~3.99in, part2 ~27 lines /
  ~3.74in, in ~4.81in available.

## State / notes

- Reader/working-facing slides; NOT wired to the workbook (conceptual logic;
  numbers/thresholds hand-synced).
- Connectors were intentionally left at flow weights (0.75 / 0.5pt), not bumped to
  1pt — they are lines, not shape borders. Flagged to the user; revisit if they
  want uniform 1pt on the arrows too.
- The breadcrumb `fits=False` is the shared chrome quirk, not from this work.
- No PNG render done (build-green is the bar; user visually verifies).
