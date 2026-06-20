# SlideSpec — DDG appendix_ffata_limitations
# Appendix slide A5. The full FFATA limitation detail behind the body ffata_visibility_gap slide:
# an evidence-and-limitations ledger (what public data sees vs what it misses) + a cumulative
# yard-side range cue + a structural-unseen-categories rail. No chart (two measured native tables).

meta:
  slide_id: ddg-a5
  slide_order: A5
  module_name: appendix_ffata_limitations.py
  slide_type: appendix
  section: Appendix
  archetype: evidence_table_plus_range_cue
  story_role: Defend FFATA as an evidence base and a visible floor (not the TAM denominator) by making the invisible supplier layer specific and concrete, behind the body FFATA visibility-gap slide.
  inputs:
    - cost_funnel_summary.csv (LI 2122) cumulative FFATA-visible vs estimated yard-side band
    - SAM Build §2 supplier-addressable shares (subaward-derived bucket evidence)
    - Source feeds (SAM.gov FSRS, USAspending cross-validation, Entity Management)
    - wiki 05 FFATA-visible subawards (categories FFATA misses, SAM vs USAspending)
    - wiki 12 MYP redaction and unseen layer (direct material, lower tiers, BIW under-reporting)
    - wiki 16 data sources and pipeline limitations (reporting lag, NAICS gap, IVECO contamination)
  related_appendix: []

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: FFATA limitations
  title_topic: FFATA Limitations
  title_finding: Visible first-tier subawards are a floor and evidence base, not the market denominator
  layout: slideLayout4
  sources:
    - FAR 52.204-10
    - SAM.gov Acquisition Subaward Reporting Public API
    - GAO-25-106286
  source_line_exact: "Sources: (1) FAR 52.204-10; (2) SAM.gov Acquisition Subaward Reporting Public API; (3) GAO-25-106286"

story:
  objective: Defend the use of FFATA as evidence rather than as the market-size denominator, listing the categories FFATA structurally misses and showing the visible flow as a minority share (~20.1%) of the estimated yard-side outsourcing midpoint.
  do_not_say:
    - Do not imply non-compliance is the only reason FFATA is partial; the largest gap (direct material) is legitimate accounting.
    - Do not use FFATA-visible flow as TAM.
    - Do not mix annual and cumulative values without explicit labels.
    - Do not generalize one yard's filing behavior to the other (BIW ~7% vs Ingalls ~93% of visible flow is a filing artifact).
  known_caveats:
    - FFATA captures reportable first-tier subawards; it misses lower tiers, direct material, standing agreements, and the sub-threshold tail.
    - Range-cue values are cumulative unless the slide is redesigned to annualize them.
    - The visible-share % depends on the time basis (cumulative midpoint ~20.1% vs recent-rate ~15%).

object_assessment:
  verdict: "Keep, but split the bottom limitations rail into explicit missed-category chips if density allows. The ledger remains the primary object."
  object_contract:
    render_pattern: evidence_ledger_plus_range_table_plus_missed_category_chips
    expected_rendered_object_count: 8
    compound_objects:
      - {id: limitations_rail, child_count: 6, child_type: materiality_order_chip}
    required_focal_family: "Evidence ledger primary; range cue secondary; missed-category chips are tertiary and gray/no-fill."
  anti_repetition:
    appendix_rule: "This is limitations evidence, not a re-chart of S14."
    forbidden_defaults:
      - No chart.
      - Do not frame gap as just non-compliance.

regions:
  coord_basis: BODY
  layout_pattern: evidence_table_plus_range_cue
  evidence_table:   {x: 0%, y: 0%, w: 64%, h: body_until(limitations_rail)}
  range_cue:        {x: right_of(evidence_table) + GAP, y: align_top(evidence_table), w: remaining, h: fit_content}
  limitations_rail: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: table, region: evidence_table,   prominence: primary,   paint_order: 1, content: FFATA evidence and limitations ledger (sees vs misses vs deck use), tie_out: wiki 05/12; SAM Build §2}
  - {id: e2, type: table, region: range_cue,        prominence: secondary, paint_order: 2, content: cumulative yard-side visibility range cue (visible vs band vs visible share), tie_out: cost_funnel_summary.csv}
  - {id: e3, type: rail,  region: limitations_rail, prominence: tertiary,  paint_order: 3, content: bottom rail of structural unseen categories}

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
    - table: ffata_evidence_ledger
      element: e1
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
    - table: cumulative_range_cue
      element: e2
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: limitations_rail
      element: e3
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."

