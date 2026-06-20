# 2026-06-06 — Slide-05 cost-funnel standardization, DDG extraction parity, and the deferred submarine Technology-Insertion gap

## Scope

Standardized the consolidated deck's **slide 05 ("Scope and Cost Funnel")** so both
programs read on the **same FY2022–FY2027 cumulative portfolio basis** (DDG was FY2024
illustrative; submarine was already FY22–27). The user asked that the DDG *workbook*
show the calculation (not just hardcode it in the deck), and that the removal bars
clarify what they contain. Investigating the second ask surfaced a real data issue —
the DDG "other non-BC" bar carried a **$459.8M (21%) unexplained residual** — which we
traced to an **extraction asymmetry** (DDG was single-vintage, submarines multi-vintage)
and fixed at the root. A smaller **$97.1M (0.9%) submarine residual** was identified and
**deferred** (the user asked to do it after); this log explains exactly how to close it.

Everything below is committed/working as of this session **except** the deferred
submarine fix, which is the back half of this log.

---

## What was done this session (DONE — for context)

**Root fix — DDG extraction made multi-vintage.** The DDG P-5c cost categories are now
extracted from all six SCN books (FY22–FY27) and reconciled per (FY, category) to the
most-recent settled vintage (PB year ≥ FY+2, else most-recent), matching the submarine
methodology. This backfilled the pre-FY24 HM&E that the FY27-only extraction had folded
into the residual: **FY2022 HM&E = $164.030M (PB2023), FY2023 HM&E = $295.732M (PB2025)**,
sum $459.762M = the residual, which now closes to **$0.000**.

- `projects/ddg/research/scripts/extract_scn_destroyer_lines.py` — multi-vintage loop +
  `detect_pb_year` + `reconcile()`; repointed off the dead `projects2/...` path to
  `research_shared/budget_books` (in) and `ddg/workbook/extracted` (out), `__file__`-relative.
  P-40 resource summary / P-27 schedule still taken from the latest book only (byte-identical).
- `projects/ddg/research/scripts/build_cost_funnel.py` — repointed `EXTRACTED`; docstring
  de-staled. Re-ran → `cost_funnel_summary.csv` diff shows **only** FY2022/FY2023 `hme_$M`
  populated and the "HM&E missing" flags cleared; Total/BC/GFE and all other columns identical.
- `data_scn_budget.py` — added a **§3 Portfolio cost funnel (FY2022–FY2027 cumulative)**
  block (live `SUM(C:H)` of the §1 annual rows) and a `portfolio_scn_cell(metric)` accessor.
  Verified (incl. independent recalc via the `formulas` lib): Total **$29,936.605M**, GFE
  **$10,289.934M**, other non-BC **$2,175.688M**, Basic Construction **$17,470.983M**.
- `chartdata_z_chart_data.py` §1 and `outputs_figure_register.py` slide-5 rows repointed to
  `portfolio_scn_cell`; source-index/reference counts refreshed.
- Consolidated workbook `z_chart_data.py`: `_DDG_COST_FUNNEL_B = [29.936605, -10.289934,
  -2.175688, "e"]`; §2/§3 paste-block labels standardized.
