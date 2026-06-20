# SlideSpec - submarines `ap_and_lltm` (deck slide 11)
# Chart-plus-warning body slide: a native waterfall from the P-10 gross AP / LLTM
# top-line down to a $0 additive TAM base, with ONE LARGE focal right-side warning card
# leading on the "$0 additive base" message (evidence and timing, not additive dollars).
# The $0 endpoint emphasis is carried as a chart_annotation on the waterfall frame, so
# there is exactly one filled focal card on the slide. tables: [] is an explicit design
# statement - this slide is a single decision rule, not a ledger.

meta:
  slide_id: subs-s11
  slide_order: 11
  module_name: ap_and_lltm.py
  slide_type: body
  section: TAM Build
  archetype: waterfall_plus_warning_card
  story_role: Resolve the likely challenge after the coefficient evidence - large supplier-heavy AP and LLTM flows are timing and reference evidence, not additive headline TAM under the P-5c boundary.
  inputs:
    - Chart Data CD_11_APBridge
    - AP Bridge section 5 (P-10 to TAM reconciliation bridge, FY22-27)
    - AP Bridge section 4 (P-10 bucket to TAM treatment crosswalk)
    - Assumptions and Controls (P-10 gross AP reference)
    - QA Reconciliation (AP and LLTM additive base = 0)
  related_appendix:
    - subs-a3   # appendix_ap_and_lltm_detail

chrome:
  section: Market sizing
  breadcrumb_topic: AP and LLTM
  title_topic: AP and LLTM
  title_finding: Gross AP is large but contributes $0 additive TAM
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10
    - U.S. DoD daily Contracts announcements
    - CRS RL32418 and CRS R41129
  source_line_exact: "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10; (2) U.S. DoD daily Contracts announcements; (3) CRS RL32418 and CRS R41129"

story:
  objective: Show that P-10 AP and LLTM are large and supplier-heavy but cannot be added to P-5c Basic Construction without double counting; the additive base is a confirmed $0.
  do_not_say:
    - Do not add P-10 AP to the P-5c Basic Construction base.
    - Do not imply AP and LLTM are irrelevant to suppliers.
    - Do not present AP and LLTM as headline additive TAM.
  known_caveats:
    - AP and LLTM are useful timing and supplier evidence, not an additive market-size base under the chosen model boundary.
    - The final additive base is exactly $0 in the headline model, by construction (anti-double-counting), not because supplier dollars are absent.
    - The ~$0.589B residual is the early-Virginia P-10 top-line over named bucket detail, not a real fourth exclusion category.

regions:
  coord_basis: BODY
  layout_pattern: waterfall_plus_warning_card
  # Left: native waterfall (gross -> $0). Right: a focal warning card stacked above a
  # quieter interpretation note. A pinned scope guardrail runs full width at the bottom.
  title_band:     {x: 0%, y: 0%, w: 68%, h: TITLE_BAND_H}
  chart:          {x: 0%, y: below(title_band), w: 68%, h: body_until(note_strip)}
  warning_card:   {x: right_of(chart) + GAP, y: below(title_band), w: remaining, h: 34%}
  interpretation: {x: warning_card.x, y: below(warning_card) + GAP, w: remaining, h: fit_content}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title,    region: title_band,     prominence: tertiary,  paint_order: 1, content: external waterfall title}
  - {id: e2, type: chart_frame,      region: chart,          prominence: primary,   paint_order: 2, content: waterfall from gross AP top-line to $0 additive base, tie_out: CD_11_APBridge}
  - {id: e3, type: callout,          region: warning_card,   prominence: primary,   paint_order: 3, content: large focal $0 additive-base warning card (only filled card)}
  - {id: e4, type: rail,             region: interpretation, prominence: secondary, paint_order: 4, content: evidence-not-sizing interpretation}
  - {id: e5, type: note,             region: note_strip,     prominence: tertiary,  paint_order: 5, content: scope guardrail note}
  - {id: e6, type: chart_annotation, region: chart,          prominence: secondary, paint_order: 6, content: "$0 additive base endpoint label anchored to the waterfall frame"}


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
      chart_text:
        category_axis:
          size: LABEL_9PT
          font: FONT
          color: DK
        value_axis:
          size: LABEL_9PT
          font: FONT
          color: DK
        data_labels:
          size: not shown
          note: show_value_labels=false; carry values in step labels/annotation
    e3:
      text_runs:
      - role: $0 lead
        size: MESSAGE_11PT
        color: WHITE
        font: FONT
        bold: true
      - role: warning body
        size: DENSE_BODY_10PT
        color: WHITE
        font: FONT
    e4:
      text_runs:
      - role: interpretation
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e5:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e6:
      text_runs:
      - role: endpoint label
        size: VALUE_14PT
        color: DK
        font: FONT
        bold: true
  render_notes:
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: waterfall_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      steps:
        - {label: Gross AP top-line, value: 44.709, kind: start}
        - {label: GFE design and weapons, value: -27.273, kind: delta}
        - {label: Already inside BC, value: -16.847, kind: delta}
        - {label: Unitemized overlap, value: -0.589, kind: delta}
        - {label: Additive base, value: 0.000, kind: end}
    params:
      value_axis_format: '"$"0.0"B"'
      show_value_labels: false        # values carried in step labels / annotation to keep the $0 endpoint clean
      cat_header: Step
      title: null                     # house style: external exhibit_title element
    external_title:
      text: P-10 AP and LLTM bridge to additive TAM base, FY2022-FY2027, $B
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "$44.7B gross AP becomes $0 additive TAM under the P-5c BC boundary.", anchor_to: e2}
      - {text: "$0 additive base", anchor_to: e2, annotation_element: e6, at_step: Additive base}   # endpoint emphasis carried as a chart_annotation, not another filled readout

