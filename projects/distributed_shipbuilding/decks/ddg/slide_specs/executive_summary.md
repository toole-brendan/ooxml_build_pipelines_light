# SlideSpec — DDG executive_summary
# Body slide 3. Pure KPI answer board: two dark hero KPI cards (TAM and broad SAM),
# four light support KPI cards, one no-fill findings rail, and no chart.

meta:
  slide_id: ddg-s03
  slide_order: 3
  module_name: executive_summary.py
  slide_type: body
  section: Answer
  archetype: kpi_answer_board_no_chart
  story_role: "Give the headline answer immediately after the primer: annual supplier TAM, broad SAM, the two-stream split, per-hull framing, and the average-annual convention."
  inputs:
    - TAM Build §5 (portfolio TAM, avg-annual, per-hull; DO-01)
    - TAM Build §5a (BC and AP/LLTM stream totals; CD02)
    - SAM Build §4a (broad component manufacturing scenario; CD08)
    - Executive Summary tab §1-§2 (headline KPIs + TAM bridge)
    - z_ChartData CD01_EXEC_KPIS, CD02_TAM_STREAM_SPLIT
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (TAM bridge behind the headline)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Answer
  title_topic: Executive Summary
  title_finding: DDG-51 supplier TAM averages ~$573M per year, with ~$327M per year in broad component SAM
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
    - DoW DDG-51 contract announcements, July 2022 to May 2026
    - SAM.gov Subaward Reporting Public API
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (2) DoW DDG-51 contract announcements, July 2022 to May 2026; (3) SAM.gov Subaward Reporting Public API"

story:
  objective: Give the answer up front while making clear the values are average-annual FY22-27 sizing conventions, not a steady run-rate or a capture forecast.
  do_not_say:
    - Do not call the ~$573M a steady annual run-rate.
    - Do not include SOM, win probability, or capture language.
    - Do not make cumulative values visually equal to annual values.
    - Do not sum TAM and SAM, or sum the SAM scenarios.
  known_caveats:
    - Average-annual convention smooths lumpy program timing; it is not a run-rate.
    - Broad SAM is a work-type scenario, not a probability-weighted opportunity.
    - Broad SAM excludes the ~42.9% unbucketed residual carried in TAM.

object_assessment:
  verdict: "Aggressive redesign: remove the small stream chart. An executive summary should answer, not add another exhibit to decode."
  object_contract:
    render_pattern: kpi_answer_board_no_chart
    expected_rendered_object_count: 9
    compound_objects: []
    required_focal_family: "Exactly two dark hero KPI cards: TAM and broad SAM. All support cards are light-fill with GRAY_3 borders."
  anti_repetition:
    versus_market_primer: "This is not a map."
    versus_cost_funnel: "This is not a chart. The next numerical slide earns the chart slot."
    forbidden_defaults:
      - No stream-split chart.
      - No funnel.
      - No Venn or bubble object.
      - No more than two dark cards.

