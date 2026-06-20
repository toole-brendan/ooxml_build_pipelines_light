# USCG Hull and Vessel Classification -- Current State and Issues

---

## What We Did

Added 13 USCG hull program patterns to `classify_awards_v2.py` based on the
vessel taxonomy (WMSL, WPC, WMEC, WAGB, WLB, WLM, WLIC, WLR, WLI, WTGB, WPB)
plus OPC (Heritage-class Offshore Patrol Cutter). Patterns match hull designators
in contract descriptions (e.g., "WMSL", "WPC-1101") and named cutter classes for
NSC (Bertholf, Waesche, Stratton, etc.) and WMEC (Bear, Tampa, Spencer, etc.).

Result: CG classification went from 99.7% unclassified to 56% unclassified by
dollars. 203 of 4,667 CG awards now have a hull program assignment.

---

## Description Field

The `description` field IS pulled from FPDS -- it maps to `descriptionOfContractRequirement`
in the FPDS XML. 100% of CG awards have descriptions populated. This is the latest
modification's description, so it may reflect a funding mod rather than the original
contract scope.

---

## Known False Positives

### 1. CG-47 Ticonderoga matching Coast Guard identifiers

The Navy vessel pattern `CG-47 Ticonderoga` uses regex `cg[\s-]?\d{2}|ticonderoga`.
This falsely matches Coast Guard contracts containing:

- **CG vessel registry numbers**: "CG-35103", "CG45610", "CG45612" -- these are
  Coast Guard hull numbers (different from Navy CG-47 cruiser designators)
- **CG small boat references**: "CG 300 CRANE", "45' RBM" with CG prefix
- **87' USCG PATROL BOAT** descriptions that contain "CG" followed by numbers

Examples of false positives (all are Coast Guard contracts, not Navy cruisers):
- $3.7M: "SCALABLE INTEGRATED NAVIGATION SYSTEM" -- Teledyne FLIR, CG contract
- $1.2M: "KONGSBERG FF3755 JET DRIVE PARTS TO SUPPORT USCG 45' RBM SMALL BOATS"
- $0.4M: "KONGSBERG FF3755S JET DRIVE PARTS TO SUPPORT USCG 45' RB-M SMALL BOATS"
- $0.1M: "LEAD INFUSED INSULATION REPLACEMENT ON CG45612"
- $0.1M: "COMPLETE EXHAUST LAGGING FIT FOR AN 87' USCG PATROL BOAT"
- $0.0M: "CG 300 CRANE ONBOARD" -- crane installation
- $0.0M: "MARINE JET POWER, CG-35103" -- a part number

**Impact**: $5.6M in CG awards falsely classified as CG-47 Ticonderoga.

**Root cause**: The regex `cg[\s-]?\d{2}` is too broad. It was designed for Navy
contracts where "CG-47" or "CG-52" unambiguously means a Ticonderoga-class cruiser.
In Coast Guard contracts, "CG" is the service abbreviation, not a hull type.

**Fix needed**: When `service = "Coast Guard"`, skip the CG-47 pattern entirely.
Or tighten the regex to require "CG-47" through "CG-73" specifically (actual
Ticonderoga hull numbers).

### 2. Columbia (SSBN-826) matching "Sector Columbia River"

The pattern `columbia|ssbn[\s-]?8[2-3]\d` matches the word "columbia" anywhere
in the description. Coast Guard has a "Sector Columbia River" in Portland, OR,
and several contracts reference it:

- $0.0M: "PLUM KIT FOR SECTOR COLUMBIA RIVER COOP"
- $0.0M: "FIRE HYDRANT REPLACE FOR UTILITY/FIRE MAIN AT SECTOR COLUMBIA RIVER"
- $0.0M: "COMPRESSOR REPLACEMENT FOR A HVAC TRANE UNIT AT SECTOR COLUMBIA RIVER"
- $0.0M: "SECTOR COLUMBIA RIVER HVAC COMPRESSOR REPLACEMENT"

**Impact**: 4 CG awards ($50K total) falsely classified as Columbia-class submarine.

**Root cause**: "Columbia" without submarine context (no "class", "SSBN", or hull
number) matches a geographic name.

**Fix needed**: Require "columbia" to appear with "class", "ssbn", or a hull number.
Or exclude matches where "sector" or "river" appears nearby.

