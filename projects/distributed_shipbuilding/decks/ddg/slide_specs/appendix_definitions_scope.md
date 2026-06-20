# SlideSpec — DDG appendix_definitions_scope
# Appendix A1. Table-heavy denominator + scope ledger: a glossary-plus-guardrail that
# keeps total ship cost, SCN LI 2122, Basic Construction, AP and LLTM, FFATA-visible
# flow, supplier-addressable TAM, and SAM scenarios separate, and states the scope
# window, the in-scope PIID set, and the explicit exclusions. No chart.

meta:
  slide_id: ddg-a1
  slide_order: A1
  module_name: appendix_definitions_scope.py
  slide_type: appendix
  section: Appendix
  archetype: full_width_denominator_ledger
  story_role: Clarify the denominator stack and the scope gate before readers audit the model or compare TAM, SAM, SCN, and FFATA — a glossary and guardrail, not a new argument.
  inputs:
    - Scope Exclusions §1-§2 (records kept / excluded PIIDs by class; in-scope dollars and parent UEIs)
    - TAM Build §2-§5 (two-stream model: BC base, AP and LLTM base, supplier coefficients, portfolio TAM)
    - AP Bridge §3 (AP/EOQ line-level INCLUDE/EXCLUDE classification)
    - SAM Build §4a (scenario menus within TAM)
    - POP Corpus / POP Source Audit (gated, non-GFE, confirmed corpus the coefficients are measured over)
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (the supplier-addressable TAM these denominators build to)
    - ddg-a5   # appendix_ffata_limitations (why FFATA-visible flow is a floor, not the denominator)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Definitions and scope
  title_topic: Definitions and Scope
  title_finding: Total ship cost, SCN, Basic Construction, FFATA-visible flow, and supplier-addressable TAM each do a different job
  layout: slideLayout4
  sources:
    - U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c
    - FAR 52.204-10 and 48 C.F.R. Part 45
    - CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109
  source_line_exact: "Sources: (1) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-5c; (2) FAR 52.204-10 and 48 C.F.R. Part 45; (3) CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109"

story:
  objective: Make it impossible to confuse total ship cost, SCN LI 2122 spend, the Basic Construction base, FFATA-visible first-tier flow, and supplier-addressable TAM, and to state the FY2022-27 TAM window, the in-scope new-construction PIID set, and the explicit scope exclusions (Zumwalt, depot sustainment, WPN and OPN weapons, GFE, the IVECO contaminant).
  do_not_say:
    - Do not imply the deck is sizing total DDG-51 ship cost.
    - Do not use FFATA-visible flow as the market-size denominator.
    - Do not describe SAM as SOM or as a capture-weighted forecast.
  known_caveats:
    - FFATA-visible first-tier flow is useful evidence but structurally narrower than total supplier flow (a floor, not the denominator).
    - GFE-heavy prime flows remain visible for context but are excluded from the non-GFE supplier TAM.
    - The wiki uses an FY2018-2027 framing window; the TAM model window is FY2022-2027 (six years). State the TAM window here.

object_assessment:
  verdict: "Keep as a professional appendix ledger. Tighten it: one dominant native table, one no-fill scope rail, one boundary note."
  object_contract:
    render_pattern: glossary_ledger_plus_scope_guardrail
    expected_rendered_object_count: 4
    compound_objects: []
    required_focal_family: "Native table is dominant; any guardrail stays no-fill or a single muted strip."
  anti_repetition:
    appendix_rule: "Do not add charts or model-audit plumbing. This is a definitions appendix, not QA."
    forbidden_defaults:
      - No chart.
      - No workbook/figure-register table.

regions:
  coord_basis: BODY
  layout_pattern: full_width_denominator_ledger
  ledger:       {x: 0%, y: 0%, w: 100%, h: fit_content}              # dominant object, full BODY width
  scope_rail:   {x: 0%, y: below(ledger) + GAP, w: 100%, h: fit_content}
  note_strip:   {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: ledger,     prominence: tertiary,  paint_order: 1, content: external table title (no-fill text_box above the table)}
  - {id: e2, type: table,         region: ledger,     prominence: primary,   paint_order: 2, content: 7-row denominator ledger (definition / included / excluded / where used), tie_out: Scope Exclusions + TAM Build + SAM Build}
  - {id: e3, type: rail,          region: scope_rail, prominence: secondary, paint_order: 3, content: no-fill scope rail (window, in-scope PIID set, explicit exclusions, boundary cue)}
  - {id: e4, type: note,          region: note_strip, prominence: tertiary,  paint_order: 4, content: boundary cue that TAM is not total spend and SAM is not SOM}

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
    - table: denominator_ledger
      element: e2
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: title_1
      element: e1
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: scope_rail_1
      element: e3
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."
    - shape: note_1
      element: e4
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Use no fill/no border; reserve filled treatment for warning/scope-boundary notes only."

