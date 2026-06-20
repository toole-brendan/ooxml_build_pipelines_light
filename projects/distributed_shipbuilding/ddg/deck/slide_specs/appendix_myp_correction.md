# SlideSpec — DDG appendix_myp_correction
# Appendix A3. The MYP redaction reconstruction in full: a reconstruction-and-POP house_table
# + a shape-built two-bar outside-yards comparison (disclosed artifact corrected to MYP-corrected)
# + a guardrail note. The most important methodological appendix. No native chart.

meta:
  slide_id: ddg-a3
  slide_order: A3
  module_name: appendix_myp_correction.py
  slide_type: appendix
  section: Appendix
  archetype: reconstruction_table_plus_two_bar_comparison
  story_role: Back up the MYP redaction correction that governs the outside-yards view and the BC supplier coefficient, showing why the disclosed-only reading is an artifact and how the corrected reading is reached.
  inputs:
    - Inputs §4 (MYP master reconstruction: BIW $6,400M / Ingalls $8,180M; reconstructed POP %)
    - TAM Build §4 (MYP master rows; disclosed-only vs MYP-corrected outside-yards; swing)
    - TAM Build §3b (outside-yards disclosed artifact vs MYP-corrected; never present the disclosed ~87%)
    - TAM Build §3c (all-gated MYP-corrected POP site shares; deck CD04 distribution)
    - POP Source Audit §2-§3 (gated corpus incl. masters; masters as % of gated)
    - POP Corpus (the gated place-of-performance evidence the coefficients are measured over)
  related_appendix:
    - ddg-a2   # appendix_tam_calculation (the BC coefficient this correction feeds)

chrome:
  section: DDG-51 supplier TAM
  breadcrumb_topic: MYP correction
  title_topic: MYP Correction
  title_finding: Folding the redacted $14.58B masters back into the corpus corrects outside-yards POP to about one third
  layout: slideLayout4
  sources:
    - DoW DDG-51 contract announcements, Aug. 1 and Aug. 11, 2023 (FY23-27 multiyear masters)
    - 41 U.S. Code 2101 et seq. and FAR 2.101 and 3.104 (source-selection sensitive)
    - USNI News, Navy reporting on the FY23-27 DDG-51 multiyear master awards, 2023
  source_line_exact: "Sources: (1) DoW DDG-51 contract announcements, Aug. 1 and Aug. 11, 2023; (2) 41 U.S. Code 2101 et seq. and FAR 2.101 and 3.104; (3) USNI News, Navy reporting on the FY23-27 DDG-51 multiyear master awards, 2023"

story:
  objective: Show how the BIW and Ingalls FY23-27 multiyear masters are reconstructed, why the disclosed-only outside-yards reading is a redaction artifact, and how folding the masters back corrects outside-yards POP to ~32.8% and underpins the applied BC supplier coefficient.
  do_not_say:
    - Do not headline the disclosed artifact (neither the ~87% announcement-corpus reading nor the 73.6% workbook reading) as the conclusion.
    - Do not imply the artifact is a defensible denominator.
    - Do not use visible arrows; use words such as "corrected to".
    - Do not present the ~32.8% outside-yards POP as the BC supplier coefficient (12.5%).
  known_caveats:
    - The ~32.8% all-gated outside-yards POP is distinct from the applied 12.5% BC supplier coefficient (measured on the non-GFE BC corpus). They are related but not identical.
    - Per-hull allocation within a master PIID is not disclosed; the POP weights are the analytical reconstruction.
    - Redaction is a source-disclosure feature of the two-yard competitive procurement, not a compliance failure.

object_assessment:
  verdict: "Keep, but de-text-box the comparison. The outside-yards comparison must be a compound two-bar object with muted artifact and emphasized corrected bar."
  object_contract:
    render_pattern: reconstruction_table_plus_shape_built_two_bar_comparison
    expected_rendered_object_count: 7
    compound_objects:
      - {id: outside_yards_comparison, child_count: 4, child_type: two_bar_comparison_children}
    required_focal_family: "Reconstruction table is primary; corrected 32.8% bar is BLUE_5; artifact bar is GRAY_3 and smaller in emphasis."
  anti_repetition:
    appendix_rule: "No second waterfall and no visible arrow motif. Use 'corrected to' wording."
    forbidden_defaults:
      - Do not headline the artifact.
      - Do not present 32.8% as the 12.5% coefficient.

