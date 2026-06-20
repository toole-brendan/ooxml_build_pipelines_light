# Session 2026-04-17 (II): Services MRO Segmentation + Raw $M + % Views + SAM Split

## Context

Building on `SESSION_2026-04-17.md` (v2.48 workbook, 44 -> 68 PSCs, Services residual at 2.3%).

Two issues surfaced this session:

1. The 8-group condensed rollup on Services used the PSC letter axis (J0xx/K0xx/N0xx...) with labels that meant nothing to a non-technical deck audience. The J0xx bucket alone blended 27 PSCs spanning weapons, nuclear, HM&E, C4ISR, and miscellaneous industrial work - segments an investor or exec would want to see separately.
2. The Services sheet needed a restructured layout for the deck: a raw $M view and a percent-of-column-total view, with the SAM content moved off the main sheet.

Ended at **v2.51 workbook** with the restructured Services sheet and a separate Services SAM (Temporary) tab.

---

## Work completed, in order

### 1. Evaluation of the existing condensed grouping

Starting grouping (8 rows, organized by PSC-letter = activity type):
- J998/J999 Ship Repair
- J0xx Equipment Maint & Repair (27 PSCs)
- K0xx Modification
- N0xx Installation
- H QC/Test/Inspection
- L Technical Representation
- M1 Shipyard Operations
- M2xx Husbanding

Diagnosis:
- J0xx alone is ~40% of the PSC count and blends fundamentally different market segments: weapons sustainment (J010/J012/J013/J014/J017), nuclear (J044), C4ISR (J058/J059/J061/J063/J066), HM&E (propulsion, pumps, valves, HVAC, ship equipment), and misc industrial.
- Labels like "J0xx Equipment Maint & Repair" are PSC-taxonomy jargon, not investor vocabulary.
- The activity axis (maint vs mod vs install) is irrelevant to a non-technical audience, which thinks in "which part of the ship is being serviced."
- Weapons sustainment and Nuclear are the investment theses the existing methodology docs already call out; the old grouping hid them inside a generic bucket.

Recommended a 6-segment MRO functional-segment grouping using standard industry vocabulary (NAVSEA / shipbuilder / sustainment analyst terminology):

- Depot Ship Repair
- Combat Systems Sustainment
- Nuclear Propulsion Sustainment
- Hull, Mechanical & Electrical (HM&E)
- Electronics & C4ISR Sustainment
- Port & Technical Services

User approved.

### 2. New segmentation + reference table (v2.48 -> v2.50)

**Replaced** `SERVICE_CONDENSED_GROUPS` in `sheets/services.py` with 6 explicit PSC lists (no more glob wildcards). Coverage verified programmatically: 68 PSCs total, each appearing exactly once across segments.

| Segment | # PSCs | PSCs |
|---|---:|---|
| Depot Ship Repair | 2 | J998, J999 |
| Combat Systems Sustainment | 11 | J010, J012, J013, J014, J017, K010, K012, K014, N010, N012, N014 |
| Nuclear Propulsion Sustainment | 3 | J044, K044, N044 |
| Hull, Mechanical & Electrical (HM&E) | 24 | J019/J020/J029/J030/J035/J036/J039/J041/J043/J047/J048/J049/J052/J056/J091/J099 + K019/K020/K034/K099 + N019/N020/N025/N056 |
| Electronics & C4ISR Sustainment | 7 | J058, J059, J061, J063, J066, K058, K059 |
| Port & Technical Services | 21 | H119-H920 (8) + L019, L020 + M1ED + M2AA-M2CA (10) |

**Added** `MRO_SEGMENT_DESCRIPTIONS` dict mapping each segment to a one-line plain-English description (e.g., "Weapons, fire control, guided missiles, VLS, aircraft launching/landing -- includes Trident II sustainment carried by SSBNs").

**Added** `_write_segment_definitions(ws, r, mc)` helper that writes a reference table on the Services sheet with columns: `# PSCs | MRO Segment | PSC Codes | What It Covers`. PSC list and description columns are merged across multiple Excel columns with wrap_text for readability.

**Wired** into `create_mro` between the CG Hull Program crosstab and the Condensed TAM sections.

v2.49 shipped with 40pt forced row heights on the definitions table; content fit on one line so rows were over-tall. **v2.50 removed** the row-height override so the definitions rows match the surrounding tables.

