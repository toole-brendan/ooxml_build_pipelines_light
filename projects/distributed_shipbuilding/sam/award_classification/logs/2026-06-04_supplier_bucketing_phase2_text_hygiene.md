# 2026-06-04 — Supplier bucketing Phase 2 follow-up: stale-label text hygiene

## Scope

An independent review of the Phase-2 workbooks confirmed the numeric model is **correct and
validated** (0 formula errors; DDG/subs control totals match the signed-off reconciliation) and said
explicitly: *do not reopen the methodology, do not redo the model.* The only blocker to client-ready
was reader-facing text still describing the **old "description-led" classification** and the
**"foreign = supplier-addressable"** framing — both contradicting the registry-first method now wired
into the build. This pass patched exactly those rendered strings, rebuilt both books **in place**, and
reran the Phase-2 validation. **Text-only. No model / taxonomy / registry / scenario logic. No
`deck_core` / `workbook_core` changes. Decks untouched. Numbers byte-identical to Phase 2.**

Owner-confirmed scope: **rendered workbook text only** (`sheet_specs/*.md` design docs + module
docstrings left as-is); **`gfe_mib` / `gfe_sib` role-key split left untouched** — intentional (MIB vs
SIB domain language); each `_registry.py` normalizes the shared CSV `gfe` independently, and shared
tools (`check_build.py`, `reconcile.py`) defensively accept `{gfe, gfe_mib, gfe_sib}`. Not a calc defect.

## What was done (5 string edits)

1. **DDG `guide_methodology.py:60`** — §1 glossary row
   `("Description-led bucketing", "award description is the primary bucket arbiter", "DDG primary signal (subs is NAICS/vendor-led)")`
   → `("Registry-led bucketing", "operating-entity UEI resolves role + bucket; NAICS-4 fallback", "primary signal (both books)")`.
2. **DDG `guide_methodology.py:226`** — SAM hover `ExcelNote` residual `~42.9%` → `~33.6%`
   (residual $2,027.0M / addressable $6,027.2M = 33.6%; rest of the note unchanged).
3. **DDG `sources_references.py:52`** — SRC-08 `nc_records_long.csv` note
   `"Canonical subaward source. Description-led bucketing input."`
   → `"Canonical subaward source. Signed subaward records + sub_entity_uei for registry-led entity classification."`
4. **DDG `data_location_master.py:74`** — §3 banner `(foreign = supplier-addressable)`
   → `(foreign / FMS is excluded scope)`.
5. **Subs `data_location_master.py:85`** — §3 banner `(foreign = supplier-addressable)`
   → `(foreign / FMS is excluded scope)`.

## Validation (all green)

- **Rebuild:** both `.xlsx` regenerated in place, exit 0 (DDG 22 sheets, subs 18 sheets).
- **Numbers unchanged (the key safety check):** `check_build.py` oracle both **STATUS OK**, every total
  byte-identical to Phase 2 — DDG physical $4,000M / mission $2,665M / foreign $359M / residual
  $2,027M / addressable $6,027M / electrical $347M / VLS $1,678M; subs physical $4,786M / electrical
  $2,027M / modular $618M / addressable $5,451M. The text edits moved nothing.
- **Structural QA (DDG `validate_workbook.py`):** 51 parts, **0 xml errors, 0 error-literal cells**,
  22 sheets, tables intact.
- **Rendered-output grep (both `.xlsx`):** `Description-led` / `foreign = supplier-addressable` /
  `primary bucket arbiter` / `NAICS/vendor-led` = **0**; new strings present; the only `%…residual`
  label is now `33.6% unbucketed residual`; no literal `42.9%` text (bare-`42.9` digit hits are
  unrelated numeric cell values).

## Docstring sweep (raised during the session)

Module docstrings across both projects' `sheets/*.py` are **clean** — the only `description` mention in
a docstring is `_taxonomy.py` (module docstring + `classify()` comment), which correctly states
classification is registry-led and the legacy description-keyword step is dropped. Remaining
`description` hits are all legitimate: a CSV column name (`sources_source_index.py`), generic
"Description" QA table headers (`validation_qa_reconciliation.py` ×2), and the §6a justification text
("the prime's CLIN description … too coarse / misleading", which *supports* the new method).

## Open / flagged (not changed)

- **`guide_methodology.py:117`** — §4a "In TAM" list item `"Supplier-addressable component work, per
  award description"`. A rendered cell with a mild residual of the old framing (describes scope, not
  method). Flagged to owner; left as-is pending a decision — it was outside the review's list and the
  approved 5 edits.

## Files touched

- **Edited (build code, text only):** DDG `guide_methodology.py`, `sources_references.py`,
  `data_location_master.py`; subs `data_location_master.py`.
- **Regenerated in place:** both `20260601_…_vS.xlsx`.
- **Refreshed (auto-generated):** `reports/sheet_probe/*`.
- **No deck / `deck_core` / `workbook_core` / model / taxonomy / registry edits.**

## Status / next

Text hygiene complete; both workbooks rebuilt green, numbers identical to Phase 2, stale labels gone —
ready for workbook-level delivery. Decks remain untouched (separate narrative pass if wanted). One
optional rendered-text tweak (`guide_methodology.py:117`) awaits the owner's call.
