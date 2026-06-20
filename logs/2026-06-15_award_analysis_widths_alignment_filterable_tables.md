# 2026-06-15 — Award Analysis workbook: de-LLM styling pass, then standardized widths / header alignment / filterable cut tables

Pipeline: `projects/distributed_shipbuilding/workbook_award_analysis/`
Output:   `projects/distributed_shipbuilding/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`
Build:    `python3.12 build_workbook.py` → `python3.12 validate_workbook.py`
(the system `python3` is 3.9 and lacks the right env; `python3.12` has openpyxl.)

Two distinct phases this session. Phase 1 was a source-level "de-LLM" styling
review the user pasted in. Phase 2 (planned + approved) was a larger
column-width / header-alignment / filterability refactor.

---

## Phase 1 — de-LLM styling pass

Implemented a reviewer's recommendations to make the workbook read as analyst-
built rather than generated. All builds clean (0 xml errors, 0 error-literal
cells) throughout.

1. **Short section banners** — every `§N - …` banner compressed to a short noun
   phrase (e.g. `§N - Virginia (Reported Subaward $M by Role x Subaward FY)` →
   `§N - Virginia by role`). Applied to all sheets incl. the leaf tables not in
   the reviewer's explicit list, per the stated standard "every section banner
   short."
2. **Overview section numbered** — `Corpus shape` → `§1 - Corpus shape`.
3. **Compressed the long visible note rows** on By PIID, PIID x Work Type (×2),
   Re-buy Timing, Source Concentration, Prime Awards, Tie-Outs to one short
   analyst sentence each (authoring detail stays in the source docstrings).
