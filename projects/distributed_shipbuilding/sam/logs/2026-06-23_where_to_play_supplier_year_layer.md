# 2026-06-23 — Where-to-Play layer: a Program × Archetype × FY analytical spine for the SAM workbook

Implemented an external design review's "where to play" recommendation on
`award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The review found the workbook had the right ingredients
but could not assemble a defensible "where to play" argument, because its three core views lived
at **incompatible grains**: concentration was lifetime Program × Domain, supplier activity was
portfolio-wide and lifetime, and domain/output mix was Program × FY. Those cannot be combined to
say a vertical is incumbent-heavy, open, or attractive. Separately, the old "Observed Activity
Profile" (`MAX(breadth tier, duration tier)`) was an *activity-intensity* measure mislabeled as
supplier recurrence/incumbency.

The fix: two new layers at **one Program × Archetype × FY grain**, with the Executive Summary
re-cast as a thin presentation layer over them; the existing intensity and lifetime-concentration
tabs reframed (not deleted) so their labels match what they prove.

Workbook goes **19 → 21 sheets, 15 → 17 native tables**. Build clean (**0 XML errors, 0
error-literal cells**); house-style linter **0 failures, 0 warnings**; **full headless LibreOffice
recalc is 0-error workbook-wide** with every arithmetic invariant satisfied (this also discharges
the standing Subaward Activity recalc gate from prior logs).

**Scope was confirmed with the user up front:** implement the transcript's concrete file-by-file
spec only; fold the recalc gate into this work's verification; deliver as a single batch.
**Deferred (out of scope by the user's call):** CR3, FY2023–25 pooled columns, a top-of-summary
Decision Readout, dual UEI+parent grain on every metric, two-year-incumbent sensitivity, and any
chart.

Everything is **uncommitted working tree** at the time of writing (committed immediately after).

---

## Architecture (clean DAG — no new circular refs)

```
transactions (ddg/virginia/columbia)  ─┐
Supplier Master (parent, D, P @ Prog×UEI)─┤
                                          ▼
              Supplier-Year Activity  (model, NEW)   one row per Program × UEI × Federal FY
                                          ▼
                  Where to Play        (summary, NEW) one row per Axis × Program × Archetype × FY
                                          ▼
              Executive Summary (reordered; reads Where to Play + Supplier-Year Activity)
