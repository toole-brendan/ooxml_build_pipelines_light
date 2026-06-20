# SlideSpec - submarines `appendix_definitions_and_scope` (appendix A1, deck slide 19)
# Glossary + boundary appendix: a dark-skin glossary/boundary matrix owns the page,
# a no-fill setup line sits above it, and a filled guardrail strip at the bottom makes
# the two load-bearing boundary rules unavoidable (No SOM is modeled; AP/LLTM additive
# base = $0). Definitions mirror the workbook Methodology tab §1 exactly so the appendix
# governs the same boundary the body deck uses.

meta:
  slide_id: subs-a1
  slide_order: A1               # appendix letter retained; renders as deck slide 19
  module_name: appendix_definitions_and_scope.py
  slide_type: appendix
  section: Appendix
  archetype: glossary_matrix_plus_guardrail_strip
  story_role: Give diligence readers the shared vocabulary and boundary rules behind the market-sizing model, so SAM is never read as SOM and AP/LLTM is never added to the headline.
  inputs:
    - Methodology tab section 1 (definitions) and section 4 (scope boundary)
    - Methodology tab section 5 (exclusion rules)
    - Scope and funnel framework (wiki 01): four denominators, 15 new-construction PIIDs, FY window
    - TAM Build (portfolio TAM, applied BC coefficient, AP/LLTM reference coefficient)
    - SAM Build (scenario SAM definition; unbucketed residual excluded from SAM)
    - SIB Excluded (DO-08 SIB exclusion total)
  related_appendix: []

chrome:
  section: Appendix
  breadcrumb_topic: Definitions and scope
  title_topic: Definitions and Scope
  title_finding: Key terms define the model boundary and prevent double counting
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy SCN Justification Books
    - FAR 52.204-10
    - FAR Part 45
  source_line_exact: "Sources: (1) U.S. Department of the Navy SCN Justification Books; (2) FAR 52.204-10; (3) FAR Part 45"

story:
  objective: Define TAM, SAM, SOM, Basic Construction, GFE and GFP, SIB, AP and LLTM, FFATA and FSRS, POP, and the supplier coefficient, and state plainly what is outside the model.
  do_not_say:
    - Do not imply SAM is SOM, capture share, win probability, or a revenue forecast.
    - Do not treat AP and LLTM as additive TAM under the current boundary; its additive base is $0.
    - Do not use MIB in visible text; use SIB.
    - Do not treat SIB capacity-development funding as current component delivery into hulls.
  known_caveats:
    - Definitions mirror the workbook Methodology tab and the main-deck boundary; this is an interpretation aid, not a legal glossary.
    - FFATA and FSRS are a named first-tier-vendor floor, not full supplier-layer coverage.
    - The outsourced layer can be measured against four distinct denominators (wiki 01); the headline uses the Navy/SCN and outside-the-prime-team views.

regions:
  coord_basis: BODY
  layout_pattern: glossary_matrix_plus_guardrail_strip
  # Vertical stack: a no-fill setup line, the glossary/boundary matrix filling the
  # middle, and a pinned guardrail strip above the sources footer.
  setup_line:      {x: 0%, y: 0%, w: 100%, h: NOTE_H}
  glossary_matrix: {x: 0%, y: below(setup_line), w: 100%, h: body_until(guardrail_strip)}
  guardrail_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: note,    region: setup_line,      prominence: tertiary,  paint_order: 1, content: no-fill scope-anchor setup line}
  - {id: e2, type: table,   region: glossary_matrix, prominence: primary,   paint_order: 2, content: glossary and boundary matrix (9 terms), tie_out: Methodology tab section 1 definitions}
  - {id: e3, type: callout, region: guardrail_strip, prominence: secondary, paint_order: 3, content: scope guardrail strip (No SOM; AP/LLTM additive base = $0)}


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
      - role: setup lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: setup body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e2:
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
    e3:
      text_runs:
      - role: guardrail cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: guardrail body
        size: MESSAGE_11PT
        color: DK
        font: FONT
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts: []

