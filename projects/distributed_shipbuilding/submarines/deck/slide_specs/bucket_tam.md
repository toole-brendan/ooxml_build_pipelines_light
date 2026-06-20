# ══════════════════════════════════════════════════════════════════════════════
# MERGED SLIDE SPEC — two slides, one file  (consolidated 2026-06-04; 43→40 specs)
# Documents TWO rendered slides whose modules stay SEPARATE; the build is unchanged.
#   1. subs-s12  work_type_taxonomy.py — work-type taxonomy (card grid)
#   2. subs-s13  bucket_tam.py          — bucket TAM (ranked bar)
# Both original specs follow verbatim, separated by the `---` YAML document break.
# Edit each slide within its own document.
# ══════════════════════════════════════════════════════════════════════════════

# SlideSpec - submarines `work_type_taxonomy` (deck slide 12)
# Card-grid taxonomy: a shapes-only slide (no chart, no table). Seven work-type
# bucket cards (4 over 3) under one section label, plus a gray residual card and a
# method note. Demonstrates element types diagram / callout / note and the closed
# region grammar on a slide with no exhibit frame.

meta:
  slide_id: subs-s12
  slide_order: 12               # deck-spec narrative position; not yet registered (KNOWN GAP, S12-S16)
  module_name: work_type_taxonomy.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: card_grid_taxonomy
  story_role: Make the seven-bucket SAM structure intuitive before the deck shows bucket dollars (S13) and scenario SAM (S14).
  inputs:
    - Slide Data SD_12_WorkTypeTaxonomy
    - taxonomy.py (BUCKETS + NAICS4_BUCKET crosswalk)
    - SAM Build section 4 (modeled bucket shares)
    - Assumptions and Controls (work-type crosswalk)
    - Worktype Evidence
  related_appendix:
    - subs-a5   # appendix_sam_bucket_crosswalk

chrome:
  section: Market sizing
  breadcrumb_topic: Work-type taxonomy
  title_topic: Work-Type Taxonomy
  title_finding: Seven component buckets define the serviceable market
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - FAR 52.204-10
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

story:
  objective: Explain how the model converts a dollar TAM into serviceable component-manufacturing buckets, and where unbucketed flow goes.
  do_not_say:
    - Do not imply the residual is worthless or non-addressable.
    - Broad SAM is the seven buckets only; it is scenario-based, not SOM.
    - No dollar values on this slide (they appear on S13 and S14).
  known_caveats:
    - NAICS is corporate-primary, not a per-action work description, so an explicit residual is kept rather than forcing ambiguous dollars into a bucket.

regions:
  coord_basis: BODY
  layout_pattern: card_grid_taxonomy
  # Two stacked section labels with a 4-over-3 card grid, then a full-width residual
  # card, then a pinned method note. The grid's internal 4-then-3 split is a build
  # detail (two _grid_x sub-rows inside the card_grid region); see shapes -> grid_1.
  section_label_included: {x: 0%, y: 0%,  w: 70%,  h: fit_content}
  card_grid:              {x: 0%, y: 9%,  w: 100%, h: 50%}
  section_label_excluded: {x: 0%, y: 63%, w: 70%,  h: fit_content}
  residual_card:          {x: 0%, y: 71%, w: 100%, h: fit_content}
  method_note:            {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: note,    region: section_label_included, prominence: tertiary,  paint_order: 1, content: "section label: Included in broad component manufacturing"}
  - {id: e2, type: diagram, region: card_grid,              prominence: primary,   paint_order: 2, content: "seven bucket cards (enumerated; 4 over 3)", tie_out: SD_12 / taxonomy.BUCKETS}
  - {id: e3, type: note,    region: section_label_excluded, prominence: tertiary,  paint_order: 3, content: "section label: Outside broad component SAM"}
  - {id: e4, type: callout, region: residual_card,          prominence: secondary, paint_order: 4, content: gray residual card (unbucketed / ambiguous, outside broad SAM)}
  - {id: e5, type: note,    region: method_note,            prominence: tertiary,  paint_order: 5, content: method note (classification basis)}


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
      - role: section label
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
    e2:
      text_runs:
      - role: bucket card title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: bucket definition
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: section label
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
    e4:
      text_runs:
      - role: residual lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: residual body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e5:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes: []

