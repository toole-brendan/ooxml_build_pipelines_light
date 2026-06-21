# 2026-06-20 — Recompete Radar: predecessor↔successor lineage detection — session log + handoff

Ninth session (same day). Closes handoff item #2 from
`logs/2026-06-20_workbook_contracts_data_sheets.md`: *"the radar treats each family
independently; it does NOT yet link a predecessor vehicle to its successor."* This session added a
**build-time lineage derivation** to the Recompete Radar so an "Expired" vehicle is split into a
**true overdue recompete** (no follow-on) vs **superseded** (a live follow-on already exists). All
changes are in **one file**: `workbook_army/sheets/model_recompete_radar.py`. Build is green.

## Decisions locked this session (from the user)
- **Annotate the radar in-place**, not a separate sheet. The verdict has to sit next to the
  Recompete-window column so filtering the window also surfaces the lineage call. Radar grows 23→26 cols.
- **Same-incumbent follow-ons only** — match on `recipient_uei` + `psc_code` + temporal gap. High
  confidence, uses only `contract_awards.csv` (already loaded). A recompete won by a RIVAL stays flagged
  "Overdue" — **competed-away (different-vendor) detection is deliberately deferred** (would need the
  `award_actions.csv` `contracting_office` join + a lower-confidence tier).

## What was built (`model_recompete_radar.py`)
- **`_build_lineage(attrs)`** (new module fn): groups relevant families by `(uei, psc)`, sorts by
  start, chains A(earlier)→B(later) when `B.start − A.end ∈ [−_OVERLAP_DAYS, _GAP_CAP_DAYS]` days
  (negative = overlap); **closest-gap candidate wins** (resolves concurrent overlapping IDVs). Returns
  `(pred_of, succ_of)` key→PIID maps.
- **Full-universe attribute pass** (replaces the old single `selected` loop): builds per-family
  attributes (`uei` from the dominant-$ award's `recipient_uei`, `psc`, `start`=min `pop_start_date`,
  `end`=max `pop_current_end_date`, `total`) over **every watercraft-relevant family BEFORE the $1M
  floor** — a shown vehicle's successor/predecessor may itself be sub-$1M. `selected` is then the
  ≥ $1M subset, sorted by $ desc (unchanged downstream).
- **3 new columns:** `Predecessor vehicle` + `Successor vehicle` (build-time PIID literals, after
  `Last competition`) and `Lineage status` (after `Recompete window`).
- **Lineage status is a hybrid:** a SUPERSEDED row (has a successor) gets the **static literal**
  `"Superseded"` (successor existence is As-of-independent); a chain TAIL gets a **live formula**
  `=IF($S{r}="Expired","Overdue",IF($S{r}="n/a","","Active"))` that reads the existing Recompete-window
  cell, so Overdue↔Active re-clocks when the analyst edits the in-sheet As-of date.
- **Tunables** near `_MIN_OBLIG`: `_GAP_CAP_DAYS = 913` (30 mo), `_OVERLAP_DAYS = 548` (18 mo).
- Docstring + trailing caption document the method and that the DERIVED status is distinct from the
  blank analyst Confidence column.

### Column-list edits (kept `len(_COLS)==len(_HEADERS)`)
`_HEADERS` 23→26; `_COLS` inserted `18,18` (PIIDs) + `15` (status); `styles` leading `S_DEFAULT` run
7→9 and the window/in-market `S_DEFAULT` pair →run of 3 →
`[S_DEFAULT]*9 + [S_INT,S_NUM,S_INT] + [S_DATE]*3 + [S_INT,S_INT] + [S_DEFAULT]*3 + [S_TEXT_INPUT]*6`.
**Everything else auto-tracked** — `_CL`, `FB/CE/PE/MO`, `RW`, `J=_CL["Obligated $M"]`, `table_ref`,
`total_vals/total_sty` all derive from `_HEADERS`/`_NCOLS` by name, so no column letter was hardcoded.

## Why 18 mo overlap (not 12) + why the full universe
- The real Birdon chain `W56HZV14C0015` (ends 2020-09-30) → `W56HZV19D0093` (earliest order
  2019-08-12) **overlaps by 415 days** — a successor IDV routinely starts ordering while the
  predecessor C-contract runs out its option years. A 12-mo overlap tolerance *rejects* it.
