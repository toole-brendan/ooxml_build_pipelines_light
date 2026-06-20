# SlideSpec — DDG tam_methodology
# Body slide 7. Shape-built two-stream equation engine with an explicit PLUS operator
# and four counted connectors. No native chart or workbook table.

meta:
  slide_id: ddg-s07
  slide_order: 7
  module_name: tam_methodology.py
  slide_type: body
  section: TAM Methodology
  archetype: two_stream_equation_engine
  story_role: Introduce the two-stream supplier TAM method (Basic Construction plus AP and LLTM) and the denominator correction behind the BC coefficient, before the numeric waterfall on the next slide.
  inputs:
    - TAM Build model_tam_build §2b (stream bases), §3a (per-stream coefficients), §5a/§5c/§5d (TAM by FY, portfolio, per-hull)
    - Assumptions inputs_assumptions §3 (CY AP), §5 (ship-construction share 0.80, AP supplier coefficient 0.85)
    - AP Bridge data_ap_bridge §2 (CY AP x share x coefficient = AP/LLTM stream TAM)
    - POP Corpus / TAM Build §3a-§3b (BC coefficient support, MYP correction audit)
    - Deck Outputs DO-16 .. DO-22
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (full numeric TAM build)
    - ddg-a3   # appendix_myp_correction (disclosed-only vs MYP-corrected outside-yards)
    - ddg-a4   # appendix_ap_lltm_sensitivity (AP stream knobs)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Method
  title_topic: TAM Methodology
  title_finding: TAM combines Basic Construction supplier work with AP and LLTM supplier material
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
    - DoD DDG-51 daily contract announcements, July 2022 to May 2026
    - SAM.gov Acquisition Subaward Reporting Public API
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoD DDG-51 daily contract announcements, July 2022 to May 2026; (3) SAM.gov Acquisition Subaward Reporting Public API"

story:
  objective: Explain the sizing equation clearly enough that a reader understands the two streams and the denominator correction behind the Basic Construction coefficient, before the numeric build.
  do_not_say:
    - Do not call the model SOM, capture probability, win probability, or a sales forecast.
    - Do not present the 32.8% outside-yards POP correction as the BC supplier coefficient.
    - Do not present the disclosed-only ~87% artifact as the BC supplier coefficient.
    - Do not turn the methodology into SAM bucket taxonomy; that belongs to later slides.
    - Use words such as "times" and "plus" in visible equation text rather than symbols.
  known_caveats:
    - The AP and LLTM stream is assumption-driven because there is no DDG AP POP corpus equivalent to the Basic Construction actions.
    - The BC supplier coefficient is measured on a MYP-corrected non-GFE corpus and then applied to the BC base.
    - The 12.5% BC coefficient, the ~32.8% MYP-corrected outside-yards POP, and the disclosed-only ~87% artifact are three distinct numbers; keep them separate.

object_assessment:
  verdict: "Aggressive redesign: make the equation a two-input engine with an explicit plus operator and counted connectors. The old two-card layout under-specifies the flow."
  object_contract:
    render_pattern: two_stream_equation_engine
    expected_rendered_object_count: 9
    compound_objects:
      - {id: stream_connectors_1, child_count: 4, child_type: connector}
      - {id: operator_plus_1, child_count: 1, child_type: operator_glyph}
    required_focal_family: "The portfolio output card is the only BLUE_5 1.5pt hero block. Stream cards are secondary light panels."
  anti_repetition:
    versus_myp_redaction: "No chart or correction bars."
    versus_annual_tam_build: "No numeric waterfall/table; that is S08."
    forbidden_defaults:
      - No seven-step card row.
      - No workbook table.
      - No additional dark stream cards.

