# 2026-06-21 — Audit response: release-gate fixes (the 7-item review)

Session log AND handoff. Continues the same-day Recompete + customer redesign
(`2026-06-21_recompete_customer_redesign.md`). An independent audit reviewed the EXPORTED
workbook snapshot and judged it "technically credible but not yet a decision-grade Saronic
market model": keep the architecture (contract-family spine, reconciliation, segmentation,
classified timing, money discipline), but fix a set of concrete defects, retire stale
terminology, and wire — not fabricate — the analyst layer. This session executed the agreed
scope in one pass.

Build is green: **19 sheets, 16 native tables, 2 note parts, 0 error cells.** Output:
`projects/army/20260620_US Army Market Mapping_vS.xlsx`. Verification: **`verify_timing.py`
25/25 pass** (was 19; +6 for the in-market predicate + lineage-from-disposition invariant),
**0 `t="e"` cells**, **0 `#REF!`/`#NAME?`/`#DIV0!`/`#VALUE!`/`#N/A`**, all worksheet + styles
XML well-formed, conditionalFormatting emitted before tableParts on both decision sheets.

## Scope decisions taken with the user (before coding)
- **Analyst layer** → build STRUCTURE + readiness metrics only; leave values blank (honest
  `x/y`). Real BD judgment (owners, pursuit access, confidence, milestones, validated
  assumptions) is not fabricated — it would violate the faithful-facts-vs-analyst separation.
- **Queue split** → ONE sheet + a live **Scope** column (not 3 sheets). Filter Scope=Active.
- **Work-package serviceability bridge** → DEFERRED (grain integrity, needs seed
  decomposition). P-5 dedup still done now.
- **Terminology** → fix stale REMNANTS only; keep the `Recompete Research Queue` tab and the
  internal `RECOMPETE_RADAR` / `model_recompete_*` / `_radar_formulas` identifiers.
- **Dropped per user**: freeze panes (also unsupported by the OOXML pipeline), data-validation
  dropdowns, the DRAFT/SEED banner. Low/base/high scenarios deferred with the WP bridge.

## Audit-claim reconciliation (verified against source, not the export)
The audit reviewed an export; several claims had already drifted from the live tree:
- #1 in-market ignores As-of/deadline — **TRUE** (`_radar_formulas.py inmkt`).
- #2 queue "Obligated $M" always the actions sum — **TRUE**.
- #5a Data Freshness static + "Recompete Radar $C$6" — **TRUE** (`data_source_clocks.py`).
- #5b queue footer "43+182" hardcoded — **PARTIAL** (it was `len(forward)/len(overdue)`,
  dynamic at build but not live; added a disclosure rather than a "fix").
- #5c Customer Map counts all families — **TRUE** (register 1,688 vs screen 226).
- #6 P-5 dups — **TRUE exactly**: 7 whole-row + 24 row_hash collisions (48 rows).
- #7 verify_lineage auto-chains "Superseded" — **TRUE**; #7 workbook_core missing — **N/A**
  (export artifact; the package exists in the tree).

---

## Gate 1 — defect fixes

### 1.1 In-market signal + auto-confirm removal (audit #1)
- `_radar_formulas.py`: added `NL_DEADLINE = notice_links_cols("response_deadline")`; `inmkt`
  is now `COUNTIFS(family, fam, confirmed,"Y", response_deadline,">="&asof)>0`. The `asof`
  param (previously received but unused) is now load-bearing. No separate lifecycle column
  exists, so the deadline is the open-notice proxy — same test as Related activity (PSC).
