# 2026-06-18 — Classification methodology merge + consolidated workbook refactor: session log

Continues `logs/2026-06-18_taxonomy_scoring_registry_integration_session.md`. This session (1) reconciled
the previous agent's methodology to the user's *actual* target, (2) replaced the methodology + task docs,
(3) built the single consolidated workbook everything now lives in, and (4) redesigned the deliverable
taxonomy (5 → 10 categories). Written to be read cold. Active files under `projects/research_shared/`.

---

## 1. Methodology reconciled to the true target

The prior agent's `CLASSIFICATION_METHODOLOGY.md` aligned ~80% with the user's stated vision (a message to
his boss, which is authoritative). Strong agreement on the *engine* (NAICS-6 entity-level work_type +
vendor registry overrides + deliverable overlay). Two divergences, both resolved this session:

- **SWBS role.** The prior doc made SWBS a *referee* ("validate/calibrate NAICS purity, never redefine
  categories"). The user's target makes SWBS a real **output dimension**: the `subsystem` (ship-system
  worked on) tag carried on HII-DDG subawards. **Decision: drop the referee framing entirely.** SWBS now
  only produces the subsystem dimension — transaction-level, HII-DDG-only (subs lack SWBS; ~half carry a
  GDEB code that is order-detail/dates, not work type).
- **`scope_status`.** Keep it, but it was never in the target as a co-equal axis. **Decision:** it is a
  hygiene tag **scored at the very end**, after full mapping + registry; flags things that should've been
  filtered upstream (workforce-training / GFE / prime-owned in-house — an **illustrative, non-exhaustive**
  list). Quarantine-and-report, don't purge.

**Settled model — four dimensions:**
- `work_type` — NAICS-6 + registry, **entity (UEI)**, primary, 18 categories + `99`.
- `delivered_output_class` — deliverable overlay, **entity**, redesigned this session (see §5).
- `subsystem` — observed SWBS, **transaction-level**, **HII-DDG only**.
- `scope_status` — hygiene, applied **last**.

Entity-vs-transaction split is the crux: work_type + deliverable are constant per UEI; subsystem varies
per subaward. Reconciled at the `entity_uei` join.

## 2. Doc refactor (under `projects/research_shared/`)

- **Created `CLASSIFICATION_METHODOLOGY_OVERVIEW.md`** — concise, matter-of-fact statement of the approach
  (no "SWBS downgraded" narrative, no tasks). SWBS presented plainly as the source of `subsystem`.
  **Deleted** the old `CLASSIFICATION_METHODOLOGY.md`.
- **Created `TASKS.md`** — reframed roadmap. New/changed vs the old `REMAINING_TASKS.md`:
  - **New task A:** emit the `subsystem` dimension by mapping observed SWBS on HII-DDG rows (repurpose the
    `taxonomy_hii_scoring/` join; drop its purity-scoring layer).
  - `scope_status` moved to the **end** (was on the critical path feeding C).
  - Registry-expansion selection driven by **dollars**, not "low-purity flags" (a referee artifact).
  - Sequencing: **A + B + D → C → F**, with **E (scope_status) last**.
  - **Deleted** the old `REMAINING_TASKS.md`.
- **Deleted `audit_log.md`** (user request) and removed its task + key-path from `TASKS.md`.

## 3. Consolidated workbook — `award_classification_refactor.xlsx`

Everything for the refactor now lives in **one** workbook (moved to the `research_shared` **root**).

- Renamed `vendor_registry_output/top50_vendor_classifications.xlsx` → `award_classification_refactor.xlsx`.
- **Stripped all styling to default Excel.** Rebuilt value-only into a fresh workbook (guarantees defaults):
  removed dark-blue/white bold centered headers, all custom column widths, and freeze panes (A2). No merged
  cells, no native tables existed. Verified **zero data loss** first — no hyperlinks, no custom number
  formats, only strings/numbers.
- **Deleted** the old workbook file and `build_classifications_workbook.py` (re-running it would overwrite
  the workbook and re-apply old styling — a standing risk).