regions:
  coord_basis: BODY
  layout_pattern: reconstruction_table_plus_two_bar_comparison
  recon_table:    {x: 0%, y: 0%, w: 66%, h: fit_content}
  comparison:     {x: right_of(recon_table) + GAP, y: align_top(recon_table), w: remaining, h: fit_content}
  guardrail_note: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: exhibit_title, region: recon_table,    prominence: tertiary,  paint_order: 1, content: external table title (no-fill text_box above the table)}
  - {id: e2, type: table,         region: recon_table,    prominence: primary,   paint_order: 2, content: MYP reconstruction and POP correction table, tie_out: Inputs §4 and TAM Build §3b-§4 and POP Audit}
  - {id: e3, type: callout,       region: comparison,     prominence: secondary, paint_order: 3, content: shape-built two-bar outside-yards comparison (disclosed corrected to MYP-corrected), tie_out: TAM Build §3b / CD04}
  - {id: e4, type: note,          region: guardrail_note, prominence: tertiary,  paint_order: 4, content: artifact guardrail and TAM sensitivity note}

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
    - table: myp_reconstruction
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
    - shape: outside_yards_comparison
      element: e3
      profile: compact_bridge_or_comparison
      runs:
        - {role: cap, size: DENSE_BODY_10PT, bold: true, color: DK, font: FONT}
        - {role: row_label, size: LABEL_9PT, color: DK, font: FONT}
        - {role: value, size: VALUE_14PT, bold: true, color: DK, font: FONT}
        - {role: qualifier, size: FINEPRINT_8_5PT, italic: true, color: DK, font: FONT}
      note: "If rendered as mini-bars/rows, labels use LABEL_9PT and numbers use VALUE_14PT; do not flatten into one 10pt paragraph."
    - shape: guardrail_note
      element: e4
      profile: no_fill_commentary_rail
      runs:
        - {role: lead, size: FINEPRINT_8_5PT, bold: true, color: DK, font: FONT}
        - {role: body, size: FINEPRINT_8_5PT, color: DK, font: FONT}
      note: "Multi-run bullets: bold lead-in plus regular body; keep no fill/no border."

charts: []                   # NO native chart — a shape-built two-bar comparison is enough

tables:
  - id: myp_reconstruction
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: MYP reconstruction and POP correction
      purpose: reconcile
      reader_takeaway: The reconstructed ~$14.58B masters are ~67% of the gated corpus and pull outside-yards POP down from the disclosed artifact to the ~32.8% MYP-corrected view.
      row_order: BIW master, Ingalls master, combined masters, disclosed announcement corpus, gated corpus incl. masters, corrected outside-yards POP, disclosed-only artifact, TAM sensitivity
      highlight_rows: [Combined reconstructed masters, Corrected outside-yards POP]
      guardrails:
        - The disclosed artifact is a trapdoor, not the conclusion.
        - Corrected outside-yards POP is the defensible reading.
        - The reconstructed master POP weights are analytical, not disclosed per hull.
    render:
      table_skin: rule        # appendix reconstruction reads cleaner light; 1.5pt header rule carries it
      size: 850               # 8.5pt; dense appendix table; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [2.4, 1.0, 1.7, 2.0, 1.5]   # Item / approx $M / POP treatment / model use / guardrail
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "l", "l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Item", "Approx. $M", "Reconstructed POP", "Model use", "Guardrail"]
        - ["BIW FY23-27 MYP master", "6,400", "Bath 86%, supplier 14%", "PIID N00024-23-C-2305", "Redacted dollar value"]
        - ["Ingalls FY23-27 MYP master", "8,180", "Pascagoula 88%, supplier 12%", "PIID N00024-23-C-2307", "Redacted dollar value"]
        - ["Combined reconstructed masters", "14,580", "Yard-heavy", "67.2% of gated corpus", "Too large to ignore"]
        - ["Disclosed announcement corpus", "7,132", "152 gated actions", "Disclosed-only base", "Over-weights GFE"]
        - ["Gated corpus incl. masters", "21,712", "All gated", "Denominator for correction", "Use for the corrected view"]
        - ["Corrected outside-yards POP", "n.a.", "32.8%", "Other-US and foreign", "Defensible reading"]
        - ["Disclosed-only artifact", "n.a.", "73.6%", "Guardrail only", "Do not headline"]
        - ["TAM sensitivity", "1,310", "Uplift", "~$3.44B corrected vs ~$2.13B disclosed-only", "Method swing"]
      cell_fills:
        "(3,0)": BLUE_1        # combined reconstructed masters
        "(6,0)": BLUE_2        # corrected outside-yards POP (the conclusion)
        "(7,0)": GRAY_2        # disclosed-only artifact (muted)
      cell_bold:
        "(3,0)": true
        "(6,0)": true
      cell_text_colors:
        "(7,0)": GRAY_5        # mute the disclosed artifact row label
      footnotes:
        - "Master dollar values are source-selection redacted (FAR 2.101 and 3.104); ~$14.58B reconstructed from FPDS obligated amount and trade-press totals. POP weights are the analytical reconstruction, not disclosed per hull."
    columns:
      - {name: Item, unit: name, tie_out: Inputs §4 / POP Audit §2}
      - {name: Approx. $M, unit: $M, tie_out: Inputs §4 (masters) / POP Audit §2 (corpus)}
      - {name: Reconstructed POP, unit: percent or text, tie_out: Inputs §4 / TAM Build §3b}
      - {name: Model use, unit: text, tie_out: POP Corpus / TAM Build §4}
      - {name: Guardrail, unit: text, tie_out: TAM Build §4c}

