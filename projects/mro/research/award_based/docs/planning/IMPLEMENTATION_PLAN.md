# Implementation Plan: Domnann TODO Backlog

## Context

The Domnann workbook builder has accumulated a backlog of correctness fixes, scope adjustments, and formatting issues documented in `TODOs.md`. Research (R1-R8) has been completed. This plan implements the remaining unchecked items, prioritizing data correctness first.

**Important**: The TODOs.md references line numbers from an older monolithic `build_from_data.py`. The codebase has since been refactored into modules under `build/`. All line references below use the current modular structure.

**Deferred**: C1 (executive summary sheet) is out of scope for this round.

**User decisions incorporated**:
- B4: Remove "Less: No vessel type designation" bridge row entirely (items with TAM category but blank vessel type will flow into TAM)
- B6: Replace dead RCOH/SLEP mekko rows with GFE and Construction Engineering (net 4 rows)
- R5: Exclude "Construction engineering / planning yard" from SAM scope; only GFE flows into SAM
- C1: Deferred to a follow-up round

---

## Phase 1: Fix ~$1B Double-Count (R3) -- CRITICAL

**Goal**: Eliminate OPN_BA3/BA5-8 duplicate rows that inflate FY26 by ~$729M and FY27 by ~$1.037B.

### Step 1.1: Mark duplicate rows as [REFERENCE] in data_v2.xlsx
- **File**: `build/data_v2.xlsx`, sheet "J Book Items Cons."
- **Rows**: 3209, 3210, 3211, 3221, 3222 (1-indexed spreadsheet rows)
- **Change**: Set column E (Row Type) to `[REFERENCE]` for each row
- The build script's `additive()` function (`data_reader.py:70`) returns `False` for `[REFERENCE]`, and the Row Class helper formula (`named_ranges.py:24`) produces `""` instead of `"ADD"`, so all SUMIFS automatically exclude these rows

### Step 1.2: Update Validation sheet text
- **File**: `sheets/validation.py`
- Update the OPN duplicate data quality issue description to note it has been resolved, with actual impact figures (~$729M FY26, ~$1.037B FY27)

### Verify
- Rebuild workbook. Compare Total Funding totals to prior version -- FY26 should drop ~$729M, FY27 ~$1.037B

---

## Phase 2: SAM Scope Corrections (R1 + R5)

**Goal**: Add USV to SAM exclusions; add GFE to SAM sub-category whitelist. Refactor bridge sections to use config set.

### Step 2.1: Add USV to exclusion set
- **File**: `config.py:74`
- Change `SAM_EXCLUDED_TYPES` from `{'Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles'}` to `{'Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles', 'Unmanned Surface Vehicles'}`

### Step 2.2: Refactor Newbuild SAM bridge to use config
- **File**: `sheets/newbuild_sam.py`
- Line 63: Replace hardcoded list `['Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles']` with `sorted(SAM_EXCLUDED_TYPES)` (already imported at line 10)
- Lines 44-56: Update purpose row text in both FY26 and FY27 branches to mention USVs

### Step 2.3: Refactor MRO SAM bridge to use config
- **File**: `sheets/mro_sam.py`
- Line 7: Add `SAM_EXCLUDED_TYPES` to the import from `build2.config`
- Line 49: Replace hardcoded list with `sorted(SAM_EXCLUDED_TYPES)`
- Lines 63-66: Replace hardcoded list in `excl_parts` with `sorted(SAM_EXCLUDED_TYPES)`
- Lines 32-39: Update purpose row text to mention USVs

### Step 2.4: Add GFE to Newbuild SAM calculations (R5)
- **File**: `sheets/newbuild_sam.py`
- GFE is NOT a DD&C sub-type, so it should NOT go in `ddc_subs` (line 29). Instead, add a separate GFE column to Section B (Vessel Type table) and Section C (Hull Program table):
  - Section B (~line 70-96): Add "GFE" header column after SLEP. Add SUMIFS formula `cf('JB_B,1', f'JB_W,"{vt}"', 'JB_F,"GFE / combat systems for newbuild"')`. Update `mc_subcat` from 8 to 9.
  - Section C (~line 98-132): Same pattern -- add GFE column. Update `mc_hull` from 9 to 10.
- Construction engineering is **excluded** from SAM per user decision

### Step 2.5: Update Validation sheet
- **File**: `sheets/validation.py`
- Add USV to SAM exclusions table with rationale
- Document GFE inclusion in SAM scope

