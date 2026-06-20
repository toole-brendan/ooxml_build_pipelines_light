# 2026-06-16 — Award Analysis: LIVE dynamic-array migration (SESSION LOG + HANDOFF)

**STATUS: COMPLETE and verified in Excel.** The award-wave analytical pipeline now
derives LIVE in the workbook (Excel-365 dynamic-array spills) from one raw leaf,
instead of being precomputed in Python and loaded as hardcoded CSV values. Two
external-review cycles drove this; both are now implemented and verified.

Pipeline: `projects/distributed_shipbuilding/`. Build env: `python3.12` only.
Run order: `extract_workbook_cuts.py` → `compute_jumpball_signals.py` →
`build_workbook.py` → `validate_workbook.py` (build/validate from the OUTER
`workbook_award_analysis/`). Module root = `workbook_award_analysis/workbook_award_analysis/`.

## 0. What this session did (two efforts, same day)

### Effort A — implemented the cadence-applicability review (`transcript_review.rtf`)
Continuation of the prior handoff (`2026-06-16_award_analysis_cadence_applicability_handoff.md`).
- Added data sheets **Lane Signals / Wave Sensitivity / Wave Pair Metrics / Award
  Events** (then) so model tabs became formula-only (no blue leaf cells on model
  tabs); rewired Re-buy Timing / Wave Cadence / Continuous Sourcing / Source
  Diversification to live SUMIFS/XLOOKUP over those leaves.
- **Active-now gate** on Continuous Sourcing: 3 new §2b controls (active lookback
  365 / min records 1 / min $M 0); the "always-on" flag now requires recent
  activity → headline "Active continuous sourcing openings" drops from 18 to **7**
  (excludes the 11 stale lanes the reviewer flagged); kept "Continuous multi-source
  lanes" (=18 structural) as a diagnostic.
- **Workbook-only terminology rename**: tab "Re-buy Timing" → **Periodic Sourcing**;
  Re-buy due → Periodic opening due, Timing due → Forecast window due, Re-buy
  cadence → Award-wave cadence, Re-buy eligible → Shared-lane eligible, Date-only
  signal → Ungated timing signal, sourcing-mode "Periodic re-buy" → "Periodic
  sourcing". Kept "re-buy" in the methodology doc; decks untouched.
- Staged `projects3/updated3_award_analysis/`. (Reviewed → drove Effort B.)

### Effort B — the LIVE dynamic-array migration (`transcript_review_new.rtf`) — the bulk
User directive: get the analytical computation OUT of Python — specifically
"compute award waves / cadence / sensitivity" and "compute cosine allocation
similarity". Only the raw extracted fields (dates, $) may be hardcoded. Result:
the wave pipeline is now LIVE in Excel.

## 1. The live architecture (final)

One raw leaf drives everything: **Award Events** (native table, `wb_award_events.csv`)
— one row per FSRS supplier award (program, PIID, work type, vendor, date, $, +
live helper cols: `Wave` = 90-day wave number via SUMIFS over Event Dates, `Wave
key` = program|piid|wt|wave, `Wave-vendor key`, `Positive $M`).

| Sheet | How it's derived now |
|---|---|
| **Event Dates** (NEW, non-table) | one row per distinct lane-date; `Wave start @W` flags = cell-above running formula `IF(lane<>laneAbove,1,IF(date-dateAbove>WindowCell,1,0))` for W∈{45,60,90,120,180}, each reading a live Assumptions window cell. n_waves@W = `SUMIFS(start@W, lane)`. |
| **Award Waves** | dynamic-array **spill**: `B = SORT(UNIQUE(AwardEvents[Wave key]))`; identity parsed via TEXTBEFORE/TEXTAFTER; start/end/span/records/$/gross$ via MINIFS/MAXIFS/SUMIFS/COUNTIFS over ANCHORARRAY(B); anchor = `BYROW(…,LAMBDA(_xlpm.wkey,MEDIAN(IF(key=_xlpm.wkey,date))))`; prior gap = XLOOKUP of wave-1's anchor in the sheet's own spill. |
| **Wave Vendors** | **spill** (per lane·wave·vendor) over Award Events; share on positive-gross basis. |
| **Wave Pairs** | **spill** (per consecutive wave pair); vendor retention + **live cosine** allocation similarity (`BYROW+LET+MAP+FILTER+SUMPRODUCT/SUMSQ`, all over the stable Award Events ranges). |
| **Wave Sensitivity** | live `SUMIFS(EventDates[start@W], lane)` per window + single-cell array MEDIAN gap. |
| **Lane Signals** (132-row table) | LIVE: award waves (Event Dates), median gap / IQR / CV / median span (cross-sheet `MEDIAN(IF)` / `LET+FILTER+QUARTILE/STDEV` over the Award Waves prior-gap & span spills), longest span (cross-sheet MAXIFS), median quiet gap (Event Dates), vendor retention + allocation (`AVERAGEIFS` over Wave Pairs spill), prior top-1 (Lane Vendor FY), last award (Award Events), window-stable (Event Dates 60/90/120 compare). RESIDUAL computed leaf (see §4). |
| **Assumptions** | clustering window + §3b sensitivity windows (45/60/120/180) are now LIVE blue controls; change one → waves re-cluster. |

