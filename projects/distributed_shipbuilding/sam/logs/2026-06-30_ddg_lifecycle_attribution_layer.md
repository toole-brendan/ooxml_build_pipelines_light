# 2026-06-30 — DDG-51 construction-lifecycle attribution layer

Built the **lifecycle phase** the 2026-06-29 hull-linkage log deferred: use subaward **timing** —
when each purchase was made vs when each ship was actually being built — to (1) stage-tag the
exact-hull (A/B) dollars by construction phase and (2) **narrow** the family-level (C/D) candidate
hull set toward the ships in build at the purchase date. In the SAM workbook
(`sam_awards_data/workbook_award_classification_refactor`,
`20260620_Distributed Shipbuilding Master SAM_vS.xlsx`). Driven by the zero-context briefing
`/Users/brendantoole/projects3/ddg_hull_lifecycle_attribution_briefing.md`.

The load-bearing discipline, honored throughout: **narrowing the candidate SET is attribution
(evidence); splitting a family dollar across hulls is allocation (modeling) — and is NOT done.** The
evidence layer stays pure; no per-hull dollar is ever assigned to a C/D row.

Workbook went **30 → 35 sheets** (5 new lifecycle tabs). Build clean; structural validation 0 XML
errors / 0 error cells / 35-sheet order correct; **full headless LibreOffice recalc reconciles the
live SUMIFS to the dollar**; tagger + builder idempotent, tx column order stable across re-run.

Scope confirmed with the user up front: **both A/B and C/D rows**; **curate the missing high-$
hulls** (the only schedule file omitted DDG 117–125 ≈ $1.1B + DDG 128); **curate real launch dates →
4 real stages**.

---

## 1. What the layer does — two axes

- **Axis 1 — WHICH STAGE (stage tagging, A/B + C/D).** Compare the purchase date to the hull's build
  schedule → the construction stage it supported. For A/B the hull is known → one clean stage; for
  C/D each candidate hull gets a per-candidate stage.
- **Axis 2 — narrowing (C/D only).** Keep only the family hulls physically in build on the purchase
  date — shrinking the 5–7-hull candidate set. Never collapses to one hull; the C/D `Hull Confidence`
  and blank `Assigned Hull` are untouched, and a **separate** `Lifecycle Confidence` carries timing
  strength.

### The numbers (live recalc)

**A/B exact-hull = $1,269.7M FY2026$ / 2,380 rows**, split across stages (the four partition the total):

| Stage | FY2026 $M |
|---|---:|
| Long-lead | 1,103.1 |
| Construction | 71.2 |
| Outfit / test | 60.5 |
| Post-delivery | 34.9 |
| **Total** | **1,269.7** |

**C/D family-level = $2,753.1M FY2026$ / 3,577 rows**, by timing-narrowing result:

| Narrowing result | Records | FY2026 $M |
|---|---:|---:|
| Single candidate | 41 | 16.0 |
| 2-3 candidates | 379 | 322.7 |
| Still family-level (4+) | 3,023 | 2,104.1 |
| Exception (no window match) | 134 | 310.3 |
| No schedule data | 0 | 0.0 |
| **Total** | **3,577** | **2,753.1** |

By **lifecycle confidence**: High $2.2M / Medium $336.4M / Low $2,104.1M / Flagged $310.3M (= $2,753.1M).

**Honest headline:** timing meaningfully narrows only **~$340M** of the $2.75B to ≤3 candidate hulls
(just $2.2M to High), $310M are *exceptions* outside any hull's window (spares / repair / class-wide
/ mis-dated, surfaced for review), and the bulk stays Low-confidence family-level — long, overlapping
construction windows and missing launch dates for the newer hulls, exactly as the briefing predicted.
Long-lead dominates the A/B split because the newest hulls (DDG 145/146) carry the most exact $ and
have not started fabrication, so all of it is advance/long-lead material (DDG 145 alone = $244.3M,
entirely Long-lead).

---

## 2. The five new tabs

| Tab | Group | Role |
|---|---|---|
| `Lifecycle Methodology` | guide | the 4 stages + windows, the two confidence axes, the wall |
| `DDG Hull x Lifecycle Stage` | model | exact (A/B) subaward $ by hull × build stage (live SUMIFS) |
| `DDG C-D Lifecycle Coverage` | model | family-level $ by narrowing result and by lifecycle confidence |
| `DDG C-D Lifecycle Rollup` | model | one row per C/D tx: the narrowed candidate set + verdict |
| `DDG C-D Lifecycle Candidates` | model | one row per C/D tx × candidate hull (kept AND excluded) |

`Hull Mapping Methodology` §6 "Lifecycle deferred" line updated to point at the new layer.

---