## 4. Sheet structure + platform tabs

Final tab order: **`Taxonomy` · `Classifications (first-pass)` · `Vendor Context` · `DDG Top Vendors` ·
`Virginia Top Vendors` · `Columbia Top Vendors`**.

- Old `Classifications` tab renamed → **`Classifications (first-pass)`**; `Vendor Context` kept.
- Three platform tabs created blank, named with "Top" inserted (per user), then **ported from CSVs verbatim**
  (each keeps its own source schema — not yet normalized):
  - `DDG Top Vendors` ← `ddg51_vendor_research.csv` (38 vendors, 9 cols)
  - `Virginia Top Vendors` ← `virginia_submarine_vendor_research.csv` (35 vendors, 12 cols)
  - `Columbia Top Vendors` ← `columbia_submarine_vendor_research.csv` (29 vendors, 11 cols)
  - BOM stripped from the Virginia header; row-number column coerced to numeric; all default-styled.

## 5. Taxonomy sheet + deliverable redesign (the substantive piece)

New **`Taxonomy`** sheet at position 0, three sections, default-styled, with one-line glosses on each header:

- **WORK TYPES** — vendor-capability categories inferred from NAICS-6 code analysis (entity-level). Lists
  all **19** categories (01–18 + `99`) — id / name / definition pulled verbatim from
  `taxonomy_design_output/navy_work_type_schema.csv` (IDs kept as strings so leading zeros survive).
- **DELIVERABLE CATEGORIES** — the form/integration level in which a vendor's output is delivered
  (entity-level). **Redesigned: 5 → 10** (see below).
- **SWBS CODE MAPPINGS** — ship subsystem worked on, from observed SWBS codes (transaction-level; HII-DDG
  only). Content = **`TBD`** (the §A task).

**Deliverable taxonomy redesign.** Analyzed the ~70 distinct free-text deliverable strings across the three
program sheets (DDG 21 distinct / Virginia 25 / Columbia 24; columns `Delivery category` /
`delivery_form_classification` / `delivery_category`). They collapse to recurring form-buckets. The old
canonical 5-class set (`MA / CE / MT / SV / UN`, with EQ+CP merged into CE) was expanded per user decisions:

- **Split EQ vs CP** (the headline ask — reverses the prior CE merge).
- **Added `SY`** (major equipment / integrated system) tier above EQ.
- **Split `FG`** (forging/casting/near-net) out of MT — forgings matter to the analysis.
- **Added `FB`** (fabricated structure/assembly) — the data's clearest cluster between component and module.
- **`MX` (mixed/multi-form) is its own category, not a flag.** User dislikes flags: every vendor gets exactly
  **one** deliverable decision — either a non-mixed primary or `MX` — adjudicated case-by-case.
- **`SV` kept** as a category (used to filter service items out of the article base).
- **`UN` distinct from `MX`** (missing evidence vs a positive multi-form finding).

Final 10, integration order (high→low, then non-article, then residual):
**`MA · SY · EQ · FB · CP · FG · MT · SV · MX · UN`** — each with a one-line definition in the sheet.

## 6. Where things stand / open items

- **`CLASSIFICATION_METHODOLOGY_OVERVIEW.md` is now stale on one line** — it still lists
  `delivered_output_class` as the old 5-class `MA / CE / MT / SV / UN` (with the retired CE merge). The
  change was scoped to the sheet; **the doc still needs syncing to the new 10-category set.**
- **`TASKS.md` "Done" section** still says "Builder appends future vendors … no code changes" — stale, since
  `build_classifications_workbook.py` was deleted. Workbook edits are now manual / fresh-script.
- **Platform tabs not yet normalized** — three different schemas; the ~70 free-text deliverable strings still
  need mapping onto the new 10-category controlled set.
- **`subsystem` dimension still TBD** (§A) — SWBS→subsystem mapping not built.
- Next substantive work per `TASKS.md`: B (deliverable prior table) + the subsystem mapping → C (full
  1,203-UEI applied table, tie to $13.1B) → F (publish); E (scope_status) last.
