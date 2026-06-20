# SlideSpec - submarines `tam_bridge` (deck slide 8)
# Shape-built formula bridge (no chart, no table): two input cards (Basic Construction
# base, applied BC supplier coefficient) multiply through a mathMultiply operator and an
# orthogonal merge bus into a cumulative portfolio TAM card, which divides by six model
# years into the focal average annual TAM card. A secondary subtraction-bridge strip and
# a strict-coefficient guardrail pin below. tables: [] and charts: [] are explicit.

meta:
  slide_id: subs-s8
  slide_order: 8
  module_name: tam_bridge.py
  slide_type: body
  section: TAM Build
  archetype: formula_bridge_with_guardrail
  story_role: Convert the ~$56.6B Basic Construction denominator into the headline ~$19.8B cumulative and ~$3.3B average annual TAM in one auditable bridge.
  inputs:
    - Chart Data CD_08_TAMBridge
    - TAM Build section 3a (per-stream supplier coefficients)
    - TAM Build section 4e (annualization + deck-bridge figures)
    - POP Source Audit (coefficient corpus support)
  related_appendix:
    - subs-a4   # appendix_coefficient_sensitivity

chrome:
  section: Market Sizing
  breadcrumb_topic: TAM Bridge Calculation
  title_topic: TAM Bridge
  title_finding: Applying the strict 35.0% coefficient yields ~$3.3B average annual TAM
  layout: slideLayout4
  sources:
    - U.S. Department of the Navy SCN Justification Books, Exhibit P-5c
    - U.S. DoD daily Contracts announcements
    - SAM.gov FFATA and FSRS records
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA and FSRS records"

story:
  objective: Show the exact bridge from Basic Construction base to cumulative TAM and average annual TAM, while preventing broader POP views or AP and LLTM from entering the headline math. Read it as a multiplication, not a sequence of cost removals.
  do_not_say:
    - Do not use the broader POP coefficient as the headline coefficient.
    - Do not add AP and LLTM to the Basic Construction base.
    - Do not present average annual TAM as a steady run-rate.
    - Do not introduce SAM or TAM/SAM circles here; this is a bridge, not a Venn diagram.
  known_caveats:
    - Applied coefficient is 35.0235% in the workbook (TAM Build section 3a) and displayed as 35.0% on the slide.
    - AP and LLTM additive base is $0 in the headline model; the secondary subtraction bridge ($56.647B minus $36.807B) is a check, not an independent waterfall.