## 2. The packager spill mechanism (`workbook_core/primitives.py` + `lib.py`)
- `SpillF(str)` marker → cell emitted as
  `<c cm="1"><f t="array" ref="{anchor}">FORMULA</f><v>0</v></c>` (anchor-ONLY ref +
  cached `<v>0`; `cm="1"` points at a new `xl/metadata.xml` XLDAPR/fDynamic record).
- `ArrayF(str)` marker → single-cell CSE array `<f t="array" ref="self">` (for
  scalars like `MEDIAN(IF(...))`).
- `lib.build_metadata_xml()` + a `sheetMetadata` content-type override + workbook
  rel. Always emitted (harmless if unused).

## 3. *** CRITICAL hard-won encoding rules (all verified in the user's Excel) ***
These cost ~6 Excel "Removed Records" repair cycles to nail. Honor them for ANY
future spill work in this pipeline:
1. **Spill cell = `cm="1"` + `t="array"` + ANCHOR-ONLY `ref` + cached `<v>0`.** A
   full-range `ref` needs the (unknown) extent; a single-cell CSE `t="array"`
   ref on a spilling result → Excel REMOVES the formula on load.
2. **`LET` variables AND `LAMBDA` parameters BOTH need the `_xlpm.` prefix** (e.g.
   `LET(_xlpm.g, …, …)`), and every reference to them too. A bare `LET` var was
   the single biggest cause of removed formulas (broke the Award Waves top-vendor
   AND the first cosine attempt).
3. Prefixes: `SORT`/`FILTER`/`SORTBY` = `_xlfn._xlws.`; `UNIQUE`, `MAP`, `BYROW`,
   `LAMBDA`, `LET`, `VSTACK`, `ANCHORARRAY`, `TEXTBEFORE`, `TEXTAFTER`, `MINIFS`,
   `MAXIFS`, `XLOOKUP` = `_xlfn.`; MEDIAN/IF/SUMIFS/COUNTIFS/AVERAGEIFS/SUMPRODUCT/
   SUMSQ/SQRT/QUARTILE/STDEV/AVERAGE/MATCH/ISNUMBER/IFERROR/INDEX = no prefix.
4. The `#` spill operator is stored as `_xlfn.ANCHORARRAY(Anchor)`. Self-contained
   spills over the STABLE Award Events native table are the safe base; cross-sheet
   rollups over a spill via `_xlfn.ANCHORARRAY('Sheet'!Anchor)` inside AVERAGEIFS /
   MAXIFS / MEDIAN(IF) / FILTER ALSO work (verified) — the earlier failure that
   looked like "cross-sheet ANCHORARRAY is fragile" was actually the bare-LET bug.
5. `workbook.xml` keeps `fullCalcOnLoad="1" forceFullCalc="1"` (already present) so
   Excel computes + re-extents spills on open.
6. **Verification method**: I cannot self-verify spills (LibreOffice ignores `cm`
   dynamic arrays → useless oracle). The loop is: build → user opens+saves in Excel
   → I read the cached `<v>` values from the saved XML. SMOKE-TEST a risky new
   construct in a tiny standalone xlsx first (see `projects3/spill_smoke_test.xlsx`,
   `cosine_smoke_test.xlsx`) — and note a tiny minimal `styles.xml` must be
   schema-valid (empty `<font/>`/`<fill/>` → "Xml parsing error").

## 4. What still runs in Python (justified; not in the "out" ask)
`compute_jumpball_signals.py` now emits ONLY `wb_award_events.csv` (raw leaf) +
`wb_lane_signals.csv` (residual) + the prime calendar / clustering test. It NO
LONGER emits wb_award_waves / wb_wave_vendors / wb_wave_pairs / wb_wave_sensitivity
(those sheets are live). `build_waves()` still runs to produce the residual Lane
Signals columns Excel can't derive live: **top-vendor stability, capability
coherence** (cross-wave composition), **2nd-source FY, incumbent / still-active**
(source transition), **vendor-adds, active-months %**, prod-cycle confidence. These
are blue leaf cells on Lane Signals (a data sheet) — acceptable.