**Formula length sanity check**: the HM&E bucket's 24-PSC SUMIFS formula in a hull-program cell is ~3,300 chars, well under Excel's 8,192 limit.

### 3. Services sheet restructure (v2.50 -> v2.51)

New layout per user spec:

```
Row 1  : Title band
Row 2  : Purpose
Row 4+ : Vessel Type crosstab (combined Navy + CG, $)
         Navy Hull Program crosstab ($)
         Coast Guard Hull Program crosstab ($)

         [Blank divider band - black, no text]

         MRO Segment Definitions reference table

         [Blank divider band]

         U.S. Navy + Coast Guard condensed (Vessel Type cols) [$M raw]
         U.S. Navy condensed (Hull Program cols) [$M raw]
         U.S. Coast Guard condensed (Hull Program cols) [$M raw]

         [Blank divider band]

         U.S. Navy + Coast Guard condensed (Vessel Type cols) [% of col total]
         U.S. Navy condensed (Hull Program cols) [% of col total]
         U.S. Coast Guard condensed (Hull Program cols) [% of col total]
```

Percent tables: cells = source_cell / source_column_total, formatted as %. Each table's bottom Total row references the source table's total row directly, formatted as $M (raw dollars shown in millions).

The right-most "Total" column in the percent tables shows row_total / grand_total (not cell-sum, which would be meaningless across different column totals).

### 4. SAM moved to "Services SAM (Temporary)" sheet

All SAM content split from the Services sheet to a new tab. SAM cells reference TAM cells on the Services sheet cross-sheet (e.g. `=Services!F17*SAM_OPS_MULT`). Overview still reads `NAVY_SAM_SVC` / `CG_SAM_SVC` defined names unchanged -- defined names are workbook-wide so cross-sheet moves are transparent to consumers.

Tab color gray (`9E9E9E`) to flag as temporary.

### 5. Shared helpers

**`NUM_FMT_M`** added to `styles.py` -- format string `'#,##0,,;[Red](#,##0,,);"-"'`. Uses Excel trailing-comma scaling to display the underlying dollars divided by millions. Critical: the underlying cell VALUE stays in raw dollars, so `NAVY_TAM_SVC` and related named ranges still read correctly in Overview via NUM_FMT.

**`_write_condensed`** in `sheets/product_procurement.py` extended with three new parameters:

- `value_format` in `{'dollars', 'millions', 'percent'}`.
  - `'dollars'` (default): existing NUM_FMT behavior on cells and totals.
  - `'millions'`: NUM_FMT_M on cells and totals.
  - `'percent'`: PCT_FMT on cells, NUM_FMT_M on the bottom total row; cells compute `=IFERROR(source_cell/source_total,0)`.
- `tam_total_row` -- source table's total-row row number. Required for `'percent'` mode.
- `tam_sheet` -- source TAM sheet name. When provided and different from the current sheet, cross-sheet references are emitted (used by the SAM tables on the new temp sheet).

Existing SAM-mode behavior preserved; no breaking changes to callers. Product Procurement continues unchanged.

---

## Files created

| File | Purpose |
|---|---|
| `SESSION_2026-04-17_ii_services_restructure.md` | This file |

## Files modified

| File | Change |
|---|---|
| `styles.py` | Added `NUM_FMT_M` (displays $ in millions via trailing-comma scaling) |
| `sheets/services.py` | Replaced `SERVICE_CONDENSED_GROUPS` with 6 MRO functional segments (explicit PSC lists); added `MRO_SEGMENT_DESCRIPTIONS`; added `_write_segment_definitions()` helper; restructured `create_mro()` with 3 sections separated by blank divider bands (crosstabs -> $M condensed -> % condensed); `create_mro()` now returns a context dict for the temp SAM sheet; added `create_services_sam_temp(wb, ctx)` |
| `sheets/product_procurement.py` | Extended `_write_condensed` with `value_format`, `tam_total_row`, `tam_sheet` params; three rendering modes (raw $, $M, percent-of-column-total); cross-sheet TAM references |
| `build_from_data.py` | Imports and calls `create_services_sam_temp(wb, ctx)` after `create_mro(wb)`; added gray tab color for temp sheet |

## Workbook artifacts

