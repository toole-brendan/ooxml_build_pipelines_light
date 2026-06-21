# Deck build session — 2026-05-25 (part 3)

Continuation of the destroyer-outsourced-work deck build. Companion to
`DECK_SPEC.md` at the project root and to the two earlier session logs
(`deck_build_session_2026-05-25.md` produced s00..s03;
`deck_build_session_2026-05-25_pt2.md` produced s04 divider, s05, s06, s07,
plus pre-wrote s08 and s11 dividers).

This session closed out the remaining body slides and brought the deck to
its planned 15-slide footprint.

## Context at session start

- Deck had 8 slides wired (cover + 3 overview + Sizing divider + 3 sizing
  body slides). `s08_divider_layers.py` and `s11_divider_direction.py`
  were pre-written from part 2 but not yet wired into `SLIDES`.
- `DECK_SPEC.md` described 7 more planned slides: 2 Layers body (s09
  Aegis+SPY-6, s10 other GFE), 3 Direction (divider + s12 HII, s13 Navy),
  and 1 Appendix (s14 method/sources).
- Build pipeline unchanged. Live data sources: wiki chapters 10, 11, 13,
  14, 16.

## Work completed

### 1. Read-in of all logs and wiki chapters (context phase)

Read every file in `logs/` plus all 16 chapters of `wiki_ddg/` + INDEX.md.
This served as the data substrate for the 5 new body slides — every
dollar figure, vendor name, city, and quote on the new slides traces to a
specific wiki chapter or `extracted/` CSV.

### 2. s09_aegis_spy6.py — the two ~$5B GFE megabuckets

- **Title.** `Aegis and SPY-6 | Together about $5B, 70 percent of the $7.13B supplier-TAM corpus`
  - Disambiguated from DECK_SPEC's verbatim title "The two ~$5B GFE
    megabuckets" because Aegis is $3.55B and SPY-6 is $1.48B — they are
    not each ~$5B; *together* they are ~$5B. Posed two title options to
    user via AskUserQuestion; user picked the disambiguated wording.
- **Visual.** Two side-by-side dark-blue panels (5.65" wide × 3.30" tall):
  - Left (BLUE_5): Aegis Combat System / Lockheed Martin at Moorestown,
    NJ / `$3.55B` / 74 actions, 86% supplier-city POP / top subs Mission
    Solutions, Arctic Slope, Extreme Engineering
  - Right (BLUE_4): AN/SPY-6(V)1 radar / Raytheon at Andover, MA /
    `$1.48B` / 7 actions, 82% supplier-city POP / top subs GD Mission
    Systems, CAES, Northrop Grumman
- **Anchor strip** (SZ_SECTION bold) at top: "Combined about $5.0B, 70
  percent of the $7.13B supplier-TAM corpus."
- **Caption.** "Each is a single-prime, single-city concentration. That
  structural fact is the reason the 87 percent outside-yards headline
  understates operational concentration: roughly seventy cents of every
  supplier-TAM dollar lands in two ZIP codes."
- **Data.** Wiki ch 10 / `extracted/dod_action_pop_by_worktype.csv`.

### 3. s10_other_gfe.py — the five smaller GFE buckets

