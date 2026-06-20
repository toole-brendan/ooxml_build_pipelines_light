# SlideSpec - submarines `sib_exclusion` (deck slide 16)
# Ledger + treatment-card body slide: a three-row GRAY EXCLUSION LEDGER (native table:
# BlueForge / TMG / IALR plus a total row, with an explicit Rationale column), paired with
# a focal black-outlined treatment card that dominates the slide and states why the SIB
# pass-throughs are excluded from component TAM AND SAM, a total-excluded readout, and a
# small SIB/MIB terminology note. Deliberately NOT a ranked bar - it breaks the run of
# three consecutive ranked-bar slides (S13 bucket TAM, S14 SAM scenarios, S15 visible
# suppliers) that would otherwise end the section, and now CARRIES THE FOLDED A8 DETAIL
# (former appendix_sib_exclusion_detail) in its reserve. Ledger fills are gray exclusion
# tones (GRAY_5/GRAY_2/GRAY_1), never the counted-TAM/SAM blues. SIB (Submarine Industrial
# Base) is the standard term in all visible copy.

meta:
  slide_id: subs-s16
  slide_order: 16               # deck-spec narrative position; not yet registered (KNOWN GAP, S12-S16)
  module_name: sib_exclusion.py
  slide_type: body
  section: SAM and Supplier Landscape
  archetype: exclusion_ledger_plus_treatment_card
  story_role: Keep the model clean - show the large SIB capacity pass-throughs and explain why they are excluded from component TAM and SAM.
  inputs:
    - Chart Data CD_16_SIBExclusion
    - SIB Excluded tab (sib_total_cell, per-entity $)
    - SAM Build (SAM exclusions)
    - Source Index
  related_appendix: []   # A8 (appendix_sib_exclusion_detail) deleted; its detail is folded into this slide's reserve

chrome:
  section: Market sizing
  breadcrumb_topic: SIB exclusion
  title_topic: SIB Exclusion
  title_finding: Capacity-development pass-throughs are material but outside component TAM
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - GAO-25-106286
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) GAO-25-106286"

story:
  objective: Explain why large SIB capacity-development recipients are excluded from component TAM/SAM even though they are material dollar flows in the broader industrial base.
  do_not_say:
    - Do not minimize SIB; it is crucial context, just outside the component-TAM boundary.
    - Do not treat SIB pass-throughs as additive component TAM.
    - Use SIB (Submarine Industrial Base); do not use MIB / Maritime Industrial Base in visible copy.
  known_caveats:
    - SIB dollars fund supplier development, workforce, capacity, qualification, and infrastructure - not current component delivery into a hull.
    - Earlier source files use MIB / Maritime Industrial Base terminology; the deck standardizes on SIB.

