# Deck redesign session — 2026-05-25 (submarine pattern sweep)

Deck-wide visual upgrade applying the submarine deck's composition
patterns to every content slide of the destroyer deck. Sister to the
prior deck-build sessions in this folder.

## Context at session start

- Destroyer deck at `/Users/brendantoole/projects2/destroyer_outsourced_work/deck/`
  was already authored end-to-end (s00 cover, 5 section dividers,
  s01–s11 content slides). All built cleanly; pipeline unchanged from
  the prior sessions (`build.py`, `builder.py`, `primitives.py`,
  `style.py`, `validate.py`, `layout_check.py`).
- Sister submarine deck at `/Users/brendantoole/projects2/submarine_outsourced_work/deck/`
  shares the same `style.py` palette and typography tokens but uses a
  richer composition vocabulary: dark BLUE_5 anchor blocks, ALL-CAPS
  italic section labels, lane pairs, split TAKEAWAY bands, two-zone
  cards, three-lens cards, color ramps, line-weight hierarchy.
- User feedback over the session pointed at "positioning and underfills
  alone look rough" — the destroyer deck was reading as a thinner
  vocabulary (body_box + cards + KPI rows) compared to the submarine.
- Two hard constraints from the user: **keep every image placeholder**
  (s01, s03, s08, s09, s10) and **keep every native chart** (s03 ranked,
  s04 waterfall, s05 stacked, s06 ranked, s07 stacked, s08 ranked).

## Work completed

### 1. s01 Market Architecture — earlier-in-session redesign (already shipped)

Original module was `Simple Market Model` with a shallow top-right image
slot and three same-color cards that didn't distinguish self-perform from
supplier-addressable layers. Replaced with:

- Breadcrumb / title: `Overview / Market Architecture`,
  `Market Architecture | DDG-51 supplier flow is split between yard-side
  work and Navy-procured GFE`.
- Three full-width layer cards with intent-driven palette
  (GRAY_1 self-perform / BLUE_2 yard-side outsourcing / BLUE_4
  Navy-procured GFE), each at `SZ_CARD_TITLE` + 3-line body, no bullets,
  centered.
- Channel labels (`Inside Basic Construction contract` /
  `Outside the yard contract`) sit over their card columns.
- Full-width image strip `ArchitectureVisual` at y=4.50, replacing the
  former slim top-right placeholder.
- Single `BLUE_1` `note_band` for the market read; transparent footer
  label previewing the next-slide FY24 anchors (60.5% / 32.9% / ~$1.8B).
- Arrows dropped (the three layers are parallel buckets, not a flow).

### 2. s02 Cost Funnel — earlier-in-session redesign (already shipped)

Original was a stacked-column chart with a right-rail card stack.
Replaced with a **vertical funnel** mirroring submarine `cost_funnel.py`:

- `TOTAL SHIP ESTIMATE` gate (GRAY_2) carrying `$5.49B FY24 two-ship buy`.
- Centered black arrow → `ABOVE BASIC CONSTRUCTION` italic divider →
  3 above-BC chips (BLUE_1, tapered inward): Plans 1.5%, GFE 32.9%,
  Other 5.1%.
- Italic caption "remove these layers to isolate the construction base"
  → centered arrow.
- `BASIC CONSTRUCTION` gate (BLUE_5 dark anchor, white `SZ_CARD_TITLE`
  bold, `LINE_HEAVY` 1.5pt border) — the slide's visual focal point.
- `INSIDE BASIC CONSTRUCTION` divider → 4 inside-BC lanes
  (GRAY_2 self-perform + 3 BLUE_1 lanes: Direct material, FFATA-visible
  first tier, Lower-tier and unseen). Hidden-slice lane carries the
  `~$1.5B` figure.
- Split TAKEAWAY band (BLUE_5 cap + GRAY_1 message) replacing the
  former GRAY_1 note_band.
- Em dashes stripped per style rules; chart removed so module returns
  `s.to_xml()` (no `build_finalize`).
