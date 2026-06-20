# 2026-06-16 — Outsourcing Ceiling: plain-language methodology doc (new Word pipeline)

Pipeline: `projects/distributed_shipbuilding/doc/doc_outsourced_ceiling/`
Launcher: `projects/distributed_shipbuilding/doc/build_outsourced_ceiling.py`
Output:   `projects/distributed_shipbuilding/20260616_Outsourcing Ceiling_Methodology_vS.docx`
Build:    `cd projects/distributed_shipbuilding/doc && python3.12 build_outsourced_ceiling.py`

## Goal

Produce a from-the-top, plain-English explainer of the **Outsourcing Ceiling**
methodology (the workbook built 2026-06-15, see
`2026-06-15_outsourcing_ceiling_workbook.md`) — for a reader who has never opened
the workbook. User asked for a NEW doc folder `doc/doc_outsourced_ceiling` that
**reuses the existing Word build pipeline**, modeled on the sibling page module
`doc/doc_distributed_shipbuilding/pages/rebuy_methodology_explainer.py`, mimicking
its formatting/styling as closely as possible.

## What was built — new self-contained pipeline mirroring doc_distributed_shipbuilding

Same shape as the sibling: thin per-doc package + a launcher one level above it;
shared raw-OOXML engine is the canonical `docx_core` at the workspace root (no
vendored copy). The new folder sits at the same depth, so the `__init__.py`
`parents[1]`/`parents[4]` sys.path logic is identical.

- `build_outsourced_ceiling.py` — launcher (`from doc_outsourced_ceiling.lib import build`).
- `doc_outsourced_ceiling/__init__.py` — sys.path setup (build dir + workspace root).
- `doc_outsourced_ceiling/lib.py` — binds `OUT` (project root, `…_Methodology_vS.docx`)
  + docProps identity; `build()` calls `docx_core.lib.package_docx`.
- `doc_outsourced_ceiling/pages/__init__.py` — `PAGES = [ceiling_methodology_explainer]`.
- `doc_outsourced_ceiling/pages/ceiling_methodology_explainer.py` — the page.

## The page module (styling lifted verbatim from the reference)

Copied the reference's helpers unchanged so rendering is identical in kind:
`_h` (black-run heading override + thin gray `_HRULE` under H1/H2 — no blue font),
`_rule_table` (inline `<w:cantSplit/>` per row + repeating header), `_list`/`_olist`
(hand-drawn markdown glyph hierarchy • ◦ ▪, one indent system, 6pt after-list
breather), and the local `PageSetup` for 0.75in left/right margins (top/bottom stay
1in). Only the INTENT/OUTLINE docstrings, `PAGE_TITLE`, and `_body()` are new.

Content is plain-speak, faithful to the workbook log: the ceiling question → the
breakthrough (no published make/buy line + today's POP share is the **floor**, so
**build** the ceiling from two sourced numbers) → Basic Construction basics →
the two numbers (h ≈ 50% movable hours; L ≈ 40% labor share, re-based onto BC) →
core vs. ceiling identity → hours→dollars bridge → headline (Table 1: ~75–80%
ceiling, ~3× today's distributed share) → two honest limits → sourced inputs
(Table 2). Sources softened to reader-facing prose (Rucker/Defense News, CRS+CBO,
FMR+10-Ks, POP shares); source line points back to the workbook for exact figures.

## Two user revisions during the session

- **Dropped the "Why the old answer wasn't good enough" (×1.30) section** and
  scrubbed the two other spots that leaned on the ×1.30 comparison. Rationale
  (user): the ×1.30 intent uplift was never actually replaced — the analysis ended
  up using the **POP %s as the primary frame** (the prior award analysis was
  backward-looking anyway), so leading with "replacing ×1.30" misframes the page.
  The "vs. today" column is now strictly ceiling-vs-POP-floor.
- **Added a top orienting section** `Where this fits in the distributed shipbuilding
  project`: one-line project framing + a two-item split — backward-looking (the
  separate Award Analysis workbook: who already wins outsourced work, concentration,
  re-buy cadence) vs. forward-looking (this workbook: the upper bound) — closing on
  the headline read as the gap between today's distributed share and the ceiling.

## Verification

- Build green: `1 page`, wrote the .docx at the project root (no XML errors).
- `docx_core/doc_probe.py` on the built .docx: **1 × H1, 10 × H2**, outline reads
  *Where this fits → The question → The breakthrough → Basics → The two numbers →
  Core vs. ceiling → Hours to dollars → What we found → Two honest limits → Where
  the numbers come from*; **2 RuleTables** (4-col headline, 3-col sources); portrait,
  margins `left/right = 1080 twips (0.75in)`, `top/bottom = 1440 (1in)`; one Source
  line. Probe artifacts under `doc/reports/doc_probe/`.
- Grep confirms no `1.30` / `1.3` / "old model" / "round guess" strings remain.

## State / notes

- **Stand-alone doc**, same as the workbook — nothing wired into the live model;
  it is a reader-facing companion. Rebuild after edits with the launcher above.
- Slide-mock pages from the sibling pipeline were not ported; this folder carries
  the single prose explainer page only.
