# SlideSpec — DDG appendix_ap_lltm_sensitivity
# Appendix slide A4. AP and LLTM stream build table + a 3x3 sensitivity matrix on the two
# editable AP knobs (ship-construction share, AP supplier coefficient), with a line-level
# treatment cue and the standard sizing note. No chart (two measured native tables).

meta:
  slide_id: ddg-a4
  slide_order: A4
  module_name: appendix_ap_lltm_sensitivity.py
  slide_type: appendix
  section: Appendix
  archetype: assumption_table_plus_sensitivity_matrix
  story_role: Document the AP and LLTM stream as an assumption-driven second TAM stream (no DDG AP POP corpus exists), with its line-level exclusions and its sensitivity to the two editable AP knobs.
  inputs:
    - AP Bridge §2 TAM-base derivation (CY AP in-window x ship-construction share x supplier coeff)
    - AP Bridge §3 line-level classification (INCLUDE / EXCLUDE / IN BC ALREADY)
    - Sensitivity §4 AP/LLTM stream (editable knobs + BC/AP split)
    - Assumptions §3 AP/LLTM values (CY AP by FY) + §5 AP/LLTM knobs
    - TAM Build §5 portfolio TAM (DO-01) for the portfolio-share denominator
    - TAM Build §3a BC disclosed-only coefficient note (masters ~93% of BC corpus)
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (portfolio TAM bridge)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: AP and LLTM sensitivity
  title_topic: AP and LLTM Sensitivity
  title_finding: The AP and LLTM stream is assumption-driven and contributes about 36% of portfolio TAM
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, Line Item 2122
    - CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109
    - DoD daily contract announcement, DDG 51 FY23-27 multiyear award, Aug. 1, 2023
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, Line Item 2122; (2) CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; (3) DoD daily contract announcement, DDG 51 FY23-27 multiyear award, Aug. 1, 2023"

story:
  objective: Show the AP and LLTM stream build (CY AP in-window x 80.0% ship-construction share x 85.0% supplier coefficient = ~$1.25B cumulative, ~$208M per year), document the line-level treatment, and bound the stream against the two editable AP knobs.
  do_not_say:
    - Do not treat AP and LLTM as part of the Basic Construction stream.
    - Do not present the 85.0% AP supplier coefficient as measured; it is an Inputs assumption (no DDG AP POP corpus).
    - Do not re-add Power Conversion Modules already moved into Basic Construction.
    - Do not mix cumulative matrix values with annualized labels.
    - Do not present the disclosed-only BC coefficient as the applied BC coefficient.
  known_caveats:
    - The 85.0% AP supplier coefficient is an editable Inputs knob, not a coefficient measured over a POP corpus.
    - In-window CY AP is FY25-27 only (FY22-24 AP sits in Prior Years), so the base is a lower bound.
    - Sensitivity matrix values are FY22-27 cumulative $M, not annualized.
    - AP stream timing is lumpy by fiscal year (FY26 carries the bulk); the headline smooths it across six years.

object_assessment:
  verdict: "Keep two native tables. The build table and sensitivity matrix are legitimate rectangular data; do not turn them into cards."
  object_contract:
    render_pattern: assumption_build_table_plus_sensitivity_matrix
    expected_rendered_object_count: 5
    compound_objects: []
    required_focal_family: "Build table is primary; sensitivity matrix is secondary; treatment cue is no-fill."
  anti_repetition:
    appendix_rule: "No chart. Sensitivity is a table, not a nine-card grid."
    forbidden_defaults:
      - No chart.
      - No card matrix.
      - Do not imply AP coefficient is measured.

