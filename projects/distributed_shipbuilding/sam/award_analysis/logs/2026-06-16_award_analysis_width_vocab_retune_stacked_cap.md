# 2026-06-16 — Award Analysis workbook → width-vocabulary retune + stacked-tab cap

## Goal

Make the 8-tab Award Analysis workbook
(`20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`, pipeline
`projects/distributed_shipbuilding/workbook_award_analysis/`) read as one ruled
system instead of "some areas padded, others tight." Follow-on to the
[8-tab refactor](2026-06-16_award_analysis_8tab_refactor_steps3-6.md), which
flagged the stacked-width compromise as a known cosmetic item.

Two separate problems, fixed independently:
1. **Retune the semantic width vocabulary** in `_widths.py` so a given column TYPE
   sizes the same everywhere.
2. **Cap inherited widths on the stacked coordinator tabs** so one long
   vendor/label/work-type column in a later section can't widen the same physical
   column for an unrelated FY/count/status field elsewhere. (This was the bigger
   issue: Indicators / Market Views / Detail Tables stack heterogeneous sections
   and `merge_cols(*col_lists)` took a literal per-position max.)

**Cosmetic only** — every edit is a `cols=[...]` width or a header-cell alignment
style. Zero formulas/values touched, so the tie-out invariant holds by
construction (baseline unchanged: virginia $4343.6 / 7725 · columbia $3342.2 /
5281 · ddg $3095.4 / 5741).

## Changes

**`_widths.py` (the shared vocabulary).**
- Retuned all 19 semantic constants. Text columns tightened so wide fields stop
  driving sheet width — long edge-case strings clip rather than widen:
  `W_VENDOR` 42→34, `W_LABEL` 46→40, `W_WORKTYPE` 34→30, `W_CAPABILITY` 30→28;
  `W_ROLE` 22→24, `W_PIID` 17→18, `W_BUILDER` 13→14, `W_PROGRAM`/`W_FAMILY` 11→12,
  `W_CLASS` 10→12, `W_STATUS` 13→15. Numerics nudged up for header breathing room:
  `W_FY` 9→**10**, `W_FY_N` 7→**8**, `W_COUNT` 13→14, `W_DOLLAR` 12→13,
  `W_PCT` 13→14, `W_DATE` 12→13. (`W_UEI` 14, `W_NAICS4` 8 unchanged.) Kept
  `W_FY`/`W_FY_N` below the guide's general 12–14 numeric range on purpose: the
  15–16-column FY grids would bloat otherwise. Used the **primary** baseline
  `W_FY=10`, not the conservative `W_FY=9` alternative.
- **`STACKED_COL_CAP = 32`** + `merge_cols(*lists, cap=STACKED_COL_CAP)`: still a
  per-position max, then `min(w, cap)`. `cap=None` = old true-max behavior. 32
  (not 30) so real text columns still breathe but `W_VENDOR=34` / `W_LABEL=40`
  can't dominate.
- **`header_styles(headers, date_headers=(), center_headers=())`** extended:
  centers date columns AND any FY/numeric headers named in `center_headers`
  (text headers stay left). Module + function docstrings updated.

**Hard-coded sheet widths (the tabs that bypass `_widths.py`).**
- `summary_overview.py`  label col 34→**38** (program cols stay 24).
- `summary_inputs.py`    `[42,18,52]` → **`[38,18,44]`** (was too airy).
- `summary_sources.py`   `[26,96]` → **`[24,72]`** (96 was document-wide; long
  caveats now clip).
- `validation_tie_outs.py` (hidden) check-label col 40→**42**.
- `data_piid_worktype.py` flag cols `[13,14,15]` → **`[W_STATUS]*3`** (=15 each;
  added `W_STATUS` to the import). Standardizes Multi-source / Concentration /
  New 2nd source instead of special-casing the last.

**Header centering wired into the 5 dense-FY-grid sheets.** Each got a module-level
`_CENTER_HDRS` set (matching the existing `_DATE_HDRS` idiom) passed as
`center_headers`, handling the per-sheet FY-label prefix:
- `data_program.py`, `data_piid_worktype.py` — `set(VAL_LABELS)` (raw labels).
- `data_lane_detail.py` — `{f"$ {l}"} | {f"N {l}"}` over `VAL_LABELS`.
- `data_lane_vendor_fy.py` — `{f"$ {l}"} | {f"N {l}"}` over `FY_LABELS`.
- `data_role_detail.py` — `{f"$ {l}" for VAL_LABELS} | {"Records"}`.

## Verification

`build_workbook.py` + `validate_workbook.py`: **8 sheets, 14 native tables, 1 note
part, 0 xml errors, 0 error-literal cells.** Inspected the emitted sheet XML:

- **Cap working** — the 3 stacked coordinators (Indicators / Market Views / Detail
  Tables) all top out at **exactly 32.0**; the old 40/42-wide columns are clamped.
- **Standalone literals landed** — Summary `38/24`, Inputs `38/18/44`, Sources
  `24/72`, Checks `42/14`, Supplier Lanes flags `15/15/15`, FY grids at `10`($)/`8`(N).
- **Header alignment** — FY headers (`≤FY12`, `FY13`…`FY26`, `Total`, `$ FY13`,
  `N FY13`, `$ Total`) center; text headers (Program/PIID/Work Type/Builder/
  Multi-source) stay left; date headers (First Award) still center.

No tie-out re-run needed: width/alignment only, no formula/data touched. User does
the final visual Excel check per the standing no-render rule.

## Notes / easy follow-ups

- If the 15–16-col FY grids feel too wide in Excel, flip `W_FY = 9` (one line).
- Market Views §1 Program's first few FY columns are still widened by `merge_cols`
  (now capped at 32 instead of ballooning to 40–46) — reduced, not eliminated.

## Files

- **Edited:** `_widths.py` (constants + cap + `header_styles`), `summary_overview.py`,
  `summary_inputs.py`, `summary_sources.py`, `validation_tie_outs.py`,
  `data_piid_worktype.py`, `data_program.py`, `data_lane_detail.py`,
  `data_lane_vendor_fy.py`, `data_role_detail.py`.
