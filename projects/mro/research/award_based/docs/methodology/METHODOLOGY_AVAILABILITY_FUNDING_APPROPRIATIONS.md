# Availability Funding by Appropriation -- Research Note

**Date:** 2026-04-20
**Purpose:** Resolve the source for the deck claim "Depot availabilities (DSRAs, DPIAs, CNO avails) are funded through OPN BA-7, not OMN CE-928" (appears in MRO_DECK_v1.5_RECONCILIATION_SPEC.md Slide 4 callout card 3 and Slide 3 footnote 1).
**Finding:** The claim as stated is incorrect on both halves. Availabilities are funded by both OMN and OPN; the OPN portion is in BA-01, not BA-07.
**Sources used:** FY2026 President's Budget Submission, sourced from `sources/OMN_Book.txt` and `sources/OPN_BA1_Book.txt`.

---

## 1. What the original claim said

From the v1.5 reconciliation spec and the v3 deck footer:

> Depot availabilities (DSRAs, DPIAs, CNO avails) are funded through BA-7, not through OMN CE-928 contract maintenance.

This claim has two parts:
1. OPN funds availabilities (true, but partial)
2. OPN BA-7 is the specific line (false -- it is BA-01)

And implicitly:
3. OMN CE-928 does not fund availabilities (false -- CE-928 is the private-contract slice of OMN 1B4B, which funds 65% of availabilities)

## 2. Primary source A -- OMN Exhibit OP-5, SAG 1B4B

**Location:** `sources/OMN_Book.txt` lines 5326-5400 (Exhibit OP-5, 1B4B, Pages 1-3 of 29).

**Document:** FY2026 President's Budget Submission, Operation and Maintenance, Navy, Budget Activity: Operating Forces, Activity Group: Ship Operations, Detail by Subactivity Group: Ship Maintenance.

**Key finding:** The Navy's own Ship Maintenance SAG exhibit explicitly partitions every depot availability by appropriation source. The exhibit has three tables on three successive pages: total (OMN + OPN), OMN-only, and OPN-only.

### FY2024 availability counts by appropriation (from OP-5 1B4B)

| Availability Type | Total | OMN | OPN |
|---|---|---|---|
| Overhauls (OH) | 8 | 4 | 4 |
| Selected Restricted Availabilities (SRA) | 38 | 18 | 20 |
| Surface Incremental Availabilities (SIA) | 16 | 16 | 0 |
| Planned Incremental Availabilities (PIA) | 4 | 4 | 0 |
| Phased Maintenance Availabilities (PMA) | - | - | - |
| Carrier Incremental Availabilities (CIA) | 2 | 2 | 0 |
| Service Craft Overhauls (SCO) | - | - | - |
| Non-Depot / Intermediate Maintenance | - | - | - |
| **Total** | **68** | **44 (65%)** | **24 (35%)** |

Plus MSC: FY26 Navy plans 17 mid-term availabilities + 34 regular overhauls on MSC platforms, all OMN-funded (transferred to 1B4B from 1B1B per OMN Volume 1, line 4466).

### OMN 1B4B financial scale

- 1B4B Ship Maintenance FY24 actual: $11,502M
- 1B4B Ship Maintenance FY25 estimate: $11,764M
- 1B4B Ship Maintenance FY26 request: $13,803M
- **CE-928 Ship Maintenance By Contract (FY24 actual):** $2,083,856K = **$2.08B**
  - This is one cost element within 1B4B -- the private-contracted slice.
  - Other cost elements under 1B4B cover public-yard customer orders (NWCF payments), civilian labor, material, travel, facility support, etc.
- CE-928 is the primary OMN source for private-contracted availability labor.

### Direct quote establishing OMN + OPN co-funding (line 5349)

> FY 2024-2026 includes Operation and Maintenance, Navy (OMN) and Other Procurement, Navy (OPN)

## 3. Primary source B -- OPN Exhibit P-40, BA-01 Line Item 1000

**Location:** `sources/OPN_BA1_Book.txt` lines 21185-21310 (Exhibit P-40, Budget Line Item Justification, PB 2026 Navy).

