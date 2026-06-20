# SlideSpec - submarines `coefficient_evidence` (deck slide 10)
# Chart-plus-table body slide: a three-bar coefficient ladder on the left (all-gated POP
# anchor 51.8%, AP and LLTM reference 48.5%, applied BC supplier 35.0%) with the applied
# bar highlighted darkest, ONE compact native evidence table (metric/value rows) on the
# right, and a headline read line plus a bottom guardrail strip. This is the POP-evidence
# slide: it proves the supplier coefficient is evidence-based while keeping only the strict
# 35.0% Basic Construction coefficient in the headline math. The detailed POP-corpus
# evidence CARDS live in appendix A4; this slide de-duplicates to a single compact table.

meta:
  slide_id: subs-s10
  slide_order: 10
  module_name: coefficient_evidence.py
  slide_type: body
  section: TAM Build
  archetype: coefficient_ladder_plus_evidence_table
  story_role: Explain why the headline model uses the strict 35.0% applied BC supplier coefficient despite broader distributed-production POP evidence.
  inputs:
    - Chart Data CD_10_CoefficientLadder
    - TAM Build section 3 (POP coefficients; primary_tam_coeff, bc_supplier_coeff, ap_lltm_supplier_coeff)
    - POP Corpus (658-row place-of-performance gate)
    - POP Source Audit (confirmation coverage, unparsed share, concentration)
  related_appendix:
    - subs-a4   # appendix_coefficient_sensitivity

chrome:
  section: Market sizing
  breadcrumb_topic: Coefficient evidence
  title_topic: Coefficient Evidence
  title_finding: POP data supports distributed production, but the headline coefficient remains strict
  layout: slideLayout4
  sources:
    - U.S. DoD daily Contracts announcements, July 2022-May 2026
    - DoD Contracts releases dated April 30, 2025 and May 11, 2026
    - GAO-25-106286
  source_line_exact: "Sources: (1) U.S. DoD daily Contracts announcements, July 2022-May 2026; (2) DoD Contracts releases dated April 30, 2025 and May 11, 2026; (3) GAO-25-106286"

story:
  objective: Show that the supplier coefficient is evidence-based while making clear that only the strict 35.0% Basic Construction coefficient feeds headline TAM.
  do_not_say:
    - Do not imply the all-gated 51.8% POP anchor is wrong; it is broader than the headline TAM boundary.
    - Do not apply the 51.8% or 48.5% views to the headline TAM.
    - Do not double count AP and LLTM.
  known_caveats:
    - Largest-action concentration (~48.8%) and the ~10.1% unparsed single-site POP share are limitations behind the strict coefficient, not reasons to discard the evidence.
    - The AP and LLTM reference coefficient (~48.5%) is explanatory only because the AP and LLTM additive base is $0 in the headline model.
    - POP percentages are dollar-weighted across the 43 gated TAM-relevant actions; the bucket shares sum to ~89.9% with the remaining ~10.1% unparsed (single-site rows without a stated percentage).

regions:
  coord_basis: BODY
  layout_pattern: coefficient_ladder_plus_evidence_table
  # Ranked-bar chart fills the left ~55%; ONE compact evidence table sits right of it,
  # top-aligned to the chart; a read line pins under the chart and a guardrail strip pins
  # full-width.
  title_band: {x: 0%, y: 0%, w: 55%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 55%, h: 62%}
  evidence_table: {x: right_of(chart) + GAP, y: align_top(chart), w: 39%, h: fit_content}
  read_callout: {x: 0%, y: below(chart) + GAP, w: 55%, h: fit_content}
  guardrail:  {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary, paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame, region: chart, prominence: primary, paint_order: 2, content: ranked coefficient ladder (3 bars), tie_out: CD_10_CoefficientLadder}
  - {id: e3, type: table, region: evidence_table, prominence: secondary, paint_order: 3, content: compact POP-corpus evidence table (6 metric/value rows + header)}
  - {id: e4, type: note, region: read_callout, prominence: tertiary, paint_order: 4, content: headline read line (no-fill, under chart base)}
  - {id: e5, type: note, region: guardrail, prominence: tertiary, paint_order: 5, content: headline-coefficient guardrail strip (no-fill)}


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
    e4:
      text_runs:
      - role: Read lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: read body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e5:
      text_runs:
      - role: Guardrail lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: guardrail body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).
  - For charts, keep factory title=null and instantiate the external title element from this typography block.

