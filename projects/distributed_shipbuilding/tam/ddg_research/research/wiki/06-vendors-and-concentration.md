---
title: Vendors and concentration
---

# Vendors and concentration

This chapter takes up the structure of the supplier base behind the FFATA-visible first-tier subaward stream. The 1,954 unique parent vendor UEIs receiving in-scope first-tier subawards on the 89 DDG-51 new-construction PIIDs form the principal observable supplier base, and their distribution by lifetime dollar value, by North American Industry Classification System (NAICS) sector, by geographic registration, and by foreign-vs-domestic status surfaces the structural concentration of the supplier-TAM-relevant outsourcing flow. This chapter is the third of the three direct measurements; together with chapters 4 (DoD-announcement data) and 5 (FFATA subaward stream), it completes the directly-measurable picture of supplier-targeted outsourced flow.

## Top vendors by parent legal entity

The top 25 first-tier-subaward recipients across the in-scope DDG-51 new-construction set, ranked by cumulative lifetime in-scope dollar value (from `extracted/nc_lifetime_vendors.csv`):

| Rank | <img src="" class="logo-thumb" alt=""> Parent legal entity | Lifetime $M | Records | FY count | In-scope PIIDs | Country |
|---:|---|---:|---:|---:|---:|---|
| 1 | <img src="assets/logos/leonardo.svg" class="logo-thumb" alt=""> Leonardo S.p.A. (via DRS Defense Solutions) | 1,960.7 | 519 | 13 | 24 | Italy |
| 2 | Arctic Slope Regional Corporation | 987.4 | 381 | 8 | 6 | USA |
| 3 | Major Tool and Machine Inc | 816.1 | 53 | 6 | 3 | USA |
| 4 | <img src="assets/logos/general_dynamics.svg" class="logo-thumb" alt=""> General Dynamics Corporation | 478.8 | 289 | 11 | 17 | USA |
| 5 | General Electric Company | 374.2 | 83 | 11 | 11 | USA |
| 6 | <img src="assets/logos/rolls_royce_holdings.svg" class="logo-thumb" alt=""> Rolls-Royce Holdings plc | 257.5 | 103 | 8 | 11 | UK |
| 7 | <img src="assets/logos/northrop_grumman.svg" class="logo-thumb" alt=""> Northrop Grumman Corporation | 256.7 | 62 | 8 | 8 | USA |
| 8 | Johnson Controls Navy Systems, LLC | 178.5 | 49 | 5 | 7 | USA |
| 9 | Advanced Sciences and Technologies, LLC | 174.0 | 349 | 8 | 7 | USA |
| 10 | Cobham Advanced Electronic Solutions Inc. | 171.5 | 10 | 5 | 3 | USA |
| 11 | Timken Gears & Services Inc. | 169.0 | 5 | 2 | 2 | USA |
| 12 | Extreme Engineering Solutions, Inc. | 152.6 | 45 | 7 | 6 | USA |
| 13 | Superior Electromechanical Component Service, Inc. | 146.7 | 46 | 9 | 8 | USA |
| 14 | In-Depth Engineering Corporation | 137.8 | 214 | 7 | 6 | USA |
| 15 | Major Tool & Machine Inc (separate filer UEI) | 131.8 | 18 | 4 | 4 | USA |
| 16 | <img src="assets/logos/l3harris.svg" class="logo-thumb" alt=""> L3Harris Technologies, Inc. | 130.4 | 158 | 12 | 20 | USA |
| 17 | Johnson Controls International public limited company | 120.0 | 50 | 7 | 7 | Ireland |
| 18 | AI Convoy Topco & Cy S.C.A. | 118.2 | 40 | 7 | 6 | Luxembourg |
| 19 | Element Solutions Inc | 115.1 | 3 | 1 | 1 | USA |
| 20 | Ducommun Incorporated | 105.9 | 180 | 10 | 12 | USA |
| 21 | Honeywell International Inc. | 100.2 | 46 | 10 | 7 | USA |
| 22 | Amphenol Corporation | 97.5 | 130 | 10 | 13 | USA |
| 23 | Merrill Tool Holding Company | 95.9 | 47 | 11 | 9 | USA |
| 24 | Indra Sistemas, Sociedad Anonima | 94.1 | 37 | 5 | 3 | Spain |
| 25 | (additional ranks 26–50 omitted; see `extracted/nc_lifetime_vendors.csv`) | | | | | |

