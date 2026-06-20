# SlideSpec — DDG annual_tam_build
# Body slide 8. Native waterfall (annualized BC base -> POP removal -> BC stream -> add AP -> portfolio)
# plus a compact cumulative bridge table. Required-if-present for BOTH a chart and a table.

meta:
  slide_id: ddg-s08
  slide_order: 8
  module_name: annual_tam_build.py
  slide_type: body
  section: TAM Methodology
  archetype: waterfall_plus_right_bridge_table
  story_role: Reconcile the ~$573M per year supplier TAM headline to the two-stream method in the same average-annual convention, with a cumulative bridge as the audit cue.
  inputs:
    - z_ChartData CD05_ANNUAL_TAM_BUILD (currently cumulative; annualize in module)
    - TAM Build model_tam_build §5a (TAM by FY), §5c (portfolio), §5e (bridge: BC base -> POP removal -> supplier TAM)
    - AP Bridge data_ap_bridge §2 (AP and LLTM stream TAM)
    - Deck Outputs DO-17 .. DO-22
    - Figure Audit
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (full numeric TAM build)
    - ddg-a3   # appendix_myp_correction (POP removal basis)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: TAM build
  title_topic: Annual TAM Build
  title_finding: The corrected model yields ~$573M per year of supplier TAM
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
    - DoD DDG-51 daily contract announcements, July 2022 to May 2026
    - SAM.gov Acquisition Subaward Reporting Public API
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API"

story:
  objective: Make the average-annual supplier TAM calculation visible without forcing the reader into the workbook, and tie the annual waterfall to the cumulative bridge.
  do_not_say:
    - Do not use cumulative chart values while the slide is titled Annual TAM Build.
    - Do not let the negative waterfall step read as a loss; it is the non-supplier portion removed from scope.
    - Do not cite workbook tabs or internal CSVs in the source line.
    - No SOM or capture language.
  known_caveats:
    - The current workbook CD05 block stores cumulative values; the module should annualize or use an annualized block.
    - Built-in waterfall labels may not place negative labels cleanly; the bridge table is the fallback audit cue.
    - The POP removal step is prime-yard, co-prime, and GFE POP, not a loss.

object_assessment:
  verdict: "Keep the waterfall plus bridge table, but classify labels as chart annotations rather than generic callouts. The chart/table split is the point."
  object_contract:
    render_pattern: annualized_waterfall_plus_cumulative_bridge_table
    expected_rendered_object_count: 6
    compound_objects:
      - {id: chart_1_annotations, child_count: 2, child_type: chart_annotation_overlay}
    required_focal_family: "Waterfall is primary; bridge table is secondary. The negative step gets a scope-removal annotation, not a warning card."
  anti_repetition:
    versus_tam_methodology: "This is numeric reconciliation, not a formula diagram."
    versus_tam_timing: "Right-side cumulative table distinguishes it from the full-width timing chart."
    forbidden_defaults:
      - No right commentary rail.
      - No extra KPI card.

