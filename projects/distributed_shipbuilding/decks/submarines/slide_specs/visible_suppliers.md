# SlideSpec - submarines `visible_suppliers` (deck slide 15)
# Chart + table body slide: a ranked horizontal bar of the top 10 FFATA-visible
# suppliers, plus a small chart-side evidence table (recipient count, visible value,
# parent count) that frames the named list as a floor. Exercises required-if-present
# for BOTH a chart and a table.

meta:
  slide_id: subs-s15
  slide_order: 15               # deck-spec narrative position; not yet registered (KNOWN GAP, S12-S16)
  module_name: visible_suppliers.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: ranked_bar_plus_evidence_table
  story_role: Make the supplier layer tangible by naming the largest visible vendors, while warning that the visible stream is a floor, not the full layer.
  inputs:
    - Chart Data CD_15_TopVisibleSuppliers
    - Entity Master (top supplier indices, parent-normalized $)
    - SAM Build (supplier-addressable visible value)
    - Worktype Evidence
  related_appendix:
    - subs-a6   # appendix_top_25_visible_suppliers

chrome:
  section: Market sizing
  breadcrumb_topic: Visible suppliers
  title_topic: Visible Suppliers
  title_finding: The named vendor base is broad but anchored by a few large suppliers
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - FAR 52.204-10
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

story:
  objective: Show the top named visible suppliers and frame them as a floor, not a capture-target list or the full supplier layer.
  do_not_say:
    - Visible does not mean complete; FFATA names a floor, not the whole supplier layer.
    - Do not treat the ranking as a capture target list or win-probability ordering.
    - No company logos in this build.
  known_caveats:
    - FFATA captures first-tier subaward filings above the $30,000 threshold; it misses purchased material, lower-tier subcontracts, long-term agreements, and most of the HII Newport News team-build share.
    - Names are parent-normalized via SAM.gov Entity Management where the relationship is supported; classification is work-type informed, not perfect.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_right_matrix
  # Chart on the left ~64%, a chart-side evidence table to its right, and a pinned note.
  title_band: {x: 0%, y: 0%, w: 64%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 64%, h: body_until(note_strip)}
  matrix:     {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,      prominence: primary,   paint_order: 2, content: ranked bar of top 10 visible suppliers, tie_out: CD_15_TopVisibleSuppliers}
  - {id: e3, type: table,         region: matrix,     prominence: secondary, paint_order: 3, content: chart-side evidence table (counts + visible value + floor caveat), tie_out: Entity Master}
  - {id: e4, type: note,          region: note_strip, prominence: tertiary,  paint_order: 4, content: parent-normalization + floor note}


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
    e4:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:               # parent display names, Title Case (not all-caps SAM legal names), rank 1..10
        - "Northrop Grumman Corporation"
        - "Leonardo SpA"
        - "Curtiss-Wright Electro-Mechanical Corp."
        - "Scot Forge Company"
        - "ESCO Technologies Inc."
        - "DC Fabricators Inc."
        - "Rhoads Metal Fabrications, Inc."
        - "Curtiss-Wright Corporation"
        - "The Graham Corporation"
        - "Austal USA, LLC"
      series:
        - name: Visible subaward $M
          values: [1426.6, 490.6, 198.0, 197.5, 188.5, 162.9, 141.9, 110.8, 89.1, 87.6]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_3, BLUE_3, BLUE_3, BLUE_1, BLUE_1, BLUE_1, BLUE_1, BLUE_1]
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
      gap_width: 35
      cat_header: Supplier (parent)
      title: null                     # house style: external exhibit_title element
    external_title:
      text: Top 10 FFATA-visible suppliers, cumulative subaward value FY2016-FY2026
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Northrop Grumman leads visible flow by a wide margin.", anchor_to: e2}

tables:
  - id: evidence_1
    element: e3
    role: chart_side_evidence
    factory: house_table
    semantic:
      table_name: Visible-supplier evidence
      purpose: summarize       # frame the named list as a floor; not a ranking by itself
      reader_takeaway: The named bars sit inside a broader visible base, and the visible base is itself a floor.
      row_order: recipients, visible value, broader parents
      highlight_rows: []
      guardrails:
        - The visible stream is a floor, not the full supplier layer.
    render:
      table_skin: rule          # chart-side evidence: no header fill, 1.5pt header bottom-rule carries it
      size: 900                 # 9.0pt (== LABEL_9PT); row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [2.6, 1.0]      # metric label wide; value column narrow
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Visible-supplier evidence", "Value"]
        - ["Classified subaward recipients", "150"]
        - ["Supplier-addressable visible value", "~$5.46B"]
        - ["Broader FFATA-visible parents", "~759"]
      cell_fills: {}
      cell_bold: {}
      footnotes:
        - "FFATA-visible first-tier filings are a floor, not the full supplier layer; parents are normalized via SAM.gov Entity Management where supported."
    columns: []

