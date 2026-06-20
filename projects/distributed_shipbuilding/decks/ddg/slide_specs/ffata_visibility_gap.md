# SlideSpec — DDG ffata_visibility_gap
# Body slide 14. Visible-vs-estimated comparison bar plus five explicit missed-flow
# chips and a pointer-callout chart annotation. No long right bullet rail.

meta:
  slide_id: ddg-s14
  slide_order: 14
  module_name: ffata_visibility_gap.py
  slide_type: body
  section: SAM and Work Types
  archetype: comparison_bar_plus_missed_flow_chips
  story_role: Explain why the deck does not simply sum visible subawards — FFATA first-tier flow is a public evidence floor, while most true yard-side supplier flow sits outside the FFATA-visible stream.
  inputs:
    - z_ChartData CD10_FFATA_GAP
    - extracted/cost_funnel_summary.csv (LI 2122; visible + low/mid/high outsourcing band)
    - Prime Financials / cost-funnel (yard-side outsourcing estimate)
    - SAM Build and Entities (visible subaward flow)
  related_appendix:
    - ddg-a5   # appendix_ffata_limitations (full limitation detail)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Visibility gap
  title_topic: FFATA Visibility Gap
  title_finding: FFATA is evidence, not the market-size denominator
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - HII and General Dynamics Form 10-K filings
    - U.S. BLS OEWS, NAICS 336611
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) HII and General Dynamics Form 10-K filings; (3) U.S. BLS OEWS, NAICS 336611"

story:
  objective: Show the visible FFATA flow against the estimated yard-side outsourcing band and land that visible subawards are a floor (evidence), not the denominator; the deck's TAM does not come from summing FFATA.
  do_not_say:
    - Do not present the visible-share % as a precise figure.
    - Do not mix the cumulative-midpoint read (~20.1%) and the recent-rate read (~15%) on one chart without stating each basis.
    - Do not treat the low-mid-high outsourcing band as precise.
  known_caveats:
    - The exact visible-share % depends on the time basis chosen.
    - BIW under-reports FFATA; Ingalls reports much more richly — do not generalize one yard's filing behavior to the other.
    - Chart values are cumulative FY-summed $M; label them as cumulative unless annualized columns are added.

object_assessment:
  verdict: "Aggressive redesign: keep the comparison bar, but split the explanation rail into real missed-flow chips. The object set must show structural gaps, not bury them in bullets."
  object_contract:
    render_pattern: comparison_bar_plus_missed_flow_chips_and_pointer_callout
    expected_rendered_object_count: 10
    compound_objects:
      - {id: missed_flow_chips, child_count: 5, child_type: text_box_chip}
      - {id: callout_1, child_count: 1, child_type: pointer_callout_overlay}
    required_focal_family: "Visible-flow bar is blue; estimate band is gray; missed-flow chips are light gray, not callouts."
  anti_repetition:
    versus_supplier_landscape: "No supplier evidence table."
    versus_market_direction: "No qualitative timeline table."
    forbidden_defaults:
      - No long right bullet rail.
      - No precision claim around the visible-share percentage.

regions:
  coord_basis: BODY
  layout_pattern: comparison_bar_plus_missed_flow_chips_and_pointer_callout
  title_band:       {x: 0%, y: 0%, w: 62%, h: TITLE_BAND_H}
  chart:            {x: 0%, y: below(title_band), w: 62%, h: body_until(note_strip)}
  missed_title:     {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: TITLE_BAND_H}
  chip_direct:      {x: right_of(chart) + GAP, y: below(missed_title), w: remaining, h: fit_content}
  chip_lower_tier:  {x: right_of(chart) + GAP, y: below(chip_direct) + GAP, w: remaining, h: fit_content}
  chip_agreements:  {x: right_of(chart) + GAP, y: below(chip_lower_tier) + GAP, w: remaining, h: fit_content}
  chip_threshold:   {x: right_of(chart) + GAP, y: below(chip_agreements) + GAP, w: remaining, h: fit_content}
  chip_compliance:  {x: right_of(chart) + GAP, y: below(chip_threshold) + GAP, w: remaining, h: fit_content}
  share_callout:    {x: 13%, y: below(title_band) + GAP, w: 35%, h: fit_content}
  note_strip:       {x: 0%, y: BODY_B - NOTE_H, w: 62%, h: NOTE_H}

