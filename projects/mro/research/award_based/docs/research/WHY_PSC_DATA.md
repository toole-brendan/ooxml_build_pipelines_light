# Why PSC-Coded Contract Data, Not Budget Exhibits

**Purpose:** consolidated argument for why this workbook sizes the U.S. Navy + U.S. Coast Guard ship MRO market from PSC-coded federal contract awards (FPDS / USAspending) rather than from Navy / USCG budget justification books (P-1 / R-1 / SCN exhibits).

This file pulls together the case previously spread across `methodology.md` §1, `OBJECTIVE.md` "Why Awards Data Only", and `restructuring/restructure_progress.md` Phases 5-7 (the v1.x reconciliation attempt that motivated the shift).

---

## TL;DR

Budget exhibits are a **plan**: annual authority, vessel-type granularity, no contractor detail. PSC-coded contract data is the **actuals**: per-hull, per-vendor, per-PSC obligations at the modification level. For a market-sizing / investor-facing model, the actuals are the right unit -- they describe the commercially addressable slice a contractor or investor can actually compete for. Budget data is useful as a cross-check layer but cannot carry the model on its own.

---

## Part 1 - What was tried and why it didn't work (v1.x)

The previous version of this workbook (v1.x) combined two data sources:

- **Top-down:** Navy justification books (P-1 weapons procurement, R-1 RDT&E, SCN shipbuilding & conversion). Annual budget authority, per FY.
- **Bottom-up:** FPDS contract data pulled via keyword search on contract descriptions.

A dedicated `sheets/reconciliation.py` module (89 rows, workbook v1.18) was built to compare the two views. In use, three structural problems surfaced:

### 1. Incommensurable units

Budget authority is **annual** (what Congress authorized for one fiscal year). FPDS obligations in v1.x were pulled as **cumulative lifetime** (every dollar obligated against a contract since award). These are not the same unit.

The reconciliation could only compare **percentage shares**, not dollar values. Example from the v1.18 reconciliation sheet: top-down SCN FY26 authority for the Virginia-class was compared to FPDS cumulative obligations on every active Virginia contract. The ratio was meaningless as a dollar cross-check, so the sheet compared "share of total shipbuilding" on each side instead -- useful as a sanity check, but not as a market size.

### 2. Granularity mismatch

- **Budget data:** classifies at the vessel type level. "Surface Combatants" is one line. "Aircraft Carriers" is one line.
- **Contract data:** classifies at the hull class level. DDG-51 Arleigh Burke, DDG-1000 Zumwalt, CG-47 Ticonderoga are separate lines.

No budget-side per-class split exists. You cannot join the top-down and bottom-up views at the same resolution; one has to be rolled up (losing hull-class detail) or the other has to be inferred (adding estimation error).

The v1.18 Reconciliation sheet documents this explicitly:

> "Budget authority is only available at the vessel type level (e.g., 'Surface Combatants'), not per hull class. The reconciliation shows per-class FPDS detail indented under category-level budget authority."

This works for visual cross-reference but the numbers on each row are answering different questions.

### 3. Keyword-search gaps

The v1.x bottom-up pull used FPDS description keyword matching: 187 queries across 11 vessel classes (32 shared searches + 155 class-specific). Even at that scale, **~25% of contracts were unclassifiable** because FPDS description text is inconsistent -- a Virginia-class contract might say "SSN-774 EB CONSTRUCTION" or "BLOCK V SUBMARINE" or just "NEW CONSTRUCTION SUBMARINE." Keyword search can't catch them all without over-matching.

Additionally, the 25.5% of FPDS MRO data flagged as unclassified had no budget-line equivalent -- you cannot reconcile what you cannot categorize on both sides.

### Why v1.x kept going as long as it did

The reconciliation sheet was useful as a **structure check** (does the bottom-up share roughly mirror the top-down share?) even when the dollar values didn't tie. But it could not size the market. Going from "these shares are plausibly similar" to "the market is $X.XB and looks like Y" required abandoning the reconciliation framing and committing to one side.

---

## Part 2 - The positive case for PSC-coded contract data

### 2.1 What a PSC is, and why it is the right unit

PSC = Product and Service Code. A 4-character code the **contracting officer at the buying command** assigns to every federal contract action. It classifies what the government is buying.

Three properties make PSCs the right unit for market sizing:

1. **Buyer-assigned, not vendor-self-reported.** The code is set by the contracting officer at Navy / USCG / etc. when the contract or modification is issued. Vendors do not assign their own code. This makes PSC the most reliable "what was bought" field in federal contract data -- more reliable than NAICS (vendor-industry code, self-reported at SAM registration and often not updated) and more reliable than free-text description.

