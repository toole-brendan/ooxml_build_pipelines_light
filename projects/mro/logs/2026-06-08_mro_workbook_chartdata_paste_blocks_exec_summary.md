# 2026-06-08 — MRO workbook: source-idiom cleanup (z_ChartData paste blocks, Executive Summary, label fixes)

## Scope

Post-native-rewrite **source-idiom alignment** pass on the MRO workbook
(`projects/mro/workbook/workbook_mro/sheets/`), bringing the *reader tab*, the
*chart-data tab*, and a set of *placeholder / content-drift labels* into the gold
`workbook_ddg` / `workbook_submarines` idiom. (The model/data sheets were already
aligned by the prior 06-08 styling passes; this pass closes the remaining gaps.)
User chose, via AskUserQuestion: **faithful gold paste rectangles** for chartdata
(drop analytical ref rows) and **add a real Executive Summary** tab.

Build green: `build_workbook.py` → **19 sheets**, **0 defined names**, 8 native tables;
`qa/verify_crosstab.py` → OK (4,290 formulas); `qa/tie_out.py compare … --tol 1.0`
→ **Invariant B (86 figures) + Invariant A (engine multiset) both match**.

## Two load-bearing findings that shaped the plan

- **"Marauder" is real, not a placeholder.** It's load-bearing across the *deck*
  (slide titles "Marauder-Like Fleet MRO", the SAM definition "Depot Ship Repair spend
  on Marauder-type platforms", a 14-hull / 3-tier comp-set worth $758M in
  `deck_mro/slides/fleet_mro.py` + `fleet_structure.py`). Renaming would desync the
  workbook from the deck → **kept the term, added a one-line definition** in Methodology.
- **The deck does NOT read the workbook programmatically** (no `xlsx`/`openpyxl`/
  `load_workbook` anywhere in `mro/deck`; the deck's think-cell charts were transcribed
  statically). So `z_ChartData` is a **human copy-paste support tab**, not a live deck
  input. That means the waterfall-shape question is moot per the user's own fallback:
  can't confirm a loader accepts the gold "e"-in-row pattern → **kept the explicit
  "Bar type" (s/d/e) row** and just added the paste perimeter styling.

## Part 1 — value-neutral fixes (no `regen-baseline`; B+A stayed green)

- **65-vs-68 PSC drift fixed.** `_crosstab.PSC_ROWS == 65` (verified). `validation_scope_
  reconciliation.py` said "68 PSCs" / "68 J/K/N/M/H/L codes" in 3 places (§7.1, §8 BAR 8,
  the bar map) → all corrected to 65. Everywhere else already said 65.
