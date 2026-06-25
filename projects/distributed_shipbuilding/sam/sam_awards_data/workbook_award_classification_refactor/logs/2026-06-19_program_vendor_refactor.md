# 2026-06-19 — Program-vendor refactor (entity-grain corpus roll-ups)

Replaced the three AI-research "Top Vendors" sheets with three **entity-grain
program-vendor sheets** built on the canonical subaward corpus, deleted the
superseded tabs, and finalized a 17-column schema. The workbook is now a 5-sheet
anchor set (Taxonomy · Methodology · DDG/Virginia/Columbia Program Vendors).
Build green. Next-agent handoff below.

---

## §1 — The reframe (why this session happened)

The old `*_top_vendors.csv` sheets were **AI-research rosters** keyed on a
*parent-first* UEI (the `vendor_key` = `subParentUei` if reported, else
`subEntityUei`), the same grain as `workbook_award_analysis`'s `vendors` sheet.
That grain is inconsistent (parent UEI for some vendors, entity UEI for others;
a vendor can even fragment into two rows) and the UEIs don't join to the SAM
enrichment files.

New model (user-directed): **one row per distinct subawardee UEI (`subEntityUei`)
per program**, sourced from the canonical corpus, with SAM enrichment joined on
that UEI and the AI prose carried over only as descriptive color. These sheets
are the prototype intended to **port back into `workbook_award_analysis` and
replace its single `vendors` sheet** — fixing the grain there too. (Memory:
`program-vendor-refactor`.)

---

## §2 — Files built / changed / deleted this session

**New — extraction**
- `scripts/build_program_vendors.py` — entity-grain roll-up generator.
  `python3 scripts/build_program_vendors.py <ddg|virginia|columbia>`.

**New — renderers** (`workbook_award_classification_refactor/sheets/`)
- `ddg_program_vendors.py`, `virginia_program_vendors.py`,
  `columbia_program_vendors.py` — thin `make_flat_sheet` wrappers, group `data`.

**New — extracted data** (`extracted/`)
- `ddg_program_vendors.csv` (470 rows), `virginia_program_vendors.csv` (645),
  `columbia_program_vendors.csv` (595).

**Changed**
- `sheets/_tabs.py` — added `TAB_DDG_PROGRAM` / `TAB_VIRGINIA_PROGRAM` /
  `TAB_COLUMBIA_PROGRAM`; removed the 5 old tab constants.
- `sheets/__init__.py` — registry now: Taxonomy, Methodology, + 3 program-vendor
  sheets. Docstring updated to `guide -> data` (the `model` group is now empty
  and absent — the build allows a missing group).

**Deleted (tabs: module + registry entry + tab constant)**
- `sheets/classifications.py`, `vendor_context.py`, `ddg_top_vendors.py`,
  `virginia_top_vendors.py`, `columbia_top_vendors.py`.

**Preserved on disk (NOT deleted)**
- `extracted/ddg_top_vendors.csv`, `virginia_top_vendors.csv`,
  `columbia_top_vendors.csv` — **the extraction reads these** for the
  `Role / Description` + `Source URLs` join. Do not delete.
- `extracted/vendor_context.csv`, `extracted/classifications.csv` — now dormant
  (nothing reads them); left in place, safe to remove if desired.

**Current tab order:** Taxonomy · Methodology · DDG Program Vendors ·
Virginia Program Vendors · Columbia Program Vendors.

---

## §3 — Build / extraction commands

```bash
cd projects/research_shared/workbook_award_classification_refactor
# regenerate the 3 data CSVs (prints a coverage report per program)
for p in ddg virginia columbia; do python3 scripts/build_program_vendors.py $p; done
# build the workbook (writes ../award_classification_refactor.xlsx)
python3 build_workbook.py
```
`workbook_core` resolves on `sys.path` automatically when run from the project
dir (no PYTHONPATH needed). The extraction imports `_corpus` from
`projects/distributed_shipbuilding/research/scripts/` (added to `sys.path` inside
the script).

---

## §4 — The finalized 17-column schema

Column order is locked. `make_flat_sheet` reads headers from the CSV, so the
**header strings live in `build_program_vendors.py`'s `HEADERS`** (the renderers
only set widths + which cols are int/float).

| # | Header | Source | Coverage / note |
|---|---|---|---|
| 1 | Subawardee UEI | corpus `subEntityUei` (row key) | 100% |
| 2 | Subawardee NAICS-6 (Primary) | `vendor_naics_reference` is_primary=Y → SAM `primary_naics_6` fallback | ~68–75% |
| 3 | Subawardee NAICS-6 Description | `vendor_naics_reference.naics_desc`, backfilled via code→title harvest | matches code coverage |
| 4 | Parent UEI | **blank** — awaiting standardized parent-UEI list | — |
| 5 | Parent Vendor Name | corpus `subEntityParentLegalBusinessName` (raw, $-modal) | ~63–66% |
| 6 | Subawardee Vendor Name | corpus `subEntityLegalBusinessName` ($-modal) | 100% |
| 7 | Domestic or Foreign | corpus country code (`Foreign`/`Domestic`) | 100% |
| 8 | Subaward $M | corpus sum `dollar_m` | 100%, reconciles to corpus to the cent |
| 9 | Subaward Actions | count of distinct `subAwardReportId` | 100% |
| 10 | First Subaward | min `subAwardDate` (ISO text) | 100% |
| 11 | Last Subaward | max `subAwardDate` (ISO text) | 100% |
| 12 | Capability Domain Archetype (D) | **blank** — assignment pass | — |
| 13 | Primary Output Archetype (P) | **blank** — assignment pass | — |
| 14 | Capability Domain Archetype Basis | **blank** — `Registry override` / `NAICS-6 map` (Sentence case) | — |
| 15 | Primary Output Archetype Basis | **blank** — same vocab | — |
| 16 | Role / Description | old `*_top_vendors.csv` prose, joined on UEI or raw parent UEI | sparse (matched families only) |
| 17 | Source URLs | old `*_top_vendors.csv` URLs, same join | sparse |

