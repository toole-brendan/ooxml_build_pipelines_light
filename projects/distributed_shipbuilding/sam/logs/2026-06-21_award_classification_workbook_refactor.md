# 2026-06-21 — Award-Classification workbook refactor (correctness + structural simplification)

Session goal: implement a reviewer's verdict on the `award_classification_refactor` workbook
(`projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/`).
The plan: fix two real correctness bugs + a data-integrity drift, then simplify ~70k formula cells
(some classification formulas >800 chars), add a market-estimate bridge, and reorder the tabs.
Delivered in three phases, each built + tie-out-verified. **The headline totals are unchanged:
$13.505B nominal / $15.508B FY2026$.** Build is clean (18 sheets, 0 XML errors, 0 error-literal cells).

Approved scope (via AskUserQuestion): required correctness+integrity fixes; structural
simplification; tab regrouping; Market Bridge with bands **derived now**. Out of scope: a
standalone Model Checks sheet (integrity instead lives as a build-time Python assertion).

Every factual premise in the plan was re-verified against the live tree before editing (the CSVs
were git-modified, so this mattered) — all numbers matched exactly, incl. the 36-key footprint.

---

## Phase 1 — correctness + integrity (verified)

- **Domain Concentration formulas** (`sheets/domain_concentration.py`). Both reviewer claims were
  real bugs (an Explore pass had wrongly dismissed them):
  - *Top-1 firm* was `INDEX(NM, MATCH(MAXIFS(M,D,code), M, 0))` — `MAXIFS` domain-scoped but the
    outer `MATCH` searched the **full** amount range, so a tied $ in another domain mis-named the
    firm. Now a domain-constrained match on a new **Top-1 $M** helper column (col G):
    `INDEX(NM, MATCH(1, INDEX((D="code")*(M=G),0), 0))`.
  - *HHI* squared **all** within-domain amounts incl. negatives over a net denominator. Now
    positive-only in both: `SUMPRODUCT(--(D=code),--(M>0),M^2)/SUMIFS(M,D,code,M,">0")^2` ⇒ HHI∈(0,1].
- **Deflator magic number** (`sheets/deflators.py`): `=102.10/$C{r}` → `=$C$23/$C{r}` with the
  FY2026 row **derived** from `_FY_ROW_ORDER` + two layout assertions (re-basing is a one-row edit).
- **Dimension drift + build-stopping guard.** Root cause confirmed: `build_uei_dimensions.py` built
  its (UEI×program) spine from the corpus independently of the program-vendor build; the
  `N00024-20-C-2120` prime added to scope 2026-06-21 refreshed the tx/vendor pulls but not the
  dimension pulls, leaving **36 Virginia UEIs** (93 tx, $110.38M FY2026$) resolving to dashes→D0/P0.
  New `sheets/_integrity.py::assert_universes_aligned()` (wired into `lib.build()`) fails the build
  unless program-vendor = transaction = supplier dimension on the (Program×UEI) universe. Confirmed
  it **fires** on the stale CSVs (naming the 36) then **passes** after regeneration. The corpus is
  runnable here and yields the correct universe (470/669/582), so no external data was needed.
- **Methodology prose** (`sheets/guide_methodology.py`): six stale `~$12.49B`/`$13.1B` literals
  (reconciling to neither current unit) rewritten to point at the live Executive Summary §2 total.

36-key impact (characterized): all 36 now have dimension rows (vendor name + parent resolve, no
more "-"); **11 ($7.71M)** newly classify to a real Capability Domain, **25 ($102.67M)** legitimately
stay D0 (long-tail Virginia vendors with no NAICS). The domain-mix shift is small; the integrity win
is that the universe is now provably aligned and guarded.

---

## Phase 2 — structural simplification (verified)

- **2.4 Layout accessor** (`_flat.py`): `make_flat_sheet` now returns a callable `Cols` object
  exposing `.letter/.cell/.range/.row_span`; added `_cuts.load_headers()` + `flat_header_letters()`
  so a module resolves its OWN column letters by name at build time. No load-bearing column letters
  remain in Python (`_NAICS_COL="C"`, `$AZ`/`$BA`, `=SUM(M:AA)` all gone).
- **2.3 SWBS match-row** (`ddg_subaward_transactions.py`): one `SWBS Match Row` helper does the
  crosswalk MATCH once; the three SWBS outputs `INDEX` it (3 MATCH→1 over ~6.4k rows).
- **2.2 Transaction-grain economics** (`_fiscal.py` + the 3 tx sheets): each tx sheet gains formula
  columns `Federal FY`, `Deflator Factor`, `Subaward $ FY2026$`. Program-vendor per-FY cells collapse
  to one `SUMIFS` over the constant-$ column keyed on UEI + Federal FY; lifetime is one `SUMIFS`.
  **Provably value-preserving** (the deflator is constant within each FY bin, so it factors out;
  verified 0 transactions post-date FY2026, so lifetime == sum-of-bins). Deflators now feed the tx
  layer for all four downstream sheets (incl. the SWBS rollup, also migrated).
