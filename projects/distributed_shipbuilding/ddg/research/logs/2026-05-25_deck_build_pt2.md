# Deck build session — 2026-05-25 (part 2)

Continuation of the destroyer-outsourced-work deck build. Companion to
`DECK_SPEC.md` at the project root and to `2026-05-25_deck_build.md`
(part 1, which produced s00..s03).

## Context at session start

- Deck had four slides done: `s00_cover`, `s01_answer_in_one_page`,
  `s02_cost_funnel`, `s03_production_baseline`. All in the Overview section,
  aggressive one-big-idea-per-slide style locked in.
- `DECK_SPEC.md` described 11 more planned slides: 4 section dividers
  (Sizing, Layers, Direction, plus an unreferenced fourth) + 6 body slides
  + 1 appendix. Spec Open Question #1 (keep dividers or drop them) still
  unanswered.
- `deck/` was self-contained (slim-copied chrome at `deck/_extracted/` and
  `deck/assets_deck/`). Build pipeline (`build.py`, `builder.py`,
  `primitives.py`, `style.py`, `layout_check.py`) unchanged.
- Live data sources: `extracted/dod_action_pop_by_worktype.csv`,
  `extracted/nc_lifetime_vendors.csv`, wiki chapters 4 / 5 / 6 / 9.

## Work completed

### 1. Microsoft PresentationML doc review (no code change)

User pointed at `https://learn.microsoft.com/en-us/office/open-xml/presentation/overview`
and asked whether anything in it should inform the next slide. Read both
the overview and the deeper "Structure of a PresentationML document" page.

Conclusion: nothing operationally new — the pipeline already implements
the rules the doc describes (package parts, Content_Types overrides,
slide→layout→master inheritance via per-slide rels, `<p:clrMapOvr>` with
`<a:masterClrMapping/>`, 13.333" × 7.5" canvas, unique `<p:cNvPr id=...>`
per slide with id=1 reserved for the group shape). Re-confirmed four
disciplines to keep in mind while authoring: don't pass `sp_id=` overrides
in the reserved range (2/3/4/9999/100/101/110/111); don't set a module-
level `LAYOUT` constant on normal content slides (default `slideLayout4`
is right); stay within the bounds the builder validates; give every shape
a descriptive `name=` for the audit trail.

### 2. s05_dod_pop_corpus.py — the headline 87% finding

- **Title.** `DoD POP Corpus | 87 percent of disclosed dollars flow outside both yards`
- **Visual.** Big 72pt "87%" as anchor with one-line subhead; full-width
  horizontal stacked bar with four segments (BIW 11.2% BLUE_5, Ingalls
  1.3% BLUE_4, U.S. supplier cities 73.6% BLUE_2, residual 13.9% GRAY_3);
  two city callouts pinned beneath the supplier-cities segment with thin
  vertical connectors (Moorestown NJ / Aegis Combat System; Andover MA /
  AN/SPY-6(V)1 radar); caption with the MYP-redaction caveat.
