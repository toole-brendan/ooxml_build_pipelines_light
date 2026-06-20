# SlideSpec - submarines `sizing_boundary` (deck slide 03)
# Shape-built three-column boundary board (INCLUDED / EXCLUDED / CONTEXT ONLY):
# one no-fill header note, three filled boundary cards, and one high-emphasis
# bottom warning rail ("No SOM is modeled", the BLACK-bordered focal object).
# Cards, not a native table; NO arrows and NO ecosystem map (deliberately
# distinct from the S2 system map) so it reads like a consulting boundary slide.
# This is the contract with the audience about what the model sizes.

meta:
  slide_id: subs-s3
  slide_order: 3
  module_name: sizing_boundary.py
  slide_type: body
  section: Market and Scope
  archetype: three_column_boundary_cards_with_warning_rail
  story_role: "Set the contract with the audience: what is included, excluded, and context-only before the deck defends inputs."
  inputs:
    - guide_methodology.py (Methodology tab) section 4 scope boundary and section 5 exclusion rules
    - inputs_assumptions.py (Assumptions tab) section 3, AP/LLTM additive base confirmed at $0
    - model_tam_build.py (TAM Build tab), BC stream and AP/LLTM reference stream
    - wiki 01 Scope and the funnel framework (in / out of the outsourced definition)
    - wiki 03 Plans, GFE, and other layers (the four GFE categories, BPMI)
    - wiki 12 Unseen layer (FFATA visible floor vs unseen, HII share)
    - wiki 16 Data sources, pipeline, and limitations (FFATA lag, POP evidence)
  related_appendix:
    - subs-a1   # appendix_definitions_and_scope

chrome:
  section: Market and Scope
  breadcrumb_topic: Boundary
  title_topic: Sizing Boundary
  title_finding: The model sizes non-nuclear supplier opportunity, excluding GFE, SIB, yards, and SOM
  layout: slideLayout4
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10
    - FAR 52.204-10 and FAR Part 45
    - GAO-25-106286
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibits P-5c and P-10; (2) FAR 52.204-10 and FAR Part 45; (3) GAO-25-106286"

story:
  objective: Draw the sizing boundary explicitly so later objections about P-10 AP double-counting, GFE inclusion, SIB funding, yards, or SOM are defused upfront.
  do_not_say:
    - Do not add AP and LLTM to P-5c Basic Construction in the headline model.
    - Do not imply GFE, SIB grants, or yard work are potential upside inside the modeled TAM.
    - Do not use SOM, capture share, win probability, or revenue forecast language.
    - Avoid Venn diagrams and TAM, SAM, SOM circles.
  known_caveats:
    - AP and LLTM are timing and reference evidence; the additive base equals $0 under the current boundary because supplier LLTM is already inside Basic Construction.
    - FFATA visible vendor flow is a floor, not the full supplier layer.
    - Context-only items can be used as evidence, but not as add-ons to the numerator.

regions:
  coord_basis: BODY
  layout_pattern: three_column_boundary_cards_with_warning_rail
  header_note: {x: 0%, y: 0%, w: 100%, h: NOTE_H}
  included_card: {x: 0%, y: 13%, w: 31%, h: 60%}
  excluded_card: {x: right_of(included_card) + GAP, y: align_top(included_card), w: 31%, h: 60%}
  context_card: {x: right_of(excluded_card) + GAP, y: align_top(included_card), w: remaining, h: 60%}
  warning_rail: {x: 0%, y: 80%, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: note, region: header_note, prominence: tertiary, paint_order: 1, content: boundary philosophy sentence}
  - {id: e2, type: diagram, region: included_card, prominence: primary, paint_order: 2, content: included in TAM boundary card}
  - {id: e3, type: diagram, region: excluded_card, prominence: secondary, paint_order: 3, content: excluded from TAM boundary card}
  - {id: e4, type: diagram, region: context_card, prominence: secondary, paint_order: 4, content: context-only evidence card}
  - {id: e5, type: callout, region: warning_rail, prominence: primary, paint_order: 5, content: no SOM warning rail}


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
      - role: card cap/header
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
        note: Use ALL CAPS only where the visible text already uses it.
      - role: card body/bullets
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: card cap/header
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
        note: Use ALL CAPS only where the visible text already uses it.
      - role: card body/bullets
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: card cap/header
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
        note: Use ALL CAPS only where the visible text already uses it.
      - role: card body/bullets
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e5:
      text_runs:
      - role: Boundary warning lead
        size: MESSAGE_11PT
        color: WHITE
        font: FONT
        bold: true
      - role: warning body
        size: DENSE_BODY_10PT
        color: WHITE
        font: FONT
  render_notes: []