charts: []                   # NO chart — a denominator ledger, not a visual

tables:
  - id: denominator_ledger
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Denominator and scope ledger
      purpose: define        # what each denominator measures, what is in, what is out, where it is used
      reader_takeaway: Total ship cost, SCN LI 2122, Basic Construction, AP and LLTM, FFATA-visible flow, supplier-addressable TAM, and SAM scenarios serve different jobs and must not be conflated.
      row_order: total ship cost, SCN LI 2122, Basic Construction base, AP and LLTM base, FFATA-visible flow, supplier-addressable TAM, SAM scenarios
      highlight_rows: [Supplier-addressable TAM]
      guardrails:
        - TAM is not total ship cost.
        - FFATA-visible flow is evidence, not the market-size denominator.
        - SAM scenarios are not SOM and are not additive totals.
    render:
      table_skin: rule        # appendix glossary reads cleaner light; 1.5pt header rule carries it
      size: 850               # 8.5pt; dense appendix copy; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [1.7, 2.7, 2.3, 2.3, 1.7]   # Denominator / Definition / Included / Excluded / Where used
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l", "l", "l", "l"]      # text-heavy -> left align all
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size, min_row_h: 274320}
      rows:
        - ["Denominator", "Definition", "Included examples", "Excluded examples", "Where used"]
        - ["Total ship cost", "P-5c Total Ship Estimate by procurement year", "Basic Construction, Electronics, Ordnance, Plans, HM&E, Other", "WPN and OPN weapons, depot sustainment", "Cost funnel context only"]
        - ["SCN LI 2122", "DDG-51 Class Destroyer line item in the Navy SCN budget books", "DDG-51 Flight IIA and Flight III new construction", "DDG-1000 Zumwalt (LI 2119), cruiser modernization, depot repair", "Scope gate and schedule"]
        - ["Basic Construction base", "Prime construction layer flowing through BIW and Ingalls prime contracts", "Yard work and yard-side supplier work", "Navy-procured Aegis, SPY-6, Mk 41, Mk 45, LM2500, SEWIP", "BC stream TAM"]
        - ["AP and LLTM base", "Current-year advance procurement and long-lead material that is supplier-addressable", "Ship-construction EOQ and long-lead material after the non-GFE filter", "AWS EOQ, Other GFE, VLS and weapons AP", "AP and LLTM stream TAM"]
        - ["FFATA-visible flow", "First-tier subawards reported to FSRS and surfaced through SAM.gov", "Reportable first-tier subcontracts above the threshold", "Direct material, lower-tier subs, standing agreements, sub-threshold tail", "Evidence and bucket rules"]
        - ["Supplier-addressable TAM", "BC base times the BC supplier coefficient, plus AP and LLTM base times the AP coefficient", "Non-GFE new-construction supplier work away from the prime yards", "GFE, WPN and OPN weapons, sustainment, design-only, SOM and capture", "Headline market size"]
        - ["SAM scenarios", "Selected work-type bucket menus within TAM", "Broad, metal, electrical, modular, HM&E", "Unbucketed residual unless later classified, capture probability", "Where-to-play menu"]
      cell_fills:
        "(6,0)": BLUE_1        # supplier-addressable TAM row label — the headline denominator
      cell_bold:
        "(6,0)": true
      cell_text_colors: {}
      footnotes:
        - "Seven distinct denominators. Total ship cost and SCN context the scope; the headline market is supplier-addressable TAM after exclusions and coefficients."
    columns:
      - {name: Denominator, unit: name, tie_out: deck glossary}
      - {name: Definition, unit: text, tie_out: TAM Build §2-§5 / SAM Build §4a / FAR 52.204-10}
      - {name: Included examples, unit: text, tie_out: Scope Exclusions / AP Bridge §3}
      - {name: Excluded examples, unit: text, tie_out: Scope Exclusions §2 / wiki 01}
      - {name: Where used, unit: text, tie_out: deck figure register}

