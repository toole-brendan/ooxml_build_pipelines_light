# TODOs

## Group 1: Research / Investigation

These need answers before code changes. Several downstream tasks depend on them.

- [x] **R1 - UUV vs. "Unmanned" exclusion** — DECIDED: exclude all unmanned. USV funding ($1.15B FY26 for MUSV) is currently flowing into SAM alongside UUV. 
  - **FIX PLAN:** In `build_from_data.py` line 95, add `'Unmanned Surface Vehicles'` to `SAM_EXCLUDED_TYPES`. Change from `{'Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles'}` to `{'Submarines', 'Aircraft Carriers', 'Unmanned Undersea Vehicles', 'Unmanned Surface Vehicles'}`. This affects all 4 SAM sheets (FY26/FY27 Newbuild/MRO) — bridge rows will show "Less: Unmanned Surface Vehicles" alongside existing "Less: Unmanned Undersea Vehicles". USV rows will still appear in TAM sheets (Unmanned Maritime Platforms remains in `TAM_CATEGORIES`).
- [x] **R2 - RCOH/SLEP dual-bucketing** — RESOLVED. No double-counting. All 193 RCOH/SLEP rows live solely in Bucket 5. Zero in Bucket 1. Newbuild SAM has dead RCOH/SLEP formula rows (always 0%) — harmless, could clean up.
- [ ] **R3 - Data quality issues in Validation sheet** — CRITICAL. OPN_BA3/BA5-8 duplicate issue is still open. Validation sheet says "$1.0-1.3M" impact but actual FY27 double-count is ~$1.037B across 5 line items (LI 176 "Spares" = $766M, LI 122 UMCS = $211M, LI 117 EMALS = $37M, LI 116 AAG = $24M). Surface Combatants variant issue (Issue 1) is confirmed resolved.
  - **FIX PLAN:** For all 5 duplicates, keep OPN_BA3 copy (has FY26 Enacted and richer row types), change OPN_BA5-8 copy to `[REFERENCE]` in col E of `data_v2.xlsx`. Rows to change: 3209, 3210, 3211, 3221, 3222. Build script picks up automatically. Removes ~$729M FY26 and ~$1.037B FY27 double-count. Also update Validation sheet impact estimate from "$1.0-1.3M" to actual figures.
- [x] **R4 - GFE sub-category** — ANSWERED. `GFE / combat systems for newbuild` exists as a Bucket Sub Category in 25 rows (23 in Bucket 1, 2 in Bucket 4). Also appears as P-8a cost-element names on carrier programs. Documented in Validation sheet. IMPACT: Newbuild TAM tables D and E are missing a GFE row — the sub-category mekko breakdown only has Full Ship DD&C, Advance Procurement, RCOH, SLEP but not GFE. GFE funding won't match any of those filters, so percentages don't sum to 100% for vessel types with GFE spending. See new task B6.
- [x] **R5 - Government-only vs. private funding granularity** — REVISED. GFE ($954M FY26) is procured by the Navy from OEMs (Raytheon, LM, BAE), not from shipyards. However, the company's market scope includes BOTH hull module fabrication AND combat systems/GFE modules — so GFE is addressable market and should be INCLUDED in SAM, not excluded. "Construction engineering / planning yard" ($1.2B) remains a gray area.
  - **FIX PLAN:** Add `"GFE / combat systems for newbuild"` to the sub-category whitelist (`ddc_subs` or equivalent) in the Newbuild SAM build logic so GFE flows into SAM calculations. The P-8a system-level detail (SPY-6, Aegis, SEWIP, VLS, etc.) should be surfaced prominently as addressable module-level market. See also B6 — GFE row needed in Newbuild TAM tables D/E.
- [x] **R6 - OMN sub-component sourcing for MRO SAM Section E/F** — FULLY ANSWERED.
  - Sub-component names exist in data sheet as [SUB] row titles under 4 OMN parent programs (1B4B, 1D4D, 2B2G, 2A1F). No new column needed.
  - Section E $K column IS hardcoded (build script writes literal ints at line 1581). Section F references Section E cells, so fixing E fixes the chain.
  - **SUMIFS CAN replace the hardcoded values.** All needed named ranges exist except Line Item Title. Fix: add `('JB_T', 'D')` to shared ranges (line 1970), then change line 1581 to write `=SUMIFS(JB_26BV, JB_S,"[SUB]", JB_B,2, JB_H,"", JB_A,"OMN", JB_T,"<title>")`. Hull-name regex exclusion is handled implicitly (build script still picks which titles get rows).
  - "1BRB" in original TODO was a typo — correct PE is 1B4B. Section header says "OMN Ship Maintenance" but spans multiple programs — minor text fix.