charts:
  - id: chart_1
    factory: bar_chart
    chart_index: 0              # -> rId2
    title_element: e1
    frame_element: e2
    data:
      categories:
        - All-gated POP anchor
        - AP and LLTM reference
        - Applied BC supplier coefficient
      series:
        - name: Coefficient view
          # Stored as fractions (0.518 etc.); axis/labels format as 0.0% -> 51.8 / 48.5 / 35.0.
          values: [0.518, 0.485, 0.350]
          data_point_colors: [BLUE_3, BLUE_2, BLUE_5]   # applied bar darkest (BLUE_5) to highlight the headline input
    params:
      mode: ranked
      value_axis_format: '0.0%'
      show_legend: false
      show_gridlines: true
      major_gridline_color: GRAY_1
      major_gridline_width: 3175       # 0.25pt quiet gridline
      show_value_labels: true
      value_label_format: '0.0%'
      value_label_size_pt: 9
      cat_label_size_pt: 9
      gap_width: 55
      cat_header: Coefficient view
      title: null
    external_title:
      text: Supplier coefficient evidence, %
      size: CHART_TITLE_10PT
      italic: true
      color: DK
    annotations:
      - {text: "Reference only; additive base = $0", anchor_to: e2}     # beside the 48.5% bar
      - {text: "Only input to headline TAM", anchor_to: e2}             # beside the 35.0% bar

tables:
  - id: house_table
    element: e3
    role: chart_side_evidence
    table_skin: rule
    size: 900
    columns: [Metric, Value]
    column_widths:
      ratio: [2.6, 1.0]
      sum_to_region_width: true
    aligns: ["l", "r"]
    row_h: estimate_row_heights
    rows:
      - ["Evidence", "Value"]                       # header
      - ["POP rows screened", "658"]
      - ["Gated TAM-relevant actions", "43"]
      - ["Gated POP corpus", "~$25.4B"]
      - ["In-scope non-GFE corpus", "~$19.3B"]
      - ["Confirmation coverage", "100%"]
      - ["Unparsed share (limitation)", "10.1%"]
    footnote: "Unparsed share is a tracked limitation: single-site POP rows without a stated percentage are floored, so reported outsourcing shares are conservative."
    meaning: Compact POP-corpus evidence; rule-skinned chart-side table that proves the coefficient is evidence-based without re-running the appendix A4 cards.

shapes:
  - id: read_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Read: Evidence supports a large distributed-production layer; the model applies a stricter coefficient."   # lead MESSAGE_11PT bold, body DENSE_BODY_10PT
    meaning: Headline read line under the chart base.
  - id: guardrail_1
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Guardrail: Higher POP views are explanatory and sensitivity views; they are not multiplied into headline TAM."   # lead MESSAGE_11PT bold, body DENSE_BODY_10PT, centered
    meaning: Main guardrail preventing coefficient drift; only the 35.0% applied BC coefficient feeds TAM.

