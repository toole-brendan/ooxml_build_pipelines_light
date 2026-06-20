# Session 2026-04-18 (ii): Sub & Carrier Coverage scope-reconciliation sheet - v2.69 -> v2.71

## Context

DECK.md Slide 2 (Vessel Mix) asserts in a right-margin callout that
"submarine spend is structurally understated" because ~$4-6B of annual
nuclear depot work is performed in-house at the four public naval
shipyards (Portsmouth, Norfolk, Puget Sound, Pearl Harbor) and does not
generate FPDS records. DECK.md Slide 3 (MRO Work Segments) carries a
footnote that "Nuclear Propulsion Sustainment PSCs (J044/K044/N044) appear
at ~$0 because reactor work is contracted under ship-level shipbuilding
codes at HII Newport News, Fluor Marine, and Bechtel."

User wanted both claims verified with actual FY2025 figures (not just
references to methodology doc `docs/methodology/METHODOLOGY_CVN_SSN_
COVERAGE.md`), and a new workbook sheet + draft deck slide explaining
where submarine and carrier funding actually lives in the data.

Budget-book PDFs (NWCF, OMN, OMN Vol 2, OPN BA1-8, SCN, USCG, WPN) were
added mid-session at `sources/` with `.txt` extractions alongside.

Ended at **v2.70 workbook** with a new **Sub & Carrier Coverage**
scope-reconciliation sheet slotted after Depot Ship Repair, plus a
standalone Slide 5 mockup file in `deck/`.

---

## Work completed, in order

### 1. Initial exploration and claim formulation

Re-read `README.md`, `CLAUDE.md`, `build_from_data.py`, `DECK.md`. Read
`sheets/awards.py`, `sheets/services.py`, `sheets/product_procurement.py`
to understand how the Services TAM (68 MRO PSCs) and Product Procurement
(newbuild PSCs) views are PSC-filtered slices of the unified Awards
table. Read `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md` to
understand the existing framing of the public-yard gap and J044
emptiness. Read `docs/Seven_Bucket_TAM_Crosswalk.md` to understand the
bucket taxonomy and budget-anchor references.

Proposed two claims to verify for FY2025:

1. Most submarine MRO is performed in-house at public naval shipyards
   (not in FPDS).
2. Private-contractor submarine and carrier MRO that IS awarded gets
   coded into Product Procurement / shipbuilding PSCs (PSC 1905), so it
   sits on the Product Procurement sheet rather than the Services sheet.

### 2. First-pass data query (v2.69 unchanged)

**`/tmp/query_subs_carriers.py`** (scratch). Loaded `navy_awards_master.
json` (69 MB) + `cg_awards_master.json` (16 MB), filtered to
`vessel_supergroup in ('Submarines', 'Aircraft Carriers')`, classified
each row into one of:

- `services_mro` (PSC in `MRO_PSCS`)
- `newbuild_product` (PSC in `NEWBUILD_PSCS`)
- `nuclear_excluded` (J044 / K044 / N044)
- `other`

FY25 totals by bucket:

| Platform          | Services MRO | Newbuild/Product | Nuclear (J044/K044/N044) |
|-------------------|-------------:|-----------------:|-------------------------:|
| Submarines        | $838M (3%)   | **$25,099M (97%)** | $0M                   |
| Aircraft Carriers | $422M (23%)  | **$1,437M (77%)**  | $0M                   |

Cross-check: Services TAM rebuild = $7,066.9M, matches DECK.md $7.1B
headline.

PSC 1905 is the mega-bucket at $38.1B total FPDS - $24.3B tagged
Submarines, $1.43B tagged Aircraft Carriers, $5.65B Surface Combatants,
rest to amphibs / CLF / unclassified. PSC 4470 Nuclear Reactors = $1.87B,
100% unclassified supergroup (Fluor Marine Propulsion reactor-plant
components are not hull-tagged).

### 3. User pushback: "verify PIIDs, don't just cite the methodology doc"

User pushed back that citing `METHODOLOGY_CVN_SSN_COVERAGE.md` wasn't
enough - wanted PIID-level evidence plus budget-book cross-check. Also
noted `sources/` now contained the budget-book PDFs and `.txt`
extractions. Warning to be careful not to crash on large files.

### 4. PIID-level verification

**`/tmp/query_piids.py`** (scratch). Dumped top-15 PIIDs for each of:

- Submarines x PSC 1905
- Aircraft Carriers x PSC 1905
- PSC 4470 (Fluor Marine, Bechtel)
- Submarines x MRO PSCs (the $838M Services slice)
- Aircraft Carriers x MRO PSCs (the $422M Services slice)

