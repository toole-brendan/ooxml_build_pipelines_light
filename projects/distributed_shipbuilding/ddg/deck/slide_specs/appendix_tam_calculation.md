# SlideSpec — DDG appendix_tam_calculation
# Appendix A2. The full FY22-27 supplier-TAM backup: a detailed two-stream reconciliation
# house_table + a compact shape-built cumulative bridge + a per-hull KPI strip + the
# standard sizing note. No native chart. Defends the ~$573M per year headline.

meta:
  slide_id: ddg-a2
  slide_order: A2
  module_name: appendix_tam_calculation.py
  slide_type: appendix
  section: Appendix
  archetype: reconciliation_table_plus_compact_bridge
  story_role: Defend the average-annual TAM headline by reconciling the FY22-27 cumulative two-stream model in one place, with the per-FY profile, the per-hull view, and the BC-base to supplier-TAM bridge.
  inputs:
    - TAM Build §5a (TAM by FY = BC base x BC coeff plus AP base x AP coeff)
    - TAM Build §5c-d (portfolio TAM, average-annual, per-hull and BC-per-hull)
    - TAM Build §5e (BC base to supplier TAM bridge; POP removal of prime, co-prime, GFE)
    - TAM Build §3a (BC supplier coefficient 12.5%, MYP-corrected)
    - AP Bridge §2 (CY AP in-window, ship-construction share, AP and LLTM stream TAM)
    - Inputs §3/§5 (CY AP values FY25-26; ship-construction share 0.80; AP coefficient 0.85)
  related_appendix:
    - ddg-a3   # appendix_myp_correction (the MYP-corrected BC coefficient applied here)
    - ddg-a4   # appendix_ap_lltm_sensitivity (the AP and LLTM stream knobs)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: TAM calculation
  title_topic: TAM Calculation
  title_finding: The annual headline is the FY22-27 cumulative two-stream model divided by six
  layout: slideLayout4
  sources:
    - U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122, Exhibit P-5c
    - U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-40
    - DoW DDG-51 contract announcements, July 2022 to May 2026
  source_line_exact: "Sources: (1) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122, Exhibit P-5c; (2) U.S. Navy FY2027 SCN Justification Book, LI 2122, Exhibit P-40; (3) DoW DDG-51 contract announcements, July 2022 to May 2026"

story:
  objective: Show the full FY22-27 cumulative TAM calculation, the per-FY profile, and the six-year average-annual convention behind the ~$573M per year headline, plus the BC-base to supplier-TAM bridge and the per-hull view.
  do_not_say:
    - Do not imply the annual headline is a smooth yearly run-rate.
    - Do not show workbook formulas on the slide.
    - Do not use capture, win-rate, or SOM language except as an exclusion.
  known_caveats:
    - Average-annual values are FY22-27 cumulative divided by six; the per-FY profile is lumpy (FY26 spikes on the AP, FY22 is the trough).
    - AP and LLTM is additive only after GFE-heavy and weapons AP lines are excluded; in-window CY AP is FY25-27 (FY22-24 sit in Prior Years), so it is a lower bound.

object_assessment:
  verdict: "Keep, but make the compact bridge a real compound object: two stream rows, one total row, one annualization row."
  object_contract:
    render_pattern: reconciliation_table_plus_compound_cumulative_bridge
    expected_rendered_object_count: 6
    compound_objects:
      - {id: mini_bridge, child_count: 4, child_type: bridge_row}
      - {id: kpi_strip, child_count: 3, child_type: inline_kpi}
    required_focal_family: "Detailed native table is primary; bridge is secondary and should not become a second table."
  anti_repetition:
    appendix_rule: "No native chart; the body already has waterfall and timing charts."
    forbidden_defaults:
      - No chart.
      - No workbook formulas rendered.

