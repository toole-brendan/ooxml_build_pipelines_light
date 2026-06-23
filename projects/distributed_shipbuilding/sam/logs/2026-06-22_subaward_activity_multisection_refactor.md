# 2026-06-22 — Subaward Activity refactored into a 4-section recurrence sheet (+ Block/MYP)

Second session of the day on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The morning session stood up a flat **Subaward
Activity** table + a **Prime Awards** data sheet (see
`2026-06-22_subaward_activity_and_prime_awards.md`). This session **rewrote Subaward Activity
into a single multi-section sheet** that characterizes *who* the suppliers are — one-off /
single-component makers vs long-running, recurring vendors — driven by a design discussion the
user brought in. Workbook stays **22 sheets**; native tables **15 → 16** (the new sheet now
carries **two** native tables). Build clean (**22 sheets, 0 XML errors, 0 error-literal cells**);
the **$13,883.99M** FY2026$ headline is untouched and reconciles to the cent.

Everything is **uncommitted** (working tree only).

---

## The load-bearing architecture finding — multiple native tables on ONE worksheet IS supported

The user's mockup was a single stacked sheet (§3 → §2 → §1 → §4), but every existing sheet uses
**≤ 1 native table** (`make_flat_sheet` builds exactly one; the multi-section sheets like
`parent_concentration` use `RowCursor` with **no** native table). Verified the core packager
supports many tables per sheet end-to-end and it's standard OOXML:

- `WorksheetSpec.tables` is a `list[ExcelTable]`; `build_table_part_xml` uses a **workbook-global**
  table id; `inject_table_parts` emits one `<tableParts>` with N `<tablePart>` children
  (`workbook_core/tables.py`).
- The packager loops `for t in spec.tables:` — global numbering, per-sheet rels accumulate,
  workbook-unique name check (`workbook_core/lib.py:526-543`).

So the stacked single sheet is buildable with **§1/§2 as native sortable tables** and **§3/§4 as
styled blocks**. Cost: the sheet can no longer use `make_flat_sheet` — it's a custom `RowCursor`
`render()` (the `parent_concentration` pattern) that hand-rolls per-cell styling and emits two
`ExcelTable` specs. Nobody imports `subaward_activity_cols` / `prime_awards_cols` (both leaf
sheets), so the accessor could be dropped freely.

---

## Decisions locked this session (supersede the morning log)

