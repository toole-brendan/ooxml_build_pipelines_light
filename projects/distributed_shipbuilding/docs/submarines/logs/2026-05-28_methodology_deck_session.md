# 2026-05-28 — Methodology side-deck session

## Scope
Began building the methodology side deck (`sub_pptx/`) for the submarine outsourced new-construction analysis. The deck is a raw-OOXML PowerPoint generator (no python-pptx) — slide modules compose inline `<p:sp>` strings, `deck_submarines/lib.py` packages them into `sub.pptx`. Final session state: 3 of 6 planned slides built (cover, cost funnel, methodology computation pipelines).

---

## 1. Project housekeeping

- Identified that `sub_work/._METHODOLOGY.md` was a macOS AppleDouble resource-fork stub (binary metadata), not a real markdown file. The actual `METHODOLOGY.md` lived at `sub_work/submarine_outsourced_work/METHODOLOGY.md`.
- Audited the `._` files across the whole `sub_work/` tree: **2,194 total**, only **3 were orphans** (no real counterpart): `._METHODOLOGY.md`, `wiki_submarines/assets/._logos`, `wiki_submarines/assets/._photos`. The other 2,191 were AppleDouble companions to real files.
- **Deleted all 2,194 `._` files.** Windows-incompatible cruft from a Mac sync; useless on this filesystem.
- **Moved** `submarine_outsourced_work/METHODOLOGY.md` → `sub_work/METHODOLOGY.md` (project root).
- Flagged but did not fix: internal doc references inside METHODOLOGY.md (`wiki_submarines/`, `scripts/`, `extracted/`, `MIB_Excluded` sheet, `SAM_GOV_HOWTO.md`, `deck/`) are now off by one directory level after the move.

## 2. Methodology deck planning

Started from `sub_pptx/slide_topics.md` (older 5-slide outline) and iterated through several proposals. Final 6-slide plan written to `slide_topics.md`:

1. **Cover** *(existing)*
2. **Framing** — what we are measuring and why it is hard
3. **Scope & definitions** — IN/OUT scope panel + decoder ring
4. **Cost funnel + four denominators** — vertical funnel with denominator lens annotations
5. **Computation pipelines** — four parallel measurement pipelines *(existing slide rebuilt)*
6. **What this means & doesn't mean** — band visual, MIB exclusion, top caveats

Considered a competing 6-slide proposal from another agent and rejected most of it (lacked a computation-pipeline rebuild, demoted the four denominators, used a hub-and-spoke data-sources diagram that subtly violated the "never blend" guardrail). Folded in their framing-slide concept as our slide 2.

## 3. Slide rebuilt — `methodology.py` (computation pipelines)

### Diagnosis
The existing slide presented a **single chained equation** (FPDS + SAM − MIB = flow, then × PoP = allocation). This is wrong relative to the methodology in three ways:

- FPDS GFE prime obligations and SAM subawards are not additive — they sit in different lenses (§3).
- MIB is not subtracted from a sum — it is excluded from the FFATA subaward subset before bucketing (§8).
- There is no single chained computation. The methodology is a layered measurement framework — funnel decomposition, observed floor, band estimate, and geographic allocation are reported against different lenses and never collapsed (§1 + §9 guardrails).

### Rebuild — Option A: four parallel measurement lanes
Each lane is a small arithmetic expression `[input1] [operator] [input2] [equals] [output]`. Lanes are stacked vertically with a small caption above each:

| Lane | Equation |
|---|---|
| ① SCN funnel | SCN Total Ship Cost − Plans, GFE, change orders = **Basic Construction baseline** |
| ② Observed floor | GDEB-PIID subawards − MIB and BlueForge recipients = **FFATA-visible floor** |
| ③ Band estimate *(MODELED)* | Basic Construction baseline × 50/60/65% band = **Modeled outsourced layer** |
| ④ Geography | Action dollars × DoW POP % = **PoP-weighted allocation** |

- Operators are real DrawingML AutoShapes via `prstGeom` `mathMinus`, `mathMultiply`, `mathEqual`. Existing `_operator()` helper retained.
- Output boxes BLUE_5 with white text and 1.5pt borders (focal anchors); subtracted-term inputs GRAY_1 (Lanes ① and ②); multiplied-term inputs BLUE_1 (Lanes ③ and ④).
- Title swapped to: *"Methodology | Four parallel computations, reported against different denominator lenses"*.
- Breadcrumb topic label: *"Computation Pipelines"*.
- Sources line updated to drop FPDS (no lane uses it now) and reference SCN J-Books, SAM FSRS, and DoW announcements.

### Dependency connector
Added a thin gray dashed connector from Lane ① output → Lane ③ input (since the BC baseline computed in Lane ① feeds the band calc in Lane ③). Implemented as a `custGeom` `<p:sp>` polyline:
- Route: down into the gap below Lane 1, left to the slide's left margin (x=200,000), down past Lane 2 in the margin, right into Lane 3 input1's left edge. Three bends total.
- Implemented as `custGeom` because `bentConnectorN` caps at 2 bends and this route needs 3.

User feedback: shifted source point from bottom-left **corner** of the Basic Construction box to bottom-edge **center** so the line clearly exits downward.

## 4. Slide built — `cost_funnel.py` (cost funnel + four denominators)

New slide module. Wired into `deck_submarines/lib.py` as slide 2 (between cover and methodology) so the visual deck order matches the final plan. Bumped `N_SLIDES_OUT` from 2 to 3.

### Iterations
Went through five passes before converging:

**Pass 1 — Boxed funnel.** Vertical 4-level funnel of rectangles (Total → Plans/GFE/ChgOrd/BC → Yard/Outsourced → FFATA/Unseen) on the left, four lens cards stacked on the right, full-width BLUE_5 footer band. Too tight; text wrapped or clipped in the narrow Level 3 boxes.

**Pass 2 — More flexible helpers.** Applied a set of corrections: made `_filled_box` accept per-shape insets, optional `normAutofit`, `vertOverflow="clip"`; made `_funnel_box` support a compact label-only mode for the narrow Level 3 boxes; added a `_note_box` to use the empty Level 3 right side; tightened the denominator cards; added safe XML escaping via `xml.sax.saxutils.escape`; added three thin `bentConnector3`-style spine arrows linking adjacent levels.

**Pass 3 — Layered composition.** Adopted the layered-composition pattern from `deck_n81/slides/marauder_vs_consolidated.py`: every body block is a no-text background rectangle plus separately positioned no-fill textboxes layered on top, each precisely sized for its content. Bumped `_LEVEL_GAP` 100,000 → 300,000 EMU so spine arrows had room to read. Dropped autofit entirely.

**Pass 4 — Full visual redesign.** Replaced the boxed decomposition with a **sloped-ribbon funnel** via `custGeom` quadrilaterals (new `_quad_band_bg` helper). Non-focal categories (Plans, GFE, Change orders, Yard self-performed) moved to small **side chips** rather than co-equal boxes. Removed the spine arrows entirely (alignment carries direction). Replaced the four full BLUE_3 lens cards with a **quiet ledger panel**: headline lenses (2 and 3) marked by a narrow BLUE_3 left stripe + HEADLINE badge instead of full blue fill. Footer changed from full dark band to slim rule + small caption. Title shortened to *"Cost Funnel | Denominator choice determines the reported outsourcing band"*.

**Pass 5 — Final polish.** Removed the rounded-corner container around the lens column; switched all chips to sharp corners (changed `_pill` to use `_bg_rect` instead of the rounded helper); standardized all exterior shape borders to **1pt (12,700 EMU)** including focal funnel bands and Level 3 boxes; added a **1.5pt black bottom rule** directly under the "Four denominator lenses" header textbox. `_round_rect_bg` removed (no longer used).

### Final structure of `cost_funnel.py`
- Layered composition throughout (background rect + no-fill textboxes per element).
- Sloped focal pathway: Total Ship Cost → Basic Construction → Outsourced within BC → flat-bottom split (FFATA floor + Unseen layer).
- Context chips (Plans, GFE, Change orders) beside the BC band with a "Context buckets" caption; Yard self-performed chip beside the Outsourced band.
- Inline note to the right of the Level 3 split explaining observed (FFATA floor) vs modeled (Unseen layer).
- Open lens ledger (no outer container): left-aligned header with 1.5pt black bottom rule, four rows separated by 0.75pt hairline rules. Lenses 2 and 3 marked as headline via thin BLUE_3 stripe + HEADLINE chip.
- Slim guardrail footer: 1pt BLUE_5 horizontal rule + small bold dark caption.

---

## Final deck state

3 slides built and rendering cleanly:
1. **Cover** — unchanged (`deck_submarines/slides/cover.py`)
2. **Cost Funnel and Denominator Lenses** — `deck_submarines/slides/cost_funnel.py` (new)
3. **Methodology / Computation Pipelines** — `deck_submarines/slides/methodology.py` (rebuilt)

3 more slides outlined in `slide_topics.md`, not yet built:
- Framing (final order slot 2)
- Scope & definitions (final order slot 3)
- What this means & doesn't mean (final order slot 6)

Output artifact: `sub_pptx/sub.pptx`. Build entry point: `python sub_pptx/build_deck.py`.

---

## Reference files internalized this session

- `sub_pptx/ooxml_cheat_sheet_pptx.md` — sections 1-13 (parts, IDs, units, masters/layouts, themes, shapes, text, fills/lines/borders) and 16-18 (connectors, group shapes, custom geometry).
- `sub_pptx/deck_submarines/slides/body_template.py` — STYLE RULES (title format "Topic | Finding", color ramps, typography, "no /, +, ×, → as separators" prose rule) and CHROME specs (locked breadcrumb / title / sources / preliminary chip / page number coordinates and sp_ids).
- `sub_pptx/connector_ooxml.txt` — `p:cxnSp` with `bentConnector3` and unconnected `a:tailEnd type="triangle"` is the recommended pattern for fixed schematic arrows.
- `sub_pptx/schematic_ooxml.txt` — `mathPlus`, `mathMinus`, `mathMultiply`, `mathEqual` AutoShape preset geometries for arithmetic-style schematics.
- `C:\Users\BrendanToole\OneDrive - Saronic\Documents\N81 meeting\deck_n81\slides\marauder_vs_consolidated.py` — reference module that demonstrates clean layered composition (background rect + layered no-fill textboxes), the pattern adopted for `cost_funnel.py`.

---

## Open follow-ups for the next session

- Build the remaining three slides: Framing (slot 2), Scope & definitions (slot 3), What this means & doesn't mean (slot 6).
- Renumber methodology and cost_funnel positions in `lib.py` once the missing slides land (cost_funnel will move from slide 2 to slide 4; methodology from slide 3 to slide 5).
- Decide whether to update internal doc references inside `sub_work/METHODOLOGY.md` to reflect the new project-root location (folders like `wiki_submarines/`, `scripts/`, `extracted/` now sit one level deeper than the doc).
