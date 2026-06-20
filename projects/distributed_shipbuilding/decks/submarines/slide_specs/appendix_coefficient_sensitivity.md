# SlideSpec - submarines `appendix_coefficient_sensitivity` (appendix A4, deck slide 23)
# Appendix sensitivity slide backing the body coefficient evidence slide (S10).
# A ranked horizontal coefficient ladder owns the left side (the primary object):
# the strict ~35.0% applied Basic Construction supplier coefficient is highlighted
# even though it is the lowest bar, with the broader place-of-performance views (AP
# and LLTM reference, all-gated POP anchor, GFE-excluded, distributed-production,
# the outsourced band) shown as sensitivity and evidence. ONE compact corpus-controls
# table on the right carries the corpus controls (it does NOT repeat S10's six
# evidence cards); a bottom guardrail strip states that only the strict coefficient
# feeds headline TAM.

meta:
  slide_id: subs-a4
  slide_order: A4                 # appendix letter (registry comment maps A4 -> appendix_coefficient_sensitivity)
  module_name: appendix_coefficient_sensitivity.py
  slide_type: appendix
  section: Appendix
  archetype: ranked_bar_plus_evidence_cards
  story_role: Defend the strict ~35.0% applied non-nuclear supplier coefficient that feeds headline TAM by showing how TAM moves as the coefficient varies, with the broader place-of-performance views held out as sensitivity and evidence only.
  inputs:
    - Sensitivity section 2 (coefficient ladder)                               # validation_sensitivity.py §2
    - TAM Build section 3 (per-stream POP supplier coefficients)               # model_tam_build.py §3
    - TAM Build section 3c-3d (distributed-production and scope variants)
    - POP Corpus section 1 (gated POP corpus rollup)                           # data_pop_corpus.py §1
  related_appendix: []

chrome:
  section: Appendix
  breadcrumb_topic: Coefficient sensitivity
  title_topic: Coefficient Sensitivity
  title_finding: The strict 35.0% supplier coefficient feeds TAM; broader POP views are sensitivity
  layout: slideLayout4            # -> module-level LAYOUT
  sources:
    - U.S. DoD daily Contracts announcements
    - GAO-25-106286
    - FAR 52.204-10
  source_line_exact: "Sources: (1) U.S. DoD daily Contracts announcements; (2) GAO-25-106286; (3) FAR 52.204-10"