regions:
  coord_basis: BODY
  layout_pattern: exclusion_ledger_plus_right_treatment_card
  # Three-row gray exclusion ledger (native table) on the left ~62%, a focal black-outlined
  # treatment card to its right that dominates the slide, a total-excluded readout beneath
  # the ledger, and a pinned SIB/MIB terminology note.
  detail_table:     {x: 0%, y: below(title_band), w: 62%, h: fit_content}
  treatment_card:   {x: right_of(detail_table) + GAP, y: align_top(detail_table), w: remaining, h: fit_content}
  total_strip:      {x: 0%, y: below(detail_table) + GAP, w: 62%, h: fit_content}
  terminology_note: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: table,   region: detail_table,     prominence: primary,   paint_order: 1, content: SIB exclusion ledger (BlueForge / TMG / IALR + total, with Rationale column; gray exclusion fills), tie_out: CD_16_SIBExclusion / SIB Excluded}
  - {id: e2, type: callout, region: treatment_card,   prominence: primary,   paint_order: 2, content: focal treatment card (exclude from component TAM and SAM) - the dominant object on the slide}
  - {id: e3, type: note,    region: total_strip,      prominence: tertiary,  paint_order: 3, content: total excluded readout}
  - {id: e4, type: note,    region: terminology_note, prominence: tertiary,  paint_order: 4, content: SIB / MIB terminology note}


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
    e2:
      text_runs:
      - role: treatment cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: treatment body
        size: MESSAGE_11PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: total label
        size: MESSAGE_11PT
        color: DK
        font: FONT
      - role: total value
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
    e4:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts:
  - id: chart_1
    factory: waterfall_chart        # decision (2026-06-04): waterfall, per docs/chart_conversion_spec.md (SRT pattern); supersedes the earlier ledger-table design below
    chart_index: 0                  # -> rId2
    semantic:
      reader_takeaway: The three visible SIB pass-throughs build to the ~$4,251.8M total excluded; all sit outside component TAM and SAM.
    data:
      steps:
        - {label: BlueForge, value: 4173.3, kind: start}
        - {label: TMG, value: 77.0, kind: delta}
        - {label: IALR, value: 1.5, kind: delta}
        - {label: Total excluded, value: null, kind: end}
    params:
      value_axis_format: '"$"#,##0"M"'
      increase_color: "A1A1A1"      # SRT gray - these are excluded dollars, not hero TAM
      decrease_color: "A1A1A1"
      total_color: "79838F"         # neutral; the point of the slide is that this is NOT counted TAM
      show_value_labels: true
      show_gridlines: true
      major_gridline_color: GRAY_1
      cat_label_size_pt: 9
      cat_header: SIB pass-through
      title: null                   # house style: external exhibit_title element
    external_title:
      text: SIB capacity-development pass-throughs (excluded from component TAM and SAM)
      size: CHART_TITLE_10PT
      italic: true
      color: DK

# SUPERSEDED (2026-06-04): the module renders the chart_1 waterfall above, not this ledger
# table. The earlier object-discipline pass authored this table but the module never built it;
# decision (b) made the slide a waterfall. Block retained for reference only - not built.
tables:
  - id: ledger_1
    element: e1
    role: primary
    factory: house_table
    semantic:
      table_name: SIB exclusion ledger
      purpose: summarize       # entity-by-entity treatment with explicit rationale, not a ranking
      reader_takeaway: Every visible SIB pass-through is excluded from component TAM and SAM by role, and the three tie to the $4,251.8M anchor.
      row_order: Largest excluded recipient first (BlueForge), then TMG, then IALR, then the total row.
      highlight_rows: [4]      # total row
      guardrails:
        - Ledger fills are gray exclusion tones (GRAY_5/GRAY_2/GRAY_1), never the counted-TAM/SAM blues.
        - Visible copy uses SIB; MIB appears only in the footnote reconciliation.
        - The total ties to the SIB Excluded validation anchor of $4,251.8M.
    render:
      table_skin: dark         # dark house skin, but recolored to GRAY exclusion fills (never counted-TAM/SAM blue)
      size: 900                # 9.0pt; row_h derives size_pt = size/100
      column_widths:
        mode: ratio
        values: [2.8, 1.0, 1.1, 2.5]   # Entity | Amount $M | Treatment | Rationale
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "l", "l"]
      row_h: {fn: estimate_row_heights, size_pt_from: size, header_size_pt_from: size}
      rows:
        - ["Entity", "Amount $M", "Treatment", "Rationale"]
        - ["BlueForge Alliance", "4,173.3", "Exclude", "Capacity development (nonprofit integrator)"]
        - ["Training Modernization Group, Inc.", "77.0", "Exclude", "Workforce and training"]
        - ["Institute for Advanced Learning and Research", "1.5", "Exclude", "Industrial-base support, applied R&D"]
        - ["Total excluded SIB pass-throughs", "4,251.8", "Exclude", "Outside component TAM and SAM"]
      cell_fills:
        # header row -> GRAY_5; BlueForge -> GRAY_2; TMG + IALR -> GRAY_1; total row -> GRAY_5
        "(0,0)": GRAY_5
        "(0,1)": GRAY_5
        "(0,2)": GRAY_5
        "(0,3)": GRAY_5
        "(1,0)": GRAY_2
        "(1,1)": GRAY_2
        "(1,2)": GRAY_2
        "(1,3)": GRAY_2
        "(2,0)": GRAY_1
        "(2,1)": GRAY_1
        "(2,2)": GRAY_1
        "(2,3)": GRAY_1
        "(3,0)": GRAY_1
        "(3,1)": GRAY_1
        "(3,2)": GRAY_1
        "(3,3)": GRAY_1
        "(4,0)": GRAY_5
        "(4,1)": GRAY_5
        "(4,2)": GRAY_5
        "(4,3)": GRAY_5
      cell_text_colors:
        # WHITE text on the dark GRAY_5 header and total rows for contrast
        "(0,0)": WHITE
        "(0,1)": WHITE
        "(0,2)": WHITE
        "(0,3)": WHITE
        "(4,0)": WHITE
        "(4,1)": WHITE
        "(4,2)": WHITE
        "(4,3)": WHITE
      cell_bold:
        "(4,0)": true
        "(4,1)": true
      footnotes:
        - "SIB (Submarine Industrial Base) capacity-development pass-throughs, excluded from component TAM and SAM by role, not size. Earlier source files use MIB / Maritime Industrial Base. Total ties to the SIB Excluded validation anchor of $4,251.8M."
    columns:
      - {name: Entity, unit: text, tie_out: CD_16_SIBExclusion / SIB Excluded}
      - {name: Amount $M, unit: $M, tie_out: CD_16_SIBExclusion / SIB Excluded}
      - {name: Treatment, unit: text, tie_out: SAM Build section 8 guardrail}
      - {name: Rationale, unit: text, tie_out: SAM Build section 8 guardrail (analyst classification)}

