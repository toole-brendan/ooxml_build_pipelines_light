# Session 2026-04-17 (IV): Deck Design, Designer-Facing Sheet Polish, and Standalone Services File

## Context

Building on `SESSION_2026-04-17_iii_top_contractors.md` (v2.53 workbook with Ultimate Parent + Consolidated top-15 tables and per-segment top-3 tables).

Two goals this session:
1. Design a 4-slide deck built entirely from the Services sheet, ready for a designer / analyst to execute.
2. Polish the Services sheet itself so the designer can identify which tables map to which slides without reading the full 400-row sheet, and extract a single-sheet standalone file they can work from directly.

Ended at **v2.55 workbook** + `output/Services_Sheet_Only_v2.55.xlsx` (single-sheet extract with values) + two new documentation files at root (`DECK_SLIDES.md`, `WHY_PSC_DATA.md`).

---

## Work completed, in order

### 1. 4-slide deck structure designed

Iterated with the user through several passes:
- Initial 4-slide skeleton (size -> shape -> contractors -> where to play)
- Reconciled with the pre-existing `DECK_WIREFRAMES.md` (which had more content / numbers but ASCII-art placeholder charts)
- Critique from a parallel AI agent ("chart-led, not table-led") adopted where appropriate, with two counter-arguments preserved: keep the PSC primer on Slide 1 (DD decks travel as PDFs, speaker notes don't) and keep the margin overlay visible on Slide 4 (the 3x OI-margin spread is the investor punchline)
- User pushed to de-emphasize exclusion detail on Slide 1 in favor of a positive case for PSC-coded data

Final Slide 1 anchor visual is the **PSC universe funnel** (Option A: 2,539 active PSCs -> ~1,800 services -> 68 ship MRO -> $7.1B TAM). This replaced an earlier proposal for a PSC taxonomy tree (Option B, "Product vs Services") which was drafted but not chosen.

### 2. Documentation created at root

**`DECK_SLIDES.md`** - complete 4-slide spec with content blocks, hero numbers, callouts, takeaways, and footnotes. Heavy iteration:
- Slide 4 rank-10 contractor swapped Pacific Shipyards -> S.C.A. Shipping Consultants (matches v2.53 data)
- Rank-4/6/8 $ rounding corrected (Vigor 439->440, Detyens 226->225, East Coast 141->142)
- Port & Technical row added to the Top-3-per-segment table (was missing)
- Electronics/C4ISR takeaway reworded ("top 3 cluster at ~15%" rather than "no leader >15%", since Amentum is 15.1%)
- `Other` row on Slide 2 corrected from $525M / 7.4% (stale wireframe data) to $952M / 13.5% (current v2.55), flagged by a parallel AI agent reviewing the spec

**`WHY_PSC_DATA.md`** - consolidated argument for PSC-coded contract awards vs Navy/USCG budget exhibits. Pulls together content previously spread across:
- `methodology.md` section 1 ("Why Awards Data")
- `OBJECTIVE.md` ("Why Awards Data Only")
- `restructuring/restructure_progress.md` (Phases 5-7, the v1.x reconciliation attempt)

Five-part structure: TL;DR, what was tried in v1.x and why it didn't work (3 structural problems), positive case for PSC data, external validation (GD 10-K $1,183M vs our $939M), scope caveat (public-yard gap), where budget data still earns its keep, summary decision table.

### 3. Workbook polish - v2.53 -> v2.54

Added two designer-friendly blocks to Services sheet:

**`_write_tam_headline(ws, r, mc)`** - summary block inserted between the purpose row and the first cross-tab. Writes:
- Navy / USCG / Total Services TAM with $M and % of TAM
- 6-segment roll-up directly below (Depot, HM&E, Combat Systems, Nuclear, Electronics/C4ISR, Port & Technical)

All values are live SUMIFS against `AwardsByHull`, not hard-coded. Makes Slide 1 (Navy/CG split) and Slide 3 (segment totals) readable from a single block instead of scanning multiple tables at R351, R361, R371.

**Market Concentration callout** - added as a new `include_concentration` kwarg to `_write_top_contractors`. When True, appends Top 3 / Top 10 / Top 15 cumulative share rows after the Services TAM row, referencing the Cumulative % column above. Enabled only on the Consolidated Top 15 call.

v2.54 workbook built successfully. Row positions shifted down ~17 rows from the headline block insertion; all named ranges and cross-sheet references adjust automatically (dynamic row positions).

### 4. Workbook polish - v2.54 -> v2.55 (designer-facing tables)

Four changes in one build:

**(a) Percentages rounded to 0%** - `PCT_FMT` changed globally in `styles.py` from `'0.0%;[Red](0.0%);"-"'` to `'0%;[Red](0%);"-"'`. Affects all sheets, not just Services. User confirmed this is fine.

**(b) Contractor names title-cased on display.** New `titlecase_contractor()` function in `services.py`:
- Pre-cased names pass through unchanged (e.g., `'BAE Systems'` from `CORPORATE_PARENT_ROLLUP`)
- All-caps FPDS names converted to Title Case (e.g., `'VIGOR MARINE LLC'` -> `'Vigor Marine LLC'`)
- Preserves always-upper acronyms (LLC, USA, BAE, HII, PCCI, SAIC, L3, etc.) via an allowlist
- Preserves dotted acronyms like `S.C.A.` via regex
- Handles possessives correctly: `COLONNA'S` -> `Colonna's`
- Applied in both `_write_top_contractors` and `_write_segment_contractors` at the display column only; SUMIFS criterion uses the original uppercase name (Excel SUMIFS is case-insensitive, so this is safe)

**(c) Margin overlay table added.** New `_write_margin_overlay(ws, r, mc)` helper placed between the Consolidated Top 15 block and the Consolidated Top-3-per-Segment block. Two sub-tables:
- Consolidated parents: HII / GD / BWXT with FY2025 revenue, OI, OI margin, and services-TAM relevance
- Pure-services sub-segments: HII Mission Technologies, GD Marine Systems, BWXT Gov Ops

Values hard-coded from `sheets/public_comps.py` CONSOL and SEG dicts (FY2025 10-K disclosures). Cross-sheet formulas avoided to keep the block simple; the overlay is labeled "See Public Comps sheet for full time series" for anyone who wants the audit trail.

**(d) Designer-facing tables marked with italic title + pale yellow body.** New `BG_YELLOW` fill and `F_SUBSEC_I` / `F_SLIDE_NOTE` fonts in `styles.py`. New helpers in `services.py`:
- `_designer_subsec(ws, r, text, mc, slide_tag=None)` - subsec_band with optional italic suffix `" -- Slide N"`
- `_shade_body(ws, r1, r2, c1, c2)` - applies pale yellow to rectangle, skips dark-filled cells (band rows keep their color)
- Modified `_write_condensed` in `product_procurement.py` to accept `slide_tag` param (default None preserves Product Procurement sheet behavior unchanged)

Seven designer-facing tables marked:
| Row | Table | Slide |
|---|---|---|
| 4 | Services TAM Headline (Navy/CG split) | Slide 1 |
| 10 | by MRO Segment (segment rollup) | Slide 3 |
| 242 | MRO Segment Definitions | Slide 3 |
| 308 | Top 15 Contractors Consolidated + Market Concentration | Slide 4 |
| 338 | Public Comp FY2025 Margin Overlay | Slide 4 |
| 355 | Top 3 Contractors per MRO Segment (Consolidated) | Slide 4 |
| 382 | U.S. Navy + Coast Guard Vessel Type Rollup ($M) | Slide 2 |

Per user spec: Ultimate Parent (as-reported) tables and the Navy-only / CG-only hull-program tables are explicitly left unshaded. Designer uses the Consolidated tables and the Navy+CG combined vessel type rollup only.

### 5. Standalone Services file

Created `output/Services_Sheet_Only_v2.55.xlsx` containing just the Services sheet with all values and formatting but no formulas or cross-sheet references.

Process:
1. openpyxl alone could not populate cached values (it writes formulas but can't evaluate them)
2. Ran `soffice --headless --calc --convert-to xlsx` to force LibreOffice to evaluate all formulas and rewrite the file
3. Loaded the evaluated file with `data_only=True` and copied each cell (value + style) to a fresh single-sheet workbook
4. Preserved merged ranges (14), column widths (6), row heights (444), tab color, sheet view properties

Result: 444 rows x 33 cols, ~2,345 yellow-shaded cells, 14 merged ranges, italic slide-tag titles intact. Verified sample values: Navy TAM $6.79B, CG TAM $273M, Total $7.07B, BAE consolidated $1.07B.

### 6. Slide copy editing

User built 4 slides in a slide tool; shared screenshots. Walked through each slide row-by-row:

**Slide 1 (Methodology)**
- Title: `"PSC-based classification identifies $7.1B"` -> `"A bottom-up read from 68 services PSCs sizes the FY2025 ship MRO market at $7.1B"`
- Funnel box 1 descriptor: `"Module build and systems integration over ~5-7 years"` (wrong) -> `"Every federal contract-action code category"`
- Funnel box 2 descriptor: `"Services-only codes (R, J, M, N families)"` (R is wrong, missing K/H/L) -> `"Services-only codes (J, K, N, H, L, M families); products excluded"`
- Detail-column rewrites for all four rows (PSC, Awards vs budget, In scope, Out of scope)
- Source line: `"Source: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast Guard, 68 services PSCs, post-exclusions). Data as of April 2026."`

**Slide 2 (Vessel Mix)**
- Title: `"Surface combatants, amphibious warfare and submarines"` -> `"Surface combatants, amphibs, and submarines"` (Oxford comma, tighter)
- Chart title: `"Vessel Type x Work Segment, FY2025 ($M)"`
- Bullet 1: rewritten for active voice and term-of-art ("availability cycles")
- Bullet 2: public-yard list updated, verb precision ("does not generate FPDS contract records" rather than "does not appear in FPDS")
- `Other` row corrected from $525M / 7.4% to $952M / 13.5% (fix to DECK_SLIDES.md; parallel agent had flagged)

**Slide 3 (MRO Work Segments)**
- Title kept (already good)
- Coverage column rewritten row-by-row:
  - Depot: dropped the DSRA/SRA/CMAV/DPIA/PIA/CIA acronym list, kept the RMC + MAC-MO framing
  - HM&E: added pumps, piping, ship structural systems
  - Combat Systems: surfaced Trident II sustainment (~55% of segment)
  - Electronics/C4ISR: added radar and sonar (core J058 content)
  - Port & Technical: removed the misplaced Epsilon reference (Epsilon is Depot, not Port & Technical); added QC/testing/inspection (8 PSCs, the largest sub-family in this segment)
- MSRA callout rewritten with arrow notation: `"MSRA pre-qualification -> MAC-MO IDIQ -> fixed-price task orders against third-party planner specs. Entry requires qualification at all three levels."` Moved exclusively to Slide 3 (was duplicated on Slide 2 and Slide 4)
- Added nuclear footnote: `"Nuclear Propulsion Sustainment PSCs (J044/K044/N044) appear at ~$0 because reactor work is contracted under ship-level shipbuilding codes at HII Newport News, Fluor Marine, and Bechtel - not standalone services PSCs."`
- Bottom-of-column label: `"Total FY2025 MRO TAM"` -> `"Total FY2025 MRO Spend"` (drops TAM jargon; parallels deck voice)

**Slide 4 (Prime Landscape)**
- Title edit proposed: `"held ~36% of vessel MRO spend in FY2025"` -> `"capture ~36% of FY2025 MRO spend"` (active voice; "vessel" redundant; FY2025 prefixing parallels Slides 1/2)
- HM&E <-> Combat Systems segment labels were SWAPPED on user's slide; contractor numbers were correct but row labels needed to trade places. Flagged and user fixed.
- `G. PCCI` -> `Global PCCI` on HM&E row (single-letter abbreviation was inconsistent with the rest of the table)
- Chart title: `"Top 10 Contractors by FY2025 MRO Spend ($M)"`
- MSRA callout replaced with HII Mission Tech margin Note: `"Note: HII Mission Technologies posted a ~5.0% OI margin in 2025 ($3.0B revenue / $153M OI). At ~91% service revenue mix, it is the cleanest pure-services proxy in public comps."`
  - User also flagged that this should say "2025" not "FY2025" because HII is on a calendar fiscal year; mixing federal FY and corporate CY in the same deck is confusing
- Footnotes: `(a)(b)(c)` -> `(1)(2)(3)` per user request; verbs standardized to "includes" (was comprises / includes / encompasses)
- Source line adds: `"; SEC 10-K filings (HII, GD, BWXT), FY2025."` (for the margin overlay)
- Optional Slide 4 side bullets drafted (depot is consolidated / sustainment niches are fragmented) in case user wants to mirror Slide 2 layout

### 7. Unified chart title naming convention

Agreed pattern: `"FY2025 MRO Spend by [Dimension] ($M)"`
- Slide 1: `"FY2025 MRO Scope Derivation - PSC Filter Cascade"` (special case - not a $ distribution)
- Slide 2: `"FY2025 MRO Spend by Vessel Type x Work Segment ($M)"`
- Slide 3: `"FY2025 MRO Spend by Work Segment ($M)"`
- Slide 4: `"FY2025 MRO Spend by Contractor - Top 10 ($M)"`

Format rules: FY2025 always leads; units always in parentheses at the end; "by" is the $-distribution connector; em dash introduces sub-detail.

---

## Files created

| File | Purpose |
|---|---|
| `DECK_SLIDES.md` | 4-slide spec with content blocks, callouts, takeaways, source lines, and optional side bullets |
| `WHY_PSC_DATA.md` | Consolidated argument for PSC-coded contract data vs budget exhibits; 5-part structure |
| `SESSION_2026-04-17_iv_deck_design_and_sheet_polish.md` | This file |
| `output/Services_Sheet_Only_v2.55.xlsx` | Standalone Services sheet: values + formatting preserved, formulas + cross-sheet refs stripped |

## Files modified

| File | Change |
|---|---|
| `styles.py` | `PCT_FMT` '0.0%' -> '0%'; added `F_SUBSEC_I` (italic bold white for designer-facing titles), `F_SLIDE_NOTE` (italic dark-gold), `BG_YELLOW` (pale yellow designer fill) |
| `sheets/services.py` | Added `titlecase_contractor()`, `_write_tam_headline()`, `_write_margin_overlay()`, `_designer_subsec()`, `_slide_tag()`, `_shade_body()`; `include_concentration` and `slide_tag` kwargs on `_write_top_contractors` / `_write_segment_contractors` / `_write_segment_definitions`; title-case applied at display column of both contractor tables; wired slide tags to designer-facing calls in `create_mro` |
| `sheets/product_procurement.py` | `_write_condensed` accepts `slide_tag` kwarg; when set, uses italic bold white title and applies yellow body fill at block end. Default None preserves Product Procurement sheet behavior unchanged |

## Workbook artifacts

| File | State |
|---|---|
| `output/archive/08APR2028_Newbuild_and_MRO_Spend_v2.53.xlsx` | Archived (end of session III) |
| `output/archive/08APR2028_Newbuild_and_MRO_Spend_v2.54.xlsx` | Archived (TAM headline + concentration block) |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.55.xlsx` | **Current.** Adds title-cased names, rounded %, margin overlay, designer slide tags + yellow shading |
| `output/Services_Sheet_Only_v2.55.xlsx` | Standalone Services sheet (no formulas, values only via LibreOffice evaluation) |

---

## Outcomes

|  | v2.53 start | v2.55 end |
|---|---|---|
| PCT_FMT display | 0.0% | **0%** (no decimals) |
| TAM headline block at top of Services | no | **yes** (Navy/CG/Total + 6-segment rollup, live SUMIFS) |
| Market Concentration callout (Top 3/10/15 cumulative %) | no | **yes** (adjacent to Consolidated Top 15) |
| Public Comp margin overlay on Services sheet | no | **yes** (HII/GD/BWXT consolidated + sub-segments) |
| Contractor names | ALL CAPS FPDS | **Title Case display** (SUMIFS criterion still case-insensitive-safe) |
| Designer-facing tables marked | no | **7 tables** (italic "-- Slide N" title + pale yellow body) |
| Standalone Services file | no | **Services_Sheet_Only_v2.55.xlsx** |
| Deck spec documentation | implicit in DECK_WIREFRAMES.md | **DECK_SLIDES.md** (finalized) |
| PSC vs budget argument | spread across 3 files | **consolidated in WHY_PSC_DATA.md** |

---

## Key decisions

1. **PSC-coded contract data is primary; budget data is optional validation.** Rationale consolidated in WHY_PSC_DATA.md. v1.x mistake was treating them as peers.
2. **Percentages round globally to 0%.** Services-focused deck wants no-decimal display for consistency across tables; the workbook's other sheets also benefit from the cleaner rendering.
3. **Slide 1 anchor visual is the PSC funnel**, not the taxonomy tree. User preferred showing scope derivation as positive selection from the PSC universe (2,539 -> 68) over the Product/Services split diagram.
4. **Slide 4 HM&E and Combat Systems segment labels were mis-swapped on user's slide.** Draper/Lockheed/Leidos belong to Combat Systems; Global PCCI/Oceaneering/HII belong to HM&E. Percentages were correct; only the row labels needed fixing.
5. **Margin overlay values are hard-coded from 10-Ks**, not cross-sheet formulas. Overlay is labeled "See Public Comps sheet for full time series" for the audit trail. Reduces formula complexity and standalone-file conversion friction.
6. **Standalone file generated via LibreOffice headless.** openpyxl cannot evaluate formulas on its own. LibreOffice headless conversion populates cached values; openpyxl then copies cell-by-cell to a new single-sheet workbook with formulas stripped.
7. **Only 7 tables are designer-shaded.** Navy-only / CG-only hull-program tables and Ultimate Parent (as-reported) contractor tables are explicitly left unshaded. User wants the designer to work from the Consolidated view + combined-vessel-type rollup only.
8. **Slide 4 margin callout uses "2025" not "FY2025"** because HII is on calendar-year fiscal. Federal FY2025 drives the rest of the deck; mixing the two in the same slide is confusing.
9. **MSRA/MAC-MO three-tier callout lives on Slide 3 only.** Was previously duplicated on Slides 2 and 4; Slide 3 is where depot-as-68% is the headline, so the callout is most relevant there.
10. **Nuclear Propulsion segment explicitly disclosed as methodology artifact** on Slide 3 footnote. Reactor work is bundled under shipbuilding PSCs (not services PSCs) so J044/K044/N044 show ~$0.

---

## Potential next steps

### Deck finalization
1. **Slide 4 title** - user's current slide still says `"held ~36% of vessel MRO spend in FY2025"`; recommended edit to `"capture ~36% of FY2025 MRO spend"` not yet applied
2. **Slide 4 G. PCCI -> Global PCCI** - single-letter abbreviation still on user's slide
3. **Slide 2 Oxford comma** - `"(Portsmouth, Norfolk, Puget Sound, Pearl Harbor)"` in bullet 2 missing the serial comma before "Pearl Harbor" (Slide 1 has it correctly)
4. **Optional Slide 4 side bullets** - currently Slide 4 has a chart + table + callout but no bullets, unlike Slide 2. Two drafts available (Depot consolidation, sustainment fragmentation) if the user wants to mirror Slide 2's layout.

### Documentation alignment
5. **Align DECK_SLIDES.md percentages with deck rendering** - spec still has some one-decimal percentages (e.g., "30.0%") while the deck now uses integer percentages. Not load-bearing but worth a cleanup pass.
6. **Add a WHY_PSC_DATA.md pointer from `methodology.md`** - the consolidated doc doesn't yet have a back-reference from the source files.

### Workbook
7. **Product Procurement sheet designer polish** - same designer slide tags + yellow shading could mirror what was done on Services. `_write_condensed` already accepts `slide_tag`, so the remaining work is in the Product Procurement sheet builder.
8. **Concentration block percentages** - the Market Concentration block currently reads Top 3 / Top 10 / Top 15 at fixed offsets (2, 9, 14 rows from first_data). Works only when `top_n=15`. If `top_n` changes, the offsets need to adapt or the block should receive `top_n` as a parameter.

### Not recommended
- **A fifth slide for public-yard gap + forward-looking budget** - currently the public-yard caveat lives on Slide 2 (submarine understatement bullet) and Slide 1 (Out-of-scope row). Forward-looking authority is out of scope for this deck (bottom-up FY2025 actuals only). Adding a fifth slide would dilute the 4-slide focus.
- **Cross-sheet formulas in the margin overlay** - deliberately avoided; hard-coded values are simpler and survive the standalone-file extraction without degradation.
