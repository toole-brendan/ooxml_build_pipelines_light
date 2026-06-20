# 2026-06-16 — Supplier-lane methodology slides: flow-chart polish (gold-reference pass)

Follow-up to `2026-06-16_supplier_lane_sam_methodology_slides.md`. Same two
working / SME-review slides + their shared kit; a round of flow-chart refinements
driven by a gold-standard reference, then title-strip + chip tuning from review.
Downward flow direction was kept throughout (explicit user instruction).

Files touched (only these three — kit is imported by nothing else):
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/_lane_method_kit.py`
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/supplier_lane_method_part1.py`  (deck slide 12)
  - `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/supplier_lane_method_part2.py`  (deck slide 13)
Build:  `cd projects/distributed_shipbuilding/deck_primary && python3 build_deck.py`
Probe:  `cd <repo root> && PYTHONPATH=.:projects/distributed_shipbuilding/deck_primary python3 -m deck_core.slide_probe deck_primary.slides.supplier_lane_method_part1 --text-estimate --out-dir /tmp/probe`

Gold reference reviewed (NOT copied wholesale):
  `projects/gso_JM_reference/deck_gso_JM/deck_gso_JM/slides/flow_charts_graph.py`

## What was taken from the reference (and what was not)

The reference's best idea is that **every connector carries meaning** (white
relationship chips painted on the edge, masking the line under them) and a clean
node/edge separation. Borrowed: edge labels + the "labels paint last, mask the
line" discipline. Deliberately NOT borrowed: the pinned preset-connector
machinery (`bentConnector3` + rot/flipH/flipV/adj1 — exists only to reproduce a
hand-drawn PPT export), its self-contained re-implemented OOXML primitives (the
exact anti-pattern this kit avoids — it imports `deck_core`), and its wide
per-category palette (our restrained blue=opening / gray=context is intentional).

## Changes, in order

### Round 1 — flow-chart grammar
- **Branch-edge chips.** New `edge_chip()` kit helper: a white-filled, no-border,
  italic `CONNECTOR_NOTE_8_5PT` chip that rides a connector. part1 gate→bands:
  `High share` / `Lower share` / `Low / none`. part2 Track A: `Maintained` /
  `Weakening`; cadence fork: `Periodic` / `Continuous`. The redundant
  share-condition sublines were trimmed out of the band nodes (the condition is
  the chip now). Chips are appended LAST so the white fill masks the line.
- **Crooked arrows, never diagonal.** New `orthogonal_fork()` helper: a
  right-angled fan-out (vertical feed → horizontal rail → arrowed child drops).
  Replaced part2's only two diagonals — `Enter→A/B` and cadence `test→B1/B2`.
  part1 was already orthogonal.
- **Arrowheads on the directional spine.** The "leads-to" links now carry heads:
  part1 build stack (`Strip→Lane→Vendor→Gate`), part2 `Hdr→Test`. Structural
  trunks/rails (buses, fork rails) stay headless ON PURPOSE — the head goes on
  the segment that lands on a box, not on the rail that fans out.
- **Legend rendered.** `legend()` helper, bottom-left. Text sharpened to
  `Outcome fill — blue: sourcing opening; gray: context / monitor` — scoped to
  outcomes because blue is also the process/stage color (the old unscoped
  "Blue = sourcing opening" was misleading).
- **part1 tightening** (the user flagged dead vertical padding in the 3 bottom
  bands): band heights 620/620/600k → 460/460/420k; build-stack gaps opened to
  250k so the new arrowheads read (`_SPINE_GAP`); gate→band channel widened
  (`_BUS_X` left, `_BAND_X` inset to 1_500_000) so chips sit in the gutter clear
  of the bands. `_STRIP_H` nudged 450→470k to keep `Build3` fitting.
- **part2 spread** (the user noted unused vertical room): flow pushed down to
  bottom ~5_540_000 (was ~4_880_000), using the ~1M EMU of slack.

