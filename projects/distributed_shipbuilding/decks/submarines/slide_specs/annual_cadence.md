# SlideSpec - submarines `annual_cadence` (deck slide 9)
# Chart-only body slide: a native clustered column chart of annual TAM and annual
# broad SAM across FY2022-FY2027, with two peak annotations (FY2024, FY2027) and a
# pinned convention note that average annual is NOT a run-rate. tables: [] is an
# explicit design statement - the cadence is the message, not a table of numbers.

meta:
  slide_id: subs-s9
  slide_order: 9
  module_name: annual_cadence.py
  slide_type: body
  section: TAM Build
  archetype: clustered_column_with_peak_annotations
  story_role: Make the average annual headline interpretable - prevent ~$3.3B average annual TAM from being read as a smooth yearly run-rate by showing the lumpy fiscal-year path.
  inputs:
    - Chart Data CD_09_AnnualTAMAndSAM
    - TAM Build section 4 (annual portfolio TAM by FY)
    - SAM Build section 8 (annual broad SAM by FY)
    - QA Reconciliation
  related_appendix: []

chrome:
  section: Market sizing
  breadcrumb_topic: Annual cadence
  title_topic: Annual Cadence
  title_finding: TAM and broad SAM are lumpy, with FY2024 and FY2027 peaks
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibit P-5c
    - U.S. DoD daily Contracts announcements
    - SAM.gov FFATA/FSRS and Entity Management records
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA/FSRS and Entity Management records"

story:
  objective: Show actual annual TAM and broad SAM outputs and tie the FY2024 and FY2027 peaks to procurement cadence, so the average annual headline is not mistaken for a flat yearly market.
  do_not_say:
    - Do not present ~$3.3B average annual TAM as a smooth annual run-rate.
    - Do not describe annual peaks as commercial-style market volatility.
    - Do not imply broad SAM is an independent budget line.
  known_caveats:
    - Annual values are model outputs tied to procurement timing (when Virginia and Columbia Basic Construction enter the budget each FY), not a forecast of market growth.
    - Broad SAM moves with TAM because it is a scenario cut from TAM (~84.8% of TAM), not a separate procurement account.

regions:
  coord_basis: BODY
  layout_pattern: clustered_column_with_peak_annotations
  # Full-width clustered columns; two small peak annotations float over the FY2024 and
  # FY2027 clusters; a pinned convention note runs full width at the bottom.
  title_band: {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 100%, h: body_until(note_strip)}
  anno_2024:  {x: 36%, y: 10%, w: 22%, h: fit_content}
  anno_2027:  {x: 72%, y: 10%, w: 24%, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title,    region: title_band, prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,      region: chart,      prominence: primary,   paint_order: 2, content: clustered columns for annual TAM and annual broad SAM across six FY, tie_out: CD_09_AnnualTAMAndSAM}
  - {id: e3, type: chart_annotation, region: anno_2024,  prominence: tertiary,  paint_order: 3, content: FY2024 peak annotation chip (BLUE_1 fill, GRAY_3 secondary border)}
  - {id: e4, type: chart_annotation, region: anno_2027,  prominence: tertiary,  paint_order: 4, content: FY2027 peak annotation chip (BLUE_1 fill, GRAY_3 secondary border)}
  - {id: e5, type: note,             region: note_strip, prominence: tertiary,  paint_order: 5, content: average-annual and cadence convention note}


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
          size: SOURCES_8PT
          font: FONT
          color: auto/DK
          note: Build converts token to *_size_pt expected by chart factory.
        category_axis:
          size: LABEL_9PT
          font: FONT
          color: DK
        legend:
          size: LABEL_9PT
          font: FONT
          color: DK
    e2:
      value_labels:
        size: SOURCES_8PT
        font: FONT
        color: auto/DK
        note: Build converts token to *_size_pt expected by chart factory.
      category_axis:
        size: LABEL_9PT
        font: FONT
        color: DK
      legend:
        size: LABEL_9PT
        font: FONT
        color: DK
    e3:
      text_runs:
      - role: annotation chip
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
    e4:
      text_runs:
      - role: annotation chip
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
    e5:
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
      categories: [FY2022, FY2023, FY2024, FY2025, FY2026, FY2027]
      series:
        - {name: Annual TAM, values: [1.667, 1.785, 5.403, 1.866, 3.606, 5.514], color: BLUE_4}
        - {name: Annual broad SAM, values: [1.414, 1.514, 4.584, 1.583, 3.060, 4.678], color: BLUE_2}
    params:
      mode: clustered
      value_axis_format: '"$"0.0"B"'
      show_legend: true
      legend_pos: b
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175      # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '"$"0.0"B"'
      value_label_size_pt: 8
      cat_label_size_pt: 9
      gap_width: 80
      cat_header: Fiscal year
      title: null                     # house style: external exhibit_title element
    external_title:
      text: Annual TAM and broad SAM, FY2022-FY2027
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "FY2024 peak: Virginia and Columbia Basic Construction", anchor_to: e3}
      - {text: "FY2027 peak: two-boat Virginia plus Columbia", anchor_to: e4}

