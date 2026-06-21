# 2026-06-20 — Recompete Calendar — session log + HANDOFF (next: make the workbook fully formula-driven)

Eleventh session (same day). Built a new **Recompete Calendar** sheet (forward, date-ordered view of
the live recompete targets) and an exact-PSC open-notice flag. Build green (**7 sheets, 6 native
tables**). **This document is a handoff** — the next owner's job is in §NEXT below: make every number in
the workbook a real formula (or an honestly-blue input), because the calendar currently bakes several
values in Python at build time and styles them black as if they were derived. Start by reading §NEXT.

---

## NEXT (the handoff task): make the workbook COMPLETELY formula-driven

**Goal.** Every displayed number must be one of three things, and its font color must say which:
- **BLACK** — a live in-sheet formula (an aggregation / math computed in Excel from on-sheet data).
  Styles: `S_NUM` / `S_INT` / `S_DATE` (and `S_DEFAULT` for derived text).
- **GREEN** — a single-source cross-sheet pull (one value surfaced verbatim from another sheet).
  Styles: `S_LINK_NUM` / `S_LINK_INT` / `S_DATE_LINK`. (Per convention, green is ONLY for single-source
  pulls, NOT for SUMIFS/MAXIFS aggregations — those are black even though they reference another sheet.)
- **BLUE** — a hardcoded input (a value typed/loaded, not computed in-sheet).
  Styles: `S_*_INPUT` (`S_NUM_INPUT` / `S_INT_INPUT` / `S_DATE_INPUT` / `S_TEXT_INPUT`).

**The problem.** The model sheets should be driven by the data leaves (Contract Awards / Award Actions /
Subawards / Pipeline Events) via formulas — every number traceable to a cell on a data sheet, or
honestly blue. The **Recompete Radar already obeys this** (Vehicle type / Task orders / Obligated $M /
Current end / Potential end / Months / Option headroom / In-market are all live COUNTIFS / SUMIFS /
MAXIFS over the leaves). The **Recompete Calendar does NOT** — I computed several columns in Python at
build time and rendered them as static numbers styled black, which lies about their provenance (e.g.
*"Tenure (yrs)"* is a Python chain-walk baked into the cell, not a formula).

### Audit — Recompete Calendar (`model_recompete_calendar.py`), what each numeric column is vs should be
| Column | Today | Make it |
|---|---|---|
| **Decision date** | static serial `a["end"]`, `S_DATE` (black, but baked) | live MAXIFS over `Contract Awards` pop_current_end_date — copy the radar's `cur_end_f` (MAX of MAXIFS on piid and parent). Black. |
| **Notice-by (est)** | static serial `end-90`, black baked | `=<DecisionCell> - 90` (formula off the Decision-date cell). Black. |
| **Months to decision** | LIVE formula off `AS_OF_CELL` | ✅ already compliant — the model to copy. |
| **Obligated $M** | static `total/1e6`, `S_NUM` black baked | live SUMIFS over `Award Actions` amount — copy the radar's `obl_f`. Black. |
| **Option yrs left** | static int, `S_INT` black baked | `=ROUND((<PotentialEnd> - <CurrentEnd>)/365,0)` — needs a (live) Potential-end cell on the row too (add it like the radar). Black. |
| **Open notice (PSC)** | static text `"Y (n)"` | COUNTIFS over `Pipeline Events` (PSC match AND response_deadline >= `AS_OF_CELL`). Black/derived. |
| **Decision FY** | static text label | derive from the Decision-date cell (`=IF(MONTH>=10,YEAR+1,YEAR)` formatted `"FY"&..`). Lower priority (text). |
| **Tenure (yrs)** | static float, black baked — **the flagged example** | see below — genuinely hard; pick an option. |
| Family / Incumbent / PSC / Phase | build-time **text** identity | acceptable build-time (text labels, like the radar) — or pull GREEN from the awards row. Numbers are the priority, not these. |

**Note on row order:** keep the build-time computation for SORTING (forward-by-decision-FY then
overdue) and grouping — that's a legitimate build-time concern. Only the *rendered cells* change from
baked values to formulas (exactly how the radar sorts `selected` build-time but renders live formulas).

### The Tenure (yrs) decision — the example you flagged
Tenure = years the incumbent has held the work, walked back through the **predecessor lineage chain** to
its root, then `As-of − root.start`. A multi-hop chain walk is not expressible as a simple Excel formula.
Three honest options (pick one):
1. **Per-vehicle tenure as a formula (black):** `(As-of − MINIFS(Contract Awards pop_start_date by
   piid/parent))/365`. Fully formula-driven; **loses** the "incumbent has held since the predecessor"
   chain nuance (tenure resets at each vehicle).
2. **Chain-root start as a BLUE input + black formula:** surface the build-time chain-root start date as
   a blue hardcoded cell (a column, or a small helper sheet), then Tenure `= (As-of − <blue cell>)/365`
   is black. Keeps the chain nuance AND obeys the color rule (the un-formulable part is honestly blue).