| File | State |
|---|---|
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.48.xlsx` | Archived (end of first 04-17 session) |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.49.xlsx` | Archived - first pass with 6-segment rollup + definitions table (row heights wrong) |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.50.xlsx` | Archived - row heights fixed |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.51.xlsx` | **Current.** Restructured Services sheet with $M + % views; SAM moved to Services SAM (Temporary) |

---

## Outcomes

|  | v2.48 start | v2.51 end |
|---|---|---|
| Services condensed rollup rows | 8 (activity axis) | **6 (MRO functional segments)** |
| Segment grouping axis | PSC letter (J/K/N/H/L/M) | **Ship system / market segment** |
| MRO Segment Definitions reference table | no | **yes** |
| Services condensed tables (raw) | yes ($ format) | **yes ($M format)** |
| Services condensed tables (% of col total) | no | **yes (new)** |
| SAM tables location | Services sheet | **Services SAM (Temporary)** |
| Cross-sheet TAM references in SAM | n/a | yes (`=Services!F17*SAM_OPS_MULT`) |
| `NAVY_TAM_SVC` / `CG_TAM_SVC` defined names | Services sheet | Services sheet (unchanged) |
| `NAVY_SAM_SVC` / `CG_SAM_SVC` defined names | Services sheet | Services SAM (Temporary) sheet |
| Sheet count in workbook | 9 | 10 |

Key methodology decisions:

1. **Condensed rollup axis is market segment, not PSC activity.** Labels are zero-jargon (except "HM&E" which is industry-standard). Matches how NAVSEA, shipbuilders, and sustainment analysts segment the MRO market - so the slide reads the way a defense-focused audience already thinks.

2. **Display in $M via number format, not formula division.** Underlying cell values stay in raw dollars, so downstream named-range consumers (Overview) read true dollars with NUM_FMT unchanged. Only the display format differs.

3. **Percent tables derive from the $M tables.** Cells are `=source_cell / source_total_cell`; total row directly references the source total row. No duplicated SUMIFS, and the two tables are mathematically locked to each other - if the $M number moves, the % number moves in lockstep.

4. **SAM sheet is a sibling, not a child.** Defined names are workbook-wide, so moving SAM off Services doesn't break Overview references. Cross-sheet formulas handle TAM cell references transparently.

---

## Potential next steps

### Services sheet polish

1. **Differentiate subsec labels on percent tables** - right now the $M and % tables both use "U.S. Navy + Coast Guard" / "U.S. Navy" / "U.S. Coast Guard" subsec bands. The blank divider provides context but repeated labels can confuse. Consider appending " (% of column total)" to the percent-table subsec bands.

2. **Format polish on percent cells** - currently `PCT_FMT` is `0.0%`. Consider `0%` (no decimals) if the deck looks cleaner without them.

3. **Segment definitions table layout** - the 4-column layout (`# PSCs | MRO Segment | PSC Codes | What It Covers`) works but can be adjusted (e.g., wider "What It Covers" column, or merging PSC Codes across more columns).

### SAM temporary sheet

4. **Decide fate of Services SAM (Temporary)** - the name flags it as pending. Options: keep as audit-only; fold TAM+SAM into Product Procurement-style tables; or remove entirely if SAM is no longer in scope for the deck.

### Product Procurement parity

5. **Mirror the $M + % treatment on Product Procurement.** Current PP layout still has condensed in raw $. The extended `_write_condensed` already supports both formats, so implementation is a handful of lines plus a blank-divider layout pass.

### Segment mapping iteration

6. **Revisit segment boundaries on request** - a few PSCs have judgment-call placements: J063 (alarm/signal) goes Electronics vs HM&E; J052 (measuring tools) goes HM&E vs shop; N025 (vehicular equipment install) goes HM&E vs separate. Easy to shift if user preference differs; mapping is a single dict/list edit.

### Not recommended

- **Computing percent via SUMIFS/SUMIFS rather than cell references** - would duplicate formula logic and risk the $M and % tables diverging if a third party edits one. Cell-reference approach locks them together.
- **Inlining MRO segment descriptions into the SERVICE_CONDENSED_GROUPS tuples** - separate dict is cleaner and lets the reference table render independently of the rollup order.
- **Computing $M in formulas via /1000000** - the trailing-comma format approach preserves the underlying value for downstream consumers. Formula-based scaling would break `NAVY_TAM_SVC` defined-name reads in Overview without coordinated format changes there.
