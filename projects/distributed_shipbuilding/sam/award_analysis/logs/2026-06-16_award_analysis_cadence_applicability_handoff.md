# 2026-06-16 — Award Analysis: cadence-applicability refactor (SESSION LOG + HANDOFF)

**STATUS: implementation COMPLETE, build green. External review of THIS implementation is
in progress — STANDBY. Do not start further refinements of the updated workbook until the
review notes come back.** When they arrive, treat them the way §7 of the prior handoff
described: reconcile each note against the verified facts below before acting.

This session resolved the open §5 methodology issue from the prior handoff
(`logs/2026-06-16_award_analysis_award_wave_refactor_handoff.md`) by implementing the external
reviewer's recommendations (the review the user pasted in). The approved plan is at
`~/.claude/plans/here-is-the-review-majestic-frog.md`.

Pipeline: `projects/distributed_shipbuilding/`. Build env: `python3.12` only.
Run order: `extract_workbook_cuts.py` → `compute_jumpball_signals.py` → `build_workbook.py`
→ `validate_workbook.py` (build/validate from the OUTER `workbook_award_analysis/`).

## 0. The problem this session solved

90-day single-linkage clustering chains continuously-active lanes into multi-year "mega-waves,"
so the derived cadence / next-expected / timing-due signal was an artifact for those lanes (prior
handoff §5). Resolution (reviewer + user-confirmed): **split multi-source lanes into PERIODIC
re-buy lanes (get a dated next-wave WINDOW) and CONTINUOUS / always-on lanes (no dated forecast;
pursued as supplier-access openings)**, with the periodic/continuous verdict computed LIVE in the
workbook from blue shape metrics + new adjustable Assumptions controls.

## 1. User-confirmed forks (via AskUserQuestion)

- Forecast = **expected WINDOW (start–end)**, not a point date.
- Continuous lanes get a **dedicated "Continuous Sourcing" tab**.
- Wave share = **positive-gross allocation** (net kept as the tie-out basis).
- House-rule call (not a fork): shape metrics are blue leaf data, but the verdicts
  (`Sourcing mode`, `Cadence applicable`, `Cadence confidence`, the forecast window, due /
  always-on flags) are **LIVE formulas** over new **Assumptions §2b** controls — mirroring the
  existing `Re-buy eligible` / `Timing due` pattern. No baked-in CSV verdicts.

## 2. What was implemented

### Compute (`research/scripts/compute_jumpball_signals.py`)
All derived from the SAME single `build_waves()` pass (no re-clustering). New columns:
- `wb_lane_signals.csv`: `max_wave_duration_days`, `median_wave_duration_days`,
  `median_quiet_gap_days` (true end-to-start lull; distinct from the kept anchor-to-anchor
  `median_wave_gap_days`), `n_quiet_gaps`, `max_wave_duration_to_gap_ratio`, `active_months_frac`;
  trailing-activity snapshots at the fixed `AS_OF = 2026-05-22`: `dollars_last180_m`,
  `records_last180`, `dollars_last365_m`, `records_last365`, `days_since_last_award`,
  `vendor_adds_last365`.
- `wb_award_waves.csv`: `wave_dollars_positive_m`. `wb_wave_vendors.csv`:
  `wave_vendor_dollars_positive_m`. (Net columns unchanged — tie-outs stay net.)

### Workbook
- **Assumptions §2b (NEW, `summary_inputs.py`)**: live controls + `input_*_cell()` accessors —
  Periodic max wave duration (365), Span/cadence ratio cap (1.25), Strong-periodic min waves (3),
  Strong-periodic gap-CV cap (0.60), Always-on materiality recent $M (50).
- **Re-buy Timing (`model_rebuy_timing.py`, 24 cols)**: blue Gap CV / Longest span / Median span /
  Median quiet gap; live Span/cadence ratio, **Sourcing mode**, **Cadence applicable**,
  **Cadence confidence**, **Forecast start/end** (= Last award + median quiet gap, + median wave
  span), **Timing due** (now requires cadence-applicable AND window-overlaps-horizon), Re-buy due,
  and a **Date-only signal** diagnostic (naive point-date-in-horizon). `rb_due_count` →
  periodic-due (col X); `rb_timing_due_count` → Date-only (col Y).
