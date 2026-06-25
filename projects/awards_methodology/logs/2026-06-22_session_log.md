# 2026-06-22 - Session log (deck_awards_methodology)

Swapped the Awards Methodology deck from its prior methodology / alternative-versions
slide set over to a three-slide "Market Sizing" contracts set, archived the old modules,
and did a breadcrumb + ordering pass. Build stayed green throughout
(`python build_deck.py` -> 3 slides, 0 charts, no repair). Output:
`20260622_Awards Methodology_vS.pptx` at the deck root.

---

## What changed

1. **Archived the old slide set.** Made `deck_awards_methodology/archive/` and moved all
   10 existing slide modules out of `slides/` into it (`customer_anatomy`, `budget_bridge`,
   `awards_universe`, `awards_universe_2`, `methodology_sources`, `budget_to_customer_pipeline`,
   `award_data_pull_workflow`, the two `divider_alternative_versions*`, and the prior
   `contracts_recompete_timing`). `slides/` keeps only its `__init__.py` registry. The archive
   has no `__init__.py` - retained but not importable/built.

2. **Installed three new active modules** (copied from `~/Downloads`, all syntax-checked and
   built clean):
   - `contracts_recompete_timing.py` - recompete-clock swim-lane schematic
   - `contracts_obligated_vs_unobligated.py` - contract-value snapshots vs additive action obligations
   - `contracts_award_data_sourcing.py` - source methodology -> one validated operating model

   All three are `LAYOUT = "slideLayout4"` body slides with a `render()` and no `CHARTS`.

3. **Recompete-timing re-swap.** Replaced `contracts_recompete_timing.py` with the newer
   `~/Downloads/contracts_recompete_timing (2).py` (20.5 KB version). Same filename, so the
   registry was untouched by this swap.

4. **Rewrote the registry** (`slides/__init__.py`) to register only the three, then **reordered**
   to the requested sequence:
   1. `contracts_recompete_timing`
   2. `contracts_obligated_vs_unobligated`
   3. `contracts_award_data_sourcing`

   (Note: data sourcing intentionally lands last, with timing as the lead hook - flagged as
   slightly unusual for a methodology arc, user confirmed the order.)

## Breadcrumb pass

`breadcrumb(section, topic_label)` renders **bold `{section}`** + non-bold ` / {topic_label}`.
Previously each module passed `_TOPIC` for both the breadcrumb second half and the title topic.

- Set `_SECTION = "Market Sizing"` on all three (was `Contracts` / `Contract Vehicles` / `Contracts`).
- Added a **distinct `_BREADCRUMB_TOPIC`** per module (the house pattern, per the archived slides:
  breadcrumb second half is a separate, slightly different label from the title topic) and pointed
  `breadcrumb()` at it. Title topics (`_TOPIC`) left unchanged.
- Second halves are **Title Case** (per user correction; "and" stays lowercase):

  | # | Module | Title topic (`_TOPIC`) | Breadcrumb |
  |---|--------|------------------------|------------|
  | 1 | contracts_recompete_timing | Recompete Timing | **Market Sizing** / Recompete Addressability |
  | 2 | contracts_obligated_vs_unobligated | Obligated vs. Unobligated | **Market Sizing** / Obligated and Unobligated Value |
  | 3 | contracts_award_data_sourcing | Award Data Sourcing | **Market Sizing** / Sources and Validation |

## Notes / open items

- The whole `projects/other/awards_methodology/` tree is still **untracked in git** - all moves
  above were plain filesystem ops, nothing staged.
- A stale `~$20260622_Awards Methodology_vS.pptx` lock file sits at the deck root, suggesting the
  deck may be open in PowerPoint. Close it before reopening the freshly built file.
- The archived modules are dead files; if any are wanted back, re-copy into `slides/` and
  re-register in `slides/__init__.py`.