### Verify
- Rebuild. Check FY26 Newbuild SAM bridge shows 4 "Less:" rows (Submarines, Aircraft Carriers, UUV, USV)
- Check FY26 MRO SAM bridge shows same 4 exclusions
- Check GFE column appears in Newbuild SAM Sections B and C with non-zero values for DDG/CVN programs
- USV rows still appear in TAM sheets

---

## Phase 3: Replace Hardcoded Values with SUMIFS (B1)

**Goal**: MRO SAM Section E should use live Excel formulas, not Python-computed literals.

### Step 3.1: Add JB_T named range
- **File**: `named_ranges.py:34-46`
- Add `('JB_T', 'D'),` to the `shared` list (column D = Line Item Title)

### Step 3.2: Replace literal values with SUMIFS formulas
- **File**: `sheets/mro_sam.py:226-230`
- Currently: `wc(ws, r, 2, val, font=F_DATA, fmt=NUM_FMT)` where `val` is a float from `d['sdm_cost_mix']`
- Change to write a SUMIFS formula. The `[SUB]` rows have Row Class = `""` (not `"ADD"`), so we cannot use the existing `cf()` cascade. Write the formula directly:
  ```python
  formula = f'=SUMIFS({bv_range},JB_S,"[SUB]",JB_B,2,JB_H,"",JB_A,"OMN",JB_T,"{title}")'
  wc(ws, r, 2, formula, font=F_DATA, fmt=NUM_FMT)
  ```
- This requires passing `bv_range` (the best-value range name, e.g. `'JB_26BV'`) into `create_mro_sam()`

### Step 3.3: Update function signature and call site
- **File**: `sheets/mro_sam.py:19` -- add `bv_range=None` parameter to `create_mro_sam()`
- **File**: `build_from_data.py:85` -- pass `bv_range=fyc['best_value_range']` in the call

### Step 3.4: Keep sdm_mix for ordering/filtering only
- The `sdm_titles` list (line 213) still uses `sdm_mix` to determine which rows to create and in what order. Keep this -- just change the cell value from literal to formula.

### Verify
- Rebuild. Click any $K cell in FY26 MRO SAM Section E -- should show a SUMIFS formula
- Values should match prior version's literal numbers exactly

---

## Phase 4: Newbuild TAM Fixes (B3, B4, B6, C2)

**Goal**: Fix table structure to show all in-scope types (B3), remove redundant bridge row (B4), replace dead mekko rows (B6), and restructure Section E layout (C2).

### Step 4.1: Remove "Less: No vessel type" from Newbuild TAM bridge (B4)
- **File**: `sheets/newbuild_tam.py:38-40`
- Delete the 3-line block that writes the "Less: No vessel type designation" row and its SUMIFS formula

### Step 4.2: Remove "Less: No vessel type" from MRO TAM bridge (B4)
- **File**: `sheets/mro_tam.py:41-44`
- Delete the same 3-line block

### Step 4.3: Show all in-scope types/hulls including zero-funding (B3)
- **File**: `data_reader.py`
- Currently `d['nb_nz']` (non-zero Newbuild types) is used for Sections B and D, and `d['nb_hull_tam_nz']` (non-zero hulls) for Sections C and E. Section B/C should show ALL in-scope entries including zero-funding; Sections D/E should keep the non-zero filter.
- Add new keys to the return dict:
  - `'all_nb_types'`: all vessel types in TAM_CATEGORIES with Bucket 1 data OR zero, sorted by service then name. Can reuse `d['all_tam_types']` which already includes all TAM-category types regardless of funding.
  - `'all_nb_hulls'`: all hull programs associated with in-scope vessel categories, including zero-funding hulls. Collect these during the main scan loop -- any hull where `cat in TAM_CATEGORIES` and `bs == '1'`, plus hulls with zero NB funding that belong to in-scope categories.
- **File**: `sheets/newbuild_tam.py`
  - Section B (line 48): Change from `d['nb_nz']` to `d['all_tam_types']` (already used here via `svc_order(d['all_tam_types'], ...)`  -- verify this is correct and includes zero-funding types)
  - Section C (line ~68): Change from `hull_tam_nz` to the new `d['all_nb_hulls']` list so all hull programs appear even with $0 funding
  - Sections D and E: Keep using `d['nb_nz']` and `hull_tam_nz` respectively (drop zeroed-out entries per the requirement)

