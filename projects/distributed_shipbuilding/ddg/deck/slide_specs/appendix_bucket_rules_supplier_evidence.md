# SlideSpec — DDG appendix_bucket_rules_supplier_evidence
# Appendix slide A6. The bucket-to-scenario inclusion rulebook + per-bucket supplier evidence:
# one full-width measured table (seven named buckets + explicit residual) with a classification
# arbiter and scenario-membership cue. No chart (one measured native table).

meta:
  slide_id: ddg-a6
  slide_order: A6
  module_name: appendix_bucket_rules_supplier_evidence.py
  slide_type: appendix
  section: Appendix
  archetype: appendix_bucket_rules_table
  story_role: Provide the rulebook that maps visible subaward evidence into seven named work-type buckets and an explicit residual, with per-bucket supplier proof points and scenario-membership flags.
  inputs:
    - _taxonomy BUCKETS (seven buckets + description-keyword and NAICS-4 crosswalks + classify())
    - SAM Build §2/§3 bucket TAM and the unbucketed residual
    - Worktype Evidence §1 bucket map + §2 top vendors by bucket + §3 classification arbiter
    - Vendors tab data_vendors.tbl_ddg_top_vendors (parent-level lifetime visible flow)
    - extracted/nc_lifetime_vendors.csv (cleaned parent-level proof points)
    - inputs_scenarios scenario flags (metal, HM&E, electrical, modular, broad)
  related_appendix: []

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Bucket rules
  title_topic: Bucket Rules and Supplier Evidence
  title_finding: Description-led classification maps subawards into seven target work types, with an explicit residual
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - SAM.gov Entity Management API
    - FAR 52.204-10
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

story:
  objective: Show the rules that convert visible subaward evidence into work-type buckets, the per-bucket supplier proof points, the residual logic, and the SAM scenario-membership inputs.
  do_not_say:
    - Do not hide the residual inside broad component SAM.
    - Do not present top-vendor examples as exhaustive rankings; they are proof points and a floor.
    - Do not overstate NAICS precision; it is a fallback when descriptions are thin, not the work performed.
    - Do not source supplier evidence from z_ChartData CD09 (bucket-split; drops GFE and prime-named firms).
  known_caveats:
    - Vendor cleanup caveats matter; duplicate parent names and UEI variants can appear (Major Tool, Rolls-Royce).
    - The residual is a discipline feature, not a flaw to hide.
    - Supplier evidence is parent-level lifetime visible flow, not bucket-pure SCN-scope TAM.

object_assessment:
  verdict: "Keep as one full-width native rulebook table. This is exactly what tables are for: definitions, values, examples, and scenario flags."
  object_contract:
    render_pattern: full_width_bucket_rulebook_table_plus_classification_cue
    expected_rendered_object_count: 3
    compound_objects: []
    required_focal_family: "Rulebook table is primary; residual row is gray and explicit; cue stays no-fill."
  anti_repetition:
    appendix_rule: "Do not add logos or turn proof points into a supplier ranking chart."
    forbidden_defaults:
      - No chart.
      - No company logos.
      - Do not hide residual.