shapes:
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Parent-normalized where SAM.gov Entity data supports the relationship. Visible value is a floor: FFATA misses purchased material, lower-tier subcontracts, long-term agreements, and most HII Newport News team-build work."   # FINEPRINT_8_5PT italic
    meaning: Names what the visible stream omits, so the bars are not read as the full layer.

commentary:
  visible:
    element: e3
    container: table_note
    title:
    bullets:
      - {lead: "Read:", body: "the named bars are a floor inside a broader, partly unseen supplier layer."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the "make it concrete" slide of the SAM section
      (S12 taxonomy -> S13 bucket TAM -> S14 scenario SAM -> S15 here -> S16 SIB
      exclusion). After sizing the serviceable market, it names the suppliers behind it
      and then bounds the claim: the FFATA-visible stream is a floor.

      THE TOP TEN (visible cumulative subaward $M, FY2016-FY2026, parent-normalized).
      Northrop Grumman ~$1,427M is the largest visible recipient by a wide margin
      (electrical/electronics, propulsion-electronics). Then Leonardo SpA ~$491M;
      Curtiss-Wright Electro-Mechanical ~$198M (electrical/power); Scot Forge ~$198M
      (forgings -> castings and forgings); ESCO Technologies ~$189M; DC Fabricators
      ~$163M and Rhoads Metal Fabrications ~$142M (structural fabrication); Curtiss-Wright
      Corporation ~$111M; The Graham Corporation ~$89M (heat exchangers -> HM&E); Austal
      USA ~$88M (structural). The list spans most work-type buckets, supporting the thesis
      that the supplier layer is real and multi-firm, not a theoretical residual.

      THE EVIDENCE FRAME. ~150 classified subaward recipients; ~$5.46B supplier-addressable
      visible value; ~759 broader FFATA-visible unique parents across the fifteen in-scope
      new-construction PIIDs (the three SIB pass-through parents excluded). The named bars
      are the top of that distribution, not the whole of it.

      WHY VISIBLE IS A FLOOR (the load-bearing caveat). FAR 52.204-10 defines first-tier
      subaward reporting narrowly and sets a $30,000 per-action threshold; it excludes
      purchased material booked as direct cost, lower-tier subcontracts, indirect/G&A
      services, and long-term standing supplier agreements. The single largest omission is
      the HII Newport News team-build share - HII-NNS performs roughly half of Virginia and
      about a fifth of Columbia construction by workload, yet appears against the GDEB
      primes at essentially 0% in recent years (a gap of 100x to 10,000x). Net: the
      FFATA-visible first-tier stream captures roughly 10-20% of the actual outsourced layer
      within Basic Construction; the other 80-90% is unseen at the named-vendor first-tier
      level. That is why the deck uses FFATA for supplier EXAMPLES and work-type allocation,
      while the headline coefficient rests on the DoD place-of-performance corpus and other
      evidence.

      CLASSIFICATION CAVEATS. Names are parent-normalized via the SAM.gov Entity Management
      API where the corporate relationship is confirmed; ~45 of the top 150 are not
      currently samRegistered=Yes (expired/deactivated), so NAICS coverage is ~93.5% of
      dollar-weighted flow but only ~70% of vendor count. Some top names are GFE-adjacent or
      span buckets; work-type classification is informed, not perfect.

      DEMAND BACKDROP (directional, not a sizing input). DoD has invested >$10B in the
      submarine industrial base (GAO-26-109068); GD has called supply chain "the gating
      item" with ~70% of critical suppliers sole-source (CRS RL32418); HII has guided +30%
      YoY outsourcing hours (HII FY26 Q1). The visible supplier base is expanding for
      structural reasons.

      DENSITY GUIDANCE. Default is chart + evidence table + floor note. To densify, add a
      work-type tag beside the top names or a second evidence row (e.g. concentration of
      the top 5), but keep the floor caveat prominent and do not turn the ranking into a
      target list.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [matrix, note_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Floor, not ceiling:"
        body: "FFATA-visible flow captures only ~10-20% of the outsourced layer in Basic Construction; the named bars are the visible floor."
        evidence: Unseen layer (wiki 12); FAR 52.204-10
        safe_container: note_strip
        density_trigger: Keep this as the first line whenever the note strip grows.
      - priority: 2
        lead: "HII Newport News gap:"
        body: "HII-NNS performs ~half of Virginia and ~a fifth of Columbia by workload yet files at ~0% against the GDEB primes - the single largest omission."
        evidence: HII Newport News gap (wiki 11); HII Form 10-K
        safe_container: note_strip
        density_trigger: Add when a reviewer asks why a known major builder is absent.
      - priority: 3
        lead: "Concentration:"
        body: "Northrop Grumman alone (~$1.43B) is a large share of the ~$5.46B visible value; the tail is long and multi-bucket."
        evidence: CD_15_TopVisibleSuppliers; Vendors and concentration (wiki 09)
        safe_container: matrix       # add a 'top 1 share' evidence row
        density_trigger: Add if the evidence table has a spare row.
      - priority: 4
        lead: "Work-type spread:"
        body: "The top names cover electrical (NG, Curtiss-Wright), structural (DC Fabricators, Rhoads, Austal), castings (Scot Forge), and HM&E (Graham)."
        evidence: Entity Master; Worktype Evidence
        safe_container: matrix
        density_trigger: Add a work-type tag column if the matrix widens.
      - priority: 5
        lead: "Not a target list:"
        body: "The ranking is visible historical flow, not capture probability or a recommended pursuit order."
        evidence: story.do_not_say
        safe_container: note_strip
        density_trigger: Add if an investor reads the bars as a pipeline.
      - priority: 6
        lead: "Parent normalization:"
        body: "Subsidiaries are rolled up to parent legal entity via SAM.gov Entity Management UEIs where confirmed; ~45 of the top 150 are not currently registered."
        evidence: SAM.gov Entity Management API; Entity Master
        safe_container: note_strip
        density_trigger: Add if a reader questions why two Curtiss-Wright lines appear.
      - priority: 7
        lead: "Why FFATA at all:"
        body: "FFATA is used for supplier examples and work-type allocation; the headline coefficient rests on the DoD place-of-performance corpus, not on summing subawards."
        evidence: methodology; DoD contract announcement data (wiki 07)
        safe_container: note_strip
        density_trigger: Add if a reader assumes the market size is summed from these bars.
      - priority: 8
        lead: "Demand backdrop:"
        body: ">$10B invested in the submarine industrial base; GD calls supply chain the gating item, ~70% sole-source; HII guiding +30% outsourcing."
        evidence: GAO-26-109068; CRS RL32418; HII FY26 Q1; Executive commentary (wiki 13)
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 9
        lead: "Threshold mechanics:"
        body: "FAR 52.204-10 sets a $30,000 per-action floor and excludes material buys, lower-tier subs, indirect/G&A, and long-term supplier agreements."
        evidence: FAR 52.204-10
        safe_container: note_strip
        density_trigger: Add if a reviewer wants the precise reason the stream is partial.
    do_not_add:
      - capture %, win-probability, or target-list framing
      - company logos (names only in this build)
      - AML3D or other SIB downstream examples (those belong on S16, with a footer update)

data_and_calculations:
  data_inputs:
    - {input: Northrop Grumman Corporation,                     value: 1426.6, unit: $M, rank: 1,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Leonardo SpA,                                     value: 490.6,  unit: $M, rank: 2,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Curtiss-Wright Electro-Mechanical Corporation,    value: 198.0,  unit: $M, rank: 3,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Scot Forge Company,                               value: 197.5,  unit: $M, rank: 4,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: ESCO Technologies Inc.,                           value: 188.5,  unit: $M, rank: 5,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: DC Fabricators Inc.,                              value: 162.9,  unit: $M, rank: 6,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Rhoads Metal Fabrications Inc.,                   value: 141.9,  unit: $M, rank: 7,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Curtiss-Wright Corporation,                       value: 110.8,  unit: $M, rank: 8,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: The Graham Corporation,                           value: 89.1,   unit: $M, rank: 9,  tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Austal USA LLC,                                   value: 87.6,   unit: $M, rank: 10, tie_out: CD_15_TopVisibleSuppliers, used_in: chart_1}
    - {input: Classified subaward recipients,                   value: 150,    unit: count,  tie_out: Entity Master, used_in: evidence_1}
    - {input: Supplier-addressable visible value,               value: 5.46,   unit: $B,     tie_out: SAM Build, used_in: evidence_1}
    - {input: Broader FFATA-visible unique parents,             value: 759,    unit: count,  tie_out: Vendors (wiki 09), used_in: evidence_1}
  rounding_rules: Whole $M on bars; visible value to two significant figures ($5.46B); counts as published (~150, ~759).
  reconciliation: Top-10 bars are a subset of the ~150 classified recipients and the ~$5.46B visible value; the named list is not expected to sum to the visible total.

qa:
  guardrails:
    - Top 10 suppliers appear in descending order with the rounded values above; Northrop Grumman is #1 by a wide margin.
    - The slide states FFATA-visible is a floor, not the full supplier layer.
    - The ranking is not framed as a capture target list.
    - Display names are Title Case parent names, not all-caps SAM legal names; no logos.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov, FAR 52.204-10); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    - slide_probe --table-fit   # optional: estimated table row-height info
    - resolved column widths sum to the matrix region width