shapes:
  - id: title_1
    element: e1
    factory: text_box        # external table title (house exhibit-title pattern)
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Denominator and scope ledger, DDG-51 supplier TAM"
    meaning: Names the exhibit in the house 10pt italic title style above the table.
  - id: scope_rail_1
    element: e3
    factory: text_box        # no-fill scope rail (slide_guide -> no-fill commentary)
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    text:
      bullets:
        - {lead: "TAM window:", body: "FY2022 to FY2027 (six years); the wiki framing window is FY2018 to FY2027."}
        - {lead: "In scope:", body: "the DDG-51 new-construction PIID set, two prime yards plus the major GFE primes; 22,235 records, $13.8B FFATA-visible, 1,954 parent vendors."}
        - {lead: "Excluded:", body: "Zumwalt DDG-1000 (LI 2119, closed), DDG depot sustainment, WPN and OPN weapons (SM, ESSM, Tomahawk, CIWS), GFE combat-system content, and the IVECO Marine Corps Mk 110 contaminant."}
    meaning: States the TAM window, the in-scope PIID set, and the explicit scope exclusions in one rail.
  - id: note_1
    element: e4
    factory: text_box        # no-fill bottom boundary cue
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Boundary cue: the deck does not size total DDG-51 ship cost. It sizes non-GFE new-construction supplier work within Basic Construction and AP and LLTM. SAM is a strict subset of TAM, never SOM."
    meaning: Reinforces the denominator and SAM-not-SOM guardrail in one no-fill line.

images: []

