# 2026-06-15 — Award Analysis workbook: "Concentrated Lanes" jump-ball tab (the missing concentration read)

Pipeline: `projects/distributed_shipbuilding/workbook_award_analysis/`
Output:   `projects/distributed_shipbuilding/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`
Build:    `python3.12 compute_jumpball_signals.py` (research/scripts) →
          `python3.12 build_workbook.py` → `python3.12 validate_workbook.py`

## Goal

Reviewing the jump-ball logs, the user flagged a conceptual gap in **jump ball 2**.
As built, jump ball 2 = "single-source lane already splitting to multi-source"
(top-1 share *falling*, a second source recently entered). The user wanted jump
ball 2 to be the broader **concentrated-lane** category, with the splitting case
as one subset and **plain high vendor concentration (no movement required)** as
the other — and worried the recent work didn't surface the stable-monopoly
lanes at all.

## The gap (confirmed against the latest sheet modules)

- The raw number existed: `Source Concentration` already computes `Top-1 recent`
  **live** (MAXIFS/SUMIFS over the Lane Vendors x FY leaf) for *every* lane.
- But nothing **surfaced** stable high-concentration lanes as an opportunity.
  Source Concentration is framed/sorted/screened around the *split in motion*,
  and its Overview rollup `sc_emerging_count` counts only `Incumbent active="yes"`
  rows (the split subset). A lane at top-1 = 92% with no recent entrant read as
  the *least* interesting row — e.g. **Virginia electrical / Northrop Grumman,
  92.6%, ~$503M recent**, the purest jump ball on the board, was unflagged.
- `PIID x Work Type` has a `Vendors` count but **no top-1 $ share**, so a lane
  with 5 vendors where one holds 95% reads as "multi-source" there. `Overview §3`
  had only *program-level* top-vendor share, not a lane-level concentration count.
- Grain nuance (carried from the 06-15 jump-balls log §5): at the work-type lane
  grain the meaningful concentration signal is **top-1 $ share**, not vendor
  count (literal 1-vendor lanes are rare here; pure ones live at the capability
  tier in Lane Vendors x FY).

## Decisions (via AskUserQuestion)

- **Where:** add a 3rd model tab (clearest separation of the two subsets), not a
  reframe of Source Concentration or an Overview-only finding.
- **Threshold:** top-1 $ share **≥ 75%** defines "concentrated".
- (Mine, then surfaced to the user): **sort by recent $**, not by concentration —
  a pure top-1 sort floats trivial 100%-but-tiny lanes (e.g. Riverhead Building
  Supply) above the material ones; materiality-first matches the sibling tabs and
  makes the filtered (≥75%) view lead with the big lanes.

## What changed

1. **Research extract** `research/scripts/compute_jumpball_signals.py` — added
   `recent_top1_uei` / `recent_top1_name` to `wb_lane_signals.csv` (the lane's
   *current* dominant vendor, argmax of `recent_d` over `recent_v`, mirroring the
   prior-window `incumbent`). **Append-only** — the workbook loads by header name,
   so Re-buy Timing and Source Concentration are unaffected. Docstring updated:
   jump ball 2 reframed as "Concentrated lane … its dynamic subset is a single →
   multi split." Regenerated the CSV (132 lanes, all other outputs unchanged).
2. **New sheet** `sheets/data_concentrated_lanes.py` — model tab
   **`Concentrated Lanes`**, one filterable native table `ConcentratedLanes`:
   `Program | PIID | Work Type | Active vendors | Recent $M | Top-1 share | Top
   vendor (recent)`. Active vendors / Recent $M / Top-1 share are **live**
   COUNTIFS / SUMIFS / `_xlfn.MAXIFS` over the leaf on the recent window, keyed on
   each row's own PIID (C) + Work Type (D); only the top-vendor *name* is a leaf
   text value (S_DEFAULT). Zero-recent-$ lanes read Top-1 share 0 and sink. Screen
   note states the ≥75% cut; bottom Totals Row is filter-aware `SUBTOTAL(109,…)`.
   Promotes `cl_concentrated_count(program)` = COUNTIFS(Program, Top-1 share
   ">=0.75") over the table body.
3. **Registry** `sheets/__init__.py` — inserted between Re-buy Timing and Source
   Concentration so the model order reads JB1 re-buy → JB2 level (this tab) →
   JB2 motion (split).
4. **Overview §3** `sheets/summary_overview.py` — new live finding
   **"Concentrated lanes (top-1 ≥ 75%)"** (S_INT), placed after "Top vendor share
   of program $". Docstring §3 updated to name the new screen.

## Conceptual model now

Jump ball 2 = **concentrated lanes**, two reads:
- **stable monopoly** → `Concentrated Lanes` (new), top-1 ≥ 75% regardless of movement;
- **splitting** → `Source Concentration` (existing), top-1 falling + 2nd source entered.

## Verification

- Build green: **16 sheets, 14 native tables, 0 xml errors, 0 error-literal
  cells**, 51 parts. New tab is sheet 8.
- `ConcentratedLanes`: `autoFilter == ref` (B6:H138), 7-column span; leaf-keyed
  formulas confirmed in the built XML (leaf D=piid, E=wt, O=dol_recent,
  Q=rec_recent; e.g. `G7 =IF(F7=0,0,_xlfn.MAXIFS('Lane Vendors x FY'!$O$7:$O$2903,
  …)/F7)`).
- Sort spot-check: top rows lead with the material N0002417C2100 Virginia lanes
  (electrical/Northrop first).
- **Overview count independently recomputed from the CSV** (build can't evaluate
  formulas; Excel recalcs on open): the live COUNTIFS will read **Virginia 9 /
  Columbia 0 / DDG 9** concentrated lanes at ≥75%. Columbia 0 is consistent with
  the prior finding that its lanes are fragmented.
- Tie-Outs untouched — the tab introduces no independent totals (recent $ is
  SUMIFS over the already-reconciled leaf), so the reconciliation oracle is unchanged.

## Two knobs left easy to flip

- **Threshold** `_THRESHOLD = "0.75"` in `data_concentrated_lanes.py` (+ the
  Overview label string).
- **Sort** — currently recent $ desc; swap the `sorted(... key=...)` to top-1
  share if a concentration-first default is preferred.

## Files

- **new** `workbook_award_analysis/sheets/data_concentrated_lanes.py`
- **edited** `research/scripts/compute_jumpball_signals.py` (recent_top1 uei/name +
  docstring), `workbook_award_analysis/sheets/__init__.py` (register),
  `workbook_award_analysis/sheets/summary_overview.py` (§3 finding + import + docstring)
- **regenerated** `workbook_award_analysis/extracted/wb_lane_signals.csv`
  (+2 columns), `projects/distributed_shipbuilding/20260612_Distributed
  Shipbuilding Award Analysis_vS.xlsx`
