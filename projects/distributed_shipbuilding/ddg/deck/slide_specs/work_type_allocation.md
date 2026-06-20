# ══════════════════════════════════════════════════════════════════════════════
# MERGED SLIDE SPEC — two slides, one file  (consolidated 2026-06-04; 43→40 specs)
# Documents TWO rendered slides whose modules stay SEPARATE; the build is unchanged.
#   1. ddg-s10  sam_taxonomy.py         — SAM taxonomy (bucket menu + membership cue)
#   2. ddg-s11  work_type_allocation.py — work-type allocation (ranked bar)
# Both original specs follow verbatim, separated by the `---` YAML document break.
# Edit each slide within its own document.
# ══════════════════════════════════════════════════════════════════════════════

# SlideSpec — DDG sam_taxonomy
# Body slide 10. Shape-built taxonomy tree (7 named buckets + residual) plus a
# compact bucket->scenario membership cue. The conceptual bridge from TAM to SAM.
# No native chart; this slide defines the bucket architecture, not the allocation.

meta:
  slide_id: ddg-s10
  slide_order: 10
  module_name: sam_taxonomy.py
  slide_type: body
  section: SAM and Work Types
  archetype: taxonomy_tree_plus_membership_matrix
  story_role: Define the work-type bucket architecture (seven named buckets + an explicit residual) and the scenario membership rules before work_type_allocation (S11) sizes the buckets and sam_scenarios (S12) sizes the SAM menu.
  inputs:
    - SAM Build §2a (observed bucket shares + Inputs adjustment; explicit residual)
    - SAM Build §3b (bucket TAM = portfolio TAM x modeled share) and §4a (scenario SAM)
    - Scenarios tab inputs_scenarios.SCENARIOS (bucket->scenario inclusion sets + prose definitions)
    - Worktype Evidence §1 (bucket map definitions) and §2 (top vendors by bucket)
    - _taxonomy.BUCKETS (the seven-bucket vocabulary + description / NAICS-4 crosswalk)
  related_appendix:
    - ddg-a6   # appendix_bucket_rules_supplier_evidence (bucket -> scenario rules + supplier evidence)
    - ddg-a2   # appendix_tam_calculation (portfolio TAM the SAM cuts apply to)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: SAM taxonomy
  title_topic: SAM Taxonomy
  title_finding: SAM is a work-type bucket menu, not a capture forecast
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - FAR 52.204-10
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122"

story:
  objective: Transition from TAM to SAM by defining the named bucket menu, keeping the unbucketed residual explicit, and showing that the five scenarios are alternative inclusion cuts of the same seven buckets, never additive pools.
  do_not_say:
    - Do not imply SAM is SOM, capture probability, or a win forecast.
    - Do not hide or zero out the unbucketed and ambiguous residual.
    - Do not imply the scenario definitions are additive.
    - No company logos; this is a text-chip taxonomy.
  known_caveats:
    - Scenario buckets overlap by design; for example, machining appears in both metal components and HM&E components, so scenario sizes must never be summed.
    - The unbucketed residual is evidence ambiguity (parent-unknown, GFE-adjacent specialty, or no clean description or NAICS cue), not a statement that those dollars are unreachable.
    - This slide carries no bar lengths; bucket sizing lives on work_type_allocation (S11) and sam_scenarios (S12).

object_assessment:
  verdict: "This is the only intentional card-chip page in the SAM section. Make every bucket chip explicit and keep the residual visually different."
  object_contract:
    render_pattern: taxonomy_chip_tree_plus_native_membership_table
    expected_rendered_object_count: 12
    compound_objects:
      - {id: named_bucket_chips, child_count: 7, child_type: text_box_chip}
    required_focal_family: "Seven named buckets use BLUE_1 with GRAY_3 borders; residual is gray and black-outlined; TAM banner is the only dark anchor."
  anti_repetition:
    versus_tam_timing: "No chart."
    versus_work_type_allocation: "Define buckets here; size them with bars on S11."
    forbidden_defaults:
      - Do not make the membership cue a card grid; it is a native table.
      - Do not hide residual.

