# 2026-06-06 — Submarine Technology-Insertion resolution + consolidated z_ChartData freshness audit

## Scope

Two pieces of work this session:

1. **Closed the deferred submarine "Technology Insertion" gap** flagged in
   `2026-06-06_cost_funnel_parity_and_deferred_sub_tech_insertion.md` — the ~$97.1M (0.9%)
   Virginia-class residual in the submarine "other non-BC" removal bar. Executed end-to-end
   (extraction → funnel CSV → workbook/deck surfacing → rebuild/validate).
2. **Audited the consolidated workbook's `z_ChartData`** (`projects/consolidated/workbook`)
   against the current DDG + submarine program data to confirm it reflects (a) this session's
   submarine fix and (b) the prior-session DDG cost-funnel rebase. **Result: already fully
   current — no consolidated changes were needed.**

---

## Part 1 — Submarine "Technology Insertion" resolution (DONE)

### What it was
"Technology Insertion" is a Virginia-class P-5c cost line that the submarine extractor never
captured. Since `Total = Σ(all P-5c lines)`, the uncaptured line was exactly the unreconciled
residual in "other non-BC" (Total − GFE − Basic Construction). Columbia already reconciled to $0
(it has no TI line). Classified **non-GFE** (kept `gfe_sum` = Propulsion+Electronics+Ordnance), so
the funnel bars and all hardcoded `_SUB_*` constants do **not** move — a completeness/audit fix,
not a numbers change.

### Changes
- **`projects/submarines/research/scripts/extract_scn_p5c_multi_vintage.py`**
  - Repointed off the dead `/Users/brendantoole/projects2/...` paths to `__file__`-relative
    `_HERE`/`_REPO` (input → `research_shared/budget_books`, output → `submarines/workbook/extracted`),
    mirroring the DDG pattern.
  - Added `"Technology Insertion"` to `CATEGORIES` (+ docstring). Parser/reconciler unchanged.
- **`projects/submarines/research/scripts/build_cost_funnel.py`**
  - Repointed `EXTRACTED` (`_HERE`/`_REPO`).
  - Added `"Technology Insertion"` to `P5C_CATEGORIES`; `ti = g_p5c("Technology Insertion")`;
    new `technology_insertion_$M` column in the wide CSV header + row (between `change_orders_$M`
    and `total_ship_estimate_$M`). **Did NOT** add `ti` to `gfe_parts` (keeps funnel bars fixed).
- **`projects/submarines/research/scripts/join_ffata_to_funnel.py`**
  - Repointed `EXTRACTED` only. Column passes through automatically (`dict(row)` + keys-derived
    `fieldnames`), so `cost_funnel_with_subawards.csv` gains the TI column with no further edit.
- **Surfaced it** (parity with last session's DDG HM&E itemization):
  - `projects/submarines/workbook/workbook_submarines/sheets/data_scn_budget.py` — added
    `"technology_insertion": "technology_insertion_$M"` to `metric_cols` and a
    `drow("Technology Insertion", "technology_insertion")` row in the SCN Budget sheet.
  - `projects/consolidated/deck/deck_consolidated/slides/s05_body_scope_cost_funnel.py` — card #2
    now names "plus Virginia technology insertion on the submarine side"; the `($2.18B DDG,
    $10.28B sub)` figures are **unchanged** (TI was already inside the $10.28B residual).

### Verification (all gates passed)
- Re-ran chain `extract → build_cost_funnel → join_ffata_to_funnel`.
- **No drift:** `scn_p5c_per_fy_reconciled.csv` minus the new TI rows is byte-identical to the
  pre-run backup; `cost_funnel_summary.csv` / `cost_funnel_with_subawards.csv` differ only by the
  new `technology_insertion_$M` column (total / gfe_sum / basic_construction unchanged).
- **Residual closes:** every Virginia and Columbia row reconciles to ~0.0000. Cumulative Virginia
  TI FY22–27 = **$97.132M** (15.398 + 15.706 + 16.020 + 16.340 + 16.667 + 17.001). Columbia has no
  TI line (unaffected).
- **Rebuilt + validated** submarine workbook (18 sheets; TI row + value `15.398` confirmed in the
  built `.xlsx` SCN Budget sheet), consolidated workbook, consolidated deck (24 slides). Clean.
  Backups removed.

Memory `ddg-sub-cost-funnel-parity` updated DEFERRED → RESOLVED.

---

## Part 2 — Consolidated `z_ChartData` freshness audit (verification only; NO changes)

### Question
The consolidated workbook (`projects/consolidated/workbook/.../sheets/z_chart_data.py`) is a
**hand-copied snapshot** of the two program workbooks' `z_ChartData` outputs (its docstring says
so: "intentionally not a model: every value below is hardcoded"). After the submarine TI fix and
the prior DDG rebase, is the snapshot stale?

### Method
- Recomputed the two **cost funnels** directly from the current extracted CSVs (FY22–27 cumulative).
- For the **model-derived** sections, read the **cached** resolved values from the program
  workbooks. (The program `z_ChartData` blocks are live Excel formulas → `model_*` sheets → CSVs;
  openpyxl alone shows only the formula string. The user re-opened/re-saved
  `projects/ddg/…DDG_vS.xlsx` and `projects/submarines/…Submarines_vS.xlsx` so Excel cached the
  computed values, which were then read with `openpyxl(..., data_only=True)`.)