## 3. Mechanism — milestone dates + a pure-Python engine (stage is materialized, not a live formula)

**Milestone dates → the curated `DDG Hull Master`.** Per the briefing, milestone dates belong on the
hull dimension. Added five columns to `extracted/ddg_hull_master.csv`: `Start Fabrication` / `Launch`
/ `Delivery` / `Schedule Confidence` (+ `Milestone Source URL`, folded into a hover note on Schedule
Confidence, mirroring the existing Source-URL-on-Hull note). Curated all 34 in-family hulls
(DDG 113–149) by web research (Wikipedia ship infoboxes, USNI, NVR, HII/GD/NAVSEA releases):
**12 Actual / 22 Projected**, 15 launched. Start Fabrication = published fab-start, else keel-laying
as the proxy (noted per hull). The only prior schedule (`tam/ddg_research/extracted/
scn_li_production_schedule.csv`) had award/start/delivery for **126–156 only** and **no launch** — so
curation filled DDG 113–125 + 128 and every launch date. One correction caught: DDG 127 actually
delivered May 2026 (accelerated), not the schedule's Sep 2026.

**Engine `scripts/_lifecycle.py`** — the date counterpart to `_hull_logic.py`, pure Python (a
date-window join across the hull schedule can't be a clean Excel formula). `load_milestones()`,
`stage_for(date, win)` → `(stage, window_match, date_conf)`, `narrow(family, date, milestones)` →
the candidate analysis. Four stages: **Long-lead** (before start fab) / **Construction** (start→launch,
or →delivery if not yet launched) / **Outfit / test** (launch→delivery) / **Post-delivery**. A hull
not yet launched carries no Outfit window — its in-build spend reads as Construction (no invented
launch). Windows collapse gracefully where a date is missing → `No schedule data`.

**Key subtlety — the 48-month long-lead cap applies to C/D narrowing ONLY, not the A/B stage label.**
For a *known* hull (A/B) a purchase before fabrication is simply its Long-lead, however far ahead (so
DDG 145's $244.3M, ordered ~8 yr before its Sep 2031 fab start, is Long-lead, not "pre-program"). For
C/D *narrowing*, a date > 48 months before a candidate hull's fab start makes that hull an
implausible candidate → `window_match` False, so an early purchase narrows AWAY the latest family
hulls. Implemented as: `stage_for` returns the natural stage always; the cap only flips the match flag.

**Tagger `scripts/tag_ddg_transactions_lifecycle.py`** (runs after the hull tagger) materializes 5
per-row columns onto `ddg_subaward_transactions.csv`: `Lifecycle Stage` / `Lifecycle Stage Basis` /
`Date Source Confidence` / `Narrowing Result` / `Lifecycle Confidence`. A/B rows carry the stage trio
(Narrowing/Confidence blank); C/D rows carry the narrowing pair (Stage blank — per-candidate stages
live on the Candidates sheet); X/unassigned blank. Re-derives the A/B/C/D/X grade with the shared
`_hull_logic.resolve()`. Idempotent.

**Builder `scripts/build_ddg_cd_lifecycle.py`** (after `build_ddg_vendor_hull`) expands each C/D tx
across its full PIID family with `_lifecycle.narrow()` and emits two spines:
`ddg_cd_lifecycle_candidates.csv` (**21,413 rows** = C/D tx × family hull; kept + excluded, each with
a reason) and `ddg_cd_lifecycle_rollup.csv` (**3,577 rows** = one per C/D tx). Same `narrow()` the
tagger uses, so the per-row tx columns and the candidate grain are consistent by construction.

**tx column layout:** `[50 raw][5 SWBS][4 hull regex][5 lifecycle][12 sheet-only formula]` =
**76 columns** (`_WIDTHS` assert 71 → 76). The 5 materialized lifecycle columns are text (default
black), rendered straight from the CSV. The two live roll-ups SUMIFS over them: `DDG Hull x Lifecycle
Stage` on (Assigned Hull × Lifecycle Stage); `DDG C-D Lifecycle Coverage` on Narrowing Result /
Lifecycle Confidence. Constant FY2026$ (`TX_REAL`).

**`scripts/` not importable from the build process** (the taggers use bare `import _lifecycle`/`_paths`
relying on `sys.path[0]`), so the sheet modules hardcode the stage/narrowing label strings and a new
integrity guard is the drift check (the same "two implementations, diffed by a guard" pattern as the
hull recalc QA).

---

## 4. The wall — attribution vs allocation

The candidate and rollup spines carry **no per-hull dollar column**. Every rollup row states it in the
data: `Lifecycle Attribution Scope = "Evidence-based narrowing, not modeled allocation"`, `Assigned
Hull` blank. `Lifecycle Confidence` is a separate axis and never upgrades the A/B/C/D/X hull grade.
Splitting a family dollar across hulls (even-split, or pro-rata to known spend) is modeling — if ever
needed it must live in a separate, clearly labelled modeled view, never mixed into these sheets.

---

## 5. Integrity guards

Two build-stopping guards, wired into `lib.build()`:
- `assert_hull_milestones_monotonic` — every curated hull satisfies Start Fabrication ≤ Launch ≤
  Delivery wherever present (an inverted boundary would mis-tag every purchase against it).
- `assert_lifecycle_columns_consistent` — (a) every materialized Lifecycle Stage / Narrowing Result is
  a KNOWN label (drift vs the sheet SUMIFS criteria); (b) Lifecycle Stage (A/B) and Narrowing Result
  (C/D) are mutually exclusive per row; (c) the rollup is one row per C/D tx and its Narrowing Result
  matches the tx column; (d) each rollup `Timing Candidate Count` equals that tx's TRUE candidate rows;
  (e) the candidate / rollup spines carry no $/allocation column (the wall, asserted).

---

## 6. Verification

- **Build clean** (exit 0; all integrity guards pass, including the two new ones; width assert 76).
- **Structural validation** (`validate_workbook.py`, brought current 21 → 35 EXPECTED_SHEETS, which
  was stale since before the hull-linkage layer): 0 XML errors, 0 error-literal cells, 35-sheet order
  exact, lifecycle SUMIFS spot-checks live.
- **Python reconciliation** (replicating the Deflators factor = index(FY2026)/index(year)): A/B =
  $1,269.7M, C/D = $2,753.1M — both match the briefing to the decimal; every partition (stage /
  narrowing / confidence) sums back to its total.
- **Full headless LibreOffice recalc** (forced via OOXMLRecalcMode=0): the actual workbook SUMIFS
  produce $1,269.7M (Hull × Lifecycle Stage, 4 stages summing to Total) and $2,753.1M (C-D Coverage,
  by result AND by confidence). Spot hulls sensible — DDG 145 all Long-lead; DDG 113/119/125
  (delivered) spread across all four stages incl. Post-delivery.
- **Narrowing spot-checks** — a 2014-03 FY13–17 HII C/D purchase narrows to the 4 early hulls,
  excluding DDG 125 (too early); a Jul 2022 BIW C/D purchase excludes the already-delivered DDG 118
  and keeps the 4 in-build hulls; a single-candidate example pins to DDG 125 (Outfit, High).
- **Idempotent + stable column order** — re-running the full tagger chain (swbs → hulls → lifecycle)
  restores `[50][5 SWBS][4 hull][5 lifecycle]` = 64 CSV cols; rebuild stays green.

---

## 7. File inventory

**New** — `scripts/_lifecycle.py`, `scripts/tag_ddg_transactions_lifecycle.py`,
`scripts/build_ddg_cd_lifecycle.py`; `sheets/lifecycle_methodology.py`,
`sheets/ddg_hull_lifecycle_stage.py`, `sheets/ddg_cd_lifecycle_coverage.py`,
`sheets/ddg_cd_lifecycle_rollup.py`, `sheets/ddg_cd_lifecycle_candidates.py`; generated
`extracted/ddg_cd_lifecycle_candidates.csv` + `ddg_cd_lifecycle_rollup.csv`.

**Modified** — `extracted/ddg_hull_master.csv` (+5 milestone columns, curated),
`extracted/ddg_subaward_transactions.csv` (+5 lifecycle columns); `sheets/ddg_hull_master.py`
(date columns + milestone-source note), `sheets/ddg_subaward_transactions.py` (widths 71 → 76,
docstring), `sheets/hull_mapping_methodology.py` (lifecycle line), `sheets/_tabs.py` (5 tab names),
`sheets/__init__.py` (imports + SHEETS), `sheets/_integrity.py` (2 guards), `lib.py` (call the guards);
`scripts/rebuild_all.py` (2 stages); `validate_workbook.py` (EXPECTED_SHEETS → 35 + lifecycle
formula spot-checks).

Additive and non-destructive — no raw-pull FSRS column overwritten; the hull-linkage layer and TAM
untouched.

---

## 8. Deferred / declined

- **Wider narrowing** would need launch dates for the FY18–22 HII hulls (DDG 133/135/137/139, not yet
  launched) to split their long construction windows; until then most of that block's $1.27B stays
  family-level. Refresh `Schedule Confidence` Projected → Actual as those ships launch/deliver.
- A **fenced modeled-allocation overlay** (per-hull $ split, clearly labelled) — explicitly out of
  scope this pass; the wall is the point.
- The **$310M exception bucket** is worth a follow-on review (are these predominantly spares/repair or
  mis-dated long-lead?) but is correctly surfaced, not hidden.
