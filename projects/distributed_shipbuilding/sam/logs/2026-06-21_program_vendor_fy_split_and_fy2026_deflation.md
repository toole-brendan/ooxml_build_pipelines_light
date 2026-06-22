# 2026-06-21 — Program-vendor sheets: FY-split $ columns, then constant-FY2026$ deflation

Two sequential, user-driven features on the `award_classification_refactor` program-vendor sheets
(DDG / Virginia / Columbia), both done as **live cross-sheet formulas with no change to the raw
transaction sheets**. Neither was in `TENTATIVE_PLAN.md` PART A as written; the user directed both
explicitly. Workbook went 12 → 13 sheets; nothing committed (left in the working tree for review).

Same-day-but-separate from the morning's `2026-06-21_phase1_built_validated_reverted.md` session.

---

## Task 1 — Per-FY `$M` split on the program-vendor sheets

**Ask:** add columns splitting each subawardee-UEI's `Subaward $M` roll-up by **federal fiscal
year**, deriving FY from the calendar `Subaward Date` *at cross-sheet-reference time* (no FY column
added to the transaction sheets).

**Decisions (user):** dollars only (not records); **uniform axis** `≤FY12 + FY2013…FY2026` (15 bins,
matching the `award_analysis` convention); placed **after `Last Subaward`, before the archetype
columns** (Role/Description stays last → existing `right_spacer` untouched).

**Mechanism.** A federal FY is a contiguous date range and `Subaward Date` is stored as real Excel
serials, so each per-FY cell is the existing `Subaward $M` SUMIFS plus two date-boundary criteria on
the same date column (the one feeding First/Last) — e.g. FY24 = `>=DATE(2023,10,1)` &
`<=DATE(2024,9,30)`; `≤FY12` is open-below. The CY→FY conversion lives entirely in the formula. FY
column on the tx sheet is **not** touched. (Resolved an earlier agent discrepancy: the formulas key
on `$J` = Subaward Date via the `ddg_tx_cols("Subaward Date")` accessor, not a hardcoded letter.)

**Pre-verified** against the tx CSVs: **0 blank Subaward Dates** in all three programs and every
record falls in `≤FY12 ∪ FY13…FY26` → the 15 columns sum **exactly** to `Subaward $M`. Spans:
DDG FY2002(1 rec)+FY2013–FY2026; Virginia FY2013–FY2025; Columbia FY2016–FY2025.

**Build mechanics — the recurring constraint.** `make_flat_sheet` derives a sheet's columns from its
`extracted/<name>.csv` headers, so new columns must exist in the CSV. The canonical generator
`scripts/build_program_vendors.py` **cannot run in this tree** — its `_corpus` enrichment input
(`tam/ddg/research/extracted/entity_naics_lookup.csv`) was relocated by the `c8fdc925` tam/
restructure. So, mirroring the morning's `enrich_program_transactions.py` post-processor pattern:
- **Source-of-truth fix:** edited `build_program_vendors.py` (`HEADERS` + blank row placeholders) so
  a future corpus rebuild emits the FY columns.
- **Apply-now step:** patched the 3 committed `extracted/*_program_vendors.csv` directly (insert 15
  empty columns after `Last Subaward`). The FY cells are formula placeholders, so the corpus has zero
  influence on them — the validated baseline (rows/dollars/prose) stayed byte-identical but for the
  new columns. (Considered fixing `_corpus` to regenerate instead; rejected as higher-risk for this
  task — 6 candidate corpus copies exist post-restructure, and a regen could silently drift
  rows/dollars. Logged as a separate future fix if the pipeline is needed for PART B.)

**Files:** `build_program_vendors.py`; the 3 `*_program_vendors.py` (a `_fy_sumifs`/`_fy_le_sumifs`
factory + `_FY_HEADERS`, widths `W_FY×15`, `float_cols`, intro caption); the 3 extracted CSVs.

**Verify:** build green (12 sheets/10 tables); validate 0 errors; reconciliation `max |Σ FY − total| =
0.00 $M`, 0 out-of-axis, grand total **$12,486.97M ≈ $12.487B** (matches baseline).

---

## Task 2 — Convert the program-vendor `$` columns to constant **FY2026$**

**Ask:** the FY-split `$` (and the `Subaward $M` total) should *display constant FY2026$* — converted
**in place, no new columns** — via formula referencing a back-of-book deflator "helper" sheet, again
without touching the data sheets. Method per the `tam/master` workbook (Green Book).

**Decisions (user):** FY columns converted **in place** (not a parallel block); `Subaward $M`
**also converted** to FY2026$ so the FY columns still reconcile to it (whole dollar layer uniform
constant-$). Diverges from `TENTATIVE_PLAN` Phase 4's "parallel view, nominal as system of record" —
the user chose in-place; the canonical nominal $12.487B survives in the tx rows + these logs.