shapes:
  - id: treatment_1
    element: e2
    factory: text_box
    fill: GRAY_2              # scope-boundary / caveat treatment; the dominant black-outlined focal object on the slide
    line_color: BLACK         # focal/hero: black outline at 1.5pt
    line_width: 19050         # 1.5pt
    insets: INSETS_MESSAGE
    text: "EXCLUDE FROM COMPONENT TAM AND SAM. SIB dollars fund supplier development, workforce, capacity expansion, qualification, and infrastructure rather than current components delivered into a hull. Material to the industrial-base story, not additive component TAM."
    meaning: The focal "so what" and the dominant object on the slide - SIB is material industrial-base context, not additive component market.
  - id: total_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Total excluded SIB pass-throughs: ~$4,252M"   # MESSAGE_11PT, bold value
    meaning: Anchors the excluded set to the ~$4.25B SIB total without crowding the ledger.
  - id: terminology_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Deck standardizes on SIB (Submarine Industrial Base); earlier source files may use MIB (Maritime Industrial Base)."   # FINEPRINT_8_5PT italic
    meaning: Reconciles the SIB term used here with MIB terminology in older research files.

commentary:
  visible:
    element: e2
    container: callout         # the focal treatment card is the visible commentary
    title:
    bullets:
      - {lead: "Treatment:", body: "material to the industrial-base story, not additive component TAM."}
    body_size: DENSE_BODY_10PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It closes the SAM and Supplier Landscape section (S12-S16) by
      keeping the model clean: it removes the large SIB capacity pass-throughs from the
      market numerator so the component TAM/SAM is not overstated. Excluding these is the
      SAM Build Section 8 guardrail.

      THE EXCLUDED SET. ~$4,252M total visible, dominated by BlueForge Alliance ~$4,173M,
      then Training Modernization Group ~$77M and the Institute for Advanced Learning and
      Research ~$1.5M. BlueForge alone is more than $4.1B in the visible excluded set, large
      enough to distort the visible subaward stream if treated as an ordinary component
      supplier.

      WHY THEY ARE EXCLUDED (the treatment). SIB (Submarine Industrial Base) dollars fund
      shipyard capacity expansion, workforce and training programs, supplier development,
      qualification infrastructure, and industrial-base R&D - investment in FUTURE supplier
      capacity, not current component manufacture into a hull. Including them in component
      TAM would overstate the commercial supplier opportunity and confuse the market
      definition. BlueForge Alliance is a nonprofit integrator that channels submarine
      supplier-development funding for the shipbuilders (GAO-25-106286); a dedicated SIB
      Program Office was directed by Navy memorandum in June 2024 and has operated since
      September 2024.

      THE BROADER SIB FLOW (context, not in the numerator). The SIB line carries roughly
      $1-2B per year of capacity-investment spending, routed primarily through the Columbia
      prime construction contract; DoD has invested more than $10B in the submarine
      industrial base to date (GAO-26-109068), with CRS placing the running total near
      $9.8B through FY2028 and AUKUS Pillar 1 adding a $3B Australian contribution to the
      U.S. submarine industrial base (CRS RL32418). This is exactly why the supplier
      opportunity is expanding - the deck can use SIB as a tailwind argument while keeping
      SIB pass-throughs out of the market-size numerator.

      TERMINOLOGY. Visible copy uses SIB (Submarine Industrial Base). Earlier research files
      and some source documents use MIB / Maritime Industrial Base for the same flow; the
      one glossary reconciliation lives on the workbook's Methodology and Scope tab. The
      first publicly named downstream SIB sub-recipient is AML3D; it is held OFF this slide
      by default (showing it would require adding its source to the footer). Do not minimize
      SIB - it is crucial context, simply outside the component TAM/SAM boundary.

      DENSITY GUIDANCE. Default is the gray three-row exclusion ledger + treatment card +
      total + terminology note. To densify, add one line on the SIB role split (capacity vs
      workforce vs R&D) in the treatment card, or a single AML3D downstream example (then
      update the source footer). Keep the ledger rows gray (exclusion), never the
      counted-TAM/SAM blues, and do not let the slide become a BlueForge profile.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 2, safe_containers: [treatment_card, total_strip], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Role, not size, decides:"
        body: "SIB dollars are excluded because their role is capacity development, not component delivery - size is large but the boundary is about role."
        evidence: SAM Build section 8 guardrail; SIB Excluded
        safe_container: treatment_card
        density_trigger: If the treatment card gains a line, lead with this.
      - priority: 2
        lead: "BlueForge dominates:"
        body: "BlueForge Alliance (~$4.17B) is the single largest named SIB recipient and a nonprofit integrator for the shipbuilders."
        evidence: GAO-25-106286; SIB Excluded
        safe_container: total_strip
        density_trigger: Add when a reviewer asks what BlueForge is.
      - priority: 3
        lead: "Why it matters anyway:"
        body: "SIB is the investment side of the same shift the deck documents on the demand side - >$10B invested to expand the supplier base shipbuilders are outsourcing to."
        evidence: GAO-26-109068; Maritime Industrial Base (wiki 10)
        safe_container: treatment_card
        density_trigger: Add for an investor audience on trajectory.
      - priority: 4
        lead: "Scale of the SIB line:"
        body: "The SIB line runs ~$1-2B per year of capacity investment, routed primarily through the Columbia prime construction contract."
        evidence: Maritime Industrial Base (wiki 10)
        safe_container: total_strip
        density_trigger: Add if the total readout has room for a second line.
      - priority: 5
        lead: "AUKUS contribution:"
        body: "AUKUS Pillar 1 adds a $3B Australian contribution to the U.S. submarine industrial base, on top of DoD's own >$10B."
        evidence: CRS RL32418
        safe_container: treatment_card
        density_trigger: Add for an audience focused on the policy tailwind.
      - priority: 6
        lead: "Downstream example (held off):"
        body: "AML3D is the first publicly named downstream SIB sub-recipient; add it only as an intentional example, and update the source footer if shown."
        evidence: Maritime Industrial Base (wiki 10)
        safe_container: total_strip
        density_trigger: Add only if a downstream example is wanted; requires a footer update.
      - priority: 7
        lead: "SIB Program Office:"
        body: "A dedicated SIB Program Office was directed by Navy memorandum in June 2024 and has operated since September 2024."
        evidence: GAO-25-106286
        safe_container: treatment_card
        density_trigger: Add if the institutional history is relevant to the audience.
      - priority: 8
        lead: "Terminology:"
        body: "Visible copy uses SIB; earlier files use MIB / Maritime Industrial Base for the same flow - the glossary note lives on Methodology and Scope."
        evidence: SIB Excluded module docstring; Methodology and Scope tab
        safe_container: terminology_note
        density_trigger: Keep as the terminology note; expand only if reviewers raise the MIB/SIB difference.
      - priority: 9
        lead: "Clean numerator:"
        body: "Excluding SIB keeps component TAM/SAM as current-delivery opportunity; including it would overstate the commercial supplier market."
        evidence: SAM Build section 8; QA Reconciliation
        safe_container: treatment_card
        density_trigger: Add if a reader asks why such large dollars are dropped.
      # --- Folded from deleted appendix A8 (appendix_sib_exclusion_detail) ---
      - priority: 10
        lead: "Would distort the model:"
        body: "In FY2024 BlueForge alone received ~$2.7B against the Columbia prime, ~42% of that year's Columbia Basic Construction; counting it would inflate the apparent outsourcing rate by ~two-thirds."
        evidence: Maritime Industrial Base (wiki 10)
        safe_container: treatment_card
        density_trigger: Add when a reviewer asks how large the distortion would be if SIB were counted (folded A8 detail).
      - priority: 11
        lead: "Role, not size, decides:"
        body: "BlueForge is excluded despite being the largest visible recipient because its role is pass-through, not component delivery - the boundary is about role, not magnitude."
        evidence: SAM Build section 8
        safe_container: treatment_card
        density_trigger: Add when a reviewer asks why the single largest recipient is the one dropped (folded A8 detail).
    do_not_add:
      - MIB / Maritime Industrial Base in any visible copy (use SIB)
      - any framing that SIB is additive component TAM
      - AML3D in the ledger unless intentionally added as a downstream example (then update the footer)
      - turning the slide into a BlueForge company profile

