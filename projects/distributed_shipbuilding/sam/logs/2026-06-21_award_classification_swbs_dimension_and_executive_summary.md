# 2026-06-21 — Award-classification workbook: SWBS dimension + Executive Summary (formula-driven build)

User-driven build session on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). Two deliverables, arrived at through several
user-steered pivots: **(1)** a fully formula-driven SWBS (Ship Work Breakdown Structure)
dimension for the DDG-51 program, brought to structural parity with the existing
program-vendor sheets; **(2)** a front-door **Executive Summary** tab. Net result: workbook
grew **13 → 16 sheets**, all new analytics are LIVE formulas (no baked numbers), and the
SWBS dimension now mirrors the archetype dimension's dictionary→leaf→roll-up pattern.

---

## End state — 16 sheets (guide → model → data)

| # | Tab | Group | Role |
|---|---|---|---|
| 1 | **Executive Summary** | guide | NEW front-door dashboard (live) |
| 2 | Taxonomy | guide | |
| 3 | Methodology | guide | |
| 4 | NAICS-6 Archetype Map | guide | archetype dictionary |
| 5 | **HII Work-Item SWBS Crosswalk** | guide | NEW SWBS dictionary (code→SWBS) |
| 6 | DDG Program Vendors | model | |
| 7 | **DDG SWBS by Ship-System** | model | NEW per-subsystem roll-up (per-FY FY26$) |
| 8 | Virginia Program Vendors | model | |
| 9 | Columbia Program Vendors | model | |
| 10 | DDG Subaward Transactions | data | NOW SWBS-tagged (+5 cols) |
| 11–12 | Virginia / Columbia Subaward Transactions | data | unchanged |
| 13–16 | Subawardee UEI Index · Subawardee Parents · Vendor Archetype Overrides · Deflators | data | unchanged |

The SWBS dimension is the structural twin of the archetype dimension:

| Role | Archetype side | SWBS side |
|---|---|---|
| Dictionary (guide) | NAICS-6 Archetype Map | **HII Work-Item SWBS Crosswalk** |
| Transaction leaf (data) | DDG Subaward Transactions | **same sheet, SWBS-tagged** |
| Roll-up, per-FY const-FY2026$ (model) | DDG Program Vendors | **DDG SWBS by Ship-System** |

---

## The arc (pivots matter — they encode the reasoning)

1. **Ask:** add `SWBS` + `SWBS basis` columns to the entity-grain **DDG Program Vendors** sheet.
   **Rejected** — taxonomy guardrail (`_taxonomy.py:254`): *"Grain is the subaward transaction…
   SWBS is never collapsed to one-per-UEI."* A vendor's subawards hit many SWBS groups.
2. **v1 (built then superseded):** a transaction-grain `DDG Subaward SWBS` sheet with SWBS
   resolved in Python and written as static strings. Coverage surfaced the real story →
3. **"Why is almost everything U?"** Answer: U is **65% of records but only 30% of dollars**
   (the documented "~70% of dollars / ~30% of records" property). The unmapped tail is
   low-dollar. Identified a **$691M recoverable pool** in ~15–30 high-dollar codes the
   dictionary left blank but whose component text is unambiguous.
4. **User: centralize + make it formula-driven + add the "C" curated layer + move to `model`.**
   Key enabling finding: **code→subsystem is deterministic in this pull** (0 explicit-vs-modal
   conflicts; only 1 explicit row lacks a code) → the whole thing collapses to ONE code-keyed
   crosswalk (the NAICS-map shape). Decision: **fold basis E into X** (the crosswalk's observed
   subsystem IS derived from the explicit rows), costing 1 row.
5. **Executive Summary** built (§1–§4): scope/caveat (static) + program totals + Capability-
   Domain and Primary-Output mix-by-FY matrices (live).
6. **SWBS parity ask:** make the SWBS sheet look like a program-vendor sheet (per-FY FY26$).
   Constraint taught: **per-FY columns need a multi-FY grain** (a transaction is single-FY), so
   the SWBS sheet must roll up — to the **SWBS subsystem** (the vendor-analog). And **don't
   maintain a separate SWBS transaction sheet** — tag the real one. Final structure above; §5
   added to the Executive Summary.

---

## Decisions locked

- **Single crosswalk, code-keyed**, not a separate codebook + per-row explicit parse (justified
  by the 0-conflict / 1-row finding). Basis values: `X · code crosswalk (observed)`,
  `C · curated inference`, `U · no SWBS evidence`, `—` (non-HII).
