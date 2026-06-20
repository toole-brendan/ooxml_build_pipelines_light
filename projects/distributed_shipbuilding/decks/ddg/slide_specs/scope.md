# SlideSpec — DDG scope
# Body slide 4. NO chart — a two-column in-scope / out-of-scope ledger (light table)
# plus a no-fill denominator boundary cue. Locks denominator discipline before the
# cost funnel and TAM build. A conceptual boundary, not a data table.

meta:
  slide_id: ddg-s04
  slide_order: 4
  module_name: scope.py
  slide_type: body
  section: Scope and Denominator
  archetype: two_column_scope_ledger
  story_role: Lock denominator discipline before the deck shows the cost funnel and TAM build; set the in-scope / out-of-scope boundary so later arguments are about magnitude, not definition.
  inputs:
    - Methodology §2-§3 (in/out of TAM; exclusions vocabulary)
    - Scope Exclusions tab (excluded PIIDs by class; contaminant cleanup)
    - wiki 01 (scope window; Zumwalt exclusion; four denominators)
    - SAM Build §2-§3 (bucket logic context only; no values shown)
  related_appendix:
    - ddg-a1   # appendix_definitions_scope (record counts, contaminant PIIDs, full audit)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Scope
  title_topic: Scope
  title_finding: The analysis sizes non-GFE new-construction supplier work, not total DDG spend
  layout: slideLayout4
  sources:
    - CRS RL32109, Navy DDG-51 and DDG-1000 Destroyer Programs
    - U.S. Navy FY2027 SCN Justification Book, LI 2122
    - FAR 52.204-10 and FAR Part 45
  source_line_exact: "Sources: (1) CRS RL32109, Navy DDG-51 and DDG-1000 Destroyer Programs; (2) U.S. Navy FY2027 SCN Justification Book, LI 2122; (3) FAR 52.204-10 and FAR Part 45"

story:
  objective: Prevent misinterpretation by defining the bounded market before any denominator or TAM math appears; the deck sizes non-GFE new-construction supplier work outside the two yards, not total ship cost.
  do_not_say:
    - Do not make GFE examples look like target opportunities; they are context and exclusions.
    - Do not introduce SOM or capture language.
    - Do not cite internal worksheet names in rendered sources.
    - Do not put model dollar values on this slide; it is a conceptual boundary.
  known_caveats:
    - FFATA is a visibility source, not the market definition.
    - Audit record counts from Scope Exclusions belong in the appendix, not on this main scope slide.
    - DDG-1000 is excluded as out of class (closed; OPN-funded modernization only).

object_assessment:
  verdict: "Keep, but sharpen: this is the boundary ledger, not a second ecosystem map or card board."
  object_contract:
    render_pattern: native_scope_ledger_plus_single_warning_rail
    expected_rendered_object_count: 3
    compound_objects: []
    required_focal_family: "One native house_table owns the page; the bottom warning rail is the only filled shape outside the table."
  anti_repetition:
    versus_market_primer: "No connectors, no nodes, no lane map."
    versus_cost_funnel: "No numeric bars or denominator chart here."
    forbidden_defaults:
      - No chart.
      - No model dollars.
      - No arrow/funnel motif.

regions:
  coord_basis: BODY
  layout_pattern: two_column_scope_ledger
  ledger:       {x: 10%, y: 3%,  w: 80%, h: 72%}
  boundary_cue: {x: 8%,  y: 80%, w: 84%, h: fit_content}

element_inventory:
  - {id: e1, type: table, region: ledger,       prominence: primary,  paint_order: 1, content: two-column in-scope and out-of-scope ledger, tie_out: Methodology §3; Scope Exclusions}
  - {id: e2, type: note,  region: boundary_cue, prominence: tertiary, paint_order: 2, content: no-fill denominator boundary cue}

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
  table_rules:
    - table: ledger_1
      element: e1
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: boundary_cue_1
      element: e2
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: MESSAGE_11PT, color: DK, font: FONT}
      note: "Short thesis or boundary sentence; keep no fill/no border."

charts: []

