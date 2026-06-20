# Worked example — DDG `sam_scenarios` (SlideSpec format)
# Demonstrates required-if-present for BOTH a chart and a table, the closed region grammar,
# and exhibit blocks referencing element_inventory ids (no repeated region fields).
# Source data: projects/ddg/deck/slide_specs/sam_scenarios.md (deck slide 12).

meta:
  slide_id: ddg-s12
  slide_order: 12
  module_name: sam_scenarios.py
  slide_type: body
  section: SAM and Work Types
  archetype: ranked_bar_plus_right_matrix
  story_role: Pay off the SAM setup — size the serviceable-market menu the deck promised at S10–S11.
  inputs:
    - z_ChartData CD08_SAM_SCENARIOS
    - SAM Build section 4a (scenario values)
    - Scenarios tab (inclusion flags + definitions)
    - Deck Outputs DO-37 .. DO-46
  related_appendix:
    - ddg-a6   # appendix_bucket_rules_supplier_evidence (bucket -> scenario rules)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: SAM scenarios
  title_topic: SAM Scenarios
  title_finding: Broad component manufacturing represents ~$327M per year of serviceable market
  layout: slideLayout4        # -> module-level LAYOUT
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - FAR 52.204-10
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122"

story:
  objective: Show the five scenario sizes and make it unmistakable that scenarios are alternative definitions, not additive segments.
  do_not_say:
    - No SOM, capture probability, or win rate.
    - Never present a summed scenario total.
  known_caveats:
    - Broad is the largest scenario only because it includes all seven named buckets.
    - HM&E overlaps machining; it is not additive to metal.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_right_matrix
  title_band: {x: 0%, y: 0%, w: 62%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 62%, h: body_until(note_strip)}
  matrix:     {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,      prominence: primary,   paint_order: 2, content: ranked bar of 5 scenarios, tie_out: CD08}
  - {id: e3, type: table,         region: matrix,     prominence: secondary, paint_order: 3, content: bucket-to-scenario inclusion matrix, tie_out: Scenarios tab}
  - {id: e4, type: note,          region: note_strip, prominence: tertiary,  paint_order: 4, content: standard sizing note}

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Broad component manufacturing (57.1%)"
        - "Metal components (29.6%)"
        - "Electrical and power (23.0%)"
        - "Modular assemblies (18.2%)"
        - "HM&E components (15.4%)"
      series:
        - name: Average annual SAM
          values: [327.3, 169.7, 131.8, 104.3, 88.5]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_3, BLUE_2, BLUE_1]
    params:
      mode: ranked
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 45
      cat_header: Scenario
      title: null
    external_title:
      text: SAM scenarios, average annual FY22-27
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations: []

tables:
  - id: matrix_1
    element: e3
    role: chart_side_evidence
    factory: house_table
    semantic:
      table_name: Scenario inclusion cue
      purpose: define     # which buckets each scenario includes; not additive
      reader_takeaway: Each scenario is a different inclusion cut of the same seven buckets.
      row_order: structural, machining, castings, piping, electrical, HVAC, coatings
      highlight_rows: []
      guardrails:
        - Scenarios overlap; do not sum.
    render:
      table_skin: rule
      size: 900               # 9.0pt (== LABEL_9PT); row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [3.4, 1.0, 1.0, 1.0, 1.0, 1.0]   # bucket col wide; 5 flag cols equal
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "ctr", "ctr", "ctr", "ctr", "ctr"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Bucket",      "Metal", "HM&E", "Elec", "Modular", "Broad"]
        - ["Structural",  "Yes",   "No",   "No",   "Yes",     "Yes"]
        - ["Machining",   "Yes",   "Yes",  "No",   "No",      "Yes"]
        - ["Castings",    "Yes",   "No",   "No",   "No",      "Yes"]
        - ["Piping",      "No",    "Yes",  "No",   "No",      "Yes"]
        - ["Electrical",  "No",    "No",   "Yes",  "No",      "Yes"]
        - ["HVAC",        "No",    "Yes",  "No",   "No",      "Yes"]
        - ["Coatings",    "No",    "No",   "No",   "Yes",     "Yes"]
      cell_fills: {}           # first column auto-bolds via house_table; rule skin keeps it light
      cell_bold:               # bold the "Yes" hits so membership reads at a glance
        "(1,1)": true, "(1,4)": true, "(1,5)": true
        "(2,1)": true, "(2,2)": true, "(2,5)": true
        "(3,1)": true, "(3,5)": true
        "(4,2)": true, "(4,5)": true
        "(5,3)": true, "(5,5)": true
        "(6,2)": true, "(6,5)": true
        "(7,4)": true, "(7,5)": true
      footnotes:
        - "Scenarios are alternative serviceable-market definitions. Do not sum them."
    columns: []

