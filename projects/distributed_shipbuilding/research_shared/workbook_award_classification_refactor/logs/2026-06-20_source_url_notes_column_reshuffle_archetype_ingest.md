# 2026-06-20 — Source-URL hover notes, M–P reshuffle, and the archetype-ingest pipeline

Session that moved the program-vendor sheets from "blank archetype columns + a visible
Source-URLs column" to a finished, evidence-rich layout on all three program-vendor
sheets (DDG / Virginia / Columbia):
1. **Source URLs → native Excel hover Notes** on the `Role / Description` cell, and the
   Source-URLs *column* deleted (Columbia first, then DDG + Virginia).
2. A **fake spacer column** (single space, no header) right of the table so the long
   `Role / Description` text stops instead of running across the empty grid.
3. **Reordered columns M–P** to `D · D-basis · P · P-basis` (group each archetype with its
   basis) — driven from the CSV source of truth, zero data drift.
4. Stood up the **archetype-ingest pipeline** and ingested all 6 completed classification
   pulls: codes into M/O, the `Research override` basis tier into N/P, and the per-axis
   **reasoning + sources into hover Notes** on the two basis cells. Methodology legend
   updated to the new basis vocab.

Build stays green throughout (0 XML errors, 0 error-literal cells, 8 native tables, no
repair). Follow-on to `2026-06-19_research_pull_ingestion_and_archetype_worklists.md`
(which shipped the worklists this session ingested).

---

## §1 — Native-note pipeline already existed; we used it three ways

`workbook_core/notes.py` + `lib.package_workbook` already wire legacy Excel Notes
end-to-end (comments part + VML drawing + sheet rels + `<legacyDrawing>` + content-types,
one comments/VML part per note-bearing sheet). A sheet just declares
`WorksheetSpec(ws, notes=[ExcelNote("Q7", "…")])`. We never touched `workbook_core`; all
new behavior lives in the project's shared builder `sheets/_flat.py`.

`make_flat_sheet` gained three opt-in params (default off → ddg/virginia/tx/dimension
sheets unaffected unless they opt in):
- **`note_from={anchor: source}`** — URL-normalized notes. Drops the source column from the
  visible table; per row, folds its value (via `_note_text`: split on whitespace/`|`/`;`,
  keep `http*` tokens one per line; **fall back to the raw text when a cell holds no URL** —
  e.g. Virginia's one `"No reliable public source located"` row, which otherwise would have
  vanished with the column) into a Note on the anchor cell.
- **`note_from_verbatim={anchor: source}`** — same drop+anchor contract, but the note text
  is used **as-is** (`_note_verbatim`: end-trim only, internal newlines preserved) for
  pre-composed evidence (the archetype Basis reasoning + sources). Internally both maps
  merge into one `note_specs = [(anchor, src, mode)]` list; an anchor must not appear in
  both (Excel keeps one Note per cell).
- **`right_spacer=True`** — writes a single-space cell in the column immediately right of the
  table on **data rows only** (no header, no banner extension, not in the table_ref) to clip
  a long final text column's overflow.

## §2 — Source URLs → notes + spacer (all three sheets)

Geometry (verified against the built workbook): header row 6, data from row 7;
`Role / Description` = **column Q**, the old `Source URLs` = column R. Wiring on each sheet:
`note_from={"Role / Description": "Source URLs"}` + `right_spacer=True`, and `W_URL` dropped
from `_WIDTHS` (17 → 16 visible columns; table `B6:Q…`).

Result: Source-URLs column gone; each prose cell carries a red-triangle hover Note listing
its sources (one URL per line); column R holds a `" "` on every data row to stop overflow.
Coverage: **DDG 98 / Virginia 100 / Columbia 95** URL notes (= the frontier prose rows),
0 orphans, exact 1:1 match between CSV rows-with-URLs and notes.

## §3 — Columns M–P reshuffled to `D · D-basis · P · P-basis`