regions:
  coord_basis: BODY
  layout_pattern: assumption_table_plus_sensitivity_matrix
  build_table:   {x: 0%, y: 0%, w: 54%, h: fit_content}
  treatment_cue: {x: 0%, y: below(build_table) + GAP, w: 54%, h: fit_content}
  sens_title:    {x: right_of(build_table) + GAP, y: align_top(build_table), w: remaining, h: TITLE_BAND_H}
  sensitivity:   {x: right_of(build_table) + GAP, y: below(sens_title), w: remaining, h: fit_content}
  note_strip:    {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: table,         region: build_table,   prominence: primary,   paint_order: 1, content: AP and LLTM stream build table (CY AP to stream TAM), tie_out: AP Bridge §2}
  - {id: e2, type: note,          region: treatment_cue, prominence: secondary, paint_order: 2, content: line-level INCLUDE / EXCLUDE / IN BC ALREADY cue, tie_out: AP Bridge §3}
  - {id: e3, type: exhibit_title, region: sens_title,    prominence: tertiary,  paint_order: 3, content: external title for the sensitivity matrix}
  - {id: e4, type: table,         region: sensitivity,   prominence: secondary, paint_order: 4, content: AP and LLTM cumulative TAM 3x3 sensitivity matrix, tie_out: Sensitivity §4}
  - {id: e5, type: note,          region: note_strip,    prominence: tertiary,  paint_order: 5, content: standard sizing note}

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
    - table: ap_stream_build
      element: e1
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
    - table: ap_sensitivity_matrix
      element: e4
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: sens_title_1
      element: e3
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: line_treatment
      element: e2
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Lead/body paragraphs; keep no fill/no border and do not render as chips."
    - shape: sizing_note
      element: e5
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts: []

tables:
  - id: ap_stream_build
    element: e1
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: AP and LLTM stream build
      purpose: calculate
      reader_takeaway: CY AP in-window x 80.0% ship-construction share x 85.0% supplier coefficient yields ~$1.25B cumulative, ~$208M per year, about 36% of portfolio TAM.
      row_order: CY Advance Procurement in-window, ship-construction share, AP and LLTM supplier coefficient, AP and LLTM stream TAM
      highlight_rows: [AP and LLTM stream TAM]
      guardrails:
        - AP and LLTM is additive only after GFE-heavy and weapons flows are excluded.
        - The 85.0% supplier coefficient is an Inputs assumption, not measured over a POP corpus.
        - Use "AP and LLTM", not slash notation, in visible labels.
    render:
      table_skin: light
      size: 850
      column_widths:
        mode: ratio
        values: [2.5, 1.0, 1.0, 1.0, 2.0]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "r", "ctr", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Step", "Cum $M", "Avg $M per year", "Share or coeff.", "Treatment note"]
        - ["CY Advance Procurement, in-window", "1,833.2", "305.5", "n.a.", "FY25-27 CY AP base"]
        - ["x ship-construction share", "1,466.6", "244.4", "80.0%", "Strips AWS EOQ and other GFE"]
        - ["x AP and LLTM supplier coefficient", "1,246.6", "207.8", "85.0%", "Inputs assumption (no AP POP corpus)"]
        - ["AP and LLTM stream TAM", "1,246.6", "207.8", "36.3%", "Share of ~$3.44B portfolio TAM"]
      cell_fills:
        "(4,0)": BLUE_2
        "(4,1)": BLUE_1
      cell_bold:
        "(4,0)": true
        "(4,1)": true
      cell_text_colors: {}
      footnotes:
        - "In-window CY AP is FY25-27 (FY22-24 AP sits in Prior Years); a lower bound."
    columns:
      - {name: Step, unit: text, tie_out: AP Bridge §2, formula: null}
      - {name: Cum $M, unit: $M cumulative, tie_out: AP Bridge §2, formula: null}
      - {name: Avg $M per year, unit: $M per year, tie_out: AP Bridge §2, formula: "cumulative divided by six"}
      - {name: Share or coeff., unit: percent, tie_out: Assumptions §5 knobs, formula: null}
      - {name: Treatment note, unit: text, tie_out: AP Bridge §3, formula: null}
  - id: ap_sensitivity_matrix
    element: e4
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: AP and LLTM cumulative TAM sensitivity
      purpose: sensitivity
      reader_takeaway: The two editable AP knobs bound the stream between ~$962M and ~$1,568M cumulative across the 3x3 grid; the central case is ~$1,247M.
      row_order: 70% share, 80% share, 90% share
      highlight_rows: [80% share]
      guardrails:
        - Matrix values are FY22-27 cumulative $M, not annualized.
        - Cell = CY AP in-window $1,833.224M x row share x column coefficient.
        - The 80% row x 85% column central cell ties to the build table's ~$1,246.6M.
    render:
      table_skin: light
      size: 900
      column_widths:
        mode: ratio
        values: [1.2, 1.0, 1.0, 1.0]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "r", "r"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Share", "AP coeff 75%", "AP coeff 85%", "AP coeff 95%"]
        - ["70%", "962", "1,091", "1,219"]
        - ["80%", "1,100", "1,247", "1,393"]
        - ["90%", "1,237", "1,403", "1,568"]
      cell_fills:
        "(2,0)": BLUE_2
        "(2,2)": BLUE_1
      cell_bold:
        "(2,0)": true
        "(2,2)": true
      cell_text_colors: {}
      footnotes:
        - "Matrix values are FY22-27 cumulative $M; central case (80% x 85%) = ~$1,247M."
    columns: []

