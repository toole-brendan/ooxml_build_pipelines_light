# 2026-06-20 - NAICS-6 archetype crosswalk sheet + override-first archetype wiring (handoff)

Session that added a **NAICS-6 -> archetype crosswalk** to the workbook and rewired the
three program-vendor sheets so their Capability Domain (D) / Primary Output (P) cells are
**override-first live formulas** instead of hardcoded leaves. Archetype coverage on the
program-vendor rows went from **17% -> 73%** (the long tail is now tagged mechanically
from each firm's NAICS-6). Build stays green throughout (12 sheets, 10 native tables, 6
note parts, 0 XML errors, 0 error-literal cells, no repair).

This doc is also a **handoff to the next agent**: §8 lists the one remaining phase (2026
dollars) and §9 lists decisions already made so they are not relitigated.

---

## §1 - What was built

Two new sheets + a new resolution mechanism:

1. **`NAICS-6 Archetype Map`** (guide group, tab #3, after Methodology) - the crosswalk.
   One row per **observed** subawardee NAICS-6 (176 codes), giving the DEFAULT 3-axis
   archetype: Capability Domain (D), Operating Role (R, internal), Primary Output (P),
   plus QA flags (Resolution / Review Flag / R-P Lattice Status / High-Integration Gate).
   The per-axis rationale + caveats fold into hover Notes on the D / R / P / Resolution
   cells. D / R / P + the NAICS key render blue (leaf input).
2. **`Vendor Archetype Overrides`** (data group, last tab) - the hand-researched overrides.
   293 rows, grain **(Program, UEI)**, columns Program | Subawardee UEI | D | P, with the
   research evidence (reasoning + URLs) folded into hover Notes on the D / P cells. This is
   the same override data that used to be baked inline into each program-vendor CSV, now
   lifted into its own (Program, UEI) leaf table.
3. **Override-first archetype formulas** on the three program-vendor sheets (see §2).

## §2 - Resolution precedence (the core mechanism)

Each program-vendor row resolves D and P (and their Basis label) as one live formula:

```
D = IF a (UEI x Program) research override exists  -> the override code
    else IF the row's NAICS-6 is in the crosswalk  -> the mapped default code
    else                                            -> "D0"   (P uses "P0")

Basis = "Research override"  /  "NAICS-6 map"  /  "Unresolved"   (which tier fired)
```

- The override lookup is the existing composite (UEI x Program) INDEX/MATCH (same trick as
  `composite_lookup`), returning "" on a miss so it composes inside the outer IF.
- The crosswalk lookup is a single-key INDEX/MATCH of the row's resolved **NAICS-6 cell
  (column C)** into the map's NAICS-6 column.
- **Per-axis independent**: a row can take its D from an override and its P from the map,
  or vice-versa (an override row blank on one axis falls through to the map on that axis).
- The two helpers live in `sheets/_flat.py`: `override_then_map()` (the code) and
  `override_then_map_basis()` (the tier label), sharing `_override_inner()`.

Expected resolution over the 1,710 program-vendor rows (Excel computes the live values on
open; this is the precomputed split for sanity):

| Basis tier        | rows | share |
|-------------------|-----:|------:|
| Research override |  293 |  17%  |
| NAICS-6 map       |  957 |  56%  |
| Unresolved D0/P0  |  460 |  27%  |

The 460 unresolved are the rows with no usable NAICS-6 (the ~469 no-NAICS finding, minus
the few that carry an override). This is the honest floor - NAICS cannot resolve a firm
with no industry code.

## §3 - Files changed

**New:**
- `sheets/naics6_archetype_map.py` - the crosswalk sheet (table `Naics6ArchetypeMap`).
- `sheets/vendor_archetype_overrides.py` - the overrides sheet (table `VendorArchetypeOverrides`).
- `scripts/build_archetype_overrides.py` - emits `extracted/vendor_archetype_overrides.csv`
  from the `*_archetype_results.csv` pulls, filtered to UEIs present on each program sheet.
- `extracted/naics6_archetype_map.csv` (176 rows) - the filled crosswalk (provenance §4).
- `extracted/vendor_archetype_overrides.csv` (293 rows) - DDG 98 / Virginia 100 / Columbia 95.

**Edited:**
- `sheets/_flat.py` - added `override_then_map` / `override_then_map_basis` / `_override_inner`.
- `sheets/{ddg,virginia,columbia}_program_vendors.py` - import `naics_map_cols` + `overrides_cols`;
  added `_arch` / `_arch_basis` binders + the four archetype `formula_cols`; relabels (see below);
  removed the `note_from_verbatim` (Basis cells no longer carry evidence Notes - evidence lives
  on the two new source sheets).
- `sheets/_tabs.py` - `TAB_NAICS_MAP`, `TAB_ARCHETYPE_OVERRIDES` (+ the <=31-char assert).
- `sheets/__init__.py` - registered both new sheets (guide / data groups).
- `scripts/build_program_vendors.py` - HEADERS relabeled + the two transient Note columns
  dropped + the four archetype cells now written blank (formulas own them); removed the dead
  `load_archetype` / `fmt_archetype_note` / `ARCHETYPE_RESULTS` / `ARCHETYPE_BASIS` and the
  archetype row-assembly block (this session's cleanup pass).

**Relabels** (user-confirmed): `Subaward Actions -> Published Subaward Records`
(the COUNTIFS counts FSRS reports, not procurement actions); `Domestic or Foreign ->
Predominant Place of Performance (by records)` (the formula is a record-count majority,
not an entity-nationality field).

## §4 - Crosswalk provenance (the 176-row map)

Produced by an **external deep-research agent** (run by the user; package staged at
`/Users/brendantoole/projects3/naics_archetype_crosswalk_brief/`, deliverable returned as
the filled `crosswalk_TEMPLATE.csv`, copied to `extracted/naics6_archetype_map.csv`).

- **Observed-only**: the 176 NAICS-6 codes that actually appear among the subawardees
  (the work-list `observed_naics_seed.csv` carried per-code dollar/vendor weight + the
  override D/P profile for the 88 codes that had override calibration; the other 88 were
  assigned cold from the NAICS definition).
- **Method** (the agent's, validated): assign D, R, P **independently** from each NAICS
  definition; use the R-P lattice as a QA/review flag (NOT a deterministic NAICS->R->P
  chain); apply a **P4/P5 positive-evidence gate** (never auto-assign integrated-system /
  ship-module outputs from an industry code). Override profiles were used as calibration,
  not majority-vote labels.
- **Distribution**: 103 Mapped / 67 Partial / 6 Unresolved; 104 review-flagged; **36% of
  codes resolve to D0** (services, distributors, residual "all other" codes, and dual-domain
  codes genuinely have no single ship domain). NAICS resolves P and R well, D only ~64%.
- Empirical claims in the agent's write-up were spot-checked against the override data and
  matched exactly (e.g. 332911 valves 19/19 -> D4/P3; 335311 DRS D2 on Columbia only).

## §5 - The overrides table

`build_archetype_overrides.py` reads `extracted/{program}_archetype_results.csv` (columns
`Subawardee UEI, Capability Domain (D), Capability Domain Basis, Capability Domain URLs,
Primary Output (P), Primary Output Basis, Primary Output URLs`) and keeps a row only if the
UEI is present in that program's `*_program_vendors.csv`. The Basis hover Note is composed
exactly as the old inline path did (reasoning, blank line, URLs one per line). **R is not
carried here** - the overrides were D/P research only; R is the internal axis, defaulted
from the crosswalk.

## §6 - Verification

- `python3 build_workbook.py` + `python3 validate_workbook.py`: 12 sheets, 10 native tables,
  6 note parts, **0 XML errors, 0 error-literal cells**, no repair.
- Generated formula strings were pulled and every range mapping checked against the source
  sheets: Overrides `B=Program C=UEI D=D E=P`; Map `B=NAICS-6 C=Title D=D E=R F=P`. The D
  formula reads override `$D` then map `$D`; P reads override `$E` then map `$F`; both key
  the override on `$C`(UEI)+`$B`(Program=label) and the map on this row's NAICS `$C{r}`.
- Excel evaluates the live values on open; per the workbook convention (`no-png-render-
  verification`) the user verifies visually. Spot-check: filter the `Capability Domain
  Archetype Basis` column for the 293 / 957 / 460 split; a row whose NAICS-6 description
  reads `n/a (...)` should show `D0` / `P0` / `Unresolved`.

## §7 - Conventions / gotchas (this session)

- **Column letters are load-bearing in the formulas.** On the program-vendor sheets the
  resolved NAICS-6 is **column C** (`_NAICS_COL = "C"`); the UEI key is column B. These are
  fixed by `build_program_vendors.HEADERS` order - do not reorder those columns without
  updating `_NAICS_COL`. Data rows start at **row 9** (title/intro/blank/banner/blank/header).
- **Leaf is blue, derived is a live formula.** The crosswalk D/R/P and the override D/P are
  blue leaf inputs (`input_cols`, rendered via `S_TEXT_INPUT`). The program-vendor D/P/basis
  are now formulas -> black `S_DEFAULT` (text formula columns are always black; only numeric
  formula columns can go green via `link_cols`).
- **R stays internal**: it lives on the crosswalk sheet (and conceptually inside the
  resolution), but is **not** a per-vendor column on the program-vendor sheets, and the
  overrides table is D/P only.
- **The crosswalk is ONE global table, not three.** A NAICS-6 -> archetype rule is program-
  invariant; program-specific exceptions are handled entity-by-entity via the (UEI x Program)
  overrides, never by a per-program crosswalk (would drift). Decided with evidence in §9.
- **Adding a flat sheet**: `make_flat_sheet` derives the sheet's columns from the CSV header;
  `formula_cols` only re-renders an EXISTING column - it cannot add one. So a column the sheet
  shows must exist in the CSV (hence the blank archetype placeholder columns).
- Build green = done; the user verifies visually.

## §8 - OPEN: Phase 4 - 2026 dollars (next step, not started)

The user wants Subaward $ standardized to **constant FY2026 dollars**, keeping nominal.

- **Source is already in the codebase**: `workbook_core.deflators` (DoD **Green Book
  Procurement TOA**, rebased to constant **FY2026**), accessors `factor(fy)` / `raw_index(fy)`
  / `FY_RANGE` / `EXTRAPOLATED_FYS` / `GREEN_BOOK_CITE`. The DDG sibling workbook renders it
  via `projects/distributed_shipbuilding/ddg/workbook/workbook_ddg/sheets/data_deflators.py`
  (copy that sheet pattern). NOTE: `workbook_award_analysis` - the workbook the user first
  pointed at - has **no** deflator (it is all-nominal); use `workbook_core.deflators`.
- **Plan**: add a `Deflators` sheet (reuse `workbook_core.deflators`); add a `Subaward $M
  (2026)` column beside the nominal one on each program-vendor sheet, as a `SUMPRODUCT` of
  each transaction's nominal amount x its year's factor (computed against the raw tx sheet,
  so raw stays raw and nominal is never overwritten); show both columns; negatives keep sign.
- **DECISION PENDING**: the deflator series is keyed by **fiscal year**, but these pulls are
  **calendar year** (captions say CY2013-2026). Pick CY-vs-FY price-year basis and document it.
  Confirm `FY_RANGE` covers the full date span (DDG runs to 2026; 2001 outliers were dropped).
- **Watch-out** (from the schema review): `Total Contract Value $` is non-additive prime
  context - it is currently NEVER summed in the workbook; do not start summing it, and do not
  produce a 2026 version of it without first selecting one observation per prime.

## §9 - Decisions already made (do not relitigate)

- **One global crosswalk** (not per-program). Evidence: among the 88 override-calibrated
  codes, conflicts in D/P exist WITHIN a single program too (22 codes >1 D, 21 >1 P), and a
  program-level rule would misclassify (e.g. a Columbia-wide 335311->D2 rule breaks Power
  Paragon). Program-specific exceptions are (UEI x Program) overrides.
- **P determination**: independent D/R/P + R-P lattice as QA, with the P4/P5 positive-
  evidence gate - NOT a deterministic NAICS->R->P chain.
- **Override-wins precedence** (research override > NAICS map > unresolved).
- **Slim crosswalk sheet**: rationale lives in hover Notes, not visible columns (trivially
  flippable if the user later wants them visible).
- **Relabels** confirmed by the user (§3).
- The broader "normalize the whole workbook into ~15 keyed tables" proposal from a separate
  schema-review agent was **declined** as over-engineering for this artifact; only the cheap/
  correct items were adopted (crosswalk-separate, override-first, P4/P5 gate, the two
  relabels, 2026-dollars-as-a-separate-derived-measure). See the chat history for the full
  wheat-from-chaff cut.

## §10 - How to rebuild (for the next agent)

From `projects/research_shared/workbook_award_classification_refactor/`:

```
python3 scripts/build_archetype_overrides.py                 # -> extracted/vendor_archetype_overrides.csv
python3 scripts/build_program_vendors.py {ddg|virginia|columbia}   # -> the 3 program-vendor CSVs
python3 build_workbook.py                                     # -> ../award_classification_refactor.xlsx
python3 validate_workbook.py                                  # 0 xml errors / 0 error-literal cells
```

To inspect a generated formula without Excel:
`PYTHONPATH=<repo-root>:<project-dir> python3 -c "from workbook_award_classification_refactor.sheets import ddg_program_vendors as m; print(m._FORMULAS['Capability Domain Archetype (D)'](9))"`.

The crosswalk content itself is regenerated only by re-running the external research agent
(package at `projects3/naics_archetype_crosswalk_brief/`); the workbook just ingests
`extracted/naics6_archetype_map.csv`.
