# Session 2026-04-19 (iii): Deck Data Sheet -- Reflow to New 10-Slide Spec

## Context

Session (i) earlier today created the `Deck Data` workbook sheet
backing the 10-slide Saronic / Port Alpha MRO deck (workbook v2.85).
Session (ii) then rewrote `deck/DECK_PROPOSED.md` into a restructured
10-slide flow (new Slide 4 TAM Composition merged, Slide 6 Geographic
Context moved up, brand-new Slide 8 Prime Landscape - Depot). The
spec moved; `sheets/deck_data.py` was still emitting the old layout.

This session brings the Deck Data sheet into alignment with the new
spec so every think-cell source table matches the slide it feeds.

**Output**: workbook v2.88 (v2.87 archived). No deck-spec changes;
no data-pull changes.

---

## Changes to `sheets/deck_data.py`

### Slide 4 -- rewritten: TAM Composition (merged)

Old Slide 4 (Work Segments, 100% stacked column) + old Slide 6
(Vessel Mix Mekko) collapsed into a single block:

- **Primary Mekko**: rows = 5 work segments (stack series), columns =
  5 named vessel categories + Other + Row Total. Formula pattern
  lifted verbatim from the former `_write_slide6`.
- **Secondary "Work-Segment Summary"**: 4-column table (Segment /
  FY25 $M / % of TAM / Coverage). Coverage text migrated from the
  former `_write_slide4` coverage list into a module-level dict
  `SLIDE4_COVERAGE` keyed by segment name.
- Constants `SLIDE6_VESSEL_CATEGORIES` / `SLIDE6_SEGMENT_ORDER`
  renamed to `SLIDE4_*` for locality.

### Slide 5 -- trimmed

Kept the Headline ($M totals, 3 rows) and Primary Mekko (Tier x IDV
scope group). **Dropped** the Secondary "Tier-1 CONUS prime roster"
table -- that content now belongs on new Slide 8. Module constant
`TIER1_PRIMES` removed as dead code.

### Slide 6 -- relocated: Geographic Context

Old `_write_slide8` (RMC x Tier Mekko + RMC geography text + candidate
site proximity text) renamed to `_write_slide6` and repositioned in
natural reading order between Slide 5 and Slide 7. Body unchanged.
Module constant `SLIDE8_RMC_BUCKETS` renamed to `RMC_BUCKETS` since
the new Slide 8 also consumes it.

### Slide 7 -- title edit only

`_section_header` title changed from `'Prime Landscape'` to
`'Prime Landscape - Total MRO'`. No formula changes.

### Slide 8 -- NEW: Prime Landscape - Depot Ship Repair

Brand-new block, structurally parallel to Slide 7's Pareto, scoped to
J998/J999:

- **Headline denominator** (3 rows): Gross J998+J999 / Less FMS
  carve-out / In-Scope Depot TAM. In-Scope cell is the cumulative-%
  denominator for the Pareto.
- **Primary Pareto** (10 rows x 5 cols): Rank | Contractor |
  FY25 Depot $M | Cumulative $M | Cumulative % of Depot. Python-side
  rank uses a new `depot_parent_totals()` helper (see below). Each
  row's $M is a `SUM(SUMIFS(J998J999Data[FY2025 Obligation],
  J998J999Data[PSC], {"J998","J999"}, J998J999Data[Corporate Parent],
  "{parent}"))/1E6`. Top-10 subtotal row at the bottom.
- **Secondary Prime x RMC crosstab** (10 rows x 9 cols): rows = the
  same top-10 primes, columns = 7 RMC buckets + Total $M. Each cell
  filters J998J999Data by Corporate Parent + RMC (summing RMC
  sub-values within each bucket).

### TOC + orchestrator

- `_write_toc` slide list re-keyed to the 9 data-bearing slides
  (Slide 1 is a framing slide, no data table).
- `create_deck_data` now also loads `depot_rows` (via the existing
  `load_rows` in `sheets/j998_j999_data.py`) and passes them to the
  new `_write_slide8(ws, r, depot_rows)`.
- Added `'corporate_parent': 'Corporate Parent'` to the `_j998_m`
  `field_to_col` dict so Slide 8's SUMIFS pattern can filter
  J998J999Data by consolidated parent.

---

## New helper in `sheets/depot_ship_repair.py`

```python
def depot_parent_totals(rows, consolidated=True):
    """Sum fy2025_obligation per parent on J998/J999 rows. Mirrors
    services._parent_totals so deck_data.py can Python-rank depot
    primes the same way it ranks Services primes on Slide 7."""
