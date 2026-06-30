# 2026-06-29 — DDG-51 subaward→hull linkage layer (build + live-formula refactor)

Built a **DDG-51 subaward-to-hull linkage layer** in the SAM workbook
(`sam_awards_data/workbook_award_classification_refactor`,
`20260620_Distributed Shipbuilding Master SAM_vS.xlsx`), answering a manager's two questions:
(1) connect subaward records to the hull numbers built, and (2) frame HII's construction naming
hierarchy. Driven by `ddg51-subawards-and-construction-hierarchy-transcript.md`. The session
covered Phase 1 (the layer), a stale-path fix to the offline build chain, a date-display fix, and
**Phase 1.5** (converting the hull classification from static-generated to **live Excel formulas**
after an external review, plus a finer vendor×hull×SWBS tab).

Core methodology constraint, honored throughout: **never force one subaward onto one hull.**
Attribution is two-layer (PIID→hull *family* + direct hull text) and confidence-scored (A/B/C/D/X),
with conflicts held out of the roll-ups, not hidden.

Workbook went **21 → 30 sheets** (9 new DDG hull tabs). Build clean; house-style linter **0
warnings** (2 pre-existing Supplier Master failures only, untouched); **full headless LibreOffice
recalc 0-error workbook-wide**, every arithmetic invariant satisfied. The light module-cost bridge
tab was added; **TAM untouched**. Lifecycle attribution deferred to a later phase per the user.

---

## 1. What the layer answers (the numbers)

Validated against the live recalc. The full DDG subaward universe is **$4,028.2M FY2026$ / 6,020
records** (reproduces the transcript's ~$4.03B). Hull attribution splits by evidence grade:

| Grade | Meaning | Records | FY2026 $M |
|---|---|---:|---:|
| `A` | official exact — single-ship PIID | 477 | 69.0 |
| `B` | in-family direct subaward text | 1,903 | 1,200.6 |
| `C` | prime-requirement text only | 2,474 | 1,787.9 |
| `D` | PIID-family only | 1,103 | 965.2 |
| `X` | conflict / multi-hull (excluded) | 63 | 5.4 |
| **Total** | | **6,020** | **4,028.2** |

Exact-hull attribution (A+B) = **2,380 rows / $1,269.7M** (~31.5% of DDG subaward $). The honest
headline for the manager: *exact where the evidence supports it, family-level otherwise, exceptions
exposed* — not a complete hull-by-hull accounting. The **DDG Hull Coverage** tab makes that split
visible so the assigned-hull roll-ups are never mistaken for the whole universe.

**The conflict story (grade X):** 61 of the 63 X rows are out-of-family direct hulls — almost all
`REBUY` orders citing a part's *origin* hull (e.g. `REBUY S012 T-386585 DDG119` under the
*DDG 128-and-follow* MYP `N0002418C2307`), not the ship being built. These carry a blank
`Assigned Hull`, never roll up, and surface in **DDG Hull Exceptions** for review.

---

## 2. The nine new tabs

| Tab | Group | Role |
|---|---|---|
| `Mapping - PIID to Hull` | inputs | curated PIID → hull family — the SINGLE source of truth |
| `DDG Hull Master` | inputs | one row per hull: builder, PIID, block/MYP, Flight, award FY |
| `DDG Hull Spend Summary` | model | assigned subaward $ per hull (exact A/B only) |
| `DDG Hull Coverage` | model | exact vs inferred vs conflict $ across the whole universe |
| `DDG Hull x SWBS` | model | HII hulls × SWBS major group |
| `DDG Vendor x Hull Exposure` | model | vendor × assigned hull (long-format) |
| `DDG Vendor x Hull x SWBS` | model | vendor × hull × SWBS subsystem (HII; Phase 1.5) |
| `DDG Hull Exceptions` | model | conflict / multi-hull review queue |
| `Hull Mapping Methodology` | guide | the two-layer method + confidence grades |

Two curated CSVs are **hand-maintained inputs** (NOT regenerated): `ddg_piid_hull_map.csv` (8 in-
scope DDG PIIDs → families, from HII supplier-procurement PDFs + SAR/MSAR + USNI) and
`ddg_hull_master.csv` (35 hulls, confidence-graded). DDG 150 is carried as an unvalidated outlier —
in Hull Master as "Needs validation", absent from every PIID family, so the one row naming it lands
in the exception queue.

Module-cost workbook got one light **`SAM-to-Module Bridge Notes`** tab (guide): SWBS is a
functional/system taxonomy; module / grand block / structural unit is a physical/production (PWBS)
breakdown — subaward text supports SWBS/vendor/timing/hull, not the physical module. Cites the
NSRP-0164 / IHI PWBS lineage.

---

## 3. Mechanism — mirrors the SWBS dimension (regex materialized, classification live)

