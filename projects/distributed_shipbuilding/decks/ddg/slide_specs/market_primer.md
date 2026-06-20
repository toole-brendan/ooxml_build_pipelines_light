# SlideSpec — DDG market_primer
# Body slide 2. Counted system map: Navy funding node, two prime-yard nodes, one
# in-scope supplier lane, six explicit connectors, four thin excluded/evidence tags, and no chart.

meta:
  slide_id: ddg-s02
  slide_order: 2
  module_name: market_primer.py
  slide_type: body
  section: Market Definition
  archetype: shape_built_system_map_with_exclusion_tags
  story_role: Make the DDG-51 construction ecosystem legible before the deck introduces any market-size number, so the reader never applies one gross denominator to every DDG-51 dollar.
  inputs:
    - Methodology tab (in/out of TAM; two-stream definition)
    - Scope Exclusions tab (GFE / weapons / DDG-1000 boundary)
    - TAM Build tab (two-stream structure context only; no values shown)
    - wiki 01 (scope and funnel framework; two-yard structure)
    - wiki 03 (Plans, GFE, and other layers)
  related_appendix:
    - ddg-a1   # appendix_definitions_scope (full in/out-of-scope record)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Market primer
  title_topic: Market Primer
  title_finding: DDG-51 construction dollars flow through prime yards, Navy-procured GFE primes, and yard-side suppliers
  layout: slideLayout4
  sources:
    - U.S. Navy FY2027 SCN Justification Book, LI 2122
    - FAR Part 45 and FAR 52.245-1, Government Property
    - FAR 52.204-10
  source_line_exact: "Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122; (2) FAR Part 45 and FAR 52.245-1, Government Property; (3) FAR 52.204-10"

story:
  objective: Explain who pays whom and which flows are in scope so the reader does not treat DDG-51 construction as one undifferentiated supplier pool; make the denominator language visual before the cost funnel, MYP correction, and TAM build.
  do_not_say:
    - Do not use logos; use text chips only.
    - Do not imply GFE primes are bad data; they are real DDG spend outside this non-GFE TAM.
    - Do not call the excluded GFE lane a GFE supplier TAM.
    - Do not introduce SOM, capture, or win-probability language.
    - Do not put a TAM or SAM dollar value on this slide; it is the primer, not the answer.
  known_caveats:
    - FFATA-visible subawards are an evidence source, not the market definition.
    - GFE remains important context even though it is excluded from this TAM.
    - The two yards are prime-yard nodes, not target suppliers inside the addressable layer.

object_assessment:
  verdict: "Aggressive redesign: the previous spec was a polite ecosystem card page. Make it a true flow map with counted lanes and explicit excluded tags."
  object_contract:
    render_pattern: system_map_with_counted_connectors_and_exclusion_tags
    expected_rendered_object_count: 19
    compound_objects:
      - {id: connectors_1, child_count: 6, child_type: connector, paint_first: true}
      - {id: excluded_tags, child_count: 4, child_type: text_box_tag}
    required_focal_family: "One BLUE_5 Navy node plus one BLUE_1 in-scope supplier lane; excluded lanes are thin gray tags, not equal cards."
  anti_repetition:
    versus_next_slide: "Scope is a native ledger; this slide must use connectors and lane tags, not a two-column table."
    forbidden_defaults:
      - No KPI cards.
      - No ranked bar.
      - No equal-weight card grid.
      - No logos.

regions:
  coord_basis: BODY
  layout_pattern: system_map_with_counted_connectors_and_exclusion_tags
  thesis_strip:    {x: 0%,  y: 0%,  w: 100%, h: 12%}
  navy_node:        {x: 3%,  y: 20%, w: 22%,  h: 18%}
  yard_biw:         {x: 32%, y: 16%, w: 27%,  h: 15%}
  yard_ingalls:     {x: 32%, y: 35%, w: 27%,  h: 15%}
  supplier_lane:    {x: 66%, y: 21%, w: 34%,  h: 24%}
  connector_bus:    {x: 0%,  y: 13%, w: 100%, h: 40%}
  excluded_title:   {x: 0%,  y: 58%, w: 100%, h: TITLE_BAND_H}
  excluded_gfe:     {x: 0%,  y: 65%, w: 24%,  h: fit_content}
  excluded_weapons: {x: 25%, y: 65%, w: 24%,  h: fit_content}
  excluded_sustain: {x: 50%, y: 65%, w: 24%,  h: fit_content}
  excluded_ffata:   {x: 75%, y: 65%, w: 25%,  h: fit_content}
  legend:           {x: 0%,  y: 82%, w: 61%,  h: fit_content}
  commentary_rail:  {x: 66%, y: 82%, w: remaining, h: fit_content}