```

Mirrors `services._parent_totals` with the FMS-inclusive default --
Slide 8's Pareto ranks by gross J998+J999 $, with the in-scope
denominator applied only to the cumulative % column.

---

## Build + verification

- Ran `python3 -m domnann.build_from_data`. v2.87 auto-archived;
  v2.88 saved.
- Deck Data sheet: 319 rows x 15 cols; 9 slide blocks present in
  reading order 2 -> 10. All section headers match the new spec
  titles.
- Spot-checked Slide 8 formulas:
  - BAE Pareto $M: `=SUM(SUMIFS(J998J999Data[FY2025 Obligation],
    J998J999Data[PSC], {"J998","J999"}, J998J999Data[Corporate
    Parent], "BAE Systems"))/1000000` -- well-formed.
  - BAE x SWRMC cell: triple SUMIFS with PSC + Corporate Parent +
    RMC filters -- well-formed.
  - Denominator at B173 = B171+B172 (gross + negative FMS =
    in-scope).
  - Cumulative % references the in-scope denominator cell.

Python-ranked top 10 depot primes came out:
1. BAE Systems
2. General Dynamics
3. Huntington Ingalls Industries
4. Vigor Marine LLC
5. Detyens Shipyards Inc.
6. East Coast Repair & Fabrication LLC
7. Epsilon Systems Solutions Inc.
8. Pacific Shipyards International LLC
9. Colonna's Ship Yard Incorporated
10. Amentum Services Inc.

Ranks 1-5 match the spec exactly. Ranks 6-10 differ from the spec's
placeholder FDNF-heavy list (Hanwha Ocean / Navantia / Sumitomo / 
NASSCO Mayport / East Coast Repair) because FDNF yards roll up under
non-US consolidated parents that rank below the CONUS Tier-2 primes
when scored by total J998+J999 $. The spec already flagged its
ranks 6-10 as "approximate placeholders"; the live figures supersede
them when slides are drawn.

---

## Files changed

- `sheets/deck_data.py` -- all slide-block reflow; new Slide 8 added;
  TOC + orchestrator re-keyed; `_j998_m` gained a `corporate_parent`
  field mapping; dead constants (`TIER1_PRIMES`, `SLIDE6_*`,
  `SLIDE8_RMC_BUCKETS`) removed or renamed.
- `sheets/depot_ship_repair.py` -- added `depot_parent_totals()`
  helper (mirrors `services._parent_totals`).

## Files NOT touched

- `deck/DECK_PROPOSED.md` -- spec is the source of truth this session
  was aligning TO, no content change needed.
- `deck/DECK.md` -- still the 4-slide delivered reference.
- `build_from_data.py` -- orchestrator is unchanged (the build order
  stayed the same; deck_data still runs last among data sheets).
- Awards / Services / J998 J999 Data / Budget Anchors / PSC Catalog
  builders -- unchanged.
- `data_pull/` -- no regeneration needed; Slide 8 reads the same
  J998J999Data table that Slide 5 and Slide 6 already read.

## Follow-ups

- When Slide 8 is actually drawn in think-cell, the workbook cells
  will supersede the spec's ranks 6-10 placeholder table. The spec
  already acknowledges this; no markdown edit needed.
- Spec shows GD and HII depot $ derived from Slide 7's segment
  top-3 shares (22% / 18% / 10%) applied to the $4,923M denominator.
  Live Python-ranked totals will reconcile against that once the
  slide is drawn; if they diverge materially, the Slide 5 footnote
  calling out "parent-company rollup vs NASSCO + CMSD sub-units"
  may need a numeric refresh.
- Spec's ranks 6-10 (FDNF) story could be recovered by adding a
  hand-curated FDNF roster block to Slide 8 (or widening the Pareto
  to top 15). Deferred; not part of the reflow ask.
