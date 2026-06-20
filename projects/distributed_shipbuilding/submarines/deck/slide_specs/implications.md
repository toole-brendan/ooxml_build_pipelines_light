# SlideSpec - submarines `implications` (deck slide 18)
# Closing body slide: a shape-built opportunity-priority scorecard (seven work-type
# buckets x five judgment columns) plus a pinned closing note. The scorecard is
# DECK JUDGMENT: only the average annual TAM column is workbook-computed (it ties to
# the Bucket TAM slide); addressability, qualification burden, evidence confidence,
# and priority are analyst ratings, not a modeled composite index.

meta:
  slide_id: subs-s18
  slide_order: 18
  module_name: implications.py
  slide_type: body
  section: Interpretation
  archetype: priority_scorecard_with_closing_note
  story_role: Close the main body by turning modeled bucket TAM plus qualitative addressability, qualification burden, and evidence into a diligence-priority order, without presenting a capture plan.
  inputs:
    - Bucket TAM by work-type bucket (average annual)
    - SAM Build bucket allocation
    - Worktype evidence (qualitative addressability, qualification burden, evidence confidence)
    - Analyst priority judgment (where-to-play, not workbook-computed)
    - Wiki 06 Outsourced layer within Basic Construction
    - Wiki 09 Vendors and concentration
    - Wiki 13 Executive commentary
    - Wiki 14 Navy and OSD industrial-base policy
  related_appendix: []

chrome:
  section: Interpretation
  breadcrumb_topic: Implications
  title_topic: Implications
  title_finding: Priority areas are electrical and power, structural fabrication, and piping
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records and Entity Management API
    - U.S. GAO, GAO-25-106286
    - HII and General Dynamics earnings calls
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records and Entity Management API; (2) U.S. GAO, GAO-25-106286; (3) HII and General Dynamics earnings calls"

story:
  objective: Translate the model into practical, prioritized market areas for diligence and supplier scouting, grounded in modeled bucket TAM plus qualitative judgment, without presenting a capture plan.
  do_not_say:
    - Do not call the scorecard a capture plan or a SOM.
    - Do not imply priority rank equals ease of winning; rank combines size, distributed-build fit, addressability, burden, and evidence confidence.
    - Do not introduce SOM, win probability, or price realization.
    - Do not present the qualitative columns as workbook-computed; they are analyst judgment.
  known_caveats:
    - Electrical and power is largest but likely has entrenched suppliers and high qualification burden; large does not mean easy.
    - Smaller buckets can still matter if bottlenecked or qualification-constrained.
    - The addressability, qualification-burden, evidence, and priority columns are deck judgment, not a modeled index; only the average annual TAM column is workbook-computed.

regions:
  coord_basis: BODY
  layout_pattern: priority_scorecard_with_closing_note
  scorecard:  {x: 0%, y: 0%, w: 100%, h: body_until(note_strip)}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: table, region: scorecard,  prominence: primary,  paint_order: 1, content: opportunity priority scorecard, 7 buckets x 5 judgment columns, tie_out: Bucket TAM (avg annual column only); priority is analyst judgment}
  - {id: e2, type: note,  region: note_strip, prominence: tertiary, paint_order: 2, content: closing diligence message}


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
    e2:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts: []