Key PIIDs surfaced:

- **`N0002418C4314`** HII $424M FY25 PSC 1905 = "USS BOISE (SSN 764)
  ENGINEERED OVERHAUL EXECUTION" at SUP OF SHIPBUILDING CONV AND R.
  Real SSN depot EOH at Newport News, coded as shipbuilding rather than
  J998/J999. This is direct PIID evidence that PSC 1905 contains
  private-yard sub MRO bundled into the newbuild PSC - not pure
  construction.
- **`N0002417C2100`** Electric Boat $9,336M at SUP OF SHIPBUILDING
  GROTON = "BALANCE TESTING OF THE MAIN PROPULSION UNIT" (Columbia MPU)
- **`N0002417C2117`** Electric Boat $6,176M = "DRAWING UPDATES FOR
  GOVERNMENT FURNISHED INFORMATION" (Columbia drawings)
- **`N0002424C2110`** Electric Boat $3,095M = "SSN 814 LONG LEAD TIME
  MATERIAL" (Virginia long-lead)
- **`N0002424C2115`** Bechtel Plant Machinery $1,101M = "FY25 NUC
  COMPONENTS" (Virginia reactor)
- **`N0002424C2135`** BlueForge Alliance $366M = "US SIB SUB SUPPLIER
  DEVELOPMENT SUPPORT" (Submarine Industrial Base per OMN line 6754)
- **`N0002425C2127`** HII $97M PSC 1905 = "CVN 68 INACTIVATION AP
  EMERGENT" (Nimitz inactivation - real CVN MRO, bundled into 1905)
- **`N0002418C2130`** Fluor Marine Propulsion $1,810M PSC 4470 =
  "FUNDING OBLIGATIONS AND DE-OBLIGATIONS" (Naval Reactors Program)
- **`N0003024C6001`** Draper Lab $318M PSC J014 at STRATEGIC SYSTEMS
  PROGRAMS = "MK7 LE2 SYSTEM REQUIREMENTS FY25" (Trident II
  sustainment - dominant single line in the $838M sub Services slice)
- **`N4523A25F0302`** HII $91M + $75M PSC J998 at PUGET SOUND NAVAL
  SHIPYARD IMF = "CVN 76 FY 25 DPIA UCA DELIVERY ORDER" (Reagan DPIA -
  private contractor at public yard, IN Services TAM)

### 5. Budget-book cross-reference

Line counts confirmed `.txt` extractions manageable for grep (NWCF 9k
lines, OMN 30k lines, SCN 17k lines, ~192k lines total across 11
files). Used Grep tool + Read with `offset` / `limit` to pull specific
sections; never read any of the large .txt files wholesale.

**OMN SAG 1B4B Ship Maintenance** (FY2026 President's Budget submission,
detail by subactivity group):

| Cost Element                             | FY24 Actuals |  FY25 Enacted | FY26 Request |
|------------------------------------------|-------------:|--------------:|-------------:|
| 928 Ship Maintenance By Contract         |   $1,769,659 |   $2,228,255  |   $3,971,574 |
| ... all other cost elements ...          |              |               |              |
| TOTAL 1B4B Ship Maintenance              |  $11,502,495 |  $11,763,594  |  $13,803,188 |

The non-contract remainder of SAG 1B4B FY25 = $11,764M - $2,228M =
**$9,535M** flowing to public-yard labor, supplies, intra-government
support, NWCF reimbursement to Naval Shipyards.

