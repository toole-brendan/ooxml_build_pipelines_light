# SlideSpec - submarines `sam_scenarios` (deck slide 14)
# Chart + commentary body slide: a ranked horizontal bar of the five SAM scenarios by
# average annual SAM, a no-fill interpretation rail naming each scenario's bucket
# composition, and one filled combined caveat strip that carries BOTH the "scenario SAM
# only, no SOM" guardrail AND the overlap / average-annual convention. No table here (the
# bucket-to-scenario mapping is carried as a rail, not a matrix).

meta:
  slide_id: subs-s14
  slide_order: 14               # deck-spec narrative position; not yet registered (KNOWN GAP, S12-S16)
  module_name: sam_scenarios.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: ranked_bar_plus_guardrail_strip
  story_role: Pay off the SAM setup - size the serviceable-market menu and make it unmistakable that scenarios are alternative definitions, not additive segments.
  inputs:
    - Chart Data CD_14_SAMScenarios
    - SAM Build section 6 (scenario SAM = SUMPRODUCT(bucket TAM, scenario flags))
    - Assumptions and Controls (scenario matrix / inclusion flags)
    - SAM Build section 5a (bucket TAM)
  related_appendix:
    - subs-a5   # appendix_sam_bucket_crosswalk

chrome:
  section: Market sizing
  breadcrumb_topic: SAM scenarios
  title_topic: SAM Scenarios
  title_finding: Broad component manufacturing is the largest scenario at ~$2.8B per year
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - U.S. Department of the Navy SCN Justification Books
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

story:
  objective: Show the five scenario sizes and make clear that scenarios are overlapping inclusion cuts of the same TAM, not market share, capture, or win probability.
  do_not_say:
    - No SOM, capture probability, win rate, qualification haircut, or pricing discount.
    - Never present a summed scenario total.
  known_caveats:
    - Broad is the largest scenario only because it is the union of all seven buckets (the envelope), not a single wedge.
    - Machining sits in BOTH metal and HM&E, so those two are not additive.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_right_rail
  # Chart on the left ~62%, a no-fill interpretation rail to its right, and one full-width
  # combined caveat strip fixed at the bottom (chart height runs down to it) that carries
  # both the guardrail and the overlap / average-annual convention.
  title_band:   {x: 0%, y: 0%, w: 62%, h: TITLE_BAND_H}
  chart:        {x: 0%, y: below(title_band), w: 62%, h: body_until(caveat_strip)}
  rail:         {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  caveat_strip: {x: 0%, y: BODY_B - CAVEAT_H, w: 100%, h: CAVEAT_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,   prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,        prominence: primary,   paint_order: 2, content: ranked bar of 5 scenarios by average annual SAM, tie_out: CD_14_SAMScenarios}
  - {id: e3, type: rail,          region: rail,         prominence: secondary, paint_order: 3, content: no-fill interpretation rail (scenario bucket composition)}
  - {id: e4, type: callout,       region: caveat_strip, prominence: secondary, paint_order: 4, content: "filled combined caveat strip (scenario-SAM-only guardrail + overlap / average-annual convention)"}


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
      external_title:
      - role: chart/exhibit title
        size: CHART_TITLE_10PT
        color: DK
        font: FONT
        italic: true
      chart_text:
        value_labels:
          size: LABEL_9PT
          font: FONT
          color: auto/DK
          note: Build converts token to *_size_pt expected by chart factory.
        category_axis:
          size: LABEL_9PT
          font: FONT
          color: DK
    e2:
      value_labels:
        size: LABEL_9PT
        font: FONT
        color: auto/DK
        note: Build converts token to *_size_pt expected by chart factory.
      category_axis:
        size: LABEL_9PT
        font: FONT
        color: DK
    e3:
      text_runs:
      - role: rail title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
        italic: true
      - role: bullet lead
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
      - role: bullet body
        size: LABEL_9PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: Scenario SAM only lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: guardrail body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
  render_notes:
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Broad component manufacturing (84.8%)"
        - "Electrical and power (38.0%)"
        - "Metal components (26.2%)"
        - "Modular assemblies (22.0%)"
        - "HM&E components (20.6%)"
      series:
        - name: Average annual SAM
          values: [2805.5, 1257.1, 865.4, 726.0, 679.6]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_3, BLUE_2, BLUE_1]
    params:
      mode: ranked
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175      # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 45
      cat_header: Scenario
      title: null                     # house style: external exhibit_title element
    external_title:
      text: SAM scenarios, average annual FY2022-FY2027
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Percent in each label is share of TAM; scenarios overlap and do not sum.", anchor_to: e2}

