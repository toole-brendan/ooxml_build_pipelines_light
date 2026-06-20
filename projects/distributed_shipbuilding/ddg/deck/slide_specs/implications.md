# ══════════════════════════════════════════════════════════════════════════════
# MERGED SLIDE SPEC — two slides, one file  (consolidated 2026-06-04; 43→40 specs)
# Documents TWO rendered slides whose modules stay SEPARATE; the build is unchanged.
#   1. ddg-s15  market_direction.py — direction of travel (qualitative timeline)
#   2. ddg-s16  implications.py      — where-to-play scorecard (closing body slide)
# Both original specs follow verbatim, separated by the `---` YAML document break.
# Edit each slide within its own document.
# ══════════════════════════════════════════════════════════════════════════════

# SlideSpec — DDG market_direction
# Body slide 15. NO chart — a qualitative evidence-timeline house_table + a no-fill
# interpretation rail. The CD11 block is qualitative evidence, never a numeric index.

meta:
  slide_id: ddg-s15
  slide_order: 15
  module_name: market_direction.py
  slide_type: body
  section: SAM and Work Types
  archetype: evidence_timeline_table_plus_interpretation_rail
  story_role: Show the direction of travel without over-sizing the future — connect prime commentary and policy context into a qualitative read that external production capacity is likely to matter more, not less.
  inputs:
    - z_ChartData CD11_OUTSOURCING_INDEX (qualitative shape_table; NOT a numeric index)
    - extracted/exec_quotes_outsourcing.csv (HII/GD outsourcing commentary)
    - References tab sources_references (CITE-03 GAO; CITE-04 Navy 30-Year Plan)
  related_appendix: []

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Market direction
  title_topic: Market Direction
  title_finding: Distributed shipbuilding points toward more external production capacity
  layout: slideLayout4
  sources:
    - HII quarterly earnings materials, FY2024 Q3-FY2026 Q1
    - General Dynamics earnings materials, FY2025 Q4-FY2026 Q1
    - GAO-25-106286
  source_line_exact: "Sources: (1) HII quarterly earnings materials, FY2024 Q3-FY2026 Q1; (2) General Dynamics earnings materials, FY2025 Q4-FY2026 Q1; (3) GAO-25-106286"

story:
  objective: Present a qualitative evidence timeline of distributed-shipbuilding signals and interpret the direction of travel as more external production capacity, especially at HII Ingalls — directional, not a refreshed TAM.
  do_not_say:
    - Do not fabricate a numeric outsourcing index from the qualitative evidence.
    - Do not introduce a future TAM forecast.
    - Do not treat GD as an equivalent DDG outsourcing-hours commitment to HII's.
  known_caveats:
    - HII's "doubled / +30% / 23 vendors" figures are enterprise/shipbuilding-wide (Ingalls + Newport News), not DDG-only.
    - GD's "supply chain is the gating item" was said in an Electric Boat / submarine context, not BIW / DDG.
    - This slide is directional; the deck's market size remains FY22-27 average-annual TAM and SAM.

object_assessment:
  verdict: "Keep the qualitative timeline table. This slide is the deck's non-numeric direction-of-travel proof; do not invent a chart."
  object_contract:
    render_pattern: qualitative_evidence_timeline_table_plus_no_fill_readout
    expected_rendered_object_count: 3
    compound_objects: []
    required_focal_family: "One full-width native table dominates; interpretation is a no-fill readout below, not a side rail."
  anti_repetition:
    versus_ffata_visibility_gap: "After missed-flow chips, this becomes a chronological evidence table."
    versus_implications: "S16 is a decision scorecard, not an evidence timeline."
    forbidden_defaults:
      - No numeric outsourcing index.
      - No future TAM forecast.
      - No chart.

