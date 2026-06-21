# 2026-06-20 — SAM award workbooks: comparison, audit, and a tentative go-forward plan

SAM-level cross-cutting session (spans both `award_analysis` and `award_classification`), so it lives in a
new `sam/logs/` — mirroring why the artifact it produced, `sam/TENTATIVE_PLAN.md`, sits at the `sam/` root.
No workbook code was changed this session; the outputs are the plan doc and this log.

The living artifact is **`sam/TENTATIVE_PLAN.md`** — read that for the plan itself. This log is the session
narrative: what we compared, what the audit corrected, and the reasoning behind the plan.

---

## 1. What the two SAM workbooks are (the framing the session started from)

- **`award_analysis`** (`20260612_…Award Analysis_vS.xlsx`) — the original **contestability / "where to play"**
  analysis: award timing, waves, concentration, source diversification, cadence. **Frozen since 2026-06-16**
  (last commits were slide-flowchart polish, not analysis). Methodology judged not good enough → restarted.
- **`award_classification`** (`award_classification_refactor.xlsx`) — the go-forward workbook. Today it's a
  **labeling layer** (Domain / Role / Output archetypes + raw transaction port) on the **~$12.49B
  hull-builder subset** of the $13.1B canonical `_corpus`.

User's stated intent: `award_classification` supersedes `award_analysis`; it has the raw data to rebuild the
analysis but currently emits none of the behavioral analytics.

## 2. Audit — what analysis `award_analysis` has that `award_classification` lacks

Mapped both workbooks sheet-by-sheet against their source modules. `award_analysis`'s analytical layer lives
at one grain: the **lane = (PIID × work_type) × fiscal year**. `award_classification` is modeled at the
**entity (UEI)** and **raw transaction** grain with no lane construct and no time axis — so it's missing the
whole lane-and-time layer, not just two screens. Specifically absent in classification: FY trend, concentration,
source diversification, wave/cadence engine, periodic-vs-continuous sourcing, the competability signal pack,
the lane abstraction, dimensional rollups (work-type/vessel/PIID), prime-vs-sub role analysis, the live
Assumptions control surface, and tie-out checks. (The by-vendor cut is partially covered — the program-vendor
sheets carry per-UEI $ + records + first/last dates.)

## 3. Intent of `award_analysis`'s "cuts" (so the worth-keeping ideas aren't lost)

The whole workbook is one **contestability funnel**: corpus → supplier-base structure → screens → named
targets, tunable off a live Assumptions tab. The cuts answer four questions per lane: **material?** (sizing
cuts: Program/Work Type/Vessel/PIID/Vendor), **locked or opening?** (Concentration + Source Diversification),
**timeable?** (Wave Cadence / Periodic / Continuous + the wave-detection engine), **incumbent churning?**
(Lane Vendors / Lane Signals / Role). Dimensional cuts triangulate materiality; indicator screens apply the
four tests.

## 4. The three "honesty fixes" worth carrying forward

`award_analysis` (and the 2026-06-20 caveat work) paid the tuition on three artifacts that fake a "where to
play" signal:
- **Censoring** — a first-visible award inside the window may hide earlier history → fake entrant. Guard:
  pre-window record-share diagnostic.
- **Novation** — an incumbent reappears renamed/acquired/re-filed (Timken=Philadelphia Gear; GE "enters" DDG
  machining at $333M). Guard: entrant-credibility $ cap → `credible_entrant` vs `reported-entrant (likely
  incumbent)` (known cost: mislabels Austal, a real entry).
- **Depth** — a share can be one contract deep (Virginia D2 = 40%, but 72% is one NG contract). Guard:
  distinct-contract/vendor depth flag.

## 5. The plan — foundation first, analysis later

User's decision: do the **for-sure foundation work before** the **improved contestability analysis** (the
mirrored-from-`award_analysis` methodology, not yet trusted). Low-regret because none of the foundation work
commits us to the analysis, each item improves the workbook standalone, and deferring the screens defers the
lane-unit decision at no cost.

