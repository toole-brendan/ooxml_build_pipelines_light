# Session 2026-04-17 (III): Top Contractors Tables on Services Sheet

## Context

Building on `SESSION_2026-04-17_ii_services_restructure.md` (v2.51 workbook, Services restructured with 6 MRO functional segments + $M and % views + SAM on a separate tab).

Goal: add a slide-ready "top contractors" view to the Services sheet so the user can show % breakdown of the leading primes for a deck. Two tables requested - a global Top 15 and a Top 3 per MRO segment. After reviewing the raw FPDS parent data, added a second pair of tables using a consolidated corporate-parent rollup (BAE subsidiaries, HII subsidiaries, GD subsidiaries) so the deck can show either the FPDS-as-reported or the true-corporate-parent view.

Ended at **v2.52 workbook** with four new tables on the Services sheet.

---

## Work completed, in order

### 1. Data inspection

Loaded the exploded services rows (Navy + Coast Guard v2 JSONs, after shore/base exclusions) and confirmed:

- 8,693 rows, $7.07B Services TAM - matches the Vessel Type crosstab at the top of the sheet.
- 100% of rows have `ultimate_parent_name` populated (no fallback path needed).
- Ranked list of parents with > $20M showed 57 entries with clean concentration at the top.

### 2. First pair of tables - Ultimate Parent (FPDS as reported)

Added two tables between the MRO Segment Definitions reference table and the $M condensed rollups:

**Table 1 - Top 15 Contractors by FY2025 Obligation:**

| Col | Content |
|---|---|
| Rank | 1 through 15 |
| Ultimate Parent | raw FPDS name |
| FY2025 $M | `=SUMIFS(AwardsByHull[FY2025 Obligation], AwardsByHull[Ultimate Parent], "<parent>")` |
| % of Services TAM | cell $ / `SUM(AwardsByHull[FY2025 Obligation])` |
| Cumulative % | running sum of the % column |

Followed by a Top 15 Subtotal row, an All Other Contractors row, and a Services TAM total row.

**Table 2 - Top 3 Contractors per MRO Segment:**

Each segment gets a `subsubsec_band` header, followed by three rows with:

| Col | Content |
|---|---|
| Rank | 1-3 |
| Ultimate Parent | raw FPDS name |
| FY2025 $M | sum across segment PSCs of `SUMIFS(PSC=<psc>, Parent=<parent>)` |
| % of Segment | cell $ / inline sum of segment-total SUMIFS |
| % of Services TAM | cell $ / `SUM(AwardsByHull[FY2025 Obligation])` |

The Nuclear Propulsion Sustainment segment is auto-skipped (top-1 parent below a $1M threshold) because direct J044/K044/N044 spend is ~$0 - reactor work bundles under ship-level PSCs per `METHODOLOGY_CVN_SSN_COVERAGE.md`.

### 3. Observation that prompted the consolidated view

FPDS reports `ultimate_parent_name` at the immediate-parent level, so a single corporate parent can appear as multiple rows:

- **BAE Systems plc**: BAE SD ($673M) + BAE Norfolk ($257M) + BAE Jacksonville ($114M) + BAE Land & Armaments ($29M) + BAE Space & Mission Systems ($0.3M) = $1.07B
- **Huntington Ingalls Industries**: HII (3 variants) + Metro Machine + Marine Hydraulics Intl = $516M
- **General Dynamics**: GD Corp + Continental Maritime + GD Mission Systems + Electric Boat + GDIT = $939M

The FPDS-as-reported Top 15 shows BAE as 3 separate rows (SD / Norfolk / Jacksonville), HII as 3 separate subsidiaries, and GD partially rolled up - a reader can't see the real corporate concentration at a glance. Flagged this to user; user asked for a second pair of tables with a consolidated corporate-parent view.

### 4. Corporate parent rollup

Added `CORPORATE_PARENT_ROLLUP` dict in `sheets/services.py` mapping 16 raw FPDS names to 3 consolidated labels ('BAE Systems', 'Huntington Ingalls Industries', 'General Dynamics'). Exposed `consolidate_parent(raw_name)` that returns the consolidated label or the raw name if no rollup applies.