story:
  objective: Show how headline TAM moves as the supplier coefficient varies, with the strict ~35.0% non-nuclear Basic Construction coefficient as the applied input and the broader place-of-performance views (AP and LLTM reference, all-gated POP, GFE-excluded, distributed-production, the 50-65% outsourced band) as sensitivity and evidence only.
  do_not_say:
    - Do not multiply the broader POP views (48.5%, 51.8%, ~54.5%, ~78%, the 50-65% band) into headline TAM on this slide.
    - Do not treat the AP and LLTM reference coefficient as applied; its additive base is $0.
    - Do not hide that the strict 35.0% is the lowest view; that conservatism is the point.
    - Do not present a broader place-of-performance view as the headline coefficient.
  known_caveats:
    - The strict applied coefficient is ~35.0% (precisely ~35.0235% in the workbook); render to one decimal as 35.0%.
    - Place-of-performance views are a different lens (where work is performed) than the strict non-nuclear supplier coefficient (commercial supplier manufacturing opportunity); keep the strict-vs-broad distinction explicit.
    - Largest-action concentration (48.8%) and the 10.1% unparsed share remain limitations even with 100% confirmation coverage of in-scope non-GFE dollars.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_corpus_controls_table
  # Left 58%: external chart title band over the ranked coefficient ladder (primary).
  # Right ~38%: one compact corpus-controls table. Bottom: guardrail strip.
  title_band:      {x: 0%,  y: 0%,  w: 58%, h: TITLE_BAND_H}
  chart:           {x: 0%,  y: below(title_band), w: 58%, h: body_until(guardrail_strip)}
  corpus_controls: {x: 62%, y: 0%,  w: 38%, h: body_until(guardrail_strip)}
  guardrail_strip: {x: 0%,  y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,      prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,           prominence: primary,   paint_order: 2, content: ranked horizontal bar of coefficient and place-of-performance views, tie_out: Sensitivity section 2 + TAM Build section 3}
  - {id: e3, type: table,         region: corpus_controls, prominence: secondary, paint_order: 3, content: compact corpus-controls table (6 controls), tie_out: POP Corpus section 1 + TAM Build section 3b}
  - {id: e4, type: note,          region: guardrail_strip, prominence: secondary, paint_order: 4, content: coefficient boundary guardrail}


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
      - role: lead/prefix
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0               # -> rId2
    title_element: e1
    frame_element: e2
    data:
      # Ranked descending so the strict applied coefficient is the lowest, highlighted bar.
      # The strict coefficient (BLUE_5) feeds headline TAM; every other bar is sensitivity / evidence.
      categories:
        - "Distributed, incl. unparsed (78%)"
        - "Outsourced band, high (65%)"
        - "BC stream incl-GFE (61%)"
        - "All-gated, GFE-excluded (54.5%)"
        - "All-gated POP anchor (51.8%)"
        - "Outsourced band, low (50%)"
        - "AP and LLTM reference (48.5%)"
        - "Applied non-nuclear supplier coefficient (35.0%)"
      series:
        - name: Coefficient view
          values: [0.780, 0.650, 0.610, 0.545, 0.518, 0.500, 0.485, 0.350]
          data_point_colors: [BLUE_2, BLUE_2, BLUE_2, BLUE_3, BLUE_3, BLUE_2, BLUE_2, BLUE_5]
    params:
      mode: ranked
      value_axis_format: '0%'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175       # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '0.0%'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 50
      cat_header: Coefficient and place-of-performance view
      title: null                      # house style: external exhibit_title element
    external_title:
      text: Supplier coefficient and place-of-performance views, percent of relevant corpus
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Only the strict 35.0% non-nuclear supplier coefficient feeds headline TAM; all higher bars are sensitivity and evidence.", anchor_to: e2}

tables:
  - id: corpus_controls_1
    element: e3
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Corpus controls
      purpose: summarize
      reader_takeaway: The strict coefficient rests on a screened, gated, GFE-excluded corpus with 100% confirmation coverage and a tracked unparsed share.
      row_order: breadth (rows screened, gated actions), then denominators (gated POP corpus, in-scope non-GFE corpus), then quality (confirmation coverage, unparsed share)
      highlight_rows:
        - In-scope non-GFE corpus
        - Confirmation coverage
      guardrails:
        - The unparsed share is a tracked limitation, not a haircut applied to the coefficient.
        - The in-scope non-GFE corpus is the strict-coefficient denominator.
    render:
      table_skin: rule              # light skin; the chart is the primary object, the table is secondary
      size: 900                     # LABEL_9PT
      column_widths:
        mode: ratio
        values: [2.5, 1.0]          # Control | Value
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r"]
      row_h:
        fn: estimate_row_heights
        size_pt_from: size
        header_size_pt_from: size
      rows:
        - ["Corpus control", "Value"]
        - ["POP rows screened", "658"]
        - ["Gated TAM-relevant actions", "43"]
        - ["Gated POP corpus", "$25.4B"]
        - ["In-scope non-GFE corpus", "$19.3B"]
        - ["Confirmation coverage", "100%"]
        - ["Unparsed share", "10.1%"]
      cell_fills: {}
      cell_bold: {}
      cell_text_colors: {}
      footnotes: []
    columns: []

shapes:
  - id: guardrail_1
    element: e4
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3            # secondary guardrail strip; the chart is the primary/focal object
    insets: INSETS_MESSAGE
    text: "Only the strict 35.0% non-nuclear Basic Construction supplier coefficient feeds headline TAM; the broader place-of-performance views are sensitivity and evidence."
    meaning: Boundary caveat for coefficient application; the strict-vs-broad guardrail.

