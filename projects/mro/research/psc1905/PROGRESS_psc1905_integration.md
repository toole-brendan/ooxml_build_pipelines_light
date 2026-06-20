# PSC 1905 Integration — Progress Report (2026-04-22)

_Execution record for the first integration pass of PSC 1905 embedded MRO ($1,904M Central) into the workbook. Companion to [IMPACT_psc1905_on_workbook_tam.md](IMPACT_psc1905_on_workbook_tam.md), which remains the full plan. This file captures what shipped this session, what's newly available to downstream work, and what's explicitly still open._

## TL;DR

- Workbook advanced from `v4.5.xlsx` → **`v4.7.xlsx`**.
- **Phases 1–5** of the IMPACT plan are complete: rollup-dict fix, classifier upgrade, per-parent rollup, new workbook sheet, Reconciliation named ranges.
- **11 named ranges** now live on the Reconciliation sheet (up from 3 PSC 1905-specific ones pre-session), including a new `RECONCILED_MRO_TAM = $8,971M` formula cell.
- New **`PSC 1905 Classified`** workbook sheet (201 rows × 17 cols) exposes the classifier output as an openpyxl Table (`PSC1905Classified`) for SUMIFS attribution.
- Per-parent rollup locked: **GD $965M, HII $872M, BAE $48M, Other $20M** (Central basis). HII Fleet Support Group's $169M now consolidates into HII via the fixed rollup.
- **Output sheet chart blocks not yet updated** — that is the remaining work and matches IMPACT sections A–K (minus D, H, L which are now unblocked by this session).

## What shipped this session

### Phase 1 — Corporate-parent rollup-dict fix
**File:** `build_script_slim/sheets/services.py` (line ~761)

Added one entry to `CORPORATE_PARENT_ROLLUP`:

```python
'HII MISSION TECHNOLOGIES CORP': 'Huntington Ingalls Industries',
```

Benefit is workbook-wide: Awards / Services / Depot Ship Repair / Output all call `consolidate_parent()` against `ultimate_parent_name`, so any HII MT records now roll up correctly everywhere, not just for PSC 1905.

The ANSWER doc's "HII Fleet Support Group" concern was resolved differently: its `ultimate_parent_name` is already `HUNTINGTON INGALLS INDUSTRIES  INC.` (which was already in the dict), so the $169M flowed into HII correctly once the classifier was pointed at `ultimate_parent_name` instead of `recipient_name` in Phase 2.

### Phase 2 — Classifier emits per-PIID corporate parent + per-parent rollup
**File:** `build_script_slim/psc_1905_classifier.py`

1. Imported `consolidate_parent` from `sheets.services`.
2. Added `ultimate_parent_name` + `corporate_parent` columns to every row of `psc_1905_classified.csv`.
3. Added `parent_rollup_central_m` block to `psc_1905_summary.json`, keyed by consolidated parent.

### Phase 3 — Reran classifier
```bash
python3 -m build_script_slim.psc_1905_classifier
```

Regenerated artifacts:
- `build_script_slim/output/psc_1905_classified.csv` (now 17 columns, was 15)
- `build_script_slim/output/psc_1905_summary.json` (now includes `parent_rollup_central_m`)

Verified Central total of **$1,904M** unchanged post-rerun (matches ANSWER §4.2).

### Phase 4 — New `PSC 1905 Classified` workbook sheet
**Files:** `build_script_slim/sheets/psc_1905.py` (new), `build_script_slim/build_from_data.py`

- New sheet module follows the `j998_j999_data.py` pattern (load CSV → stamp as openpyxl Table).
- Table name: `PSC1905Classified`.
- Columns: PIID, Service, Recipient, Ultimate Parent, Corporate Parent, Vessel Supergroup, Vessel Class, Hull Program, FY2025 Obligation, Total Obligation, Start/End Date, Bucket, Evidence, TAS Federal Accounts, Description, Parent IDV Description.
- Added as the last visible sheet in the tab order; slate tab color (matching Awards / J998 J999 Data).

Makes PIID-level attribution auditable and SUMIFS-compatible across arbitrary dimensions (parent × vessel × bucket × hull program).

### Phase 5 — 8 new Reconciliation named ranges
**File:** `build_script_slim/sheets/reconciliation.py`

