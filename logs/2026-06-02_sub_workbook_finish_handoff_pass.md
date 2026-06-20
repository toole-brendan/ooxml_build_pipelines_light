# 2026-06-02 — sub workbook: finish-handoff pass (deck contract, SIB, notes, annual headlines)

## Scope

Implemented the `core/submarine/workbook_finish_handoff_plan_2026-06-02.md` across the
`workbook_sub` sheet modules. This is a **finishing pass, not a modeling rewrite**:
the TAM/SAM calc chain, the AP/LLTM additive base = $0, and the no-SOM boundary are
unchanged. Work was presentation semantics, native Notes, gutter consistency, SIB
terminology, deck-data packaging, and the same-sheet green-link cleanup.

**Hard constraints honored (per the user, mid-session):**
- **No edits to any `core/workbook_core/` engine file.** Every change is in
  `core/submarine/workbook/workbook_sub/sheets/`. Verified: zero engine edits.
- **No `AP/LLTM`→"AP and LLTM" / `TAM/SAM`→"TAM and SAM" relabel.** The plan's
  Phase 3.3 slash→"and" deck-label change was dropped; the few I'd seeded into the new
  deck sheets were reverted to the slash convention (incl. `GFE / SIB`, not "GFE and SIB").
- **No package-hygiene / gutter-audit tools added to `core/tools`.** The plan wanted
  permanent tools there; instead the gates were verified with a throwaway pipeline-local
  script (removed after).

Two forks the user chose: **both** `Chart Data` and `Slide Data` output sheets, and the
**deep** `gfe_mib`→`gfe_sib` rename (not just visible-label).

Final: `python build_workbook.py` → **21 sheets, 12 native tables, 8 note parts, 155,620 bytes**.

---

## 1. SIB terminology + deep `gfe_mib` → `gfe_sib` rename

- `taxonomy.py`: `GFE_MIB_NAME_KEYS`→`GFE_SIB_NAME_KEYS`; `classify()` role `gfe_mib`→`gfe_sib`
  and basis `"GFE/MIB name"`→`"GFE/SIB name"`. (Role mask + emitted role value change
  together, so the SUMPRODUCT rollups are value-preserving.)
- `entity_master.py`: `role_keys`, `_BASIS_KEYS`, at-a-glance `role_dollar_cell('gfe_sib')`,
  the "GFE / SIB total" label; `§5` header + banner `Basis`→`Class rule`.
- `sam_build.py` `_XROLES`: `gfe_sib` + "GFE / SIB (Navy-directed, BlueForge)".
- `mib_excluded.py` (filename kept): tab `_TAB`→**`SIB Excluded`**; `_build/_render`/SheetEntry
  →`_build_sib_excluded`/`_render_sib_excluded`/`SIB_EXCLUDED`; accessor `sib_total_cell()`
  with `mib_total_cell = sib_total_cell` **back-compat alias**; all visible labels →SIB.
  Source-data JSON key `dollars_excluded_mib_$M` left as-is (external file key).
- `figure_register.py`/`qa_reconciliation.py`/`methodology_scope.py`/`source_index.py`/
  `pop_source_audit.py`: import `sib_total_cell`; DO-08/QA-09 + definitions/exclusions/
  precedence + Source Index text →SIB. `__init__.py` registers `mib_excluded.SIB_EXCLUDED`.
- `worktype_evidence.py`: per-bucket vendor `Basis`→`Class rule` header.
- The single MIB→SIB glossary note lives on Methodology & Scope (see §6).

## 2. Annual headline metrics + defined-name promotion

- `executive_summary.py` §1: **average annual** TAM/SAM moved **above** cumulative; cumulative
  relabeled `FY22-FY27 cumulative`; wording "average annual FY22-FY27 opportunity".
- `sam_build.py`: scenario-output columns reordered to **`Avg annual $M` first**, then
  `Cumulative SAM $M`, then `% of TAM` (accessors `sam_cell`→col D, `sam_pct_cell`→E,
  `avg_annual_sam_cell`→C updated to match; §7 INDEX/MATCH ranges + §9 broad check repointed).
  At-a-glance now leads with avg-annual selected SAM.
