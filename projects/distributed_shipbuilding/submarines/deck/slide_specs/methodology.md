# SlideSpec - submarines `methodology` (deck slide 06)
# Seven-step process RAIL rendered as numbered dots on a process axis (budget base
# -> remove non-addressable -> apply supplier coefficient -> calculate TAM ->
# allocate buckets -> scenario flags -> SAM menu), with seven compact step labels,
# a quotable FOCAL formula box, and a scope-notes rail. The steps are numbered dots
# on an axis, NOT a horizontal row of seven full filled cards, so the page reads as
# a lightweight flow. Shape-built flow, not a dense methodology table. Makes the
# model auditable before the deck defends the denominator, coefficient, and
# allocation.

meta:
  slide_id: subs-s6
  slide_order: 6
  module_name: methodology.py
  slide_type: body
  section: TAM Build
  archetype: seven_step_process_rail_with_formula_box
  story_role: Make the model auditable before the deck defends the denominator, coefficient, and allocation inputs.
  inputs:
    - guide_methodology.py (Methodology tab) section 2 formula framework and section 3 market-sizing flow
    - model_tam_build.py (TAM Build tab) sections 2, 3, and 4 (two-stream bases, POP coefficients, TAM bridge)
    - inputs_assumptions.py (Assumptions tab), AP/LLTM additive base 0 and scenario matrix
    - wiki 01 Scope and the funnel framework (the four denominators, multi-vintage SCN reconciliation)
    - wiki 06 Outsourced layer within Basic Construction (the supplier-share evidence band)
    - wiki 07 DoD contract announcement data (place-of-performance coefficient evidence)
    - wiki 08 FFATA-visible first-tier subawards (bucket allocation source)
    - wiki 16 Data sources, pipeline, and limitations (reconciliation rule, NAICS caveat)
  related_appendix:
    - subs-a4   # appendix_coefficient_sensitivity

chrome:
  section: TAM Build
  breadcrumb_topic: Methodology
  title_topic: Methodology
  title_finding: TAM is built from Basic Construction, supplier coefficients, and work-type allocation
  layout: slideLayout4
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10
    - U.S. DoD daily Contracts announcements
    - SAM.gov FFATA/FSRS and Entity Management records
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA/FSRS and Entity Management records"

story:
  objective: "Show the model logic in one clean process rail: budget base, exclusions, supplier coefficient, TAM calculation, bucket allocation, scenario flags, and SAM outputs."
  do_not_say:
    - Do not show detailed coefficient evidence; that belongs on the coefficient slide.
    - Do not show bucket values; those belong on the bucket and scenario slides.
    - Do not add gross AP and LLTM to the Basic Construction numerator.
    - Do not use SOM, capture, win probability, or company-specific revenue language.
  known_caveats:
    - The strict 35.0% applied BC coefficient feeds the headline TAM; broader distributed-production coefficients are appendix context only.
    - AP and LLTM are reference evidence; the additive headline base equals $0 because supplier LLTM is already inside Basic Construction.
    - SAM scenarios are bucket-inclusion menus, not capture forecasts.

