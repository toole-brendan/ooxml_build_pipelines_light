# SlideSpec - submarines `market_primer` (deck slide 02)
# Shape-built ecosystem SYSTEM MAP: one thesis strip over a three-node counted
# path (Navy/SCN -> GDEB Basic Construction -> counted non-nuclear supplier
# layer, the BLACK-bordered focal node) plus an HII context node and a work-type
# bucket node, with FOUR thin gray excluded-lane TAGS (GFE/GFP, BPMI nuclear,
# SIB, depot) rendered as short tag bands NOT equal-weight cards, a legend, and
# one compound connector group of 5 enumerated flow arrows. No chart, no external
# image. Establishes what is being sized before any number appears.

meta:
  slide_id: subs-s2
  slide_order: 2
  module_name: market_primer.py
  slide_type: body
  section: Market and Scope
  archetype: ecosystem_map_with_exclusion_lanes
  story_role: Establish what is being sized before any number appears, and separate the counted non-nuclear supplier layer from context and excluded procurement lanes.
  inputs:
    - guide_methodology.py (Methodology tab) sections 1 and 4, definitions and scope boundary
    - model_tam_build.py (TAM Build tab) for the Basic Construction base and two-stream framing
    - wiki 01 Scope and the funnel framework (cost funnel, four denominators, in-scope PIIDs)
    - wiki 02 Total ship cost (P-5c Total Ship Estimate, LI 2013 / LI 1045)
    - wiki 03 Plans, GFE, and other layers (GFE primes, BPMI, P-5c categories)
    - wiki 12 Unseen layer (FFATA floor vs unseen, HII team-build share)
  related_appendix:
    - subs-a1   # appendix_definitions_and_scope

chrome:
  section: Market and Scope
  breadcrumb_topic: Ecosystem primer
  title_topic: Market Primer
  title_finding: Submarine construction is a layered procurement ecosystem
  layout: slideLayout4
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibit P-5c
    - General Dynamics Corporation FY2021 Form 10-K
    - GAO-25-106286
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) General Dynamics Corporation FY2021 Form 10-K; (3) GAO-25-106286"

story:
  objective: Show that Navy submarine new-construction dollars move through multiple procurement layers and that the deck sizes only the non-nuclear supplier component layer inside Basic Construction.
  do_not_say:
    - Do not imply total ship cost equals supplier opportunity.
    - Do not imply GFE, nuclear reactor work, SIB capacity funding, depot work, or yard labor are inside TAM.
    - Do not present HII Newport News team-build work as open supplier SAM.
    - Avoid submarine photos, Navy seals, logos, or external imagery in the first build.
  known_caveats:
    - HII Newport News is operationally central but treated as a team-build yard layer, not an open supplier target; its workshare flows through the GDEB prime.
    - FFATA visibility is a named-vendor floor, not the full supplier layer.
    - SIB is used consistently in visible text; older MIB wording is avoided unless a source title forces it.

