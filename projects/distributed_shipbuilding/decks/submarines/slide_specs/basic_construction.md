# SlideSpec - submarines `basic_construction` (deck slide 7)
# Stacked-column body slide: Basic Construction by fiscal year, Virginia + Columbia
# stacked into the FY2022-FY2027 denominator, with a right interpretation rail and a
# unit/scope note. This is the first numerical denominator slide in the TAM build:
# it resets the audience from total ship cost to the P-5c Basic Construction line
# before any supplier coefficient is applied (S08 TAM Bridge).

meta:
  slide_id: subs-s7
  slide_order: 7
  module_name: basic_construction.py
  slide_type: body
  section: TAM Build
  archetype: stacked_column_plus_right_rail
  story_role: Establish the P-5c Basic Construction denominator (~$56.6B FY2022-FY2027) before any supplier coefficient is applied.
  inputs:
    - Chart Data CD_07_BasicConstructionByFY
    - SCN Budget (P-5c Basic Construction by class/FY)
    - TAM Build section 4e (cumulative BC construction base)
    - SCN Budget section 4 (portfolio rollup)
  related_appendix: []

chrome:
  section: Market sizing
  breadcrumb_topic: Budget denominator
  title_topic: Basic Construction
  title_finding: The FY2022-FY2027 denominator averages ~$9.4B annually
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-5c
    - CRS RL32418
    - CRS R41129
  source_line_exact: "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-5c; (2) CRS RL32418; (3) CRS R41129"

story:
  objective: Defend the construction-contract denominator used for headline TAM and separate it from total ship cost, GFE, and prime self-performed labor.
  do_not_say:
    - Do not call Basic Construction total ship cost.
    - Do not imply Basic Construction equals GDEB self-performed labor.
    - Do not treat the annual average as a smooth yearly run-rate.
  known_caveats:
    - Columbia contributes zero Basic Construction in FY2022, FY2023, and FY2025 in this model window (AP-only years).
    - Basic Construction includes yard work, HII team-build workshare, purchased material, first-tier subcontracting, and lower-tier supplier flow.
    - Per-FY values are nominal then-year dollars drawn from the most recent Justification Book showing the year as a settled actual; no inflation normalization is applied.

regions:
  coord_basis: BODY
  layout_pattern: stacked_column_plus_right_rail
  # Chart fills the left ~70% of BODY; a no-fill interpretation rail sits right of it,
  # top-aligned; a full-width unit/scope note pins below the chart.
  title_band: {x: 0%, y: 0%, w: 70%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 70%, h: body_until(note_strip)}
  rail:       {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 70%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary, paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame, region: chart, prominence: primary, paint_order: 2, content: stacked column chart of Basic Construction by class and FY, tie_out: CD_07_BasicConstructionByFY}
  - {id: e3, type: rail, region: rail, prominence: secondary, paint_order: 3, content: denominator interpretation rail (no-fill)}
  - {id: e4, type: chart_annotation, region: chart, prominence: tertiary, paint_order: 4, content: FY2024 peak chart annotation, no-fill text_box with gray hairline leader to the column}
  - {id: e5, type: chart_annotation, region: chart, prominence: tertiary, paint_order: 5, content: FY2027 peak chart annotation, no-fill text_box with gray hairline leader to the column}
  - {id: e6, type: note, region: note_strip, prominence: tertiary, paint_order: 6, content: AP-only and average-run-rate unit note}


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
      - role: connector annotation
        size: CONNECTOR_NOTE_8_5PT
        color: DK
        font: FONT
        italic: true
    e5:
      text_runs:
      - role: connector annotation
        size: CONNECTOR_NOTE_8_5PT
        color: DK
        font: FONT
        italic: true
    e6:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: column_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      # Values are $B (P-5c Basic Construction; producer cells are $M, divided to $B for display).
      categories: [FY22, FY23, FY24, FY25, FY26, FY27]
      series:
        - name: Virginia
          values: [4.758, 5.095, 9.071, 5.327, 3.137, 8.889]
          data_point_colors: [BLUE_4, BLUE_4, BLUE_4, BLUE_4, BLUE_4, BLUE_4]
        - name: Columbia
          values: [0.000, 0.000, 6.356, 0.000, 7.160, 6.854]
          data_point_colors: [BLUE_2, BLUE_2, BLUE_2, BLUE_2, BLUE_2, BLUE_2]
    params:
      mode: stacked
      value_axis_format: '"$"0.0"B"'
      show_legend: true
      legend_pos: b
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175       # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '"$"0.0"B"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 90
      cat_header: FY
      title: null                      # house style: external exhibit_title element
    external_title:
      text: Basic Construction by fiscal year and class, $B
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      # Columbia zero-year labels are rendered WHITE so $0.0B does not read on-slide.
      - {text: "FY2024 peak: Virginia and Columbia Basic Construction.", anchor_to: e2}
      - {text: "FY2027 peak: two-boat Virginia plus Columbia.", anchor_to: e2}

