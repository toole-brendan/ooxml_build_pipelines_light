# SlideSpec — DDG tam_timing
# Body slide 9. Native stacked-column chart (TAM by FY and stream) + a no-fill KPI rail.
# Chart-only (tables: []); the KPI rail is the visible commentary. Closes the TAM-build trio
# (tam_methodology s07 -> annual_tam_build s08 -> tam_timing s09).

meta:
  slide_id: ddg-s09
  slide_order: 9
  module_name: tam_timing.py
  slide_type: body
  section: TAM Methodology
  archetype: stacked_column_plus_kpi_rail
  story_role: Stop the reader from treating the average-annual supplier TAM headline as a smooth run-rate by showing the lumpy fiscal-year profile and naming the FY26 AP and LLTM spike.
  inputs:
    - z_ChartData CD06_TAM_BY_FY (BC and AP/LLTM stream by FY)
    - TAM Build model_tam_build §5a (TAM by FY), §5d (average annual, per-hull)
    - AP Bridge data_ap_bridge §2 (AP and LLTM stream timing; FY26 CY AP)
    - Assumptions inputs_assumptions §3 (CY AP by FY), §5 (0.80 share, 0.85 coefficient)
    - Deck Outputs DO-23 .. DO-28 (Figure Register)
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (full numeric TAM build, per-FY detail)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Timing
  title_topic: TAM Timing
  title_finding: Annual supplier TAM is lumpy, with the FY26 spike driven by AP and LLTM
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
    - DoD DDG-51 daily contract announcements, July 2022 to May 2026
    - SAM.gov Acquisition Subaward Reporting Public API
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API"

story:
  objective: Show the fiscal-year supplier TAM profile by stream and make obvious that FY26 is a one-year AP and LLTM material spike, not the ongoing run-rate, while the average-annual headline stays the sizing convention.
  do_not_say:
    - Do not smooth the annual profile into a line chart; the stack is the point.
    - Do not describe ~$573M per year as a year-by-year procurement forecast.
    - Do not use a full-width takeaway bar.
    - No SOM or capture language.
  known_caveats:
    - The average-annual headline is a sizing convention, not a year-by-year demand forecast.
    - FY25 carries a small AP and LLTM contribution; FY26 carries the large one; the other years are BC-stream only in the current model.
    - Title must stay within 2 title lines at 20pt over the content width.

object_assessment:
  verdict: "Keep the full-width stacked chart. Be stricter: no side rail and no bottom readout bar. Use two quiet KPI notes and two chart annotations only."
  object_contract:
    render_pattern: full_width_stacked_column_with_quiet_kpi_notes
    expected_rendered_object_count: 7
    compound_objects:
      - {id: chart_annotations, child_count: 2, child_type: chart_annotation_overlay}
    required_focal_family: "The stacked chart owns the page; KPI notes are no-fill text, not cards."
  anti_repetition:
    versus_annual_tam_build: "Full-width timing chart, no right table."
    versus_sam_taxonomy: "Last TAM chart before a non-chart taxonomy page."
    forbidden_defaults:
      - No line chart.
      - No right rail.
      - No filled takeaway strip.

