# 2026-06-16 — Award Analysis workbook: award-wave re-buy refactor (HANDOFF, in progress)

**Status: PAUSED mid-implementation, build green.** A new "award wave" grain was added to the
re-buy analysis and verified (tie-outs hold, 21 sheets build clean), but an unresolved
**cadence/timing methodology issue** (continuous-lane "mega-wave" chaining) was found during
verification. Implementation is otherwise complete except the docs pass. This doc is the
handoff for the next agent: §1–4 = what's done + current state, §5 = the open issue to
resolve, §6 = remaining tasks, §7 = how to incorporate the incoming external review notes,
§8 = build/verify commands.

Pipeline: `projects/distributed_shipbuilding/workbook_award_analysis/` (nested package:
`workbook_award_analysis/workbook_award_analysis/sheets/`).
Compute: `projects/distributed_shipbuilding/research/scripts/compute_jumpball_signals.py`.
Output: `projects/distributed_shipbuilding/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`.
Build env: `python3.12` only (system `python3` is 3.9 / no openpyxl).
Run order: `extract_workbook_cuts.py` → `compute_jumpball_signals.py` →
`build_workbook.py` → `validate_workbook.py` (build/validate from the OUTER
`workbook_award_analysis/`).

## 0. Why this work (intent)

The user asked to verify + deepen the **re-buy** sourcing-opening methodology, specifically the
recurring ~90-day award "clumps": (Q1) how often they recur per lane, (Q2) whether the same
vendors / same $-split recur each time, (Q3) what they're tied to in the production cycle.
A prior external LLM proposed a clump-level layer; this session implemented a disciplined
subset, corrected against the real code/corpus. The full assessment + approved plan is at
`/Users/brendantoole/.claude/plans/ok-now-i-want-dynamic-snowglobe.md`.

## 1. Decisions locked with the user (via AskUserQuestion + follow-ups)

- **Scope = Full:** 2 new data leaves (Award Waves, Wave Vendors) + a new Wave Cadence model
  tab + surgical fixes to the re-buy screen.
- **Terminology = full rename** off "recompete" → **"Re-buy"** / **"award wave"**; retire
  "buy bursts".
- **Q3 = defer the heavy text-mining, but ship a confidence token now:** included prime-base
  offset + capability mix + an evidence-backed `prodcycle_confidence` token; **deferred** the
  hull/build-year/admin text-token parsing (would require extending the shared
  `_corpus.iter_records`). Left as a hook.
- **Summary count = strict:** headline = `Re-buy due` (eligible AND timing-due); keep the
  broad date-only measure as a secondary "Timing signal due" row.
- **Architecture:** no live in-Excel re-clustering (workbook holds wave-grouped data, can't
  re-cluster live). Did the one internal refactor that pays off — cluster **once** into the
  wave table, derive lane signals from it (single source of truth). Window sensitivity
  precomputed; active 90-day window shown as a **read-only** as-built reference on Assumptions.

## 2. What was implemented

### Research / compute (`compute_jumpball_signals.py`, fully rewritten)
- **Wave-first:** `build_waves(recs, gap)` clusters a lane's records once; `process_lane()`
  derives the lane signal row + per-wave rows + per-wave-vendor rows from that single pass.
  Net **signed** dollars. `assert dt is not None` on every supplier record (0 today; keeps a
  future undated record from silently un-tying Checks).
- **New CSV `wb_award_waves.csv`** (one row per program/piid/work_type/wave_seq): start, end,
  anchor (= **plain median award date**), duration, prior-wave interval, n_records, net $M,
  n_vendors, top vendor + top1/others share, modal_capability, neg_correction_m,
  prime_base_offset_days.
- **New CSV `wb_wave_vendors.csv`** (one row per …/vendor): net $M, share-of-wave, records,
  first/last date in wave, capability, entrant_flag.
- **Extended `wb_lane_signals.csv`** with: `n_waves`, `median_wave_gap_days` (renamed from
  `n_clusters` / `median_cluster_gap_days`), `gap_iqr_days`, `gap_cv`, `n_gaps`,
  `last_wave_anchor`, `next_expected`, `vendor_retention_avg`, `allocation_similarity_avg`
  (cosine on dollar-share vectors), `top_vendor_stable_frac`, `capability_coherence`,
  `n_waves_w{45,60,120,180}` + `median_gap_w{…}`, `window_stable`, `prodcycle_confidence`.
  (Existing columns kept; only `n_clusters`/`median_cluster_gap_days` were renamed.)

### Workbook sheets
NEW: `data_award_waves.py` (Award Waves; rollups/shares LIVE SUMIFS/COUNTIFS/MAXIFS over Wave
Vendors), `data_wave_vendors.py` (atomic leaf; share = live ratio), `model_wave_cadence.py`
(lane-level cadence + composition + window-stable + confidence; all blue "non-liveable"
signals except Next expected = live last-award+gap).