regions:
  coord_basis: BODY
  layout_pattern: formula_bridge_with_guardrail
  # Two input cards top-left and top-right; mathMultiply operator centered between them
  # with a quiet caption; a wired bridge bus carries base and coefficient into the operator,
  # the operator into the centered cumulative card, and the cumulative card down into the
  # focal average-annual card; a divide-by-6 annotation labels the cumulative->annual link;
  # then a subtraction strip and guardrail.
  base_card:       {x: 6%, y: 6%, w: 30%, h: 20%}
  operator:        {x: 47%, y: 9%, w: 6%, h: fit_content}
  coeff_card:      {x: 64%, y: 6%, w: 30%, h: 20%}
  bridge_bus:      {x: 6%, y: 6%, w: 88%, h: 77%}   # spans the four wired links across the formula stack
  cumulative_card: {x: 29%, y: 34%, w: 42%, h: 19%}
  divide_anno:     {x: 71%, y: 53%, w: 14%, h: fit_content}   # labels the cumulative->annual link
  annual_card:     {x: 27%, y: 59%, w: 46%, h: 24%}
  bridge_strip:    {x: 0%, y: 85%, w: 100%, h: fit_content}
  note_strip:      {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: diagram, region: base_card, prominence: secondary, paint_order: 1, content: Basic Construction base input card, tie_out: CD_08_TAMBridge (cumulative_bc_base_cell)}
  - {id: e2, type: diagram, region: coeff_card, prominence: secondary, paint_order: 2, content: Applied BC supplier coefficient input card, tie_out: TAM Build section 3a bc_supplier_coeff_cell}
  - {id: e3, type: connector, region: operator, prominence: tertiary, paint_order: 3, content: mathMultiply operator AutoShape plus quiet caption}
  - {id: e4, type: connector, region: bridge_bus, prominence: tertiary, paint_order: 4, content: 4 enumerated bridge connectors (base->operator, coefficient->operator, operator->cumulative, cumulative->annual)}
  - {id: e5, type: chart_annotation, region: divide_anno, prominence: tertiary, paint_order: 5, content: divide-by-6 annotation on the cumulative->annual link}
  - {id: e6, type: diagram, region: cumulative_card, prominence: secondary, paint_order: 6, content: cumulative portfolio TAM output card, tie_out: CD_08_TAMBridge (cumulative_tam_cell)}
  - {id: e7, type: diagram, region: annual_card, prominence: primary, paint_order: 7, content: average annual TAM output card (focal hero), tie_out: CD_08_TAMBridge (avg_annual_tam_cell)}
  - {id: e8, type: note, region: bridge_strip, prominence: tertiary, paint_order: 8, content: secondary subtraction-check strip}
  - {id: e9, type: note, region: note_strip, prominence: tertiary, paint_order: 9, content: strict-coefficient and AP guardrail}


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
      - role: input cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: input value
        size: RIBBON_KPI_18PT
        color: DK
        font: FONT
        bold: true
      - role: input qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e2:
      text_runs:
      - role: input cap
        size: CAP_12PT
        color: WHITE
        font: FONT
        bold: true
      - role: input value
        size: RIBBON_KPI_18PT
        color: WHITE
        font: FONT
        bold: true
      - role: input qualifier
        size: FINEPRINT_8_5PT
        color: WHITE
        font: FONT
        italic: true
    e3:
      text_runs:
      - role: operator caption
        size: CONNECTOR_NOTE_8_5PT
        color: DK
        font: FONT
        italic: true
    e4:
      connector_text: none; connector labels, if rendered, use CONNECTOR_NOTE_8_5PT italic DK
    e5:
      text_runs:
      - role: connector annotation
        size: CONNECTOR_NOTE_8_5PT
        color: DK
        font: FONT
        italic: true
    e6:
      text_runs:
      - role: output cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: output value
        size: ANSWER_KPI_24PT
        color: DK
        font: FONT
        bold: true
      - role: output qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
    e7:
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
    e8:
      text_runs:
      - role: subtraction-check lead
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
      - role: subtraction-check body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e9:
      text_runs:
      - role: Guardrail lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: guardrail body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
  render_notes: []

charts: []                # NONE: this is a shape-built diagram, not a native chart -> no rId / table-fit checks
tables: []                # NONE: explicit design statement