Rollup was built from direct data inspection (not model memory) - all entities present in the Services data with BAE / HUNTINGTON / INGALL / METRO MACH / MARINE HYDRAUL / GENERAL DYNAM / CONTINENTAL MARITIME / ELECTRIC BOAT substrings were listed and manually assigned.

Names not in the rollup pass through unchanged - Vigor Marine, Draper Lab, Detyens, Lockheed, Austal, Fincantieri etc. stay as-is.

### 5. New "Corporate Parent" column on AwardsByHull

To keep the consolidated SUMIFS formulas short and consistent with the rest of the sheet, added a `Corporate Parent` column to the `AwardsByHull` Excel table (column 5 in the sheet, right after `Ultimate Parent`). Populated per row in `awards_by_hull.load_exploded_rows()` via `consolidate_parent()`.

With the column in place, the consolidated Top 15 uses a simple:

```
=SUMIFS(AwardsByHull[FY2025 Obligation], AwardsByHull[Corporate Parent], "BAE Systems")
```

instead of OR-logic summing multiple SUMIFS per subsidiary (which would have hit Excel's 8,192-char formula limit for the HM&E segment's 24 PSCs).

### 6. Parametrized the writers

Refactored `_write_top_contractors` and `_write_segment_contractors` to accept `column_name`, `label_variant`, and `consolidated` kwargs so both views share one code path. Defaults preserve the existing FPDS-as-reported behavior; consolidated view passes `column_name='Corporate Parent'`, `label_variant='Consolidated Corporate Parent'`, `consolidated=True`.

Section titles now read:
- "Top 15 Contractors by FY2025 Obligation - Ultimate Parent (FPDS as Reported)"
- "Top 3 Contractors per MRO Segment - Ultimate Parent (FPDS as Reported)"
- "Top 15 Contractors by FY2025 Obligation - Consolidated Corporate Parent"
- "Top 3 Contractors per MRO Segment - Consolidated Corporate Parent"

### 7. Placement in `create_mro()`

Inserted the 4 tables between the MRO Segment Definitions reference table and the $M Condensed TAM sections, separated by blank title bands (matching the existing divider pattern on the sheet):

```
Segment Definitions
[blank divider]
Top 15 - Ultimate Parent (FPDS as Reported)
[blank divider]
Top 3 per Segment - Ultimate Parent (FPDS as Reported)
[blank divider]
Top 15 - Consolidated Corporate Parent              [new]
[blank divider]
Top 3 per Segment - Consolidated Corporate Parent   [new]
[blank divider]
$M Condensed tables (combined VT, Navy, CG)
[blank divider]
% Condensed tables (combined VT, Navy, CG)
```

### 8. Workbook rebuild v2.51 -> v2.52

Ran `python3 -m domnann.build_from_data`. Services sheet now 405 rows; AwardsByHull is 39 columns (was 38, new `Corporate Parent` column inserted at position 5). All existing tables and named ranges unchanged.

---

## Key numbers (FY2025 Services TAM = $7.07B)

### Top 15 - Ultimate Parent (FPDS as reported)

| Rank | Parent | FY25 $M | % of TAM | Cum % |
|---:|---|---:|---:|---:|
| 1 | General Dynamics Corporation | 691 | 9.8% | 9.8% |
| 2 | BAE Systems San Diego Ship Repair Inc. | 673 | 9.5% | 19.3% |
| 3 | Vigor Marine LLC | 439 | 6.2% | 25.5% |
| 4 | The Charles Stark Draper Laboratory Inc. | 318 | 4.5% | 30.0% |
| 5 | BAE Systems Norfolk Ship Repair Inc. | 257 | 3.6% | 33.7% |
| 6 | Detyens Shipyards Inc. | 226 | 3.2% | 36.8% |
| 7 | Metro Machine Corp | 195 | 2.8% | 39.6% |
| 8 | Marine Hydraulics International LLC | 168 | 2.4% | 42.0% |
| 9 | Continental Maritime of San Diego LLC | 162 | 2.3% | 44.3% |
| 10 | Epsilon Systems Solutions Inc. | 149 | 2.1% | 46.4% |
| 11 | East Coast Repair & Fabrication LLC | 141 | 2.0% | 48.4% |
| 12 | Lockheed Martin Corporation | 132 | 1.9% | 50.3% |
| 13 | BAE Systems Jacksonville Ship Repair LLC | 114 | 1.6% | 51.9% |
| 14 | S.C.A. Shipping Consultants Associated Ltd. | 112 | 1.6% | 53.5% |
| 15 | Pacific Shipyards International LLC | 111 | 1.6% | 55.0% |
| | **Top 15 Subtotal** | **3,890** | **55.0%** | |
| | All Other Contractors | 3,180 | 45.0% | |
| | Services TAM | 7,070 | 100.0% | |

