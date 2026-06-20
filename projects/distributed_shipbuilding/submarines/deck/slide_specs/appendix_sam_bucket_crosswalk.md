# SlideSpec - submarines `appendix_sam_bucket_crosswalk` (appendix A5)
# Dense appendix crosswalk table: the seven work-type buckets, their NAICS-4
# evidence cues, and how each maps into broad SAM plus the four overlapping
# scenario cuts (metal, modular, HM&E, electrical). A gray residual row sits
# outside broad SAM. A bottom no-fill note states that scenario cuts overlap and
# must not be summed. Verified against taxonomy.py (BUCKETS + NAICS4_BUCKET) and
# inputs_assumptions.py SCENARIOS membership.

meta:
  slide_id: subs-a5
  slide_order: A5               # registry position A5 (deck_spec sec.5 order); module wired in slides/__init__.py
  module_name: appendix_sam_bucket_crosswalk.py
  slide_type: appendix
  section: Appendix
  archetype: dense_crosswalk_table_plus_caveat_note
  story_role: Back the S13 Bucket TAM and S14 SAM Scenarios slides by showing exactly which work-type buckets compose broad SAM and each overlapping scenario cut, and why the residual is held out.
  inputs:
    - Chart Data CD_A6_SAMBucketCrosswalk     # internal provenance only (NOT a citation)
    - Taxonomy (seven buckets + NAICS-4 crosswalk)
    - SAM Build sections 4-6 (modeled shares, bucket TAM, scenario flags)
    - Assumptions and Controls section 5 (target scenario matrix)
    - Worktype Evidence (top vendors per bucket)
    - Entity Master (SAM.gov Entity Management NAICS enrichment)
  related_appendix:
    - subs-a6   # appendix_top_25_visible_suppliers (the named-vendor evidence behind the cues)

chrome:
  section: Appendix
  breadcrumb_topic: SAM bucket crosswalk
  title_topic: SAM Bucket Crosswalk
  title_finding: NAICS and vendor evidence map the seven buckets into broad SAM and four overlapping scenario cuts
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - U.S. Department of the Navy SCN Justification Books
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

story:
  objective: Define the bucket-to-scenario inclusion logic so a reader can audit which buckets compose broad SAM and each scenario cut, and confirm the residual is excluded from broad SAM.
  do_not_say:
    - Do not sum the scenario columns; the cuts overlap and are not additive.
    - Do not force the residual flow into broad SAM.
    - Do not describe NAICS as a per-action work description; it is a corporate-primary classification.
    - Do not present the crosswalk as SOM; no capture haircut is applied.
  known_caveats:
    - NAICS is useful but imperfect because it is generally corporate-primary, not per-action; the NAICS-4 cues are directional, with named vendor overrides where the corporate code is misleading.
    - Machining sits in BOTH the metal and HM&E scenarios, so metal + HM&E double-counts machining; this is the clearest reason the columns must not be summed.
    - The residual exists because the model refuses to force ambiguous dollars into a named bucket; excluded from broad SAM, not a claim it is non-addressable.

regions:
  coord_basis: BODY
  layout_pattern: dense_crosswalk_table_plus_caveat_note
  # Vertical stack: caption band, full-width crosswalk table, pinned bottom note.
  caption:         {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  crosswalk_table: {x: 0%, y: below(caption), w: 100%, h: body_until(bottom_note)}
  bottom_note:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: caption,         prominence: tertiary, paint_order: 1, content: matrix caption}
  - {id: e2, type: table,         region: crosswalk_table, prominence: primary,  paint_order: 2, content: bucket-to-scenario crosswalk table (7 buckets + residual), tie_out: CD_A6_SAMBucketCrosswalk + taxonomy.NAICS4_BUCKET + inputs_assumptions.SCENARIOS}
  - {id: e3, type: note,          region: bottom_note,     prominence: tertiary, paint_order: 3, content: scenario-overlap / no-sum caveat}


