# 2026-06-03 — Workbook standardization: finished Phases 4-6 (Note/Basis scrub finish, sheet-spec reconcile, verification)

## Scope

Picked up `docs/2026-06-03_workbook_standardization_HANDOFF.md` ("Phase 4 ~95%,
Phases 5-6 not started") and **completed the job**: finished the submarines
Note-column strip (Phase 4), reconciled all 45 sheet specs to the renamed/scrubbed
modules (Phase 5), and ran the full verification battery (Phase 6). Both workbooks
build green throughout. Workspace is **not** under git / no backup, so each module
edit was followed by a rebuild.

Modules touched: 3 submarines sheets. Specs touched: all 45 (rename + header +
Notes-section). **No `workbook_core` changes; no formula/value/row edits** — only
trailing commentary-column removals and documentation reconciliation.

---

## Phase 4 finish — submarines Note-column strip (3 sheets)

Per the handoff's line-level spec; columns removed (rightmost commentary col, so
cols B/C don't shift and formulas stay valid), notes re-anchored to the value cell:

- **`guide_methodology.py`** — stripped §2a `Coefficient (live)|Value|Note` and §5a
  `Measure|$M|Note` (header + rows + matching style). Kept §3 `Method` (real
  crosswalk). Left the 4 glossary `ExcelNote`s on the §1 Definition cell (col C).
- **`model_sam_build.py`** — stripped §9 `Check|Status|Note` and §1 at-a-glance
  `Measure|Value|Note`; re-anchored the 2 `ExcelNote`s `B`→`C` (`alloc_unb`,
  `scen['broad']`). The import-time row-count asserts still hold (columns removed,
  not rows) — confirmed by a green build.
- **`chartdata_z_chart_data.py`** (the handoff's "optional" item) — stripped the §1
  at-a-glance `Measure|Value|Note` only. **Left the `tbl_deck_chart_data` manifest
  table untouched** (the PowerPoint pipeline reads it; its `Note` field is a real
  loader column). Rationale for doing it: DDG's chartdata has *no* such at-a-glance
  block, the handoff says "the at-a-glance summary blocks above the loader tables are
  fair game," and stripping it makes the two decks consistent (effort thread #1).

After: submarines builds green (21 tabs, 8 note parts); **no `ExcelNote(f"B{`
anywhere in either deck**; the only surviving `c.write([... "Note"/"Notes" ...])`
header literals are the two sanctioned submarines Sources columns.

## Phase 5 — reconcile all 45 sheet specs to the modules

Specs are not on any build path (pure docs), so this was done by script + targeted
edits with central grep verification. Authoritative inputs extracted up front: every
module's `_TAB` / `_GROUP` and its real `ExcelNote` anchor columns; `groups.py`
labels/colors; the surviving Note/Basis header columns.

1. **Rename + header rewrite (deterministic script).** Renamed the 17 stale-named
   specs to their module basename (10 DDG + 7 subs); rewrote lines 1-3 of all 45 from
   module data (tab name = `_TAB`, `Tab color: HEX (name)  ·  group: Label`,
   `Module: <name>.py`). Result: **spec basename == module basename, 1:1, both decks.**
   z_ChartData → `chartdata` / `404040`; subs POP Source Audit → `validation` / gray.
2. **Note-column lines.** Set `- Note column:` to `none.` on the 41 non-Sources specs
   (commentary columns were stripped or relabeled to real data). Kept/curated the line
   on the Sources specs (Sources exception): subs references §3, subs source_index §4
   (already correct); corrected DDG source_index `none.`→`§1.` (its §1 datasets table
   carries a real per-dataset Note column). Dropped all stale `Basis column:` mentions.
3. **Native-note anchors.** Updated every `§X (col):` anchor letter to the module's
   current anchor: blanket `B`/`D`/`E`→`C` for the all-C sheets; per-note mapping for
   the two mixed sheets (DDG `model_tam_build` §4a→`D`; DDG `validation_pop_source_audit`
   §2 masters→`D`). Dropped the two notes the cascade removed and fixed the counts:
   DDG `summary_executive_summary` 4→3 (dropped the §6 FFATA note),
   DDG `validation_sensitivity` 2→1 (dropped the orphan FFATA memo note).
4. **Stale tab-name sweep in prose** (Reads / Feeds / On-the-sheet / glosses), current
   names only — DDG: Inputs→Assumptions (guarding the `Inputs & levers` group label),
   Entities→Entity Master, Locations→Location Master, Bucket Evidence→Worktype
   Evidence, Deck Outputs→Figure Register, Figure Audit→Number Audit, QA Checks→QA
   Reconciliation, POP Audit→POP Source Audit, Source Lineage→Source Index; subs:
   Assumptions & Controls→Assumptions, Methodology & Scope→Methodology, SCN
   Annual→SCN Budget, LLTM AP→AP Bridge, POP Location Parse→POP Corpus, Chart
   Data→z_ChartData. Relabeled DDG `data_entity_master` body `Basis`→`Arbiter` (the
   module's relabeled real column). Reworded two `Assumptions assumption` double-words.

**Cross-check (0 problems):** for all 45 specs, `Native cell notes: N` == count of
`§X (col):` anchor lines == module `ExcelNote(` count. Headers re-validated against the
canonical group table; no old tab name survives in any spec body.

## Phase 6 — verification

| Check | Result |
|---|---|
| DDG build | exit 0 — 24 tabs, 12 native tables, 6 note parts |
| Submarines build | exit 0 — 21 tabs, 12 native tables, 8 note parts |
| Tab order / group / color | both decks match the handoff target exactly; groups contiguous, no order violations |
| z_ChartData | last tab, `chartdata` / `404040`, both decks |
| POP Source Audit | in `validation` (gray), both decks |
| DDG `validate_workbook.py` | 72 parts, **0 xml errors**, 24 sheets, **0 error-literal cells** (subs has no validator) |
| `ExcelNote(f"B{` anywhere | none |
| Stray commentary `Note`/`Basis` `c.write` headers | none (only the 2 sanctioned subs Sources columns) |
| Note-bearing sheets vs note parts | DDG 6/6, subs 8/8 |
| Spec ↔ module name parity | 1:1, both decks |

## Open items / caveats

- **Audit gates not evaluated.** The QA Reconciliation / Number Audit "0 FAIL" gates
  are runtime Excel formulas; this environment has no Excel, so I confirmed structure
  (green build, 0 xml errors, **0 error-literal cells** = no `#REF!`/`#VALUE!`) but not
  the computed gate results. The edits removed only trailing commentary columns and
  moved note anchors — no formula, value, or row changed — so the gates should be
  unaffected; **confirm in Excel for final sign-off** (no backup exists).
- **Cosmetic:** a few `Reads`-block rows lost monospace column alignment where a new
  tab name is shorter than the old (e.g. `AP Bridge` vs `LLTM AP`). Content is correct;
  left un-repadded.
- **Scratch:** `/tmp/phase5_headers.py` (rename + header script; one-shot, already run).
- The earlier `/tmp/ddg_cascade.py` / `/tmp/sub_cascade.py` (module rename scripts from
  the standardization session) remain; harmless.