EDITED:
- `model_rebuy_timing.py` — tab `Recompete Timing` → **`Re-buy Timing`**; columns: Last award
  (live MAXIFS), Re-buy cadence (= `median_wave_gap_days`, blue), Award waves (= `n_waves`,
  blue), Next expected wave (= Last award + cadence, live), **Re-buy eligible** (AND(active ≥
  Assumptions multi-min, top-1 ≤ Assumptions cutoff)), **Timing due**, **Re-buy due**.
  Accessors: `rb_due_count` (strict = Re-buy due) + new `rb_timing_due_count` (broad date-only).
- `summary_overview.py` — §4 headline now strict `Re-buy openings due (eligible ≤ horizon)`
  + secondary `Timing signal due (date only)`.
- `summary_inputs.py` — added read-only "Clustering window (days, as-built) = 90" + accessor
  `input_wave_window_ref()`; renamed control "Recompete horizon" → "Re-buy horizon".
- `validation_tie_outs.py` — added Award Waves + Wave Vendors $ / record legs.
- `model_piid_worktype.py` — internal `recompete_flag` → `multisource_flag` (visible header
  was already "Multi-source"; behavior unchanged).
- `_tabs.py` — added `TAB_AWARD_WAVES`, `TAB_WAVE_VENDORS`, `TAB_WAVE_CADENCE`; renamed
  `TAB_RECOMPETE_TIMING` → `TAB_REBUY_TIMING` (= "Re-buy Timing").
- `_widths.py` — added `W_WAVE_SEQ = 7`.
- `sheets/__init__.py` — registered the 3 new sheets in group order (model:
  …Supplier Lanes → Re-buy Timing → Wave Cadence → Concentration…; data: …Lane Vendor FY →
  Award Waves → Wave Vendors → Role Detail…). 18 → **21 sheets**.
- `data_lane_vendor_fy.py`, `data_prime_awards.py` — docstring "recompete" → "re-buy" only.

## 3. Verification that PASSED (re-runnable; see §8)

- Build green: **21 sheets, 17 native tables, 64 parts, 0 xml errors, 0 error-literal cells.**
- 0 visible "recompete" / "clump" / "buy burst" in the built XML; "Re-buy" present.
- **Tie-outs hold** (recomputed from CSVs; the build can't evaluate formulas, user verifies
  in Excel on open per the standing no-headless-recalc rule):
  - Records EXACT across Lane Vendor FY / Award Waves / Wave Vendors:
    **virginia 7,725 / columbia 5,281 / ddg 5,741.**
  - $ within the $0.5M oracle (max drift $0.014M); vendor-lane grain (2,897 keys) records
    exact, max $ drift $0.002M. Baseline $: virginia 4343.6 / columbia 3342.2 / ddg 3095.4.
  - lane `n_waves` == count of Award Waves rows (**132 lanes / 572 waves / 3,595 wave-vendor
    rows**; 14 single-wave lanes carry blank next-expected; no share > 1; 10 net-negative
    waves handled).
- Live formulas spot-checked in built XML (eligibility, timing, rollup, share).

## 4. Staged external-review copy