shapes:
  - id: base_1
    element: e1
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    insets: INSETS_CARD
    text: |
      BASIC CONSTRUCTION BASE
      $56.647B
      FY2022-FY2027 P-5c
    meaning: First bridge input (cap CAP_12PT bold; value RIBBON_KPI_18PT bold; qualifier FINEPRINT_8_5PT italic, all DK; BLACK border at 1pt, formula family).
  - id: operator_1
    element: e3
    factory: text_box           # rendered as a mathMultiply AutoShape (prst=mathMultiply), not a typed glyph
    fill: BLACK
    line_color: BLACK
    insets: INSETS_DEFAULT
    text: ""                     # symbol shape, no text; quiet caption "multiplied by" sits just below
    meaning: Multiplicative bridge operator as a real AutoShape; caption uses CONNECTOR_NOTE_8_5PT italic DK.
  - id: coeff_1
    element: e2
    factory: text_box
    fill: BLUE_4
    line_color: BLACK
    insets: INSETS_CARD
    text: |
      APPLIED BC SUPPLIER COEFFICIENT
      35.0%
      strict, non-nuclear, yard-excluded
    meaning: Second bridge input (value WHITE on BLUE_4; BLACK border at 1pt, formula family); visually distinct from broader POP evidence.
  - id: bridge_bus_1
    element: e4
    factory: connector
    fill: null
    line_color: GRAY_3            # quiet GRAY_3 hairline wiring; no fill on a connector
    insets: INSETS_NONE
    from_to:
      # ONE compound connector object enumerating the 4 wired bridge links (count stated in element_inventory e4)
      - {n: 1, from: base_1,       to: operator_1,    label: "base into operator"}
      - {n: 2, from: coeff_1,      to: operator_1,    label: "coefficient into operator"}
      - {n: 3, from: operator_1,   to: cumulative_1,  label: "operator into cumulative"}
      - {n: 4, from: cumulative_1, to: annual_1,      label: "cumulative into annual (divide by six)"}
    meaning: Compound bridge bus wiring the formula as 4 enumerated GRAY_3 hairline arrows so base x coefficient = cumulative, then cumulative / 6 = annual reads as a wired bridge.
  - id: divide_anno_1
    element: e5
    factory: text_box
    fill: null
    line_color: null             # no-fill annotation rides the cumulative->annual link
    insets: INSETS_NONE
    text: "divide by 6"          # CONNECTOR_NOTE_8_5PT italic DK; labels link 4 of bridge_bus_1
    meaning: No-fill divide-by-6 annotation on the cumulative->annual connector (link 4 of bridge_bus_1); annualizes $19.840B over six model years.
  - id: cumulative_1
    element: e6
    factory: text_box
    fill: BLUE_2
    line_color: BLACK
    insets: INSETS_ANSWER_CARD
    text: |
      CUMULATIVE PORTFOLIO TAM
      $19.840B
      FY2022-FY2027
    meaning: Intermediate output before annualization (value ANSWER_KPI_24PT bold DK on BLUE_2; BLACK border at 1pt, formula family).
  - id: annual_1
    element: e7
    factory: text_box
    fill: BLUE_5
    line_color: BLACK
    line_width: 19050             # hero: thicker 1.5pt BLACK border; only dark hero on the slide
    insets: INSETS_ANSWER_CARD
    text: |
      AVERAGE ANNUAL TAM
      ~$3.307B
      FY2022-FY2027 model-period average
    meaning: Focal hero output of the slide (value HERO_32PT bold WHITE on BLUE_5; BLACK border at 1.5pt / line_width 19050).
  - id: bridge_strip_1
    element: e8
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_MESSAGE
    text: "Subtraction check: $56.647B BC base minus $36.807B prime, co-prime, and excluded share equals $19.840B TAM."
    meaning: Secondary subtraction check for waterfall-minded readers (GRAY_1 fill, GRAY_3 border); same result as the multiplication.
  - id: note_1
    element: e9
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Guardrail: Only the strict 35.0% BC coefficient feeds headline TAM; broader POP views are sensitivity."   # lead MESSAGE_11PT bold, body DENSE_BODY_10PT
    meaning: Guardrail against coefficient drift or double counting; broader distributed-production views stay in sensitivity.

