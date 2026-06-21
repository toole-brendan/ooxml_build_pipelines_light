# 2026-06-09 — DDG & submarine workbooks: convert nominal then-year $ → constant FY2026 $

## Problem / goal

The DDG and submarine TAM/SAM workbooks
(`projects/ddg/workbook/workbook_ddg`, `projects/submarines/workbook/workbook_submarines`)
were built entirely in **nominal then-year dollars** — every P-5c budget figure was the
appropriated amount in its own FY (FY2022–FY2027). Goal: restate the **workbooks** (not the
deck — out of scope this session) in **constant FY2026 dollars** via the OSD "Green Book"
method, with the conversion shown as auditable work in a new "Deflators" tab. Implements the
repo-root plan `plan_fy2026_constant_dollar_conversion.md`.

## Deflator basis (verified at primary source)

OSD **National Defense Budget Estimates for FY2025** ("Green Book",
`~/Downloads/fy25_Green_Book.pdf`), **Table 5-4 DoD Deflators – TOA by Public Law Title**,
**Procurement** column (FY2025=100). SCN is a procurement appropriation and inherits the
Procurement deflator — the Green Book publishes no Navy/SCN-specific deflator. Rebased to
FY2026 = 1.000:

| FY | Procurement deflator (FY2025=100) | factor = 102.10 / deflator |
|----|-----------------------------------|----------------------------|
| 2022 | 93.13 | 1.0963 |
| 2023 | 95.77 | 1.0661 |
| 2024 | 97.92 | 1.0427 |
| 2025 | 100.00 | 1.0210 |
| 2026 | 102.10 | 1.0000 |
| 2027 | 104.24 | 0.9795 |

Use **Procurement**, not the O&M-Excl-DHP column (91.61/95.18/… with base 101.96) that an
earlier plan draft mistakenly listed.

## Design: parallel constant-$ layer on a shared index

Keep then-year inputs intact and blue (provenance); add a visible Deflators bridge; **repoint
the two model accessors** (`scn_cell`, `ap_lltm_base_cell`) to a parallel constant-$ block so
TAM → SAM → scenario → annual inherits constant FY2026 dollars. Only budget **levels** are
deflated; award/POP/MYP dollars stay nominal because they appear only inside dimensionless
SUMPRODUCT ratios (`model_tam_build §3` supplier coeff = `SUMPRODUCT(mask*$)/SUMPRODUCT(mask*$)`,
`model_sam_build §2` bucket shares) where the deflator cancels.

### Key plan-vs-code findings established during exploration
- **The "single chokepoint" claim is only partly automatic for DDG.** DDG
  `data_scn_budget.py` §2 derived ratios (`r_total = P["total"]`) and the §3 portfolio cost
  funnel (`_fy_sum(pkey) = SUM(...{P[pkey]}...)`) read the §1 row positions **directly via
  `P[...]`**, *not* through `scn_cell`. Repointing `scn_cell` alone leaves them on then-year —
  they had to be repointed to the constant rows too. **Subs are different**: their §1
  at-a-glance and §4 rollup route through `scn_cell`/`_portfolio`, so they inherit constant-$
  automatically once `scn_cell` is repointed.
- **`data_ap_bridge.py` needed no edit.** It has no "nominal/then-year" text, and its §2
  TAM-base derivation already sums `_cp_ap_base` (= `ap_lltm_base_cell`), so it inherits
  constant-$ once that accessor is repointed. The "no inflation" string the plan worried about
  lives only in the **unregistered** `validation_qa_reconciliation.py:99` (commented out of
  `SHEETS`, not rendered).
- **Only two rendered "Nominal $M" labels** exist: DDG `inputs_assumptions.py:89`, subs `:117`.

## Changes

### NEW `workbook_core/deflators.py` (shared, pure data + helpers)
`PROCUREMENT_TOA` (base 2025), `BASE_FY=2026`, `FY_RANGE`, `raw_index(fy)`, `factor(fy)`,
`GREEN_BOOK_CITE`. Mirrors the data-only convention of `groups.py`. Both workbooks import it.

