---
title: Prime shipbuilders and major suppliers
---

# Prime shipbuilders and major suppliers

U.S. nuclear submarine construction is concentrated on a small group of firms. The contractual prime of record on every Virginia-class (SSN-774) and Columbia-class (SSBN-826) new-construction contract is **General Dynamics Electric Boat**. A second yard, **HII Newport News Shipbuilding**, participates as a team partner with a publicly described workload share but does not appear as a prime in federal procurement data for submarine construction. A third group of firms holds *separate* prime contracts with the Navy for major equipment that the government ships to the GDEB yard for installation; these include the naval reactor plant (Bechtel Plant Machinery), the Trident II strategic weapon system (Lockheed Martin), and elements of the combat system (Lockheed Martin and Northrop Grumman). The remainder of the article uses "prime" for the first group, "team partner" for the second, and "GFE prime" for the third.

## General Dynamics Electric Boat (GDEB)

**General Dynamics Electric Boat** is a wholly-owned subsidiary of General Dynamics Corporation, headquartered in Groton, Connecticut, with a major fabrication and outfitting facility at Quonset Point, Rhode Island. GDEB is the **lead yard for Columbia** and the **prime of record on all Virginia construction contracts**. The Federal Procurement Data System captures GDEB as `ELECTRIC BOAT CORPORATION` and, on some older records, as `GENERAL DYNAMICS ELECTRIC BOAT CORPORATION`.[^repo-fpds-summary]