### Top 15 - Consolidated Corporate Parent

| Rank | Corporate Parent | FY25 $M | % of TAM | Cum % |
|---:|---|---:|---:|---:|
| 1 | BAE Systems | 1,073 | 15.2% | 15.2% |
| 2 | General Dynamics | 939 | 13.3% | 28.5% |
| 3 | Huntington Ingalls Industries | 516 | 7.3% | 35.8% |
| 4 | Vigor Marine LLC | 439 | 6.2% | 42.0% |
| 5 | The Charles Stark Draper Laboratory Inc. | 318 | 4.5% | 46.5% |
| 6 | Detyens Shipyards Inc. | 226 | 3.2% | 49.7% |
| 7 | Epsilon Systems Solutions Inc. | 149 | 2.1% | 51.8% |
| 8 | East Coast Repair & Fabrication LLC | 141 | 2.0% | 53.8% |
| 9 | Lockheed Martin Corporation | 132 | 1.9% | 55.7% |
| 10 | S.C.A. Shipping Consultants Associated Ltd. | 112 | 1.6% | 57.3% |
| 11 | Pacific Shipyards International LLC | 111 | 1.6% | 58.8% |
| 12 | Austal USA LLC | 90 | 1.3% | 60.1% |
| 13 | Alabama Shipyard LLC | 88 | 1.2% | 61.4% |
| 14 | Colonna's Ship Yard Incorporated | 86 | 1.2% | 62.6% |
| 15 | Sumitomo Heavy Industries Ltd | 76 | 1.1% | 63.7% |
| | **Top 15 Subtotal** | **4,500** | **63.7%** | |
| | All Other Contractors | 2,570 | 36.3% | |
| | Services TAM | 7,070 | 100.0% | |

Top 3 consolidated = BAE + GD + HII = $2.53B / **35.8% of Services TAM**. This is the concentration story the as-reported view hides.

### Top 3 per MRO Segment (consolidated)

| Segment | #1 | #2 | #3 |
|---|---|---|---|
| Depot Ship Repair ($4.78B) | BAE Systems 21.8% | General Dynamics 17.9% | Huntington Ingalls 9.7% |
| Combat Systems ($585M) | Draper Lab 54.5% | Lockheed Martin 22.4% | Leidos 9.7% |
| HM&E ($938M) | Global PCCI 6.8% | Oceaneering 6.2% | Huntington Ingalls 5.6% |
| Electronics & C4ISR ($333M) | Amentum 15.1% | L3 Technologies 14.9% | SAIC 14.6% |
| Port & Technical Services ($431M) | S.C.A. 25.9% | Waypoint 8.6% | Fairlead Boatworks 6.3% |
| Nuclear Propulsion | (skipped - direct J044/K044/N044 spend is ~$0; reactor work bundles under ship-level PSCs, see `METHODOLOGY_CVN_SSN_COVERAGE.md`) |

---

## Files created

| File | Purpose |
|---|---|
| `SESSION_2026-04-17_iii_top_contractors.md` | This file |

## Files modified

| File | Change |
|---|---|
| `sheets/services.py` | Added `CORPORATE_PARENT_ROLLUP` dict + `consolidate_parent()`; added `_load_services_rows()`, `_parent_totals(consolidated=)`, `_write_top_contractors()` (parametrized), `_write_segment_contractors()` (parametrized); called all four writers from `create_mro()` between Segment Definitions and $M Condensed |
| `sheets/awards_by_hull.py` | Added `corporate_parent` to COLUMNS and populated it per row in `load_exploded_rows()` via `consolidate_parent()` |

## Workbook artifacts