regions:
  coord_basis: BODY
  layout_pattern: two_stream_equation_engine
  equation_banner: {x: 0%, y: 0%, w: 100%, h: 15%}
  stream_left:     {x: 0%, y: below(equation_banner) + GAP, w: 43%, h: 37%}
  operator_plus:   {x: 46%, y: align_top(stream_left), w: 8%, h: 37%}
  stream_right:    {x: 57%, y: align_top(stream_left), w: remaining, h: 37%}
  connector_bus:   {x: 0%, y: below(stream_left), w: 100%, h: 13%}
  output_card:     {x: 29%, y: below(connector_bus) + GAP, w: 42%, h: 18%}
  guardrail_note:  {x: 0%, y: below(output_card) + GAP, w: 100%, h: fit_content}
  note_strip:      {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: diagram,   region: equation_banner, prominence: tertiary,  paint_order: 2, content: no-fill equation banner}
  - {id: e2, type: diagram,   region: stream_left,     prominence: secondary, paint_order: 4, content: Basic Construction stream card, tie_out: TAM Build §2b/§3a}
  - {id: e3, type: diagram,   region: operator_plus,   prominence: tertiary,  paint_order: 5, content: plus operator glyph between the two streams}
  - {id: e4, type: diagram,   region: stream_right,    prominence: secondary, paint_order: 4, content: AP and LLTM stream card, tie_out: AP Bridge §2 / Inputs §5}
  - {id: e5, type: connector, region: connector_bus,   prominence: tertiary,  paint_order: 3, content: four explicit connectors from stream cards through plus glyph into output}
  - {id: e6, type: diagram,   region: output_card,     prominence: primary,   paint_order: 6, content: portfolio supplier TAM output card, tie_out: TAM Build §5c / DO-16 .. DO-22}
  - {id: e7, type: note,      region: guardrail_note,  prominence: tertiary,  paint_order: 7, content: BC coefficient guardrail}
  - {id: e8, type: note,      region: note_strip,      prominence: tertiary,  paint_order: 8, content: standard sizing note}

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
    - shape: equation_1
      element: e1
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: MESSAGE_11PT, color: DK, font: FONT}
      note: "Short thesis or boundary sentence; keep no fill/no border."
    - shape: bc_stream_1
      element: e2
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: operator_plus_1
      element: e3
      profile: operator_glyph
      runs:
        - {role: operator, size: BADGE_16PT, bold: true, all_caps: true, color: DK, font: FONT}
      note: "Single centered word; keep it visually subordinate to the portfolio output card."
    - shape: ap_stream_1
      element: e4
      profile: secondary_map_or_stream_node
      runs:
        - {role: title, size: LABEL_9PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: emphasis, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
      note: "Use title/body hierarchy inside the node; no hidden inherited sizes."
    - shape: stream_connectors_1
      element: e5
      profile: connector_group
      runs: []
      note: "No text runs; any connector annotation uses CONNECTOR_NOTE_8_5PT italic with font=FONT."
    - shape: portfolio_output_1
      element: e6
      profile: primary_kpi_or_output_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: WHITE, font: FONT}
        - {role: value, size: ANSWER_KPI_24PT, bold: true, color: WHITE, font: FONT}
        - {role: qualifier, size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
      note: "Value line dominates; cumulative or qualifier line stays smaller than the annual value."
    - shape: guardrail_1
      element: e7
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."
    - shape: sizing_note_1
      element: e8
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts: []
tables: []
images: []

shapes:
  - id: equation_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Supplier TAM is the sum of two separately gated supplier streams."
    meaning: No-fill thesis; avoids a third filled card family.
  - id: bc_stream_1
    element: e2
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: |
      BASIC CONSTRUCTION STREAM
      BC base (P-5c Basic Construction): ~$17.47B cumulative
      Times 12.5% MYP-corrected supplier coefficient
      Equals ~$365M per year
      (~$2.19B cumulative)
    meaning: Defines the BC stream and keeps the applied 12.5% coefficient visible.
  - id: operator_plus_1
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    insets: INSETS_CHIP
    text: "PLUS"
    meaning: Explicit operator glyph; separates the two streams without using a symbol.
  - id: ap_stream_1
    element: e4
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: |
      AP AND LLTM STREAM
      CY AP base after 80.0% ship-construction share: ~$1.47B cumulative
      Times 85.0% AP supplier coefficient
      Equals ~$208M per year
      (~$1.25B cumulative)
    meaning: Defines the assumption-driven AP and LLTM stream.
  - id: stream_connectors_1
    element: e5
    factory: connector_group
    fill: null
    line_color: GRAY_4
    insets: INSETS_NONE
    child_connectors:
      - {name: bc_to_plus, from: stream_left, to: operator_plus, arrow: false}
      - {name: ap_to_plus, from: stream_right, to: operator_plus, arrow: false}
      - {name: plus_to_output_left, from: operator_plus, to: output_card, arrow: false}
      - {name: plus_to_output_right, from: operator_plus, to: output_card, arrow: false}
    meaning: Counted connector group; avoids ambiguous connector bus instructions.
  - id: portfolio_output_1
    element: e6
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    paragraphs:
      - runs:
          - {text: "PORTFOLIO SUPPLIER TAM", size: CAP_12PT, bold: true, color: WHITE}
      - runs:
          - {text: "~$573M per year", size: ANSWER_KPI_24PT, bold: true, color: WHITE}
      - runs:
          - {text: "(~$3.44B FY22-27 cumulative)", size: LABEL_9PT, italic: true, color: WHITE}
    meaning: Only dark hero object on the slide.
  - id: guardrail_1
    element: e7
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Guardrail: the BC coefficient is 12.5% on the MYP-corrected non-GFE corpus. It is not the ~32.8% outside-yards POP share, nor the disclosed-only ~87% artifact."
    meaning: Prevents readers from substituting the outside-yards POP figure or artifact for the actual coefficient.
  - id: sizing_note_1
    element: e8
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note.

commentary:
  visible:
    element: e6
    container: method_note
    title: Guardrail
    bullets:
      - {lead: "BC coefficient:", body: "12.5% on the MYP-corrected non-GFE corpus, not the ~32.8% outside-yards POP and not the disclosed-only ~87% artifact."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the method bridge between the cost funnel / MYP
      slides and the numeric TAM build (S08 annual_tam_build) and timing (S09
      tam_timing). The goal is not to prove every source cell, but to make the
      two-stream structure legible: portfolio supplier TAM = Basic Construction
      supplier work away from the two prime yards, PLUS AP and LLTM supplier material
      that is addressable after the ship-construction share. The deck headline is
      ~$573M per year (~$3.44B cumulative FY22-27). [tie-out: TAM Build §5; DO-01]

      THE BASIC CONSTRUCTION STREAM. Base = P-5c Basic Construction (SCN LI 2122),
      summed FY22-27: $1,960.0 + $4,558.2 + $3,322.5 + $4,628.2 + $282.6 + $2,719.6 =
      ~$17,471M (~$17.47B). The applied supplier coefficient is 12.5% (the live
      computed value is ~12.55%, displayed as 12.5%). It is defined as the
      MYP-corrected other-US plus foreign POP share over the non-GFE BC corpus, with
      the $-redacted BIW and Ingalls MYP masters folded back at reconstructed POP.
      ~$17.47B x 12.5% = ~$2,192M (~$2.19B), or ~$365M per year. Note FY26 BC base is
      anomalously low (~$283M, an AP-only budget year), which is why the BC stream
      dips to ~$35M that year. [tie-out: TAM Build §2b/§3a; SCN Budget basic_construction]

      WHY 12.5% AND NOT 32.8% OR 87%. Three POP figures travel together and must stay
      distinct: (a) the disclosed-only outside-yards artifact ~87%, which over-weights
      GFE because the two MYP masters are $-redacted and drop out of the disclosed
      denominator; (b) the MYP-corrected outside-yards POP ~32.8% (the 0.33 anchor),
      once the ~$14.58B BIW plus Ingalls masters are folded back at reconstructed POP;
      and (c) the applied BC supplier coefficient 12.5%, measured over the non-GFE BC
      corpus specifically (a narrower denominator than all-gated POP). Presenting 87%
      or 32.8% as the coefficient would overstate the BC stream several-fold.
      [tie-out: TAM Build §3a-§3c; wiki 04, 12]

      THE AP AND LLTM STREAM. This is a separate, assumption-driven stream because
      DDG advance procurement has no FFATA POP corpus to measure a coefficient over.
      In-window CY Advance Procurement (FY25 $83.224M + FY26 $1,750.0M = $1,833.2M;
      FY22-24 sit in Prior Years) x 80.0% ship-construction share = ~$1,466.6M
      (~$1.47B, the intermediate AP base) x 85.0% AP supplier coefficient = ~$1,246.6M
      (~$1.25B), or ~$208M per year. The 80.0% share strips AWS EOQ and other GFE from
      CY AP; the 85.0% coefficient is an Inputs knob. Both are editable assumptions.
      [tie-out: Inputs §3/§5; AP Bridge §2; TAM Build §5a]

      THE TWO STREAMS COMBINE. ~$365M per year (BC) plus ~$208M per year (AP and LLTM)
      = ~$573M per year; ~$2.19B plus ~$1.25B = ~$3.44B cumulative. Per-hull framing:
      ~$265M supplier TAM per in-window hull across 13 hulls awarded FY22-27, of which
      BC-only is ~$169M per hull (distinct from the metal SAM scenario's ~$170M per
      year; do not conflate). [tie-out: TAM Build §5c/§5d]

      DENSITY GUIDANCE. Default is one equation, two stream cards, one output card,
      one guardrail. Do not add a workbook-style calculation table here; the next
      slide carries the numeric bridge and the appendix (A2) carries the full build.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e5, e6, e7]}
      dense:  {add_bullets: 3, safe_containers: [guardrail_note, stream_left, stream_right], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Two streams:", body: "BC supplier work and AP and LLTM supplier material are modeled separately, then added to portfolio TAM.", evidence: "TAM Build §5a", safe_container: guardrail_note, density_trigger: "Add only if the stream labels need more explanation."}
      - {priority: 2, lead: "Three distinct POP numbers:", body: "12.5% applied BC coefficient (non-GFE BC corpus), ~32.8% MYP-corrected outside-yards POP, and the disclosed-only ~87% artifact are not interchangeable.", evidence: "TAM Build §3a-§3c; wiki 12", safe_container: guardrail_note, density_trigger: "Add if a reviewer asks about the denominator correction."}
      - {priority: 3, lead: "AP base intermediate:", body: "In-window CY AP ~$1.83B times the 80.0% ship-construction share gives the ~$1.47B AP base before the 85.0% coefficient.", evidence: "AP Bridge §2; Inputs §3/§5", safe_container: stream_right, density_trigger: "Add in a dense methodology version."}
      - {priority: 4, lead: "BC coefficient definition:", body: "12.5% = MYP-corrected other-US plus foreign POP over the non-GFE BC corpus, with the redacted BIW and Ingalls masters folded back at reconstructed POP.", evidence: "TAM Build §3a (BC stream coefficient note)", safe_container: stream_left, density_trigger: "Add if the audience asks what the coefficient measures."}
      - {priority: 5, lead: "Output tie:", body: "~$365M per year from BC plus ~$208M per year from AP and LLTM reconciles to ~$573M per year and ~$3.44B cumulative.", evidence: "DO-16 .. DO-22; TAM Build §5c", safe_container: output_card, density_trigger: "Use only if numeric reconciliation is needed on the method slide."}
      - {priority: 6, lead: "Per-hull anchor:", body: "~$265M supplier TAM per in-window hull across 13 hulls; BC-only ~$169M per hull (not the ~$170M metal scenario).", evidence: "TAM Build §5d", safe_container: guardrail_note, density_trigger: "Add when the audience thinks per-ship."}
      - {priority: 7, lead: "AP is assumption-driven:", body: "The 80.0% ship-construction share and 85.0% AP coefficient are Inputs knobs because DDG AP has no FFATA POP corpus to measure over.", evidence: "Inputs §5; AP Bridge §4", safe_container: stream_right, density_trigger: "Add if a reviewer treats the AP stream as measured rather than assumed."}
      - {priority: 8, lead: "FY26 dip explained:", body: "FY26 BC base is anomalously low (~$283M, an AP-only budget year), so the BC stream is only ~$35M that year while AP carries the load.", evidence: "SCN Budget (FY26 basic_construction); AP Bridge", safe_container: stream_left, density_trigger: "Add if the timing slide raises the FY26 question early."}
      - {priority: 9, lead: "Not SAM, not capture:", body: "This sizes supplier-addressable TAM only; it applies no win or capture probability and is not SAM bucket taxonomy.", evidence: "Consolidated deck specification", safe_container: guardrail_note, density_trigger: "Add if commercial or SAM language starts creeping in."}
      - {priority: 10, lead: "Readable equation:", body: "Keep words such as times and plus in the visible equation so it reads as a plain-English method, not a workbook formula.", evidence: "Build notes", safe_container: equation_banner, density_trigger: "Builder guidance only."}
    do_not_add:
      - Detailed workbook cell references on the slide.
      - Capture probability, win probability, or SOM language.
      - The ~32.8% outside-yards POP or the disclosed-only ~87% artifact presented as the BC coefficient.
      - SAM bucket taxonomy (belongs to later slides).

data_and_calculations:
  data_inputs:
    - {input: Basic Construction base, value: 17471.0, unit: "$M cumulative", year: "FY22-27", tie_out: "TAM Build §2b; SCN Budget basic_construction", used_in: bc_stream_1}
    - {input: BC supplier coefficient (applied), value: "12.5%", unit: coefficient, year: "FY22-27", tie_out: "TAM Build §3a (computed ~12.55%, displayed 12.5%)", used_in: bc_stream_1}
    - {input: In-window CY AP base, value: 1833.2, unit: "$M cumulative", year: "FY25-26", tie_out: "Inputs §3; AP Bridge §2", used_in: ap_stream_1}
    - {input: AP ship-construction share, value: "80.0%", unit: coefficient, year: "FY22-27", tie_out: "Inputs §5", used_in: ap_stream_1}
    - {input: AP base after ship-construction share, value: 1466.6, unit: "$M cumulative", year: "FY22-27", tie_out: "AP Bridge §2", used_in: ap_stream_1}
    - {input: AP and LLTM supplier coefficient, value: "85.0%", unit: coefficient, year: "FY22-27", tie_out: "Inputs §5", used_in: ap_stream_1}
    - {input: BC stream TAM, value: 365, unit: "$M per year", cumulative: 2.19, tie_out: "TAM Build §5a/§5b", used_in: portfolio_output_1}
    - {input: AP and LLTM stream TAM, value: 208, unit: "$M per year", cumulative: 1.25, tie_out: "AP Bridge §2; TAM Build §5a", used_in: portfolio_output_1}
    - {input: Portfolio supplier TAM, value: 573, unit: "$M per year", cumulative: 3.44, tie_out: "TAM Build §5c; DO-16 .. DO-22", used_in: portfolio_output_1}
  calculations:
    - {name: BC stream TAM, formula: "BC base ~$17,471M times 12.5% MYP-corrected supplier coefficient", output: "~$2,192M cumulative, ~$365M per year", used_in: bc_stream_1}
    - {name: AP and LLTM stream TAM, formula: "in-window CY AP ~$1,833M times 80.0% ship-construction share times 85.0% AP coefficient", output: "~$1,247M cumulative, ~$208M per year", used_in: ap_stream_1}
    - {name: Portfolio TAM method, formula: "BC stream plus AP and LLTM stream", output: "~$573M per year and ~$3.44B cumulative", used_in: equation_1}
  rounding_rules: Round annual values to nearest whole $M in visible text; cumulative values to two decimals in $B; coefficients to one decimal percent.
  reconciliation: BC stream (~$365M per year) plus AP and LLTM stream (~$208M per year) equals portfolio supplier TAM (~$573M per year). The 12.5% applied coefficient is distinct from the ~32.8% MYP-corrected outside-yards POP and the disclosed-only ~87% artifact.

qa:
  guardrails:
    - Equation uses words in visible slide text and avoids mathematical symbols.
    - BC supplier coefficient is shown as 12.5%, not 32.8% and not 87%.
    - AP supplier coefficient (85.0%) and ship-construction share (80.0%) are clearly labeled as assumptions.
    - The ~$1.47B intermediate AP base appears on the AP stream card.
    - No SOM, capture, or win-probability language appears.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal docs, workbook tabs, or chart IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "no chart rIds required because charts is empty"
