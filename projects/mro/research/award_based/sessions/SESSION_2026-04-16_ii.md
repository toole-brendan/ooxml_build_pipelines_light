# Session 2026-04-16 (II): Tier 0 Wikipedia Name Lookup, Taxonomy Cleanup, Symmetric PP/Services Layout

## Context

Building on `SESSION_2026-04-16.md`. That session had built the v2 explosion pipeline (per-mod hull regex + parent-IDV enrichment + supergroup fallback), removed aircraft component PSCs (J016/K016/N016), and taken Services classification from ~26% -> ~49% of $ classified. Services residual stood at ~$4.2B out of $8.3B.

Goals this session:

1. Drop remaining non-ship PSCs hiding in Services (aviation engines, flight simulators).
2. Surface USS/USNS/USCGC proper names referenced in FPDS text that the existing regex was missing (e.g., "USS RUSSELL" - regex doesn't know RUSSELL is DDG-59).
3. Build a proper-name-to-hull lookup from canonical sources (Wikipedia), not from model memory.
4. Wire the lookup in as a new Tier 0 in the classification cascade.
5. Apply the same Tier 0 to the Awards Data sheet (which Product Procurement queries) so both sheets benefit from the improved tagging.
6. Include previously-excluded craft / boat categories and add a Vessel Type rollup to Product Procurement so its layout mirrors Services.

## Work Completed

### 1. Dropped remaining aviation PSCs

Reviewed residual contracts by PSC and spotted two aviation buckets:

- **J028 Engines/Turbines** -- $363M, top recipient Rolls-Royce $211M. Mod text: "TO FUND NOV & DEC FLIGHT HOURS", "T56-A-427A ENGINE MODULES" (C-130/E-2 engine), "T700-GE-401C" (helicopter engine). Contracting office: Naval Air Systems Command. Parent IDV: "MAINTENANCE & RELATED SERVICES (CNATRA)" -- Chief of Naval Air Training.
- **J069 Training Aids and Devices** -- $348M. Mod text: "NAVY FLIGHT SIMULATION TRAINING DEVICES", "HELICOPTER TRAINING DEVICES". Contracting office: NAWC Training Systems Div. Parent IDV: FTSS V (Fielded Training Systems Support) -- flight simulators.

Removed both from `MRO_PSCS` in `sheets/services.py`. Same treatment as J016/K016/N016. -$711M from residual.

### 2. Built a residual-PIID dump for manual inspection

`data_pull/extract_unclassified_services.py` -- walks the v2 explosion, collects mods that fall through to residual per PIID, aggregates unique mod descriptions with $ and count. Output JSON grouped by PSC, ranked by total residual $. PSC groups sorted high-$ to low so "where to look first" is obvious.

### 3. USS proper-name regex extractor

`extract_uss_names()` added to `data_pull/classify_awards.py`:

- `USS_NAME_PATTERN` matches `USS|USNS|USCGC|CGC` prefix + 1-4 ALL-CAPS words
- Internal negative lookahead blocks connector words (AND, OR, THE, etc.), FY tags (FY25, FY-24), maintenance acronyms (SRA, DSRA, RCOH, AVAILABILITY), hull-class codes (DDG, CVN), cutter designators (WAGB, WMEC, WMSL), month names, and Navy command abbreviations
- `NAME_STOP_TOKENS` post-filter for trailing noise after the regex captured
- Possessive `'S` stripping in normalization

Wired into `vessel_explode_v2.py` as `_collect_proper_names()` -- scans award description + IDV description + every mod description for the PIID, deduplicates, attaches ` | `-joined list as `proper_names_detected` on every emitted row. New "Proper Names Detected" column on the AwardsByHull sheet.

New output file `data_pull/output/fpds/services_unclassified_proper_names.json`: 805 unique extracted names, covering $1.61B of unclassified $. This was the "what names are referenced in residual text" audit used to size the Tier 0 opportunity and seed the Wikipedia lookup.

### 4. Wikipedia-sourced name-to-hull lookup

`data_pull/proper_names_lookup.py` -- the lookup table the user specifically requested come from an external source (not model memory).

Three prefix-keyed dicts built from Wikipedia WebFetch:

- `USS_LOOKUP` (230 ships) -- `List_of_current_ships_of_the_United_States_Navy`
- `USNS_LOOKUP` (~85 ships) -- `List_of_Military_Sealift_Command_ships`
- `CGC_LOOKUP` (~150 cutters) -- `List_of_United_States_Coast_Guard_cutters`

Each entry maps normalized name to `(class_string, hull_number)` e.g. `'RUSSELL' -> ('DDG-59 Arleigh Burke', 'DDG-59')`.

`match_ship_name()` does:

- **Tier 1** -- longest-prefix match (catches `MESA VERDE SETTLE VARIOUS` -> LPD-19)
- **Tier 2** -- single-token unambiguous last-word match, canonical-only index so typo aliases don't pollute (catches `TRUMAN` -> HARRY S TRUMAN CVN-75)
- Possessive `'S` stripping during normalization
- Noise-tail stripping (`REGULAR`, `MAINT`, `DRYDOCK`, `ENGINE`, etc. -- ~50 tokens) before matching so `KAISER REGULAR` -> KAISER -> HENRY J KAISER
- Abbreviation blocklist (`UNIT`, `ARB`, `BUL`, `PGN`, `RSV`, `BLR`, `OSA`, `INSTALLS`, etc.) -- regex false positives explicitly return no-match
- Typo aliases stored separately so tier-2 last-word index stays canonical:
  - `GERAL R FORD` -> GERALD R FORD (CVN-78)
  - `MAKIND ISLAND` -> MAKIN ISLAND (LHD-8)
  - 6 variants of `KEARSARGE` typos -> LHD-3
  - `IOWA JIMA` -> IWO JIMA (LHD-7, overrides tier-1 match to IOWA SSN-797)
  - `HARRY CLARIBORNE` / `HARY CLAYBOURN` -> HARRY CLAIBORNE (WLM-561)
  - `HOLLHOCK` -> HOLLYHOCK (WLB-214)
  - Etc.

`parse_wiki_class()` derives `(vessel_class, hull_program, supergroup)` from a Wikipedia class string like `DDG-59 Arleigh Burke`, normalizing to the existing workbook taxonomy where applicable (`DDG-59 Arleigh Burke` -> canonical `DDG-51 Arleigh Burke`). SSGN is aliased to SSBN for hull_program rollup.

**Match results**: 578 of 805 names (71.8%) map to a hull, covering **91.6% of unclassified $ touching a proper name** ($1.48B of $1.61B).

Companion script `data_pull/build_proper_names_xlsx.py` emits the 805-row table as Excel with Hull Class + Hull Number populated for matches -- the spreadsheet the user asked for so they could validate / extend manually.

### 5. Wired name lookup as Tier 0 in the v2 explosion

`vessel_explode_v2.classify_mod` cascade is now 6 tiers:

```
Tier 0 -- name_lookup via mod desc    (NEW, Wikipedia)
Tier 0 -- name_lookup via IDV desc    (NEW, Wikipedia)
Tier 1 -- VESSEL_DESC_PATTERNS via mod
Tier 2 -- VESSEL_DESC_PATTERNS via IDV
Tier 3 -- supergroup regex via mod
Tier 4 -- supergroup regex via IDV
```

New `name_hull` kind handled in `_row_from_bucket`: `vessel_class` / `hull_program` / `vessel_supergroup` all derived from `parse_wiki_class`. Per-row `matched_proper_name` + `matched_hull_number` metadata stored for audit.

Two new columns on AwardsByHull sheet: **Matched Ship Name** and **Hull Number**.

Tier 0 contribution: $3.24B Navy + $89M CG classified by name lookup. Most of this recategorizes existing regex hits with better specificity (e.g., rows previously in "DDG-51 Arleigh Burke" bucket now carry the specific hull DDG-59/DDG-95/etc. in Hull Number). Net residual drop: **$437M** -- smaller than Tier-0-classified $ because Tier 0 mostly re-assigns from Tier 1/3 to higher-quality Tier 0, not from residual.

### 6. Applied Tier 0 to Awards Data (feeds Product Procurement)

Awards Data goes through `data_pull/classify_awards.py`, not through the v2 explosion -- so Tier 0 needed wiring there too, otherwise PP wouldn't benefit.

Added Tier 0 to `classify_vessel()` in `classify_awards.py`. Added hull_program + supergroup derivation in `classify_award()`. Added `VESSEL_CLASS_TO_HULL` mapping to the file (was previously sourced from `classify_awards_v2.py`).

**Chain-input gotcha**: the earlier `*_deduped_classified.json` had `hull_program` populated by an old run of `classify_awards_v2.py`, which has an extensive `_CG_CUTTER_NAMES` substring-matcher that `classify_awards.py` doesn't replicate. My first-pass rewrite clobbered those CG classifications, pushing CG newbuild-PSC unclassified from 45.7% to 99%.

Fix: modified `classify_awards.main()` to chain on top of existing `_classified.json` if present. New workflow is:

```
1. classify_awards_v2.py <X>_deduped.json  -- baseline vessel_class + hull_program
2. classify_awards.py <X>_deduped.json     -- reads v2's output, adds Tier 0, preserves hull_program when no new answer
```

The preserve logic: only overwrite `hull_program` if Tier 0 hit OR the new `vessel_class` is in `VESSEL_CLASS_TO_HULL`. Otherwise keep whatever was there.

Also added `CVN-78 Ford` to `VESSEL_CLASS_TO_HULL` -- that label is emitted by `VESSEL_DESC_PATTERNS` but was absent from the mapping, causing 4 Ford-class PIIDs ($2.15B) to silently lose hull_program during the first-pass rewrite.

Three new columns on Awards Data sheet: **Vessel Type**, **Matched Ship Name**, **Hull Number**.

### 7. Removed `in_tam=False` taxonomy exclusions

Per user decision, flipped to `in_tam=True` in `sheets/vessel_taxonomy.py`:

- USN Combatant Crafts (LCAC, LCU, PC, patrol boats, special warfare craft)
- USN Support Crafts (yard craft, barges, tugs -- including the newly added MWT)
- USCG Boats (MLB, response boats, buoy boats, etc.)

MWT (Modular Warping Tug, $13.2M in Navy Services) was unmapped entirely. Added to USN Support Crafts > Harbor Tugs.

Result: TAM_HULLS set expanded 130 -> 183 entries. No hull programs are silently dropped from Services / PP crosstabs anymore.

### 8. Symmetric Vessel Type layout on Product Procurement

Services had gained a Vessel Type crosstab as its top table (combined Navy+CG, rolling up hulls into 15 supergroups per Vessel Taxonomy). PP had only Hull Program tables and no vessel-type rollup.

Parameterized `get_vessel_types(..., source='awards_by_hull' | 'awards')` so the Vessel Type sort source can be picked per sheet (matches the source the SUMIFS actually sums against -- critical for dynamic column ordering).

Rewired `create_newbuild()` layout to mirror Services exactly:

```
1. Vessel Type crosstab (combined Navy + CG, 15 types)
2. Navy by Hull Program (31 hulls)
3. CG by Hull Program (19 hulls)
4. Condensed TAM by Vessel Type (combined)
5. Condensed TAM by Hull Program (Navy + CG)
6. Condensed SAM by Vessel Type (combined)
7. Condensed SAM by Hull Program (Navy + CG)
```

## Files Created

| File | Purpose |
|---|---|
| `data_pull/extract_unclassified_services.py` | Dump residual (unclassified) services PIIDs grouped by PSC, ranked by $ |
| `data_pull/proper_names_lookup.py` | Wikipedia-sourced lookup + matcher + Wiki-class-to-taxonomy parser |
| `data_pull/build_proper_names_xlsx.py` | Emit `services_unclassified_proper_names.xlsx` with Hull Class populated |
| `SESSION_2026-04-17.md` | This file |

## Files Modified

| File | Change |
|---|---|
| `sheets/services.py` | Removed J028 (aviation engines) + J069 (flight simulators) from MRO_PSCS and PSC_DESCRIPTIONS |
| `data_pull/classify_awards.py` | Added `extract_uss_names()` + USS_NAME_PATTERN + NAME_STOP_TOKENS; added `VESSEL_CLASS_TO_HULL` with Ford class; Tier 0 in `classify_vessel`; hull_program + supergroup + matched_name derivation in `classify_award`; chain-input support in `main()` |
| `data_pull/vessel_explode_v2.py` | Added `_collect_proper_names()`, Tier 0 (`name_hull` kind) in `classify_mod`, `matched_name`/`matched_hull` threading through `_row_from_bucket`, per-tier stats |
| `sheets/awards_data.py` | Added Vessel Type, Matched Ship Name, Hull Number columns |
| `sheets/awards_by_hull.py` | Added Proper Names Detected, Matched Ship Name, Hull Number columns |
| `sheets/product_procurement.py` | Added `source=` param to `get_vessel_types`; rewrote `create_newbuild()` layout with Vessel Type table + condensed TAM/SAM by VT |
| `sheets/vessel_taxonomy.py` | Set `in_tam=True` on Combatant Crafts / Support Crafts / Boats; added MWT to Harbor Tugs |

## Data Files Produced

| Path | Contents |
|---|---|
| `data_pull/output/fpds/services_unclassified_piids.json` | Residual PIIDs grouped by PSC, ranked by $ with mod-description context |
| `data_pull/output/fpds/services_unclassified_proper_names.json` | 805 unique USS/USNS/CGC names extracted from residual text with $ / sample PIIDs |
| `data_pull/output/fpds/services_unclassified_proper_names.xlsx` | Excel view of above with Hull Class populated for 578 matched names |
| `data_pull/output/fpds/navy_fy2025_deduped_classified.json` | Re-classified via chained v2 -> v1 |
| `data_pull/output/fpds/cg_fy2025_deduped_classified.json` | Re-classified via chained v2 -> v1 |
| `data_pull/output/fpds/navy_services_awards_by_hull_v2.json` | Re-exploded with Tier 0 |
| `data_pull/output/fpds/cg_services_awards_by_hull_v2.json` | Re-exploded with Tier 0 |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.41.xlsx` | Final workbook |

## Outcomes

Workbook counts before / after:

|  | v2.36 (start of day) | v2.41 (end of day) |
|---|---|---|
| Services: Navy hull programs | 24 | 30 |
| Services: CG hull programs | 7 | 16 |
| Services: Vessel Type table | yes | yes |
| Product Procurement: Navy hull programs | 22 | 31 |
| Product Procurement: CG hull programs | 15 | 19 |
| Product Procurement: Vessel Type table | no | **yes (15 types)** |
| Awards Data columns | 29 | 32 |
| AwardsByHull columns | 36 | 38 |
| Services total classified % | 49.4% | 54.6% |
| Services residual $ | $4.19B | $3.75B |

Qualitative wins beyond the classification rate:

- **Hull-level specificity** on Services: Instead of aggregating to "DDG-51 Arleigh Burke" class, rows now carry the specific hull (DDG-59, DDG-95, etc.) in the `Hull Number` column. Useful for per-ship validation against budget docs.
- **Aviation is out of Services TAM entirely**. J016 + J028 + J069 + K016 + N016 -- all five Aircraft Components / Engines / Training Devices PSCs excluded.
- **Audit trail for Tier 0 matches**: `Matched Ship Name` column lets a reviewer eyeball whether the regex caught the right ship.
- **Full taxonomy coverage**: no hull silently dropped from crosstabs due to `in_tam=False`.
- **Sheet symmetry**: PP and Services now have the same section structure, making side-by-side review possible.

## Potential Next Steps

### Close more Services residual

1. **Manual pass on the unmatched proper names** -- 245 names / $124M in the xlsx without a Hull Class. Bulk is (a) decommissioned ships absent from Wikipedia current-ships list (USS PAUL FOSTER ex-DD-964, USS PHILLADELPHIA, USS NORMANDY ex-CG-60), (b) ambiguous typos that weren't aliased, (c) regex false positives that slipped the blocklist. Worth an hour of manual review to fill in the high-$ rows, then feed back into `proper_names_lookup.py` aliases.

2. **Expand aliases + blocklist iteratively** -- each iteration catches another slice. The three lookup dicts and the alias / blocklist / noise-tail sets are the places to edit.

3. **Shore/base filter for J059** -- top parent IDVs in J059 residual are "GLOBAL SUSTAINMENT OF ATFP SYSTEMS" (CNIC base security), "PUBLIC SAFETY SYSTEMS", "PROJECT 75... USNAVCENT NETWORK TECH REFRESH BAHRAIN". Not ship MRO. SERCO alone is $149M of base infrastructure work. Should be stripped from Services TAM like aviation was, probably by contracting-office filter (NAVFAC / CNIC) rather than by PSC code.

4. **Recipient + geography priors tier** -- the fifth classification tier that SESSION_2026-04-16.md already sketched. Electric Boat + CT/RI -> SSN/SSBN, HII Ingalls + MS -> LPD/LHA/DDG, BIW + ME -> DDG-51, NASSCO + CA -> T-AO/T-AKE, Austal + AL -> LCS, Fincantieri Marinette + WI -> FFG-62, Pearl Harbor Naval Shipyard + HI -> SSN/CVN. Low confidence but covers the long tail where description text is silent.

5. **Subaward narrative enrichment** -- `usa_client.get_subawards()` exists but is unused for residual diagnosis. Subaward narratives from HII / BAE / NASSCO often name the specific hull being fed.

### Product Procurement improvements

6. **Newbuild-PSC classification saw tiny Tier 0 lift** -- ~0.1% improvement. Expected: newbuild contracts reference programs (DAP) more than ship names. If PP residual is a priority, different signals needed: manual PIID-to-hull map, NAICS + recipient priors, or cross-reference against vessel-taxonomy PSC-to-hull crosswalks.

7. **SSN / SSBN residual audit** -- SSN alone is $17.6B of PP. Classified via DAP "SSN 774" -> Virginia. Worth spot-checking that residual SSN work isn't actually Columbia-class or cross-class in reality.

### Quality / audit

8. **Add an automated reconciliation check** -- Services' Vessel Type total should equal its Hull Program total (both query `AwardsByHull`). PP similarly. Add to `build_from_data.py` so rebuilds that break the invariant fail loudly.

9. **Separate "decommissioned / test ship" bucket** -- $9M USS PAUL FOSTER (ex-DD-964 Self Defense Test Ship at NSWC Port Hueneme) and $17M USS PHILLADELPHIA are real, legitimate work but don't belong in a "current fleet" TAM calc. Worth a dedicated category.

### What not to re-attempt

- SAM.gov bulk CSV for historical solicitations -- proven < 1% coverage in 2026-04-16 session.
- Per-solnum SAM.gov API lookups -- rate-limit prohibitive.
- Classifying proper names from model memory -- user explicitly ruled out; use Wikipedia or user-validated lookups only.
