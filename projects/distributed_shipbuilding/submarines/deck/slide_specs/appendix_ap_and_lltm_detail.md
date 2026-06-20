# SlideSpec - submarines `appendix_ap_and_lltm_detail` (appendix A3, deck slide 22)
# Appendix detail table backing the body AP and LLTM slide (S11). A native
# reconciliation table owns the page: gross P-10 advance-procurement top-line
# steps down through GFE/design/weapons, the portion already inside Basic
# Construction, and an un-itemized residual to a $0.000B additive base. A compact
# formula line sits above the table; a right-side boundary warning card plus a
# no-fill interpretation rail reinforce that AP and LLTM are reference timing
# evidence, not additive TAM. No chart (the body slide owns the waterfall).

meta:
  slide_id: subs-a3
  slide_order: A3                 # appendix letter (registry comment maps A3 -> appendix_ap_and_lltm_detail)
  module_name: appendix_ap_and_lltm_detail.py
  slide_type: appendix
  section: Appendix
  archetype: reconciliation_table_plus_boundary_warning
  story_role: Back the body AP and LLTM slide (S11) with the exact line-item reconciliation from gross P-10 advance procurement to a $0.000B additive base, proving the AP and LLTM additive contribution to headline TAM is zero.
  inputs:
    - AP Bridge section 5 (P-10 -> TAM reconciliation bridge, FY22-27)         # data_ap_bridge.py §5
    - AP Bridge section 4 (P-10 bucket -> TAM treatment crosswalk)             # data_ap_bridge.py §4
    - AP Bridge sections 2-3 (Virginia LI 2013 / Columbia LI 1045 P-10 buckets)
    - TAM Build section 2 (AP/LLTM base in TAM, confirmed 0)                    # model_tam_build.py §2
  related_appendix: []

chrome:
  section: Appendix
  breadcrumb_topic: AP and LLTM detail
  title_topic: AP and LLTM Detail
  title_finding: Gross P-10 reference flow reconciles to a $0 additive base
  layout: slideLayout4            # -> module-level LAYOUT
  sources:
    - U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10
    - U.S. DoD daily Contracts announcements
    - CRS RL32418
  source_line_exact: "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-10; (2) U.S. DoD daily Contracts announcements; (3) CRS RL32418"

story:
  objective: Show the exact line-item bridge from gross P-10 advance-procurement reference flow to a $0.000B additive base under the P-5c Basic Construction boundary, so the body slide's $0 claim is auditable.
  do_not_say:
    - Do not imply AP and LLTM are unimportant; they are material, supplier-heavy reference evidence.
    - Do not add P-10 AP to P-5c Basic Construction; that double counts unless the model boundary is rebuilt.
    - Do not call the gross AP flow current component TAM.
    - Do not present this as a second waterfall; the body slide (S11) owns the waterfall, this is the reconciliation ledger.
  known_caveats:
    - Three-decimal $B values stay exact in the table so the bridge visibly nets to 0.000.
    - The un-itemized overlap (0.589) is an early-Virginia top-line-over-named-detail reconciliation residual, not a separate exclusion category.
    - Gross AP is the authoritative P-10 top-line but overlaps Basic Construction; it is reference magnitude, not additive.

regions:
  coord_basis: BODY
  layout_pattern: reconciliation_table_plus_boundary_warning
  # Left 70%: a one-line formula anchor, then the reconciliation table beneath it.
  # Right 30%: a filled boundary warning card over a no-fill interpretation rail.
  formula_line:         {x: 0%, y: 0%, w: 70%, h: NOTE_H}
  detail_table:         {x: 0%, y: below(formula_line), w: 70%, h: fit_content}
  warning_card:         {x: right_of(detail_table) + GAP, y: 0%, w: remaining, h: 32%}
  interpretation_note:  {x: right_of(detail_table) + GAP, y: below(warning_card) + GAP, w: remaining, h: fit_content}

element_inventory:
  - {id: e1, type: note,     region: formula_line,        prominence: tertiary,  paint_order: 1, content: compact reconciliation formula line}
  - {id: e2, type: table,    region: detail_table,        prominence: primary,   paint_order: 2, content: AP and LLTM reconciliation table (gross to $0 additive base), tie_out: AP Bridge section 5}
  - {id: e3, type: callout,  region: warning_card,        prominence: secondary, paint_order: 3, content: boundary warning card (do not add P-10 AP)}
  - {id: e4, type: rail,     region: interpretation_note, prominence: tertiary,  paint_order: 4, content: no-fill interpretation bullets (evidence / boundary)}


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
      - role: formula values
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: formula operators/body
        size: MESSAGE_11PT
        color: DK
        font: FONT
    e2:
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
    e3:
      text_runs:
      - role: warning cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: warning body
        size: MESSAGE_11PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: rail title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
        italic: true
      - role: bullet lead
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
      - role: bullet body
        size: LABEL_9PT
        color: DK
        font: FONT
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts: []                       # NONE: the body slide (S11) owns the waterfall; appendix uses a native reconciliation table