charts: []                # none - this is a definitional taxonomy, not a data exhibit
tables: []                # NONE: object choice is a card grid (independent panels), not a table

shapes:
  - id: label_included_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Included in broad component manufacturing"   # DENSE_BODY_10PT bold, no fill
    meaning: Names the seven-bucket group that makes up broad component SAM.
  - id: grid_1
    element: e2
    factory: text_box           # 7 cards via a slide-local _card() helper looped over the list
    fill: BLUE_1                 # uniform secondary cards; NOT the focal black family
    line_color: GRAY_3           # light secondary border (one card family, equal weight)
    insets: INSETS_CARD
    meaning: >
      Seven equal bucket cards laid out 4-over-3 with _grid_x(4) then _grid_x(3) inside
      card_grid (GAP between cards). Each card = a bold LABEL_9PT title over a
      FINEPRINT_8_5PT definition subline. Keep titles identical to the S13/S14 chart
      category labels.
    cards:                       # title (visible) + definition subline; build detail, not on-slide dollars
      - {title: "Structural fabrication and pre-outfit", definition: "hull sections, fabricated structural metal, pre-outfit modules"}
      - {title: "Machining",                             definition: "machine shops, precision machining, mechanical power transmission"}
      - {title: "Castings and forgings",                 definition: "iron and steel forging, foundries, cast and forged components"}
      - {title: "Piping, valves, and pumps",             definition: "industrial valves, pumps, measuring and dispensing, pipe and fittings"}
      - {title: "Electrical and power",                  definition: "switchgear, electronic components, propulsion-electronics, power distribution"}
      - {title: "HVAC and ventilation",                  definition: "air-conditioning, heating, shipboard ventilation systems"}
      - {title: "Coatings and insulation",               definition: "rubber and synthetic products, composites, coatings and insulation"}
  - id: label_excluded_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Outside broad component SAM"                 # DENSE_BODY_10PT bold, no fill
    meaning: Sets off the residual card from the seven-bucket group.
  - id: residual_1
    element: e4
    factory: text_box
    fill: GRAY_3                 # residual / ambiguous styling (guide color ref); the one black-outlined object
    line_color: BLACK            # focal family on this slide
    line_width: 19050            # 1.5pt focal weight (single focal object)
    insets: INSETS_MESSAGE
    text: "Unbucketed / ambiguous residual: visible vendor flow not confidently assigned to one of the seven buckets. Kept in TAM, excluded from broad component SAM."
    meaning: Keeps the residual visible and honest without forcing ambiguous dollars into a named bucket.
  - id: method_1
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Mapped from FFATA-visible vendors using SAM.gov Entity Management NAICS and manual work-type evidence; NAICS is corporate-primary, not a per-action work description."   # FINEPRINT_8_5PT italic
    meaning: States the classification basis without claiming per-action precision.