tables: []                # NONE: bucket-to-scenario composition is carried as a no-fill rail, not a matrix

shapes:
  - id: rail_1
    element: e3
    factory: text_box          # no-fill / no-border interpretation rail (slide-local _commentary_rail)
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    meaning: >
      No-fill rail naming each scenario's bucket composition so the reader sees the
      cuts overlap. Bold lead-in (LABEL_9PT) + regular body; one bullet per scenario.
    paragraphs:                # bold lead-in : body (DENSE_BODY_10PT lead, LABEL_9PT body)
      - {lead: "Broad:", body: "all seven buckets, residual excluded - the envelope."}
      - {lead: "Electrical:", body: "the electrical and power bucket alone."}
      - {lead: "Metal:", body: "structural fabrication, machining, and castings and forgings."}
      - {lead: "Modular:", body: "structural fabrication and pre-outfit, with coatings and insulation."}
      - {lead: "HM&E:", body: "piping, valves, pumps, HVAC, and machining (machining also sits in metal)."}
  - id: caveat_1
    element: e4
    factory: text_box
    fill: GRAY_2               # scope-boundary / caveat strip (guide color ref); the one filled focal callout
    line_color: BLACK          # focal family on this slide
    line_width: 19050          # 1.5pt focal weight (single focal object)
    insets: INSETS_MESSAGE
    text: "Scenario SAM only. No SOM, share capture, win probability, qualification success, or pricing haircut is modeled. Scenarios are overlapping cuts of one TAM; do not sum across them. Values are average annual FY2022-FY2027; cumulative shown for context."
    meaning: The section's governing guardrail combined with the overlap / average-annual convention - scenarios are serviceable-market definitions, not obtainable-market forecasts, and are non-additive cuts of one TAM.