```

Within Supplier-Year Activity, `Prior-Year Active` / `Earlier-Year Active` reference the same
sheet's `Positive Supplier $M` column for *other* (FY-1 / earlier) rows — a cross-row reference,
not a self-reference, so no circular formula. Every cross-sheet ref uses the bounded
`$first:$last` ranges from the existing `cols` accessors.

**Verified conventions (resolved by reading the code before building):**
- Canonical program key is **`"DDG"` / `"Virginia"` / `"Columbia"`** (Supplier Master `Key` =
  `"DDG|UEI"`; `ddg_program_vendors` passes `program="DDG"`). `"DDG-51"` is a *display* label only.
  The spine stores `"DDG"`; Where to Play shows `"DDG-51"` but `SUMIFS`-filters on `"DDG"`.
- `make_flat_sheet` with an intro lands the header at row 8, first data row at row 9.
- Fiscal constants in `sheets/_fiscal.py`: `TX_FED_FY="Federal FY"`, `TX_REAL="Subaward $ FY2026$"`;
  Federal FY = `y + int(m>=10)` (matches `_integrity` and the new builder).
- Positive-dollar convention: `Positive Supplier $M = MAX(Net, 0)`, matching Domain Concentration.

---

## What changed (13 modified + 4 new)

### A. New data spine
- **`scripts/build_supplier_year_activity.py` (NEW)** — mirrors `build_subaward_activity`'s
  materialize-identity-only pattern. Groups the three transaction CSVs by `(Program, Federal FY,
  UEI)` over **all** fiscal years (FY2022's "first observed" needs full pre-FY2022 history),
  materializing `Program | Federal FY | Subawardee UEI | Distinct Subaward Numbers` and leaving the
  11 formula columns blank. Asserts one row per key.
- **`extracted/supplier_year_activity.csv` (NEW, generated)** — **5,363** supplier-year rows
  (DDG 1,817 · Virginia 2,059 · Columbia 1,487), spanning FY2002–FY2026.

### B. New sheets
- **`sheets/supplier_year_activity.py` (NEW, `model` group, slate tab)** — via `make_flat_sheet`.
  Live columns: `Subawardee Vendor Name`, `Parent Key`, `Capability Domain (D)`, `Primary Output
  (P)` (one `SM Match Row` + INDEX into Supplier Master), `Net Subaward $M` (per-row program's
  transaction-leaf SUMIFS), `Positive Supplier $M`, `Reports`, `Prior-Year Active`, `Earlier-Year
  Active`, `Activity Status` (`Adjustment-only / First observed / Continued / Reactivated`),
  `Active FYs`. Eight hidden helpers carry the per-axis parent-concentration pre-aggregates (D and
  P): `Parent {D,P}-FY $M`, `Parent {D,P} HHI Numerator`, `Parent {D,P} Firm Weight`, plus `UEI
  Positive $ Squared`. Exports `supplier_year_cols`.
- **`sheets/where_to_play.py` (NEW, `summary` group, charcoal tab)** — in-memory spine (no CSV):
  `Axis ∈ {D,P}` × `{Virginia, Columbia, DDG-51}` × `FY2022–25` × `_taxonomy.{DOMAINS,OUTPUTS}` =
  **228 rows**. Every metric is a live `SUMIFS`/`COUNTIFS` over Supplier-Year Activity with shared
  `(program key, FY, axis code)` criteria: `Net Subaward $M`, `Program Share`, `YoY $ Growth`,
  `Active Suppliers`, `Parent Top-1`, `Parent HHI`, `Parent Eff Firms`, `Incumbent Vendors %`,
  `Incumbent $ %`, `Retention %`, `First-observed $ %`, `Reactivated $ %`, and an `Observed
  Structure` 2×2 screen (Thin observation < 3 suppliers; else Parent HHI ≥ 0.4 × Incumbent $ ≥ 0.75
  → Fortress / Concentrated-rotating / Broad-relationship / Open-dynamic). Exports
  `where_to_play_cols`. Note: share/ratio columns render as decimals (the flat-table builder has no
  percent number format); values are exact and the Executive Summary re-renders them as percents.

### C. Wiring
- **`sheets/_tabs.py`** — `TAB_SUPPLIER_YEAR = "Supplier-Year Activity"`, `TAB_WHERE_TO_PLAY =
  "Where to Play"`, both added to the ≤31-char assertion.
- **`sheets/__init__.py`** — `WHERE_TO_PLAY` registered in **summary** (after Domain
  Concentration), `SUPPLIER_YEAR_ACTIVITY` in **model** (after Supplier Master); groups stay
  contiguous (the packager asserts it).
- **`lib.py`** — imports + calls the 8th integrity assert `assert_supplier_year_activity_spine()`.
  The muted palette already maps `summary`→262626 and `model`→48596B, so the two new tabs colored
  correctly with no palette edit.
- **`sheets/_integrity.py`** — `assert_supplier_year_activity_spine()` rebuilds the
  `{(Program, FY, UEI)}` universe from the three transaction CSVs and asserts the spine matches it
  exactly, no duplicate keys.
- **`scripts/rebuild_all.py`** — new `build_supplier_year_activity` stage after
  `build_subaward_activity`, before `build_ddg_swbs_rollup`; docstring + "8 integrity asserts".

### D. Reframes (labels/framing only; positions & accessors preserved)
- **`sheets/executive_summary.py`** — reordered to answer-first: §1 Scope · §2 Observed SAM by
  program & FY (new `_program_fy_totals`: per-program FY $ + lifetime memo + FY25 active UEIs +
  FY25 share) · §3 Capability Domain mix · §4 **FY2025 where-to-play scorecard** (new
  `_fy25_domain_scorecard`, INDEX/MATCH into Where to Play, percent-styled here) · §5 **Supplier
  continuity by program & FY** (new `_program_fy_continuity` off Supplier-Year Activity:
  incumbent $ share + retention) · §6 Primary Output mix · §7 DDG SWBS mix. Removed the old §3/§4
  lifetime concentration + portfolio-recurrence headline sections and their now-unused accessor
  imports.
- **`sheets/subaward_activity.py`** — reframed to **Historical Activity Intensity**: rewrote the
  docstring, `INTRO`, `CAV1`, and the §1 banner to state it is a descriptive breadth + observed-
  duration measure, **not** annual retention/incumbency (those now live on Where to Play). The
  breadth/duration math, the 4×4 matrix and the block-continuity block are unchanged; all row
  positions and the exported accessors are intact.
- **`sheets/domain_concentration.py`** — renamed the `Contestability` column to **`Observed
  Structure`** with relabeled outputs (`High / Moderate / Lower concentration`, `Check`); updated
  the docstring + caveat to frame it as the **lifetime structural view** and point to Where to Play
  for annual dynamics. (The only consumer of the old `Contestability` header was the removed
  Exec-Summary headline section, so no live ref broke.)
- **`sheets/guide_methodology.py`** — added **§5 Activity and continuity definitions** (active,
  first observed, continued, reactivated, incumbent vendor/$ share, retention, parent
  concentration, and the analyst-defined Observed-Structure thresholds).

### E. Gates
- **`tools/style_audit.py`** — added the 7 new hidden helper headers to `FORBIDDEN_HEADERS` (a
  regression guard that they stay hidden).
- **`validate_workbook.py`** — added `EXPECTED_SHEETS` (21, in order), `EXPECTED_TAB_COLORS`
  (palette anchors incl. the two new tabs), and `EXPECTED_FORMULA_COLS` spot checks
  (`Supplier-Year Activity!Activity Status`, `Where to Play!Observed Structure` carry a live
  formula on row 9). All fold into the structural-report exit code.

### F. Latent-bug fix surfaced by the recalc gate — `sheets/_flat.py`
`override_or_map` / `override_or_map_basis` used `AND(match>0, INDEX(range, match)<>"")`. `AND`
does **not** short-circuit, so `INDEX(range, 0)` was evaluated whenever there was no override
match; on a Supplier Master row **outside** the override range (rows ≥ 300, range ends at 299) that
`INDEX(range, 0)` fails by **implicit intersection** → `#VALUE!`. The workbook built clean (valid
formula strings) but produced `#VALUE!` for ~270 vendors' resolved D/P on actual recalc — and that
cascaded into the program-vendor sheets, Domain Concentration, the mix matrices, and the new
Supplier-Year/Where-to-Play sheets (it was the reason Virginia/Columbia reconciliation was ~20%
short before the fix). Fix: guard the index inside the non-short-circuiting boolean with
`INDEX(range, MAX(match,1))` (the value is irrelevant there since the first `AND` arg is already
FALSE; behavior is identical for every previously-correct row). This is a pre-existing bug, not
introduced by this session — saved as a memory.