| File | State |
|---|---|
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.51.xlsx` | Archived. Pre-top-contractors. |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.52.xlsx` | **Current.** Services sheet has 4 new contractor tables; AwardsByHull has new Corporate Parent column. |

---

## Outcomes

|  | v2.51 start | v2.52 end |
|---|---|---|
| Services sheet rows | ~353 | **405** |
| AwardsByHull columns | 38 | **39** (+ Corporate Parent) |
| Top-contractor tables on Services | 0 | **4** (2 views x 2 cuts) |
| Top 15 subtotal - as reported | n/a | 55.0% |
| Top 15 subtotal - consolidated | n/a | **63.7%** |
| Top 3 consolidated share of TAM | n/a | **35.8%** (BAE + GD + HII) |

Key design decisions:

1. **Two views are both correct, not a "right vs wrong" choice.** FPDS as-reported is defensible methodology ("as the government catalogs the data"). Consolidated is defensible methodology ("as the capital markets would read it"). The deck can cite either and the audit trail is transparent because both tables sit side by side on the sheet.

2. **Rollup lives in services.py as a dict, not in a config file.** Easy to extend in one place. Unmapped parents pass through as-is, so adding a new rollup rule is a one-line edit; no broader refactor needed.

3. **Corporate Parent column on AwardsByHull, not inline SUMIFS OR-logic.** The HM&E segment has 24 PSCs; combining OR-logic across multiple subsidiaries and multiple PSCs would have produced ~10K-char formulas and hit Excel's 8,192 limit. A single column with the rolled-up label keeps SUMIFS short and fast.

4. **Nuclear Propulsion segment auto-skipped.** Top-1 parent below $1M = segment skipped. Prevents the ugly "88.5% of $0" percentages that would otherwise show. The methodology doc already explains why direct J044 is empty.

---

## Potential next steps

### Rollup extension

1. **Add more corporate parents as they matter for the deck.** Current dict covers the three that dominated the residual in the as-reported view (BAE, HII, GD). Candidates to add if a future slide needs them:
   - L3Harris Technologies - would fold L3 Technologies + any Harris entries. Currently no Harris subsidiaries visible.
   - RTX / Raytheon Technologies - only Raytheon Company visible now; Pratt / Collins don't appear in Services data.
   - Vigor / Titan Acquisition Holdings - would consolidate Vigor Marine + any other Titan ship-repair subs. Not currently multi-subsidiary.
   - Fincantieri - only Fincantieri Marinette Marine and Fincantieri Marine Repair appear; could roll up if either grows.

2. **Formalize the rollup as a data file** (JSON or YAML) if the dict grows past ~50 entries, so the editing experience doesn't require a Python code change. Not needed at current size.

### Layout polish

3. **Expand Services sheet column 2 width to 42** if long parent names (HUNTINGTON INGALLS INDUSTRIES INCORPORATED, S.C.A. SHIPPING CONSULTANTS ASSOCIATED LTD.) spill in the rendered deck. Current width is 38 (inherited from the crosstab headers above).

4. **Add a cumulative % column to the consolidated Top 15** - already there. No change.

5. **Consider ordering the percent-cell formatting** - currently `PCT_FMT = '0.0%;[Red](0.0%);"-"'`. Looks clean; no change needed.

### Audit

6. **Spot-check the consolidated rollup against the J998/J999 research memo** - the doc says "HII consolidated is ~$745M" for J998/J999 alone; our full-services HII number is $516M which is lower because we're only capturing the ship-repair portion visible at the prime level in AwardsByHull (the research brief number includes other HII entities not in the services-PSC pull). Worth a one-pass sanity check before the deck ships.

### Not recommended

- **OR-logic SUMIFS instead of the Corporate Parent column** - would hit Excel's 8,192-char limit on the HM&E segment (24 PSCs x ~5 subsidiaries = 120 SUMIFS per cell).
- **Static hardcoded $ values in the Excel cells** - would decouple the table from AwardsByHull, breaking the audit promise that Services cross-tabs and top-contractor tables come from the same table.
- **Expanding the rollup to every corporate entity in USAspending** - beyond the deck's audience, diminishing returns. Three rollups already cover 35.8% of the TAM.