commentary:
  visible:
    element: e3
    container: right_rail      # the bucket-composition rail is the visible commentary
    title: How to read the scenarios
    bullets:
      - {lead: "Broad:", body: "all seven buckets, residual excluded - the envelope."}
      - {lead: "Electrical:", body: "the electrical and power bucket alone."}
      - {lead: "Metal:", body: "structural fabrication, machining, and castings and forgings."}
      - {lead: "Modular:", body: "structural fabrication and pre-outfit, with coatings and insulation."}
      - {lead: "HM&E:", body: "piping, valves, pumps, HVAC, and machining (machining also sits in metal)."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the payoff of the SAM section (S12 taxonomy -> S13
      bucket TAM -> S14 here -> S15 visible suppliers -> S16 SIB exclusion). Portfolio
      TAM is ~$3.307B average annual (~$19.84B cumulative FY2022-FY2027), from ~$56.6B
      Basic Construction x a strict 35.0% applied supplier coefficient. This slide cuts
      that TAM into five overlapping serviceable-market definitions via the scenario
      matrix (SUMPRODUCT of bucket TAM and 0/1 inclusion flags).

      THE FIVE SCENARIOS, WHY THEY RANK AS THEY DO, AND WHAT THEY INCLUDE.
      - Broad component manufacturing ~$2,805M/yr (~$16.83B; 84.8% of TAM) = all seven
        buckets, residual excluded. Largest only because it is the union; an envelope,
        not a single wedge. Identity: broad SAM = TAM - unbucketed residual.
      - Electrical and power ~$1,257M/yr (~$7.54B; 38.0%) = the electrical bucket alone.
        Largest single named bucket, but narrower than a multi-bucket cut and
        qualification-heavy.
      - Metal components ~$865M/yr (~$5.19B; 26.2%) = structural fabrication + machining +
        castings/forgings. The largest cut that reads cleanly as one "where to play" wedge.
      - Modular assemblies ~$726M/yr (~$4.36B; 22.0%) = structural fabrication and
        pre-outfit + coatings/insulation. Most aligned with the distributed-build
        direction, even though modeled smaller than metal.
      - HM&E components ~$680M/yr (~$4.08B; 20.6%) = piping/valves/pumps + HVAC + machining.
        Machining is shared with metal, so HM&E and metal must never be added together.

      WHY OVERLAP MATTERS. The five bars share buckets (machining in both metal and HM&E;
      structural in metal, modular, and broad), so they are alternative cuts of one TAM,
      not five additive submarkets. Summing them double-counts. Share-of-TAM percentages
      therefore sum to well over 100% by design.

      WHY THIS IS SAM, NOT SOM. The slide says what the serviceable market is under each
      definition. It applies no capture share, qualification haircut, pricing discount, or
      probability of success. Broad SAM has no haircut at all - it is exactly TAM minus the
      unbucketed residual.

      SUPPLIER PROOF POINTS (visible first-tier flow, FFATA; from S15). Northrop Grumman
      ~$1.43B (electrical/electronics) leads visible flow; Curtiss-Wright Electro-Mechanical
      ~$198M (electrical); Scot Forge ~$198M (forgings -> castings); DC Fabricators ~$163M
      and Rhoads ~$142M (structural). These name the suppliers behind the buckets; they are
      not a target list and not the denominator.

      THE FFATA CAVEAT THAT BOUNDS ALL OF THIS. Visible first-tier flow is a FLOOR: ~$5.46B
      cumulative visible value across ~150 classified recipients (~759 broader parents),
      versus an outsourced layer the FFATA stream captures only ~10-20% of (wiki 12).
      Scenarios are sized from modeled TAM, not by summing FFATA subawards.

      DENSITY GUIDANCE. Default is chart + composition rail + guardrail strip + note. To
      densify, add one explanatory line in the note strip or extend a rail bullet; do not
      add a fourth visual. This slide's job is clarity about overlap, not exhaustiveness.
    density_modes:
      normal: {visible_bullets: 5, keep: [e2, e3, e4]}
      dense:  {add_bullets: 2, safe_containers: [caveat_strip, rail], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Metal vs broad:"
        body: "Metal components (~$865M) is the largest cut you can describe as a single wedge; broad (~$2,805M) is an envelope, not a go-to-market."
        evidence: SAM Build section 6
        safe_container: caveat_strip
        density_trigger: If the rail compresses, free one note line for this.
      - priority: 2
        lead: "No double-count:"
        body: "HM&E shares machining with metal; never add HM&E to the metal scenario."
        evidence: Assumptions and Controls scenario flags
        safe_container: rail        # extend the HM&E bullet
        density_trigger: Add if a reviewer asks why scenarios are not summed.
      - priority: 3
        lead: "Broad is an identity:"
        body: "Broad SAM = TAM minus the ~15.2% unbucketed residual; it is 84.8% of the ~$3.3B/yr TAM, with no capture haircut."
        evidence: SAM Build section 9 (SAM checks)
        safe_container: caveat_strip
        density_trigger: Add if a reader assumes broad SAM is the full TAM.
      - priority: 4
        lead: "Modular = distributed-build lane:"
        body: "Modular assemblies (~$726M) is the cut most aligned with the distributed-shipbuilding trajectory (10% -> 50% distributed sites)."
        evidence: SAM Build section 6; Navy and OSD policy (wiki 14)
        safe_container: caveat_strip
        density_trigger: Add when presenting alongside the market-direction story.
      - priority: 5
        lead: "Electrical caveat:"
        body: "Electrical and power (~$1,257M) is the largest single named bucket but qualification-heavy and narrower than metal as a go-to-market."
        evidence: bucket_tam (S13); Worktype Evidence
        safe_container: caveat_strip
        density_trigger: Add when the chart frame is shortened.
      - priority: 6
        lead: "FFATA is a floor:"
        body: "Scenario sizes come from modeled TAM, not summed subawards; visible FFATA flow captures only ~10-20% of the outsourced layer."
        evidence: Unseen layer (wiki 12); visible_suppliers (S15)
        safe_container: caveat_strip
        density_trigger: Add if a reader assumes the bars are summed FFATA dollars.
      - priority: 7
        lead: "Supplier proof point:"
        body: "Northrop Grumman (~$1.43B visible) anchors electrical; Scot Forge and the structural fabricators anchor metal."
        evidence: Entity Master; CD_15_TopVisibleSuppliers
        safe_container: rail
        density_trigger: Add if the rail gains a vendor line.
      - priority: 8
        lead: "Coefficient lineage:"
        body: "All five cuts apply to the same ~$3.3B/yr TAM = ~$56.6B Basic Construction x the strict 35.0% supplier coefficient, /6 years."
        evidence: tam_bridge; methodology
        safe_container: caveat_strip
        density_trigger: Add only if the audience has not seen the TAM bridge.
      - priority: 9
        lead: "Residual excluded here:"
        body: "Every scenario excludes the ~15.2% unbucketed/ambiguous residual carried in TAM; these cuts live inside the seven named buckets."
        evidence: SAM Build section 5a; work_type_taxonomy (S12)
        safe_container: chart
        density_trigger: Add only in a max-density appendix-style variant.
    do_not_add:
      - capture %, win-probability, SOM, or pricing-haircut language
      - any summed scenario total
      - company logos (names only)

data_and_calculations:
  data_inputs:
    - {input: Broad component manufacturing, value: 2805.5, unit: $M/yr, cumulative: 16832.9, share_of_tam: 84.8%, tie_out: CD_14_SAMScenarios, used_in: chart_1}
    - {input: Electrical and power,          value: 1257.1, unit: $M/yr, cumulative: 7542.7,  share_of_tam: 38.0%, tie_out: CD_14_SAMScenarios, used_in: chart_1}
    - {input: Metal components,              value: 865.4,  unit: $M/yr, cumulative: 5192.3,  share_of_tam: 26.2%, tie_out: CD_14_SAMScenarios, used_in: chart_1}
    - {input: Modular assemblies,            value: 726.0,  unit: $M/yr, cumulative: 4355.9,  share_of_tam: 22.0%, tie_out: CD_14_SAMScenarios, used_in: chart_1}
    - {input: HM&E components,               value: 679.6,  unit: $M/yr, cumulative: 4077.6,  share_of_tam: 20.6%, tie_out: CD_14_SAMScenarios, used_in: chart_1}
  calculations:
    - {name: scenario SAM, formula: "SUMPRODUCT(bucket TAM, scenario inclusion flags)", output: "per-scenario cumulative SAM", used_in: chart_1}
    - {name: average annual SAM, formula: "cumulative SAM / 6 years", output: "the charted value", used_in: chart_1}
    - {name: broad identity, formula: "broad SAM = portfolio TAM - unbucketed residual", output: "~$16.83B cumulative / 84.8% of TAM", used_in: chart_1}
  rounding_rules: Whole $M on the slide; share-of-TAM to one decimal in category labels; $B to two decimals for cumulative.
  reconciliation: Scenarios are overlapping cuts of the same TAM; they are NOT expected to sum to portfolio TAM. Broad <= TAM; broad = TAM - unbucketed.

qa:
  guardrails:
    - Broad component manufacturing is the top bar at ~$2,805M average annual (~$16.83B cumulative, 84.8% of TAM).
    - Slide explicitly states scenarios overlap, are not additive, and are not SOM.
    - Scenario bucket composition matches the Assumptions and Controls scenario matrix exactly.
    - Broad is framed as the envelope, not a single wedge.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov, SCN Justification Books); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit / column-width checks do not apply
