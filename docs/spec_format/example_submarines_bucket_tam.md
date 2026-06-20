# Worked example — submarines `bucket_tam` (SlideSpec format)
# Demonstrates the required-if-present rule from the OTHER side: a chart-only slide with
# `tables: []`, percentage-based regions, and a rich two-layer reserve/density bank.
# Source data: projects/submarines/deck/slide_specs/bucket_tam.md (deck slide 13).

meta:
  slide_id: subs-s13
  slide_order: 13
  module_name: bucket_tam.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: ranked_bar_plus_residual_strip
  story_role: Make the ~$3.3B TAM actionable by showing where the work-type dollars sit, before scenario SAM.
  inputs:
    - Chart Data CD_13_BucketTAM
    - SAM Build section 5a (modeled bucket shares)
    - Assumptions & Controls (work-type crosswalk)
    - Worktype Evidence
  related_appendix:
    - subs-a6   # appendix_sam_bucket_crosswalk

chrome:
  section: Market sizing
  breadcrumb_topic: Bucket TAM
  title_topic: Bucket TAM
  title_finding: Electrical and power, structural fabrication, and piping lead the opportunity
  layout: slideLayout4        # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - U.S. Department of the Navy SCN Justification Books
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

story:
  objective: Rank the seven component buckets by average annual TAM and locate the largest opportunities.
  do_not_say:
    - Do not imply the residual is worthless or non-addressable.
    - Broad SAM is scenario-based, not SOM.
  known_caveats:
    - Residual exists because the model does not force ambiguous vendor dollars into a bucket.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_residual_strip
  # Simple vertical stack by % of BODY height (no sibling refs needed); note pinned to BODY_B.
  title_band:     {x: 0%, y: 0%,  w: 100%, h: TITLE_BAND_H}
  chart:          {x: 0%, y: 8%,  w: 88%,  h: 64%}
  residual_strip: {x: 0%, y: 76%, w: 100%, h: fit_content}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,     prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,          prominence: primary,   paint_order: 2, content: ranked bar of 7 buckets, tie_out: CD_13}
  - {id: e3, type: callout,       region: residual_strip, prominence: secondary, paint_order: 3, content: gray residual strip (outside broad SAM)}
  - {id: e4, type: note,          region: note_strip,     prominence: tertiary,  paint_order: 4, content: average-annual convention note}

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Electrical and power (38.0%)"
        - "Structural fabrication and pre-outfit (18.9%)"
        - "Piping, valves, and pumps (15.7%)"
        - "Castings and forgings (4.3%)"
        - "Coatings and insulation (3.1%)"
        - "Machining (3.0%)"
        - "HVAC and ventilation (1.9%)"
      series:
        - name: Average annual TAM
          values: [1257.1, 624.5, 519.6, 142.8, 101.5, 98.1, 61.9]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_3, BLUE_1, BLUE_1, BLUE_1, BLUE_1]
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
      gap_width: 35
      cat_header: Work-type bucket
      title: null
    external_title:
      text: Average annual TAM by work-type bucket
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Top three buckets ≈ 73% of modeled TAM before the residual.", anchor_to: e2}

tables: []               # NONE on this slide -> block left explicit; no table-fit / col-width checks apply

shapes:
  - id: residual_1
    element: e3
    factory: text_box
    fill: GRAY_3         # exclusion styling — NOT the counted-TAM blues; not part of the ranked stack
    line_color: null
    insets: INSETS_MESSAGE
    text: "Unbucketed / ambiguous residual: ~$501M per year (~$3.01B cumulative). Tracked in TAM, excluded from broad component SAM."
    meaning: Keeps the residual visible and honest without forcing ambiguous dollars into a named bucket.
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Values are average annual FY2022-FY2027; cumulative shown for context."
    meaning: Average-annual convention note.