tables:
  - id: ledger_1
    element: e1
    role: primary
    factory: house_table
    semantic:
      table_name: Scope boundary ledger
      purpose: define
      reader_takeaway: The deck sizes non-GFE new-construction supplier work; it excludes total DDG spend, GFE-heavy flows, sustainment and depot, weapons procurement, DDG-1000, and contaminants.
      row_order: program scope, appropriation, Basic Construction, AP and LLTM, place-of-performance boundary
      highlight_rows: ["IN SCOPE"]
      guardrails:
        - GFE examples belong only in the out-of-scope column.
        - The slide is a scope boundary, not a data table; no model dollars.
        - Use commas and "and"; no visible slash or plus separators.
    render:
      table_skin: light       # scope boundary reads cleaner as a light two-column ledger
      size: 900               # 9.0pt (== LABEL_9PT); row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [1.0, 1.0]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["IN SCOPE\nsized in TAM and SAM", "OUT OF SCOPE\nnot in TAM"]
        - ["DDG-51 Flight IIA and Flight III new construction", "DDG-1000 Zumwalt (out of class, closed)"]
        - ["SCN Line Item 2122 appropriation", "WPN and OPN weapons procurement"]
        - ["Basic Construction supplier work", "Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, SEWIP, CIWS, and other GFE-heavy prime flows"]
        - ["AP and LLTM supplier-addressable material", "Sustainment, depot, ship repair, design-only, and MIB"]
        - ["Work performed away from BIW, Ingalls, GFE prime sites, and Navy-directed flows", "Contaminants such as the IVECO Mk 110 gun and Thales ESSM artifacts"]
      cell_fills:
        "(1,0)": BLUE_1
        "(2,0)": BLUE_1
        "(3,0)": BLUE_1
        "(4,0)": BLUE_1
        "(5,0)": BLUE_1
        "(1,1)": GRAY_1
        "(2,1)": GRAY_1
        "(3,1)": GRAY_1
        "(4,1)": GRAY_1
        "(5,1)": GRAY_1
      cell_bold: {}            # header row auto-bolds via house_table
      cell_text_colors: {}
      footnotes:
        - "Conceptual boundary; the appendix carries the in-scope and excluded record audit."
    columns:
      - {name: In scope, unit: text, tie_out: Methodology §2 (In TAM), formula: null}
      - {name: Out of scope, unit: text, tie_out: Methodology §3 / Scope Exclusions, formula: null}

shapes:
  - id: boundary_cue_1
    element: e2
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Boundary cue: total DDG spend, then non-GFE new-construction base, then supplier-addressable TAM, then the SAM work-type menu."
    meaning: Quiet no-fill cue beneath the ledger; summarizes the funnel without a new visual hierarchy. No visible arrows.

images: []

