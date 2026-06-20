# J998 / J999 - Navy Non-Nuclear Ship Repair: Research Brief

**Scope.** FY2025 USAspending awards filtered to PSC J998 and J999. Deduped canonical totals: 2,861 awards / 9,231 mods / $5.01B FY25 obligation. Source: `data_pull/output/fpds/j998_j999_awards.json`.

## 1. What these two PSCs actually mean

Product Service Code J998 and J999 are the Navy's non-nuclear ship repair buckets, split by geography along the 108th meridian:

- **J998 - Non-Nuclear Ship Repair (East).** "Ship repair including overhauls and conversions performed on non-nuclear propelled and nonpropelled ships east of the 108th meridian."
- **J999 - Non-Nuclear Ship Repair (West).** Same scope, west of the 108th meridian.

The 108th runs roughly through Denver / Albuquerque, so in practice J998 captures Atlantic Fleet + Gulf + FDNF Europe/Bahrain, and J999 captures Pacific Fleet + FDNF Japan/Guam/Korea/Singapore. Our data confirms this cleanly:

| PSC | Top recipient states (pop_state) |
|---|---|
| J998 | VA $1,118M, SC $229M, FL $193M, AL $73M, ME $26M |
| J999 | CA $1,554M, WA $433M, OR $285M, HI $153M, GU $74M, AK $23M |

Nothing *nuclear* rolls up here. CVN reactor-plant work, SSN/SSBN hull work, RCOHs - those sit under **PSC J995 (Nuclear Ship Repair)**, which is why SSN/SSBN obligations are nearly absent from this extract (Submarines $12M, all auxiliary/peripheral). CVN dollars that do show up here ($203M) are the non-nuclear portions of PIAs/CIAs/DPIAs - flight deck, catapult, hull coatings, HVAC, elevators - not reactor-plant work.

NAICS is 99% 336611 (Ship Building and Repairing). Small slivers in 333618 (engines), 488390 (transportation support), 541614 (logistics consulting).

## 2. Who buys it

Ship repair work under J998/J999 is purchased almost exclusively by the Naval Sea Systems Command (NAVSEA) network of **Regional Maintenance Centers (RMCs)**, coordinated by **Commander, Navy Regional Maintenance Center (CNRMC)** headquartered in Washington DC / Norfolk:

| Contracting office | FY25 $ | Role |
|---|---|---|
| Southwest RMC (SWRMC), San Diego | $1,584M | Pacific Fleet surface combatants + amphibs, LCS homeported San Diego |
| Mid-Atlantic RMC (MARMC), Norfolk | $1,022M | Atlantic Fleet surface combatants + amphibs |
| MSC HQ Norfolk (Military Sealift Command) | $520M | MSC non-commissioned ships (T-AO, T-AKE, T-AH, T-ARS, T-EPF) |
| Puget Sound Naval Shipyard IMF | $424M | Pacific Northwest CVN and surface ship work; also NW RMC partner |
| NAVSUP Yokosuka | $345M | Japan Regional MC (SRF-JRMC) - FDNF ships forward-deployed Japan |
| Southeast RMC (SERMC), Mayport | $182M | Mayport-based destroyers + LCS; Mayport barges |
| NAVSUP Sigonella/Naples | $127M | FDRMC (Naples) detachment - Europe/Rota FDNF |
| Pearl Harbor Naval Shipyard IMF | $125M | Hawaii RMC partner |
| NAVSEA HQ | $92M | Strategic-level IDIQ awards |
| SFLC Procurement Branch 1 & 2 | $143M | Coast Guard - USCG Surface Forces Logistics Center (the CG-only slice, ~$150M of the $5B total) |

The RMC is not primarily the shipyard - it is the *program office* that plans, contracts, oversees, and test-accepts the work. Actual hands-on labor is done by either a navy-owned **Intermediate Maintenance Facility (IMF)** co-located with a shipyard, or by a **private-sector contractor** under a contract awarded by the RMC. J998/J999 is where the private-sector contract flow lives.

## 3. Who sells it - the shipyard ecosystem

Four-tier market. FY25 J998/J999 totals:

**Tier 1 - CONUS public-yard complex private repair primes (big-ticket DSRAs / SRAs / PIAs):**
- BAE Systems Ship Repair (San Diego $673M + Norfolk $257M + Jacksonville $114M = $1.04B combined) - BAE is structurally the biggest private repair prime
- General Dynamics NASSCO ($391M) - ship construction yard in San Diego that also wins repair availabilities
- Huntington Ingalls ($98M direct + Metro Machine $479M / Marine Hydraulics Intl $168M - both HII subsidiaries - so HII consolidated is ~$745M)
- Vigor Marine ($448M) - Portland/Seattle/Alaska; Titan Acquisition-owned
- Continental Maritime of San Diego ($162M) - GD-owned
- Detyens Shipyards, Charleston SC ($208M) - independent; dominant J998 for MSC hulls

**Tier 2 - regional / mid-market private repair:**
- East Coast Repair & Fabrication, Norfolk ($125M)
- Colonna's Shipyard, Norfolk ($89M)
- Alabama Shipyard ($71M)
- Pacific Shipyards International, Honolulu ($119M)
- Bay Ship & Yacht ($36M)
- Bayonne Drydock ($29M)
- Tecnico Corp ($26M)

**Tier 3 - specialized trades / technical services (not shipyards):**
- Epsilon Systems Solutions ($110M / 97 awards) - planning, engineering, and management support (third-party planner under MAC-MO; see below)
- Amentum Services ($85M) - technical/engineering support
- Southcoast Welding & Manufacturing ($60M / 51 awards)
- MAN Energy Solutions ($25M) - diesel engine OEM support

**Tier 4 - Forward-Deployed Naval Forces (FDNF) / foreign yards under MSRA:**
- Sumitomo Heavy Industries, Japan ($52M / 90 awards - FDNF Yokosuka)
- Navantia, Rota Spain ($75M)
- Hanwha Ocean, Korea ($71M)
- UniThai Shipyard, Thailand ($57M)
- Cabras Marine, Guam ($58M)
- Brodogradiliste Viktor Lenac, Croatia ($28M)
- Seatrium (ex-Sembcorp), Singapore ($27M)
- Yokohama Engineering Works, Japan ($31M)

Total offshore / FDNF-coded foreign shipyard prime $ is ~$340M. This is the work that foreign yards can bid on because they hold a **Master Ship Repair Agreement (MSRA)** with NAVSEA - e.g. `N4034524G0007 MSRA WITH HANWHA OCEAN` and `N4034524G0002 MSRA ISSUED TO UNITHAI`.

## 4. What the money actually buys - availability types

Navy surface-ship maintenance runs on a scheduled "availability" cycle. Our mod-description scan (grepping all 9,231 mod descriptions per award and tallying by FY25 $):

| Availability keyword | Awards | FY25 $ | What it is |
|---|---|---|---|
| DSRA (Docking Selected Restricted Availability) | 20 | $1,432M | Drydocked availability with full hull work + restricted systems. Typical duration 6-8 months. The single biggest ticket item per occurrence. |
| SRA (Selected Restricted Availability) | 28 | $449M | Pierside availability with selected system repairs + alterations. Typical 4-6 months. |
| CMAV (Continuous Maintenance Availability) | 153 | $277M | Short (2-6 wk) non-docking availability scheduled once per non-deployed quarter. Many mods, smaller $. |
| drydock (keyword, other) | 47 | $356M | Drydock events not explicitly labeled DSRA. |
| DPIA (Docking Planned Incremental Availability) | 2 | $170M | CVN-specific; ~10.5 months; hull/drydock portion of CVN cycle. |
| EDSRA (Extended DSRA) | 1 | $119M | Extended scope DSRA. |
| CNO availability (explicit) | 3 | $135M | Explicit mention of CNO-controlled availability. |
| PIA / CIA | 8 | $87M | CVN Planned Incremental Availability (~6 mo) / Continuous Incremental Availability (~1-1.5 mo). |
| PMAV (Pre-deployment Maintenance Availability) | 21 | $32M | Short pre-deployment tune-up. |
| emergent | 69 | $69M | Unplanned - casualty, damage, readiness failure. |
| voyage repair | 40 | $37M | Repairs completed while the ship is between underway periods. |
| inspection / survey | 36 | $11M | Condition surveys, MPI inspections. |
| (no availability keyword) | 2,451 | $1,995M | Long tail - mostly sub-CMAV tasking: specific system repairs, component overhauls, planning mods, small-value admin mods, option exercises. |

