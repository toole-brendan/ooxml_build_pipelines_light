# 2026-06-20 — Recompete Calendar made fully formula-driven (handoff §NEXT done)

Twelfth session (same day). Executed the §NEXT handoff from
`2026-06-20_recompete_calendar.md`: made the **Recompete Calendar** completely
formula-driven so every displayed number is a LIVE in-sheet formula (BLACK) or an
honest hardcoded input (BLUE) — no more Python-baked values styled black as if derived.
Build green (**7 sheets, 6 native tables, 0 error cells**). Radar output is
**byte-identical** to before (verified). The flagged Tenure provenance lie is resolved.

## What changed

### 1. New shared `_radar_formulas.py` (the "ONE definition" the handoff asked for)
Factored the radar's family-keyed live-formula builders into
`family_formulas(fam, asof)` → dict of row→formula builders (`cur_end`, `pot_end`,
`parent_end`, `vtype`, `tos`, `obl`, `acts`, `inmkt`). `fam` is a callable
row→family-key cell ref (column letter differs per sheet, so the caller owns it); leaf
ranges resolve from the leaves' own `cols()` accessors. Radar and Calendar now compute
the shared roll-ups from the same source, so they can never disagree on a number.

### 2. Radar refactored to consume it — BYTE-IDENTICAL
`model_recompete_radar.py` drops its inline leaf ranges + family lambdas and binds them
from `family_formulas(fam, ASOF)`. Within-row date math (months/headroom/window/status)
stays local (keys on the radar's own column letters). Verified: radar sheet XML
**2651 formulas, identical to the pre-refactor baseline** (`diff == True`).

### 3. Calendar rewritten — `model_recompete_calendar.py`
Every numeric cell is now a formula or honest blue input. Table grew to **B8:R172
(17 cols × 164 rows)**, **1476 formulas = 9 formula-cols × 164 rows**. Per the §NEXT
audit table:

| Column | Now |
|---|---|
| Decision date | `cur_end` MAXIFS over Contract Awards `pop_current_end_date` (black) — shared w/ radar |
| Notice-by (est) | `=Decision − 90` (black date) |
| Months to decision | live vs `AS_OF_CELL` (already was; kept) |
| Obligated $M | `obl` SUMIFS over Award Actions `amount` (black) — **identical to radar `obl_f`** |
| Potential end | **NEW col** — `pot_end` MAXIFS `pop_potential_end_date` (black) |
| Option yrs left | `=IF(OR(PE="",DD=""),0,MAX(0,ROUND((PE−DD)/365,0)))` (black int) |
| Open notice (PSC) | COUNTIFS over Pipeline Events (PSC match AND deadline ≥ As-of), `"Y (n)"`/`""` |
| Decision FY | derived from the live Decision-date cell (`MONTH/YEAR`, FY rolls Oct 1) |
| Tenure (yrs) | **handoff option 2** — see below |
| Phase | build-time section label (Forward/Overdue) — coheres with static section order |

**Tenure decision = handoff option 2 (honest blue + black formula).** Added a BLUE
`Incumbent since` column = the build-time chain-root start (walk `pred_of` to root →
`attrs[root]["start"]`). The multi-hop chain walk is the one thing a formula can't
reach, so it is surfaced as `S_DATE_INPUT` (blue). Tenure = `(As-of − Incumbent since)
/ 365.25` (black) and now **re-clocks off the As-of cell** like everything else.
This keeps the predecessor-chain nuance AND obeys the color rule.

Removed the now-dead Python: `_open_notice_pscs`, `tenure_yrs`, `_to_date`, `_dod_fy`,
`_EPOCH`, the `datetime` import. Build-time logic kept ONLY for row sort/grouping +
the forward/overdue split (legitimate build-time concerns) — `asof_ser` survives just
for the split.

## Verification (structural — LibreOffice can't recalc this book)
- Build: **7 sheets, 6 native tables, exit 0**. `t="e"` error-cell scan = **0 on all 7 sheets**.
- Radar: **2651 formulas byte-identical to baseline**; lineage **overdue 124 / superseded 62 / active 40** (unchanged). Calendar split **Forward 40 / Overdue 124 = 164**.
- Spot row Gunderson `W912BU24C0046` — recomputed the live-formula inputs directly
  from the leaf CSVs: decision **2026-07-01**, notice-by **2026-04-02**, Obligated
  **$49.8M**, tenure **2.6y**, Potential end 2026-07-01 → Option yrs **0**, Open notice
  **Y (2)**. Matches the prior session's baked spot-check exactly — the formulas
  reproduce the old numbers, now live.
- Formula cell-by-cell read of rows 9 / 48 / 172 confirms each column's style + reference
  (Decision date→`$U`, Potential end→`$V`, Obligated→Award Actions `$K`, Open notice→
  Pipeline `$K`/`$I`, Incumbent since = blue `S_DATE_INPUT` serial, analyst cols blank `S_TEXT_INPUT`).

## One deliberate carve-out (per the handoff)
The whole-workbook sweep found the **only** remaining baked-black numerics are
`fiscal_year` on **Award Actions** and **Pipeline Events** — exactly the cells the §NEXT
handoff lists as the accepted "fiscal_year derived black" state ("confirm none slipped").
They are a deterministic source-derive (FY = f(date) off the blue source date), so black
honestly reads as "derived, not input." Left as-is per the handoff. If strict purity is
wanted they can become `=IF(MONTH(date)>=10,YEAR(date)+1,YEAR(date))` via `_flat`'s
`formula_cols` — but that adds ~7.8k formulas to the 14 MB Award Actions sheet for a
trivial derive; not done.

## Files
Created: `workbook_army/sheets/_radar_formulas.py`. Changed:
`workbook_army/sheets/model_recompete_radar.py` (consume shared builders),
`workbook_army/sheets/model_recompete_calendar.py` (full formula-driven rewrite; +2 cols
`Incumbent since` / `Potential end`, 15→17 cols).
Output: `projects/army/20260620_US Army Market Mapping_vS.xlsx`.

## Still deferred (lower priority — unchanged from prior handoff)
Confidence auto-derive (blank), deeper option structure (base+option extraction;
option-yrs is still `(potential−current)/365`, notice-by a flat −90d), deck slide +
Overview scaffold, analyst tagging (Confidence/Pursuit/program/capability_node).

## How to re-run
```bash
cd projects/army/workbook && python3 build_workbook.py   # → 7 tabs, calendar now formula-driven
```