regions:
  coord_basis: BODY
  layout_pattern: evidence_timeline_table_plus_interpretation_rail
  title_band: {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  timeline:   {x: 0%, y: below(title_band), w: 100%, h: fit_content}   # the dominant object
  rail:       {x: 0%, y: below(timeline) + GAP, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external table title (no-fill text_box above the table)}
  - {id: e2, type: table,         region: timeline,   prominence: primary,   paint_order: 2, content: qualitative evidence timeline (Period / Source / Signal / Implication), tie_out: CD11_OUTSOURCING_INDEX}
  - {id: e3, type: rail,          region: rail,       prominence: secondary, paint_order: 3, content: no-fill interpretation rail (directional read + the FY22-27-TAM caveat)}

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
    - table: timeline_1
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
    - shape: rail_1
      element: e3
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."

charts: []                  # NO native chart — CD11 is qualitative; never fabricate an index

tables:
  - id: timeline_1
    element: e2
    role: primary
    factory: house_table
    semantic:
      table_name: Market direction (evidence)
      purpose: summarize     # paraphrased quote evidence by period; directional, not numeric
      reader_takeaway: External production capacity is expanding, led by HII; GD signals constraint; policy supports the direction.
      row_order: chronological by fiscal period, HII first, then GD, then policy
      highlight_rows: []
      guardrails:
        - Use short paraphrases, not long transcript quotes.
        - No fabricated numeric index column.
    render:
      table_skin: rule        # evidence register reads cleaner light; the 1.5pt header rule carries it
      size: 950               # 9.5pt house dense default; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [1.1, 1.4, 4.3, 2.4]   # Period / Source / Signal (wide) / Implication
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l", "l", "l"]      # text-heavy -> left align all columns
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size, min_row_h: 274320}
      rows:
        - ["Period",    "Source",           "Signal",                                                                       "Implication"]
        - ["FY24 Q3",   "HII",              "Outsourcing over 1 million hours in 2024; planned increase of more than 30% in 2025", "Outsourcing is now a named lever"]
        - ["FY25 Q4",   "HII",              "Outsourcing doubled year over year in 2025; +30% planned in 2026; over 23 vendors established", "Supplier network is scaling"]
        - ["FY26 Q1",   "HII",              "On track to grow outsourcing hours ~30%; first 2 of 32 units in yard from partners on DDG 137", "Distributed work reaching the DDG line"]
        - ["FY25 Q4",   "General Dynamics", "Supply chain remains the gating item (Electric Boat context); no comparable DDG outsourcing-hours target", "Constraint is broad, not a DDG plan"]
        - ["FY25-FY26", "Navy and GAO",     "Shipbuilders already outsource to overcome constrained physical space; distributed production policy", "Directional tailwind"]
      cell_fills: {}
      cell_bold: {}           # first column (Period) auto-bolds via house_table
      cell_text_colors: {}
      footnotes:
        - "Qualitative evidence; paraphrased from earnings materials and GAO. Not a numeric index and not a TAM forecast."
    columns: []

shapes:
  - id: title_1
    element: e1
    factory: text_box        # external table title (house chart/exhibit title pattern)
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Distributed-shipbuilding signals, FY2024 Q3 to FY2026 Q1"
    meaning: Names the exhibit in the house 10pt italic title style above the table.
  - id: rail_1
    element: e3
    factory: text_box        # no-fill interpretation rail (slide_guide -> no-fill commentary)
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    text:
      bullets:
        - {lead: "Direction:", body: "external production capacity is expanding, especially at HII Ingalls."}
        - {lead: "Asymmetry:", body: "HII has the clearest public commitment; GD signals supplier constraints, submarine-centric."}
        - {lead: "Scope:", body: "directional only — it does not change the FY22-27 TAM math without a refreshed model."}
    meaning: Interprets the timeline without introducing a forecast; keeps the read qualitative.

