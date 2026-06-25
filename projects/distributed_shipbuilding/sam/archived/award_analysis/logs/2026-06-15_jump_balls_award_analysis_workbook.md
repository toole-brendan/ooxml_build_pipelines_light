# 2026-06-15 — "Jump ball" identification tabs in the Award Analysis workbook

## Goal

Build, into the Award Analysis workbook
(`20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`, pipeline
`projects/distributed_shipbuilding/workbook_award_analysis/`), the identification
of two kinds of **jump ball** — a contestable sourcing opportunity for a new
entrant:
1. existing **multi-source** contracts coming up for re-buy;
2. existing **single-source moving to multi-source**.

Came in as a methodology question (the user had asked two external LLMs, who
could not see this repo and guessed at data availability). The user then said:
actually find the jump balls now, render into the **workbook only** (no slides),
and **drop the "campy"** competability verdict vocabulary (COMPETABLE / SEEDED /
COMPONENT-TIER / LOCKED). Two follow-ups added during the work: write up the
data-provenance answers the reviewers asked for, and note a grain finding in a
findings doc.

## 0. What the repo actually had (the pivot)

The external LLMs' advice was built on guesses; the directory overturned the
big ones:
- **No new pull needed.** `nc_records_long.csv` (subs 9,268 / DDG 22,867 rows)
  already retains subaward action date, amount, subawardee + parent UEI,
  subaward number, prime PIID; raw JSON in `sam_subawards_fullhistory/` has
  more. Prime/FPDS dates + PIID→block labels also on disk.
- **Parent normalization already exists** (`vendor_key = parent_uei or
  entity_uei` in `_corpus.py`).
- **The LLMs' centerpiece — a component taxonomy parsed from subaward
  descriptions — is a dead end.** Descriptions are boilerplate ("See Below");
  the competability handoff had already settled "classify on the vendor, not
  the award." Used vendor-side SAM NAICS **capability tags** instead.
- **~70% of the substrate already existed** as the competability scorecard.
  The jump balls are a thin extension, reframed as descriptive cuts (no campy
  gates, per the house "present data before characterization" rule).

## 1. New leaf cut — vendor × lane × FY

`research/scripts/extract_workbook_cuts.py`: added a `vend_fy` accumulation in
the existing `pw` lane loop and a `capability()` helper (dollar-weighted modal
SAM NAICS per vendor_key). Emits **`wb_vendor_lane_fy.csv`** — one row per
(program, PIID, work type, vendor): per-FY $ and counts, first/last award,
naics4 + capability, totals. 2,897 rows; asserts it reconciles to
`wb_vendor_lane.csv` per vendor-lane and on row count. The capability tag does
its job immediately — the 70-vendor Virginia *piping* lane resolves into
Industrial Valve (3329) / Measuring-Dispensing (3339) / pipe-fitting / etc.

## 2. New compute script — the non-liveable signals + prime calendar

`research/scripts/compute_jumpball_signals.py` (stdlib, reuses
`_corpus.iter_records`):
- **`wb_lane_signals.csv`** (per PIID × work-type lane): median inter-award
  interval, award-burst clusters + median gap, last award, prior/recent active
  vendor counts + top-1 shares + recent/prior $, **second-source entry FY**,
  **incumbent (prior top-1) + still-active flag**.