- **Title.** `Other GFE | Five smaller buckets, each a single-prime concentration`
- **Visual.** Five cards in a single row (2.20" × 3.30" each, 0.18" gaps,
  fills the 11.73" content band exactly). Each card carries 7 elements
  top-to-bottom: program name (SZ_LEAD bold), prime, city, big dollar
  (28pt), unit label (italic), meta line. Card fills:
  - Mk 41 VLS — BLUE_5 (highest dollar)
  - LM2500 turbines — BLUE_4
  - Mk 45 5-inch gun — BLUE_4
  - AN/SLQ-32 SEWIP — BLUE_3 (lower)
  - Mk 15 Phalanx CIWS — GRAY_5 (out-of-SCN-TAM marker)
- **Dollar-source choice.** Cards mix two metrics by necessity: VLS / Mk
  45 / LM2500 use DoD-announcement TAM corpus dollars (consistent with
  s09); SEWIP and CIWS use cumulative FFATA subaward dollars (since
  neither has its own row in the DoD-announcement by-worktype rollup —
  SEWIP rolls into combat_systems, CIWS is excluded from the TAM gate
  entirely). Each card carries an italic "unit" label distinguishing the
  two metrics.
- **CIWS treatment.** Greyed (GRAY_5) and meta line reads "WPN-funded,
  outside SCN TAM". Visually flagged as separate from the four SCN-funded
  buckets while preserving the spec's request to include it for the
  broader supplier-base picture.
- **Caption.** Notes CIWS is the largest single PIID subaward base in the
  in-scope FFATA stream — visually important context for why it is shown
  at all.

### 4. s12_hii_outsourcing.py — 2× anchor + three-bar growth chart

- **Title.** `HII Outsourcing | Doubled in 2025, plus 30 percent guided for 2026`
- **Visual.** 72pt `2×` anchor at top (matching the s05 87% / s06 15% /
  s13 5× rhythm), followed by a three-bar chart of HII outsourcing hours:
  - 2024 actual: ~1.0M hrs (BLUE_3)
  - 2025 actual: ~2.0M hrs (BLUE_4)
  - 2026 guided: ~2.6M hrs (BLUE_5)
  - Growth annotations in the gaps between bars: "+100%" and "+30%"
- **Data caveat.** Hours figures are inferred from Kastner's public
  commitments ("doubled in 2025" + "30 percent for 2026") plus the
  publicly-stated 2024 baseline ("over 1 million hours"). HII has not
  directly disclosed exact hour figures. The slide caption and the slide
  docstring both note the inference. DECK_SPEC Open Question #3 covers
  this. Trajectory shape is correct; exact magnitudes are estimates.
- **Caption.** 23 vendors established 2025; DDG 137 received first 2 of
  32 distributed-fab units in Q1 2026; NNS Charleston 0.5M hours year
  one, 2× target for 2026.

### 5. s12 layout patch (3 bbox overlaps)

First-build `layout_check` flagged 5 real overlaps on s12:
- Year_2024/2025/2026 boxes ↔ Caption — year boxes ran y=5.40 to 6.05,
  caption started at y=6.00
- SourcesLine ↔ Caption — caption ended at y=6.50, SourcesLine at y=6.49
- Val_2025 ↔ Growth_1 — value-label box (centered on bar with width
  bar_w + 0.60) extended into the inter-bar gap zone where the growth
  annotation lived

Fixes:
- Shrunk year-label box height from 0.65 to 0.55 → ends at y=5.95
- Reduced caption height from 0.50 to 0.45 → ends at y=6.45 (clear of
  SourcesLine at 6.49)
- Constrained value-label boxes to `bar_w` (not `bar_w + 0.60`) so they
  no longer extend into the inter-bar gaps where the growth labels sit

After fixes: slide 13 shows only the documented breadcrumb false-positives.

### 6. s13_navy_50pct.py — 5× anchor + before/after horizontal bars

- **Title.** `Navy Industrial-Base Policy | Distributed shipbuilding from ~10 percent today to ~50 percent`
- **Visual.** 72pt `5×` anchor at top, two horizontal bars on a shared
  left edge:
  - Today (~10%) — narrow gray bar (GRAY_3), 1.40" wide
  - Plan target (~50%) — wide blue bar (BLUE_5), 7.00" wide
  - 5× ratio reads directly off the bar widths
- Labels left of bars (right-aligned), values right of bars
  (left-aligned). Both rows on the same baseline.
- **Caption.** Sources the May 2026 30-Year Shipbuilding Plan ("Golden
  Fleet" Plan), Maritime Industrial Base PMO June-2024 stand-up /
  September-2024 operational, and GAO-25-106286 $5.8B-FY14-FY23 +
  $12.6B-planned-FY28 funding levels.

### 7. s14_method_sources.py — 3×2 source grid + uncertainty card

- **Title.** `Method and Sources | Seven primary-source feeds; uncertainty band on the yard-side estimate`
- **Visual.** Six small data-source cards in a 3×2 grid (3.75" × 1.30"
  each, 0.24" h-gap, 0.20" v-gap — fills the 11.73" content band
  exactly):
  - Row 1: FPDS Atom Feed, SAM.gov FFATA Subawards, USAspending.gov
  - Row 2: DoD daily Contracts, SCN Justification Books, 10-K segment
    financials
  - Primary feeds in BLUE_4; cross-validation/secondary in BLUE_3.
- One wider uncertainty card below (full 11.73" wide × 1.30" tall, BLUE_1
  light-fill with C_DK1 body text): `$1.4B to $2.2B per year (point
  estimate ~$1.8B). Two convergent triangulation methods...`
- **Caption** (italic): Source-selection redaction on the FY23–FY27 MYP
  master is the dominant residual uncertainty in the dollar-weighted
  view.
- Listing only 6 cards rather than the spec's 7 — one of the seven feeds
  (SAM Entity Management API for NAICS) is folded into the SAM.gov FFATA
  Subawards card to keep the grid clean. The 7 in the title still reads
  correctly against ch 16's enumeration.

### 8. Wired all new modules

Added 5 entries to `build.py` SLIDES: `s10_other_gfe`,
`s11_divider_direction`, `s12_hii_outsourcing`, `s13_navy_50pct`,
`s14_method_sources`. Both dividers (s08, s11) were pre-built in part 2
and just needed wiring.

## Final deck state (15 slides)

```
1.  s00_cover                       — cover                  (slideLayout1)
2.  s01_answer_in_one_page          — Overview / Executive answer
3.  s02_cost_funnel                 — Overview / Cost funnel
4.  s03_production_baseline         — Overview / Production baseline
5.  s04_divider_sizing              — Sizing divider         (slideLayout2)
6.  s05_dod_pop_corpus              — Sizing / 87% outside yards
7.  s06_visibility_gap              — Sizing / 15% FFATA-visible
8.  s07_top_vendors                 — Sizing / Top 10 = 41% of flow
9.  s08_divider_layers              — Layers divider         (slideLayout2)
10. s09_aegis_spy6                  — Layers / Aegis + SPY-6 ≈ $5B (70%)
11. s10_other_gfe                   — Layers / 5 smaller GFE buckets
12. s11_divider_direction           — Direction divider      (slideLayout2)
13. s12_hii_outsourcing             — Direction / HII outsourcing 2×
14. s13_navy_50pct                  — Direction / Navy 10% to 50% (5×)
15. s14_method_sources              — Appendix / Method + sources
```

Build artifacts:
- `deck/out/destroyer_deck.pptx` — 15 slides, ~85 KB
- `deck/out/renders/destroyer_deck.pdf` + `slide-{1..15}.png` at 150 DPI

`python3 layout_check.py out/destroyer_deck.pptx` exits with only the
documented chrome false positives (breadcrumb overlap-with-Prelim,
breadcrumb spAutoFit overfill) on content slides plus the intrinsic
structural underfill on the 3 section dividers' big title blocks
(inherent to slideLayout2). Zero real layout flags on any slide.

## Key decisions and tradeoffs

- **Title disambiguation on s09.** DECK_SPEC's "two ~$5B megabuckets"
  reads as if each program is ~$5B. Reality: Aegis $3.55B + SPY-6
  $1.48B = together ~$5B. Asked user via AskUserQuestion; user
  confirmed the math-accurate wording over verbatim-spec wording.
- **Mixed dollar metrics on s10.** Three of the five buckets (VLS, Mk
  45, LM2500) have DoD-announcement TAM corpus rows; SEWIP and CIWS do
  not (SEWIP rolls into combat_systems; CIWS is excluded from SCN TAM).
  Used cumulative FFATA for SEWIP/CIWS with explicit unit labels on
  every card so the mixed sourcing reads cleanly rather than hiding.
- **CIWS shown but greyed.** Spec called for inclusion despite the WPN-
  funded exclusion from the SCN TAM gate. Greyed card (GRAY_5) + "WPN-
  funded, outside SCN TAM" meta line carries the methodological caveat
  visually without dropping the bucket from the slide.
- **Inferred hours on s12.** HII has publicly committed to "doubled in
  2025" + "30 percent for 2026" + "over 1 million hours in 2024" — but
  has not directly disclosed exact hour figures. Used the implied 1.0 /
  2.0 / 2.6M trajectory and flagged the inference in both slide docstring
  and DECK_SPEC. If HII discloses exact figures later, this is a one-
  variable update at the top of the data list.
- **Anchor-number rhythm preserved.** Big 72pt percentage / ratio anchor
  used on 4 of the 7 body slides:
  - s05 → `87%` (outside-yards POP)
  - s06 → `15%` (FFATA capture rate)
  - s12 → `2×`  (HII outsourcing growth)
  - s13 → `5×`  (Navy distributed-shipbuilding target)
  This is the deck's visual signature for the "one big idea per slide"
  spec convention. s07 / s09 / s10 / s14 broke the rhythm intentionally
  (bar charts / cards as the primary visual).
- **6 cards + 1 uncertainty card on s14, not 7 cards.** Spec said "six
  source-cards plus one wider methodology card"; collapsed SAM Entity
  Management (NAICS) into the SAM.gov FFATA Subawards card since both
  hit the same SAM.gov host and the NAICS feed is methodologically
  secondary. The slide title's "seven primary-source feeds" still reads
  correctly against the underlying wiki ch 16 enumeration.

## Known issues / open items

1. **s12 hours figures are inferred.** ~1.0M / ~2.0M / ~2.6M is the
   trajectory implied by Kastner's "doubled" + "30 percent" + "over 1
   million hours" language. HII has not disclosed exact hour figures.
   DECK_SPEC Open Question #3 covers this. Update one tuple if/when HII
   discloses precise values.
2. **s10 LM2500 meta says "single-supplier"** rather than the literal
   parser-residual "19 percent supplier-city". The 19% in
   `dod_action_pop_by_worktype.csv` is a parser artifact (GE bulletins
   often state a single city without a percent figure); the true POP
   is ~100% supplier-city. The slide elides the parser noise. A more
   complete parser patch would clean this up; tracked as open item in
   wiki ch 16.
3. **s14 caption references "DoD POP corpus" slide.** The cross-
   reference is to s05_dod_pop_corpus by topic, not by slide number,
   since slide numbers may shift if dividers are dropped in a future
   version.
4. **Wiki ch 6 prose error from part 2 not yet patched.** The wiki says
   "top 10 alone account for approximately $4.7 billion (34 percent)"
   but the actual computed value is $5.66B / 41%. The s07 slide uses the
   computed values. Patching ch 6 prose is still open per part 2's known-
   items list.
5. **Section dividers' title-block underfill** continues to trigger
   `layout_check` flags on slides 5, 9, 12. This is intrinsic to
   slideLayout2 (the layout reserves a 2.30" tall title block that the
   single-line "Sizing"/"Layers"/"Direction" text only fills 20% of). Not
   a real issue; cannot be fixed without rebuilding slideLayout2.

## How to view + extend

```bash
# View the deck
open /Users/brendantoole/projects2/destroyer_outsourced_work/deck/out/destroyer_deck.pptx

# Rebuild after any slide edit
cd /Users/brendantoole/projects2/destroyer_outsourced_work/deck
python3 build.py

# Re-render PDF + PNGs (LibreOffice headless)
soffice --headless --convert-to pdf --outdir out/renders out/destroyer_deck.pptx
pdftoppm -png -r 150 out/renders/destroyer_deck.pdf out/renders/slide

# Layout check
python3 layout_check.py out/destroyer_deck.pptx
```

## Files written this session

- `deck/slides/s09_aegis_spy6.py` (new)
- `deck/slides/s10_other_gfe.py` (new)
- `deck/slides/s12_hii_outsourcing.py` (new, patched once for layout)
- `deck/slides/s13_navy_50pct.py` (new)
- `deck/slides/s14_method_sources.py` (new)
- `deck/build.py` (wired s08, s09, s10, s11, s12, s13, s14 into SLIDES)
- `deck/out/destroyer_deck.pptx` (15 slides)
- `deck/out/renders/destroyer_deck.pdf` + `slide-{1..15}.png`

## What's left

The deck is complete against `DECK_SPEC.md`. Possible next-pass items:

1. **Spec reconciliation.** DECK_SPEC was authored before the slides
   landed; a few specifics drifted during authoring (s09 title math,
   s07 expected-leaders list, s14 card count). Reconcile DECK_SPEC text
   against the as-built slides if the spec is still treated as
   authoritative documentation.
2. **Real HII hours figures.** If HII discloses exact 2024 / 2025
   outsourcing-hour numbers (Q2 2026 earnings call due ~Aug 2026), update
   the `DATA` tuple at the top of `s12_hii_outsourcing.py`.
3. **Photographs/logos.** Slides are typography- and bar-only — no
   subject photos. The wiki has 8 placeholder JPGs at
   `image_assets/ddg_subject_photos/` which could be dropped into a
   visual-refresh pass.
4. **Hardening for cold-reader.** First-time viewers of the deck will
   benefit from a 30-second-per-slide narration. If the deck is going to
   a stakeholder review, draft a one-line speaker note per slide.

## How to resume

Point the next session at:
1. `DECK_SPEC.md` (root) — the authoritative spec
2. This log + parts 1 and 2
3. `deck/slides/` — 15 slide modules (12 body + cover + 3 dividers — note
   the `s00` cover uses slideLayout1, the dividers use slideLayout2 via
   `LAYOUT = DIVIDER_LAYOUT`, all other modules default to slideLayout4)
4. `wiki_ddg/*.md` for source data on any future edits

Total target slides: **15 — all built, no slots open.**