regions:
  coord_basis: BODY
  layout_pattern: taxonomy_tree_plus_membership_matrix
  tam_banner:        {x: 0%, y: 0%, w: 100%, h: 18%}
  bucket_structural: {x: 0%, y: 24%, w: 29%, h: fit_content}
  bucket_machining:  {x: 32%, y: 24%, w: 29%, h: fit_content}
  bucket_castings:   {x: 0%, y: 36%, w: 29%, h: fit_content}
  bucket_piping:     {x: 32%, y: 36%, w: 29%, h: fit_content}
  bucket_electrical: {x: 0%, y: 48%, w: 29%, h: fit_content}
  bucket_hvac:       {x: 32%, y: 48%, w: 29%, h: fit_content}
  bucket_coatings:   {x: 0%, y: 60%, w: 29%, h: fit_content}
  residual_chip:     {x: 67%, y: 24%, w: 33%, h: fit_content}
  main_note:         {x: 67%, y: below(residual_chip) + GAP, w: 33%, h: fit_content}
  scenario_matrix:   {x: 0%, y: 76%, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: diagram, region: tam_banner, prominence: primary, paint_order: 1, content: portfolio TAM banner, tie_out: SAM Build §3a / TAM Build portfolio_tam}
  - {id: e2, type: diagram, region: bucket_structural, prominence: secondary, paint_order: 2, content: structural fabrication chip}
  - {id: e3, type: diagram, region: bucket_machining, prominence: secondary, paint_order: 2, content: machining chip}
  - {id: e4, type: diagram, region: bucket_castings, prominence: secondary, paint_order: 2, content: castings and forgings chip}
  - {id: e5, type: diagram, region: bucket_piping, prominence: secondary, paint_order: 2, content: piping valves and pumps chip}
  - {id: e6, type: diagram, region: bucket_electrical, prominence: secondary, paint_order: 2, content: electrical and power chip}
  - {id: e7, type: diagram, region: bucket_hvac, prominence: secondary, paint_order: 2, content: HVAC and ventilation chip}
  - {id: e8, type: diagram, region: bucket_coatings, prominence: secondary, paint_order: 2, content: coatings and insulation chip}
  - {id: e9, type: callout, region: residual_chip, prominence: secondary, paint_order: 3, content: unbucketed and ambiguous residual chip, tie_out: SAM Build §3b unbucketed_tam_cell}
  - {id: e10, type: rail, region: main_note, prominence: tertiary, paint_order: 4, content: SAM is not capture forecast note}
  - {id: e11, type: table, region: scenario_matrix, prominence: secondary, paint_order: 5, content: scenario membership cue, tie_out: Scenarios tab inputs_scenarios.SCENARIOS}