## 6. Audit of the *current* workbook — corrections (this is the load-bearing part)

An external data-architecture critique (empirically grounded — its data claims verified almost exactly) plus
my own first draft both flagged work that turned out **already done**. Verified against the sheet modules:

- **Already implemented (do not re-litigate):** `Published Subaward Records` (not "Subaward Actions");
  `Predominant Place of Performance (by records)` (the "Domestic or Foreign" rename); `Total Contract Value $`
  is never aggregated (non-issue); dollars already labeled "nominal"; **the full SWBS taxonomy** (legend,
  mapping-method `E/X/C/L/U`, hierarchy, guardrails, methodology §9); and **R (Operating Role) is already a
  defined axis** — the taxonomy is explicitly Domain/Role/Output.
- **I was wrong about:** SWBS ("not built" → only the *application* to DDG rows is missing); R ("just prose" →
  it's a real axis, just not a published column); "deflator must extend to 2001" (alarmist — only ~4 records
  total predate 2013).

### Verified data facts (current `extracted/*.csv`)
20,623 records (DDG 6,380 / Virginia 8,443 / Columbia 5,800); report IDs unique, no cross-file overlap;
1,191 distinct UEIs over 1,685 UEI×program rows; 399 UEIs on >1 program; 458 rows missing primary NAICS;
832 negatives + 2 zeros; date ranges DDG 2001-10-22→2026-05-27, Virginia 2013-01-28→2025-08-22,
Columbia 2016-01-06→2025-02-18 (captions 2013/2016/2016 off by 1/3/0 records — immaterial); one DDG prime
shows 65 distinct Total Contract Values (confirms TCV non-additivity); country codes unstandardized.

## 7. Net plan (see `TENTATIVE_PLAN.md` for detail)

**PART A — foundation, three real items:** (1) month/date dimension → derive both CY and FY + recent-period
provisional flag; (2) **apply** SWBS to DDG transaction rows (taxonomy already done); (3) FY2026$ parallel
column (~2013→2026, floor the ~4 pre-2013 records) — the only "iffy-value" item, payoff mostly the sizing layer.
Optional/minor: parent "standardized"→"observed modal"; place-of-performance value→shares; publish R as a column.

**PART B — deferred analytics** (replaces the earlier sketch, adopts the stronger external design):
concentration-as-a-question + explicit access factor; probability-not-date **buy-window radar** with a backtest
gate; **prime-event-to-subaward lag** as the real predictor (gated on a new prime-award pull); "observed
reported first-tier concentration," never "monopoly"; channel units `D×P` (and DDG `SWBS×P`), not `PIID×work_type`;
dedupe re-filed reports into a **subcontract instrument** for timing; run the month-grain vendor×channel work in
**pandas at pipeline time**, not live Excel panels; carry the three honesty fixes.

**Deliberately NOT doing** (the critique was a data-warehouse spec; this is a curated Excel deliverable):
full normalized model / ~20 typed tabs; SCD versioning columns; live month-grain Excel panels;
`classification_evidence`/`sources` evidence-graph (premature — registry has ~0 source URLs). Kept in reserve:
an exact-string raw-sheet builder (current flat builder coerces dates/money, so "raw" tabs aren't byte-faithful).

## 8. Open decisions / next
- FY2026$ — in the for-sure block or held with the analysis? (recommend hold unless cross-year $ wanted regardless)
- Deflator series (recommend FY25 Green Book Table 5-4 Procurement, project-local, ~2013→2026).
- Publish R as a column? channel/lane unit (`D×P`)? deliverable shape (cross-program D/R/P spine + DDG SWBS appendix)?
- New prime-award pull for the lag model (required for the radar).
- **Definite next step (pending go-ahead):** Phase 0 baseline → Phase 1 (month/CY/FY) + Phase 2 (SWBS apply);
  decide Phase 3 (FY2026$) separately. Nothing implemented this session.