tables:
  - id: ap_reconciliation_1
    element: e2
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: AP and LLTM reconciliation
      purpose: reconcile
      reader_takeaway: Gross AP and LLTM are material reference flow, but after exclusions and overlap the additive base under the current boundary is $0.000B.
      row_order: gross top-line, GFE/design/weapons exclusion, already-inside-BC exclusion, un-itemized overlap, final additive base
      highlight_rows:
        - Gross AP top-line
        - Additive AP and LLTM base
      guardrails:
        - Do not add P-10 AP to P-5c Basic Construction unless the model boundary is rebuilt.
        - The final $0.000B row must read as visually stronger than the gross AP row.
    render:
      table_skin: rule
      size: 900                  # LABEL_9PT
      column_widths:
        mode: ratio
        values: [2.8, 1.0, 1.4, 2.4]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: ["l", "r", "l", "l"]
      row_h:
        fn: estimate_row_heights
        size_pt_from: size
        header_size_pt_from: size
      rows:
        - ["Step", "Value $B", "Treatment", "Model reason"]
        - ["Gross P-10 AP top-line", "44.709", "Reference", "Authoritative AP total, Va and Col"]
        - ["Less GFE, design, and weapons", "(27.273)", "Exclude", "Nuclear, electronics, ordnance, missile, plans - outside boundary"]
        - ["Less already inside Basic Construction", "(16.847)", "Exclude overlap", "Shipbuilder-procured, CFE, EOQ, HM&E, propulsor"]
        - ["Less un-itemized overlap", "(0.589)", "Reconcile", "Early-Virginia top-line over named detail"]
        - ["Additive AP and LLTM base", "0.000", "Final", "Do not add to TAM"]
      cell_fills:
        "(1,0)": BLUE_1
        "(1,1)": BLUE_1
        "(1,2)": BLUE_1
        "(1,3)": BLUE_1
        "(2,0)": GRAY_1
        "(2,1)": GRAY_1
        "(2,2)": GRAY_1
        "(2,3)": GRAY_1
        "(3,0)": GRAY_2
        "(3,1)": GRAY_2
        "(3,2)": GRAY_2
        "(3,3)": GRAY_2
        "(4,0)": GRAY_1
        "(4,1)": GRAY_1
        "(4,2)": GRAY_1
        "(4,3)": GRAY_1
        "(5,0)": BLUE_5
        "(5,1)": BLUE_5
        "(5,2)": BLUE_5
        "(5,3)": BLUE_5
      cell_bold:
        "(1,1)": true
        "(5,0)": true
        "(5,1)": true
        "(5,2)": true
        "(5,3)": true
      cell_text_colors:
        "(5,0)": WHITE
        "(5,1)": WHITE
        "(5,2)": WHITE
        "(5,3)": WHITE
      footnotes:
        - "Values are cumulative FY2022-FY2027 in $B. Gross AP is the authoritative P-10 top-line shown for reference; it overlaps Basic Construction and is not additive."
    columns:
      - {name: Step, unit: label, tie_out: AP Bridge section 5}
      - {name: Value $B, unit: $B, tie_out: AP Bridge section 5, formula: gross + exclusions + overlap = 0.000}
      - {name: Treatment, unit: label, tie_out: AP Bridge section 4}
      - {name: Model reason, unit: label, tie_out: AP Bridge section 4}

shapes:
  - id: formula_1
    element: e1
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "$44.709B gross P-10 AP, less exclusions and overlap, equals $0.000B additive base."   # MESSAGE_11PT, key values bold
    meaning: One-line arithmetic anchor above the reconciliation table.
  - id: warning_1
    element: e3
    factory: text_box
    fill: GRAY_2
    line_color: BLACK            # the one focal border family on this slide
    line_width: 19050            # 1.5pt focal warning-card frame weight
    insets: INSETS_MESSAGE
    text: |
      DO NOT ADD P-10 AP
      Adding P-10 AP to P-5c Basic Construction would double count unless the model boundary is rebuilt.
    meaning: Boundary warning card; the focal caveat, not a second waterfall.
  - id: interpretation_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: |
      Evidence: AP and LLTM show a large, supplier-heavy purchasing cadence years ahead of construction.
      Boundary: under this model AP and LLTM are reference evidence, not additive TAM.
    meaning: No-fill interpretation rail for the right side.

images: []