**Deviation from the plan:** the plan had `_flat.py` scoped as untouched. The `override_or_map`
fix was required to make the recalc gate (which the user asked to fold in) pass, and to make the
new sheets correct on recalc, so it was applied. It only fixes errors; it changes no
previously-correct value.

---

## Verification (all green)

| Check | Result |
|---|---|
| `python3 scripts/build_supplier_year_activity.py` | **5,363** supplier-year rows, all FYs |
| `python3 build_workbook.py` | exit 0, **21 sheets, 17 native tables**, 8 integrity guards pass |
| `python3 validate_workbook.py` | parts 76, **0 XML errors, 0 error-literal cells, 0 structural-check issues** (sheet set/order, tab palette, new formula columns) |
| `python3 tools/style_audit.py` | **0 hard failures, 0 warnings** |
| Tab placement / colors (openpyxl) | Where to Play (3) charcoal·summary; Supplier-Year Activity (13) slate·model; groups contiguous ✓ |
| **Headless LibreOffice recalc** (soffice, OOXMLRecalcMode=0) | **0 error cells across all 21 sheets** (incl. Subaward Activity — the standing recalc gate) |
| Invariant: incumbent$ + first-observed$ + reactivated$ = 100% | 0 violations (219 active cells) |
| Invariant: retention ≤ 100% | 0 violations |
| Invariant: parent Top-1² ≤ parent HHI ≤ parent Top-1 | 0 violations |
| Invariant: program-share sums to 1.0 per program (D axis, FY25) | Virginia/Columbia/DDG-51 = 1.0000 |
| Invariant: D-axis vs P-axis program-FY net totals match | OK |
| Reconciliation: Where-to-Play net == program-vendor FY totals | exact match, all 12 program×FY cells |
| Exec-Summary presentation layer recalc | §2/§4 scorecard/§5 continuity all resolve to sane in-range values |

