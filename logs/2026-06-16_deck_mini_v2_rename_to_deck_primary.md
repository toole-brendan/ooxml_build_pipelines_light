# 2026-06-16 — Rename `deck_mini_v2` → `deck_primary` (+ deliverable rebrand)

Pipeline: `projects/distributed_shipbuilding/deck_primary/` (was `deck_mini_v2/`)
Output:   `projects/distributed_shipbuilding/20260610_Distributed Shipbuilding New Construction_vS.pptx`
Build:    `cd deck_primary && /usr/bin/python3 build_deck.py`

## Goal

Promote the New Construction methodology mini-deck to the primary deck: rename the
directory `deck_mini_v2` → `deck_primary`, carry the rename through every dependent
file so the build stays green, and rebrand the user-facing deliverable away from the
"Mini v2" framing.

## What made it more than a folder rename

- **Nested package of the same name.** The build dir held a package also called
  `deck_mini_v2` (`deck_mini_v2/deck_mini_v2/`). Both dirs renamed; the two imports
  that resolve it updated (`build_deck.py` → `from deck_primary.lib`, `lib.py` →
  `from deck_primary.slides`), else the build breaks.
- **Output name + docProps are hardcoded** in `lib.py` (they do NOT derive from the
  folder name), so filename/title/creator/app were edited explicitly.
- **Path resolution is depth-based** (`Path(...).parents[N]`); the rename doesn't
  change tree depth, so all those indices stayed valid — no logic changes.

## Decisions (asked the user)

- **Rebrand the deliverable too** (not just code internals).
- **Live refs only** — update README/handoff/sibling-workbook comment; leave the
  `logs/` history untouched (records what was true at the time).

## Changes

**Directories** (`projects/distributed_shipbuilding/`)
- `deck_mini_v2/` → `deck_primary/`; nested `deck_mini_v2/deck_mini_v2/` →
  `deck_primary/deck_primary/`; stale `__pycache__` cleared (plain `mv`, repo not git).

**Package code** (`deck_primary/`)
- `build_deck.py` & `deck_primary/lib.py`: the two imports now resolve `deck_primary`.
- `lib.py` identity: `_CREATOR`/`_APP` → `deck_primary`; docstrings/comments/error-
  message path updated in all three files (`build_deck.py`, `__init__.py`, `lib.py`).
- Slide modules import only `deck_core.*` → untouched.

**Deliverable rebrand** (`lib.py`, plus mirror in `build_deck.py` docstring + `render.sh`)
- Filename: `20260610_New Construction Methodology Mini_v2.pptx`
  → (interim) `20260610_New Construction Methodology.pptx`
  → **final** `20260610_Distributed Shipbuilding New Construction_vS.pptx`
  (`_vS` convention matches the consolidated deck in the same folder).
- `_TITLE`: `Defense Demand Drivers - New Construction (Methodology Mini-Deck v2)`
  → **`Distributed Shipbuilding - New Construction`** (verified in docProps/core.xml).

**QA scripts** (`deck_primary/_qa/`)
- `render.sh` (new PPTX name + `deck_primary` png path), `regen_charts.sh` (both
  `_chart_xml` paths), archived `archive_pre_v3/make_chart4_hilo.py` string.

**Live docs**
- `README.md:42` tree entry; `handoff_competability_methodology_20260611.md` (×2);
  `workbook_outsourcing_ceiling/workbook_outsourcing_ceiling/__init__.py:12` comment.

**Cleanup** — removed orphaned old outputs: `…Mini_v2.pptx`, the interim
`…Methodology.pptx`, and the stale `_qa/png/…Mini_v2.pdf`.

**Memory** — updated `~/.claude/.../memory/{editable-bundled-chart,
consolidated-mini-deck-port}.md` so they point at `deck_primary` (old `_qa` log
filenames keep the `deck_mini_v2` token by design).

## Deliberately NOT changed

- `deck/deck_consolidated/slides/fr1_body_outsourced_bc_walk.py:438` — a provenance
  comment crediting "the deck_mini … table rules" (a credit, not a path).
- All `logs/` history (per "live refs only").

## Verification

- Build green: exit 0, **11 slides / 7 charts** → the new `_vS` deliverable (charts
  bundle OK, so the editable-bundled-chart path still resolves post-rename).
- `rg deck_mini_v2 projects/distributed_shipbuilding/deck_primary` → **0 hits**.
- `rg deck_mini_v2 --glob '!logs/**' .` → **0 hits** (only `logs/` retain the token).
- docProps `dc:title` in the built file reads `Distributed Shipbuilding - New
  Construction`.

## State / open items

- Filename keeps the `20260610` date prefix (the deck's vintage), even though the
  rename happened 2026-06-16.
- `render.sh` PNGs not regenerated this session — the existing `_qa/png/slide-*.png`
  still show the old 6-slide render; run `bash deck_primary/_qa/render.sh` to refresh
  to the current 11-slide deck.
