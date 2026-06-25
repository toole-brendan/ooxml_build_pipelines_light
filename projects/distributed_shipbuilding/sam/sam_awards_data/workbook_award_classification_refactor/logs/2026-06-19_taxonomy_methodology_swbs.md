# Session Log — workbook_award_classification_refactor — 2026-06-19 (taxonomy + methodology refactor; SWBS axis)

**Handoff doc for the next AI agent.** This session (a) finalized the entity-level
classification schema and rebuilt the **Taxonomy** legend sheet, (b) added a new
**Methodology** sheet matching the ddg/submarines house style, and (c) added the
**SWBS / Ship-System Application** dimension to the *guide* layer (legend + method).
The SWBS *data* sheets are designed but **not yet built** — that's the main open work.

Build pipeline: `workbook_award_classification_refactor/` →
`projects/research_shared/award_classification_refactor.xlsx` (canonical, 7 tabs).

Read first for context:
1. `projects/research_shared/CLASSIFICATION_METHODOLOGY_OVERVIEW.md` — the *stale-but-directional* method baseline (the durable spine; specific category counts in it are dead).
2. The `_taxonomy` leaf: `workbook_award_classification_refactor/sheets/_taxonomy.py` — **single source of truth** for the whole schema (all legends, tie-breaks, boundaries, assignment rule, lattice, SWBS).
3. The two guide sheets that render it: `sheets/taxonomy.py` (legend) and `sheets/guide_methodology.py` (method).
4. This file.

Auto-memory worth knowing (already saved): `legend-vs-methodology-separation`,
`checkpoint-before-large-builds`, `subaward-classification-vocab`,
`derived-metrics-live-formulas`, `present-data-before-characterization`,
`canonical-corpus-source`.

---

## 1. TL;DR — the one thing that matters

The classification schema is **three entity-level axes + one transaction-level companion**, all defined once in `_taxonomy.py`:

| Axis | Codes | Grain | Published? |
|---|---|---|---|
| **Capability Domain** | D1–D10, D0 | UEI × Program | yes |
| **Operating Role** | R1–R5, R0 | UEI × Program | **no — internal validation only** |
| **Primary Output** | P1–P6, P0 | UEI × Program | yes |
| **Ship-System Application (SWBS)** | 100–900, X00/L00/U00 | **subaward transaction (HII-DDG only)** | yes, with coverage |

Hard rule the user enforces: **Taxonomy = what codes mean (legend only); Methodology = how codes are assigned/disambiguated/validated.** Don't put assignment rules, tie-breaks, boundary tests, or the validation lattice on the Taxonomy sheet (I did once and was corrected). Both sheets render from the `_taxonomy` leaf, so edit the schema there, not in the renderers.

---

## 2. What was built this session