# ── TYPOGRAPHY UPDATE ─────────────────────────────────────────────────────
typography:
  inherits: SPEC_FORMAT typography contract
  contract:
    font: FONT
    body_runs: Every non-chrome text run must pass explicit size and font=FONT.
    line_spacing: LNSPC_BODY unless a local helper intentionally changes it.
    colors: Use DK on light/no fill; WHITE on BLUE_3/BLUE_4/BLUE_5/GRAY_5; BREADCRUMB only in chrome.
    chart_title_rule: Keep chart factory title=null and render an external no-fill CHART_TITLE_10PT italic text_box unless the chart must be self-contained.
    fallback: When a body text string is still a scalar text field, build it as paragraphs/runs using the element style below; do not let the builder inherit body typography.
  elements:
    e1:
      text_runs:
      - role: matrix caption
        size: CHART_TITLE_10PT
        color: DK
        font: FONT
        italic: true
    e2:
      table_text:
        body:
          size: LABEL_9PT
          font: FONT
          color: DK
        header:
          size: LABEL_9PT
          font: FONT
          bold: true
        first_column:
          size: LABEL_9PT
          font: FONT
          bold: as indicated by cell_bold or house_table first_col
    e3:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts: []                # NONE on this slide -> no chart rIds; chart-fit checks N/A

tables:
  - id: crosswalk_1
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Work-type bucket to SAM scenario crosswalk
      purpose: define
      reader_takeaway: Broad SAM is the seven classified buckets; the four scenario cuts overlap (machining is in both metal and HM&E); the residual is tracked in TAM but excluded from broad SAM.
      row_order: seven classified buckets in taxonomy order, then the gray residual row
      highlight_rows:
        - Residual (Unbucketed / ambiguous)
      guardrails:
        - Scenario cuts overlap; do not sum the Metal, Modular, HM&E, and Elec columns.
        - Machining is flagged Yes under BOTH Metal and HM&E (per inputs_assumptions.SCENARIOS).
        - Coatings is flagged Yes under Modular (structural + coatings), not just Broad.
        - Residual row uses GRAY exclusion styling and is No across every scenario including Broad.
        - No SOM is modeled; flags are inclusion logic, not capture.
    render:
      table_skin: light          # light GRAY_1 header per house guidance for dense matrices; dark header would dominate
      size: 900                  # 9.0pt body (LABEL_9PT); dense appendix crosswalk
      column_widths:
        mode: ratio
        # Bucket | Evidence cues (NAICS-4 + example vendor) | Broad | Metal | Modular | HM&E | Elec
        values: [2.6, 3.6, 0.85, 0.85, 0.95, 0.85, 0.85]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: [l, l, ctr, ctr, ctr, ctr, ctr]
      row_h:
        fn: estimate_row_heights
        size_pt_from: size
        header_size_pt_from: size
      rows:
        - ["Bucket", "Evidence cues (NAICS-4; example vendor)", "Broad", "Metal", "Modular", "HM&E", "Elec"]
        - ["Structural fab / pre-outfit", "3323, 3324, 3366, 3369; e.g. DC Fabricators, Rhoads", "Yes", "Yes", "Yes", "No", "No"]
        - ["Machining", "3327, 3336; e.g. Advance Mfg., B. & F. Machine", "Yes", "Yes", "No", "Yes", "No"]
        - ["Castings and forgings", "3321, 3315, 3312; e.g. Scot Forge", "Yes", "Yes", "No", "No", "No"]
        - ["Piping / valves / pumps", "3329, 3339, 4235; e.g. Curtiss-Wright, CIRCOR", "Yes", "No", "No", "Yes", "No"]
        - ["Electrical / power", "3353, 3344, 3359, 3364; e.g. Northrop Grumman, Leonardo", "Yes", "No", "No", "No", "Yes"]
        - ["HVAC / ventilation", "3334; e.g. Johnson Controls Navy Systems", "Yes", "No", "No", "Yes", "No"]
        - ["Coatings / insulation", "3252, 3259, 3262; e.g. Globe Composite", "Yes", "No", "Yes", "No", "No"]
        - ["Residual (Unbucketed / ambiguous)", "no clean NAICS bucket; e.g. ESCO (5511), L3Harris, BWX", "No", "No", "No", "No", "No"]
      cell_fills:
        # Header row uses the light-skin default GRAY_1 header (no per-cell override needed)
        # Residual row (row 8): gray exclusion styling - NOT the counted-SAM blues
        "(8,0)": GRAY_3
        "(8,1)": GRAY_3
        "(8,2)": GRAY_3
        "(8,3)": GRAY_3
        "(8,4)": GRAY_3
        "(8,5)": GRAY_3
        "(8,6)": GRAY_3
      cell_bold:
        "(0,0)": true
        "(0,1)": true
        "(0,2)": true
        "(0,3)": true
        "(0,4)": true
        "(0,5)": true
        "(0,6)": true
        "(8,0)": true
      cell_text_colors: {}        # light-skin header -> dark text by default; no WHITE overrides
      footnotes:
        - "Scenario cuts overlap and must not be summed (machining is in both Metal and HM&E). Broad SAM excludes the unbucketed / ambiguous residual. No SOM is modeled."
    columns: []