### NEW `…/sheets/data_deflators.py` (DDG + subs twins, `data` group)
Renders the index as auditable work: FY | Procurement deflator (FY2025=100, blue input) |
Factor to constant FY2026 $. Promotes `deflator_factor_cell(fy)` → a live `'Deflators'!D<row>`
the budget sheets multiply by. `DEFLATORS = SheetEntry("Deflators", "data", _render)`.

### EDIT `…/sheets/data_scn_budget.py`
- **DDG**: added a **§1b "Constant FY2026 $M"** block (`Pc` dict) = each then-year §1 cell ×
  `deflator_factor_cell(fy)` (green `S_LINK_NUM`); repointed the three in-sheet dollar
  consumers `P → Pc` — `scn_metric_row` (drives `scn_cell`), §3 `_fy_sum`, and §2
  `r_total`/`num_r`. Ratio metrics (`bc_pct`/`gfe_pct`) left on the existing rows
  (deflator-invariant).
- **subs** (two classes 2013/1045): added a per-class **§Nd "Constant FY2026 $M"** sub-block
  (`pos_const`); repointed `scn_cell` dollar metrics → `pos_const`, ratios → `pos`. §1/§4
  inherit via `_portfolio`. `_DETAIL_BASE` assert unaffected (it bounds the §1 at-a-glance,
  which didn't change).

### EDIT `…/sheets/inputs_assumptions.py`
- **DDG** (`:89`, `:111`, `:167`): added a constant AP row = then-year AP × factor; repointed
  `ap_lltm_base_cell` → it; flipped Units label to `Constant FY2026 $M (then-year source
  retained)`.
- **subs** (`:117`, `:140`, `:224`): mirror; AP base = 0 for both classes so it's a numeric
  no-op, added for symmetry/scalability.

### EDIT `…/sheets/__init__.py` (both)
Registered `data_deflators` import + `data_deflators.DEFLATORS` in the `data` group, first
(before `SCN_BUDGET`). `package_workbook → _assert_group_blocks` (`lib.py:198-230`) enforces
one contiguous, canonically ordered run per group — passed.

### Inherited automatically (verified, no formula edits)
`model_tam_build` (`_scn(_LI,fy,'basic')`, `_cp_ap_base`), `model_sam_build` (single
`portfolio_tam` link), `data_ap_bridge` §2, chartdata/outputs.

## Verification (both workbooks)

Build: `PYTHONPATH=<repo root> python3 projects/<prog>/workbook/build_workbook.py` — DDG 23
sheets (Deflators = sheet 7), subs 19 (Deflators = sheet 6), contiguity assert passed.

Recalc: LibreOffice headless (`/opt/homebrew/bin/soffice --headless
-env:UserInstallation=file:///tmp/lo_profile --convert-to xlsx:"Calc MS Excel 2007 XML"`)
into a clean profile, then `openpyxl(data_only=True)` to read cached values + scan for error
cells.
- **0 Excel error cells** across all sheets in both workbooks.
- Deflator factors compute exactly (`[1.0963, 1.0661, 1.0427, 1.021, 1.0, 0.9795]`).
- Constant BC FY2022 ÷ then-year = 1.0963 (Procurement factor, **not** the 1.1130 O&M error);
  constant FY2026 == then-year. DDG §3 funnel "Basic Construction base" = `SUM` of the
  **constant** rows (the §2/§3 repoint worked).
- Headline TAM rose modestly (full precision): DDG portfolio TAM 3438.6 nominal → 3524.2
  constant (+2.49%); subs cumulative TAM ≈ 20,274. Supplier coefficient and SAM/TAM ratios
  unchanged — confirms the deflator only moved levels, not award-dollar ratio logic.

## Follow-up pass (same day) — user revisions to the Deflators tab

User asked to (1) delete the CBO Shipbuilding Composite Index secondary column, (2) show the
factor to 2 decimals, (3) de-LLM-ify the two column headers.

- **(1)** Removed the SCI column from both Deflators sheets (now 3 content columns) and its
  source row; removed `CBO_SCI`/`CBO_SCI_CITE` + docstring para from `workbook_core/deflators.py`
  (orphaned once the column was gone).
- **(2)** First attempt added an `S_NUM2` 2-decimal style (numFmt 168 + cellXf + constant) to
  `workbook_core/styles.py`. **User rejected touching shared styles** — reverted all three
  edits and did it **inline**: the factor is written as a preformatted string
  `f"{_d.factor(fy):.2f}"` ("1.10", "1.07", …). `cell()`/`write_row` only accept an integer
  cellXfs index (no inline numFmt), so a string is the only inline way to display 2 decimals.
  The budget formulas (`=<then-year>*'Deflators'!D<row>`) multiply by the text → Excel/LO
  **coerce the numeric string** in arithmetic → constants reconcile exactly to the displayed
  2-dp factor. Verified: 0 error cells, BC FY2022 ratio = 1.10000, FY2026 = then-year.
  Consequence: TAM now computed at 2-dp factor precision (DDG portfolio TAM 3524.2 → **3525.8**;
  immaterial, and now display = calc).
- **(3)** Headers: "Green Book Procurement deflator (FY2025=100)" → "Procurement deflator
  (FY2025=100)"; "Factor -> constant FY2026 $ (FY2026=1.000)" → "Factor to constant FY2026 $".

## Follow-up pass (same day) — external review reconciliation

Checked a third-party review (run against a stale, sheets-only `updated_ddg/` snapshot the
user had me copy earlier). Findings:
- "Registry update missing", "shared deflators.py missing" — **non-issues**; both are present
  in the real repo. The reviewer hit them because the snapshot copied only the `sheets/`
  folder (so `workbook_core/deflators.py` wasn't in it) and mistook `_registry.py` (a non-sheet
  helper) for the `__init__.py` SHEETS list.
- "CBO SCI still a placeholder" — **moot**; deleted in the pass above.
- **Polish A (fixed)**: DDG `data_ap_bridge.py` §2 header "Value $M" → "Value, constant
  FY2026 $M" (that block now derives from the repointed constant AP base). Subs AP Bridge has
  no analogous header (P-10 bucket bridge, AP base = 0).
- **Polish B (left open, optional)**: neither workbook's Source Index / References tab carries
  a Green Book/deflator row. The Deflators tab self-cites, and Source Index §1 is a native
  table strictly of `extracted/` CSVs (the Green Book is a hardcoded PDF-derived index, so it
  doesn't fit that schema). Offered to add a row to References if wanted.

## Gotchas / notes for next time

- **`col_letter` is 0-indexed** (0→A). In these budget sheets the label sits at col B
  (`col_letter(1)`), FY values run C..H (`col_letter(2..7)`); `write_row` `start_col=1` puts
  value[0] at col B (col A is the gutter).
- **Repointing `scn_cell` is NOT sufficient for DDG.** Its §2/§3 read `P[...]` directly; subs
  route through `scn_cell`/`_portfolio` and inherit. Always check whether an in-sheet consumer
  goes through the accessor or hits the captured row dict.
- **No inline number format exists** — `cell(ref, style=int)` only. To display N decimals you
  either register a cellXfs style (shared `styles.py`) or write a preformatted **string** in
  the module (which then relies on arithmetic coercion downstream — works in Excel and
  LibreOffice, verified).
- **The `updated_ddg/` snapshot is stale** (predates the SCI removal / 2-dp factor / header
  edits and is sheets-folder-only). Don't treat it as the source of truth; the repo is.
- Build invocation in this env: **`python3`** (not `python`), with `PYTHONPATH` = repo root
  (`ooxml_build_pipelines_light`) so `workbook_core` resolves; the launcher's own dir provides
  `workbook_<prog>`.
- Recalc-to-values for verification: `soffice --headless --convert-to xlsx` into a throwaway
  `-env:UserInstallation` profile re-saves with cached `<v>`, then `openpyxl(data_only=True)`
  reads them; error scan = any cell value starting `#` and ending `!`/`?`.

## Out of scope / follow-up
- **Deck unchanged this session** — slides s02/s05/s09/s11/s12/s13 + z_ChartData still say
  "nominal then-year"; workbook and deck intentionally diverge until a later deck pass.
- Polish B (central Green Book source row) pending user decision.
- A real CBO SCI sensitivity column would now be a fresh add (the placeholder was removed).