regions:
  coord_basis: BODY
  layout_pattern: waterfall_plus_right_bridge_table
  title_band:   {x: 0%, y: 0%, w: 66%, h: TITLE_BAND_H}
  chart:        {x: 0%, y: below(title_band), w: 66%, h: body_until(note_strip)}
  bridge_table: {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip:   {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary, paint_order: 1, content: external waterfall title}
  - {id: e2, type: chart_frame, region: chart, prominence: primary, paint_order: 2, content: annualized TAM waterfall, tie_out: CD05_ANNUAL_TAM_BUILD / TAM Build §5e}
  - {id: e3, type: table, region: bridge_table, prominence: secondary, paint_order: 3, content: cumulative bridge table, tie_out: TAM Build §5e cumulative rows}
  - {id: e4, type: note, region: note_strip, prominence: tertiary, paint_order: 4, content: standard sizing note}

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
      legend: {enabled: false}
  table_rules:
    - table: bridge_1
      element: e3
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: sizing_note_1
      element: e4
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts:
  - id: chart_1
    factory: waterfall_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      steps:
        - {label: "BC construction base", value: 2911.8, kind: start}
        - {label: "Less prime, co-prime, GFE POP", value: -2546.5, kind: delta}
        - {label: "BC-stream supplier TAM", value: 365.3, kind: subtotal}
        - {label: "Add AP and LLTM stream", value: 207.8, kind: delta}
        - {label: "Portfolio supplier TAM", value: 573.1, kind: end}
    params:
      value_axis_format: '"$"#,##0"M"'
      show_value_labels: false
      cat_header: Step
      title: null           # house style: external exhibit_title element (e1)
    external_title:
      text: Average annual supplier TAM build, FY22-27
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Waterfall values are average annual; the right-hand bridge is FY22-27 cumulative.", anchor_to: e2}

tables:
  - id: bridge_1
    element: e3
    role: chart_side_evidence
    factory: house_table
    semantic:
      table_name: Cumulative bridge, FY22-27
      purpose: reconcile
      reader_takeaway: The annualized waterfall ties back to the cumulative portfolio TAM of ~$3.44B.
      row_order: BC base, removed, BC stream, AP and LLTM, portfolio TAM
      highlight_rows: ["Portfolio TAM"]
      guardrails:
        - Keep this table clearly cumulative so it does not conflict with the annualized waterfall.
        - Removed row = BC base minus BC stream (~$17.47B minus ~$2.19B = ~$15.28B).
    render:
      table_skin: rule
      size: 900
      column_widths:
        mode: ratio
        values: [2.1, 1.0]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Cumulative bridge", "FY22-27"]
        - ["BC base", "~$17.47B"]
        - ["Removed", "~$15.28B"]
        - ["BC stream", "~$2.19B"]
        - ["AP and LLTM", "~$1.25B"]
        - ["Portfolio TAM", "~$3.44B"]
      cell_fills: {}
      cell_bold:
        "(5,0)": true
        "(5,1)": true
      cell_text_colors: {}
      footnotes:
        - "Chart values are average annual; bridge values are cumulative."
    columns: []

images: []

shapes:
  - id: sizing_note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note; prevents average annual and cumulative conventions from blending.

commentary:
  visible:
    element: e4
    container: method_note
    title: Unit note
    bullets:
      - {lead: "Read:", body: "the waterfall is annualized; the right-hand bridge is cumulative FY22-27."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the numeric payoff to the method slide (S07
      tam_methodology) and the setup for the timing slide (S09 tam_timing). It
      reconciles the headline supplier TAM in average-annual terms while a compact
      cumulative bridge gives the audit tie-out.

      THE ANNUALIZED WATERFALL (TAM Build §5e, divided by six years). BC construction
      base ~$2,911.8M per year (~$17,471M / 6) -> less prime, co-prime, and GFE POP
      ~$2,546.5M per year -> BC-stream supplier TAM ~$365.3M per year subtotal -> add
      AP and LLTM stream ~$207.8M per year -> portfolio supplier TAM ~$573.1M per
      year. The removal step is the non-supplier portion of the BC base: prime-yard
      (BIW), co-prime-yard (Ingalls), and GFE POP, the complement of the 12.5% BC
      supplier coefficient. It is a scope removal, not a loss. [tie-out: TAM Build §5e]

      THE CUMULATIVE BRIDGE (the right-hand table). BC construction base ~$17.47B
      minus removed ~$15.28B = BC stream ~$2.19B; add AP and LLTM ~$1.25B = portfolio
      ~$3.44B. The removal exactly equals BC base minus BC stream
      (~$17,471M minus ~$2,192M = ~$15,279M). The BC supplier coefficient is 12.5%
      (live ~12.55%); the AP and LLTM supplier coefficient is 85.0% on an 80.0%
      ship-construction share of in-window CY AP. [tie-out: TAM Build §5e; AP Bridge §2]

      VERIFICATION AGAINST SOURCE. BC base by FY: $1,960.0 + $4,558.2 + $3,322.5 +
      $4,628.2 + $282.6 + $2,719.6 = $17,471M. AP and LLTM = (CY AP $83.224M FY25 +
      $1,750.0M FY26) x 0.80 x 0.85 = $1,246.6M. Portfolio TAM = $2,192M + $1,247M =
      $3,439M (~$3.44B); / 6 = ~$573M per year. All three deck figures tie to the
      workbook. [tie-out: SCN Budget basic_construction; Inputs §3/§5]

      BUILD CAUTION. The current CD05_ANNUAL_TAM_BUILD block stores CUMULATIVE values
      (BC base +17,471; POP removal -15,279; BC stream +2,192; AP and LLTM +1,247;
      portfolio +3,439). Under the annual title, the module must annualize (divide by
      6) or use an annualized block. Do not render cumulative bars under an annual
      title without retitling the chart and the slide.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [bridge_table, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Annualized chart values:", body: "Use start +$2,911.8M, less $2,546.5M, subtotal $365.3M, add $207.8M, total $573.1M.", evidence: "TAM Build §5e annualized", safe_container: chart, density_trigger: "Builder guidance or chart annotation if needed."}
      - {priority: 2, lead: "Cumulative tie:", body: "The same bridge reconciles to ~$3.44B cumulative FY22-27 portfolio supplier TAM.", evidence: "TAM Build §5e cumulative", safe_container: bridge_table, density_trigger: "Add as a bridge-table footnote."}
      - {priority: 3, lead: "Removed portion:", body: "The negative step is prime-yard, co-prime, and GFE POP removed from the BC base; the complement of the 12.5% BC coefficient, not a loss.", evidence: "TAM Build §5e; §3a-§3c", safe_container: note_strip, density_trigger: "Add if the negative step could read as a loss."}
      - {priority: 4, lead: "Two streams:", body: "BC-stream supplier TAM (~$365M per year) plus AP and LLTM stream TAM (~$208M per year) equals the portfolio headline.", evidence: "DO-17 .. DO-22; AP Bridge §2", safe_container: note_strip, density_trigger: "Add if the method slide is skipped."}
      - {priority: 5, lead: "Coefficient note:", body: "BC coefficient is 12.5% (live ~12.55%); AP and LLTM coefficient is 85.0% on an 80.0% ship-construction share.", evidence: "TAM Build §3a; Inputs §5", safe_container: bridge_table, density_trigger: "Add in an appendix-style dense version."}
      - {priority: 6, lead: "Removal equals base minus stream:", body: "The ~$15.28B removed is exactly BC base ~$17.47B minus BC stream ~$2.19B, so the bridge cannot drift.", evidence: "TAM Build §5e (removal = bc_base - bc_tot)", safe_container: bridge_table, density_trigger: "Add if a reviewer audits the removal figure."}
      - {priority: 7, lead: "No new market:", body: "This slide reconciles the existing headline; it does not introduce a separate market definition or SAM cut.", evidence: "Commentary notes", safe_container: note_strip, density_trigger: "Add if a reviewer requests a takeaway."}
      - {priority: 8, lead: "Per-hull cross-tie:", body: "The same ~$3.44B is ~$265M per in-window hull across 13 hulls; BC-only ~$169M per hull.", evidence: "TAM Build §5d", safe_container: note_strip, density_trigger: "Add when tying to the per-hull framing."}
      - {priority: 9, lead: "Label caution:", body: "Built-in waterfall labels can be cramped on the negative step; use adjacent text labels or rely on the bridge table.", evidence: "Build notes", safe_container: chart, density_trigger: "Builder guidance only."}
    do_not_add:
      - A full-width takeaway bar that restates the title.
      - Internal workbook tab names in the rendered source line.
      - Cumulative waterfall bars under an annual slide title.
      - Reading the negative step as a loss rather than a scope removal.

data_and_calculations:
  data_inputs:
    - {input: BC construction base, value: 2911.8, unit: "$M per year", cumulative: 17.471, tie_out: "TAM Build §5e; SCN Budget basic_construction", used_in: chart_1}
    - {input: Less prime, co-prime, and GFE POP, value: -2546.5, unit: "$M per year", cumulative: -15.279, tie_out: "TAM Build §5e (BC base minus BC stream)", used_in: chart_1}
    - {input: BC-stream supplier TAM, value: 365.3, unit: "$M per year", cumulative: 2.192, tie_out: "TAM Build §5a/§5b", used_in: chart_1}
    - {input: AP and LLTM stream TAM, value: 207.8, unit: "$M per year", cumulative: 1.247, tie_out: "AP Bridge §2; TAM Build §5a", used_in: chart_1}
    - {input: Portfolio supplier TAM, value: 573.1, unit: "$M per year", cumulative: 3.439, tie_out: "TAM Build §5c; DO-17 .. DO-22", used_in: chart_1}
  calculations:
    - {name: Annualized bridge, formula: "2911.8 minus 2546.5 equals 365.3 subtotal, plus 207.8 equals 573.1", output: "573.1", used_in: chart_1}
    - {name: Cumulative bridge, formula: "17,471 minus 15,279 equals 2,192, plus 1,247 equals 3,439", output: "3,439 ($M)", used_in: bridge_1}
    - {name: Annualization, formula: "cumulative bridge component / 6 fiscal years", output: "per-year waterfall values", used_in: chart_1}
  rounding_rules: Show whole $M on the waterfall; show cumulative bridge in $B to two decimals.
  reconciliation: Annual waterfall total (~$573M per year) ties to cumulative bridge total (~$3.44B FY22-27). Removed cumulative equals BC base minus BC stream by construction.

qa:
  guardrails:
    - Hero total is ~$573M per year.
    - Cumulative portfolio TAM is ~$3.44B and appears only in the bridge table or secondary labels.
    - Annualized chart and slide title match; cumulative values are confined to the bridge.
    - Negative step is framed as a scope removal (prime, co-prime, GFE POP), not a loss.
    - Removed row equals BC base minus BC stream.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal docs, workbook tabs, or chart IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the bridge_table region width"
