# Session log — submarine deck spec + deck pipeline rewire + first slide build-out

**Date:** 2026-06-02
**Scope:** `core/submarine/deck/` (new), `core/ddg/deck/` (rewired), `core/deck_core/`
(added shared template/assets/docs — no engine code changes).
**Goal:** (1) Write a consolidated deck spec for the submarine supplier market-sizing deck;
(2) deprecate the stale, vendored deck pipelines and rewire both program decks to the shared
`deck_core` engine (mirroring the `workbook_sub → workbook_core` pattern); (3) start building real
slide modules and render them.

---

## 1. Deliverable A — `deck_spec.txt`

Path: `core/submarine/deck/deck_spec.txt` (plain text, not markdown, by request).

Built by consolidating three deck-design transcripts + `workbook_finish_handoff_plan_2026-06-02.md`
+ the finished workbook (`workbook/20260601_Distributed Shipbuilding Submarines_vS.xlsx`), then
revised against the real `deck_core` house style.

**v1 decisions (asked + confirmed):**
- Numbers: **reference values, workbook wins** — figures are a dated snapshot; source of truth is the
  workbook `Chart Data` / `Slide Data` / `Figure Register` at build time.
- Workbook side: **data-contract only** (CD_*/SD_* IDs + fields), not the workbook task list.
- Generic market-sizing theory: **dropped** (concrete spec only).
- Image placeholders via `_draft_slot`; takeaway shapes allowed but **varied, not identical on every slide**.

**v2 changes (after reading `deck_core/slide_guide.md`, `slide_snippets.md`, `style.py`,
`charts.py`, `primitives.py`, `text_metrics.py`):**
- **Per-slide chrome quadruple** documented: breadcrumb (`Section / Topic Label`), title
  (`Topic | Finding`), auto **Preliminary** chip, **Sources line** (2–3 primary, no final period).
  Sources were missing in v1 — added to every content slide.
- **Labels: HYBRID** — expand work-type buckets to "and" form on slides (`Electrical and power`,
  `Piping, valves and pumps`, …) but keep acronym compounds (`AP/LLTM`, `HM&E`, `GFE`, `SIB`, …).
  Workbook keeps slash forms as data keys. (Reversed v1's "mirror verbatim"; deck_core forbids `/` as
  a slide separator.) Includes a workbook-key → slide-label crosswalk.
- **Separators/typography** aligned to slide_guide (no `/ + x ->` word separators, no em dashes,
  `per year` not `/yr`; math operators OK inside formula/waterfall exhibits).
- **+4 section dividers** (`section_divider_layout`). Logical IDs **S01–S18 stay the workbook contract
  keys**; dividers shift cosmetic page numbers only.
- Title ≤2 lines (hard); color-role → palette map; **waterfall labels default OFF** caveat (overlay or
  bridge table); table skins (`dark`/`rule`/`light`) + `estimate_row_heights`; one black-outlined family
  + ≤1 focal callout per slide.

The 18-slide narrative spine, reference values, SIB terminology, and no-SOM rule are unchanged.

---

## 2. Audit — both deck pipelines were stale, vendored, NOT wired to `deck_core`

The correct pattern is the **submarine workbook**: a 463-byte `build_workbook.py` → thin
`workbook_sub/lib.py` that imports `workbook_core.*` and calls `package_workbook(OUT, SHEETS, …)`;
per-sheet modules registered in `sheets/__init__.py`; `__init__.py` bootstraps `sys.path`. No vendored
engine.

`core/deck_core/` is the matching shared engine: `lib.build_pptx(slide_module_renders, *, out,
extracted, assets, title, creator, app, …)`, `primitives.py`, `style.py`, `charts.py` (column / bar /
line / waterfall / marimekko), `slide_base_template.py`, docs, `tools/slide_probe.py`.

Findings:
- `submarine/deck/deck_sub/` and `ddg/deck/deck_ddg/` were **self-contained vendored copies** (own
  `lib/charts/primitives`), importing only `deck_{sub,ddg}.*`, never `deck_core`. `submarine/deck/
  build_deck.py` even still said *"telemetry one-pager"*. Both carried the retired 11-slide /
  50–65%-band model.
- A third stale copy under `ddg/research/deck/` (+ an OOXML schema/docs stash).
- Brand chrome triplicated and **byte-identical** (md5 of `slideMaster1.xml` and `media/image3.svg`
  matched across all three). `deck_core` shipped no template/assets of its own.

---

## 3. Archive + consolidation (nothing deleted — everything moved)

**Consolidated into `deck_core/` (the single source):**
- `deck_core/template/` — the unzipped PPTX chrome (slideLayouts 1–6, master, themes, handout, tags).
- `deck_core/assets/` — brand `media/` (6 files) + `embeddings/`.
- `deck_core/_schema/` (27 OOXML XSDs) + `deck_core/_docs/` — rescued from `ddg/research/deck`.

**Archived to dated `_archive_old_deck_20260602/`:**
- `submarine/deck/` — stale `deck_sub`, `_extracted`, `assets_deck`, `reports`, `tools`, old `.pptx`,
  `slide_topics.md`, vendored cheat-sheets.
- `ddg/deck/` — stale `deck_ddg`, `deck_telemetry_one_pager`, template/asset copies, old `.pptx`,
  `logs`, `telemetry_one_pager.pptx`.
- `ddg/research/deck/` — moved wholesale into the ddg archive after the schema/docs rescue.
  (`ddg/research/` proper, with its real research, was left untouched.)

---

## 4. Rewire — thin program decks on `deck_core`

Mirrors `workbook_sub → workbook_core`. Created for **both** programs:

```
submarine/deck/                      ddg/deck/
  build_deck.py                        build_deck.py          (thin launcher)
  deck_sub/__init__.py                 deck_ddg/__init__.py   (sys.path: project root + core/)
  deck_sub/lib.py                      deck_ddg/lib.py        (binds OUT/title -> deck_core.build_pptx,
                                                               TEMPLATE/ASSETS -> deck_core/{template,assets})
  deck_sub/slides/__init__.py          deck_ddg/slides/__init__.py   (SLIDE_RENDERS registry)
```

No vendored engine, no per-program chrome — both point `extracted=`/`assets=` at
`deck_core/template` and `deck_core/assets`.

**Smoke tests passed:** the engine builds a valid 1-slide `.pptx` from the consolidated chrome
(39 parts, slide master + 6 media present); both program launchers resolve the full
`deck_{sub,ddg} → deck_core` import chain and stop at the intended empty-registry guard.

---

## 5. First slide modules built (submarine)

Authored against `deck_core` (verified signatures first). Added a program-local
`deck_sub/slides/_helpers.py` (thin compositions: `chart_title`, `caption`, `commentary_rail`,
`kpi_card`, and a copy-from `_table` recipe) so slides stay short.

Modules written by me:
- `cover` (cover_layout), 4 dividers (`divider_market_scope/tam_build/sam_supplier/interpretation`,
  section_divider_layout).
- `executive_summary` (KPI cards), `basic_construction` (stacked column), `tam_bridge` (waterfall),
  `annual_cadence` (clustered column), `ap_lltm` (waterfall), `bucket_tam` / `sam_scenarios` /
  `sib_exclusion` (ranked bars).

Integrated from another agent (deck_core-aware):
- `coefficient_evidence` — from a `test/` drop (bar chart + evidence cards + method rail); rendered,
  then staged to `draft_slides/`. `test/` deleted.
- Front-of-deck drafts: `market_sizing_assessment` (cover), `market_primer` (ecosystem map),
  `sizing_boundary` (scope matrix), `executive_summary_v2` (hero-number KPI page), `demand_backdrop`
  (policy timeline). Renamed (stripped `slideXX_` prefix); the draft exec summary kept as
  `executive_summary_v2` to avoid colliding with mine (per "name one slightly differently").

Build progression verified: 1 → 12 → 17 slides, all exit 0.

---

## 6. Final reorg — skeleton registry + `draft_slides` preview loop

By request, the **real registry now holds only the skeleton**: the draft cover
(`market_sizing_assessment`) + the 4 dividers. All other content modules were **deprecated to
`draft_slides/`** (now an importable package: `__init__.py` bootstraps the path; `_helpers.py` copied
in for the `from ._helpers import` slides).

New **`build_draft.py`** (deck root): auto-discovers every non-`_` module in `draft_slides/` that
exposes `render()` and packs them into a separate scratch preview — no registry edits, never clobbers
the real deck.

**Final builds:**
- `build_deck.py` → `20260602_Distributed Shipbuilding Submarines_vS.pptx` — **5 slides** (cover + 4
  dividers), 0 charts.
- `build_draft.py` → `DRAFT_preview_Distributed Shipbuilding Submarines.pptx` — **14 slides, 8 charts**
  (annual_cadence, ap_lltm, basic_construction, bucket_tam, coefficient_evidence, cover,
  demand_backdrop, executive_summary, executive_summary_v2, market_primer, sam_scenarios,
  sib_exclusion, sizing_boundary, tam_bridge).

Promote workflow: copy a draft `draft_slides/` → `deck_sub/slides/`, add `from . import <name>` +
`(<name>, <name>.render)` to the registry, rebuild.

---

## 7. Decisions captured this session

| # | Question | Decision |
|---|----------|----------|
| 1 | Numbers in spec | Reference values; workbook wins at build time |
| 2 | Workbook side in spec | Data contract only |
| 3 | Generic theory | Drop |
| 4 | Slide labels (slash vs and) | **Hybrid** — buckets to "and", keep AP/LLTM, HM&E, etc. |
| 5 | Section dividers | Add 4 |
| 6 | Shared template/assets home | In `deck_core` (single source) |
| 7 | Execute scope | Archive + rewire **both** deck folders now |
| 8 | Exec-summary name collision | Name the draft slightly differently → `executive_summary_v2` |

---

## 8. State / next steps

- `deck_spec.txt` is v2 and engine-aligned; a slide author can copy
  `deck_core/slide_base_template.py`, set the 4 chrome fields from spec §4, and compose with the §7
  helpers.
- Real submarine deck is a 5-slide skeleton; 14 content slides are staged in `draft_slides/` for
  iteration via `build_draft.py`.
- `ddg/deck/` is rewired but its `SLIDE_RENDERS` is still empty (no ddg slides authored yet).
- Two executive-summary designs exist (`executive_summary` mine, `executive_summary_v2` draft) — pick
  one when promoting.
- Not yet built per the spec: S12 taxonomy, S15 visible suppliers, S17 data-limits iceberg, S18
  implications scorecard (S18 specced, not authored). Demand-backdrop policy events are narrative
  (not in the workbook `SD_05` contract, which holds analysis-window anchors only).

## 9. Gotchas / conventions to remember

- Do **not** edit `deck_core` to author a deck — compose with imported builders + slide-local
  `_`-helpers (program-local `_helpers.py` is fine; do not add shared helpers to `deck_core`).
- Logical slide IDs **S01–S18** are the workbook contract keys; dividers/cover shift only the cosmetic
  auto page numbers.
- `waterfall_chart` value labels default OFF (decrease stored unsigned) → overlay text or pair a bridge
  table for TAM/AP bridges.
- Native tables don't autofit — size rows with `text_metrics.estimate_row_heights`.
- Images aren't auto-wired by `build_pptx` — use `_draft_slot` stand-ins until rel-wiring lands.