charts: []
tables: []
images: []

shapes:
  - id: boundary_header_note
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "A narrower answer is more defensible than a larger, double-counted market."   # FINEPRINT_8_5PT italic
    meaning: Quiet interpretive line that frames the matrix without becoming another card.
  - id: included_card_1
    element: e2
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    paragraphs:
      - runs:
          - {text: "INCLUDED IN TAM", size: CAP_12PT, bold: true, color: DK, font: FONT}
      - runs:
          - {text: "- P-5c Basic Construction base for Virginia and Columbia new construction\n- Non-nuclear supplier component manufacturing inside that base\n- Purchased material, subcontracts, and lower-tier supplier flow where supported\n- Work-type buckets used for scenario SAM: structural, machining, castings and forgings, piping, valves, pumps, electrical and power, HVAC, coatings and insulation", size: DENSE_BODY_10PT, color: DK, font: FONT}
    text: "INCLUDED IN TAM\n- P-5c Basic Construction base for Virginia and Columbia new construction\n- Non-nuclear supplier component manufacturing inside that base\n- Purchased material, subcontracts, and lower-tier supplier flow where supported\n- Work-type buckets used for scenario SAM"
    meaning: Defines the counted numerator.
  - id: excluded_card_1
    element: e3
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "EXCLUDED FROM TAM\n- GFE and GFP: reactor plant, combat systems, sonar, weapons, ordnance\n- BPMI nuclear reactor work\n- SIB capacity-development grants and pass-throughs\n- Prime and co-prime yard work at GDEB and HII\n- Depot, sustainment, overhauls, design-only, classified payloads\n- AP and LLTM already inside Basic Construction; additive base is $0"
    meaning: Keeps excluded dollars from being mistaken as upside.
  - id: context_card_1
    element: e4
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "CONTEXT ONLY\n- Total Ship Estimate and TOA as top-of-funnel context\n- Gross AP and LLTM reference stream; additive base is $0\n- FFATA and FSRS visible first-tier vendor floor\n- DoD place-of-performance evidence behind the supplier coefficient\n- HII Newport News visibility gap and unseen-layer limitations"
    meaning: Separates evidence and timing streams from addressable TAM.
  - id: warning_rail_1
    element: e5
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_MESSAGE
    text: "Boundary warning: No SOM is modeled. SAM is a scenario menu, not market share, capture, win probability, or revenue forecast."
    meaning: High-emphasis bottom rail; focal object, BLACK-bordered to prevent TAM and SAM from being read as a capture forecast.