- **Roll-up grain = SWBS subsystem** (~47 + a `U00` row); Executive Summary §5 rolls it to
  **major group**. (Subsystem = atomic, the true parallel to "vendor"; major group = the §5 roll-up,
  the parallel to "domain".)
- **SWBS scope = HII-Ingalls DDG only.** GD-BIW subawards carry no SWBS → blank `SWBS Subsystem`
  (auto-excluded from real-subsystem totals); HII-unmapped → `U00`. §5 denominator is therefore
  HII-Ingalls-only and **differs from §3/§4** (which include BIW) — captioned on the sheet.
- **Tag the real transactions sheet** (no redundant SWBS tx sheet). The slim v1 sheet was deleted.

---

## Curated "C" layer (lifts coverage ~70% → 82.4% of HII $)

`extracted/swbs_curated_c.csv` — 22 hand-authored code→subsystem entries, each verified against
`swbs_hierarchy.csv` + the code's `top_components`. Recovers **$426M / 427 records**. Examples:
`03003-01/05002-01 shaft/struts→243` · `03019-01 SSGTG→311` · `04018-01 P&L panels→324` ·
`02002-02 A/C→514` · `03174-* fire/halon→555` · `01021/01022/01027 doors/hatches/scuttles→167` ·
`01043-02 deck covering→634` · `01039-* commissary→651`. **Medium-confidence (flagged for review):**
`01549-02 hangar doors→588` (vs 167), `05011-01/05055-01 rudder→561` (vs 568), `02517-01 vent→512`,
`01041-01 reefers→516`, `09108-01 blast&paint→631`. Generic "valve" / blank-description codes were
**deliberately left U** (honest unknowns).

Coverage (verified, nominal HII $): **X+C = $2,808M = 82.4%**; U00 = $599M = 17.6%; total HII $3,407M.
By record: 1,186 explicit (E, now folded into X) + 571 X-crosswalk + 427 C; 5,900 HII / 480 BIW of 6,380 tx.

---

## How the three SWBS layers wire (all verified in the built .xlsx)

- **Leaf — DDG Subaward Transactions** (+5 cols appended, cols **AZ–BD**): `HII Work-Item Code` (AZ,
  materialized) + `Builder` (BA, materialized) are leaves; `SWBS Subsystem` (BB) / `SWBS` (BC) /
  `SWBS basis` (BD) are **crosswalk-lookup formulas**, Builder-gated. 19,140 such formula cells.
  e.g. `=IF($BA9<>"HII-Ingalls","",IFERROR(INDEX(Crosswalk!$C…,MATCH($AZ9,Crosswalk!$B…,0)),"U00"))`.
- **Roll-up — DDG SWBS by Ship-System**: per-FY = **date-bounded `SUMIFS` over the tx leaf keyed on
  `SWBS Subsystem` ($BB) × the Green Book deflator** — byte-for-byte the program-vendor `_fy_sumifs`,
  subsystem instead of UEI. 720 per-FY formula cells (48 rows × 15 FY). Guard: FY block I:W.
- **Executive Summary §5**: `SUMIFS` over the roll-up's per-FY columns by `SWBS Major Group`, rows =
  the 12 SWBS groups + U00, columns sum to 100%, + a live `SWBS coverage` line
  (`=1-SUMIFS(SubawardM, MajorGroup,"U00")/SUM(SubawardM)`). 49 SUMIFS cells.

§3/§4 (Capability Domain / Primary Output) are `SUMIFS` over the three program-vendor sheets'
**existing** per-FY const-FY2026$ columns by the resolved D/P code (`AB`/`AD`), programs side-by-side
(FY22–FY25), % body + a `Total $M (FY26$)` row. 228 SUMIFS + 18 headline cells.

---

## Key technical facts & gotchas (so they aren't relearned)

- **Deflation is deflation-invariant for share cells.** Within one federal FY the Green Book factor
  is a single constant, so it cancels in numerator÷denominator → the % matrices need NO deflation;
  only the `Total $M (FY26$)` rows multiply by the FY factor. Saved a lot of formula complexity.
- **`build_program_transactions.py` is BROKEN** (pre-existing, unrelated): `load_scope` reads
  `tam/ddg/extracted/nc_scope_summary.json`, which the `tam/` restructure relocated → can't
  regenerate the canonical tx CSV from raw JSON. **Workaround:** `scripts/tag_ddg_transactions_swbs.py`
  augments the *committed* CSV in place (join the SWBS package by `Subaward Report ID`; idempotent).
  **Run order when the scope path is fixed:** `build_program_transactions.py ddg` → `tag_ddg_transactions_swbs.py` → `build_workbook.py`.
