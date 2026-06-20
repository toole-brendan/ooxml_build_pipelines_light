# SlideSpec — DDG myp_redaction
# Body slide 6. Two-chart correction exhibit (MYP-corrected POP distribution + an
# outside-yards corrected-vs-disclosed-artifact comparison) with two evidence badges and a
# no-fill explanation rail. Defends the denominator correction that prevents the redacted
# multiyear masters from inflating the disclosed-only outside-yards share to an ~87% artifact.

meta:
  slide_id: ddg-s06
  slide_order: 6
  module_name: myp_redaction.py
  slide_type: body
  section: Scope and Denominator
  archetype: two_chart_correction_exhibit_plus_right_rail
  story_role: Defend the most important denominator correction. Restoring the $-redacted FY23-27 multiyear masters shifts the all-gated outside-yards view from the disclosed-only ~87% artifact down to the MYP-corrected ~33%, the share that feeds the BC supplier coefficient.
  inputs:
    - z_ChartData CD04_MYP_POP_CORRECTION (split CD04A_MYP_SITE_DISTRIBUTION + CD04B_MYP_OUTSIDE_YARDS_BRIDGE)
    - TAM Build §3b (outside-yards disclosed artifact vs MYP-corrected) and §3c (all-gated POP site shares)
    - TAM Build §4 (MYP correction; master awards, swing) and §5e (POP removal)
    - POP Source Audit §2 (gated corpus, GFE/Navy-directed scope, MYP masters $)
    - Assumptions §4 (BIW + Ingalls MYP master $ and reconstructed POP %)
  related_appendix:
    - ddg-a3   # appendix_myp_correction (full reconstruction + sensitivity)
    - ddg-a2   # appendix_tam_calculation (where the corrected POP feeds the BC coefficient)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: Denominator correction
  title_topic: MYP Redaction
  title_finding: Restoring the redacted multiyear masters corrects the outside-yards artifact to ~33%
  layout: slideLayout4
  sources:
    - DoD daily contract announcements, war.gov articles 3479250 (Aug. 1, 2023) and 3491276 (Aug. 11, 2023)
    - 41 U.S. Code 2101 et seq. and FAR 2.101 and FAR 3.104
    - U.S. Naval Institute News reporting on the FY23-27 DDG-51 multiyear award
  source_line_exact: "Sources: (1) DoD daily contract announcements, war.gov articles 3479250 (Aug. 1, 2023) and 3491276 (Aug. 11, 2023); (2) 41 U.S. Code 2101 et seq. and FAR 2.101 and FAR 3.104; (3) U.S. Naval Institute News reporting on the FY23-27 DDG-51 multiyear award"

story:
  objective: Explain why the model restores the redacted FY23-27 multiyear master values before using place-of-performance data to estimate outside-yards share, and land that the corrected ~33% (not the ~87% disclosed-only artifact) is what feeds the BC supplier coefficient.
  do_not_say:
    - Do not headline the disclosed-only ~87% outside-yards artifact; show it only as a muted caveat.
    - Do not present the ~32.8% outside-yards share as the 12.5% BC supplier coefficient; they are different quantities.
    - Do not describe the reconstructed master values as directly disclosed dollars; say reconstructed, restored, or folded back.
    - Do not imply the corrected outside-yards POP share alone equals the total supplier TAM.
  known_caveats:
    - The ~87% artifact is the disclosed-only outside-both-yards share (BIW 11.2% plus Ingalls 1.3% inside, so ~87% outside); the 73.6% figure that sometimes appears is only the disclosed Other-US supplier site share, one bucket, not the outside-yards artifact.
    - The masters are POP-disclosed but dollar-redacted; the ~$14.58B is reconstructed from FPDS obligatedAmount plus trade press, not disclosed in the announcement bulletins.
    - The reconstructed masters are folded back before the BC supplier coefficient is computed; the corrected POP feeds the coefficient, it is not the coefficient.