commentary:
  visible:
    element: e3
    container: method_note
    title:
    bullets:
      - {lead: "Direction:", body: "external production capacity is expanding, especially at HII Ingalls."}
      - {lead: "Asymmetry:", body: "HII has the clearest public commitment; GD signals constraint, submarine-centric."}
      - {lead: "Scope:", body: "directional only — it does not change the FY22-27 TAM math without a refreshed model."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the penultimate body slide, turning the static FY22-27
      sizing into a direction-of-travel read before Implications (S16). It is qualitative
      by construction: the CD11_OUTSOURCING_INDEX block is a shape_table of exec-quote
      evidence (factory "shape_table", unit "(qualitative)", note "no structured index
      yet"), fed from exec_quotes_outsourcing.csv. Source SRC-14 is annotated "direction-
      of-travel signal ... NOT dollar sizing." Do NOT fabricate an index value. [tie-out:
      chartdata_z_chart_data.py CD11; sources_references SRC-14]

      THE HII EVIDENCE (strongest, most DDG-specific, verbatim-anchored).
      - FY24 Q3 (call Oct 31, 2024): "we are outsourcing over 1 million hours in 2024 and
        plan to increase that by over 30% in 2025."
      - FY25 Q4 (Jan 2026): "doubled outsourcing year-over-year in 2025 ... planning to
        increase outsourcing by another 30% in 2026"; "established over 23 vendors last
        year." (Phrasing is "over 23," "over 30%.")
      - FY26 Q1 (call May 5, 2026): "on track to grow our outsourcing hours year-over-year
        by 30%"; and the single most granular DDG datapoint — "received the first 2 of 32
        units in yard from our distributed shipbuilding partners on DDG 137 John F. Lehman."
        One Flight III hull = ~32 distributed-fab units.
      CAVEAT: the doubled / +30% / 23-vendor figures are HII enterprise/shipbuilding-wide
      (Ingalls + Newport News, incl. the Charleston site doing carrier/sub work), not
      DDG-only. [tie-out: wiki 08, 13; exec_quotes_outsourcing.csv]

      THE GD CONTRAST. "The supply chain remains the gating item" (Novakovic, GD FY25 Q4,
      Jan 28 2026) was said in an Electric Boat / submarine context (that call's program
      mentions: DDG 0, Electric Boat 8, submarine 6), NOT about BIW/DDG. GD has made NO
      comparable DDG outsourcing-hours commitment; its supplier commentary and >$900M FY26
      capex are submarine-centric. The only BIW/DDG note (FY26 Q1): "the DDG51 program
      continues to improve in both efficiency and schedule" — qualitative, no number. The
      asymmetry (HII forward, GD cautious) is itself the market signal. [tie-out: wiki 07, 13]

      POLICY BACKDROP (makes the direction credible, not speculative). GAO-25-106286
      (Feb 27, 2025): "two of the shipbuilders we spoke with are already outsourcing work
      that would normally be done at their shipyards to their suppliers to overcome
      constrained physical space, with plans to expand the volume." DoD spent >$5.8B on the
      shipbuilding industrial base FY2014-2023, +$12.6B planned through FY2028; the Navy's
      May 2026 30-Year Plan sets a 10%->50% distributed-shipbuilding target. [tie-out: wiki
      14; sources_references CITE-03, CITE-04]

      WHY IT STAYS DIRECTIONAL. HII frames the strategy as horizontal capacity expansion,
      NOT vertical integration (Kastner: "I really don't want to vertically integrate"); the
      ramp is a near-term margin headwind (FY26 shipbuilding margin guided 5.5-6.5%, with
      outsourcing costs cited as a drag). Throughput (~15%) and outsourcing (~30%) are
      reported as distinct levers. None of this is a disclosed dollar figure, so the slide
      must not imply a refreshed TAM. [tie-out: wiki 08, 13, 15]

      DENSITY GUIDANCE. Default is the 5-row evidence timeline + a 3-line interpretation
      rail. To densify, add the DDG-137 "32 units" specificity to the FY26 Q1 row, or a
      policy line to the rail. Keep paraphrases short and never add a numeric index column.
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e3]}
      dense:  {add_bullets: 2, safe_containers: [rail, timeline], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT"]}
    approved_extra_points:
      - priority: 1
        lead: "DDG-specific proof:"
        body: "First 2 of 32 distributed-fab units arrived in-yard on DDG 137 (FY26 Q1), one Flight III hull = ~32 distributed units; the most granular public DDG datapoint."
        evidence: HII FY26 Q1 call (May 5, 2026)
        safe_container: timeline   # expand the FY26 Q1 Signal cell
        density_trigger: Add when the audience wants a concrete DDG-line example.
      - priority: 2
        lead: "Enterprise vs DDG:"
        body: "HII's doubled / +30% / 23-vendor figures are shipbuilding-wide (Ingalls + Newport News), not DDG-only."
        evidence: wiki 08 (Charleston); wiki 13
        safe_container: rail
        density_trigger: Add if a reader reads the figures as DDG-specific.
      - priority: 3
        lead: "GD is not equivalent:"
        body: "GD's 'supply chain is the gating item' was about Electric Boat/submarine; GD made no comparable DDG outsourcing-hours commitment."
        evidence: GD FY25 Q4 (Jan 28, 2026); wiki 07
        safe_container: rail
        density_trigger: Add to prevent treating GD and HII as equal commitments.
      - priority: 4
        lead: "Policy anchor:"
        body: "GAO-25-106286 finds yards already outsource to overcome constrained physical space, with plans to expand volume, the load-bearing policy quote."
        evidence: GAO-25-106286 (Feb 27, 2025); wiki 14
        safe_container: rail
        density_trigger: Add when the audience questions whether the trend is real.
      - priority: 5
        lead: "Navy target:"
        body: "The Navy's May 2026 30-Year Plan sets a 10%->50% distributed-shipbuilding target; DoD industrial-base spend +$12.6B planned through FY2028."
        evidence: wiki 14; sources_references CITE-04
        safe_container: rail
        density_trigger: Add for a policy-focused audience.
      - priority: 6
        lead: "Not vertical integration:"
        body: "HII frames this as horizontal capacity expansion, not vertical integration (Kastner: 'I really don't want to vertically integrate')."
        evidence: HII FY24 Q4; wiki 08
        safe_container: rail
        density_trigger: Add if a reader assumes HII is in-sourcing.
      - priority: 7
        lead: "Margin headwind:"
        body: "The ramp is a near-term cost: FY26 shipbuilding margin guided 5.5-6.5%, with outsourcing costs cited as a drag, capacity over short-term margin."
        evidence: wiki 13, 15
        safe_container: rail
        density_trigger: Add for an investor audience.
      - priority: 8
        lead: "Vendor cadence:"
        body: "'Over 23 vendors established last year' is HII's hardest quantitative onboarding anchor, with more to follow."
        evidence: HII FY25 Q4 call
        safe_container: timeline
        density_trigger: Add to the FY25 Q4 Signal cell if room.
    do_not_add:
      - a fabricated numeric outsourcing index
      - a future TAM forecast
      - GD framed as an equivalent DDG outsourcing-hours commitment
      - long verbatim transcript quotes (paraphrase)

data_and_calculations:   # qualitative slide — no derived numbers; figures are paraphrased evidence
  data_inputs: []
  rounding_rules: None; all figures are paraphrased evidence stated as the source states them (e.g. "over 1 million hours," "over 30%").
  reconciliation: Evidence is directional and not reconciled to a dollar figure; the deck's market size stays FY22-27 average-annual TAM and SAM.

qa:
  guardrails:
    - HII is shown as the strongest directional signal; GD is context, not an equivalent public commitment.
    - Policy context is directional, not a new sizing input.
    - No future TAM forecast and no fabricated numeric index are introduced.
    - GD's gating-item quote is attributed to its Electric Boat/submarine context, not BIW/DDG.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal CSVs, workbook tabs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the timeline region width"
    - "table bottom + interpretation rail both sit within BODY (size rows via estimate_row_heights)"

---

# SlideSpec — DDG implications
# Body slide 16 (closing body slide). NO chart — a scorecard house_table + a no-fill
# where-to-play / sizing note. A disciplined prioritization screen, not a capture forecast.

meta:
  slide_id: ddg-s16
  slide_order: 16
  module_name: implications.py
  slide_type: body
  section: SAM and Work Types
  archetype: scorecard_table_plus_note
  story_role: Convert the market sizing into where-to-play choices — practical but disciplined, pointing to prioritization logic without pretending to be a capture forecast.
  inputs:
    - SAM Build and Scenarios (quantitative scenario values)
    - z_ChartData SD12_IMPLICATIONS_SCORECARD (re-emits the CD08 scenario values)
    - Deck Outputs DO-31..DO-40 (Figure Register)
    - Bucket Evidence (data confidence / target-lane interpretation)
  related_appendix:
    - ddg-a6   # appendix_bucket_rules_supplier_evidence
    - ddg-a2   # appendix_tam_calculation

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Implications
  title_topic: Implications
  title_finding: Prioritization depends on product scope, qualification burden, and confidence in bucket visibility
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122
    - GAO-25-106286
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; (3) GAO-25-106286"

story:
  objective: Leave the reader with usable where-to-play choices via a disciplined scenario scorecard — broad is the envelope, metal the largest targeted scenario, electrical the largest single bucket, modular the distributed-capacity lane, HM&E selective — without adding capture odds or a revenue forecast.
  do_not_say:
    - No SOM, capture probability, or win-rate columns.
    - Do not present broad component manufacturing as a single sales wedge.
    - No bubble chart (it would imply false precision).
  known_caveats:
    - This is a where-to-play screen, not SOM; no capture probability is applied.
    - Confidence / qualification / priority are deck judgment, not workbook-computed values.
    - Title must stay within 2 title lines at 20pt over the content width.

object_assessment:
  verdict: "Keep the closing scorecard, but make it the only object that matters. No chart, no cards, no bubble plot."
  object_contract:
    render_pattern: full_width_primary_scorecard_table_plus_closing_note
    expected_rendered_object_count: 3
    compound_objects: []
    required_focal_family: "Dark-header native table owns the slide; only top priority cells get BLUE_1 highlights. Closing note remains no-fill."
  anti_repetition:
    versus_market_direction: "This is not a timeline or evidence table; it is a prioritization screen."
    forbidden_defaults:
      - No SOM column.
      - No capture probability.
      - No bubble chart.

regions:
  coord_basis: BODY
  layout_pattern: scorecard_table_plus_note
  title_band: {x: 0%, y: 0%, w: 100%, h: TITLE_BAND_H}
  scorecard:  {x: 0%, y: below(title_band), w: 100%, h: fit_content}   # dominant object, full BODY width
  note_strip: {x: 0%, y: below(scorecard) + GAP, w: 100%, h: fit_content}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external table title (no-fill text_box above the table)}
  - {id: e2, type: table,         region: scorecard,  prominence: primary,   paint_order: 2, content: 5-scenario prioritization scorecard (size + confidence + priority read), tie_out: SD12_IMPLICATIONS_SCORECARD}
  - {id: e3, type: note,          region: note_strip, prominence: tertiary,  paint_order: 3, content: no-fill where-to-play + sizing note (2 lines)}

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
    - table: scorecard_1
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
    - shape: note_1
      element: e3
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts: []                  # NO native chart — a scorecard table, not a bubble chart