**Document structure:**
- Appropriation: 1810N Other Procurement, Navy
- Budget Activity: **BA 01: Ships Support Equipment** (not BA 07)
- Budget Sub-Activity: BSA 10: Reactor Plant Equipment
- P-1 Line Item Number / Title: **1000 / Ship Maintenance, Repair and Modernization**

### Financial scale

| Year | Amount ($M) |
|---|---|
| Prior Years | 4,848.631 |
| FY2024 actual | 2,839.179 |
| FY2025 estimate | 2,392.190 |
| FY2026 Base request | 2,392.620 |
| FY2026 Total | 2,392.620 |

### Scope quotes (verbatim from source)

Line 21205: *"Division A of the Consolidated Appropriations Act, 2020, Public Law 116-93 appropriated funding in Other Procurement, Navy (OPN) to initiate a program funding private contracted ship maintenance in the U.S. Pacific Fleet (CPF) in Fiscal Year (FY) 2020."*

Line 21207: *"Division C of the Consolidated Appropriations Act, 2022 expanded the program to include both U.S. Pacific Fleet and U.S. Fleet Forces (FFC)."*

Line 21209: *"FY 2026 funds $2.4B for Continental United States (CONUS) private contracted surface and submarine maintenance in both U.S. Pacific Fleet (CPF) and U.S. Fleet Forces Command (FFC)."*

Line 21211: *"Funding private contracted ship maintenance planned for CPF and FFC with OPN allows the Navy to implement commercial best practices for ship maintenance and achieve Navy's A-120 contracting policy."*

Line 21296: *"FY 2026 requests $2.4 Billion for U.S. Pacific Fleet and U.S. Fleet Forces to continue private contracted ship maintenance. Funding for ship maintenance Overhauls (OH) to Restricted/Technical Availabilities (RA/TA) performed at private shipyards."*

### Full availability taxonomy defined in this line item (lines 21216-21268)

The OPN BA-01 Line 1000 justification explicitly defines every availability type this appropriation funds:

- **CIA** (Carrier Incremental Availability): Continuous depot maintenance and selected modernization on CVN-68 class aircraft carriers.
- **DMP** (Depot Modernization Period): Scheduled primarily for installation of major high-priority warfare improvement alterations.
- **DPIA** (Docking Planned Incremental Availability): Labor-intensive availability, less than one year duration, for CVNs in an Incremental Maintenance Plan.
- **DPMA** (Docking Phased Maintenance Availability): A PMA expanded to include maintenance requiring dry-docking.
- **DSRA** (Docking Selected Restricted Availability): An SRA expanded to include dry-docking.
- **EDPMA** (Extended Docking Phased Maintenance Availability): A DPMA extended for work that cannot be done in a DPMA.
- **EDSRA** (Extended Docking Selected Restricted Availability): A DSRA extended for work that cannot be done in a DSRA.
- **ERP** (Extended Refit Period): SRA with short docking inspection.
- **EOH** (Engineered Overhaul): Overhaul of nuclear-powered submarines without reactor refueling.
- **ERO** (Engineered Refueling Overhaul): Major overhaul with reactor refueling.
- **MMP** (Major Maintenance Period): Onsite non-CNO availability for SSGNs.
- **OH** (Overhaul): Major availability typically exceeding 6 months.
- **PIA** (Planned Incremental Availability): Labor-intensive availability less than 6 months for CVNs.
- **PIRA** (Pre-Inactivation Restricted Availability): Hull-specific, pre-inactivation.
- **PMA** (Phased Maintenance Availability): Short labor-intensive availability for Phased Maintenance Program ships.
- **RA / TA** (Restricted / Technical Availability): Depot-level support including combat systems, habitability, calibration, NRMF work.
- **SCO** (Service Craft Overhaul): Major industrial availability for service craft.
- **SRA** (Selected Restricted Availability): Short labor-intensive industrial period for Progressive or Engineered Operating Cycle Maintenance ships.

Every availability type that the deck referenced ("DSRAs, DPIAs, CNO avails") is explicitly in this BA-01 line.

