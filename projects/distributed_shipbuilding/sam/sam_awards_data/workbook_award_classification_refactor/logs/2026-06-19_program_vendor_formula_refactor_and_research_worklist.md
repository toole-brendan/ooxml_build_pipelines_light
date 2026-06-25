# 2026-06-19 — Program-vendor formula refactor + NAICS n/a labeling + blue UEI key + research worklist

Enrichment-planning session that turned the three Program Vendors sheets from
mostly-hardcoded leaf rows into **10-of-17 live-formula** rows, added typed `n/a`
reasons for missing NAICS, fixed a non-determinism landmine in the prose join, styled
the UEI key as a blue input, fixed an `INDEX`-of-empty `0`→`-` quirk, and shipped three
per-program AI-deep-research worklists. Build stays green throughout (0 XML errors, 0
error-literal cells, 8 native tables, no repair). Follow-on to
`2026-06-19_program_vendor_refactor.md` and `2026-06-19_complete_raw_subaward_field_port.md`.

---

## §1 — Audit (read-only) and the decisions it drove

Audited the three `*_program_vendors.csv` (470 / 645 / 595 UEIs; 1,215 distinct, 95 on
all three programs). Fill rates: NAICS-6 68/70/75%, parent name ~65%, **prose
(Role/Description) only 10/7/6%**, standardized Parent UEI 0%. Dollars are steeply
Pareto, so a `$`-coverage cutoff is the right scoping lever.

Decisions locked with the user:
- **Description cutoff = top 90% of program $** (≈ DDG 77 / VA 82 / Col 90 frontier
  UEIs; net-new-to-research = 49 / 52 / 59; **141 deduped**).
- **Extra fields:** fill the standardized **Parent UEI**, and have the research pass
  also return **NAICS-6**.
- **Parent collapse rule = dollar-modal pair** (the parent UEI+name carrying the most
  subaward $ for that subawardee; median dominance ~75%).

## §2 — SAM reality check (why the plan changed)

Inspected the 871 cached SAM records (`sam_entity_enrichment/raw/`):
- **No parent/UEI hierarchy** anywhere (0/871). SAM's `corporateRelationships` gives an
  owner *name + CAGE*, never a UEI — so a **standardized Parent UEI can only come from
  the tx as-reported data (dollar-modal)**, not SAM.
- NAICS *is* present (`assertions.goodsAndServices.primaryNaics` + `naicsList` desc),
  but the cache is already drained: of the 436 missing-NAICS UEIs, **0** are fillable
  from cache, **340** are un-pulled long-tail worth only **$8M**, **62** have no SAM
  record ($1,208M), **34** have a SAM record with no NAICS ($443M). A fresh pull buys
  almost nothing by dollars → user **declined the long-tail pull**; the high-$ NAICS gap
  folds into the research pass.

## §3 — The two NAICS descriptions (durable backfill)

Codes `424710` (Martin Energy → *Petroleum Bulk Stations and Terminals*) and `424410`
(Sysco → *General Line Grocery Merchant Wholesalers*) had a code but no title (absent
from `vendor_naics_reference.csv`). Added `NAICS_TITLE_OVERRIDES` to
`build_program_vendors.load_naics_titles()` (values from the SAM `naicsList`, = Census
titles); `build_uei_dimensions` inherits it via the shared import. Reference harvest
still wins where it has the code.

## §4 — Prose-drift determinism fix (the landmine)

Re-running `build_program_vendors.py` silently changed `Role/Description` on a few rows.
Root cause: a subawardee can carry **several prose-bearing parent UEIs**, and the
prose-match iterated a Python **`set`** → which parent won was hash-seed-dependent
(non-reproducible). Fix: pick the **dollar-modal parent** (`pdol`, sorted by $ desc,
tie-break by UEI). Now reproducible across `PYTHONHASHSEED` (verified 0-diff). Two rows
moved from their old random pick to the dollar-dominant parent's prose (DDG SPD
Electrical; VA Curtiss-Wright Flow Control) — both legitimate `top_vendors` prose.

## §5 — NAICS-gap labeling (typed `n/a` in the description)