- **`wb_prime_calendar.csv`** (per in-scope PIID, from `fpds_raw/*.json`
  filtered to the PIID): base/last prime action dates, action count, block
  label; flags `covered` (37/39) and **`base_is_window_floored`** (18/37 —
  the FPDS pull floors at SIGNED_DATE 2018-01-01 subs / 2017-10-01 DDG, so a
  pre-floor contract's "base award" is not real).
- **`jumpball_prime_clustering.csv`** — the empirical timing test (§5).

Recent window set to **FY22→present (incl. partial FY26)**, deliberately wider
than the scorecard's FY22-25 snapshot, so the newest second sources are caught.

## 3. New workbook tabs (descriptive, no verdict labels)

All counts/shares are **live** COUNTIFS/SUMIFS/`_xlfn.MAXIFS` over the leaf,
keyed on each row's own PIID + Work Type; only the non-liveable signals are blue
leaf values (house rule: leaf data blue, aggregations live, no on-tab checks).
- **Lane Vendors × FY** (data, native table) — the leaf; per-FY blue inputs +
  live $M/Records totals and live prior/recent window sums.
- **Prime Awards** (data, native table) — the prime-calendar reference;
  coverage + window-floored flags travel on every row.
- **Re-buy Timing** (model) — jump ball 1: active vendors, top-1 / others'
  share, recent $, last award, re-buy gap + bursts (blue leaf), next re-buy
  (= last + gap). Sorted by recent $; multi-source = ≥2 vendors and material
  others' share (transparent, not a label).
- **Source Concentration** (model) — jump ball 2: prior vs recent active
  vendors + top-1 share, second-source entry FY, incumbent + still-active.
- Registered in `sheets/__init__.py` (model block + data block, contiguity
  preserved); `_cuts.py` gained `RECENT_FY_KEYS` / `PRIOR_FY_KEYS` / `N_PRIOR`.
- **Tie-Outs** gained a leg (`lvf_total_cell` / `lvf_records_total_cell`):
  the leaf's per-program supplier $ and records tie to every other cut exactly
  (verified: virginia 7,725 / columbia 5,281 / ddg 5,741 records; $4,343.6 /
  $3,342.2 / $3,095.4M — equal across By Role, By Vendor, leaf). Build green,
  15 sheets, 6 native tables.

## 4. Timing anchor — tested, not assumed

Per the user's pushback (and the second LLM's walk-back): the outsourced market
re-sources on the shipbuilder→supplier clock, not the Navy→prime clock. Made
subaward **cadence/turnover primary** and the prime calendar a **tested
overlay**. The test (supplier award-burst start → nearest prime base award) is
**diffuse on all three programs** — median 942 d Virginia (9% within ±180 d),
511 d Columbia (22%), 1,162 d DDG (11%). So supplier re-sourcing does not track
prime/block awards; the re-buy estimate uses subaward cadence only and Prime
Awards is context. (Refined mid-build: the naive "nearest prime *action*"
read 6 d on DDG — an artifact of hundreds of admin mods; base-award proximity
is the meaningful, and diffuse, signal.)

## 5. Grain finding — jump ball 2 at the work-type grain

**The strict "1 prior vendor → 2+ recent" fires ~zero times at the work-type
lane grain** — work-type lanes aggregate too many components to ever have a
single historical vendor. Not "no second-sourcing"; a grain artifact. At this
grain the usable signal is a **falling top-1 share + recent second-source entry
with the incumbent still active** (a split): e.g. Columbia castings Scot Forge
96%→69% (active), DDG machining Rolls-Royce 90%→42%, DDG piping CIRCOR
100%→32%; vs swaps where the incumbent went silent (Columbia coatings Globe
Composite 64%→25%). The cleanest 1→2 events live at the **capability tier** —
drill `Lane Vendors × FY` to a lane. Recorded in the findings doc.

## 6. Docs

- `methodology_jump_balls_20260615.md` — definitions/thresholds, "no new pull"
  basis, the cadence-primary + prime-tested timing model, the grain decision
  (7 buckets + capability tag), caveats, and **§7 answering the reviewers'
  data-provenance questions** (source / PIID filters / date field / description
  retention / role tagging / parent normalization / record-level dates + UEI)
  — so no separate provenance doc was needed.
- `findings_jump_balls_20260615.md` — headline multi-source lanes per program,
  the electrical counter-example (21 vendors, top-1 93% → correctly not
  flagged), the prime-clustering result, and the §2 grain finding.

## Files

- `research/scripts/extract_workbook_cuts.py` (extended), `compute_jumpball_signals.py` (new)
- `workbook_award_analysis/sheets/`: `data_lane_vendor_fy.py`, `data_prime_calendar.py`,
  `data_rebuy_timing.py`, `data_source_concentration.py` (new); `__init__.py`,
  `_cuts.py`, `validation_tie_outs.py` (edited)
- `methodology_jump_balls_20260615.md`, `findings_jump_balls_20260615.md` (new)
- Extracts: `wb_vendor_lane_fy.csv`, `wb_lane_signals.csv`, `wb_prime_calendar.csv`
  (workbook dir); `jumpball_prime_clustering.csv` (research/extracted)

Run order: `extract_workbook_cuts.py` → `compute_jumpball_signals.py` →
`build_workbook.py`. Build green = done.