tables: []                # NONE on this slide -> explicit design statement; no table-fit / col-width checks apply

shapes:
  - id: rail_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: |
      How to read the denominator
      Total: FY2022-FY2027 Basic Construction totals ~$56.6B.
      Average: the denominator averages ~$9.4B annually across six years.
      Cadence: FY2024 and FY2027 are peak years when both classes contribute.
      Scope: BC includes yards, team-build work, purchased material, first-tier subs, and lower-tier flow.
    meaning: No-fill interpretation rail (title bold italic LABEL_9PT; bulleted leads DENSE_BODY_10PT bold + LABEL_9PT body) so the chart remains the dominant object.
  - id: peak_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "FY2024 peak, Virginia and Columbia Basic Construction"   # CONNECTOR_NOTE_8_5PT italic, centered; gray hairline leader
    meaning: Deictic chart annotation (no-fill text_box) marking the first peak denominator year; a gray hairline leader line points down to the FY2024 column.
  - id: peak_2
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "FY2027 peak, two-boat Virginia plus Columbia"            # CONNECTOR_NOTE_8_5PT italic, centered; gray hairline leader
    meaning: Deictic chart annotation (no-fill text_box) marking the second peak denominator year; a gray hairline leader line points down to the FY2027 column.
  - id: note_1
    element: e6
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "AP-only Columbia years contribute no Basic Construction to this denominator. Average annual BC is a six-year average, not a smooth run-rate."   # FINEPRINT_8_5PT italic
    meaning: Unit and scope note that prevents misreading the denominator as a steady run-rate.

