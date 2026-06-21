# Sea-Range Telemetry — alternative_v1 methodology slides (s05–s08)

**Date:** 2026-06-08
**Pipeline:** `projects/sea_range_telemetry/deck/deck_sea_range_telemetry`
**Engine:** shared `deck_core` (no vendored copy)

## Goal

Build four new methodology slide modules from the `specs/alternative_v1/` spec set
and wire them into the `deck_sea_range_telemetry` build so they render **after** the
existing four appendix slides (s01–s04). Per the user: use the specs and the
`deck_core` core files as the guide; do **not** model the new slides on the existing
s01–s04 modules (the user is not a fan of them).

Specs consumed:
- `specs/alternative_v1/01_methodology_roadmap.md`
- `specs/alternative_v1/02_evidence_streams.md`
- `specs/alternative_v1/03_tam_build.md`
- `specs/alternative_v1/04_sam_build.md`

## What was built

New files under `deck_sea_range_telemetry/slides/`:

| File | Slide | Spec | Core objects |
|---|---|---|---|
| `s05_appendix_methodology_roadmap.py` | Methodology Roadmap + scope gate | 01 | shape-built only (no chart, no table) |
| `s06_appendix_evidence_streams.py` | Evidence Streams + model controls | 02 | one native table + shapes |
| `s07_appendix_tam_build.py` | TAM Build method | 03 | one native table + shapes |
| `s08_appendix_sam_build.py` | SAM Build + audit controls | 04 | one native table + shapes |
| `_house.py` | (shared helper, not a slide) | — | `dark_table()` honest-height table |

Registry: `slides/__init__.py` now imports s05–s08 and appends them to
`SLIDE_RENDERS` **after** s01–s04 → deck is now **8 slides** (existing 4, then the
4 new ones). The stale package-root duplicates of s01–s04 (in
`deck_sea_range_telemetry/` itself, not `slides/`) were left untouched — they are
not registered and not imported.

Build verified: `python build_deck.py` → `wrote …_vS.pptx (8 slides, 0 charts)`.

## Conventions followed (from deck_core, not the old slides)

- Chrome via `deck_core.primitives` (`breadcrumb`, `title_placeholder`, `prelim_chip`,
  `sources_line`); body via `text_box` / `paragraph` / `run` / `connector` / `table`.
- Spec breadcrumbs/titles used verbatim: `Appendix / <topic>`, title in
  `Topic | Finding.` form. Step markers `STEP n / 4 — …` as BLUE_1 chips top-right of
  the body band; output chip full-width BLUE_1; dark guardrail/caveat strips BLUE_5.
- Spec palette maps 1:1 onto the deck_core ramp tokens:
  `263746=BLUE_5, 3D5972=BLUE_4, 6E91B1=BLUE_3, E2E9EF=BLUE_1, B6C8D8=BLUE_2,
  F2F2F2=GRAY_1, D9D9D9=GRAY_2`. No off-palette colors introduced.
- Operator `×`, `÷`, `+`, `=` used only inside formula cards/chips (allowed as
  deliberate formula notation), per slide_guide.
- Spec copy kept faithfully, **including** its em-dash section headers
  (e.g. "TAM CHAPTER — DEFINE AND SIZE THE ANNUAL MARKET"). Note this is a knowing
  deviation from the slide_guide "no em dashes" prose rule — the spec copy is the
  more specific instruction for this content and uses `—` as a label separator.

## Key technical decision: honest-height tables (`_house.dark_table`)

Memory gotcha "house_table row-height gotcha": `house_table` renders cells at 115%
line spacing, so the real table height runs ~15% taller than
`text_metrics.estimate_row_heights` predicts. These pages put a table directly above
a caveat/diligence strip, so an under-estimated frame `cy` would let the table grow
into the strip.

Fix: `_house.py::dark_table()` rebuilds the house dark-header posture on the
low-level `table()`/`trow()`/`tcell_rich()` engine with every cell pinned to
**100% line spacing**, so `sum(row_h)` from `estimate_row_heights` matches the
render exactly. It keeps the contract: BLUE_5 white-caps header, bold first column,
cascading horizontal rules (1.5pt under header, 1pt under body rows, none last),
per-cell fills/bold/color overrides. Used by s06 (evidence ledger), s07 (U.S. TAM
bridge), s08 (SAM bridge).

## QA loop (soffice → pdftoppm)

Rendered to PNG at 200 DPI and inspected each new slide; cropped tight regions for
detail. Fixes applied from the renders:

1. **s05** — right chapter label ("…FOR ASV ROLES") wrapped to 2 lines and "ROLES"
   spilled onto the node row. Cause: soffice Arial is ~16% wider than the 0.50
   char-ratio estimate. Fix: chapter labels 10pt → **9pt**. Now one line each;
   6-node roadmap + dashed "TAM ends here; SAM starts here" seam read cleanly.
2. **s07** — Europe stack `+ / + / =` operator chips were centered and **overlapped
   the card sublines**. Fix: reserved a left **gutter** (`_EUR_GUTTER=470_000`); cards
   shifted right, operators now sit in the empty gutter as a vertical arithmetic
   column. No overlap; full sublines visible.
3. **s08** (densest — overloaded by spec) — two overflow bugs:
   - Role-treatment chips spilled a 3rd line below the box. Fix: **inline** bold
     label + body in one paragraph (2 lines), font 7.8pt, `_ROLE_H` 455k.
   - The 6th audit card ("Output integrity") was hidden behind the diligence band
     because cards rendered taller than estimated. Fix: audit cards → **7.8pt**,
     `_vcard_height()` now estimates line count at an inflated `size_pt=8.8` (to track
     soffice's wider glyphs) and pins height to the 7.8pt render pitch; gap 16k.
     Stream-card sublines trimmed to one rendered line; vertical budget rebalanced.

After fixes, all four slides render without overflow or collisions. (General lesson
re-confirmed: soffice Arial ≈ 0.58 avg char/width-ratio vs the metrics module's
0.50 — treat `estimate_row_heights`/`wrapped_line_count` as optimistic for tight
shape text and add margin or inflate `size_pt` when budgeting.)

## Status

- [x] s05–s08 written from alternative_v1 specs
- [x] `_house.dark_table` honest-height helper
- [x] registered after s01–s04; build green (8 slides)
- [x] rendered + visually QA'd; overflow/collision fixes applied and re-verified
- [ ] not done: slide_probe geometry reports for s05–s08; final copyedit pass; any
  decision on whether to remove the stale package-root s01–s04 duplicates.

## Files touched

- A `deck_sea_range_telemetry/slides/s05_appendix_methodology_roadmap.py`
- A `deck_sea_range_telemetry/slides/s06_appendix_evidence_streams.py`
- A `deck_sea_range_telemetry/slides/s07_appendix_tam_build.py`
- A `deck_sea_range_telemetry/slides/s08_appendix_sam_build.py`
- A `deck_sea_range_telemetry/slides/_house.py`
- M `deck_sea_range_telemetry/slides/__init__.py` (registry)

Output: `projects/sea_range_telemetry/20260607_Sea Range Telemetry_vS.pptx`