element_inventory:
  - {id: e1,  type: connector, region: connector_bus,   prominence: tertiary,  paint_order: 1,  content: connector group with six explicit child connectors linking Navy to yards, GFE, and in-scope supplier lane}
  - {id: e2,  type: note,      region: thesis_strip,    prominence: tertiary,  paint_order: 2,  content: no-fill thesis strip explaining the market is layered}
  - {id: e3,  type: diagram,   region: navy_node,       prominence: primary,    paint_order: 3,  content: Navy SCN Line Item 2122 funding node, tie_out: Methodology §1}
  - {id: e4,  type: diagram,   region: yard_biw,        prominence: secondary,  paint_order: 4,  content: GD Bath Iron Works prime-yard node, tie_out: wiki 01}
  - {id: e5,  type: diagram,   region: yard_ingalls,    prominence: secondary,  paint_order: 5,  content: HII Ingalls prime-yard node and distributed-network context, tie_out: wiki 01}
  - {id: e6,  type: diagram,   region: supplier_lane,   prominence: primary,    paint_order: 6,  content: in-scope yard-side supplier lane sized by the deck, tie_out: Methodology §4}
  - {id: e7,  type: exhibit_title, region: excluded_title, prominence: tertiary, paint_order: 7,  content: no-fill excluded-lanes label}
  - {id: e8,  type: diagram,   region: excluded_gfe,     prominence: tertiary,  paint_order: 8,  content: thin excluded GFE tag, tie_out: wiki 03}
  - {id: e9,  type: diagram,   region: excluded_weapons, prominence: tertiary,  paint_order: 9,  content: thin excluded weapons tag, tie_out: Methodology exclusions}
  - {id: e10, type: diagram,   region: excluded_sustain, prominence: tertiary,  paint_order: 10, content: thin excluded sustainment and depot tag, tie_out: Scope Exclusions}
  - {id: e11, type: diagram,   region: excluded_ffata,   prominence: tertiary,  paint_order: 11, content: thin FFATA evidence-not-definition tag, tie_out: FAR 52.204-10}
  - {id: e12, type: note,      region: legend,           prominence: tertiary,  paint_order: 12, content: no-fill legend explaining blue lane vs gray excluded tags}
  - {id: e13, type: rail,      region: commentary_rail,  prominence: secondary, paint_order: 13, content: no-fill market-layer reading rail}

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
  table_rules: []
  shape_rules:
    - shape: connectors_1
      element: e1
      profile: connector_group
      runs: []
      note: "No text runs; any connector annotation uses CONNECTOR_NOTE_8_5PT italic with font=FONT."
    - shape: thesis_strip_1
      element: e2
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: MESSAGE_11PT, color: DK, font: FONT}
      note: "Use no fill/no border; reserve filled treatment for warning/scope-boundary notes only."
    - shape: navy_node_1
      element: e3
      profile: primary_map_or_stream_node
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: WHITE, font: FONT}
        - {role: body, size: LABEL_9PT, color: WHITE, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: WHITE, font: FONT}
      note: "Primary node is allowed a stronger cap but should not use answer-card KPI scale unless it is a numeric output."
    - shape: biw_node_1
      element: e4
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: ingalls_node_1
      element: e5
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: supplier_lane_1
      element: e6
      profile: primary_map_or_stream_node
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Primary in-scope lane; stronger than excluded tags but below numeric hero-card scale."
    - shape: excluded_title_1
      element: e7
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: tag_gfe_1
      element: e8
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: tag_weapons_1
      element: e9
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: tag_sustain_1
      element: e10
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: tag_ffata_1
      element: e11
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: legend_1
      element: e12
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Use no fill/no border; reserve filled treatment for warning/scope-boundary notes only."
    - shape: commentary_rail_1
      element: e13
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."

