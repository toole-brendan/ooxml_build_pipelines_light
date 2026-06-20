# SlideSpec — DDG supplier_landscape
# Body slide 13. Ranked bar of the top visible first-tier suppliers plus a native
# chart-side evidence table. Names only; no logos and no generic caveat rail.

meta:
  slide_id: ddg-s13
  slide_order: 13
  module_name: supplier_landscape.py
  slide_type: body
  section: SAM and Work Types
  archetype: top_supplier_ranked_bar_plus_evidence_table
  story_role: Add market texture and credibility by showing the visible first-tier supplier landscape — a concentrated set of specialized defense manufacturers, not a generic industrial pool — while making clear this is the visible floor, not the full market.
  inputs:
    - Vendors tab data_vendors.tbl_ddg_top_vendors (parent-level lifetime visible flow)
    - extracted/nc_lifetime_vendors.csv (cleaned, contaminants removed)
    - z_ChartData CD09_TOP_SUPPLIERS (bucket-split; see guardrails — NOT the chart source)
    - Source Index sources_source_index (nc_lifetime_vendors, entity NAICS inputs)
  related_appendix:
    - ddg-a6   # appendix_bucket_rules_supplier_evidence (bucket-level supplier examples)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Supplier landscape
  title_topic: Supplier Landscape
  title_finding: Visible supplier flow is concentrated among specialized defense manufacturers
  layout: slideLayout4
  sources:
    - SAM.gov Acquisition Subaward Reporting Public API
    - SAM.gov Entity Management API
    - FAR 52.204-10
  source_line_exact: "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

story:
  objective: Rank the top visible first-tier suppliers by lifetime flow and frame them as a concentrated landscape of specialized manufacturers, engineering-services firms, and GFE-adjacent suppliers — evidence of the visible base, not the full true market.
  do_not_say:
    - Do not imply these suppliers are the only target companies.
    - Do not imply visible subawards equal the market denominator.
    - No company logos; supplier names only.
  known_caveats:
    - This is a landscape read, not a TAM sizing slide.
    - Some parent names blend product, service, and prime-related activity (Arctic Slope = engineering services; General Dynamics = prime-affiliated).
    - '"Foreign" is country of incorporation, not work location (Leonardo does DDG work at U.S. DRS sites).'
    - The chart must be sourced from the parent-level Vendors tab, NOT z_ChartData CD09 (which is bucket-split and drops GFE/prime-named firms).

object_assessment:
  verdict: "Aggressive redesign: replace the generic caveat rail with a native evidence table. A supplier landscape needs auditable categories/caveats, not another right bullet column."
  object_contract:
    render_pattern: top_supplier_ranked_bar_plus_evidence_table
    expected_rendered_object_count: 4
    compound_objects: []
    required_focal_family: "Chart ranks the top suppliers; evidence table classifies role and caveat. Names only, no logos."
  anti_repetition:
    versus_sam_scenarios: "This table is supplier evidence, not scenario membership."
    versus_ffata_visibility_gap: "S14 uses missed-flow chips, not a supplier table."
    forbidden_defaults:
      - No logos.
      - No generic rail.
      - Do not source from bucket-split CD09 unless retitling the chart.

