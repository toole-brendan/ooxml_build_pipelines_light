# Taxonomy-design input bundle (CANONICAL) — data dictionary

Deduplicated Navy new-construction **subaward** records across three programs —
**Virginia-class** and **Columbia-class** submarines and **DDG-51** destroyers — pulled
from SAM.gov FSRS. One row per unique subaward (deduped on subaward report id).

**This bundle is built from the same record stream the award-analysis workbook consumes**
(`_corpus.iter_records`): scope-filtered to in-scope new-construction PIIDs, with
pass-through/industrial-base conduits (BlueForge, Training Modernization Group, IALR)
and out-of-scope work removed, and LCS line-item contamination stripped. SAM entity
attributes (NAICS-6, NAICS list, PSC, org-structure) are joined per UEI as a lookup; the
dollars and program split are computed from the canonical stream, not from SAM.

## Universe (read this before designing categories)
- **Total: $13,111M** — submarines **$9,563M**, DDG-51 **$3,547M**.
- **1,203 supplier entities (UEIs).**
- **87.5% of dollars carry a primary NAICS-6**; the remaining **~12.5% ($1.6B)** has no
  resolvable primary NAICS-6 (unregistered, no-SAM-record, or foreign) and must be
  classified from other evidence or left unresolved.
- A subaward transaction carries **no subawardee NAICS or PSC** of its own; entity
  NAICS/PSC below come from a separate SAM entity lookup keyed by UEI.
- Subaward **descriptions are unusable for submarines** (filler) but **usable for the
  HII-Ingalls DDG segment**, which carries a structured work-item code and often an
  explicit SWBS reference. Submarines are therefore represented at the entity level only.
- Note: an entity's self-certified NAICS may not reflect its subaward work (e.g. several
  entities under NAICS 336611 "Ship Building" are first-tier suppliers, not shipbuilders).

## Files

**naics6_distribution.csv** — every primary NAICS-6 in the universe, on canonical dollars.
`primary_naics_6, desc, vendors` (# entities), `dollars_$M, pct_dollars`. The bucket
`(no_primary_naics6)` collects entities with no resolvable primary NAICS-6.

**uei_entity_profile.csv** — one row per supplier entity (UEI), dollars from the canonical
stream. `uei, name, dollars_total_$M, dollars_submarines_$M, dollars_ddg_$M, records,
foreign, enriched` (whether a SAM record was found), then SAM attributes:
`sam_match, reg_status, org_structure_desc, primary_naics_6, primary_naics_4, naics_count,
all_naics_6` (full self-certified NAICS list, `|`-joined), `psc_count, psc_list,
immediate_owner, highest_owner, cage, exclusion, business_types`.

**uei_naics_long.csv** — long form of every entity's full NAICS list. `uei, naics6, desc,
is_primary, dollars`. (Filtered to the canonical UEIs.)

**uei_psc_long.csv** — long form of every entity's PSC list (sparse). `uei, psc, desc,
dollars`. (Filtered to the canonical UEIs.)

**hii_ddg_record_components.csv** — the one segment with record-level work signal:
HII-Ingalls DDG subawards parsed from the description (LCS records removed). `piid, builder,
sub_report_id, sub_date, fy, amount_usd, vendor_uei, parent_uei, vendor_name,
raw_description, code` (HII work-item code NNNNN-NN), `swbs_group` (explicit SWBS token
where present, else propagated from the recurring code; blank if neither), `hull,
component_text, n_component_words`.

**hii_ddg_code_dictionary.csv** — compact view of the HII work-item codes (recomputed after
the LCS strip). `code, n_subawards, total_usd, modal_swbs_group, top_components`.

> **HII code ↔ SWBS relationship (verified).** The HII work-item code is a *finer
> sub-index nested inside a single SWBS subsystem*, not an orthogonal scheme. On the codes
> that carry an explicit SWBS cross-reference (~71% of HII $), each code maps to exactly
> one SWBS 3-digit subsystem (100% purity), and each subsystem fans out into several codes.
> So `modal_swbs_group` is a reliable 1:1 mapping where present; ~14% of HII $ is
> coded-but-opaque (no cross-ref to prove it). Consequence: the HII segment can support
> granularity *finer than* an SWBS subsystem; the rest of the corpus generally cannot reach
> even subsystem level — so achievable granularity differs by segment. (The separate 2-digit
> "family" prefix is coarser than SWBS and spans subsystems — ignore it.)

**swbs_hierarchy.csv** — authoritative Navy SWBS/ESWBS codebook (reference, not ours).
`eswbs_code` (5-digit), `one_digit_group` (1–9), `group_name`, `nomenclature, remarks`.
Groups: 1 Hull, 2 Propulsion, 3 Electric, 4 Command/Control/Surveillance, 5 Auxiliary,
6 Outfit/Furnishings, 7 Armament, 8 Integration/Engineering, 9 Assembly/Support.

**build_bundle.py** — the script that produced this bundle (provenance; reproducible).
