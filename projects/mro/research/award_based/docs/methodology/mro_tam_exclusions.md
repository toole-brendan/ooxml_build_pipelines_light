# MRO TAM Exclusions -- FY2025 Navy + USCG

**Headline:** The $7,067M post-exclusion MRO TAM is derived from an
$8,769M raw MRO-PSC universe (FY2025 Navy + USCG obligations on 68
ship-services PSCs) by removing **$1,702M of non-ship-MRO awards**
across seven natural exclusion categories. The v1.5 spec's
"approximately $333M combined" figure for shore-base and FMS was an
undercount -- $333M covers only the shore-facilities grouping; total
exclusions are 5x larger.

**Purpose:** Correct the Slide 3 footnote (3) and Slide 4 footnote
(3) of `deck/MRO_DECK_v1.5_RECONCILIATION_SPEC.md`, both of which
currently cite "~$333M" for shore-base and FMS exclusions. The true
exclusion total is $1,702M with a seven-category breakdown.

## Derivation

1. Load `navy_awards_master.json` + `cg_awards_master.json` (FPDS
   FY2025 master data with vessel classifications).
2. Filter to rows whose `psc_code` is in `MRO_PSCS` (68 codes defined
   in `sheets/services.py`) and whose `fy2025_obligation` is nonzero.
3. **Raw MRO-PSC universe:** $8,769.3M across 9,755 FPDS rows.
4. Apply `is_shore_base_excluded()` from `sheets/services.py` -- the
   same classifier used to build the Services TAM in the workbook.
5. **Kept (post-exclusion MRO TAM):** $7,066.9M across 8,572 rows.
   Matches deck headline $7,067M.
6. **Excluded:** $1,702.5M across 1,183 rows.

## Seven natural exclusion categories

Each excluded row is assigned to its primary category (first match in
the classifier). Categories grouped for deck narrative:

| Category | Rows | FY25 $M | % of excluded |
|---|---:|---:|---:|
| Cross-platform engineering IDIQs | 113 | 500.1 | 29.4% |
| Aviation MRO (NAVAIR / NAWC / FRC) | 447 | 376.2 | 22.1% |
| Shore-base facilities (ATFP / NAVFAC) | 427 | 323.0 | 19.0% |
| Non-Navy / non-ship (Army, Marine Corps, Army watercraft, USACE, JCREW) | 50 | 223.7 | 13.1% |
| LLM-flagged non-ship-MRO | 120 | 150.9 | 8.9% |
| Foreign Military Sales (FMS) | 21 | 86.4 | 5.1% |
| Inactive / decommissioned vessel maintenance | 5 | 42.2 | 2.5% |
| **Total excluded** | **1,183** | **1,702.5** | **100.0%** |

## Category details

### 1. Cross-platform engineering IDIQs ($500M, 29%)

Generic engineering / IT services IDIQs that pass through MRO PSCs
(J058 Comm/Detection, J059 Electrical/Electronic, K058, K099, etc.)
but are not ship-specific work. Biggest contributors:

- **SeaPort-NxG** ($379M): Navy's primary services IDIQ for engineering
  and professional services across all of NAVSEA, NAVAIR, SPAWAR,
  etc. When MRO PSCs are assigned to SeaPort-NxG task orders, the work
  is usually cross-platform engineering support, not ship MRO.
  Top orders: Atlas Technologies ($43M), Vector Planning ($24M, USCG
  C4ISR), HII Tech Solutions ($23M, integrated training systems).
- **Cyber Mission Engineering** ($72M): Scientific Research Corporation
  and Leidos task orders for cyber engineering work on Navy networks
  -- not ship MRO.
- **NIEF Engineering Services** ($24M), **Depot Systems Support** ($34M),
  **Combat Environment Instrumentation** ($41M), **ATC Platform
  Integration** ($5M): smaller cross-platform engineering IDIQs.

### 2. Aviation MRO ($376M, 22%)

Awards issued by Navy aviation commands that pass through ship MRO
PSCs but are aviation depot work (a separate TAM).

- **Naval Air Warfare Center (NAWC)** ($224M, 165 rows): primary
  contracting activity for NAVAIR technical labor. Examples: BAE
  Systems Technology Solutions ($22M), The MIL Corp ($17M).
- **Fleet Readiness Center (FRC)** ($59M, 103 rows): aviation depot.
  Example: Arrows Edge LLC ($27M, aviation GSE).
- **NAVAIR** ($12M), **Naval Air Systems Command** ($26M): direct
  NAVAIR awards.
- **Raytheon NAVAIR aviation missile guidance** and similar work.

### 3. Shore-base facilities ($323M, 19%)

Land-based facility work that isn't afloat ship MRO. This is the
grouping closest to the deck's "shore-base" label (and matches the
old $333M figure within rounding).

- **ATFP / Anti-Terrorism / Force Protection / Public Safety Systems**
  ($150M, 27 rows): Serco contracts for CNIC Public Safety Systems
  (installation and sustainment of shore-base security systems).
- **NAVFACSYSCOM** ($119M, 330 rows): facility repair / HVAC / housing
  repair -- e.g., repairs to Unaccompanied Personnel Housing (UPH) at
  Hawaii bases.
- **NAVFAC Systems and Exp Warfare Ctr** ($48M): related NAVFAC
  contracting activity.
- **Facility Investment Services** ($7M): small NAVFAC IDIQ.

### 4. Non-Navy / non-ship ($224M, 13%)

Contracts from non-Navy agencies that end up on MRO PSCs because of
PSC-level overlap.