commentary:
  visible:
    element: e5
    container: callout
    title:
    bullets:
      - {lead: "No SOM:", body: "scenario SAM defines inclusion cuts; it does not model share, win rate, or revenue."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      THE BOUNDARY CONTRACT. This slide is the deck's contract with the audience:
      what is included, what is excluded, and what is used only as context or
      evidence. The model deliberately does not size every dollar that leaves the
      Navy. The job here is to disarm, up front, the four objections that
      otherwise recur: that total ship cost is the market, that GFE is upside,
      that SIB funding is supplier revenue, and that AP and LLTM should be added
      to Basic Construction.

      THE INCLUDED NUMERATOR. TAM is the non-GFE, non-SIB new-construction
      supplier opportunity: the P-5c Basic Construction base for Virginia SSN-774
      and Columbia SSBN-826, times the applied supplier coefficient, restricted to
      non-nuclear supplier component manufacturing, purchased material, and
      first- and lower-tier subcontract flow where the evidence supports it. That
      counted layer is then allocated into seven work-type buckets used for
      scenario SAM.

      WHY GFE AND NUCLEAR ARE OUT. GFE and nuclear reactor work are real dollars,
      but they are not part of the non-nuclear supplier TAM. The four P-5c GFE
      categories (Propulsion Equipment, Electronics, Hull-Mechanical-Electrical,
      Ordnance) are Navy-direct procurements: Bechtel Plant Machinery, Inc.
      supplies the reactor plant under Naval Reactors direction; Lockheed Martin
      and Northrop Grumman supply combat systems and sonar; the Trident strategic
      weapon system is funded outside SCN entirely. None of these flow through the
      GDEB prime, so none are in the supplier-addressable layer.

      THE AP AND LLTM DOUBLE-COUNTING TRAP. This is the main trap the slide must
      defuse. P-10 Advance Procurement is valuable because it shows what long-lead
      material is bought and when, but the additive AP and LLTM base is confirmed
      at $0 in the headline model: supplier LLTM is already inside the Basic
      Construction base, so adding the P-10 gross (roughly $10-20B across the
      window) would double-count. The gross can appear in appendix or context
      views as a reference stream, but it never inflates headline TAM. The
      workbook even runs an AP/LLTM reference coefficient (~48.5%) that is computed
      but deliberately not applied, precisely because the base is $0.

      WHY SIB IS OUT. SIB spending is strategically important, but it is
      capacity-development funding and pass-through support (for example BlueForge
      Alliance, ~$4.17B cumulative FY2016-FY2025) rather than direct component
      delivery into a hull. The Maritime Industrial Base Program Office was stood
      up by Navy memorandum in June 2024; the dollars fund shipyard capacity and
      workforce, not construction outsourcing, so they are excluded from SAM.

      WHY THE YARDS ARE OUT. Prime and co-prime yard work at GDEB (Groton and
      Quonset Point) and HII Newport News stays outside the open supplier SAM
      unless the boundary is explicitly changed. HII's team-build workshare flows
      through the GDEB prime; it is context and a visibility limitation, not an
      addressable third-party target.

      THE NO-SOM WARNING. TAM and SAM are opportunity ceilings and scenario
      definitions. The model does not include company-specific capture share, win
      probability, price realization, revenue forecast, or probability-weighted
      opportunity. Scenario SAM is a menu of included buckets (broad, electrical,
      metal, modular, HM&E), built by including or excluding work-type buckets,
      not a share forecast. This warning should be the most visually prominent
      element after the three cards.

      VISUAL READ. The matrix should read like three consulting boundary cards,
      not a data grid. The included card is the numerator; the excluded card
      blocks double-counted and non-addressable flows; the context card preserves
      useful evidence without letting it become an add-on.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4, e5]}
      dense: {add_bullets: 3, safe_containers: [included_card, excluded_card, context_card, warning_rail], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT", "LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "AP and LLTM rule:"
        body: "P-10 is reference evidence for timing; the headline additive base stays $0 to avoid double counting Basic Construction."
        evidence: inputs_assumptions.py section 3 additive base 0; SCN Justification Books, Exhibit P-10
        safe_container: context_card
        density_trigger: Add when the audience asks why P-10 is not in the numerator.
      - priority: 2
        lead: "GFE rule:"
        body: "Government-furnished reactor, combat systems, sonar, weapons, and ordnance categories are outside non-nuclear supplier TAM."
        evidence: wiki 03 Plans, GFE, and other layers; FAR Part 45
        safe_container: excluded_card
        density_trigger: Add if the GFE and GFP bullet needs a second line.
      - priority: 3
        lead: "SIB rule:"
        body: "SIB and BlueForge-type flows are industrial-base investment, not direct construction-component delivery."
        evidence: GAO-25-106286; wiki 01 MIB pass-throughs
        safe_container: excluded_card
        density_trigger: Add for policy-oriented audiences.
      - priority: 4
        lead: "FFATA caveat:"
        body: "FFATA and FSRS identify named first-tier flow and help allocate buckets, but they are not the whole layer."
        evidence: wiki 12 unseen layer; SAM.gov FFATA and FSRS records under FAR 52.204-10
        safe_container: context_card
        density_trigger: Add if the next section dives into visibility gaps.
      - priority: 5
        lead: "Yard exclusion:"
        body: "Prime and co-prime yard work at GDEB and HII stays outside the open supplier SAM unless the boundary is explicitly changed."
        evidence: General Dynamics FY2021 Form 10-K; wiki 12 HII share
        safe_container: excluded_card
        density_trigger: Add when HII or GDEB workshare is debated.
      - priority: 6
        lead: "Scenario language:"
        body: "SAM is a bucket-inclusion scenario menu; no capture probability, price realization, win rate, or revenue haircut is modeled."
        evidence: guide_methodology.py section 2b SAM framework
        safe_container: warning_rail
        density_trigger: Add if the bottom rail is expanded to two lines.
      - priority: 7
        lead: "Narrower is more defensible:"
        body: "The deck chooses a smaller, fully-supported supplier numerator over a larger figure that would double-count or include non-addressable flows."
        evidence: guide_methodology.py section 4 scope boundary
        safe_container: header_note
        density_trigger: Add if a reviewer pushes for a bigger headline number.
      - priority: 8
        lead: "Two classes in scope:"
        body: "The boundary applies to Virginia SSN-774 (Line Item 2013) and Columbia SSBN-826 (Line Item 1045) new construction over FY2022-FY2027."
        evidence: wiki 01 scope window; wiki 02 total ship cost
        safe_container: included_card
        density_trigger: Add if program scope needs to be explicit.
      - priority: 9
        lead: "Context can support, not add:"
        body: "Total Ship Estimate, gross AP, FFATA flow, and POP evidence inform assumptions; none are summed into the TAM numerator."
        evidence: guide_methodology.py definitions; wiki 16 data sources
        safe_container: context_card
        density_trigger: Add if context items are mistaken for upside.
      - priority: 10
        lead: "Depot stays out:"
        body: "Depot maintenance and engineered overhauls run through federal naval shipyards as government payroll, not new-construction supplier flow."
        evidence: wiki 12 categorically excluded; wiki 01 scope
        safe_container: excluded_card
        density_trigger: Add if sustainment dollars are raised.
    do_not_add:
      - TAM, SAM, SOM circles or Venn diagrams
      - any summed AP plus Basic Construction numerator
      - any line suggesting excluded flows are addressable upside under the current model
      - SOM, capture, or win-probability language anywhere on the slide

data_and_calculations:
  data_inputs:
    - {input: AP and LLTM additive base, value: 0, unit: dollars, display: "$0", tie_out: inputs_assumptions.py section 3 (additive base confirmed 0), used_in: excluded_card_1}
  rounding_rules: Display the additive AP and LLTM base as $0.
  reconciliation: Included, excluded, and context-only columns are mutually exclusive interpretation buckets for the current boundary; context evidence can support assumptions but is never added to TAM.

qa:
  guardrails:
    - The boundary explicitly excludes GFE, SIB, yards, depot and sustainment, and SOM.
    - AP and LLTM are shown as $0 additive, not added to Basic Construction.
    - The bottom warning rail states no capture share, win probability, or revenue forecast.
    - The three-column layout uses cards, not a native table, to avoid reading like a data grid.
  source_checks:
    - Visible sources are external published documents only (SCN P-5c and P-10, FAR 52.204-10 and Part 45, GAO-25-106286); no workbook tabs or wiki chapters appear in chrome.sources.
    - Internal provenance (guide_methodology.py, inputs_assumptions.py, wiki chapters) stays in meta.inputs, tie_outs, and reserve evidence only.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - no chart rIds because charts is empty
    - no table-fit check because the boundary matrix is shape-built cards, not a native table
