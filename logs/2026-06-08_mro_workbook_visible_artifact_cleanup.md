# 2026-06-08 — MRO workbook: remove visible modeling/debug artifacts (generation-layer fixes)

## Scope

Sixth 06-08 presentation pass on the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`). Fixed a set of visible "modeling/debug"
artifacts that were leaking into presentation tabs, **in the sheet modules** (not by
post-processing the built xlsx). Six concrete defects, all from a user spec:

1. `z_ChartData` rendered bracketed deck chart keys (`[mro_work_segments]`) in section
   banners and filled every banner across all 25 columns (`_NCOLS=25`), so narrow blocks
   (§1/§5/§10/§12) looked like the fill ran forever.
2. `Reconciliation` rendered a "Deck slide" column in §1 and used one global column layout
   where the §2 wide "Line Item" column forced §1's numeric Value column (D) comically wide
   — one column doing two jobs.
3. `Methodology` still had a §7 "Confidence levels" section; §2a was missing a spacer; §1
   definition values were inconsistently capitalized.
4. `Awards` still exposed a raw "Vessel Confidence" column.
5. `Scope Reconciliation` filled every section banner across 11 columns (set by the §10
   paste block) even though most sections are 3–5 cols; §13.5 read "USCG confidence caveat".
6. `References` SRC-09 note still said "Confidence LOW on top-down".

**Every edit is presentation/text/layout only — no model/value change.** All gates green
with **no `regen-baseline`**: `build_workbook.py` → 19 sheets, **0 defined names**, 8 native
tables; `qa/verify_crosstab.py` → OK (4,290 formulas); `qa/tie_out.py compare … --tol 1.0`
→ **Invariant B (86 figures) + Invariant A (engine multiset) both match**. Workbook
7,363,110 → 7,292,125 bytes (dropped columns/section). Green baseline was confirmed
**before** editing so any post-edit delta would be attributable; it stayed green after.

## Why value-neutral (safety model)

- **Banner width / banner text** changes touch only styled-empty or text cells (a banner
  row has no numeric `<c>`), so Invariant A (numeric multiset over the 9 engine tabs, incl.
  `z_ChartData` and `Scope Reconciliation`) is unchanged.
- **Reconciliation column relocation** moves numeric cells *within* the same engine tab
  (§2 amounts shift one column right, F→G; §1 stays in D) and deletes only the **text**
  "Deck slide" cells. Invariant A is relocation-proof → unchanged. The producer accessors
  (`mro_tas_cell`/`omn_cell`/`scn_cell`/`uscg_isvs_cell`) capture the value column via
  `_NAME_COL`, and `qa/name_map` calls those same accessors, so Invariant B re-validates the
  86 figures at their new cells automatically (verified: §2 names now resolve to col **G**,
  §1 names stay col **D**).
- **Methodology / Awards / References** edits are on non-engine tabs (guide/data/sources);
  the deleted §7 / Vessel Confidence / SRC-09 phrase are all text, no numeric cells.

## Per-file changes

### chartdata_output.py (z_ChartData)
- Added `_CHART_KEY_RE` + `_visible_title()`; `_paste_block` now banners
  `_visible_title(title)` at **`n_cols=len(header)`** (the block's own width) instead of
  `_NCOLS`. The internal `title` strings keep their `[chart_key]` (deck-loader contract);
  only the rendered banner text drops the tag, and narrow blocks stop filling at their
  data width. Widened `_COLS` `[42]+[11]*24` → `[34]+[14]*24` (the 11-wide headers were
  cramped). Docstring updated. The §3 hull cross-tab (25-wide header) still spans B:Z.

### model_reconciliation.py (Reconciliation)
- **Dropped the "Deck slide" column** from §1 (header + both anchor loops + the deferred
  RECONCILED_MRO_TAM row); the `slide` field stays in the `_ANCHORS_*` tuples as in-source
  provenance (unpacked as `_slide`), and the orphaned `_RECON_SLIDE` constant was removed.
- **Decoupled the two-jobs column.** §1 stays in B:D (Anchor / Line / Value, value col D).
  §2 BudgetAnchors now starts at column **C** (`_S2_START_COL=2`, passed as `start_col` on
  every §2 `c.write`) and runs **C:I**, so the wide Line Item column gets its own column
  **E** and §1's numeric Value column D is narrow again. `_NCOLS 7→8`; new `_S1_NCOLS=3`;
  `_COLS [14,14,60,16,16,16,32] → [44,18,14,48,16,16,16,32]`. §2 amount columns shifted
  `E/F/G → F/G/H`; the FY25-Enacted name column `"F" → _FY25 ("G")`; the BudgetAnchors
  `ExcelTable` ref derived from `_S2_START_COL` (now `C30:I71`). §1 banner narrowed to
  `_S1_NCOLS`. The §2 internal-sum frow formulas were re-pointed to F/G/H; the deferred
  RECON row still references `D7` for the §1 embedded anchor.

### guide_methodology.py (Methodology)
- **Deleted §7 "Confidence levels"** (the whole section, all text). Added a generated
  `c.blank()` in §2a between the TAM formula sentence and the "Component (live)" header
  (a real emitted row, so row numbers stay deterministic). Sentence-cased five §1
  definition values (MRO / Embedded MRO / Reconciled MRO TAM / Private-addressable / FMS).
  Docstring drops the confidence mention and the §7 line.

### data_awards.py (Awards)
- Removed the `("Vessel Confidence", …)` entry from `_COLUMNS`. Safe: downstream SUMIFS use
  structured refs (`Awards[PSC]`, `Awards[FY2025 Obligation]`, …) and **no formula
  references `Awards[Vessel Confidence]`** (only stale `qa/*/probe/09_Awards.json` diagnostic
  dumps mention it; not a gate). Awards is excluded from Invariant A.

### validation_scope_reconciliation.py (Scope Reconciliation)
- `_section()` gained a default `n_cols=3`; §1 passes `n_cols=5`, §5 `n_cols=4`, §10
  `n_cols=_NCOLS` (the paste block). Every other section (§2/§3/§4/§6/§7/§8/§9/§11/§12/§13)
  uses the 3-col default, so narrow banners no longer fill across B:L. `_NCOLS` stays 11
  (the §10 paste sets the sheet width). Renamed §13.5 "USCG confidence caveat" → "USCG ISVS
  floor anchor".

### sources_references.py (References)
- Removed " Confidence LOW on top-down." from the SRC-09 USCG ISVS context note. (Reverses
  the prior pass's deliberate keep, per explicit user request this pass.)

## Verification

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py            # 19 sheets, 0 defined names, 8 native tables
/usr/bin/python3 qa/verify_crosstab.py        # CROSSTAB VERIFY OK (4,290 formulas)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Defense Drivers MRO_vS.xlsx" --tol 1.0
# -> Invariant B: 86 figures match; Invariant A: engine multiset matches  (NO regen)
```

Empirical built-xlsx spot-check (openpyxl): no `[` in any z_ChartData banner + §1 banner
fill stops at col C; Reconciliation has no "Deck slide", §1 header B:D, §2 header
C:Appropriation…E:Line Item…G:FY25 Enacted…I:Source, `OMN_1B4B_TOTAL` value 11,763,594 at
**G51**, table ref C30:I71; Methodology has no §7; Awards has no Vessel Confidence header;
References has no "Confidence LOW". `defined names: 0`. AST unused-import check clean
(only the `__future__` false positive). `py_compile` clean.

## Output filename note

The built workbook is now `projects/mro/20260607_Defense Drivers MRO_vS.xlsx` (the older
logs referenced `…Navy USCG Vessel MRO Spend_vS.xlsx`). `qa/tie_out.py`'s soffice recompute
uses a private UserInstallation, so it runs even with the file open in a desktop app.

## Not done / deliberate (offered, not applied)

- **Banner-width localization in `model_services.py` / `model_depot_ship_repair.py`** (user
  item 7's "especially …"). These were NOT in the stated defect list / priority order and
  are larger engine-tab surfaces (~14 / ~12 sections each, several true cross-tabs that must
  keep the wide width). The change is provably value-neutral (banners carry no numeric
  cells), so it's a clean follow-up if wanted — pass a local `n_cols` per simple section and
  keep the wide `_NCOLS` only for the genuine cross-tabs.
- `Reconciliation` §2 now leaves column **B** empty (44-wide) to the left of the C-started
  table — the deliberate cost of decoupling §1/§2; reads as the §2 table indented under a
  full-width banner.
- SRC-10 in References still reads "HII **Marine** Technologies (Ingalls)" — the actual HII
  segment is **Mission Technologies** (the Figure Register was already fixed Marine→Mission a
  prior pass). Not in this pass's spec; flagged for a future correctness fix.
