# 2026-06-07 — Appendix: source-line / terminology de-jargon (5 slides) + archive the old appendix modules

## Scope

Two follow-on passes on the consolidated deck (`projects/consolidated/deck`), continuing from
`2026-06-07_consolidated_appendix_methodology_slides_and_two_polish_passes.md`:

1. **De-jargon pass** across the five appendix methodology modules — pull internal workbook/model
   nouns out of the visible **source footers**, delete the leftover "workbook term" chip, and make
   **"supplier-share factor"** the single canonical term (drop "coefficient" / "workbook" from visible
   copy). Deck stayed **green at 29 slides / 4 charts**.
2. **Archive pass** — moved the six *older* appendix content modules to a new `deck/archived/` folder and
   pulled them out of the build registry, slimming the appendix to the section divider + the five new
   methodology slides. Deck rebuilds **green at 23 slides / 4 charts**.

Governing rule adopted this session for the source boxes: **keep workbook sheet names / internal model
nouns in code comments, figure registers, or methodology notes — not in the slide footer.** The footer
answers one question: *what external evidence did this page ultimately rely on?* Recurring source families
across the five slides:

```
Navy SCN budget justification books / P-5c / P-10 exhibits
DoD/DoW contract-announcement POP corpus
FPDS Atom feeds (where prime / MYP reconstruction matters)
SAM.gov FSRS / FFATA first-tier subaward records
SAM.gov Entity API and USAspending UEI / NAICS enrichment
Program scope-exclusion / PIID records
```

Standing conventions from prior sessions still honored: no internal M-series codes in visible copy
(`no-m-series-codes-in-visible-slide-copy`), bare black arithmetic AutoShapes, `$M` stays `$M` / `$B`
rounded to one decimal, white equation cards (the reverted-to colors), and zero em-dashes in rendered
text on slides 26–29.

## Pass 1 — de-jargon (5 files)

### `appendix_supplier_share_pop_conversion.py` (slide 27)
- **Deleted the right-side `WorkbookTermChip`** ("Workbook term: applied supplier coefficient") entirely —
  it introduced a second label for the same concept. Removed the `_DEF_CHIP_*` geometry block (replaced
  with `_DEF_RINS = 140_000`), the `def_chip` text_box, and `def_chip` from the return tuple. The
  definition strip now spans the **full body width** (12.34 in).
- **Rewrote the definition strip:** "Supplier-share factor = conversion rate that turns retained budget
  dollars into outsourced supplier TAM. It answers: for every $1 of retained budget base, how many cents
  become supplier work?"
- Formula-machine title: "How POP evidence becomes the conversion factor" → "…the **supplier-share
  factor**".
- `_COMMENTARY`: "The coefficient is a conversion rate…" → "The **supplier-share factor** is a conversion
  rate…"; "…blending coefficients." → "…blending **supplier-share factors**."
- `_SOURCES`: workbook tabs (DDG/sub TAM Build, POP Corpus, AP Bridge) → DoD/DoW POP corpus CY2022–CY2026;
  FPDS Atom feeds + DDG MYP master-total reconstruction; Navy SCN P-5c / P-10 budget exhibits FY2022–FY2027.
- Cleanups: removed now-unused `GRAY_2` import; dropped "workbook chip" from the `_SZ_BODY` comment;
  docstring opener "coefficient" → "supplier-share factor".

### `appendix_methodology_roadmap.py` (slide 25)
- `_SOURCES` → Navy SCN budget justification books FY2022–FY2027; DoD/DoW POP corpus CY2022–CY2026;
  SAM.gov FSRS / FFATA subawards + SAM.gov / USAspending UEI / NAICS enrichment FY2017–FY2026.
- First reader-key chip body: "Plain-English name for the workbook coefficient: how many cents…" →
  "**Conversion rate** showing how many cents of each retained budget dollar become outsourced supplier
  work." (removes "workbook coefficient"; the chip's formula line was already canonical).

### `appendix_tam_budget_base_scope_gates.py` (slide 26)
- `_SOURCES` → Navy SCN budget justification books FY2022–FY2027; P-5c Basic Construction and P-10 AP/LLTM
  budget exhibits; DDG-51, Virginia, and Columbia scope-exclusion reconciliations.
- Ledger handoff guardrail (row 5, RETAINED OUTPUT cell): "No blended **coefficients**; no supplier TAM
  yet" → "No blended **supplier-share factors**; no supplier TAM yet".