The top of the list - DSRA + SRA + DPIA + PIA/CIA + EDSRA - is what the Navy internally calls **CNO Availabilities** (scheduled by the Chief of Naval Operations). These are the big-dollar, multi-hundred-million-dollar task orders. The long tail is CMAVs, emergent work, and sub-availability task orders.

Nuclear CVN cycle for reference (50-year service life of a CVN): 32 CIAs + 12 PIAs + 4 DPIAs + 1 RCOH. Only the nuclear portion of the RCOH sits under J995; the non-nuclear portion of every other availability type lands in J998/J999.

## 5. Contract-vehicle plumbing - MSRA -> MAC-MO -> task order

Three-layer model:

1. **Master Ship Repair Agreement (MSRA).** Not a contract. An umbrella agreement governed by DFARS 217.71. NAVSEA awards MSRAs to contractors that meet facility + 55%-in-house-execution qualifications. Holding an MSRA makes a yard *eligible* to compete for task orders. Separately there is an **Agreement for Boat Repair (ABR)** for smaller craft. MSRAs are a prerequisite filter, not a funding vehicle.
2. **Multiple Award IDIQ** (umbrella contract). MSRA holders compete for slots on an IDIQ - for example:
   - `N0002422D4402` / `N0002422D4445` / `N0002422D4442` - **CNO AVAILABILITIES COMPLEX SURFACE COMBATANTS IDIQ** (DDG/CG)
   - `N0002422D4408` / `N0002422D4453` - **CNO AVAILABILITIES COMPLEX AMPHIBIOUS SHIPS IDIQ** (LPD/LHA/LHD/LSD)
   - `N0002422D4470` / `N0002422D4461` - **NON-COMPLEX EMERGENT MAINTENANCE + CM + CNO AVAILS IDIQ**
   - `N0002421D4443` / `N0002421D4444` / `N0002418D4327` - **AVAILS, CM, EM, MOD & REPAIR - CONUS**
   - `N0002419D4310` - **CVN PACIFIC NORTHWEST PRIVATE SECTOR MAINTENANCE (PSM)** (Vigor + Puget Sound area; $180M touching)
   - `N0002423D4107` - **PIA/CIA PLANNING/EXECUTION SAN DIEGO CARRIERS** ($98M)
   - `N4034522D8000` - **LCS EMERGENT AND CONTINUOUS MAINTENANCE** ($35M)
   - `N4044623D0001` - **GUAM GENERAL SHIP REPAIR IDIQ** (Cabras, $58M)
   - `N6817121D6003` - **ROTA SURFACE SHIP REPAIR CONTRACT** (Navantia, $75M)
   - Foreign MSRAs: `N4034524G0007` (Hanwha), `N4034524G0002` (UniThai), `N6264921G0002` (Samsung Heavy), `N6264923G0010` (Mitsubishi Heavy FLCY)

   2,390 of 2,861 J998/J999 awards (84%) reference at least one parent IDV - task orders off a larger vehicle rather than standalone contracts.

3. **Task Order (the PIID).** Issued under the IDIQ for a specific ship-and-availability. Example: `N0002425C4411` ($248M) is a task order under the Complex Amphibious IDIQ for USS GREEN BAY (LPD-20) FY25 DSRA, executed by BAE San Diego. The 32 mods on that PIID are option exercises, descope/growth work, administrative changes, J-4 / section B reconciliation, and bilateral incorporations - standard Navy availability lifecycle.

### MAC-MO vs MSMO (strategy transition)

Relevant context for why FY25 data looks the way it does. Until ~2015 the Navy ran surface ship maintenance under the **Multi-Ship Multi-Option (MSMO)** strategy - cost-reimbursement, single-contractor-per-ship-per-homeport, multi-year. GAO (GAO-17-54, 2016) and GAO-20-370 (2020) document the transition to **Multiple Award Contract - Multi Order (MAC-MO)**:
- Firm-fixed-price task orders instead of cost-reimbursement
- Multiple pre-qualified primes compete per availability
- Third-party planners produce the work spec so contractors bid fixed-price against a common baseline (this is why Epsilon Systems shows up with 97 small awards - planning support, not repair labor)

The IDIQs listed above are the MAC-MO vehicles. Epsilon's award count suggests the third-party-planner role is now heavily operationalized.

## 6. Hull mix - what's being repaired