- **22 of 62 superseded families have a successor BELOW the $1M floor** — building attributes only
  over the 226 shown would misclassify those 22 as Overdue (false opportunities).

## Verification (all green)
- **`verify_lineage.py`** (new standalone replica, `csv`+`datetime`, no workbook imports, lives at
  `workbook/verify_lineage.py`): reproduces universe **1,688 / 1,667 / 226** and split
  **OVERDUE 124 · SUPERSEDED 62 · ACTIVE 40** (sum 226); reports the 22/62 below-floor diagnostic; the
  four named chains resolve (Birdon pair −415d, Vigor `W56HZV17D0086` + Eastern `W912BU23C0020` as
  Active sole tails).
- **Build:** `cd workbook && python3 build_workbook.py` → green, **6 sheets, 5 native tables**.
- **Rendered xlsx (source-XML scan of sheet2):** RecompeteRadar table = **26 cols, `B11:AA237`
  (226 rows)**; **0 error-literal cells**; Lineage column = **62 `Superseded` literals + 164 live tail
  formulas** (the 164 = 124 Overdue + 40 Active live); named rows match the replica exactly
  (`W56HZV14C0015` → Successor `W56HZV19D0093`, status `Superseded`). Column letters resolved as
  Family=B, Predecessor=H, Successor=I, Recompete window=S, Lineage status=T; tail formula correctly
  references `$S` and the As-of `$C$6`.
- The live Overdue/Active split reconciles with the prior session's verified window distribution
  (Expired 185 / forward 41 = 124 overdue-tail + 61 superseded-expired / 40 active-tail + 1
  superseded-forward).

## Gotchas worth keeping
- **LibreOffice can't QA this sheet's live values.** `soffice --convert-to ods` does NOT force a
  recalc (our writer emits `<f>` with no cached `<v>`), and even with `fullCalcOnLoad="1"` injected,
  the **`outline_level=1` collapsible data rows do not round-trip** (raw `<table-row>` count collapses
  to ~14). Verify live math with the Python replica over the CSV — the project convention ("Excel was
  not run"), not via an LO recalc.
- **This engine uses inline strings, not `xl/sharedStrings.xml`.** A source-XML QA scan must read
  `t="inlineStr"` (`<is><t>`), not a shared-strings table (there isn't one).
- **`col_letter(i)` is gutter-offset** (returns Excel column `i+1`): `_CL[header_i]=col_letter(i+1)`,
  so Family lands at column **B** and `table_ref` ends at `col_letter(26)='AA'`. Never hardcode letters;
  derive from `_CL` by header name and they auto-shift on insertion.
- **`python` is not on PATH — use `python3`.**

## HANDOFF — what's left
- **Competed-away (different-vendor) successors** — deferred this session. Same PSC + same
  `contracting_office` + different UEI + gap → a likely rival-won follow-on. Needs the
  `award_actions.csv` office join and its own (lower) confidence tier; would move some families from
  Overdue → a new "competed away" status.
- **Follow-on lineage chains as their own view** — the radar shows one hop each way (Predecessor /
  Successor PIID). A dedicated chains sheet (predecessor → current → successor as linked rows) per the
  methodology spec would visualize multi-hop families end to end.
- **Tolerance sensitivity** — `_GAP_CAP_DAYS` / `_OVERLAP_DAYS` are tunable; `verify_lineage.py` is the
  place to sweep them before changing the defaults.
- Earlier handoff items still open: analyst tagging pass (program / capability_node / Window /
  Confidence / Pursuit), and the Stage 5 Opportunities full run (In-market notice column).

## Files created / changed
Changed: `workbook_army/sheets/model_recompete_radar.py` (lineage derivation + 3 columns + captions).
Created: `workbook/verify_lineage.py` (standalone lineage replica / QA).
Output: `projects/army/20260620_US Army Market Mapping_vS.xlsx` (rebuilds from `build_workbook.py`).

## How to re-run
```bash
cd projects/army/workbook
python3 verify_lineage.py     # confirms 1688/1667/226 and OVERDUE 124 / SUPERSEDED 62 / ACTIVE 40
python3 build_workbook.py     # → ../20260620_US Army Market Mapping_vS.xlsx (6 tabs, 26-col radar)
```