`/Users/brendantoole/projects3/updated_award_analysis/` — **20 files** (cap is 20), each sheet
module `updated_`-prefixed, plus `updated_compute_jumpball_signals.py`, the built workbook, and
`00_PROGRESS_AND_METHODOLOGY_ISSUE.md` (the review-facing writeup — deliberately **no fix
suggestions**, so the incoming review isn't anchored). The 10 trimmed copies were unchanged,
unrelated modules (5 market-view tabs, lane_detail/lane_vendors/role_detail leaves,
summary_sources, _taxonomy). Originals in the pipeline are untouched.

## 5. THE OPEN METHODOLOGY ISSUE (must resolve to finish)

Only the **cadence / "next expected wave" / timing-due** signal is affected. The descriptive
wave tables, the eligibility gate, and the composition-similarity signals (Q1/Q2) are fine.

### 5a. Anchor sensitivity (already navigated, but revisit if review disagrees)
Next expected = origin + median wave gap. The **wave-median anchor** sits ~½ a wave-duration
before the last award → biased early → dropped the largest periodic lane (DDG `N0002423C2307`
machining, $491.5M) as "overdue" (2026-04-28, 24d before the 2026-05-22 as-of). **Switched to
last-actual-award + wave-based cadence** (→ 2026-08-04, due). Note the wave-median anchor did
NOT solve its stated purpose either (a stray late record >90d forms its own last wave either
way). Current build uses last-award + median wave gap.

### 5b. Core issue: single-linkage clustering chains continuous lanes into multi-year waves
For lanes with near-continuous activity (awards <90d apart for years), the 90-day single-
linkage rule chains everything into one multi-year "wave," so the derived cadence is an
artifact and the next-expected/timing-due flag is spurious. Example — Columbia
`N0002417C2117` electrical ($1,138M recent, top-1 54%, eligible): "wave 4" spans **2021-01-11
→ 2025-01-24 (1,474 days, 196 records, $1,031M)**; median wave gap 598d → next 2026-09-14 →
reads "Re-buy due". (The prior model masked this via start-to-start gaps reading it "overdue";
nothing about the lane actually changed.)

### 5c. Scale (data, not a verdict)
Longest-wave-duration per lane (132 lanes): ≤90d **42**, 91–365d **36**, 366–730d **19**,
>730d **35** → **54/132 (41%)** have a wave > 1 year. Of the current **14 strict Re-buy-due
lanes ($2,563.7M)**: **9 ($1,788.3M) are "continuous"** (longest wave >365d, cadence spurious;
incl. both big Columbia lanes) and only **5 ($775.4M) are genuinely periodic** (DDG
`N0002423C2307` machining/hvac/structural/castings + 1 small Virginia lane). Broad date-only =
**20 / $2,622.0M**. So the headline $ is dominated by lanes where the cadence isn't meaningful.

### 5d. The tension to resolve
The re-buy *cadence/timing* model assumes discrete periodic bursts separated by years; ~41% of
lanes (and most material $) are continuously active, so 90-day single-linkage can't separate
"periodic re-buys" (next-date meaningful) from "always-on sourcing" (next-date meaningless).
**Open directions observed (NOT decided — weigh against the incoming review notes):** (a)
detect continuous lanes via longest-wave-duration / duty-cycle and treat their cadence/timing
as N/A while keeping them on the multi-source/concentration screens; (b) alternative
clustering (max-span cap, calendar binning, per-lane gap distribution); (c) restrict the
timing-due flag to genuinely periodic lanes. Do not pick one without the user — this changes
the headline numbers.

## 6. Remaining tasks

1. **Resolve §5** (the cadence/timing issue) with the user, incorporating the review notes.
2. **Re-verify** after any change: tie-outs (§8) must still hold; rebuild green; recompute the
   strict/broad counts and the continuous/periodic split.
3. **Docs pass (deferred):** update `doc/doc_distributed_shipbuilding/pages/rebuy_methodology_explainer.py`
   (award-wave vocab, wave/wave-vendor grain, Q1/Q2/Q3 framing, eligibility gate, and whatever
   §5 resolution lands) and `methodology_jump_balls_20260615.md` (wave-first refactor,
   median-vs-last-award anchor decision, strict re-buy-due, window-not-live, the continuous-
   lane treatment). Currently the explainer still describes the OLD single-date cadence.
4. **Optional later:** Q3 text-token parsing (hull/build-year/admin) — needs extending
   `_corpus.iter_records` (reconciliation-critical; don't change its dedup/filter).

## 7. Incorporating the incoming external review notes

The user is sending review notes on the staged `updated_award_analysis/` copy. When they
arrive: (a) the reviewer only saw the staged 20 files + the no-fix writeup, so notes on §5 are
independent — treat them as primary input to the §5 decision; (b) reconcile each note against
the verified facts here (tie-out baseline, the 41% continuous-lane finding, the anchor
history) before acting — some "bugs" a reviewer flags (e.g. shares, the renamed gap columns,
the strict-count drop vs the old model) are intended/explained above; (c) keep house rules:
leaf data blue / aggregations live, present-data-before-characterization (no verdict labels
gating anything), preserve the tie-out oracle, build-green = done (user does the visual Excel
check, no PNG/headless render).

## 8. Build + verify commands

```
# from research/scripts/ :
python3.12 extract_workbook_cuts.py        # leaves (unchanged this session)
python3.12 compute_jumpball_signals.py     # waves + lane signals
# from the OUTER workbook_award_analysis/ :
python3.12 build_workbook.py               # expect 21 sheets / 17 native tables
python3.12 validate_workbook.py            # expect 0 xml errors / 0 error-literal
```
Tie-out + count re-verification snippets were run against the `extracted/` CSVs
(`wb_award_waves.csv`, `wb_wave_vendors.csv`, `wb_lane_signals.csv`, `wb_vendor_lane_fy.csv`):
records must match 7725/5281/5741; AW/WV $ within $0.5M of Lane Vendor FY per program;
`n_waves` == count of Award Waves rows per lane. The strict/broad re-buy-due counts and the
continuous-vs-periodic split (§5c) are recomputed from `wb_lane_signals.csv` +
`wb_award_waves.csv` using as-of 2026-05-22, horizon 12mo, multi-min 2, cutoff 0.75.

## Files (this session)

- **new:** `sheets/data_award_waves.py`, `sheets/data_wave_vendors.py`,
  `sheets/model_wave_cadence.py`; extracts `wb_award_waves.csv`, `wb_wave_vendors.csv`.
- **rewritten:** `research/scripts/compute_jumpball_signals.py` (wave-first).
- **edited:** `sheets/model_rebuy_timing.py`, `summary_overview.py`, `summary_inputs.py`,
  `validation_tie_outs.py`, `model_piid_worktype.py`, `_tabs.py`, `_widths.py`,
  `__init__.py`, `data_lane_vendor_fy.py` (doc), `data_prime_awards.py` (doc);
  regenerated `wb_lane_signals.csv`.
- **plan:** `~/.claude/plans/ok-now-i-want-dynamic-snowglobe.md`.
- **staged review copy:** `projects3/updated_award_analysis/` (20 files).