tables:
  - id: scorecard_1
    element: e1
    role: primary
    factory: house_table
    semantic:
      table_name: Opportunity priority scorecard
      purpose: summarize
      reader_takeaway: Electrical and power, structural fabrication and pre-outfit, and piping, valves, and pumps are the top three priority areas.
      row_order: Priority ascending from 1 to 7.
      highlight_rows: [1, 2, 3]
      guardrails:
        - Priority is a diligence order, not a capture share or win probability.
        - The average annual TAM column must match the Bucket TAM slide.
        - The addressability, burden, and evidence columns are qualitative analyst ratings, not modeled values.
    render:
      table_skin: dark
      size: 900
      column_widths:
        mode: ratio
        values: [3.7, 1.0, 1.25, 1.35, 1.0, 0.55]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "ctr", "ctr", "ctr", "ctr", "ctr"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Bucket", "Avg TAM", "Addressability", "Qual. burden", "Evidence", "Pri."]
        - ["Electrical and power", "$1,257M", "Medium", "High", "High", "1"]
        - ["Structural fab and pre-outfit", "$625M", "High", "Med-high", "High", "2"]
        - ["Piping, valves, and pumps", "$520M", "High", "High", "Med-high", "3"]
        - ["Castings and forgings", "$143M", "Medium", "Very high", "Medium", "4"]
        - ["Machining", "$98M", "High", "Medium", "Medium", "5"]
        - ["Coatings and insulation", "$101M", "Medium", "High", "Medium", "6"]
        - ["HVAC and ventilation", "$62M", "Medium", "Medium", "Medium", "7"]
      cell_fills:
        "(1,0)": BLUE_1
        "(1,1)": BLUE_1
        "(1,2)": BLUE_1
        "(1,3)": BLUE_1
        "(1,4)": BLUE_1
        "(1,5)": BLUE_1
        "(2,0)": BLUE_1
        "(2,1)": BLUE_1
        "(2,2)": BLUE_1
        "(2,3)": BLUE_1
        "(2,4)": BLUE_1
        "(2,5)": BLUE_1
        "(3,0)": BLUE_1
        "(3,1)": BLUE_1
        "(3,2)": BLUE_1
        "(3,3)": BLUE_1
        "(3,4)": BLUE_1
        "(3,5)": BLUE_1
      cell_bold:
        "(1,5)": true
        "(2,5)": true
        "(3,5)": true
      cell_text_colors: {}
      footnotes:
        - "Priority is a diligence guide, not a SOM or win-rate estimate. Avg TAM is workbook-computed; the qualitative columns are analyst judgment."
    columns:
      - {name: Bucket, unit: text, tie_out: Bucket TAM by work-type bucket}
      - {name: Avg TAM, unit: $M average annual, tie_out: Bucket TAM by work-type bucket}
      - {name: Addressability, unit: qualitative, tie_out: Worktype evidence (analyst judgment)}
      - {name: Qualification burden, unit: qualitative, tie_out: Worktype evidence (analyst judgment)}
      - {name: Evidence, unit: qualitative, tie_out: Worktype evidence (analyst judgment)}
      - {name: Priority, unit: rank, tie_out: Analyst priority judgment}

shapes:
  - id: note_1
    element: e2
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "The deck sizes opportunity, not capture. Priority should guide diligence on supplier availability, qualification paths, capacity, concentration, and make-or-buy posture by bucket."   # FINEPRINT_8_5PT italic
    meaning: Closing message that reinforces the model boundary and points to the next workstream.