typography:
  contract:
    font: FONT
    line_spacing: LNSPC_BODY
    body_runs_explicit: true
    chrome_inherits: true
    emphasis_rule: "bold, italic, and ALL CAPS stay explicit at the run/call site"
    color_rule: "DK on light or no fill; WHITE on BLUE_3, BLUE_4, BLUE_5, and GRAY_5"
    chart_size_note: "Chart *_size_pt params are API point integers; all slide text_box/table sizes use style tokens or table render.size."
  defaults:
    external_exhibit_title: {size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
    no_fill_note: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
    no_fill_commentary_rail: {lead_size: DENSE_BODY_10PT, lead_bold: true, body_size: LABEL_9PT, color: DK, font: FONT}
    chip: {cap_size: LABEL_9PT, cap_bold: true, body_size: FINEPRINT_8_5PT, font: FONT}
    table_cells: {size_source: "tables[].render.size", font: FONT, row_height_source: estimate_row_heights}
  chart_rules: []
  table_rules:
    - table: scenario_membership_1
      element: e11
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: tam_banner_1
      element: e1
      profile: primary_kpi_or_output_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: WHITE, font: FONT}
        - {role: value, size: RIBBON_KPI_18PT, bold: true, color: WHITE, font: FONT}
        - {role: qualifier, size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
      note: "Value line dominates; cumulative or qualifier line stays smaller than the annual value."
    - shape: bucket_structural_1
      element: e2
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_machining_1
      element: e3
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_castings_1
      element: e4
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_piping_1
      element: e5
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_electrical_1
      element: e6
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_hvac_1
      element: e7
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: bucket_coatings_1
      element: e8
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: residual_1
      element: e9
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: main_note_1
      element: e10
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Lead/body paragraphs; keep no fill/no border and do not render as chips."

charts: []
images: []

shapes:
  - id: tam_banner_1
    element: e1
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    insets: INSETS_ANSWER_CARD
    text:
      paragraphs:
        - {lead: "PORTFOLIO TAM", body: ""}
        - {lead: "~$573M per year", body: "(~$3.44B FY22 to FY27 cumulative)"}
    meaning: Full-portfolio anchor from which SAM buckets are selected; banner text avoids visible plus or slash separators.
  - id: bucket_structural_1
    element: e2
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Structural fabrication and pre-outfit"
    meaning: Named work-type bucket; included in metal, modular, and broad scenarios.
  - id: bucket_machining_1
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Machining"
    meaning: Named work-type bucket; included in metal, HM&E, and broad scenarios.
  - id: bucket_castings_1
    element: e4
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Castings and forgings"
    meaning: Named work-type bucket; included in metal and broad scenarios.
  - id: bucket_piping_1
    element: e5
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Piping, valves, and pumps"
    meaning: Named work-type bucket; included in HM&E and broad scenarios.
  - id: bucket_electrical_1
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Electrical and power"
    meaning: Named work-type bucket; the standalone electrical scenario and part of broad.
  - id: bucket_hvac_1
    element: e7
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "HVAC and ventilation"
    meaning: Named work-type bucket; included in HM&E and broad scenarios.
  - id: bucket_coatings_1
    element: e8
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Coatings and insulation"
    meaning: Named work-type bucket; included in modular and broad scenarios.
  - id: residual_1
    element: e9
    factory: text_box
    fill: GRAY_3
    line_color: GRAY_3
    insets: INSETS_CARD
    text:
      paragraphs:
        - {lead: "Unbucketed / ambiguous", body: ""}
        - {lead: "~$246M per year", body: "42.9% of TAM"}
    meaning: Keeps evidence ambiguity explicit rather than forcing ambiguous dollars into named buckets; canonical slash label preserved.
  - id: main_note_1
    element: e10
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "SAM selects from named work-type buckets inside TAM. It does not apply win probability, capture probability, or SOM. Residual ambiguity remains explicit."
    meaning: Conceptual guardrail distinguishing SAM from a capture forecast and from SOM.

tables:
  - id: scenario_membership_1
    element: e11
    role: chart_side_evidence
    factory: house_table
    semantic:
      table_name: Scenario membership cue
      purpose: define
      reader_takeaway: Scenarios are alternative inclusion cuts of the same named buckets, not additive pools.
      row_order: scenarios in menu order (metal, HM&E, electrical, modular, broad)
      highlight_rows: ["Broad component manufacturing"]
      guardrails:
        - Membership must match the Scenarios tab inclusion sets exactly (Metal = structural, machining, castings; HM&E = machining, piping, HVAC; Electrical = electrical; Modular = structural, coatings; Broad = all seven).
        - Do not sum scenarios.
        - Keep the residual outside named scenario buckets.
    render:
      table_skin: rule
      size: 900
      column_widths:
        mode: ratio
        values: [1.6, 3.0]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Scenario", "Named bucket membership"]
        - ["Metal components", "Structural, machining, castings"]
        - ["HM&E components", "Machining, piping, HVAC"]
        - ["Electrical and power", "Electrical only"]
        - ["Modular assemblies", "Structural, coatings"]
        - ["Broad component manufacturing", "All seven named buckets"]
      cell_fills: {}
      cell_bold:
        "(5,0)": true
        "(5,1)": true
      cell_text_colors: {}
      footnotes:
        - "Scenarios are alternative serviceable-market definitions and should not be summed."
    columns: []

commentary:
  visible:
    element: e10
    container: right_rail
    title: Concept guardrail
    bullets:
      - {lead: "SAM:", body: "a work-type bucket menu, not SOM, capture probability, or a win forecast."}
      - {lead: "Residual:", body: "real evidence ambiguity, shown rather than hidden."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the conceptual bridge from TAM to SAM and the open of
      the SAM section (S10 sam_taxonomy -> S11 work_type_allocation -> S12 sam_scenarios).
      It defines the bucket architecture, so it should read cleaner than the next two data
      slides, which carry the numeric weight. The basis is the non-GFE DDG-51 supplier TAM
      of ~$573M/yr (~$3.44B cumulative FY22-27), built from two streams: Basic Construction
      ~$365M/yr (~$2.19B) and AP and LLTM ~$208M/yr (~$1.25B). [tie-out: TAM Build §5;
      SAM Build §3a]

      THE SEVEN NAMED BUCKETS (the _taxonomy.BUCKETS vocabulary; description-led
      classifier, with vendor-name override and NAICS-4 crosswalk as fallbacks).
      - Structural fabrication and pre-outfit: hull sections, fabricated structural metal,
        deckhouse, foundations, pre-outfit modules. (~$101M/yr; 17.7% of TAM.)
      - Machining: machine shops, precision/CNC machining, mechanical power transmission,
        gears, shafts, bearings. (~$66M/yr; 11.4%.)
      - Castings and forgings: iron/steel forging, steel foundries, cast components.
        (~$3M/yr; 0.5%.)
      - Piping, valves, and pumps: industrial valves, pumps, manifolds, pipe and fittings,
        hydraulics, flanges, strainers. (~$13M/yr; 2.3%.)
      - Electrical and power: switchgear, switchboards, cable, wiring, power distribution,
        generators, motors, transformers, circuits, controllers. (~$132M/yr; 23.0% — the
        largest single named bucket.)
      - HVAC and ventilation: air conditioning, chilled water, warm-air heating, shipboard
        ventilation, air-handling units, fan coils, ductwork. (~$10M/yr; 1.7%.)
      - Coatings and insulation: coatings, paint, deck covering, insulation, rubber,
        synthetic, composites, preservation, non-skid. (~$3M/yr; 0.5%.)
      [tie-out: SAM Build §3b / CD07_BUCKET_TAM; Worktype Evidence §1]

      THE RESIDUAL (kept explicit by design). The unbucketed / ambiguous residual is
      ~$246M/yr (~$1.47B cumulative; 42.9% of TAM). It captures parent-unknown,
      GFE-adjacent specialty, holding-company (NAICS 5511), or records with no clean
      description or NAICS cue. The model refuses to force it into a named bucket; broad
      SAM = TAM less this residual. Hiding it would overstate the precision of the bucket
      model. [tie-out: SAM Build §2a unbucketed_share_cell; §3b unbucketed_tam_cell]

      THE FIVE SCENARIOS ARE INCLUSION CUTS, NOT POOLS. Each scenario is a different subset
      of the same seven buckets, sized by SUMPRODUCT(bucket-TAM range, scenario 0/1 flags):
      Metal = structural + machining + castings (~$170M/yr); HM&E = machining + piping +
      HVAC (~$89M/yr); Electrical = electrical alone (~$132M/yr); Modular = structural +
      coatings (~$104M/yr); Broad = all seven (~$327M/yr; 57.1% of TAM). Because they share
      buckets (machining in both metal and HM&E; structural in metal, modular and broad),
      summing them double-counts. The reader should leave knowing not to sum the scenarios
      and not to read SAM as SOM. [tie-out: Scenarios tab inputs_scenarios.SCENARIOS;
      SAM Build §4a]

      SUPPLIER TEXTURE BEHIND THE NAMED BUCKETS (names only, a floor, not a target list).
      Visible first-tier flow gives proof points per bucket: Major Tool and Machine
      (~$816M visible) anchors machining/metal; Leonardo via DRS (~$1.81B) and CAES
      (~$169M) anchor electrical; Johnson Controls Navy Systems (~$178M) anchors HVAC.
      Supplier evidence is sourced from the parent-level Vendors tab (nc_lifetime_vendors),
      NOT z_ChartData CD09, which is bucket-split and drops GFE/prime-named firms.
      [tie-out: Vendors tab; nc_lifetime_vendors.csv; wiki 06]

      DENSITY GUIDANCE. Default is the banner + seven chips + residual chip + guardrail
      note + membership cue. To densify, add bucket one-line definitions inside the chips
      or a membership footnote; avoid adding bar lengths (those belong on S11/S12) and
      avoid logos.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11]}
      dense:  {add_bullets: 3, safe_containers: [main_note, residual_chip, scenario_matrix], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Broad SAM:", body: "The seven named buckets comprise broad component SAM of ~$327M per year, or 57.1% of TAM; broad excludes the residual.", evidence: "SAM Build §4a / CD08", safe_container: tam_banner, density_trigger: "Add if a numeric bridge is needed on the taxonomy slide."}
      - {priority: 2, lead: "Residual:", body: "Unbucketed and ambiguous is ~$246M per year, 42.9% of TAM; it is evidence ambiguity, not zero market.", evidence: "SAM Build §2a unbucketed_share_cell", safe_container: residual_chip, density_trigger: "Add if the residual chip has room."}
      - {priority: 3, lead: "No capture:", body: "SAM buckets are not win probability, capture probability, or SOM; SAM is a strict subset of TAM.", evidence: "SAM Build §4b note", safe_container: main_note, density_trigger: "Always safe as a guardrail."}
      - {priority: 4, lead: "Overlap:", body: "Machining sits in both metal and HM&E, and structural in metal, modular, and broad, so scenario outputs must never be summed.", evidence: "Scenarios tab inclusion sets", safe_container: scenario_matrix, density_trigger: "Add as a matrix footnote if needed."}
      - {priority: 5, lead: "Electrical is largest named:", body: "Electrical and power is the largest single named bucket (~$132M per year, 23.0% of TAM) and the standalone electrical scenario.", evidence: "SAM Build §3b / CD07", safe_container: bucket_electrical, density_trigger: "Add in a dense explainer version."}
      - {priority: 6, lead: "Description-led:", body: "Buckets are assigned by award description first (e.g. valve to piping), then vendor-name override, then NAICS-4 fallback; that ordering produces the residual.", evidence: "_taxonomy.classify; Worktype Evidence §3", safe_container: main_note, density_trigger: "Add if the audience asks how buckets are assigned."}
      - {priority: 7, lead: "HM&E cue:", body: "HM&E includes machining, piping, and HVAC, but not electrical in this scenario menu.", evidence: "Scenarios tab inclusion sets", safe_container: scenario_matrix, density_trigger: "Add when using a compact tag rail instead of the table."}
      - {priority: 8, lead: "Supplier proof point:", body: "Major Tool and Machine (~$816M visible) anchors machining; Leonardo via DRS (~$1.81B) anchors electrical; both are floors, not targets.", evidence: "Vendors tab (parent-level); wiki 06", safe_container: scenario_matrix, density_trigger: "Add if the matrix is replaced by a tag rail with spare room."}
      - {priority: 9, lead: "Supplier evidence source:", body: "Bucket supplier evidence comes from the parent-level Vendors tab, not z_ChartData CD09, which is bucket-split and drops GFE and prime-named firms.", evidence: "data_vendors.tbl_ddg_top_vendors; chartdata_z_chart_data.py", safe_container: main_note, density_trigger: "Add as a method note if a reviewer asks where supplier figures come from."}
      - {priority: 10, lead: "Residual outside broad:", body: "The named bucket list is the source menu for serviceable-market scenarios; the residual stays outside the named menu and outside broad SAM.", evidence: "SAM Build §3b / §4b", safe_container: main_note, density_trigger: "Add if the audience asks whether the residual is inside broad SAM."}
    do_not_add:
      - Any summed scenario total.
      - Company logos.
      - Capture probability, win probability, or SOM framing.
      - Bar lengths or bucket sizing as a chart (that lives on S11 and S12).

data_and_calculations:
  data_inputs:
    - {input: Portfolio TAM basis, value: 573, unit: "$M per year", cumulative: 3.44, tie_out: "SAM Build §3a / TAM Build portfolio_tam", used_in: tam_banner_1}
    - {input: Broad component SAM, value: 327, unit: "$M per year", cumulative: 1.96, share_of_tam: "57.1%", tie_out: "SAM Build §4a / CD08", used_in: scenario_membership_1}
    - {input: Unbucketed and ambiguous residual, value: 246, unit: "$M per year", cumulative: 1.47, share_of_tam: "42.9%", tie_out: "SAM Build §2a / §3b unbucketed_tam_cell", used_in: residual_1}
  calculations:
    - {name: bucket TAM, formula: portfolio TAM x modeled bucket share (observed subaward share + Inputs adjustment), output: per-bucket $M, used_in: scenario_membership_1}
    - {name: residual share, formula: 1 - SUM(7 named bucket modeled shares), output: 42.9% (~$246M/yr), used_in: residual_1}
    - {name: scenario SAM, formula: SUMPRODUCT(bucket-TAM range, scenario 0/1 inclusion flags), output: per-scenario $M, used_in: scenario_membership_1}
  rounding_rules: Whole $M in visible text; share-of-TAM to one decimal where shown; $B to two decimals for cumulative.
  reconciliation: Seven named buckets plus the residual reconcile to portfolio TAM by construction; scenarios are alternative overlapping cuts and are NOT additive.

qa:
  guardrails:
    - All seven named buckets appear (structural, machining, castings, piping, electrical, HVAC, coatings).
    - Unbucketed / ambiguous appears explicitly with the canonical slash label.
    - Slide states SAM is not SOM and not a capture forecast.
    - Scenario membership matches the Scenarios tab inclusion sets and does not imply additivity.
    - No visible plus or slash separators in rendered text except the canonical "Unbucketed / ambiguous" label.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal worksheets, workbook tabs, chart IDs, CSVs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "no chart rIds required because charts is empty"
    - "slide_probe --table-fit"
    - "resolved column widths sum to the scenario_matrix region width"

---

# SlideSpec — DDG work_type_allocation
# Body slide 11. Full-width ranked horizontal bar of portfolio TAM by work type plus
# a single gray residual cue. No right rail and no table.

meta:
  slide_id: ddg-s11
  slide_order: 11
  module_name: work_type_allocation.py
  slide_type: body
  section: SAM and Work Types
  archetype: full_width_ranked_bar_with_residual_cue
  story_role: Show the full work-type distribution of portfolio TAM, name the largest targetable buckets (electrical, structural, machining), and keep the residual ambiguity visible before sam_scenarios (S12) sizes the SAM menu.
  inputs:
    - SAM Build §3b (bucket TAM = portfolio TAM x modeled share; ranked work-type allocation)
    - SAM Build §2a (observed bucket shares + Inputs adjustment; explicit residual)
    - z_ChartData CD07_BUCKET_TAM (the chart producer; avg annual = cumulative / 6, share = cumulative / portfolio TAM)
    - Worktype Evidence §1/§2 (bucket definitions + top vendors by bucket)
  related_appendix:
    - ddg-a6   # appendix_bucket_rules_supplier_evidence (bucket -> scenario rules + supplier evidence)
    - ddg-a2   # appendix_tam_calculation (portfolio TAM the allocation distributes)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Work-type allocation
  title_topic: Work-Type Allocation
  title_finding: Residual ambiguity is the largest line, while electrical and structural are the largest named buckets
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - FAR 52.204-10
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122"

story:
  objective: Rank portfolio TAM by work type, identify the largest named buckets, and keep the unbucketed residual visible and visually distinct so the reader does not mistake it for a named target lane.
  do_not_say:
    - Do not hide or visually minimize the residual.
    - Do not color the residual the same way as the named SAM buckets.
    - Do not call the residual a target wedge.
    - Do not imply the small buckets are zero or irrelevant.
    - No company logos; supplier names only if referenced.
  known_caveats:
    - The residual is part of TAM but not part of broad component SAM.
    - Bars are modeled bucket TAM (portfolio TAM x modeled share), not summed FFATA subaward dollars; the supplier-$ behind a bucket is a separate visible-floor read.
    - Cumulative values are secondary and should not replace the average-annual chart values or retitle the chart.

object_assessment:
  verdict: "Aggressive redesign: remove the generic right rail. Use a full-width ranked bar and a single residual cue so S11 does not become the first of four chart-plus-rail slides."
  object_contract:
    render_pattern: full_width_ranked_bar_with_residual_cue
    expected_rendered_object_count: 4
    compound_objects: []
    required_focal_family: "Chart owns the page; residual cue is gray and subordinate. No chart-side rail."
  anti_repetition:
    versus_sam_taxonomy: "This sizes the buckets; no chip grid."
    versus_sam_scenarios: "S12 can use a right-side matrix because S11 does not."
    forbidden_defaults:
      - No right commentary rail.
      - No table.
      - Do not color residual like a named SAM bucket.

regions:
  coord_basis: BODY
  layout_pattern: full_width_ranked_bar_with_residual_cue
  title_band:     {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  chart:          {x: 0%, y: below(title_band), w: 100%, h: body_until(residual_cue)}
  residual_cue:   {x: 0%, y: BODY_B - NOTE_H - NOTE_H, w: 100%, h: NOTE_H}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,   prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,        prominence: primary,   paint_order: 2, content: full-width ranked horizontal bar of work-type TAM, tie_out: SAM Build §3b / CD07_BUCKET_TAM}
  - {id: e3, type: note,          region: residual_cue, prominence: secondary, paint_order: 3, content: gray residual cue under chart}
  - {id: e4, type: note,          region: note_strip,   prominence: tertiary,  paint_order: 4, content: standard sizing note}

typography:
  contract:
    font: FONT
    line_spacing: LNSPC_BODY
    body_runs_explicit: true
    chrome_inherits: true
    emphasis_rule: "bold, italic, and ALL CAPS stay explicit at the run/call site"
    color_rule: "DK on light or no fill; WHITE on BLUE_3, BLUE_4, BLUE_5, and GRAY_5"
    chart_size_note: "Chart *_size_pt params are API point integers; all slide text_box/table sizes use style tokens or table render.size."
  defaults:
    external_exhibit_title: {size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
    no_fill_note: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
    no_fill_commentary_rail: {lead_size: DENSE_BODY_10PT, lead_bold: true, body_size: LABEL_9PT, color: DK, font: FONT}
    chip: {cap_size: LABEL_9PT, cap_bold: true, body_size: FINEPRINT_8_5PT, font: FONT}
    table_cells: {size_source: "tables[].render.size", font: FONT, row_height_source: estimate_row_heights}
  chart_rules:
    - chart: chart_1
      title_element: e1
      external_title: {size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      native_title: null
      category_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      value_axis_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      data_labels: {size_pt_from: params.value_label_size_pt, color: auto_contrast, font: FONT}
      legend: {enabled: false}
  table_rules: []
  shape_rules:
    - shape: residual_cue_1
      element: e3
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: sizing_note_1
      element: e4
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Unbucketed / ambiguous (42.9%)"
        - "Electrical and power (23.0%)"
        - "Structural fabrication and pre-outfit (17.7%)"
        - "Machining (11.4%)"
        - "Piping, valves, and pumps (2.3%)"
        - "HVAC and ventilation (1.7%)"
        - "Coatings and insulation (0.5%)"
        - "Castings and forgings (0.5%)"
      series:
        - name: Average annual TAM
          values: [245.8, 131.8, 101.4, 65.6, 13.0, 9.9, 2.8, 2.7]
          data_point_colors: [GRAY_3, BLUE_5, BLUE_4, BLUE_3, BLUE_1, BLUE_1, BLUE_1, BLUE_1]
    params:
      mode: ranked          # single pre-sorted descending series; bar_chart reads top-to-bottom
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 50
      cat_header: Work type
      title: null           # house style: external exhibit_title element (e1)
    external_title:
      text: Portfolio TAM allocation by work type, average annual FY22-27
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Residual is evidence ambiguity; keep it visually distinct from named buckets.", anchor_to: e2}

tables: []

images: []

shapes:
  - id: residual_cue_1
    element: e3
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_EVIDENCE
    text: "Residual is evidence ambiguity, not a target lane. The seven named buckets sum to broad component SAM; the gray residual remains in TAM but outside broad SAM."
    meaning: Replaces the right rail with one residual cue and keeps the chart full-width.
  - id: sizing_note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note.

commentary:
  visible:
    element: e3
    container: right_rail
    title: Readout
    bullets:
      - {lead: "Residual:", body: "not a target wedge; it is evidence ambiguity that should remain visible."}
      - {lead: "Named lanes:", body: "electrical, structural, and machining are the largest targetable work-type buckets."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the first slide that shows the full bucket distribution
      (S10 sam_taxonomy -> S11 here -> S12 sam_scenarios). The bars are modeled bucket TAM =
      portfolio TAM (~$573M/yr; ~$3.44B cumulative FY22-27) x modeled bucket share, where
      modeled share = observed FFATA subaward share + Inputs adjustment. Average-annual bar
      values are cumulative / 6 years and category shares are cumulative / portfolio TAM, so
      the chart ties to SAM Build §3b by construction. [tie-out: SAM Build §3b /
      CD07_BUCKET_TAM]

      THE RANKING (average annual; share of the ~$573M/yr TAM).
      - Unbucketed / ambiguous ~$246M/yr (~$1.47B; 42.9%) — the largest single line. Keep it
        prominent and honest but gray, because it is evidence ambiguity (parent-unknown,
        GFE-adjacent specialty, holding-company NAICS 5511, or no clean description/NAICS
        cue), not a named target lane. It is part of TAM but excluded from broad component
        SAM (broad SAM = TAM less this residual).
      - Electrical and power ~$132M/yr (~$791M; 23.0%) — the largest named bucket and the
        standalone electrical scenario.
      - Structural fabrication and pre-outfit ~$101M/yr (~$608M; 17.7%).
      - Machining ~$66M/yr (~$394M; 11.4%) — the third core metal-component lane.
      - Piping, valves, and pumps ~$13M/yr (~$78M; 2.3%); HVAC and ventilation ~$10M/yr
        (~$59M; 1.7%); coatings and insulation ~$3M/yr (~$17M; 0.5%); castings and forgings
        ~$3M/yr (~$16M; 0.5%). Small but not zero; labels can sit outside the bars.
      The seven named buckets sum to ~$327M/yr (57.1% of TAM = broad SAM); +42.9% residual =
      100%. The metal-components scenario (structural + machining + castings ~$170M/yr) reads
      across three of these bars. [tie-out: SAM Build §3b / §4a; CD07]

      MODELED TAM vs OBSERVED SUPPLIER-$ — TWO DIFFERENT READS. The bars rank modeled TAM,
      not summed subaward dollars. The observed supplier-$ texture is consistent: electrical
      is also the largest observed supplier-$ bucket (Leonardo via DRS ~$1.81B visible, CAES
      ~$169M), but combat-system electrical/power work is largely GFE-directed and
      qualification-heavy, so a large bucket is not a clear open-market target. Machining is
      anchored by Major Tool and Machine (~$816M visible; ~$948M consolidated across two
      UEIs), structural by yard-side fabrication subs, HVAC by Johnson Controls Navy Systems
      (~$178M). [tie-out: Vendors tab; wiki 06; wiki 10/11]

      SUPPLIER-EVIDENCE SOURCE DISCIPLINE (load-bearing). When citing supplier-$ behind a
      bucket, source it from the parent-level Vendors tab (data_vendors.tbl_ddg_top_vendors /
      nc_lifetime_vendors.csv), NOT z_ChartData CD09_TOP_SUPPLIERS. CD09 is bucket-split (one
      row per vendor x UEI x role x bucket) and drops GFE/MIB-named and prime-named firms via
      the role=="supplier" filter, so it understates electrical and omits Leonardo/DRS,
      Northrop Grumman, GD, etc. NAICS is a corporate-primary code, not the work performed:
      ~35% of the top-150 vendors (~$2.28B of dollar value) return no NAICS in SAM Entity
      Management, and several top firms (Leonardo, GE, Northrop Grumman) carry aerospace
      NAICS 3364 despite naval product lines. [tie-out: chartdata_z_chart_data.py;
      entity_naics_lookup.csv; wiki 06]

      THE FFATA FLOOR THAT BOUNDS THE OBSERVED-$ READ. Visible first-tier flow is a floor:
      ~$13.84B cumulative in-scope across 1,954 parent vendors, but FFATA captures only
      ~15-20% of real yard-side outsourcing (S14 ffata_visibility_gap). The bucket TAM here
      is modeled from the supplier-addressable corpus, not from summing FFATA; do not read
      bar magnitudes as either summed subawards or a target list.

      DENSITY GUIDANCE. Default is chart + interpretation rail + sizing note. To densify, add
      a metal-trio or residual line to the rail, or a small footnote under the chart. Keep
      the residual gray and visible; the chart owns the page.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [residual_cue, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Residual:", body: "~$246M per year and 42.9% of TAM is unbucketed and ambiguous; keep it visible but gray, distinct from named buckets.", evidence: "SAM Build §2a / §3b; CD07_BUCKET_TAM", safe_container: rail, density_trigger: "Add if the chart label cannot carry the residual interpretation."}
      - {priority: 2, lead: "Electrical:", body: "Electrical and power is the largest named bucket at ~$132M per year, or 23.0% of TAM; it is also the largest observed supplier-$ bucket.", evidence: "SAM Build §3b; Vendors tab", safe_container: rail, density_trigger: "Add if the rail can take a third bullet."}
      - {priority: 3, lead: "Electrical is GFE-heavy:", body: "Combat-system electrical and power work is largely GFE-directed and qualification-heavy, so a large bucket is not a clean open-market target.", evidence: "wiki 10/11; SAM Build §2b GFE exclusion", safe_container: note_strip, density_trigger: "Add when discussing electrical as a target lane."}
      - {priority: 4, lead: "Structural:", body: "Structural fabrication and pre-outfit is the second-largest named bucket at ~$101M per year, or 17.7% of TAM.", evidence: "SAM Build §3b / CD07", safe_container: rail, density_trigger: "Add in a dense version focused on target lanes."}
      - {priority: 5, lead: "Machining:", body: "Machining adds a third core metal-component lane at ~$66M per year, or 11.4%; anchored by Major Tool and Machine (~$816M visible).", evidence: "SAM Build §3b; Vendors tab", safe_container: rail, density_trigger: "Add if the metal-components interpretation is important."}
      - {priority: 6, lead: "Small buckets:", body: "Piping, HVAC, coatings, and castings are small (each under 2.5% of TAM) but should not disappear; labels can sit outside the bars.", evidence: "SAM Build §3b / CD07", safe_container: note_strip, density_trigger: "Add if the small labels are compressed."}
      - {priority: 7, lead: "Modeled, not summed:", body: "Bars are modeled bucket TAM (portfolio TAM x modeled share), not summed FFATA subaward dollars.", evidence: "SAM Build §3b", safe_container: note_strip, density_trigger: "Add if a reader reads bars as summed subawards."}
      - {priority: 8, lead: "Broad SAM boundary:", body: "The seven named buckets sum to ~$327M per year (57.1% of TAM = broad SAM); the residual is part of TAM but outside broad SAM.", evidence: "SAM Build §4a / §4b", safe_container: rail, density_trigger: "Add if SAM scenario discussion follows immediately."}
      - {priority: 9, lead: "Supplier evidence source:", body: "Cite supplier-$ behind a bucket from the parent-level Vendors tab, not z_ChartData CD09, which is bucket-split and drops GFE and prime-named firms.", evidence: "data_vendors.tbl_ddg_top_vendors; chartdata_z_chart_data.py", safe_container: note_strip, density_trigger: "Add as a method note if a reviewer asks where supplier figures come from."}
      - {priority: 10, lead: "NAICS caveat:", body: "NAICS is a corporate-primary code, not the work performed; ~35% of top-150 vendors return no NAICS (~$2.28B unclassified).", evidence: "wiki 06; entity_naics_lookup.csv", safe_container: note_strip, density_trigger: "Add if a reviewer reads NAICS labels as the work type."}
      - {priority: 11, lead: "FFATA is a floor:", body: "Visible first-tier flow (~$13.84B cumulative) is ~15-20% of estimated yard-side outsourcing; bucket TAM is modeled, not summed FFATA.", evidence: "wiki 05/09; ffata_visibility_gap (S14)", safe_container: note_strip, density_trigger: "Add if magnitudes are compared to visible subaward totals."}
    do_not_add:
      - Residual rendered as a named target bucket or in a blue ramp color.
      - A source line containing internal workbook tabs, chart IDs, CSVs, or wiki chapters.
      - A chart sorted by cumulative values instead of average-annual values.
      - Company logos.

data_and_calculations:
  data_inputs:
    - {input: Unbucketed / ambiguous, value: 245.8, unit: "$M per year", cumulative: 1474.8, share_of_tam: "42.9%", tie_out: "SAM Build §3b unbucketed_tam_cell / CD07", used_in: chart_1}
    - {input: Electrical and power, value: 131.8, unit: "$M per year", cumulative: 791.0, share_of_tam: "23.0%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: Structural fabrication and pre-outfit, value: 101.4, unit: "$M per year", cumulative: 608.4, share_of_tam: "17.7%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: Machining, value: 65.6, unit: "$M per year", cumulative: 393.6, share_of_tam: "11.4%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: Piping, valves, and pumps, value: 13.0, unit: "$M per year", cumulative: 78.0, share_of_tam: "2.3%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: HVAC and ventilation, value: 9.9, unit: "$M per year", cumulative: 59.4, share_of_tam: "1.7%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: Coatings and insulation, value: 2.8, unit: "$M per year", cumulative: 16.8, share_of_tam: "0.5%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
    - {input: Castings and forgings, value: 2.7, unit: "$M per year", cumulative: 16.2, share_of_tam: "0.5%", tie_out: "SAM Build §3b / CD07", used_in: chart_1}
  calculations:
    - {name: bucket TAM (cumulative), formula: portfolio TAM (~$3.44B) x modeled bucket share, output: per-bucket cumulative $M, used_in: chart_1}
    - {name: avg-annual bucket TAM, formula: cumulative bucket TAM / 6 portfolio years, output: per-bucket $M/yr (bar length), used_in: chart_1}
    - {name: share of TAM, formula: cumulative bucket TAM / portfolio TAM, output: percent (category label), used_in: chart_1}
    - {name: named-bucket / scenario tie, formula: structural + machining + castings = metal (~$170M/yr); all seven = broad (~$327M/yr), output: cross-check vs sam_scenarios (S12), used_in: chart_1}
  rounding_rules: Whole $M in data labels; share-of-TAM to one decimal in category labels; $B to two decimals for cumulative in reserve.
  reconciliation: Seven named buckets (~$327M/yr) plus the residual (~$246M/yr) sum to portfolio TAM (~$573M/yr) by construction. Scenario SAM cross-checks (metal = structural+machining+castings = ~$170M/yr; broad = all seven = ~$327M/yr) tie to sam_scenarios (S12). Cumulative values are secondary.

qa:
  guardrails:
    - Residual is visible, labeled "Unbucketed / ambiguous," and gray (GRAY_3), distinct from the blue named buckets.
    - Electrical and structural are the largest named buckets; machining is third.
    - Chart is sorted descending by average-annual value, not cumulative.
    - Bars are modeled bucket TAM, not summed FFATA subaward dollars; values are annual unless the chart is clearly retitled.
    - If supplier-$ evidence is shown, it is sourced from the parent-level Vendors tab, not z_ChartData CD09.
    - No visible plus or slash separators in rendered category labels, bar labels, rail, or note.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal workbook tabs, chart IDs, CSVs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    # no table on this slide -> table-fit / column-width checks do not apply