regions:
  coord_basis: BODY
  layout_pattern: seven_step_process_rail_with_formula_box
  thesis_strip: {x: 0%, y: 0%, w: 100%, h: NOTE_H}
  process_rail: {x: 0%, y: 14%, w: 100%, h: 32%}
  # process_axis is the horizontal line the seven numbered dots sit on; dots occupy
  # the top of each step slot, compact labels sit just beneath them.
  process_axis: {x: 0%, y: 20%, w: 100%, h: 4%}
  step_1: {x: 0%, y: 14%, w: 13%, h: 32%}
  step_2: {x: right_of(step_1) + GAP, y: align_top(step_1), w: 13%, h: 32%}
  step_3: {x: right_of(step_2) + GAP, y: align_top(step_1), w: 13%, h: 32%}
  step_4: {x: right_of(step_3) + GAP, y: align_top(step_1), w: 13%, h: 32%}
  step_5: {x: right_of(step_4) + GAP, y: align_top(step_1), w: 13%, h: 32%}
  step_6: {x: right_of(step_5) + GAP, y: align_top(step_1), w: 13%, h: 32%}
  step_7: {x: right_of(step_6) + GAP, y: align_top(step_1), w: remaining, h: 32%}
  formula_box: {x: 0%, y: 54%, w: 68%, h: 32%}
  scope_notes: {x: right_of(formula_box) + GAP, y: align_top(formula_box), w: remaining, h: 32%}
  note_strip: {x: 0%, y: 90%, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: callout, region: thesis_strip, prominence: tertiary, paint_order: 1, content: simplicity thesis}
  - {id: e12, type: connector, region: process_axis, prominence: tertiary, paint_order: 2, content: process axis line the seven numbered step dots sit on}
  - {id: e2, type: glyph_set, region: process_rail, prominence: secondary, paint_order: 3, content: seven numbered step dots (step number plus short title each)}
  - {id: e3, type: label_set, region: process_rail, prominence: secondary, paint_order: 4, content: seven compact step labels (one per dot)}
  - {id: e9, type: callout, region: formula_box, prominence: primary, paint_order: 5, content: headline TAM formula and applied arithmetic, tie_out: model_tam_build.py section 4e}
  - {id: e10, type: rail, region: scope_notes, prominence: secondary, paint_order: 6, content: AP, LLTM, and SAM scenario notes}
  - {id: e11, type: note, region: note_strip, prominence: tertiary, paint_order: 7, content: no SOM method note}


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
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e12:
      connector_text: none
    e2:
      text_runs:
      - role: dot number
        size: LABEL_9PT
        color: auto/DK-or-WHITE
        font: FONT
        bold: true
      - role: optional dot title
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        bold: true
    e3:
      text_runs:
      - role: step label title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: step label source/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e9:
      text_runs:
      - role: formula cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: formula body
        size: MESSAGE_11PT
        color: DK
        font: FONT
      - role: applied arithmetic values
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
    e10:
      text_runs:
      - role: scope note title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: scope note body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e11:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes: []

charts: []
tables: []
images: []

shapes:
  - id: thesis_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "The headline model is intentionally simple; complexity is handled in the evidence and exclusions."   # FINEPRINT_8_5PT italic
    meaning: Provides an interpretive lead-in without crowding the process rail.
  - id: process_axis_1
    element: e12
    factory: connector
    fill: null
    line_color: GRAY_4
    insets: INSETS_NONE
    style: {color: GRAY_4, width: CONNECTOR_NORMAL, arrow: true}
    meaning: No-fill process axis (line_color GRAY_4, no fill); single left-to-right connector with a terminal arrow that the seven numbered step dots sit on, replacing the former six step-to-step arrows.
  - id: step_dots
    element: e2
    factory: glyph_set
    fill: null
    line_color: null
    insets: INSETS_NONE
    children:
      - {dot: d1, step: 1, x_on_axis: 7%,  title: "Build budget base",          fill: BLUE_1, line_color: GRAY_3}
      - {dot: d2, step: 2, x_on_axis: 21%, title: "Remove non-addressable",      fill: BLUE_1, line_color: GRAY_3}
      - {dot: d3, step: 3, x_on_axis: 36%, title: "Apply supplier coefficient",  fill: DK,     line_color: BLACK, emphasized: true}
      - {dot: d4, step: 4, x_on_axis: 50%, title: "Calculate portfolio TAM",     fill: BLUE_1, line_color: GRAY_3}
      - {dot: d5, step: 5, x_on_axis: 64%, title: "Allocate work-type buckets",  fill: BLUE_1, line_color: GRAY_3}
      - {dot: d6, step: 6, x_on_axis: 79%, title: "Apply scenario flags",        fill: BLUE_1, line_color: GRAY_3}
      - {dot: d7, step: 7, x_on_axis: 93%, title: "Output SAM menu",             fill: BLUE_1, line_color: GRAY_3}
    meaning: Seven numbered step dots sitting on the process axis, each a small filled circle carrying its step number; the controlled-glyph vocabulary replaces seven full filled step cards. Dot 3 (the supplier coefficient) is the darkest/emphasized dot (DK fill, BLACK rule) because it is the main model conversion; the other six dots are BLUE_1 with GRAY_3 rules. Enumerates exactly seven numbered step dots. The container itself is a no-fill glyph set (per-dot fills carried on each child).
  - id: step_labels
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    children:
      - {label: l1, under_dot: d1, text: "1  Build budget base\nP-5c Basic Construction; P-10 AP and LLTM reference"}
      - {label: l2, under_dot: d2, text: "2  Remove non-addressable flows\nGFE, BPMI, SIB, yards, design-only, depot"}
      - {label: l3, under_dot: d3, text: "3  Apply supplier coefficient\nPOP evidence; strict 35.0% feeds headline TAM"}
      - {label: l4, under_dot: d4, text: "4  Calculate portfolio TAM\nBasic Construction base times coefficient; AP and LLTM additive base is $0"}
      - {label: l5, under_dot: d5, text: "5  Allocate work-type buckets\nFFATA, FSRS, SAM.gov entity data, NAICS mapping"}
      - {label: l6, under_dot: d6, text: "6  Apply scenario flags\nBucket inclusion menus; SAM scenario, not SOM"}
      - {label: l7, under_dot: d7, text: "7  Output SAM menu\nBroad, electrical, metal, modular, HM and E; no SOM"}
    meaning: Seven compact step labels, one beneath each numbered dot (LABEL_9PT title plus a short DENSE_BODY_10PT/LABEL_9PT source line). No-fill label set (no fill, no border); these are the step text only, not filled cards. Enumerates exactly seven compact step labels.
  - id: formula_box_1
    element: e9
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    text: "Average annual TAM = FY2022-FY2027 Basic Construction base times applied BC supplier coefficient, divided by 6\nApplied: $56.647B times 35.0% = ~$19.840B cumulative TAM; over 6 years = ~$3.307B average annual"
    meaning: Primary/focal object; provides the quotable model formula and applied arithmetic. Filled BLUE_1 with a heavy BLACK rule (line_width 19050) so the formula reads as the slide's hero/answer object.
  - id: scope_notes_1
    element: e10
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Scope notes\n- AP and LLTM gross is retained as reference evidence; the additive headline base is $0.\n- SAM scenarios are bucket inclusion menus; no SOM or win-probability haircut is applied.\n- Detailed coefficient evidence belongs on the coefficient slide, not here."
    meaning: Keeps the method slide transparent without trying to prove every input.
  - id: note_1
    element: e11
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Method note: SAM is a scenario menu, not SOM, capture share, win probability, or company revenue forecast."   # FINEPRINT_8_5PT italic
    meaning: Extra no-SOM reinforcement if the bottom row has room.