tables:
  - id: scorecard_1
    element: e2
    role: primary
    factory: house_table
    semantic:
      table_name: Scenario prioritization scorecard
      purpose: summarize     # rank scenarios by size + confidence + a qualitative priority read
      reader_takeaway: Metal and electrical are the most concrete near-term lanes; broad is the envelope; modular is the strategic distributed lane; HM&E is selective.
      row_order: by average-annual SAM descending (broad, metal, electrical, modular, HM&E)
      highlight_rows: [Metal components, Electrical and power]   # the most concrete near-term lanes
      guardrails:
        - Broad is labeled an envelope, not a wedge.
        - No capture / win-probability / revenue-forecast column.
        - Priority-read cells fold qualification difficulty + strategic fit; they are deck judgment.
    render:
      table_skin: dark        # the deck's ONE closing primary table -> dark BLUE_5 header
      size: 950               # 9.5pt; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [2.6, 1.5, 1.4, 1.1, 1.5, 3.2]   # Scenario / Avg annual / Cumulative / TAM share / Confidence / Priority read (wide)
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "r", "ctr", "ctr", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Scenario",                    "Avg annual",     "Cumulative", "TAM share", "Confidence",  "Priority read"]
        - ["Broad component manufacturing", "~$327M per year", "~$1.96B",   "57.1%",     "Medium",      "Envelope, not a single wedge"]
        - ["Metal components",            "~$170M per year", "~$1.02B",    "29.6%",     "Medium-high", "Largest targeted scenario; high if fabrication or machining scope fits"]
        - ["Electrical and power",        "~$132M per year", "~$791M",     "23.0%",     "Medium",      "Largest single named bucket; high but qualification-heavy"]
        - ["Modular assemblies",          "~$104M per year", "~$626M",     "18.2%",     "Medium",      "Strategic distributed-capacity lane; smaller in the current model"]
        - ["HM&E components",             "~$89M per year",  "~$531M",     "15.4%",     "Medium-low",  "Selective, product-by-product; evidence-dependent"]
      cell_fills:
        "(2,5)": BLUE_1        # Metal priority cell — concrete near-term lane
        "(3,5)": BLUE_1        # Electrical priority cell — concrete near-term lane
      cell_bold: {}            # first column (Scenario) auto-bolds via house_table
      cell_text_colors: {}
      footnotes:
        - "Where-to-play screen, not SOM. No capture probability is applied."
    columns:
      - {name: Scenario, unit: name, tie_out: inputs_scenarios.SCENARIOS}
      - {name: Avg annual, unit: $M/yr, tie_out: SAM Build §4a, formula: cumulative SAM / 6 years}
      - {name: Cumulative, unit: $B, tie_out: SAM Build §4a}
      - {name: TAM share, unit: percent, tie_out: scenario cumulative SAM / portfolio TAM}
      - {name: Confidence, unit: qualitative, tie_out: deck judgment (Bucket Evidence)}
      - {name: Priority read, unit: qualitative, tie_out: deck judgment}