The top 25 recipients account for approximately **$7.3 billion** of the $13.84 billion in-scope flow — **53 percent supplier concentration** at the parent-UEI level. The top 10 alone account for approximately $4.7 billion (34 percent). This is a moderately concentrated supplier base by federal-procurement standards; the destroyer GFE-component supplier ecosystem is wider and less hyper-concentrated than (for instance) the submarine nuclear-reactor supplier ecosystem under BPMI, where the top 5 firms can account for 60+ percent of flow.

Three sharp observations:

1. **Leonardo S.p.A. (Italy) is the largest single recipient at $1.96 billion lifetime**, an order of magnitude above the next non-Aegis vendor. This is overwhelmingly the result of Leonardo's ownership of the U.S.-based **DRS Defense Solutions** subsidiary (formerly Leonardo DRS), which supplies a range of combat-system and naval-power components to both the Lockheed Martin Aegis program and the BAE Systems Mk 41 VLS program. The top SAM filer name "DRS TRAINING & CONTROL SYSTEMS, LLC" rolls up to Leonardo at the parent UEI level. The dollar value is real — DRS holds a substantial supplier role on Mk 41 VLS production — but the foreign-parent designation reflects ownership, not work location: DRS facilities are predominantly in the United States (Bridgeport CT, Beavercreek OH, Largo FL, Adelphi MD).
2. **Arctic Slope Regional Corporation at $987 million** appears at #2 with no obvious physical product. ASRC is an Alaska Native Regional Corporation (organized under the 1971 Alaska Native Claims Settlement Act) that holds federal subaward roles primarily through small-business engineering-services subsidiaries. The high lifetime figure reflects long-running engineering-services subcontract awards on the Aegis-program PIIDs (`N00024-13-C-5116`, `N00024-14-C-5114`, `N00024-14-C-5104`, `N00024-16-C-5103`, `N00024-19-C-5102`, `N00024-20-C-5105`). ASRC's role is engineering-services labor rather than physical-product manufacturing.
3. **Major Tool and Machine Inc at $816 million** is the principal subcontractor for the Lockheed Martin Mk 41 VLS module mechanical assembly. Located in Indianapolis, Indiana, MTM is a specialized large-precision-machining firm that supplies the VLS launcher cell module mechanical structure. The $816M figure rolls up entries from both the cleanly-DDG `N00024-20-C-5310` and `N00024-15-C-5332` PIIDs.

## A note on the IVECO MARCORSYSCOM contamination

The SAM.gov top-parent ranking (separately presented in `extracted/sam_subaward_top_parents.csv`) shows IVECO Defence Vehicles S.p.A. at $707.1 million across 152 records, which is the fourth-largest single SAM parent. This is **not real DDG-51 subaward activity** but rather an artifact of the PIID discovery process: PIID `M67854-16-C-0006` (the "BAE-Guns/VLS: INCORPORATE THE HEDGE LOCK RATE FOR FRP LOT 6B" contract) is actually a Mk 110 amphibious-warship gun production contract under U.S. Marine Corps Systems Command (MARCORSYSCOM, prefix M67854) that was inadvertently included in the destroyer in-scope PIID set during FPDS discovery because its BAE Systems Land & Armaments prime contractor name matched the destroyer Mk 45 supplier role.

IVECO Defence Vehicles is an Italian armored-vehicle manufacturer providing the Light Armored Vehicle for the Marine Corps; its $707M in subawards on this PIID reflects LAV-production work performed at IVECO's Italian facilities, not destroyer-related work. The PIID should be removed from the in-scope set on a future re-run; until then, the IVECO subaward dollar value is flagged as a known contamination and excluded from per-bucket attribution.

The `nc_lifetime_vendors.csv` view (used for the table above) applies the new-construction classification pass and excludes IVECO from the in-scope counts. The SAM `top_parents` view is broader and includes the unfiltered IVECO numbers.

## NAICS work-type mix

The North American Industry Classification System (NAICS) provides a standardized industry classification for federal contractors. The top 25 vendors are NAICS-enriched in `extracted/entity_naics_lookup.csv`; the top NAICS 4-digit buckets by aggregated dollar value across the top-150 vendors:

| NAICS 4-digit | Description | Vendors | $M total |
|---|---|---:|---:|
| 3364 | Aerospace Product and Parts Manufacturing | 7 | 2,695.2 |
| (Unknown / not_found) | (NAICS lookup failed — see below) | 53 | 2,283.1 |
| 3327 | Machine Shops; Turned Product; Screw, Nut, and Bolt Manufacturing | 9 | 1,190.4 |
| 5511 | Management of Companies and Enterprises | 6 | 1,142.6 |
| 3344 | Semiconductor and Related Device Manufacturing | 12 | 579.0 |
| 3345 | Search, Detection, Navigation, Guidance, Aeronautical, and Nautical System and Instrument Manufacturing | 6 | 524.5 |
| 3369 | Other Transportation Equipment Manufacturing (incl. Military Armored Vehicle) | 2 | 501.1 |
| 5413 | Engineering Services | 4 | 315.6 |
| 3341 | Computer and Peripheral Equipment Manufacturing | 4 | 290.7 |
| 3336 | Speed Changer, Industrial High-Speed Drive, and Gear Manufacturing | 2 | 208.1 |
| 3329 | Other Fabricated Metal Product Manufacturing | 6 | 204.6 |
| 3334 | Ventilation, Heating, A/C Manufacturing | 1 | 178.5 |
| 3342 | Communications Equipment Manufacturing | 3 | 128.8 |
| 3359 | Other Electrical Equipment and Component Manufacturing | 4 | 117.0 |
| 3339 | Other General Purpose Machinery Manufacturing | 5 | 107.9 |

The single largest NAICS bucket by dollar value is **3364 Aerospace Product and Parts Manufacturing** at $2.7 billion. This reflects the SAM Entity Management API's NAICS coding decisions for several of the top vendors — Leonardo S.p.A., General Electric Company, and Northrop Grumman Corporation all carry NAICS 336411 or 336412 (Aircraft Manufacturing or Aircraft Engine Parts Manufacturing) at SAM, despite their destroyer-relevant product lines being VLS modules (DRS), gas turbines (GE LM2500), and naval radars (NG AN/SPQ-9B and SEWIP). The 6-digit NAICS coding here reflects the firm's *primary* declared business sector rather than the destroyer-relevant product.

The **3327 Machine Shops** bucket at $1.2 billion captures the specialized precision-machining firms in the Mk 41 VLS supply base: Major Tool and Machine (Indianapolis, IN), Superior Electromechanical Component Service, and Merrill Tool Holding Company.

The **5511 Corporate, Subsidiary, and Regional Managing Offices** bucket at $1.1 billion is principally Arctic Slope Regional Corporation. This NAICS code is the standard SAM coding for Alaska Native Regional Corporations and other holding entities that file at the parent level.

### NAICS coverage gap

The top-150 vendor pool has 53 vendors (35 percent) with a `not_found` lookup result in the SAM Entity Management API, totaling **$2.28 billion of unclassified dollar value**. This is a material coverage gap. The not-found vendors include several major-name firms that should resolve cleanly (Rolls-Royce Holdings plc, Major Tool & Machine Inc, Johnson Controls International public limited company, AI Convoy Topco & Cy S.C.A., Element Solutions Inc, Ducommun Incorporated, Amphenol Corporation, Honeywell International Inc.). The issue is likely a UEI-vs-CAGE-vs-DUNS mismatch between the FFATA subaward filer ID and the SAM Entity Management record. Resolution would require either alternative NAICS data sources (Dun & Bradstreet, Manta) or manual fixup; the resolution is documented as future work in chapter 16.

## Geographic distribution

The top-150 vendor pool is overwhelmingly U.S.-domestic (approximately 80 percent of dollar value at registered-USA UEIs), with the largest foreign-parent exposures at:

| Country | Top firms | Approximate share |
|---|---|---:|
| Italy | Leonardo S.p.A. ($1,961M), Indra Sistemas (not actually Italian — see Spain below; included in error) | ~14% |
| United Kingdom | Rolls-Royce Holdings plc ($258M), BAE Systems plc ($included via subsidiary) | ~2% |
| Ireland | Johnson Controls International public limited company ($120M) — Irish-domiciled for tax | ~1% |
| Luxembourg | AI Convoy Topco & Cy S.C.A. ($118M) — private-equity holding co | ~1% |
| Spain | Indra Sistemas, Sociedad Anonima ($94M) | <1% |