- Float-rounding trap encountered: `LM=0.495` rounded to 452,628 EMU,
  below the 453,079 EMU LEFT_MARGIN. Fix is `LM=0.50`. Documented in
  the plan for downstream slides.

### 3. Pattern catalogue and per-slide plan

Approved plan saved to
`/Users/brendantoole/.claude/plans/putting-you-in-plan-gentle-matsumoto.md`.
Pattern menu extracted from submarine slides:

| Pattern | Source | What it produces |
|---|---|---|
| Dark BLUE_5 anchor block | `cost_funnel.py` BC gate | Focal point with white `SZ_CARD_TITLE` + italic subtitle, 1.5pt border |
| Split TAKEAWAY band | `gfe_pipe.py` | Dark left cap + light message panel |
| Controlled chart title | `cost_funnel.py` text-box pattern | `s.text` above the chart; `title=None` on native chart |
| Three-lens cards | `public_data_lenses.py` | Header + body with two ALL-CAPS bullet sections |
| Two-zone card | `historical_reset.py` | Dark header band + lighter body zone |
| Lane pair (tag + body) | `basic_construction.py` | Narrow BLUE_5 tag + wider body cell |
| ALL-CAPS italic section label | `cost_funnel.py` | Transparent structural divider |
| Force snapshot strip | `mission_families.py` | Full-width GRAY_1, bold facts, pipe-separated |
| Numbered tab lens | `cost_funnel.py` denominator strip | Numbered chips + body cells |
| Color ramp via `BLUE_SCALE[i]` / `BLUE_TEXT[i]` | `historical_reset.py` | Gradient across a multi-step sequence |
| Line-weight hierarchy | every slide | 0.5pt chips → 1pt cards/bands → 1.5pt anchors |

### 4. Helpers added to `slides/_helpers.py`

Seven reusable helpers + 3 line-weight constants exported:

- `section_label(s, x, y, w, text)` — ALL-CAPS italic divider strip.
- `split_takeaway_band(s, x, y, w, label_text, message)` — dark cap +
  light message pair; default label `TAKEAWAY`.
- `dark_anchor_block(s, x, y, w, h, title, subtitle)` — BLUE_5 anchor
  with white `SZ_CARD_TITLE` and italic subtitle, `LINE_HEAVY` border.
- `two_zone_card(s, x, y, w, h, header_title, header_subtitle,
  body_paragraphs)` — dark header band + body zone with custom
  paragraphs.
- `lane_pair(s, x, y, w, h, tag, body_title, body_text)` — narrow
  BLUE_5 tag + BLUE_1 body cell.
- `three_lens_card(s, x, y, w, h, header_title, section1_label,
  section1_items, section2_label, section2_items)` — header strip +
  body with two ALL-CAPS bullet sections.
- `force_snapshot_strip(s, x, y, w, facts)` — full-width GRAY_1 strip
  with pipe-separated bold facts.
- Constants: `LINE_THIN = 6_350`, `LINE_STD = 12_700`, `LINE_HEAVY =
  19_050`.

All helpers use shared `style.py` tokens and route through `SlideBuilder`
so palette validation and bounds checking still apply.

### 5. Per-slide redesigns (s03–s11)

Every slide builds cleanly; only flag remaining on each is the
documented breadcrumb-overfill false positive plus expected image-
placeholder underfills.

**s03 production_baseline.** Kept `ranked_column_chart` (FY18–FY27)
and `YardImage`. Added controlled chart title; image moved into a
dark-headered two-zone composition; KPI row tightened with BLUE_2 /
BLUE_3 / BLUE_5 ramp; mini_chips replaced by an ALL-CAPS section label
+ split TAKEAWAY band.

**s04 market_size.** Kept `waterfall_chart`. Chart title added.
`Combined ~$6.8B` promoted to a dark BLUE_5 `dark_anchor_block`
headline in the right rail. `Measured` and `Estimated` became
two-zone cards (BLUE_5 / BLUE_4 headers + GRAY_1 bodies with bullets).
`note_band` → split TAKEAWAY.

