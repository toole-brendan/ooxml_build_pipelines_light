# 2026-06-04 — DDG slide specs: add the `typography:` block (21 specs, purely additive)

## Scope

Applied an externally-authored typography package (`~/Downloads/typography_updated_specs/`)
to the **21 DDG slide specs** (`projects/ddg/deck/slide_specs/*.md`). Each updated spec adds
a top-level `typography:` block and changes nothing else. User direction was explicit:
apply them, and **don't block on format deviations from `SPEC_FORMAT.md`** ("i dont care if
they slightly go against the format of spec-format").

Specs only — no `deck_core`, no slide modules, no registry, no README, and submarines
untouched. Specs are off every build path, so the safety net is the pre-overwrite diff plus a
YAML parse of all 21 (no rebuild possible/needed). Workspace is not under git and has no
backup, so the package was diffed against the live specs **before** overwrite.

The package was branched from the **current** (`object_assessment`) spec state, not an older
copy — verified before touching anything (see §1), so the swap does not revert the 00:19–00:25
object-differentiation work.

---

## 1. Pre-overwrite verification (the deciding checks)

Two risks for an external package on a no-backup tree: (a) it was branched from a stale copy
and silently reverts recent work, (b) it claims to be additive but regresses numbers/content.
Both were ruled out before copying:

- **Branch point.** Every download spec already carries `object_assessment` (1/file, matching
  the current specs) and adds `typography:` (1/file, absent from current). So it was branched
  from the post-`object_assessment` state — the swap cannot revert that work.
- **Purely additive.** `diff current → download` for all 21 files: **0 removed/changed lines
  ('<'), only added lines ('>')**, 34–115 added per file (the `typography:` block). All
  numbers, `charts`/`tables`/`shapes`/`commentary`/`qa`, and the `object_assessment` blocks are
  preserved verbatim. The recurring `work_type_allocation` `Unbucketed / ambiguous` slash-label
  regression (reverted twice in prior sessions) **cannot have entered** — 0 removed lines there.

## 2. What the `typography:` block contains

Per the package `TYPOGRAPHY_UPDATE_CHANGELOG.md`, each block makes font/spacing/run hierarchy
first-class for the builder:
- `contract` — `font: FONT`, `line_spacing: LNSPC_BODY`, `body_runs_explicit`, emphasis/color
  rules, chart-size note.
- `defaults` — per-profile run sizing (external exhibit titles, no-fill notes, commentary
  rails, chips, table cells).
- `chart_rules` / `table_rules` / `shape_rules` — per-shape run breakdowns (cap / value /
  qualifier / body / lead-in roles, each with size + color + bold/italic + `FONT`).

## 3. Apply

Copied the 21 `*.md` specs over the current DDG specs (1:1 by filename). The package's six
**non-spec** files were **not** copied — they are out of the literal "DDG slide specs" scope
and the user waved off format alignment: `SPEC_FORMAT.md`, `style.py`,
`slide_base_template.py`, `slide_guide.md`, `slide_snippets.md`, `TYPOGRAPHY_UPDATE_CHANGELOG.md`.

---

## Verification

| Check | Result |
|---|---|
| Pre-overwrite diff (current → download) | purely additive, **0** removed/changed lines across all 21 |
| `object_assessment` still present | 21/21 |
| `typography:` now present | 21/21 |
| YAML parse (`safe_load_all`) | 21/21 |
| `work_type_allocation` slash label | untouched (0 removed lines) |
| Submarine specs / `deck_core` / registry | not touched |

## Files touched

- **Overwritten (typography package), `projects/ddg/deck/slide_specs/`:** all 21 specs.
- **Not copied:** the package's `SPEC_FORMAT.md`, `style.py`, `slide_base_template.py`,
  `slide_guide.md`, `slide_snippets.md`, `TYPOGRAPHY_UPDATE_CHANGELOG.md`.
- **Not changed:** `deck_core/*`, slide modules, registry, `docs/spec_format/*`, README, all
  submarine files.

## Open items / follow-ups

- **Undefined style tokens (flagged, user declined).** The typography blocks reference size
  tokens that are likely not yet defined in `deck_core/style.py` — e.g. `ANSWER_KPI_24PT`,
  `CHART_TITLE_10PT`, `DENSE_BODY_10PT`, `FINEPRINT_8_5PT`, `LABEL_9PT`, `CAP_12PT`,
  `VALUE_14PT`, `MESSAGE_11PT`, `LNSPC_BODY`. Harmless now (specs are off the build path), but a
  builder that consumes the `typography:` contract would need these added to `style.py`. User
  said not to chase this.
- **`SPEC_FORMAT.md` not updated.** The package shipped an updated `SPEC_FORMAT.md` documenting
  the new block; left the repo's copy as-is per the user's "don't care about format" direction.
  Apply it later if the `typography:` block should become part of the documented standard.
- **DDG-only.** The same typography pass has not been applied to the submarine specs.
- **Carried over from the prior DDG session (still open):** 27 stale `safe_container` references
  from the object-differentiation rewrites, and the `work_type_allocation` `commentary.visible`
  `right_rail` naming mismatch — untouched by this pass.