commentary:
  visible:
    element: e9
    container: method_note
    title:
    bullets:
      - {lead: "Guardrail:", body: "Only the strict 35.0% Basic Construction coefficient feeds headline TAM; broader distributed-production views stay in sensitivity."}
    body_size: DENSE_BODY_10PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It follows the Basic Construction denominator slide (S07)
      and turns the $56.647B construction-contract base into the headline supplier TAM.
      It should feel like a calculator: base times coefficient equals cumulative TAM,
      then cumulative TAM divided by six years equals average annual TAM. The denominator
      came from the preceding slide; the supplier coefficient is the strict coefficient
      derived from place-of-performance evidence after excluding non-addressable streams,
      BPMI naval-nuclear, GFE, and prime-yard / co-prime-yard portions.

      CORE MATH. The model applies a strict 35.0235% Basic Construction supplier
      coefficient (TAM Build section 3a; displayed as 35.0%) to the $56.647B Basic
      Construction base. This produces $19.840B of cumulative portfolio TAM across
      FY2022-FY2027 ($56.647B x 35.0235% = $19.840B) and $3.307B average annual TAM
      ($19.840B / 6 = $3.307B). The secondary bridge is the same result expressed as a
      subtraction: $56.647B Basic Construction less $36.807B of prime, co-prime, and
      excluded share equals $19.840B TAM. In the workbook the removal figure is computed
      as cumulative BC base minus cumulative TAM, so the subtraction is a check on the
      multiplication, not an independent waterfall of cost removals.

      WHY THE COEFFICIENT IS STRICT. The POP evidence supports broader
      distributed-production views (the all-gated POP anchor is ~51.8%; an AP and LLTM
      reference coefficient is ~48.5%), but the headline coefficient is intentionally
      narrower because it is sizing non-nuclear supplier manufacturing opportunity rather
      than all work performed away from a yard. The strict coefficient is the
      dollar-weighted supplier + foreign share over the gated, in-scope, non-GFE BC-stream
      corpus, with BPMI naval-nuclear (GFE) dropped. This is why the model does not use a
      simplistic 50% or 60% outsourced-share assumption and why the final TAM is lower than
      a broad-distributed estimate. The coefficient detail is proven on S10 (Coefficient
      Evidence) and stress-tested in appendix A4 (coefficient sensitivity).

      AP AND LLTM GUARDRAIL. Advance procurement and long-lead-time material are
      supplier-heavy evidence, but the headline model sets the additive AP and LLTM base
      to $0 to avoid double counting against the Basic Construction boundary (supplier
      LLTM is already inside Basic Construction). This slide can mention that guardrail,
      but the full proof belongs on the AP and LLTM bridge slide (S11). The reference AP
      coefficient (~48.5%) is explanatory only because its base is $0.

      NOT A RUN-RATE. The final card is an average annual TAM across six model years, not
      a steady-state run-rate; the underlying base is lumpy (S07, S09 annual cadence).
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4, e5, e6, e7, e8, e9]}
      dense: {add_bullets: 3, safe_containers: [bridge_strip, note_strip, annual_card], allowed_font_step_down: ["MESSAGE_11PT -> DENSE_BODY_10PT", "LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "Exact coefficient:", body: "The workbook coefficient is 35.0235%, displayed as 35.0% on the slide; the displayed value is the dollar-weighted POP supplier share over the in-scope BC corpus.", evidence: "TAM Build section 3a (bc_supplier_coeff_cell)", safe_container: note_strip, density_trigger: "Add in a QA or appendix-style version."}
      - {priority: 2, lead: "Cumulative math:", body: "$56.647B x 35.0% = ~$19.840B cumulative TAM across FY2022-FY2027.", evidence: "CD_08_TAMBridge (cumulative_tam_cell)", safe_container: bridge_strip, density_trigger: "Add if arithmetic needs to be explicit."}
      - {priority: 3, lead: "Annual math:", body: "$19.840B divided by six fiscal years equals ~$3.307B average annual TAM.", evidence: "TAM Build section 4e (avg_annual_tam_cell)", safe_container: bridge_strip, density_trigger: "Add if the annualization is challenged."}
      - {priority: 4, lead: "Secondary bridge:", body: "$36.807B is the modeled prime, co-prime, and excluded share removed from the Basic Construction base; the subtraction is a check on the multiplication.", evidence: "CD_08_TAMBridge (removal_cell)", safe_container: bridge_strip, density_trigger: "Use for a waterfall-minded reader."}
      - {priority: 5, lead: "Strict boundary:", body: "The coefficient is narrower than the broader distributed-production evidence (~51.8% all-gated anchor) because it targets non-nuclear supplier manufacturing opportunity, not all distributed work.", evidence: "POP Source Audit; Coefficient Evidence (S10)", safe_container: note_strip, density_trigger: "Add for audiences who expect a higher outsourced share."}
      - {priority: 6, lead: "AP exclusion:", body: "AP and LLTM are evidence and context, not additive TAM inside this headline boundary; the additive AP base is confirmed $0 because supplier LLTM is already inside Basic Construction.", evidence: "AP and LLTM bridge (S11); TAM Build section 3a", safe_container: note_strip, density_trigger: "Add if AP or LLTM appears in nearby discussion."}
      - {priority: 7, lead: "No SOM:", body: "This is market opportunity sizing, not share capture, pricing realization, or win probability.", evidence: "Deck guardrails", safe_container: annual_card, density_trigger: "Add only if the slide is used as a standalone excerpt."}
      - {priority: 8, lead: "Not a run-rate:", body: "Average annual TAM is the six-year average across lumpy procurement timing, not a stable yearly market flow.", evidence: "Annual cadence (S09)", safe_container: note_strip, density_trigger: "Add when annual cadence is not shown afterward."}
      - {priority: 9, lead: "Base lineage:", body: "The $56.647B base is the cumulative FY2022-FY2027 P-5c Basic Construction (Virginia ~$36.3B plus Columbia ~$20.4B) carried in from the prior slide.", evidence: "TAM Build section 4e (cumulative_bc_base_cell); Basic Construction (wiki 04)", safe_container: bridge_strip, density_trigger: "Add when this slide is shown without S07."}
      - {priority: 10, lead: "Multiplication, not removals:", body: "Read the bridge as base times coefficient; the subtraction strip is the same answer for waterfall-minded viewers, not a separate set of independent cost removals.", evidence: "TAM Build section 4 (TAM = BC_base x BC_coeff)", safe_container: note_strip, density_trigger: "Add if a reviewer reads the strip as a standalone waterfall."}
    do_not_add:
      - broader POP coefficient as a headline multiplier
      - additive AP and LLTM dollars
      - capture share, SOM, or win probability
      - TAM and SAM circles or a Venn framing

data_and_calculations:
  data_inputs:
    - {input: Basic Construction base, value: 56.647, unit: $B, period: FY2022-FY2027, tie_out: CD_08_TAMBridge (cumulative_bc_base_cell), used_in: base_1}
    - {input: Applied BC supplier coefficient, value: 35.0235, unit: percent, period: FY2022-FY2027, tie_out: TAM Build section 3a (bc_supplier_coeff_cell), used_in: coeff_1}
    - {input: Removed prime co-prime and excluded share, value: 36.807, unit: $B, period: FY2022-FY2027, tie_out: CD_08_TAMBridge (removal_cell), used_in: bridge_strip_1}
    - {input: AP and LLTM additive base, value: 0.000, unit: $B, period: FY2022-FY2027, tie_out: TAM Build section 2a (include AP/LLTM stream = 0; ap_lltm_base in TAM), used_in: note_1}
  calculations:
    - {name: Cumulative portfolio TAM, formula: "$56.647B x 35.0235%", output: "$19.840B", used_in: cumulative_1}
    - {name: Average annual portfolio TAM, formula: "$19.840B / 6 fiscal years", output: "$3.307B", used_in: annual_1}
    - {name: Secondary subtraction bridge, formula: "$56.647B - $36.807B", output: "$19.840B", used_in: bridge_strip_1}
  rounding_rules: Display coefficient as 35.0%; display dollars to three decimals in $B on the formula cards; title rounds to ~$3.3B.
  reconciliation: Multiplicative and subtraction bridge both reconcile to $19.840B cumulative TAM and ~$3.307B average annual TAM (TAM Build section 5 checks - portfolio TAM = BC TAM + AP/LLTM TAM, and average annual x fiscal years = cumulative).

qa:
  guardrails:
    - The focal card is average annual TAM, not a steady-state run-rate.
    - The slide clearly states only the 35.0% Basic Construction coefficient feeds headline TAM.
    - AP and LLTM additive base is shown as $0 or excluded except as a guardrail; no AP dollars are added to the base.
    - The subtraction strip is labeled as a check, not presented as an independent waterfall.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN P-5c Justification Books, DoD daily Contracts announcements, SAM.gov FFATA and FSRS); no internal docs, workbook tabs, wiki chapters, or chart IDs rendered.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    # no charts or tables on this slide -> rId and table-fit checks do not apply
