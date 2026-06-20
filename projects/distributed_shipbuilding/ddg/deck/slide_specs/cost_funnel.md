# SlideSpec — DDG cost_funnel
# Body slide 5. Ranked FY24 cost-category bar plus a three-step denominator-decision ladder.
# The old generic right rail is removed so this is not another chart-plus-bullets slide.

meta:
  slide_id: ddg-s05
  slide_order: 5
  module_name: cost_funnel.py
  slide_type: body
  section: Scope and Denominator
  archetype: ranked_bar_plus_denominator_ladder
  story_role: Teach the denominator. Move from total DDG-51 ship cost to Basic Construction as the supplier-addressable base, and show why the GFE-heavy Electronics and Ordnance categories are excluded from the non-GFE supplier TAM.
  inputs:
    - z_ChartData CD03_COST_FUNNEL_FY24
    - SCN Budget FY24 P-5c cost categories and derived ratios (bc_pct_of_total, gfe_pct_of_total)
    - extracted/cost_funnel_summary.csv (LI 2122; FY24 row)
    - TAM Build §5e (BC construction base to supplier TAM bridge)
  related_appendix:
    - ddg-a1   # appendix_definitions_scope (cost-category definitions, GFE/CFE allocation)
    - ddg-a2   # appendix_tam_calculation (where the BC base feeds the supplier TAM)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Cost funnel
  title_topic: Cost Funnel
  title_finding: Basic Construction is the supplier-addressable base after excluding GFE-heavy cost categories
  layout: slideLayout4
  sources:
    - U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c
    - Congressional Research Service, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109
    - FAR Part 45 and FAR 52.245-1
  source_line_exact: "Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c; (2) Congressional Research Service, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; (3) FAR Part 45 and FAR 52.245-1"

story:
  objective: Establish the denominator. Show the FY24 cost-category decomposition with Basic Construction as the largest single category and the starting base for the BC supplier stream; visually de-emphasize the GFE-heavy Electronics and Ordnance block that is excluded from the non-GFE supplier TAM.
  do_not_say:
    - Do not use a literal funnel shape; ranked bars are simpler and less gimmicky.
    - Do not imply the total ship estimate is the supplier TAM.
    - Do not over-explain the HM&E contractor-furnished nuance in the chart.
    - Do not inflation-adjust the FY24 nominal cost categories on this slide.
  known_caveats:
    - HM&E is a visible P-5c category beginning in FY24, but much HM&E procurement still flows through Basic Construction as contractor-furnished equipment.
    - Electronics and Ordnance are grouped as GFE-heavy for visible simplicity; the GFE/CFE split of a specific item is set by the contract and budget cycle, not the item's identity.
    - FY24 nominal dollars are a single representative two-ship year, not the model window; the TAM model runs FY22-27.

object_assessment:
  verdict: "Aggressive redesign: keep the ranked bar, but replace the generic right commentary rail with a denominator-decision ladder so this is not another chart-plus-bullets page."
  object_contract:
    render_pattern: ranked_bar_plus_three_step_denominator_ladder
    expected_rendered_object_count: 7
    compound_objects:
      - {id: denominator_ladder, child_count: 3, child_type: text_box_step}
    required_focal_family: "Chart is the primary visual; ladder steps are light gray/blue, not dark callouts."
  anti_repetition:
    versus_scope: "Scope uses a table; this uses a numerical bar."
    versus_myp_redaction: "This has one chart only; S06 can carry the two-chart correction lab."
    forbidden_defaults:
      - No literal funnel shape.
      - No right bullet rail.
      - No extra table.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_three_step_denominator_ladder
  title_band:    {x: 0%, y: 0%, w: 66%, h: TITLE_BAND_H}
  chart:         {x: 0%, y: below(title_band), w: 66%, h: body_until(evidence_chip)}
  evidence_chip: {x: 0%, y: BODY_B - NOTE_H, w: 66%, h: NOTE_H}
  ladder_title:  {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: TITLE_BAND_H}
  ladder_total:  {x: right_of(chart) + GAP, y: below(ladder_title), w: remaining, h: 18%}
  ladder_bc:     {x: right_of(chart) + GAP, y: below(ladder_total) + GAP, w: remaining, h: 18%}
  ladder_next:   {x: right_of(chart) + GAP, y: below(ladder_bc) + GAP, w: remaining, h: 18%}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,    prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,         prominence: primary,   paint_order: 2, content: FY24 ranked cost-category bar, tie_out: CD03_COST_FUNNEL_FY24}
  - {id: e3, type: note,          region: evidence_chip, prominence: tertiary,  paint_order: 3, content: denominator chip - total ship estimate reference vs Basic Construction}
  - {id: e4, type: exhibit_title, region: ladder_title,  prominence: tertiary,  paint_order: 4, content: denominator-decision ladder title}
  - {id: e5, type: diagram,       region: ladder_total,  prominence: secondary, paint_order: 5, content: step 1 total ship cost is context}
  - {id: e6, type: diagram,       region: ladder_bc,     prominence: secondary, paint_order: 6, content: step 2 Basic Construction is the starting base}
  - {id: e7, type: diagram,       region: ladder_next,   prominence: secondary, paint_order: 7, content: step 3 supplier coefficient comes next}

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
      data_labels: {size_pt_from: params.value_label_size_pt, color: auto_contrast, font: FONT}
      legend: {enabled: false}
  table_rules: []
  shape_rules:
    - shape: evidence_chip_1
      element: e3
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: ladder_title_1
      element: e4
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: ladder_total_1
      element: e5
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: ladder_bc_1
      element: e6
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: ladder_next_1
      element: e7
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Basic Construction (60.5%)"
        - "Electronics and Ordnance GFE (32.9%)"
        - "Other smaller categories (6.6%)"
      series:
        - name: FY24 cost category value
          values: [3322, 1807, 363]
          data_point_colors: [BLUE_5, GRAY_3, GRAY_1]   # BC = blue (addressable base); GFE block = gray (excluded); residual = lightest
    params:
      mode: ranked           # single pre-sorted series; bar_chart reads top-to-bottom
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 45
      cat_header: FY24 cost category
      title: null            # house style: external exhibit_title element (e1)
    external_title:
      text: FY24 DDG-51 cost categories, both ships
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Total ship estimate is the denominator reference, not a competing bar: ~$5,492M.", anchor_to: e3}