regions:
  coord_basis: BODY
  layout_pattern: kpi_answer_board_no_chart
  qualifier_note: {x: 0%,  y: 0%,  w: 100%, h: 10%}
  hero_tam:       {x: 0%,  y: 14%, w: 48%,  h: 27%}
  hero_sam:       {x: right_of(hero_tam) + GAP, y: align_top(hero_tam), w: remaining, h: 27%}
  support_bc:     {x: 0%,  y: below(hero_tam) + GAP, w: 23%, h: 21%}
  support_ap:     {x: right_of(support_bc) + GAP, y: align_top(support_bc), w: 23%, h: 21%}
  support_share:  {x: right_of(support_ap) + GAP, y: align_top(support_ap), w: 23%, h: 21%}
  support_hull:   {x: right_of(support_share) + GAP, y: align_top(support_share), w: remaining, h: 21%}
  findings_rail:  {x: 0%, y: below(support_bc) + GAP, w: 100%, h: fit_content}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: note,    region: qualifier_note, prominence: tertiary,  paint_order: 1, content: no-fill convention qualifier; average annual not run-rate}
  - {id: e2, type: callout, region: hero_tam,       prominence: primary,   paint_order: 2, content: supplier TAM hero KPI card, tie_out: TAM Build §5 portfolio_tam / DO-01}
  - {id: e3, type: callout, region: hero_sam,       prominence: primary,   paint_order: 3, content: broad SAM hero KPI card, tie_out: SAM Build §4a broad / CD08}
  - {id: e4, type: callout, region: support_bc,     prominence: secondary, paint_order: 4, content: Basic Construction stream support KPI, tie_out: TAM Build §5a / CD02}
  - {id: e5, type: callout, region: support_ap,     prominence: secondary, paint_order: 5, content: AP and LLTM stream support KPI, tie_out: TAM Build §5a / CD02}
  - {id: e6, type: callout, region: support_share,  prominence: secondary, paint_order: 6, content: broad SAM share support KPI, tie_out: SAM Build §4a broad % of TAM / CD08}
  - {id: e7, type: callout, region: support_hull,   prominence: secondary, paint_order: 7, content: per-hull support KPI, tie_out: TAM Build §5d per_hull_tam}
  - {id: e8, type: rail,    region: findings_rail,  prominence: secondary, paint_order: 8, content: no-fill answer findings rail}
  - {id: e9, type: note,    region: note_strip,     prominence: tertiary,  paint_order: 9, content: standard sizing note}

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
    - shape: qualifier_1
      element: e1
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: MESSAGE_11PT, color: DK, font: FONT}
      note: "Use no fill/no border; reserve filled treatment for warning/scope-boundary notes only."
    - shape: hero_tam_1
      element: e2
      profile: primary_kpi_or_output_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: WHITE, font: FONT}
        - {role: value, size: ANSWER_KPI_24PT, bold: true, color: WHITE, font: FONT}
        - {role: qualifier, size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
      note: "Value line dominates; cumulative or qualifier line stays smaller than the annual value."
    - shape: hero_sam_1
      element: e3
      profile: primary_kpi_or_output_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: WHITE, font: FONT}
        - {role: value, size: ANSWER_KPI_24PT, bold: true, color: WHITE, font: FONT}
        - {role: qualifier, size: LABEL_9PT, italic: true, color: WHITE, font: FONT}
      note: "Value line dominates; cumulative or qualifier line stays smaller than the annual value."
    - shape: support_bc_1
      element: e4
      profile: support_kpi_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Support cards stay smaller than the two hero cards; do not use ANSWER_KPI_24PT here."
    - shape: support_ap_1
      element: e5
      profile: support_kpi_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Support cards stay smaller than the two hero cards; do not use ANSWER_KPI_24PT here."
    - shape: support_share_1
      element: e6
      profile: support_kpi_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Support cards stay smaller than the two hero cards; do not use ANSWER_KPI_24PT here."
    - shape: support_hull_1
      element: e7
      profile: support_kpi_card
      runs:
        - {role: cap, size: CAP_12PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Support cards stay smaller than the two hero cards; do not use ANSWER_KPI_24PT here."
    - shape: findings_rail_1
      element: e8
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."
    - shape: note_1
      element: e9
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts: []                  # deliberately no chart on the answer slide; streams appear as support cards

tables: []

shapes:
  - id: qualifier_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Answer convention: headline values are average annual FY22-27; cumulative values are secondary and shown only as context."
    meaning: No-fill qualifier; prevents TAM from being read as run-rate.
  - id: hero_tam_1
    element: e2
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    text: "SUPPLIER TAM
~$573M per year
($3.44B FY22-27)"
    meaning: Primary answer card; annual value dominates.
  - id: hero_sam_1
    element: e3
    factory: text_box
    fill: BLUE_4
    line_color: BLACK
    line_width: 19050
    insets: INSETS_ANSWER_CARD
    text: "BROAD SAM
~$327M per year
($1.96B FY22-27)"
    meaning: Second dark hero card; broad component manufacturing SAM, not SOM.
  - id: support_bc_1
    element: e4
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "BC STREAM
~$365M per year
~$2.19B cumulative"
    meaning: Stream split appears as support card instead of a chart.
  - id: support_ap_1
    element: e5
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "AP AND LLTM
~$208M per year
~$1.25B cumulative"
    meaning: Second stream support card; AP and LLTM remains visibly separate.
  - id: support_share_1
    element: e6
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "BROAD SAM SHARE
57.1% of TAM"
    meaning: Share card ties broad SAM back to the TAM denominator.
  - id: support_hull_1
    element: e7
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "PER HULL
~$265M supplier TAM
13 in-window hulls"
    meaning: Per-hull context; secondary to the two answer cards.
  - id: findings_rail_1
    element: e8
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    text:
      bullets:
        - {lead: "Answer:", body: "supplier TAM is ~$573M per year after non-GFE and MYP-corrected scope gates."}
        - {lead: "Serviceable menu:", body: "broad component SAM is the largest scenario at ~$327M per year."}
        - {lead: "Discipline:", body: "SAM is not SOM and the scenarios are never summed."}
    meaning: Findings rail replaces chart decoding with a short answer readout.
  - id: note_1
    element: e9
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing note.

images: []

commentary:
  visible:
    element: e1
    container: right_rail
    title: "Answer rail"
    bullets:
      - {lead: "TAM:", body: "~$573M per year across FY22-27, with cumulative values secondary."}
      - {lead: "SAM:", body: "broad component manufacturing is the largest serviceable scenario, not a capture forecast."}
      - {lead: "Streams:", body: "Basic Construction drives most of the TAM; AP and LLTM adds a second lumpy stream."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. The answer slide, immediately after the market primer (S02) and
      before scope (S04). It lands the portfolio supplier TAM, broad component SAM, two-stream
      split, per-hull framing, and the average-annual convention without re-arguing the
      denominator. The slides that follow defend scope, the cost funnel, the MYP correction,
      and the TAM build. [tie-out: Executive Summary tab §1-§2; TAM Build §5]

      THE CANONICAL HEADLINE (must be identical across the deck; verified against the workbook).
      Portfolio non-GFE DDG-51 supplier TAM ~$573M per year, ~$3.44B cumulative FY22-27. Built
      from two streams: Basic Construction supplier work ~$365M/yr (~$2.19B cumulative) and AP
      and LLTM supplier material ~$208M/yr (~$1.25B cumulative). Broad component manufacturing
      SAM ~$327M/yr (~$1.96B cumulative) = 57.1% of TAM. Per-hull: ~$265M supplier TAM per
      in-window hull across 13 in-window hulls (BC-only ~$169M per hull — distinct from the
      metal scenario ~$170M/yr; do not conflate). [tie-out: TAM Build §5/§5a/§5d; SAM Build §4a]

      HOW THE TAM IS BUILT (the bridge the A2 appendix expands). TAM = BC_base x BC_coeff +
      AP_LLTM_base x AP_coeff. BC stream: P-5c Basic Construction base (~$17.47B cumulative)
      x a 12.5% MYP-corrected BC supplier coefficient (other-US plus foreign POP share over the
      non-GFE BC corpus, with the $-redacted BIW/Ingalls MYP masters folded back at
      reconstructed POP). AP and LLTM stream: CY advance-procurement base x 80.0%
      ship-construction share (~$1.47B) x an 85.0% AP supplier coefficient (an Inputs
      assumption, since DDG advance procurement has no FFATA POP corpus to measure over) =
      ~$1.25B. The two streams add to the ~$3.44B headline. [tie-out: TAM Build §3a, §5;
      Inputs assumptions; appendix_tam_calculation A2]

      HOW TO READ THE NUMBERS. Annual values are the hero convention; cumulative values sit in
      parentheses or smaller text. The average-annual figure is cumulative TAM divided by six
      fiscal years — an average, NOT a steady run-rate (the award profile is lumpy across the
      window, e.g. the FY26 SCN base is anomalously low). Broad SAM is a serviceable work-type
      menu; it is never SOM, capture, win probability, or a revenue ramp, and the five SAM
      scenarios are overlapping cuts of TAM that must never be summed. Broad SAM (~$327M)
      already excludes the ~42.9% unbucketed/ambiguous residual (~$1.47B) that TAM carries.
      [tie-out: TAM Build §5d note "average, not a run-rate"; SAM Build §4b "not SOM"]

      WHY THE MYP CORRECTION MATTERS EVEN HERE. The single most important guardrail behind the
      headline coefficient is that the disclosed-only outside-yards POP reads ~87% (a redaction
      artifact, because the two yard-heavy MYP masters are $-redacted and excluded), while the
      MYP-corrected outside-yards POP is ~33%. The ~33% is the outside-yards POP share, NOT the
      12.5% BC supplier coefficient; never present the disclosed ~87% as the coefficient. The
      headline TAM uses the MYP-corrected figures throughout. [tie-out: TAM Build §3b/§4;
      Executive Summary tab note on the ~87% artifact]

      DENSITY GUIDANCE. Default is the two-hero KPI board + four support cards + findings rail +
      sizing note. To densify, add a cumulative second line inside the TAM/SAM cards, a stream
      cumulative annotation under the chart, or the per-hull BC-only figure (~$169M) to the
      hull card. Keep annual values visually dominant and keep the no-SOM note.
    density_modes:
      normal: {visible_bullets: 4, keep: [e1, e2, e3, e4, e5, e7, e8]}
      dense:  {add_bullets: 4, safe_containers: [findings_rail, note_strip, support_bc, support_ap], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Annual convention:"
        body: "Values are average annual FY22-27 (cumulative divided by six years), not a promised steady run-rate; the award profile is lumpy."
        evidence: TAM Build §5d note
        safe_container: note_strip
        density_trigger: Add if timing lumpiness is likely to confuse the audience.
      - priority: 2
        lead: "Cumulative view:"
        body: "Portfolio TAM is ~$3.44B cumulative; broad component SAM is ~$1.96B cumulative across FY22-27."
        evidence: TAM Build §5; SAM Build §4a
        safe_container: card_tam
        density_trigger: Add only as secondary card text.
      - priority: 3
        lead: "Stream split:"
        body: "Basic Construction (~$365M per year, ~$2.19B) contributes more than AP and LLTM (~$208M per year, ~$1.25B)."
        evidence: TAM Build §5a / CD02
        safe_container: stream_chart
        density_trigger: Add if the chart loses native value labels.
      - priority: 4
        lead: "No capture:"
        body: "Broad SAM is a scenario definition, not a capture forecast; SAM is a strict subset of TAM and the scenarios never sum."
        evidence: SAM Build §4b note
        safe_container: answer_rail
        density_trigger: Add if a reviewer asks for win probability.
      - priority: 5
        lead: "Per hull:"
        body: "~$265M supplier TAM per in-window hull across 13 hulls (BC-only ~$169M per hull) is a scale check, not a ship-by-ship forecast."
        evidence: TAM Build §5d
        safe_container: card_hull
        density_trigger: Add when presenting to a hull-count-oriented audience.
      - priority: 6
        lead: "Coefficient guardrail:"
        body: "The BC coefficient is 12.5% (MYP-corrected); the ~33% outside-yards POP is a different number, and the disclosed ~87% is a redaction artifact never used as the coefficient."
        evidence: TAM Build §3a/§3b/§4
        safe_container: answer_rail
        density_trigger: Add if a reviewer questions the BC coefficient.
      - priority: 7
        lead: "Residual is excluded:"
        body: "Broad SAM (~$327M) excludes the ~42.9% unbucketed/ambiguous residual (~$1.47B) that TAM carries; the model refuses to force it into a named bucket."
        evidence: SAM Build §2a (unbucketed_share_cell)
        safe_container: note_strip
        density_trigger: Add if a reader assumes broad SAM equals TAM.
      - priority: 8
        lead: "Scope exclusions:"
        body: "The sizing excludes GFE-heavy flows, WPN and OPN weapons procurement, sustainment and depot, and SOM."
        evidence: Methodology §3; Scope slide (S04)
        safe_container: answer_rail
        density_trigger: Add if this slide is used standalone.
      - priority: 9
        lead: "FFATA is a floor:"
        body: "The headline is modeled from budget and POP, not summed FFATA; visible first-tier flow is only ~15-20% of estimated yard-side outsourcing."
        evidence: wiki 05, 09; ffata_visibility_gap (S14)
        safe_container: note_strip
        density_trigger: Add if a reader assumes the headline is a sum of subawards.
    do_not_add:
      - SOM, win probability, capture rate, or capture dollars
      - a summed SAM and TAM total, or summed SAM scenarios
      - a claim that ~$573M is a steady annual run-rate
      - the disclosed ~87% POP presented as the BC coefficient
      - internal workbook tab names or chart IDs in the rendered sources

data_and_calculations:
  data_inputs:
    - {input: Portfolio supplier TAM, value: 573, unit: $M per year, cumulative: 3.44, cumulative_unit: $B, tie_out: TAM Build §5 portfolio_tam / DO-01, used_in: kpi_tam_1}
    - {input: Broad component SAM, value: 327, unit: $M per year, cumulative: 1.96, cumulative_unit: $B, share_of_tam: "57.1%", tie_out: SAM Build §4a broad / CD08, used_in: kpi_sam_1}
    - {input: Basic Construction stream TAM, value: 365, unit: $M per year, cumulative: 2.19, cumulative_unit: $B, tie_out: TAM Build §5a / CD02, used_in: support cards}
    - {input: AP and LLTM stream TAM, value: 208, unit: $M per year, cumulative: 1.25, cumulative_unit: $B, tie_out: TAM Build §5a / CD02, used_in: support cards}
    - {input: Supplier TAM per in-window hull, value: 265, unit: $M per hull, hulls: 13, tie_out: TAM Build §5d per_hull_tam, used_in: kpi_hull_1}
  calculations:
    - {name: Broad SAM share, formula: "broad SAM cumulative / portfolio TAM (~$1.96B / ~$3.44B)", output: "57.1%", used_in: kpi_share_1}
    - {name: Average annual TAM, formula: "cumulative TAM / 6 fiscal years", output: "~$573M/yr", used_in: kpi_tam_1}
    - {name: Per-hull supplier TAM, formula: "cumulative TAM / 13 in-window hulls", output: "~$265M/hull", used_in: kpi_hull_1}
  rounding_rules: Annual values round to whole $M on cards and chart labels; cumulative values round to two decimals in $B; share rounds to one decimal.
  reconciliation: Portfolio TAM equals Basic Construction stream plus AP and LLTM stream under the average-annual convention (~$365M + ~$208M = ~$573M/yr). SAM scenarios are overlapping cuts of TAM and are NOT expected to sum to TAM.

qa:
  guardrails:
    - Annual values are visually dominant; cumulative values are secondary.
    - Sizing note appears on the slide verbatim.
    - No SOM, win-probability, capture, or steady-run-rate language appears.
    - Stream chart does not compete with the KPI cards.
    - TAM and SAM are never summed; the disclosed ~87% POP is never shown as the coefficient.
  source_checks:
    - Sources are real external citations only (SCN justification books, DoW contract announcements, SAM.gov subaward API); no internal workbook, wiki, or chart-data IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