Extended the Deck Evidence Anchors block. Anchor count went from 7 → 15.

**New named ranges (all live on Reconciliation sheet, `v4.7.xlsx`):**

| Name | Cell | Value | Consumer |
|---|---|---:|---|
| `PSC1905_MRO_SURFCOMBS` | C8 | 119 | S9 TAM Composition Mekko Depot row, Surface Combatants column |
| `PSC1905_MRO_UNCL` | C9 | 193 | S9 Mekko Depot row, Other column |
| `PSC1905_MRO_TIER0` | C10 | 235 | S20 Scope Reconciliation footnote / S23 appropriation detail |
| `PSC1905_MRO_GD` | C11 | 965 | S17 Prime Landscape TAM re-ranking |
| `PSC1905_MRO_HII` | C12 | 872 | S17 re-ranking |
| `PSC1905_MRO_BAE` | C13 | 48 | S17 re-ranking |
| `PSC1905_MRO_OTHER_PRIMES` | C14 | 20 | S17 rollup residual |
| `RECONCILED_MRO_TAM` | C15 | formula: `=NAVY_TAM_SVC+CG_TAM_SVC+PSC1905_MRO_EMBEDDED` | Deck-wide $8,971M headline |

**Pre-existing (unchanged):**

| Name | Value |
|---|---:|
| `PSC1905_MRO_EMBEDDED` | 1,904 |
| `PSC1905_MRO_SUBS` | 1,255 |
| `PSC1905_MRO_CARRIERS` | 337 |

## Verification

**Supergroup reconciliation** (should sum to Central total):
$$1{,}255 + 337 + 119 + 193 = 1{,}904 \;\;\checkmark$$

**Per-parent reconciliation** (Central basis, ±1 rounding):
$$965 + 872 + 48 + 20 = 1{,}905 \;\;\checkmark$$

**Reconciled MRO TAM** (formula resolves at Excel open):
$$7{,}067 + 1{,}904 = 8{,}971 \;\;\checkmark$$

## Files changed this session

| File | Change |
|---|---|
| `build_script_slim/sheets/services.py` | +1 line (`CORPORATE_PARENT_ROLLUP` addition) |
| `build_script_slim/psc_1905_classifier.py` | +import, +2 columns per row, +per-parent rollup block |
| `build_script_slim/sheets/psc_1905.py` | New file (123 lines) — data-sheet loader |
| `build_script_slim/build_from_data.py` | +import, +`create_psc_1905(wb)` call, +sheet-order entry, +tab color |
| `build_script_slim/sheets/reconciliation.py` | +8 deck evidence anchors, +per-parent rollup lookup, +formula cell |

## Regenerated artifacts

| Artifact | Source |
|---|---|
| `build_script_slim/output/psc_1905_classified.csv` | Phase 3 classifier rerun (17 columns) |
| `build_script_slim/output/psc_1905_summary.json` | Phase 3 classifier rerun (incl. `parent_rollup_central_m`) |
| `build_script_slim/output/08APR2028_MRO_Spend_v4.7.xlsx` | Phase 4+5 workbook rebuild |

## What this unblocks

Against IMPACT_psc1905_on_workbook_tam.md's "Changes by workbook block" table:

| IMPACT section | Status |
|---|---|
| **D. Slide 6 / Target S9 — TAM Composition Marimekko** | Named ranges ready (`PSC1905_MRO_SUBS/_CARRIERS/_SURFCOMBS/_UNCL`). Mekko formula change itself still open. |
| **H. Slide 15 / Target S17 — Prime Landscape — TAM** | Per-parent named ranges ready (`PSC1905_MRO_GD/_HII/_BAE/_OTHER_PRIMES`). Re-ranking still open. |
| **L. Reconciliation sheet — add named ranges** | **Complete.** All 8 proposed names plus `RECONCILED_MRO_TAM` shipped. |
| Optional upstream change: add `PSC 1905 Classified` sheet | **Complete.** Ships as `PSC1905Classified` table. |
| Decision checklist item 8 (named ranges vs. sheet) | **Resolved** — both paths implemented. |

## Still open (not addressed this session)

IMPACT sections A, B, C, E, I, J, K, M — all Output-sheet / Services-sheet block-level restructures:

