# 2026-06-03 — cover/divider copy guidance, chart-annotation overlays, lint demotion, cover/divider content, research import

## Scope

A core-pipeline + content session on the **light** workspace, in five threads:

1. Add real authoring guidance for **cover and section-divider copy** (there was none).
2. Incorporate two **chart-annotation overlay** patterns (oval value badge, wedge
   pointer callout) as *encouraged, not enforced* recipes, plus the one generic
   primitive they need.
3. **Demote** the probe's taste rules (sharp-rect discipline, hero/border
   hierarchy) from blocking lint violations to non-blocking notes — they were
   fighting deliberate visual choices.
4. **Audit + rewrite** the submarines cover/dividers and **author** net-new DDG
   cover/dividers, grounded in each deck's specs.
5. **Move** three external `research/` trees into the workspace.

This task was explicitly a change to the **core engines**, so the locked-core
rule (README) was suspended for `deck_core/`. Workspace is **not** under git —
edits/moves were direct, with a build re-run after each content change. All
deck builds green at the final state.

Decisions taken (via in-session questions):
- Chart overlays: **full proposal**, including the generic `geom_adj` primitive.
- Cover footer: **date only** (`Month YYYY`) — no fidelity word, no separator.
- Lint: **demote taste, keep correctness** (notes, not violations).

---

## 1. Core engine — `primitives.py`: generic preset-geometry adjustments

`text_box()` previously hard-coded an empty `<a:avLst/>`, so non-rect presets
that need adjustment handles (callout tails, custom corner radii) couldn't be
expressed. Added:

- `_prst_avlst_xml(geom_adj=None)` — builds `<a:avLst>` from a `{name: value}`
  map (ints → `val N`; strings used verbatim as the formula); empty/None →
  `<a:avLst/>` (byte-identical to the old default).
- New `geom_adj=None` kwarg on `text_box()`, wired into the `<a:prstGeom>` line.

This is a **generic capability** (preset-geometry handles), not a callout-specific
feature. Verified: default path still emits `prst="rect"><a:avLst/>`; a
`wedgeRectCallout` with `{"adj1": -25000, "adj2": 65000}` emits the two `<a:gd>`
handles; string formulas pass through unchanged.

## 2. Core engine — `slide_probe.py`: lint demotion + overlay classification

The sharp-rect rule and the "one hero / few heavy borders" hierarchy rules were
turned from **violations** into **non-blocking notes**, so the probe stops
fighting intentional non-rect overlays. Correctness checks stay as violations.

- New `check_taste_notes(shapes)` holds the demoted checks (non-rect geometry,
  >1 hero run, >4 1.5pt borders). The CLI prints them as `~ … note —` lines and
  never sets the non-zero exit.
- `check_lint()` keeps the **correctness** guards only: explicit size + Arial
  font, filled-shape border rule, tight-inset clipping, no-fill-border naming,
  and **table-fit overflow**.