### Step 4.4: Replace RCOH/SLEP with GFE + Construction Engineering in Section D (B6)
- **File**: `sheets/newbuild_tam.py:103-141`
- Current row layout: `dr = r+1` (DD&C), `ar = r+2` (AP/LLTM), `rcoh_r = r+3` (RCOH), `slep_r = r+4` (SLEP), `tkr = r+5` (Total)
- New layout: `dr = r+1` (DD&C), `ar = r+2` (AP/LLTM), `gfe_r = r+3` (GFE), `ce_r = r+4` (Const. Eng.), `tkr = r+5` (Total)
- Replace RCOH block (lines 129-134) with GFE:
  - Label: `'GFE / Combat Systems'`
  - SUMIFS filter: `'JB_F,"GFE / combat systems for newbuild"'`
- Replace SLEP block (lines 136-141) with Construction Engineering:
  - Label: `'Construction Engineering / Planning Yard'`
  - SUMIFS filter: `'JB_F,"Construction engineering / planning yard"'`

### Step 4.5: Same replacement in Section E mekko (B6)
- **File**: `sheets/newbuild_tam.py:147-203`
- Same pattern: replace RCOH/SLEP rows with GFE and Construction Engineering
- `rcoh_h = r+3` becomes `gfe_h = r+3`, `slep_h = r+4` becomes `ce_h = r+4`

### Step 4.6: Restructure Section E layout -- nest hulls under vessel type headers (C2)
- **File**: `sheets/newbuild_tam.py:147-203`
- Currently Section E is a flat mekko table with hull programs as columns, same structure as Section D
- Restructure to remove the Vessel Type column and instead group hull program rows under vessel type header rows, mirroring how Section G tables look on the Newbuild SAM sheet (`sheets/newbuild_sam.py` lines ~342-463)
- Implementation:
  - Group `hull_tam_nz` by vessel type using `d['hull_type']` mapping
  - For each vessel type that has non-zero hulls, write a `subsubsec_band` header row with the vessel type name
  - Under each header, write the hull program sub-category percentage rows (DD&C, AP/LLTM, GFE, Const. Eng.) and a Total $K row
  - This replaces the single wide mekko table with multiple per-vessel-type tables stacked vertically

### Verify
- Rebuild. Check FY26 Newbuild TAM:
  - Bridge section (A) no longer has "Less: No vessel type" row
  - Section B lists ALL in-scope vessel types including any with $0 funding
  - Section C lists ALL hull programs including any with $0 funding
  - Section D mekko shows DD&C, AP/LLTM, GFE, Const. Eng. (no RCOH/SLEP), only non-zero vessel types
  - Section E shows hull programs nested under vessel type headers, only non-zero hulls
  - Sub-category percentages should sum closer to 100% for vessel types with GFE
- Check FY26 MRO TAM bridge also lacks "No vessel type" row
- TAM totals will increase slightly (items with TAM category but blank vessel type now included)

---

## Phase 5: Validation & Vessel Audit (B5 + C3)

### Step 5.1: Vessel inclusion audit (B5)
- After rebuilding with all Phase 1-4 changes, compare vessel type lists across sheets:
  - TAM Section B should list all vessel types in TAM_CATEGORIES (including zero-funding)
  - SAM sections should include all non-excluded, non-zero types
  - No accidental drop-offs from the R1 USV change
- This is a verification step, not a code change (unless issues are found)

### Step 5.2: Add bucket 6+7 exclusion rationale (C3)
- **File**: `sheets/mro_sam.py:32-39` -- expand purpose row to explicitly state buckets 6+7 are excluded because they are "enabling" work types that support but are not themselves outsourceable depot/maintenance/modernization work
- **File**: `sheets/validation.py` -- add a section explaining the bucket 6+7 exclusion rationale

### Verify
- Rebuild. Read MRO SAM purpose row -- should mention bucket 6+7 rationale
- Spot-check vessel types in TAM vs SAM to confirm no drop-offs

---

## Phase 6: Formatting Fixes (D1-D4)

### Step 6.1: Em/en dashes to hyphens (D1)
Replace all em dashes (`\u2014`), en dashes (`\u2013`), and right arrows (`\u2192`) in workbook-facing strings with hyphens (`-`) or ASCII alternatives (`->`). Also replace right single quotes (`\u2019`) with straight apostrophes (`'`).