shapes:
  - id: title_1
    element: e1
    factory: text_box        # external table title (house exhibit-title pattern)
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Scenario prioritization scorecard, average annual FY22-27"
    meaning: Names the exhibit in the house 10pt italic title style above the table.
  - id: note_1
    element: e3
    factory: text_box        # no-fill bottom note (slide_guide -> no-fill commentary)
    fill: null
    line_color: null
    insets: INSETS_NONE
    text:
      paragraphs:
        - {lead: "Where-to-play screen, not SOM.", body: "Prioritization depends on product scope, qualification burden, and confidence in bucket visibility."}
        - {body: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."}
    meaning: Two-line no-fill note — the where-to-play disclaimer plus the standard sizing convention.

commentary:
  visible:
    element: e3
    container: table_note
    title:
    bullets:
      - {lead: "Screen:", body: "where-to-play, not SOM; no capture probability is applied."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the deck's closing body slide — it should leave the
      reader with usable choices, not reopen the methodology debate. It restates the five
      scenarios (S12) as a prioritization screen. The scenario numbers are workbook-computed
      and tie out exactly (CD08 / SD12_IMPLICATIONS_SCORECARD); the confidence /
      qualification / priority columns are deck judgment — the workbook deliberately leaves
      that scoring to the deck (SD12 carries the literal cell text "confidence / difficulty /
      priority set in deck"). Keep it disciplined: no capture odds, no revenue-forecast
      column, no bubble chart. [tie-out: chartdata_z_chart_data.py SD12; SAM Build §4a]

      THE RECOMMENDED QUALITATIVE READ (per scenario).
      - Broad component manufacturing (~$327M/yr; 57.1%): the umbrella market envelope, not
        a single wedge. Confidence medium; use as the framing total.
      - Metal components (~$170M/yr; 29.6%): the largest targeted scenario; attractive if
        product scope includes structural fabrication, machining, or cast/forged components.
        Confidence medium-high (broadest physical-fab base; castings is the thin leg at
        ~0.5% of TAM). Backed by named machining proof points (Major Tool and Machine).
      - Electrical and power (~$132M/yr; 23.0%): the largest single named bucket and the
        largest observed supplier-$ bucket; attractive but requires specialized power-system
        qualification and supplier relationships, and much of it is GFE-directed combat-
        system work. Confidence medium.
      - Modular assemblies (~$104M/yr; 18.2%): strategically important because distributed
        shipbuilding favors pre-outfit and module work (GAO-25-106286: yards already
        outsource to overcome constrained physical space); current modeled size is smaller
        than broad and metal. Confidence medium.
      - HM&E components (~$89M/yr; 15.4%): the narrowest lane; depends heavily on exact
        product family, certification, and evidence visibility (the SCN HM&E cost line is
        missing pre-FY24). Confidence medium-low to medium.

      WHY THESE ARE CHOICES, NOT A FORECAST. The screen sorts scenarios by modeled SAM and a
      qualitative confidence/fit read; it deliberately applies no capture probability. Metal
      and electrical are the most concrete near-term lanes in the current model, but product
      fit governs. Modular ties to the S15 distributed-shipbuilding direction. Broad must
      never be presented as a single sales wedge. [tie-out: SAM Build §4b note "not SOM"]

      OPTIONAL FULLER COLUMN SET. The original contract lists seven scorecard columns
      (avg-annual, cumulative, TAM share, data confidence, qualification difficulty,
      strategic fit, near-term priority). This spec folds qualification difficulty +
      strategic fit into the "Priority read" cell to keep six readable columns; a denser
      future version can split them back out (qualification: metal medium-high, electrical
      high, modular high, HM&E medium-high; strategic fit: metal high if scope fits,
      electrical high for power specialists, modular high for distributed build).

      DENSITY GUIDANCE. Default is the 5-row scorecard + a 2-line no-fill note. To densify,
      split the priority read into qualification + strategic-fit columns, or add a per-row
      proof-point footnote. Keep it a rule/dark table, never a bubble chart, and keep the
      no-SOM note.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3]}
      dense:  {add_bullets: 2, safe_containers: [scorecard, note_strip], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Metal is the workhorse lane:"
        body: "Largest targeted scenario (~$170M/yr); medium-high confidence on the broadest physical-fab base (structural + machining + castings)."
        evidence: SAM Build §4a; wiki 06 (machining proof points)
        safe_container: scorecard   # qualification/fit column if split out
        density_trigger: Add when splitting the priority read into qualification + fit.
      - priority: 2
        lead: "Electrical is large but gated:"
        body: "Largest single bucket (~$132M/yr) and largest observed supplier-$ bucket, but combat-system power work is GFE-directed and qualification-heavy."
        evidence: Entity Master bucket summary; wiki 10
        safe_container: scorecard
        density_trigger: Add to the qualification column if split out.
      - priority: 3
        lead: "Modular = distributed lane:"
        body: "Smaller today (~$104M/yr) but the scenario most aligned with the S15 distributed-shipbuilding direction; GAO notes yards outsource to overcome constrained space."
        evidence: market_direction (S15); GAO-25-106286
        safe_container: note_strip
        density_trigger: Add when shown alongside the market-direction slide.
      - priority: 4
        lead: "HM&E is selective:"
        body: "Narrowest lane (~$89M/yr); evidence-dependent and the SCN HM&E cost line is missing pre-FY24, treat as product-by-product."
        evidence: cost_funnel_summary.csv (HM&E data flag)
        safe_container: scorecard
        density_trigger: Add a confidence caveat footnote.
      - priority: 5
        lead: "Broad is the envelope:"
        body: "~$327M/yr (57.1% of TAM) is the umbrella, not a go-to-market; it already excludes the ~42.9% unbucketed residual."
        evidence: SAM Build §2a, §4b
        safe_container: note_strip
        density_trigger: Add if a reader treats broad as a single addressable wedge.
      - priority: 6
        lead: "Not SOM:"
        body: "No capture probability is applied anywhere; this is a where-to-play screen, and SAM is a strict subset of TAM."
        evidence: SAM Build §4b note
        safe_container: note_strip
        density_trigger: Keep visible; expand if a reviewer asks about capture.
      - priority: 7
        lead: "Per-hull anchor:"
        body: "~$265M supplier TAM rides on each of 13 in-window hulls; the scenarios are cuts of that combined TAM, not separate budgets."
        evidence: TAM Build §5d; DO-21
        safe_container: note_strip
        density_trigger: Add for an audience sizing the per-hull opportunity.
      - priority: 8
        lead: "Confidence is deck judgment:"
        body: "The workbook computes the SAM dollars but leaves confidence/qualification/priority to the deck (SD12: 'set in deck'), state it as judgment, not a model output."
        evidence: chartdata_z_chart_data.py SD12
        safe_container: scorecard
        density_trigger: Add a method footnote if a reviewer asks how confidence is scored.
    do_not_add:
      - capture %, win-probability, or revenue-forecast columns
      - a bubble chart
      - broad component manufacturing framed as a single sales wedge
      - SOM language

data_and_calculations:
  data_inputs:
    - {input: Broad component manufacturing, value: 327.3, unit: $M/yr, cumulative: 1963.8, share_of_tam: 57.1%, tie_out: SAM Build §4a / SD12, used_in: scorecard_1}
    - {input: Metal components,              value: 169.7, unit: $M/yr, cumulative: 1018.2, share_of_tam: 29.6%, tie_out: SAM Build §4a / SD12, used_in: scorecard_1}
    - {input: Electrical and power,          value: 131.8, unit: $M/yr, cumulative: 791.0,  share_of_tam: 23.0%, tie_out: SAM Build §4a / SD12, used_in: scorecard_1}
    - {input: Modular assemblies,            value: 104.3, unit: $M/yr, cumulative: 625.5,  share_of_tam: 18.2%, tie_out: SAM Build §4a / SD12, used_in: scorecard_1}
    - {input: HM&E components,               value: 88.5,  unit: $M/yr, cumulative: 531.1,  share_of_tam: 15.4%, tie_out: SAM Build §4a / SD12, used_in: scorecard_1}
  rounding_rules: Avg-annual to whole $M ("~$XXXM per year"); cumulative to $B (two decimals or ~$XXXM under $1B); share-of-TAM to one decimal.
  reconciliation: Scenarios are overlapping cuts of the same TAM; the scorecard ranks them, it does not sum them. SAM is a strict subset of TAM, never SOM.

qa:
  guardrails:
    - Broad component manufacturing is labeled an envelope, not a wedge.
    - Metal components is the largest targeted scenario; electrical and power the largest single named bucket.
    - Slide explicitly avoids SOM and capture probability; no bubble chart.
    - Confidence / priority columns are presented as deck judgment, not workbook outputs.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal docs, workbook tabs, or chart IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the scorecard region width"
    - "scorecard + note both sit within BODY (size rows via estimate_row_heights)"