shapes:
  - id: caption_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Work-type bucket to SAM scenario crosswalk"   # CHART_TITLE_10PT italic DK
    meaning: External matrix caption; no fill keeps the table dominant.
  - id: note_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Scenario cuts overlap; do not sum scenarios (machining is in both Metal and HM&E). Broad SAM excludes the unbucketed / ambiguous residual. No SOM is modeled."   # FINEPRINT_8_5PT
    meaning: Bottom no-sum caveat; no fill to keep the matrix dominant.

images: []

commentary:
  visible:
    element: e3
    container: table_note
    title:
    bullets:
      - {lead: "Read:", body: "scenarios overlap and are not additive; broad SAM is all seven buckets, residual excluded."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHAT THIS APPENDIX BACKS. This is the audit table behind S13 (Bucket TAM)
      and S14 (SAM Scenarios). It shows the seven classified work-type buckets, the
      NAICS-4 evidence cues that populate them, and the inclusion flags that turn
      buckets into broad SAM and the four overlapping scenario cuts. It is the
      "show your work" for how FFATA-visible vendor flow and SAM.gov Entity
      Management NAICS enrichment compose the SAM the deck quotes.

      THE SEVEN BUCKETS AND THEIR NAICS-4 CROSSWALK (verified against the model's
      taxonomy; NAICS-4 -> bucket map):
      - Structural fabrication and pre-outfit <- 3323 (fabricated structural metal),
        3324 (metal tanks/boilers), 3366 (ship/boat building), 3369 (other transport
        eq). Hull sections, fabricated structural metal, pre-outfit modules.
      - Machining <- 3327 (machine shops / turned product), 3336 (mechanical power
        transmission). Machine shops, precision machining.
      - Castings and forgings <- 3321 (iron/steel forging), 3315 (steel/nonferrous
        foundries), 3312 (steel product). Forged and cast components.
      - Piping, valves, and pumps <- 3329 (other fabricated metal: valves/fittings),
        3339 (pumps, measuring/dispensing), 4235 (metal service centers). Valves,
        pumps, pipe and fittings.
      - Electrical and power <- 3353 (switchgear/motors), 3344 (electronic
        components), 3359 (other electrical), 3364 (a name-override artifact:
        Northrop Grumman / Leonardo propulsion-electronics carry an aircraft-parts
        corporate NAICS but supply submarine electrical content). Switchgear, power
        conversion, propulsion-electronics.
      - HVAC and ventilation <- 3334 (air-conditioning / warm-air heating). Shipboard
        ventilation and air systems.
      - Coatings and insulation <- 3252 (synthetic rubber/resins), 3259 (other
        chemicals), 3262 (rubber product). Coatings, rubber, insulation, composites.
      Beyond the NAICS map, named-vendor overrides reassign firms whose corporate
      NAICS is misleading: Rhoads Metal and Austal -> structural; Curtiss-Wright
      Flow, CIRCOR, Hunt Valve, Tioga Pipe -> piping; Oil States -> coatings; and
      BWX, Ultra Electronics, Goodrich, APCO, L3Harris -> residual.

      HOW BUCKETS BECOME SCENARIOS (the inclusion matrix, verified against the
      model's scenario membership). Each scenario is the SUMPRODUCT of bucket TAM
      and a 0/1 flag vector:
      - Broad component manufacturing = all seven buckets (residual excluded). The
        scenario ceiling, ~84.8% of TAM.
      - Metal components = structural + castings + machining.
      - HM&E components = piping + HVAC + machining.
      - Modular assemblies = structural + coatings.
      - Electrical / power = electrical (standalone).
      CRITICAL OVERLAP: machining is a member of BOTH metal and HM&E, and structural
      is a member of metal, modular, and broad. The cuts therefore overlap and are
      NOT additive; summing the four scenario columns double-counts. This is the
      single most important guardrail on the slide.

      THE RESIDUAL. Unbucketed / ambiguous flow (~$501M/yr, ~$3.01B cumulative,
      ~15.2% of TAM at the S13 modeled split) is held OUT of broad SAM and every
      scenario. It is real visible vendor flow that the model declines to force into
      a named bucket - e.g. ESCO Technologies (corporate NAICS 5511, a holding-co
      rollup), L3Harris and BWX (override -> residual). NAICS is a corporate-primary
      classification, not a per-action work description, so forcing these into a
      bucket would overstate broad SAM. The residual stays in the TAM tie-out (the
      allocation is exhaustive) but is excluded from SAM - a credibility feature, not
      a claim the dollars are non-addressable.

      WHY THE EVIDENCE CUES ARE TRUSTWORTHY BUT IMPERFECT. The SAM Entity Management
      API was queried for the top FFATA-visible parents; NAICS enrichment covers
      ~93.5% of dollar-weighted visible flow but only ~70% of unique vendor count
      (~45 of the top 150 are no longer samRegistered=Yes). Northrop Grumman is the
      canonical NAICS limitation: corporate code 336413 (aircraft parts) even though
      its submarine-relevant content is sonar, combat systems, and propulsion
      electronics - which is why the model carries a 3364 -> electrical override.

      DENSITY GUIDANCE. Default is caption + crosswalk table + no-sum note. To
      densify, expand the evidence-cue column to add a second example vendor per
      bucket, or add a one-line scenario-key legend above the note. Keep the residual
      row gray and visually separate from the blue header at any density.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3]}
      dense:  {add_bullets: 3, safe_containers: [bottom_note, crosswalk_table], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Do not sum scenarios:"
        body: "Machining is in both Metal and HM&E and structural is in Metal, Modular, and Broad, so the scenario columns overlap and are not additive."
        evidence: inputs_assumptions.SCENARIOS membership
        safe_container: bottom_note
        density_trigger: Keep visible in all versions; it is the core guardrail.
      - priority: 2
        lead: "Broad = all seven:"
        body: "Broad component manufacturing is the seven classified buckets with no capture haircut, ~84.8% of TAM; it is a ceiling, not a SOM."
        evidence: SAM Build section 6 (broad scenario)
        safe_container: bottom_note
        density_trigger: Add if a reviewer asks what broad SAM contains.
      - priority: 3
        lead: "Residual logic:"
        body: "The unbucketed / ambiguous residual stays in the TAM tie-out but is excluded from broad SAM and every scenario; it is not automatically non-addressable."
        evidence: SAM Build section 5a (unbucketed allocation)
        safe_container: crosswalk_table
        density_trigger: Add if reviewers question why the residual row is all No.
      - priority: 4
        lead: "NAICS is corporate-primary:"
        body: "NAICS is a corporate-primary classification, not a per-action work description; the model adds vendor overrides where the corporate code is misleading."
        evidence: SAM.gov Entity Management API; taxonomy VENDOR_BUCKET_OVERRIDES
        safe_container: bottom_note
        density_trigger: Add in a denser diligence version.
      - priority: 5
        lead: "The Northrop example:"
        body: "Northrop Grumman carries corporate NAICS 336413 (aircraft parts) yet supplies submarine sonar and propulsion electronics, so the model maps 3364 to electrical / power."
        evidence: Vendors and concentration (NAICS work-type mix)
        safe_container: crosswalk_table
        density_trigger: Add as a cell footnote if the electrical row is questioned.
      - priority: 6
        lead: "Metal cut:"
        body: "Metal components = structural fab, machining, and castings and forgings; it anchors the fabricated-metal opportunity (DC Fabricators, Scot Forge, Pegasus Steel)."
        evidence: SAM Build section 6 (metal scenario); Worktype Evidence
        safe_container: crosswalk_table
        density_trigger: Add when this slide is paired with S14.
      - priority: 7
        lead: "HM&E cut:"
        body: "HM&E components = piping, valves, pumps plus HVAC and machining; specialty flow components with meaningful qualification burden (Curtiss-Wright, CIRCOR, Johnson Controls)."
        evidence: SAM Build section 6 (HM&E scenario); Worktype Evidence
        safe_container: crosswalk_table
        density_trigger: Add when this slide is paired with S14.
      - priority: 8
        lead: "Modular cut:"
        body: "Modular assemblies = structural fab plus coatings and insulation, aligned with pushing pre-outfit module work out of the legacy yards."
        evidence: SAM Build section 6 (modular scenario)
        safe_container: crosswalk_table
        density_trigger: Add for an audience focused on distributed-build logic.
      - priority: 9
        lead: "Coverage of the cues:"
        body: "NAICS enrichment covers ~93.5% of dollar-weighted visible flow but only ~70% of unique vendor count, so the cues are directional, not exhaustive."
        evidence: Vendors and concentration (NAICS enrichment coverage)
        safe_container: bottom_note
        density_trigger: Add if a reviewer asks how complete the NAICS mapping is.
      - priority: 10
        lead: "Bucket names are stable:"
        body: "Bucket names match the S12 taxonomy, S13 bucket TAM, S14 SAM scenarios, and S18 implications slides; do not rename them here."
        evidence: taxonomy.BUCKETS display names
        safe_container: crosswalk_table
        density_trigger: Build QA only; do not render.
    do_not_add:
      - a summed scenario total
      - SOM, capture, or win-probability language
      - icon-only checkmarks without text labels
      - the residual rendered as a counted SAM bucket (keep it gray and No across all scenarios)

data_and_calculations:
  data_inputs:
    - {input: Structural fab / pre-outfit, value: "NAICS 3323/3324/3366/3369", unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: Machining,                   value: "NAICS 3327/3336",           unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: Castings and forgings,       value: "NAICS 3321/3315/3312",      unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: Piping / valves / pumps,     value: "NAICS 3329/3339/4235",      unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: Electrical / power,          value: "NAICS 3353/3344/3359/3364", unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: HVAC / ventilation,          value: "NAICS 3334",                unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
    - {input: Coatings / insulation,       value: "NAICS 3252/3259/3262",      unit: crosswalk, tie_out: taxonomy.NAICS4_BUCKET, used_in: crosswalk_1}
  calculations:
    - {name: Metal scenario, formula: "structural + castings + machining", output: "0/1 flag vector", used_in: crosswalk_1}
    - {name: HM&E scenario, formula: "piping + hvac + machining", output: "0/1 flag vector", used_in: crosswalk_1}
    - {name: Modular scenario, formula: "structural + coatings", output: "0/1 flag vector", used_in: crosswalk_1}
    - {name: Electrical scenario, formula: "electrical", output: "0/1 flag vector", used_in: crosswalk_1}
    - {name: Broad scenario, formula: "all seven buckets (residual excluded)", output: "0/1 flag vector", used_in: crosswalk_1}
  rounding_rules: No numeric values rendered on this slide; flags are Yes/No text.
  reconciliation: Crosswalk flags define inclusion logic; scenarios are overlapping cuts and are not expected to sum. Broad SAM = TAM minus the unbucketed residual.

qa:
  guardrails:
    - Use Yes and No text rather than icon-only flags.
    - Machining is Yes under BOTH Metal and HM&E; coatings is Yes under Modular; verify against the model scenario membership.
    - Residual row is GRAY and No across every scenario including Broad - never the counted-SAM blues.
    - Keep bucket names consistent with main-deck slides 12, 13, 14, and 18.
    - Do not sum the scenario columns anywhere on the slide.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov FFATA/FSRS, SAM.gov Entity Management API, SCN Justification Books); no internal docs, workbook tabs, wiki chapters, or CD_ IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - "if a table exists: resolved column widths sum to its region width"
    # no chart on this slide -> chart rId / chart-fit checks do not apply
