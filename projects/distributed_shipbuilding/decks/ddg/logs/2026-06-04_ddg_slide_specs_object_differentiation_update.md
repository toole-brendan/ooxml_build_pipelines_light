# 2026-06-04 — DDG slide specs: object-differentiation update (visual_differentiation → object_assessment + 7 rewrites)

## Scope

Applied two successive externally-authored update packages to the **21 DDG slide
specs** (`projects/ddg/deck/slide_specs/*.md`). The second package supersedes the
first, so the **surviving repo state** is: every spec carries an `object_assessment`
block, seven specs have real object-level rewrites, and `visual_differentiation` (added
by the first package) has been removed again per user direction.

Specs only — **no `deck_core`, no slide modules, no registry, no README changes**, and
submarines untouched. Specs are not on any build path, so the safety net is a YAML parse
of all 21 plus structural checks (no rebuild possible/needed). Workspace is not under git
and has no backup, so each package was diffed against the live specs **before** overwrite.

Both packages were branched from the pre-existing specs by an alternate AI agent; both
re-introduced the same `work_type_allocation` residual-label regression, caught and
reverted both times (see §3).

---

## 1. Pass 1 — `~/Downloads/updated_slide_specs` (visual_differentiation)

Per its `SPEC_UPDATE_NOTES.md`: added a `story.visual_differentiation` block
(`signature_move` / `contrast_with` / `avoid_repetition` / `build_notes`) to all 21, plus
parse-safety YAML requoting. Verified the diff was **purely additive** (~+237 lines total,
~10/file, all the new block) except cosmetic requotes:
- quoted the `"charts: [] -> no chart rId checks"` QA line (7 files),
- quoted the `"Foreign"`-leading caveat in `supplier_landscape`,
- split `sam_scenarios`' compact `cell_bold` inline map into one key per line.

No data / numbers / sources / chart-table defs / reserves changed. Applied, then on user
review the block was judged **thin** (mostly restated what `element_inventory` already
implied; only the `contrast_with` lines were genuinely new). → motivated Pass 2.

## 2. Pass 2 — `~/Downloads/ddg_aggressive_slide_specs_final` (object_assessment) — SURVIVING STATE

Package contents: 21 specs + `UPDATE_NOTES.md` + `VALIDATION_REPORT.{txt,json}` (the
non-spec files were **not** copied in). The package was branched from the originals, so it
contains **no** `visual_differentiation` — applying it deleted that block, which the user
explicitly confirmed ("delete the visual differentiation blocks").

Applied wholesale (21 files). Changes:
- **`object_assessment` block on all 21** — harsh verdict, `object_contract`
  (`render_pattern`, `expected_rendered_object_count`, `compound_objects`,
  `required_focal_family`), and `anti_repetition` rules. Answers "what objects get
  emitted?" instead of leaving the builder to infer count from prose.
- **7 object-level rewrites:**
  - `executive_summary` — removed the two-stream split chart → pure KPI answer board
    (2 hero cards + 4 support cards); `charts: []`.
  - `market_primer` — system map → counted connector/node contract (6 connectors,
    4 excluded-lane tags).
  - `cost_funnel` — generic right rail → 3-step denominator-decision ladder.
  - `tam_methodology` — two-stream equation engine (PLUS operator + named connector
    children).
  - `work_type_allocation` — removed right rail; full-width ranked bar + single gray
    residual cue.
  - `supplier_landscape` — caveat rail → native evidence table.
  - `ffata_visibility_gap` — explanation rail → 5 explicit missed-flow chips.
- **Filled-shape border fix** — `line_color: null` on filled shapes replaced with explicit
  `BLACK` / `GRAY_3`; **0 filled-shape `line_color: null` remain** (no-fill shapes still
  correctly use `fill: null` + `line_color: null`).
- YAML parse fixes (unquoted QA/check strings, invalid inline maps).

## 3. Recurring fix — `work_type_allocation` residual label

Both packages reverted the rendered residual label `Unbucketed / ambiguous` →
`Unbucketed and ambiguous` in 3 lines (chart category, `data_and_calculations` row, qa
line). This contradicts the documented canonical constant — `sam_taxonomy` **in the same
package** still carries qa lines asserting *"Unbucketed / ambiguous appears explicitly with
the canonical slash label"* and *"No visible … slash separators … except the canonical
'Unbucketed / ambiguous' label."* It's an accidental branch artifact, not an intended edit
(the notes promise chart/table defs were preserved). **Restored the slash both times.**
(Internal prose in `sam_taxonomy` reserve/data — "Unbucketed and ambiguous" as a sentence —
is pre-existing, not the rendered label, and left as-is.)

## Verification (final state)

| Check | Result |
|---|---|
| YAML parse | 21/21 |
| `object_assessment` present | 21/21 |
| `visual_differentiation` present | 0 (removed per direction) |
| Filled-shape `line_color: null` | 0 (matches package VALIDATION_REPORT) |
| `executive_summary` chart removal consistent | `charts: []`, support cards in `element_inventory`, QA updated ✓ |
| Residual label canonical slash | restored (all 4 lines in `work_type_allocation`) |

## Open items / follow-ups

- **27 stale `safe_container` references — NOT yet fixed (awaiting go-ahead).** The 7
  rewrites renamed/removed regions but did **not** update the `reserve.approved_extra_points`
  chips' `safe_container` tags, so they point at regions that no longer exist. This is soft
  density-bank guidance (not the build contract — nothing that builds is broken), but it
  degrades the handoff. Counts and proposed remap:
  - `executive_summary` (3): `card_tam`→`hero_tam`, `card_hull`→`support_hull`,
    `stream_chart`→**obsolete** (chart removed; chip should be dropped).
  - `market_primer` (4): `gfe_node`×3 → `excluded_gfe`; `supplier_rail` → `supplier_lane`.
  - `cost_funnel` (5): `rail` → `ladder_total` / `evidence_chip`.
  - `work_type_allocation` (5): `rail` → `residual_cue` / `note_strip`.
  - `supplier_landscape` (4): `rail` → `evidence_table` / `note_strip`.
  - `ffata_visibility_gap` (6): `rail` → the `chip_*` regions / `share_callout`.
  - (`tam_methodology` is clean — no dangling refs.)
- **`work_type_allocation` `commentary.visible`** still names `container: right_rail` with a
  "Readout" title though the redesign removed the rail (its `element` is `e3`, the residual
  cue). Cosmetic naming mismatch; flag for the same cleanup pass.
- **Submarine specs** untouched — the same object_assessment treatment has not been applied
  there.
- No deck rebuild (specs off the build path); if a module is later regenerated from one of
  these specs, run `slide_probe` against it.

## Files touched

- **Overwritten (aggressive package), `projects/ddg/deck/slide_specs/`:** all 21 specs.
- **Hand-corrected after copy:** `work_type_allocation.md` (residual slash, 3 lines).
- **Not copied:** the packages' `UPDATE_NOTES.md` / `SPEC_UPDATE_NOTES.md` /
  `VALIDATION_REPORT.*` (meta, not specs).
- **Not changed:** `deck_core/*`, workbook/research, `docs/spec_format/*`, registry, README,
  all submarine files.