- **Implementation notes.** Ingalls segment (0.15" wide) too narrow to
  hold inside text — labeled below the bar with a 0.10" tick connector.
  Pin connectors drop from bar bottom (y=3.95) to callout top (y=4.55).
  Data from `extracted/dod_action_pop_by_worktype.csv` (152 supplier-TAM
  rows / $7.13B corpus).

### 3. s06_visibility_gap.py — FFATA captures ~15% of the true flow

- **Title.** `Visibility Gap | FFATA catches about 15 percent of the true yard-side flow`
- **Visual.** Big 72pt "15%" anchor + subhead; two side-by-side vertical
  bars on a common baseline at y=5.30 with max_h=2.10"; bar heights scaled
  to dollar values so the 15.9% ratio reads off the chart directly ($286M
  bar = 0.334" tall vs $1.8B bar = 2.10"); dashed horizontal "visibility
  line" at the small bar's top extends across to the big bar marking
  where the eye stops with only FFATA data; centered gap annotation in
  the upper portion ("The unseen: about $1.5B per year" header + 4
  short bullets); caption naming the triangulation methods.
- **Layout fix needed.** First build flagged a real 0.02" overlap between
  the subhead box (ends y=2.87) and the bar-B value-label box
  (started y=2.85). Tightened the value-label box from h=0.30 to h=0.27
  and shifted up to bar_top - 0.32. Margin to subhead 0.05" — clean.

### 4. s07_top_vendors.py — top 10 parent vendors

- **Title.** `Vendor Concentration | Top 10 parent vendors absorb most of the visible flow`
- **Visual.** Horizontal bar chart, 10 rows, ranked by lifetime in-scope
  FFATA-visible dollars (sourced from `extracted/nc_lifetime_vendors.csv`,
  re-tabulated in wiki ch 6). Each row: rank + vendor name + proportional
  BLUE_4 bar + right-aligned dollar label at fixed x for column-scan.
  Header row with thin black rule. Country code suffixes "(IT)" / "(UK)"
  on the two foreign-parent vendors. Caption computes the sum and
  percentage dynamically so the visible bars can't drift from the
  reported totals.
- **Spec note.** DECK_SPEC.md's "Expected leaders" list (LM, RTX, NG,
  BAE, GE Aero, L3Harris) refers to the GFE *primes* — the upper-tier
  contractors who *receive* DoD contracts. The FFATA-visible top-10
  recipients are different — they are the *subawardees* those primes
  report paying. Slide title and chart use the actual recipient data,
  not the spec's prime list, since FFATA is the data source.

### 5. Wiki ch 6 arithmetic error discovered

While building s07, the computed sum across the displayed top-10 came out
to $5.66B = 40.9% of the $13.84B in-scope total. The wiki ch 6 prose says
"top 10 alone account for approximately $4.7 billion (34 percent)". The
per-row dollar values in the wiki's own table (which I cross-checked
against `extracted/nc_lifetime_vendors.csv` — exact match) sum to $5.66B.
The wiki's $7.3B / 53% figure for the top 25 is roughly correct ($7.46B /
53.9% actual).

Used the computed values in the slide (so the slide is internally
consistent: bars sum to caption number). The wiki ch 6 prose needs a
correction — flagged in the open-items list below.

### 6. Section dividers — wrote all three, wired only Sizing

User answered Open Question #1: keep the dividers. Built all three
divider files (each is ~12 lines, uses `SlideBuilder.divider(...)` with
`LAYOUT = DIVIDER_LAYOUT` at module scope):