### 3. WLI matching WLR contract

The $32M contract "AWARD INLAND BUOY TENDER (WLR) 1801" was classified as WLI
(Inland Buoy Tender) instead of WLR (River Buoy Tender).

**Root cause**: The WLI pattern `wli[\s-]?\d|inland\s+buoy\s+tender` matches
"inland buoy tender" broadly. Both WLI and WLR are types of inland buoy tenders,
but the contract explicitly identifies itself as WLR. The WLI pattern fires first
because the generic "inland buoy tender" phrase appears before checking for the
more specific WLR designator.

**Fix needed**: Make the description regex patterns more specific. Check for
explicit hull designators (WLR, WLI) before falling back to generic type names.
Or reorder patterns so WLR is checked before WLI.

### 4. T-AKE Lewis & Clark false positive

One CG contract ($17K) was classified as T-AKE. The description contains a part
number string "2125405B4500AJ002" which does not obviously contain "AKE" -- this
needs investigation. May be matching on a substring.

**Root cause**: The T-AKE pattern `t[\s-]?ake[\s-]?\d|lewis\s+and\s+clark` --
unclear what matched. Possibly a false regex interaction.

---

## Correct Classifications (Verified)

These classifications look accurate based on description evidence:

| Hull Program | Awards | FY2025 $ | Evidence Quality |
|---|---|---|---|
| OPC | 1 | $707M | Explicit: "OPC-RFV-0002.B" in description |
| NSC | 90 | $15.6M | Strong: Named cutters (Bertholf, Waesche, Midgett, Munro, etc.) + "WMSL" |
| WMEC | 61 | $19.7M | Strong: Named cutters (Bear, Spencer, Reliance, etc.) + "WMEC 270" |
| WAGB | 23 | $15.8M | Strong: "CGC HEALY", "CGC POLAR STAR", explicit icebreaker references |
| WLIC | 2 | $37.4M | Strong: "INLAND CONSTRUCTION TENDER (WLIC)" explicit |
| FRC | 5 | $0.4M | Moderate: "FRC" abbreviation, "FAST RESPONSE CUTTER" |
| WLB | 2 | $40K | Strong: "WLB-225 CGC WALNUT", "WLB-225 CGC ALDER" |
| WPB | 2 | $185K | Moderate: Part numbers with propulsion shaft context |
| WTGB | 1 | $10K | Strong: "WTGB 140" explicit |

---

## Unclassified CG Spend ($1.06B, 56%)

Major unclassified buckets:

- **$127M PSC 1925** (Special Service Vessels): Offshore Service Vessels LLC --
  likely the Polar Security Cutter or similar program. Description doesn't name
  a hull class.
- **$187M PSC J016** (Aircraft Components Maint): Helicopter engine maintenance
  (Safran, Rolls-Royce, Rockwell Collins) -- not vessel-related, correctly unclassified.
- **$71M PSC 1940** (Small Craft): Safe Boats, Inventech -- various small boats
  without specific hull designators.
- **$28M PSC J020** (Ship/Marine Equipment Maint): Generic marine equipment
  maintenance across 572 awards.
- **$21M PSC 2090** (Misc Ship/Marine Equipment): Small parts purchases.

Much of the unclassified spend is legitimately unclassifiable: small parts purchases,
aircraft maintenance (J016), and generic equipment orders that don't reference a
specific cutter.

---

## Fixes To Implement

1. **Service-aware CG-47 pattern**: Skip or tighten the `cg[\s-]?\d{2}` regex
   when classifying Coast Guard awards. Navy CG-47/52/73 hull numbers don't
   appear in CG contracts.

2. **Tighten Columbia pattern**: Require "columbia" + ("class" or "ssbn" or
   hull number). Exclude when "sector" or "river" appears within 20 chars.

3. **Reorder WLR/WLI patterns**: Check for explicit "WLR" designator before
   the generic "inland buoy tender" pattern. WLR is River Buoy Tender, WLI is
   Inland Buoy Tender -- the generic phrase shouldn't default to WLI.

4. **Investigate T-AKE false positive**: Check what substring triggered the match.

5. **Add OPC sub-patterns**: The $127M "special service vessels" contract from
   OSV may be identifiable with additional description or recipient evidence.
   Austal's $707M contract matches via "OPC" in description -- check if other
   OPC contracts use different terminology.
