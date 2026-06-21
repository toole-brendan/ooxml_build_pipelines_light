# 2026-06-20 — Pipeline Events: Stage-5 activation + live Open? leaf + radar In-market upgrade

Tenth session (same day). The Pipeline Events tab was a 4-notice **smoke sample** whose events
were all ~10-11 months stale (a hardcoded `01/01/2025-12/31/2025` window). This session made it
**real and forward-looking**: ran the Stage-5 SAM Opportunities pull for real (active mode), scoped
it to Army+USACE, surfaced open-vs-closed live against the radar As-of date, and upgraded the radar's
In-market signal to count only OPEN notices. Build is green.

## Why / intent (re-grounded with the user)
Pipeline Events is the **pre-award half** of the recompete radar (the post-award half is the lineage /
PoP-expiry work). A forward pipeline is by definition *what's currently active/open* - so the stale
smoke notices weren't the design, just an artifact of one hardcoded window.

## Decision locked this session (from the user)
**Faithful-raw + a derived live flag (NOT a hard drop at pull time).** Open-vs-closed is time-relative,
so it is DERIVED against the radar's editable As-of cell (one clock for the whole book), not frozen
into the leaf. Reasons: (1) consistency with the As-of re-clock built for the radar; (2) the leaf stays
faithful/re-runnable; (3) a just-*closed* notice = an imminent award, worth keeping, not deleting.
Coverage = **same-as-the-workbook scope**: Army + USACE only.