**s05 dod_pop.** Kept `stacked_column_chart`. Top row: dark anchor
`~87%` + corpus / caveat cards. Chart title above chart. Right rail
became a single two-zone "HOW TO READ THE TWO BARS" card with
`DISCLOSED READ` + `ADJUSTED READ` mini-sections. Bottom: split
TAKEAWAY.

**s06 ffata_visible.** Kept `ranked_column_chart`. KPI ramp at top.
Replaced both right-side body_boxes with one canonical `three_lens_card`
("What FFATA shows, and what it doesn't" — WHAT IT SEES / WHAT IT
MISSES). 4 mini_chips folded into the lens. Split TAKEAWAY at bottom.
Caught and fixed a 0.05" KPI/lens overlap (x=5.40+2.30=7.70 vs lens at
x=7.65) — nudged lens to x=7.80.

**s07 hidden_yard_layer.** Kept `stacked_column_chart`. `dark_anchor_block`
`~$1.82B combined` + three flanking KPIs (BIW $1.13B, Ingalls $0.69B,
FFATA-visible $0.29B). Chart title added. Right rail's `Range / Read it
as` cards replaced by 3 `lane_pair`s: `ASYMMETRY`, `TIER 2+`, `RULE`.
Split TAKEAWAY.

**s08 aegis_spy6.** Kept `ranked_column_chart` and both image
placeholders. Chart title added. The Aegis / SPY-6 cards became
image-bearing two-zone cards: BLUE_5 / BLUE_4 header (program + prime +
site) → image placeholder → BLUE_1 detail body with 3 bullets. The
images are now integrated into the cards, not dangling below. Bottom:
force snapshot strip + split TAKEAWAY.

**s09 other_gfe.** Kept all 3 image placeholders. Replaced the
disconnected image row + chips + cards layout with a **three-card deck**
(mission_families pattern): each card = BLUE_5 header (program +
prime + sites) → image → BLUE_1 fact chip → GRAY_1 detail. Mk 41 VLS,
Mk 45 5-inch gun, LM2500 turbine. Force snapshot for SEWIP/SPQ-9B
+ foreign-exposure / scope notes. Split TAKEAWAY.

**s10 direction_of_travel.** Kept `DistributedBuildImage`. The 4-step
KPI sequence became a **color-ramped timeline** of two-zone cards
using `BLUE_SCALE[1..4]` headers (BLUE_2 → BLUE_5) — `BLUE_TEXT[i]`
auto-pairs the text color. Arrows dropped; the gradient itself carries
the progression. Middle row: dark-headered image card + HII Ingalls
two-zone (BLUE_5 header, 3 bullets) + GD Bath two-zone (BLUE_4 header,
3 bullets). Split TAKEAWAY at the bottom.

**s11 method_appendix.** Three `three_lens_card`s, one per measurement
(`1 · SCN cost funnel`, `2 · DoD POP corpus`, `3 · FFATA + triangulation`),
each with WHAT IT MEASURES / WHAT IT MISSES. Caveats body_box + mini_chips
replaced by a **numbered caveat tab strip** (01 REDACTION / 02 VISIBILITY
/ 03 RESIDUAL / 04 SCOPE) — direct lift of submarine `cost_funnel.py`'s
denominator strip. Bottom: split TAKEAWAY with `BEST READ` label
carrying `$5.0B GFE + $1.8B yard-side`.

### 6. Verification

Final build clean. `out/destroyer_deck.pptx` is 81 KB, 17 slides,
6 native chart parts (`ppt/charts/chart1.xml`..`chart6.xml`).
Layout check across the deck reports only:

- Documented breadcrumb overfill on every content slide (the placeholder
  uses `spAutoFit` so the static estimator can't size to runtime
  content; README false positive).
- DividerTitle underfill on every section divider (also documented —
  small text in a tall placeholder).
- Image placeholder underfills (18–29% filled) — by design, since
  `image_placeholder` shows only its caption text inside a dashed
  border.
- s10 (slide 15) HII/GD body underfills at 25% — text content is brief
  inside h=1.70 boxes; `anchor="ctr"` centers the content so the visual
  is fine.

No real overlap, overflow, or palette violations anywhere.

## Files modified

- `deck/slides/_helpers.py` — added 7 helpers + 3 line-weight constants;
  expanded module docstring.
- `deck/slides/s01_simple_model.py` — Market Architecture redesign
  (earlier session; documented here for completeness).
- `deck/slides/s02_cost_funnel.py` — vertical funnel.
- `deck/slides/s03_production_baseline.py` — chart title + two-zone
  image card + KPI ramp + split TAKEAWAY.
- `deck/slides/s04_market_size.py` — dark anchor headline + two-zone
  Measured / Estimated cards.
- `deck/slides/s05_dod_pop.py` — anchor + chart title + two-zone
  interpretation card.
- `deck/slides/s06_ffata_visible.py` — KPI ramp + three-lens card.
- `deck/slides/s07_hidden_yard_layer.py` — anchor + 3 lane pairs.
- `deck/slides/s08_aegis_spy6.py` — image-bearing two-zone program
  cards + force snapshot.
- `deck/slides/s09_other_gfe.py` — three image-bearing program cards.
- `deck/slides/s10_direction_of_travel.py` — color-ramped timeline
  + two-zone yard cards.
- `deck/slides/s11_method_appendix.py` — three-lens method cards +
  numbered caveat tabs.

Untouched: `style.py`, `builder.py`, `primitives.py`, `build.py`,
`validate.py`, `charts.py`, `layout_check.py`, every section divider
(`div_*.py`), `s00_cover.py`. All slide modules continue to expose
`render(*, page_num, total_pages)` returning slide XML; chart-bearing
modules return `s.build_finalize()`, others return `s.to_xml()`.

## Reusable lessons for future deck work

- **Float-rounding trap on `LM=0.495`.** `_emu(0.495)` rounds to 452,628
  which is below the 453,079 EMU `LEFT_MARGIN`. Use `LM=0.50` and
  `CW=12.33` so right edge stays at 12.83 (within the 12.838 usable
  width).
- **Image placeholders always look underfilled.** They display only
  caption text inside a dashed border — heuristic underfill flags are
  expected and not a problem to fix.
- **Mixed alignment in `card(... bullets=True)` is awkward.** The
  helper centers the title but left-aligns the bullets. For cleaner
  cards, use `bullets=False` and pass a list-of-strings body with
  `anchor="ctr"` — the helper centers each body line.
- **Em dashes are blocked by style rules** (`style.py` top docstring,
  line 27). Substitute semicolons or rephrase.
- **`split_takeaway_band` replaces almost every `note_band`** that
  carries a real slide takeaway. The split structure (dark cap + light
  message) reads as a real conclusion, not a footer.
- **`three_lens_card` is the right pattern for any SEES/MISSES,
  MEASURES/LIMITS, or PROS/CONS framing.** Helper signature already
  enforces the two-section structure.
- **Color ramps via `BLUE_SCALE[i]` + `BLUE_TEXT[i]`** auto-pair the
  fill and text color across a gradient. Use indices 1..4 to skip the
  too-light BLUE_1 in step sequences.
- **`build.py` and the registration list are unchanged across this
  sweep.** Module filenames and `render` signatures stay; only module
  bodies change.

## Open follow-ups (not done this session)

- Cover slide (`s00_cover.py`) and section dividers (`div_*.py`) left
  structurally as-is. Submarine equivalents are also minimal — could
  enrich subtitles to preview next-slide-group content but not
  load-bearing.
- Native charts have `show_legend=True` on stacked variants; could
  audit legend placement / label truncation if visual review flags it.
- The 25% body underfills on s10 HII/GD cards center text vertically —
  visually fine but the heuristic still flags them. If layout-check
  noise becomes an issue, fold the section label into the card header
  instead of leaving it as a separate band.
