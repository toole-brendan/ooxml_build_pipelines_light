# SlideSpec - submarines `executive_summary` (deck slide 4)
# KPI-card answer slide: one no-fill qualifier note, two BLACK-bordered hero
# answer cards (average annual TAM in BLUE_5, average annual broad SAM in BLUE_4
# - the ONLY dark/focal family), four smaller light supporting cards (cumulative
# TAM, cumulative broad SAM, applied BC supplier coefficient, AP and LLTM additive
# base), and a no-fill findings rail carrying the interpretation rules. NO chart,
# funnel, or Venn: this is the clean answer slide, not the trend proof. Both
# charts: [] and tables: [] are explicit design statements.

meta:
  slide_id: subs-s4
  slide_order: 4
  module_name: executive_summary.py
  slide_type: body
  section: Market and Scope
  archetype: kpi_cards_with_findings_rail
  story_role: Lead with the quantitative answer and the interpretation rules before the deck starts defending individual inputs, so the rest of the body reads as support for a number the audience already has.
  inputs:
    - Executive Summary headline KPIs
    - TAM Build (applied BC supplier coefficient, cumulative and average annual TAM)
    - SAM Build (broad component-manufacturing scenario)
    - AP Bridge (AP and LLTM additive base, confirmed 0)
    - Wiki 04 Basic Construction
    - Wiki 06 Outsourced layer within Basic Construction
    - Wiki 07 DoD contract announcement data
    - Wiki 08 FFATA-visible first-tier subawards
    - Wiki 09 Vendors and concentration
  related_appendix: []

chrome:
  section: Market and Scope
  breadcrumb_topic: Executive summary
  title_topic: Executive Summary
  title_finding: Average annual opportunity is about $3.3B TAM and $2.8B broad SAM
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10
    - U.S. DoD daily Contracts announcements
    - SAM.gov FFATA/FSRS records and Entity Management API
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA/FSRS records and Entity Management API"

story:
  objective: Give executives the headline TAM and broad SAM, the cumulative context, the applied supplier coefficient, the AP and LLTM additive base, and the most important interpretation rules in one view.
  do_not_say:
    - Do not call the average annual figures a smooth run-rate; they are lumpy FY2022-FY2027 model-period averages.
    - Do not show TAM, SAM, SOM circles or a funnel diagram.
    - Do not use SOM, capture share, win probability, price realization, or company-specific revenue-forecast language.
    - Do not add AP and LLTM gross to the headline base; the additive base is $0 (no double count).
  known_caveats:
    - Values are lumpy FY2022-FY2027 model-period averages, not a steady commercial run-rate; annual flow peaks later in the deck.
    - Broad SAM is a scenario cut of the work-type buckets (all seven, residual excluded), not a capture forecast.
    - The headline coefficient is the strict, non-nuclear, yard-excluded Basic Construction supplier share; observed POP evidence can support larger views.