object_assessment:
  verdict: "Keep the correction-lab structure, but stop letting badges compete with the charts. Treat evidence badges as stamps and keep the artifact muted."
  object_contract:
    render_pattern: two_chart_correction_lab_with_evidence_stamps
    expected_rendered_object_count: 9
    compound_objects:
      - {id: chart_1, child_count: 1, child_type: percent_stacked_bar_chart}
      - {id: chart_2, child_count: 1, child_type: muted_artifact_comparison_chart}
    required_focal_family: "Corrected ~33% is blue; artifact is gray; evidence stamps are BLUE_1 with GRAY_3 borders, not hero cards."
  anti_repetition:
    versus_cost_funnel: "Two short correction exhibits, not another denominator bar plus right rail."
    versus_tam_methodology: "This proves the correction; S07 only carries the method formula."
    forbidden_defaults:
      - Do not make the ~87% artifact the largest object.
      - Do not turn evidence stamps into KPI cards.

regions:
  coord_basis: BODY
  layout_pattern: two_chart_correction_exhibit_plus_right_rail
  dist_title:   {x: 0%, y: 0%, w: 65%, h: TITLE_BAND_H}
  dist_chart:   {x: 0%, y: below(dist_title), w: 65%, h: 24%}
  comp_title:   {x: 0%, y: 34%, w: 65%, h: TITLE_BAND_H}
  comp_chart:   {x: 0%, y: below(comp_title), w: 65%, h: 28%}
  badge_master: {x: 0%, y: 74%, w: 31%, h: fit_content}
  badge_corpus: {x: right_of(badge_master) + GAP, y: align_top(badge_master), w: 31%, h: fit_content}
  rail:         {x: right_of(dist_chart) + GAP, y: 0%, w: remaining, h: fit_content}