data_and_calculations:
  data_inputs:
    - {input: BlueForge Alliance,                                value: 4173.3, unit: $M, treatment: exclude, tie_out: CD_16_SIBExclusion / SIB Excluded, used_in: ledger_1}
    - {input: Training Modernization Group Inc.,                 value: 77.0,   unit: $M, treatment: exclude, tie_out: CD_16_SIBExclusion / SIB Excluded, used_in: ledger_1}
    - {input: Institute for Advanced Learning and Research,      value: 1.5,    unit: $M, treatment: exclude, tie_out: CD_16_SIBExclusion / SIB Excluded, used_in: ledger_1}
  calculations:
    - {name: total excluded SIB, formula: "BlueForge + Training Modernization Group + IALR", output: "~$4,251.8M", used_in: total_1}
  rounding_rules: Ledger amounts shown to one decimal $M (4,173.3 / 77.0 / 1.5 / 4,251.8); the total readout rounds to whole $M (~$4,252M). IALR exact value ~$1.5M noted in data.
  reconciliation: The three entities sum to the SIB exclusion total (~$4,251.8M); this total is excluded from component TAM and every SAM scenario.

qa:
  guardrails:
    - All three excluded entities plus the total row appear in the ledger with the values above; the total ties to the $4,251.8M SIB Excluded anchor (~$4,252M).
    - The slide states SIB is excluded from component TAM AND SAM, and explains why (capacity vs current components).
    - Ledger fills are gray exclusion tones (header/total GRAY_5 with WHITE text, BlueForge GRAY_2, TMG/IALR GRAY_1), never the counted-TAM/SAM blues.
    - Visible copy uses SIB; MIB appears only inside the SIB/MIB reconciliation note and the ledger footnote.
    - AML3D is not shown unless intentionally added (with a source-footer update).
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov FFATA/FSRS, GAO-25-106286); no internal docs, workbook tabs, or chart IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - resolved column widths sum to its region width   # ledger_1 columns [2.8,1.0,1.1,2.5] -> detail_table width
