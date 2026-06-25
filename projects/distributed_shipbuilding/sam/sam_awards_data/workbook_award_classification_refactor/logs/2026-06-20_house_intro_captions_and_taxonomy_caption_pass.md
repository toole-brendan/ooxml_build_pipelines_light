# 2026-06-20 — Italic intro captions on every sheet + banner shorten + Taxonomy caption pass

Session that gave **all 10 sheets** the Taxonomy top-of-sheet house pattern — title
banner → italic orientation caption → two blank rows → §1 section banner — then
shortened the §1 banners so they no longer repeat the caption, and finished by
re-cutting the Taxonomy tab's own captions/banners/intros to the same rule.

1. **`intro=` param on `make_flat_sheet`** writes the italic caption + `blank(2)` for
   the 8 flat sheets; the same line added inline to Methodology. Taxonomy already had
   the pattern.
2. Per-sheet **orientation captions** (what the sheet is + grain + key caveat), grounded
   in each module's docstring; the dollar/data sheets also carry a **CY year range** and
   a **nominal-dollars** note (both researched, see §3).
3. **§1 banners shortened** to bare labels on the 8 flat sheets (the parenthetical detail
   now lives in the caption).
4. **Taxonomy overhaul** — top caption corrected for its mixed grain, banners stripped of
   their `(published)`/scope parentheticals, section intros trimmed (method content
   defers to Methodology).

Build stays green throughout (0 XML errors, 0 error-literal cells, 10 sheets, 8 native
tables, 4 note parts, no repair). Follow-on to
`2026-06-20_source_url_notes_column_reshuffle_archetype_ingest.md`.

---

## §1 — The pattern + how it's wired

Taxonomy's house rhythm is **row 2 title banner → row 3 italic caption → rows 4-5 blank →
row 6 §1 banner** (`S_ITALIC`, the scoped italic-black style from `_italic.py`). The other
9 sheets had no caption and only one blank (banner at row 4). Replicating it = add the
italic line and bump `blank()` → `blank(2)`.

- **8 flat sheets** (`_flat.make_flat_sheet`): new opt-in **`intro=`** param. When present
  the cursor writes `c.write([intro], styles=[S_ITALIC])` then `c.blank(2)` right after the
  title banner; when absent the old title→1-blank→banner spacing is kept. Reused the
  existing `S_ITALIC` (imported into `_flat.py`); **no `workbook_core` change**.
- **Methodology** (`guide_methodology.py`, not a flat sheet): the italic line + `blank(2)`
  added inline after its title banner; `S_ITALIC` imported.

Net geometry on **every** sheet now: caption at **B3**, §1 banner at **B6**. On the flat
sheets the table_ref and hover-note anchors shifted down 2 rows automatically (both are
computed from the `RowCursor`, not literals) — validation confirms tables (8) and note
parts (4) intact.

## §2 — Captions by group (final text)

House style is **ASCII hyphen throughout** rendered text — the only non-ASCII glyph in any
sheet string is `§` (U+00A7). Year ranges use a hyphen (`CY2013-2026`), matching the
existing `FY22-25` convention; no em/en-dashes, no `×` (lowercase `x` for "UEI x Program").

- **Model — program-vendor roll-ups:** *Entity-grain roll-up: one row per {DDG-51 /
  Virginia-class / Columbia-class} subawardee UEI, {CY2013-2026 / CY2016-2025 /
  CY2016-2025}; nominal dollars.*
- **Data — transaction fact spines:** *The raw {program} subaward pull, {CY range} - one
  row per deduped FSRS published report; nominal dollars, with {GFE primes and }MIB/BlueForge
  UEIs already removed upstream.* (GFE-primes clause **DDG only** — see §3.)
- **Data — enrichment dimensions:** *Per-UEI enrichment - {NAICS-6 industry / parent
  ownership}, not carried in the native subaward reports.* (The last two sheets are
  enrichments — attributes absent from the native FSRS reports, looked up for the
  program-vendor sheets.)