regions:
  coord_basis: BODY
  layout_pattern: reconciliation_table_plus_compact_bridge
  header_note: {x: 0%, y: 0%, w: 100%, h: fit_content}
  calc_table:  {x: 0%, y: below(header_note) + GAP, w: 68%, h: fit_content}
  bridge:      {x: right_of(calc_table) + GAP, y: align_top(calc_table), w: remaining, h: fit_content}
  kpi_strip:   {x: 0%, y: below(calc_table) + GAP, w: 100%, h: fit_content}
  note_strip:  {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: note,    region: header_note, prominence: tertiary,  paint_order: 1, content: annualization header note (cumulative divided by six, not a run-rate)}
  - {id: e2, type: table,   region: calc_table,  prominence: primary,   paint_order: 2, content: detailed FY22-27 two-stream TAM reconciliation table, tie_out: TAM Build §5 and AP Bridge §2}
  - {id: e3, type: callout, region: bridge,      prominence: secondary, paint_order: 3, content: compact shape-built cumulative bridge from the two streams to the annual headline, tie_out: TAM Build §5a/§5c}
  - {id: e4, type: note,    region: kpi_strip,   prominence: tertiary,  paint_order: 4, content: in-window hull and per-hull KPI strip}
  - {id: e5, type: note,    region: note_strip,  prominence: tertiary,  paint_order: 5, content: standard sizing note}

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
    - table: tam_reconciliation
      element: e2
      cell_font: FONT
      cell_size_from: render.size
      header: {bold: true, size_from: render.size}
      first_column: {bold: true, size_from: render.size}
      row_height: {derive_from: render.row_h, size_pt: "render.size / 100"}
      footnotes: {size: FINEPRINT_8_5PT, color: DK, font: FONT}
  shape_rules:
    - shape: annualization_header
      element: e1
      profile: no_fill_note
      runs:
        - {role: lead_if_present, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: MESSAGE_11PT, color: DK, font: FONT}
      note: "Short thesis or boundary sentence; keep no fill/no border."
    - shape: mini_bridge
      element: e3
      profile: compact_bridge_or_comparison
      runs:
        - {role: cap, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: row_label, size: LABEL_9PT, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "If rendered as mini-bars/rows, labels use LABEL_9PT and numbers use VALUE_14PT; do not flatten into one 10pt paragraph."
    - shape: kpi_strip
      element: e4
      profile: no_fill_kpi_note
      runs:
        - {role: label, size: LABEL_9PT, italic: true, color: DK, font: FONT}
        - {role: value, size: RIBBON_KPI_18PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "No fill/no border; value may be centered within the note region if space allows."
    - shape: sizing_note
      element: e5
      profile: standard_sizing_note
      runs:
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "One-line note; keep no fill/no border and do not promote to a readout bar."

charts: []                   # NO native chart — a shape-built bridge is enough

tables:
  - id: tam_reconciliation
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: FY22-27 supplier-TAM reconciliation
      purpose: reconcile
      reader_takeaway: Portfolio supplier TAM equals the BC stream plus the AP and LLTM stream, then divided by six fiscal years for the annual headline.
      row_order: Basic Construction base, BC supplier coefficient, BC-stream supplier TAM, CY AP in-window, ship-construction share, non-GFE AP base, AP and LLTM coefficient, AP and LLTM stream TAM, portfolio supplier TAM, average-annual convention
      highlight_rows: [BC-stream supplier TAM, AP and LLTM stream TAM, Portfolio supplier TAM, Average annual convention]
      guardrails:
        - Annual values are average annual, not a run-rate.
        - AP and LLTM values must remain labeled as the second stream.
        - No SOM or capture language.
    render:
      table_skin: rule        # appendix reconciliation reads cleaner light; 1.5pt header rule carries it
      size: 850               # 8.5pt; dense appendix table; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [3.0, 1.2, 1.1, 1.1, 2.4]   # Step / cumulative / avg per year / coefficient / note
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "r", "ctr", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Step", "FY22-27 cumulative $M", "Avg $M per year", "Coefficient", "Model source or note"]
        - ["Basic Construction base", "17,471.0", "2,911.8", "n.a.", "P-5c BC base, LI 2122"]
        - ["BC supplier coefficient (MYP-corrected)", "n.a.", "n.a.", "12.5%", "Other-US and foreign POP"]
        - ["BC-stream supplier TAM", "2,192.0", "365.3", "applied", "Base times coefficient"]
        - ["CY AP in-window (FY25 to FY27)", "1,833.2", "305.5", "n.a.", "FY22-24 sit in Prior Years"]
        - ["Ship-construction share of CY AP", "1,466.6", "244.4", "80.0%", "Non-GFE share"]
        - ["Non-GFE AP base", "1,466.6", "244.4", "n.a.", "AP base after the share"]
        - ["AP and LLTM supplier coefficient", "n.a.", "n.a.", "85.0%", "Inputs assumption knob"]
        - ["AP and LLTM stream TAM", "1,246.6", "207.8", "applied", "Second stream"]
        - ["Portfolio supplier TAM", "3,438.6", "573.1", "n.a.", "Headline TAM"]
        - ["Average annual convention", "3,438.6", "573.1", "divide by 6", "Not a steady run-rate"]
      cell_fills:
        "(3,0)": BLUE_1        # BC-stream supplier TAM
        "(8,0)": BLUE_1        # AP and LLTM stream TAM
        "(9,0)": BLUE_2        # Portfolio supplier TAM (the headline)
        "(10,0)": GRAY_1       # average-annual convention
      cell_bold:
        "(3,0)": true
        "(8,0)": true
        "(9,0)": true
        "(10,0)": true
      cell_text_colors: {}
      footnotes:
        - "Average annual = FY22-27 cumulative divided by six fiscal years; an average, not a steady run-rate. The per-FY TAM profile is lumpy: ~$245M FY22, ~$1,225M FY26."
    columns:
      - {name: Step, unit: text, tie_out: TAM Build §5 and AP Bridge §2}
      - {name: FY22-27 cumulative $M, unit: $M, tie_out: TAM Build §5a/§5e source outputs}
      - {name: Avg $M per year, unit: $M per year, tie_out: cumulative divided by six}
      - {name: Coefficient, unit: percent or treatment, tie_out: TAM Build §3a / Inputs §5}
      - {name: Model source or note, unit: text, tie_out: source tabs}

shapes:
  - id: annualization_header
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Average annual values are FY22-27 cumulative divided by six; they are not a steady run-rate. The per-FY TAM profile is lumpy, with a FY26 spike on the advance procurement."
    meaning: Prevents the annual headline from being read as a smooth run-rate and flags the lumpy per-FY profile.
  - id: mini_bridge
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MESSAGE
    text:
      paragraphs:
        - {lead: "Cumulative bridge, $M", body: ""}
        - {body: "BC-stream supplier TAM: ~2,192.0"}
        - {body: "AP and LLTM stream TAM: ~1,246.6"}
        - {body: "Portfolio supplier TAM: ~3,438.6"}
        - {body: "Divide by 6: ~573.1 per year"}
    meaning: Compact shape-built bridge that makes the two-stream arithmetic visible without a native chart; the builder may render the two stream values as stacked segments.
  - id: kpi_strip
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "13 in-window hulls (award FY22-27). Supplier TAM per hull ~$265M; BC TAM per hull ~$169M. BC base ~$17.47B less POP removal of prime, co-prime, and GFE leaves the ~$2.19B BC stream."
    meaning: Per-hull KPI strip plus the one-line §5e bridge from BC base to BC-stream TAM.
  - id: sizing_note
    element: e5
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
    meaning: Standard sizing convention note.

images: []

commentary:
  visible:
    element: e1
    container: method_note
    title:
    bullets:
      - {lead: "Convention:", body: "average annual divides cumulative FY22-27 dollars by six and does not imply a steady run-rate."}
      - {lead: "Two streams:", body: "Basic Construction ~$365M per year plus AP and LLTM ~$208M per year equals ~$573M per year."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix page backs the headline TAM slides and the stream
      build. It shows how the portfolio supplier TAM of ~$3,438.6M cumulative becomes the
      ~$573.1M per year headline by averaging across six fiscal years, and it carries the
      per-FY profile, the per-hull view, and the BC-base to supplier-TAM bridge. Every figure
      here ties to TAM Build or AP Bridge. [tie-out: TAM Build §5; AP Bridge §2; DO-01]

      THE TWO-STREAM MODEL (verified to the workbook). The Basic Construction stream starts with
      the ~$17,471.0M cumulative BC base (P-5c Basic Construction summed FY22-27: 1,960.0 +
      4,558.2 + 3,322.5 + 4,628.2 + 282.6 + 2,719.6) and applies the 12.5% MYP-corrected BC
      supplier coefficient, yielding ~$2,192.0M cumulative (~$365.3M per year). The AP and LLTM
      stream starts with ~$1,833.2M cumulative CY AP in-window (FY25 ~83.2 + FY26 ~1,750.0; FY22-24
      sit in Prior Years, so it is a lower bound), applies the 80.0% ship-construction share to get
      ~$1,466.6M non-GFE AP base, then applies the 85.0% AP supplier coefficient, yielding ~$1,246.6M
      cumulative (~$207.8M per year). [tie-out: TAM Build §2b/§5a; AP Bridge §2; Inputs §3/§5]

      RECONCILIATION. BC-stream TAM plus AP and LLTM stream TAM equals ~$3,438.6M cumulative;
      dividing by six fiscal years gives ~$573.1M per year. The slide must say this is an
      average-annual convention, not a smooth annual run-rate. [tie-out: TAM Build §5c-d]

      THE PER-FY PROFILE (why average, not run-rate). TAM by FY = BC base x BC coeff plus AP base
      x AP coeff. The profile is lumpy: ~$245M FY22, ~$570M FY23, ~$415M FY24, ~$635M FY25,
      ~$1,225M FY26 (the AP spike: ~$1,750M of FY26 CY AP drives ~$1,190M of AP-stream TAM that
      single year), ~$340M FY27. The FY26 spike is the structural reason the headline is reported
      as a six-year average rather than a steady annual figure. [tie-out: TAM Build §5a]

      PER-HULL VIEW. With 13 in-window hulls (award FY22-27), supplier TAM per hull is ~$264.5M
      (~$265M) and BC TAM per hull is ~$168.6M (~$169M). Note ~$169M BC-per-hull is distinct from
      the metal scenario ~$170M per year — do not conflate. [tie-out: TAM Build §5d]

      THE 5e BRIDGE (BC base to supplier TAM). TAM Build §5e states it directly: BC construction
      base ~$17,471.0M, less the POP removal of prime, co-prime, and GFE place-of-performance,
      leaves the ~$2,192.0M BC-stream supplier TAM. The removal is the application of the BC
      supplier coefficient: only the other-US-plus-foreign POP share over the non-GFE BC corpus
      (with the redacted BIW and Ingalls MYP masters folded back at reconstructed POP) survives as
      supplier-addressable. [tie-out: TAM Build §5e; appendix_myp_correction (A3)]

      AP ADDITIVITY (no double-count). The AP and LLTM stream is additive because P-5c Basic
      Construction is net of prior-year AP, so CY AP is genuinely incremental (the PY-AP credit in
      the TAM stream bases is 0). The ship-construction share strips AWS EOQ and other GFE from CY
      AP before the coefficient. The AP coefficient (85.0%) is an Inputs assumption, not a measured
      coefficient — there is no DDG AP POP corpus to SUMPRODUCT over (unlike the BC coefficient,
      which is measured). [tie-out: AP Bridge §3-§4; TAM Build §3a]

      COEFFICIENT LINEAGE (keep distinct). The applied 12.5% BC supplier coefficient is the
      MYP-corrected other-US-plus-foreign POP share over the non-GFE BC corpus; it is NOT the
      disclosed-only artifact and NOT the ~32.8% all-gated outside-yards POP. Appendix A3 carries
      that correction in full; keep the 12.5% coefficient conceptually separate from the ~32.8%
      outside-yards POP. [tie-out: appendix_myp_correction (A3); TAM Build §3a/§3b]

      BUILDER GUIDANCE. Use a measured table with explicit row heights. Keep the bridge secondary
      and shape-built (no native chart). Use one decimal place in the table and rounded compact
      labels in the bridge if space is tight. Keep the sizing note and the no-SOM exclusion. Use
      "BC and AP and LLTM" wording, never a visible plus or slash separator.
    density_modes:
      normal: {visible_bullets: 2, keep: [e1, e2, e3, e4, e5]}
      dense:  {add_bullets: 3, safe_containers: [header_note, bridge, kpi_strip], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Two streams:"
        body: "Portfolio TAM combines BC-stream TAM (~$2.19B cumulative, ~$365M per year) and AP and LLTM TAM (~$1.25B cumulative, ~$208M per year)."
        evidence: TAM Build §5; AP Bridge §2
        safe_container: bridge
        density_trigger: Add if the bridge is expanded.
      - priority: 2
        lead: "Annual convention:"
        body: "The ~$573M headline equals ~$3.44B cumulative divided by six fiscal years; it is an average, not a run-rate."
        evidence: TAM Build §5d
        safe_container: header_note
        density_trigger: Add if the title is shortened.
      - priority: 3
        lead: "Lumpy by year:"
        body: "Per-FY TAM runs ~$245M FY22 to ~$1,225M FY26; the FY26 spike comes from ~$1,750M of CY advance procurement, which is why the headline is a six-year average."
        evidence: TAM Build §5a; Inputs §3
        safe_container: header_note
        density_trigger: Add when explaining the FY26 spike.
      - priority: 4
        lead: "Per-hull view:"
        body: "13 in-window hulls imply ~$265M supplier TAM per hull, ~$169M of it from the BC stream; ~$169M BC-per-hull is distinct from the ~$170M metal scenario."
        evidence: TAM Build §5d
        safe_container: kpi_strip
        density_trigger: Add if the KPI strip can take a second line.
      - priority: 5
        lead: "BC bridge:"
        body: "BC base ~$17.47B, less the POP removal of prime, co-prime, and GFE, leaves the ~$2.19B BC stream; the removal is the MYP-corrected supplier coefficient."
        evidence: TAM Build §5e
        safe_container: kpi_strip
        density_trigger: Add for a model-audit appendix.
      - priority: 6
        lead: "AP additivity:"
        body: "AP and LLTM is additive because P-5c BC is net of prior-year AP, so CY AP is incremental; the in-window CY AP is FY25-27, a lower bound."
        evidence: AP Bridge §2/§4
        safe_container: bridge
        density_trigger: Add for a model-audit appendix.
      - priority: 7
        lead: "Coefficient lineage:"
        body: "The 12.5% BC supplier coefficient is MYP-corrected; it is not the disclosed-only artifact and not the ~32.8% outside-yards POP."
        evidence: appendix_myp_correction (A3); TAM Build §3a
        safe_container: bridge
        density_trigger: Add when A3 is not in the appendix pack.
      - priority: 8
        lead: "AP knob, not corpus:"
        body: "The 85.0% AP coefficient is an Inputs assumption; there is no DDG AP POP corpus to measure it over, unlike the BC coefficient."
        evidence: TAM Build §3a (ap note); Inputs §5
        safe_container: header_note
        density_trigger: Add for a sensitivity-focused audience.
      - priority: 9
        lead: "SOM exclusion:"
        body: "The calculation stops at TAM and excludes SOM and capture; no win rate or bookings figure is applied anywhere."
        evidence: TAM Build §5; methodology
        safe_container: note_strip
        density_trigger: Add if a reviewer asks about bookings.
      - priority: 10
        lead: "Precision:"
        body: "Use rounded labels on the slide; the exact decimals remain in the model (~$264.5M and ~$168.6M per hull)."
        evidence: build notes
        safe_container: kpi_strip
        density_trigger: Add only for build QA.
    do_not_add:
      - Native chart for the mini bridge
      - Workbook formulas on the slide
      - SOM, capture probability, win rate, or bookings language
      - Visible plus or slash separators in rendered labels

data_and_calculations:
  data_inputs:
    - {input: Basic Construction base, value: 17471.0, unit: $M cumulative, year: FY22-27, tie_out: TAM Build §2b / SCN Budget, used_in: tam_reconciliation}
    - {input: BC supplier coefficient, value: 12.5%, unit: percent, year: n.a., tie_out: TAM Build §3a, used_in: tam_reconciliation}
    - {input: BC-stream supplier TAM, value: 2192.0, unit: $M cumulative, year: FY22-27, tie_out: TAM Build §5a, used_in: tam_reconciliation and mini_bridge}
    - {input: CY AP in-window, value: 1833.2, unit: $M cumulative, year: FY25-27, tie_out: AP Bridge §2 / Inputs §3, used_in: tam_reconciliation}
    - {input: Ship-construction share of CY AP, value: 80.0%, unit: percent, year: n.a., tie_out: Inputs §5, used_in: tam_reconciliation}
    - {input: Non-GFE AP base, value: 1466.6, unit: $M cumulative, year: FY25-27, tie_out: AP Bridge §2, used_in: tam_reconciliation}
    - {input: AP and LLTM supplier coefficient, value: 85.0%, unit: percent, year: n.a., tie_out: Inputs §5, used_in: tam_reconciliation}
    - {input: AP and LLTM stream TAM, value: 1246.6, unit: $M cumulative, year: FY22-27, tie_out: AP Bridge §2, used_in: tam_reconciliation and mini_bridge}
    - {input: Portfolio supplier TAM, value: 3438.6, unit: $M cumulative, year: FY22-27, tie_out: TAM Build §5c / DO-01, used_in: tam_reconciliation and mini_bridge}
    - {input: Average annual TAM, value: 573.1, unit: $M per year, year: FY22-27 average, tie_out: TAM Build §5d, used_in: tam_reconciliation and mini_bridge}
    - {input: In-window hulls, value: 13, unit: hulls, year: FY22-27, tie_out: TAM Build §5d, used_in: kpi_strip}
    - {input: Supplier TAM per hull, value: 264.5, unit: $M per hull, year: FY22-27, tie_out: TAM Build §5d, used_in: kpi_strip}
    - {input: BC TAM per hull, value: 168.6, unit: $M per hull, year: FY22-27, tie_out: TAM Build §5d, used_in: kpi_strip}
  calculations:
    - {name: BC-stream TAM, formula: BC base 17471.0 times 12.5% coefficient, output: ~$2192.0M cumulative, used_in: tam_reconciliation}
    - {name: Non-GFE AP base, formula: CY AP in-window 1833.2 times 80.0% ship-construction share, output: ~$1466.6M cumulative, used_in: tam_reconciliation}
    - {name: AP and LLTM stream TAM, formula: non-GFE AP base 1466.6 times 85.0% AP coefficient, output: ~$1246.6M cumulative, used_in: tam_reconciliation}
    - {name: Portfolio TAM, formula: BC-stream TAM plus AP and LLTM stream TAM, output: ~$3438.6M cumulative, used_in: mini_bridge}
    - {name: Average annual TAM, formula: portfolio TAM divided by six fiscal years, output: ~$573.1M per year, used_in: title and mini_bridge}
    - {name: Supplier TAM per hull, formula: portfolio TAM divided by 13 hulls, output: ~$264.5M per hull, used_in: kpi_strip}
    - {name: BC TAM per hull, formula: BC-stream TAM divided by 13 hulls, output: ~$168.6M per hull, used_in: kpi_strip}
  rounding_rules: One decimal place for $M values in the table; whole $M labels in the compact bridge if space is tight. Annual whole $M ("~$XXXM per year"); cumulative $B to two decimals ("~$3.44B").
  reconciliation: The annual headline is a six-year average of the cumulative FY22-27 portfolio TAM; it is not a smooth annual run-rate. The two streams sum to portfolio TAM; SAM scenarios (overlapping cuts of this TAM) are out of scope here.

qa:
  guardrails:
    - Portfolio TAM equals ~$3.44B cumulative and ~$573M per year.
    - BC stream equals ~$2.19B cumulative and ~$365M per year; AP and LLTM stream equals ~$1.25B cumulative and ~$208M per year.
    - Annual headline is explicitly cumulative divided by six; the per-FY profile is shown to be lumpy (FY26 spike).
    - The 12.5% BC coefficient is MYP-corrected and is kept distinct from the ~32.8% outside-yards POP.
    - No SOM or capture language appears except as an exclusion.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal workbook tabs or chart IDs rendered.
    - Internal provenance (TAM Build, AP Bridge, Inputs) appears only in meta.inputs, tie_out, and reserve evidence.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the calc_table region width"
    - "table, bridge, KPI strip, and sizing note all sit within BODY (size rows via estimate_row_heights)"