element_inventory:
  - {id: e1,  type: exhibit_title, region: title_band,      prominence: tertiary,  paint_order: 1,  content: external chart title}
  - {id: e2,  type: chart_frame,   region: chart,           prominence: primary,   paint_order: 2,  content: visible-vs-estimated-band comparison bar, tie_out: CD10_FFATA_GAP}
  - {id: e3,  type: exhibit_title, region: missed_title,    prominence: tertiary,  paint_order: 3,  content: no-fill title for missed-flow chips}
  - {id: e4,  type: diagram,       region: chip_direct,     prominence: secondary, paint_order: 4,  content: missed-flow chip for direct material}
  - {id: e5,  type: diagram,       region: chip_lower_tier, prominence: secondary, paint_order: 5,  content: missed-flow chip for lower tiers}
  - {id: e6,  type: diagram,       region: chip_agreements, prominence: secondary, paint_order: 6,  content: missed-flow chip for standing agreements}
  - {id: e7,  type: diagram,       region: chip_threshold,  prominence: secondary, paint_order: 7,  content: missed-flow chip for threshold and lag}
  - {id: e8,  type: diagram,       region: chip_compliance, prominence: secondary, paint_order: 8,  content: missed-flow chip for BIW under-reporting}
  - {id: e9,  type: callout,       region: share_callout,   prominence: secondary, paint_order: 9,  content: pointer-callout over visible bar — implied visible share at midpoint}
  - {id: e10, type: note,          region: note_strip,      prominence: tertiary,  paint_order: 10, content: cumulative-basis evidence note}

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
  chart_rules:
    - chart: chart_1
      title_element: e1
      external_title: {size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      native_title: null
      category_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      value_axis_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      data_labels: {size_pt_from: params.value_label_size_pt, color: auto_contrast, font: FONT}
      legend: {enabled: false}
  table_rules: []
  shape_rules:
    - shape: missed_title_1
      element: e3
      profile: external_exhibit_title
      runs:
        - {role: title, size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      note: "Use a no-fill/no-border text_box, left aligned unless the slide explicitly centers the title."
    - shape: chip_direct_1
      element: e4
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: chip_lower_tier_1
      element: e5
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: chip_agreements_1
      element: e6
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: chip_threshold_1
      element: e7
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: chip_compliance_1
      element: e8
      profile: chip_or_step
      runs:
        - {role: cap, size: LABEL_9PT, bold: true, all_caps: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
        - {role: value_if_present, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Use a small cap/body ladder; do not render chip text as one flat run."
    - shape: callout_1
      element: e9
      profile: chart_value_callout
      runs:
        - {role: body, size: MESSAGE_11PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "Pointer/value callout: concise message-size text, not a hero KPI."
    - shape: note_1
      element: e10
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Use no fill/no border; reserve filled treatment for warning/scope-boundary notes only."

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "FFATA-visible yard-side flow (~$2.73B)"
        - "Estimated outsourcing, low (~$11.31B)"
        - "Estimated outsourcing, midpoint (~$13.57B)"
        - "Estimated outsourcing, high (~$16.16B)"
      series:
        - name: Cumulative FY2016-FY2027
          values: [2728.6, 11311.4, 13573.7, 16159.2]
          data_point_colors: [BLUE_5, GRAY_2, GRAY_4, GRAY_2]   # visible = blue (auditable); band = gray (estimate), mid emphasized
    params:
      mode: clustered        # single series; a comparison, not a rank
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 60
      cat_header: Measure
      title: null            # house style: external exhibit_title element (e1)
    external_title:
      text: Cumulative FFATA-visible flow vs estimated yard-side outsourcing, $M
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Implied visible share at midpoint ~20.1%; a floor, not a denominator.", anchor_to: e4}

tables: []

shapes:
  - id: missed_title_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "What public FFATA misses"
    meaning: No-fill title above the missed-flow chips.
  - id: chip_direct_1
    element: e4
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "DIRECT MATERIAL
Booked as direct cost, not a subcontract"
    meaning: Structural miss, not non-compliance.
  - id: chip_lower_tier_1
    element: e5
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "LOWER TIERS
A sub's sub is outside FFATA visibility"
    meaning: Second missed category; explicit chip object.
  - id: chip_agreements_1
    element: e6
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "STANDING AGREEMENTS
Long-term supplier deals may not sit under a prime PIID"
    meaning: Third missed category; explicit chip object.
  - id: chip_threshold_1
    element: e7
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "THRESHOLD AND LAG
Sub-$30,000 actions plus 12-30 month reporting lag"
    meaning: Fourth missed category; explicit chip object.
  - id: chip_compliance_1
    element: e8
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CHIP
    text: "REPORTING GAP
BIW under-reporting is acute but not the whole gap"
    meaning: Fifth missed category; prevents over-framing as pure non-compliance.
  - id: callout_1
    element: e9
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MESSAGE
    text: "Visible flow is ~20.1% of the midpoint estimate on a cumulative basis."
    meaning: Pointer-callout overlay aimed at the visible bar; builder sets tip_x/tip_y after probe.
  - id: note_1
    element: e10
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "FFATA provides public evidence of the supplier base; it does not capture the full true flow. Values are cumulative FY2016-FY2027."
    meaning: One-line evidence-not-denominator reminder and cumulative-basis label.

commentary:
  visible:
    element: e3
    container: right_rail
    title: Why visible is not the full market
    bullets:
      - {lead: "Direct material:", body: "purchased material booked as direct cost, not a subcontract."}
      - {lead: "Lower tiers:", body: "FFATA reaches only one tier below the prime."}
      - {lead: "Standing agreements:", body: "long-term supplier deals not subordinated to the prime."}
      - {lead: "Threshold and lag:", body: "sub-$30,000 actions and 12-30 month reporting lag."}
      - {lead: "Compliance:", body: "under-reporting, acute at BIW."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the credibility hinge of the deck: it explains why TAM
      is modeled (Basic Construction x a strict supplier coefficient) rather than summed
      from FFATA. The exhibit (CD10_FFATA_GAP) compares cumulative FFATA-visible yard-side
      subaward flow ~$2,728.6M against an estimated yard-side outsourcing band — low
      ~$11,311.4M, midpoint ~$13,573.7M, high ~$16,159.2M — all summed FY2016-FY2027 from
      cost_funnel_summary.csv (LI 2122). Implied visible share at the midpoint is
      ~$2,728.6M / ~$13,573.7M = 20.1% (visible/low 24.1%, visible/high 16.9%, so the band
      implies ~17-24% visibility).

      TWO RATIOS, DIFFERENT BASES — DO NOT MIX. The chart's 20.1% is a cumulative,
      cost-funnel-derived ratio (~$455M/yr visible vs ~$2.26B/yr midpoint, each = cumulative
      / 6 portfolio years). The narrative also carries a recent-rate ~15% read (~$286M/yr
      visible vs a segment-revenue yard estimate of ~$1.8B/yr; range $1.4-2.2B/yr). They are
      the same order of magnitude by design but NOT interchangeable — put one on the axis
      and cite the other in prose with its own basis. Avoid the even-lower ~7% "average"
      recent-rate read on this slide.

      WHY VISIBLE UNDERCOUNTS TRUE FLOW (ordered by est. materiality). (1) Purchased
      material booked as direct material — steel plate, prefab piping, reduction gears,
      generators booked under direct-material accounting, not a subcontract clause; the
      largest invisible category (~$400-700M/yr both yards), a legitimate CAS treatment,
      not a gap. (2) Lower-tier subcontracts — FAR 52.204-10 reaches only one tier below
      prime; adds an estimated 30-50%. (3) FFATA non-compliance / under-reporting — acute at
      BIW. (4) Long-term / standing supplier agreements not subordinated to the prime.
      (5) Sub-$30,000 long tail (the indexed FFATA threshold; was $25,000). (6) Reporting
      lag of 12-30 months — recent obligations undercounted 2-3x, so the FY23-27 MYP visible
      flow is still accumulating. [tie-out: wiki 05, 12; appendix_ffata_limitations]

      THE BIW vs INGALLS ASYMMETRY (the heart of the caveat). Of the visible flow, ~93% is
      Ingalls (~$2,550.4M) and only ~7% is BIW (~$178.2M) — a filing-behavior artifact, not
      a real-activity split. Ingalls's FFATA reporting density is ~6x BIW's; on the parallel
      FY23-27 MYP masters it is ~$1,144.5M (Ingalls, 493 subawards) vs ~$0 (BIW). BIW's
      FY23-27 master N00024-23-C-2305 (~$6.4B trade-press / $5.03B FPDS-obligated) carries
      zero published subawards as of the May 2026 pull — a near-certain compliance gap. Never
      generalize one yard's filing behavior to the other. [tie-out: wiki 07, 08; cost_funnel_summary.csv]

      HOW THE OUTSOURCING BAND IS ESTIMATED (segment-revenue triangulation, NOT FFATA).
      Method 1 allocates active-ship revenue scaled to prime 10-K segment disclosure x DDG
      share x yard-side supplier content. Method 2 decomposes labor cost vs BLS NAICS 336611
      wages, leaving materials+subs as a residual. The CD10 low/mid/high bands themselves are
      SCN P-5c Basic Construction dollars x a BC-outsourced coefficient band (~0.83x / 1.0x /
      1.19x). Combined headline ~$1.82B/yr both yards (range $1.4-2.2B/yr); CSIS benchmarks
      supplier content at 65-75%. Emphasize a qualitative read ($1-2B/yr, not $100M or
      $10B). [tie-out: wiki 09, 15]

      DENSITY GUIDANCE. Default is comparison bar + explanation rail + a small implied-share
      callout + a cumulative-basis note. To densify, add the BIW/Ingalls asymmetry line or
      the segment-revenue method to the rail, or expand the note to two lines. Keep the
      visible bar visually distinct (blue) from the gray estimate band at any density, and
      never let the band read as precise.
    density_modes:
      normal: {visible_bullets: 5, keep: [e2, e3, e4, e5]}
      dense:  {add_bullets: 2, safe_containers: [chip_direct, chip_lower_tier, chip_agreements, chip_threshold, chip_compliance, note_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Headline gap:"
        body: "Visible ~$2.73B vs ~$13.57B midpoint estimate = ~20.1% visible; the bars show a floor, not the market."
        evidence: CD10_FFATA_GAP; cost_funnel_summary.csv
        safe_container: note_strip
        density_trigger: Add if the title alone does not carry the gap.
      - priority: 2
        lead: "BIW vs Ingalls:"
        body: "~93% of visible flow is Ingalls (~$2,550M), ~7% BIW (~$178M); Ingalls reports ~6x denser, a filing artifact, not real activity."
        evidence: wiki 07, 08; cost_funnel_summary.csv
        safe_container: rail
        density_trigger: Add the asymmetry line if the rail has room.
      - priority: 3
        lead: "BIW zero-filing:"
        body: "BIW's FY23-27 MYP master (~$6.4B) shows zero published subawards as of the May 2026 pull, a near-certain compliance gap."
        evidence: wiki 07
        safe_container: rail
        density_trigger: Add as the vivid single example of under-reporting.
      - priority: 4
        lead: "Largest invisible category:"
        body: "Purchased material booked as direct material (~$400-700M/yr) is the biggest unseen layer, legitimate CAS accounting, not non-compliance."
        evidence: wiki 12; wiki 05
        safe_container: rail
        density_trigger: Add when a reviewer asks what is missing.
      - priority: 5
        lead: "Annualized:"
        body: "~$455M/yr visible vs ~$2.26B/yr midpoint (each = cumulative / 6 portfolio years)."
        evidence: CD10 derivation
        safe_container: note_strip
        density_trigger: Add only if annualized columns are explicitly added to the chart.
      - priority: 6
        lead: "Two bases:"
        body: "The chart's 20.1% is cumulative cost-funnel; the narrative ~15% is recent-rate segment-revenue, same order of magnitude, different bases; never on one axis."
        evidence: wiki 09; wiki 05
        safe_container: note_strip
        density_trigger: Add if a reader cites the ~15% figure and asks why the chart says 20%.
      - priority: 7
        lead: "Lower tiers:"
        body: "FAR 52.204-10 reaches only one tier below the prime; lower-tier subcontracts add an estimated 30-50% on top of visible first-tier flow."
        evidence: wiki 12; wiki 01
        safe_container: rail
        density_trigger: Add in a max-density variant.
      - priority: 8
        lead: "Reporting lag:"
        body: "FFATA filings lag 12-30 months; recent prime obligations are undercounted 2-3x, so FY23-27 MYP visible flow is still accumulating."
        evidence: wiki 16; wiki 12
        safe_container: rail
        density_trigger: Add to explain why the visible figure will rise.
      - priority: 9
        lead: "Outsourcing intensity:"
        body: "Yard-side outsourcing is ~54% of the Basic Construction layer and ~33% of the FY24 two-ship Total Ship Estimate; ~66% of total ship cost incl. GFE (CSIS 70-80%)."
        evidence: wiki 09; CSIS 2022
        safe_container: note_strip
        density_trigger: Add for an audience sizing the outsourced share of the ship.
      - priority: 10
        lead: "SAM is canonical:"
        body: "SAM.gov (FSRS) has no per-PIID cap; USAspending truncates at ~2,500 records and introduces artifacts, so SAM.gov is the authoritative source."
        evidence: wiki 05; wiki 12
        safe_container: rail
        density_trigger: Add only if a reviewer asks why USAspending was not used.
    do_not_add:
      - a precise single visible-share % presented without its basis
      - the ~20.1% and ~15% reads mixed on one chart
      - the low-mid-high band rendered as precise
      - internal cost_funnel, workbook tabs, or wiki chapters cited in the footer

data_and_calculations:
  data_inputs:
    - {input: FFATA-visible yard-side subaward flow, value: 2728.6,  unit: $M cumulative, tie_out: CD10_FFATA_GAP / cost_funnel_summary.csv, used_in: chart_1}
    - {input: Estimated yard-side outsourcing, low,  value: 11311.4, unit: $M cumulative, tie_out: CD10 / cost_funnel BC-outsourced low, used_in: chart_1}
    - {input: Estimated yard-side outsourcing, mid,  value: 13573.7, unit: $M cumulative, tie_out: CD10 / cost_funnel BC-outsourced mid, used_in: chart_1}
    - {input: Estimated yard-side outsourcing, high, value: 16159.2, unit: $M cumulative, tie_out: CD10 / cost_funnel BC-outsourced high, used_in: chart_1}
  calculations:
    - {name: implied visible share (midpoint), formula: 2728.6 / 13573.7, output: 20.1%, used_in: e4}
    - {name: visible share range, formula: visible / low and visible / high, output: 24.1% to 16.9%, used_in: reserve}
    - {name: annualized, formula: cumulative / 6 portfolio years, output: ~$455M/yr visible; ~$2.26B/yr midpoint, used_in: reserve}
  rounding_rules: Chart values are cumulative $M; ~$B shown in category labels for readability; visible share to one decimal.
  reconciliation: Visible flow and the estimated band are different measures (auditable first-tier vs triangulated total yard-side outsourcing); the gap is the point. TAM is modeled, not summed from the visible bar.

qa:
  guardrails:
    - Slide says FFATA is evidence, not the denominator.
    - Chart labels are clearly cumulative (or annual if annualized columns are added).
    - Visible flow is ~$2.73B cumulative; midpoint estimated outsourcing ~$13.57B cumulative.
    - The implied-share callout is a chart annotation (does not count against the one-filled-callout budget) and names its basis.
    - The estimate band is not presented as precise; BIW/Ingalls asymmetry is not generalized.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal cost_funnel, workbook tabs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    - "pointer-callout overlay named PointerCallout* so the probe classifies it; appended after the graphic_frame (paint order)"
    - "no table on this slide -> table-fit / column-width checks do not apply"