- **2.5 Factory + `_fiscal`** (`_program_vendors.py`): the 3 near-identical vendor modules are now
  ~20-line configs over `make_program_vendor_sheet()`; the FY axis is defined once in `_fiscal.py`
  (consumed by the factory, SWBS rollup, and Deflators).
- **2.1 Supplier Master** (the big one): `subawardee_uei_index` + `subawardee_parents` merged into one
  `supplier_master.py` (built by `scripts/build_supplier_master.py`), keyed by composite `Program|UEI`.
  It resolves the archetype **once per Program×UEI** via two short match-row helpers
  (override → NAICS-map → D0/P0); a `Key` column was added to the Overrides sheet for a single MATCH.
  Each program-vendor row now does **one MATCH + INDEX columns** instead of 5 two-criteria array
  searches + 4 ~800-char `override_then_map` formulas; each vendor sheet now depends on just its tx
  leaf + Supplier Master. Resolution distribution across 1,721 rows: 291 override / 955 NAICS-map /
  475 unresolved (healthy, non-degenerate; logic identical to the prior `override_then_map`).

---

## Phase 3 — Market Bridge + regrouping (verified)

- **Market Bridge** (`sheets/market_bridge.py`, `summary` group): observed reported subawards (live =
  Σ of the three program-vendor $M) + **editable** HII co-build Low/Base/High bands → estimated
  outsourced market. Bands derived from the HII Co-Build disclosed ledger — Virginia
  10,200/15,000/22,000 $M anchored on the disclosed $10.2B Block V figure; Columbia 3,400/5,000/8,000
  $M from the lineage-summed mods — each basis-labeled, CRS% never mixed with disclosed $, co-build
  mass **not** allocated across domains, kept separate from the classified ("observed") tables.
- **Reader-first tab order** onto the existing shared 9-group taxonomy (no `workbook_core` change):
  **summary** (Exec Summary, Domain Concentration, Market Bridge) → **guide** (Taxonomy, Methodology,
  HII Co-Build) → **inputs** (NAICS Map, Overrides) → **model** (3 vendor sheets, SWBS rollup) →
  **data** (Supplier Master, SWBS Crosswalk, Deflators, 3 transactions).

---

## Cleanup

Pruned the now-dead `_flat.py` helpers superseded by the Supplier Master / match-row pattern:
`composite_lookup`, `_override_inner`, `override_then_map`, `override_then_map_basis`, and the
standalone `swbs_value` / `swbs_basis` / `swbs_subsystem` (confirmed unused, then re-built clean).

---

## Files

- **New:** `sheets/_fiscal.py`, `sheets/_integrity.py`, `sheets/_program_vendors.py`,
  `sheets/supplier_master.py`, `sheets/market_bridge.py`, `scripts/build_supplier_master.py`,
  `extracted/supplier_master.csv`.
- **Deleted:** `sheets/subawardee_uei_index.py`, `sheets/subawardee_parents.py`,
  `scripts/build_uei_dimensions.py`, `extracted/subawardee_uei_index.csv`,
  `extracted/subawardee_parents.csv`.
- **Modified:** `_flat.py`, `_cuts.py`, `_tabs.py`, `__init__.py`, `lib.py`, `domain_concentration.py`,
  `deflators.py`, `guide_methodology.py`, `naics6_archetype_map.py`, `vendor_archetype_overrides.py`,
  the 3 `*_program_vendors.py`, the 3 `*_subaward_transactions.py`, `ddg_swbs_rollup.py`,
  `executive_summary.py`.

---

## Carry-forward

- **Nothing committed.** The change set is staged in the working tree only; `award_classification_refactor.xlsx`
  rebuilt. Commit when ready.
- **Build/verify:** `python build_workbook.py` (the §1.3 universe guard runs first) → `python validate_workbook.py`.
  Regenerate the supplier dimension with `python scripts/build_supplier_master.py` (uses the live corpus).
- **Market Bridge bands are editable estimates**, not transactional data — order-of-magnitude, mixed
  nominal/FY2026$ vintages, basis-labeled on the sheet. Refine the Low/Base/High input cells (blue) as
  better disclosures land; the estimate updates live. Consistent with the HII-gap conclusion
  (`DOMAIN_SHARE_CONCENTRATION_CAVEAT.md`): the co-build workshare is recoverable only via issuer
  disclosures / FOIA, never a federal transactional feed.
- **Not verified headless:** opening in Excel to watch cells evaluate. All formula structures were
  verified in the rendered xlsx; deflation + archetype logic are provably equivalent to the prior version.