commentary:
  visible:
    element: e5
    container: method_note
    title:
    bullets:
      - {lead: "Guardrail:", body: "Higher POP views are explanatory and sensitivity views; they are not multiplied into headline TAM."}
    body_size: DENSE_BODY_10PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It explains why the model is conservative after the TAM
      Bridge (S08). The DoD daily-announcement place-of-performance (POP) corpus shows
      real distributed production away from Electric Boat sites and away from the
      two-yard team, but the headline TAM does not use the broadest distributed-production
      view. The slide proves the coefficient is evidence-based without letting the broad
      evidence into the headline math.

      THE THREE COEFFICIENT VIEWS. The all-gated POP anchor is 51.8% - the dollar-weighted
      Other-US supplier plus foreign share over all 43 gated TAM-relevant actions
      (the published drift-guard anchor of 0.518 reproduced by the model). It is
      directionally important and functions as a drift guard and supporting evidence, but
      it is broader than the headline TAM boundary. The AP and LLTM reference coefficient
      is 48.5%, but the AP and LLTM additive base is $0 in the headline model, so it is
      reference only. The applied Basic Construction supplier coefficient is 35.0%
      (35.0235% exact), and it is the only coefficient that feeds headline TAM; it is the
      supplier+foreign share over the gated, in-scope, non-GFE BC-stream corpus with BPMI
      naval-nuclear dropped.

      THE POP DISTRIBUTION BEHIND THE ANCHOR. Across the 43 TAM-relevant actions totaling
      ~$25.4B, the dollar-weighted place-of-performance distribution is ~21.9% at EB-sites
      (Groton, Quonset Point, North Kingstown), ~16.2% at HII Newport News, ~51.8% at
      Other-US supplier cities, and ~0% foreign (wiki 07). Two headline outsourcing
      measurements follow: ~78% of dollars flow outside Electric Boat (denominator 1) and
      ~52% flow outside both shipyards combined (denominator 2). Both are conservative
      floors because single-supplier-site actions without a stated percentage are parsed
      as missing rather than 100% at that site (~$1.6B across ~17 rows).

      EVIDENCE BASE. The POP audit screened 658 corpus rows, identified 43 gated
      TAM-relevant actions, and produced a $25.4B gated POP corpus. The in-scope non-GFE
      corpus is $19.3B (after removing BPMI naval-nuclear ~$4.8B and submarine GFE
      electronics/components), with 100% confirmation coverage of in-scope non-GFE
      dollars. The unparsed share is ~10.1%, tracked as a limitation. Largest-action
      concentration is ~48.8% (the $12.42B April 30, 2025 Virginia Block VI LLTM action
      over the ~$25.4B gated pool), which is useful for appendix or speaker commentary if
      the coefficient is challenged.

      TRAJECTORY (supporting, not sizing). The POP corpus shows a sharp outsourcing shift:
      a December 2022 Columbia LLTM action placed 0% at outside-yard suppliers, while a
      May 11, 2026 Virginia Block VI LLTM action ($2.31B) placed 98% at outside-yard
      supplier cities. The trajectory corroborates GAO's finding that shipbuilders are
      expanding outsourcing (GAO-25-106286), but the headline coefficient is sized on the
      cumulative corpus, not the most aggressive single action.

      MAIN GUARDRAIL. The broader evidence is not thrown away. It explains why a supplier
      layer exists and why the denominator is not purely yard self-perform. But the
      headline coefficient is narrower because it sizes the non-nuclear supplier
      manufacturing opportunity after excluding non-addressable streams, BPMI naval-
      nuclear, GFE, and prime-yard and co-prime-yard portions. The 51.8% and 48.5% views
      are sensitivity and reference, stress-tested in appendix A4, never headline math.
    density_modes:
      normal: {visible_bullets: 1, keep: [e2, e3, e4, e5]}
      dense: {add_bullets: 4, safe_containers: [guardrail, chart, read_callout], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - {priority: 1, lead: "51.8%:", body: "The all-gated POP anchor is the dollar-weighted Other-US supplier plus foreign share over the 43 gated actions; it is a directional drift guard, broader than the headline TAM boundary.", evidence: "CD_10_CoefficientLadder (primary_tam_coeff_cell); DoD POP corpus (wiki 07)", safe_container: chart, density_trigger: "Add as a small chart note if needed."}
      - {priority: 2, lead: "48.5%:", body: "The AP and LLTM reference coefficient is explanatory only because the additive AP and LLTM base is $0; supplier LLTM is already inside Basic Construction.", evidence: "TAM Build section 3a (ap_lltm_supplier_coeff_cell); AP and LLTM bridge (S11)", safe_container: guardrail, density_trigger: "Add if AP is being discussed."}
      - {priority: 3, lead: "35.0%:", body: "The applied BC supplier coefficient is the only coefficient multiplied into headline TAM; exact value 35.0235%.", evidence: "TAM Build section 3a (bc_supplier_coeff_cell)", safe_container: guardrail, density_trigger: "Always safe in a dense variant."}
      - {priority: 4, lead: "Corpus scale:", body: "The evidence base is 43 gated TAM-relevant actions and a $25.4B gated POP corpus across the July 2022 to May 2026 window.", evidence: "POP Corpus; POP Source Audit", safe_container: evidence_table, density_trigger: "Use if card labels can expand."}
      - {priority: 5, lead: "Non-GFE basis:", body: "The in-scope non-GFE corpus is $19.3B after removing BPMI naval-nuclear and submarine GFE, anchoring the exclusion logic behind the stricter coefficient.", evidence: "POP Source Audit (inscope_dollar_cell)", safe_container: evidence_table, density_trigger: "Use for a denser proof-point card."}
      - {priority: 6, lead: "Parser limitation:", body: "The ~10.1% unparsed share is tracked as a limitation; single-site actions without a stated percentage are floored, so reported outsourcing shares are conservative.", evidence: "POP Source Audit (unparsed_share_cell); DoD POP corpus (wiki 07)", safe_container: evidence_table, density_trigger: "Add if limitation handling is challenged."}
      - {priority: 7, lead: "Concentration risk:", body: "Largest-action concentration is ~48.8% (the $12.42B Virginia Block VI LLTM action), a note for diligence rather than a headline weakening of the evidence.", evidence: "POP Source Audit (concentration_cell); DoD release April 30, 2025 (wiki 07)", safe_container: guardrail, density_trigger: "Add in a diligence-heavy version."}
      - {priority: 8, lead: "Boundary language:", body: "The applied coefficient sizes non-nuclear supplier manufacturing opportunity, not all distributed production.", evidence: "TAM Build section 3; coefficient methodology", safe_container: guardrail, density_trigger: "Add for external audiences."}
      - {priority: 9, lead: "Outside-yard shares:", body: "Across the gated corpus ~78% of dollars flow outside Electric Boat and ~52% outside both shipyards combined, both conservative floors.", evidence: "DoD POP corpus (wiki 07)", safe_container: read_callout, density_trigger: "Add if the read callout can take a second line."}
      - {priority: 10, lead: "Trajectory:", body: "A May 2026 Virginia Block VI LLTM action placed 98% of dollars at outside-yard suppliers, up from 0% on a December 2022 Columbia action - the cleanest outsourcing-shift evidence.", evidence: "DoD releases Dec 21 2022 and May 11 2026 (wiki 07); GAO-25-106286", safe_container: guardrail, density_trigger: "Add for an audience focused on the structural shift."}
      - {priority: 11, lead: "Confirmation:", body: "Confirmation coverage is 100% of in-scope non-GFE dollars under a tiered manual-review protocol (all $100M+ actions confirmed).", evidence: "POP Source Audit (coverage_cell)", safe_container: evidence_table, density_trigger: "Add if a reviewer questions data confirmation."}
    do_not_add:
      - any formula using 51.8% or 48.5% as the headline multiplier
      - language implying the broad POP view is wrong
      - capture share or SOM language

data_and_calculations:
  data_inputs:
    - {input: All-gated POP anchor, value: 51.8, unit: percent, tie_out: CD_10_CoefficientLadder (primary_tam_coeff_cell; published anchor 0.518), used_in: chart_1}
    - {input: AP and LLTM reference coefficient, value: 48.5, unit: percent, tie_out: CD_10_CoefficientLadder (ap_lltm_supplier_coeff_cell), used_in: chart_1}
    - {input: Applied BC supplier coefficient, value: 35.0, unit: percent, tie_out: CD_10_CoefficientLadder (bc_supplier_coeff_cell; 35.0235% exact), used_in: chart_1}
    - {input: POP rows screened, value: 658, unit: rows, tie_out: POP Corpus (n_rows), used_in: house_table}
    - {input: Gated TAM-relevant actions, value: 43, unit: actions, tie_out: POP Corpus (gated count), used_in: house_table}
    - {input: Gated POP corpus, value: 25.4, unit: $B, tie_out: POP Source Audit (gated_dollar_cell), used_in: house_table}
    - {input: In-scope non-GFE corpus, value: 19.3, unit: $B, tie_out: POP Source Audit (inscope_dollar_cell), used_in: house_table}
    - {input: Confirmation coverage, value: 100, unit: percent, tie_out: POP Source Audit (coverage_cell), used_in: house_table}
    - {input: Unparsed share, value: 10.1, unit: percent, tie_out: POP Source Audit (unparsed_share_cell), used_in: house_table}
    - {input: Largest-action concentration, value: 48.8, unit: percent, tie_out: POP Source Audit (concentration_cell), used_in: reserve}
  rounding_rules: Percentages shown to one decimal; corpus dollars shown to one decimal $B.
  reconciliation: Coefficient ladder is explanatory; only the applied 35.0% coefficient ties to the TAM Bridge (S08). EB + HII + Other-US bucket shares (~21.9% + ~16.2% + ~51.8%) sum to ~89.9%; the ~10.1% remainder is the unparsed single-site share.

qa:
  guardrails:
    - Three coefficients are shown as 51.8%, 48.5%, and 35.0%; the applied 35.0% bar is highlighted darkest (BLUE_5) even though it is the smallest.
    - Slide clearly states only 35.0% feeds headline TAM.
    - AP and LLTM reference does not create additive TAM.
    - Evidence proof points live in ONE compact rule-skinned chart-side table (Metric/Value), distinct from the blue coefficient bars; the detailed cards are de-duplicated to appendix A4.
  source_checks:
    - Sources are the exact real citations in chrome.sources (DoD daily Contracts announcements, dated DoD releases, GAO-25-106286); no internal docs, workbook tabs, wiki chapters, or chart IDs rendered.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_1 chart_index 0 -> rId2)
    - resolved column widths sum to its region width