- **Army Contracting Command Rock Island (W912CH)** ($116M, 23 rows):
  Army watercraft repair contracts (LCU 2020, LCM-8, LSV). Bay Ship
  & Yacht, Yokohama Engineering, Colonna's Shipyard handle these.
- **JCREW** ($69M, 1 row): Joint Counter-RCIED Electronic Warfare --
  Northrop Grumman ground EW hardware, ended up on PSC K010.
- **USACE Portland (W9127N)** ($21M): dredge vessel overhaul.
- **Marine Corps Systems Command (M67854)** ($18M): ground weapons
  modifications on K010 / K012 PSCs.

### 5. LLM-flagged ($151M, 120 rows, 9%)

PIIDs flagged as NOT_SHIP_MRO by LLM-assisted review (pipeline at
`data_pull/output/fpds/llm_exclusions.json`, 152 PIIDs total). Covers
edge cases the regex-based classifier missed. Examples: Raytheon TIS
9/16/18 incremental funding ($12M), Lockheed engineering services
USN ($9M), Nakupuna Consulting Cameron Bell ($7M).

### 6. Foreign Military Sales ($86M, 5%)

US shipyards performing ship repair for foreign navies under FMS
programs. Reimbursable revenue, but not US Navy / USCG MRO market:

- Amentum FMS Case EG-P-GKB ($27M, Egyptian Navy)
- Amentum FMS Case IQPGA ($22M, Iraqi Navy)
- Amentum FMS Case SR-P-GBU ($4M, Saudi Arabia)
- Plus ~$31M of other foreign-navy hits.

### 7. Inactive / decommissioned vessel ($42M, 5 rows, 2.5%)

Maintenance on ships already removed from the active fleet -- not
part of the current-fleet TAM.

## Correction to v1.5 deck

### Current v1.5 text (incorrect)

**Slide 3 footnote (3):**
> Exclusions applied to the $7,067M: shore-base work and Foreign
> Military Sales, approximately $333M combined; see Slide 4.

**Slide 4 footnote (3):**
> All figures on a post-exclusion ($7,067M) basis. Shore-base and FMS
> exclusions (~$333M) are treated proportionally across appropriations;
> see Slide 3 footnote (3).

### Suggested corrected text

**Slide 3 footnote (3):**
> Exclusions applied to the raw $8,769M MRO-PSC universe to derive the
> $7,067M TAM: $1,702M across seven categories -- cross-platform
> engineering IDIQs ($500M, SeaPort-NxG and cyber), aviation MRO
> ($376M, NAVAIR / NAWC / FRC), shore-base facilities ($323M, ATFP /
> NAVFAC), non-Navy contracting activities ($224M, Army W912CH
> watercraft, JCREW, USACE, Marine Corps M67854), LLM-flagged
> non-ship-MRO ($151M), Foreign Military Sales ($86M), and inactive-
> vessel maintenance ($42M). Method: `sheets/services.py::
> is_shore_base_excluded`. Full breakdown: `docs/methodology/
> mro_tam_exclusions.md`.

**Slide 4 footnote (3):**
> All figures on a post-exclusion ($7,067M) basis. Exclusions ($1.7B)
> are treated proportionally across appropriations; see Slide 3
> footnote (3) for category breakdown.

## Why the old "$333M" number was off

The v1.5 spec carried forward a "~$333M combined shore-base + FMS"
footnote from older drafts. Two issues:

1. **$333M only covers the shore-facilities category.** The actual
   shore-base grouping (ATFP + NAVFAC + Facility Investment) totals
   $323M, which rounds to $333M if one adds FMS. The figure was
   correct for those two narrow categories but omitted the five
   larger categories (cross-platform eng IDIQs, aviation MRO, non-
   Navy, LLM-flagged, inactive vessels).

2. **The deck's implied pre-exclusion universe ($7.4B) was a
   TAS-attributed number, not the raw FPDS MRO-PSC universe.** The
   $7.4B was what got matched to Treasury Accounts for the
   appropriation-sourcing view (Slide 4). The raw MRO-PSC FPDS
   universe is $8.77B. The difference between these two "pre-exclusion"
   numbers ($8.77B vs $7.4B) is the portion of MRO-PSC awards that
   didn't get TAS-attributed and went through imputation -- that's
   the "51% imputed" share flagged in Slide 4 RHS callout.

In practice, the pipeline applies exclusions before TAM rollup, so
the Services TAM builder sees $7,067M. The footnote was describing
a different residual ($7.4B -> $7.067B = ~$333M) that reflects TAS-
attribution math, not the exclusion math.

## Supporting numbers

- Raw MRO-PSC universe (pre-exclusion): **$8,769.3M**, 9,755 rows
- Exclusions: **$1,702.5M**, 1,183 rows
- MRO TAM (post-exclusion, ties to deck): **$7,066.9M**, 8,572 rows
- Exclusion rate: 19.4% of raw universe
- Top three categories: cross-platform eng ($500M), aviation ($376M),
  shore-base ($323M) -- together 70% of exclusions

## Confidence

**High.** The classifier is the production `is_shore_base_excluded()`
function used to build the Services TAM in the workbook. The kept-
total ($7,066.9M) reconciles to the headline $7,067M deck figure
within $0.1M rounding. Category assignments are based on documented
regex patterns in `sheets/services.py`, not ad-hoc tagging.

Residual uncertainty is in the LLM-flagged bucket ($151M) -- those
are case-by-case exclusions that could be re-reviewed, but the
aggregate dollar impact is small relative to the total.

Generated: 2026-04-20 (walk-in build session for v1.5 deck).