**Method reverse-engineered from `tam/master`** (`workbook_master_tam/sheets/submarines/data_deflators.py`
+ shared `workbook_core/deflators.py`): a `Deflators` tab holds FY · Procurement TOA index · a derived
`factor` · basis; consuming cells do `=then_year × 'Deflators'!D<row>`. Basis = OSD **FY2025 Green
Book, Table 5-4 (DoD Deflators – TOA), Procurement column (FY2025=100)**, rebased FY2026 → `factor =
102.10 / index`.

**Critical gap + sourcing.** `workbook_core/deflators.py` only covers **FY2022–FY2031** (the SCN-budget
years). The FY split needs **FY2002 + FY2013–FY2021** too. Read those straight from the authoritative
local PDF `~/Downloads/fy25_Green_Book.pdf` p.59 (Table 5-4, Procurement, Base Year 2025); FY2022–FY2026
matched the in-repo module exactly, confirming the right column. Index values used (FY2025=100):
FY2002 59.60 · FY2013 73.25 · FY2014 74.32 · FY2015 75.50 · FY2016 76.94 · FY2017 78.66 · FY2018 80.61 ·
FY2019 82.96 · FY2020 85.93 · FY2021 89.62 · FY2022 93.13 · FY2023 95.77 · FY2024 97.92 · FY2025 100.00 ·
FY2026 102.10. Kept a **project-local** table; shared `workbook_core/deflators.py` left untouched.

**Implementation.**
- **NEW** `extracted/deflators.csv` (hand-authored; no corpus dependency) + **NEW** `sheets/deflators.py`
  (`group="data"`, factor column = live formula `=102.10/$C{r}` — full precision, an improvement over
  tam/master's 2-dp string). Exports `deflator_factor_cell(fy_key)` → `'Deflators'!$D$<row>` (column +
  first row parsed from the rendered range; row order matches the CSV). `≤FY12` uses the FY2002 index
  (the lone 2001-10-22 → FY2002 record; $0 for the subs, a no-op there).
- Registered in `_tabs.py` (`TAB_DEFLATORS`) and `sheets/__init__.py` (appended at the **end** of
  `SHEETS` → last in the contiguous `data` block → back of the tab order).
- The 3 `*_program_vendors.py`: FY factory now appends `*{factor_cell}`; `Subaward $M` →
  `=SUM(M{r}:AA{r})` (sum of the deflated FY block = constant-$ lifetime total); a build-time assert
  (`"!$M$" in _cols("≤FY12 $M") and "!$AA$" in _cols("FY26 $M")`) guards the hardcoded block range;
  intro captions changed "nominal dollars" → "constant FY2026$ (Green Book … see Deflators tab)".
- **No CSV patching this round** — the FY columns already exist; only their *formulas* changed.

**Verify.** Build green (**13 sheets / 11 tables**); validate 0 errors. Rendered formulas confirmed
(FY24 → `…*'Deflators'!$D$21`, ≤FY12 → `$D$9`, FY26 → `$D$23`; `Subaward $M = SUM(M:AA)`). Offline
recon: constant-$ total **$14,405.3M** vs $12,487.0M nominal (**+15.4%**, older years scaled up;
per-program 11.0–17.9% by year-mix). **LibreOffice headless recalc** (gold standard): **0 error
cells**; recalc'd `Σ Subaward $M` matches offline **to the dollar** (DDG 4,192.70 / Virginia 6,027.51 /
Columbia 4,185.14); factor full-precision (FY2024 = 1.0426879…).

---

## Net state
- Program-vendor sheets: 15 per-FY `$M` columns + `Subaward $M`, **all in constant FY2026$**, summing
  to the total; new auditable `Deflators` tab with Green Book provenance.
- Transaction sheets, `_corpus`, and shared `workbook_core/deflators.py`: **unchanged**.
- Nothing committed. The 3 `*_program_vendors.csv` + `build_program_vendors.py` carry Task-1 edits;
  Task-2 added `deflators.csv`/`deflators.py` and touched `_tabs.py`, `__init__.py`, the 3 sheet modules.

## Carry-forward
- **No nominal $ on the program-vendor sheets** now (user choice). Canonical nominal $12.487B (matches
  USAspending) lives in the tx rows + logs; cite it from there if a nominal headline is needed.
- **Corpus pipeline is not runnable in this tree** (tam/ restructure moved `_corpus` inputs into
  `tam/{ddg_research,virginia_columbia_research}/…`). Both features were applied via direct-artifact
  edits with the generators fixed in parallel. Repairing `_corpus.PROGRAMS` paths is a worthwhile
  standalone task before any corpus-driven regen (PART B / prime pulls).
- Deflation is a single Procurement-index scalar (standard Green Book caveat) — not commodity- or
  supplier-specific inflation.