## 5. Verification that PASSED (re-runnable)
- Build: **27 sheets, 19 native tables** (the 3 live-spill sheets + Event Dates are
  no longer native tables), **0 xml errors, 0 error-literal cells**.
- Excel-verified cached values: Award Waves spill = **572 rows**; Wave Vendors =
  **3,595**; Wave Pairs = **440**; per-program tie-outs records **7,725 / 5,281 /
  5,741** EXACT; **Checks 6/6 OK**; zero `#…` errors workbook-wide.
- Lane Signals live vs Python CSV: award-waves sum 572=572, retention mean
  0.3302=0.3302, longest-span sum 76,746=76,746, Gap-CV sum 57.70=57.70 (exact);
  median gap / span match within int-rounding (live is exact, Python `_median_int`
  rounded); Gap IQR differs only on 1-gap lanes (live 0 vs Python blank). All
  expected, not errors.
- Live clustering reproduces `build_waves` exactly at all 5 windows (0 mismatches).

## 6. Open items / next agent
1. **Deferred Lane Signals composition cols stay computed** (§4) — making
   top-vendor-stable / capability-coherence / 2nd-source-FY / incumbent live would
   need heavy modal / first-appearance formulas; not requested, low ROI.
2. **Award Waves vendor columns (Vendors/Top-1/Top-vendor/modal-cap) were dropped**
   when first attempted (the bare-LET bug, since fixed). They are NOT load-bearing
   (full vendor composition is on the Wave Vendors spill). Could be re-added now
   with the `_xlpm.`-correct BYROW argmax if desired.
3. **Performance**: recalc is heavier (live per-record Wave number = SUMIFS over 11k
   Event Dates × 18.7k records, + the spill/BYROW work). User reported it acceptable.
   `forceFullCalc` recomputes on every open. If it ever drags, the per-record Wave
   SUMIFS is the hot path to optimize first.
4. **Excel-365 only**: the workbook now requires the dynamic-array engine. Older
   Excel will not spill.
5. After ANY change: rebuild green, then **open+save in Excel and read cached
   values** (no headless recalc — [no-png-render-verification]); confirm Checks
   6/6 OK and 0 error cells.

## 7. Build + verify commands
```
# from research/scripts/ :
python3.12 compute_jumpball_signals.py     # 132 lanes / 572 waves / 18747 events;
                                           # no longer writes waves/wave-vendors/pairs CSVs
# from the OUTER workbook_award_analysis/ :
python3.12 build_workbook.py               # expect 27 sheets / 19 native tables
python3.12 validate_workbook.py            # expect 0 xml errors / 0 error-literal
```
Then open the .xlsx in Excel 365, save, and re-read cached <v> values to verify.

## 8. Staged review copies
- `projects3/updated3_award_analysis/` — after Effort A (formula-only model tabs).
- `projects3/updated5_award_analysis/` — FINAL, the live-spill state: 16 modules
  (`updated5_`-prefixed) + the built workbook + `updated5_README.md` (the encoding
  rules + the live-architecture table for the reviewer). NO `updated4` folder (it
  was the mid-effort handoff that resolved the spill encoding; deleted).
- Scratch smoke-test xlsx (spill + cosine proofs) were deleted after use; the rules
  they established are captured in §3. Regenerate ad-hoc if a new construct needs proving.

## Files (Effort B)
- **packager:** `workbook_core/primitives.py` (SpillF/ArrayF/cell), `workbook_core/lib.py`
  (build_metadata_xml + content-type + rel + part).
- **new sheet:** `sheets/data_event_dates.py`.
- **rewritten to live spills:** `sheets/data_award_waves.py`, `data_wave_vendors.py`,
  `data_wave_pairs.py`, `data_wave_sensitivity.py`.
- **edited:** `sheets/data_award_events.py` (+Wave/Wave key/Positive $M/Wave-vendor key),
  `data_lane_signals.py` (live cadence + retention/allocation; residual leaf),
  `summary_inputs.py` (live clustering + §3b sensitivity windows), `validation_tie_outs.py`,
  `_tabs.py` (+TAB_EVENT_DATES), `__init__.py` (register Event Dates).
- **compute:** `research/scripts/compute_jumpball_signals.py` (retired sensitivity +
  waves/wave-vendors/pairs CSV emission; build_waves kept for residual lane signals).