tables: []                # NONE on this slide -> block left explicit; the decision rule is the content, not a ledger

shapes:
  - id: warning_1
    element: e3
    factory: text_box
    fill: BLUE_5              # focal dark card: the one high-emphasis family on this slide
    line_color: BLACK         # focal hero border
    line_width: 19050         # 1.5pt black border on the large focal $0 card
    insets: INSETS_MESSAGE
    text: "$0 additive base. Do not add P-10 AP to P-5c Basic Construction - P-10 is timing and reference evidence unless the model boundary is rebuilt."   # lead "$0 additive base" MESSAGE bold, WHITE text on BLUE_5
    meaning: Large focal $0 warning card leading on the $0-additive-base message; the slide's decision rule made unmissable and the only filled card on the slide.
  - id: interpretation_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "AP and LLTM are useful evidence of supplier-heavy purchasing, but not additive market size in the headline model."   # DENSE_BODY_10PT
    meaning: No-fill interpretation that distinguishes evidence from sizing, so the $0 endpoint does not read as dismissal.
  - id: note_1
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Large does not mean additive. Adding P-10 AP to P-5c Basic Construction would double count unless the whole boundary changes."   # FINEPRINT_8_5PT italic
    meaning: Bottom guardrail restating the slide's decision rule.

commentary:
  visible:
    element: e3
    container: callout         # the focal warning card is the visible commentary
    title:
    bullets:
      - {lead: "Warning:", body: "P-10 AP is timing and reference evidence under this boundary, not additive TAM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This slide resolves a likely challenge right after the
      coefficient evidence (S10): advance procurement (AP) and long-lead-time material
      (LLTM) look supplier-heavy and large, so audiences may try to add them to Basic
      Construction. The answer is deliberately firm. In this model boundary, AP and LLTM
      are evidence and context, not additive headline market size. AP and LLTM are some of
      the most concrete public evidence that the submarine industrial base is
      supplier-heavy: Exhibit P-10 shows real purchasing activity one to four fiscal years
      before construction, and the shipbuilder-procured LLTM stream is directly relevant to
      supplier capacity. But the sizing boundary uses P-5c Basic Construction as the
      denominator, and the supplier-addressable LLTM already sits inside that base.

      THE WATERFALL (workbook AP Bridge section 5, FY2022-FY2027). P-10 gross AP and LLTM
      top-line totals $44.709B in the window (the latest-vintage published P-10 "TOTAL:
      Advance Procurement" line for Virginia LI 2013 plus Columbia LI 1045). The model then
      removes, in order: $27.273B of GFE, design, and weapons outside the boundary (nuclear
      plant LLTM via BPMI, combat-systems electronics, ordnance, missile-compartment LLTM,
      and lead-yard Plans/SIB); $16.847B already inside P-5c Basic Construction
      (shipbuilder-procured LLTM and CFE, EOQ, HM&E, propulsor material); and a $0.589B
      un-itemized overlap. The result is a $0.000B additive AP and LLTM base in the headline
      model - confirmed by the workbook reconciliation checks (bridge nets to base; base = 0).

      WHAT THE $0.589B RESIDUAL ACTUALLY IS. It is NOT a fourth real exclusion category. It
      is the early-Virginia P-10 top-line running slightly over the sum of the named bucket
      detail (the published gross for Virginia FY2022 and FY2023 is ~$2.1B and ~$2.0B against
      named buckets summing to ~$1.73B and ~$1.81B in the rollup). The workbook books that
      gap explicitly as "less un-itemized overlap" so the bridge nets cleanly to zero rather
      than hiding the gap. Treat it as a reconciliation line, not an analytic claim.

      WHY ZERO IS NOT DISMISSAL. AP and LLTM are real supplier-heavy purchasing signals. The
      shipbuilder-procured LLTM bucket alone runs ~$2.0B to $2.5B per year combined across
      both classes at the FY2025-FY2027 rate and is growing (from ~$0.7B to $0.9B in
      FY2021-FY2022), tracking HII guidance of +30% YoY outsourcing hours. The zero additive
      base is an anti-double-counting decision: the headline denominator already uses P-5c
      Basic Construction, and the addressable LLTM is inside it, so wiring P-10 AP as a
      separate stream would double-count the BC TAM. There is a reference (non-applied)
      AP/LLTM POP coefficient of ~48.5%; it is shown elsewhere but never applied because the
      base is $0.

      WHY THE BOUNDARY MATTERS (preview of A3 detail). AP can only become additive if the
      whole model boundary is rebuilt around a different denominator (for example, a gated-POP
      AP/LLTM corpus of ~$18.8B for the 48.5% reference coefficient). That is a different lens,
      not the headline P-5c model, and it also reconciles to a $0 additive contribution under
      the chosen boundary. The appendix A3 (ap_and_lltm_detail) carries the per-bucket P-10
      grids and the full crosswalk; the main slide should give the arithmetic and the warning,
      not every P-10 bucket.

      MAIN AUDIENCE GUARDRAIL. Be firm: audiences often want to add every supplier-looking
      line. The correct answer is that AP and LLTM are evidence and context, not an additive
      headline base. Keep the final $0 bar visually obvious - it is the slide's point - and
      keep detail in the appendix.

      DENSITY GUIDANCE. Default is waterfall + focal warning card + interpretation note +
      bottom guardrail. To densify, add step values as chart labels (gross, the three
      decrements, $0), or expand the interpretation rail to a second line distinguishing
      evidence from sizing. Never let the $0 endpoint read as "AP does not matter."
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4, e5]}
      dense:  {add_bullets: 3, safe_containers: [warning_card, interpretation, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Gross AP:"
        body: "P-10 gross AP and LLTM totals ~$44.7B FY2022-FY2027 (latest-vintage published top-line, Virginia plus Columbia)."
        evidence: AP Bridge section 5; SCN P-10
        safe_container: chart
        density_trigger: Add as the start label if the waterfall has label room.
      - priority: 2
        lead: "GFE exclusion:"
        body: "$27.3B is removed for GFE, design, and weapons outside the boundary (BPMI nuclear, electronics, ordnance, missile compartment, lead-yard Plans)."
        evidence: AP Bridge section 4; wiki 05 (long-lead and advance procurement)
        safe_container: chart
        density_trigger: Add to the first decrement label if the waterfall is label-light.
      - priority: 3
        lead: "Already in BC:"
        body: "$16.8B is not additive because shipbuilder-procured LLTM, EOQ, HM&E, and propulsor material already sit inside P-5c Basic Construction."
        evidence: AP Bridge section 4
        safe_container: chart
        density_trigger: Add when the double-count risk is the central question.
      - priority: 4
        lead: "Residual is a tie-out:"
        body: "$0.6B is the early-Virginia P-10 top-line over named bucket detail, booked as un-itemized overlap, not a real fourth exclusion."
        evidence: AP Bridge section 5 (un-itemized overlap line)
        safe_container: note_strip
        density_trigger: Add only in appendix-style density or if a reviewer asks about the residual.
      - priority: 5
        lead: "Zero additive:"
        body: "The headline AP and LLTM additive base is $0, not because suppliers are absent but because the boundary prevents double counting."
        evidence: QA Reconciliation; AP Bridge section 5
        safe_container: note_strip
        density_trigger: Always safe in a dense variant.
      - priority: 6
        lead: "Supplier evidence:"
        body: "Shipbuilder-procured LLTM runs ~$2.0B to $2.5B per year combined and is growing, strong evidence of supplier-heavy purchasing years before construction."
        evidence: SCN P-10; wiki 05; wiki 07 (DoD contract announcements)
        safe_container: interpretation
        density_trigger: Add if the zero endpoint feels too dismissive.
      - priority: 7
        lead: "Boundary condition:"
        body: "AP can only become additive if the whole model boundary is rebuilt around a different denominator; the chosen P-5c model holds it at $0."
        evidence: AP Bridge docstring; TAM Build AP and LLTM stream base
        safe_container: warning_card
        density_trigger: Add for diligence or methodology reviews.
      - priority: 8
        lead: "Reference coefficient:"
        body: "A reference AP/LLTM POP coefficient of ~48.5% exists but is never applied, because the additive base is $0."
        evidence: TAM Build section 3a (AP/LLTM coefficient, reference)
        safe_container: interpretation
        density_trigger: Add for an audience that has seen the coefficient ladder (S10).
      - priority: 9
        lead: "Outsourcing trajectory:"
        body: "A Va Block VI LLTM action placed 98% of value at outside-yard suppliers in May 2026 versus 0% on a Dec 2022 Columbia LLTM action - directional, not a sizing input."
        evidence: wiki 07 (DoD daily Contracts, FY2022 vs FY2026 anchors)
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on supplier-base expansion.
      - priority: 10
        lead: "Not a capture model:"
        body: "This bridge is a sizing boundary, not a view of supplier capture, award timing, or revenue realization."
        evidence: Deck guardrails
        safe_container: note_strip
        density_trigger: Use when the slide is excerpted out of sequence.
      - priority: 11
        lead: "Appendix backup:"
        body: "The per-bucket P-10 grids for both classes and the full TAM-treatment crosswalk live in the AP and LLTM detail appendix (A3)."
        evidence: appendix_ap_and_lltm_detail (A3)
        safe_container: note_strip
        density_trigger: Add when the audience wants the bucket-level detail.
    do_not_add:
      - P-10 AP added to P-5c Basic Construction
      - language saying AP and LLTM do not matter
      - long P-10 line-item detail on the main slide (it belongs in A3)
      - SOM, capture, or win-probability language

data_and_calculations:
  data_inputs:
    - {input: Gross AP top-line FY22-27, value: 44.709, unit: $B, tie_out: AP Bridge section 5 (CD_11_APBridge), used_in: chart_1}
    - {input: Less GFE design and weapons, value: -27.273, unit: $B, tie_out: AP Bridge section 5, used_in: chart_1}
    - {input: Less already inside Basic Construction, value: -16.847, unit: $B, tie_out: AP Bridge section 5, used_in: chart_1}
    - {input: Less un-itemized overlap, value: -0.589, unit: $B, tie_out: AP Bridge section 5 (early-Va top-line over named detail), used_in: chart_1}
    - {input: AP and LLTM additive base, value: 0.000, unit: $B, tie_out: QA Reconciliation, used_in: chart_1}
  calculations:
    - {name: Additive AP and LLTM base, formula: "44.709 - 27.273 - 16.847 - 0.589", output: "0.000", used_in: chart_1}
  rounding_rules: Show $B to one decimal on chart labels; keep exact $M values in the embedded chart data.
  reconciliation: Waterfall starts at $44.709B gross AP and ends at $0.000B additive base; workbook checks confirm the bridge nets to the base and the base equals 0.

qa:
  guardrails:
    - Waterfall starts at $44.709B and ends at $0.000B additive base.
    - The three decreases are $27.273B (GFE/design/weapons), $16.847B (already in BC), and $0.589B (un-itemized overlap).
    - The $0.589B residual is a reconciliation tie-out (early-Virginia top-line over named detail), not a real fourth exclusion.
    - Slide says AP and LLTM are reference and timing evidence, not additive TAM; the $0 endpoint is anti-double-counting, not dismissal.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN P-10, DoD daily Contracts, CRS RL32418/R41129); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit / column-width checks do not apply