Header rules: Title Case; "Archetype" in all four D/P columns; `or` lowercase in
`Domestic or Foreign`; `UEI` / `NAICS-6` / `$M` left as-is.

---

## §5 — Data provenance (where the numbers come from)

**Spine = canonical corpus.** `_corpus.iter_records(program)` in
`projects/distributed_shipbuilding/research/scripts/_corpus.py`. One record = one
deduped published subaward transaction. It already applies: in-scope-PIID filter
(DDG = shipbuilder-directed GD-BIW + HII-Ingalls only), `subAwardReportId` dedup,
MIB/BlueForge exclusion, null-date drop. For submarines it yields both classes;
filter `rec["vclass"].lower()` for virginia/columbia. Raw JSON lives in each
program's `research/sam_subawards_fullhistory/`. **Dollars/actions/dates come
ONLY from here.**

**Enrichment (per-UEI attribute lookups, keyed on `subEntityUei`):**
- `projects/research_shared/submarine_subaward_code_package/vendor_naics_reference.csv`
  (`uei, naics6, naics_desc, is_primary`) — primary NAICS-6 + official title.
  Covers 654/1352 corpus UEIs; submarine-skewed (strong VA/Col, weak DDG).
- `projects/research_shared/sam_entity_enrichment/unique_uei_sam_enrichment.csv`
  (`primary_naics_6, foreign, immediate_owner, highest_owner, cage, all_naics_6`,
  …) — used ONLY as the NAICS-6 *code* fallback here; **never a dollar source**
  (it's the non-canonical all-'ddg'/BlueForge-inclusive file — see memory
  `canonical-corpus-source`). Covers 939/1352.

**Critical UEI-key fact:** both enrichment files are keyed on `subEntityUei`
(100%), NOT on the parent-first `vendor_key` the old top-vendor rosters used —
which is why the old rosters showed ~1/27 overlap with them. Subaward
transactions carry **no NAICS** (`primeNaics` exists, no sub equivalent); NAICS
is entity-level only (memory `subaward-classification-vocab`). Rolling up to
`subEntityUei` is therefore the grain at which NAICS is even defined.

**Per-program coverage (last build):**
| Program | Rows | $M (= corpus) | NAICS-6 code | Desc | Parent name | Foreign | Prose rows | Old vendors matched |
|---|---|---|---|---|---|---|---|---|
| DDG | 470 | 3,604.198 | 68% | 68% (+179 backfilled) | 66% | 10 | 49 | 27/27 |
| Virginia | 645 | 5,118.693 | 70% | 70% | 66% | 12 | 48 | 27/27 |
| Columbia | 595 | 4,444.805 | 75% | 75% | 63% | 13 | 36 | 25/25 |

(Prose fans out: an old top-vendor entry's narrative is copied to every child
`subEntityUei` of that family on the program sheet. 0 crosswalk misses.)

---

## §6 — Open work (priority order)

- **(A) Archetype-assignment pass — the gating next phase.** Fill `Capability
  Domain Archetype (D)` / `Primary Output (P)` per UEI×program using a
  NAICS-6 → archetype map, with a **vendor-registry override** taking precedence;
  record which was used in the two Basis columns (`Registry override` /
  `NAICS-6 map`). The map and the registry-vs-mechanical method are NOT built
  yet. `workbook_award_analysis` does registry-first classification but drops the
  `basis` before the workbook (only prose on its Sources sheet + a read-only
  override list on Inputs §5) — we are doing the per-row basis it never surfaced.
- **(B) Parent UEI** — blank until a definitive standardized parent-UEI list
  exists. Raw `subParentUei` is available if an interim is wanted (but multi-
  valued per UEI — that's why it's deferred).
- **(C) Port to `workbook_award_analysis`** — replace its `vendors` sheet
  (`model_by_vendor.py` / `wb_vendor_fy.csv`) with this entity-grain model.
- **(D) Polish (optional):** First/Last Subaward are **ISO text**, not native
  Excel date cells — `make_flat_sheet` has no date path; converting needs a small
  custom renderer (mirror award_analysis's `date_serial`). Archetype/basis
  headers are long vs their column widths (codes are short, so headers clip per
  the house no-wrap norm) — widen if undesired.

---

## §7 — Conventions / gotchas

- **Dollars only from `_corpus`.** Enrichment files are attribute lookups only.
- **Don't delete the `*_top_vendors.csv` files** — the extraction reads them.
- **Edit headers in `build_program_vendors.py` (`HEADERS`)**, not the renderers;
  renderers only carry `_WIDTHS` (must equal column count) + `int_cols` /
  `float_cols` (whose names must match the CSV headers exactly, or centering /
  numeric coercion silently won't apply). Currently int=`Subaward Actions`,
  float=`Subaward $M`.
- NAICS codes are kept as **text** (not float) so leading digits / form survive.
- Build green = done; user verifies visually (memory `no-png-render-verification`).
- The `model` group is now empty/absent; build allows it (guide → data).