commentary:
  visible:
    element: e3
    container: callout       # the residual strip is the visible commentary
    title:
    bullets:
      - {lead: "Residual:", body: "real evidence ambiguity, not zero market — kept in TAM, out of broad SAM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the first "make it actionable" slide after the TAM
      bridge. The headline TAM is built simply: ~$56.6B FY2022-FY2027 Basic Construction
      base x a strict 35.0% applied supplier coefficient = ~$19.84B cumulative TAM, /6 =
      ~$3.307B average annual. This slide allocates that ~$3.3B/yr across seven work-type
      buckets plus an explicit residual; S14 (sam_scenarios) then turns the buckets into
      scenario SAM.

      THE RANKING AND WHAT DRIVES IT.
      - Electrical and power ~$1,257M/yr (~$7.54B; 38.0%) - submarine power distribution,
        electronics, controls, and propulsion-related components; by far the largest.
      - Structural fabrication and pre-outfit ~$625M/yr (~$3.75B; 18.9%) - hull sections,
        fabricated metal, modules; aligns with distributed-build logic (work pushed out of
        the legacy yards creates module/fab demand).
      - Piping, valves, and pumps ~$520M/yr (~$3.12B; 15.7%) - broad HM&E plus specialty
        components with meaningful qualification burden.
      - Castings and forgings ~$143M/yr (4.3%), Coatings and insulation ~$102M/yr (3.1%),
        Machining ~$98M/yr (3.0%), HVAC and ventilation ~$62M/yr (1.9%). Lower dollars, but
        any of these can be a critical bottleneck.
      Top three buckets ~ 73% of modeled TAM before the residual.

      THE RESIDUAL. ~$501M/yr (~$3.01B; 15.2%) is unbucketed/ambiguous: visible vendor flow
      not confidently assigned to one of the seven buckets. It is kept IN TAM but EXCLUDED
      from broad component SAM. It exists because NAICS is a corporate-primary code, not a
      per-action work description, so the model refuses to force ambiguous dollars into a
      named bucket - which improves credibility and keeps broad SAM from being overstated.
      It is not a claim that the residual is non-addressable.

      HOW BUCKETS BECOME SCENARIOS (preview of S14). Electrical and power is also a
      standalone scenario (~$1,257M). Metal components (structural + machining + castings) =
      ~$865M. HM&E (piping + HVAC) = ~$680M. Modular assemblies = ~$726M. Broad component
      manufacturing (all seven, residual excluded) = ~$2,805M, i.e. 84.8% of TAM.

      SUPPLIER PROOF POINTS (visible first-tier flow, FFATA). Northrop Grumman ~$1.43B is the
      largest visible recipient (electrical/electronics). Others: Leonardo ~$491M,
      Curtiss-Wright Electro-Mechanical ~$198M (electrical/power), Scot Forge ~$198M
      (forgings -> castings/forgings), ESCO ~$189M, DC Fabricators ~$163M and Rhoads ~$142M
      (structural fab), Graham ~$89M (heat exchangers -> HM&E). ~150 classified recipients,
      ~$5.46B visible value, ~759 broader FFATA parents - a named floor, not the full layer.

      DEMAND BACKDROP (directional, not a sizing input). CRS counts ~16,000 suppliers with
      ~70% sole-source; AUKUS points toward ~2.33 Virginia-class/yr; HII has guided +30%
      YoY outsourcing; >$10B has been invested in the submarine industrial base. These
      support why the supplier opportunity is expanding but do not change the FY22-27 math.

      DENSITY GUIDANCE. Default is chart + gray residual strip + convention note. To densify,
      add context lines in the note strip or expand the residual strip to two lines. Keep the
      residual visually separate from the ranked bars (gray, not blue) at any density.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [residual_strip, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Why electrical leads:"
        body: "Power distribution, electronics, controls, and propulsion-related components concentrate the largest bucket (~$1.26B; 38% of TAM)."
        evidence: Worktype Evidence; Vendors and concentration (wiki 09)
        safe_container: residual_strip
        density_trigger: If the residual strip gains a second line, add this as context above it.
      - priority: 2
        lead: "Structural = distributed-build fit:"
        body: "Structural fabrication and pre-outfit (~$625M) aligns with pushing module work out of the legacy yards."
        evidence: SAM Build 5a; FFATA-visible subawards (wiki 08)
        safe_container: note_strip
        density_trigger: Add when the chart frame is shortened.
      - priority: 3
        lead: "Small != unimportant:"
        body: "Castings/forgings, machining, coatings, and HVAC can be critical bottlenecks even at lower dollar values."
        evidence: Worktype Evidence
        safe_container: note_strip
        density_trigger: Add in a max-density variant.
      - priority: 4
        lead: "Concentration:"
        body: "Top three buckets (electrical, structural, piping) ~ 73% of modeled TAM before the residual."
        evidence: CD_13_BucketTAM
        safe_container: chart   # chart annotation
        density_trigger: Add if the chart has vertical headroom.
      - priority: 5
        lead: "Buckets -> scenarios:"
        body: "Electrical is also a standalone scenario (~$1,257M); metal (structural+machining+castings) ~$865M; broad (all seven) ~$2,805M = 84.8% of TAM."
        evidence: SAM Build; sam_scenarios (S14)
        safe_container: note_strip
        density_trigger: Add when this slide is shown right before the scenarios slide.
      - priority: 6
        lead: "Supplier proof points:"
        body: "Northrop Grumman ~$1.43B (electrical) leads visible flow; Scot Forge ~$198M (forgings), DC Fabricators/Rhoads (structural fab) anchor metal buckets."
        evidence: Entity Master; CD_15 visible suppliers
        safe_container: chart
        density_trigger: Add if the chart is narrowed to leave a right margin.
      - priority: 7
        lead: "Coefficient lineage:"
        body: "These buckets allocate the ~$3.3B/yr TAM = ~$56.6B Basic Construction x the strict 35.0% supplier coefficient, /6 years."
        evidence: tam_bridge; methodology
        safe_container: note_strip
        density_trigger: Add only if the audience has not seen the TAM bridge.
      - priority: 8
        lead: "Demand backdrop:"
        body: "~16,000 suppliers, ~70% sole-source (CRS); AUKUS toward ~2.33 Virginia/yr; HII guiding +30% outsourcing - directional, not a sizing input."
        evidence: demand_backdrop (S05); GAO-25-106286
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 9
        lead: "Why a residual at all:"
        body: "NAICS is corporate-primary, not per-action; the model keeps an explicit residual rather than forcing ambiguous dollars into a bucket - this is a credibility feature."
        evidence: Assumptions & Controls; SAM Taxonomy (S12)
        safe_container: residual_strip
        density_trigger: Add if a reviewer questions the residual.
    do_not_add:
      - SOM, capture, or win-probability language
      - any claim that the residual is non-addressable
      - the residual rendered inside or adjacent to the ranked bars (keep it gray + separate)

data_and_calculations:
  data_inputs:
    - {input: Electrical and power,                    value: 1257.1, unit: $M/yr, cumulative: 7542.7, share_of_tam: 38.0%, tie_out: CD_13, used_in: chart_1}
    - {input: Structural fabrication and pre-outfit,   value: 624.5,  unit: $M/yr, cumulative: 3747.1, share_of_tam: 18.9%, tie_out: CD_13, used_in: chart_1}
    - {input: Piping valves and pumps,                 value: 519.6,  unit: $M/yr, cumulative: 3117.5, share_of_tam: 15.7%, tie_out: CD_13, used_in: chart_1}
    - {input: Castings and forgings,                   value: 142.8,  unit: $M/yr, cumulative: 856.7,  share_of_tam: 4.3%,  tie_out: CD_13, used_in: chart_1}
    - {input: Coatings and insulation,                 value: 101.5,  unit: $M/yr, cumulative: 608.8,  share_of_tam: 3.1%,  tie_out: CD_13, used_in: chart_1}
    - {input: Machining,                               value: 98.1,   unit: $M/yr, cumulative: 588.5,  share_of_tam: 3.0%,  tie_out: CD_13, used_in: chart_1}
    - {input: HVAC and ventilation,                    value: 61.9,   unit: $M/yr, cumulative: 371.6,  share_of_tam: 1.9%,  tie_out: CD_13, used_in: chart_1}
    - {input: Unbucketed / ambiguous residual,         value: 501.1,  unit: $M/yr, cumulative: 3006.8, share_of_tam: 15.2%, tie_out: CD_13, used_in: residual_1}
  rounding_rules: Whole $M for average-annual labels; $B to two decimals for cumulative.
  reconciliation: Seven named buckets + residual sum to portfolio TAM (~$3,306.6M/yr); residual is excluded from broad SAM.

qa:
  guardrails:
    - Electrical and power is the top bucket at ~$1.26B average annual TAM.
    - Residual is shown in GRAY (e3), separate from the ranked bars — never inside the ranked stack.
    - Slide states broad SAM is scenario-based, not SOM.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov, SCN); no internal docs, workbook tabs, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit / column-width checks do not apply