commentary:
  visible:
    element: e3
    container: method_note
    title:
    bullets:
      - {lead: "Window:", body: "the supplier TAM is FY2022 to FY2027, six years."}
      - {lead: "Excluded:", body: "Zumwalt, depot sustainment, WPN and OPN weapons, and GFE are gated out; the IVECO Mk 110 PIID is a flagged contaminant."}
      - {lead: "Boundary:", body: "GFE-heavy prime flows stay visible as context; non-GFE supplier TAM is the sizing object."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix page is a glossary and guardrail, not a new
      argument. It answers the denominator and scope questions that otherwise interrupt the
      cost funnel, TAM build, SAM scenario, and FFATA visibility slides. Everything on it is
      definitional; no value here is newly computed. [tie-out: deck glossary; Scope Exclusions]

      THE CORE BOUNDARY. The deck does not size total DDG-51 ship spend. It sizes non-GFE
      new-construction supplier work within two streams: Basic Construction and AP and LLTM.
      Total ship cost (P-5c Total Ship Estimate, ~$2.7B per ship on recent FY23-25 vintages)
      and SCN LI 2122 provide scope and budget context, but the headline supplier-addressable
      TAM is ~$573M per year (~$3.44B cumulative FY22-27) after exclusions and coefficients.
      [tie-out: TAM Build §5; SCN Budget; wiki 02]

      THE DEFINITIONS (carried from the original wireframe, verified to the workbook).
      - Outsourced = any SCN new-construction dollar that flows to a firm other than the prime
        yard's own labor and overhead: first-tier (and lower-tier) subcontracts, GFE the Navy
        buys from separate primes, and lead-yard / design-agent engineering. [wiki 01]
      - Prime = the assembling yard of record on the SCN PIID (BIW Bath ME, Ingalls Pascagoula
        MS). DDG-51 is a two-yard competitive procurement: each hull is awarded to one yard on
        its own prime contract, so each yard's first-tier subaward tree is independently visible
        (no submarine-style invisible team-build partner). [wiki 01]
      - Subaward = a first-tier subcontract reported under FAR 52.204-10 to FSRS via SAM.gov,
        threshold $30,000 per action; lower-tier (a sub's sub) is not reportable. [FAR 52.204-10]
      - GFE = government-furnished equipment the Navy procures from a separate prime and ships to
        the yard (Aegis LM Moorestown, SPY-6 RTX Andover, Mk 41 VLS LM, Mk 45 gun BAE, LM2500
        GE, SEWIP NG). Outsourced from the SCN perspective but not a subaward of the yard; the
        supplier TAM targets the NON-GFE supplier-addressable layer. [FAR Part 45; wiki 01, 03]

      THE FOUR DENOMINATORS OF "OUTSOURCED" (wiki 01, the load-bearing distinction). (1)
      outsourced-from-the-prime-yard = the yard's first-tier subaward tree plus the larger unseen
      purchased-material / lower-tier layer; (2) outsourced-from-the-Navy/SCN = adds the GFE-prime
      flows; (3) outside-the-yards = measured directly per action from DoD-announcement POP
      percentages (the ~87% outside-both-yards headline lives here); (4) private-sector work
      outside the assembling yards = everything in (1) and (2) plus FFRDC/lab work outside SCN.
      The deck emphasizes (2) and (3); the supplier TAM is the non-GFE slice of (2).

      WHY FFATA IS SEPARATE (a floor, not the denominator). FFATA-visible first-tier subawards
      are observable evidence — they support supplier names, descriptions, bucket rules, and
      concentration — but they are NOT the full market denominator. Direct material booked as
      direct cost, lower-tier subcontracts, standing supplier agreements, and sub-threshold
      actions sit outside the visible first-tier record set. Visible first-tier yard-side flow is
      ~$2.73B cumulative vs an estimated yard-side outsourcing midpoint ~$13.57B (~20% visible);
      a recent-rate read is ~15% (~$286M/yr visible vs ~$1.8B/yr estimated). FFATA threshold
      $30,000; reporting lag 12-30 months. [tie-out: appendix_ffata_limitations (A5); wiki 05, 09, 12]

      WHY SAM IS SEPARATE FROM TAM. Supplier-addressable TAM is the modeled market; SAM scenarios
      are work-type menus selected from within TAM (broad, metal, electrical, modular, HM&E). SAM
      is a strict subset of TAM, never SOM, and applies no capture probability. The five scenarios
      are overlapping cuts of the same TAM and must never be summed. [tie-out: SAM Build §4a/b]

      THE EXPLICIT EXCLUSIONS (Scope Exclusions tab + wiki 01, 12, 16). The headline TAM gate
      (is_ddg_new_construction_tam) excludes: Zumwalt-class DDG-1000 (SCN LI 2119, three hulls all
      delivered, closed program; remaining flows are OPN-funded modernization); DDG depot
      sustainment (~$2.0B of ddg_repair across 23 records, plus BAE private ship-repair at San
      Diego / Jacksonville / Norfolk / Mayport); federal naval-shipyard depot work (Norfolk,
      Portsmouth, Pearl Harbor, Puget Sound — federal payroll, not outsourced); and WPN/OPN
      weapons (Standard Missile, ESSM, Tomahawk, CIWS — loaded aboard but funded from a different
      appropriation; including them double-counts). The Scope Exclusions tab classifies the
      excluded PIIDs into three blocks: IVECO (Marine Corps Mk 110 gun, PIID M67854-16-C-0006,
      ~$707M, a flagged FPDS-discovery contaminant, an Italian armored-vehicle maker, not a
      destroyer supplier), DDG-1000 / Zumwalt, and WPN/OPN weapons (ESSM + CIWS). [tie-out: Scope
      Exclusions §2a-c; wiki 01, 12]

      WHY ELECTRONICS AND ORDNANCE ARE GFE-HEAVY (kept visible, excluded from non-GFE TAM). On the
      FY24 vintage, Electronics (11.3%) + Ordnance (21.6%) = ~33% of total ship cost, and both are
      overwhelmingly Navy-procured GFE. That is the structural reason the supplier-TAM-relevant
      outside-yards flow is GFE-heavy, and the reason the deck keeps GFE flows visible for context
      while sizing only the non-GFE supplier-addressable work. [tie-out: SCN Budget §2; wiki 02, 03]

      BUILDER GUIDANCE. Keep this as one measured native table plus a no-fill scope rail and a
      no-fill boundary note. Wording stays plain: what each denominator measures, what is in, what
      is out, where it is used. Keep internal workbook tabs and research chapter names out of the
      source line (public sources only). Avoid a second dominant visual; the ledger is the slide.
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [scope_rail, note_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "TAM boundary:"
        body: "The headline excludes GFE, WPN and OPN weapons, depot sustainment, design-only work, SOM, and capture; it is non-GFE new-construction supplier work only."
        evidence: Scope Exclusions; TAM Build §5
        safe_container: note_strip
        density_trigger: Add if readers ask whether the estimate is total ship spend.
      - priority: 2
        lead: "Window discipline:"
        body: "The supplier TAM is FY2022 to FY2027 (six years); the wiki framing window is FY2018 to FY2027, so do not mix the two when quoting cumulative dollars."
        evidence: Inputs §1 (FY range 2022-2027); wiki 01
        safe_container: scope_rail
        density_trigger: Add if a reader quotes a cumulative figure against the wrong window.
      - priority: 3
        lead: "FFATA is a floor:"
        body: "Visible first-tier flow is ~$2.73B cumulative vs ~$13.57B estimated yard-side outsourcing (~20% visible); it supports evidence and bucket rules, not the denominator."
        evidence: appendix_ffata_limitations (A5); wiki 05, 09
        safe_container: scope_rail
        density_trigger: Add if the FFATA limitation appendix is omitted from the pack.
      - priority: 4
        lead: "Two streams:"
        body: "Supplier TAM = Basic Construction base x BC coefficient plus AP and LLTM base x AP coefficient; AP and LLTM is a second stream after GFE-heavy and weapons AP lines are excluded."
        evidence: AP Bridge §3; appendix_tam_calculation (A2)
        safe_container: ledger
        density_trigger: Add if the TAM-calculation appendix is not shown.
      - priority: 5
        lead: "SAM not SOM:"
        body: "SAM is a scenario menu inside TAM; it implies no capture probability and no forecasted revenue, and the five scenarios overlap and are never summed."
        evidence: SAM Build §4b
        safe_container: note_strip
        density_trigger: Add in a reader-facing appendix pack.
      - priority: 6
        lead: "SCN gate:"
        body: "SCN LI 2122 is the new-construction scope gate and schedule context, not the full Navy weapons universe; Zumwalt sits under the separate LI 2119."
        evidence: SCN Budget; wiki 01
        safe_container: ledger
        density_trigger: Add if reviewers conflate appropriations lines.
      - priority: 7
        lead: "GFE stays visible:"
        body: "Electronics plus Ordnance is ~33% of total ship cost (FY24) and overwhelmingly GFE; the model keeps it visible as context while excluding it from non-GFE TAM."
        evidence: SCN Budget §2; wiki 02, 03
        safe_container: scope_rail
        density_trigger: Add if Electronics or Ordnance questions dominate.
      - priority: 8
        lead: "IVECO contaminant:"
        body: "PIID M67854-16-C-0006 (Marine Corps Mk 110 gun, ~$707M, IVECO) was inadvertently pulled in during FPDS discovery and is excluded; it is a flagged cleanup item, not a destroyer supplier."
        evidence: Scope Exclusions §2a; wiki 12, 16
        safe_container: scope_rail
        density_trigger: Add in a dense model-audit version.
      - priority: 9
        lead: "In-scope set:"
        body: "89 prime PIIDs discovered, 22,235 in-scope records kept, ~$13.8B FFATA-visible cumulative across 1,954 unique parent vendor UEIs (FY2002-FY2026 action date)."
        evidence: Scope Exclusions §1; wiki 01
        safe_container: scope_rail
        density_trigger: Add when an audience asks how the corpus was bounded.
      - priority: 10
        lead: "Residual discipline:"
        body: "Unbucketed or ambiguous supplier evidence (~42.9% of TAM) is not forced into a named SAM bucket unless later classified."
        evidence: SAM Build §2a; bucket_rules appendix (A6)
        safe_container: ledger
        density_trigger: Add in a dense model-audit version.
      - priority: 11
        lead: "Source hygiene:"
        body: "Use public sources in the footer; keep workbook tabs and wiki chapter names in internal tie-outs only."
        evidence: SPEC_FORMAT source-clean rule
        safe_container: note_strip
        density_trigger: Add only for build-agent QA.
    do_not_add:
      - Any internal workbook tab, chart-data block, or research chapter in chrome.sources
      - Any capture, SOM, win-rate, or forecast language
      - A second visual panel that competes with the denominator ledger

data_and_calculations:        # definitional glossary — no derived numbers, only scope counts cited in reserve
  data_inputs: []
  calculations: []
  rounding_rules: No quantitative rounding required beyond existing labels; scope counts (22,235 records; 1,954 vendors; $13.8B) are stated as in Scope Exclusions §1.
  reconciliation: This is a denominator and scope glossary; it preserves distinctions rather than reconciling to one total. SAM is a strict subset of TAM, never SOM.

qa:
  guardrails:
    - Slide states that TAM is not total ship cost.
    - Slide states that FFATA-visible flow is evidence, not the market-size denominator.
    - Slide separates TAM and SAM from SOM or capture.
    - Scope exclusions name Zumwalt DDG-1000, depot sustainment, and WPN and OPN weapons; the TAM window is FY2022-2027.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal workbook tabs, chart IDs, or wiki chapters rendered.
    - Internal provenance (Scope Exclusions, TAM Build, AP Bridge, POP Corpus) appears only in meta.inputs, tie_out, and reserve evidence.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the ledger region width"
    - "ledger + scope rail + note all sit within BODY (size rows via estimate_row_heights)"