shapes:
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note; reinforces the average-annual convention and the SOM exclusion.

commentary:
  visible:
    element: e3
    container: table_note
    title:
    bullets:
      - {lead: "Read:", body: "Broad is the envelope; metal is the largest single targetable wedge."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the payoff of the SAM section (S10 taxonomy -> S11
      work-type allocation -> S12 here). The deck's headline is a non-GFE DDG-51 supplier
      TAM of ~$573M per year (~$3.44B cumulative FY22-27), built from two streams: Basic
      Construction (~$365M/yr) and AP and LLTM (~$208M/yr). This slide cuts that TAM into
      five overlapping serviceable-market definitions. Per-hull framing: ~$265M supplier
      TAM per in-window hull across 13 hulls.

      THE FIVE SCENARIOS AND WHY THEY RANK AS THEY DO.
      - Broad component manufacturing ~$327M/yr (~$1.96B; 57.1% of TAM) = all seven named
        buckets. Largest only because it is the union; an envelope, not a single wedge.
      - Metal components ~$170M/yr (~$1.02B; 29.6%) = structural fabrication + machining +
        castings/forgings. The largest scenario that reads cleanly as one wedge, so usually
        the most useful for a "where to play" conversation.
      - Electrical and power ~$132M/yr (~$791M; 23.0%) = the electrical bucket alone. Largest
        single named bucket, but narrower than metal as a scenario and qualification-heavy.
      - Modular assemblies ~$104M/yr (~$626M; 18.2%) = structural fabrication + coatings.
        Most aligned with the distributed-shipbuilding direction on S15 (market_direction),
        even though its current modeled size sits below broad/metal.
      - HM&E components ~$89M/yr (~$531M; 15.4%) = machining + piping + HVAC. Overlaps
        machining with the metal scenario, so the two must never be added together.

      WHY OVERLAP MATTERS. The five bars share buckets (machining in both metal and HM&E;
      structural in metal, modular and broad), so they are alternative cuts of one TAM, not
      five additive submarkets. Summing them double-counts.

      SUPPLIER PROOF POINTS (visible first-tier flow, FFATA). Led by Leonardo SpA ~$1.81B
      (electronics, electrical), Arctic Slope Regional Corp ~$987M (largely engineering
      services - caveat for a physical-components read), Major Tool and Machine ~$816M
      (machining -> metal), GE ~$336M, Rolls-Royce ~$257M, Northrop Grumman ~$249M. These
      name the visible suppliers behind the buckets; not a target list, not the denominator.

      THE FFATA CAVEAT THAT BOUNDS ALL OF THIS. Visible first-tier flow is a floor: ~$2.73B
      cumulative versus an estimated yard-side outsourcing midpoint of ~$13.57B (~20%
      visible). Scenarios are sized from modeled TAM, not by summing FFATA; S14
      (ffata_visibility_gap) carries this in full.

      DENSITY GUIDANCE. Default slide is chart + matrix + sizing note. To densify, the safest
      moves are (a) one explanatory line in the note strip, and (b) bolded membership already
      in the matrix. Avoid adding a fourth visual; this slide's job is clarity about overlap,
      not exhaustiveness.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [note_strip, matrix, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Metal vs broad:"
        body: "Metal components (~$170M) is the largest scenario you can describe as a single wedge; broad (~$327M) is an envelope, not a go-to-market."
        evidence: SAM Build section 4a
        safe_container: note_strip
        density_trigger: If the matrix compresses to a tag rail, free one body line for this.
      - priority: 2
        lead: "Electrical caveat:"
        body: "Electrical and power (~$132M) is the largest single named bucket but is narrower than metal as a scenario, and qualification-heavy."
        evidence: Work-Type Allocation (S11)
        safe_container: note_strip
        density_trigger: Add when the chart frame is shortened.
      - priority: 3
        lead: "No double-count:"
        body: "HM&E overlaps machining; never add HM&E to the metal scenario."
        evidence: Scenarios tab flags
        safe_container: matrix   # extend the existing footnote
        density_trigger: Add if a reviewer asks why scenarios are not summed.
      - priority: 4
        lead: "Modular = distributed-build lane:"
        body: "Modular assemblies (~$104M) is the scenario most aligned with the distributed-shipbuilding trajectory on S15."
        evidence: SAM Build 4a; market_direction (S15)
        safe_container: note_strip
        density_trigger: Add when presenting alongside the market-direction slide.
      - priority: 5
        lead: "Scale framing:"
        body: "~$327M/yr broad SAM = 57.1% of the ~$573M/yr portfolio TAM; ~$265M supplier TAM per hull across 13 hulls."
        evidence: TAM Build; Deck Outputs DO-01..DO-07
        safe_container: chart   # chart annotation
        density_trigger: Add if the chart has vertical headroom.
      - priority: 6
        lead: "Two streams:"
        body: "Portfolio TAM = Basic Construction (~$365M/yr) + AP and LLTM (~$208M/yr); SAM cuts apply to the combined TAM."
        evidence: appendix_tam_calculation (A2)
        safe_container: note_strip
        density_trigger: Add only if the audience has not seen the exec summary.
      - priority: 7
        lead: "Supplier proof point:"
        body: "Major Tool and Machine (~$816M visible) anchors the machining evidence behind metal; Leonardo (~$1.81B) behind electrical."
        evidence: Vendors sheet (parent-level)
        safe_container: matrix   # small note beneath the matrix
        density_trigger: Add if the matrix is replaced by a tag rail with spare room.
      - priority: 8
        lead: "FFATA is a floor:"
        body: "Scenario sizes come from modeled TAM, not summed subawards; visible FFATA flow is ~20% of estimated yard-side outsourcing."
        evidence: ffata_visibility_gap (S14)
        safe_container: note_strip
        density_trigger: Add if a reader assumes the bars are summed FFATA dollars.
      - priority: 9
        lead: "Residual is excluded here:"
        body: "Broad SAM already excludes the ~42.9% unbucketed/ambiguous residual carried in TAM; these five scenarios live inside the named buckets."
        evidence: SAM Taxonomy (S10)
        safe_container: chart
        density_trigger: Add only in a max-density appendix-style variant.
    do_not_add:
      - capture %, win-probability, or SOM language
      - any summed scenario total
      - company logos (names only in v1)

data_and_calculations:
  data_inputs:
    - {input: Broad component manufacturing, value: 327.3, unit: $M/yr, cumulative: 1962, share_of_tam: 57.1%, tie_out: SAM Build 4a, used_in: chart_1}
    - {input: Metal components,              value: 169.7, unit: $M/yr, cumulative: 1018, share_of_tam: 29.6%, tie_out: SAM Build 4a, used_in: chart_1}
    - {input: Electrical and power,          value: 131.8, unit: $M/yr, cumulative: 791,  share_of_tam: 23.0%, tie_out: SAM Build 4a, used_in: chart_1}
    - {input: Modular assemblies,            value: 104.3, unit: $M/yr, cumulative: 626,  share_of_tam: 18.2%, tie_out: SAM Build 4a, used_in: chart_1}
    - {input: HM&E components,               value: 88.5,  unit: $M/yr, cumulative: 531,  share_of_tam: 15.4%, tie_out: SAM Build 4a, used_in: chart_1}
  rounding_rules: Whole $M on the slide; share-of-TAM to one decimal in category labels.
  reconciliation: Scenarios are overlapping cuts of the same TAM; they are not expected to sum to portfolio TAM.

qa:
  guardrails:
    - Slide explicitly states scenarios are not additive and not SOM.
    - Broad is framed as the envelope, not a single wedge.
    - Matrix Yes/No flags match the Scenarios tab definitions exactly.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal docs, workbook tabs, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    - slide_probe --table-fit   # optional: estimated table row-height info
    - resolved column widths sum to the matrix region width
