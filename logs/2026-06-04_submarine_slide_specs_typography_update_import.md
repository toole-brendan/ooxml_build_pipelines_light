# 2026-06-04 — Submarine slide specs: import typography-updated versions (append-only)

## Scope

Replaced all **22 submarine slide specs** (`projects/submarines/deck/slide_specs/*.md`)
with the typography-updated versions supplied at
`~/Downloads/slide_specs_typography_updated/updated_specs/`. The user's instruction was
explicit: update every submarine spec to the Downloads version, and **format compliance
with `docs/spec_format/` does not matter** for this pass ("just update").

Specs are not on any build path, so there was no rebuild; the safety net was a mechanical
pre-copy verification (filename parity + append-only diff) and a post-copy byte-identity
check. Workspace is **not** under git / no backup — the copy overwrote each original in
place. No `deck_core`, registry, module, README, or DDG file was touched.

## What the update is

The Downloads source carries the same 22 filenames as the live submarine spec set (1:1,
verified — `diff` of the two `ls` listings was empty). Each updated file is a **pure
superset** of its current counterpart: the existing SlideSpec body is preserved **verbatim**
and a trailing block is appended:

```
# ── TYPOGRAPHY UPDATE ─────────────────────────────────────────────────────
typography:
  inherits: SPEC_FORMAT typography contract
  contract: { font, body_runs (explicit size+font), line_spacing, colors,
              chart_title_rule, fallback }
  elements:
    e1: { text_runs: [ { role, size: <TOKEN>, color, font, bold/italic } , … ] }
    e2: …
```

i.e. a per-spec `typography:` contract plus per-`element_inventory`-id (`e1`, `e2`, …)
text-run styling that pins each run's role → size token → color → font → weight/italic.

## Verification

| Check | Result |
|---|---|
| Filename set (src vs dst) | identical — 22 ↔ 22, `diff` empty |
| Diffs append-only (no body rewrite) | **0 of 22** non-additive (every change is an `aNNN` hunk) |
| Post-copy byte-identity (dst == src) | 0 mismatches of 22 |
| `TYPOGRAPHY UPDATE` block present | 22 of 22 |

The append-only check is the important one: it confirms the import added typography without
disturbing any existing `meta`/`chrome`/`story`/`regions`/`element_inventory`/`reserve`/`qa`
content from the prior object-discipline pass.

## Files touched

- **Overwritten in place** (`projects/submarines/deck/slide_specs/`): all 22 specs —
  the 17 body (`annual_cadence`, `ap_and_lltm`, `basic_construction`, `bucket_tam`,
  `coefficient_evidence`, `data_limits`, `demand_backdrop`, `executive_summary`,
  `implications`, `market_primer`, `methodology`, `sam_scenarios`, `sib_exclusion`,
  `sizing_boundary`, `tam_bridge`, `visible_suppliers`, `work_type_taxonomy`) + the 5
  appendix (`appendix_{definitions_and_scope, ap_and_lltm_detail, coefficient_sensitivity,
  sam_bucket_crosswalk, top_25_visible_suppliers}`).
- **Not touched:** `deck_core/*`, the registry/modules, the workbook, `docs/spec_format/*`,
  the README, all DDG files.

## Open items / follow-ups

- **DDG specs not updated.** The same typography pass has not been applied to the DDG slide
  specs; the Downloads source only carried submarine files. A parallel DDG pass would be a
  separate task.
- **Sibling docs left in Downloads, not imported** (out of scope — only the specs were
  requested): `SPEC_FORMAT_typography_updated.md`, `SPEC_FORMAT_typography_addendum.md`,
  `SLIDESPEC_TYPOGRAPHY_UPDATE_RECOMMENDATIONS.md`. Folding the addendum/updated format into
  `docs/spec_format/` is a separate decision (and would reconcile the "format doesn't matter"
  exception taken here against the standard).
- **No build / probe run.** Specs are documentation-only; if a module is later (re)generated
  from one of these enriched specs, run `slide_probe` against it to confirm the typography
  resolves to real `style.py` tokens.