2. is the better fit for "fully formula-driven with honest provenance"; 1 is simpler. Either is fine —
   what's NOT fine is the current state (a black-styled Python value).

### Enabling work (this is what "make the data sheets the actual source" means)
- The calendar needs the leaf `cols()` accessors (`awards_cols`, `actions_cols`, `pipeline_cols`) and the
  family→formula key (`parent_idv_piid` or `piid`) — same inputs the radar already uses. Import them /
  reuse the radar's formula lambdas (consider factoring `cur_end_f` / `obl_f` / the window logic into a
  shared `_radar_formulas.py` so radar and calendar share ONE definition, the way they now share
  `load_families`).
- Anything a formula genuinely can't reach must be **surfaced onto a sheet as a blue input** (e.g. the
  Tenure chain-root start, option 2). That is the literal meaning of "the data needs to be an actual
  sheet": no model number may depend on a Python value that lives nowhere in the book.

### Whole-workbook sweep (do this, not just the calendar)
1. Scan every sheet for numeric cells whose value is **baked at build time but styled black** → convert
   to a formula or restyle blue. The calendar is the main offender; **verify the radar and the four
   leaves too** (leaves: source numbers should already be blue `*_INPUT`, `fiscal_year` derived black,
   the new `Open?`/`Days to deadline` formulas black — confirm none slipped).
2. Confirm cross-sheet **single-source** pulls (if any) are GREEN, and that SUMIFS/MAXIFS aggregations
   stay BLACK (don't over-green the aggregations).
3. Re-build and spot-check with the source-XML scan (`t="e"` error scan + read a few `<f>` formulas) —
   the established verification path (LibreOffice can't recalc this book; outline-group rows don't
   round-trip to ODS).

### Other deferred punch-list items (lower priority than the formula-driven sweep)
- Auto-derive a first-pass **Confidence** (Confirmed/Strong/Inferred/Speculative) — left blank this pass
  by request.
- **Deeper option structure** (options-remaining / final-option-year / a real option-notice deadline)
  needs base+option extraction; today Option-yrs is `(potential−current)/365` and Notice-by is a flat −90d.
- **Presentation artifact** — deck slide + Overview tab are still scaffold placeholders.
- **Analyst tagging** — Confidence / Pursuit / program / capability_node across radar + calendar.

---

## What was built this session (the Recompete Calendar)
- **Shared family builder:** extracted the radar's family-attributes + lineage into
  `model_recompete_radar.load_families()` → `(attrs, pred_of, succ_of)` (added `pot` = potential-end
  serial). Radar and calendar both call it, so they never disagree on tail-vs-superseded. Verified: radar
  build byte-identical, lineage still **124/62/40**.
- **New sheet `model_recompete_calendar.py` → "Recompete Calendar"** (model group, after the radar): one
  native table, **164 actionable vehicles = chain TAILS** (superseded folded out), ordered **Forward (40,
  by decision FY then date) → Overdue (124, most-recently-expired first)**. 15 columns: Decision FY,
  Phase, Decision date, Notice-by (est), Months to decision (LIVE), Family PIID, Incumbent, Tenure (yrs),
  PSC, Obligated $M, Option yrs left, Open notice (PSC), and blank Confidence / Pursuit / Notes inputs.
  **Caveat carried into §NEXT:** Decision date / Notice-by / Tenure / $M / Option-yrs / Open-notice are
  build-time baked, not formulas — that's the next task.
- **Notice linkage finding:** the 13 open notices are USACE civil-works one-offs, NOT the vehicles'
  recompetes. Exact-PSC matching → a sparse, weak "Open notice (PSC)" flag (~17 PSC-1935 vehicles flag
  `Y (2)`); NAICS matching was noise and dropped. Most rows blank = the accurate signal.

## Verification (this session, structural)
- Build: **7 sheets, 6 native tables**, exit 0. Radar lineage unchanged (124/62/40).
- Calendar table `RecompeteCalendar` = **B8:P172 (15 cols × 164 rows)**, **0 error cells**, phase split
  **Forward 40 / Overdue 124** (matches the standalone Python prototype). Spot row Gunderson
  `W912BU24C0046`: decision 2026-07-01, notice-by 2026-04-02, $49.8M, tenure 2.6y, Open notice `Y (2)`.

## Files created / changed
Created: `workbook_army/sheets/model_recompete_calendar.py`. Changed:
`workbook_army/sheets/model_recompete_radar.py` (extracted `load_families`, +`pot`),
`workbook_army/sheets/_tabs.py` (+`TAB_RECOMPETE_CALENDAR`),
`workbook_army/sheets/__init__.py` (registered the calendar).
Output: `projects/army/20260620_US Army Market Mapping_vS.xlsx` (7 tabs).

## How to re-run
```bash
cd projects/army/workbook && python3 build_workbook.py   # → 7 tabs incl. Recompete Calendar
```