- Reconciled all 10 consolidated sections against the resolved program values.

### Finding — every section already matches the current program output

| Consolidated section | Check | Result |
|---|---|---|
| §1 Exec TAM/SAM | DDG TAM 573.098 M/yr ÷1000 = 0.573098; Sub TAM Σ(annual)/6 = 3.306616; Broad SAM 2903.364+380.356 = 3283.721 ÷1000 | ✅ exact |
| §2 DDG cost funnel | DDG `cost_funnel_summary.csv` FY22–27 cum: 29936.605 / 10289.934(GFE=elec+ord) / 17470.983(BC) | ✅ exact |
| §3 Sub cost funnel | submarine `cost_funnel_with_subawards.csv` FY22–27 cum: 83790.155 / 16863.106 / 56646.727 (TI fix did not move it) | ✅ exact |
| §4 DDG TAM bridge | DDG §4 avg-annual × 6: BC 2911.83→17470.983; non-supplier −2546.498→−15278.990; AP/LLTM 207.765→1246.592 | ✅ exact |
| §5 Sub TAM bridge | BC 56646.727; supplier TAM Σ(annual)=19839.693; AP/LLTM additive base = 0.0 | ✅ exact |
| §6 Supplier-share % | DDG outside-yards corrected 0.32839 / disclosed 0.73644 / applied BC 0.12546; Sub POP 0.51756 / AP-LLTM 0.48486 / applied BC 0.35024 | ✅ exact |
| §7 Annual cadence | DDG per-FY (BC+AP/LLTM)/1000 = [.2459,.5719,.4169,.6373,1.2255,.3412]; Sub TAM row /1000 = [1.6665,1.7846,5.4030,1.8655,3.6062,5.5138] | ✅ exact |
| §8 Work-type | Sub §5 buckets + DDG §6 buckets (incl. DDG **Castings** 9.694, col J); residual = combined TAM − broad SAM | ✅ exact |
| §9 SAM scenarios | broad 3.28372; HM&E 2027.21+324.19=2.3514; elec 1229.77+32.98=1.26275; metal 808.32+266.58=1.0749; modular 374.81+6.67=0.38148 | ✅ exact |
| §10 Supplier visibility | DDG `_load_ffata()` (all LI-2122 rows, `ffata_visible_yards`/`bc_outsourced_*`): 2728.6/11311.4/13573.7/16159.2; Sub visible flow 5451.121335849999 (`SAM Build!C37`, `Entity Master!C8`, `Figure Register!E24`) | ✅ exact |

### Why it was already current
The prior-session log already records updating the consolidated workbook for DDG:
> "Consolidated workbook `z_chart_data.py`: `_DDG_COST_FUNNEL_B = [29.936605, -10.289934,
> -2.175688, "e"]`; §2/§3 paste-block labels standardized." … "Builds clean: … consolidated
> workbook … **No downstream hardcoded values changed** because Total/BC/GFE did not move."

So the DDG rebase was propagated at the time, and because it didn't move Total/BC/GFE the other
sections stayed correct. This session's submarine TI fix is non-GFE and numerically inert, so it
required no consolidated change. **Net: the consolidated `z_ChartData` reflects all current program
data; nothing was edited in `projects/consolidated/workbook`.**

### Note for next time
The consolidated workbook stays a manual snapshot (by design / user preference: centralized
literals, not auto-derived). To re-confirm freshness after future program changes, re-open/save
the two program workbooks and diff their resolved `z_ChartData` values against the consolidated
literals (the §-by-§ table above is the reference). A repeatable `reconcile_vs_programs.py` was
discussed but not built (left to the user's discretion).

---

## Files

### Part 1 — edited
| File | Change |
|---|---|
| `projects/submarines/research/scripts/extract_scn_p5c_multi_vintage.py` | repoint + add `Technology Insertion` to CATEGORIES |
| `projects/submarines/research/scripts/build_cost_funnel.py` | repoint + `technology_insertion_$M` column (kept out of `gfe_parts`) |
| `projects/submarines/research/scripts/join_ffata_to_funnel.py` | repoint only |
| `projects/submarines/workbook/workbook_submarines/sheets/data_scn_budget.py` | TI metric + SCN Budget row |
| `projects/consolidated/deck/deck_consolidated/slides/s05_body_scope_cost_funnel.py` | card #2 names TI (figures unchanged) |
| (regenerated) `projects/submarines/workbook/extracted/cost_funnel_*.csv` | new TI column; Virginia residual → ~0 |

### Part 2 — read/verified only (no edits)
| File | Role |
|---|---|
| `projects/consolidated/workbook/workbook_consolidated/sheets/z_chart_data.py` | snapshot under audit — confirmed current, unchanged |
| `projects/{ddg,submarines}/2026*_vS.xlsx` | re-saved by user; cached `z_ChartData` read for reconciliation |
| `projects/{ddg,submarines}/workbook/.../sheets/chartdata_z_chart_data.py` | source derivation reference |