- **A.** Output sheet title ($7,067M → $8,971M)
- **B.** Slide 4 / S5 TAM Sizing Approach funnel (add reconciliation step)
- **C.** Slide 7 / S8 MRO Work Segments (roll $1,904M into Depot row; recalc shares)
- **E.** Slide 11 / S13 Depot Spend Structure headline reference row
- **I.** Slide 16 / S18 Prime Landscape Depot reference row
- **J.** Slide 20 / S22 Scope Reconciliation waterfall restructure (5 → 7 columns with explicit addback)
- **K.** Slide 10 / S23 Appropriation Sourcing annotation
- **M.** Services sheet secondary updates (add `+ Embedded PSC 1905 MRO` row to MRO TAM block)

IMPACT decision checklist items 1–7 also remain open. The easiest path forward is to pick a decision-set (recommended defaults are already flagged in IMPACT) and then execute sections A/B/C/E/J in sequence — those are the highest-visibility edits.

Sections F (Marauder-Like Fleet MRO) and G (SAM Sizing) remain no-change under the plan — the comp set has zero PSC 1905 exposure.

## Known-issue carry-forward

### Metro Machine Corp attribution
Metro Machine's ~$59M of PSC 1905 MRO (USS Eisenhower FY25 PIA, USS Bush CMAV, CVN-75 LLTM, etc.) attributes to **General Dynamics** in the new `PSC1905Classified` sheet because FPDS reports `ultimate_parent_name = GENERAL DYNAMICS CORPORATION`. The existing `CORPORATE_PARENT_ROLLUP` dict contains `'METRO MACHINE CORP': 'Huntington Ingalls Industries'`, but that entry is dead code — every call site uses `ultimate_parent_name`, not `recipient_name`, so the dict lookup never sees `METRO MACHINE CORP`.

Impact: ~$59M of embedded MRO that should arguably belong to HII counts as GD. Same bug affects Awards / Services / Depot sheets identically.

Proper fix requires either:
- A compound `consolidate_parent` that checks both `recipient_name` and `ultimate_parent_name`, or
- Marking specific recipients as parent-overrides (e.g., `RECIPIENT_PARENT_OVERRIDE = {'METRO MACHINE CORP': 'Huntington Ingalls Industries'}`) and threading that through all call sites.

Deferred to a future session. If executed, both the services MRO rankings and the PSC 1905 per-parent rollup would shift by ~$59M (GD ↓, HII ↑).

### Upper vs. Central bound
All named ranges use the Central basis ($1,904M = strong + TAS-confirmed + probable MRO buckets). Upper bound ($2,057M, adds MRO POP-only) and Conservative bound ($1,553M, strong only) are not wired as separate named ranges. If the deck ever shows a range instead of a single number, `PSC1905_MRO_EMBEDDED_UPPER` and `_CONSERVATIVE` would need adding.

## How to reproduce from a clean checkout

```bash
cd /Users/brendantoole/projects2/branmut

# Re-run classifier (regenerates CSV + summary JSON)
python3 -m build_script_slim.psc_1905_classifier

# Rebuild workbook (produces next v4.N.xlsx under build_script_slim/output/)
python3 -m build_script_slim.build_from_data
```

Classifier expects `data_pull/output/fpds/navy_awards_master.json` and `cg_awards_master.json`; both are symlinks into the `domnann/` working copy. No external API calls are made unless `build_script_slim/output/psc_1905_funding_agg.json` is missing (Tier 0 TAS evidence becomes a no-op if so — Central bound drops by $235M if that file doesn't exist).

## Related documents

- [ANSWER_psc_1905_embedded_mro.md](ANSWER_psc_1905_embedded_mro.md) — $1,904M classifier-locked, methodology detail
- [IMPACT_psc1905_on_workbook_tam.md](IMPACT_psc1905_on_workbook_tam.md) — full plan (sections D / H / L now closed by this session)
- [AUDIT_workbook_vs_target_deck.md](AUDIT_workbook_vs_target_deck.md) — workbook chart-block coverage audit (findings unchanged by this session; references `v4.5` workbook but data findings still hold for `v4.7`)
- [PLAN_deck_revisions.md](PLAN_deck_revisions.md) — deck-copy edits Step 3+ (still open)