- `aggregate_contracts.py:build_notice_family_links`: **removed** the heuristic that
  auto-confirmed the single top-scored open link. `analyst_confirmed` is now set ONLY by a
  human (preserved via `prior`) or the explicit, curated (empty) `SEED_NOTICE_CONFIRMATIONS`.
  Also cleared the one stale machine-confirmed row already baked into
  `analyst/notice_family_links.csv` (so `prior` can't resurrect it). Fresh build →
  **0 analyst-confirmed links** (the honest default; In-market stays empty until a disposition).

### 1.2 Queue money columns (audit #2)
`model_recompete_calendar.py`: the single misleading **"Obligated $M"** (always the
reconstructed action sum) is replaced by **Selected $M** (green INDEX/MATCH into Contract
Families `selected_measure`/1e6 — the measure that drives materiality/ranking), **Award-reported
$M** (live SUMIFS over Contract Awards `obligation_amount`, reusing `F["obl_award"]`), and
**Recon. $M (actions)** (the original `F["obl"]`). With the existing Coverage + Materiality
basis columns, the ~41 award-fallback rows are no longer misread. `_NCOLS` 30 → 33.

### 1.3 Live-vs-static (audit #5)
- **5a** `aggregate_contracts.py:write_source_clocks` — renamed the `model_as_of` row to
  `data_snapshot` with a note that the EDITABLE clock is a separate live cell;
  `data_source_clocks.py` intro now reads "Timing & Incumbent Screen $C$6" (not "Recompete
  Radar $C$6"). The authoritative editable clock stays the screen `$C$6`, live-linked on
  Overview (`summary_overview.py`).
- **5b** queue footer appends "counts are AS OF THE BUILD As-of; Scope/Phase re-clock live but
  totals + row order only update on the next build".
- **5c** `data_customer_map.py` — the "Vehicles at this office" COUNTIFS is tightened to the
  screened universe: `COUNTIFS(office, off, is_watercraft,"Y", selected_measure,">="&1000000)`
  using `families_cols(...)` + `CFG.MIN_OBLIG`. Header → **"Screened vehicles at office
  (wc >= $1M)"** so it ties to the screen count, not the 1,688-row register.
- **5d** the screen's As-of input note now states physical row order + summary counts are
  fixed at build (re-run to re-sort).

---

## Gate 2 — terminology + retire verifier

### 2.1 Stale-remnant rename (reader-facing only)
"Radar universe" → **"Screened universe"** (`summary_overview.py`, `qa_reconciliation.py` ×5);
"radar floor" → **"materiality floor"** (`data_contract_families.py` intro + docstring);
"Recompete window" → **"Decision window"** column header on the screen (and `RW =
_CL["Decision window"]` keyed reference, + docstring). Verified in the built workbook:
**0** occurrences of any stale reader-facing term; new terms all present.

### 2.2 Retired `verify_lineage.py` (audit #7)
Deleted `workbook/verify_lineage.py` — it auto-chained same-UEI/PSC neighbours and labelled
predecessors "Superseded", contradicting the analyst-confirmed lineage model (and not called
by the build). Its one useful invariant is folded into `verify_timing.py`: supersession comes
ONLY from `analyst_disposition in (Confirmed, Probable)`; a blank disposition is an
evidence-scored CANDIDATE, never a verdict. Asserts: **453** predecessors have only
blank-disposition candidates (NOT superseded); the one curated seed (`W56HZV14C0015` Birdon
C-contract → IDV follow-on) IS superseded; every superseded predecessor is a real family.

---

## Gate 3 — analyst structure + readiness (no fabricated values)

### 3.1 Overview readiness block
`summary_overview.py` new "§3 - Analyst-layer readiness (build-time snapshot)" — Python reads
the analyst CSVs at build (same mechanism as `len(forward)`) and renders honest `x/y`:
- Core families attributed: **1 / 38** · Forward pursuits reviewed: **0 / 43** · Customer orgs
  owned: **0 / 13** · Lineage candidates dispositioned: **1 / 454** · Assumptions
  independently sourced: **0 / 3**.
These read low by design until the analyst pass fills the bridges; structures are wired and
rebuild-durable. (Freshness section renumbered §3 → §4.)

### 3.2 Queue Scope column
`model_recompete_calendar.py` — leftmost live **Scope** column:
`IF(decision<As-of,"Expired-lineage","Active")` (re-clocks live; superseded vehicles already
fold out at build). Intro: "filter Scope = Active for the capture queue." No default applied
filter (filter-criteria/hidden-row emission isn't in the pipeline; AutoFilter stays manual).

---

## Gate 4 — P-5 dedup + conditional formatting

### 4.1 P-5 dedup (audit #6) — `research/budget_materials/extract_budget_cuts.py`
Root cause: line item **`9552ML5355`**'s Recurring-Cost subtotal block is parsed as two
interleaved copies, so each identity (`row_hash` = bli/fy/section/label/role/obs) appears with
a real value and a `0.0` twin. New `_dedupe_p5()`: (1) drop exact whole-row dups (**7**);
(2) fold a `0.0` phantom into its single non-zero twin (**15**); (3) where two DISTINCT
non-zero values share an identity (a genuine parse ambiguity — `prior_years` 192.784 vs 10.131
in FY2026/FY2027), keep BOTH with a collision-safe `row_hash` suffix (`-2`) and **LOG a loud
WARNING** — never silently pick one. Asserts `row_hash` unique afterwards. Result:
**1,272 → 1,250 rows, row_hash unique, 0 exact dups, 2 flagged collisions.**

### 4.2 Conditional formatting — `workbook_core/styles.py` + `primitives.py` + both decision sheets
`styles.DXFS` extended past the reserved `dxfId=0` with 4 background-fill dxfs
(`DXF_ANOMALY`/`DXF_IMMINENT`/`DXF_COVERAGE`/`DXF_INMARKET`); new `primitives.cf_rule()`
builds an expression `<conditionalFormatting>` block. The screen + queue each carry 4 rules:
imminent decision (0 ≤ months ≤ 12), anomaly flag set, incomplete coverage (cov < 1),
confirmed In-market = "Y". Verified: `dxfs count="5"`, 4 CF blocks per sheet, dxfId 1-4,
schema-valid (CF before tableParts).

---

## Verification
1. `python3 research/contracts/scripts/aggregate_contracts.py` → 1,688 families / 226 screen;
   notice_family_links **0 confirmed**; lineage_edges **1 Confirmed** (Birdon seed);
   source_clocks `data_snapshot` row written.
2. `python3 research/budget_materials/extract_budget_cuts.py` → P-5 dedup log (7 exact + 15
   phantom dropped, 2 collisions flagged), 1,250 rows.
3. `python3 workbook/build_workbook.py` → 19 sheets, 16 tables, 2 notes, green guards.
4. `cd workbook && python3 verify_timing.py` → **ALL 25 CHECKS PASSED**.
5. XML scans over the built `.xlsx`: 0 `t="e"`, 0 `#REF!`/`#NAME?`/etc.; all XML well-formed;
   spot-checked formulas resolve — In-market (`COUNTIFS(..., deadline,">="&'…'!$C$6)`),
   Selected/Award-reported/Recon $M, Scope, and the screened-universe office COUNTIFS.

## Critical files
- `research/contracts/scripts/aggregate_contracts.py` — drop notice auto-confirm; `data_snapshot`.
- `research/budget_materials/extract_budget_cuts.py` — `_dedupe_p5()` + hash-uniqueness assert.
- `workbook_core/`: `styles.py` (CF dxfs + `DXF_*` handles), `primitives.py` (`cf_rule`).
- `workbook/workbook_army/sheets/`: `_radar_formulas.py` (inmkt deadline), `model_recompete_
  calendar.py` (money block + Scope + CF), `model_recompete_radar.py` (Decision window + CF +
  As-of note), `data_customer_map.py` (screened office count), `data_source_clocks.py`
  (clock string), `summary_overview.py` (readiness block), `qa_reconciliation.py` /
  `data_contract_families.py` (terminology).
- `workbook/verify_timing.py` — in-market predicate + lineage-from-disposition; **deleted**
  `workbook/verify_lineage.py`.

---

# HANDOFF — what remains

## A. The analyst pass (human; structures wired, values blank/seed today)
The Overview readiness block quantifies the gap and will rise as these fill:
- **`analyst/award_opportunity_attribution.csv`** — only 1/38 Core families attributed; attribute
  more to populate the triage trio + Saronic priority sort.
- **`analyst/recompete_reviews.csv`** — 0/43 forward pursuits reviewed; fill Window / Confidence
  / Pursuit access / program / capability_node / planned RFI-solicitation-award milestones.
- **`analyst/customer_org_map.csv`** — 0/13 orgs owned; fill engagement_status / next_action /
  relationship owner; extend beyond the 13 seeded orgs.
- **`analyst/lineage_edges.csv`** — 1/454 dispositioned; mark Confirmed/Probable/Rejected (only
  Confirmed/Probable suppress a predecessor as Superseded).
- **`analyst/notice_family_links.csv`** — 0 confirmed; set `analyst_confirmed="Y"` on validated,
  still-OPEN links to fire In-market (deadline must be >= As-of).
- **`analyst/market_assumptions.csv`** / **`saronic_relevance.csv`** — replace seed %/probs with
  real, independently-sourced values (0/3 sourced today).

## B. Deferred coding (when prioritized)
1. **Bottom-up work-package serviceability bridge** (audit #6) — decompose each funded line into
   commercial packages (hull / propulsion / autonomy / nav / C2 / payload / launch-recovery /
   sustainment). `analyst/work_package_saronic_route.csv` + `work_packages.csv` exist (2 seed
   rows each) but are NOT surfaced; give work packages their OWN sheet (per-WP grain) rather than
   denormalizing onto the opportunity-grain Market Size.
2. **Low/base/high scenarios** on Market Size (replace the single weighted-pursuit point estimate)
   — deferred with the WP bridge; needs low/base/high assumption sets.
3. **P-5 line item `9552ML5355`** — the duplicate Recurring-Cost subtotal block (prior_years
   192.784 vs 10.131) is flagged in the extract log; resolve against the source PDF and, if it's
   a column-misalignment parse bug, fix `collect_p5_events`/`extract_p5` so the suffix hack isn't
   needed.
4. **FPDS Atom → SAM Contract Awards API migration** (still deferred from Phase 1 decision #4;
   FPDS ezSearch decommissioned 2026-02-24). `pull_sam_contract_awards.py` is the foundation;
   the gap is recent-DoD dollar completeness (SAM Revealed excludes < 90-day DoD awards).

## C. Invariants held (unchanged)
Faithful facts (`workbook/extracted/`, written by the aggregators) vs analyst judgment
(`workbook/analyst/`, seeded-if-absent / never clobbered, merged blue + rebuild-durable). Every
rendered cell is a LIVE formula (black/green) or an honest BLUE input; classified facts (segment,
coverage, agreement type, decision date, tier, cohort) are loaded leaf values. Money discipline
(never sum across amount type; historical obligations ≠ TAM/SAM). Group contiguity
(`_assert_group_blocks`). Single As-of cell re-clocks all timing. `python3` only; verify via
Python replica + `t="e"` scan (LibreOffice can't recalc this book).