- **Continuous Sourcing (`model_continuous_sourcing.py`, NEW tab, 22 cols)**: per-lane activity +
  contestability (recent $, active vendors, top-1/others, prior top-1, top-1 trend, last 180/365d
  $ + records, days-since, vendor adds, capability coherence) + live Sourcing mode +
  **Always-on opening** flag = eligible AND mode=Continuous AND recent$≥materiality. Accessor
  `cont_opening_count`. Registered in the model group after Wave Cadence (sheet 6).
- **Wave Cadence (`model_wave_cadence.py`, 23 cols)**: added blue Longest/Median span, Median
  quiet gap, Active months %; live Span/median gap, Cadence applicable, Sourcing mode, Cadence
  confidence. Docstring tightened.
- **Award Waves (`data_award_waves.py`)**: added blue `Wave $M (gross+)`, live `Top-1 (gross+)`
  and live `Wave type` (Clean / Extended / Continuous episode / Correction-only). Net Top-1 kept.
- **Wave Vendors (`data_wave_vendors.py`)**: added `Wave $M (gross+)`; repointed `Wave share` to
  positive-gross floored at 0 — `=IF(SUMIFS(gross,…)<=0,0,MAX(0,MIN(vendor_gross/wave_gross,1)))`.
  Fixes the 43 negative shares. `wv_cols()` now also exposes `gross`.
- **Summary §4 (`summary_overview.py`)**: split into **Periodic re-buy openings due** /
  **Continuous multi-source openings** / **Timing signal due (date only, diagnostic)**.
- Plumbing: `_tabs.py` (+`TAB_CONTINUOUS_SOURCING`), `__init__.py` (registered), `_widths.py`
  (+`W_MODE`/`W_RATIO`/`W_DAYS`), `summary_sources.py` (added the two wave CSVs + generator note).
  `validation_tie_outs.py` UNCHANGED — tie-outs stay on net $ (positive-gross is display-only).

### Docs
- `doc/.../pages/rebuy_methodology_explainer.py`: rewrote the cadence section (periodic-vs-
  continuous gate, window forecast, continuous lanes routed to Continuous Sourcing); dropped all
  "recompete" wording. Builds green (`doc/build_doc.py`).
- **Deleted** `methodology_jump_balls_20260615.md` (user: superseded). See §5 for the dangling ref.

## 3. Verification that PASSED (re-runnable; see §6)

- Build: **22 sheets, 18 native tables, 67 parts, 0 xml errors, 0 error-literal cells.**
- Built XML: 0 "recompete"/"clump"/"buy burst"; new terms present; positive-gross floor
  `MAX(0,MIN(` present; no `#REF`/`#NAME`/`#VALUE`.
- **Tie-outs hold** (recomputed from CSVs; user verifies formula evaluation in Excel per the
  no-headless-recalc rule): records EXACT virginia **7,725** / columbia **5,281** / ddg **5,741**;
  positive-gross wave-vendor shares all in [0,1]; 132 lanes / 572 waves / 3,595 wave-vendor rows.
- **Counts recomputed from CSVs** (as-of 2026-05-22, horizon 12mo, multi-min 2, cutoff 0.75,
  periodic-max 365, ratio-cap 1.25), mirroring the exact live formula logic:
  - **Periodic re-buy due = 4 / $621.5M** (virginia 2, columbia 0, ddg 2)
  - **Continuous openings = 18 / $3,833.6M** (virginia 6, columbia 6, ddg 6)
  - **Date-only signal = 20 / $2,622.0M**
  - Sourcing-mode distribution over 132 lanes: 55 Periodic / 58 Continuous / 14 Weak / 5 Sparse.
  - Columbia `N0002417C2117` electrical ($1,138M) and structural ($416M) both classify
    **Continuous** (the key requirement).

## 4. Decisions / deviations a reviewer should know (do not "re-fix" without checking)

- **Sourcing-mode tests continuity FIRST, then "Sparse."** A lane active for years with no
  90-day gap is ONE long wave — continuous, not sparse. Getting this order wrong undercounts
  Continuous by 2 lanes / $260M. This was a mid-build fix; the workbook now matches the verified 18.