commentary:
  visible:
    element: e4
    container: method_note
    title: null
    bullets:
      - {lead: "Evidence:", body: "AP and LLTM show a large, supplier-heavy purchasing cadence years ahead of construction."}
      - {lead: "Boundary:", body: "the additive base is $0.000B under the current P-5c Basic Construction boundary."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This appendix backs the body AP and LLTM slide (S11),
      which lands the answer-first finding that gross P-10 advance procurement is
      large (~$44.7B in the FY2022-FY2027 window) but contributes $0 additive TAM.
      The body slide carries the waterfall; this appendix carries the auditable
      line-item ledger so a diligence reader can trace every step.

      THE RECONCILIATION (AP Bridge section 5, FY22-27, $B).
      - Gross P-10 AP top-line: $44.709B. The authoritative advance-procurement
        total across Virginia (LI 2013) and Columbia (LI 1045), summed over
        FY2022-FY2027 from Exhibit P-10. It is reference magnitude: it overlaps
        Basic Construction and is non-additive.
      - Less GFE, design, and weapons: ($27.273B). Removes the nuclear-plant LLTM
        (Bechtel Plant Machinery, naval reactor - GFE), electronics LLTM
        (Navy-furnished combat-system electronics), ordnance LLTM (WPN/OPN, not
        SCN), missile-compartment LLTM (Common Missile Compartment tubes - GFE /
        industrial base), and Plans / SIB (lead-yard design and supplier-base
        pass-through). These sit outside the P-5c Basic Construction boundary.
      - Less already inside Basic Construction: ($16.847B). Removes the
        shipbuilder-procured LLTM (and CFE), EOQ, HM&E LLTM, and propulsor LLTM -
        direct material that is already inside the P-5c Basic Construction base, so
        wiring P-10 AP as a separate stream would double count the BC TAM.
      - Less un-itemized overlap: ($0.589B). An early-Virginia top-line-over-named-
        detail reconciliation residual; the published P-10 detail does not break out
        every sub-category at the same granularity in every Justification Book, so a
        small residual is expected.
      - Additive AP and LLTM base: $0.000B. Confirmed zero. AP and LLTM contribute
        no TAM beyond the Basic Construction stream.

      WHY THE BUCKETS RESOLVE THIS WAY (AP Bridge section 4 crosswalk). The
      supplier-addressable LLTM - shipbuilder-procured, EOQ, HM&E, propulsor - is
      ALREADY inside the P-5c Basic Construction base, so it is captured by the BC
      coefficient rather than added on top. The GFE buckets (nuclear plant,
      electronics, missile compartment) and the weapons / design buckets (ordnance,
      Plans / SIB) are outside the boundary entirely. Nothing is left to add.

      THE SUPPLIER SIGNAL THAT MATTERS ANYWAY. The shipbuilder-procured LLTM stream
      is the most directly addressable bucket for new and expanding submarine
      suppliers, and it is rising sharply: combined across both classes from roughly
      $0.7-0.9B per year in FY2021-FY2022 to roughly $2.0-2.5B per year at the
      FY2025-FY2027 rate. Columbia shipbuilder-procured LLTM grew from ~$176M in
      FY2021 to ~$1,576M in FY2027; Virginia CFE one-year plus two-year ran ~$542M
      in FY2020-FY2021 up to ~$1,065M in FY2025. This is real, growing supplier
      demand - it just is not additive to the headline TAM denominator.

      MAGNITUDE CHECK. Exhibit P-10 reports Columbia FY2027 current-year AP of
      $4,763M and Virginia FY2025 of ~$3,720M; advance procurement runs roughly
      $3-5B per class per fiscal year, so a cumulative two-class FY2022-FY2027 gross
      AP near $44.7B is consistent with the per-year rates.

      DENSITY GUIDANCE. Default is formula line + reconciliation table + warning
      card + interpretation rail. To densify, add the supplier-signal context into
      the interpretation rail or extend the table footnote; never convert the table
      into a second waterfall (the body slide owns that visual).
    density_modes:
      normal: {visible_bullets: 2, keep: [e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [interpretation_note, formula_line], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Reference stream, not additive:"
        body: "Gross AP and LLTM are material, supplier-heavy evidence of purchasing years ahead of construction; they are simply not additive TAM under the P-5c boundary."
        evidence: AP Bridge section 5; wiki 05 (Exhibit P-10)
        safe_container: interpretation_note
        density_trigger: Add if the warning card risks reading as dismissive of AP and LLTM.
      - priority: 2
        lead: "Already inside BC:"
        body: "The $16.847B already-inside-BC line is shipbuilder-procured, CFE, EOQ, HM&E, and propulsor material - direct material captured by the BC coefficient, so adding it again double counts."
        evidence: AP Bridge section 4 crosswalk
        safe_container: interpretation_note
        density_trigger: Add when a reviewer asks why the overlap line is so large.
      - priority: 3
        lead: "GFE is out of boundary:"
        body: "The $27.273B exclusion is nuclear-plant (BPMI), electronics, ordnance, missile-compartment, and Plans / SIB - GFE, weapons, and design that sit outside P-5c Basic Construction."
        evidence: AP Bridge section 4 crosswalk; wiki 05
        safe_container: interpretation_note
        density_trigger: Add for an audience unfamiliar with the P-10 bucket structure.
      - priority: 4
        lead: "Shipbuilder-procured is the live bucket:"
        body: "Shipbuilder-procured LLTM combined across both classes rose from ~$0.7-0.9B/yr (FY2021-22) to ~$2.0-2.5B/yr (FY2025-27) - real supplier demand, even though it is inside BC and non-additive."
        evidence: wiki 05 (combined shipbuilder-procured LLTM)
        safe_container: interpretation_note
        density_trigger: Add for an investor audience focused on supplier trajectory.
      - priority: 5
        lead: "Un-itemized residual:"
        body: "The $0.589B residual is an early-Virginia top-line-over-named-detail reconciliation, not a separate exclusion; P-10 granularity varies by Justification Book vintage."
        evidence: AP Bridge section 5; wiki 05 (P-40 reconciliation)
        safe_container: detail_table
        density_trigger: Add as a footnote if a reviewer questions the residual line.
      - priority: 6
        lead: "Table discipline:"
        body: "Three-decimal $B values keep the reconciliation visibly tying to 0.000; rounding to one decimal would hide the exact net-to-zero."
        evidence: AP Bridge section 5
        safe_container: detail_table
        density_trigger: Keep in build notes; surface only if values are mistakenly rounded.
      - priority: 7
        lead: "Magnitude anchor:"
        body: "Exhibit P-10 reports Columbia FY2027 AP of $4,763M and Virginia FY2025 of ~$3,720M; ~$3-5B per class per year supports the ~$44.7B cumulative gross."
        evidence: wiki 05 (Exhibit P-10 per-FY top-lines)
        safe_container: formula_line
        density_trigger: Add if the gross top-line is challenged as too large.
      - priority: 8
        lead: "Boundary, not dismissal:"
        body: "Only a rebuilt denominator could decide whether and how to include P-10 AP in headline TAM; under this model it stays reference evidence."
        evidence: AP Bridge section 4; TAM Build section 2
        safe_container: warning_card
        density_trigger: Add for diligence audiences asking about alternate boundaries.
      - priority: 9
        lead: "Confirmed zero:"
        body: "The workbook reconciliation check asserts the AP/LLTM additive base equals 0 within reading precision - this is a confirmed control, not an assumption."
        evidence: AP Bridge section 6 (reconciliation checks)
        safe_container: interpretation_note
        density_trigger: Add when the audience wants proof the zero is enforced, not asserted.
    do_not_add:
      - a duplicate waterfall chart (the body slide owns it)
      - any claim that AP and LLTM are unimportant or non-addressable
      - workbook-tab or wiki-chapter citation in the visible sources footer
      - rounding the table to fewer than three decimals (hides the net-to-zero)

data_and_calculations:
  data_inputs:
    - {input: Gross P-10 AP top-line,                value: 44.709,  unit: $B, year: FY2022-FY2027, tie_out: AP Bridge section 5, used_in: ap_reconciliation_1}
    - {input: Less GFE, design, and weapons,         value: -27.273, unit: $B, year: FY2022-FY2027, tie_out: AP Bridge section 5, used_in: ap_reconciliation_1}
    - {input: Less already inside Basic Construction, value: -16.847, unit: $B, year: FY2022-FY2027, tie_out: AP Bridge section 5, used_in: ap_reconciliation_1}
    - {input: Less un-itemized overlap,              value: -0.589,  unit: $B, year: FY2022-FY2027, tie_out: AP Bridge section 5, used_in: ap_reconciliation_1}
  calculations:
    - {name: Additive AP and LLTM base, formula: "44.709 - 27.273 - 16.847 - 0.589", output: 0.000 $B, used_in: ap_reconciliation_1}
  rounding_rules: All table values in $B with three decimals so the bridge visibly nets to 0.000.
  reconciliation: Gross P-10 AP top-line less GFE/design/weapons, less already-inside-BC, less un-itemized overlap equals $0.000B additive base (AP Bridge section 6 check, confirmed within reading precision).

qa:
  guardrails:
    - The final $0.000B additive-base row (e2) must read as visually stronger than the gross AP row.
    - Do not imply AP and LLTM are counted TAM; they are reference evidence, additive base $0.
    - Do not present a second waterfall; this appendix is a native reconciliation table.
    - Keep three-decimal $B values so the bridge nets visibly to 0.000.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SCN Justification Books Exhibit P-10, DoD daily Contracts, CRS RL32418); no internal docs, workbook tabs, wiki chapters, or chart IDs in the rendered footer.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - if a table exists: resolved column widths sum to its region width
    # no chart on this slide -> chart rId / CHARTS-order checks do not apply