- Replaced the flat `APPROVED_NON_RECT_PRSTS` / `APPROVED_NON_RECT_NAME_TOKENS`
  with a per-preset map `APPROVED_NON_RECT_BY_PRST` (`roundRect`→Tag/Classification,
  `ellipse`→StepDot/Dot/**ChartValueBadge/ValueBadge**, `chevron`→Chevron,
  **`wedgeRectCallout`→PointerCallout**). It now only **suppresses the note** for
  recognized, intentionally named roles — nothing is blocked.
- Added a **"Preset geometry adjustments"** section to the Markdown report
  (`prst_avlst` was already in JSON but invisible in MD), so callout tails are
  inspectable. Updated `--lint` help + `check_lint` docstring.

Effect on the existing decks (lint is strictly more permissive now): the
`tam_bridge` `mathMultiply` shape that previously **failed** lint is now a soft
note; recognized `StepDot`/`Tag`/`Chevron` shapes stay silent. The 4 remaining
`x` violations on submarines slides 1/2/6/14 are **pre-existing** (cover/divider
placeholders `CoverTitle`/`CoverFooter`/`DividerTitle`/`DividerSubtitle` inherit
font from the layout and aren't tagged `chrome_role`) — untouched here, flagged
as a separate future cleanup.

## 3. Core docs — `slide_guide.md` + `slide_snippets.md`

`slide_guide.md`:
- New **"Cover and divider copy"** section. Anchors the *locked* type (title 28pt
  non-italic, subtitle 20pt italic — the part the existing modules got right) and
  governs only the wording:
  - **Cover** — Title: short Title-Case noun phrase, names the engagement, no
    verb/period; Subtitle: scope-first, sentence case, time horizon as a
    subordinate trailing qualifier; Footer: **date only**, `Month YYYY` (no draft
    marker — cover/divider carry no Preliminary chip by design).
  - **Divider** — Title: Title-Case noun phrase, no numbering; Subtitle: the
    section's governing thought stated **qualitatively**, with the worst→best
    **ladder** (agenda ✗ → process ✗ → numeric ✗ → qualitative ✓), illustrative
    forms, and the **fallback** (drop the subtitle rather than force a claim;
    never fall back to an agenda list).
- Extended the visual-vocabulary item (4) to allow **chart-annotation overlays**
  (`_chart_value_badge`, `_pointer_callout`) and note the probe now *notes*
  rather than rejects non-rect geometry; extended callout-restraint item (5) so a
  **pointer callout does NOT count** against the one-filled-focal-callout budget
  (it's a deictic chart annotation, not the page's editorial callout); extended
  the chart-data-labels line to distinguish native `c:dLbls` from manual overlays.
- **"Building a slide"**: removed the **stale** step ("Rename the `render`
  function to match the filename" — every module keeps `render()`, the registry
  calls `module.render`), renumbered, and added a **"Module naming"** note:
  `cover_*` (slideLayout1) / `divider_*` (slideLayout2) / `appendix_*` / plain
  body names; cover+divider skip the base template and call the layout builders
  directly.

`slide_snippets.md` (recipes only — encouraged, not promoted to core):
- "chart annotation overlays" note: native `c:dLbls` vs manual `<p:sp>` overlays;
  append the overlay **after** the `graphic_frame` (paint order); name them so the
  probe classifies them; don't call them `DataLabel`.
- `_chart_value_badge` (ellipse via `text_box(prst="ellipse")`, GRAY_3 0.75pt
  secondary border) and `_pointer_callout` (`wedgeRectCallout` via the new
  `geom_adj`, with the signed-offset adj math), plus a layered `_body()` example.

## 4. Content — submarines audit + rewrite, DDG net-new

Submarines cover/dividers were audited against the new guidance and rewritten
(the existing examples were explicitly **not** treated as correct). Caught and
corrected one cross-contamination: the submarines **TAM Build** divider must use
the *coefficient-evidence* story (strict 35% coefficient, AP/LLTM adds $0), not
DDG's redaction story.

- **Submarines** (`deck_submarines/slides/`):
  - Renamed cover module `market_sizing_assessment.py` → **`cover_market_sizing_assessment.py`**
    (role prefix); title → `Submarine Supplier Market Sizing`; subtitle →
    `TAM and SAM for the U.S. submarine new-construction supplier base, average annual FY2022–FY2027`
    (scope-first, window de-emphasized as *average annual*, en dash); footer →
    `June 2026` (was `Preliminary | June 2026`).
  - Divider subtitles rewritten to qualitative, deck-accurate lines:
    Market and Scope → *"…narrow layer inside a much larger procurement ecosystem"*;
    TAM Build → *"…one deliberately strict coefficient, even where the evidence would support more"*;
    SAM and Supplier Landscape → *"…a menu of work types, and the visible suppliers are a concentrated floor"*;
    Interpretation → *"What the data shows is a visible floor, not the full supplier layer"*.
  - Registry import + tuple updated for the renamed cover; old file removed.
  - Slide count unchanged (**25**).

- **DDG** (`deck_ddg/slides/`) — had **no** cover/dividers; opened straight into
  `market_primer`. Added net-new, grounded in DDG specs, **without reordering**
  body slides:
  - `cover_market_sizing.py` — `DDG-51 Supplier Market Sizing` /
    `TAM and SAM for the DDG-51 new-construction supplier base, average annual FY2022–FY2027` /
    `June 2026`.
  - `divider_market_and_scope.py` — *"The supplier-addressable market is a narrow slice of total DDG-51 spend"*.
  - `divider_tam_build.py` — *"Two supplier streams build the market, and a single year carries an outsized share"*.
  - `divider_sam_work_types.py` — *"The serviceable market is a menu of work types, not a single capture number"*.
  - Registry: cover first, then a divider before each of the three body sections
    (Market and Scope: primer/exec/scope; TAM Build: cost_funnel/myp_redaction/
    methodology/annual_build/timing; SAM and Work Types: taxonomy/allocation),
    appendix untouched. Slide count **16 → 20** (7 charts unchanged).

## 5. Research trees moved into the workspace

`mv` (same volume → fast renames) from `../distributed_shipbuilding/`:

| Source | Destination | Files | Size |
|---|---|---|---|
| `research_shared` | `projects/research_shared/` | 19 | 48M |
| `ddg/research` | `projects/ddg/research/` | 2,590 | 361M |
| `sub/research` | `projects/submarines/research/` | 2,106 | 264M |

Verified: file counts + sizes match the originals; sources removed. These land
**outside** the build paths (builders read only `deck/`, `workbook/`, `infra/`),
so no build is affected. (README layout updated — see Follow-ups below.)

---

## 6. Follow-ups — README, divider positioning, lint quirk

Done after the initial write-up, in response to live review:

- **README.md** — documented the moved research trees and the module-naming
  convention. The layout block now lists `projects/research_shared/` and a
  `research/` under each project (each marked *not read by any build*); the
  Authoring-model → Decks bullet names the `cover_*` (slideLayout1) / `divider_*`
  (slideLayout2) / `appendix_*` / plain-body file-role prefixes. The same
  "Module naming" note was added to `slide_guide.md`'s Building-a-slide steps,
  and a stale "rename the `render` function" step was removed (every module
  keeps `render()`; the registry calls `module.render`).

- **Divider positioning matched to the cover** (`primitives.py`
  `section_divider_layout`). The dividers used two *inherited* slideLayout2
  placeholders (`idx=11` title at y=2383743, a separate `idx=12` subtitle at
  y=4715093) — neither coincided with the cover's single block. Folded the title
  (line 1) + subtitle (line 2) into **one `idx=11` placeholder** with the cover's
  geometry override, so the two lines land exactly where the cover's do.
  (For the record: `cover_layout`'s override is *width-only* — its y/cy already
  equal the inherited layout values — so the original vertical mismatch lived in
  the two layout definitions, not the override.)

- **Top-anchor fix (wrapping)** — a long subtitle that wraps to a 2nd line was
  pushing the title **up** (a bottom-anchored block grows upward). Switched both
  `cover_layout` and `section_divider_layout` to **`anchor="t"`** and pinned the
  block low at **`y=4140000`** (≈ where the bottom-anchored 2-line cover title
  already sat, and clear of the cover footer). Now line 1 is fixed and the
  subtitle grows **downward**; all divider titles align regardless of subtitle
  length, and the cover stays matched.

- **Lint quirk fixed** (`slide_probe.py`). The typography "explicit size + Arial
  font" check now skips **placeholder-bound shapes** (`s.is_placeholder`) —
  cover/divider title/subtitle/footer inherit size/font from the layout by
  design, so flagging them was a false-positive. Body content shapes (`text_box`,
  no placeholder) are unaffected and still checked. This retires the pre-existing
  false-positives noted earlier; both decks now lint **clean** (0 violations),
  with only the intentional `mathMultiply` `~` note remaining.

---

## Verification

| Build | Result |
|---|---|
| submarines deck | green — **25** slides, 5 charts |
| ddg deck | green — **20** slides, 7 charts |
| `geom_adj` unit checks | default `<a:avLst/>` preserved; int→`val N`; string fmla verbatim; ellipse badge clean |
| probe import | `check_taste_notes` present; `APPROVED_NON_RECT_BY_PRST` replaces the old flat constants |
| lint demotion (sub pptx, `--all --lint`) | non-rect `mathMultiply` now a `~` note; recognized non-rect suppressed; only pre-existing font violations remain as `x` |
| rendered cover/divider text | all titles/subtitles/footers correct; en dash + `June 2026` confirmed from the registries |
| divider → cover geometry | cover + all dividers share `off=(453080, 4140000)`, `ext=(11285842, 2162129)`, `anchor="t"` |
| lint after quirk fix | both decks **0 violations**; cover/divider placeholders no longer flagged; only the `mathMultiply` `~` note remains |

## Files touched

- Core: `deck_core/primitives.py` (geom_adj; divider single-box + top-anchor),
  `deck_core/slide_probe.py` (lint demotion; placeholder typography skip),
  `deck_core/slide_guide.md`, `deck_core/slide_snippets.md`.
- Top-level: `README.md` (research folders + module-naming convention).
- Submarines: `slides/cover_market_sizing_assessment.py` (new, replaces
  `market_sizing_assessment.py`), `slides/divider_{market_scope,tam_build,sam_supplier,interpretation}.py`,
  `slides/__init__.py`.
- DDG: `slides/cover_market_sizing.py`, `slides/divider_market_and_scope.py`,
  `slides/divider_tam_build.py`, `slides/divider_sam_work_types.py` (all new),
  `slides/__init__.py`.

## Open items / follow-ups

- **Submarines `divider_sam_supplier`** subtitle was refreshed but the module is
  still intentionally **unwired** (its SAM/Supplier section S12–S16 isn't built).
- **DDG section assignment** placed `cost_funnel`/`myp_redaction` under TAM Build
  (denominator → correction → method → build → timing); revisit if those read
  better under Market and Scope.
- The new chart-overlay recipes (`_chart_value_badge`, `_pointer_callout`) are
  available but **not yet used** by any slide — first real use will exercise the
  `geom_adj` tail math end-to-end.