regions:
  coord_basis: BODY
  layout_pattern: top_supplier_ranked_bar_plus_evidence_table
  title_band:     {x: 0%, y: 0%, w: 63%, h: TITLE_BAND_H}
  chart:          {x: 0%, y: below(title_band), w: 63%, h: body_until(note_strip)}
  evidence_table: {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip:     {x: 0%, y: BODY_B - NOTE_H, w: 63%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band,     prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,          prominence: primary,   paint_order: 2, content: ranked horizontal bar of top-10 visible suppliers by lifetime flow, tie_out: Vendors tab}
  - {id: e3, type: table,         region: evidence_table, prominence: secondary, paint_order: 3, content: supplier-role evidence table with caveats; replaces generic rail}
  - {id: e4, type: note,          region: note_strip,     prominence: tertiary,  paint_order: 4, content: visible-floor reminder under the chart}

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
  table_rules:
    - table: supplier_evidence_1
      element: e3
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: note_1
      element: e4
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
        - "Leonardo SpA"
        - "Arctic Slope Regional Corp"
        - "Major Tool and Machine"
        - "General Dynamics Corp"
        - "General Electric Co"
        - "Rolls-Royce Holdings plc"
        - "Northrop Grumman Corp"
        - "Johnson Controls Navy Systems"
        - "Advanced Sciences and Technologies"
        - "CAES Systems LLC"
      series:
        - name: Lifetime visible flow
          values: [1810.3, 987.4, 816.1, 372.0, 335.6, 257.2, 249.3, 178.2, 174.0, 169.2]
          data_point_colors: [BLUE_5, BLUE_4, BLUE_4, BLUE_3, BLUE_3, BLUE_2, BLUE_2, BLUE_1, BLUE_1, BLUE_1]
    params:
      mode: ranked          # single pre-sorted series; bar_chart reads top-to-bottom
      value_axis_format: '"$"#,##0"M"'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '"$"#,##0"M"'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 40
      cat_header: Supplier (parent)
      title: null           # house style: external exhibit_title element (e1)
    external_title:
      text: Top visible first-tier suppliers by lifetime flow, $M
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations: []

tables:
  - id: supplier_evidence_1
    element: e3
    role: chart_side_evidence
    factory: house_table
    semantic:
      table_name: Supplier role and caveat cue
      purpose: classify
      reader_takeaway: Top visible suppliers include product manufacturers, services, and prime-affiliated parents; the chart is a floor, not a target list.
      row_order: highest-risk interpretation caveats first
      highlight_rows: []
      guardrails:
        - Names only, no logos.
        - Parent-level Vendors tab, not bucket-split CD09.
        - Evidence table is not a target-account list.
    render:
      table_skin: rule
      size: 850
      column_widths:
        mode: ratio
        values: [1.4, 1.4, 2.6]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Example", "Role", "Caveat"]
        - ["Leonardo via DRS", "Electrical and VLS", "Foreign parent, U.S. work sites"]
        - ["Arctic Slope", "Engineering services", "Not a pure component manufacturer"]
        - ["Major Tool", "Machining", "Clean physical-components proof point"]
        - ["General Dynamics", "Prime-affiliated", "Do not read as third-party wedge"]
        - ["GE and Rolls-Royce", "Propulsion", "Visible flow can understate vertical integration"]
      cell_fills: {}
      cell_bold: {}
      cell_text_colors: {}
      footnotes:
        - "Supplier evidence is visible first-tier parent flow; a floor, not the full supplier base."
    columns: []

shapes:
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Lifetime visible first-tier subaward flow per parent vendor; a floor, not the full supplier base. Names only, no logos."
    meaning: One-line visible-floor reminder beneath the chart.

commentary:
  visible:
    element: e3
    container: right_rail
    title: Evidence caveats
    bullets:
      - {lead: "Visible only:", body: "first-tier FFATA flow, not the full true market."}
      - {lead: "Mixed roles:", body: "some parent names blend product, service, and prime-related activity."}
      - {lead: "Aggregate parents:", body: "clean duplicate name variants; avoid bucket-split rows."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It follows the SAM scenarios (S12) and adds supplier
      texture before the FFATA visibility gap (S14) explains why visible flow is only a
      floor. It is a landscape read, NOT a sizing slide — the bars are lifetime visible
      first-tier subaward flow per parent vendor, not TAM and not a target list.

      SOURCE DISCIPLINE (the load-bearing build decision). Source the ranked bars from
      the parent-level Vendors tab (data_vendors.tbl_ddg_top_vendors, driven by
      nc_lifetime_vendors.csv), NOT z_ChartData CD09_TOP_SUPPLIERS. CD09 is built from
      Entity Master top_supplier_indices(12), which is aggregated one row per
      (vendor, UEI, role, bucket): the same parent repeats by bucket, dollars are
      per-bucket exposure rather than parent lifetime totals, and any GFE/MIB-named
      (Lockheed, Raytheon, BAE, L3Harris, Northrop Grumman Systems) or prime-named
      (GD/BIW/Ingalls) firm is dropped by the role=="supplier" filter. If a builder uses
      CD09 as-is, the chart answers a different question and must be retitled "Top
      supplier-bucket exposures." [tie-out: chartdata_z_chart_data.py; data_entity_master.py]

      THE TOP SUPPLIERS AND THEIR CAVEATS.
      - Leonardo SpA ~$1.81B — entirely via U.S. subsidiary DRS: Mk 41 VLS canister/
        launcher-cell module work, Aegis hardware, CEC. Foreign parent (Italy) does NOT
        mean foreign work location; DRS plants are U.S. (Bridgeport CT, Beavercreek OH,
        Largo FL, Adelphi MD). SAM NAICS (336411) is a corporate-primary miscode.
      - Arctic Slope Regional Corp ~$987M — Alaska Native Regional Corp; largely Aegis
        engineering-services labor (~$437M on one CSEA PIID), NOT physical components.
        Caveat hard for a components-focused read.
      - Major Tool and Machine ~$816M — Indianapolis large-precision machining; Mk 41 VLS
        launcher-cell module mechanical structure. A clean physical-components proof.
        Duplicate filer UEI adds ~$132M (consolidated ~$948M) — clean before charting.
      - General Dynamics Corp ~$372M — prime/affiliated blend: GD Mission Systems is the
        SPY-6 receiver/exciter sub, but GD is also a destroyer prime (BIW). Do not read as
        a third-party supplier wedge; the SAM "foreign" flag on GD is a filer artifact, not
        real (GD is U.S.-domiciled).
      - General Electric ~$336M (LM2500 propulsion; GE's deep vertical integration
        suppresses visible subawards), Rolls-Royce ~$257M (gas-turbine/mechanical power;
        duplicate UEI -> ~$312M consolidated), Northrop Grumman ~$249M (SPY-6 sub-assembly,
        SEWIP, AN/SPQ-9B; name maps to gfe_mib so it is excluded from CD09), Johnson
        Controls Navy Systems ~$178M (HVAC), Advanced Sciences and Technologies ~$174M
        (Aegis engineering services — another services caveat), CAES Systems ~$169M
        (= Cobham Advanced Electronic Solutions; SPY-6 RF — reconcile so CAES and Cobham
        are not double-listed).

      WHY ELECTRONICS AND COMBAT-SYSTEM FIRMS DOMINATE. Aegis (LM Moorestown) + SPY-6
      (Raytheon Andover) account for ~70% of the supplier-TAM-relevant corpus; SPY-6's
      top-3 subs (GD Mission Systems, CAES, Northrop Grumman) are ~46% of its production
      PIID, and Mk 41 VLS is dominated by Leonardo/DRS + Major Tool. Several parents'
      lifetime totals also include WPN-funded CIWS subawards that sit OUTSIDE the SCN TAM
      gate — a footnote so bar magnitudes are not read as pure SCN-scope. [tie-out: wiki 10, 11]

      CONCENTRATION AND VISIBILITY. Top-25 parent UEIs ~53% of the ~$13.84B in-scope
      visible flow; top-10 ~34%. Moderately concentrated (HHI on top-150 ~600-800) —
      broader than the submarine base. Effective foreign-vendor share is ~0% by work
      location. ~35% of top-150 vendors return no NAICS in SAM Entity Management (~$2.28B
      unclassified), and NAICS is a corporate-primary code, not the work performed. The
      whole picture is a visible FLOOR: FFATA captures only ~15-20% of real yard-side
      outsourcing (S14). [tie-out: wiki 05, 06]

      DENSITY GUIDANCE. Default is chart + caveat rail + one-line floor note. To densify,
      add a tenure/concentration line to the rail or a small footnote under the chart.
      Keep caveat language visible but not dominant; the chart owns the page.
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e3, e4]}
      dense:  {add_bullets: 2, safe_containers: [evidence_table, note_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Concentration:"
        body: "Top-25 parents ~53% of ~$13.84B visible in-scope flow; top-10 ~34%, moderately concentrated, broader than the submarine base."
        evidence: wiki 06 (concentration); wiki 05 (top recipients)
        safe_container: rail
        density_trigger: Add a line to the rail if it has vertical room.
      - priority: 2
        lead: "Foreign != foreign work:"
        body: "Leonardo (Italy) is #1 but does DDG work at U.S. DRS sites; effective foreign-vendor share by work location is ~0%."
        evidence: wiki 06 (geographic distribution)
        safe_container: rail
        density_trigger: Add if a reader flags the foreign-parent at the top of the chart.
      - priority: 3
        lead: "Services vs components:"
        body: "Arctic Slope (~$987M) and Advanced Sciences (~$174M) are largely engineering services, not physical components, caveat for a components read."
        evidence: wiki 06; wiki 10
        safe_container: note_strip
        density_trigger: Add when the audience is focused on physical-component suppliers.
      - priority: 4
        lead: "Why electronics lead:"
        body: "Aegis (LM) + SPY-6 (Raytheon) are ~70% of the supplier-TAM-relevant corpus; the visible top is combat-system electronics, not hull fabrication."
        evidence: wiki 10 (Aegis/SPY-6)
        safe_container: note_strip
        density_trigger: Add to explain why metal-fab names are not at the very top.
      - priority: 5
        lead: "NAICS caveat:"
        body: "NAICS is a corporate-primary code, not the work performed; ~35% of top-150 vendors return no NAICS at all (~$2.28B unclassified)."
        evidence: wiki 06 (NAICS coverage gap); Entity NAICS lookup
        safe_container: note_strip
        density_trigger: Add if a reviewer reads NAICS labels as the work type.
      - priority: 6
        lead: "Duplicate-UEI cleanup:"
        body: "Major Tool (~$816M + ~$132M) and Rolls-Royce (~$257M + ~$55M) each file under two UEIs; consolidate to ~$948M and ~$312M for a parent read."
        evidence: nc_lifetime_vendors.csv
        safe_container: rail
        density_trigger: Add if presenting consolidated parent totals.
      - priority: 7
        lead: "CIWS contamination:"
        body: "Some lifetime totals include WPN-funded CIWS subawards that sit outside the SCN TAM gate (e.g. Leonardo/DRS ~$141M, GD ~$90M); the bars are lifetime visible flow, not pure SCN-scope."
        evidence: wiki 11 (CIWS)
        safe_container: note_strip
        density_trigger: Add if the magnitudes are compared to SCN-scope TAM.
      - priority: 8
        lead: "CD09 is not parent-level:"
        body: "z_ChartData CD09 is bucket-split and drops GFE/prime-named firms; the parent-level Vendors tab is the correct source for this ranking."
        evidence: chartdata_z_chart_data.py; data_entity_master.py
        safe_container: rail
        density_trigger: Add as a method note if a reviewer asks where the ranking comes from.
      - priority: 9
        lead: "GFE-prime is the real concentration:"
        body: "Five GFE primes (LM, Raytheon, BAE, GE, Northrop Grumman) hold most supplier-TAM value; the supplier tier under each is only moderately concentrated."
        evidence: wiki 06 (concentration)
        safe_container: note_strip
        density_trigger: Add for an audience focused on where market power sits.
    do_not_add:
      - company logos (names only)
      - any claim that these are the only target companies
      - any claim that visible subawards equal the market denominator
      - reading NAICS labels as the work performed

data_and_calculations:
  data_inputs:
    - {input: Leonardo SpA (via DRS),                 value: 1810.3, unit: $M lifetime, tie_out: Vendors tab / nc_lifetime_vendors.csv, used_in: chart_1}
    - {input: Arctic Slope Regional Corp,             value: 987.4,  unit: $M lifetime, tie_out: Vendors tab, used_in: chart_1}
    - {input: Major Tool and Machine,                 value: 816.1,  unit: $M lifetime, tie_out: Vendors tab (single UEI; consolidated ~947.9), used_in: chart_1}
    - {input: General Dynamics Corp,                  value: 372.0,  unit: $M lifetime, tie_out: Vendors tab (prime-affiliated), used_in: chart_1}
    - {input: General Electric Co,                    value: 335.6,  unit: $M lifetime, tie_out: Vendors tab, used_in: chart_1}
    - {input: Rolls-Royce Holdings plc,               value: 257.2,  unit: $M lifetime, tie_out: Vendors tab (single UEI; consolidated ~312.0), used_in: chart_1}
    - {input: Northrop Grumman Corp,                  value: 249.3,  unit: $M lifetime, tie_out: Vendors tab, used_in: chart_1}
    - {input: Johnson Controls Navy Systems,          value: 178.2,  unit: $M lifetime, tie_out: Vendors tab, used_in: chart_1}
    - {input: Advanced Sciences and Technologies,     value: 174.0,  unit: $M lifetime, tie_out: Vendors tab (services), used_in: chart_1}
    - {input: CAES Systems LLC,                        value: 169.2,  unit: $M lifetime, tie_out: Vendors tab (= Cobham AES), used_in: chart_1}
  rounding_rules: Whole $M on the slide; values are lifetime visible first-tier flow per parent vendor.
  reconciliation: Bars are NOT additive to TAM and are not expected to sum to it; lifetime flow spans FYs and appropriations (incl. some WPN-funded CIWS) outside the SCN TAM gate.

qa:
  guardrails:
    - The slide clearly states this is visible first-tier flow only, not the full true market.
    - Chart is parent-level (Vendors tab), or retitled "Top supplier-bucket exposures" if CD09 is used as-is.
    - Duplicate parent name variants (Major Tool, Rolls-Royce) are cleaned or caveated; CAES and Cobham are not double-listed.
    - No company logos.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal CSVs, workbook tabs, or chart IDs rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)"
    - "slide_probe --table-fit   # optional: estimated table row-height info
    - resolved column widths sum to the evidence_table region width"