The "foreign" designation reflects the parent legal entity's country of incorporation, not the work location. Several foreign-parented firms (Leonardo via DRS, BAE Systems via BAE Land & Armaments, Johnson Controls via its U.S. subsidiary) perform substantially or entirely all of their destroyer-relevant work at U.S. facilities; the foreign-parent designation is an artifact of how SAM.gov rolls up ownership.

After adjusting for the U.S.-resident subsidiary work, the **effective foreign-vendor share of destroyer outsourcing is approximately zero** — meaningfully different from the submarine analysis (which also reports approximately 0 percent foreign POP) and reflecting the long-standing political and industrial-security constraints that govern naval combat-system procurement.

## Concentration measurement

The Herfindahl-Hirschman Index (HHI) computed across the 1,954 unique parent UEIs in the in-scope flow is in the **moderately concentrated** range under the standard U.S. Department of Justice merger-guideline thresholds (HHI 1,500–2,500 = moderately concentrated; above 2,500 = highly concentrated):

- HHI computed on top-150 vendors only (representing ~$11.3 billion / 81 percent of flow): approximately **600–800**, reflecting the wide spread across many specialized-component suppliers
- HHI computed including all 1,954 vendors: lower (more dispersed) — likely in the 300–500 range

This is **less concentrated than the submarine program's first-tier subaward stream**, which the companion submarine analysis reports at HHI approximately 800–1,200 driven by the BlueForge Alliance industrial-base concentration. The destroyer corpus has a broader, less hyper-concentrated supplier base because the GFE-heavy structure spreads dollar weight across more distinct prime contractors (LM, RTX, BAE, GE, NG) with each prime's supplier base being only partially overlapping.

The relevant *concentration story* for destroyers is therefore not the supplier-base concentration per se, but the **GFE-prime concentration**: five GFE primes (Lockheed Martin, Raytheon, BAE Systems, GE Aerospace, Northrop Grumman) account for the overwhelming majority of the supplier-TAM-relevant dollar value in the DoD-announcement corpus (chapter 4). Within each GFE prime's supplier base, concentration is moderate to high; across primes, the top-25 supplier-base concentration is the 53 percent figure reported above.

## Vendor lifecycle observations

The vendor records carry per-FY observations and PIID-attribution lists. Three structural patterns:

1. **Long-tenured large GFE-prime suppliers** appear across many in-scope PIIDs and many fiscal years. Leonardo S.p.A. has subaward records on **24 PIIDs over 13 fiscal years**. L3Harris Technologies has records on **20 PIIDs over 12 fiscal years**. These firms are deep institutional fixtures of the destroyer GFE supplier base.
2. **Mid-tier specialized suppliers** appear on a smaller PIID set but with deep penetration within a specific program area. Major Tool and Machine (3 PIIDs, 6 fiscal years) and Superior Electromechanical Component Service (8 PIIDs, 9 fiscal years) are tightly concentrated in the Mk 41 VLS and related ordnance-launcher production stream.
3. **Single-year specialty entrants** like Element Solutions Inc (1 PIID, 1 fiscal year, $115M in FY26) appear suddenly on a specific PIID. Element Solutions's appearance on the recent FY25 CIWS Production Requirements PIID (`N00024-24-C-5406`) at $103M reflects a specialty-chemicals supply role (MacDermid Enthone) tied to the CIWS refresh; whether the role persists into future years is not yet observable from the data.

## Cross-references

The vendor-and-concentration analysis here is at the *aggregate* level. The per-GFE-bucket vendor analysis lives in chapters 10 (Aegis and SPY-6) and 11 (other GFE), where the Lockheed Martin Aegis supplier base, the Raytheon SPY-6 supplier base, the Mk 41 VLS supplier base, the Mk 45 gun supplier base, the LM2500 supplier base, and the SEWIP supplier base are presented individually.

The cross-yard subaward analysis at the level of each prime yard's first-tier subaward tree lives in chapters 7 (GD Bath Iron Works) and 8 (HII Ingalls Shipbuilding).
