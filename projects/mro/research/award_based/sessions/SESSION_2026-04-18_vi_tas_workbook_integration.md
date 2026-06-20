# Session 2026-04-18 (vi): TAS Attribution workbook integration - v2.77 -> v2.78

## Context

Session (v) produced the TAS / appropriation-color pull and rollup
(`data_pull/output/usaspending/approp_rollup_imputed.json`). Session
(vi) wires that artifact into the workbook per Phases 2 + 3 of
`docs/planning/PLAN_BROADER_BUDGET_ANCHORS.md`:

- **Phase 2**: new TAS Attribution section on `Budget Anchors` with
  defined names per appropriation bucket.
- **Phase 3**: Services sheet `_write_mro_budget_reconciliation`
  rewritten to replace the "Implied gap" framing with a full
  per-appropriation breakdown that ties to the MRO-PSC universe by
  construction.

Ended at **v2.78** with the integration complete; no pull or
classifier re-run this session.

---

## Work completed, in order

### 1. Budget Anchors - new TAS Attribution section (Phase 2)

`sheets/budget_anchors.py` additions:

- `_load_tas_rollup()` (memoized) - reads
  `data_pull/output/usaspending/approp_rollup_imputed.json`, returns
  `{federal_account: fy25_dollars}`. Warns if the file is missing
  and returns empty dict so the build never hard-fails.
- `_resolve_tas_values(row, tas_rollup)` helper - for a `kind='tas'`
  row, sums FY25 $ across `row['tas_accounts']` and converts to $K
  (same units as the rest of the sheet).
- `SECTIONS[0]` is a new section "FY2025 MRO-PSC Appropriation
  Attribution - measured via Treasury TAS (bottom-up)" ahead of the
  existing OMN BA-1 / SCN / USCG / NWCF sections. 10 per-appropriation
  rows + 1 SUM formula rollup row:

  | Row | Named cell | Accounts aggregated |
  |---|---|---|
  | TAS OMN       | `MRO_TAS_OMN_FY25`          | 017-1804 |
  | TAS OPN       | `MRO_TAS_OPN_FY25`          | 017-1810 |
  | TAS RDTE-DW   | `MRO_TAS_RDTE_DW_FY25`      | 097-0400 |
  | TAS DW other  | `MRO_TAS_DW_OTHER_FY25`     | 097-0100/0300/0130/4950/0500/4930/0460/8164 |
  | TAS Navy other| `MRO_TAS_NAVY_OTHER_FY25`   | 017-1319/1106/1506/1507/1109/1806/1612 |
  | TAS SCN       | `MRO_TAS_SCN_FY25`          | 017-1611 |
  | TAS Air Force | `MRO_TAS_AIR_FORCE_FY25`    | 057-3400/3840 |
  | TAS USCG      | `MRO_TAS_USCG_FY25`         | 070-0610/0613/8149 |
  | TAS Army      | `MRO_TAS_ARMY_FY25`         | 021-2020/2040/2035/2065 |
  | TAS Other     | `MRO_TAS_OTHER_AGENCY_FY25` | 096-4902 |
  | TAS Total     | `MRO_TAS_TOTAL_FY25`        | SUM formula over 10 rows |

- Dispatch in `create_budget_anchors` extended to handle `kind='tas'`
  rows alongside existing `data` / `memo` / `formula` types.

Resulting Budget Anchors sheet: 33 line items / 5 sections / **30
named cells** (up from 22 / 4 / 19).

### 2. Services sheet reconciliation rewrite (Phase 3)

`sheets/services.py::_write_mro_budget_reconciliation` replaced
end-to-end. New layout:

- **FPDS Services TAM block** (unchanged logic): Navy row + CG row +
  subtotal row, all referencing `NAVY_TAM_SVC` / `CG_TAM_SVC` as
  before.
- **FY25 MRO-PSC $ by Appropriation (TAS-measured)** subsection - 10
  rows referencing `MRO_TAS_*` named cells, each with a `% of TAS
  Total` formula in column D = `=MRO_TAS_<NAME>_FY25/MRO_TAS_TOTAL_FY25`
  (displayed as 0.0%). Subtotal row references `MRO_TAS_TOTAL_FY25`
  and notes that it's the pre-exclusion MRO-PSC universe, ~$340M
  larger than the Services TAM due to shore-base + FMS exclusions
  applied in Services but not in the TAS pull.