commentary:
  visible:
    element: e4
    container: callout           # the gray residual card is the visible commentary
    title:
    bullets:
      - {lead: "Residual:", body: "real evidence ambiguity, not zero market - kept in TAM, out of broad SAM."}
    body_size: DENSE_BODY_10PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the bridge from TAM to SAM and the first slide of
      the SAM and Supplier Landscape section (S12 taxonomy -> S13 bucket TAM -> S14
      scenario SAM -> S15 visible suppliers -> S16 SIB exclusion). The TAM was built
      simply: ~$56.6B FY2022-FY2027 Basic Construction base x a strict 35.0% applied
      supplier coefficient = ~$19.84B cumulative TAM, /6 = ~$3.307B average annual. To
      make that TAM serviceable, the model allocates it across seven work-type buckets
      that a supplier or investor can recognize, plus an explicit residual. This slide
      shows the STRUCTURE only; S13 puts dollars on the buckets and S14 cuts them into
      scenarios. Per the design, no dollar values appear here.

      THE SEVEN BUCKETS (and what each contains).
      - Structural fabrication and pre-outfit - hull sections, fabricated structural
        metal, pre-outfit modules; the bucket most aligned with distributed-build logic.
      - Machining - machine shops, precision machining, mechanical power transmission.
      - Castings and forgings - iron and steel forging, foundries, cast/forged parts.
      - Piping, valves, and pumps - industrial valves, pumps, measuring/dispensing,
        pipe and fittings; broad HM&E with meaningful qualification burden.
      - Electrical and power - switchgear, electronic components, propulsion-electronics,
        power distribution; the largest bucket once dollars are applied (S13, ~38%).
      - HVAC and ventilation - air-conditioning, heating, shipboard ventilation.
      - Coatings and insulation - rubber/synthetic products, composites, coatings,
        insulation, specialized protection materials.

      HOW THE CLASSIFICATION WORKS. Buckets are mapped from the FFATA-visible vendor
      base using SAM.gov Entity Management NAICS-4 codes (a NAICS-4 -> bucket
      crosswalk) plus a short list of manual vendor-bucket overrides and manual
      work-type evidence. NAICS is useful but imperfect: it is generally a
      corporate-primary classification, not a per-action work description, so a vendor's
      primary code can misstate the work on a given subaward.

      WHY A RESIDUAL EXISTS. Because NAICS is corporate-primary, the model keeps an
      explicit unbucketed/ambiguous residual rather than forcing every visible dollar
      into a named bucket. The residual stays IN TAM (the allocation is exhaustive: seven
      buckets + residual = portfolio TAM) but is EXCLUDED from broad component SAM. It is
      not a claim that the residual is non-addressable - it is simply not classified with
      enough confidence for the broad-component scenario. Roles that are not
      supplier-addressable at all (prime/co-prime yards, GFE/SIB pass-throughs, and
      service/non-component vendors) are removed earlier, before bucketing.

      PREVIEW OF DOLLARS (S13) AND SCENARIOS (S14). Once the ~$3.3B/yr TAM is applied:
      electrical and power leads (~$1.26B; 38.0%), then structural fabrication (~$625M;
      18.9%) and piping (~$520M; 15.7%); the residual is ~$501M/yr (~15.2%). Broad
      component manufacturing SAM = all seven buckets, residual excluded = ~$2,805M/yr
      (84.8% of TAM). Keep these out of the taxonomy slide itself.

      DENSITY GUIDANCE. Default is seven cards + residual card + method note. To densify,
      add a one-line NAICS-basis example inside the method note, or split a card subline
      into two short lines - but never add dollar values (those belong on S13/S14) and
      keep the residual gray and visually separate from the seven blue cards.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e4, e5]}
      dense:  {add_bullets: 2, safe_containers: [method_note, residual_card], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Classification basis:"
        body: "Buckets are a NAICS-4 -> bucket crosswalk over FFATA-visible vendors, plus manual overrides and work-type evidence."
        evidence: taxonomy.NAICS4_BUCKET; Worktype Evidence
        safe_container: method_note
        density_trigger: If the method note gains a second line, lead with this.
      - priority: 2
        lead: "Why a residual at all:"
        body: "NAICS is corporate-primary, not per-action, so the model keeps an explicit residual instead of forcing ambiguous dollars into a bucket - a credibility feature."
        evidence: Assumptions and Controls; SAM Build section 4
        safe_container: residual_card
        density_trigger: Add if a reviewer questions the residual.
      - priority: 3
        lead: "Exhaustive allocation:"
        body: "Seven buckets plus the unbucketed residual sum to portfolio TAM; nothing is dropped, the residual is just held out of broad SAM."
        evidence: SAM Build section 5 (TAM bucket allocation)
        safe_container: residual_card
        density_trigger: Add when shown right before the bucket-TAM slide.
      - priority: 4
        lead: "Excluded roles:"
        body: "Prime and co-prime yards, GFE/SIB pass-throughs, and service vendors are removed before bucketing - they are not supplier-addressable component work."
        evidence: Entity Master roles; taxonomy.classify()
        safe_container: method_note
        density_trigger: Add for an audience focused on what counts as addressable.
      - priority: 5
        lead: "Electrical leads on dollars:"
        body: "Once TAM is applied (S13), electrical and power is the largest bucket at ~38%, reflecting submarine power distribution, electronics, and controls."
        evidence: bucket_tam (S13); CD_13_BucketTAM
        safe_container: method_note
        density_trigger: Add only as a forward pointer; keep dollars off this slide.
      - priority: 6
        lead: "Structural = distributed-build fit:"
        body: "Structural fabrication and pre-outfit is the bucket most aligned with pushing module work out of the legacy yards."
        evidence: SAM Build section 4; FFATA-visible subawards (wiki 08)
        safe_container: method_note
        density_trigger: Add for an investor audience on the distributed-build thesis.
      - priority: 7
        lead: "Broad SAM definition:"
        body: "Broad component manufacturing SAM is exactly these seven buckets with the residual excluded - the envelope S14 ranks against the narrower cuts."
        evidence: SAM Build section 6; sam_scenarios (S14)
        safe_container: residual_card
        density_trigger: Add when the residual card has room for a second line.
      - priority: 8
        lead: "Naming discipline:"
        body: "Bucket names here must match the S13 bar labels and the S14 scenario composition exactly, or the section reads as inconsistent."
        evidence: bucket_tam (S13); sam_scenarios (S14)
        safe_container: method_note
        density_trigger: Build-time check, not on-slide copy.
      - priority: 9
        lead: "Supplier proof points:"
        body: "Named vendors anchor most buckets - e.g. Scot Forge (castings/forgings), DC Fabricators and Rhoads (structural), Curtiss-Wright Electro-Mechanical (electrical)."
        evidence: Entity Master; visible_suppliers (S15)
        safe_container: method_note
        density_trigger: Add only if a card gains a vendor example line.
    do_not_add:
      - any dollar value, share, or count (those live on S13/S14)
      - SOM, capture, or win-probability language
      - the residual rendered as an eighth bucket card or in blue (keep it gray + separate)

qa:
  guardrails:
    - Exactly seven named component buckets are shown.
    - Unbucketed / ambiguous appears as a residual OUTSIDE broad SAM, in gray, not as an eighth bucket.
    - No dollar values, shares, or counts on this slide.
    - Bucket names match the S13 chart labels and S14 scenario composition.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov, FAR 52.204-10); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    # no chart on this slide -> chart rId checks do not apply
    # no table on this slide -> table-fit / column-width checks do not apply