tables:
  - id: glossary_matrix_1
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Glossary and boundary matrix
      purpose: define
      reader_takeaway: "The same boundary governs the whole deck: a non-nuclear component supplier TAM inside P-5c Basic Construction, scenario SAM, no SOM, and zero additive AP and LLTM."
      row_order: model constructs first (TAM, SAM, Basic Construction), then exclusions (GFE and GFP, SIB), then the reference stream (AP and LLTM), then evidence sources (FFATA and FSRS, POP)
      highlight_rows:
        - TAM
        - SAM
        - Basic Construction
        - GFE and GFP
        - SIB
        - AP and LLTM
      guardrails:
        - SAM is not SOM and not capture share.
        - AP and LLTM additive base equals $0 under the current P-5c boundary.
        - GFE and GFP, SIB, prime and co-prime yard work, and depot work remain outside the component TAM boundary.
    render:
      table_skin: dark              # dark header band; group fills set per cell below
      size: 900                     # 9pt rows (LABEL_9PT); keep cell copy short for native row-fit
      column_widths:
        mode: ratio
        values: [1.2, 2.6, 1.4, 2.7]   # Term | Model role | Treatment | Guardrail
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: [l, l, l, l]
      row_h:
        fn: estimate_row_heights
        size_pt_from: size
        header_size_pt_from: size
        min_row_h: null
      rows:
        - ["Term", "Model role", "Treatment", "Guardrail"]
        - ["TAM", "Non-GFE, non-SIB new-construction supplier opportunity", "In model", "Inside P-5c Basic Construction; an opportunity ceiling, not a forecast"]
        - ["SAM", "Portion of TAM in targeted work-type buckets", "In model", "Scenario menu, not capture share or SOM"]
        - ["Basic Construction", "P-5c construction-contract denominator (GFE-free)", "In model", "Not total ship cost"]
        - ["GFE and GFP", "Government-furnished equipment and property", "Excluded", "Do not add to component TAM"]
        - ["SIB", "Submarine industrial base capacity grants and workforce funding", "Excluded", "Context only; not current component delivery"]
        - ["AP and LLTM", "Advance procurement and long-lead-time material reference stream", "Reference", "Additive base = $0; already inside Basic Construction"]
        - ["FFATA and FSRS", "First-tier subaward visibility under FAR 52.204-10", "Evidence", "Named-vendor floor, not the full supplier layer"]
        - ["POP", "Place-of-performance evidence", "Evidence", "Drives the supplier coefficient"]
      cell_fills:
        "(1,0)": BLUE_1     # TAM - counted construct
        "(2,0)": BLUE_1     # SAM
        "(3,0)": BLUE_1     # Basic Construction
        "(4,0)": GRAY_2     # GFE and GFP - excluded
        "(5,0)": GRAY_2     # SIB - excluded
        "(6,0)": GRAY_1     # AP and LLTM - reference
        "(7,0)": GRAY_1     # FFATA and FSRS - evidence
        "(8,0)": GRAY_1     # POP - evidence
      cell_bold:
        "(1,0)": true
        "(2,0)": true
        "(3,0)": true
        "(4,0)": true
        "(5,0)": true
        "(6,0)": true
        "(7,0)": true
        "(8,0)": true
      cell_text_colors: {}
      footnotes: []
    columns: []

shapes:
  - id: setup_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Scope anchor: these definitions mirror the model's Methodology boundary; they are an interpretation aid, not a new boundary."   # MESSAGE_11PT, bold lead-in
    meaning: Establishes that the glossary is an interpretation aid, not a separate model boundary.
  - id: guardrail_1
    element: e3
    factory: text_box
    fill: GRAY_2
    line_color: BLACK             # the one focal frame on this slide
    line_width: 19050             # 1.5pt focal guardrail-frame weight
    insets: INSETS_MESSAGE
    text: "NO SOM IS MODELED. SAM is a scenario menu, not capture share or revenue forecast. AP and LLTM additive base = $0."   # cap lead-in CAP_12PT, body MESSAGE_11PT
    meaning: Makes the two most important boundary rules unavoidable at the foot of the page.

images: []