- `s04_divider_sizing.py` — "Sizing" / "Direct evidence for the outsourced-share number" — **wired into the deck between s03 and s05**.
- `s08_divider_layers.py` — "Layers" / "What the GFE dollars actually buy" — **not wired yet** (Layers body slides s09/s10 don't exist).
- `s11_divider_direction.py` — "Direction" / "Why the outsourced layer is growing" — **not wired yet** (Direction body slides s12/s13 don't exist).

Rationale for deferring the unwired dividers: a divider with no body
slides after it would create a dead-end page. The two divider modules
exist as files and will be wired when their respective sections begin.

## Final deck state (8 slides)

```
1. s00_cover                       — cover                  (slideLayout1)
2. s01_answer_in_one_page          — Overview / Executive answer
3. s02_cost_funnel                 — Overview / Cost funnel
4. s03_production_baseline         — Overview / Production baseline
5. s04_divider_sizing              — Sizing divider         (slideLayout2)
6. s05_dod_pop_corpus              — Sizing / 87% outside yards
7. s06_visibility_gap              — Sizing / 15% FFATA-visible
8. s07_top_vendors                 — Sizing / Top 10 = 41% of flow
```

Build artifacts:
- `deck/out/destroyer_deck.pptx` — 8 slides, ~62 KB
- `deck/out/renders/` — PDF + PNG per slide at 150 DPI for visual review

`python3 layout_check.py out/destroyer_deck.pptx` exits with only the
documented false positives (breadcrumb-overlaps-Prelim, breadcrumb
spAutoFit overfill) on content slides, plus the structural underfill on
the Sizing divider's big title block (intrinsic to slideLayout2).

## Key decisions and tradeoffs

- **Stayed on the s05/s06 hero-number layout.** Big 72pt percentage at
  the top + primary visual below + caption below that. Same vertical
  rhythm across both sizing slides. s07 broke the rhythm intentionally —
  the bar chart IS the visual; no separate hero number — to keep the
  deck visually varied.
- **Computed s07's caption from the displayed data.** Hardcoding the
  wiki's $4.7B / 34% would have made the slide internally inconsistent
  (visible bars sum to a different number than the caption). The slide
  now computes `top10_sum_b`, `top10_pct`, and `tail_b` from the
  `TOP_VENDORS` list so the caption can't drift from the visual.
- **Wired only the Sizing divider.** The other two dividers sit ready in
  `deck/slides/` but aren't in `SLIDES` because their following content
  doesn't exist yet. Avoids dead-end pages in the current build.
- **Kept the spec's "Expected leaders" list for s07 even though it was
  wrong.** Spec said expect LM / RTX / NG / BAE / GE / L3Harris in the
  top 10 — those are GFE primes, but the FFATA top-10 is subawardees.
  Used the actual data (Leonardo, Arctic Slope, Major Tool & Machine,
  GD, GE, RR, NG, JCNS, AS&T, Cobham). Spec wording can be reconciled in
  a future pass.

## Known issues / open items

1. **Wiki ch 6 prose fix needed.** `wiki_ddg/06-vendors-and-concentration.md`
   line 41 says "top 10 alone account for approximately $4.7 billion
   (34 percent)" — actual is $5.66B (41%). Find with `grep "$4.7 billion" wiki_ddg/06-vendors-and-concentration.md` if reconciling.
2. **MYP-adjusted 33–40% view on s05** lives in the caption only, not
   as a visual overlay on the bar. Acceptable per spec, but a reviewer
   might want a small annotation showing the MYP-adjusted bar zone.
3. **Top-10 dedup of Major Tool & Machine.** The CSV has two UEIs for
   Major Tool & Machine ($816M rank 3 + $132M rank 15). The slide shows
   only the rank-3 UEI, so the consolidated parent-company total ($948M)
   isn't represented. Material? Probably not for the headline, but the
   #3 row understates by ~$130M.
4. **Layers + Direction dividers unwired.** Pre-built as
   `s08_divider_layers.py` and `s11_divider_direction.py`. Add to
   `build.py` SLIDES list before their respective body slides land.

## Next session

Per `DECK_SPEC.md`, the work queue is:

- **Layers section** (3 slides):
  - Wire `s08_divider_layers.py` into SLIDES
  - `s09_aegis_spy6.py` — two ~$5B GFE megabuckets (LM Moorestown, RTX Andover)
  - `s10_other_gfe.py` — VLS, Mk 45, LM2500, SEWIP, CIWS
- **Direction section** (3 slides):
  - Wire `s11_divider_direction.py` into SLIDES
  - `s12_hii_outsourcing.py` — HII outsourcing doubled in 2025; +30% guided 2026
  - `s13_navy_50pct.py` — Navy 10% → 50% distributed-shipbuilding target
- **Appendix** (1 slide):
  - `s14_method_sources.py` — methodology + uncertainty band

Total target if all built: 14 slides (cover + 3 overview + Sizing divider +
3 sizing + Layers divider + 2 layers + Direction divider + 2 direction +
1 appendix).

Before authoring s09 the spec needs the exact Aegis and SPY-6 cumulative
subaward-dollar figures pulled from wiki ch 10 (Open Question #2).

## How to resume

Point the next session at:
1. `DECK_SPEC.md` (root)
2. This log + `logs/2026-05-25_deck_build.md` (part 1)
3. `deck/slides/` — the 7 existing slide modules + 3 divider modules
4. `wiki_ddg/10-aegis-and-spy6.md` and `wiki_ddg/11-other-gfe.md` for s09
   and s10 data
5. `wiki_ddg/13-executive-commentary.md` and `extracted/exec_quotes_outsourcing.md`
   for s12 (HII outsourcing-hours numbers)