- Consolidated deck `s05_body_scope_cost_funnel.py`: sources/units/chips/steps/ticks updated
  to FY22–27 cumulative; bars use generic buckets ("Less GFE / directed equipment", "Less
  other non-BC categories") with full per-program composition in interpretation card #2.
- Builds clean: DDG workbook (0 XML errors, 0 error cells), consolidated workbook, consolidated
  deck (24 slides). **No downstream hardcoded values changed** because Total/BC/GFE did not move.

---

## DEFERRED — Submarine "Technology Insertion" gap (~$97.1M, 0.9%)

### What it is (confirmed)

The submarine "other non-BC" removal bar reconciles to its named components on Columbia
but not on Virginia:

| Program | other non-BC (Total−GFE−BC) | plans + CO + HM&E + other | residual |
|---|---|---|---|
| Columbia (LI 1045) | $4,442.259M | $4,442.259M | **$0.000** |
| Virginia (LI 2013) | $5,838.063M | $5,740.931M | **$97.132M** |

The residual is **entirely Virginia-class** and is the **"Technology Insertion"** P-5c
cost line. This is a deduction, not a guess: every other Virginia P-5c line (Plan Costs,
Basic Construction/Conversion, Change Orders, Electronics, Propulsion Equipment, HM&E,
Ordnance, Other Cost, Total) **is** captured, and "Technology Insertion" is the only one
**not** in the extractor's `CATEGORIES`. Since `Total = Σ(all P-5c lines)`, the uncaptured
line is exactly the residual. "Technology Insertion" appears in every book (FY22–FY27);
e.g. `SCN_Book_FY22.txt:4933` `Technology Insertion  73.500  28.835  13.535  …`.

### Important: this does NOT change the funnel numbers

The submarine funnel bar **other non-BC = $10.28B already includes** Technology Insertion
(it is computed as the residual `Total − GFE − Basic Construction`). So `_SUB_COST_FUNNEL_B`
in the consolidated workbook and `_SUB_STEPS` in slide 05 are **already numerically correct**.
The only thing broken is the **named component-level audit** (the parts don't sum to the
whole). Closing it is a **completeness / auditability** fix, not a numbers change —
**provided Technology Insertion is classified as non-GFE** (see the decision below).

### The one decision that sets the blast radius

**Where does Technology Insertion belong — "other non-BC" or "GFE"?**

- **Recommended: "other non-BC" (non-GFE).** It is currently *implicitly* in the
  other-non-BC residual, and the submarine `gfe_sum` is defined as Propulsion + Electronics
  + Ordnance only. Keeping Technology Insertion out of `gfe_sum` means **GFE, Basic
  Construction, and the funnel bars do not move** → zero downstream ripple. The fix simply
  makes the named breakdown reconcile (and lets card #2 list "technology insertion" under
  the submarine other-non-BC bucket). **Do this unless there's a reason not to.**
- **Alternative: "GFE".** Only if Technology Insertion is judged government-furnished.
  Then `gfe_sum` rises ~$97M, other-non-BC falls ~$97M, and the submarine funnel bars
  change → you MUST also update the hardcoded `_SUB_COST_FUNNEL_B` (consolidated workbook
  `z_chart_data.py`) and `_SUB_STEPS` (slide 05) and card #2, then rebuild/re-validate.
  Higher risk; not recommended without justification.

### Steps to resolve (assuming the recommended non-GFE classification)

All three submarine research scripts still point at the **deleted** `/Users/brendantoole/
projects2/submarine_outsourced_work/...` paths (same staleness the DDG scripts had), so
repointing is part of the fix — mirror the DDG `__file__`-relative pattern.

1. **Repoint paths** (in → `projects/research_shared/budget_books`; out → `projects/
   submarines/workbook/extracted`), `__file__`-relative, in all three:
   - `extract_scn_p5c_multi_vintage.py` (`BOOKS_DIR`, `OUT` — lines 24–25)
   - `build_cost_funnel.py` (`EXTRACTED` — line 41)
   - `join_ffata_to_funnel.py` (`EXTRACTED` — line 30)
   (Confirm these scripts still produce byte-identical non-TI output before/after, the same
   way the DDG run did, so the repoint alone introduces no drift.)

2. **Capture the category in the extractor**
   `projects/submarines/research/scripts/extract_scn_p5c_multi_vintage.py`
   - Add `"Technology Insertion"` to `CATEGORIES` (lines 34–44) and mention it in the
     docstring category list (line 11). No other parser change needed — the same
     token-split + multi-vintage reconciliation handles it.

3. **Add the column in the funnel builder**
   `projects/submarines/research/scripts/build_cost_funnel.py`
   - Add `"Technology Insertion"` to `P5C_CATEGORIES` (line ~55).
   - Add `ti = g_p5c("Technology Insertion")` alongside the other `g_p5c(...)` reads (~line 244).
   - Add a `technology_insertion_$M` column to the wide-CSV header (~line 213, near the
     other category columns) and write `fmt(ti)` in the row.
   - **Do NOT add `ti` to `gfe_parts`** (keep `gfe_sum = Propulsion + Electronics +
     Ordnance`) — this is what keeps the funnel bars unchanged.

4. **Re-run the chain** (order matters):
   `extract_scn_p5c_multi_vintage.py` → `build_cost_funnel.py` → `join_ffata_to_funnel.py`
   (the last writes `cost_funnel_with_subawards.csv`, the file the submarine workbook reads).

5. **Verify** (gate):
   - Diff `cost_funnel_with_subawards.csv`: a new `technology_insertion_$M` column populated
     for Virginia (LI 2013); `total_ship_estimate_$M`, `gfe_sum_$M`, `basic_construction_$M`
     **unchanged**.
   - Recompute the residual: `other_non_bc − (plans + CO + HM&E + other + technology_insertion)`
     → **~$0** for Virginia (i.e., reconciled Virginia Technology Insertion FY22–27 ≈ $97.132M,
     which confirms the diagnosis).

6. **Optional — surface it (parity with DDG's HM&E itemization):**
   - `projects/submarines/workbook/workbook_submarines/sheets/data_scn_budget.py` reads
     `cost_funnel_with_subawards` (line 42) into a fixed `metric_cols` map — add a
     `"technology_insertion"` entry + a row in the SCN Budget sheet if you want it visible
     there. Otherwise the column simply sits in the CSV for audit.
   - Consolidated deck `s05` card #2: add "technology insertion" to the submarine
     other-non-BC enumeration.

7. **Rebuild + validate** the submarine workbook, consolidated workbook, and consolidated
   deck. With the recommended non-GFE classification, the funnel bars and all hardcoded
   `_SUB_*` constants are unchanged, so this is a clean rebuild (no value edits).

### Files (deferred work)

| Purpose | File |
|---|---|
| Sub multi-vintage extractor (add category, repoint) | `projects/submarines/research/scripts/extract_scn_p5c_multi_vintage.py` |
| Sub funnel builder (add column, repoint, keep GFE def) | `projects/submarines/research/scripts/build_cost_funnel.py` |
| Sub FFATA join (repoint; produces workbook CSV) | `projects/submarines/research/scripts/join_ffata_to_funnel.py` |
| Workbook-read funnel CSV | `projects/submarines/workbook/extracted/cost_funnel_with_subawards.csv` |
| Optional surface in workbook | `projects/submarines/workbook/workbook_submarines/sheets/data_scn_budget.py` |
| Optional card text | `projects/consolidated/deck/deck_consolidated/slides/s05_body_scope_cost_funnel.py` |
| Source books | `projects/research_shared/budget_books/SCN_Book_FY{22..27}.txt` |
