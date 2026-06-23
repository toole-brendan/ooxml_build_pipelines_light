# 2026-06-23 — TAM house-style formatting pass on the Award Classification workbook

Formatting session on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The ask was to bring the workbook in line with the
**Master TAM** workbook's house style — the user supplied a curated, TAM-only reference of the
reusable presentation logic (tab palette, the `title/caption/section` cursor rhythm, the
visibly-editable input cells) and asked for a "formatting pass." The workbook was already ~70%
aligned (it shares `workbook_core`, a centralized `_tabs.py`, a reader-first `SHEETS` order, and a
`RowCursor`); this session closed the three remaining gaps.

Workbook stays **19 sheets**, **15 native tables**. Build clean (**0 XML errors, 0 error-literal
cells**); house-style linter **0 failures, 0 warnings**. **No live formula and no data CSV was
touched** — this is a pure presentation pass.

Everything is **uncommitted** (working tree only).

---

## Scope (confirmed with the user before building)

Asked two clarifying questions up front:

- **Target = `workbook_award_classification_refactor` only** (not the sibling `award_analysis` /
  `army` / `mro`, which are already largely aligned).
- **In scope:** (1) tab-color palette, (2) layout helpers + sheet migration, (3) editable-input
  fill. **Out of scope:** a Checks/validation tab — that is closer to a new feature (needs
  award-specific validation logic), explicitly deferred.

Gap analysis going in: the award `RowCursor` already had the **named-anchor** machinery
(`marks` / `mark=`, from the 06-23 concentration-accessor session) that TAM's lacks, but was
**missing** TAM's `title/caption/section/subsection` helpers + `_detail` auto-outline; there was
**no** tab palette (defaulting to the loud `workbook_core` colors), and **no** input fill (inputs
were blue-font-only). So the cursor work was a **merge**, not a replace.

---

## What changed (14 source files + 1 new, +211 / −121)