shapes:
  - id: sens_title_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "AP and LLTM cumulative TAM sensitivity, $M"
    meaning: External title above the 3x3 sensitivity matrix; no-fill italic title box.
  - id: line_treatment
    element: e2
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text:
      paragraphs:
        - {lead: "Include:", body: "Ship Construction EOQ and supplier-addressable long-lead material."}
        - {lead: "Exclude:", body: "Aegis Weapon System EOQ, Other GFE, VLS, weapons and ordnance AP, WPN and OPN flows."}
        - {lead: "Already in BC:", body: "Power Conversion Modules moved into Basic Construction in FY23; do not re-add."}
    meaning: Line-level treatment cue beneath the AP build table; explains what is in and out of the supplier-addressable AP stream.
  - id: sizing_note
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing convention note.

images: []

commentary:
  visible:
    element: e2
    container: method_note
    title: Treatment
    bullets:
      - {lead: "Separate stream:", body: "AP and LLTM is additive to BC only after GFE-heavy and weapons flows are excluded."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix backs the AP and LLTM stream (the second of the two
      portfolio-TAM streams) and is the backup for why the lumpy FY26 AP value on the annual
      TAM-timing slide is not a model error. The key honesty point of the page: unlike the BC
      stream (whose 12.5% supplier coefficient is COMPUTED over a gated, MYP-corrected POP
      corpus), the AP and LLTM stream is ASSUMPTION-DRIVEN. There is no DDG advance-procurement
      FFATA POP corpus to SUMPRODUCT a coefficient over, so the 85.0% AP supplier coefficient is
      an editable Inputs knob (TAM Build §3a marks it "Inputs knob - no DDG AP POP corpus").
      That is why this appendix leads with a sensitivity grid rather than a point estimate.
      [tie-out: TAM Build §3a; AP Bridge §2; Sensitivity §4]

      CORE AP BUILD (AP Bridge §2, Assumptions §3/§5). CY Advance Procurement in-window is
      ~$1,833.2M cumulative (the FY25 ~$83.2M + FY26 ~$1,750.0M CY-AP rows on Inputs LI 2122;
      FY22-24 AP sits in Prior Years, so this is a lower bound). Applying the 80.0%
      ship-construction share gives a non-GFE AP base of ~$1,466.6M cumulative; applying the
      85.0% AP supplier coefficient yields ~$1,246.6M cumulative, ~$207.8M per year (cumulative
      / 6). That stream is 36.3% of the ~$3,438.6M portfolio TAM, with the BC stream the
      remaining 63.7%. Headline check: BC ~$365M/yr (~$2.19B), AP and LLTM ~$208M/yr (~$1.25B),
      portfolio ~$573M/yr (~$3.44B). [tie-out: AP Bridge §2 (cy_ap_inwindow, ap_tam); TAM Build §5]

      LINE-LEVEL TREATMENT (AP Bridge §3). INCLUDE: Ship Construction EOQ and supplier-addressable
      long-lead material (the ship-construction share strips out the GFE part of CY AP). EXCLUDE:
      AWS EOQ (Aegis Weapon System, GFE-controlled combat system, default out), Other GFE / CBSP
      AP (Navy-furnished equipment), and VLS / weapons / ordnance AP (WPN/OPN appropriation, not
      SCN ship construction). IN BC ALREADY: Power Conversion Modules were moved GFE -> Basic
      Construction in FY23, so they must NOT be re-added to the AP stream (no double-count). The
      ship-construction-vs-AWS/other-GFE split is itself an editable Inputs knob because the P-10
      line items do not parse cleanly. No-double-count rule: P-5c BC is net of prior-year AP, so
      CY AP is additive and the prior-yr-AP credit in the TAM stream bases is 0. [tie-out: AP Bridge §3, §4]

      SENSITIVITY GRID (Sensitivity §4; cell = $1,833.224M x row share x column coeff). The 3x3
      crosses ship-construction share of CY AP at 70% / 80% / 90% with AP supplier coefficient at
      75% / 85% / 95%. Cumulative $M cells: 70%/75% ~962, 70%/85% ~1,091, 70%/95% ~1,219;
      80%/75% ~1,100, 80%/85% ~1,247 (central), 80%/95% ~1,393; 90%/75% ~1,237, 90%/85% ~1,403,
      90%/95% ~1,568. So the editable knobs bound the stream between ~$962M and ~$1,568M
      cumulative (a ~+/-25% band around the central ~$1,247M), or roughly ~$160M-$261M per year.
      Keep the matrix cumulative to avoid mixing two annualization conventions on one small table.
      [tie-out: Sensitivity §4; AP Bridge §2]

      THE BC DISCLOSED-ONLY CONTRAST (why the AP knob honesty matters; TAM Build §3a). The BC
      stream's applied 12.5% supplier coefficient is MYP-corrected: it folds the $-redacted
      BIW/Ingalls FY23-27 multiyear masters back in at reconstructed POP. A "disclosed-only" BC
      coefficient that EXCLUDES those masters is materially lower, because the masters are ~93% of
      the BC corpus and the redaction over-weights GFE. The disclosed ~87% outside-yards POP is an
      ARTIFACT of that redaction (MYP-corrected outside-yards is ~33%, live ~32.8%) and must never
      be presented as a coefficient. The AP stream has no equivalent corpus at all, which is the
      whole reason its coefficient is an explicit assumption and this page is a sensitivity page.
      [tie-out: TAM Build §3a/§3b; Sensitivity §1-§3]

      BUILDER GUIDANCE. Two measured native tables; no chart. Keep the sensitivity matrix to 3x3.
      Use one decimal in the build table (cum $M, avg $M/yr) and whole $M in the matrix. State the
      matrix is cumulative. No slash notation in visible AP and LLTM labels.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4, e5]}
      dense:  {add_bullets: 3, safe_containers: [treatment_cue, sensitivity, build_table], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Assumption, not corpus:"
        body: "The 85.0% AP supplier coefficient is an editable Inputs knob; DDG advance procurement has no FFATA POP corpus to measure a coefficient over."
        evidence: TAM Build §3a; AP Bridge §2
        safe_container: treatment_cue
        density_trigger: Add whenever a reviewer asks how the AP coefficient was derived.
      - priority: 2
        lead: "Central case:"
        body: "80.0% ship-construction share x 85.0% supplier coefficient yields ~$1.25B cumulative, ~$208M per year."
        evidence: AP Bridge §2; Sensitivity §4
        safe_container: build_table
        density_trigger: Add if the highlighted stream-TAM row is simplified.
      - priority: 3
        lead: "Portfolio share:"
        body: "AP and LLTM is 36.3% of the ~$3.44B portfolio TAM; the BC stream is the remaining 63.7%."
        evidence: Sensitivity §4; TAM Build §5
        safe_container: build_table
        density_trigger: Add if a side cue is added next to the build table.
      - priority: 4
        lead: "Matrix bounds:"
        body: "The 3x3 sensitivity spans ~$962M to ~$1,568M cumulative, roughly a 25% band on each side of the ~$1,247M central case."
        evidence: Sensitivity §4
        safe_container: sensitivity
        density_trigger: Add if the matrix title band has room.
      - priority: 5
        lead: "In-window lower bound:"
        body: "CY AP in-window is FY25-27 only (~$1,833.2M); the FY22-24 AP sits in Prior Years, so the base understates lifetime AP."
        evidence: AP Bridge §2 (cy_ap_inwindow note)
        safe_container: treatment_cue
        density_trigger: Add if a reader asks why FY22-24 AP is not in the base.
      - priority: 6
        lead: "FY26 lumpy:"
        body: "The CY AP base is concentrated in FY26 (~$1,750M of ~$1,833M); the annual headline smooths it across six fiscal years."
        evidence: Assumptions §3 (CY AP by FY)
        safe_container: treatment_cue
        density_trigger: Add to explain the FY26 spike on the annual TAM-timing slide.
      - priority: 7
        lead: "GFE filter:"
        body: "Aegis Weapon System EOQ, Other GFE, and VLS, weapons, and ordnance AP stay out of the supplier-addressable AP stream."
        evidence: AP Bridge §3
        safe_container: treatment_cue
        density_trigger: Add if the line-level treatment cue is collapsed.
      - priority: 8
        lead: "No double-count:"
        body: "Power Conversion Modules already moved into Basic Construction in FY23 must not be re-added; P-5c BC is net of prior-yr AP, so CY AP is additive."
        evidence: AP Bridge §3, §4
        safe_container: treatment_cue
        density_trigger: Add for an audit-facing version.
      - priority: 9
        lead: "BC contrast:"
        body: "The BC stream's 12.5% coefficient is computed and MYP-corrected; the AP coefficient is an assumption, which is why this page is a sensitivity grid."
        evidence: TAM Build §3a/§3b
        safe_container: sensitivity
        density_trigger: Add for an audience comparing the two streams' rigor.
      - priority: 10
        lead: "Annual view:"
        body: "The central case is ~$207.8M per year (~$1,246.6M cumulative divided by six in-window years)."
        evidence: AP Bridge §2
        safe_container: build_table
        density_trigger: Add if the average-annual column is dropped from the build table.
    do_not_add:
      - Annualized labels inside the sensitivity matrix
      - A native chart for the sensitivity grid
      - Slash notation in visible AP and LLTM labels
      - Presenting the 85.0% AP coefficient as measured rather than assumed
      - The disclosed ~87% outside-yards artifact shown as a coefficient

data_and_calculations:
  data_inputs:
    - {input: CY Advance Procurement in-window, value: 1833.2, unit: $M cumulative, year: FY25-27, tie_out: AP Bridge §2 (FY25 83.224 + FY26 1750.0), used_in: ap_stream_build and ap_sensitivity_matrix}
    - {input: Ship-construction share of CY AP, value: 80.0%, unit: percent, year: n.a., tie_out: Assumptions §5 knob (0.80), used_in: ap_stream_build}
    - {input: Non-GFE AP base, value: 1466.6, unit: $M cumulative, year: FY22-27, tie_out: AP Bridge §2 (CY AP x 0.80), used_in: ap_stream_build}
    - {input: AP and LLTM supplier coefficient, value: 85.0%, unit: percent, year: n.a., tie_out: Assumptions §5 knob (0.85), used_in: ap_stream_build}
    - {input: AP and LLTM stream TAM, value: 1246.6, unit: $M cumulative, year: FY22-27, tie_out: AP Bridge §2 (ap_tam), used_in: ap_stream_build}
    - {input: AP and LLTM stream TAM average annual, value: 207.8, unit: $M per year, year: FY22-27 average, tie_out: AP Bridge §2 / 6, used_in: ap_stream_build}
    - {input: AP and LLTM share of portfolio TAM, value: 36.3%, unit: percent, year: n.a., tie_out: Sensitivity §4 (ap_tam / (bc_tam + ap_tam)), used_in: ap_stream_build}
    - {input: Portfolio TAM, value: 3438.6, unit: $M cumulative, year: FY22-27, tie_out: TAM Build §5 portfolio_tam (DO-01), used_in: reserve context}
  calculations:
    - {name: Non-GFE AP base, formula: CY AP in-window 1833.224 x 0.80, output: ~$1,466.6M cumulative, used_in: ap_stream_build}
    - {name: AP and LLTM stream TAM, formula: non-GFE AP base 1466.58 x 0.85, output: ~$1,246.6M cumulative, used_in: ap_stream_build}
    - {name: AP stream average annual, formula: 1246.6 / 6, output: ~$207.8M per year, used_in: ap_stream_build}
    - {name: AP share of portfolio TAM, formula: 1246.6 / 3438.6, output: 36.3%, used_in: ap_stream_build}
    - {name: Sensitivity cell, formula: 1833.224 x row share x column coefficient, output: ~$962M to ~$1,568M cumulative, used_in: ap_sensitivity_matrix}
  rounding_rules: One decimal in the build table (cum $M, avg $M/yr); whole $M in the sensitivity matrix; coefficients one decimal percent.
  reconciliation: AP and LLTM is the second portfolio-TAM stream; central-case ~$1,246.6M cumulative ties the build table's stream-TAM row to the 80% x 85% sensitivity cell (~$1,247M) by construction.

qa:
  guardrails:
    - AP and LLTM stream TAM equals ~$1.25B cumulative and ~$208M per year.
    - AP and LLTM share of portfolio TAM equals 36.3% (BC = 63.7%).
    - Ship-construction share is 80.0% and the AP supplier coefficient is 85.0% (an Inputs assumption).
    - Slide excludes GFE-heavy and WPN or OPN flows; Power Conversion Modules are not re-added.
    - The disclosed ~87% outside-yards POP is never presented as a coefficient.
    - Sizing note appears; sensitivity matrix is labeled cumulative.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal AP Bridge, Sensitivity, TAM Build, or workbook tabs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "no chart on this slide -> chart rId checks do not apply"
    - "if a table exists: resolved column widths sum to its region width"
