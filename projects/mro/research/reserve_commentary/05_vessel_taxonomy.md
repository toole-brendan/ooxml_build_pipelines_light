# Slide 05 — U.S. Navy & Coast Guard Vessel Taxonomy (module: `vessel_taxonomy.py`)

> Breadcrumb: TAM › Vessel Taxonomy · table transcribed from `_chart_xml/slide05_table.xml`

## On-slide claims (verbatim)

- **Title:** "U.S. Navy and Coast Guard Vessel Taxonomy."
- **Takeaway (module):** "MRO TAM scope covers every SECNAV and USCG hull category."
- **MSC note (speech bubble):** "Military Sealift Command (MSC) vessels sit across Combatant
  Ships and Auxiliary Ships."
- **Navy taxonomy** (defns IAW SECNAVINST 5030.8D, 28 Jun 2022): Combatant Ships (Warships:
  CVN, CG/DDG/FFG/LCS, SSN/SSBN/SSGN, LHA/LHD/LPD/LSD; Other Combatants: MCM, AO/AOE/AOL/AKE,
  LCC, AS, AGOS, ARS/ATF/ATS, EPF/ESB/ESD/LSM, …), Auxiliary Ships, Combatant Crafts
  (LCAC/LCU, patrol boats, special-warfare craft, USVs, UUVs), Unmanned Maritime Platforms,
  Support Crafts.
- **USCG taxonomy:** Cutters (commissioned vessels ≥65′ with crew accommodations — WAGB, WMSL,
  WHEC, WMEC, WMSM, WPC, WPB, WLB, WLM, …) and Boats (<65′, no permanent crew — response
  boats, ATON boats, cutter boats, special-purpose craft).
- **Footer source:** "SECNAVINST 5030.8D (28 Jun 2022); Coast Guard Cutter Fleet; Boats of the
  United States Coast Guard (2024)."

## Claim-by-claim sourcing

| Claim | Source |
|---|---|
| Navy vessel classes & definitions | **SECNAVINST 5030.8D (28 Jun 2022)** — the authoritative Navy ship/craft classification instruction (deck footer) |
| USCG cutter & boat classes | **USCG "Coast Guard Cutter Fleet"** + **"Boats of the United States Coast Guard (2024)"** (deck footer) |
| "covers every SECNAV + USCG hull category" | Scope assertion — the MRO TAM filter is applied across all categories; `model_services.py` §1–§3 cross-tab Navy+USCG by vessel type / hull program |
| MSC straddles Combatant + Auxiliary | MSC fleet disposition; load-bearing for the Marauder comp-set (Tier 1 = MSC auxiliaries), slide 12 |

- Vessel-type ↔ hull-program mapping logic is documented in
  `research/award_based/docs/methodology/METHODOLOGY_VESSEL_TYPE_VS_HULL_PROGRAM.md` (how FPDS
  awards are attributed to a vessel **type** vs a specific **hull program** — the basis for the
  slide 07 / 12 / 13 cross-tabs).

## Reserve facts (could be added)

- **USCG active-cutter counts** (`research/award_based/docs/USCG_Active_Cutters.csv`, ~186+
  cutters): National Security Cutters (WMSL) **12** (Legend-class, 418′); Offshore Patrol
  Cutters (WMSM) **5** (Heritage-class, 360′); Medium Endurance Cutters (WMEC) **13**
  (Famous-class, 270′); Fast Response Cutters (WPC) **87** (Sentinel-class, 154′); Seagoing
  Buoy Tenders (WLB) **16** (Juniper-class, 225′); icebreakers **2** (Polar/Healy). Useful to
  show that only **WPC and WLB** carry material FY2025 MRO spend (slide 12, $43M).
- The taxonomy is a **scope** exhibit: it establishes that no hull category is excluded *by
  definition*; whether a category shows MRO dollars is an FPDS-data question answered on
  slides 06–07.
- The MSC straddle matters: the Marauder-comparable hulls (T-AKE, T-AO, T-EPF, ESB) are
  MSC-operated and book scheduled availabilities under depot PSCs **J998/J999** at MSRA yards —
  the through-line to slides 12–14.

## Quotable stats & attributions

- "Navy vessel classes defined IAW **SECNAVINST 5030.8D (28 Jun 2022)**." (deck footer)
- "USCG operates ~186 active cutters; only **Fast Response Cutters (WPC, 87 hulls)** and
  **Seagoing Buoy Tenders (WLB, 16 hulls)** carry material FY2025 MRO spend." (`USCG_Active_Cutters.csv`
  + slide 12)
- "MSC vessels sit across both Combatant and Auxiliary categories." (deck, slide 05)

## Source line — ready to use

> Sources: (1) SECNAVINST 5030.8D (28 Jun 2022); (2) U.S. Coast Guard Cutter Fleet; (3) Boats of the United States Coast Guard (2024)

## Caveats / confidence / staleness flags

- **Confidence: high** — this is a definitional/reference exhibit drawn from a current Navy
  instruction and USCG fleet references; **no dollar claims**, so essentially no staleness risk.
- The only quantitative reserve content (USCG cutter counts) comes from the static
  `USCG_Active_Cutters.csv` reference, not the live FPDS pull — treat as fleet-inventory context.
</content>