2. **Services / Product split is clean and mechanical.** PSCs fall into two families:
   - **Product** (1905 Combat Ships, 1410 Guided Missiles, 10xx Guns) -- delivery of a physical item
   - **Services** (J998 Ship Repair East, H119 QC of Ships, L020 Tech Rep Marine Equip) -- labor / work performed

   MRO is by definition a services activity -- keeping ships operational through overhauls, availabilities, component M&R, installations, inspections, and technical representation. That entire market therefore lives inside the services-PSC universe. In this workbook, 68 specific services PSCs define the ship MRO scope; product PSCs belong on a separate Product Procurement sheet with no cross-contamination of the TAMs.

3. **Granularity per contract is high.** A single FPDS record carries: PIID, recipient name, ultimate parent, CAGE code, per-mod signed date, per-mod obligation amount, PSC, NAICS, DoD acquisition program, contracting office, GFE / GFP flag, UCA status, type of pricing, extent of competition, and ~50 other structured fields. This lets the model cut the TAM by hull program, vessel type, contractor, segment, or contracting office without re-pulling data.

### 2.2 Discovery via structured fields, not keyword search

Awards are discovered by NAICS and PSC -- not by description text. Four collections cover the ship MRO + newbuild core market:

| Collection | Filter | What it captures |
|---|---|---|
| Shipbuilding | NAICS 336611 + Navy | All shipyard work - newbuild, repair, planning yard |
| Combat Electronics | NAICS 334511 + Navy | Radar, sonar, EW, fire control, navigation |
| Ship Repair | PSC J998 / J999 + DoD | Ship repair services coded to non-shipbuilding NAICS |
| Combat Vessels | PSC 1901 / 1904 / 1905 + DoD | Combat vessel product contracts |

These overlap by design -- a DDG construction contract coded NAICS 336611 + PSC 1905 appears in both Shipbuilding and Combat Vessels. Deduplication happens downstream at the modification level (keyed on PIID + mod_number + date_signed), then re-aggregated into per-award records.

This replaces v1.x's 187 keyword searches with a handful of structured queries. The result for Services PSCs in FY2025: **7,243 Navy + 1,450 Coast Guard exploded-by-hull rows, 68 PSCs, $7.07B TAM** after shore / base / FMS / aviation / LLM-flagged exclusions.

### 2.3 FY decomposition - the cumulative-vs-annual fix

v1.x bottom-up was cumulative-lifetime obligations; v2 uses per-modification obligation data from FPDS Atom Feed.

Each FPDS modification carries a **signed date** and a **per-mod obligation amount**. The pull script filters modifications by signed date range (e.g., 2024-10-01 to 2025-09-30 for FY2025), then sums per-mod obligations by PIID to get the FY-specific obligation per contract. This matches the unit of budget authority (annual) without having to pull the cumulative total.

Result for FY2025: 31,025 raw modifications -> 19,417 unique modifications after dedup -> 4,892 awards with positive FY2025 obligations totaling $52.6B across all collections (shipbuilding + combat electronics + ship repair + combat vessels combined, pre-exclusions and pre-services-filter).

### 2.4 Richer metadata per record

FPDS has fields that budget exhibits simply don't have:

- **Contractor identity** - recipient, ultimate parent, CAGE, DUNS / UEI. Budget data stops at the program office.
- **Contracting office** - SUPSHIP, NSWC Philadelphia, SEA 21, FRC, NAVFAC, etc. Relevant for mapping TAM exposure to specific Navy buying commands.
- **Program attribution** - DoD Acquisition Program description (Virginia-class, Ford-class, DDG-51, etc.). Budget lines have program codes but map to hull classes imperfectly.
- **Contract mechanics** - type of pricing, extent competed, UCA status, GFE / GFP flags. These matter for understanding where the market is competitive vs sole-source.
- **Subcontract plans** - links to USAspending subaward data via PIID. Budget exhibits have no concept of the subcontract layer.

This metadata is what powers the Top-15 Contractor, Top-3-per-Segment, and Market Concentration tables in the workbook. None of it is derivable from budget exhibits alone.

---

## Part 3 - External validation

The only public cross-check available for ship MRO revenue is **General Dynamics Marine Systems' 10-K** "Repair and other services" sub-line:

- GD 10-K FY2025 disclosure: **$1,183M** repair and other services revenue
- This workbook's bottom-up GD consolidated Services TAM: **$939M**