## What was built
### 1. Pull (`research/contracts/scripts/pull_sam_opportunities.py`) - new `active` mode
`python3 pull_sam_opportunities.py active` → one **trailing-363-day** posted window per title term
(12 calls). Faithful: keeps every returned notice (no open/closed filter at the pull). Ran live →
**165 distinct notices** (vs 4 smoke); watercraft 57, boat 67, barge 22, tug 13, …
- **Gotcha (load-bearing):** SAM rejects a span of *exactly* 1 year — `{"errorCode":"400",
  "errorMessage":"Date range must be null year(s) apart"}`. 365 days fails; **363 days works**. 2026
  postedTo is fine (SAM's clock agrees with the env). Probe with the error body — `_common.http_get`
  swallows it (returns `None, code`).
- Cache-key fix: filename now `{term}_{frmYYYY}_{toYYYY}.json` so the active window can't collide with
  the old smoke `watercraft_2025.json` (deleted as stale).

### 2. Aggregate (`scripts/aggregate_contracts.py`) - scope gate + open-first sort
- **Army+USACE scope gate** on `department` (`"ARMY" in dep or "CORPS OF ENGINEERS" in dep`), mirroring
  the awards' in_scope. Drops Navy/Air Force/Interior/Coast Guard/DLA/MARAD noise: **165 → 88**. The raw
  `extracted/_opportunities_index.json` keeps all 165 for audit (awards' all-vs-in-scope pattern).
- **Sort open-soonest-first:** OPEN (deadline ≥ as-of, nearest first) → no-deadline → CLOSED (most-
  recently-closed first). As-of reference = `RUN_ID[-10:]` (= 2026-06-20, the snapshot date).
- Result: **88 Army/USACE notices — 13 open · 51 no-deadline · 24 closed.**

### 3. Leaf (`sheets/data_pipeline_events.py`) - two DERIVED live columns
- Extended the shared builder `sheets/_flat.py` with a new `derived_cols=[(header, type, fn), …]`
  param: SYNTHETIC columns appended after the CSV columns (no CSV source; each a live `fn(r)->"=…"`).
  Backward-compatible (default empty → other 3 leaves byte-identical).
- Added **`Open?`** (`OPEN`/`closed`/`n/a`) and **`Days to deadline`** (signed int), both live vs the
  As-of cell. response_deadline's in-sheet letter is computed from the CSV header order (`_DL`).
- New shared constant `sheets/_tabs.py::AS_OF_CELL` (= `'Recompete Radar'!$C$6`) so the leaf and the
  radar key off ONE cell; the radar now `assert`s its rendered as-of row == `AS_OF_ROW` so the address
  can't silently drift.
- Refreshed the now-false docstring/intro (was "smoke-run only … 4 notices").

### 4. Radar (`sheets/model_recompete_radar.py`) - In-market = OPEN only
`In-market notice` upgraded from a bare award_number match to
`COUNTIFS(award_number=vehicle, response_deadline >= As-of)` — only a *live* notice counts.

## Verification (all green)
- Pull: 165 notices indexed; window probe confirmed valid (HTTP 200) before the full run.
- Aggregate: `contract_awards / award_actions / subawards` CSVs **byte-identical** (shasum -c) — only
  the pipeline CSV changed; sums still tie ($3,249.6M actions). Pipeline = 88 rows, 13 open.
- Build: green, **6 sheets, 5 native tables**.
- Rendered xlsx (source-XML, inline-string scan): `PipelineEvents` table = **21 cols, B8:V96 (88
  rows)**, last two cols `Open?` / `Days to deadline`; **0 error cells**. Spot row (Helicopter Tug,
  deadline serial 46195 = 2026-06-22, As-of 46193) → Open? formula `=IF($I9="","n/a",IF($I9>=
  'Recompete Radar'!$C$6,"OPEN","closed"))`, Days `=…$I9-'Recompete Radar'!$C$6` ⇒ OPEN, 2 days.
  Radar still 26 cols / 226 rows, 0 error cells, In-market formula references Pipeline `$N`(award_number)
  + `$I`(deadline) + the As-of cell.

## Gotchas worth keeping
- **SAM Opportunities span limit:** a posted window of exactly 1 year 400s ("null year(s) apart"); stay
  strictly under (363 days). The `active` window is **date-relative** — re-run to refresh (the cache
  filename carries the window years, so a new run on a new date pulls fresh).
- **LibreOffice still can't recalc this book** (the `outline_level=1` collapsible rows don't round-trip
  to ODS) — verify live math via Python over the CSV + structural xlsx scan, not an LO recalc.
- **In-market is award_number-keyed**, and open *solicitations* carry no award_number (only Award
  Notices do), so the column stays mostly blank for forward solicitations — a data-linkage limit, not a
  bug. Solicitation↔vehicle linkage has no shared key in SAM (a future incumbent/PSC heuristic could).

## HANDOFF — what's left
- **Title-term breadth inside Army/USACE:** the broad terms ("boat", "barge", "tug") still pull some
  non-watercraft Army/USACE notices (e.g. recreational/utility boats). The capability bridge +
  analyst tagging (`capability_node`) is the intended filter; a tighter relevance gate could be added.
- **Refresh cadence:** Pipeline Events is a dated snapshot; re-run `pull_sam_opportunities.py active`
  → `aggregate_contracts.py` → `build_workbook.py` to refresh. (~12 calls.)
- Earlier open items unchanged: analyst tagging pass; competed-away lineage; multi-hop lineage view.

## Files created / changed
Changed: `research/contracts/scripts/pull_sam_opportunities.py` (active mode + cache key),
`research/contracts/scripts/aggregate_contracts.py` (scope gate + open-first sort + count line),
`workbook/workbook_army/sheets/_flat.py` (derived_cols), `_tabs.py` (AS_OF_ROW/AS_OF_CELL),
`data_pipeline_events.py` (Open?/Days columns), `model_recompete_radar.py` (In-market open-only + assert).
Data: `research/contracts/sam_opportunities/*_2025_2026.json` (12 term pulls),
`extracted/_opportunities_index.json` (165, raw audit), `workbook/extracted/contract_pipeline_events.csv`
(88 in-scope). Output: `projects/army/20260620_US Army Market Mapping_vS.xlsx`.

## How to re-run
```bash
cd projects/army/research/contracts/scripts
python3 pull_sam_opportunities.py active      # ~12 SAM calls, trailing 363-day window
python3 aggregate_contracts.py                # rebuilds the 4 CSVs (pipeline scoped + sorted)
cd ../../../workbook && python3 build_workbook.py
```
