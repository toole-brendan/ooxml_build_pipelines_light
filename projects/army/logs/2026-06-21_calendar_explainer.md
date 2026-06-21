# 2026-06-21 — Recompete Calendar: how-it-works walkthrough (no code change)

Read-only study session. Goal was a truthful, manager-ready explanation of how the
**Recompete Calendar** works — what it shows, where the numbers come from, and (just as
important) which numbers are *inferences* vs ground truth. No files changed; this log
captures the explanation so it can be reused.

Studied the actual source, not just the prior handoff:
`workbook_army/sheets/model_recompete_calendar.py`,
`workbook_army/sheets/_radar_formulas.py`,
`workbook_army/sheets/model_recompete_radar.py` (`load_families` / `_build_lineage`).

## What the sheet is (one line)
A forward-looking, date-ordered list of existing Army watercraft contracts coming up for
re-award — "what's coming up and when." It's the actionable projection of the Recompete
Radar (Radar = full $-ranked inventory; Calendar = the live, upcoming tails).

## Data spine
Every cell is a LIVE formula over three raw data tabs in the same workbook — the calendar
stores no copy of its own:
- **Contract Awards** — the contracts + period-of-performance end dates
- **Award Actions** — obligation transactions (the dollars)
- **Pipeline Events** — open SAM.gov solicitations

## Two core concepts
- **Family / vehicle** — contracts grouped into a vehicle (task orders fold up into the
  parent IDV; key = `parent_idv_piid` else standalone `piid`). One row = one family.
- **Chain tail** — lineage links an expiring vehicle to its replacement (same incumbent
  UEI + same PSC + PoP abutting within 18-mo overlap / 30-mo gap). Superseded families are
  hidden; only the latest live **tail** in each chain shows. Filtered to families with
  ≥ $1M lifetime obligations.

## Layout
- **Forward** section: decision date ≥ As-of, soonest-first.
- **Overdue** section: decision date passed, no detected successor, most-recent-first.

## Column truth table
| Column | What it actually is |
|---|---|
| Decision date | family's latest current-PoP end (forced recompete/option point) — MAXIFS, the spine |
| Notice-by (est) | decision − 90d — a planning rule-of-thumb, NOT a real announced date |
| Months to decision | decision vs As-of |
| Obligated $M | lifetime obligations, SUMIFS over Award Actions |
| Potential end / Option yrs left | run-out if all options exercised; option yrs = (pot−dec)/365 floored 0 |
| Incumbent since (BLUE) | chain-root start; the one value a formula can't walk → honest manual input |
| Tenure (yrs) | (As-of − Incumbent since)/365.25 |
| Open notice (PSC) | weak "is something already moving" — COUNTIFS open SAM notice sharing the PSC |
| Confidence / Pursuit access / Notes | deliberately BLANK — analyst inputs |

## The load-bearing design principle (the credibility story)
Every number is either a **live formula (black)** or an **honest manual input (blue)** —
nothing is a Python-baked value styled to look derived. Payoff: one editable **As-of date**
cell re-clocks every date/tenure/months column; updating the leaves moves the dollar
totals on their own. Calendar + Radar share the same formula definitions
(`_radar_formulas.family_formulas`) so they can never disagree on a number.

Manager framing: *"It's a live, self-recalculating model, not a typed-up static report —
every cell traces to a source record and the whole thing re-clocks off one date."*

## What it is NOT (the honest caveats — each is an inference, not ground truth)
1. **Decision date is a proxy** — inferred from PoP end, not an Army-announced recompete date.
2. **Notice-by is a flat 90-day assumption** — planning estimate, not a solicitation schedule.
3. **Lineage linking is a heuristic** (incumbent+PSC+date-window); can miss or mis-link a
   replacement.
4. **Overdue rows need validation** — expired with no *detected* successor; the heuristic
   may simply have missed it (the sheet caption says as much).
5. **Option yrs left is rough** — date subtraction, not a real base+option parse.
6. **Scope is narrow/deliberate** — Army watercraft only (PSC 19xx / NAICS 33661x / vessel
   descriptors / known primes), ≥ $1M. Not the whole Army universe.

Clean one-liner: *"A live, self-recalculating shortlist of Army watercraft contracts coming
up for re-award, built from federal contracting data. Dates and dollars are real and
traceable; the recompete timing and the contract→replacement links are model inferences an
analyst should validate before acting."*

## No code changes / no build
Read-only. Build state unchanged from `2026-06-20_calendar_formula_driven.md`
(7 sheets, 6 native tables, 0 error cells).

## Possible next (offered, not done)
Open the built `projects/army/20260620_US Army Market Mapping_vS.xlsx` and pull a few real
example rows (names + dates) for a concrete manager walkthrough.