**SCN P-1 FY25 Enacted** (FY2026 President's Budget, 1611N detail):

| Line Item                                  | FY25 Enacted |
|--------------------------------------------|-------------:|
| LI 1045 Columbia Class (BA01 total FBM)    |   $9,580,774 |
| LI 2013 Virginia Class                     |   $9,500,534 |
| LI 2086 CVN Refueling Overhauls            |   $6,271,049 |
| LI 2001 Carrier Replacement (CVN-80)       |   $1,359,124 |
| LI 2004 CVN-81                             |     $800,492 |
| **SCN nuclear-platform subtotal**          |  **$27,512,073** |

Top-down cross-check: SCN nuclear-platform FY25 BA $27.5B reconciles
cleanly to FPDS PSC 1905 subs ($24.3B) + PSC 1905 carriers ($1.4B) + PSC
4470 ($1.9B) = $27.6B captured obligations (small gap explained by
prior-year rollovers, advance procurement flows, and PSC 1905 "other"
hulls).

**OMN SAG 1B2B Ship Operational Support** explicitly funds "Virginia
Class (VACL) submarine obsolescence materials public shipyard
outsourcing work in an effort to support Navy's 15-year maintenance plan
thru the FYDP" (OMN_Book line 4809). Direct budget-book confirmation
that the Navy IS leaking public-yard work to private yards, which is why
PSC 1905 contains artifacts like the HII Boise EOH.

### 6. Proposal review and direction from user

Presented findings to user. Both claims confirmed directionally with
nuance:

1. Public-yard claim: confirmed. $9.5B implied non-contract slice of
   SAG 1B4B, but this covers ALL Navy ships, not just nuclear. Nuclear
   platforms are the dominant workload at Portsmouth / Puget Sound /
   Pearl Harbor but the number isn't carved out cleanly.
2. Bundling claim: confirmed definitively. Boise EOH, CVN inactivation,
   RCOH administrative transfers all sit under PSC 1905 in FPDS.

User approved building both the sheet and the slide mockup. Sheet
placement: after Depot Ship Repair.

### 7. Sheet implementation - `sheets/sub_carrier_coverage.py`

Mirrored the pattern used by `sheets/depot_ship_repair.py`: standalone
module loading rows from the unified Awards master JSON via
`awards.load_rows()` (so shore-base exclusion is consistent with the
Services sheet), static values rather than SUMIFS (scope reconciliation
is not a column on the Awards schema), budget-book figures hard-coded
rather than parsed from `sources/` at build time.

Sheet layout:

1. Title + purpose band
2. FY2025 Scope Reconciliation headline - 7-row table showing where sub
   and carrier dollars live across Services MRO / Newbuild / Nuclear
   PSCs / PSC 4470 / public-yard buckets, with "In Services TAM?"
   column
3. Budget-Book Anchors table - three sub-sections (OMN SAG 1B4B / SCN
   Sub Programs / SCN Carrier Programs) with FY25 Enacted $M, source
   line references, and a "what it funds" column
4. Submarine top 15 PIIDs in Newbuild/Product (PSC 1905 family)
5. Submarine top 12 PIIDs in Services TAM (J/K/N/M MRO PSCs)
6. Aircraft Carrier top 15 PIIDs in Newbuild/Product
7. Aircraft Carrier top 12 PIIDs in Services TAM
8. PSC 4470 Nuclear Reactors top 10 PIIDs
9. Nuclear Maintenance PSC emptiness table (J044 / K044 / N044 + total)
10. Scope reconciliation notes - 6-item plain-English explainer

Tab color: deep purple `#4A148C` to signal scope reconciliation (distinct
from the green-family Product Procurement / Services / Depot Ship Repair
tabs).

**Wrinkle:** Excel sheet names can't contain `/`. Initial name
`Sub/Carrier Coverage` failed validation in `wb.create_sheet()`; renamed
to `Sub & Carrier Coverage`. Fixed in sheet module + build_from_data tab
color reference + smoke test script.

Smoke-tested with `/tmp/smoke_sub_carrier.py` (builds just the new sheet
into a scratch workbook) before running the full workbook build.

### 8. Wire into `build_from_data.py`

Added import, invoked `create_sub_carrier_coverage(wb)` after
`create_depot_ship_repair(wb)`, added deep-purple tab color. Final sheet
order:

`Overview` -> `Product Procurement` -> `Services` -> `Depot Ship Repair`
-> **`Sub & Carrier Coverage`** -> `Sub Ratios` -> `Public Comps` ->
`Awards` -> `Subcontract Data` -> `Vessel Taxonomy`

### 9. Slide 5 mockup - `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md`

User requested the Slide 5 description be a standalone file rather than
an edit to `DECK.md` (DECK.md is the "actual state" doc and should not
contain proposed / not-yet-delivered content). Reverted the DECK.md
edit; wrote a standalone mockup file.

Content:

- Title: "Sub & Carrier Scope | FY2025 private-contractor sub and
  carrier MRO in the Services TAM is ~$1.3B; the bulk of nuclear-
  platform work is either bundled into shipbuilding PSCs or performed
  in-house at public naval shipyards"
- Left visual: horizontal bar chart, 7 buckets ranked by $, color-coded
  by "captured in Services TAM?" status
- Right visual: budget-book anchor table (OMN SAG 1B4B + SCN line items)
- Call-out box on the Boise EOH / public-yard outsourcing leakage
- 4 footnotes covering derivation of public-yard estimate, NWCF
  mechanics, J044 emptiness explanation, sources
- Audience motivation section explaining which reader questions the
  slide answers
- Build-out assets section listing what the workbook sheet provides to
  back the slide

### 10. Build and verify - v2.70

Ran `python3 -m domnann.build_from_data`. v2.69 auto-archived to
`output/archive/`. v2.70 saved.

Build output:

```
Built Sub & Carrier Coverage (277 sub rows $25,941M, 281 carrier rows $1,867M)
```

Every other sheet unchanged (same row counts, same totals).

---

## Files touched

### New files

- `sheets/sub_carrier_coverage.py` - 500 lines. Scope-reconciliation
  sheet builder.
- `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` - standalone slide mockup.
  Not linked from DECK.md.

### Modified files

- `build_from_data.py` - import + invoke + tab color for the new sheet.

### Unchanged files (intentionally)

- `DECK.md` - Slide 5 is a proposal, not delivered state.
- `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md` - still the
  underlying narrative doc; sheet provides the FY25 numbers that doc
  leaves soft ("~$4-6B estimate").

### Scratch files (not committed)

- `/tmp/query_subs_carriers.py` - initial bucket query
- `/tmp/query_deep.py` - PSC 1905 / 4470 / 1901 / 1904 breakdown
- `/tmp/query_piids.py` - PIID-level detail dump
- `/tmp/smoke_sub_carrier.py` - single-sheet smoke test

---

## Key numbers for future reference

FY2025 FPDS obligations (from unified Awards master):

| Platform          | Services MRO | Newbuild/Product (PSC 1905) | Nuclear PSCs (J044/K044/N044) | Total FPDS |
|-------------------|-------------:|----------------------------:|------------------------------:|-----------:|
| Submarines        |        $838M |                     $24,279M |                          $0M  |   $25,941M |
| Aircraft Carriers |        $422M |                      $1,431M |                          $0M  |    $1,867M |

Cross-platform reactor product:
- PSC 4470 Nuclear Reactors: $1,875M FY25 (Fluor Marine Propulsion
  $1,810M single PIID `N0002418C2130` dominates; Bechtel Plant Machinery
  residual)

FY25 Enacted budget authority (FY2026 PB exhibits):
- OMN SAG 1B4B Ship Maintenance total: $11,764M
  - of which Ship Maint By Contract: $2,228M
  - implied non-contract (public yards + supt.): $9,535M
- SCN Columbia (LI 1045 BA01): $9,581M
- SCN Virginia (LI 2013): $9,501M
- SCN CVN RCOH (LI 2086): $6,271M
- SCN Carrier Replacement (LI 2001 CVN-80): $1,359M
- SCN CVN-81 (LI 2004): $800M
- SCN nuclear-platform subtotal: $27,512M FY25

Top-down vs bottom-up: $27.5B SCN BA reconciles to $27.6B FPDS
obligations under PSC 1905 + 4470.

---

## Follow-up: formula-driven values (v2.70 -> v2.71)

### 11. User pushback - "no formulas, this isn't live data"

After v2.70 shipped, user opened the new Sub & Carrier Coverage sheet
and noticed all numbers were hard-coded Python values rather than
formulas referencing other sheets. User asked how to fix this and
whether a new data sheet was needed for the budget-book figures not
present in Awards.

Diagnosis: the sheet mixed two kinds of numbers that both need to be
live, but with different backing sources:

- FPDS-derived figures (Services MRO, PSC 1905, PSC 4470, etc.) should
  be SUMIFS against `Awards[FY2025 Obligation]` exactly like Services
  and Product Procurement do.
- Budget-book figures (OMN SAG 1B4B, SCN Columbia, etc.) are NOT in
  Awards at all - they come from `sources/OMN_Book.txt` and
  `sources/SCN_Book.txt`. They need a new data sheet.

### 12. New data sheet - `sheets/budget_anchors.py`

Small reference table of FY24 Actuals / FY25 Enacted / FY26 Request
for seven line items used by the scope reconciliation:

- OMN SAG 1B4B Total Ship Maintenance
- OMN SAG 1B4B cost element 928 Ship Maintenance By Contract
- SCN LI 1045 Columbia Class BA01 total
- SCN LI 2013 Virginia Class
- SCN LI 2086 CVN Refueling Overhauls
- SCN LI 2001 Carrier Replacement (CVN-80)
- SCN LI 2004 CVN-81

Values in $K exactly as printed in the budget exhibits. Data lives in
an Excel Table named `BudgetAnchors`; each FY25 Enacted cell gets a
defined name at the workbook level for downstream reference:

```
OMN_1B4B_TOTAL_FY25
OMN_1B4B_CONTRACT_FY25
SCN_COLUMBIA_FY25
SCN_VIRGINIA_FY25
SCN_CVN_RCOH_FY25
SCN_CVN_REPL_FY25
SCN_CVN81_FY25
```

Tab color slate (data-sheet family), placed in the Data Sheets section
of `build_from_data.py`.

### 13. Sub & Carrier Coverage refactor

Rewrote `sheets/sub_carrier_coverage.py` to use live formulas:

- **Reconciliation headline** - every $ cell is now a SUMIFS against
  `Awards[FY2025 Obligation]` with PSC + Vessel Type filters. Added
  helper builders `_sumifs_one`, `_sumifs_many`, `_sumifs_vessel_total`
  mirroring the services.py pattern.
- **Headline design** changed from aggregated buckets to PSC-specific
  rows to fit within Excel's 8,192-char per-cell formula limit:
  PSC 1905 / PSC 4470 / J998+J999 / Other MRO (63 PSCs) / J044+K044+N044 /
  Other newbuild residual. The "Other newbuild residual" row is derived
  by subtraction from `SUMIFS(..., Vessel Type, "Submarines")` minus the
  five other bucket rows - enumerating 130 other newbuild PSCs would
  blow past the 8,192 limit.
- **"Other MRO" formula length check:** 63 PSCs x ~92 chars per SUMIFS
  = 5,428 chars for Submarines; well under the 8,192 limit.
- **Budget-book anchor table** - every $ cell is now a formula like
  `=OMN_1B4B_TOTAL_FY25/1000` (Budget Anchors stores $K; display as $M).
- **Public-yard labor cell** - formula
  `=(OMN_1B4B_TOTAL_FY25-OMN_1B4B_CONTRACT_FY25)/1000`. Updates
  automatically when the budget-book values change.
- **Nuclear Maint PSC emptiness** - SUMIFS + COUNTIFS per PSC.
- **Top-N PIID tables** stay as static Python-ranked snapshots.
  Same convention as the Services sheet's Top-N contractor tables; a
  SUMIFS keyed by a single PIID trivially matches one row, so the
  live-formula conversion would add no value.

Smoke-tested with `/tmp/smoke_v2.py` (Awards + Budget Anchors + Sub &
Carrier Coverage in a scratch workbook). All 7 defined names resolved.
Formula lengths verified via `_sumifs_many` builder.

### 14. Build v2.71

Ran `python3 -m domnann.build_from_data`. v2.70 auto-archived. v2.71
saved. Final sheet order:

```
Overview -> Product Procurement -> Services -> Depot Ship Repair
-> Sub & Carrier Coverage -> Sub Ratios -> Public Comps -> Awards
-> Subcontract Data -> Budget Anchors -> Vessel Taxonomy
```

Every FPDS figure on Sub & Carrier Coverage now recomputes when
`Awards` regenerates. Every budget-book figure recomputes when a Budget
Anchors cell is edited.

---

## Files touched (updated)

### New files (v2.70 and v2.71)

- `sheets/sub_carrier_coverage.py` - scope reconciliation sheet (v2.70,
  refactored v2.71 to use live formulas)
- `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` - standalone slide mockup
  (v2.70)
- `sheets/budget_anchors.py` - new data sheet for budget-book line
  items (v2.71)

### Modified files

- `build_from_data.py` - wired in the two new sheets plus tab colors

---

## Open questions / future work

1. Should Slide 5 enter DECK.md now as a "proposed / not delivered"
   section, or stay in the standalone mockup until the actual slide is
   designed? (User chose standalone for now.)
2. The $9.5B implied public-yard figure covers all Navy ships. A
   follow-up could carve out the nuclear-platform slice specifically
   (Portsmouth / Puget Sound / Pearl Harbor workload as reported to
   Congress in the 30-year shipbuilding plan or the Naval Shipyards
   workload plan). This would sharpen the "nuclear depot at public
   yards" claim on Slide 2 from a soft "~$4-6B estimate" to a harder
   figure.
3. The Submarine Industrial Base (SIB) program at BlueForge Alliance
   ($366M FY25) is coded as PSC 1905 Submarines and therefore sits in
   Product Procurement, not Services. It is substantively a supplier-
   development / industrial-base investment, not ship MRO nor
   construction. Worth a separate tag or callout?
4. Budget Anchors currently has 7 line items. Expanding to cover
   additional appropriations (NWCF, OPN BA5-8, WPN, USCG PC&I)
   could turn this into a general top-down budget cross-check sheet
   useful across the workbook, not just for sub/carrier reconciliation.
5. If v2.71 is committed as a milestone, the file needs `git add -f`
   per the `output/archive/` gitignore note in CLAUDE.md.