- **`BuildCo` placeholder removed.** `guide_methodology.py` §1 ("MRO a private competitor
  like BuildCo could win" → "MRO a private yard / competitor could win") and the
  (unrendered) `model_reconciliation.py` HII svc-mix note ("…public comp to BuildCo…" →
  "…public comp…"). No other live occurrences in source (the qa/*/probe BuildCo hits are
  stale snapshot artifacts).
- **Marauder definition added** to Methodology §1: `("Marauder-like fleet", "the 14-hull
  comp-set (auxiliary / patrol / logistics) used as the SAM target fleet")` and the SAM
  definition extended to name it.
- **Dead `scenario` lever removed** from `inputs_assumptions.py`. `scenario_cell` was
  exported but **consumed nowhere** (only WPN/FMS plugs feed the model). Removed the
  "Sizing scenario" row, `_SCENARIOS`, the scenario dropdown data-validation, the now-unused
  `_dv_list` helper, the accessor + its module-level export, and the docstring mentions.
- **HII segment label fix.** Figure Register DO-14/15/16 said "HII **Marine** Technologies"
  — HII's actual segment (and the Reconciliation source) is "**Mission** Technologies"
  (no "Marine Technologies" segment exists). Fixed the 3 labels.

## Part 2 — Executive Summary + Verification Answers move

- **New `summary_executive_summary.py`** (first tab, summary group): a pure reader page,
  every $ cell a green `=accessor()` link, no recompute. §1 Headline TAM (reconciled TAM,
  Navy/USCG services-MRO, embedded PSC 1905, private-addressable bottom-up/top-down),
  §2 Reconciliation bridge (top-down / bottom-up / public-NSY / gap), §3 Private-addressable
  convergence (A / B / delta). Modeled on the gold `summary_executive_summary.py`. SAM has
  no producer accessor (it's computed only in chartdata) → intentionally omitted.
- **Verification Answers moved summary → validation.** `_GROUP` "summary"→"validation",
  file renamed `summary_verification_answers.py` → `validation_verification_answers.py`
  (matches the `<group>_<name>.py` convention). `sheets/__init__.py` rewired: summary block =
  [Executive Summary]; validation block = [Verification Answers, Scope Reconciliation].
  Group-block contiguity assertion passes.
- These are multiset-neutral: Invariant A is the explicit 9-tab `_ENGINE_TABS` tuple (neither
  summary tab is in it), so adding/moving link-only tabs doesn't touch the multiset, and B
  hosts no names on these tabs. Verified: B+A green with **no regen** after Parts 1+2.

## Part 3 — chartdata rewrite (faithful gold paste rectangles) → regen-baseline

- **Tab renamed `Output` → `z_ChartData`** (`_TAB`; module/export kept as
  `chartdata_output.py` / `OUTPUT` for compat per the user). Updated `qa/tie_out.py`
  `_ENGINE_TABS` `"Output"` → `"z_ChartData"` (else Invariant A loses the tab).
- **Ported `_paste_block()` + `S_PASTE_*`** from `workbook_ddg/sheets/chartdata_z_chart_data.py`.
  Generalized it to accept a **per-row `unit` list** (so the mixed $M/% HII block works):
  banner + blank + bordered grid (S_PASTE_HEADER_* top row, S_PASTE_LABEL_* left col,
  S_PASTE_VAL_*_{INT,R,B,BR} interior/right/bottom/corner) + blank(2). Routed **every** block
  through it → the thin-black perimeter + pale-yellow fill (`FFFFFACD`) now present
  (the missing right-edge borders the user flagged). Verified in the built xlsx: §1 header
  top='thin', value cells right='thin', last cell right+bottom='thin'.
- **Dropped analytical ref rows/cols** to make clean rectangles: in-block `c.total()` totals
  (§1/§4/§8/§9/§12), cumulative-% rows (§8/§9), the "% of TAM (ref)" columns (§1/§5), the
  "Tier (ref)" annotation row (§4), the SAM "Narrowing path" subsection (§5), the "FDNF flag"
  row + the entire §9-secondary prime×RMC crosstab (no `[chart_key]`, analyst-only). §3 "Total"
  column dropped; "Other" recomputed inline (`seg_total - SUM(hulls) - Uncl`) via a **callable
  value** resolved against its row (RowCursor `_resolve`), since `_paste_block` doesn't expose
  row numbers. `[chart_key]` banner tags kept.
- **§10 HII Financials wired to real cells.** Was a values-less stub (metric names only).
  Now FY2025 column: Revenue=`hii_mt_rev_cell()` (3044), Operating Income=`hii_mt_oi_cell()`
  (153), Operating Margin=`IFERROR(oi/rev,0)`. FY23/FY24 dropped — **not in the model** (only
  FY25 HII anchors exist on Reconciliation).
- **Waterfalls (§11/§13) keep the explicit "Bar type" (s/d/e) row** inside the bordered
  rectangle (deck-loader fallback, see findings).

### regen-baseline (the sanctioned path for an intentional engine change)

Dropping ref rows + reshaping §12 (% → $M) changes the `z_ChartData` numeric cells, and
chartdata **is** an engine tab → Invariant A's multiset changes (this is the first 06-08 pass
to cross that line; prior passes held chartdata to text-only precisely to avoid it).

1. `compare` (pre-regen): **20 discrepancies, ALL Invariant A** (`count 6432→6260`; vanished
   values = the dropped small-decimal %s; new values = `153`/`3044` HII now real, `2392.19`
   etc. = §12 now $M). **Zero Invariant-B discrepancies** → no producer figure moved; change
   is isolated to chartdata.
2. `regen-baseline` → `REGEN OK — Invariant B holds for 86 figures; engine_multiset written
   (6260 values)`. **`defined_names` sha256 unchanged before/after (`ea6dfef8c6dc5bf1`, 88
   names)** — the anti-laundering freeze held; only `engine_multiset` was rewritten.
3. Final `compare`: **B + A both green.**

## Verification (final, all green)

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py            # 19 sheets, 0 defined names, 8 native tables
/usr/bin/python3 qa/verify_crosstab.py        # CROSSTAB VERIFY OK (4,290 formulas)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0
# -> Invariant B: 86 figures match; Invariant A: engine multiset matches
```
Tab order: Executive Summary · Methodology · Assumptions · [7 model] · [3 data] ·
Figure Register · Verification Answers · Scope Reconciliation · Source Index · References ·
z_ChartData. `defined names: 0`. `py_compile` clean; AST unused-import check clean.

## Files

- **Added:** `summary_executive_summary.py`.
- **Renamed:** `summary_verification_answers.py` → `validation_verification_answers.py`
  (`_GROUP` → "validation").
- **Rewritten:** `chartdata_output.py` (z_ChartData + `_paste_block` + faithful rectangles +
  HII wiring).
- **Edited:** `inputs_assumptions.py` (scenario lever removed), `guide_methodology.py`
  (BuildCo + Marauder def), `model_reconciliation.py` (BuildCo note),
  `validation_scope_reconciliation.py` (68→65), `outputs_figure_register.py`
  (Marine→Mission), `sheets/__init__.py` (registry), `qa/tie_out.py` (`_ENGINE_TABS` tab name).
- **Regenerated:** `qa/gold/baseline.json` `engine_multiset` (6432→6260); `defined_names`
  block untouched (frozen `ea6dfef8…`).

## Deliberately NOT done

- **Figure Register defined names** (the user's optional item 6). DDG's register declares
  ~10 deck names via `defined_names=`; MRO's tie-out **hard-fails on any added defined name**
  (the zero-names invariant the whole native rewrite established). Since the deck doesn't read
  the workbook, deck-compat defined names buy nothing — skipped rather than unwind the invariant.
- **`qa/*/probe/13_Output.json`** stale snapshots still say "Output" — they are standalone
  diagnostic dumps (no qa script or build reads them), not a gate. Left as-is; regenerate the
  probe set if a fresh diagnostic dump is wanted.
- chartdata `z_ChartData` module/export kept as `chartdata_output.py` / `OUTPUT` (not renamed
  to the gold `chartdata_z_chart_data.py` / `CHART_DATA`) — user-sanctioned compat; only the
  visible tab name was changed.
```
