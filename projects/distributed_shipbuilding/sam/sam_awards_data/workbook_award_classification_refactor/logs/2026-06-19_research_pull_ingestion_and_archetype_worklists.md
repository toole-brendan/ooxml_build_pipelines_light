# 2026-06-19 — Research-pull ingestion pipeline + role/desc re-research + archetype worklists

Session that (a) stood up a reusable AI-deep-research **ingestion pipeline** (raw archive →
normalize → upsert → research-prose-wins precedence + NAICS gap-fill), (b) ran **five
research pulls** through it to bring the program-vendor `Role / Description` up to full
90%-frontier coverage and de-hedge/de-duplicate the prose, (c) fixed the Taxonomy intro
layout, and (d) shipped **six new assignment worklists** (Capability Domain ×3, Primary
Output ×3) so the two published archetype axes can be filled next. Build stays green
throughout (0 XML errors, 0 error-literal cells, 8 native tables, no repair). Follow-on to
`2026-06-19_program_vendor_formula_refactor_and_research_worklist.md`.

---

## §1 — Audit that opened the session (read-only)

Audited the live `Role / Description` for two defects the user flagged:
- **Weak / hedged prose** (markers: "Likely…", "most plausibly tied", "Parent-company
  entry…", "no direct … resolved", "input row names X while public traces…"): **42 rows**
  (DDG 30 / VA 9 / Col 3).
- **Duplicated parent-level prose** — multiple subawardee-UEIs under one parent corp
  carrying byte-identical text: **79 rows in 23 shared-parent clusters** (DDG 35/11 ·
  VA 28/7 · Col 16/5). Clustering invariant is the **identical text**, not the parent-name
  string (a few siblings carry a blank/variant Parent Vendor Name).
- Overlap weak∩dup = 26; **union = 95** distinct rows.

## §2 — Re-research worklists shipped (the "what to fix" files)

`scripts/build_description_rerun_worklists.py` — two plain xlsx (bare-bones, all 3 programs,
`Program` column added, `Current Role / Description` included so the agent sees what's wrong):
- `weak_description_research_worklist.xlsx` — **16 rows** (weak **not already in** the dup
  file → clean partition, no UEI researched twice).
- `duplicate_parent_description_research_worklist.xlsx` — **79 rows**, sorted so each
  shared-text cluster is **contiguous** (cluster key = the duplicated text, ordered by
  lead-$ desc; fixes the blank/variant-parent split).

`scripts/build_columbia_hedge_worklist.py` — `columbia_hedge_rerun_worklist.xlsx`, **36
rows** ($548M), the Columbia first-pass rows whose *specific Columbia deliverable* came back
unconfirmed ("could not be confirmed" / "do not identify the exact Columbia…"). Scoped to
Columbia research-pull UEIs → disjoint from the weak/dup files.

## §3 — The ingestion pipeline (reusable, the headline infrastructure)

Three layers, mirroring the existing `sam_entity_enrichment/raw/` → derived pattern. **Only
the original subaward data pulls are sacrosanct; every research result is a derived,
regenerable file.**

1. **Raw archive (immutable)** — `research_pulls/` holds every pull byte-for-byte. 6 files
   now: `{ddg,virginia,columbia}_subaward_research_completed.xlsx`,
   `weak_description_completed.xlsx`, `duplicate_parent_description_completed.xlsx`,
   `columbia_hedge_secondpass_completed.xlsx`.
2. **Normalize** — `scripts/extract_research_results.py` (first batch, per-program files,
   UEI-keyed) and `scripts/merge_research_pulls.py` (combined-program **and** single-program
   pulls) write/upsert the per-program **`extracted/<program>_subaward_research_results.csv`**
   (`UEI · Role / Description · Source URLs · NAICS-6 code · NAICS-6 title`). Results sheet is
   found by **header signature**, not name (the pulls used `Research Results` / `Research
   Output` / `Researched Roles` / `Columbia second pass`). Faithful dump — non-numeric NAICS
   like `"Not confirmed"` carried, validation lives downstream.
3. **Consume** — `build_program_vendors.py` gained `RESEARCH_RESULTS` + `load_research_prose`
   / `load_research_naics`:
   - **Prose precedence:** leaf-UEI research result **wins**, falls back to the old
     parent-level join. (Bonus: a researched leaf that used to inherit a shared parent blurb
     now gets unique text.)
   - **NAICS gap-fill:** research code used **only** when reference *and* SAM both miss (a
     current `n/a` row), accepting only `^\d{6}$`; **never overwrites** an existing code.
   - `build_uei_dimensions.py` imports `load_research_naics` and applies the same gap-fill
     per program, so the workbook's live NAICS formula (which reads the dimension) updates.
   - **Precedence across pulls = latest wins** on a (program, UEI) clash:
     `frontier → weak → duplicate → columbia_hedge`. `merge_research_pulls.py` upserts by
     UEI, so a re-pull of an existing UEI reports as **replaced**, not new.

## §4 — Pull 1: the 3 frontier pulls (fill the 90%-$ blanks)

The original per-program worklists came back (DDG 49 / VA 52 / Col 59 = **160 rows**, 0
unmatched, all previously **blank** prose). Ingested: 160 leaf-UEI descriptions + **10**
NAICS gap-fills (DDG 2 / VA 5 / Col 3). 98 of the 108 valid research codes **agreed** with
the existing reference/SAM code (0 disagreements → nothing authoritative overwritten).
Columbia hedged heavily — ingested as-is per the user ("fix on 2nd pass").

## §5 — Pull 2: weak + duplicate (de-hedge + de-duplicate)

`navy_subcontractor_roles_researched.xlsx` (weak, **16**) and
`navy_subawardee_entity_roles_researched.xlsx` (duplicate, **79**) — combined-program,
keyed (Program, UEI). Folded in via `merge_research_pulls.COMBINED_PULLS`:
- **95/95 rows overwrote** their bad prose verbatim; disjoint from each other and from
  the frontier batch.
- **24 shared-parent clusters → 0 still sharing identical text** (the dedup worked end to
  end; e.g. the 6 DDG Leonardo/DRS siblings now read as distinct site/capability blurbs).
- **+11** NAICS gap-fills (→ 21 total: DDG 10 / VA 8 / Col 3).

## §6 — Pull 3: Columbia hedge 2nd pass (latest-wins overwrite)

`columbia_class_subcontractor_deep_second_pass.xlsx` — single-program (Columbia, UEI-keyed,
no Program column), **36 rows**, all already present from the frontier batch. Added the
`SINGLE_PROGRAM_PULLS` branch (`read_single_program`) to `merge_research_pulls.py`; folded
after the combined pulls so it **replaces** the first-pass hedged text. 36/36 verbatim;
29 now confirmed/specific, 7 honest "best-supported inference". Columbia research CSV = 78
rows (59 frontier − 36 replaced + 36 second-pass + 3 weak + 16 dup).

Final prose coverage: **DDG 98 / VA 100 / Col 95** (= the 90%-$ frontier, gapless; the
bottom-10%-of-$ long tail is intentionally blank — the long-tail pull was declined). Source
split now leaf-UEI research 90/87/78, old parent-level join 8/13/17.

## §7 — Taxonomy intro layout fix

User wanted each section intro **directly under** its banner and **italicized**, the sheet
grain note moved up, and tightened spacing. New scoped style `sheets/_italic.py` →
**`S_ITALIC`** (italic-black, font id 5; appended to `CELL_XFS` per-build, mirrors
`_text_input.py` / `_yn.py` — no shared `workbook_core` edit). `taxonomy.py` now lays out:
row 2 title banner · row 3 italic grain note · rows 4-5 blank · **row 6 §1 banner** · row 7
italic intro (immediately below the banner) · row 8 blank · row 9 headers. Same banner →
italic-intro → blank → headers pattern for §1–§4.

## §8 — Archetype assignment worklists (the next gating pass)

The two **published** axes are still blank in the workbook; shipped per-program worklists so
a zero-context agent can fill them. Both pull their controlled vocabulary straight from the
`_taxonomy` leaf (via `importlib`, no package/`workbook_core` import) so the menus can't
drift from the legend.

- `scripts/build_capability_domain_worklists.py` → `{program}_capability_domain_worklist.xlsx`
  (98/100/95). Sheet 1 = bare signals (`UEI · Vendor Name · NAICS-6 · NAICS-6 title ·
  Role / Description` + empty `Capability Domain (D)` + `Basis`). Sheet 2 = **Capability
  Domain Codes** (D1–D10, D0 + 6 tie-breaks).
- `scripts/build_primary_output_worklists.py` → `{program}_primary_output_worklist.xlsx`
  (98/100/95). Same shape; reference tab = **Primary Output Codes** (P1–P6, P0 + 5 boundary
  tests + the assignment rule). Empty `Primary Output (P)` + `Basis`.

Both worklists list the **same rows** (one per Role/Description-bearing UEI), sorted by $
desc, so the axes run independently and merge per UEI. The workbook already holds empty
`Capability Domain Archetype (D/Basis)` and `Primary Output Archetype (P/Basis)` columns →
these ingest the same way the prose pulls did.

## §9 — Files created / changed

**scripts/** (new): `extract_research_results.py`, `merge_research_pulls.py`,
`build_description_rerun_worklists.py`, `build_columbia_hedge_worklist.py`,
`build_capability_domain_worklists.py`, `build_primary_output_worklists.py`.
**scripts/** (changed): `build_program_vendors.py` (`RESEARCH_RESULTS`, `load_research_prose`,
`load_research_naics`, prose-wins + gap-fill, counters); `build_uei_dimensions.py` (import +
per-program gap-fill).
**sheets/**: `_italic.py` (new, `S_ITALIC`); `taxonomy.py` (intro layout).
**research_pulls/** (new, immutable): 6 raw xlsx.
**extracted/** (rebuilt): 3 `*_subaward_research_results.csv` (DDG 90 / VA 87 / Col 78),
3 `*_program_vendors.csv`, `subawardee_uei_index.csv`, `subawardee_parents.csv`.
**projects/research_shared/** (worklist outputs): 2 rerun + 1 columbia-hedge + 3 capability
domain + 3 primary output xlsx.
**Outputs:** `award_classification_refactor.xlsx` rebuilt (10 sheets, 8 tables).

## §10 — Verification (all green)

- Build green at every step (0 XML errors, 0 error-literal cells, 8 tables, no repair).
- Frontier: 160/160 prose verbatim, 160/160 URLs, 10 NAICS gap-fills, 0 existing codes
  changed.
- Weak/dup: 95/95 prose verbatim, 24 clusters → **0** still duplicated, +11 gap-fills.
- Columbia 2nd pass: 36/36 verbatim, reported **replaced** (latest-wins confirmed).
- Dimension NAICS code-fill 1230 → **1241**; final prose 98/100/95.
- Taxonomy: row 3 italic grain note, §1 banner on row 6, §-intros italic & immediately
  below their banners (openpyxl-checked).

## §11 — Open work / next-agent notes

- **Run the 6 archetype worklists** (Capability Domain + Primary Output) → ingest the codes
  + basis into the empty `*_Archetype (D/P)` and `*_Basis` columns. Will need a small
  archetype-ingest path analogous to the prose loaders (key on UEI; these are leaf hardcoded
  columns in the program-vendor sheets, not dimensions).
- **Operating Role (R)** is the internal validation axis (R0–R5) — not yet assigned; needed
  to run the Role × Output lattice QA.
- Long-tail prose (bottom 10% of $) remains intentionally blank — the declined long-tail
  pull is still available, low value by dollars.

## §12 — Conventions / gotchas (this session)

- **Only the original subaward data pulls are immutable**; research results are derived —
  enrich freely, never hand-edit the corpus.
- **Research prose wins by leaf-UEI; NAICS research is gap-fill only** (valid 6-digit, never
  overwrites reference/SAM). Pull precedence = **latest wins** on (program, UEI).
- **Find the results sheet by header signature, not name** — every pull named its sheet
  differently.
- **Combined-program pulls key on (Program, UEI)** (a UEI recurs across programs); single-
  program pulls are UEI-keyed with a fixed program.
- **`merge_research_pulls.py` is idempotent** (upsert by UEI) — re-running re-applies all
  pulls; a re-pull of an existing UEI shows as *replaced*.
- **Archetype/code worklists import the vocabulary from the `_taxonomy` leaf** via
  `importlib` (no package init / `workbook_core`) so the agent's menu can't drift.
- **Scoped style appends** (`S_ITALIC`) mutate `CELL_XFS` per-build only — never edit shared
  `workbook_core`; mirror `_yn.py` / `_text_input.py`.
- Build green = done; user verifies visually (`no-png-render-verification`).