regions:
  coord_basis: BODY
  layout_pattern: kpi_cards_with_findings_rail
  # Top: a one-line average-annual qualifier note. Then two hero answer cards.
  # Then a row of four supporting cards. Then a bottom findings rail.
  subtitle_note:       {x: 0%, y: 0%,  w: 100%, h: NOTE_H}
  tam_card:            {x: 0%, y: 13%, w: 48%,  h: 28%}
  broad_sam_card:      {x: right_of(tam_card) + GAP, y: align_top(tam_card), w: remaining, h: 28%}
  cumulative_tam_card: {x: 0%, y: 48%, w: 23%,  h: 17%}
  cumulative_sam_card: {x: right_of(cumulative_tam_card) + GAP, y: align_top(cumulative_tam_card), w: 23%, h: 17%}
  coeff_card:          {x: right_of(cumulative_sam_card) + GAP, y: align_top(cumulative_tam_card), w: 23%, h: 17%}
  ap_card:             {x: right_of(coeff_card) + GAP, y: align_top(cumulative_tam_card), w: remaining, h: 17%}
  findings_rail:       {x: 0%, y: 72%, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: note,    region: subtitle_note,       prominence: tertiary,  paint_order: 1, content: model-period average qualifier}
  - {id: e2, type: callout, region: tam_card,            prominence: primary,   paint_order: 2, content: average annual TAM hero KPI}
  - {id: e3, type: callout, region: broad_sam_card,      prominence: primary,   paint_order: 3, content: average annual broad SAM hero KPI}
  - {id: e4, type: callout, region: cumulative_tam_card, prominence: secondary, paint_order: 4, content: cumulative TAM supporting KPI}
  - {id: e5, type: callout, region: cumulative_sam_card, prominence: secondary, paint_order: 5, content: cumulative broad SAM supporting KPI}
  - {id: e6, type: callout, region: coeff_card,          prominence: secondary, paint_order: 6, content: applied Basic Construction supplier coefficient}
  - {id: e7, type: callout, region: ap_card,             prominence: secondary, paint_order: 7, content: AP and LLTM additive base}
  - {id: e8, type: rail,    region: findings_rail,       prominence: secondary, paint_order: 8, content: four interpretation findings}


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
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e2:
      text_runs:
      - role: kpi cap
        size: CAP_12PT
        color: WHITE
        font: FONT
        bold: true
      - role: hero value
        size: HERO_32PT
        color: WHITE
        font: FONT
        bold: true
      - role: qualifier
        size: LABEL_9PT
        color: WHITE
        font: FONT
        italic: true
    e3:
      text_runs:
      - role: kpi cap
        size: CAP_12PT
        color: WHITE
        font: FONT
        bold: true
      - role: hero value
        size: HERO_32PT
        color: WHITE
        font: FONT
        bold: true
      - role: qualifier
        size: LABEL_9PT
        color: WHITE
        font: FONT
        italic: true
    e4:
      text_runs:
      - role: support label
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: support value
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
      - role: support qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e5:
      text_runs:
      - role: support label
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: support value
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
      - role: support qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e6:
      text_runs:
      - role: support label
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: support value
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
      - role: support qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e7:
      text_runs:
      - role: support label
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: support value
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
      - role: support qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e8:
      text_runs:
      - role: rail cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: finding line
        size: LABEL_9PT
        color: DK
        font: FONT
  render_notes: []

charts: []
tables: []
images: []