- **"Dormant" was dropped from Sourcing mode.** The classifier is wave-shape only (waves / span /
  ratio) so the SAME formula reads identically on Re-buy Timing, Continuous Sourcing, and Wave
  Cadence (Wave Cadence has no active-vendor column). Dormancy is visible via the activity columns;
  it never gated a count (dormant lanes aren't eligible anyway).
- **Continuous openings = 18 is BROADER than the review's "9."** The review's 9 was only the
  subset overlapping the OLD naive headline; 18 is the full eligible-continuous-material
  population — the correct universe for a dedicated screen.
- **Periodic-due = 4, not the review's ~5.** The window-overlap test is stricter than the old
  point-date test, and cadence-applicable uses the ratio cap. Both follow from the user's chosen
  approach; exact membership is visible and tunable via the §2b controls.

## 5. Open items for the next agent

1. **WAIT for the in-progress review.** Standby on further refinements until those notes land,
   then reconcile against §3/§4 before changing anything (some apparent "bugs" are intended).
2. **Dangling reference (low priority):** `findings_jump_balls_20260615.md:4` still cites the
   deleted `methodology_jump_balls_20260615.md` as its `**Method:**`. Left untouched (the delete
   was scoped to the methodology doc). Repoint or retire the findings doc if the user wants.
3. **Likely review-driven tuning knobs** (all live §2b controls — no rebuild of compute needed to
   change them, just edit the cell defaults in `summary_inputs.py`): periodic-max 365, ratio cap
   1.25, strong min-waves 3 / gap-CV 0.60, always-on materiality $50M. The `_CONTINUOUS_SPAN = 730`
   "Continuous episode" label boundary in `data_award_waves.py` is a literal (descriptive only).
4. **After ANY change: re-verify** — tie-outs (records 7725/5281/5741, net $ within oracle,
   n_waves == Award Waves rows), rebuild green, and recompute the periodic/continuous/date-only
   split from the CSVs at the as-of.
5. Deferred (unchanged from prior handoff): Q3 text-token parsing (hull/build-year/admin) — needs
   extending `_corpus.iter_records`; reconciliation-critical, don't touch its dedup/filter.

## 6. Build + verify commands

```
# from research/scripts/ :
python3.12 compute_jumpball_signals.py     # 132 lanes / 572 waves / 3595 wave-vendor rows
# from the OUTER workbook_award_analysis/ :
python3.12 build_workbook.py               # expect 22 sheets / 18 native tables
python3.12 validate_workbook.py            # expect 0 xml errors / 0 error-literal
# docs (separate pipeline):
python3.12 doc/build_doc.py                # Re-Buy Methodology explainer
```
Count + tie-out re-verification is recomputed from the `extracted/` CSVs (`wb_lane_signals.csv`,
`wb_award_waves.csv`, `wb_wave_vendors.csv`) mirroring the live formula logic — see §3.

## 7. Staged review copy

`/Users/brendantoole/projects3/updated2_award_analysis/` — **19 files** (cap 20), each module
`updated2_`-prefixed, plus `updated2_compute_jumpball_signals.py` and the built workbook. NO
markdown (deliberate, per the user). Selection = every sheet module edited/added across the wave
refactor + the shared `_` infra; dropped the two non-wave indicator screens
(`model_concentrated_lanes`, `model_source_concentration`). Originals in the pipeline are
untouched. (The earlier-state copy is `projects3/updated_award_analysis/`.)

## Files (this session)

- **new:** `sheets/model_continuous_sourcing.py`.
- **edited compute:** `research/scripts/compute_jumpball_signals.py` (+ regenerated
  `wb_lane_signals.csv`, `wb_award_waves.csv`, `wb_wave_vendors.csv`).
- **edited sheets:** `model_rebuy_timing.py`, `model_wave_cadence.py`, `data_award_waves.py`,
  `data_wave_vendors.py`, `summary_overview.py`, `summary_inputs.py`, `summary_sources.py`,
  `_tabs.py`, `_widths.py`, `__init__.py`.
- **edited docs:** `rebuy_methodology_explainer.py`. **deleted:** `methodology_jump_balls_20260615.md`.
- **plan:** `~/.claude/plans/here-is-the-review-majestic-frog.md`.
- **staged copy:** `projects3/updated2_award_analysis/` (19 files).