- **The HII work-item code cannot be parsed in an Excel formula** (NNNNN-NN buried in free-text at
  varying positions; packager avoids dynamic-array regex for portability) → it MUST be materialized;
  everything downstream (subsystem/SWBS/basis) is then a crosswalk lookup.
- **`_taxonomy.py` is a pure-constants leaf** (only `from __future__ import annotations`) → build
  scripts load it standalone via `importlib.util.spec_from_file_location` to single-source
  `SWBS_GROUPS` / `SWBS_MAPPING_METHOD` without importing the whole `sheets` package.
- **This packager ignores merged cells** (`worksheet(..., merges=…)` is a no-op). Exec-summary
  program-group headers therefore put the program name in each 4-FY block's first column.
- **D/P columns store bare codes** (`D1`, not `D1 Hull…`), so `SUMIFS(...,"D1")` exact-matches
  cleanly (verified before writing 228 formulas).
- **SWBS code exceptions** handled in `major_bucket()`: `730→X00` (Noise & Vibration, cross-cutting),
  `351→L00` (legacy); nomenclature lookup tries `NNN00 → NNN0 → NNN` (covers 234→23400, 730→7300).
- **Program-vendor `cols` accessors were exported** (`_cols` → `ddg_pv_cols`/`virginia_pv_cols`/
  `columbia_pv_cols`) so the Executive Summary can reference their per-FY + D/P ranges; the DDG tx
  sheet exports `ddg_tx_cols`; crosswalk exports `swbs_xwalk_cols`; roll-up exports `swbs_rollup_cols`.

---

## Files

**New scripts** (`scripts/`): `build_swbs_crosswalk.py` (X from dict modal + C from curated → crosswalk
CSV, display composed with exceptions); `build_ddg_swbs_rollup.py` (per-subsystem spine from the
crosswalk + U00); `tag_ddg_transactions_swbs.py` (augments the DDG tx CSV with the SWBS tag).
**New sheet modules** (`sheets/`): `executive_summary.py`, `hii_swbs_crosswalk.py`, `ddg_swbs_rollup.py`.
**New extracted CSVs:** `swbs_curated_c.csv`, `hii_swbs_crosswalk.csv`, `ddg_swbs_by_subsystem.csv`.
**Changed:** `ddg_subaward_transactions.py` (+5 SWBS cols, guard 50→55 + AZ/BA assert), `_flat.py`
(`swbs_value`/`swbs_basis`/`swbs_subsystem` formula helpers), `ddg/virginia/columbia_program_vendors.py`
(export cols accessors), `_tabs.py`, `__init__.py`, `extracted/ddg_subaward_transactions.csv` (tagged).
**Deleted:** `sheets/ddg_subaward_swbs.py`, `scripts/build_ddg_swbs_transactions.py`,
`extracted/ddg_subaward_swbs.csv` (the superseded v1 transaction-grain sheet).

**Build:** `python3 build_workbook.py` → `award_classification_refactor.xlsx`, 16 sheets, 13 native
tables, all assertions pass (group contiguity, width/ncols, tab-name ≤31, dedup, M:AA / I:W / AZ:BA guards).

---

## Carry-forward

- **Generator dependency, unresolved:** `build_program_transactions.py` still can't run until the
  `tam/ddg/extracted/nc_scope_summary.json` path is restored. Everything here builds off the committed
  tx CSV + the idempotent tagger; re-run the tagger after any base-CSV regen.
- **Medium-confidence C entries are open to review** in `swbs_curated_c.csv` (hangar doors 588 vs 167;
  rudder 561 vs 568; etc.). Edit → `build_swbs_crosswalk.py` → `build_workbook.py` and the whole chain
  (tx tags → roll-up → §5) updates live. ~15–30 more long-tail codes could be curated for higher coverage.
- **Numbers are Excel-computed** (formulas, not cached). The structure/ranges are verified, but the
  workbook should be eyeballed once in Excel for: §2 Earliest/Latest (MIN/MAX over date columns — clean
  if every recipient has dated records, which they do), and the §5 vs §3/§4 DDG-total difference
  (expected: §5 is HII-Ingalls-only).
- **SWBS is HII-Ingalls/DDG-only by design** — Virginia/Columbia carry no SWBS equivalent; never compare
  SWBS across programs (taxonomy guardrail).
- **Plan file:** `~/.claude/plans/i-want-to-add-nifty-puzzle.md` holds the v2 SWBS plan (pre-Executive-
  Summary / pre-parity-rework); this log supersedes it.