regions:
  coord_basis: BODY
  layout_pattern: ecosystem_map_with_exclusion_lanes
  # Top thesis strip; a three-node counted path with two second-row nodes; a
  # bottom row of four thin gray excluded-lane tag bands (deliberately shorter
  # than the path nodes so they read as tags, not equal-weight cards); a legend
  # strip pinned at the base.
  thesis_strip: {x: 0%, y: 0%, w: 100%, h: NOTE_H}
  navy_node: {x: 0%, y: 14%, w: 18%, h: 19%}
  gdeb_node: {x: 26%, y: 14%, w: 25%, h: 19%}
  supplier_node: {x: 60%, y: 14%, w: 32%, h: 19%}
  hii_node: {x: 27%, y: 42%, w: 24%, h: 18%}
  bucket_node: {x: 62%, y: 42%, w: 30%, h: 18%}
  gfe_node: {x: 0%, y: 68%, w: 22%, h: 11%}
  nuclear_node: {x: 25%, y: 68%, w: 22%, h: 11%}
  sib_node: {x: 50%, y: 68%, w: 22%, h: 11%}
  depot_node: {x: 75%, y: 68%, w: 22%, h: 11%}
  legend_strip: {x: 0%, y: 88%, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: callout, region: thesis_strip, prominence: secondary, paint_order: 1, content: sizing-path thesis}
  - {id: e2, type: diagram, region: navy_node, prominence: secondary, paint_order: 2, content: Navy and SCN budget authority node}
  - {id: e3, type: diagram, region: gdeb_node, prominence: secondary, paint_order: 3, content: GDEB prime construction contract node}
  - {id: e4, type: diagram, region: supplier_node, prominence: primary, paint_order: 4, content: counted non-nuclear supplier component layer node}
  - {id: e5, type: diagram, region: hii_node, prominence: tertiary, paint_order: 5, content: HII Newport News team-build context node}
  - {id: e6, type: diagram, region: bucket_node, prominence: secondary, paint_order: 6, content: work-type bucket node}
  - {id: e7, type: diagram, region: gfe_node, prominence: tertiary, paint_order: 7, content: GFE and GFP excluded lane}
  - {id: e8, type: diagram, region: nuclear_node, prominence: tertiary, paint_order: 8, content: BPMI and nuclear reactor excluded lane}
  - {id: e9, type: diagram, region: sib_node, prominence: tertiary, paint_order: 9, content: SIB capacity-development excluded lane}
  - {id: e10, type: diagram, region: depot_node, prominence: tertiary, paint_order: 10, content: depot and sustainment excluded lane}
  - {id: e11, type: note, region: legend_strip, prominence: tertiary, paint_order: 11, content: legend and interpretation tags}
  - {id: e12, type: connector, region: navy_node, prominence: tertiary, paint_order: 12, content: "connector group: 5 enumerated flow arrows between nodes"}


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
      - role: thesis sentence
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
    e2:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: counted-node cap
        size: CAP_12PT
        color: WHITE
        font: FONT
        bold: true
      - role: counted-node body
        size: DENSE_BODY_10PT
        color: WHITE
        font: FONT
    e5:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e6:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e7:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e8:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e9:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e10:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e11:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e12:
      connector_text: none; any connector label uses CONNECTOR_NOTE_8_5PT italic DK
  render_notes: []

charts: []
tables: []
images: []

shapes:
  - id: thesis_1
    element: e1
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MESSAGE
    text: "We size the supplier-addressable component layer inside Basic Construction, not total ship cost."
    meaning: Puts the boundary answer above the ecosystem map before the audience reads the lanes.
  - id: node_navy
    element: e2
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "NAVY and SCN budget authority\nP-5c Total Ship Estimate\nP-10 AP and LLTM timing"
    meaning: Left-side origin for the procurement ecosystem; SCN appropriation for Virginia SSN-774 and Columbia SSBN-826.
  - id: node_gdeb
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "GDEB prime construction contracts\nBasic Construction base\nPrime of record for Virginia and Columbia"
    meaning: Shows that Basic Construction is the construction-contract base from which the supplier TAM is derived.
  - id: node_supplier
    element: e4
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    text: "COUNTED SUPPLIER LAYER\nNon-nuclear components and subcontracts\nIn TAM and SAM candidate"
    meaning: The visually dominant sizing path; focal node, bordered to dominate the map.
  - id: node_hii
    element: e5
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "HII Newport News\nTeam-build workshare via GDEB prime\nContext and yard layer"
    meaning: Important ecosystem participant, but not open supplier SAM; its dollars flow through the GDEB prime.
  - id: node_buckets
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Work-type buckets\nStructural, electrical, piping, machining, castings, HVAC, coatings"
    meaning: Previews how counted supplier TAM later becomes bucket and scenario SAM.
  - id: node_gfe
    element: e7
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "GFE and GFP\nCombat systems, sonar, weapons\nExcluded"
    meaning: Separates government-furnished procurement lanes from supplier TAM; thin exclusion tag, not a card.
  - id: node_nuclear
    element: e8
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Nuclear and BPMI\nReactor plant\nExcluded"
    meaning: Makes the non-nuclear scope explicit; BPMI reactor plant is GFE to the assembling yard; thin exclusion tag, not a card.
  - id: node_sib
    element: e9
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "SIB capacity flows\nGrants and BlueForge-type funding\nExcluded"
    meaning: Distinguishes capacity-development funding from construction delivery; thin exclusion tag, not a card.
  - id: node_depot
    element: e10
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Depot and sustainment\nOverhauls and maintenance\nExcluded"
    meaning: Keeps new construction separate from sustainment; thin exclusion tag, not a card.
  - id: legend_1
    element: e11
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Legend: dark blue is the counted sizing path; light blue is related component logic; gray is context or excluded lanes."   # FINEPRINT_8_5PT italic
    meaning: Explains the color semantics without adding another filled callout.
  - id: connectors_1
    element: e12
    factory: connector
    from_to:
      - [e2, e3]
      - [e3, e4]
      - [e3, e5]
      - [e4, e6]
      - [e2, e7]
    style: {color: GRAY_4, width: CONNECTOR_NORMAL, arrow: true}
    meaning: Shape-built flow arrows; the builder routes them cleanly between node centers and suppresses arrowheads if too short.