Missing-NAICS rows now read a reason instead of a blank, foreign-split on the no-record
bucket (user's call):

| Label | source signal |
|---|---|
| `n/a (foreign, no SAM record)` / `n/a (no SAM record)` | cached `_no_record`, split on Domestic/Foreign |
| `n/a (SAM record, no NAICS)` | SAM record, empty `primaryNaics` |
| `n/a (long-tail, not researched)` | not in SAM cache |

Implemented as `load_sam_status()` + `na_label()` in `build_program_vendors` (shared into
`build_uei_dimensions`); added foreign tracking to `build_uei_dimensions._aggregate`.
0 missing rows left blank; foreign split 0-mismatch vs the D/F column. (Note: foreign ≠
no-SAM-record — only 4 of the 14 high-$ no-NAICS research targets are foreign; the rest
are domestic firms whose SAM record omits a NAICS or whose UEI doesn't resolve.)

## §6 — The formula refactor (headline): 10/17 columns now live

Only the **Subawardee UEI key**, the **4 archetype columns**, and the **2 prose
columns** remain hardcoded leaf. Everything else is a live formula keyed on `$B{r}`:

| Column(s) | Formula source |
|---|---|
| Subawardee Vendor Name · NAICS-6 (Primary) · NAICS-6 Description | composite `(UEI × Program)` lookup → **Subawardee UEI Index** |
| Parent UEI · Parent Vendor Name | composite lookup → **Subawardee Parents** (dollar-modal pair) |
| $M · Actions · First · Last · Domestic/Foreign | SUMIFS / COUNTIFS / MINIFS / MAXIFS / IF over the tx leaf (unchanged) |

Plumbing:
- **`composite_lookup()`** added to `_flat.py`: `=IFERROR(IF(INDEX(ret,MATCH(1,INDEX((key=k)*(prog=v),0),0))="","-",INDEX(...)),"-")`
  — INDEX/MATCH over an INDEX-coerced boolean array. Scalar return, **no dynamic-array
  storage** → portable, no repair-on-open risk. Composite `UEI × Program` so each
  single-program sheet pulls its own program's dimension row.
- **Subawardee Parents** gained a standardized **dollar-modal Parent UEI** + its paired
  name (consistent pair — the name never bleeds from a different parent; raw
  `"; "`-joined set kept in `Parent UEI(s)`). `_modal()` made deterministic.
- `uei_index_cols` / `parents_cols` accessors exported from the two dimension sheets.

## §7 — Blue UEI key + the `0`→`-` dash fix

- **Blue input UEI:** new scoped `sheets/_text_input.py` registers `S_TEXT_INPUT` (a
  blue-font clone of `S_DEFAULT`) by appending one cellXf to `workbook_core.styles.CELL_XFS`
  **per-build, this process only** (same trick as `_yn.py`; no shared-core edit).
  `_flat._style()` extended so `input_cols` colors *text* keys blue too;
  `input_cols=["Subawardee UEI"]` on the three sheets. The one place the workbook colors
  a text cell — a deliberate exception to "color = numeric only", since the UEI is the
  one genuine hardcoded text *input* (the row's identity).
- **Dash fix:** `INDEX` of an empty dimension cell returns `0`, which printed as `0` in
  the General-format NAICS/parent columns. `composite_lookup` now returns the IB dash
  `"-"` (per `sheet_guide.md` line 190) for both the no-match and matched-but-blank
  cases. Expected counts now render `-` (DDG NAICS 150 / ParentUEI 142 / ParentName 162,
  etc.).

## §8 — Per-program research worklists (separate, plain xlsx)

`scripts/build_research_worklist.py` (xlsxwriter) writes three default-styled files to
`projects/research_shared/`, one per program — the 90%-frontier UEIs lacking prose, in
`$`-descending order, with exactly: UEI · Vendor Name · Parent Vendor Name · First/Last
Subaward · Domestic/Foreign · Current NAICS-6 · NAICS-6 Title/Status.

```
ddg_subaward_research_worklist.xlsx       49 vendors
virginia_subaward_research_worklist.xlsx  52
columbia_subaward_research_worklist.xlsx  59
```

141 deduped distinct UEIs (95 recur on all 3 programs → research once); 14 also still
lack NAICS-6 (4 foreign). The earlier combined `subaward_research_worklist_90pct.xlsx`
was deleted at the user's request.

## §9 — Files changed / created

**scripts/**
- `build_program_vendors.py` — `NAICS_TITLE_OVERRIDES`; `load_sam_status` + `na_label`;
  dollar-modal parent-prose (`pdol`, replaces the nondeterministic `parents` set);
  na_label wired into the description.
- `build_uei_dimensions.py` — foreign tracking in `_aggregate`; standardized dollar-modal
  `Parent UEI` + paired name; deterministic `_modal`; `na_label`; `PARENT_HEADERS` gains
  `Parent UEI`; coverage prints.
- `build_research_worklist.py` — **new** (3 per-program plain worklists).

**workbook_award_classification_refactor/sheets/**
- `_flat.py` — `composite_lookup()` (dash + INDEX-empty guard); `S_TEXT_INPUT` import;
  `input_cols` now colors text; docstrings.
- `_text_input.py` — **new** (scoped blue text-input style).
- `subawardee_uei_index.py` — export `uei_index_cols`; docstring.
- `subawardee_parents.py` — `+Parent UEI` width; export `parents_cols`; docstring.
- `{ddg,virginia,columbia}_program_vendors.py` — dimension imports, composite formula
  columns, `input_cols=["Subawardee UEI"]`, docstrings.

**Outputs:** `award_classification_refactor.xlsx` rebuilt (5.6 MB, 10 sheets, 8 tables);
three worklist xlsx in `projects/research_shared/`.

## §10 — Verification (all green)

- Build: 0 XML errors, 0 error-literal cells, 8 native tables, no repair (every step).
- **Formula resolution:** all 1,710 `(UEI × Program)` exist in both dimensions (0
  missing → no silent blanks); UEI Index reproduces the vendor CSV's NAICS code/desc/name
  exactly (0 mismatch); Parents `Parent UEI` **and** paired name match an independent
  dollar-modal recompute from the tx sheets (0 / 0).
- **Determinism:** `build_program_vendors` reproducible across `PYTHONHASHSEED` (0-diff).
- **n/a labels:** 0 blank descriptions on missing rows; foreign split 0-mismatch vs D/F.
- **Blue UEI:** every UEI cell `FF0000FF`; adjacent text columns stay black.
- **Worklist counts:** 49 / 52 / 59, deduped 141 — match the §1 audit exactly.

## §11 — Open work / next-agent notes

- **Run the 3 AI research pulls** (the worklists) → Role/Description + Source URLs, and
  NAICS-6 for the `n/a` rows. Then ingest: prose back into `build_program_vendors` (the
  `*_top_vendors.csv` join is now the deterministic source — likely replace with a
  research-results file keyed by UEI), and the new NAICS into the precedence/override.
- **Archetype assignment** (Capability Domain / Primary Output + the 2 Basis cols) is
  still blank — the remaining gating classification pass.
- Optional: dimension sheets show a true blank (not `-`) for empty cells — unify if a
  consistent look is wanted.

## §12 — Conventions / gotchas (this session)

- **`INDEX` of an empty cell returns `0`, not blank** — guard text lookups with
  `IF(INDEX(...)="","-",INDEX(...))`; the workbook's empty/zero glyph is the plain hyphen
  `-` (IB convention, `sheet_guide.md`).
- **Standardized Parent UEI has no authoritative source** — SAM owner data is name+CAGE,
  not a UEI; it comes from the tx **dollar-modal** parent only.
- **`composite_lookup` is deliberately INDEX/MATCH-coerced legacy array** (scalar, no
  `_xlfn` dynamic-array funcs) to avoid dynamic-array storage / repair-on-open.
- **Scoped style appends** (`S_TEXT_INPUT`) mutate `workbook_core.styles.CELL_XFS`
  per-build only — never edit shared `workbook_core`; mirror `_yn.py`.
- **Keep build scripts deterministic** — no `set` iteration feeding output (it cost us a
  silent prose drift); use dollar-modal + key tie-breaks.
- **`na_label` foreign-split applies only to the no-SAM-record bucket**; foreignness
  otherwise lives in its own Domestic/Foreign column.
- Build green = done; user verifies visually (`no-png-render-verification`).