- [x] **R7 - Other big OMN program line breakdown** — ANSWERED. Section E's Bucket 2 scope is well-covered — remaining parents (Ready Reserve Force, Equipment Maint & Depot Ops) only have hull-specific subs. The untapped opportunity is **Bucket 6** (excluded from SAM but in TAM): Ship Depot Ops Support has $1,907M in 10 no-hull sub-components, Ship Ops Support & Training $285M, Planning/Eng/Program Support $98M — totaling $2.3B. Minor: 1 Weapons Maintenance Bucket 3 sub ($24M) missed because Section E only filters Bucket 2. Bucket 6 breakdown would only be useful for TAM-level analysis since Bucket 6 is excluded from SAM.
- [ ] **R8 - Modernization bucket breakdown** — ANSWERED. Bucket 4 = $16.4B FY26. Sub-category column is essentially empty (125/126 rows blank). Best decomposition axis is source book: WPN ($6.4B, 39%), OPN BA2 ($4.4B, 27%), OPN BA1 ($2.5B, 15%), OPN BA4 ($1.3B, 8%), rest ($2.0B, 12%). Could split into 3-4 sub-buckets (Weapons & Munitions / C4ISR / Combat Systems Support / Platform Mods) derived mechanically from Source Book column. Top line items: TRIDENT II ($2.7B), Standard Missile ($1.0B), DDG Mod ($0.9B). Half the bucket has no vessel type assigned so vessel-type split won't work.

## Group 2: Build Logic / Data Integrity

Core correctness. Do these after research answers are in hand.

- [ ] **B1 - MRO SAM Section E: replace hardcoded $K with SUMIFS formulas** — Line 1581 of `build_from_data.py` writes `wc(ws, r, 2, val, ...)` with a literal int. Change to write a SUMIFS formula: `=SUMIFS(JB_26BV, JB_S,"[SUB]", JB_B,2, JB_H,"", JB_A,"OMN", JB_T,"<title>")`. Prereq: add `('JB_T', 'D')` to `shared` named ranges at line 1970. Section F and % column already use cell references, so they auto-fix. See R6.
- [x] **B2 - MRO SAM Section F: verify OMN sub-component titles** — Titles are dynamically sourced from data sheet [SUB] row titles. Section F formulas reference Section E cells. Structure is correct.
- [ ] **B6 - Add missing sub-category rows to Newbuild TAM tables D and E** — Tables D/E mekko breakdown is missing ~$3.5B across three sub-categories. Current rows (Full Ship DD&C, AP/LLTM, RCOH, SLEP) don't cover:
  - `GFE / combat systems for newbuild` — $887M FY26
  - `Construction engineering / planning yard` — $1,210M FY26
  - `(blank)` unclassified — $1,439M FY26
  - Fix: Add GFE and Construction engineering rows (same SUMIFS pattern as existing rows, filtering on `JB_F`). Investigate the $1.4B in blank sub-category — should those rows be classified? Also consider removing dead RCOH/SLEP rows (always 0% since RCOH/SLEP is Bucket 5 only, per R2).
- [ ] **B3 - Newbuild TAM Section B/C/D/E table structure** — Section B should list all in-scope vessel types (including zero-funding). Section C same for all hull programs per in-scope vessel category. Section D drops zeroed-out vessel types. Section E drops zeroed-out hull programs.
- [ ] **B4 - Remove "Less: No vessel type" from Bridge sections** — Redundant when "Less: Unattributed..." already exists. Consider adding "vessel category" to the "Unattributed" label since category is broader than type in this workbook.
- [ ] **B5 - Validate all qualifying vessels in TAM/SAM** — No accidental drop-offs? Are inclusion rules clear and being followed? Blocked by R1, R2.

## Group 3: New Features / Content

Additive work. Doesn't fix existing problems, builds new analysis.

- [ ] **C1 - Work type x $ x book source executive summary sheet** — FY26 only. Similar to what exists in Total Funding but expanded to include work type breakdown. Wait until B1-B5 are settled so totals are trustworthy.
- [ ] **C2 - Newbuild TAM Section E restructure** — Remove Vessel Type column; nest hull program rows under vessel type header rows, mirroring how Section G tables look on FY26 Newbuild SAM. Blocked by B3.
- [ ] **C3 - Add bucket 6+7 exclusion rationale** — Update MRO SAM row 2 / purpose row and Validation sheet to explain that buckets 6+7 are removed because they are "enabling" work types. Standalone.

## Group 4: Formatting / Stylistic

Lowest priority. No impact on numbers or analysis correctness.

- [ ] **D1 - Em/en dashes to hyphens** — Replace throughout. Add preference note to build script and CLAUDE.md.
- [ ] **D2 - Remove underscores** — Some text has underscores appearing in the final workbook.
- [ ] **D3 - Notes bubble: fix random newlines** — Text in notes is randomly appearing on newlines.
- [ ] **D4 - Notes bubble: fix dimension auto-fitting** — Bubble dimensions consistently cut off text vertically. Dimensions should be computed after text content is finalized, not before. May be related to D3.

## Execution Order (revised after R1-R6 investigation)

```
R3 (fix ~$1B double-count) <-- CRITICAL, highest priority
  |
R1 (USV scope decision)    <-- needs your call, affects B5
  |
B1, B6 (hardcoded $K + missing GFE row) <-- correctness
  |
B3-B5 (build logic fixes)
  |
R5, R7, R8 (remaining research)
  |
C1-C3 (new features)
  |
D1-D4 (formatting)         <-- last, low risk
```