commentary:
  visible:
    element: e3
    container: callout            # the guardrail strip is the visible commentary
    title: null
    bullets:
      - {lead: "Boundary:", body: "No SOM is modeled; AP and LLTM are reference evidence, not additive TAM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is appendix A1 (deck slide 19), the shared-vocabulary
      page for diligence readers. It defines the market-sizing terms used throughout the
      body deck and pins the model boundary: a non-nuclear component supplier TAM inside
      P-5c Basic Construction, plus scenario SAM built from work-type buckets, with GFE,
      SIB, prime and co-prime yard work, depot work, and SOM all outside the model. The
      definitions are taken verbatim in meaning from the workbook Methodology tab section 1
      so the appendix and the body deck cannot drift apart.

      THE DEFINITIONS (Methodology tab section 1).
      - TAM = non-GFE, non-SIB new-construction supplier opportunity, computed as BC base x
        supplier coefficient + AP/LLTM base x coefficient. It is an opportunity ceiling, not
        a forecast.
      - SAM = the portion of TAM in the targeted work-type buckets, shown as a scenario menu.
        No capture or win-probability haircut is applied, so SAM is not SOM.
      - SOM = the share that could realistically be won. It is NOT modeled here.
      - Basic Construction = P-5c construction-contract denominator (GFE-free); the headline
        TAM stream. Not total ship cost.
      - AP/LLTM = advance procurement / long-lead material; kept as a reference stream, but
        its additive base is $0 because supplier LLTM is already inside the Basic Construction
        base. Adding the P-10 gross would double-count.
      - GFE = government-furnished equipment and weapons; excluded from TAM. GFP is the FAR
        Part 45 umbrella term (FAR 52.245-1); the deck uses GFE in its narrow equipment sense.
      - SIB = submarine industrial base / capacity grants; excluded from SAM. (Older source
        files use MIB / Maritime Industrial Base; visible copy uses SIB.) SIB capacity
        pass-throughs such as BlueForge fund shipyard capacity and workforce, not construction
        outsourcing.
      - POP = place of performance; drives the supplier coefficient.
      - Supplier coefficient = dollar-weighted supplier-plus-foreign POP share, applied to each
        stream base. The applied BC coefficient is the strict non-nuclear value (~35.0%); the
        AP/LLTM reference coefficient (~48.5%) is not applied because that base is $0.

      THE LIVE FIGURES BEHIND THE WORDS (TAM Build, SAM Build, SIB Excluded). Cumulative
      portfolio TAM is ~$19.84B FY2022-FY2027 (~$3.31B average annual). Broad component-
      manufacturing SAM is ~$16.83B cumulative (~$2.81B average annual), 84.8% of TAM; the
      unbucketed / ambiguous residual is held in TAM but excluded from every scenario SAM.
      The Basic Construction base is ~$56.65B. SIB exclusion at the subaward level is ~$4.25B
      (BlueForge Alliance is the dominant pass-through, ~$4.17B cumulative FY2016-FY2025).
      None of these figures is rendered on this slide; they are the substance the definitions
      stand on.

      THE SCOPE BOUNDARY (Methodology tab section 4; wiki 01). In TAM: Basic Construction
      (non-GFE), supplier-addressable component procurement, work away from prime / co-prime /
      GFE sites, and eligible AP/LLTM/EOQ only if additive. Out of TAM: GFE / weapons /
      sensors / ordnance, SIB / industrial-base capacity grants, sustainment / depot /
      design-only work, prime and co-prime final-assembly yard work, and AP/LLTM already
      inside BC.

      THE FOUR DENOMINATORS OF "OUTSOURCED" (wiki 01). The outsourced question only has an
      answer once the denominator is named: (1) outsourced from GDEB - the share of GDEB's
      own prime contract paid to other firms; (2) outsourced from the Navy / SCN perspective -
      the SCN share flowing to firms other than the assembling yards, adding GFE primes; (3)
      outside-the-prime-team - measured per action from DoD daily contract announcements; (4)
      private-sector work outside the assembling yard. The headlines emphasize (2) and (3).

      SCOPE WINDOW AND THE 15 PIIDs (wiki 01). FPDS prime data uses an FY2018-FY2027
      signed-date window; FFATA subaward data an FY2016-FY2026 action-date window. The
      outsourced-flow analysis scopes to fifteen submarine new-construction prime-contract
      PIIDs spanning the two construction primes, four dollar-material GFE primes (BPMI,
      Lockheed Martin, BAE, Rolls-Royce), and the SIB layer routed through Columbia. Two
      depot/backfit PIIDs and three SIB pass-through parent entities are explicitly excluded.

      DENSITY GUIDANCE. Default is the setup line + glossary matrix + guardrail strip. To
      densify, add a second line to the guardrail strip or a context line under the matrix;
      keep cell copy short and the No-SOM rule visible at any density. Push detail to notes
      before shrinking below LABEL_9PT.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3]}
      dense:  {add_bullets: 3, safe_containers: [setup_line, guardrail_strip, glossary_matrix], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "SAM is not SOM:"
        body: "Scenario SAM sizes are serviceable-market cuts, not capture share, win probability, or a revenue forecast; no haircut is applied."
        evidence: Methodology tab section 2b (SAM framework); SAM Build broad-SAM note
        safe_container: guardrail_strip
        density_trigger: Add if a reviewer asks for SOM or capture share.
      - priority: 2
        lead: "AP and LLTM additive base = $0:"
        body: "Supplier LLTM is already inside the Basic Construction base, so adding the P-10 gross would double-count; AP/LLTM stays a reference stream."
        evidence: Methodology tab AP/LLTM note; AP Bridge (DO-57 additive base confirmed 0)
        safe_container: glossary_matrix
        density_trigger: Add if the AP and LLTM row needs more explicit wording.
      - priority: 3
        lead: "Applied vs reference coefficient:"
        body: "The applied BC supplier coefficient is the strict non-nuclear ~35.0%; the AP/LLTM reference coefficient ~48.5% is not applied because that base is $0."
        evidence: TAM Build section 3 (POP coefficients)
        safe_container: glossary_matrix
        density_trigger: Add for audiences focused on coefficient lineage.
      - priority: 4
        lead: "FFATA and FSRS are a floor:"
        body: "First-tier subawards reported under FAR 52.204-10 (over $30,000 per action) name a vendor floor, not the full supplier layer; lower tiers are not reportable."
        evidence: Scope and funnel framework (wiki 01); FAR 52.204-10
        safe_container: setup_line
        density_trigger: Add in a denser diligence appendix version.
      - priority: 5
        lead: "SIB, not MIB:"
        body: "Use SIB (Submarine Industrial Base) in all visible copy; capacity grants such as BlueForge fund shipyard capacity and workforce, not construction outsourcing, so they are excluded from SAM."
        evidence: Methodology tab SIB note; Scope and funnel framework (wiki 01)
        safe_container: glossary_matrix
        density_trigger: Add only if legacy MIB terminology surfaces in source notes.
      - priority: 6
        lead: "Four denominators of outsourced:"
        body: "The outsourced share depends on the denominator: from GDEB, from the Navy/SCN view, outside-the-prime-team, or outside the assembling yard; headlines use the Navy/SCN and outside-the-team views."
        evidence: Scope and funnel framework (wiki 01)
        safe_container: glossary_matrix
        density_trigger: Add when a reviewer questions which outsourcing number is meant.
      - priority: 7
        lead: "GFE vs GFP:"
        body: "GFP is the FAR Part 45 umbrella term; GFE is the narrow equipment sense (reactor plant, combat systems, sonar/EW) used throughout the deck, all outside the component TAM boundary."
        evidence: Scope and funnel framework (wiki 01); FAR Part 45
        safe_container: glossary_matrix
        density_trigger: Add if a reviewer conflates GFE and GFP.
      - priority: 8
        lead: "Scope window:"
        body: "FPDS prime data uses an FY2018-FY2027 signed-date window; FFATA subaward data an FY2016-FY2026 action-date window; the headline TAM is annualized over FY2022-FY2027."
        evidence: Scope and funnel framework (wiki 01); TAM Build annualization
        safe_container: setup_line
        density_trigger: Add for diligence audiences focused on the time basis.
      - priority: 9
        lead: "Fifteen new-construction PIIDs:"
        body: "Scope is fifteen submarine new-construction prime-contract PIIDs across two construction primes and four GFE primes; depot, overhaul, and backfit PIIDs are out of scope."
        evidence: Scope and funnel framework (wiki 01)
        safe_container: glossary_matrix
        density_trigger: Add if a reviewer asks which contracts underlie the denominator.
      - priority: 10
        lead: "Headline figures behind the words:"
        body: "TAM ~$19.84B cumulative (~$3.31B/yr); broad SAM ~$16.83B (~$2.81B/yr, 84.8% of TAM); Basic Construction base ~$56.65B; SIB exclusion ~$4.25B."
        evidence: TAM Build; SAM Build; SIB Excluded (DO-08)
        safe_container: glossary_matrix
        density_trigger: Add only if the audience has not seen the headline build.
      - priority: 11
        lead: "TAM is a ceiling:"
        body: "TAM is an opportunity ceiling, not a forecast; the model never claims any share will convert to revenue."
        evidence: Methodology tab TAM note
        safe_container: guardrail_strip
        density_trigger: Add if the audience reads TAM as a revenue projection.
      - priority: 12
        lead: "Residual stays in TAM, out of SAM:"
        body: "The unbucketed / ambiguous residual is held in portfolio TAM but excluded from every scenario SAM because it has no clean work-type bucket."
        evidence: SAM Build unbucketed note
        safe_container: glossary_matrix
        density_trigger: Add when shown alongside the bucket TAM or SAM scenarios slides.
    do_not_add:
      - TAM and SAM circles
      - capture share, win-probability, or SOM language
      - MIB terminology in visible copy
      - any rendered workbook tab name, figure ID (DO-xx), or wiki chapter

data_and_calculations:
  data_inputs: []
  calculations: []
  rounding_rules: No calculated figures are rendered on this slide; figures cited in reserve use $B to two decimals and whole percent.
  reconciliation: Definitions support the main model boundary; no numeric reconciliation is performed on-slide.

qa:
  guardrails:
    - Definitions match the workbook Methodology tab section 1 wording in meaning (TAM, SAM, SOM, BC, AP/LLTM, GFE, SIB, POP, supplier coefficient).
    - Keep definitions short enough for native table row-fit; push detail to reserve, not into cells.
    - Preserve the visible No-SOM rule and AP/LLTM additive base = $0 in the guardrail strip.
    - Use SIB, not MIB, in visible slide text.
    - In-scope constructs (TAM, SAM, Basic Construction) read blue; exclusions (GFE/GFP, SIB) gray; reference/evidence terms neutral.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN Justification Books, FAR 52.204-10, FAR Part 45); no workbook tabs, wiki chapters, or DO-xx figure IDs in any rendered field.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - "if a table exists: resolved column widths sum to its region width"
    # no chart on this slide -> chart rId checks do not apply