The hull tag follows the established SWBS pattern. Two halves:

**Materialized (Python — regex can't be an Excel formula).** `scripts/tag_ddg_transactions_hulls.py`
appends 4 columns to `ddg_subaward_transactions.csv`: `Direct Hull Text` / `Direct Hull Count`
(hulls scanned from Subaward Number + Description) and `Prime Requirement Hull Text` / `... Count`.
Regex `\bDDGs?[\s\-]?(\d{3})\b` limited to hulls 100–160 (so "DDG-51 class" / "DDG 1000" never
match), plus a conservative shorthand expander for `128/129`, `128, 129 and 131`, `128 & 129` (one
row: `DDG121/128`); no numeric-range expansion (zero `117-125`-style tokens occur). Idempotent: drops
and re-derives its own columns. Also writes the `ddg_hull_exceptions.csv` sidecar.

**Live (Excel — Phase 1.5).** The five classification columns — `PIID Candidate Hulls`,
`Assigned Hull`, `Hull Assignment Scope`, `Hull Assignment Basis`, `Hull Confidence` — are **live
formulas** on the transaction sheet (`sheets/_hulls.py`), resolved off the curated
`Mapping - PIID to Hull` sheet. A hidden `PIID Map Row` helper does the MATCH once; `PIID Map Kind`,
`PIID Candidate Hulls`, and a boolean `Hull In Family` resolve off it; the visible classification is
nested IFs reproducing the Python rule cell-for-cell. The roll-ups SUMIFS over these (now-formula)
columns. **So editing the PIID map inside Excel flows through to the transaction sheet and every
roll-up** — the change an external review (and the user) asked for.

The in-family test is a **space-padded SEARCH**: `ISNUMBER(SEARCH(" "&hull&" "," "&family&" "))`.
Hull strings are 3-digit `DDG NNN`, ` / `-joined, so padding makes membership delimiter-safe (no
"DDG 11" matching "DDG 119"); `ISNUMBER` swallows the `#VALUE!` SEARCH returns on a miss.

**Single Python source of the rule:** `scripts/_hull_logic.py` (`parse_hulls` / `resolve` / `load_map`),
imported by the tagger (exception log) and `build_ddg_vendor_hull.py` (the generated spines, which
need the assignment resolved at build time). The Excel formulas are the parallel translation;
the recalc QA below reconciles the two.

**Column layout** on the tx sheet: `[50 raw FSRS][5 SWBS][4 hull regex][12 sheet-only formula]`
= **71 columns** (the formula block = SWBS match-row helper + 3 hull helpers + 5 hull classification
+ 3 fiscal). 3 hull helpers hidden.

### Confidence / assignment rule (Python `resolve`, reproduced by the formulas)
- single-ship PIID → the ship (grade **A**), unless direct text names a *different* hull → conflict (**X**).
- multi-hull family, one in-family direct hull → that hull (**B**); out-of-family → conflict (**X**); >1 direct → multi-hull (**X**).
- no direct hull, prime-requirement names a hull → family-level (**C**); else PIID-family-only (**D**).
- `Assigned Hull` is non-blank ONLY for A/B.

---

## 4. Vendor×Hull and Vendor×Hull×SWBS (the manager's literal question)

`build_ddg_vendor_hull.py` emits two generated spines (re-deriving `Assigned Hull` via
`_hull_logic`, since it's no longer in the CSV); every $/record/date column is a live formula:

- `ddg_vendor_hull_exposure.csv` → **DDG Vendor x Hull Exposure** (1,193 rows / 281 vendors /
  24 hulls). Grain (UEI × assigned hull); a 2-criteria SUMIFS keyed on UEI + Assigned Hull; carries a
  predominant SWBS group.
- `ddg_vendor_hull_swbs.csv` → **DDG Vendor x Hull x SWBS** (1,296 rows, HII-only). Grain (UEI ×
  hull × SWBS subsystem); a **3-criteria** SUMIFS keyed on UEI + Assigned Hull + SWBS Subsystem.
  Refines the predominant-SWBS collapse down to subsystem detail (e.g. Timken Gears / GE /
  Rolls-Royce propulsion work on specific recent hulls). HII-only because GD-BIW carries no SWBS.

SWBS subsystem / major-group labels come from the HII work-item code crosswalk (the CSV's SWBS
columns are blank formula placeholders).

---

## 5. Integrity guards

Two build-stopping guards, wired into `lib.build()`:
- `assert_hull_piids_mapped` — every HII-Ingalls DDG transaction PIID is in the PIID map (mirror of
  `assert_piids_in_manifest`).
- `assert_hull_map_master_consistent` (Phase 1.5, replacing the old assignment-level check that read
  the now-formula columns) — every `Candidate Hulls` token has a Hull Master row, and every
  single-ship PIID lists exactly one candidate. These validate the inputs the live formulas depend
  on; the conflict-aware formula cannot itself assign out-of-family.

---

## 6. Two infrastructure fixes (this session)

**Stale offline-build paths.** `tag_ddg_transactions_swbs.py`, `build_ddg_swbs_rollup.py`, and
`build_swbs_crosswalk.py` hardcoded `sam/award_classification/...`, the directory's pre-rename name
(now `sam/sam_awards_data/...`) — they'd fail if re-run. Repointed all three to the `_paths.py`
anchors (derived from `__file__`); fixed the stale `_paths.py` comment. Verified each runs **and
produces byte-identical output** (deterministic, no drift). `build_program_transactions.py` is NOT
a stale-path victim (already correct path, corpus imports resolve). New hull scripts use `_paths`
throughout. New stages wired into `rebuild_all.py`.

**1900-epoch dates.** `MINIFS`/`MAXIFS` over an empty set return 0 → a date format renders
`1900-01-00`. Hit the BIW hulls (+ DDG 150) on Hull Spend Summary (no assigned subawards). Added
`first_last_or_na()` to `_fiscal.py` (COUNTIFS guard → "n/a"); applied to Hull Spend's First/Last.
Workbook-wide scan confirmed no other tab was affected (every other roll-up row has ≥1 record).

---

## 7. Verification

- **Build clean** (exit 0; all integrity guards pass; width assert 71).
- **Live formulas reproduce the materialized values exactly** (recalc): A=477, B=1903, C=2474,
  D=1103, X=63; 2,380 assigned; Coverage total $4,028.2M, exact A+B $1,269.7M. **0 formula-error
  cells, 0 1900-epoch cells** workbook-wide.
- **Roll-ups reconcile**: Hull Spend $1,269.7M = Vendor×Hull $1,269.7M = Coverage A+B; Hull×SWBS
  $1,268.4M = Vendor×Hull×SWBS $1,268.4M (HII portion; differs from $1,269.7M by the $1.2M lone BIW
  assigned hull). Hull×SWBS group columns sum to each row's Total for every hull.
- **Live-edit proof** (the decisive Phase-1.5 test): edited `Mapping - PIID to Hull` cell
  `N0002411C2309` candidate `DDG 113 → DDG 199` and recalced — 164 rows reassigned to `DDG 199`, the
  62 rows naming "DDG 113" in text correctly flipped to conflict/blank (113 left the family), and the
  Hull Spend `DDG 113` row dropped to $0. The map drives the workbook.
- **House-style linter**: 0 warnings (2 pre-existing Supplier Master failures only).
- **Tagger idempotent** (re-run → still 59 CSV columns).

---

## 8. File inventory

**New** — `scripts/_hull_logic.py`, `scripts/tag_ddg_transactions_hulls.py`,
`scripts/build_ddg_vendor_hull.py`; `sheets/_hulls.py`, `sheets/ddg_piid_hull_map.py`,
`sheets/ddg_hull_master.py`, `sheets/ddg_hull_spend_summary.py`, `sheets/ddg_hull_coverage.py`,
`sheets/ddg_hull_swbs.py`, `sheets/ddg_vendor_hull.py`, `sheets/ddg_vendor_hull_swbs.py`,
`sheets/ddg_hull_exceptions.py`, `sheets/hull_mapping_methodology.py`; curated
`extracted/ddg_piid_hull_map.csv` + `ddg_hull_master.csv`; generated `ddg_hull_exceptions.csv`,
`ddg_vendor_hull_exposure.csv`, `ddg_vendor_hull_swbs.csv`; module-cost
`workbook_ddg_module_cost/sheets/sam_module_bridge.py`.

**Modified** — `sheets/ddg_subaward_transactions.py` (4 regex + 8 hull formula columns),
`sheets/_fiscal.py` (`first_last_or_na`), `sheets/_integrity.py`, `sheets/_tabs.py`,
`sheets/__init__.py`, `lib.py`, `tools/style_audit.py`; `scripts/rebuild_all.py`, `_paths.py`,
`tag_ddg_transactions_swbs.py`, `build_ddg_swbs_rollup.py`, `build_swbs_crosswalk.py`;
`extracted/ddg_subaward_transactions.csv`; module-cost `sheets/__init__.py`, `sheets/_tabs.py`.

Additive and non-destructive — no raw-pull FSRS column overwritten. TAM untouched.

## 9. Deferred / declined
Lifecycle-stage attribution + per-hull milestone dates (a later phase, once dates populate Hull
Master); the lifecycle-keyed vendor-hull timeline; physical module/grand-block attribution from
subaward text. Review polish the user declined this pass: a louder DDG 150 flag, promoting Hull
Master `Source URL` to a visible column (it's a hover note), and converting DDG Hull Coverage to a
native table (it keeps its hand-built total row).