commentary:
  visible:
    element: e10
    container: method_note
    title: Scope notes
    bullets:
      - {lead: "AP and LLTM:", body: "reference evidence only; the additive base is $0."}
      - {lead: "SAM:", body: "bucket inclusion menu, not SOM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      MAKE THE MODEL AUDITABLE. This slide should make the model easy to audit in
      one read. The budget base comes from Navy SCN exhibits (P-5c Basic
      Construction, P-10 advance procurement); the supplier coefficient comes from
      DoD daily Contracts place-of-performance evidence; the work-type allocation
      comes from FFATA, FSRS, and SAM.gov visible supplier data. The headline TAM
      is simple multiplication and averaging, but credibility rests on the scope
      exclusions and the coefficient choice, not on arithmetic.

      THE TWO-STREAM FORMULA. The workbook computes TAM as two streams: BC base
      times the applied BC supplier coefficient, plus AP/LLTM base times the
      AP/LLTM reference coefficient. Because the AP/LLTM additive base is held at
      $0 (supplier LLTM is already inside Basic Construction), only the BC stream
      drives the headline. Applied: $56.647B FY2022-FY2027 Basic Construction base
      times 35.0% equals ~$19.840B cumulative TAM, divided by six fiscal years
      equals ~$3.307B average annual TAM. The precise workbook values are
      $56.6467B times 35.0235% = $19.8397B cumulative and $3.3066B average annual.

      THE STRICT COEFFICIENT MATTERS. The POP corpus can support broader
      distributed-production views (the workbook reports a confirmed
      distributed-away-from-EB coefficient near 68% and an incl-unparsed figure
      near 78%, an all-gated GFE-excluded figure near 54.5%, and a published
      anchor near 51.8%), but the headline applies the conservative non-nuclear,
      BPMI-excluded, prime-yard and co-prime-yard excluded coefficient near 35.0%.
      That is why the TAM is not simply a 50% or 60% outsourced-share assumption
      multiplied by total ship cost. The broader coefficients are appendix
      context only and are deliberately not applied.

      WHY A DENOMINATOR DISCIPLINE. Wiki 01 makes four candidate denominators of
      "outsourced" visible: outsourced from GDEB, outsourced from the Navy / SCN
      perspective, outside-the-yard per DoD announcements, and all private-sector
      work outside the assembling yard. The method picks a strict, supplier-
      addressable reading and applies it consistently rather than mixing
      denominators. The supplier coefficient is computed on the place-of-
      performance corpus, which is the most direct primary-source measurement
      because it does not depend on accounting categorization.

      MULTI-VINTAGE SCN RECONCILIATION. The per-fiscal-year base figures are not
      taken from a single budget book. The Navy revises each fiscal year across
      Justification Book vintages (an estimate column becomes an actual column the
      next year, often with material changes). The model uses the most recent book
      that shows the target year as a settled actual (defaulting to a most-recent-
      PB-year-greater-than-or-equal-to-FY-plus-2 rule), spanning the FY2022 through
      FY2027 PB books, and uses stable Line Item numbers (Virginia 2013, Columbia
      1045) rather than drifting P-1 line numbers.

      AP AND LLTM ARE REFERENCE, NOT ADDITIVE. P-10 tells an important story about
      supplier purchasing and long-lead material, but the workbook confirms the
      additive AP and LLTM base equals $0 in the headline model to avoid double
      counting. The AP/LLTM reference coefficient (~48.5%) is computed but not
      applied precisely because the base is $0.

      SAM IS A SCENARIO MENU. SAM is created by including or excluding work-type
      buckets. The scenario matrix is fixed: metal is structural, castings, and
      machining; HM&E is piping, HVAC, and machining; electrical is electrical;
      modular is structural and coatings; broad is all seven buckets. None of
      these apply capture share, win rate, probability of success, price
      realization, or company-specific addressability.

      LAYOUT DISCIPLINE. The process rail should have exactly seven steps and
      should not become a dense methodology table. Use numbered cards on a rail,
      with Step 3 (the coefficient) and the formula box receiving the strongest
      visual emphasis. The formula box should be visually separate and easy to
      quote.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2, e3, e9, e10, e11, e12]}
      dense: {add_bullets: 4, safe_containers: [formula_box, scope_notes, note_strip], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT", "LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Strict coefficient:"
        body: "Only the strict non-nuclear, BPMI-excluded, yard-excluded 35.0% coefficient feeds the headline TAM."
        evidence: model_tam_build.py section 3 (bc_supplier_coeff_cell); wiki 06 outsourced band
        safe_container: process_rail
        density_trigger: Add if Step 3 has room for a small side note.
      - priority: 2
        lead: "Formula detail:"
        body: "$56.6467B times 35.0235% = $19.8397B cumulative TAM; average annual TAM is $3.3066B."
        evidence: model_tam_build.py section 4e (cumulative and avg_annual cells)
        safe_container: formula_box
        density_trigger: Add if a more precise version is needed for internal review.
      - priority: 3
        lead: "Broad SAM preview:"
        body: "Broad component-manufacturing SAM is ~$16.833B cumulative, or ~$2.806B average annual."
        evidence: model_sam_build.py (selected_sam_cell, broad scenario)
        safe_container: scope_notes
        density_trigger: Add only if this slide must preview the executive summary math.
      - priority: 4
        lead: "AP and LLTM:"
        body: "Gross AP and LLTM stays as reference evidence; do not add it to Basic Construction without changing the boundary."
        evidence: inputs_assumptions.py section 3 (additive base 0); SCN Justification Books, Exhibit P-10
        safe_container: scope_notes
        density_trigger: Add if AP and LLTM are a live concern.
      - priority: 5
        lead: "Allocation lineage:"
        body: "Work-type buckets are allocated from FFATA and FSRS visible vendor flow, SAM.gov Entity Management NAICS enrichment, and model mapping."
        evidence: SAM.gov FFATA/FSRS and Entity Management records; inputs_assumptions.py section 6
        safe_container: process_rail
        density_trigger: Add if the audience asks how buckets are created.
      - priority: 6
        lead: "Scenario rule:"
        body: "SAM scenarios include or exclude buckets; they do not apply capture share, win rate, or probability of success."
        evidence: guide_methodology.py section 2b; inputs_assumptions.py scenario matrix
        safe_container: process_rail
        density_trigger: Add if the no-SOM warning needs repetition.
      - priority: 7
        lead: "Do not overprove here:"
        body: "Detailed coefficient evidence belongs on the coefficient slide; bucket values belong on the bucket and scenario slides."
        evidence: deck narrative sequence (S06 method, S10 coefficient, S13 buckets)
        safe_container: note_strip
        density_trigger: Add if the slide starts getting too dense.
      - priority: 8
        lead: "Transparency read:"
        body: "The method is simple enough to audit: denominator times coefficient, then bucket allocation, then scenario flags."
        evidence: guide_methodology.py section 3 market-sizing flow
        safe_container: thesis_strip
        density_trigger: Add if the audience needs a plain-language lead-in.
      - priority: 9
        lead: "Multi-vintage base:"
        body: "Per-year Basic Construction is reconciled across SCN budget vintages using the most recent book that shows each year as a settled actual, on stable Line Item numbers."
        evidence: wiki 01 multi-vintage reconciliation; wiki 16 reconciliation rule
        safe_container: process_rail
        density_trigger: Add if a reviewer questions which budget year a figure comes from.
      - priority: 10
        lead: "Denominator discipline:"
        body: "Outsourced needs a denominator; the method picks a strict supplier-addressable reading and applies it consistently across the corpus."
        evidence: wiki 01 four denominators; wiki 07 DoD announcement measurement
        safe_container: process_rail
        density_trigger: Add for an analytically rigorous audience.
      - priority: 11
        lead: "Coefficient is the conversion:"
        body: "Step 3 is the one place a budget dollar becomes a supplier-addressable dollar; everything before it is base-building and everything after is allocation."
        evidence: model_tam_build.py section 3
        safe_container: process_rail
        density_trigger: Add to emphasize why Step 3 is the focal step.
    do_not_add:
      - detailed coefficient proof or sensitivity cases
      - detailed bucket values
      - SOM, capture, win probability, or revenue forecast language
      - gross AP and LLTM added into the formula numerator

data_and_calculations:
  data_inputs:
    - {input: FY2022-FY2027 Basic Construction base, value: 56.6467, unit: $B, tie_out: model_tam_build.py section 4e (cumulative_bc_base_cell), used_in: formula_box_1}
    - {input: Applied Basic Construction supplier coefficient, value: 35.0235%, unit: share, display: "35.0%", tie_out: model_tam_build.py section 3 (bc_supplier_coeff_cell), used_in: step_dots}
    - {input: Cumulative TAM, value: 19.8397, unit: $B, display: "~$19.840B", tie_out: model_tam_build.py section 4e (cumulative_tam_cell), used_in: formula_box_1}
    - {input: Average annual TAM, value: 3.3066, unit: $B per year, display: "~$3.307B", tie_out: model_tam_build.py section 4e (avg_annual_tam_cell), used_in: formula_box_1}
    - {input: Broad component-manufacturing SAM, value: 16.8329, unit: $B cumulative, tie_out: model_sam_build.py (broad scenario), used_in: reserve_only}
    - {input: Average annual broad SAM, value: 2.8055, unit: $B per year, tie_out: model_sam_build.py (broad scenario), used_in: reserve_only}
    - {input: AP and LLTM additive base, value: 0, unit: dollars, display: "$0", tie_out: inputs_assumptions.py section 3 (additive base 0), used_in: scope_notes_1}
  calculations:
    - {name: Average annual TAM, formula: "FY2022-FY2027 Basic Construction base x applied BC supplier coefficient / 6", output: "~$3.307B", used_in: formula_box_1}
  rounding_rules: On-slide formula rounds Basic Construction to $56.647B, the coefficient to 35.0%, cumulative TAM to ~$19.840B, and average annual TAM to ~$3.307B.
  reconciliation: The headline formula uses the Basic Construction base only; AP and LLTM remain reference evidence with a $0 additive headline base under the current boundary. Portfolio TAM reconciles as BC stream TAM plus AP/LLTM stream TAM, and average annual times fiscal years equals cumulative.

qa:
  guardrails:
    - The process rail has exactly seven steps and matches the workbook market-sizing flow order.
    - The formula uses the Basic Construction base, not total ship cost.
    - The AP and LLTM additive base is stated as $0.
    - The SAM section explicitly says no SOM, capture, or win probability.
    - Detailed coefficient evidence and bucket values are not shown here.
  source_checks:
    - The visible footer lists external published documents only (SCN P-5c and P-10, DoD daily Contracts, SAM.gov records); no workbook tabs, wiki chapters, or chart IDs are rendered.
    - Internal provenance (guide_methodology.py, model_tam_build.py, inputs_assumptions.py, model_sam_build.py, wiki chapters) stays in meta.inputs, tie_outs, and reserve evidence only.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - no chart rIds because charts is empty
    - no table-fit check because tables is empty