---

## Build / verify

```
# from workbook_award_classification_refactor/ (the dir with build_workbook.py):
PYTHONPATH=<repo-root> python3 scripts/build_supplier_year_activity.py   # -> supplier_year_activity.csv
PYTHONPATH=<repo-root> python3 build_workbook.py                         # 21 sheets, 17 tables, exit 0
PYTHONPATH=<repo-root> python3 validate_workbook.py                      # 0 xml / 0 error-literal / 0 checks
PYTHONPATH=<repo-root> python3 tools/style_audit.py                      # 0 failures, 0 warnings

# Recalc gate (no committed harness; soffice forces recalc via a throwaway profile):
#   registrymodifications.xcu: /org.openoffice.Office.Calc/Formula/Load OOXMLRecalcMode=0
#   soffice --headless -env:UserInstallation=file://<profile> \
#     --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir <out> award_classification_refactor.xlsx
#   then openpyxl(data_only=True) -> scan for #DIV/0|VALUE|REF|NAME|NUM|NULL|N/A
```

## Files

- **New (4):** `scripts/build_supplier_year_activity.py`, `extracted/supplier_year_activity.csv`,
  `sheets/supplier_year_activity.py`, `sheets/where_to_play.py`.
- **Modified — sheets/engine (8):** `_flat.py` (override INDEX guard), `_tabs.py`, `_integrity.py`,
  `__init__.py`, `executive_summary.py`, `domain_concentration.py`, `subaward_activity.py`,
  `guide_methodology.py`.
- **Modified — bindings/scripts/tooling (3):** `lib.py`, `scripts/rebuild_all.py`,
  `tools/style_audit.py`, `validate_workbook.py` (4 — counted with the regenerated `.xlsx`).
- **Regenerated:** `award_classification_refactor.xlsx`.

## Carry-forward

- The recalc gate is now a real, repeatable step — see the memory `workbook-recalc-verification`.
  Future workbook changes should run it; the build + linters only check formula strings, not values.
- ⚠️ Still do **not** run `scripts/build_archetype_overrides.py` (clobbers the curated
  `vendor_archetype_overrides.csv`).
- Run `build_supplier_year_activity.py` **before** `build_workbook.py` — the new sheet calls
  `load_table("supplier_year_activity")` at import (same prerequisite as Supplier Master).
- The spine carries **all** fiscal years even though Where to Play renders only FY2022–FY2025.
- Deferred analytics (CR3, FY2023–25 pooled, Decision Readout, dual UEI+parent grain, two-year
  incumbent sensitivity, bubble chart) remain available extensions if wanted later.
- Plan file for this session: `~/.claude/plans/i-want-you-to-distributed-finch.md`.
