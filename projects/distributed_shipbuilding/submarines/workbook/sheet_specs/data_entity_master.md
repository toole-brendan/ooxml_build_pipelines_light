Entity Master
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_entity_master.py

Purpose
Subaward vendor classification (the native table) and the supplier-addressable base;
the PRODUCER of the observed bucket shares and supplier roles. Each vendor row is
classified by taxonomy.classify(vendor, naics4) -> (role, bucket, basis), and the §3/§4
summaries aggregate that classification with SUMPRODUCT masks.

Source
extracted/entity_naics_lookup.csv - one row per subaward recipient (vendor, uei,
country, naics_4digit, naics_desc, amount_M_lifetime). Rows sorted by $M descending.

Reads
- none (record-level entity source; classifies its own CSV rows)
- taxonomy.classify / BUCKETS / BUCKET_KEYS / UNBUCKETED - the work-type bucket
  vocabulary + the role/bucket/basis rule chain (vendor-override -> naics4 -> service
  NAICS -> prime/co-prime name -> GFE/SIB name -> holding-co -> residual)

Feeds
- Worktype Evidence (top-vendor register), Assumptions (modeled bucket
  shares), SAM Build, z_ChartData, Figure Register (DO-07)
- Producer cells / accessors:
  observed_bucket_share_cell(b) -> §4 share D-cell (-> Assumptions),
  observed_bucket_dollar_cell(b) -> §4 supplier $M C-cell,
  addressable_total_cell() -> §4 supplier-addressable total (-> Figure Register DO-07),
  role_dollar_cell(role) / grand_total_cell() -> §3 role $,
  table ranges ent_dollar/role/bucket/country/naics/basis_range (the SUMPRODUCT
  operands), ent_row_cell(i,key) + top_vendor_indices / top_supplier_indices /
  unbucketed_vendor_indices (-> Worktype Evidence)
- Excel table: tbl_sub_entity_master

On the sheet
§1  At a glance: supplier-addressable base
    - Same-sheet summary of the §3/§4 producer cells, shown as black derived values:
      total entities (count), supplier-addressable subaward total $M (= §4
      addressable_total_cell), prime / co-prime total $M (= §3 prime + co_prime role $),
      GFE / SIB total $M (= §3 gfe_sib role $), unbucketed supplier $M (= §4 unbucketed
      bucket $).

§2  Entity classification (subaward vendors)
    - The native table tbl_sub_entity_master, one row per CSV recipient, columns:
      Vendor, UEI, Country, NAICS-4, NAICS desc, $M, Role, Bucket, Class rule.
    - Role / Bucket / Class rule are computed by taxonomy.classify at load: role in
      {supplier, prime, co_prime, gfe_sib, service}; bucket in the 7 work-type keys or
      unbucketed; basis = which rule fired. Sorted $M descending; the table ranges back
      every §3/§4 SUMPRODUCT.

§3  Role summary ($ by classification role)
    - One row per role (supplier / prime / co_prime / gfe_sib / service):
        role $M     = SUMPRODUCT((role_range = role) x ent_dollar_range)
        % of total  = role $ / grand total
    - Grand total (all recipients) = SUMPRODUCT(ent_dollar_range)  [the % denominator].

§4  Bucket summary (observed supplier $ + share)  - the observed-bucket-share PRODUCER
    - One row per work-type bucket key, then an unbucketed row:
        supplier $M    = SUMPRODUCT((role = "supplier") x (bucket = k) x ent_dollar_range)
        observed share = supplier $ / supplier-addressable total
    - Supplier-addressable total = SUMPRODUCT((role = "supplier") x ent_dollar_range)
      [the share denominator; addressable_total_cell].
    - observed_bucket_share_cell feeds Assumptions (modeled = observed +
      adjustment).

§5  Classification rule (which rule fired)
    - One row per basis key (vendor-override, naics4, service NAICS, prime/co-prime
      name, GFE/SIB name, holding-co (parent unknown), residual):
        entity count = SUMPRODUCT(basis_range = key)
        $M           = SUMPRODUCT((basis_range = key) x ent_dollar_range)
    - Audit view of how the taxonomy chain partitioned the corpus.

Notes
- Native cell notes: none.
- Note column: none.