commentary:
  visible:
    element: e3
    container: right_rail
    title: How to read the denominator
    bullets:
      - {lead: "Total:", body: "FY2022-FY2027 Basic Construction totals ~$56.6B."}
      - {lead: "Average:", body: "the denominator averages ~$9.4B annually across six years."}
      - {lead: "Cadence:", body: "FY2024 and FY2027 are peak years when both classes contribute construction dollars."}
      - {lead: "Scope:", body: "BC includes yards, team-build work, purchased material, first-tier subs, and lower-tier flow."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the first numerical denominator slide in the TAM
      build. It resets the audience away from total ship cost and toward the Navy's
      Exhibit P-5c Basic Construction line item. Only Basic Construction feeds the
      headline non-nuclear supplier TAM; the next slide (S08 TAM Bridge) applies the
      strict 35.0% applied BC supplier coefficient to this base to produce ~$19.840B
      cumulative TAM and ~$3.307B average annual TAM. The Navy budget books report a
      Total Ship Estimate that includes Plans Costs, GFE categories (Propulsion
      Equipment, Electronics, HM&E, Ordnance), Other Cost, and Change Orders alongside
      Basic Construction; only Basic Construction is the base used here.

      WHAT THE CHART SHOWS. The FY2022-FY2027 Basic Construction denominator totals
      $56.647B and averages $9.441B per year (P-5c, SCN Justification Books). Virginia
      contributes $36.277B cumulatively across all six fiscal years; Columbia
      contributes $20.370B inside the model window, across only its three procurement
      years FY2024, FY2026, and FY2027. FY2024 ($15.4B combined) and FY2027 ($15.7B
      combined) are visibly the peaks because both Virginia and Columbia contribute
      Basic Construction. FY2022, FY2023, and FY2025 are Virginia-only inside this
      denominator (Columbia is AP-only in those years), and FY2026 combines a one-boat
      Virginia year with a Columbia construction year. Per-class per-FY figures (P-5c):
      Virginia FY22 $4,758.3M, FY23 $5,095.4M, FY24 $9,070.8M, FY25 $5,326.5M, FY26
      $3,136.8M, FY27 $8,889.3M; Columbia FY24 $6,356.1M, FY26 $7,159.8M, FY27 $6,853.7M.

      WHY THE DENOMINATOR MATTERS. Basic Construction is not the same as GDEB
      self-performed work. It is the prime construction-contract base - the dollars the
      Navy obligates to General Dynamics Electric Boat - which GDEB then distributes
      across five categories: (1) GDEB self-performed labor and overhead at Groton and
      Quonset Point; (2) HII Newport News team-build workshare under the teaming
      arrangement (publicly described as ~50% of Virginia construction and ~22% of
      Columbia by workload); (3) purchased material booked as direct material cost;
      (4) first-tier subcontracts (the subset above the FFATA $30,000-per-action
      threshold appears in FSRS); and (5) lower-tier subcontracts beneath the first
      tier. The deck therefore applies a strict supplier coefficient later rather than
      treating the entire Basic Construction base as open supplier opportunity. GAO has
      confirmed the directional posture: two shipbuilders are "already outsourcing work
      that would normally be done at their shipyards to their suppliers to overcome
      constrained physical space" (GAO-25-106286).

      MAIN AUDIENCE GUARDRAIL. The management headline later in the deck uses average
      annual TAM, but this chart should make clear that the budget base is lumpy. The
      six-year average is a modeling convenience and should not be presented as a stable
      annual market flow; on a per-FY basis combined Basic Construction runs ~$8-11B per
      year depending on which class is procuring (wiki 04). Per-FY values are nominal
      then-year dollars, not inflation-normalized.

      LEAD-BOAT CONTEXT (for share questions). Basic Construction's share of Total Ship
      Estimate varies by class and lead-boat status: Virginia runs ~56-80% of Total
      (Plans Costs modest), while the Columbia lead boat SSBN-826 ran only ~37% because
      Plans Costs absorbed the non-recurring engineering; Columbia follow-on boats settle
      to ~60-67% (wiki 04). This is why total-ship-cost comparisons are misleading here.
    density_modes:
      normal: {visible_bullets: 4, keep: [e2, e3, e6]}
      dense: {add_bullets: 3, safe_containers: [rail, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Denominator only:", body: "Only Basic Construction feeds the headline TAM denominator; Total Ship Estimate, Plans Costs, GFE, and Change Orders are outside this base.", evidence: "SCN Budget P-5c; Basic Construction (wiki 04)", safe_container: note_strip, density_trigger: "Add if a reviewer compares the slide to total ship cost."}
      - {priority: 2, lead: "Virginia base:", body: "Virginia contributes ~$36.3B of the ~$56.6B Basic Construction base across all six fiscal years FY2022-FY2027.", evidence: "CD_07_BasicConstructionByFY; SCN Budget section 4", safe_container: rail, density_trigger: "Add when the rail can support one more line."}
      - {priority: 3, lead: "Columbia base:", body: "Columbia contributes ~$20.4B inside the model window across only three procurement years, with no Basic Construction in FY2022, FY2023, or FY2025.", evidence: "CD_07_BasicConstructionByFY; Basic Construction (wiki 04)", safe_container: rail, density_trigger: "Add if Columbia timing is challenged."}
      - {priority: 4, lead: "Peak years:", body: "FY2024 (~$15.4B) and FY2027 (~$15.7B) are peak denominator years because both class programs contribute Basic Construction.", evidence: "CD_07_BasicConstructionByFY", safe_container: chart, density_trigger: "Add as a chart annotation if there is top whitespace."}
      - {priority: 5, lead: "Inside BC:", body: "BC funds GDEB yard labor, HII team-build share, purchased material, first-tier subcontracting, and lower-tier supplier flow, not yard labor alone.", evidence: "Basic Construction (wiki 04); SCN Budget P-5c", safe_container: rail, density_trigger: "Add if the audience equates BC with yard labor."}
      - {priority: 6, lead: "Not a run-rate:", body: "The ~$9.4B figure is a six-year average across lumpy procurement timing, not a stable yearly budget line; per-FY combined BC runs ~$8-11B.", evidence: "Basic Construction (wiki 04)", safe_container: note_strip, density_trigger: "Always safe for a dense variant."}
      - {priority: 7, lead: "Next step:", body: "The next slide applies the strict 35.0% supplier coefficient to this base to yield ~$19.8B cumulative TAM; this slide does not size suppliers directly.", evidence: "TAM Build section 4; CD_08_TAMBridge", safe_container: note_strip, density_trigger: "Use when presenting this slide without the next slide."}
      - {priority: 8, lead: "AP boundary:", body: "AP-only Columbia years (FY2022, FY2023, FY2025) are timing evidence, not Basic Construction dollars in this denominator.", evidence: "SCN P-10; AP and LLTM bridge (S11)", safe_container: note_strip, density_trigger: "Add if AP lines are being discussed nearby."}
      - {priority: 9, lead: "HII workshare:", body: "HII Newport News delivers ~half of Virginia construction and ~a fifth of Columbia by workload share, but those dollars sit inside GDEB's prime Basic Construction line.", evidence: "Basic Construction (wiki 04); GD Form 10-K FY2021", safe_container: rail, density_trigger: "Add if the team-build arrangement is raised."}
      - {priority: 10, lead: "Outsourcing posture:", body: "GAO confirms shipbuilders are already outsourcing work normally done at their yards to suppliers to overcome constrained space, with plans to expand.", evidence: "GAO-25-106286", safe_container: note_strip, density_trigger: "Add for an audience focused on supplier trajectory."}
      - {priority: 11, lead: "Share varies:", body: "Basic Construction is ~56-80% of Virginia Total Ship Estimate but only ~37% on the Columbia lead boat, where Plans Costs load the first hull.", evidence: "Basic Construction (wiki 04)", safe_container: note_strip, density_trigger: "Add if a reviewer asks why BC share differs across boats."}
    do_not_add:
      - SOM, capture probability, or win-rate language
      - total ship cost comparisons unless explicitly marked outside the denominator
      - any claim that the full Basic Construction base is addressable supplier opportunity

data_and_calculations:
  data_inputs:
    - {input: FY2022 Virginia BC, value: 4758.3, unit: $M, fiscal_year: FY2022, tie_out: CD_07_BasicConstructionByFY (scn_cell 2013/2022/basic), used_in: chart_1}
    - {input: FY2023 Virginia BC, value: 5095.4, unit: $M, fiscal_year: FY2023, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2024 Virginia BC, value: 9070.8, unit: $M, fiscal_year: FY2024, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2024 Columbia BC, value: 6356.1, unit: $M, fiscal_year: FY2024, tie_out: CD_07_BasicConstructionByFY (scn_cell 1045/2024/basic), used_in: chart_1}
    - {input: FY2025 Virginia BC, value: 5326.5, unit: $M, fiscal_year: FY2025, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2026 Virginia BC, value: 3136.8, unit: $M, fiscal_year: FY2026, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2026 Columbia BC, value: 7159.8, unit: $M, fiscal_year: FY2026, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2027 Virginia BC, value: 8889.3, unit: $M, fiscal_year: FY2027, tie_out: CD_07_BasicConstructionByFY, used_in: chart_1}
    - {input: FY2027 Columbia BC, value: 6853.7, unit: $M, fiscal_year: FY2027, tie_out: CD_07_BasicConstructionByFY (scn_cell 1045/2027/basic), used_in: chart_1}
  calculations:
    - {name: Virginia cumulative BC, formula: "sum(Virginia BC, FY2022-FY2027)", output: "$36.277B", used_in: rail_1}
    - {name: Columbia cumulative BC, formula: "sum(Columbia BC procurement years FY2024, FY2026, FY2027)", output: "$20.370B", used_in: rail_1}
    - {name: Total Basic Construction, formula: "Virginia cumulative + Columbia cumulative", output: "$56.647B", used_in: rail_1}
    - {name: Average annual Basic Construction, formula: "$56.647B / 6", output: "$9.441B", used_in: rail_1}
  rounding_rules: On-slide chart labels use $B to one decimal; support values keep three decimals in $B and one decimal in $M in data blocks.
  reconciliation: Annual Virginia and Columbia series sum to $56.647B across FY2022-FY2027; ties to TAM Build section 4e cumulative BC construction base (cumulative_bc_base_cell).

qa:
  guardrails:
    - Basic Construction is shown as the denominator, not as total ship cost or prime labor.
    - FY2024 and FY2027 are visibly the peak denominator years; Columbia FY2022, FY2023, FY2025 read as zero.
    - The note states average annual is not a steady run-rate; values are nominal then-year dollars.
    - Visible copy says SIB only if the supplier base is named; no MIB in visible copy.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN P-5c Justification Books, CRS RL32418, CRS R41129); no internal docs, workbook tabs, wiki chapters, or chart IDs rendered.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit and column-width checks do not apply