element_inventory:
  - {id: e1, type: exhibit_title, region: dist_title,   prominence: tertiary,  paint_order: 1, content: external distribution chart title}
  - {id: e2, type: chart_frame,   region: dist_chart,   prominence: primary,   paint_order: 2, content: MYP-corrected POP site distribution (100% bar), tie_out: CD04A / TAM Build §3c}
  - {id: e3, type: exhibit_title, region: comp_title,   prominence: tertiary,  paint_order: 3, content: external comparison chart title}
  - {id: e4, type: chart_frame,   region: comp_chart,   prominence: primary,   paint_order: 4, content: outside-yards MYP-corrected vs disclosed-only artifact comparison, tie_out: CD04B / TAM Build §3b}
  - {id: e5, type: callout,       region: badge_master, prominence: secondary, paint_order: 5, content: reconstructed MYP masters evidence badge (~$14.58B), tie_out: TAM Build §4a / Assumptions §4}
  - {id: e6, type: callout,       region: badge_corpus, prominence: secondary, paint_order: 6, content: gated POP corpus incl. masters evidence badge (~$21.71B), tie_out: POP Source Audit §2}
  - {id: e7, type: rail,          region: rail,         prominence: secondary, paint_order: 7, content: no-fill explanation rail (the correction mechanic)}

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
      legend: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
    - chart: chart_2
      title_element: e3
      external_title: {size: CHART_TITLE_10PT, italic: true, color: DK, font: FONT}
      native_title: null
      category_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      value_axis_labels: {size_pt_from: params.cat_label_size_pt, color: DK, font: FONT}
      data_labels: {size_pt_from: params.value_label_size_pt, color: auto_contrast, font: FONT}
      legend: {enabled: false}
  table_rules: []
  shape_rules:
    - shape: badge_master_1
      element: e5
      profile: evidence_badge
      runs:
        - {role: label, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Badge is a stamp, not a hero KPI card; avoid ANSWER_KPI_24PT."
    - shape: badge_corpus_1
      element: e6
      profile: evidence_badge
      runs:
        - {role: label, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
      note: "Badge is a stamp, not a hero KPI card; avoid ANSWER_KPI_24PT."
    - shape: rail_1
      element: e7
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: body, size: LABEL_9PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0           # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - "Corrected POP distribution"
      series:
        - {name: BIW site,          values: [0.290], data_point_colors: [BLUE_4]}
        - {name: Ingalls site,      values: [0.336], data_point_colors: [BLUE_3]}
        - {name: Other-US supplier, values: [0.315], data_point_colors: [BLUE_5]}
        - {name: Foreign,           values: [0.013], data_point_colors: [GRAY_3]}
        - {name: Unparsed,          values: [0.045], data_point_colors: [GRAY_1]}
    params:
      mode: percent          # single 100% stacked bar of the MYP-corrected site shares
      value_axis_format: '0%'
      show_legend: true
      legend_pos: b
      show_gridlines: false
      show_value_labels: true
      value_label_format: '0.0%'
      value_label_size_pt: 8
      cat_label_size_pt: 9
      gap_width: 35
      cat_header: Distribution
      title: null            # house style: external exhibit_title element (e1)
    external_title:
      text: MYP-corrected place-of-performance distribution
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Outside both yards, the supplier-addressable share, is Other-US 31.5% plus Foreign 1.3% = 32.8%.", anchor_to: e2}
  - id: chart_2
    factory: bar_chart
    chart_index: 1           # -> rId3
    title_element: e3
    frame_element: e4
    data:
      categories:
        - "MYP-corrected"
        - "Disclosed-only artifact, do not headline"
      series:
        - name: Outside-yards share
          values: [0.328, 0.87]
          data_point_colors: [BLUE_5, GRAY_3]   # corrected = emphasized blue; artifact = muted gray
    params:
      mode: ranked
      value_axis_format: '0%'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      show_value_labels: true
      value_label_format: '0.0%'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 50
      cat_header: View
      title: null            # house style: external exhibit_title element (e3)
    external_title:
      text: Outside-yards share after restoring redacted MYP masters
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "The ~87% is a disclosed-only artifact, shown as a caveat; do not headline it.", anchor_to: e4}

tables: []                   # NONE on this slide -> two charts + badges + a rail

shapes:
  - id: badge_master_1
    element: e5
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    insets: INSETS_EVIDENCE
    text: "Reconstructed FY23-27 MYP masters, ~$14.58B"
    meaning: Evidence badge; makes the denominator restoration concrete (BIW ~$6.40B plus Ingalls ~$8.18B) without overloading the chart.
  - id: badge_corpus_1
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: BLACK
    insets: INSETS_EVIDENCE
    text: "Gated POP corpus incl. masters, ~$21.71B"
    meaning: Evidence badge for the corrected gated corpus the distribution is computed over.
  - id: rail_1
    element: e7
    factory: text_box        # no-fill commentary rail (slide_guide -> no-fill commentary)
    fill: null
    line_color: null
    insets: INSETS_MESSAGE
    text:
      title: What changed
      bullets:
        - "The FY23-27 BIW and Ingalls multiyear masters disclose work locations but redact dollar values."
        - "Those masters are large and yard-heavy, so omitting their dollars over-weights the disclosed GFE actions."
        - "The model restores ~$14.58B of master value before applying the Basic Construction supplier coefficient."
        - "Use the corrected ~33% outside-yards view going forward, not the disclosed-only artifact."
    meaning: No-fill explanation rail; title and rail emphasize the corrected view, not the artifact.

images: []

commentary:
  visible:
    element: e7
    container: right_rail
    title: What changed
    bullets:
      - {lead: "Problem:", body: "the FY23-27 masters disclose place-of-performance but redact dollar values."}
      - {lead: "Correction:", body: "restoring ~$14.58B of master value stops GFE-heavy disclosed actions from overstating outside-yards share."}
      - {lead: "Read:", body: "use the corrected ~33% outside-yards view; keep the ~87% as a muted caveat."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the most important denominator-correction slide and a
      methodological guardrail. The scope ledger and cost funnel (S5) establish what the deck
      sizes; this slide defends why the model does NOT simply use the disclosed DoD-announcement
      outside-yards share. The correction is structurally unique to the destroyer two-yard
      competitive procurement and has no parallel in the submarine analysis. [tie-out: wiki 12, 01, 04]

      THE REDACTION (wiki 12; wiki 04). The two FY23-27 DDG-51 multiyear master awards - BIW
      PIID N00024-23-C-2305 (war.gov 3479250, Aug 1 2023) and Ingalls PIID N00024-23-C-2307
      (war.gov 3491276, Aug 11 2023) - carry the standard source-selection-sensitive redaction
      under 41 U.S. Code 2101 et seq. and FAR 2.101 / 3.104: the dollar values "will not be made
      public at this time." The bulletins DO disclose place-of-performance percentages (BIW
      master ~69% Bath ME; Ingalls master ~77% Pascagoula MS) but leave the dollar field empty.
      The two-yard competitive structure triggers the designation; single-prime submarine,
      carrier, and frigate masters disclose their dollars. [tie-out: wiki 12]

      THE ARTIFACT (the heart of the slide; wiki 04, 12; TAM Build §3b). On the disclosed-only
      DoD-announcement corpus (152 supplier-TAM-relevant actions, ~$7.13B), the dollar-weighted
      POP is BIW 11.2%, Ingalls 1.3%, Other-US 73.6%, Foreign ~0%, with ~14% unparsed residual.
      Inside-yards is 11.2% + 1.3% = 12.5%, so outside-both-yards is ~87% (the ~86.1% live raw
      figure rounds to ~87%). That ~87% is an ARTIFACT: because the two $-redacted masters carry
      zero dollars in the aggregation, the smaller disclosed GFE-heavy actions (Aegis at
      Moorestown NJ, SPY-6 at Andover MA) dominate the dollar weight and push the outside-yards
      share up. GUARDRAIL: the 73.6% is the disclosed Other-US SUPPLIER site share (one bucket),
      NOT the outside-yards artifact - do not conflate them; the outside-yards artifact is ~87%.
      [tie-out: wiki 04 (aggregate distribution); TAM Build §3b myp_disc]

      THE CORRECTION MECHANIC (TAM Build §4; POP Source Audit §2). The model reconstructs the
      ~$14.58B of master value (BIW ~$6.40B, Ingalls ~$8.18B; Assumptions §4 carries 6400 and
      8180) from FPDS obligatedAmount plus trade-press totals (USNI, Defense Daily), allocates it
      to POP classes by the reconstructed POP % on Inputs (BIW master 86% BIW-site / 12% other-US
      / 2% foreign; Ingalls master 88% Ingalls-site / 10% other-US / 2% foreign), and folds those
      two master rows back into the gated POP corpus BEFORE computing the all-gated outside-yards
      share. FPDS-obligated on the BIW master was ~$5.03B at the May 2026 pull, below the ~$6.40B
      ceiling - the gap is yet-to-be-obligated option value, which is why the trade-press total is
      used. [tie-out: wiki 12; TAM Build §4a; Assumptions §4]

      NUMERIC RESULT (TAM Build §3c, §3b; POP Source Audit §2). The gated POP corpus including
      masters is ~$21.71B; ~$6.12B of GFE / Navy-directed scope is dropped from the gated view.
      The MYP-corrected all-gated site distribution is BIW 29.0%, Ingalls 33.6%, Other-US 31.5%,
      Foreign 1.3%, Unparsed 4.5% (sums to 100.0%). Outside both yards = Other-US 31.5% + Foreign
      1.3% = 32.8%, the MYP-corrected outside-yards share. It ties to the §3e anchor target of
      0.33 (the 0.33 anchor; live ~32.8%) and is consistent with the wiki 09 reading that the
      yards self-perform on the order of 33% of total ship cost. [tie-out: TAM Build §3c, §3e]

      WHAT TRAVELS FORWARD (TAM Build §3a). The corrected outside-yards POP feeds the BC supplier
      coefficient: the applied BC supplier coefficient is 12.5% (MYP-corrected other-US + foreign
      POP share over the NON-GFE BC corpus, masters folded back). GUARDRAIL: the ~32.8% all-gated
      outside-yards share is NOT the 12.5% coefficient - the coefficient is measured over the
      non-GFE BC corpus only, a different (and smaller) base, so the two figures differ. Never
      present ~32.8% or ~87% as the coefficient. The corrected POP share alone is not the total
      TAM either; TAM = BC base x coefficient + the AP and LLTM stream. [tie-out: TAM Build §3a, §5]

      HOW TO PRESENT. This is a denominator correction, not an argument about whether outsourcing
      is large or small. The reader should take away that the corrected ~33% (not the ~87%
      artifact) is the defensible figure, and that it feeds the BC supplier coefficient. Use
      "reconstructed," "restored," or "folded back," never "directly disclosed dollars." Keep the
      ~87% artifact bar muted and explicitly labeled as a disclosed-only artifact. [tie-out: wiki 12]
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e4, e5, e6, e7]}
      dense:  {add_bullets: 5, safe_containers: [rail, badge_master, badge_corpus, comp_chart], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Corrected value:"
        body: "The MYP-corrected outside-yards share is ~32.8% (the 0.33 anchor); this travels forward into the BC supplier coefficient, not the disclosed-only ~87% artifact."
        evidence: TAM Build §3b, §3e
        safe_container: rail
        density_trigger: Add if the comparison-chart label is removed.
      - priority: 2
        lead: "Reconstruction:"
        body: "The model restores ~$14.58B of FY23-27 master value (BIW ~$6.40B, Ingalls ~$8.18B) before computing outside-yards share."
        evidence: TAM Build §4a; Assumptions §4
        safe_container: badge_master
        density_trigger: Add in a denser badge row.
      - priority: 3
        lead: "Corpus scale:"
        body: "The gated POP corpus including the masters is ~$21.71B, of which ~$6.12B of GFE and Navy-directed scope is dropped from the gated view."
        evidence: POP Source Audit §2
        safe_container: badge_corpus
        density_trigger: Add if the badge row has two-line capacity.
      - priority: 4
        lead: "Artifact caveat:"
        body: "The disclosed-only outside-yards share is ~87% (BIW 11.2% plus Ingalls 1.3% inside = 12.5%); it is a redaction artifact, not the final figure and not the coefficient."
        evidence: wiki 04; TAM Build §3b
        safe_container: comp_chart
        density_trigger: Add if a reviewer focuses on the longer bar.
      - priority: 5
        lead: "Not the 73.6%:"
        body: "The 73.6% is the disclosed Other-US supplier site share, one bucket, not the outside-yards artifact; the outside-yards artifact is ~87%."
        evidence: wiki 04 (aggregate distribution)
        safe_container: rail
        density_trigger: Add if a reader cites 73.6% as the artifact.
      - priority: 6
        lead: "Site distribution:"
        body: "Corrected POP distribution is BIW 29.0%, Ingalls 33.6%, Other-US supplier 31.5%, Foreign 1.3%, Unparsed 4.5%."
        evidence: TAM Build §3c / CD04A
        safe_container: dist_chart
        density_trigger: Add if the 100% bar cannot show labels clearly.
      - priority: 7
        lead: "Not the coefficient:"
        body: "The ~32.8% all-gated outside-yards share is not the 12.5% BC supplier coefficient; the coefficient is measured over the non-GFE BC corpus, a different base."
        evidence: TAM Build §3a, §3b
        safe_container: rail
        density_trigger: Add if a reviewer conflates the two percentages.
      - priority: 8
        lead: "Why redacted:"
        body: "The two-yard competitive multiyear triggers source-selection sensitivity (FAR 2.101 and 3.104); single-prime submarine and carrier masters disclose their dollars."
        evidence: wiki 12; wiki 01
        safe_container: rail
        density_trigger: Add when the audience asks why only destroyers have this caveat.
      - priority: 9
        lead: "Recovery basis:"
        body: "The ~$14.58B is reconstructed from FPDS obligatedAmount plus trade press (USNI, Defense Daily); FPDS-obligated on the BIW master was ~$5.03B at the May 2026 pull, below the ~$6.40B ceiling."
        evidence: wiki 12 (FPDS cross-reference)
        safe_container: badge_master
        density_trigger: Add in a method-heavy variant.
      - priority: 10
        lead: "Ties to ship cost:"
        body: "The corrected ~33% is consistent with the chapter-9 reading that the yards self-perform on the order of 33% of total ship cost at the FY24 two-ship buy."
        evidence: wiki 09; wiki 12
        safe_container: rail
        density_trigger: Add for an audience sizing the self-performed share of the ship.
    do_not_add:
      - the disclosed-only ~87% (or 73.6%) presented as a headline rather than a muted caveat
      - any statement that the reconstructed dollars were directly disclosed in the announcements
      - the ~32.8% outside-yards share presented as the 12.5% BC supplier coefficient
      - internal workbook tabs, CD IDs, or wiki chapters in rendered sources
      - a claim that the corrected POP share alone equals the total supplier TAM

data_and_calculations:
  data_inputs:
    - {input: Reconstructed FY23-27 MYP masters (combined), value: 14.58, unit: $B, tie_out: TAM Build §4a / Assumptions §4 (6400 + 8180), used_in: badge_master_1}
    - {input: BIW MYP master, value: 6.40, unit: $B, tie_out: Assumptions §4 (6400), used_in: reserve}
    - {input: Ingalls MYP master, value: 8.18, unit: $B, tie_out: Assumptions §4 (8180), used_in: reserve}
    - {input: Gated POP corpus including masters, value: 21.71, unit: $B, tie_out: POP Source Audit §2 (gated $), used_in: badge_corpus_1}
    - {input: GFE and Navy-directed scope dropped, value: 6.12, unit: $B, tie_out: POP Source Audit §2 (gfe-excluded $), used_in: reserve}
    - {input: Outside-yards POP, MYP-corrected, value: 32.8, unit: percent, tie_out: TAM Build §3b myp_corr / §3e anchor 0.33, used_in: chart_2}
    - {input: Outside-yards POP, disclosed-only artifact, value: 87, unit: percent, tie_out: TAM Build §3b myp_disc (~87%) / wiki 04, used_in: chart_2}
    - {input: BIW site share (corrected), value: 29.0, unit: percent, tie_out: TAM Build §3c / CD04A, used_in: chart_1}
    - {input: Ingalls site share (corrected), value: 33.6, unit: percent, tie_out: TAM Build §3c / CD04A, used_in: chart_1}
    - {input: Other-US supplier share (corrected), value: 31.5, unit: percent, tie_out: TAM Build §3c / CD04A, used_in: chart_1}
    - {input: Foreign share (corrected), value: 1.3, unit: percent, tie_out: TAM Build §3c / CD04A, used_in: chart_1}
    - {input: Unparsed share (corrected), value: 4.5, unit: percent, tie_out: TAM Build §3c / CD04A, used_in: chart_1}
  calculations:
    - {name: Master reconstruction, formula: "BIW master 6.40 plus Ingalls master 8.18", output: "~$14.58B", used_in: badge_master_1}
    - {name: Corrected outside-yards view, formula: "Other-US 31.5% plus Foreign 1.3% over the MYP-restored all-gated corpus", output: "32.8%", used_in: chart_2}
    - {name: Disclosed-only artifact, formula: "100% minus inside-yards (BIW 11.2% plus Ingalls 1.3% = 12.5%) on the disclosed-only corpus", output: "~87%", used_in: chart_2}
  rounding_rules: Dollar badges round to two decimals in $B; shares show one decimal except the title headline rounds to ~33%; the disclosed-only artifact is rounded to ~87%.
  reconciliation: The corrected site distribution sums to 100.0% (BIW 29.0 + Ingalls 33.6 + Other-US 31.5 + Foreign 1.3 + Unparsed 4.5). Outside both yards (Other-US 31.5% + Foreign 1.3% = 32.8%) is the MYP-corrected outside-yards share and ties to the §3e anchor 0.33. The ~87% disclosed-only artifact is a different measure (masters carry zero dollars), shown only as a caveat. Neither percentage is the 12.5% BC supplier coefficient, which is measured over the non-GFE BC corpus.

qa:
  guardrails:
    - Slide title headlines the corrected ~33%, not the artifact.
    - The disclosed-only artifact bar shows ~87% (NOT 73.6%), is muted, and is explicitly labeled a disclosed-only artifact.
    - The ~32.8% outside-yards share is never presented as the 12.5% BC supplier coefficient.
    - The ~$14.58B reconstruction (BIW ~$6.40B, Ingalls ~$8.18B) and ~$21.71B gated corpus appear as small evidence badges.
    - Reconstructed masters are described as reconstructed / restored / folded back, never directly disclosed dollars.
    - The chart does not imply the corrected POP share alone equals the total supplier TAM.
  source_checks:
    - Sources are the exact real citations in chrome.sources (DoD announcements, FAR / 41 U.S. Code, USNI); no internal workbook tabs, CD IDs, or wiki chapters rendered.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2, chart_2 chart_index 1 -> rId3)"
    - "pointer / annotation overlays appended after their graphic_frame (paint order)"
    - "no table on this slide -> table-fit / column-width checks do not apply"