shapes:
  - id: title_1
    element: e1
    factory: text_box        # external table title (house exhibit-title pattern)
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "MYP master reconstruction and outside-yards POP correction"
    meaning: Names the exhibit in the house 10pt italic title style above the table.
  - id: outside_yards_comparison
    element: e3
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_MESSAGE
    text:
      paragraphs:
        - {lead: "Outside-yards POP share", body: ""}
        - {body: "Disclosed-only artifact: 73.6%"}
        - {body: "MYP-corrected: 32.8%"}
        - {body: "Read: the corrected view is about one third of the gated corpus, corrected to from the artifact."}
    meaning: Two-bar comparison without a native chart; the builder renders the two percentages as horizontal bars with the corrected bar below the muted artifact bar. No visible arrows.
  - id: guardrail_note
    element: e4
    factory: text_box        # no-fill bottom guardrail note
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Do not headline the disclosed artifact. The disclosed-only reading over-weights GFE because the yard-heavy MYP masters disclose POP percentages but not dollar values. The announcement-corpus headline reads ~87% outside both yards; the live workbook disclosed-only figure is 73.6%; folding the masters back corrects it to 32.8%. Portfolio TAM ~$3.44B corrected versus ~$2.13B disclosed-only; uplift ~$1.31B. The ~32.8% outside-yards POP is not the 12.5% BC supplier coefficient."
    meaning: Bottom guardrail note that prevents either artifact reading from becoming the answer and keeps the outside-yards POP distinct from the BC coefficient.

images: []