Was `D · P · D-basis · P-basis`. The column order is owned by `HEADERS` in
`scripts/build_program_vendors.py` (the derived CSV's source of truth), and the four
archetype cells were emitted as positional **blanks** (`"","","",""`) so reordering the
headers needed **no row-construction change**. Process:
- Reordered the four `HEADERS` entries (+ the docstring column map).
- **Regenerated** all 3 CSVs and **diffed by column name vs backups**: row counts
  (470/645/595) + prose coverage (98/100/95) identical, **0 cell drift** — only column order
  moved. (Repo is not under git, so backups gave us the diff.)
- Swapped the two width slots in each module's `_WIDTHS` (P-code `W_CONF` ↔ D-basis
  `W_DOMFOR`) so each column keeps its width: M `W_CONF`, N `W_DOMFOR`, O `W_CONF`, P
  `W_DOMFOR`.

Live mapping now: **M** Capability Domain (D) · **N** Capability Domain Basis · **O**
Primary Output (P) · **P** Primary Output Basis · **Q** Role / Description.

## §4 — Archetype-ingest pipeline (the headline)

Mirrors the prose-research 3-layer pattern (raw archive → normalized intermediate CSV →
`build_program_vendors` consume → workbook). The 6 completed worklist pulls supply, per
UEI per axis: a **code** (D1–D10/D0, P1–P6/P0), a **free-text basis reasoning**, and
**source URLs**.

1. **Archive (immutable)** — the 6 pulls copied to `research_pulls/` as
   `{ddg,virginia,columbia}_{capability_domain,primary_output}_completed.xlsx`.
2. **`scripts/merge_archetype_pulls.py`** (new) — finds the classified sheet by header
   signature (must contain `Role / Description`, which disambiguates it from the slim
   `… Output` subset sheet some files ship), detects the URL column by `"url"` substring
   (headers vary: `URL Source(s)` / `Source URL(s)` / `URL source(s)`), keys by UEI, and
   merges both axes per program → `extracted/<program>_archetype_results.csv`
   (`UEI · D code · D basis · D URLs · P code · P basis · P URLs`). Output: **DDG 98 /
   Virginia 100 / Columbia 95**, both axes covering identical UEI sets (0 axis-only).
   Idempotent; raw pulls read-only.
3. **`build_program_vendors.py`** (extended) — `ARCHETYPE_RESULTS` map + `load_archetype()`
   + `fmt_archetype_note()` (reasoning, blank line, then URLs one per line). In the row
   build it fills **M/O = codes**, **N/P = the `Research override` tier** (constant
   `ARCHETYPE_BASIS`; a UEI in a pull was researched, so its basis is the research tier),
   and **two new transient HEADERS columns** `Capability Domain Note` / `Primary Output
   Note` (the composed evidence text). Unclassified (long-tail) rows stay blank.
4. **Render** — each module adds
   `note_from_verbatim={"Capability Domain Archetype Basis": "Capability Domain Note",
   "Primary Output Archetype Basis": "Primary Output Note"}`. The two note columns fold into
   verbatim hover Notes on the N/P **basis cells** and are dropped (so still 16 visible
   columns; widths unchanged).

So each basis cell shows the short tier `Research override`; hovering reveals the per-axis
reasoning + its specific sources. The codes (M/O) stay plain.

## §5 — Basis vocabulary decision + Methodology update

The basis columns are a **2-value method tier** (the cell), with the evidence in the note:
- **`Research override`** — classified from researched prose (these sheets are the registry
  now); takes precedence. The only value present this session.
- **`NAICS-6 map`** — the mechanical fallback for the long tail; **the map is not built
  yet**, so those rows are intentionally **blank**.

This replaces the originally-planned `Registry override` / `NAICS-6 map` from
`2026-06-19_program_vendor_refactor.md` §4/§6 (renamed `Registry override` → `Research
override` per the user). `guide_methodology.py` §1 "Assignment basis" now reads *"the method
that set the archetype label (not the result) — Research override (researched prose, takes
precedence) or NAICS-6 map; blank = not yet classified. Unresolved is a code (D0/P0), not a
basis."* and the §8 coverage line was updated to the same vocab (separating **method** from
**result** — `Unresolved` is the D0/P0 code, never a basis).