regions:
  coord_basis: BODY
  layout_pattern: appendix_bucket_rules_table
  table_title: {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  table:       {x: 0%, y: below(table_title), w: 100%, h: body_until(rule_cue)}
  rule_cue:    {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: table_title, prominence: tertiary, paint_order: 1, content: external table title}
  - {id: e2, type: table,         region: table,       prominence: primary,  paint_order: 2, content: bucket definitions, scale, supplier evidence, and scenarios table, tie_out: Worktype Evidence; SAM Build §2/§3}
  - {id: e3, type: note,          region: rule_cue,    prominence: tertiary, paint_order: 3, content: classification-arbiter and scenario-membership cue}

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
    - table: bucket_rules_1
      element: e2
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: table_title_1
      element: e1
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: rule_cue_1
      element: e3
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Lead/body paragraphs; keep no fill/no border and do not render as chips."

charts: []

tables:
  - id: bucket_rules_1
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Bucket definitions, scale, and supplier evidence
      purpose: define
      reader_takeaway: Seven named buckets are classified by description, vendor override, then NAICS fallback; the residual (~42.9% of TAM) stays explicit and outside broad SAM until evidence supports assignment.
      row_order: structural, machining, castings, piping, electrical, HVAC, coatings, residual
      highlight_rows: ["Unbucketed / ambiguous residual"]
      guardrails:
        - The residual stays explicit and is not hidden in broad component SAM.
        - Scenario membership must match the scenario flags exactly.
        - Supplier evidence is parent-level (Vendors tab), not bucket-split CD09.
    render:
      table_skin: rule
      size: 850
      column_widths:
        mode: ratio
        values: [1.7, 2.8, 1.2, 1.2, 2.5, 1.4]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l", "r", "r", "l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Bucket", "Inclusion rule", "Avg annual", "FY22-27 cum.", "Supplier evidence", "Scenarios"]
        - ["Structural fab and pre-outfit", "Hull sections, fabricated structural metal, deckhouse, pre-outfit modules", "~$101M", "~$608M", "Major Tool and Machine; Superior Electromechanical; Leonardo via DRS", "metal, modular, broad"]
        - ["Machining", "Machine shops, precision machining, mechanical power transmission", "~$66M", "~$394M", "Major Tool and Machine; Rolls-Royce; Timken Gears and Services", "metal, HM&E, broad"]
        - ["Castings and forgings", "Iron and steel forging, steel foundries, cast components", "~$3M", "~$16M", "Ellwood Group", "metal, broad"]
        - ["Piping, valves, and pumps", "Industrial valves, pumps, manifolds, pipe and fittings, hydraulics", "~$13M", "~$78M", "Curtiss-Wright; CIRCOR; Leslie Controls (vendor overrides)", "HM&E, broad"]
        - ["Electrical and power", "Switchgear, switchboards, cable, generators, motors, power distribution", "~$132M", "~$791M", "Leonardo via DRS; General Electric; DRS Naval", "electrical, broad"]
        - ["HVAC and ventilation", "Air-conditioning, chilled water, warm-air heating, shipboard ventilation", "~$10M", "~$59M", "Johnson Controls Navy Systems", "HM&E, broad"]
        - ["Coatings and insulation", "Coatings, paint, deck covering, insulation, rubber and synthetic", "~$3M", "~$17M", "M.S.M. Industries; Espey Mfg. and Electronics", "modular, broad"]
        - ["Unbucketed / ambiguous residual", "Insufficient description, ambiguous scope, or evidence too thin to classify; do not force-classify", "~$246M", "~$1.47B", "Held explicit; not assigned to a named bucket", "excluded from broad"]
      cell_fills:
        "(8,0)": GRAY_2
        "(8,1)": GRAY_2
        "(8,2)": GRAY_2
        "(8,3)": GRAY_2
        "(8,4)": GRAY_2
        "(8,5)": GRAY_2
      cell_bold:
        "(8,0)": true
        "(8,2)": true
        "(8,3)": true
        "(8,5)": true
      cell_text_colors: {}
      footnotes:
        - "Classification arbiter: description keyword, then vendor override, then NAICS-4 fallback, then residual."
        - "Broad component manufacturing is the seven named buckets (~57.1% of TAM), not the residual. Avg annual = FY22-27 cumulative divided by six."
    columns:
      - {name: Bucket, unit: text, tie_out: _taxonomy BUCKETS, formula: null}
      - {name: Inclusion rule, unit: text, tie_out: _taxonomy BUCKETS definition + DESC_BUCKET keywords, formula: null}
      - {name: Avg annual, unit: $M per year, tie_out: SAM Build §3 bucket TAM / 6, formula: "cumulative divided by six"}
      - {name: FY22-27 cum., unit: $M, tie_out: SAM Build §3 bucket TAM, formula: "portfolio TAM x modeled bucket share"}
      - {name: Supplier evidence, unit: text, tie_out: Vendors tab / nc_lifetime_vendors.csv; Worktype Evidence §2, formula: null}
      - {name: Scenarios, unit: text, tie_out: inputs_scenarios scenario flags, formula: null}

shapes:
  - id: table_title_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Bucket definitions, scale, and supplier evidence"
    meaning: External table title; no-fill title box above the table.
  - id: rule_cue_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text:
      paragraphs:
        - {lead: "Arbiter:", body: "description keyword, then vendor override, then NAICS-4 fallback, then residual."}
        - {lead: "Scenarios:", body: "broad component manufacturing is the seven named buckets; the residual is excluded until evidence assigns a named bucket."}
    meaning: Bottom cue summarizing the classification arbiter and the broad-SAM residual exclusion.

images: []

commentary:
  visible:
    element: e3
    container: table_note
    title: Classification arbiter
    bullets:
      - {lead: "Order:", body: "Description keyword first, then known-vendor override, then NAICS-4 fallback, then residual."}
      - {lead: "Residual:", body: "Shown explicitly and excluded from broad SAM until better evidence assigns a named bucket."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS APPENDIX SITS. This page is the evidence bridge from visible subaward
      descriptions and supplier names to the seven named work-type buckets used in the SAM
      scenarios; it backs the SAM taxonomy, work-type allocation, SAM scenarios, supplier
      landscape (ddg-s13), and implications slides. It carries both the classification rulebook
      and the per-bucket supplier proof points. [tie-out: _taxonomy; SAM Build §2-§4; supplier_landscape (ddg-s13)]

      CLASSIFICATION RULE (the description-led arbiter; _taxonomy.classify()). DDG bucketing is
      DESCRIPTION-led (unlike the submarine workbook, which is NAICS/vendor-led). Precedence:
      (1) prime / co-prime name (BIW, GD, Ingalls) -> role prime/co_prime, dropped from supplier
      base; (2) GFE/MIB name (Lockheed, Raytheon, BAE Land, Northrop Grumman Systems, L3Harris)
      -> role gfe_mib, dropped; (3) description keyword on the award (e.g. "valve" -> piping,
      "switchgear" -> electrical) - the PRIMARY signal; (4) vendor-name override for known
      specialty vendors (Curtiss-Wright/CIRCOR/Leslie Controls -> piping, Fairbanks Morse ->
      machining, DRS Naval/L-3 Marine -> electrical, Rolls-Royce -> machining); (5) NAICS-4
      crosswalk when the description is thin (e.g. 3329 -> piping, 3327/3336 -> machining,
      3353/3344/3359/3364 -> electrical, 3334 -> hvac); (6) service-NAICS -> role service; (7)
      residual when evidence is insufficient (incl. holding-co NAICS 5511). The residual is held
      explicit to avoid forcing ambiguous dollars into target buckets. [tie-out: _taxonomy DESC_BUCKET, NAICS4_BUCKET, VENDOR_BUCKET_OVERRIDES]

      BUCKET SCALE (SAM Build §3; portfolio TAM x modeled bucket share over the ~$3.44B portfolio).
      Electrical and power is the largest named bucket at ~$131.8M/yr, ~$791.0M cumulative, 23.0%
      of TAM. Structural fab and pre-outfit is second at ~$101.4M/yr, ~$608.4M, 17.7%. Machining
      ~$65.6M/yr, ~$393.6M, 11.4%. Piping, valves, and pumps ~$13.0M/yr, ~$78.2M, 2.3%. HVAC and
      ventilation ~$9.9M/yr, ~$59.3M, 1.7%. Coatings and insulation ~$2.8M/yr, ~$17.1M, 0.5%.
      Castings and forgings ~$2.7M/yr, ~$16.2M, 0.5%. The seven named buckets sum to ~$1,963.8M
      cumulative (~57.1% of TAM = the broad component-manufacturing scenario). Unbucketed /
      ambiguous residual is ~$245.8M/yr, ~$1,474.8M cumulative, 42.9% of TAM - the model refuses
      to force it into a named bucket. [tie-out: SAM Build §2a/§3b]

      SUPPLIER EVIDENCE - PARENT-LEVEL, NOT CD09 (the load-bearing source decision). Tie the
      supplier proof points to the parent-level Vendors tab (data_vendors.tbl_ddg_top_vendors,
      driven by nc_lifetime_vendors.csv), NOT z_ChartData CD09. CD09 is bucket-split (one row per
      vendor/UEI/role/bucket), reports per-bucket exposure rather than parent lifetime totals, and
      its role=="supplier" filter DROPS any GFE/MIB-named or prime-named firm - so it answers a
      different question. Canonical parent-level proof points (lifetime visible flow, a FLOOR):
      Leonardo SpA via DRS ~$1,810M (Mk 41 VLS canister/launcher-cell module work, Aegis hardware,
      CEC; foreign parent, U.S. work location); Major Tool and Machine ~$816M (Indianapolis
      large-precision machining of the Mk 41 VLS launcher-cell module - the clean physical-machining
      proof; +~$132M second filer UEI -> ~$948M consolidated); Rolls-Royce ~$257M (+~$55M ->
      ~$312M; gas-turbine/mechanical power -> machining override); Timken Gears and Services ~$169M
      (main reduction gears -> machining); General Electric ~$336M (LM2500 propulsion -> electrical/
      power); Johnson Controls Navy Systems ~$178M (HVAC, NAICS 3334); Superior Electromechanical
      ~$146M and Merrill Tool ~$96M (Mk 41 VLS machining); Ellwood Group ~$49M (forgings/castings);
      M.S.M. Industries ~$42M and Espey Mfg. and Electronics ~$49M (coatings/insulation). Top-25
      parents ~53% of the ~$13.84B visible in-scope flow; top-10 ~34%. [tie-out: nc_lifetime_vendors.csv; wiki 06]

      SUPPLIER-EVIDENCE CAVEATS. Examples are proof points and a visible floor, not exhaustive
      rankings or a target list. Some parents blend roles (Leonardo is foreign-parented but works
      at U.S. DRS sites; GD is prime-affiliated). Clean duplicate filer UEIs before charting (Major
      Tool ~$816M + ~$132M; Rolls-Royce ~$257M + ~$55M; CAES = Cobham AES, do not double-list).
      NAICS lookup has a ~35% not-found rate on the top-150 pool (~$2.28B unclassified), and NAICS
      is a corporate-primary code, not the work performed - which is exactly why description leads
      and NAICS is only a fallback. [tie-out: wiki 06; entity_naics_lookup.csv]

      SCENARIO MEMBERSHIP (inputs_scenarios flags; overlapping cuts of TAM, NOT additive).
      Structural -> metal, modular, broad. Machining -> metal, HM&E, broad. Castings and forgings
      -> metal, broad. Piping, valves, and pumps -> HM&E, broad. Electrical and power -> electrical,
      broad. HVAC and ventilation -> HM&E, broad. Coatings and insulation -> modular, broad. The
      residual is excluded from broad component SAM unless future evidence assigns it to a named
      bucket. The scenario rollups: metal ~$170M/yr (structural+machining+castings), electrical
      ~$132M/yr (electrical alone), modular ~$104M/yr (structural+coatings), HM&E ~$89M/yr
      (machining+piping+HVAC), broad ~$327M/yr (all seven). [tie-out: SAM Build §4a; inputs_scenarios]

      BUILDER GUIDANCE. One full-width measured native table; no chart. This is the appendix slide
      most likely to overflow - use estimate_row_heights and keep the supplier-evidence column to
      ~3 names per row. Keep visible bucket labels plain ("Electrical and power", "Piping, valves,
      and pumps"); the only slash kept is the canonical "Unbucketed / ambiguous" residual label.
      Make the residual row visually distinct (gray) but not alarming.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2, e3]}
      dense:  {add_bullets: 5, safe_containers: [rule_cue, table], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT", "900 -> 850"]}
    approved_extra_points:
      - priority: 1
        lead: "Residual discipline:"
        body: "The ~$246M per year (~$1.47B, 42.9% of TAM) residual is shown explicitly and kept outside broad SAM until evidence supports assignment."
        evidence: SAM Build §2a/§3b
        safe_container: rule_cue
        density_trigger: Add if the residual row is visually compressed.
      - priority: 2
        lead: "Electrical leads:"
        body: "Electrical and power is the largest named bucket at ~$132M per year, ~$791M cumulative, 23.0% of TAM."
        evidence: SAM Build §3b
        safe_container: table
        density_trigger: Add as a small badge if the table title has spare room.
      - priority: 3
        lead: "Structural second:"
        body: "Structural fab and pre-outfit is second at ~$101M per year, ~$608M cumulative; in the metal, modular, and broad scenarios."
        evidence: SAM Build §3b; inputs_scenarios
        safe_container: table
        density_trigger: Add if the scenarios column is removed.
      - priority: 4
        lead: "Parent-level, not CD09:"
        body: "Supplier evidence is the parent-level Vendors tab; CD09 is bucket-split and drops GFE and prime-named firms, so it answers a different question."
        evidence: data_vendors; nc_lifetime_vendors.csv
        safe_container: rule_cue
        density_trigger: Add if a reviewer asks where the supplier names come from.
      - priority: 5
        lead: "Machining proof:"
        body: "Major Tool and Machine ~$816M (Mk 41 VLS launcher-cell machining) is the clean physical-machining proof point; a second filer UEI adds ~$132M (~$948M consolidated)."
        evidence: nc_lifetime_vendors.csv; wiki 06
        safe_container: table
        density_trigger: Add when the audience focuses on physical-component suppliers.
      - priority: 6
        lead: "Arbiter order:"
        body: "Descriptions outrank vendor overrides, which outrank NAICS-4 fallback; the residual wins when evidence is insufficient."
        evidence: _taxonomy.classify(); Worktype Evidence §3
        safe_container: rule_cue
        density_trigger: Add if the rule cue expands to two lines.
      - priority: 7
        lead: "Concentration:"
        body: "Top-25 parents ~53% of the ~$13.84B visible in-scope flow; top-10 ~34%, moderately concentrated."
        evidence: wiki 06 (concentration)
        safe_container: rule_cue
        density_trigger: Add for an audience sizing supplier concentration.
      - priority: 8
        lead: "NAICS is a fallback:"
        body: "~35% of top-150 vendors return no NAICS (~$2.28B unclassified), and NAICS is a corporate-primary code, not the work performed; description leads."
        evidence: wiki 06; entity_naics_lookup.csv
        safe_container: rule_cue
        density_trigger: Add if readers question NAICS-driven bucket assignment.
      - priority: 9
        lead: "Vendor cleanup:"
        body: "Clean duplicate filer UEIs before charting (Major Tool, Rolls-Royce) and reconcile CAES with Cobham AES so they are not double-listed."
        evidence: nc_lifetime_vendors.csv
        safe_container: rule_cue
        density_trigger: Add for a reviewer-facing audit version.
      - priority: 10
        lead: "Scenario cue:"
        body: "Broad component manufacturing is all seven named buckets (~57.1% of TAM); the residual is excluded; scenarios are overlapping cuts, not additive."
        evidence: SAM Build §4a; inputs_scenarios
        safe_container: rule_cue
        density_trigger: Add if the table drops the scenarios column.
    do_not_add:
      - the residual hidden inside broad SAM
      - exhaustive-ranking language for the vendor examples
      - supplier evidence sourced from z_ChartData CD09
      - internal workbook tabs or chart IDs in the rendered sources
      - unmeasured row heights; the table must use estimate_row_heights
      - any visible slash separator except the canonical "Unbucketed / ambiguous" label

data_and_calculations:
  data_inputs:
    - {input: Electrical and power, value: 131.8, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 791.0; 23.0% of TAM), used_in: bucket_rules_1}
    - {input: Structural fab and pre-outfit, value: 101.4, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 608.4; 17.7%), used_in: bucket_rules_1}
    - {input: Machining, value: 65.6, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 393.6; 11.4%), used_in: bucket_rules_1}
    - {input: Piping, valves, and pumps, value: 13.0, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 78.2; 2.3%), used_in: bucket_rules_1}
    - {input: HVAC and ventilation, value: 9.9, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 59.3; 1.7%), used_in: bucket_rules_1}
    - {input: Coatings and insulation, value: 2.8, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 17.1; 0.5%), used_in: bucket_rules_1}
    - {input: Castings and forgings, value: 2.7, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §3b (cumulative 16.2; 0.5%), used_in: bucket_rules_1}
    - {input: Unbucketed / ambiguous residual, value: 245.8, unit: $M per year, year: FY22-27 avg, tie_out: SAM Build §2a/§3b (cumulative 1474.8; 42.9%), used_in: bucket_rules_1}
    - {input: Leonardo SpA via DRS lifetime visible flow, value: 1810.3, unit: $M lifetime, year: lifetime, tie_out: nc_lifetime_vendors.csv rank 1, used_in: bucket_rules_1}
    - {input: Major Tool and Machine lifetime visible flow, value: 816.1, unit: $M lifetime, year: lifetime, tie_out: nc_lifetime_vendors.csv rank 3 (+131.8 second UEI), used_in: bucket_rules_1}
  calculations:
    - {name: Average annual bucket TAM, formula: FY22-27 cumulative divided by six, output: per-row avg-annual column, used_in: bucket_rules_1}
    - {name: Broad component manufacturing, formula: sum of the seven named buckets, output: ~$1,963.8M cumulative (~57.1% of TAM), used_in: reserve}
    - {name: Residual share, formula: 1474.8 / 3438.6, output: 42.9% of TAM, used_in: bucket_rules_1}
  rounding_rules: Whole $M in visible cells (avg annual and cumulative); shares to one decimal; reserve may retain one decimal for tie-out.
  reconciliation: Seven named buckets plus the unbucketed residual equal modeled portfolio TAM; broad component SAM includes the named buckets only, not the residual.

qa:
  guardrails:
    - Seven named buckets appear plus the explicit unbucketed residual (~$246M per year, 42.9% of TAM).
    - The residual is visually distinct and not hidden in broad SAM.
    - Electrical and power is the largest named bucket; structural fab and pre-outfit is second.
    - Supplier evidence is parent-level (Vendors tab / nc_lifetime_vendors.csv), not bucket-split CD09.
    - Scenario membership matches the scenario flags; the only visible slash is "Unbucketed / ambiguous".
  source_checks:
    - Sources are public citations only (SAM.gov APIs and FAR 52.204-10); no internal workbook tabs, CSVs, or CD IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "no chart on this slide -> chart rId checks do not apply"
    - "resolved column widths sum to the table region width"