shapes:
  - id: subtitle_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "FY2022-FY2027 model-period averages; not a commercial-style steady run-rate."   # FINEPRINT_8_5PT italic
    meaning: Prevents the headline values from being read as a smooth annual run-rate.
  - id: kpi_tam
    element: e2
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    paragraphs:
      - runs:
          - {text: "AVERAGE ANNUAL TAM", size: CAP_12PT, bold: true, color: WHITE, font: FONT}
      - runs:
          - {text: "~$3.3B", size: HERO_32PT, bold: true, color: WHITE, font: FONT}
      - runs:
          - {text: "FY2022-FY2027 model-period average", size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
    text: "AVERAGE ANNUAL TAM\n~$3.3B\nFY2022-FY2027 model-period average"
    meaning: Primary answer card for portfolio TAM.
  - id: kpi_broad_sam
    element: e3
    factory: text_box
    fill: BLUE_4
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    paragraphs:
      - runs:
          - {text: "AVERAGE ANNUAL BROAD SAM", size: CAP_12PT, bold: true, color: WHITE, font: FONT}
      - runs:
          - {text: "~$2.8B", size: HERO_32PT, bold: true, color: WHITE, font: FONT}
      - runs:
          - {text: "Broad component-manufacturing scenario", size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
    text: "AVERAGE ANNUAL BROAD SAM\n~$2.8B\nBroad component-manufacturing scenario"
    meaning: Primary answer card for the broad component-manufacturing scenario SAM.
  - id: supporting_cumulative_tam
    element: e4
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Cumulative TAM\n~$19.8B\nFY2022-FY2027"   # LABEL_9PT
    meaning: Anchors average annual TAM to the cumulative numerator.
  - id: supporting_cumulative_sam
    element: e5
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Cumulative broad SAM\n~$16.8B\nFY2022-FY2027"   # LABEL_9PT
    meaning: Anchors average annual broad SAM to its cumulative scenario value.
  - id: supporting_coefficient
    element: e6
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Applied BC supplier coefficient\n35.0%\nstrict, non-nuclear, yard-excluded"   # LABEL_9PT
    meaning: Shows the conservative coefficient that feeds the headline model.
  - id: supporting_ap_lltm
    element: e7
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "AP and LLTM additive base\n$0\nno double count"   # LABEL_9PT
    meaning: Disarms the AP and LLTM double-counting issue; supplier LLTM already sits inside Basic Construction.
  - id: findings_rail_1
    element: e8
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    paragraphs:
      - runs:
          - {text: "KEY FINDINGS", size: CAP_12PT, bold: true, color: DK, font: FONT}
      - runs:
          - {text: "1. Basic Construction is the denominator; GFE and SIB capacity grants are excluded.", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "2. The supplier coefficient is deliberately strict: non-nuclear, BPMI-excluded, yard-excluded.", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "3. Broad SAM is a scenario menu; no SOM, capture share, or win probability is modeled.", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "4. Annual flow is lumpy, with FY2024 and FY2027 peaks shown later in the deck.", size: LABEL_9PT, color: DK, font: FONT}
    text: "KEY FINDINGS\n1. Basic Construction is the denominator; GFE and SIB capacity grants are excluded.\n2. The supplier coefficient is deliberately strict: non-nuclear, BPMI-excluded, yard-excluded.\n3. Broad SAM is a scenario menu; no SOM, capture share, or win probability is modeled.\n4. Annual flow is lumpy, with FY2024 and FY2027 peaks shown later in the deck."
    meaning: Bottom interpretation rail summarizing what makes the sizing conservative.

commentary:
  visible:
    element: e8
    container: right_rail
    title: Key findings
    bullets:
      - {lead: "Denominator:", body: "FY2022-FY2027 P-5c Basic Construction for Virginia and Columbia."}
      - {lead: "Coefficient:", body: "strict, non-nuclear, BPMI-excluded, and yard-excluded."}
      - {lead: "Scenario:", body: "broad SAM is not SOM and applies no capture probability."}
      - {lead: "Cadence:", body: "period average; annual opportunity is lumpy."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the first quantitative slide in the deck, opening
      the Market and Scope section, so it should be answer-first and direct. Across the
      FY2022-FY2027 model period the model produces about $3.3B average annual TAM and
      about $2.8B average annual broad component-manufacturing SAM. These are lumpy-
      period averages, not a stable annual run-rate; later slides (annual cadence) show
      why the annual flow spikes in FY2024 and FY2027.

      THE ARITHMETIC ANCHOR. The cumulative values anchor the headline: about $19.8B
      cumulative TAM and about $16.8B cumulative broad SAM over the six-year window. The
      bridge is the roughly $56.6B FY2022-FY2027 Basic Construction base multiplied by
      the strict supplier coefficient, with no AP and LLTM double count: $56.6B x 35.0%
      = about $19.8B cumulative TAM, /6 years = about $3.3B average annual. The exact
      workbook figures are 3306.6155 $M average annual TAM, 19839.6931 $M cumulative
      TAM, 2805.4816 $M average annual broad SAM, and 16832.8893 $M cumulative broad
      SAM; the slide displays them rounded with a leading tilde.

      THE COEFFICIENT. The applied BC supplier coefficient (0.35023547, displayed 35.0%)
      should be described as strict, not aggressive. It is the non-nuclear, BPMI-
      excluded, yard-excluded period-of-performance share. The observed DoD daily-
      Contracts POP evidence can support larger distributed-production views (the wiki
      documents a 50-to-65 percent outsourced band for complex shipbuilding), but the
      headline coefficient used here is the conservative cut, which is part of why the
      sizing is defensible.

      AP AND LLTM. Gross P-10 Advance Procurement is extracted and shown as a reference
      stream, but its additive base to the headline is $0: supplier long-lead-time
      material is already inside the P-5c Basic Construction base, so adding the P-10
      gross (on the order of $10-20B over the window) would double-count. The AP and
      LLTM additive base is confirmed zero unless the reconciliation changes; the gross
      remains evidence for supplier purchasing cadence, not additive TAM.

      WHAT BROAD SAM IS AND IS NOT. Broad SAM is the all-seven-buckets scenario from the
      SAM menu, with the unbucketed/ambiguous residual excluded. It is a subset of TAM
      with no capture haircut. This model does not include SOM, capture probability,
      company-specific win rate, price realization, or revenue forecast. Do not show
      TAM, SAM, SOM circles. The interpretation caveats in the workbook are explicit:
      SAM is not SOM; no win probability is modeled; no capability-fit haircut is
      modeled; no capacity-constrained revenue ramp is modeled.

      THE EXCLUSION BASIS. The denominator is FY2022-FY2027 P-5c Basic Construction for
      Virginia and Columbia. GFE (propulsion, electronics, ordnance), SIB capacity
      grants, and prime-yard labor are outside the denominator; the model sizes non-
      nuclear supplier components. The visible evidence that supports the coefficient
      and the work-type allocation is FFATA/FSRS subaward data, SAM.gov entity data, and
      DoD daily Contracts announcements, not a company-specific forecast.

      DENSITY GUIDANCE. Default is two hero cards, four supporting cards, and the four-
      line findings rail. To densify, expand the subtitle note, add a fifth finding to
      the rail, or add a second line inside the coefficient or AP card. Keep the two
      hero cards dominant at any density and never let a supporting card out-weigh them.
    density_modes:
      normal: {visible_bullets: 4, keep: [e1, e2, e3, e4, e5, e6, e7, e8]}
      dense: {add_bullets: 3, safe_containers: [findings_rail, subtitle_note, coeff_card, ap_card], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Arithmetic anchor:"
        body: "About $56.6B Basic Construction base times the strict 35.0% supplier coefficient is about $19.8B cumulative TAM, or about $3.3B average annual."
        evidence: TAM Build; Executive Summary headline KPIs
        safe_container: findings_rail
        density_trigger: Add if the slide needs a formula cue without becoming a bridge slide.
      - priority: 2
        lead: "Broad SAM anchor:"
        body: "Broad component-manufacturing SAM is about $16.8B cumulative, or about $2.8B average annual across FY2022-FY2027."
        evidence: SAM Build; Executive Summary headline KPIs
        safe_container: findings_rail
        density_trigger: Add if cumulative SAM needs to be explained in prose.
      - priority: 3
        lead: "Strict coefficient:"
        body: "The headline coefficient excludes nuclear BPMI, prime-yard, and co-prime-yard activity, so 35.0% is the conservative, not the aggressive, cut."
        evidence: DoD daily Contracts POP evidence; TAM Build (wiki 06, wiki 07)
        safe_container: coeff_card
        density_trigger: Add if reviewers ask whether 35.0% is aggressive.
      - priority: 4
        lead: "AP and LLTM:"
        body: "Gross AP and LLTM stay as evidence for supplier purchasing cadence; the additive headline base remains $0 because supplier LLTM is already inside Basic Construction."
        evidence: AP Bridge; U.S. Navy SCN Justification Books, Exhibit P-10
        safe_container: ap_card
        density_trigger: Add if AP and LLTM are discussed in the same meeting.
      - priority: 5
        lead: "Period average:"
        body: "The average annual number smooths a lumpy FY2022-FY2027 period; it should not be sold as a steady run-rate, and the annual flow peaks in FY2024 and FY2027."
        evidence: Executive Summary tab; annual cadence slide
        safe_container: subtitle_note
        density_trigger: Add if the subtitle note is expanded.
      - priority: 6
        lead: "No SOM:"
        body: "Broad SAM is not a capture forecast and applies no share, probability, win-rate, or revenue haircut."
        evidence: Assumptions and methodology caveats
        safe_container: findings_rail
        density_trigger: Add if the warning needs to be stronger.
      - priority: 7
        lead: "Exclusion basis:"
        body: "GFE, SIB capacity grants, and yard labor are outside the denominator; the model sizes non-nuclear supplier components on the P-5c Basic Construction base."
        evidence: Sizing Boundary slide; SCN source family; GAO-25-106286
        safe_container: findings_rail
        density_trigger: Add if this slide is presented without the boundary slide.
      - priority: 8
        lead: "Visible evidence:"
        body: "FFATA/FSRS records, SAM.gov entity data, and DoD daily Contracts support the coefficient and work-type allocation, not a company-specific forecast."
        evidence: SAM.gov FFATA/FSRS and Entity Management records; DoD daily Contracts (wiki 08, wiki 09)
        safe_container: findings_rail
        density_trigger: Add in a more evidence-heavy version.
      - priority: 9
        lead: "Demand backdrop tie-in:"
        body: "Oversight, Navy policy, and prime behavior all point toward broader distributed supplier capacity, which is why the supplier opportunity is expanding; it is directional, not a sizing input."
        evidence: demand_backdrop (S05); GAO-26-109068; CRS RL32418
        safe_container: findings_rail
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 10
        lead: "Audit status:"
        body: "Headline values pass the workbook checks: broad SAM is at or below TAM, bucketed TAM reconciles to portfolio TAM, and the AP and LLTM additive base is confirmed zero."
        evidence: QA Reconciliation; Number Audit
        safe_container: findings_rail
        density_trigger: Add if a reviewer asks whether the numbers tie out internally.
    do_not_add:
      - SOM, capture, win probability, or revenue-forecast language
      - a full TAM, SAM, SOM funnel diagram or three nested circles
      - any statement that the average annual values are smooth run-rate guidance
      - the gross AP and LLTM figure added into the headline base

data_and_calculations:
  data_inputs:
    - {input: Average annual TAM, value: 3306.6155, unit: $M per year, display: "~$3.3B", tie_out: Executive Summary headline KPIs, used_in: kpi_tam}
    - {input: Average annual broad SAM, value: 2805.4816, unit: $M per year, display: "~$2.8B", tie_out: Executive Summary headline KPIs, used_in: kpi_broad_sam}
    - {input: FY2022-FY2027 cumulative TAM, value: 19839.6931, unit: $M, display: "~$19.8B", tie_out: Executive Summary headline KPIs, used_in: supporting_cumulative_tam}
    - {input: FY2022-FY2027 cumulative broad SAM, value: 16832.8893, unit: $M, display: "~$16.8B", tie_out: Executive Summary headline KPIs, used_in: supporting_cumulative_sam}
    - {input: Applied Basic Construction supplier coefficient, value: 0.35023547, unit: share, display: "35.0%", tie_out: TAM Build, used_in: supporting_coefficient}
    - {input: AP and LLTM additive base, value: 0, unit: dollars, display: "$0", tie_out: AP Bridge, used_in: supporting_ap_lltm}
    - {input: FY2022-FY2027 cumulative Basic Construction base, value: 56600, unit: $M, display: "~$56.6B", tie_out: SCN Budget portfolio rollup, used_in: reserve}
  calculations:
    - {name: Average annual TAM, formula: "FY2022-FY2027 cumulative TAM / 6 fiscal years", output: "~$3.3B", used_in: kpi_tam}
    - {name: Average annual broad SAM, formula: "FY2022-FY2027 cumulative broad SAM / 6 fiscal years", output: "~$2.8B", used_in: kpi_broad_sam}
    - {name: Cumulative TAM, formula: "~$56.6B Basic Construction base x 35.0% supplier coefficient", output: "~$19.8B", used_in: supporting_cumulative_tam}
  rounding_rules: Headline values displayed as one-decimal billions with a leading tilde; coefficient displayed as 35.0%; AP and LLTM additive base displayed as $0.
  reconciliation: Average annual values are model-period averages across six fiscal years and reconcile to cumulative value divided by six; broad SAM is at or below TAM; bucketed TAM reconciles to portfolio TAM.

qa:
  guardrails:
    - The two headline figures round to about $3.3B and about $2.8B.
    - Cumulative values are shown as context, not as the main story.
    - The slide says average annual and FY2022-FY2027.
    - The AP and LLTM additive base is displayed as $0.
    - No SOM, capture, or win-probability language appears.
    - No "+" or "/" in visible copy except canonical labels; SIB not MIB.
  source_checks:
    - Sources are external families only: Navy SCN Justification Books, DoD daily Contracts, and SAM.gov FFATA/FSRS and Entity Management records.
    - No workbook tabs, slide-data IDs, wiki chapters, or chart IDs are rendered in chrome.sources.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - no chart rIds because charts is empty
    - no table-fit check because tables is empty