charts: []

tables: []

shapes:
  - id: connectors_1
    element: e1
    factory: connector_group
    fill: null
    line_color: GRAY_4
    insets: INSETS_NONE
    child_connectors:
      - {name: navy_to_biw, from: navy_node, to: yard_biw, arrow: false}
      - {name: navy_to_ingalls, from: navy_node, to: yard_ingalls, arrow: false}
      - {name: biw_to_supplier_lane, from: yard_biw, to: supplier_lane, arrow: false}
      - {name: ingalls_to_supplier_lane, from: yard_ingalls, to: supplier_lane, arrow: false}
      - {name: navy_to_gfe_tag, from: navy_node, to: excluded_gfe, arrow: false, dashed: true}
      - {name: supplier_lane_to_ffata_tag, from: supplier_lane, to: excluded_ffata, arrow: false, dashed: true}
    meaning: Six explicit connectors; painted first so nodes and tags sit on top.
  - id: thesis_strip_1
    element: e2
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Read DDG-51 construction as lanes: Navy funding, two prime yards, Navy-procured GFE, and the yard-side supplier layer sized in this deck."
    meaning: No-fill thesis strip; not another card.
  - id: navy_node_1
    element: e3
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_CARD
    text: "U.S. Navy SCN
Line Item 2122
new-construction funding"
    meaning: Dark funding node; one of only two focal objects.
  - id: biw_node_1
    element: e4
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "GD Bath Iron Works
Prime yard: Bath and Brunswick"
    meaning: Prime-yard node; context, not a target supplier category.
  - id: ingalls_node_1
    element: e5
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "HII Ingalls
Prime yard plus distributed-partner context"
    meaning: Prime-yard node with HII distributed-network cue.
  - id: supplier_lane_1
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    line_width: 19050
    insets: INSETS_MESSAGE
    text: "IN-SCOPE YARD-SIDE SUPPLIER WORK
Structural fabrication, machining, electrical and power, piping, HVAC, coatings, castings and forgings, and AP and LLTM material"
    meaning: Primary in-scope lane; distinct from thin excluded tags.
  - id: excluded_title_1
    element: e7
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Excluded or evidence-only lanes — shown so gross DDG spend is not mistaken for TAM"
    meaning: Quiet label over the gray tag row.
  - id: tag_gfe_1
    element: e8
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "GFE primes
Aegis, SPY-6, VLS, Mk 45, LM2500, SEWIP"
    meaning: Thin excluded lane tag, not an equal-weight card.
  - id: tag_weapons_1
    element: e9
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Weapons procurement
WPN and OPN flows"
    meaning: Thin excluded weapons tag.
  - id: tag_sustain_1
    element: e10
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "Sustainment and depot
not new construction"
    meaning: Thin excluded sustainment tag.
  - id: tag_ffata_1
    element: e11
    factory: text_box
    fill: GRAY_2
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "FFATA-visible subawards
evidence source, not definition"
    meaning: Evidence-only tag that prevents visible-flow denominator confusion.
  - id: legend_1
    element: e12
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Legend: blue objects are in-scope sizing lanes; gray tags are excluded or evidence-only context."
    meaning: No-fill legend keeps map grammar explicit.
  - id: commentary_rail_1
    element: e13
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text:
      bullets:
        - {lead: "Layering:", body: "SCN funding, prime-yard construction, GFE prime flows, and yard-side supplier work are separate lanes."}
        - {lead: "Scope:", body: "the deck sizes the non-GFE supplier lane only."}
        - {lead: "Use:", body: "this slide defines the map; no TAM or SAM dollar value appears here."}
    meaning: No-fill reading rail; secondary to the map.

images: []

