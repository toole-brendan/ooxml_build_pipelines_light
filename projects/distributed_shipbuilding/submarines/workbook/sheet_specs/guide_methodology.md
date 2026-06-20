Methodology
Tab color: 2C6E6E (teal)  ·  group: Guide & scope
Module: guide_methodology.py

Purpose
Definitions, the formula framework, the scope boundary, exclusion rules, and the
bucket taxonomy. NAICS/vendor-led classification is the submarine signal. Mostly
prose/crosswalk; the bucket vocabulary + classify() live in taxonomy.py and are
rendered here, with a few live cross-sheet figures linked in. Pure consumer (no accessors).

Reads
- TAM Build       applied BC supplier coefficient, AP/LLTM reference coefficient (the §2a
                  live coefficient rows)  [bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell]
- POP Source Audit  gated TAM corpus $, GFE/excluded scope $ (the §5a live corpus rows)
                  [gated_dollar_cell, gfe_excluded_dollar_cell]
- SIB Excluded    subaward-level SIB exclusion total (§5a)  [sib_total_cell]
- taxonomy.py     BUCKETS, UNBUCKETED, NAICS4_BUCKET (rendered into §6 / §6a)

Feeds
- none

On the sheet
§1  Definitions
    - Term / Definition / Workbook treatment table: TAM (non-GFE/SIB new-construction supplier
      opportunity = BC base x coeff + AP/LLTM base x coeff), SAM (portion of TAM in targeted buckets;
      scenario menu, no haircut), SOM (not modeled), BC (P-5c, GFE-free; headline stream), AP/LLTM
      (reference stream, additive base = 0), GFE (excluded from TAM), SIB (excluded from SAM), POP
      (drives the supplier coefficient), Supplier coefficient ($-weighted supplier+foreign POP share),
      Distributed-production view (appendix context).

§2  Formula framework
    §2a TAM framework: prose TAM = BC base x BC supplier coefficient + AP/LLTM base x AP/LLTM supplier
        coefficient; applied = BC base x non-nuclear BC coeff + $0 AP/LLTM base x reference coeff. Live
        rows: Applied BC supplier coefficient <- TAM Build, AP/LLTM reference coefficient <- TAM Build
        (not applied, base = 0).
    §2b SAM framework: prose SAM scenario = SUMPRODUCT(bucket TAM, scenario inclusion flag); no
        SOM/capture/probability haircut.

§3  Market-sizing flow
    - Step / Input / Method / Output-tab crosswalk: Budget base (SCN P-5c + P-10 -> SCN Budget / AP Bridge)
      -> remove GFE / non-addressable / dup AP (TAM Build) -> apply POP supplier coefficient (TAM Build)
      -> Portfolio TAM (base x coefficient, TAM Build) -> allocate TAM into buckets (x modeled bucket
      share, SAM Build) -> apply target scenario flags (SUMPRODUCT, SAM Build) -> SAM scenario output.

§4  Scope boundary
    §4a In TAM: Basic Construction non-GFE; supplier-addressable component procurement; work away from
        prime/co-prime/GFE sites; eligible AP/LLTM/EOQ only if additive.
    §4b Out of TAM: GFE/weapons/sensors/ordnance; SIB/industrial-base capacity grants; sustainment/
        depot/design-only; prime/co-prime final-assembly yard work; AP/LLTM already inside BC.

§5  Exclusion rules
    - Exclusion category / Treatment / Rationale / Evidence-tab table: GFE (SCN Budget), SIB (SIB
      Excluded), BPMI / naval nuclear (Sensitivity), Prime yard + Co-prime yard (POP Corpus),
      Design-only + AP/LLTM already in BC (AP Bridge), Service / non-component (Entity Master).
    §5a Effect on the corpus (live): Gated TAM corpus <- POP Source Audit (before exclusions); less GFE/
        excluded scope <- POP Source Audit (dropped from base + corpus); SIB exclusion (subaward-level)
        <- SIB Excluded (BlueForge / TMG / IALR).

§6  Bucket taxonomy
    - Bucket key / Display name / Definition / Typical-evidence table rendered from taxonomy.BUCKETS,
      plus the Unbucketed/ambiguous row (parent-unknown or no clean NAICS); evidence -> Worktype Evidence.
    §6a NAICS-4 -> bucket crosswalk: sorted NAICS4_BUCKET map (code -> bucket).

§7  Classification precedence (first match wins)
    - Priority / Rule / Result / Example table: (1) prime/co-prime name -> role=prime/co_prime; (2) GFE/SIB
      name -> role=gfe_sib; (3) vendor-name override -> bucket per override; (4) NAICS-4 crosswalk ->
      role=supplier, bucket per NAICS; (5) service NAICS -> role=service; (6) residual -> role=supplier,
      bucket=unbucketed.

Notes
- Native cell notes: 4 -
    §1 (C): SIB = Submarine Industrial Base (earlier sources / exhibits use MIB / Maritime Industrial Base)
    §1 (C): TAM = non-GFE, non-SIB new-construction supplier opportunity (BC base x supplier coeff)
    §1 (C): SAM = the portion of TAM in the targeted work-type buckets, shown as a scenario menu
    §1 (C): advance procurement / long-lead is retained as a reference stream; its additive base is $0
- Note column: none.