regions:
  coord_basis: BODY
  layout_pattern: stacked_column_plus_kpi_rail
  title_band: {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 100%, h: 68%}
  kpi_left:   {x: 14%, y: below(chart) + GAP, w: 33%, h: fit_content}
  kpi_right:  {x: right_of(kpi_left) + GAP, y: align_top(kpi_left), w: 39%, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external chart title (no-fill text_box above the frame)}
  - {id: e2, type: chart_frame,   region: chart,      prominence: primary,   paint_order: 2, content: stacked column chart, TAM by fiscal year and stream, tie_out: CD06_TAM_BY_FY}
  - {id: e3, type: note,          region: kpi_left,   prominence: secondary, paint_order: 3, content: no-fill KPI, average-annual convention (~$573M per year)}
  - {id: e4, type: note,          region: kpi_right,  prominence: secondary, paint_order: 3, content: no-fill KPI, FY26 is not the run-rate (~$1.23B, AP and LLTM)}
  - {id: e5, type: note,          region: note_strip, prominence: tertiary,  paint_order: 4, content: standard sizing note}

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
      data_labels: {enabled: false}
      legend: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
  table_rules: []
  shape_rules:
    - shape: kpi_avg_1
      element: e3
      profile: no_fill_kpi_note
      runs:
        - {role: label, size: LABEL_9PT, italic: true, color: DK, font: FONT}
        - {role: value, size: RIBBON_KPI_18PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "No fill/no border; value may be centered within the note region if space allows."
    - shape: kpi_fy26_1
      element: e4
      profile: no_fill_kpi_note
      runs:
        - {role: label, size: LABEL_9PT, italic: true, color: DK, font: FONT}
        - {role: value, size: RIBBON_KPI_18PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "No fill/no border; value may be centered within the note region if space allows."
    - shape: sizing_note_1
      element: e5
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts:
  - id: chart_1
    factory: column_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories: [FY22, FY23, FY24, FY25, FY26, FY27]
      series:
        - {name: BC stream, values: [245.9, 571.9, 416.9, 580.7, 35.5, 341.2], color: BLUE_3}
        - {name: AP and LLTM stream, values: [0, 0, 0, 56.6, 1190.0, 0], color: BLUE_5}
    params:
      mode: stacked          # bars sum to each FY raw total; segment makes the AP spike obvious
      value_axis_format: '"$"#,##0"M"'
      show_legend: true       # two series -> a short legend (BC stream; AP and LLTM stream)
      legend_pos: b
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: false # totals are busy; KPI rail carries the headline numbers
      cat_label_size_pt: 9
      gap_width: 80
      cat_header: Fiscal year
      title: null            # house style: external exhibit_title element (e1)
    external_title:
      text: Supplier TAM by fiscal year and stream
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "FY26 peak is almost entirely AP and LLTM material.", anchor_to: e2}
      - {text: "Average-annual values size the market; supplier demand is fiscally lumpy.", anchor_to: e2}

tables: []                   # NONE on this slide -> the profile is the chart; the KPI rail is shapes

images: []

shapes:
  - id: kpi_avg_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: |
      Average-annual convention
      ~$573M per year
    meaning: Keeps the deck headline in view while labeling it explicitly as an average-annual sizing convention, not a per-year forecast.
  - id: kpi_fy26_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: |
      FY26 is not the run-rate
      ~$1.23B, driven by AP and LLTM
    meaning: Interprets the spike without letting it read as a recurring annual run-rate.
  - id: sizing_note_1
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note; reinforces the average-annual convention and the SOM exclusion.

commentary:
  visible:
    element: e4
    container: method_note
    title:
    bullets:
      - {lead: "Read:", body: "FY26 is a one-year AP and LLTM material spike, not the steady annual run-rate."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It closes the TAM-build trio (S07 tam_methodology ->
      S08 annual_tam_build -> S09 here) and exists to defuse one specific misread:
      that the ~$573M per year supplier TAM headline means each fiscal year carries the
      same supplier demand. It does not. The headline is an average-annual sizing
      convention (FY22-27 cumulative ~$3,438.6M / 6 years = ~$573M per year); the
      modeled per-FY profile is lumpy. [tie-out: TAM Build §5a, §5d]

      THE MODELED FISCAL-YEAR PROFILE (CD06_TAM_BY_FY; $M total, BC + AP/LLTM).
      FY22 ~$245.9M (all BC), FY23 ~$571.9M (all BC), FY24 ~$416.9M (all BC),
      FY25 ~$637.3M (~$580.7M BC + ~$56.6M AP/LLTM), FY26 ~$1,225.5M (~$35.5M BC +
      ~$1,190.0M AP/LLTM), FY27 ~$341.2M (all BC). The six totals sum to ~$3,438.7M
      (~$3.44B) and average to ~$573M per year. BC by FY sums to ~$2,192M (~$2.19B);
      AP/LLTM by FY sums to ~$1,247M (~$1.25B). [tie-out: TAM Build §5a; CD06_TAM_BY_FY]

      WHY FY26 SPIKES (the mechanism, not just the shape). The AP and LLTM stream is
      advance-procurement / long-lead-time material, and in the model it is funded in a
      concentrated fiscal year: CY AP is ~$83.2M in FY25 and ~$1,750.0M in FY26. Apply
      the 80.0% ship-construction share and the 85.0% AP supplier coefficient and FY26
      yields ~$1,190M of supplier TAM (~$1,750.0M x 0.80 x 0.85) against only ~$35.5M of
      BC stream that year, so the FY26 column is ~97% AP and LLTM. This is procurement
      timing for long-lead material (turbines, reduction gears, switchboards bought ahead
      of the build), not a step-change in the run-rate. [tie-out: AP Bridge §2; Inputs §3/§5]

      WHY THE BC STREAM IS ALSO LUMPY. The BC stream tracks the P-5c Basic Construction
      base by FY, which swings with the award profile across the 30-hull DDG 127-156 line
      (alternating BIW and Ingalls) and the FY23-27 multiyear blocks; FY26 in particular
      shows a low BC base. The point of the slide is that neither stream is a flat annuity;
      the average-annual figure is the right cross-deck convention precisely because the
      raw years are uneven. [tie-out: TAM Build §2b/§5a; Production Schedule]

      DENSITY GUIDANCE. Default is the stacked column + a two-KPI no-fill rail + the
      sizing note. To densify, label the FY26 stack segment directly (AP and LLTM), add
      the cumulative reconciliation (~$3.44B) or the per-hull cross-tie to the rail, or
      surface FY totals as data labels if they fit. Keep it a stacked column, never a line,
      and render AP/LLTM blanks as zero (not gaps) so the BC-only years read correctly.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4, e5]}
      dense:  {add_bullets: 3, safe_containers: [kpi_left, kpi_right, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Average is a convention:"
        body: "~$573M per year is FY22-27 cumulative TAM divided by six years, a sizing convention, not a per-year procurement forecast."
        evidence: TAM Build §5d (avg_annual = cumulative / n_years)
        safe_container: kpi_left
        density_trigger: Add when an audience may equate TAM with a run-rate.
      - priority: 2
        lead: "FY26 spike mechanism:"
        body: "FY26 reaches ~$1.23B because CY AP of ~$1,750M that year, times the 80% share and 85% coefficient, contributes ~$1,190M of AP and LLTM TAM."
        evidence: AP Bridge §2; Inputs §3 (CY AP FY26)
        safe_container: kpi_right
        density_trigger: Add to explain the spike rather than just flag it.
      - priority: 3
        lead: "FY26 is mostly AP:"
        body: "Against the ~$1,190M AP and LLTM contribution, FY26 carries only ~$35.5M of BC stream, so the column is ~97% AP and LLTM."
        evidence: CD06_TAM_BY_FY (FY26 split)
        safe_container: chart
        density_trigger: Add as a chart annotation on the FY26 column.
      - priority: 4
        lead: "FY25 bridge:"
        body: "FY25 carries the only other AP and LLTM contribution, ~$56.6M, against ~$580.7M of BC stream."
        evidence: CD06_TAM_BY_FY (FY25 split)
        safe_container: note_strip
        density_trigger: Add in a dense version to show AP is not unique to FY26.
      - priority: 5
        lead: "BC-only years:"
        body: "FY22, FY23, FY24, and FY27 are BC-stream only in the modeled timing profile; the BC stream is itself lumpy with the award schedule."
        evidence: TAM Build §5a; Production Schedule
        safe_container: note_strip
        density_trigger: Add if the stream legend is not enough.
      - priority: 6
        lead: "Cumulative reconciliation:"
        body: "The lumpy profile still ties to ~$3.44B cumulative FY22-27 portfolio TAM (BC ~$2.19B plus AP and LLTM ~$1.25B)."
        evidence: TAM Build §5a/§5c; DO-23 .. DO-28
        safe_container: note_strip
        density_trigger: Add when tying back to the annual TAM-build slide.
      - priority: 7
        lead: "Per-hull cross-tie:"
        body: "The same ~$3.44B is ~$265M of supplier TAM per in-window hull across 13 hulls; the per-FY swing is timing, not a change in per-hull content."
        evidence: TAM Build §5d (per-hull, 13 in-window hulls)
        safe_container: note_strip
        density_trigger: Add for an audience sizing the per-hull opportunity.
      - priority: 8
        lead: "Long-lead material:"
        body: "AP and LLTM is advance procurement of long-lead items (turbines, reduction gears, switchboards) bought ahead of the build, hence the concentrated funding year."
        evidence: AP Bridge §1; wiki 03 (GFE/other layers)
        safe_container: kpi_right
        density_trigger: Add when an audience asks why AP concentrates in one year.
      - priority: 9
        lead: "No smoothing:"
        body: "A smoothed line would hide the one-year AP and LLTM material spike; the stacked column is what makes the cause legible."
        evidence: build discipline (stacked, not line)
        safe_container: chart
        density_trigger: Add only if a reviewer suggests a line chart.
    do_not_add:
      - a line chart that smooths the fiscal-year profile
      - a full-width takeaway bar
      - any language implying FY26 is the recurring supplier TAM run-rate
      - SOM, capture, or win-probability language

data_and_calculations:
  data_inputs:
    - {input: FY22 TAM, value: 245.9,  unit: $M, year: FY22, tie_out: CD06_TAM_BY_FY / TAM Build §5a (all BC), used_in: chart_1}
    - {input: FY23 TAM, value: 571.9,  unit: $M, year: FY23, tie_out: CD06_TAM_BY_FY / TAM Build §5a (all BC), used_in: chart_1}
    - {input: FY24 TAM, value: 416.9,  unit: $M, year: FY24, tie_out: CD06_TAM_BY_FY / TAM Build §5a (all BC), used_in: chart_1}
    - {input: FY25 TAM, value: 637.3,  unit: $M, year: FY25, tie_out: CD06_TAM_BY_FY (580.7 BC + 56.6 AP/LLTM), used_in: chart_1}
    - {input: FY26 TAM, value: 1225.5, unit: $M, year: FY26, tie_out: CD06_TAM_BY_FY (35.5 BC + 1190.0 AP/LLTM), used_in: chart_1}
    - {input: FY27 TAM, value: 341.2,  unit: $M, year: FY27, tie_out: CD06_TAM_BY_FY / TAM Build §5a (all BC), used_in: chart_1}
  calculations:
    - {name: average annual TAM, formula: FY22-27 cumulative TAM (~3438.6) / 6 fiscal years, output: ~$573M per year, used_in: kpi_avg_1}
    - {name: FY26 AP and LLTM contribution, formula: CY AP 1750.0 x 0.80 ship-construction share x 0.85 AP supplier coefficient, output: ~$1190M, used_in: chart_1}
    - {name: stream cumulatives, formula: sum BC by FY = ~2192; sum AP/LLTM by FY = ~1247, output: ~$3.44B portfolio, used_in: reserve}
  rounding_rules: Show fiscal-year totals as whole $M when labeled; FY26 peak as ~$1.23B; cumulative in $B to two decimals.
  reconciliation: Fiscal-year totals sum to ~$3.44B cumulative TAM and average to ~$573M per year. The annual profile is timing only; it does not change the cumulative, the per-hull content, or the SAM cuts. SAM is a strict subset of TAM, never SOM.

qa:
  guardrails:
    - FY26 total is shown as ~$1.23B and the stack is mostly AP and LLTM.
    - Average-annual TAM is labeled as a convention, not a run-rate.
    - Chart remains a stacked column, not a line chart; AP/LLTM blanks render as zero, not gaps.
    - The fiscal-year totals reconcile to ~$3.44B cumulative.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal docs, workbook tabs, or chart IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    - "no table on this slide -> table-fit / column-width checks do not apply"