- `figure_register.py`: added defined names `portfolio_tam_annual`, `portfolio_tam_cumulative`,
  `broad_sam_annual`, `broad_sam_cumulative`, `fiscal_year_count`; kept `portfolio_tam` /
  `sam_broad` as **cumulative aliases**. Added headline figure **DO-10** (avg annual broad SAM)
  + a **Unit** column; realigned all `slide` numbers to the 18-slide deck architecture.

## 3. Annual SAM-by-FY producers (`sam_build.py`)

New `§8 - Annual SAM by fiscal year` block + accessors `annual_sam_cell(scenario, fy)` and
`annual_broad_sam_cell(fy)`: annual scenario SAM = `tam_total_cell(fy) ×
SUMPRODUCT(modeled bucket shares, scenario flags)`. New `§9` check ties per-FY annual broad
SAM to the cumulative broad SAM (`SUM = cumulative`, holds by construction). Checks renumbered.

## 4. Deck data-contract sheets (new, `outputs` group)

- **`chart_data.py`** — `Chart Data` tab; one normalized native table `tbl_deck_chart_data`
  (12 cols, ~96 rows) with CD_07/08/09/10/11/13/14/15/16/A5/A6 blocks. Every `Value` is a
  producer link or a derived formula over producers; `assert_links()` fails the build on any
  hardcoded link row. Added producer accessors to back it: `entity_master.top_supplier_indices`,
  `mib_excluded.sib_entity_dollar_cell`/`SIB_ENTITY_NAMES`, promoted `sensitivity` coeff/TAM cells.
- **`slide_data.py`** — `Slide Data` tab; `tbl_deck_slide_data` (8 cols) with
  SD_04/05/06/12/17/18 exhibit blocks; KPI rows link producers, descriptive rows literal.
  Scorecard qualitative attributes deliberately left to the deck (not fabricated here).
- Both registered after `figure_register` (outputs group stays contiguous).

## 5. Figure Register + Number Audit for the deck contract

- Figure Register slide IDs → 18-slide architecture; DO-10 + Unit column (§ above).
- `number_audit.py`: new **`§4 - Chart Data tie-out`** — for one headline link per CD block,
  links the Chart Data value cell **and** its producer cell and computes the delta
  (`chart_data.chart_audit_links()`); 0 by construction. Confirmed each pair (e.g.
  `CD_09` `Chart Data`!H31 ↔ `TAM Build`!C119).

## 6. Native Notes + visible prose cleanup

18 hover Notes on **basis/label cells only** (never the numeric value cell), per the plan table:
- Executive Summary (3: avg-annual cadence, broad-SAM-not-SOM, AP/LLTM $0).
- Methodology & Scope (4: the one **SIB glossary** note + TAM/SAM/AP-LLTM definitions).
- Assumptions & Controls (2: AP/LLTM toggle, default scenario).
- TAM Build (2: applied vs broader coefficient, AP/LLTM reference).
- SAM Build (2: unbucketed treatment, broad-SAM-not-SOM).
- LLTM AP (2: gross overlaps BC, additive base $0).
- SIB Excluded (1: why BlueForge/TMG/IALR excluded).
- Sensitivity (2: pre-boundary not headline, gross AP reference).

No row-by-row notes on the large data tables. Entity Master / Worktype Evidence `Basis`
header → `Class rule` (reads as a rule, not prose).

## 7. Gutter `x` / outline consistency

Added `mark_collapsible=True` to section banners that govern outlined rows (directly or via
subsections): Executive Summary `§1/§2/§3/§4/§5/§6`, Methodology `§1/§2/§3/§4/§5/§6/§7`.
Removed the false marker on Methodology `§2b` (its rows are level-0). Umbrella sections that
have outlined descendants are marked, matching the existing TAM Build convention.

## 8. Same-sheet green-link cleanup + data validation