Same order of magnitude. The $244M gap is explained by (a) GD's sub-line including non-Navy / non-ship items that our exclusion logic strips, and (b) timing differences (GD 10-K is GD fiscal year; our TAM is federal FY2025). The fact that one publicly-disclosed line ties to within order-of-magnitude is the strongest single validation we have.

The remainder of the $7.07B TAM is **invisible in public filings** because BAE (foreign issuer, no US segment disclosure), Vigor (private), Detyens (private), FDNF yards (private), and specialist primes like Epsilon Systems and S.C.A. Shipping Consultants either do not disclose segment-level Navy repair revenue or are not SEC registrants. This is a value-of-the-workbook framing: the PSC-based approach surfaces a market that public filings hide.

---

## Part 4 - Known scope caveat: the public-yard gap

Committing to PSC-coded contract data means accepting that the TAM is a **private-sector addressable market**, not the full Navy MRO market. Four Navy-owned public shipyards -- Portsmouth (Kittery, ME), Norfolk (Portsmouth, VA), Puget Sound (Bremerton, WA), Pearl Harbor (Honolulu, HI) -- perform a large slice of nuclear MRO labor using federal civil servants paid through the Navy Working Capital Fund (NWCF). That labor does not generate FPDS contract records, so it is invisible to any PSC-based pull.

Documented gap: **~$4-6B per year**, concentrated on CVN and SSN / SSBN depot work. See `METHODOLOGY_CVN_SSN_COVERAGE.md` for the full accounting of what's captured vs missing per platform type.

This is the right trade-off for a market-sizing deck: the private-sector TAM is what a contractor or investor can compete for. The public-yard labor is not commercially addressable. The gap is disclosed up front so no downstream reader mistakes the $7.07B for "total Navy MRO."

Budget data could close this specific gap (NWCF numbers do appear in budget exhibits), which is why the next section notes where budget data is still useful.

---

## Part 5 - Where budget data still earns its keep

Budget exhibits are not useless. They remain the right source for:

- **Forward-looking authority** - FY26 / FY27 / FY28 numbers. FPDS is backward-looking (obligated dollars), budget exhibits are forward-looking (authorized dollars). A deck that projects the market's trajectory wants both.
- **Public-yard labor** - the NWCF gap above. Reintroducing budget data as a validation layer would let the model put a bracketed upper bound on submarine and carrier MRO.
- **Programmatic intent** - budget exhibits carry program-level narrative (what the Navy says it is buying and why). Useful for understanding the "so what" behind an obligation spike on a particular hull class.
- **Reconciliation sanity checks** - the v1.18 approach of comparing structural shares still has value as an error check, even if the dollar values don't tie.

The choice in v2 is that PSC-coded contract data is the **primary** source and budget data is an optional **validation** layer -- not the other way around. The v1.x mistake was treating them as peers.

---

## Summary table

| Question | Budget exhibits | PSC-coded contract data |
|---|---|---|
| Unit | Annual authority, per FY | Per-mod obligation, per contract action |
| Granularity | Vessel type (e.g., "Surface Combatants") | Hull class + vendor + PSC + office |
| Who decides | Navy / Congress at appropriation | Contracting officer at award / mod |
| Vendor visible? | No | Yes (recipient, ultimate parent, CAGE) |
| Forward-looking? | Yes (FY+2 in exhibits) | No (backward-looking actuals) |
| Public-yard labor? | Yes (via NWCF) | No (civil servants don't generate FPDS) |
| MRO segmentation | Coarse (SWBS groups) | Fine (68 services PSCs) |
| Commercially addressable? | Mixed (in-house + contract) | Yes (by definition - it's the contract) |
| Best use | Forward projection, public-yard bracket | Market sizing, contractor landscape |

The workbook commits to the right-hand column as the primary source. Slide 1 of the deck leads with this decision and justifies it in one graphic (the PSC taxonomy tree) plus the GD 10-K external cross-check.

---

## Source references in repo

- `methodology.md` §1 "Why Awards Data" - original short-form argument
- `OBJECTIVE.md` "Why Awards Data Only" - condensed version of the same
- `restructuring/restructure_progress.md` Phases 5-7 - historical detail on the v1.x reconciliation attempt and what broke
- `METHODOLOGY_CVN_SSN_COVERAGE.md` - the public-yard gap disclosed here, quantified by platform
- `EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md` - the exclusion logic that pares the raw PSC pull down to ship-MRO-only
- `sheets/services.py` MRO_PSCS list - the 68 services PSCs that define the ship MRO scope