| Hull program | FY25 $ | # awards | Notes |
|---|---|---|---|
| DDG | $1,120M | 453 | Destroyers - largest single class by count and $ |
| LPD | $453M | 243 | San Antonio-class amphibious transport dock |
| T-AO | $307M | 64 | Kaiser/Lewis-class MSC fleet oilers |
| LCS | $291M | 232 | Littoral Combat Ships (SD-homeported via SWRMC IDIQ, plus LCS CM/EM IDIQ) |
| LHA | $217M | 119 | Amphibious assault (America-class + Tarawa remnants) |
| CVN | $203M | 69 | Non-nuclear CVN work - PIA/CIA/DPIA hull/systems portion |
| LHD | $203M | 45 | Wasp-class amphibious assault |
| LSD | $171M | 164 | Whidbey Island / Harpers Ferry-class |
| T-AKE | $136M | 60 | Lewis-and-Clark-class MSC dry cargo |
| AS | $48M | 19 | Submarine tenders (Frank Cable, Emory Land) |
| T-EPF | $44M | 32 | Expeditionary Fast Transport |
| ESB / ESD | $42M | 11 | Expeditionary Sea Base / Dock |
| T-AH | $39M | 17 | Mercy / Comfort hospital ships |
| WPC / WMEC | $49M | 56 | Coast Guard cutters (Sentinel + Famous/Reliance classes) |
| CG | $30M | 48 | Ticonderoga-class cruisers (class nearing decommission) |
| Other + unclassified | $1,850M | 1,236 | See section 7 |

Surface Combatants ($1.45B) + Amphibs ($1.04B) + Combat Logistics ($502M) make up ~60% of the total. Submarines are conspicuously absent (only ~$12M - anything non-nuclear on an SSN is tiny).

## 7. What's still unclassified and why ($1.49B)

The `Awards Data` classifier tags 67% of J998/J999 $ to a specific hull or vessel type; ~$1.49B still lands in "no vessel type" residual. Pattern of where the residual sits:

- $405M at SWRMC and $229M at MARMC - big-dollar IDIQ task orders where the award-level description is an admin-mod stub ("EXERCISE OPTION", "ADMIN MOD TO J-4") and the hull identifier is in the mod description or parent IDV description, not in the award description. The `vessel_explode_v2.py` pipeline catches these for the Services sheet via Tier 0 + IDV-description regex, but the **Awards Data** view is per-PIID and uses only the single award-level description.
- $286M at NAVSUP Yokosuka - FDNF awards where the recipient is a Japanese yard and the description is often bilingual / sparse.
- $212M at Puget Sound IMF - public-yard-coordinated private work; descriptions often refer to work packages rather than named ships.
- $79M at NUWC - Naval Undersea Warfare Center-issued awards to ship repair primes for test-ship / range-support work (e.g., USS PAUL FOSTER at Port Hueneme self-defense test ship - previously flagged).

**The residual is mostly identifiable with human inspection of the per-mod text, which is now in `j998_j999_awards.json` under `all_mod_descriptions`.**

## 8. Starting points for PIID-level research

If you want to walk the data manually, the highest-leverage starting points:

### The big single task orders - each one is an in-depth case study
| PIID | FY25 $ | Recipient | Hull | What it is |
|---|---|---|---|---|
| N0002425C4411 | $248M | BAE San Diego | LPD-20 USS GREEN BAY | FY25 DSRA |
| N0002425C4404 | $200M | NASSCO | LHA-6 USS AMERICA | Availability |
| N0002425C4415 | $173M | BAE San Diego | (unclass) | |
| N4523A25F0302 | $166M | Metro Machine | CVN-76 USS RONALD REAGAN | CVN availability |
| N0002425C4402 | $160M | Vigor Marine | DDG-100 USS KIDD | DSRA/SRA |
| N0002425C4400 | $128M | Metro Machine | (unclass) | |
| N0002425C4412 | $123M | BAE Norfolk | DDG-58 USS LABOON | |
| N0002424C4423 | $121M | BAE San Diego | DDG-97 USS HALSEY | |
| N0002425C4427 | $119M | Metro Machine | DDG-78 USS PORTER | |
| N0002425C4421 | $112M | BAE Jacksonville | DDG-68 USS THE SULLIVANS | |
| N0002425C4431 | $99M | Marine Hydraulics Intl | LPD-21 USS NEW YORK | |
| N0002425C4430 | $97M | BAE Norfolk | LHD-1 USS WASP | |