commentary:
  visible:
    element: e2
    container: method_note
    title: "Boundary cue"
    bullets:
      - {lead: "In scope:", body: "DDG-51 new-construction supplier work outside the two assembling yards and outside GFE-heavy Navy-procured prime flows."}
      - {lead: "Out of scope:", body: "total ship cost, visible subawards alone, sustainment and depot, weapons procurement, DDG-1000, and contaminants."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. The denominator-discipline slide, between the executive summary
      (S03) and the cost funnel. It establishes the market definition before the deck shows
      total ship cost, Basic Construction, GFE-heavy cost categories, and the MYP correction —
      so later debate is about magnitude, not what is being counted. [tie-out: Methodology §2-§3]

      FORMAL SCOPE. The deck sizes a bounded market: DDG-51 new-construction supplier work
      outside BIW and Ingalls and outside GFE-heavy Navy-procured prime flows. In scope:
      DDG-51 Flight IIA and Flight III new construction; the SCN Line Item 2122 appropriation;
      Basic Construction supplier work; AP and LLTM (advance procurement / long-lead /
      economic-order-quantity) supplier-addressable material; and work performed away from
      prime, co-prime, and GFE-controlled sites. The governing rule is that the award-action
      scope controls (entity and location are hints only). [tie-out: Methodology §2 governing
      rule; wiki 01 in-scope PIID set]

      EXCLUSIONS (and why each is out). (1) DDG-1000 Zumwalt — out of class; three ships
      procured under SCN LI 2119, all delivered, with only OPN-funded modernization remaining.
      (2) WPN and OPN weapons procurement — Standard Missile, ESSM, Tomahawk, and CIWS are
      funded through Weapons / Other Procurement, not SCN; including them double-counts a
      different appropriation, even when the weapons are loaded onto DDGs. (3) GFE-heavy prime
      flows — Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, SEWIP, CIWS — Navy-directed, not supplier
      new-construction work. (4) Sustainment, depot, ship repair, design-only, and MIB
      (industrial-base capacity). (5) Named contaminants: the IVECO Mk 110 gun (~$707M, a
      Marine Corps gun that surfaced as a phantom DDG vendor) and the Thales ESSM artifact
      (~$4.2B, NATO cost-share on a Raytheon WPN-funded PIID). Exclusions are applied ONCE:
      gated out of the POP corpus AND decremented in the bridge, and the validation tabs tie
      the two. [tie-out: Methodology §3; Scope Exclusions §1-§2]

      INTERNAL AUDIT (appendix only, NOT on this slide). Scope Exclusions records 15,720
      in-scope records kept, 6,515 out-of-scope records excluded, and 16 contaminant PIIDs
      removed after cleanup, leaving 1,554 unique in-scope parent UEIs. These counts support
      the appendix audit (A1) but do not belong on the main scope page, whose point is
      conceptual boundary discipline, not a data dump. [tie-out: Scope Exclusions §1;
      nc_scope_summary.json]

      WHY THE DENOMINATOR MATTERS. The cost funnel exposes four candidate denominators of
      "outsourced": (1) outsourced from each prime yard, (2) outsourced from the Navy/SCN
      perspective (adds GFE primes), (3) outside-the-yards measured per DoD-announcement action
      (the ~87% headline lives here, before MYP correction), and (4) all private work outside
      the yards. The deck's supplier TAM uses the non-GFE, MYP-corrected slice. Stating the
      boundary here keeps the audience from reading any single denominator as the TAM. [tie-out:
      wiki 01 four denominators]

      DENSITY GUIDANCE. Default is the five-row two-column ledger + a one-line boundary cue. To
      densify, split the contaminant row into IVECO and Thales lines, add a per-row "why
      excluded" micro-note, or surface the record-count audit as a small appendix-style badge
      (reviewer-facing only). Keep it light-skin and conceptual; never a data table.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2]}
      dense:  {add_bullets: 4, safe_containers: [boundary_cue, ledger], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "New construction only:"
        body: "The market is tied to DDG-51 new construction; sustainment, depot, and private ship repair are separate markets."
        evidence: Methodology §3; wiki 01 (sustainment out of scope)
        safe_container: boundary_cue
        density_trigger: Add when the slide is used without the cost funnel.
      - priority: 2
        lead: "GFE is context, not a target:"
        body: "Aegis, SPY-6, Mk 41 VLS, Mk 45, LM2500, SEWIP, and CIWS are context and exclusions, not target opportunities."
        evidence: Methodology §3; wiki 03
        safe_container: ledger
        density_trigger: Add if the out-of-scope column is shortened.
      - priority: 3
        lead: "Weapons are a different appropriation:"
        body: "WPN and OPN weapons procurement is excluded even when the weapons are later loaded onto DDGs; including them double-counts a different budget line."
        evidence: wiki 01 (WPN/OPN); Methodology §3
        safe_container: ledger
        density_trigger: Add to distinguish GFE from weapons.
      - priority: 4
        lead: "DDG-1000 is out of class:"
        body: "Zumwalt closed at three delivered ships under SCN LI 2119; only OPN-funded modernization remains, so it is out of the new-construction scope."
        evidence: wiki 01 (Zumwalt exclusion)
        safe_container: ledger
        density_trigger: Add if a reviewer asks why DDG-1000 is excluded.
      - priority: 5
        lead: "Named contaminants:"
        body: "The IVECO Mk 110 gun (~$707M, Marine Corps) and the Thales ESSM artifact (~$4.2B, WPN-funded) were removed as phantom DDG vendors."
        evidence: Methodology §3 (named contaminants); Scope Exclusions §2
        safe_container: ledger
        density_trigger: Add when splitting the contaminant row.
      - priority: 6
        lead: "FFATA role:"
        body: "Visible first-tier subawards are evidence, not the denominator; the market definition is set here, not by SAM.gov totals."
        evidence: wiki 01 (FFATA); Methodology §7
        safe_container: boundary_cue
        density_trigger: Add if readers ask why SAM.gov appears in later sources.
      - priority: 7
        lead: "Audit backup:"
        body: "Scope Exclusions records 15,720 kept and 6,515 excluded records and 16 contaminant PIIDs; these belong in the appendix audit, not the main scope page."
        evidence: Scope Exclusions §1; appendix_definitions_scope (A1)
        safe_container: boundary_cue
        density_trigger: Add only in a reviewer-facing audit variant.
      - priority: 8
        lead: "Award scope controls:"
        body: "An award is excluded when its scope is GFE, weapons, sustainment, depot, or design-only; entity and location are hints only."
        evidence: Methodology §3 governing principle
        safe_container: boundary_cue
        density_trigger: Add if a reviewer asks how exclusion is decided.
    do_not_add:
      - SOM or capture language
      - detailed PIID counts on the main slide (appendix only)
      - GFE examples in the in-scope column
      - internal workbook tabs or wiki chapters in rendered sources

data_and_calculations:
  data_inputs: []
  calculations: []
  rounding_rules: No model dollar values on this slide; the appendix carries the record-count audit.
  reconciliation: Scope definitions align to Methodology §2-§3, Scope Exclusions, and the wiki 01 in-scope PIID set; exclusions are applied once (gated out of POP and decremented in the bridge).

qa:
  guardrails:
    - The slide states non-GFE new-construction supplier work clearly in the title and in-scope column.
    - GFE examples appear only in the out-of-scope column.
    - No SOM or capture language appears; no model dollar values on the main slide.
    - DDG-1000 and WPN/OPN weapons are shown as out of scope with the right rationale.
    - No visible slash or plus separators; commas and "and" only.
  source_checks:
    - Sources are real external citations only (CRS RL32109, SCN justification book, FAR 52.204-10 and FAR Part 45); no workbook tabs, internal CSVs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the ledger region width"
    - "ledger bottom + boundary cue both sit within BODY (size rows via estimate_row_heights)"