### `appendix_sam_classification_field_audit.py` (slide 28)
- `_SOURCES` (was internal model nouns — "parent-prime PIID scope arbiter", "operating-entity supplier
  registry", "NAICS-4 fallback classifier") → SAM.gov FSRS / FFATA first-tier subaward records
  FY2017–FY2026; SAM.gov Entity API + USAspending UEI / NAICS enrichment; FPDS / DoD PIID records and
  program scope-exclusion registers.

### `appendix_sam_allocation_scenario_views.py` (slide 29)
- `_SOURCES` (biggest cleanup; the old footer cited model logic — "SAM Build tabs", "scenario inclusion
  matrices", "bucket-to-scenario crosswalk") → SAM.gov FSRS / FFATA subaward records FY2017–FY2026;
  SAM.gov Entity API / USAspending NAICS enrichment and work-type evidence; DoD/DoW POP corpus and Navy
  SCN budget books supporting fixed supplier TAM. Used the **full** version (shorter than the original
  4-segment line that already rendered fine), not the optional shortened variant.

## Pass 2 — archive the old appendix modules

- **Created** `projects/consolidated/deck/archived/` (a plain folder — no `__init__.py`, so it is out of
  the package / build).
- **Moved six modules** out of `deck_consolidated/slides/` → `archived/`:
  - `s18_appendix_definitions_terminology.py`
  - `m1_revised_sizing_approach.py`
  - `m2_revised_tam_methodology.py`
  - `m3_revised_sam_methodology.py`
  - `s19_appendix_method_deltas.py`
  - `s20_appendix_bucket_scenario_crosswalk.py`
- **Pulled them from the registry** (`slides/__init__.py`): deleted the six `from . import …` lines and the
  six `SLIDE_RENDERS` tuples; refreshed the structure docstring and the appendix comment to point at
  `deck/archived/`.
- **Kept `divider_appendix`** in the build — it is the section divider, not a content slide; without it
  the deck would jump from the last evidence slide straight into the methodology roadmap. (Trivially
  reversible if the divider should also be archived.)

Appendix order is now: **divider → methodology roadmap → TAM budget base → supplier-share conversion →
SAM classifier → SAM allocation** (divider + 5 slides).

## Verification

`build_deck.py`: **green at 29 slides / 4 charts** after Pass 1; **green at 23 slides / 4 charts** after
Pass 2 (29 − 6 archived; none of the six carried `CHARTS`, so chart count held at 4). QA via
`deck_core/slide_probe.py <pptx> --slide N --table-fit --text-estimate`:

- **Slide 26 ledger fits** after the longer handoff cell: authored == estimated 2,316,480 EMU (2.533 in),
  estimated bottom 5.022 in within `BODY_B` (5.870 in), **no rows short**, ~0.26 in clearance to the strip.
- **Slide 27**: no real content overflow. Definition strip now full width (12.339 in), `fits=True`. The
  only `fits=False` flags are the known false-positives — empty operator AutoShapes (`avail 0.000`,
  phantom `endParaRPr` line) and the locked breadcrumb chrome (`avail 12.139`).
- **Source lines** all `fits=True`: slides 25 & 29 wrap to 2 lines inside the 0.491-in footer (the longest
  two), slide 28 to one line.
- **Sweeps on slides 26–29**: 0 `coefficient` / `workbook`, 0 M-series codes, 0 em-dashes in rendered
  text. Spot-checked rendered strings: definition strip, formula title, and the row-5 handoff cell all
  read as intended.
- Pass 2: confirmed via grep that **no other module imported any of the six** (references existed only in
  `__init__.py` + the files' own docstrings); the post-move rebuild proves the registry is clean.

## Gotchas / notes

- **Editing live files, not the snapshots.** The de-jargon instructions referenced `updated2_appendix_*.py`
  filenames, but those are the reference snapshots at the projects3 root. The standing instruction was to
  "pay no heed to the `updated2_` prefix" and edit the live modules under `deck_consolidated/slides/`. The
  `updated_slides/` and `updated2_slides/` snapshots at the projects3 root are now **stale** relative to
  the live files.
- **En-dash vs em-dash.** The new source lines use en-dashes (`–`) in the FY/CY ranges (e.g.
  `FY2022–FY2027`), which is the existing house convention for ranges and is *not* what the em-dash sweep
  targets. Slides 26–29 stay at 0 em-dashes in rendered text.
- **Pre-existing em-dashes on the roadmap (slide 25):** the two chapter-band labels still read
  "TAM CHAPTER — BUILD THE FIXED DOLLAR POOL" / "SAM CHAPTER — ALLOCATE THE FIXED POOL". These predate
  this session — the roadmap was deliberately excluded from the prior em-dash→colon cleanup (which only
  covered 26–29) — and were left untouched here. Open follow-up if the zero-em-dash convention should
  extend to slide 25.
- **Probe report scaffolding uses `—`.** A naive `grep -c "—"` over the probe markdown returns 46–130 per
  slide; those are the report's own empty-cell markers (`| sp | — |`), not slide text. Filter to quoted
  paragraph lines (`^\s*[0-9]+\.\s+"`) to count em-dashes in rendered copy.

## Current state / how to resume

- **Green, 23 slides / 4 charts.** The five appendix methodology modules carry the de-jargoned source
  footers and the canonical "supplier-share factor" wording; the `WorkbookTermChip` is gone.
- **`deck/archived/`** holds the six retired appendix modules (out of the build; still wired to
  `deck_core`, so reference snapshots — not runnable from that folder).
- `divider_appendix` retained; one-line revert if it should also be archived.
- Snapshot copies at the projects3 root (`updated_slides/`, `updated2_slides/`) are stale; refresh if a
  current reference snapshot is wanted.

```
cd projects/consolidated/deck
/usr/bin/python3 build_deck.py        # -> 23 slides, 4 charts
cd ../../..
/usr/bin/python3 deck_core/slide_probe.py \
    "projects/consolidated/20260605_Distributed Shipbuilding Consolidated_vS.pptx" \
    --slide 22 --table-fit --text-estimate --out-dir /tmp/probe
# appendix is now: 18=divider 19=roadmap 20=TAM base 21=supplier 22=classifier 23=allocation
```