## 4. What OPN BA-07 actually funds

`sources/OPN_BA5-8_Book.txt` lines 11609-11650 (OPN BA 07 / BSA 2 / P-1 Line Item 8106 Command Support Equipment):

- FY24 actual: $45M
- FY25 estimate: $30M
- FY26 request: $34M

Line 11629: *"This line provides for new and systematic replacement of investment items required in support of the Navy's operational mission. Procurement of Command Support Equipment throughout the Navy involves..."*

BA-07 funds investment-level equipment. Some of this equipment is installed on ships during availabilities (Navy Cash hardware, command systems), but the availability itself is not funded from BA-07. The deck conflates "equipment installed during an availability" with "funding for the availability."

## 5. Corrected claim for the deck

Replace the BA-7 claim with:

> Maintenance availabilities are funded by both OMN and OPN. OMN funds ~65% of availabilities via SAG 1B4B Ship Maintenance (CE-928 "Ship Maintenance By Contract" is the $2.08B private-contract slice of 1B4B's $11.76B FY25 total). OPN funds ~35% of availabilities via BA-01 Line Item 1000 "Ship Maintenance, Repair and Modernization" ($2.4B FY26 request for CPF and FFC private-contracted maintenance; legal basis PL 116-93, Consolidated Appropriations Act 2020). OPN BA-7 (Personnel & Command Support Equipment) funds investment equipment installed during availabilities, not the availabilities themselves.
>
> *Sources: OMN Vol 1 Exhibit OP-5 SAG 1B4B pp 1-3; OPN Vol 1 Exhibit P-40 BA-01 BSA-10 Line Item 1000.*

## 6. Secondary discrepancy -- workbook OPN Program Activity attribution

### The puzzle

Our workbook's `approp_opn_pa_split.json` (coverage and rollup) attributes FY25 MRO-PSC OPN dollars as:

| OPN Budget Activity | $M | % of OPN |
|---|---|---|
| BA-7 Personnel & Command Support Equip (PA 0007) | 1,591 | 61.5% |
| BA-8 Spares & Repair Parts (PA 0008) | 825 | 31.9% |
| BA-1 Ships Support Equipment (PA 0001) | 65 | 2.5% |
| Undistributed / Unspecified | 107 | 4.1% |
| **OPN Total (on MRO PSCs)** | **2,588** | **100%** |

But the OPN P-5 shows BA-01 Line 1000 Ship Maintenance alone is $2.4B FY26 request. If that line is coded to J998 / J999 MRO PSCs in FPDS, our BA-01 share would be dominant -- not $65M.

### Likely explanation

The $2.4B of OPN BA-01 Line 1000 is probably coded to **PSC 1905 (Ship and Boat Construction)** or another non-MRO PSC in FPDS, not to our 68 MRO PSCs. In that case:

- The $2.4B does not appear in the MRO TAM at all -- it is inside the bottom-left cell of the Slide 3 matrix, part of the $38.1B PSC 1905 "with embedded MRO" block.
- The $1.59B "BA-7" in our MRO-PSC data represents OPN BA-7 investment equipment installs flowing through MRO PSCs (real BA-7 activity).
- The OPN MRO $ we capture is NOT the OPN availability-contracts pot -- it is the OPN equipment-installs-during-availabilities pot.

This dovetails with the Slide 3 "PSC 1905 contains hidden MRO" story: if the $2.4B OPN-funded private-contracted maintenance program is coded to PSC 1905, then PSC 1905 contains at least $2.4B of embedded MRO just from OPN BA-01 alone.

### Follow-up investigation (not yet done)

1. Pull all FY25 FPDS awards with TAS 017-1810 and Program Activity 0001 (OPN BA-1). Tabulate by PSC. Verify whether these awards hit PSC 1905 or the MRO PSCs.
2. Cross-reference award descriptions: "CPF private-contracted ship maintenance" language should appear in the OPN BA-01 Line 1000 awards, making them easy to find.
3. If confirmed that the $2.4B OPN BA-01 Line 1000 hits PSC 1905, this is load-bearing evidence for the Slide 3 claim that PSC 1905 contains embedded MRO -- and puts a specific $ floor on the embedded amount.

Expected effort: 1 hour.

## 7. Implications for v1.5 reconciliation spec

### Load-bearing corrections

1. **Slide 4 callout card 3** (currently "Depot availabilities funded through BA-7, not OMN CE-928"): rewrite with the paragraph from Section 5 above. Drops the false BA-7 claim and the false CE-928 claim.
2. **Slide 3 footnote (1)** interim bound language: the OMN 1B4B less CE-928 = $9.5B derivation for public-yard labor remains suspect but for a different reason than the v1.5 spec listed. OMN 1B4B funds 44 of 68 availabilities; CE-928 is the $2.08B private-contract slice; the residual $9.5B (non-CE-928 portion of 1B4B) is a mix of NWCF public-yard customer orders, material, civilian labor, travel, and facility support -- not purely public-yard labor. The direct NWCF sourcing research (v1.5 Priority 1) remains the right fix.
3. **The v1.5 "OPN 35% diagnostic" framing softens modestly.** The OMN 1B4B OP-5 exhibit pp 1-3 already documents the OMN / OPN co-funding of availabilities. A careful budget analyst reading the exhibit would see the OPN share. The awards-first advantage is real but narrower than the v1.5 spec claimed -- it is the PSC / vendor / hull tagging advantage, not "discovering OPN funds availabilities."

### Framing that still holds

- Awards data tags every transaction with customer-assigned PSC, vendor, vessel, hull class, and period. Budget books do not.
- Only awards data isolates the contractor-addressable slice cleanly -- NWCF public-yard labor is on the budget side but not FPDS-visible.
- The $2.4B OPN BA-01 Line 1000 money, if it does flow through PSC 1905 as hypothesized in Section 6, is itself evidence that even an experienced budget analyst would struggle to size MRO from budget books alone without cross-referencing to awards data for PSC-level work-type classification.

## 8. Primary sources reference

| Source | Location | What it establishes |
|---|---|---|
| OMN Vol 1 OP-5 1B4B pp 1-3 | `sources/OMN_Book.txt` lines 5326-5400 | OMN and OPN co-fund availabilities; FY24 split 44 / 24 of 68 total |
| OMN Vol 1 OP-5 1B4B pp 4+ | `sources/OMN_Book.txt` lines 5419+ | 1B4B financial summary; $11.76B FY25 total |
| OMN Cost Element 928 | `sources/OMN_Book.txt` line 1035 | CE-928 Ship Maintenance By Contract = $2.08B FY24 actual |
| OPN P-40 BA-01 BSA-10 LI 1000 | `sources/OPN_BA1_Book.txt` lines 21185-21310 | $2.4B FY26 OPN-funded private-contracted ship maintenance in CPF and FFC; defines every availability type |
| OPN P-40 BA-07 BSA-2 LI 8106 | `sources/OPN_BA5-8_Book.txt` lines 11609-11650 | BA-7 Command Support Equipment = $34M FY26 request; investment equipment, not availability funding |
| Legal basis PL 116-93 | Consolidated Appropriations Act 2020 Division A | Established OPN authority for private-contracted ship maintenance in CPF |
| Legal basis expansion | Consolidated Appropriations Act 2022 Division C | Extended OPN private-contracted ship maintenance to FFC |

## 9. Workbook reference

| File | Purpose |
|---|---|
| `data_pull/output/usaspending/approp_rollup_imputed.json` | Coverage: direct $3.645B + imputed $3.761B = $7.406B universe (49 / 51 split) |
| `data_pull/output/usaspending/approp_opn_pa_split.json` | OPN-only drill by Program Activity code: PA 0007 $1.59B (62%), PA 0008 $825M (32%), PA 0001 $65M (2.5%) |
| `data_pull/classify_opn_pa_split.py` | Maps PA 0001 -> BA-1, PA 0007 -> BA-7, PA 0008 -> BA-8. Verified against Treasury File C program_activity_name fields which match labels exactly. |