charts: []

tables:
  - id: ffata_evidence_ledger
    element: e1
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: FFATA evidence and limitations ledger
      purpose: summarize
      reader_takeaway: FFATA is useful for supplier names, bucket evidence, and concentration, but structurally misses parts of the supplier flow; it is a floor, not the denominator.
      row_order: FFATA first-tier subawards, SAM.gov published and deleted records, Yard-prime PIID filings, Vendor and description fields, SAM.gov Entity Management enrichment, USAspending cross-validation
      highlight_rows: [FFATA first-tier subawards]
      guardrails:
        - FFATA is the observable floor, not the full market denominator.
        - Structural misses are broader than non-compliance.
    render:
      table_skin: light
      size: 850
      column_widths:
        mode: ratio
        values: [1.7, 2.1, 2.1, 2.2]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l", "l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Public-data element", "What it captures", "What it misses", "Implication for deck use"]
        - ["FFATA first-tier subawards", "Direct prime-to-sub subcontracts above the $30,000 threshold", "Lower-tier suppliers and sub-threshold actions", "Visible floor and evidence base"]
        - ["SAM.gov published and deleted records", "FSRS records surfaced through the SAM.gov API (no per-PIID cap)", "Reporting lag of 12 to 30 months and late corrections", "Longitudinal evidence with a timing caveat"]
        - ["Yard-prime PIID filings", "Yard-side filings by BIW and Ingalls", "Direct material booked as direct cost and standing agreements", "Supports the supplier landscape, not the denominator"]
        - ["Vendor and description fields", "Visible supplier names and award descriptions", "Incomplete NAICS and UEI resolution", "Bucket evidence for SAM classification"]
        - ["SAM.gov Entity Management enrichment", "Entity attributes, country, and validation support", "Corporate-primary NAICS, not action-level work type", "Useful for cleaning and enrichment"]
        - ["USAspending cross-validation", "A cross-check against the federal spending view", "Truncation at about 2,500 records per PIID and timing differences", "Triangulation only; SAM.gov is canonical"]
      cell_fills:
        "(1,0)": BLUE_1
      cell_bold:
        "(1,0)": true
      cell_text_colors: {}
      footnotes:
        - "FFATA is the legal reporting framework (FAR 52.204-10); SAM.gov FSRS is the public access path."
    columns:
      - {name: Public-data element, unit: text, tie_out: wiki 05/16, formula: null}
      - {name: What it captures, unit: text, tie_out: wiki 05, formula: null}
      - {name: What it misses, unit: text, tie_out: wiki 05/12, formula: null}
      - {name: Implication for deck use, unit: text, tie_out: wiki 05, formula: null}
  - id: cumulative_range_cue
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Cumulative yard-side view
      purpose: compare
      reader_takeaway: FFATA-visible flow is only ~20.1% of the estimated yard-side outsourcing midpoint on a cumulative basis.
      row_order: FFATA visible, estimated low, estimated midpoint, estimated high, visible share at midpoint
      highlight_rows: [Estimated midpoint, Visible share at midpoint]
      guardrails:
        - Values are cumulative FY2016-FY2027.
        - Do not place annualized values in this matrix unless fully relabeled.
    render:
      table_skin: rule
      size: 900
      column_widths:
        mode: ratio
        values: [2.0, 1.2]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Cumulative yard-side view", "Value"]
        - ["FFATA visible", "~$2.73B"]
        - ["Estimated low", "~$11.31B"]
        - ["Estimated midpoint", "~$13.57B"]
        - ["Estimated high", "~$16.16B"]
        - ["Visible share at midpoint", "20.1%"]
      cell_fills:
        "(1,0)": GRAY_1
        "(3,0)": BLUE_1
        "(5,0)": BLUE_2
      cell_bold:
        "(3,0)": true
        "(5,0)": true
      cell_text_colors: {}
      footnotes:
        - "Cumulative FY2016-FY2027. Annual view (off-slide): ~$455M per year visible vs ~$2.26B per year midpoint."
    columns: []

shapes:
  - id: limitations_rail
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "What FFATA misses (by estimated materiality): direct material booked as direct cost (~$400 to 700M per year), lower-tier subcontracts (add ~30 to 50%), BIW under-reporting, long-term supplier agreements, the sub-$30,000 long tail, and 12 to 30 month reporting lag."
    meaning: Bottom rail listing the structural unseen categories in materiality order; frames the gap as structural, not a data error.