---

# SlideSpec - submarines `bucket_tam` (deck slide 13)
# Chart-only body slide: a ranked horizontal bar of the seven work-type buckets by
# average annual TAM, a gray residual strip held out of broad SAM, and an
# average-annual convention note. tables: [] is an explicit design statement.

meta:
  slide_id: subs-s13
  slide_order: 13               # deck-spec narrative position; not yet registered (KNOWN GAP, S12-S16)
  module_name: bucket_tam.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: ranked_bar_plus_residual_strip
  story_role: Make the ~$3.3B average annual TAM actionable by showing where the work-type dollars sit, before scenario SAM (S14).
  inputs:
    - Chart Data CD_13_BucketTAM
    - SAM Build section 5a (TAM by work-type bucket)
    - SAM Build section 4 (modeled bucket shares)
    - Assumptions and Controls (work-type crosswalk)
    - Worktype Evidence
  related_appendix:
    - subs-a5   # appendix_sam_bucket_crosswalk

chrome:
  section: Market sizing
  breadcrumb_topic: Bucket TAM
  title_topic: Bucket TAM
  title_finding: Electrical and power, structural fabrication, and piping lead the opportunity
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - U.S. Department of the Navy SCN Justification Books
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

story:
  objective: Rank the seven component buckets by average annual TAM and locate the largest opportunities before scenario SAM.
  do_not_say:
    - Do not imply the residual is worthless or non-addressable.
    - Broad SAM is scenario-based, not SOM.
    - Do not rank by cumulative TAM or by workbook source-order; rank by average annual TAM.
  known_caveats:
    - The residual exists because the model does not force ambiguous vendor dollars into a bucket.
    - Average annual is not a run-rate; the FY2022-FY2027 cadence is lumpy.

regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_residual_strip
  # Vertical stack by % of BODY height: title band, ranked bar, full-width gray
  # residual strip, then a pinned convention note.
  title_band:     {x: 0%, y: 0%,  w: 100%, h: TITLE_BAND_H}
  chart:          {x: 0%, y: 8%,  w: 88%,  h: 62%}
  residual_strip: {x: 0%, y: 73%, w: 100%, h: fit_content}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,     prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,          prominence: primary,   paint_order: 2, content: ranked bar of 7 buckets by average annual TAM, tie_out: CD_13_BucketTAM}
  - {id: e3, type: callout,       region: residual_strip, prominence: secondary, paint_order: 3, content: gray residual strip (outside broad SAM)}
  - {id: e4, type: note,          region: note_strip,     prominence: tertiary,  paint_order: 4, content: average-annual convention note}


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
      external_title:
      - role: chart/exhibit title
        size: CHART_TITLE_10PT
        color: DK
        font: FONT
        italic: true
      chart_text:
        value_labels:
          size: LABEL_9PT
          font: FONT
          color: auto/DK
          note: Build converts token to *_size_pt expected by chart factory.
        category_axis:
          size: LABEL_9PT
          font: FONT
          color: DK
    e2:
      value_labels:
        size: LABEL_9PT
        font: FONT
        color: auto/DK
        note: Build converts token to *_size_pt expected by chart factory.
      category_axis:
        size: LABEL_9PT
        font: FONT
        color: DK
    e3:
      text_runs:
      - role: residual lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: value phrase
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: residual body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Electrical and power (38.0%)"
        - "Structural fabrication and pre-outfit (18.9%)"
        - "Piping, valves, and pumps (15.7%)"
        - "Castings and forgings (4.3%)"
        - "Coatings and insulation (3.1%)"
        - "Machining (3.0%)"
        - "HVAC and ventilation (1.9%)"
      series:
        - name: Average annual TAM
          values: [1257.1, 624.5, 519.6, 142.8, 101.5, 98.1, 61.9]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_3, BLUE_1, BLUE_1, BLUE_1, BLUE_1]
    params:
      mode: ranked
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175      # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 40
      cat_header: Work-type bucket
      title: null                     # house style: external exhibit_title element
    external_title:
      text: Average annual TAM by work-type bucket, FY2022-FY2027
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Top three buckets are ~73% of modeled TAM before the residual.", anchor_to: e2}

tables: []                # NONE on this slide -> block left explicit; no table-fit / col-width checks apply

shapes:
  - id: residual_1
    element: e3
    factory: text_box
    fill: GRAY_3              # residual / exclusion styling - NOT the counted-TAM blues; not part of the ranked stack
    line_color: BLACK         # focal family on this slide
    line_width: 19050         # 1.5pt focal weight (single focal object)
    insets: INSETS_MESSAGE
    text: "Unbucketed / ambiguous residual: ~$501M per year (~$3.01B cumulative). Tracked in TAM, excluded from broad component SAM."
    meaning: Keeps the residual visible and honest without forcing ambiguous dollars into a named bucket.
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Values are average annual FY2022-FY2027; cumulative shown for context. Average annual is not a run-rate."   # FINEPRINT_8_5PT italic
    meaning: Average-annual convention note; guards against reading the bars as a single-year rate.