## §6 — Files created / changed

**scripts/** (new): `merge_archetype_pulls.py`.
**scripts/** (changed): `build_program_vendors.py` — reordered `HEADERS` (M–P) + 2 new note
columns; `ARCHETYPE_RESULTS` / `ARCHETYPE_BASIS` / `load_archetype` / `fmt_archetype_note`;
fills codes + tier + note columns in the row build; archetype coverage line.
**sheets/** (changed): `_flat.py` — `note_from`, `note_from_verbatim`, `right_spacer`,
`_note_text` (URL-normalize + non-URL fallback), `_note_verbatim`; `{ddg,virginia,columbia}_
program_vendors.py` — dropped `W_URL`, swapped M–P width slots, added `note_from` +
`note_from_verbatim` + `right_spacer`; `guide_methodology.py` — basis vocab (×2).
**research_pulls/** (new, immutable): 6 `*_completed.xlsx` archetype pulls.
**extracted/** (regenerated): 3 `*_program_vendors.csv` (now with codes + `Research
override` + 2 note columns), 3 new `*_archetype_results.csv`.
**Outputs:** `award_classification_refactor.xlsx` rebuilt (10 sheets, 8 tables, 4 note
parts).

## §7 — Verification (all green)

- Build clean at every step: 0 XML errors, 0 error-literal cells, 8 tables, note parts 4
  (Methodology + the 3 program-vendor sheets), no repair.
- Source-URL notes: DDG 98 / VA 100 / Col 95 on column Q, 0 orphans, exact CSV match;
  spacer `" "` on every data row of column R; Source-URLs column gone (16 cols, table B6:Q…).
- M–P reorder: order correct on all 3; regeneration drift = **0** on every non-archetype
  column.
- Archetype: codes filled 98/100/95 per program, `Research override` on **every** code row
  (0 code-without-tier), notes land on exactly **N + P + Q** with matching counts
  (e.g. Columbia 95/95/95). Columbia basis notes **190/190 match** the composed source
  byte-for-byte; format = reasoning → blank line → URLs.

## §8 — Open work / next-agent notes

- **NAICS-6 map pass (the long tail).** The bottom-of-$ rows with no `Role / Description`
  (~372 DDG / 545 VA / 500 Col) are unclassified. Building the NAICS-6 → archetype map (with
  the registry-vs-mechanical method) fills their D/P codes and sets their basis to
  `NAICS-6 map`. Until then those cells are blank by design.
- **Operating Role (R)** axis (R0–R5) still unassigned — needed for the Role × Output
  lattice QA (internal validation layer, not published).
- **Parent UEI** still blank pending a standardized parent-UEI list.

## §9 — Conventions / gotchas (this session)

- **Notes pipeline is opt-in per sheet** via `_flat.make_flat_sheet`: `note_from`
  (URL-normalized), `note_from_verbatim` (as-is), `right_spacer` (clip overflow). Never edit
  shared `workbook_core`; the engine already supports many notes / multiple note-columns per
  sheet (one comments+VML part per sheet, distinct refs).
- **Column order is owned by `HEADERS` in `build_program_vendors.py`**, not the sheet module.
  Reorder there + regenerate; widths in the module are **positional** and must be reordered to
  match. Archetype cells being blank made the reshuffle a pure header/width change.
- **Always back up + diff by column name before regenerating a CSV** (no git): row
  counts/prose coverage must hold, drift must be confined to the columns you intended.
- **Transient note columns** (Source URLs, Capability/Primary Output Note) live in the CSV
  only to be folded into notes and dropped by `note_from*` — they never render. `widths` count
  the columns that REMAIN after the drop.
- **Find the pull's data sheet by header signature, not name** (require `Role / Description`
  to skip the slim `… Output` subset sheet); **URL header name varies** — match on `"url"`.
- **Basis = method, not result.** Cell carries the tier (`Research override` / `NAICS-6 map`
  / blank); `D0`/`P0` "unresolved" is a code. Evidence (reasoning + sources) lives in the
  hover note, not a column.
- Build green = done; user verifies visually (`no-png-render-verification`).