tables: []                   # NONE on this slide -> categories are a chart; the logic is shapes

shapes:
  - id: evidence_chip_1
    element: e3
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_EVIDENCE
    text: "Total ship estimate reference: ~$5,492M. Basic Construction is ~$3,322M, or 60.5% of total."
    meaning: Small denominator note under the chart; total ship estimate is context, not a competing bar.
  - id: ladder_title_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Denominator decision"
    meaning: No-fill title for the three-step ladder; avoids a generic right rail.
  - id: ladder_total_1
    element: e5
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "1. TOTAL SHIP COST
Too broad for supplier TAM"
    meaning: First step; context only.
  - id: ladder_bc_1
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    insets: INSETS_CARD
    text: "2. BASIC CONSTRUCTION
Supplier-addressable starting base"
    meaning: Main denominator conclusion of the slide.
  - id: ladder_next_1
    element: e7
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "3. NEXT CORRECTION
Apply the MYP-corrected supplier coefficient"
    meaning: Handoff to the MYP correction and TAM build slides.

images: []

commentary:
  visible:
    element: e4
    container: right_rail
    title: Denominator read
    bullets:
      - {lead: "Boundary:", body: "total ship cost is not supplier TAM."}
      - {lead: "Base:", body: "Basic Construction is the supplier-addressable starting point."}
      - {lead: "GFE:", body: "Electronics and Ordnance explain why the gross ship number is too large."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the first numerical denominator slide, immediately after
      the scope ledger. It teaches why the model begins with Basic Construction rather than
      total ship cost, and why GFE-heavy categories are excluded from the non-GFE supplier TAM.
      It sets up the two downstream corrections: the MYP-redaction POP correction (S6) and the
      BC supplier coefficient (TAM Build §3a). [tie-out: wiki 01, 02; SCN Budget §1-2]

      THE FUNNEL (wiki 01). Total ship cost descends through the P-5c budget-justification
      categories (Plan Costs, GFE, Other, Basic Construction), then one further layer inside
      Basic Construction, splitting yard self-performed labor and overhead from the outsourced
      supplier layer. The outsourced layer within BC, plus the GFE layer in full, is the object
      of the deck; everything above BC in the funnel exists to size and qualify it. Four
      candidate denominators of "outsourced" exist; the deck headlines (2) outsourced-from-Navy
      and (3) outside-the-yards. This slide names denominator (1), the BC base.

      FY24 VALUES (representative recent two-ship year; cost_funnel_summary.csv LI 2122 FY24
      row; ties to wiki 02). Total ship estimate ~$5,492.3M. Basic Construction ~$3,322.5M =
      60.5% (the workbook bc_pct_of_total = 0.6049). Electronics ~$619.8M = 11.3%; Ordnance
      ~$1,187.5M = 21.6%; together Electronics and Ordnance GFE ~$1,807.3M = 32.9% (the workbook
      gfe_pct_of_total = 0.3291). The four smaller categories are Plans ~$82.7M (1.5%), Change
      Orders ~$91.6M (1.7%), HM&E ~$100.7M (1.8%), and Other Cost ~$87.7M (1.6%), summing to
      ~$362.6M = 6.6%. The three visible groups reconcile exactly: ~$3,322M + ~$1,807M + ~$363M
      = ~$5,492M. [tie-out: SCN Budget §1; CD03_COST_FUNNEL_FY24]

      WHY ELECTRONICS AND ORDNANCE ARE GFE-HEAVY (wiki 01, 03). The combat-system /
      electronics category is overwhelmingly GFE (Aegis at Lockheed Martin Moorestown NJ,
      AN/SPY-6 at Raytheon Andover MA, Mk 41 VLS, AN/SLQ-32 SEWIP, CEC). Ordnance is GFE (Mk 45
      5-inch gun, VLS canisters; the missiles themselves are WPN/OPN-funded and gated out
      entirely). Roughly a third of every destroyer's cost (32.9% on FY24) is direct GFE
      procurement from the GFE primes - the structural reason the supplier-TAM-relevant
      outsourced share is GFE-heavy, and why the deck's supplier TAM targets the non-GFE
      supplier-addressable BC work rather than the GFE block. [tie-out: wiki 03, 10, 11]

      WHY START AT BASIC CONSTRUCTION. BC ~60% of total ship cost (FY24) is meaningfully lower
      than the 56-80% band seen for nuclear submarines, because the destroyer is GFE-heavy.
      Plan Costs are small (1.5%) because BIW already holds a separate class Design Agent
      contract that performs most engineering work; the per-ship Plans line picks up only
      incremental class-design for that hull. BC is the prime construction base - the dollars
      that flow to BIW or Ingalls on the SCN PIID - so it is the right denominator for the
      supplier-addressable layer. [tie-out: wiki 02]

      THE HM&E NUANCE. HM&E first appears as a distinct P-5c line in the FY24 vintage
      (~$100.7M). It is contractor-furnished (CFE), not GFE, but much HM&E material can still
      flow through Basic Construction as contractor-furnished equipment, so the appearance of a
      separate HM&E line does not remove HM&E from the BC supplier-addressable story. Do not
      over-explain this in the chart; it lives in the appendix. [tie-out: wiki 03; data_ap_bridge §3]

      MODEL HANDOFF. This slide teaches the denominator, it does not calculate the final TAM.
      The BC construction base (TAM Build §5e: ~$17.47B cumulative FY22-27 over the model
      window) is what the BC supplier coefficient (12.5%, MYP-corrected) is applied to
      downstream; the AP and LLTM stream is added separately. Values here are nominal FY24
      dollars from P-5c and should not be inflation-adjusted on this slide. [tie-out: TAM Build §3a, §5e]
    density_modes:
      normal: {visible_bullets: 3, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 4, safe_containers: [ladder_total, ladder_bc, ladder_next, evidence_chip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Total reference:"
        body: "FY24 total ship estimate is ~$5,492M, but that gross number is not supplier TAM."
        evidence: SCN Budget §1 (total); cost_funnel_summary.csv FY24
        safe_container: evidence_chip
        density_trigger: Add if total ship estimate is not otherwise visible.
      - priority: 2
        lead: "GFE-heavy block:"
        body: "Electronics ~$620M (11.3%) plus Ordnance ~$1,187M (21.6%) total ~$1,807M, or 32.9%, and are excluded from the non-GFE supplier TAM."
        evidence: SCN Budget §1-2 (gfe_pct_of_total 0.3291); wiki 02
        safe_container: rail
        density_trigger: Add if the chart uses the granular P-5c categories.
      - priority: 3
        lead: "Smaller categories:"
        body: "Plans ~$83M, Change Orders ~$92M, HM&E ~$101M, and Other Cost ~$88M sum to ~$363M, or 6.6%."
        evidence: SCN Budget §1; cost_funnel_summary.csv FY24
        safe_container: evidence_chip
        density_trigger: Add only if the chart exposes the granular category list.
      - priority: 4
        lead: "BC share is structural:"
        body: "Basic Construction ~60% of total ship cost is below the 56-80% submarine band; the destroyer is GFE-heavy by design."
        evidence: wiki 02
        safe_container: rail
        density_trigger: Add when comparing DDG vs submarine cost structure.
      - priority: 5
        lead: "HM&E nuance:"
        body: "HM&E is a visible P-5c line from FY24 (~$101M), but much HM&E material still flows through Basic Construction as contractor-furnished equipment."
        evidence: wiki 03; data_ap_bridge §3
        safe_container: rail
        density_trigger: Add only in a reviewer-facing appendix variant.
      - priority: 6
        lead: "Why GFE primes are not yard subs:"
        body: "Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500 are Navy-procured GFE on separate prime contracts; the yards do not pay them, so they are outside the BC supplier-addressable layer."
        evidence: wiki 01, 03
        safe_container: rail
        density_trigger: Add if a reviewer asks why the GFE block is set aside.
      - priority: 7
        lead: "Next step:"
        body: "After isolating Basic Construction, the model corrects the outside-yards POP (S6) and applies the BC supplier coefficient before the BC base becomes TAM."
        evidence: TAM Build §3a, §3b
        safe_container: rail
        density_trigger: Add if this slide is presented standalone.
      - priority: 8
        lead: "BC base over the window:"
        body: "Over the FY22-27 model window the cumulative BC construction base is ~$17.47B; the 12.5% MYP-corrected coefficient applies to this, not to total ship cost."
        evidence: TAM Build §3a, §5e
        safe_container: evidence_chip
        density_trigger: Add when the audience asks what number the coefficient multiplies.
      - priority: 9
        lead: "Per-ship cost:"
        body: "Recent per-hull Total Ship Estimate is ~$2.7B (FY24 two-ship buy $5,492M divided by 2); the FY24 chart shows both-ship totals."
        evidence: wiki 02
        safe_container: evidence_chip
        density_trigger: Add if the audience needs a per-ship anchor.
      - priority: 10
        lead: "Nominal dollars:"
        body: "FY24 categories are then-year nominal P-5c dollars and are not inflation-adjusted on this slide."
        evidence: wiki 01 (dollar-bucketing conventions)
        safe_container: evidence_chip
        density_trigger: Add only if a reviewer asks about real-vs-nominal.
    do_not_add:
      - a literal funnel diagram
      - total ship cost presented as TAM
      - internal chart IDs, workbook tabs, or wiki chapters in rendered sources
      - inflation-adjusted values on this nominal cost-category slide

data_and_calculations:
  data_inputs:
    - {input: Total ship estimate, value: 5492, unit: $M, year: FY24, tie_out: SCN Budget §1 / cost_funnel_summary.csv, used_in: evidence_chip_1}
    - {input: Basic Construction, value: 3322, unit: $M, share_of_total: "60.5%", year: FY24, tie_out: SCN Budget §1 / CD03_COST_FUNNEL_FY24, used_in: chart_1}
    - {input: Electronics and Ordnance GFE, value: 1807, unit: $M, share_of_total: "32.9%", year: FY24, tie_out: SCN Budget §1 (gfe sum) / CD03, used_in: chart_1}
    - {input: Other smaller categories, value: 363, unit: $M, share_of_total: "6.6%", year: FY24, tie_out: SCN Budget §1 (Plans+CO+HM&E+Other), used_in: chart_1}
    - {input: Electronics, value: 620, unit: $M, share_of_total: "11.3%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
    - {input: Ordnance, value: 1187, unit: $M, share_of_total: "21.6%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
    - {input: Plans, value: 83, unit: $M, share_of_total: "1.5%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
    - {input: Change Orders, value: 92, unit: $M, share_of_total: "1.7%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
    - {input: HM&E, value: 101, unit: $M, share_of_total: "1.8%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
    - {input: Other Cost, value: 88, unit: $M, share_of_total: "1.6%", year: FY24, tie_out: SCN Budget §1, used_in: reserve}
  calculations:
    - {name: GFE-heavy grouping, formula: "Electronics 620 plus Ordnance 1187", output: "~$1,807M, or 32.9%", used_in: chart_1}
    - {name: Smaller category grouping, formula: "Plans 83 plus Change Orders 92 plus HM&E 101 plus Other Cost 88", output: "~$363M, or 6.6%", used_in: chart_1}
    - {name: visible-group reconciliation, formula: "3322 plus 1807 plus 363", output: "~$5,492M = total ship estimate", used_in: reconciliation}
  rounding_rules: Whole $M on the slide; one-decimal shares in chart category labels; FY24 nominal dollars, not inflation-adjusted.
  reconciliation: The three visible chart groups (BC, GFE-heavy block, smaller categories) sum to the FY24 total ship estimate reference (~$5,492M). Basic Construction is the supplier-addressable base; the GFE block and the residual are excluded from the non-GFE supplier TAM. The total ship estimate is a reference, not a competing bar.

qa:
  guardrails:
    - Basic Construction is clearly the supplier-addressable starting base, not the whole TAM.
    - Electronics and Ordnance are visually separated (gray) or labeled as GFE-heavy and excluded.
    - The total ship estimate is shown as a denominator reference, not a competing bar.
    - No literal funnel shape; no full-width takeaway bar.
    - FY24 values are nominal and not inflation-adjusted.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal SCN Budget tab, CD03, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    - "no table on this slide -> table-fit / column-width checks do not apply"