Files to update (output-facing strings only):
- `sheets/newbuild_tam.py` -- title band (line 22), purpose row (line 24), bridge (line 29), mekko headers (lines 97, 150)
- `sheets/newbuild_sam.py` -- title band (line 42), bridge (line 59)
- `sheets/mro_tam.py` -- title band (line 23), bridge (line 30), bucket label (line 32)
- `sheets/mro_sam.py` -- title band (line 31), bridge (line 42), section F header (line 252)
- `build_from_data.py` -- annotation text (~lines 140-270), error message (line 285)
- `sheets/validation.py` -- throughout (~50 occurrences)
- `sheets/total_funding.py`, `sheets/competitive_dynamics.py` -- title/purpose strings

### Step 6.2: Add dash preference to CLAUDE.md
- **File**: `CLAUDE.md`
- Add to Rules section: "Use hyphens (-) and ASCII arrows (->) instead of em dashes, en dashes, or Unicode arrows in all workbook-facing text. Use straight apostrophes (') not curly quotes."

### Step 6.3: Investigate underscores (D2)
- The `_italic_` markup in `prototype_annotations.py` strips underscores and applies italic formatting. If underscores leak, the fix is in `_make_drawing_xml()` (line ~68). Need to verify in actual workbook output.

### Step 6.4: Fix note bubble newlines (D3)
- Check annotation text lists in `build_from_data.py` for embedded `\n` characters or extraneous empty-string lines that create unwanted blank paragraphs
- Each item in the `lines` list becomes a separate `<a:p>` paragraph in OOXML

### Step 6.5: Fix note bubble dimension auto-fitting (D4)
- **File**: `prototype_annotations.py:33-54`
- Increase `_LINE_H` from `11 * _PT` to `14 * _PT` (177,800 EMU/line -- better for 8pt font with line spacing)
- Increase `_T_INS` and `_B_INS` from `45720` to `68580` (~50% more vertical padding)
- These changes make auto-computed `cy` taller, preventing vertical text cutoff
- May need iterative tuning after visual inspection

### Verify
- Rebuild. Open workbook in Excel:
  - No em/en dashes, curly quotes, or Unicode arrows in any cell or annotation
  - No raw underscores in annotation text (italic renders correctly)
  - No unwanted blank lines in annotation bubbles
  - Full text visible in each note bubble without vertical cutoff

---

## Summary of Files Modified

| File | Phases | Changes |
|------|--------|---------|
| `build/data_v2.xlsx` | 1 | Mark 5 rows as [REFERENCE] |
| `config.py` | 2 | Add USV to SAM_EXCLUDED_TYPES |
| `named_ranges.py` | 3 | Add JB_T named range |
| `build_from_data.py` | 3, 6 | Pass bv_range param; fix dashes in annotations |
| `data_reader.py` | 4 | Add all-inclusive type/hull lists for B3 |
| `sheets/newbuild_tam.py` | 4, 6 | Remove bridge row; show zero-funding types; replace mekko sub-categories; restructure Section E layout; fix dashes |
| `sheets/newbuild_sam.py` | 2, 6 | Use config for bridge; add GFE column; fix dashes |
| `sheets/mro_tam.py` | 4, 6 | Remove bridge row; fix dashes |
| `sheets/mro_sam.py` | 2, 3, 5, 6 | Use config for bridge; SUMIFS for Section E; bucket rationale; fix dashes |
| `sheets/validation.py` | 1, 2, 5, 6 | Update data quality text; add USV/GFE docs; bucket rationale; fix dashes |
| `prototype_annotations.py` | 6 | Fix auto-fitting constants |
| `CLAUDE.md` | 6 | Add dash preference rule |

## Dependency Graph

```
Phase 1 (R3 - fix double-count) -- CRITICAL, do first
  |
  +--- Phase 2 (R1 + R5 - SAM scope) ---+--- Phase 4 (B6 + B4 - mekko + bridge)
  |                                       |
  +--- Phase 3 (B1 - SUMIFS)       ------+--- Phase 5 (B5 + C3 - audit + rationale)
  |
  +--- Phase 6 (D1-D4 - formatting) -- independent, can run in parallel with any phase
```

## Execution Notes

- Each phase ends with a workbook rebuild and verification
- Phase 1 requires editing `data_v2.xlsx` (openpyxl write to mark rows as [REFERENCE])
- Phases 2 and 3 can be done in parallel (independent changes)
- Phase 4 depends on Phase 2 (SAM_EXCLUDED_TYPES must be finalized)
- Phase 5 depends on Phases 1-4
- Phase 6 is independent and can run in parallel with any phase