### Round 2 — "To discuss:" as a title-strip + A-chip fixes
- Found the deck's **single-cell-table title-strip** pattern (slides 1–2, e.g.
  the "Methodology" caption over the slide-2 ledger): a 1×1 table, no fill, **1pt
  black bottom rule** (`lnB w="12700"`), 10pt bold, style GUID
  `{2D5ABB26-0587-4C30-8999-92F81FD0307C}` (== `NO_STYLE_NO_GRID`). New
  `rail_title()` (later `title_strip()`) helper reproduces it via
  `table()`/`tcell()`. Pulled "To discuss:" out of the question box into its own
  strip; `sme_rail()` now takes the shared `sid` counter (title strip + question
  box = one id each).
- **A chips widened + lifted.** "Weakening" was wrapping in real PowerPoint
  (Arial italic renders wider than the fit-estimate). Bumped `edge_chip`'s
  auto-width formula and gave the two Track-A chips explicit `w=800_000`; added a
  `place="above"` mode so they float just above the tap line instead of masking
  its middle (the user wanted them above the connectors).

### Round 3 — flow captions become matching title-strips
- "Build the lane, then split on concentration" / "What each concentration track
  means" converted to the same `title_strip` structure — **Sentence case**, 10pt
  bold (same font/size as "To discuss:"). Renamed `rail_title → title_strip`
  (now generic). Added shared constants `TITLE_STRIP_Y/H/GAP`.
- **One aligned, lifted header row.** All three strips sit at `TITLE_STRIP_Y =
  1_240_000` (h 251_778, rule at 1_491_778). The row had to move UP (above
  BODY_Y, into the title→body band) because on the vertically-full part1 a rule
  at the old caption y (1_623_378) would have sliced the build strip. Flow
  content stayed put — `Build1`/`Enter` clear the rule by 38k / 88k EMU. The pane
  `divider()` start dropped below the strip row (1_531_778) so it divides only
  the content.

## Verification

- Deck **builds green**; package validates (zip OK, all slide XML parts
  well-formed).
- Slide-probe (`--text-estimate`): every body shape `fits=True` on both slides;
  only `fits=False` is the shared Breadcrumb chrome box (pre-existing, deck-wide).
- Title strips confirmed pixel-aligned across the divider (both flow caption and
  "To discuss:" at y=1_240_000, rule at 1_491_778). All 7 branch chips fit
  single-line; the two Track-A chips sit above their taps (bottoms 3_886_000 /
  4_926_000; taps at 3_930_000 / 4_970_000). Question rails fit with headroom.
- Generated title-strip XML verified byte-faithful to the reference: same style
  GUID, `sz="1000" b="1"`, `lnB w="12700"`, side/top borders `noFill`.

## State / notes

- **Slide-count change is NOT from this work.** Mid-session the deck went 12→13
  slides / 6→7 charts because an external edit added `outsourced_bc_annual_tam_layers`
  (a chart-bearing "Stage-2 twin", now slide 4) to `slides/__init__.py` — a file
  this work never touched. `_lane_method_kit` is imported only by part1/part2, so
  these changes are isolated. The supplier-lane slides are now **slide 12
  (part1)** and **slide 13 (part2)**.
- "To discuss:" changed from bold-italic 9pt to bold 10pt (non-italic) to match
  the title-strip pattern; flag if italic is wanted back.
- Scope choices left open (not done, easy to extend): branch chips are on
  first-level branches only — Track B's leaf yes/no's keep their condition in the
  outcome sublines (the ~2in sub-columns are too narrow for a chip); and only the
  Track-A chips were moved above their lines (per the "2/2" instruction) — part1's
  branch chips and the Periodic/Continuous fork chips still ride their lines.
- Connector weights left at the existing flow weights (0.75pt flow / 0.5pt
  divider); the new arrowheads are on those same 0.75pt lines.
- No PNG render (build-green is the bar; user visually verifies).
