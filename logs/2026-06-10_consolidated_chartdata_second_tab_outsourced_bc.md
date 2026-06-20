# 2026-06-10 — Consolidated workbook: split the Outsourced BC chart data to a second paste-only tab

## Problem / goal

The consolidated workbook's single `z_ChartData` tab had grown §11–§15 (the
2026-06-09 sessions' blocks behind the three Outsourced BC front-row slides:
walk, annual TAM outlook + penetration + avg line, work type by program). User
asked to (1) move those blocks to a **second sheet** and restart the numbering
at §1, and (2) make the new tab strictly **paste-ready**: one table per
think-cell chart, no extra/memo blocks — the §11 walk block carried BOTH
programs' waterfalls in one table ("difficult to just copy and paste what I
need, which is the whole goal of these sheets").

## Changes

### NEW `workbook_consolidated/sheets/z_chart_data_outsourced_bc.py` → tab "z_ChartData_OutsourcedBC"
Second chartdata-group sheet, registered right after `z_chart_data` in
`sheets/__init__.py` (group contiguity holds). One paste rectangle per chart,
in slide order:

| New § | Was | Content |
|---|---|---|
| §1 | §11 row 1 | DDG outsourced BC walk (waterfall, 1 row, "e" markers) |
| §2 | §11 row 2 | Submarine outsourced BC walk (waterfall; Prime AP/LLTM step blank) |
| §3 | §15 | Outsourced BC by work type (per program, stacked column) |
| §4 | §12 | Annual TAM with outlook (5 series × FY22–31) |
| §5 | §14 | FY22–25 avg reference line — **Combined value only** (per-program averages render in the program workbooks' chartdata) |
| §6 | §13 rows 1–3 | DDG penetration strip (Actual / Assumed low / Assumed high) |
| §7 | §13 rows 4–6 | Submarine penetration strip |

- **§11b "walk components" memo DELETED** (backed no chart = "extra stuff");
  the composition stays as a code comment, and component provenance lives in
  the program workbooks (SCN Budget / OBBBA Mandatory / TAM Build).
- Walk split mirrors the §2/§3 funnel convention on tab 1 (per-program
  waterfall tables, steps as columns, one unlabeled row).
- Shared series are **imported from `.z_chart_data`** so the tabs can't drift:
  `_FY_HDR`, `_DDG_ANNUAL_TAM_B`, `_SUB_ANNUAL_TAM_B` (§4 actuals = tab 1 §7),
  `_WORKTYPE_HDR` (§3 bucket order = tab 1 §8). Cursor/paste-block emitter is a
  local copy (house "snippets stay copy-from" principle), `_NCOLS = 11`.

### EDIT `sheets/z_chart_data.py`
Removed the §11–§15 blocks + their module constants; docstring now maps §1–§10
and points at the second tab; `_NCOLS` 11 → 9 (widest block is now §8); notes
added where the shared constants are exported.

### EDIT deck sync pointers (comments/docstrings only, no build-output change)
- `s03_body_outsourced_bc_overview.py`: → "z_ChartData_OutsourcedBC §1-§2".
- `s03b_body_worktype_by_program.py`: "z_ChartData §15" → "z_ChartData_OutsourcedBC §3" (×3).
- `s11a_body_outsourced_bc_annual_tam.py`: "§12/§13/§14" → "§4 (bars), §6-§7 (penetration), §5 (avg)".

## Verification

- Build: 2 sheets (`z_ChartData`, `z_ChartData_OutsourcedBC`); validate: 0 xml
  errors, 0 error-literal cells.
- openpyxl content dump: tab 1 ends at §10; tab 2 carries §1–§7 in slide order.
  Walk rows keep the "e" markers and the submarine blank step; §3 columns sum
  exactly to the walk endpoints (3.95128 / 21.212173); §4 implied-low values sit
  in FY2028–31 columns only; §5 = 3.307667 (= 0.491491 + 2.816177); penetration
  actuals FY22–27 / assumed FY28–31 land in the right columns.
- `ast.parse` clean on the three touched slide modules (comment-only edits;
  deck not rebuilt).

## Gotchas / notes

- **Chartdata tabs are paste-only**: one bordered rectangle per think-cell
  chart/element, slide order, no memo/"considered & excluded"/components
  blocks. A multi-chart exhibit (e.g. two waterfalls on one slide) gets one
  table PER CHART, not one per slide.
- The walk endpoint identity (work-type columns sum to the per-program walk
  endpoints) survived the split — §3 and §1/§2 now live on the same tab.
- Program workbooks' chartdata tabs (DDG/subs §10–§12 outlook blocks) were NOT
  restructured — consolidated only, per the ask. If the paste-only/one-table-
  per-chart rule should apply there too, that's a separate pass.