images: []

commentary:
  visible:
    element: e3
    container: table_note
    title:
    bullets:
      - {lead: "Read:", body: "FFATA is the observable floor. It supports supplier names, bucket evidence, and concentration, but not the full market denominator."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix is the full limitation detail behind the body
      FFATA visibility-gap slide (ddg-s14) and the backup for the supplier landscape slide
      (ddg-s13). It reassures the reader that the deck is not ignoring FFATA: the deck uses FFATA
      for what it can support (supplier names, bucket evidence, concentration), while modeling TAM
      from Basic Construction x a strict supplier coefficient rather than summing visible
      subawards. Mirror the body slide's reserve depth. [tie-out: ffata_visibility_gap (ddg-s14); supplier_landscape (ddg-s13)]

      THE RANGE VIEW (cost_funnel_summary.csv, LI 2122). FFATA-visible cumulative yard-side flow
      is ~$2.73B (~$2,728.6M) against an estimated yard-side outsourcing band: low ~$11.31B
      (~$11,311.4M), midpoint ~$13.57B (~$13,573.7M), high ~$16.16B (~$16,159.2M), all summed
      FY2016-FY2027. Implied visible share at the midpoint is ~$2,728.6M / ~$13,573.7M = 20.1%
      (visible/low 24.1%, visible/high 16.9%, so the band implies ~17-24% visibility). Annualized
      (cumulative / 6 portfolio years): ~$455M/yr visible vs ~$2.26B/yr midpoint. A separate
      recent-rate read is ~15% (~$286M/yr visible vs ~$1.8B/yr yard estimate, range $1.4-2.2B/yr).
      The 20.1% (cumulative cost-funnel) and 15% (recent-rate segment-revenue) are the same order
      of magnitude by design but NOT interchangeable; never put both on one axis. [tie-out: wiki 05, 09]

      WHY VISIBLE UNDERCOUNTS TRUE FLOW (ordered by estimated materiality; wiki 05, 12). (1)
      Purchased material booked as direct material cost - hull steel, prefab piping, reduction
      gears, generators booked under direct-material accounting rather than a subcontract clause;
      estimated ~$400-700M/yr both yards, the single largest invisible category. This is a
      LEGITIMATE cost-accounting-standards treatment, NOT non-compliance. (2) Lower-tier
      subcontracts - FAR 52.204-10 reaches only one tier below the prime, so a sub's sub is
      invisible; broader DIB research adds an estimated 30-50% on top of visible first-tier flow.
      (3) FFATA non-compliance / under-reporting - acute at BIW. (4) Long-term supplier agreements
      not subordinated to the prime (tens of millions per year). (5) The sub-$30,000 long tail (the
      indexed FFATA threshold; was $25,000) - 5-10% of true activity for high-action-count primes.
      (6) Reporting lag of 12-30 months - recent prime obligations undercounted 2-3x, so the
      FY23-27 MYP visible flow is still accumulating as of the May 2026 pull. [tie-out: wiki 05, 12, 16]

      THE BIW vs INGALLS ASYMMETRY (the heart of the caveat). Of the visible flow, ~93% is Ingalls
      (~$2,550M) and only ~7% is BIW (~$178M) - a filing-behavior artifact, not a real-activity
      split. Ingalls reports ~6x denser; on the parallel FY23-27 MYP masters Ingalls shows 493
      published subawards at ~$1,144.5M while BIW's FY23-27 master N00024-23-C-2305 (~$6.4B
      trade-press, ~$5.03B FPDS-obligated) shows ZERO published subawards as of the May 2026 pull -
      a near-certain compliance gap (the FY18-22 BIW master is similarly thin, ~$57M on a $5.3B+
      total). Never generalize one yard's filing behavior to the other. The in-scope visible total
      across all PIIDs is ~$13.84B across 1,954 unique parent vendors. [tie-out: wiki 05, 12]

      SAM.gov IS CANONICAL, NOT USAspending (wiki 05). Both read the same FFATA/FSRS database, but
      USAspending truncates at ~2,500 records per prime PIID (SAM.gov has no cap) and introduces
      derivative artifacts (the $4.2B Thales Nederland ESSM Block 2 NATO cost-share record, which
      is not U.S. Navy DDG spend and which SAM.gov correctly excludes; ~93% of the USAspending
      dollar delta sits in that one record). After backing it out, the net SAM-vs-USAspending delta
      is ~$350M-$1.1B, comparable to ordinary reporting-lag noise. SAM.gov is upstream and is the
      authoritative denominator for this analysis. [tie-out: wiki 05; wiki 16]

      KNOWN PIPELINE CAVEATS (wiki 16). NAICS lookup has a ~35% not-found rate on the top-150
      vendor pool (~$2.28B unclassified across 53 vendors), and NAICS is a corporate-primary code,
      not the work performed. The IVECO MARCORSYSCOM contamination (~$707M of Marine Corps Mk 110
      amphib-gun work on PIID M67854-16-C-0006) is filtered out of the nc_lifetime_vendors view but
      remains in the broader SAM top-parents view; it is a known contamination to be cleaned on a
      future re-run. GAO-25-106286 (Feb 27 2025) generically flags FFATA compliance issues across
      the federal prime base. [tie-out: wiki 06, 16]

      BUILDER GUIDANCE. The evidence ledger is the dominant object; the range cue sits on the right;
      the structural-misses rail is short across the bottom. Do not make the slide read as an
      error-correction page only - the largest gap (direct material) is legitimate accounting. Keep
      cumulative vs annual labels explicit. Two measured native tables; no chart.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3]}
      dense:  {add_bullets: 3, safe_containers: [limitations_rail, range_cue, evidence_table], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Headline gap:"
        body: "Visible ~$2.73B vs ~$13.57B midpoint estimate = ~20.1% visible at midpoint (cumulative basis); a floor, not the denominator."
        evidence: cost_funnel_summary.csv (LI 2122)
        safe_container: range_cue
        density_trigger: Add if the range cue gets a caption.
      - priority: 2
        lead: "Largest invisible category:"
        body: "Purchased material booked as direct material (~$400 to 700M per year) is the biggest unseen layer, and it is legitimate cost-accounting, not non-compliance."
        evidence: wiki 12; wiki 05
        safe_container: limitations_rail
        density_trigger: Add when a reviewer asks what is missing.
      - priority: 3
        lead: "BIW vs Ingalls:"
        body: "~93% of visible flow is Ingalls (~$2,550M), ~7% BIW (~$178M); Ingalls reports ~6x denser, a filing artifact, not real activity."
        evidence: wiki 05; wiki 12
        safe_container: limitations_rail
        density_trigger: Add the asymmetry line if the rail wraps to two lines.
      - priority: 4
        lead: "BIW zero-filing:"
        body: "BIW's FY23-27 MYP master (~$6.4B trade-press) shows zero published subawards as of the May 2026 pull, a near-certain compliance gap."
        evidence: wiki 05; wiki 12
        safe_container: evidence_table
        density_trigger: Add as the vivid single example of under-reporting.
      - priority: 5
        lead: "Lower tiers:"
        body: "FAR 52.204-10 reaches only one tier below the prime; lower-tier subcontracts add an estimated 30 to 50% on top of visible first-tier flow."
        evidence: FAR 52.204-10; wiki 12
        safe_container: evidence_table
        density_trigger: Add in a denser table row.
      - priority: 6
        lead: "Reporting lag:"
        body: "FFATA filings lag 12 to 30 months; recent prime obligations are undercounted 2 to 3x, so the FY23-27 MYP visible flow is still accumulating."
        evidence: wiki 16; wiki 12
        safe_container: limitations_rail
        density_trigger: Add for time-series readers.
      - priority: 7
        lead: "SAM is canonical:"
        body: "SAM.gov FSRS has no per-PIID cap; USAspending truncates at ~2,500 records and adds artifacts (the $4.2B Thales record), so SAM.gov is the authoritative source."
        evidence: wiki 05; wiki 16
        safe_container: evidence_table
        density_trigger: Add if a reviewer asks why USAspending was not used.
      - priority: 8
        lead: "Two bases:"
        body: "The cumulative cost-funnel read is ~20.1%; the recent-rate segment-revenue read is ~15%; same order of magnitude, different bases, never on one axis."
        evidence: wiki 09; wiki 05
        safe_container: range_cue
        density_trigger: Add if a reader cites the ~15% figure and asks why the cue says ~20%.
      - priority: 9
        lead: "NAICS caveat:"
        body: "NAICS is a corporate-primary code, not the work performed; ~35% of top-150 vendors return no NAICS at all (~$2.28B unclassified)."
        evidence: wiki 06; wiki 16
        safe_container: evidence_table
        density_trigger: Add if readers question bucket assignment from NAICS.
      - priority: 10
        lead: "Sub-threshold tail:"
        body: "Actions below the $30,000 FFATA threshold are not reported; for high-action-count primes the tail is an estimated 5 to 10% of true subaward activity."
        evidence: wiki 05; wiki 12
        safe_container: limitations_rail
        density_trigger: Add for a max-density variant of the rail.
      - priority: 11
        lead: "IVECO contamination:"
        body: "~$707M of Marine Corps Mk 110 amphib-gun work (IVECO, PIID M67854-16-C-0006) is filtered from the in-scope vendor view but remains in the broader SAM top-parents view."
        evidence: wiki 06; wiki 16
        safe_container: evidence_table
        density_trigger: Add only for a data-method audit version.
    do_not_add:
      - Annual and cumulative values in the same cue without explicit labels
      - A claim that non-compliance is the only limitation
      - The ~20.1% and ~15% reads mixed on one axis
      - A dense dashboard with multiple competing charts
      - Generalizing BIW's filing behavior to Ingalls or vice versa

data_and_calculations:
  data_inputs:
    - {input: FFATA-visible yard-side flow, value: 2728.6, unit: $M cumulative, year: FY2016-FY2027, tie_out: cost_funnel_summary.csv (LI 2122), used_in: cumulative_range_cue}
    - {input: Estimated yard-side outsourcing low, value: 11311.4, unit: $M cumulative, year: FY2016-FY2027, tie_out: cost_funnel BC-outsourced low, used_in: cumulative_range_cue}
    - {input: Estimated yard-side outsourcing midpoint, value: 13573.7, unit: $M cumulative, year: FY2016-FY2027, tie_out: cost_funnel BC-outsourced mid, used_in: cumulative_range_cue}
    - {input: Estimated yard-side outsourcing high, value: 16159.2, unit: $M cumulative, year: FY2016-FY2027, tie_out: cost_funnel BC-outsourced high, used_in: cumulative_range_cue}
    - {input: Visible share at midpoint, value: 20.1%, unit: percent, year: FY2016-FY2027, tie_out: 2728.6 / 13573.7, used_in: cumulative_range_cue}
    - {input: Annualized midpoint (off-slide), value: 2.26, unit: $B per year, year: FY22-27 average, tie_out: midpoint / 6, used_in: reserve only}
    - {input: Annualized visible flow (off-slide), value: 455, unit: $M per year, year: FY22-27 average, tie_out: visible / 6, used_in: reserve only}
    - {input: In-scope visible total (all PIIDs), value: 13840, unit: $M, year: lifetime, tie_out: wiki 05 (1,954 parents), used_in: reserve context}
  calculations:
    - {name: Visible share at midpoint, formula: 2728.6 / 13573.7, output: 20.1%, used_in: cumulative_range_cue}
    - {name: Visible share range, formula: visible / low and visible / high, output: 24.1% to 16.9%, used_in: reserve}
    - {name: Annualized, formula: cumulative / 6 portfolio years, output: ~$455M/yr visible; ~$2.26B/yr midpoint, used_in: reserve}
  rounding_rules: $B to two decimals in the range cue; percentages to one decimal; cumulative values labeled cumulative.
  reconciliation: FFATA-visible flow is a minority of estimated yard-side outsourcing; the slide labels FFATA as a floor and evidence base, not TAM. The estimated band is triangulated (segment revenue + labor-cost decomposition), not summed from FFATA.

qa:
  guardrails:
    - Slide says FFATA is a floor and evidence base, not TAM.
    - Range cue is labeled cumulative if it uses ~$2.73B and ~$13.57B values.
    - Visible share at midpoint is 20.1% if shown; the ~15% recent-rate read is not mixed onto the same cue.
    - Slide includes structural misses beyond non-compliance (direct material is the largest and is legitimate accounting).
    - BIW ~7% vs Ingalls ~93% asymmetry is not generalized across yards.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal cost_funnel, SAM Build, wiki chapters, or CD IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "no chart on this slide -> chart rId checks do not apply"
    - "if a table exists: resolved column widths sum to its region width"
