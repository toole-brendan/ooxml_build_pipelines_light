# 2026-06-20 — Master TAM workbook consolidation + tam/ folder restructure

Consolidated the three per-program TAM workbooks into ONE master **TAM-only**
workbook, then stripped the now-redundant workbook pipelines from `tam/`,
preserving the research corpora. Lives in `tam/logs/` because it spans the whole
`tam/` area (new master pipeline + folder restructure).

## 1. New master pipeline — `tam/master/workbook_master_tam/`
One workbook, **42 tabs**, combining the former `submarines` (split into
Virginia + Columbia), `ddg`, and `outsourcing_ceiling` workbooks. Grouped by
FUNCTION with program as the inner axis (the engine enforces group contiguity);
program-specific tabs are prefixed `Sub `/`DDG `/`Ceiling `.

- Each former workbook relocated into `sheets/{submarines,ddg,ceiling}/` with a
  thin `_bind.py` pointing at a **namespaced snapshot** of extracted data under
  `master/extracted/{submarines,ddg,ceiling}` — **no live links** (per user).
- `Deflators` de-duplicated to one shared tab; figure-register defined names were
  namespaced `sub_`/`ddg_` (then removed with the deck tabs, below).
- New **Portfolio Summary** answer page (Virginia | Columbia | DDG-51 | Total):
  per-class TAM from `tam_cell(li, fy)` on Sub TAM Build (LI 2013 = Virginia,
  1045 = Columbia; the all-streams per-class row sums exactly to the portfolio),
  DDG from DDG TAM Build, ceiling metrics from the ceiling layer. A §4 tie-out
  asserts Va + Col cumulative TAM = Sub TAM Build portfolio TAM.
- Relocation verified faithful: every per-program tab matched its source workbook
  cell-for-cell (only tab-name echoes differed), 0 formula errors on LibreOffice
  recalc, 0 dangling refs. (Committed as `5fd26030`, pre-SAM-strip.)

## 2. TAM-only (SAM model removed)
Per user: "it's the TAM workbook, not the TAM + SAM workbook." Removed the SAM
model and everything built only to feed it (TAM is upstream of SAM, so no TAM
number moved):

- **Deleted tabs/modules**: SAM Build ×2; DDG Scenarios; Worktype Evidence ×2;
  Worktype by FY ×2; Entity Master ×2; Location Master ×2; DDG Vendors; DDG FPDS
  Primes. Plus the deck-contract tabs (you don't use the decks): Figure Register
  ×2 and z_ChartData ×2. Plus unregistered dead modules (QA Reconciliation ×2,
  Number Audit ×2).
- **Stripped SAM from kept tabs**: Sub/DDG Executive Summary (SAM rows + scenario
  menu); Portfolio Summary (SAM rows, leaving TAM + ceiling); Sub Assumptions
  (scenario selector/matrix, bucket adjustments, default-scenario — rewritten
  TAM-only); DDG Assumptions (selected-scenario, §6 bucket adjustments);
  Sub/DDG Sensitivity (entity-master VLS section); Sub/DDG Methodology (SAM
  framework, bucket taxonomy, classification precedence, SAM flow rows).
- Verified: 42 tabs, 0 dangling refs, 0 formula errors on recalc, tie-out OK.

## 3. tam/ folder restructure (research preserved)
The per-program folders were ~95% upstream research corpus (`submarines/` 274 M,
`ddg/` 389 M — almost all `research/`), not workbook. So instead of deleting the
folders wholesale:

- **Renamed** `submarines/` -> `virginia_columbia_research/`,
  `ddg/` -> `ddg_research/` (kept `research/`, `extracted/`, `logs/`).
- **Deleted** the redundant workbook pieces (`workbook_<prog>/`, `build_workbook.py`,
  `validate_workbook.py`, `sheet_specs/`, the per-program `.xlsx`).
- **Deleted** `outsourcing_ceiling/` entirely EXCEPT `build_ceiling_base.py`,
  which moved to `master/build_ceiling_base.py`, repointed to read the renamed
  research corpora and write `master/extracted/ceiling/`. Reran it — output
  reproduces the committed snapshot exactly.
- Fixed the hardcoded `tam/<oldname>` path tokens in 7 research scripts; all
  compile.

## Verification
- Master rebuilds (42 tabs); LibreOffice recalc → 0 formula-error cells, 0
  dangling sheet-refs, Portfolio tie-out = OK.
- Relocated ceiling generator reproduces `wb_cost_base.csv` + `wb_anchors.csv`
  with zero diff vs the committed snapshot.
- Research corpora intact (`virginia_columbia_research` 270 M, `ddg_research`
  386 M).

## Open / not done
- **SAM `award_classification` scripts** (`sam/award_classification/...`, ~14
  files incl. `check_build.py`, `reconcile.py`, `extract_workbook_cuts.py`,
  `build_program_*.py`) reference the old `tam/{submarines,ddg}` paths and the
  deleted workbook packages. Left untouched per user (that bucketing workstream
  is considered stale — `reconcile.py` already pointed at `projects2`). If revived,
  those references need repointing.
- **Decks** (`decks/{submarines,ddg}`) still reference the old per-program `.xlsx`
  outputs; not repointed (decks out of scope — no live links wanted).
- Minor cosmetic prose staleness left as-is: Methodology §5 "evidence tab" column
  and the DDG Source Index "consumed by" column still name a few removed tabs.
- `tam/consolidated/` left in place (skipped per user; no dependency on the
  renamed folders).