4. **Black derived-date style** — added `S_DATE` (54) and `S_DATE_TOTAL` (55) to
   `workbook_core/styles.py` (numFmt 169, black/bold fonts) + `BORDER_TOP_FOR`
   entries. Re-buy Timing's **Last award** (`MAXIFS`) and **Next re-buy** (`last
   + gap`) switched from green `S_DATE_LINK` to `S_DATE` — they are derived
   formulas, not pure cross-sheet links. (PIID x Work Type's First/Last Award
   stay `S_DATE_LINK` — those *are* genuine links into Lane Detail.)
5. **Bold total-row labels** — passed `S_BOLD` (→ `S_TOTAL` via `BORDER_TOP_FOR`)
   as the first style in every `c.total(...)` on By Role / By Work Type / By
   Vessel / By PIID / PIID x Work Type.
6. **Source-only doc drift** — fixed the registry comment in `sheets/__init__.py`
   (`summary → model → data → validation`, model before data) and genericized
   the TAM/SAM wording in shared `workbook_core/groups.py` (the `model` group
   description + the unused `GROUP_LABEL` "Model (TAM/SAM)" → "Model"). Confirmed
   `GROUP_LABEL` is unused anywhere, so that change is cosmetic/safe for the
   other pipelines that import `workbook_core`.

`styles.py` additions are append-only (indices 54/55), so no existing style
index shifted — the MRO / consolidated / ddg / submarine pipelines are
unaffected.

---

## Phase 2 — widths, header alignment, filterable cut tables (planned + approved)

### The triggering bug
User: "tried using a filter on one table and it just didn't work at all." Root
cause (verified against source + the built .xlsx): only the **6 leaf "data"
sheets** were native Excel tables; the **9 model/screen sheets had no filter at
all** — no worksheet- or table-level `autoFilter`. `fullCalcOnLoad="1"` is set,
the leaf table autoFilters are wired correctly, so it was a coverage gap, not a
wiring bug. The user most likely clicked a model/screen sheet (By PIID, a jump-
ball screen, …) that looks like a table but isn't one.

### Decisions (via AskUserQuestion)
- Header alignment: **left for all columns except date columns (centered).**
- Filtering: **make every cut sheet filterable.**
- By Vessel (multi-grain): **flatten only the builder×work-type detail; keep the
  class/builder summary styled.**
- On-sheet totals: **filter-aware Totals Row (SUBTOTAL).**
- By Role "Supplier share of reported" %: **relocate to Overview.**

### Key enabling insight
The cut sheets hold **no unique data** — every cell is already a SUMIFS/SUM over
a leaf (Lane Detail / Role Detail / Lane Vendors / Lane Vendors x FY). So the
cross-sheet accessors that pointed at on-sheet subtotal cells were reimplemented
as **SUMIFS-over-leaf fragments** with the *same signature* `fn(program) -> str`.
Consumers wrap them as `f"={accessor(prog)}"`, so **Overview and Tie-Outs needed
no formula changes**, and the tie-out invariant survives (the independence lives
in the leaves, not the cuts).

### What changed
1. **New `sheets/_widths.py`** — one width constant per column semantic
   (`W_PIID`, `W_FY`, `W_FY_N`, `W_DATE`, `W_PCT`, `W_COUNT`, `W_DOLLAR`,
   `W_VENDOR`, `W_WORKTYPE`, `W_ROLE`, `W_LABEL`, …) + `header_styles(headers,
   date_headers)` (left for all, center for named date columns). FY columns kept
   compact (~9/7) since their headers are ≤5 chars; the truncated offenders were
   the long meta headers.
2. **Width + alignment on the non-flattened sheets** — Role Detail, Lane Detail,
   Lane Vendors, By Vendor, Lane Vendors x FY, Prime Awards. A few over-long
   headers shortened per house style (e.g. `$M (full hist)` → `$M (hist)`,
   `PIIDs w/ work type (fleet)` → `PIIDs (flt)`, `Prime base award` →
   `Base award`). Lane Vendors x FY Work Type widened 18 → 34 (was clipping
   bucket names).
3. **Additive leaf ranges** — `ld_cols()` += `dtot`/`ntot` ($ Total / N Total
   columns), `rd_cols()` += `dtot`. Build-verified as a no-op first.
4. **Flattened 6 cut sheets** into single filterable native tables, each with a
   leading **Program** column, one section banner, a combined program loop, a
   **+1 column-shift** on every criteria self-reference (Program inserted at B),
   and a filter-aware `SUBTOTAL(109,…)` Totals Row placed one row *below* the
   table ref:
   - By Role (`ByRole`), By Work Type (`ByWorkType`, the two $/N grids merged to
     one row per the Lane Detail side-by-side pattern), By PIID (`ByPIID`),
     PIID x Work Type (`PIIDxWorkType`), Re-buy Timing (`RebuyTiming`), Source
     Concentration (`SourceConcentration`).
5. **By Vessel (option b)** — kept §1 class summary + §2 builder summary as the
   styled two-pass blocks; replaced §3/§4 detail grids with one filterable table
   `ByVesselDetail` (`Builder | Work type | …FY… | Total`). Summary blocks share
   the detail's value columns (D..S) with a blank column C so the shapes align
   under one width set. §1 class rows flipped green→black (now SUMIFS over Lane
   Detail, not links to By Work Type). Two-pass `assert det_pos2 == det_pos`
   kept.
6. **Accessor rewire** — `wt_total_cell` / `wt_records_total_cell` /
   `wt_total_fy_refs` / `role_supplier_*` / `vessel_total_cell` / `piid_total_*`
   / `pw_*` now return SUMIFS-over-leaf fragments. `piid_section_cols` still
   returns per-program contiguous sub-ranges (the loop writes program-by-program,
   so rows stay contiguous) → **Overview's PIID-coverage formula unchanged.**
7. **Overview** — added a per-program "Supplier share of reported" row
   (`SUMIFS supplier $ / SUMIFS all-role $` over Role Detail). Flipped the
   headline `$M` / records rows green→black (they're SUMIFS now, not pure links).
8. **Tie-Outs** — added an `is_link` flag per measure: the two leaf legs (By
   Vendor, Lane Vendors x FY) stay green `S_LINK_*` (real cell links); the five
   SUMIFS legs are black `S_NUM`/`S_INT`. No structural change — it remains the
   reconciliation oracle.

### Verification
- Build clean: 0 xml errors, 0 error-literal cells; **native tables 6 → 13**;
  48 parts.
- All 13 tables: `autoFilter == ref`, column span == header count.
- Totals rows: each new table's `SUBTOTAL` row sits at `ref_last + 1` (outside
  the table ref) with a "Total" label.
- Column shifts spot-checked in the built XML (By Role role-criteria `$C`, By
  PIID `C7`, PIID×WT `C7`/`D7`, By Vessel detail `$C23`, etc.).
- Header alignment confirmed in built file (all `s=2` left; First/Last Award
  `s=22` center).
- By Vessel §2 SUMs verified against the detail spans (GD-BIW = rows 23–29,
  HII-Ingalls = 30–37).
- **Tie-out math independently recomputed from the extracted CSVs** (the build
  can't evaluate formulas; per user, no headless-recalc step). Per program, all
  five $ leaves agree within rounding (<$0.5M) and all four record leaves agree
  exactly:

  | program  | LaneDet | RoleDet | LaneVend | ByVendor | LaneVndFY |
  |----------|--------:|--------:|---------:|---------:|----------:|
  | virginia | 4343.60 | 4343.60 | 4343.60  | 4343.60  | 4343.59   |
  | columbia | 3342.23 | 3342.23 | 3342.22  | 3342.23  | 3342.23   |
  | ddg      | 3095.42 | 3095.41 | 3095.40  | 3095.41  | 3095.40   |

  Records: virginia 7725 / columbia 5281 / ddg 5741 — exact across all leaves.
  So Tie-Outs §1/§2 will read **OK** for all three programs on reopen in Excel.

### Files touched (Phase 2)
- **new** `sheets/_widths.py`
- `sheets/data_lane_detail.py`, `sheets/data_role_detail.py` (+dtot/ntot ranges;
  widths/alignment)
- `sheets/data_vendor_lane.py`, `sheets/data_by_vendor.py`,
  `sheets/data_lane_vendor_fy.py`, `sheets/data_prime_calendar.py`
  (widths/alignment, header shortening)
- `sheets/data_by_role.py`, `sheets/data_by_worktype.py`,
  `sheets/data_by_piid.py`, `sheets/data_piid_worktype.py`,
  `sheets/data_rebuy_timing.py`, `sheets/data_source_concentration.py`,
  `sheets/data_by_vessel.py` (flatten + table + totals row + accessor rewire)
- `sheets/summary_overview.py` (share rows, color), `sheets/validation_tie_outs.py`
  (per-leg color)
- No `workbook_core/` changes in Phase 2 (autoFilter, no-format table style,
  S_HEADER_* all already existed). Totals rows are plain `SUBTOTAL` rows below
  each table — the engine has no `totalsRowCount` support, so the native
  totals-row mechanism was avoided deliberately (and it sidesteps a ref
  off-by-one).

### Notes / follow-ups
- Verification of Tie-Outs OK/FAIL is by the user reopening in Excel (caches the
  recalced values); intentionally no LibreOffice headless step.
- A few long headers still clip by ~1 char at the standard width (e.g. "Active
  vendors", "Vendors recent") — accepted edge cases per the user's "most headers
  readable" bar.
- The longest work-type bucket ("Electrical power / distribution / generation",
  43 chars) clips at `W_WORKTYPE=34` — accepted edge case; the bucket display
  names are copy-from canonical taxonomy and were not shortened.