tables: []                # NONE on this slide -> block left explicit; the cadence is the message, not a table

shapes:
  - id: anno_2024_1
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MICRO_CAP
    text: "FY2024: both classes contribute Basic Construction"   # LABEL_9PT
    meaning: Peak annotation placed above the FY2024 cluster.
  - id: anno_2027_1
    element: e4
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MICRO_CAP
    text: "FY2027: two-boat Virginia plus Columbia"   # LABEL_9PT
    meaning: Peak annotation placed above the FY2027 cluster.
  - id: note_1
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Average annual TAM is ~$3.3B and broad SAM is ~$2.8B, but actual annual flow follows procurement cadence. Peaks are cadence effects, not commercial-style volatility."   # FINEPRINT_8_5PT italic
    meaning: Prevents the average annual headline from being read as a flat annual run-rate.

commentary:
  visible:
    element: e5
    container: method_note      # the convention note is the visible commentary
    title:
    bullets:
      - {lead: "Read:", body: "Average annual is a model-period summary; the chart shows the lumpy fiscal-year path."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It follows the TAM Bridge (S08) and makes the average annual
      headline interpretable. The management headline is ~$3.3B average annual TAM and ~$2.8B
      average annual broad SAM, but the model output is not a flat annual run-rate. If someone
      expects a $3.3B bar every year, they will misunderstand the procurement cycle. Annual
      opportunity follows how the Navy authorizes Virginia and Columbia Basic Construction in
      each fiscal year.

      WHAT THE CHART SHOWS (workbook TAM Build section 4, FY2022-FY2027). Annual TAM is
      $1.667B in FY2022, $1.785B in FY2023, $5.403B in FY2024, $1.866B in FY2025, $3.606B in
      FY2026, and $5.514B in FY2027. Each FY's TAM is the portfolio Basic Construction base
      that year times the applied ~35.0% supplier coefficient. Annual broad SAM is $1.414B,
      $1.514B, $4.584B, $1.583B, $3.060B, and $4.678B over the same years - in each FY a
      ~84.8% scenario cut of that year's TAM. The annual TAM bars sum to ~$19.84B cumulative
      TAM (tying back to the TAM Bridge); annual broad SAM sums to ~$16.83B.

      WHY FY2024 AND FY2027 PEAK. FY2024 (~$5.4B TAM, ~$4.6B SAM) is high because both class
      programs contribute Basic Construction in the same year: the final Virginia Block V
      two-boat year (per P-5c, ~$11.4B Total Ship Estimate) plus Columbia SSBN-827
      construction. FY2027 (~$5.5B TAM, ~$4.7B SAM) is the highest because it combines a
      two-boat Virginia Block VI year (~$11.4B Total Ship Estimate) with Columbia SSBN-829
      construction. FY2026 (~$3.6B TAM) is also elevated because Columbia SSBN-828 contributes
      strongly even though Virginia is a one-boat Block VI year. FY2022, FY2023, and FY2025 are
      smaller because the Basic Construction denominator is lighter in those years (Block V
      two-boat at lower then-year cost in FY22-23; single Block VI lead boat in FY2025).

      WHY SAM MOVES WITH TAM. Broad SAM is not an independent budget line. It is a scenario
      cut from annual TAM using the modeled bucket inclusion logic (broad component
      manufacturing, all seven buckets, residual excluded - ~84.8% of TAM), so it moves with
      the annual TAM base in every fiscal year. The chart should compare TAM and broad SAM in
      each fiscal year without implying two separate procurement accounts.

      MAIN AUDIENCE GUARDRAIL. The annual pattern is procurement cadence, not commercial-style
      market volatility. It reflects authorized construction timing and the Basic Construction
      denominator, not a change in supplier appetite or pricing. The six-year average smooths
      the model for communication; it should not be forecast as a flat annual market.

      DENSITY GUIDANCE. Default is clustered columns + two peak annotations + convention note.
      To densify, add a per-year reason line in the note strip (e.g. why FY2026 is elevated),
      or add the cumulative tie-back to the TAM Bridge. Keep clustered (not stacked) columns so
      TAM and broad SAM stay directly comparable in each year; do not use a line chart - the
      cadence is categorical fiscal-year procurement, not a continuous time series.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4, e5]}
      dense:  {add_bullets: 3, safe_containers: [note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "FY2024:"
        body: "TAM reaches ~$5.4B and broad SAM ~$4.6B when both class programs contribute Basic Construction (final Virginia Block V two-boat plus Columbia SSBN-827)."
        evidence: TAM Build section 4; wiki 02 (total ship cost)
        safe_container: chart
        density_trigger: Add if the FY2024 annotation has room.
      - priority: 2
        lead: "FY2027:"
        body: "TAM reaches ~$5.5B and broad SAM ~$4.7B with a two-boat Virginia Block VI year plus Columbia SSBN-829."
        evidence: TAM Build section 4; wiki 02
        safe_container: chart
        density_trigger: Add if the FY2027 annotation has room.
      - priority: 3
        lead: "FY2026:"
        body: "FY2026 is elevated (~$3.6B TAM) because Columbia SSBN-828 contributes strongly even though Virginia is a one-boat Block VI year."
        evidence: TAM Build section 4
        safe_container: note_strip
        density_trigger: Add for a denser interpretation note.
      - priority: 4
        lead: "Lighter years:"
        body: "FY2022, FY2023, and FY2025 are smaller because the Basic Construction denominator is lighter (Block V at lower then-year cost; single Block VI lead boat in FY2025)."
        evidence: Basic Construction (S07); wiki 04
        safe_container: note_strip
        density_trigger: Add if the chart is presented before the Basic Construction slide.
      - priority: 5
        lead: "SAM mechanic:"
        body: "Broad SAM is a ~84.8% scenario cut of TAM, not a separate budget line, so it moves with the TAM bars in every fiscal year."
        evidence: SAM Build section 8 (annual broad SAM)
        safe_container: note_strip
        density_trigger: Add if SAM independence is a risk with the audience.
      - priority: 6
        lead: "Average headline:"
        body: "The six-year average smooths the model for communication; it should not be forecast as a flat annual market."
        evidence: TAM Build section 4 (average annual portfolio TAM)
        safe_container: note_strip
        density_trigger: Always safe in a dense variant.
      - priority: 7
        lead: "Cumulative tie:"
        body: "The annual TAM bars sum to ~$19.84B cumulative TAM, tying back to the TAM Bridge; broad SAM sums to ~$16.83B."
        evidence: TAM Build section 4; TAM Bridge (S08)
        safe_container: note_strip
        density_trigger: Add for a reconciliation-heavy review.
      - priority: 8
        lead: "Cadence framing:"
        body: "Peaks are procurement-cadence effects from authorized construction timing, not commercial-style market volatility."
        evidence: SCN P-5c; speaker commentary
        safe_container: note_strip
        density_trigger: Keep if the note strip is shortened to one sentence.
      - priority: 9
        lead: "Coefficient lineage:"
        body: "Each FY's TAM is that year's portfolio Basic Construction base times the applied ~35.0% supplier coefficient."
        evidence: TAM Build section 4a (applied BC coefficient)
        safe_container: note_strip
        density_trigger: Add if the audience has not seen the coefficient evidence (S10).
      - priority: 10
        lead: "Outsourcing trajectory:"
        body: "Supplier-targeted LLTM contract value has shifted sharply outside the two yards over the window, supporting why the opportunity is real even in lighter years."
        evidence: wiki 07 (DoD daily Contracts, FY2022 vs FY2026)
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 11
        lead: "Clustered, not stacked:"
        body: "The chart clusters TAM and broad SAM per year so the two are directly comparable; do not stack and do not use a line chart."
        evidence: Design note (B); house chart conventions
        safe_container: chart
        density_trigger: Reference only if a build variant changes the chart form.
    do_not_add:
      - annual market-growth interpretation read off the lumpy bars
      - independent budget-line framing for broad SAM
      - stacked columns or a line chart in place of clustered columns
      - SOM or capture-rate language

data_and_calculations:
  data_inputs:
    - {input: FY2022 annual TAM, value: 1.667, unit: $B, fiscal_year: FY2022, tie_out: TAM Build section 4 (CD_09_AnnualTAMAndSAM), used_in: chart_1}
    - {input: FY2023 annual TAM, value: 1.785, unit: $B, fiscal_year: FY2023, tie_out: TAM Build section 4, used_in: chart_1}
    - {input: FY2024 annual TAM, value: 5.403, unit: $B, fiscal_year: FY2024, tie_out: TAM Build section 4, used_in: chart_1}
    - {input: FY2025 annual TAM, value: 1.866, unit: $B, fiscal_year: FY2025, tie_out: TAM Build section 4, used_in: chart_1}
    - {input: FY2026 annual TAM, value: 3.606, unit: $B, fiscal_year: FY2026, tie_out: TAM Build section 4, used_in: chart_1}
    - {input: FY2027 annual TAM, value: 5.514, unit: $B, fiscal_year: FY2027, tie_out: TAM Build section 4, used_in: chart_1}
    - {input: FY2022 annual broad SAM, value: 1.414, unit: $B, fiscal_year: FY2022, tie_out: SAM Build section 8, used_in: chart_1}
    - {input: FY2023 annual broad SAM, value: 1.514, unit: $B, fiscal_year: FY2023, tie_out: SAM Build section 8, used_in: chart_1}
    - {input: FY2024 annual broad SAM, value: 4.584, unit: $B, fiscal_year: FY2024, tie_out: SAM Build section 8, used_in: chart_1}
    - {input: FY2025 annual broad SAM, value: 1.583, unit: $B, fiscal_year: FY2025, tie_out: SAM Build section 8, used_in: chart_1}
    - {input: FY2026 annual broad SAM, value: 3.060, unit: $B, fiscal_year: FY2026, tie_out: SAM Build section 8, used_in: chart_1}
    - {input: FY2027 annual broad SAM, value: 4.678, unit: $B, fiscal_year: FY2027, tie_out: SAM Build section 8, used_in: chart_1}
  calculations:
    - {name: Average annual TAM, formula: "sum annual TAM / 6", output: "~$3.3B", used_in: note_1}
    - {name: Average annual broad SAM, formula: "sum annual broad SAM / 6", output: "~$2.8B", used_in: note_1}
    - {name: Annual TAM by FY, formula: "portfolio Basic Construction base (FY) x applied 35.0% supplier coefficient", output: "per-FY TAM", used_in: chart_1}
  rounding_rules: Chart labels use $B to one decimal; data block keeps three decimals.
  reconciliation: Annual TAM values sum to ~$19.84B cumulative TAM; annual broad SAM values sum to ~$16.83B cumulative broad SAM (~84.8% of TAM in each FY).

qa:
  guardrails:
    - Chart shows both annual TAM and annual broad SAM for all six fiscal years.
    - FY2024 and FY2027 are visibly annotated as the two peaks (both-class years).
    - Slide explicitly says average annual (~$3.3B TAM, ~$2.8B SAM) is not a run-rate; peaks are cadence, not volatility.
    - Broad SAM is shown moving with TAM (a ~84.8% scenario cut), never as an independent budget line.
    - Columns are clustered, not stacked; the chart is not a line chart.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN P-5c, DoD daily Contracts, SAM.gov); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit / column-width checks do not apply