commentary:
  visible:
    element: e8
    container: right_rail
    title: "How to read the map"
    bullets:
      - {lead: "Layering:", body: "Navy SCN dollars, yard prime flows, GFE prime flows, and yard-side supplier work are different economic lanes."}
      - {lead: "Scope:", body: "only the non-GFE new-construction supplier lane is sized in this deck."}
      - {lead: "GFE:", body: "excluded here, but essential to understanding why total DDG spend is not supplier TAM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. First body slide after the cover/divider, ahead of the
      executive summary (S03) and scope (S04). Its job is NOT to size the market; it is
      to stop the reader from applying one gross denominator to every DDG-51 dollar.
      The DDG-51 new-construction program has at least three visible lanes: (1) SCN-funded
      prime-yard construction at GD Bath Iron Works and HII Ingalls; (2) Navy-procured GFE
      prime flows (Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, SEWIP); and (3) yard-side
      supplier work embedded in Basic Construction plus AP and LLTM. Only the third lane is
      the focus of the TAM and SAM sizing. [tie-out: Methodology §1-§2; wiki 01 funnel]

      THE TWO-YARD STRUCTURE (what makes DDG distinct from the submarine program). DDG-51 is
      a TWO-YARD competitive procurement: both BIW and Ingalls hold direct prime contracts
      with the Navy (vs the submarine program's single GDEB prime with HII Newport News as an
      invisible team-build partner). Each hull is awarded to one yard on its own prime PIID;
      the FY23-27 multiyear blocks are two parallel prime contracts (BIW N00024-23-C-2305,
      Ingalls N00024-23-C-2307), not one umbrella prime. Consequence for this map: each yard's
      first-tier subaward tree is independently visible in FFATA, but the master award dollar
      values are source-selection-redacted (FAR 2.101 / 3.104) — the structural caveat that
      drives the MYP correction later in the deck. [tie-out: wiki 01 two-yard structure]

      WHY GFE IS DE-EMPHASIZED BUT NOT DISMISSED. GFE is the single largest outsourced layer
      by dollar weight: Electronics plus Ordnance run ~33% of Total Ship Estimate on the FY24
      vintage, and Aegis (LM Moorestown NJ) plus SPY-6 (Raytheon Andover MA) alone are ~$5.0B
      of the ~$7.13B DoD-announcement supplier corpus (~70%). The Navy procures GFE from
      separate primes and ships it to the yards for installation, so those dollars never appear
      as yard subawards and are NOT supplier-addressable new-construction work. The map shows
      GFE so the reader understands why "total DDG spend" overstates the addressable pool — not
      because GFE is bad data. Weapons (Standard Missile, ESSM, Tomahawk, CIWS) are a further
      step out: they are WPN/OPN-funded, not SCN, and gated out entirely. [tie-out: wiki 03;
      Methodology §3 exclusions]

      THE IN-SCOPE SUPPLIER LANE. The bottom rail is the object of the whole deck: non-GFE
      yard-side supplier work performed away from BIW, Ingalls, and GFE prime sites. It is
      modeled across seven work-type buckets (structural fabrication, machining, castings and
      forgings, piping, electrical, HVAC, coatings) plus AP and LLTM supplier-addressable
      material. DDG bucketing is description-led (the award description is the primary arbiter),
      unlike the submarine workbook's NAICS/vendor-led approach. [tie-out: Methodology §4-§5]

      FFATA IS A VISIBILITY LAYER, NOT THE DENOMINATOR. Later slides use SAM.gov first-tier
      subawards as evidence, but FFATA captures only ~15% of true yard-side subcontract flow
      (threshold $30,000 per action, FAR 52.204-10; one tier deep only; 12-30 month lag). The
      primer should set up that distinction without numbers so the audience is not surprised
      when SAM.gov appears in later sources. [tie-out: wiki 01; Methodology §7 caveats]

      DESIGN GUIDANCE. Keep the slide pictorial and low-number (only SCN LI 2122 and GFE system
      names carry text that looks numeric). Text chips, not logos. Thin connectors without
      arrowheads (visible-language rule). The yard-side supplier rail must read as the strongest
      visual; the GFE lane is intentionally quieter.
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e4, e5, e6, e7, e8]}
      dense:  {add_bullets: 3, safe_containers: [commentary_rail, supplier_rail], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Not one pool:"
        body: "DDG-51 construction dollars split across prime yards, Navy-procured GFE primes, and yard-side suppliers; only the third lane is sized."
        evidence: Methodology §1-§2; wiki 01 funnel
        safe_container: commentary_rail
        density_trigger: Add if a reader treats total DDG spend as TAM.
      - priority: 2
        lead: "Two-yard, two primes:"
        body: "Both BIW and Ingalls hold direct Navy prime contracts; each hull is awarded to one yard, so each yard's subaward tree is independently visible."
        evidence: wiki 01 (two-yard competitive procurement)
        safe_container: commentary_rail
        density_trigger: Add when contrasting with the single-prime submarine program.
      - priority: 3
        lead: "GFE is ~a third of the ship:"
        body: "Electronics plus Ordnance run ~33% of Total Ship Estimate; Aegis and SPY-6 alone are ~70% of the DoD-announcement supplier corpus, all outside the yards."
        evidence: wiki 03 (FY24 layer table); wiki 04
        safe_container: gfe_node
        density_trigger: Add if the GFE node has spare vertical space.
      - priority: 4
        lead: "GFE examples are context:"
        body: "Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, and SEWIP are real Navy-procured flows but sit outside this non-GFE TAM definition."
        evidence: wiki 03 (GFE primes); Methodology §3
        safe_container: gfe_node
        density_trigger: Add if a reviewer asks which systems are GFE.
      - priority: 5
        lead: "FFATA role:"
        body: "FFATA first-tier subawards are a visibility layer used later as evidence, not the denominator; they capture only ~15% of yard-side subcontract flow."
        evidence: wiki 01 (FFATA threshold); Methodology §7
        safe_container: commentary_rail
        density_trigger: Add if the audience asks why SAM.gov appears in later sources.
      - priority: 6
        lead: "Yards are not suppliers:"
        body: "BIW and Ingalls are assembling prime yards; the addressable supplier layer sits outside them, not inside."
        evidence: wiki 01 (denominators 2 and 3)
        safe_container: commentary_rail
        density_trigger: Add only if the yard nodes are misread as target suppliers.
      - priority: 7
        lead: "Weapons are a different appropriation:"
        body: "Standard Missile, ESSM, Tomahawk, and CIWS are WPN and OPN funded, not SCN, so they are gated out before the TAM begins."
        evidence: wiki 01; Methodology §3 (WPN/OPN)
        safe_container: gfe_node
        density_trigger: Add in a denser version distinguishing GFE from weapons.
      - priority: 8
        lead: "Description-led buckets:"
        body: "The in-scope supplier rail is modeled across seven work-type buckets classified by award description, the DDG primary arbiter."
        evidence: Methodology §4-§5 (taxonomy, precedence ladder)
        safe_container: supplier_rail
        density_trigger: Add in a denser supplier rail that names the seven buckets.
    do_not_add:
      - company logos
      - numerical TAM or SAM values
      - SOM, capture, or win-probability language
      - internal workbook tab names or wiki chapters in the rendered sources

data_and_calculations:
  data_inputs: []
  calculations: []
  rounding_rules: No numeric sizing on this slide beyond SCN Line Item 2122 and system names.
  reconciliation: This is a taxonomy and flow map, not a calculation slide; it aligns to the Methodology in/out-of-TAM definitions and the wiki 01 cost funnel.

qa:
  guardrails:
    - In-scope supplier rail is visually stronger than the GFE rail.
    - GFE examples appear only in the excluded lane, never in the supplier rail.
    - No SOM, capture, or win-probability language appears; no TAM or SAM dollar value on the slide.
    - The two yards are depicted as prime-yard nodes, not as suppliers.
    - No visible pipe, slash, or plus separators in any node or rail; commas and "and" only.
  source_checks:
    - Sources are real external citations only (SCN justification book, FAR Part 45 / 52.245-1 government property, FAR 52.204-10); no internal workbook tabs or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "connectors painted first (paint_order 1) so nodes sit on top"