images: []

commentary:
  visible:
    element: e4
    container: callout
    title: null
    bullets:
      - {lead: "Guardrail:", body: "only the strict 35.0% Basic Construction supplier coefficient feeds headline TAM; higher POP views are sensitivity."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix backs the body coefficient evidence
      slide (S10), which lands the finding that the POP corpus supports a large
      distributed-production layer but the headline coefficient stays strict. This
      appendix shows the full coefficient ladder so a diligence reader can see how
      headline TAM would move under each alternative, and why the strict input is
      the conservative floor rather than the broadest defensible view.

      THE STRICT APPLIED COEFFICIENT. The only coefficient multiplied into headline
      TAM is the strict, non-nuclear Basic Construction supplier coefficient,
      ~35.0% (precisely ~35.0235% in the workbook; render 35.0%). It is the
      dollar-weighted supplier-plus-foreign share over the gated, in-scope,
      confirmed BC-stream corpus with BPMI naval-nuclear removed as GFE. It sizes
      the non-nuclear commercial supplier manufacturing opportunity, deliberately
      narrower than "all distributed production." Pre-boundary, with BPMI naval-
      nuclear left in, the coefficient runs ~75.7% - the BPMI exclusion is exactly
      what moves it from ~75.7% to the applied ~35.0%; that ~75.7% view is
      sensitivity only and never applied.

      THE BROADER VIEWS (SENSITIVITY AND EVIDENCE ONLY).
      - AP and LLTM reference coefficient ~48.5%: the supplier share over the AP and
        LLTM POP stream. Reference only, because the AP and LLTM additive base is $0
        (see appendix A3) - it is never multiplied into headline TAM.
      - All-gated POP anchor ~51.8%: the supplier-plus-foreign share over all gated
        actions; the published v4 anchor and drift guard, directional evidence, not
        the headline input.
      - All-gated, GFE-excluded ~54.5%: both streams minus GFE; a reconciliation
        variant, not applied.
      - BC stream incl-GFE ~61%: GFE left in the denominator; a handoff reference.
      - Distributed-production view: ~68% confirmed (away from the EB yard,
        confirmed) and ~78% including unparsed (away from the EB yard incl
        single-site / no-percent parses). Broader than commercial TAM; appendix lens.
      - Place-of-performance, action-level (wiki 06 / DoD daily Contracts): across
        the 43 submarine-relevant supplier-targeted actions, ~78% of dollar value
        flowed to firms other than General Dynamics Electric Boat and ~52% flowed to
        firms outside both shipyards combined. Independent confirmation of the band,
        not a headline coefficient.
      - Outsourced-share band (wiki 06): the 50-65% industry-baseline band for
        purchased-plus-subcontracted content of complex shipbuilding (50% low, 60%
        mid, 65% high). Directional baseline, not applied.

      STRICT VS BROAD - WHY IT MATTERS. The place-of-performance views answer a
      different question (where is work performed) than the strict supplier
      coefficient (what is the addressable non-nuclear commercial supplier
      manufacturing opportunity). The strict coefficient is the lowest bar on
      purpose: anchoring headline TAM to the most conservative, GFE- and
      yard-excluded view keeps the sizing defensible, with every broader view kept
      as upside evidence rather than headline math.

      CORPUS CONTROLS (POP Corpus section 1). The place-of-performance corpus is 658
      rows; 43 are gated TAM-relevant actions. The gated POP corpus totals ~$25.4B;
      the in-scope non-GFE corpus (the strict-coefficient denominator) is ~$19.3B.
      Confirmation coverage is 100% of in-scope non-GFE dollars. The unparsed share
      is ~10.1% and stays visible as a limitation, not folded into the coefficient.
      Largest-action concentration is ~48.8% - a single-action risk note that argues
      for the strict input, not for the broader ones.

      DENSITY GUIDANCE. Default is chart + compact corpus-controls table + guardrail
      strip. To densify, add ladder context into the guardrail strip, annotate the
      chart, or add a row to the corpus-controls table; keep the strict 35.0% bar
      highlighted (BLUE_5) at every density. Do not compute new TAM sensitivity dollar
      outputs on the slide unless the workbook provides approved sensitivity labels.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [guardrail_strip, chart, corpus_controls], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Why 35.0%:"
        body: "It is the strict, non-nuclear Basic Construction supplier coefficient and the only coefficient multiplied into headline TAM; render 35.0% (workbook ~35.0235%)."
        evidence: TAM Build section 3a; Sensitivity section 2
        safe_container: guardrail_strip
        density_trigger: Always keep this visible.
      - priority: 2
        lead: "BPMI exclusion drives it:"
        body: "With BPMI naval-nuclear left in, the BC coefficient is ~75.7%; removing BPMI as GFE is exactly what produces the applied ~35.0%. The 75.7% view is sensitivity, never applied."
        evidence: Sensitivity section 2a (BPMI exclusion)
        safe_container: chart
        density_trigger: Add when an audience asks why the headline is so much below the POP views.
      - priority: 3
        lead: "Sensitivity, not headline:"
        body: "48.5% AP and LLTM, 51.8% all-gated POP, ~54.5% GFE-excluded, ~78% distributed, and the 50-65% band are support evidence; none is multiplied into headline TAM."
        evidence: TAM Build section 3c-3d; Sensitivity section 2
        safe_container: chart
        density_trigger: Add if chart labels alone do not make the role clear.
      - priority: 4
        lead: "Place of performance is a different lens:"
        body: "Action-level POP shows ~78% of dollars away from Electric Boat and ~52% outside both yards - where work is performed, not the addressable non-nuclear supplier share."
        evidence: wiki 06 (DoD contract-announcement data); FAR 52.204-10
        safe_container: guardrail_strip
        density_trigger: Add to clarify the strict-vs-broad distinction for diligence audiences.
      - priority: 5
        lead: "Corpus quality:"
        body: "43 gated actions and a $19.3B in-scope non-GFE corpus carry 100% confirmation coverage; the coefficient rests on confirmed dollars, not estimates."
        evidence: POP Corpus section 1
        safe_container: guardrail_strip
        density_trigger: Add for diligence audiences probing data quality.
      - priority: 6
        lead: "AP and LLTM is reference:"
        body: "The 48.5% AP and LLTM coefficient is reference-only because the AP and LLTM additive base is $0 (appendix A3); it is shown for completeness, not application."
        evidence: TAM Build section 3a; AP Bridge section 5
        safe_container: chart
        density_trigger: Add when this slide is shown alongside the AP and LLTM detail appendix.
      - priority: 7
        lead: "Limitation, not adjustment:"
        body: "The 10.1% unparsed share is a tracked limitation (single-site / no-percent parses), not a haircut applied to the coefficient."
        evidence: TAM Build section 3b (unparsed %)
        safe_container: corpus_controls
        density_trigger: Add if the unparsed-share control needs a qualifier.
      - priority: 8
        lead: "Concentration risk:"
        body: "Largest-action concentration is ~48.8% of the gated corpus - a single-action sensitivity that argues for the strict input rather than the broader views."
        evidence: POP Corpus section 1 (dollar-ranked corpus)
        safe_container: guardrail_strip
        density_trigger: Add for an audience focused on corpus concentration risk.
      - priority: 9
        lead: "Outsourced band context:"
        body: "Industry-baseline outsourced share for complex shipbuilding is a 50-65% band (50/60/65); the strict 35.0% supplier coefficient sits deliberately below it."
        evidence: wiki 06 (50-to-65% band); GAO-25-106286
        safe_container: chart
        density_trigger: Add for an audience benchmarking against the industry outsourcing baseline.
      - priority: 10
        lead: "Distributed-production view:"
        body: "Away-from-EB distributed production runs ~68% confirmed and ~78% including unparsed; broader than commercial TAM and held as an appendix lens, not applied."
        evidence: TAM Build section 3c
        safe_container: chart
        density_trigger: Add when the distributed-production framing is questioned.
    do_not_add:
      - computed TAM sensitivity dollar values unless approved by the workbook
      - 48.5%, 51.8%, ~54.5%, ~78%, or the 50-65% band as a headline input
      - a new coefficient derived by the slide builder
      - the ~75.7% pre-boundary coefficient presented as anything but sensitivity

data_and_calculations:
  data_inputs:
    - {input: Applied non-nuclear supplier coefficient, value: 0.350, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3a (applied; ~35.0235%), used_in: chart_1}
    - {input: AP and LLTM reference coefficient,        value: 0.485, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3a (reference; base = 0), used_in: chart_1}
    - {input: All-gated POP anchor,                     value: 0.518, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3e (published anchor), used_in: chart_1}
    - {input: All-gated, GFE-excluded,                  value: 0.545, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3d (reference variant), used_in: chart_1}
    - {input: BC stream incl-GFE,                       value: 0.610, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3d (handoff ref), used_in: chart_1}
    - {input: Distributed incl-unparsed,                value: 0.780, unit: share, year: FY2022-FY2027, tie_out: TAM Build section 3c (appendix view), used_in: chart_1}
    - {input: Outsourced band low / high,               value: 0.500 / 0.650, unit: share, year: FY2022-FY2027, tie_out: wiki 06 (industry-baseline band), used_in: chart_1}
    - {input: POP rows screened,                        value: 658,   unit: rows,    year: FY2022-FY2027, tie_out: POP Corpus section 1, used_in: corpus_controls_1}
    - {input: Gated TAM-relevant actions,               value: 43,    unit: actions, year: FY2022-FY2027, tie_out: POP Corpus section 1, used_in: corpus_controls_1}
    - {input: Gated POP corpus,                         value: 25.4,  unit: $B,      year: FY2022-FY2027, tie_out: POP Corpus section 1, used_in: corpus_controls_1}
    - {input: In-scope non-GFE corpus,                  value: 19.3,  unit: $B,      year: FY2022-FY2027, tie_out: POP Corpus section 1, used_in: corpus_controls_1}
    - {input: Confirmation coverage,                    value: 1.00,  unit: share,   year: FY2022-FY2027, tie_out: POP Corpus section 1, used_in: corpus_controls_1}
    - {input: Unparsed share,                           value: 0.101, unit: share,   year: FY2022-FY2027, tie_out: TAM Build section 3b, used_in: corpus_controls_1}
  calculations: []
  rounding_rules: Coefficient labels to one decimal percent; evidence $B to one decimal. The applied coefficient is ~35.0235% internally but renders 35.0%.
  reconciliation: Only the strict ~35.0% non-nuclear Basic Construction coefficient is applied to headline TAM; all other coefficient and place-of-performance views on this slide are sensitivity and evidence.

qa:
  guardrails:
    - Highlight the strict 35.0% bar (BLUE_5) despite it being the lowest view.
    - Do not multiply any broader POP view (48.5%, 51.8%, ~54.5%, ~78%, 50-65% band) into headline TAM.
    - Keep the strict-vs-broad distinction explicit: headline uses the strict non-nuclear supplier coefficient; place-of-performance views are sensitivity only.
    - Do not calculate unapproved TAM sensitivity dollar outputs.
    - Pass title null to the chart factory and use the external chart title element.
  source_checks:
    - Sources are the exact real citations in chrome.sources (DoD daily Contracts, GAO-25-106286, FAR 52.204-10); no internal docs, workbook tabs, wiki chapters, or chart IDs in the rendered footer.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    - "if a table exists: resolved column widths sum to its region width"