commentary:
  visible:
    element: e2
    container: table_note
    title:
    bullets:
      - {lead: "Next step:", body: "test supplier qualification, capacity, concentration, and make-or-buy posture by bucket."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the closing slide for the main body, opening the
      Interpretation section's payoff. It translates the market-sizing model into
      priorities for diligence, supplier scouting, or strategic assessment. It is deck
      judgment about where to play, not a capture plan and not a workbook-computed
      index: of the five columns, only the average annual TAM figure is computed (it
      ties to the Bucket TAM slide); addressability, qualification burden, evidence
      confidence, and the priority rank are analyst ratings layered on top of that
      number. The slide must not pretend to model win probability.

      TOP THREE PRIORITIES. Electrical and power ranks first because it is the largest
      bucket by a wide margin at about $1,257M average annual TAM (38 percent of TAM).
      It also has high specialization and likely entrenched supplier positions, so it is
      important but not necessarily easy: high TAM, high qualification burden, high
      evidence confidence, medium addressability. Structural fabrication and pre-outfit
      ranks second at about $625M because it has the strongest fit with distributed
      shipbuilding and module-build logic: it is the most intuitive distributed-yard
      bucket, aligning with the policy and prime behavior in the demand-backdrop slide
      (more work moving outside the legacy yards, more module and fabrication partners).
      Piping, valves, and pumps ranks third at about $520M because it is large, central
      to submarine hull, mechanical, and electrical systems, qualification-heavy, and
      supplier-base relevant.

      REMAINING BUCKETS. Castings and forgings is smaller at about $143M but can be a
      bottleneck and carries very high qualification criticality, so it ranks fourth
      ahead of larger-feeling but more serviceable work. Machining (about $98M) is
      fragmented and serviceable, with high addressability but medium burden. Coatings
      and insulation (about $101M) is niche and qualification-driven. HVAC and
      ventilation (about $62M) is the smallest named bucket. Note that machining is
      ranked fifth ahead of coatings despite coatings carrying slightly more TAM, which
      is a deliberate judgment call reflecting addressability and burden, not a sorting
      error: priority is not a pure TAM sort.

      HOW TO USE THE SCORECARD. The slide guides where to conduct next-step diligence:
      supplier availability, qualification paths, capacity, concentration, and buyer
      behavior by bucket. The rank combines size, distributed-build relevance,
      addressability, burden, and evidence confidence. It does not indicate capture
      probability or ease of winning, and it does not apply any share, win-rate, or
      revenue haircut. Average annual TAM values reconcile to the Bucket TAM slide so
      the scorecard cannot drift from the model: electrical $1,257M, structural $625M,
      piping $520M, castings $143M, coatings $101M, machining $98M, HVAC $62M.

      WHY THE COLUMNS ARE JUDGMENT, NOT MODEL. Addressability reflects how open the
      buyer behavior and qualification path appear for a new or expanding supplier;
      qualification burden reflects the depth of certification and documentation
      required; evidence confidence reflects how much FFATA-visible and DoD-announcement
      data backs the bucket. These are deliberately qualitative so the slide does not
      manufacture false precision. If the deck is later asked for a composite score, the
      model would need to be rebuilt; do not invent one here.

      DENSITY GUIDANCE. Default is the seven-row scorecard plus the closing note. To
      densify, add a line to the closing note or step the qualitative font down one
      level; if the table does not fit, remove the evidence-confidence column before
      reducing the font too far, and keep all seven rows visible.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2]}
      dense: {add_bullets: 4, safe_containers: [scorecard, note_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Electrical and power:", body: "Largest bucket at about $1,257M, high specialization, likely entrenched supplier positions: important, not necessarily easy.", evidence: "Bucket TAM by work-type bucket", safe_container: note_strip, density_trigger: "Add if the scorecard is simplified."}
      - {priority: 2, lead: "Structural fab:", body: "Strongest fit with distributed-build and module-fabrication logic, aligning with the demand-backdrop policy and prime behavior.", evidence: "Worktype evidence; demand_backdrop (S05) (wiki 14)", safe_container: note_strip, density_trigger: "Add when presenting to supplier-scouting audiences."}
      - {priority: 3, lead: "Piping:", body: "Large at about $520M, qualification-heavy, and central to submarine hull, mechanical, and electrical systems.", evidence: "Bucket TAM by work-type bucket", safe_container: note_strip, density_trigger: "Add if the third priority needs explanation."}
      - {priority: 4, lead: "Castings:", body: "Smaller dollars at about $143M can still be a bottleneck when qualification criticality is very high.", evidence: "Worktype evidence", safe_container: note_strip, density_trigger: "Add in a dense version for a bottleneck-focused audience."}
      - {priority: 5, lead: "Machining:", body: "High addressability, medium burden, and smaller modeled TAM at about $98M; useful but not top-priority by size.", evidence: "Worktype evidence", safe_container: scorecard, density_trigger: "Use if the machining row is discussed."}
      - {priority: 6, lead: "Coatings:", body: "Qualification-driven and niche at about $101M, but still material if capacity or certification constrains work.", evidence: "Worktype evidence", safe_container: note_strip, density_trigger: "Use for the max-density version only."}
      - {priority: 7, lead: "HVAC:", body: "Smallest named bucket at about $62M but still relevant if qualification or supplier concentration creates a bottleneck.", evidence: "Worktype evidence", safe_container: note_strip, density_trigger: "Use for a comprehensive verbal walk-through."}
      - {priority: 8, lead: "No capture:", body: "Priority rank is a diligence order, not SOM, win probability, or price realization.", evidence: "Deck guardrails", safe_container: note_strip, density_trigger: "Always safe when the slide is excerpted."}
      - {priority: 9, lead: "Rank is not a TAM sort:", body: "Machining ranks ahead of coatings despite slightly less TAM; rank blends size with addressability, burden, and evidence, by design.", evidence: "Analyst priority judgment", safe_container: note_strip, density_trigger: "Add if a reviewer questions the row order."}
      - {priority: 10, lead: "Columns are judgment:", body: "Addressability, qualification burden, and evidence confidence are qualitative analyst ratings; only average annual TAM is workbook-computed.", evidence: "Worktype evidence; Bucket TAM", safe_container: note_strip, density_trigger: "Add if the audience reads the columns as modeled outputs."}
    do_not_add:
      - capture-share or SOM language
      - a bubble chart or an overly precise composite score unless the model is rebuilt
      - a claim that priority rank equals ease of winning

data_and_calculations:
  data_inputs:
    - {input: Electrical and power, value: 1257.1, unit: $M average annual TAM, addressability: Medium, qualification_burden: High, evidence_confidence: High, priority: 1, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: Structural fabrication and pre-outfit, value: 624.5, unit: $M average annual TAM, addressability: High, qualification_burden: Medium-high, evidence_confidence: High, priority: 2, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: Piping valves and pumps, value: 519.6, unit: $M average annual TAM, addressability: High, qualification_burden: High, evidence_confidence: Medium-high, priority: 3, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: Castings and forgings, value: 142.8, unit: $M average annual TAM, addressability: Medium, qualification_burden: Very high, evidence_confidence: Medium, priority: 4, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: Machining, value: 98.1, unit: $M average annual TAM, addressability: High, qualification_burden: Medium, evidence_confidence: Medium, priority: 5, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: Coatings and insulation, value: 101.5, unit: $M average annual TAM, addressability: Medium, qualification_burden: High, evidence_confidence: Medium, priority: 6, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
    - {input: HVAC and ventilation, value: 61.9, unit: $M average annual TAM, addressability: Medium, qualification_burden: Medium, evidence_confidence: Medium, priority: 7, tie_out: Bucket TAM by work-type bucket, used_in: scorecard_1}
  rounding_rules: On-slide Avg TAM values round to whole $M; qualitative categories kept short to avoid table overflow.
  reconciliation: Scorecard average annual TAM values tie to the Bucket TAM slide; the priority rank and qualitative columns are analyst judgment, not a workbook computation.

qa:
  guardrails:
    - Top three priorities are electrical and power, structural fabrication and pre-outfit, and piping, valves, and pumps.
    - The slide avoids claiming capture share, SOM, or win probability.
    - Average annual TAM values match the Bucket TAM slide.
    - The scorecard is presented as diligence priority and judgment, not a modeled composite index.
    - No "+" or "/" in visible copy except canonical labels; "make-or-buy" is spelled out.
  source_checks:
    - Sources are real external citations only: SAM.gov FFATA/FSRS and Entity Management, GAO-25-106286, and HII/GD earnings calls.
    - No workbook tabs, slide-data IDs, wiki chapters, or chart IDs are rendered in chrome.sources.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - slide_probe --table-fit
    - resolved column widths sum to the scorecard region width