commentary:
  visible:
    element: e3
    container: callout         # the residual strip is the visible commentary
    title:
    bullets:
      - {lead: "Residual:", body: "real evidence ambiguity, not zero market - kept in TAM, out of broad SAM."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the first "make it actionable" slide after the
      taxonomy (S12). The headline TAM is built simply: ~$56.6B FY2022-FY2027 Basic
      Construction base x a strict 35.0% applied supplier coefficient = ~$19.84B
      cumulative TAM, /6 = ~$3.307B average annual. This slide allocates that ~$3.3B/yr
      across seven work-type buckets plus an explicit residual; S14 (sam_scenarios)
      then turns the buckets into scenario SAM.

      THE RANKING AND WHAT DRIVES IT.
      - Electrical and power ~$1,257M/yr (~$7.54B; 38.0%) - submarine power distribution,
        electronics, controls, and propulsion-related components; by far the largest.
      - Structural fabrication and pre-outfit ~$625M/yr (~$3.75B; 18.9%) - hull sections,
        fabricated metal, modules; aligns with distributed-build logic (work pushed out
        of the legacy yards creates module/fab demand).
      - Piping, valves, and pumps ~$520M/yr (~$3.12B; 15.7%) - broad HM&E plus specialty
        components with meaningful qualification burden.
      - Castings and forgings ~$143M/yr (4.3%), Coatings and insulation ~$102M/yr (3.1%),
        Machining ~$98M/yr (3.0%), HVAC and ventilation ~$62M/yr (1.9%). Lower dollars,
        but any of these can be a critical bottleneck.
      Top three buckets ~73% of modeled TAM before the residual.

      THE RESIDUAL. ~$501M/yr (~$3.01B; 15.2%) is unbucketed/ambiguous: visible vendor
      flow not confidently assigned to one of the seven buckets. It is kept IN TAM but
      EXCLUDED from broad component SAM. It exists because NAICS is a corporate-primary
      code, not a per-action work description, so the model refuses to force ambiguous
      dollars into a named bucket - which improves credibility and keeps broad SAM from
      being overstated. It is not a claim that the residual is non-addressable.

      HOW BUCKETS BECOME SCENARIOS (preview of S14). Electrical and power is also a
      standalone scenario (~$1,257M). Metal components (structural + machining +
      castings) = ~$865M. HM&E (piping + HVAC + machining) = ~$680M. Modular assemblies
      (structural + coatings) = ~$726M. Broad component manufacturing (all seven, residual
      excluded) = ~$2,805M, i.e. 84.8% of TAM. Note machining sits in BOTH metal and HM&E,
      so those two scenarios are not additive.

      SUPPLIER PROOF POINTS (visible first-tier flow, FFATA). Northrop Grumman ~$1.43B is
      the largest visible recipient (electrical/electronics). Others: Leonardo ~$491M,
      Curtiss-Wright Electro-Mechanical ~$198M (electrical/power), Scot Forge ~$198M
      (forgings -> castings/forgings), ESCO ~$189M, DC Fabricators ~$163M and Rhoads
      ~$142M (structural fab), Graham ~$89M (heat exchangers -> HM&E). ~150 classified
      recipients, ~$5.46B visible value, ~759 broader FFATA parents - a named floor, not
      the full layer (S15).

      DEMAND BACKDROP (directional, not a sizing input). DoD has invested >$10B in the
      submarine industrial base (GAO-26-109068); AUKUS points toward a 2.0-then-2.33
      Virginia-class/yr requirement against ~1.3/yr delivered today (CRS RL32418); HII has
      guided +30% YoY outsourcing hours (HII FY26 Q1). These support why the supplier
      opportunity is expanding but do not change the FY2022-FY2027 math.

      DENSITY GUIDANCE. Default is chart + gray residual strip + convention note. To
      densify, add context lines in the note strip or expand the residual strip to two
      lines. Keep the residual visually separate from the ranked bars (gray, not blue) at
      any density.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [residual_strip, note_strip, chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Why electrical leads:"
        body: "Power distribution, electronics, controls, and propulsion-related components concentrate the largest bucket (~$1.26B; 38% of TAM)."
        evidence: Worktype Evidence; Vendors and concentration (wiki 09)
        safe_container: residual_strip
        density_trigger: If the residual strip gains a second line, add this as context above it.
      - priority: 2
        lead: "Structural = distributed-build fit:"
        body: "Structural fabrication and pre-outfit (~$625M) aligns with pushing module work out of the legacy yards."
        evidence: SAM Build section 4; FFATA-visible subawards (wiki 08)
        safe_container: note_strip
        density_trigger: Add when the chart frame is shortened.
      - priority: 3
        lead: "Small is not unimportant:"
        body: "Castings/forgings, machining, coatings, and HVAC can be critical bottlenecks even at lower dollar values."
        evidence: Worktype Evidence
        safe_container: note_strip
        density_trigger: Add in a max-density variant.
      - priority: 4
        lead: "Concentration:"
        body: "Top three buckets (electrical, structural, piping) are ~73% of modeled TAM before the residual."
        evidence: CD_13_BucketTAM
        safe_container: chart        # chart annotation
        density_trigger: Add if the chart has vertical headroom.
      - priority: 5
        lead: "Buckets -> scenarios:"
        body: "Electrical is also a standalone scenario (~$1,257M); metal (structural+machining+castings) ~$865M; broad (all seven) ~$2,805M = 84.8% of TAM."
        evidence: SAM Build section 6; sam_scenarios (S14)
        safe_container: note_strip
        density_trigger: Add when this slide is shown right before the scenarios slide.
      - priority: 6
        lead: "Supplier proof points:"
        body: "Northrop Grumman ~$1.43B (electrical) leads visible flow; Scot Forge ~$198M (forgings), DC Fabricators/Rhoads (structural) anchor the metal buckets."
        evidence: Entity Master; CD_15_TopVisibleSuppliers
        safe_container: chart
        density_trigger: Add if the chart is narrowed to leave a right margin.
      - priority: 7
        lead: "Coefficient lineage:"
        body: "These buckets allocate the ~$3.3B/yr TAM = ~$56.6B Basic Construction x the strict 35.0% supplier coefficient, /6 years."
        evidence: tam_bridge; methodology
        safe_container: note_strip
        density_trigger: Add only if the audience has not seen the TAM bridge.
      - priority: 8
        lead: "Demand backdrop:"
        body: ">$10B invested in the submarine industrial base (GAO); AUKUS toward 2.33 Virginia/yr; HII guiding +30% outsourcing - directional, not a sizing input."
        evidence: demand_backdrop (S05); GAO-26-109068; CRS RL32418
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 9
        lead: "Why a residual at all:"
        body: "NAICS is corporate-primary, not per-action; the model keeps an explicit residual rather than forcing ambiguous dollars into a bucket - a credibility feature."
        evidence: Assumptions and Controls; work_type_taxonomy (S12)
        safe_container: residual_strip
        density_trigger: Add if a reviewer questions the residual.
    do_not_add:
      - SOM, capture, or win-probability language
      - any claim that the residual is non-addressable
      - the residual rendered inside or adjacent to the ranked bars (keep it gray + separate)

data_and_calculations:
  data_inputs:
    - {input: Electrical and power,                  value: 1257.1, unit: $M/yr, cumulative: 7542.7, share_of_tam: 38.0%, tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Structural fabrication and pre-outfit, value: 624.5,  unit: $M/yr, cumulative: 3747.1, share_of_tam: 18.9%, tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Piping valves and pumps,               value: 519.6,  unit: $M/yr, cumulative: 3117.5, share_of_tam: 15.7%, tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Castings and forgings,                 value: 142.8,  unit: $M/yr, cumulative: 856.7,  share_of_tam: 4.3%,  tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Coatings and insulation,               value: 101.5,  unit: $M/yr, cumulative: 608.8,  share_of_tam: 3.1%,  tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Machining,                             value: 98.1,   unit: $M/yr, cumulative: 588.5,  share_of_tam: 3.0%,  tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: HVAC and ventilation,                  value: 61.9,   unit: $M/yr, cumulative: 371.6,  share_of_tam: 1.9%,  tie_out: CD_13_BucketTAM, used_in: chart_1}
    - {input: Unbucketed / ambiguous residual,       value: 501.1,  unit: $M/yr, cumulative: 3006.8, share_of_tam: 15.2%, tie_out: CD_13_BucketTAM, used_in: residual_1}
  rounding_rules: Whole $M for average-annual labels; $B to two decimals for cumulative.
  reconciliation: Seven named buckets + residual sum to portfolio TAM (~$3,306.6M/yr); residual is excluded from broad SAM.

qa:
  guardrails:
    - Electrical and power is the top bucket at ~$1.26B average annual TAM.
    - Structural fabrication and piping are the next two buckets.
    - Residual is shown in GRAY (e3), separate from the ranked bars - never inside the ranked stack.
    - Bars are ranked by average annual TAM, not cumulative or source-order.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov, SCN Justification Books); no internal docs, workbook tabs, wiki chapters, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    # no table on this slide -> table-fit / column-width checks do not apply