### 1. Tab palette — `lib.py` (purely additive)
Added `import workbook_core.groups as _groups` + a per-build `_TAB_PALETTE` and
`_groups._COLOR.update(...)` at module import (before `build()` imports the sheets;
`group_color()` is read inside each sheet's deferred `render()`). The five groups this workbook
uses get the muted Master-TAM scheme: `summary` 262626 (charcoal), `guide` 2C5E5E (teal),
`inputs` 556B2F (olive), `model` 48596B (slate), `data` 203864 (navy). No `validation` key (no
Checks tab). Process-scoped — every other pipeline builds in its own process with its own colors.
No sheet module changed; each already calls `group_color(group)`.

### 2. `RowCursor` gains the TAM outline rhythm — `sheets/_layout.py` (merge)
Added, **alongside** the existing `marks` / `mark=` anchors (which are load-bearing for
`domain_concentration`'s cross-sheet ranges and were kept intact):
- `self._detail` running outline level; `title()` (level 0, folds the whole sheet), `caption()`
  (italic row-3), `section()` (level 1), `subsection()` (level 2) — each emits its banner and bumps
  `_detail` for the rows that follow.
- `write()` / `total()` now `setdefault("outline_level", self._detail)` (while still honoring an
  explicit override and the `mark=` capture).
- `blank()` is now **outline-aware**: inside an outlined region it emits an empty
  `<row outlineLevel=n/>` so a gap doesn't split the group (an absent row is an implicit level-0
  row); at level 0 it emits nothing, as before. **Row positions are unchanged** — `self.r` still
  advances by `n` either way, so every `mark`/accessor/`assert c.at()` stays valid.

### 3. Visibly-editable input cells — `sheets/_inputfill.py` (NEW)
Mirrors the Master-TAM `_inputfill.py`: registers ONE pale-yellow fill (`FFF2CC`) and a FILLED
clone of each input style this workbook uses — `S_NUM_INPUT_FILL` (numFmt 164), `S_INT_INPUT_FILL`
(168), `S_DATE_INPUT_FILL` (169), `S_TEXT_INPUT_FILL` (0) — each byte-identical to its non-filled
counterpart (font 3 = blue) with only the `fillId` added. Idempotent, process-scoped append to
`workbook_core.styles.FILLS` / `CELL_XFS` (the same trick `_text_input.py` / `_italic.py` use). No
percent variant — this workbook has no editable percent inputs.

### 4. Central flat-sheet builder — `sheets/_flat.py` (migration + opt-in fill)
- Migrated the banner block to the declarative helpers: `c.title(tab, ncols)` /
  `c.caption(intro)` / `c.section(banner, ncols)`, and dropped the manual `outline_level=1` on the
  data-row `c.write(...)` (the cursor now supplies level 2). One edit migrates **~13 flat tabs**.
- Added an opt-in `input_fill=False` param. When `True`, `_style(h)` returns the filled variant for
  an `input_cols` cell (a new `_INPUT_FILL_BY_TYPE` map + `S_TEXT_INPUT_FILL` for text) instead of
  blue-font-only. Removed now-dead imports (`S_TITLE_SHEET/SECTION`, `S_ITALIC`).

### 5. The 6 hand-built sheets — migrated to `title/caption/section`
`executive_summary.py`, `subaward_activity.py`, `market_bridge.py`, `guide_methodology.py`,
`taxonomy.py`, `domain_concentration.py`: every `c.banner(..., S_TITLE_SHEET)` → `c.title()`, every
`c.banner(..., S_TITLE_SECTION, mark_collapsible=True)` → `c.section()`, the row-3 intro →
`c.caption()`, and all the manual `outline_level=1` on body rows dropped. `domain_concentration`'s
`mark=` anchors were preserved; `subaward_activity`'s `assert c.at() == <precomputed row>` guards
still hold because positions are unchanged. Dropped the now-unused `S_TITLE_*` imports.

### 6. Surgical fill application — only the editable levers
`input_fill=True` on the **four `inputs`-group** sheets only: `naics6_archetype_map`,
`vendor_archetype_overrides`, `hii_swbs_crosswalk`, `deflators`. **Deliberately NOT** on the
`data`-group transaction spines or `model`-group `supplier_master` / `ddg_swbs_rollup` /
program-vendor sheets — those `input_cols` are source-evidence leaves and identity keys, not
editable levers, and filling thousands of rows would defeat the highlight.

### 7. House-style linter — `tools/style_audit.py` (one follow-on)
`title()` making the row-2 title collapsible (the TAM whole-sheet fold) tripped the audit, whose
heuristic assumed **every** gutter-`x` banner is a `§N` section → 19 false failures. The title is
already validated by the `B2 == tab name` rule, so the section-banner regex check now **skips
row 2**. This is the audit's outdated assumption catching up to the new (TAM-aligned) reality, not
a workbook defect.

**Behavioral note (intended):** the outline deepened from the old flat 1-level (a section folds its
level-1 body) to TAM's nested 2-level — the **row-2 title folds the whole sheet**, each `§`-section
folds its level-2 body. Section bodies moved from outline level 1 → 2; the title row became a
collapse control. `show_outline_symbols` per sheet was left as-is.

---

## Verification (all green)

| Check | Result |
|---|---|
| `python3 build_workbook.py` | exit 0, **19 sheets, 15 native tables**, 7 `_integrity` guards pass |
| `python3 validate_workbook.py` | parts 70, **0 XML errors, 0 error-literal cells** |
| `python3 tools/style_audit.py` | **0 hard failures, 0 warnings** |
| Tab colors (openpyxl readback) | all 19 tabs match the muted palette — **0 mismatches** |
| Input fill — levers | `FFF2CC` cells: Deflators **15**, NAICS Defaults **528**, Vendor Overrides **873**, HII→SWBS **270** |
| Input fill — non-levers | DDG Subaward Transactions / Supplier Master / Prime Awards: **0** fill cells (blue-font-only preserved) ✓ |
| Outline nesting (Deflators) | row 2 title `x`/level 0 → row 3 caption level 1 → level-1 blanks → row 6 `§1` `x`/level 1 → header+data level 2 ✓ |
| Diff footprint | 14 source files + new `_inputfill.py` + rebuilt `.xlsx`; **no data-build script / CSV touched** |

---

## Build / verify

```
# from workbook_award_classification_refactor/ (the dir with build_workbook.py):
PYTHONPATH=<repo-root> python3 build_workbook.py      # -> 19 sheets, 15 tables, exit 0
PYTHONPATH=<repo-root> python3 validate_workbook.py   # 0 xml errors, 0 error-literal cells
PYTHONPATH=<repo-root> python3 tools/style_audit.py   # 0 failures, 0 warnings
```

## Files

- **New:** `sheets/_inputfill.py` (pale-yellow filled input styles, process-scoped).
- **Engine helpers:** `sheets/_layout.py` (`RowCursor` + title/caption/section/subsection +
  outline-aware blank, anchors kept), `sheets/_flat.py` (helper migration + `input_fill` flag).
- **Bindings:** `workbook_award_classification_refactor/lib.py` (tab palette).
- **Sheets migrated:** `executive_summary`, `subaward_activity`, `market_bridge`,
  `guide_methodology`, `taxonomy`, `domain_concentration` (declarative banners); `deflators`,
  `naics6_archetype_map`, `vendor_archetype_overrides`, `hii_swbs_crosswalk` (`input_fill=True`).
- **Tooling:** `tools/style_audit.py` (exclude row-2 title from the `§N` check).
- **No data regen**; regenerated `award_classification_refactor.xlsx`.

## Carry-forward

- **Nothing committed** — working tree only.
- **Checks/validation tab deferred** (out of scope by the user's call). If built later, add a
  `validation` group + the `595959` muted-gray palette key (already the Master-TAM convention) and a
  reader-facing `checks.py` with bounds + a master verdict + red conditional formatting.
- **`input_fill` is the one switch** for the visibly-editable treatment — keep it OFF for any
  source-evidence or identity `input_cols`; turn it ON only for genuine editable-lever sheets.
- The `RowCursor` now carries **both** the named anchors (06-23 unification) and the TAM outline
  rhythm; future hand-built sheets should use `title/caption/section` + `mark=` rather than raw
  `banner()` + hand-counted `outline_level=`.
- Plan file for this session: `~/.claude/plans/could-you-please-do-soft-crescent.md`.