- **Guide — Methodology:** *How the classification is produced - unit, grain, the three
  axes, evidence precedence, and the assignment rule.* (A planned "code definitions live on
  the Taxonomy tab" pointer was added then removed per the user — no cross-tab pointer.)

## §3 — Research behind the year range + dollar basis

Two caption facts were confirmed against the data, not assumed:

- **Calendar year, not fiscal.** `Subaward Date` is an ISO calendar date (`2021-11-02`),
  so the per-program spans are **calendar years** → the captions say **CY**. The
  `FY22_25 = (2022, 2025)` constant in `_corpus.py` is the **competition deck's analysis
  window and is NOT applied to this raw pull**: the canonical **$13.1B reconciles to the
  all-years total ($13.17B), not the FY22-25 slice ($6.22B)**. So these sheets are
  full-history of the in-scope PIIDs.
- **Per-program spans** (from `Subaward Date`): DDG **CY2013-2026** (lone 2001 record
  dropped as noise; 2026 is partial YTD), Virginia **CY2016-2025** (2013×1 / 2015×2 dropped),
  Columbia **CY2016-2025** (clean). DDG legitimately runs a year longer than the subs.
- **Nominal dollars.** `subAwardAmount` is summed raw with no deflator anywhere → nominal
  (as-reported / current) dollars, *not* inflation-adjusted/constant. "Nominal" is the
  correct term.
- **Filter scope is not uniform.** The pull already strips, upstream in `_corpus.iter_records`:
  out-of-scope PIIDs; **GFE primes (DDG only** — DDG is restricted to the GD-BIW +
  HII-Ingalls shipbuilder-directed groups; the subs are all GDEB shipbuilder-directed so no
  GFE carve-out); and **MIB/BlueForge** UEIs (`excluded_mib_ueis`, all programs; the codebase
  term is **MIB**, not SIB). Hence GFE-primes appears only in the DDG transaction caption.

## §4 — §1 banners shortened (8 flat sheets)

Each parenthetical is now carried by the caption, so the banner drops to a bare label:

- model: `§1 - {program} subaward recipients` (was `… (entity-grain roll-up)`).
- data tx: `§1 - {program} subaward transactions` (was `… (raw FSRS published record, one
  row per subaward report)`).
- enrichment: `§1 - Subawardee UEI index` / `§1 - Subawardee parents` (dropped the
  NAICS-6 / standardized-parent parentheticals).

Methodology's own §-banners were already good and were left untouched.

## §5 — Taxonomy caption/banner/intro pass

Taxonomy had two layers of italic text (a sheet caption + a per-section intro under each
§-banner) that predated the new rule. Re-cut to match:

- **Top caption** (`GRAIN_INTRO`): the 5-sentence original → **"Entity- and
  transaction-level classification legends."** The earlier draft "Entity-level …" was
  wrong because **§4 SWBS is transaction-level**, not entity-level — the corrected phrasing
  spans both grains.
- **Section banners**: dropped the qualifier parentheticals, **kept "Archetypes"** (user
  call) and the `(SWBS)` acronym: `§1 - Capability Domain Archetypes`, `§2 - Operating Role
  Archetypes`, `§3 - Primary Output Archetypes`, `§4 - Ship-System Application (SWBS)`.
- **Section intros** (`DOMAIN_INTRO` / `ROLE_INTRO` / `OUTPUT_INTRO` / `SWBS_INTRO`):
  tightened, with each axis's **published/internal + scope flag moved into the intro** (the
  banner no longer carries it), and the **assignment-rule / boundary-test / lattice-pointer**
  lines dropped — those already render on Methodology (verified: `guide_methodology` imports
  `DOMAIN_TIEBREAKS`, `OUTPUT_BOUNDARIES`, `ROLE_OUTPUT_LATTICE`, `ASSIGNMENT_RULE`), so this
  is de-duplication per the legend-vs-methodology separation, not information loss. `SWBS_INTRO`
  keeps the transaction-level + HII-DDG scope flag and drops only the major-group/drill-down
  line (that lives in `SWBS_HIERARCHY_NOTE` below the §4 table).

The `*_INTRO` / `GRAIN_INTRO` constants live in `_taxonomy.py` and are consumed **only** by
`taxonomy.py` (Methodology imports the lattice/tie-break/boundary constants, never the
captions) — verified before editing, so the rewrites can't leak into Methodology.

## §6 — Files changed

**sheets/_flat.py** — `S_ITALIC` import; `intro=` param + docstring; cursor emits the italic
caption + `blank(2)` when `intro` is set (else the old single blank).
**sheets/{ddg,virginia,columbia}_program_vendors.py** — `intro=` (with CY range + nominal),
shortened `banner=`.
**sheets/{ddg,virginia,columbia}_subaward_transactions.py** — `intro=` (CY range + nominal +
filter note), shortened `banner=`.
**sheets/{subawardee_uei_index,subawardee_parents}.py** — `intro=` (enrichment), shortened
`banner=`.
**sheets/guide_methodology.py** — `S_ITALIC` import; inline italic caption + `blank(2)`
(pointer clause removed per user).
**sheets/_taxonomy.py** — `GRAIN_INTRO` / `DOMAIN_INTRO` / `ROLE_INTRO` / `OUTPUT_INTRO` /
`SWBS_INTRO` rewritten.
**sheets/taxonomy.py** — the 4 §-banner strings shortened.
**Outputs:** `award_classification_refactor.xlsx` rebuilt (10 sheets, 8 tables, 4 note parts).

## §7 — Verification (all green)

- Every rebuild clean: 0 XML errors, 0 error-literal cells, 8 native tables, 4 note parts
  (Methodology + the 3 program-vendor sheets), no repair.
- Rendered spot-checks against the built workbook: B3 caption + B6 §1 banner present on all
  10 sheets; CY ranges correct per program; Taxonomy B3 caption, §1-§4 banners, and the four
  section intros (B7/B24/B36/B49) match the intended text byte-for-byte.

## §8 — Conventions / gotchas (this session)

- **One house pattern, two wirings.** Flat sheets opt in via `_flat.make_flat_sheet(intro=…)`;
  non-flat sheets (Methodology, Taxonomy) write the `S_ITALIC` line + `blank(2)` inline. Both
  put the caption at **B3** and the §1 banner at **B6**.
- **Caption = orientation, banner = bare label.** The descriptive parenthetical moves from the
  §1 banner into the italic caption so the two aren't redundant. Applied to all 10 sheets.
- **Rendered text is ASCII-hyphen only** (sole non-ASCII glyph is `§`). Year ranges use a
  hyphen (`CY2013-2026`) to match `FY22-25`; lowercase `x` for "UEI x Program".
- **CY ≠ FY here, and the pull is full-history.** Don't confuse the `_corpus.FY22_25` deck
  window with this workbook's scope — the $13.1B is all-years; captions say CY off the raw
  `Subaward Date`. Per-program spans differ (DDG runs to 2026; subs to 2025); lone
  pre-start outliers are dropped from the stated range.
- **GFE-primes exclusion is DDG-only**; MIB/BlueForge stripping is all-program. The transaction
  captions reflect that asymmetry.
- **`_taxonomy.py` captions are Taxonomy-only.** Methodology shares the lattice/tie-break/
  boundary/assignment constants but not the `*_INTRO` strings — safe to rewrite the intros for
  the legend without touching Methodology.
- Build green = done; user verifies visually (`no-png-render-verification`).