- **Top-down budget-book context (memo)** - 3 rows (OMN CE 928 BA-1
  total, OMN BA-1 grand total, USCG ISVS). Explicitly flagged as
  memo-only, not summable with the TAS block.
- The prior "Implied gap" row (FPDS $7.1B - OMN CE 928 $2.4B = $4.7B)
  is **gone**. Per-appropriation breakdown closes the gap by
  construction since all appropriations funding MRO PSCs are now
  captured, not just OMN CE 928.

`_write_mro_budget_anchors_refs` gained a new first subsection listing
the 11 TAS named cells (with one-line notes each). Existing OMN / USCG
reference subsections unchanged.

`_write_mro_budget_narrative_pointer` rewrote the gray-italic pointer
line to reflect the TAS-measured approach rather than the old gap
narrative.

### 3. Smoke test + build

Smoke-tested via `/tmp/smoke_services_tas.py`: Awards + Budget Anchors
+ Services in a scratch workbook; all 11 TAS named cells resolve
cleanly, reconciliation block row layout matches intent, formula
lengths trivial (35-char max, well under the 8,192 limit).

Ran `python3 -m domnann.build_from_data`. v2.77 auto-archived to
`output/archive/`, v2.78 saved. Sheet order unchanged. Row counts and
totals unchanged on every sheet except Services (added ~35 rows for
the new reconciliation block + TAS subsection in the anchor refs
table) and Budget Anchors (added 11 rows at the top for the TAS
section).

---

## Files modified

- `sheets/budget_anchors.py` - new TAS section in `SECTIONS`,
  `_load_tas_rollup()` + `_resolve_tas_values()` helpers, dispatch
  extension, docstring update.
- `sheets/services.py` - `_write_mro_budget_reconciliation` full
  rewrite, TAS subsection added to `_write_mro_budget_anchors_refs`,
  narrative pointer updated.

## Files unchanged (intentionally)

- `data_pull/*` - the pipeline ran in session (v); this session
  consumes its output JSON without re-running it.
- `build_from_data.py` - no new sheets; existing sheet list unchanged.
- Methodology + planning docs - updated in session (v); no further
  narrative changes needed for the workbook integration itself.

## Memories added

None.

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.77 -> v2.78 | Budget Anchors TAS Attribution section (11 rows, 11 named cells) + Services reconciliation rewrite (FPDS TAM + TAS breakdown + memo context, "Implied gap" removed) | Budget Anchors: 22 -> 33 rows, 19 -> 30 named cells. Services: ~35 new rows in the reconciliation block; TAM/crosstabs/contractor views unchanged. |

v2.78 is current.

---

## Open flags

- **v2.78 not opened in Excel yet.** Smoke-test via openpyxl confirms
  formula strings are syntactically valid and defined names all point
  at the right Budget Anchors cells, but only Excel's evaluation
  confirms the cells actually compute to the intended values. Expect:
  Budget Anchors TAS Total E16 = ~$7,406K ($K units) and Services
  column D percentages on the TAS block should sum to 100.0%.

- **TAS pull is 98.4% $ coverage, not 100%.** The 52% of MRO $ that is
  PSC-bucket-imputed rather than directly classified propagates
  through the workbook values. Re-running the pull to completion (~75
  more min at USAspending's current rate-limited ~1 req/s) would
  replace imputation with direct classification but the rollup
  numbers would shift by <1%.

- **Plan Phase 5 deck update not done.** `deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md`
  still describes the old "FPDS > OMN CE 928" callout. When the slide
  is actually redrawn, the mockup file should be rewritten to match
  the data-driven "$7.4B spans 10 appropriations; OMN 38% + OPN 36% +
  RDT&E-DW 11% = 85% of the total" narrative from the methodology
  doc.

- **Plan Phase 6 extension to newbuild PSCs not started.** Running the
  same pull across ~15k newbuild / other PSC PIIDs (~3 hours at
  current pace) would enable Product Procurement-side top-down vs
  bottom-up reconciliation for SCN-backed HII NNS submarine + carrier
  programs. Not started; worthwhile when Product Procurement becomes
  deck-focus.

- **Pre-existing Services formula-length guardrail** (carried over
  from sessions i-iv) still not verified in real Excel open. Not
  related to this session's changes.