### New / rewritten files (all under `workbook_award_classification_refactor/sheets/`)
- **`_taxonomy.py`** (NEW leaf, renders nothing) — the finalized vocabulary: `DOMAINS` (D1–D10, D0), `ROLES` (R1–R5, R0), `OUTPUTS` (P1–P6, P0), `DOMAIN_TIEBREAKS`, `OUTPUT_BOUNDARIES`, `ASSIGNMENT_RULE`, `ROLE_OUTPUT_LATTICE` + `LATTICE_NOTE`, `AXES`, and the SWBS block (`SWBS_INTRO`, `SWBS_GROUPS`, `SWBS_HIERARCHY_NOTE`, `SWBS_MAPPING_METHOD`, `SWBS_GUARDRAILS`).
- **`taxonomy.py`** (rewritten) — the **Taxonomy** tab, now a pure legend: §1 Domain, §2 Role, §3 Output, §4 SWBS code tables. Dropped the old CSV-by-grid-position approach (the new content doesn't fit a 3-col CSV). No longer reads `extracted/taxonomy.csv` (that file is now unused, left in place).
- **`guide_methodology.py`** (NEW) — the **Methodology** tab, modeled on `distributed_shipbuilding/{ddg,submarines}/workbook/.../sheets/guide_methodology.py` (RowCursor, §-banners, collapsible outline, S_TITLE_SECTION/SUBSECTION, Excel hover-notes). Sections: §1 Definitions · §2 Classification unit & grain · §3 The three axes (+§3a Role→Output lattice) · §4 Evidence & precedence · §5 Assignment rule & boundary rules (+§5a Domain tie-breaks, §5b Output boundary tests) · §6 HII-DDG vs submarine · §7 Scope hygiene · §8 Coverage reporting · §9 Ship-System Application/SWBS (+§9a mapping method, §9b standing rules).

### Registration / wiring
- `sheets/_tabs.py` — added `TAB_METHODOLOGY = "Methodology"`.
- `sheets/__init__.py` — registered `guide_methodology.METHODOLOGY` right after `taxonomy.TAXONOMY` (both `guide` group; group order guide→model→data stays contiguous).

### Cleanup to the build launcher (user request)
- `workbook_award_classification_refactor/lib.py` — **removed the `WB_OUT` env-var override**; `OUT` is now hardcoded to the canonical `award_classification_refactor.xlsx`. `import os` removed.
- `build_workbook.py` — removed the `WB_OUT` paragraph from its docstring.
- Net: the build **always** writes the canonical file. There is no scratch-file path anymore.

### Current tab order (7)
`Taxonomy · Methodology · Classifications (first-pass) · Vendor Context · DDG Top Vendors · Virginia Top Vendors · Columbia Top Vendors`

---

## 3. Build & validate

```
cd projects/research_shared/workbook_award_classification_refactor
PYTHONPATH="<REPO_ROOT>:$(pwd)" python3 build_workbook.py        # writes ../award_classification_refactor.xlsx
PYTHONPATH="<REPO_ROOT>:$(pwd)" python3 validate_workbook.py      # 0 xml errors, 0 error-literal cells expected
```
`<REPO_ROOT>` = `/Users/brendantoole/projects3/ooxml_build_pipelines_light` (needed for `workbook_core`). Last build this session: 7 sheets, 105,635 bytes, 0 errors.

---

## 4. The finalized schema (reference — full text lives in `_taxonomy.py`)

**Capability Domain (D, published) — "what technical ship area is the vendor competent in?"** Pure technical-area axis (no role/activity meaning):
D1 Hull/Structures & Marine Fabrication · D2 Propulsion & Power-Transmission · D3 Electrical Power (gen/conv/dist) · D4 Fluid/Pressure & Piping · D5 Thermal/HVAC & Life-Support · D6 Mission/Combat & Communications · **D7 Electronic Components, Interconnect & Cable** · D8 Mechanical Handling/Deck Machinery & Auxiliaries · D9 Specialty Materials & Precision Components · D10 Interiors/Habitability & General Outfitting · D0 Unresolved.

**Operating Role (R, internal validation only) — "what value-chain responsibility?"** Cut on design authority then integration level:
R1 Build-to-Spec Mfr/Processor/Distributor · R2 Product/Equipment OEM · R3 Subsystem/Shipset Integrator · R4 Module/Distributed Shipbuilder · R5 Production/Test/Lifecycle Service · R0 Unresolved/Non-operating.

**Primary Output (P, published) — "what physically leaves the vendor?"** Deliverable-maturity ladder:
P1 Materials/Stock & Bulk Inputs · P2 Finished Parts & Fabricated Components · P3 Functional Equipment & Machinery · P4 Integrated Systems & Configured Shipsets · P5 Outfitted Structures & Ship Modules · P6 Services & Technical Work Products · P0 Unresolved/Attribution-Only.

**Role→Output validation lattice (QA, not derivation):** R1→P1/P2, R2→P2/P3, R3→P4, R4→P5, R5→P6, R0→P0. Off-lattice cells are **review flags, not errors** (e.g. R1×P3 = a build-to-print shop delivering a complete unit; verify it isn't actually R2).

**SWBS / Ship-System Application (transaction-level, HII-DDG only):** standard SWBS majors 100–900 plus controlled extensions X00 (cross-cutting requirements, e.g. 730→7300 Noise & Vibration), L00 (legacy/unmapped, e.g. 351), U00 (no SWBS evidence). NOT a 4th supplier archetype — it's a different-grain companion the entity tags join to. **Validates, never overwrites** the entity tags.

### Why these choices (so they aren't re-litigated)
- Derived by comparing the prior taxonomy against an external agent's bottom-up proposal (built from stripped DDG/Virginia/Columbia top-vendor prose). Kept its good consolidations (08+09→D6 mission/combat; metals+polymers→D9 materials; the sharp Output boundary tests; the explicit assignment rule; the design-authority Role cut). **Rejected its role-contamination of the Domain axis** (its "Production/Test/Support" pseudo-domain and "distributed fabrication" double-booking) — the whole point of splitting D/R/P is to keep Domain a pure technical-area axis.
- **Added D7 Electronics/Interconnect** because merging sensors(08)+ordnance(09)→D6 left component-level connectors/cable/penetrators (e.g. Teledyne) homeless.
- **Consumables folded into P1** (the bottom-up proposal dropped them — no consumables vendor is big enough to appear in the top-vendor sample).
- Caveat carried forward: the external proposal was fit to the 79 top UEI×Program pairings; **re-test new categories against the long tail** (a coatings vendor, a pure stock distributor, an interiors outfitter) before treating "few unresolved" as proof.

---

## 5. Open work / next steps (in priority order)

### (A) Entity re-classification — the gating task
`Classifications (first-pass)` still carries the **OLD** schema columns (`Work-type ID`/`Work type` 01–15, `Delivered-output class` 4 buckets). It has **not** been re-mapped onto D/R/P. Until each UEI×Program gets a D/R/P tag, the headline **Output × Ship-System matrix can't be built** (it needs the entity Primary Output tag). This is the main blocker.

### (B) SWBS data sheets — designed, not built (user paused before building)
Planned layout (fits the guide→model→data invariant):
- **model:** `Ship-System Map` — subaward $ by SWBS major group × Primary Output, mapped-coverage % on every cut, + a System Concentration section (UEIs, top-3 share, HHI, parent-family). **Live SUMIFS** over the fact table (per `derived-metrics-live-formulas`). The Output dimension is blocked on (A); the SWBS-only allocation + concentration are buildable now.
- **data:** `HII-DDG Transactions` — the transaction fact table (leaf/blue), one row per HII-DDG subaward.
- **data:** `HII–SWBS Crosswalk` — the 365-code dictionary (HII work-item code → observed SWBS).
- Bridge metrics (live, on the entity roster): `SWBS breadth` (distinct subsystems) + `specialization ratio` (largest-subsystem $ ÷ total mapped $) per UEI.
- Build approach: add an `extract_swbs_cuts.py` to curate/rename the package CSVs into `extracted/`, then render via `make_flat_sheet` (sheets/_flat.py). Keep raw transactions as faithful leaf tables; do aggregation live on the model sheet.

### (C) Keep validation flags out of published tabs
The "SWBS contradicts entity tag → revisit Pn" check is verdict-style. Per `present-data-before-characterization`, compute it in research/QA and fold only **confirmed** revisions back into the entity tags — don't ship a "misclassified?" column.

---

## 6. SWBS source data (already profiled — don't re-derive)

Package: `projects/research_shared/ddg_hii_swbs_subaward_package/` (verbatim copy; canonical originals at `projects/research_shared/taxonomy_design_input_canonical/`). See its `MANIFEST.md`.
- `hii_ddg_record_components.csv` — **5,900 rows**, all `builder == HII-Ingalls` (421 GD-BIW rows already dropped). Cols: piid, builder, sub_report_id (dedup key), sub_date, fy, amount_usd, vendor_uei, parent_uei, vendor_name, raw_description, code (HII work-item `NNNNN-NN`), swbs_group (3-digit), hull, component_text, n_component_words.
- `hii_ddg_code_dictionary.csv` — **365 rows** (one per HII code): code, n_subawards, total_usd, modal_swbs_group, top_components.
- `swbs_hierarchy.csv` — Navy SWBS/ESWBS codebook (~1,888 rows). Convert a 3-digit group `NNN` via `eswbs_code = NNN + "00"` (e.g. 234 → 23400). **3 exceptions:** 436 (use 4361x prefix-family), 730 (→ 7300 Noise & Vibration, cross-cutting X00 — not Armament), 351 (unresolved → Legacy/L00).

Profiled facts (this session): 4,318 rows carry a code and/or swbs_group; 1,186 have an explicit swbs_group; 4,317 carry an HII code. 381 distinct vendor_uei. FY 2013–2026. **14 negative-amount rows (−$8.57M)** = adjustments, not procurement; max single amount ≈ $69M. Of the 365 HII codes, **113 have an observed SWBS mapping, each to exactly one SWBS group (no 1-to-many conflicts in this pull)** — defensible deterministic crosswalk, but lock it as *observed-in-this-pull* and re-validate on new data. Coverage (per external profiling): ~29.8% of records / ~69.9% of dollars resolve to SWBS — strong on the high-dollar base, weak on the long tail. Always present cuts as "within mapped SWBS records" with coverage shown; never compare SWBS across programs.

---

## 7. Conventions / gotchas to respect

- **Edit the schema in `_taxonomy.py`,** not the renderers. Both Taxonomy and Methodology read from it.
- **Legend vs methodology split** (see §1). Taxonomy = code definitions only.
- **Build writes canonical only** — no `WB_OUT` scratch override anymore (removed this session). Don't reintroduce it.
- **Derived metrics = live formulas** — only leaf data is hardcoded/blue; %s, ratios, roll-ups, the SWBS allocation/concentration must be SUMIFS/links.
- **House style is the shared `workbook_core`** at repo root (stdlib-only raw OOXML). `validate_workbook.py` uses openpyxl only to read back the built file — never import it from the pipeline.
- Build stays green = done; the user visually verifies in Excel (no PNG render step).
- The categories may still shift — the user has said so twice. Treat the schema as the current best, not frozen.