- **Layout = vendor-rollup-first** (user's pick): `§3 Type Summary` → `§2 Vendor Rollup` (lead) →
  `§1 Engagement Detail` → `§4 Vendor Mix by Block/MYP`, all on the one **Subaward Activity** tab.
- **Recurrence typology (this REPLACES the morning log's single/<1/1–3/3–5/5+ span tiers):**
  two independent axes —
  - **breadth** = distinct subaward NUMBERS: `1 →0 · 2-3 →1 · 4-9 →2 · 10+ →3`
  - **duration** = first→last span (yrs): `0 →0 · <2 →1 · 2-6 →2 · ≥6 →3`
  - **Vendor Type = the MORE INTENSE of the two axes** (so a 1-subaward / 7-yr vendor still reads
    long-running; a 12-subaward / 3-month vendor still reads core-breadth):
    `One-off / single-component · Repeat-buy, short window · Recurring · Core / long-running`.
- **Coverage = engagement span ÷ prime PoP** (Start → Current End, from Prime Awards) — turns
  span-in-isolation into "does this vendor track the whole build or a slice".
- **Block / MYP** added to **Prime Awards** (hand-derived; not in any pull) and looked up into
  §1 by PIID. Kept in a `BLOCK_MYP` dict in `pull_prime_awards.py` so a re-pull preserves it.
- **Distinct-count stays MATERIALIZED**, not the transcript's live first-occurrence-flag idea —
  a self-referential expanding `COUNTIFS` over three 6k–16k-row leaves is the "ugly and slow" the
  morning session already flagged. Everything *additive* stays live.

---

## What was built

### Prime Awards — `+ Block / MYP` (12 PIIDs → 9 distinct blocks)
`scripts/pull_prime_awards.py`: `BLOCK_MYP` dict + new column after Award Description + a guard
(every prime must carry a label). `sheets/prime_awards.py`: width slot inserted. CSV rewritten
in place (no network re-pull). Blocks hand-derived from descriptions + Virginia hull→block
boundaries (Block IV = SSN 792-801, V = 802-811, VI = 812+): DDG FY11 single-ship / FY13-17 /
FY18-22 / FY23-27 MYP; Virginia Block IV/V/VI (LLTM) + LYS (cross-block); Columbia (design/build).
**These labels are hand judgment — flag for user review.**

### Vendor-rollup spine (§2)
`scripts/build_subaward_activity.py` now emits a **second** CSV `subaward_vendor_rollup.csv`
(one row per UEI, **1,102 vendors**), materializing only the distinct-counts: Distinct PIIDs /
Distinct Programs / Distinct Subaward Numbers. Confirms **607 vendors on >1 PIID (55%)** and
**383 on >1 program (35%)** — matching the design-discussion figures.

### Subaward Activity — custom 4-section renderer
`sheets/subaward_activity.py` rewritten (`make_flat_sheet` → custom `render()`):
- **§3 Type Summary** (styled block, live `COUNTIF`/`SUMIF`/`AVERAGEIF` over §2).
- **§2 Vendor Rollup** (native table `SubawardVendorRollup`, B18:K1120, 1,102 rows): UEI · Vendor ·
  Distinct Subawards · Portfolio Span · Vendor Type · Net $M · Reports · Corrections · Distinct
  PIIDs · Distinct Programs.
- **§1 Engagement Detail** (native table `SubawardActivity`, B1124:O3609, 2,485 rows): the §2
  columns + Program · Prime PIID · Block/MYP (INDEX/MATCH on Prime Awards) · Coverage % PoP ·
  First/Last Action. `Reports` **demoted to a QA column** (corrections/refilings inflate it).
- **§4 Vendor Mix by Block/MYP** (styled block, live over §1; distinct-vendor count via the
  `SUMPRODUCT((block=B)/COUNTIFS(uei,uei,block,block))` idiom).
- §1 and §2 **share the first 8 grid columns** (B-I) so the two tables read consistently and the
  shared column widths fit both. Cross-section live refs resolved by a **pass-1 row-position
  pre-compute** + `assert c.at()==…` guards at every banner (caught two off-by-ones during build).

---

## The bug the verification caught (and the fix)

The gold-standard pass (below) flagged **442 mismatches, all in §2 Portfolio Span** (+ the Type
cascade). Cause: §2's first-date reused §1's `MAX(MINIFS…)` trick — valid only when the key
matches **one** program leaf (PIIDs are program-disjoint, so two leaves return 0 and `MAX` picks
the real one). A **UEI spans multiple programs (383 vendors)**, so `MAX` of the per-program
minimums returns the *latest* min, not the global earliest → span understated. Fixed `_f2_span`:
`first = MIN` of the per-leaf `MINIFS` with a non-matching leaf's 0 lifted to a sentinel
(`IF(MINIFS=0, 1E9, MINIFS)`); `last = MAX(MAXIFS…)` is unaffected (a 0 can't beat a real serial).
§1 was correct throughout (single program per PIID).

---

## Verification — LibreOffice headless recalc + per-cell Python diff (gold standard)

`soffice --headless -env:UserInstallation=… --convert-to xlsx` (our formula cells carry **no**
cached `<v>`, so LibreOffice must compute on load), then `openpyxl data_only=True` diffed every
live cell against an independent replica aggregated from the **recalc'd transaction leaves**
(verifying §1/§2 SUMIFS/COUNTIFS/MINIFS *keying*) + the materialized CSVs:

- **§1: 2,485 rows · §2: 1,102 rows · 0 mismatches** across distinct, span, type, net, reports,
  corrections, block, coverage, first/last (after the span fix).
- **§3 reconciles to the cent:** 1,102 vendors, **Σ Net $M = 13,883.9944723494** = the
  program-vendor FY2026$ headline.
- **§4 exact** for all 9 blocks (distinct vendors via SUMPRODUCT, engagements, distinct subs,
  net $); totals eng=2,485 · subs=14,919 · net=$13,883.994M.

### The payoff (§3, vendor-portfolio grain)

| Vendor Type | # Vendors | % | Net $M | % of $ | Avg Span |
|---|--:|--:|--:|--:|--:|
| One-off / single-component | 264 | 24.0% | 130.4 | 0.9% | 0.0 |
| Repeat-buy, short window | 194 | 17.6% | 227.8 | 1.6% | 0.6 |
| Recurring | 266 | 24.1% | 1,446.6 | 10.4% | 2.4 |
| **Core / long-running** | **378** | **34.3%** | **12,079.3** | **87.0%** | **6.1** |

**~34% of vendors (core/long-running) hold ~87% of subaward dollars** — sharper at the vendor-
portfolio grain than the morning log's engagement-grain cut (16% of relationships / 64% of $),
because the rollup accumulates a vendor's engagements across PIIDs.

---

## Build / verify

```
python3 scripts/pull_prime_awards.py          # (only to refresh primes; Block/MYP now persisted)
python3 scripts/build_subaward_activity.py    # 2485 §1 rows + 1102 §2 rows, from committed CSVs
python3 build_workbook.py                      # -> 22 sheets, 16 native tables
python3 validate_workbook.py                   # 0 xml errors, 0 error-literal cells
python3 tools/style_audit.py                   # 0 hard failures (see carry-forward re: 1 warning)
# gold standard: soffice headless recalc -> openpyxl per-cell diff vs replica (0 mismatches)
```

## Files

- **Modified scripts:** `scripts/pull_prime_awards.py` (+`BLOCK_MYP`, +column, +guard),
  `scripts/build_subaward_activity.py` (+vendor-rollup spine).
- **Rewritten sheet:** `sheets/subaward_activity.py` (flat → custom 4-section renderer, 2 tables).
- **Modified sheet:** `sheets/prime_awards.py` (+Block/MYP width).
- **Data:** `extracted/prime_awards.csv` (+Block/MYP), `extracted/subaward_vendor_rollup.csv`
  (new); regenerated `award_classification_refactor.xlsx`.

## Carry-forward

- **Nothing committed** — all changes are in the working tree only.
- **Style audit shows 1 warning** — `[Methodology] column C width 84 (>44)`, on a sheet **NOT
  touched this session** (hard failures = 0). It is stable across rebuilds and appeared after the
  span-fix rebuild; the note-part count also drifted 8→7. **Not a Subaward Activity regression**;
  was mid-investigation (pre-existing vs hash-nondeterministic) when the session was redirected —
  confirm it's pre-existing before committing.
- **Block/MYP labels are hand judgment** (esp. the Virginia SSN→block mapping) — review.
- **Coverage uses PoP Current End**, not Potential End (excludes unexercised option years).
- **Distinct-count remains materialized** in both spines; if a live version is ever wanted, it
  needs a first-occurrence flag column on each tx leaf (perf-watch).
- Reconciliation + recalc are reproducible via the soffice + openpyxl path above (no committed
  helper script — it was run ad hoc this session).