All 12 of these have a mod ledger in the JSON showing the option structure, growth/descope mods, and dollar phasing - useful for understanding how a single availability's $ ramps from base award through completion.

### The umbrella IDIQs - each one is its own ecosystem
For each of the parent-IDV PIIDs listed in section 5, the full set of task orders written against it is visible by filtering `j998_j999_awards.json` on `parent_idvs` key. That reveals which primes are competing for slots on each IDIQ.

### Cross-cuts worth running
- **Geographic concentration.** Top states + top recipient in each state. Seven shipyards (BAE San Diego, BAE Norfolk, NASSCO, Metro Machine, Vigor, Detyens, Continental Maritime) account for ~55% of total J998/J999 $. High consolidation.
- **FDNF vs CONUS.** Foreign MSRA holders take ~7% of the total. Growth in Indo-Pacific demand (FDNF Yokosuka + Guam + Korean MSRAs) is visible in the number of newer MSRA IDVs dated 2023-2024.
- **Third-party planner penetration.** Epsilon's 97 award count vs its $110M total says third-party planning is now a pervasive support function across many availabilities - a structural MAC-MO feature.
- **Sub-CMAV long tail.** The 2,451 awards with no availability keyword aggregate to ~$2B and represent the high-volume transactional layer of J998/J999 - worth sampling to understand what kinds of small-$ direct buys RMCs do outside the IDIQ structure.

---

## Sources

- [govtribe: PSC J998 - Non-Nuclear Ship Repair (East)](https://govtribe.com/category/psc/j998-non-nuclear-ship-repair-east-ship-repair-including-overhauls-and-conversions-performed-on-non-nuclear-propelled-and-nonpropelled-ships-east-of-the-108th-meridian)
- [govtribe: PSC J999 - Non-Nuclear Ship Repair (West)](https://govtribe.com/category/psc/j999-non-nuclear-ship-repair-west-ship-repair-including-overhauls-and-conversions-performed-on-dot-non-nuclear-propelled-and-nonpropelled-ships-west-of-the-108th-meridian)
- [NAVSEA: Commander, Navy Regional Maintenance Center (CNRMC)](https://www.navsea.navy.mil/Home/RMC/CNRMC/)
- [NAVSEA: CNRMC - MSRA & ABR Application Info](https://www.navsea.navy.mil/Home/RMC/CNRMC/MSR-ABR/)
- [NAVSEA: Southwest Regional Maintenance Center (SWRMC)](https://www.navsea.navy.mil/Home/RMC/SWRMC/)
- [NAVSEA: Southeast Regional Maintenance Center (SERMC)](https://www.navsea.navy.mil/Home/RMC/SERMC/)
- [DFARS Subpart 217.71 - Master Agreement for Repair and Alteration of Vessels](https://www.acquisition.gov/dfars/subpart-217.71-master-agreement-repair-and-alteration-vessels)
- [GAO-17-54: Navy Ship Maintenance - Action Needed to Maximize New Contracting Strategy's Potential Benefits](https://www.gao.gov/assets/gao-17-54.pdf)
- [GAO-20-370: Navy Ship Maintenance - Evaluating Pilot Program Outcomes](https://www.gao.gov/assets/gao-20-370.pdf)
- [RAND: Assessment of Surface Ship Maintenance Requirements (RR-1155)](https://www.rand.org/content/dam/rand/pubs/research_reports/RR1100/RR1155/RAND_RR1155.pdf)
- [RAND: Aircraft Carrier Maintenance Cycles and Their Effects (RB-9316)](https://www.rand.org/pubs/research_briefs/RB9316.html)
- [CBO: The Capacity of the Navy's Shipyards to Maintain Its Submarines](https://www.cbo.gov/publication/57083)
- [NAVSEA: In-Service Aircraft Carriers SNA 2020 briefing](https://www.navsea.navy.mil/Portals/103/Documents/Exhibits/SNA2020/SNA2020-In-Service%20AircraftCarriers-CaptCharlesEhnes.pdf)
- [Hanwha Ocean MSRA certification announcement](https://www.hanwha.com/newsroom/news/press-releases/hanwha-ocean-earns-msra-certification-to-participate-in-us-navys-maintenance-repair-and-overhaul-business.do)
- [USNI News: Navy Regional Maintenance Centers tag](https://news.usni.org/tag/navy-regional-maintenance-centers)