commentary:
  visible:
    element: e4
    container: method_note
    title:
    bullets:
      - {lead: "Artifact:", body: "the disclosed-only reading over-weights the yards because the masters disclose POP but not dollars."}
      - {lead: "Corrected:", body: "folding the ~$14.58B masters back gives ~32.8% outside-yards POP, the defensible reading."}
      - {lead: "Distinct:", body: "the ~32.8% outside-yards POP is not the 12.5% BC supplier coefficient."}
    body_size: FINEPRINT_8_5PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the most important methodological appendix page. It backs
      the body slide that corrects the outside-yards share for the redacted FY23-27 multiyear
      masters and underpins the applied BC supplier coefficient. Everything here is reconstructed
      or computed from the POP corpus. [tie-out: TAM Build §3b-§4; POP Audit; Inputs §4]

      THE REDACTION (structurally unique to the two-yard destroyer procurement). The FY23-27
      DDG-51 multiyear masters are dollar-redacted as source-selection-sensitive under 41 U.S.
      Code 2101 et seq. and FAR 2.101 / 3.104, a direct consequence of the two-yard competitive
      structure (both BIW and Ingalls bid; disclosing per-yard dollars would reveal competitive
      pricing). The two masters: BIW PIID N00024-23-C-2305 (war.gov article 3479250, Aug. 1,
      2023) and Ingalls PIID N00024-23-C-2307 (war.gov article 3491276, Aug. 11, 2023). The
      bulletins disclose place-of-performance percentages but leave the dollar field empty.
      Submarine, carrier, and frigate single-prime MYPs disclose their dollar values; destroyers
      are the lone redacted case in the recent Navy new-construction portfolio. [tie-out: wiki 01, 12]

      THE RECONSTRUCTION (~$14.58B). The actual obligated dollars are known from trade press
      (USNI News, Defense Daily, Naval News) to total ~$14.58B combined: BIW share ~$6.40B,
      Ingalls share ~$8.18B. Recovery basis: FPDS obligatedAmount plus trade-press totals. (As of
      the May 2026 pull the BIW master shows ~$5.03B FPDS-obligated against the ~$6.40B ceiling,
      the gap being unexercised options.) The masters are carried at reconstructed POP %, editable
      on Inputs: BIW master 86% Bath / 12% other-US / 2% foreign; Ingalls master 88% Pascagoula /
      10% other-US / 2% foreign. NOTE these reconstructed weights differ from the announcement-
      disclosed POP percentages quoted in the bulletins (BIW 69% Bath; Ingalls 77% Block I / 79%
      Block II) — the slide uses the workbook reconstructed weights; the announcement percentages
      are context. Per-hull-within-master allocation is NOT disclosed; the POP weights are the
      analytical reconstruction. [tie-out: Inputs §4; TAM Build §4a/§4c; wiki 12]

      THE THREE OUTSIDE-YARDS READINGS (keep them straight). (1) The DoD-announcement-corpus
      headline is ~87% outside BOTH yards over the disclosed $7.13B / 152-action corpus
      (BIW-site 11.2%, Ingalls-site 1.3%, other-US-supplier 73.6%, foreign 0%, unparsed 13.8%;
      100 minus 11.2 minus 1.3 = 87.5%). (2) The LIVE workbook disclosed-only figure (TAM Build
      §3b/§4b, masters excluded) is 73.6% — it counts only other-US-plus-foreign over the disclosed
      gated corpus (it excludes the 13.8% unparsed), which is why it reads 73.6% rather than 87%.
      (3) The MYP-CORRECTED reading folds the ~$14.58B masters back into the POP-weighted corpus
      and gives 32.8% outside-yards POP (the 0.33 anchor; live ~32.8%). The defensible reading is
      the corrected one; the disclosed readings appear only to explain the correction. GUARDRAIL:
      never present any disclosed reading as the conclusion, and never present the ~87% (or 73.6%)
      as the BC supplier coefficient. [tie-out: TAM Build §3b; wiki 04, 12]

      THE CORPUS ARITHMETIC. Disclosed gated corpus ~$7,132M plus combined masters ~$14,580M =
      gated corpus incl. masters ~$21,712M. Masters as a share of gated = 14,580 / 21,712 = 67.2%
      — too large to ignore, which is why the disclosed-only reading is an artifact. [tie-out: POP
      Audit §2-§3]

      THE CORRECTED SITE DISTRIBUTION (deck CD04, all-gated, MYP-corrected). BIW 29.0%, Ingalls
      33.6%, Other-US 31.5%, Foreign 1.3%, Unparsed 4.5%. Outside both yards (other plus foreign)
      = 32.8% = the supplier-addressable share. The anchor regression target is 0.33; the computed
      figure ~32.8% is within tolerance. [tie-out: TAM Build §3c/§3e]

      TAM SENSITIVITY. Portfolio TAM is ~$3.44B corrected versus ~$2.13B using the disclosed-only
      BC coefficient; the MYP reconstruction uplift is ~$1.31B. The applied BC supplier coefficient
      (12.5%) is lower than a naive all-gated outside-yards share because it is measured on the
      non-GFE BC corpus, not simply the all-gated corpus — keep the all-gated outside-yards POP
      (~32.8%) and the applied BC supplier coefficient (12.5%) conceptually separate. [tie-out:
      Sensitivity; appendix_tam_calculation (A2); TAM Build §3a]

      WHY 12.5% IS NOT 32.8%. The 32.8% is the other-US-plus-foreign POP share over the WHOLE
      all-gated corpus (BC plus GFE). The 12.5% BC coefficient is the same kind of POP share but
      measured over the NON-GFE BC corpus only, where the redacted yard-heavy masters dominate
      (~93% of the BC corpus), pulling the supplier share down. The two answer different questions
      and must never be conflated. [tie-out: TAM Build §3a (bc note); §3b]

      BUILDER GUIDANCE. Use a native measured table plus a simple shape-built two-bar comparison.
      Place the corrected 32.8% bar below the muted artifact bar to imply correction; use muted
      styling on the artifact value. Avoid visible arrows; use "corrected to". Keep the guardrail
      note bottom-pinned. Use the same terms as the body MYP slide: "MYP-corrected" and "disclosed
      artifact".
    density_modes:
      normal: {visible_bullets: 3, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [comparison, guardrail_note, recon_table], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Masters dominate:"
        body: "The reconstructed ~$14.58B masters are 67.2% of the ~$21.71B gated corpus, which is why the disclosed-only reading is an artifact."
        evidence: POP Audit §3; TAM Build §4
        safe_container: comparison
        density_trigger: Add if the comparison panel has a small evidence line.
      - priority: 2
        lead: "Corrected to:"
        body: "Outside-yards POP corrects to 32.8% MYP-corrected from the 73.6% live workbook disclosed-only figure (the announcement headline is ~87%)."
        evidence: TAM Build §3b; wiki 04, 12
        safe_container: comparison
        density_trigger: Add if the two-bar comparison is expanded.
      - priority: 3
        lead: "TAM swing:"
        body: "Corrected portfolio TAM is ~$3.44B versus ~$2.13B disclosed-only, a ~$1.31B uplift from the MYP reconstruction."
        evidence: Sensitivity; appendix_tam_calculation (A2)
        safe_container: guardrail_note
        density_trigger: Add if the bottom note can take a second line.
      - priority: 4
        lead: "BIW master:"
        body: "BIW FY23-27 master ~$6.40B, PIID N00024-23-C-2305, carried at reconstructed 86% Bath; ~$5.03B FPDS-obligated against the ~$6.40B ceiling at the May 2026 pull."
        evidence: Inputs §4; wiki 12
        safe_container: recon_table
        density_trigger: Add in expanded row notes only.
      - priority: 5
        lead: "Ingalls master:"
        body: "Ingalls FY23-27 master ~$8.18B, PIID N00024-23-C-2307, carried at reconstructed 88% Pascagoula."
        evidence: Inputs §4; wiki 12
        safe_container: recon_table
        density_trigger: Add in expanded row notes only.
      - priority: 6
        lead: "Site distribution:"
        body: "Corrected all-gated POP: BIW 29.0%, Ingalls 33.6%, Other-US 31.5%, Foreign 1.3%, Unparsed 4.5% (deck CD04)."
        evidence: TAM Build §3c
        safe_container: guardrail_note
        density_trigger: Add if the sensitivity row is removed for space.
      - priority: 7
        lead: "Coefficient separation:"
        body: "The ~32.8% all-gated outside-yards POP and the applied 12.5% BC supplier coefficient are related but not identical; the coefficient is measured on the non-GFE BC corpus."
        evidence: TAM Build §3a/§3b
        safe_container: guardrail_note
        density_trigger: Add if a reviewer asks why 32.8% is not the coefficient.
      - priority: 8
        lead: "Per-hull not disclosed:"
        body: "Allocation within each master PIID is not disclosed; the reconstructed POP weights are the analytical reconstruction, not a published per-hull split."
        evidence: TAM Build §4c
        safe_container: recon_table
        density_trigger: Add for a model-audit version.
      - priority: 9
        lead: "Announcement vs reconstructed POP:"
        body: "The bulletins disclose 69% Bath (BIW) and 77% to 79% Pascagoula (Ingalls); the workbook carries reconstructed 86% and 88% yard weights. Use the reconstructed weights."
        evidence: wiki 04, 12; Inputs §4
        safe_container: recon_table
        density_trigger: Add if a reviewer cites the announcement percentages.
      - priority: 10
        lead: "Not a compliance failure:"
        body: "The redaction is a source-disclosure feature of the two-yard competitive procurement under FAR 3.104, not a reporting or compliance failure."
        evidence: wiki 12
        safe_container: guardrail_note
        density_trigger: Add if a reviewer reads the redaction as non-compliance.
    do_not_add:
      - A headline that emphasizes the ~87% or 73.6% disclosed artifact as the conclusion
      - A native chart where the simple two-bar comparison is enough
      - Visible arrows or transformation graphics that imply a precise causal pipeline
      - The ~32.8% outside-yards POP presented as the BC supplier coefficient

data_and_calculations:
  data_inputs:
    - {input: BIW FY23-27 MYP master, value: 6400, unit: $M reconstructed, year: FY23-27, tie_out: Inputs §4, used_in: myp_reconstruction}
    - {input: Ingalls FY23-27 MYP master, value: 8180, unit: $M reconstructed, year: FY23-27, tie_out: Inputs §4, used_in: myp_reconstruction}
    - {input: Combined reconstructed masters, value: 14580, unit: $M reconstructed, year: FY23-27, tie_out: TAM Build §4a / POP Audit §2, used_in: myp_reconstruction}
    - {input: Disclosed announcement corpus, value: 7132, unit: $M, year: Jul 2022 to May 2026, tie_out: POP Corpus (152 gated actions), used_in: myp_reconstruction}
    - {input: Gated corpus incl. masters, value: 21712, unit: $M, year: FY22-27, tie_out: POP Audit §2, used_in: myp_reconstruction}
    - {input: Masters share of gated corpus, value: 67.2%, unit: percent, year: n.a., tie_out: POP Audit §3, used_in: myp_reconstruction}
    - {input: Outside-yards POP MYP-corrected, value: 32.8%, unit: percent, year: n.a., tie_out: TAM Build §3b/§3e, used_in: outside_yards_comparison}
    - {input: Outside-yards POP disclosed-only (workbook), value: 73.6%, unit: percent, year: n.a., tie_out: TAM Build §3b, used_in: outside_yards_comparison}
    - {input: Outside-both-yards announcement headline, value: 87%, unit: percent, year: Jul 2022 to May 2026, tie_out: wiki 04 / POP Corpus, used_in: guardrail_note}
    - {input: Portfolio TAM MYP-corrected, value: 3438.6, unit: $M cumulative, year: FY22-27, tie_out: TAM Build §5c / DO-01, used_in: guardrail_note}
    - {input: Portfolio TAM disclosed-only, value: 2130, unit: $M cumulative, year: FY22-27, tie_out: Sensitivity, used_in: guardrail_note}
    - {input: MYP adjustment uplift, value: 1310, unit: $M cumulative, year: FY22-27, tie_out: Sensitivity, used_in: guardrail_note}
  calculations:
    - {name: Combined masters, formula: BIW master 6400 plus Ingalls master 8180, output: ~$14,580M, used_in: myp_reconstruction}
    - {name: Gated corpus incl. masters, formula: disclosed corpus 7132 plus combined masters 14580, output: ~$21,712M, used_in: myp_reconstruction}
    - {name: Masters share, formula: combined masters 14580 divided by gated corpus 21712, output: 67.2%, used_in: myp_reconstruction}
    - {name: Disclosed-only outside-yards, formula: other-US plus foreign POP $ over the disclosed gated corpus (masters excluded), output: 73.6%, used_in: outside_yards_comparison}
    - {name: MYP-corrected outside-yards, formula: other-US plus foreign POP $ over the gated corpus incl. masters, output: 32.8%, used_in: outside_yards_comparison}
    - {name: TAM uplift, formula: corrected portfolio TAM minus disclosed-only portfolio TAM, output: ~$1.31B, used_in: guardrail_note}
  rounding_rules: Whole $M in the table; one decimal place for percentage shares. The 0.33 anchor target rounds the computed ~32.8%.
  reconciliation: The corrected outside-yards share (~32.8%) is the conclusion; the disclosed-only values (the ~87% announcement headline and the 73.6% workbook figure) are redaction artifacts shown only as a guardrail. The ~32.8% all-gated outside-yards POP is kept distinct from the applied 12.5% BC supplier coefficient.

qa:
  guardrails:
    - Combined masters equal ~$14.58B; gated corpus incl. masters equals ~$21.71B; masters are 67.2% of gated.
    - Corrected outside-yards POP equals ~32.8% and is the conclusion.
    - The disclosed-only artifact (73.6% workbook; ~87% announcement headline) is explicitly labeled an artifact and never headlined.
    - The ~32.8% outside-yards POP is kept distinct from the 12.5% BC supplier coefficient.
  source_checks:
    - Sources are the exact real citations in chrome.sources; no internal workbook tabs or chart IDs rendered.
    - Internal provenance (TAM Build, POP Audit, POP Corpus, Inputs) appears only in meta.inputs, tie_out, and reserve evidence.
  engine_checks:
    - "all body objects within BODY"
    - "title <= 2 lines"
    - "charts: [] -> no chart rId checks"
    - "slide_probe --table-fit   # optional: estimated table row-height info"
    - "resolved column widths sum to the recon_table region width"
    - "table, two-bar comparison, and guardrail note all sit within BODY (size rows via estimate_row_heights)"