A search for `VENDOR_NAME:"ELECTRIC BOAT"` against the Navy contracting-agency filter `CONTRACTING_AGENCY_ID:"1700"` over the FY2018–FY2026 signed-date window returns approximately 3,000 records across 166 unique PIIDs (the record count is capped at the pull's 300-page pagination limit; the true record count is approximately 7,520).[^repo-fpds-summary] The top vendor entry in the latest-modification view of that pull is `ELECTRIC BOAT CORPORATION` with approximately $57.9 billion of cumulative `totalObligatedAmount` aggregated across the 166 PIIDs. (This figure is the cumulative-method aggregate at the latest in-window modification of each PIID and is not directly comparable to annual obligation flow; see the cumulative-versus-window discussion in [Terminology and scope](01-terminology-and-scope.md#cumulative-versus-window-dollars).)

GDEB's major active construction PIIDs are:

- **`N0002417C2100`** — Virginia Block V master vehicle, extending into Block VI; cumulative obligated approximately $34.94 billion against a $40.78 billion ceiling.[^repo-sam-prior]
- **`N0002417C2117`** — Columbia Build I (SSBN 826 USS *District of Columbia*) + Build II (SSBN 827 USS *Wisconsin*); cumulative obligated approximately $24.21–$30.83 billion (climbing rapidly) against a $42.18 billion ceiling.[^repo-sam-prior]
- **`N0002412C2115`** — Virginia Block IV multi-year procurement; cumulative obligated approximately $19.90 billion, largely closed out.[^repo-sam-prior]
- **`N0002424C2110`** — Virginia Block VI Long Lead Time Material; cumulative obligated approximately $4.96 billion (fully window-native).[^repo-sam-prior]

A complete PIID inventory is given in [Procurement and prime contracts](03-procurement-and-contracts.md).

## HII Newport News Shipbuilding (HII-NNS)

**HII Newport News Shipbuilding** is the Newport News, Virginia shipyard of Huntington Ingalls Industries. HII-NNS is the U.S. Navy's prime contractor for nuclear-powered aircraft carrier construction and refueling, and a team partner on Virginia and Columbia submarine construction. Public reporting describes the submarine workload split as approximately **50 percent on Virginia** and approximately **22 percent on Columbia**, with GDEB taking the remainder and serving as the lead yard.[^repo-readme]

As a structural pattern, this team-build work flows through the GDEB prime contracts rather than appearing as separate HII-NNS prime contracts. A search for `VENDOR_NAME:"NEWPORT NEWS SHIPBUILDING"` and `VENDOR_NAME:"HUNTINGTON INGALLS INCORPORATED"` against the Navy filter over FY2018–FY2026 returns approximately 5,731 records across 1,516 unique PIIDs, but those records are dominated by aircraft-carrier construction, refueling and complex overhaul (RCOH), and surface-combatant work — not submarine work.[^repo-fpds-summary] In the parsed annual roll-up, the HII-NNS line shows small negative obligations in most years (de-obligations on carrier contracts that net out small new flows), indicating that submarine prime work, as captured by FPDS vendor-of-record, is effectively zero on the HII-NNS line:[^repo-fpds-annual]

| Fiscal year | HII-NNS this-mod obligated ($M) | PIID count |
|---|---:|---:|
| 2018 | -4.05 | 33 |
| 2019 | -3.98 | 26 |
| 2020 | -6.83 | 28 |
| 2021 | -1.54 | 15 |
| 2022 | -0.64 | 14 |
| 2023 | 0.00 | 3 |
| 2024 | -1.20 | 23 |
| 2025 | -0.02 | 8 |
| 2026 | 0.00 | 2 |

Some HII-NNS submarine work is visible as a first-tier subaward on the GDEB Virginia Block V/VI master at the recipient name `HUNTINGTON INGALLS INC` ($98.09 million cumulative across the FY16–FY25 window), but the reported amount is far smaller than the ~50 percent workload share would imply.[^repo-subaward-top] Separately, public NAVSEA contract announcements have at times described specific Virginia and Columbia contract modifications as awarded to **both** GDEB and HII-NNS — most prominently, the April 2025 NAVSEA announcement of modifications for FY24 Virginia-class construction, shipyard productivity investments, and nuclear-powered-vessel workforce support, publicly named at approximately $12.4 billion for GDEB and approximately $1.3 billion for HII-NNS. The April 2025 modification does not appear as an HII-NNS-vendor-of-record record in this article's FPDS pull (the corresponding FPDS records on the GDEB master vehicle list vendor-of-record as `ELECTRIC BOAT CORPORATION`), but a reader should be aware that public press-release language and FPDS vendor-of-record language can diverge. The structural visibility gap and the role of Northrop Grumman as a possible HII-NNS routing channel are discussed in [Government-furnished equipment and the team-build pattern](05-gfe-and-team-build.md).

## Bechtel Plant Machinery, Inc. (BPMI)

**Bechtel Plant Machinery, Inc.** is the Naval Reactors prime contractor for the naval nuclear reactor plant. BPMI operates facilities at Monroeville, Pennsylvania, and Schenectady, New York, and reports to the Naval Sea Systems Command Code 08 (Naval Reactors) program office. BPMI ships reactor plant components to GDEB for installation in the hull; from the SCN perspective, BPMI work is government-furnished equipment.[^repo-readme]

A vendor search for `VENDOR_NAME:"BECHTEL PLANT MACHINERY"` against the Navy filter returns a tight result set — approximately 97 records across 19 unique PIIDs — almost all of which are submarine-relevant reactor work.[^repo-fpds-summary] The annual per-modification obligation profile is the most stable in the dataset: approximately **$1.4 billion to $2.2 billion per year of new-money obligation** since FY2018, reflecting the steady cadence of reactor procurement for in-build Virginia hulls and the Columbia program ramp.[^repo-fpds-annual]

| Fiscal year | BPMI this-mod obligated ($M) | PIID count |
|---|---:|---:|
| 2018 | 416.21 | 4 |
| 2019 | 1,912.07 | 6 |
| 2020 | 1,290.84 | 5 |
| 2021 | 2,000.47 | 10 |
| 2022 | 2,119.41 | 5 |
| 2023 | 1,429.55 | 8 |
| 2024 | 2,181.73 | 4 |
| 2025 | 2,145.00 | 10 |
| 2026 | 1,897.45 | 4 |

BPMI's major active PIIDs include `N0002419C2114` (Naval Reactor Components for Columbia, ~$3.38B cumulative), `N0002419C2115` (Columbia Class Industrial Base Increase, ~$3.00B), `N0002424C2114` (FY26 Virginia Class Component Funding, including an unambiguous $928M FY26 obligation mod signed December 2025), and `N0002416C2106` (Naval Reactor Components, ~$2.71B).[^repo-sam-prior]

## Lockheed Martin Corporation

**Lockheed Martin** holds multiple roles in the submarine industrial base:

- **Virginia-class combat systems** — Lockheed Martin Corporation is the prime on `N0002410C6266`, "Virginia Class Combat Systems hardware/software," at approximately $899 million cumulative obligated against a $1.37 billion ceiling.[^repo-sam-prior][^repo-usaspending-summary] This contract reports zero first-tier subawards in USAspending in the reviewed window; the structural-visibility implications are discussed in [Limitations and blind spots](10-limitations-and-blind-spots.md).
- **Trident II D5 / D5LE2 strategic missile system for Columbia** — Lockheed Martin Space holds the FY20, FY21, FY24, and FY25 Trident II D5 Production & Deployed Systems Support contracts (`N0003019C0100`, `N0003020C0100`, `N0003023C0100`, `N0003024C0100`), each at approximately $1.1–1.2 billion cumulative obligated. Trident production is funded outside the SCN appropriation and is treated separately from Columbia hull construction.[^repo-sam-prior]
- **SSBN combat system / fire control sustainment** — `N0002417C6259` (TI18 SSBN Material & Kit Additions) at approximately $1.02 billion cumulative obligated.[^repo-sam-prior]
- **MK-48 MOD 7 heavyweight torpedo guidance and control** — Lockheed Martin Sippican (Marion, Massachusetts) holds the MK-48 MOD 7 G&C Section Production contracts. Torpedo procurement is funded outside the SCN appropriation.[^repo-sam-prior]

A description-filtered search on `VENDOR_NAME:"LOCKHEED MARTIN"` × Virginia / Columbia / Submarine / Trident across the FY18–FY26 window returns 292 records across 34 unique PIIDs.[^repo-fpds-summary]

## Northrop Grumman Corporation

**Northrop Grumman** is a major component supplier on Virginia and Columbia submarines through its Systems Corporation entity. Its publicly identified scope on submarines includes sonar arrays, the AN/BLQ-10 Electronic Warfare suite, and combat-systems hardware that appears as a sub of the GDEB primes.[^repo-readme]

A description-filtered search on `VENDOR_NAME:"NORTHROP GRUMMAN"` × Submarine / Virginia / Columbia / Sonar returns a tight 132 records across 12 unique PIIDs in the FY18–FY26 window.[^repo-fpds-summary] More important than the prime data is Northrop Grumman's appearance as the **second-largest first-tier subaward recipient** across the in-scope submarine prime PIIDs: `NORTHROP GRUMMAN SYSTEMS CORPORATION` shows approximately **$2.21 billion** cumulative across the FY16–FY25 subaward window, concentrated on the GDEB Virginia Block V/VI master (~$1.27 billion) and the GDEB Columbia Build I+II (~$669 million).[^repo-subaward-top][^repo-sam-prior] An unknown portion of this NG-as-sub flow may represent HII-NNS team-build work routed through NG as a flow-through; the data do not distinguish this from genuine NG-direct sonar and combat-systems work.[^repo-lessons-v1] (See [GFE and the team-build pattern](05-gfe-and-team-build.md).)

## Other major suppliers visible in the pull

Eight additional firms appear in the FY18–FY26 vendor sweeps with submarine-relevant prime or subcontract activity:

- **BAE Systems Land & Armaments L.P.** — Forward subassemblies for the Virginia class. Prime on `N0002421C4106` (SSN 812 Forward Subassembly, ~$85M cumulative). Also a top-six first-tier subaward recipient at approximately $355 million on the Virginia Block V/VI master.[^repo-sam-prior][^repo-subaward-top]
- **L3Harris Technologies** — Type-18 / Type-M1 photonic masts (the non-penetrating replacement for traditional periscopes on Virginia). The Kollmorgen photonic-mast business is now part of L3Harris Maritime Services. Direct L3Harris primes against the Navy submarine filter are limited (approximately 44 records / 13 PIIDs); most of the photonic-mast volume is captured inside the GDEB Virginia prime as L3 Technologies subaward records of ~$6–9 million per contract.[^repo-fpds-summary][^repo-sam-prior]
- **Curtiss-Wright Corporation** — Nuclear pumps, valves, motors, and stators for both Virginia and Columbia. Top-three first-tier subaward recipient at approximately $515 million combined across CW Electro-Mechanical and CW Flow Control entities.[^repo-subaward-top] A `VENDOR_NAME:"CURTISS-WRIGHT"` Navy search returns approximately 2,490 records / 991 unique PIIDs, but the result set is **not** description-filtered to submarine work and over-counts non-submarine Curtiss-Wright Navy activity; the column should be treated as an upper bound until further filtered.[^repo-fpds-summary]
- **Rolls-Royce North America** — Submarine main engine and rotor components. Prime on `N0002421C4111` (Virginia Class Submarine Rotor, ~$29M cumulative, recipient Bird-Johnson Propeller Company LLC). A Rolls-Royce Navy vendor search returns approximately 2,980 records / 1,391 PIIDs across the window, but this includes the firm's much larger aircraft-engine business and should be treated as a non-submarine upper bound.[^repo-fpds-summary][^repo-sam-prior]
- **DRS Naval Power Systems Inc.** (a Leonardo DRS subsidiary) — Switchboards and power distribution. Fourth-largest first-tier subaward recipient at approximately $477 million combined across DRS Naval Power Systems and DRS Naval Power Systems Inc legal entities, concentrated on the Columbia program.[^repo-subaward-top]
- **BWXT Nuclear Operations Group, Inc.** (BWX Technologies subsidiary) — Reactor cores, fuel modules, and pressure vessels. Seventh-largest first-tier subaward recipient at approximately $290 million combined, primarily under the Bechtel reactor-component primes.[^repo-subaward-top]
- **Scot Forge Company** — Large structural forgings (hull rings, shafts). Fifth-largest first-tier subaward recipient at approximately $355 million across the FY16–FY25 window.[^repo-subaward-top]
- **DC Fabricators, Inc.** — Hull fabrication. Eighth-largest first-tier subaward recipient at approximately $255 million.[^repo-subaward-top]

## Foreign partners visible in the subaward data

Two foreign firms appear in the top-12 first-tier subaward list, both on Columbia:

- **Babcock Marine (Rosyth) Limited** (United Kingdom) — Approximately $240 million cumulative, described in prior analysis as the UK strategic-deterrent partner providing propulsion components and Columbia design support.[^repo-subaward-top][^repo-sam-prior]
- **APCO Technologies SA** (Switzerland) — Approximately $202 million cumulative, described as supplying launch-tube structural components for Columbia.[^repo-subaward-top][^repo-sam-prior]

These foreign-partner records are visible in the GDEB Columbia subaward tree but do not represent prime federal contracts and are not part of the United Kingdom Astute / Dreadnought or AUKUS programs covered elsewhere.

## BlueForge Alliance

**BlueForge Alliance** is a non-profit consortium based in College Station, Texas, that operates as the **Submarine Industrial Base (SIB)** workforce, supplier-development, and capacity-expansion pass-through funded directly out of the GDEB Columbia prime contract. BlueForge appears in the FY16–FY25 subaward data as the single largest first-tier recipient at **$4.21 billion** cumulative across just **7 reported subaward actions** on `N0002417C2117`.[^repo-subaward-top][^repo-sam-prior]

The $4.21 billion does not represent a single firm performing $4.21 billion of work. It is the consortium's contractual receipt, which BlueForge then distributes to a wide tail of small and mid-tier suppliers, training programs, welding-workforce development organizations, and capacity-build projects. The Maritime Industrial Base ramp is treated separately in [Maritime Industrial Base and BlueForge Alliance](07-maritime-industrial-base.md).

## Sources and known query limitations

This chapter draws on three repository data extracts:

- The FPDS pull summary (`fpds_raw/_summary.json`) for per-query record counts and unique PIID counts.[^repo-fpds-summary]
- The parsed FPDS annual roll-up CSV (`extracted/fpds_annual_by_prime.csv`) for per-FY per-vendor-group obligation history.[^repo-fpds-annual]
- The top-200 subaward recipients CSV (`extracted/subaward_top_recipients.csv`) for cumulative subaward exposure by recipient.[^repo-subaward-top]

Two known query limitations affect this chapter:

1. The GDEB FPDS pull is **capped at 300 pages (~3,000 records)** against an estimated true count of approximately 7,520 records. The top-vendor cumulative figure is therefore an undercount of GDEB's full prime activity, though the in-window per-modification annual figures derived from this dataset are not affected by the cap because they aggregate at the modification level rather than the latest-mod level.[^repo-fpds-summary]
2. The Curtiss-Wright, Rolls-Royce, and BlueForge vendor sweeps were **not description-filtered to submarine work** in the pull. The resulting record counts (2,490 / 2,980 / 3,901 records respectively) include non-submarine Navy activity (Curtiss-Wright Navy nuclear work generally, Rolls-Royce Navy aircraft engines, and substring matches on unrelated "Blue *" vendors). The annual obligation columns for these vendor groups should be treated as upper bounds, not as net submarine exposure.[^repo-fpds-summary]

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-fpds-summary]: submarine_outsourced_work, "fpds_raw/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^repo-usaspending-summary]: submarine_outsourced_work, "usaspending_subawards/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).