- **72 same-sheet green links → black** across TAM Build (30: §1 + §4a coeffs + §4 base rows),
  SCN Annual (24 glance), POP Source Audit (5), LLTM AP (5), SAM Build (4), Entity Master (2),
  Sensitivity (2). Cross-sheet links (e.g. §2 base rows → SCN Annual / A&C; the §2b register →
  POP Location Parse; selected-scenario → A&C) correctly **stay green**. Final count: **0**.
- `Assumptions & Controls`: data-validation **dropdowns** on the default-SAM-scenario cell
  (inline list of the 5 scenario names) and the two stream-include toggles (`0,1`). Emitted in
  correct CT_Worksheet order (before the notes' `legacyDrawing`). Row-2 title switched to `_TAB`.

---

## Verification (read-only / structural — the standing ceiling)

Throwaway verifier (removed after) over the freshly built `.xlsx`. **All gates PASS:**
- **Package hygiene:** `cellXfs` 23 == `len(CELL_XFS)`; no `sharedStrings.xml`; no
  `mc:Ignorable`; every native table uses `WorkbookCore_NoFormatTable`; comments parts
  `{1,2,3,4,5,7,16,17}` == VML parts; max used style idx 22 < 23.
- **Gutter:** 0 `MISSING_X`, 0 `X_WITH_NO_GROUP`.
- **Terminology:** 0 visible `MIB` in cells (only the one glossary Note).
- **Structure:** 21 sheets; outputs group contiguous (Figure Register / Chart Data / Slide
  Data); **0 `#REF`**; 0 dangling sheet refs.
- **Formula/style:** 0 same-sheet green links.
- **Notes:** 18 notes, all pass `validate_excel_notes` (single A1, unique, non-empty);
  exactly 1 MIB-explaining glossary note; none on numeric value cells.

**Environment:** `python` on PATH; read-only probe + a throwaway verifier; no mutations beyond
the workbook build output.

## Deliberately NOT done
- **No Excel recompute.** `Number Audit` 0 FAIL / `QA Reconciliation` all OK can't be
  evaluated here (needs Excel). The chains reference valid cells (0 `#REF`/dangling), the
  identities hold by construction, and the Chart Data tie-out is 0 by construction.
- **No core engine edits / no core audit tools** (per the user).
- **No slash→"and" relabel** (per the user).
- **Absolute-accessor conversion** (`sheet_ref`/`abs_ref`) and the **mass row-2 title literal
  swap** — skipped as low value for a fully-regenerated workbook (positions recompute each
  build; title literals already equal `_TAB`). Easy to revisit if wanted.

## Files changed this session
- **Added:** `workbook_sub/sheets/chart_data.py`, `workbook_sub/sheets/slide_data.py`.
- **Edited:** `taxonomy.py`, `entity_master.py`, `sam_build.py`, `tam_build.py`,
  `assumptions_controls.py`, `executive_summary.py`, `methodology_scope.py`, `lltm_ap.py`,
  `sensitivity.py`, `pop_source_audit.py`, `mib_excluded.py`, `figure_register.py`,
  `number_audit.py`, `qa_reconciliation.py`, `source_index.py`, `worktype_evidence.py`,
  `scn_annual.py`, `sheets/__init__.py`.
- **Unchanged:** all of `core/workbook_core/`; the deck pipeline; DDG.
- **Rebuilt artifact:** `20260601_Distributed Shipbuilding Submarines_vS.xlsx` (21 tabs).
- **This log.**

## Follow-ups
- **Open in Excel** to confirm `Number Audit` / `QA Reconciliation` evaluate to 0 FAIL and no
  cell trips a repair dialog (the one out-of-environment check).
- **Deck pipeline** can now consume `Chart Data` (CD_* blocks) / `Slide Data` (SD_*) and the
  new defined names (`portfolio_tam_annual`, `broad_sam_annual`, `fiscal_year_count`, …);
  `portfolio_tam` / `sam_broad` remain as cumulative aliases until the deck adopts the new names.
- Optional later: absolute accessors; deeper SIB cleanup (table-name `tbl_sub_*`); the
  row-2 `_TAB` swap across the remaining sheets.