commentary:
  visible:
    element: e1
    container: callout
    title:
    bullets:
      - {lead: "Scope:", body: "counted opportunity sits inside non-nuclear supplier components, not total ship cost."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the deck's first content slide. It prevents
      the most common confusion in the whole assessment: total submarine cost is
      not the same as supplier opportunity. The cost funnel (wiki 01) starts at
      the per-class per-fiscal-year Total Ship Estimate from SCN Exhibit P-5c,
      descends through the budget-justification cost categories (Plans Costs,
      Government-Furnished Equipment, Change Orders / Other, and Basic
      Construction), and then descends one further layer into Basic Construction
      itself, separating the share the prime shipyard self-performs from the
      share it outsources to the broader supplier base. The outsourced layer
      within Basic Construction is the object of the deck; everything else in the
      funnel exists to size, contextualize, or qualify it.

      THE COUNTED PATH. Navy SCN budget authority -> GDEB Basic Construction ->
      counted non-nuclear supplier component layer -> work-type buckets. General
      Dynamics Electric Boat (GDEB), in Groton, Connecticut with major production
      at Quonset Point, Rhode Island, is the prime of record on every active SCN
      Line Item 2013 (Virginia SSN-774 class) and Line Item 1045 (Columbia
      SSBN-826 class) construction contract. Inside the Basic Construction base
      are GDEB self-performed labor and overhead, HII Newport News team-build
      work, purchased material, first-tier subcontracts, and lower-tier supplier
      flow. The deck sizes the non-nuclear supplier component opportunity inside
      that base and maps it into seven work-type buckets.

      WHAT IS DELIBERATELY OUT. The model is not sizing nuclear-reactor GFE
      (Bechtel Plant Machinery, Inc. supplies the naval reactor plant under Naval
      Reactors direction), combat systems and sonar GFE (Lockheed Martin combat
      systems; Northrop Grumman sonar and electronic warfare), the Trident
      strategic weapon system (funded outside SCN), SIB capacity-development
      grants and BlueForge-type pass-throughs, depot and sustainment work at the
      four public naval shipyards, design-only Plans Costs, or the assembling
      yards' own labor. These are real dollars but they are not the non-nuclear
      supplier TAM.

      THE HII NODE REQUIRES CARE. HII Newport News is operationally crucial to
      Virginia and Columbia execution (publicly, roughly half of Virginia and
      about a fifth of Columbia by physical workload, and roughly six module
      sections per Columbia). But in this deck it is a co-prime or team-build
      yard layer, not a normal open supplier target. Its workshare flows through
      the GDEB prime and is recorded against GDEB as the vendor of record, so it
      is essentially invisible in the FFATA stream. That visibility gap helps
      explain why FFATA alone is a floor, but SAM should not imply a third party
      can simply capture HII team-build work.

      THE FOUR DENOMINATORS (why "outsourced" needs a denominator). Wiki 01 makes
      four candidate denominators of "outsourced" visible: (1) outsourced from
      GDEB's own prime contract; (2) outsourced from the Navy / SCN perspective
      (adds GFE primes); (3) outside-the-yard per DoD daily contract
      announcements; (4) all private-sector work outside the assembling yard. The
      deck sizes the supplier-addressable subset, closest to a strict non-nuclear
      reading of (1) and (3), and is explicit about which denominator each figure
      uses. This slide does not put numbers on the map; it sets the structure so
      later slides can.

      READ AS A MAP, NOT A CHART. This slide should read as an ecosystem map, not
      a process or financial chart. The bottom row shows procurement and funding
      lanes that are real but excluded from the modeled TAM. Keep the counted
      path visually dominant and the excluded lanes quiet gray.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]}
      dense: {add_bullets: 3, safe_containers: [thesis_strip, legend_strip, supplier_node], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Basic Construction anchor:"
        body: "Basic Construction is the construction-contract base; the Total Ship Estimate and GFE lanes are context, not the supplier denominator."
        evidence: guide_methodology.py section 4 scope boundary; wiki 01 cost funnel
        safe_container: thesis_strip
        density_trigger: Add if reviewers ask why total ship cost is not used.
      - priority: 2
        lead: "HII caution:"
        body: "HII team-build workshare is a yard layer and a visibility limitation, not open supplier SAM; it flows through the GDEB prime."
        evidence: wiki 12 unseen layer; General Dynamics FY2021 Form 10-K
        safe_container: hii_node
        density_trigger: Add if the HII node is misread as addressable supplier flow.
      - priority: 3
        lead: "GFE separation:"
        body: "Combat systems, sonar, weapons, and the reactor plant are separately procured or government-furnished and stay outside this TAM."
        evidence: wiki 03 Plans, GFE, and other layers; FAR Part 45
        safe_container: gfe_node
        density_trigger: Add if the audience includes procurement specialists.
      - priority: 4
        lead: "Who the GFE primes are:"
        body: "BPMI supplies the reactor plant; Lockheed Martin combat systems; Northrop Grumman sonar and electronic warfare; BAE deck modules; Rolls-Royce propulsion."
        evidence: wiki 01 prime of record; wiki 03 GFE categories
        safe_container: nuclear_node
        density_trigger: Add when the audience asks who builds the excluded content.
      - priority: 5
        lead: "SIB separation:"
        body: "SIB grants and BlueForge-type capacity funding support the industrial base but are not direct component-delivery revenue into a hull."
        evidence: GAO-25-106286; wiki 01 MIB pass-throughs
        safe_container: sib_node
        density_trigger: Add when demand-backdrop policy investment appears nearby.
      - priority: 6
        lead: "FFATA floor:"
        body: "Named FFATA-visible subawards support the map but do not fully expose lower-tier or embedded yard-side supplier activity."
        evidence: wiki 12 unseen layer; SAM.gov FFATA and FSRS records under FAR 52.204-10
        safe_container: legend_strip
        density_trigger: Add in a denser version that previews visibility limits.
      - priority: 7
        lead: "Four denominators:"
        body: "Outsourced needs a denominator; the deck sizes the supplier-addressable subset, closest to outsourced-from-GDEB and outside-the-yard, and says which it uses."
        evidence: wiki 01 four denominators of outsourced
        safe_container: thesis_strip
        density_trigger: Add for an analytically rigorous audience.
      - priority: 8
        lead: "Two classes, two line items:"
        body: "Scope is Virginia SSN-774 (Line Item 2013) and Columbia SSBN-826 (Line Item 1045) new construction, FY2022-FY2027."
        evidence: wiki 01 scope window; wiki 02 total ship cost
        safe_container: navy_node
        density_trigger: Add if the audience needs the exact program scope.
      - priority: 9
        lead: "Depot is separate:"
        body: "Depot maintenance and engineered overhauls run through the four public naval shipyards as federal payroll, outside the new-construction supplier flow."
        evidence: wiki 12 categorically excluded; wiki 01 scope
        safe_container: depot_node
        density_trigger: Add if sustainment dollars are raised as upside.
      - priority: 10
        lead: "Lead-boat cost shape:"
        body: "Columbia SSBN-826 carries heavy lead-boat Plans Costs (about 43% of its Total Ship Estimate), which is why total ship cost is a poor supplier denominator."
        evidence: wiki 02 total ship cost; wiki 03 lead-boat loading
        safe_container: gdeb_node
        density_trigger: Add when explaining why Plans Costs are excluded.
      - priority: 11
        lead: "SIB not MIB:"
        body: "Use SIB (Submarine Industrial Base) consistently in visible copy; older sources sometimes use MIB (Maritime Industrial Base) for the same line."
        evidence: guide_methodology.py SIB note
        safe_container: sib_node
        density_trigger: Add if a source title forces MIB wording.
    do_not_add:
      - logos, seals, submarine photography, or external images
      - TAM and SAM circles or Venn diagrams
      - any wording implying the excluded lanes are upside to be added back
      - any dollar figure on the map; numbers begin on later slides

qa:
  guardrails:
    - The counted non-nuclear supplier layer is visually obvious within 5 seconds.
    - GFE, SIB grants, depot work, and nuclear reactor work are visibly outside TAM.
    - The HII node is labeled context or yard layer, not open supplier SAM.
    - Visible text uses TAM and SAM, not a slashed TAM SAM, and uses SIB consistently.
    - No dollar figures appear on the map; this slide sets structure before numbers.
  source_checks:
    - Sources are external published documents only (SCN P-5c, GD 10-K, GAO-25-106286); no workbook tabs, wiki chapters, or chart IDs appear in chrome.sources.
    - Internal provenance (guide_methodology.py, model_tam_build.py, wiki chapters) stays in meta.inputs, element tie_outs, and reserve evidence only.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - no chart rIds because charts is empty
    - no table-fit check because tables is empty
