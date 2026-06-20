# Workbook Coverage Audit — TARGET Deck Structure vs `08APR2028_MRO_Spend_v4.5.xlsx`

_Audit of whether `build_script_slim/output/08APR2028_MRO_Spend_v4.5.xlsx` (Output sheet) contains the chart source tables required by the target deck outlined in `TARGET_deck_structure.md`. Only slides described as having a chart are in scope. Slides that are text-only, dividers, or reference tables (e.g., Definitions ladder, Contract Vehicles & Qualifications table) are omitted._

## Headline

Partial coverage. The Output sheet has chart-ready tables for **9 of the 15 chart-bearing target slides**. Six target slides have no pre-built block, and two existing blocks are structured for a different chart type than the target specifies. The Output sheet still uses the legacy slide numbering / naming (e.g. "SLIDE 11 – Depot Ship Repair Structure" rather than target S13 "Depot Spend Structure").

## Mapping table — target slide ↔ Output block

| Target slide (new #, name) | Output block (old # / name, rows) | Status |
|---|---|---|
| S4 Definitions | — (ladder diagram, no chart) | n/a |
| **S5 TAM Sizing Approach** | SLIDE 4 – TAM Sizing Approach (r19–33) | Present |
| **S6 Vessel Taxonomy** — SECNAV hierarchy | — nothing in workbook | **Missing** |
| **S7 Fleet Reference** — 6-panel (hull counts, $, %) | — no rollup; per-hull PSC data exists on Services r74–141 but is not summarized | **Missing** |
| **S8 MRO Work Segments** — 100% stacked column | SLIDE 7 – MRO Work Segments (r35–45) | Present |
| **S9 TAM Composition** — Marimekko (vessel × work seg) | SLIDE 6 – TAM Composition (r49–58); 6 vessel columns match the target 6-bucket vocabulary | Present |
| **S11 Marauder-Like Fleet MRO** — Mekko (hull class × work seg) for comp set | — no Marauder-filtered block; underlying per-hull PSC cross-tab exists on Services r74–141 (T-AKE, T-AO, T-AOE, T-EPF, T-AKR/LMSR, auxiliaries) but isn't rolled up to a Marauder subset | **Missing** |
| **S12 SAM Sizing** — narrowing diagram (BRAND NEW) | — no block (matches `.md` flag that this is net-new) | **Missing** |
| **S13 Depot Spend Structure** — Mekko (IDV scope × contractor segment) | SLIDE 11 – Depot Ship Repair Structure (r105–129); includes both full-label reference and short-label paste-ready collapsed block | Present |
| **S14 Depot Geographic Footprint** — Mekko (RMC × contractor segment) | SLIDE 12 – Depot Geographic Footprint (r133–158); 7 RMC columns match | Present |
| S15 Contract Vehicles & Qualifications | — (reference table, no chart) | n/a |
| **S17 Prime Landscape — TAM** — stacked column + by-ship-class lower band | SLIDE 15 – Prime Landscape – Total MRO (r162–181) covers the top-10 × work-segment view; **by-ship-class lower band is missing** (matches `.md` flag) | **Partial** |
| **S18 Prime Landscape — Depot Segment** — ranked column + prime × RMC crosstab | SLIDE 16 – Prime Landscape – Depot (r185–220); both blocks present | Present |
| **S20 HII MT Financials** — combo chart (3 yrs revenue columns + OI margin line) + peer-margin context | FY25-only anchors on Services r340–351 and Reconciliation r9–11; **no FY23 / FY24 revenue or OI, and no combo-chart block** | **Missing** |
| **S22 Scope Reconciliation** — 2×2 matrix (FPDS-visible × MRO scope) | SLIDE 20 – Scope Reconciliation (r224–254) — data is there, but shaped as a **waterfall** (bar-type codes `s`/`d`/`d`/`d`/`e` on r230), not a 2×2 grid | **Mismatched** |
| **S23 Appropriation Sourcing** (moved to Appendix) — funding waterfall + OPN BA breakdown | SLIDE 10 – Appropriation Sourcing (r62–101) — built as **dual 100%-stacked columns**, not a waterfall | **Mismatched** |

## Missing-block details

### 1. S6 Vessel Taxonomy (SECNAV hierarchy)
No block anywhere in the workbook. Target calls for a "compact SECNAV hierarchy table with color-coding or shading that ties each SECNAV leaf to the downstream 6-bucket grouping." The 6-bucket vocabulary (Surface Combatants / Amphibious / Submarines / Combat Logistics / Aircraft Carriers / Other) is used as column headers on Output r53 and Services r385/r398, but the SECNAV-to-6-bucket mapping itself is not tabulated. `.md` also flags that the placeholder percentage row on the current slide needs real data — that row isn't in the workbook either.

### 2. S7 Fleet Reference (6-panel grid)
No summary block. Target needs, per each of the 6 vessel buckets: dominant hull class, hull counts, FY25 $M of category MRO, % share of category MRO, and a short list of rolled-up classes. The raw ingredients are on Services r74–141 (Navy by Hull Program, 28 hull-class columns) but nothing rolls them up into the 6-panel shape.

### 3. S11 Marauder-Like Fleet MRO
No Marauder-subset rollup. Target needs MRO spend on the Marauder comp-set (T-AKE, T-AO, T-AOE, LMSR/T-AKR, USNS Cape, T-EPF, auxiliaries) across the 5 work segments — a Mekko of hull class × work segment for this subset. All the component hull classes do appear as columns in the Services hull-program cross-tab, so the block is derivable, but no pre-built Marauder-filtered table exists in Output or anywhere else.

### 4. S12 SAM Sizing
Brand-new slide per the `.md`; no block in the workbook. Needs the arithmetic breakdown TAM → Depot share → Marauder-like share → SAM. Data pull would intersect the S11 comp-set with the depot repair PSC filter (J998/J999), neither of which has been done in the workbook.

### 5. S17 Prime Landscape — TAM (by-ship-class band)
The top band (top-10 primes × work segment stacked column) is built on Output r162–181 and is solid. What's missing is the lower-band "market share by competitor × ship × MRO category" view the `.md` says was explicitly requested by the boss. No by-ship-class prime breakdown exists anywhere in the workbook.

### 6. S20 HII MT Financials (multi-year combo chart)
Only FY25 data is present anywhere in the workbook:

- Services r347: HII MT FY25 rev $3,044M, OI $153M, margin 5.03%
- Reconciliation r9–11: HII MT FY25 rev $3,044M, OI $153M, service mix 91%
- Services r340–351: FY25 peer margins for HII consolidated, GD consolidated, BWXT, GD Marine Systems, BWXT Gov Ops

The target combo chart needs **three fiscal years** of revenue columns plus an operating-margin line on the secondary axis. FY23 and FY24 revenue/OI do not appear anywhere (keyword search confirmed). The peer-margin context block the target calls out also isn't built in combo-chart-ready form.

## Chart-type mismatches

### S22 Scope Reconciliation — 2×2 vs waterfall
Output r225 labels the chart type as "2x2 matrix (FPDS-visible vs Not FPDS-visible, Ship MRO vs Ship non-MRO)", which matches the `.md`. But the paste-ready block (r228–230) is shaped as a think-cell waterfall: 6 columns (Total Navy+USCG ship spend → less Newbuild PSC 1905 → less implied public-yard labor → less reactor proc PSC 4470 → FY25 MRO contracting TAM), with bar-type codes `s d d d e` on r230. Either the `.md` description needs to be updated to "waterfall" or the block needs to be re-shaped into an actual 2×2.

### S23 Appropriation Sourcing — waterfall vs dual stacked columns
Target `.md`: "funding waterfall plus OPN Budget Activity breakdown chart plus supporting callouts." Output SLIDE 10 is explicitly "Chart type: 100%-stacked columns – 2 columns side-by-side" with 7 appropriation series on column 1 and 3 OPN BA series on column 2. The underlying appropriation $M values are present (and per-appropriation rebase-to-TAM logic is wired), but there's no waterfall-shaped block.

## Parity notes (no issue, just worth confirming)

- **6-bucket vessel vocabulary** on S9 TAM Composition Mekko matches across Output r53 and Services r385/r398 (Surface Combatants, Amphibious Warfare Ships, Submarines, Combat Logistics Ships, Aircraft Carriers, Other). Consistent with the `.md`'s new rule that S6 Vessel Taxonomy establishes this vocabulary before any downstream slide uses it.
- **RMC column set** on S14 Depot Geographic Footprint matches the `.md` 7-column list (SWRMC, MARMC, SERMC, NW RMC, FDNF, USCG SFLC, Other) exactly on Output r136.
- **Contractor-segment rows** on S13 / S14 Mekkos use the same 5-row stack (CONUS full-ship primes, Regional yards, Technical services, Foreign MSRA yards, Other) on both Output r116–120 and r137–141.
- **Depot headline block** on Output r107–111 (Gross J998+J999 → less FMS → In-Scope Depot TAM) is present and consistent with the target's depot-segment denominator story.

## Stale content (safe to ignore)

- **Output SLIDE 21 – TAM Framing** (r258–276) still has its source tables (5-method $M table + per-segment Frame A vs Frame B M1 table). Target cuts this slide entirely. Not used.
- **Output Table of Contents** (r5–16) lists the old 10-slide chart index with old numbering and old names (e.g., "Depot Ship Repair Structure" rather than "Depot Spend Structure", "Prime Landscape – Total MRO" rather than "Prime Landscape — TAM"). Informational only.

## Net workload to close the gap

New blocks needed:

1. **S6 Vessel Taxonomy** — SECNAV hierarchy table + 6-bucket mapping
2. **S7 Fleet Reference** — 6-panel rollup (dominant hull, hull count, $M, % of category MRO, other-classes list)
3. **S11 Marauder-Like Fleet MRO** — Marauder comp-set × work-segment Mekko
4. **S12 SAM Sizing** — TAM → Depot → Marauder-like → SAM arithmetic / narrowing block
5. **S17 Prime Landscape — TAM** lower band — competitor × ship-class × MRO-segment breakdown
6. **S20 HII MT Financials** — add FY23 + FY24 revenue and OI (segment-level, from 10-Ks), then build the 3-year combo-chart source block + peer-margin context block

Reshape / clarify:

7. **S22 Scope Reconciliation** — decide whether the visual is a 2×2 matrix or a waterfall, and either rebuild the block or update the target `.md` description
8. **S23 Appropriation Sourcing** — decide whether to re-shape the existing dual 100%-stacked-column block into a funding waterfall, or update the target `.md` description to match what's built
