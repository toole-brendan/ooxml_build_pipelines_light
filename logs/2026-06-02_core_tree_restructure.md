# 2026-06-02 — core/ tree restructure: program-uniform layout, name de-collision

## Scope

Renamed the `core/` tree so the per-program branches stop colliding by name,
and deleted a dead legacy workbook. This is the third 2026-06-02 change to
this tree, after the submarine and ddg pipeline migrations (engine de-dup +
relocation into `core/`) logged at
[../submarine/logs/2026-06-02_sub_workbook_pipeline_migration.md](../submarine/logs/2026-06-02_sub_workbook_pipeline_migration.md)
and
[../ddg/workbook/logs/2026-06-02_ddg_workbook_pipeline_migration.md](../ddg/workbook/logs/2026-06-02_ddg_workbook_pipeline_migration.md).

Motivation: a single program previously had up to **five** things with
"work"/"workbook" in the name — `workbook_core`, `sub_work`, `sub_workbook`,
`workbook_sub`, plus a legacy `…/workbook/`. The trio `sub_work` →
`sub_workbook` → `workbook_sub` (program / project / package) were near-
identical, the middle two being the same two words reversed. That ambiguity
is what caused the original `workbook_core` shadowing mix-up.

---

## 1. New canonical layout

```
core/
├── workbook_core/        ← shared raw-OOXML xlsx engine (single source of truth)
├── deck_core/            ← shared pptx engine
├── submarine/            (was sub_work)
│   ├── workbook/         (was sub_workbook)  build_workbook.py + extracted/ + workbook_sub/
│   │   └── workbook_sub/ ← Python package (lib + sheets/); import name kept
│   ├── deck/             (was sub_pptx)      build_deck.py + deck_sub/
│   ├── research/         (was submarine_outsourced_work)
│   └── logs/  .claude/  *.md
└── ddg/                  (was ddg_work)
    ├── workbook/         (was ddg_workbook)  build_workbook.py + extracted/ + workbook_ddg/
    │   └── workbook_ddg/
    ├── deck/             (was ddg_pptx)      build_deck.py + deck_ddg/
    └── research/         (was destroyer_outsourced_work)
```

Rule of thumb now: **shared engines** (`workbook_core`, `deck_core`) sit at
`core/` root; **each program** is one folder (`submarine`, `ddg`) with three
peers — `workbook/`, `deck/`, `research/`. The importable build packages keep
program-suffixed names (`workbook_sub`, `workbook_ddg`, `deck_sub`,
`deck_ddg`) so cross-program imports never collide.

### Rename map

| old | new |
|-----|-----|
| `sub_work` | `submarine` |
| `sub_work/sub_workbook` | `submarine/workbook` |
| `sub_work/sub_pptx` | `submarine/deck` |
| `sub_work/submarine_outsourced_work` | `submarine/research` |
| `ddg_work` | `ddg` |
| `ddg_work/ddg_workbook` | `ddg/workbook` |
| `ddg_work/ddg_pptx` | `ddg/deck` |
| `ddg_work/destroyer_outsourced_work` | `ddg/research` |

Package names unchanged: `workbook_sub`, `workbook_ddg`, `deck_sub`,
`deck_ddg`.

---

## 2. Deletion

- **Deleted** the dead legacy workbook `submarine_outsourced_work/workbook/`
  (a self-contained May-24 package with its own `styles.py`, not used by the
  build — the ancestor of the current `workbook_core`-based pipeline).

---

## 3. Why the renames were safe (pre-move audit)

- **Workbook `sys.path` is depth-based** (`parents[1]` = project root,
  `parents[3]` = `core/`), so renaming intermediate dirs doesn't change
  resolution. Confirmed both workbooks still resolve `workbook_core` →
  `core/workbook_core` and build.
- **Deck pipelines are self-contained** — no `deck_core` import, no
  `sys.path` logic in `deck_sub`/`deck_ddg/__init__.py`; launched via
  `build_deck.py` at the deck-folder root. Depth-preserving rename is safe.
- **No symlinks** under `core/` (the "symlinked cache" comments in research
  scripts are Mac-era, not real here).
- **One load-bearing cross-read fixed**:
  `submarine/deck/deck_sub/slides/supplier_concentration.py` builds
  `parents[3] / "sub_workbook" / "extracted"` to read the workbook's data.
  `parents[3]` still lands on the program dir after rename, but the literal
  `"sub_workbook"` was changed to `"workbook"`. Verified end-to-end (loads 10
  vendors from `submarine/workbook/extracted/`). ddg's deck has no analogue.

---

## 4. Files updated (beyond the renames)

- `submarine/deck/deck_sub/slides/supplier_concentration.py` — cross-read
  literal `"sub_workbook"` → `"workbook"`.
- `submarine/workbook/workbook_sub/{__init__,lib}.py` and
  `ddg/workbook/workbook_ddg/{__init__,lib}.py` — path **comments** updated to
  the new layout (code unchanged; it's depth-based).
- `submarine/.claude/settings.local.json` — permission allowlist paths
  repointed (`core\sub_work\sub_workbook\extracted` → `core\submarine\workbook\extracted`;
  `core\sub_work\sub_pptx\deck_sub` → `core\submarine\deck\deck_sub`).
- The two prior migration logs — fixed broken relative links (sub) and added
  a "superseded names" banner (both).

---

## 5. Verification

- `submarine/workbook`: `python build_workbook.py` → 10 sheets, 8 tables,
  113,566 bytes; zip OK.
- `ddg/workbook`: `python build_workbook.py` → 10 sheets, 8 tables,
  79,521 bytes; zip OK.
- Deck cross-read exercised live: `_load_top_10_in_scope()` returns 10
  vendors from the renamed path.

---

## 6. Known stale-but-harmless references (NOT changed)

These are cosmetic (docstrings / comments / dead paths) and don't affect any
build. Left as-is to avoid risk; sweep later if desired:

- Docstrings still naming old folders: `deck_*/charts.py` ("to
  sub_workbook/sub.xlsx"), `deck_*/slides/body_template.py` ("sub_pptx/reports/…"),
  `*/deck/tools/slide_probe.py` (many "sub_pptx" comments + a `sub_pptx_root`
  variable name — depth-based, works regardless), `deck_ddg/__init__.py`.
- docProps `<dc:creator>` strings in `research/deck/build.py` naming
  `submarine_outsourced_work` / `destroyer_outsourced_work`.
- `research/scripts/*.py` hard-coded `/Users/brendantoole/projects2/…`
  absolute paths — Mac-era, already non-functional on this machine,
  independent of this rename.

## How to rebuild

```text
cd "core/submarine/workbook"  &&  python build_workbook.py
cd "core/ddg/workbook"        &&  python build_workbook.py
```
