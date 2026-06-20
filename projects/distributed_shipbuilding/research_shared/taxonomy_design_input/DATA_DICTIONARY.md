# Taxonomy-design input bundle — data dictionary

Deduplicated Navy new-construction **subaward** records, two programs (submarines +
DDG-51), pulled from SAM.gov FSRS. ~$17.8B across 1,352 unique supplier entities /
22,499 records. One row per unique subaward (deduped on subaward report id).

**Key data facts to know before designing categories:**
- A subaward transaction carries **no subawardee NAICS or PSC**. The only NAICS on the
  raw record is the *prime's* (≈always 336611 Ship Building). Entity NAICS/PSC below
  come from a separate SAM **entity** lookup, keyed by the supplier's UEI.
- Subaward **descriptions are unusable for submarines** (mostly "See Below" filler) but
  **usable for HII-Ingalls DDG**, where they carry a builder work-item code and often an
  explicit SWBS token. GD-BIW DDG descriptions carry no parseable code.
- Dollars are concentrated: top 50 entities = 76% of $, top 300 = 96.6%.

## Files

**naics6_distribution.csv** — every primary 6-digit NAICS present in the corpus.
`primary_naics_6, desc, vendors` (# entities), `dollars_$M, pct_dollars`. The headline
view of what suppliers do, by dollar.

**uei_entity_profile.csv** — one row per supplier entity (UEI).
`uei, name, dollars, records, programs, foreign, sam_match, reg_status,
org_structure_desc` (e.g. "Manufacturer of Goods"), `primary_naics_6, primary_naics_4,
naics_count, all_naics_6` (full self-certified NAICS list, `|`-joined), `psc_count,
psc_list, immediate_owner, highest_owner, cage, exclusion, business_types`.

**uei_naics_long.csv** — long form of every entity's full NAICS list.
`uei, naics6, desc, is_primary, dollars`.

**uei_psc_long.csv** — long form of every entity's PSC list (sparse; ~12% of $).
`uei, psc, desc, dollars`.

**hii_ddg_record_components.csv** — the one segment with record-level work signal:
HII-Ingalls DDG subawards parsed from the description. `piid, builder, sub_report_id,
sub_date, fy, amount_usd, vendor_uei, parent_uei, vendor_name, raw_description,
code` (HII work-item code NNNNN-NN), `swbs_group` (explicit SWBS token where present,
else propagated from the recurring code; blank if neither), `hull, component_text,
n_component_words`.

**hii_ddg_code_dictionary.csv** — compact view of the HII work-item codes.
`code, n_subawards, total_usd, modal_swbs_group` (most-common SWBS seen with that code),
`top_components`.

> **HII code ↔ SWBS relationship (verified).** The HII work-item code is a *finer
> sub-index nested inside a single SWBS subsystem*, not an orthogonal scheme. On the
> 106 codes that carry an explicit SWBS cross-reference (≈71% of HII $), each code maps
> to **exactly one** SWBS 3-digit subsystem (100% purity), and each subsystem fans out
> into several codes (e.g. SWBS 551 → 13 codes). So `modal_swbs_group` is a reliable 1:1
> mapping where present. The ~14% of HII $ that is coded-but-opaque has no cross-ref to
> prove it. Practical consequence: the HII segment can support category granularity
> *finer than* an SWBS subsystem; the rest of the corpus (submarines, BIW) generally
> cannot reach even subsystem level — so achievable granularity differs by segment.
> (The separate 2-digit "family" prefix is coarser than SWBS and spans subsystems —
> ignore it.)

**swbs_hierarchy.csv** — authoritative Navy SWBS/ESWBS codebook (reference, not ours).
`eswbs_code` (5-digit), `one_digit_group` (1–9), `group_name`, `nomenclature, remarks`.
The 1-digit groups: 1 Hull, 2 Propulsion, 3 Electric, 4 Command/Control/Surveillance,
5 Auxiliary, 6 Outfit/Furnishings, 7 Armament, 8 Integration/Engineering, 9 Assembly/Support.
