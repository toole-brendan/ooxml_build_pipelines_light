# SlideSpec - submarines `appendix_top_25_visible_suppliers` (appendix A6)
# Dense appendix two-panel ledger: the top 25 FFATA-visible first-tier subaward
# parents (parent-normalized, the three SIB pass-throughs excluded), ranks 1-13 in
# the left panel and 14-25 in the right, with two evidence chips above and a
# floor-caveat note below. Ranks 11-25 (left as WORKBOOK_REQUIRED in the converted
# spec) are RESOLVED from the workbook entity master / chart-data top-visible-suppliers
# block and the vendor-concentration research. The named list is a floor, not the
# full supplier layer.

meta:
  slide_id: subs-a6
  slide_order: A6               # registry position A6 (deck_spec sec.5 order); module wired in slides/__init__.py
  module_name: appendix_top_25_visible_suppliers.py
  slide_type: appendix
  section: Appendix
  archetype: two_panel_ranked_supplier_ledger
  story_role: Extend the S15 Visible Suppliers top-10 view into a diligence top-25 ledger that makes the FFATA-visible supplier base tangible while preserving that visible filings are a floor, not the full supplier layer.
  inputs:
    - Chart Data CD_15_TopVisibleSuppliers     # internal provenance only (NOT a citation)
    - Entity Master (top supplier indices, parent-normalized $; SAM.gov Entity Management enrichment)
    - SAM Build section 3 (supplier-addressable visible value)
    - Vendors and concentration (wiki 09; top-25 parents, FY counts, headquarters)
    - FFATA-visible subawards (wiki 08; ~759 parents, $30k threshold, floor logic)
  related_appendix:
    - subs-a5   # appendix_sam_bucket_crosswalk (the bucket cues these vendors evidence)

chrome:
  section: Appendix
  breadcrumb_topic: Top visible suppliers
  title_topic: Top 25 Visible Suppliers
  title_finding: The extended FFATA-visible list is a named-vendor floor, not the full supplier layer
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - SAM.gov FFATA/FSRS records
    - SAM.gov Entity Management API
    - FAR 52.204-10
  source_line_exact: "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

story:
  objective: Make the FFATA-visible supplier base tangible by naming the top 25 parents and their visible cumulative value, while preserving the interpretation that public first-tier filings are a floor, not the complete supplier universe or a target-account list.
  do_not_say:
    - Do not present the list as a complete supplier universe, a capture-target list, or a win-probability ordering.
    - Do not sum the 25 rows into a market size; the named list is a subset of the broader visible base.
    - No company logos in this build; names only.
    - Do not describe foreign rank as work location; rank 2 and rank 11 are foreign by incorporation / registered address, not by where work is performed.
  known_caveats:
    - Values are lifetime cumulative FFATA-visible subaward dollars, parent-normalized to legal entity via SAM.gov Entity Management UEIs (FY2016-FY2026 action-date window); they are a floor, not the full supplier layer.
    - Two W International filer entities appear at ranks 12 and 14 (W International, LLC and W International SC, LLC); they share a corporate family (HII acquired W International ~2024-2025) but file under distinct UEIs, so they are kept as separate visible-filer rows and flagged here rather than silently merged.
    - The three SIB pass-through parents (BlueForge Alliance, Training Modernization Group, IALR) are excluded from this list by design; they are detailed on the S16 SIB Exclusion slide, not here (no longer a separate appendix).

regions:
  coord_basis: BODY
  layout_pattern: two_panel_ranked_supplier_ledger
  # Two evidence chips across the top, a full-width two-panel ledger (ranks 1-13 left,
  # 14-25 right) as the primary exhibit, and a pinned floor-caveat note.
  evidence_chip_1: {x: 0%,  y: 0%, w: 26%, h: fit_content}
  evidence_chip_2: {x: right_of(evidence_chip_1) + GAP, y: align_top(evidence_chip_1), w: 34%, h: fit_content}
  supplier_ledger: {x: 0%,  y: below(evidence_chip_1) + GAP, w: 100%, h: body_until(limitation_note)}
  limitation_note: {x: 0%,  y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: callout, region: evidence_chip_1, prominence: secondary, paint_order: 1, content: classified-recipients evidence chip}
  - {id: e2, type: callout, region: evidence_chip_2, prominence: secondary, paint_order: 2, content: visible supplier-addressable value evidence chip}
  - {id: e3, type: table,   region: supplier_ledger, prominence: primary,   paint_order: 3, content: two-panel top-25 visible-supplier ledger (ranks 1-13 left, 14-25 right), tie_out: CD_15_TopVisibleSuppliers + Entity Master top_supplier_indices + wiki 09 top-25}
  - {id: e4, type: note,    region: limitation_note, prominence: tertiary,  paint_order: 4, content: visible-floor limitation note}


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
      - role: chip value
        size: VALUE_14PT
        color: DK
        font: FONT
        bold: true
      - role: chip qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e2:
      text_runs:
      - role: chip value
        size: VALUE_14PT
        color: DK
        font: FONT
        bold: true
      - role: chip qualifier
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e3:
      table_text:
        body:
          size: FINEPRINT_8_5PT
          font: FONT
          color: DK
        header:
          size: FINEPRINT_8_5PT
          font: FONT
          bold: true
        first_column:
          size: FINEPRINT_8_5PT
          font: FONT
          bold: as indicated by cell_bold or house_table first_col
        note: render.size=850; keep as compact appendix exception and resolve row heights from size_pt=8.5
    e4:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  render_notes:
  - For house_table, render.size is the cell text size; convert token to size/100 for estimate_row_heights(size_pt=...).

charts: []                # NONE on this slide -> no chart rIds; chart-fit checks N/A

tables:
  - id: top25_ledger_1
    element: e3
    role: appendix_detail
    factory: house_table
    semantic:
      table_name: Top 25 visible suppliers
      purpose: summarize
      reader_takeaway: The named FFATA-visible supplier stream is broad (25 parents shown, ~759 in total) but incomplete; Northrop Grumman dominates visible flow and the long tail spans most work-type buckets.
      row_order: rank ascending 1-25, split across two panels (1-13 left, 14-25 right)
      highlight_rows:
        - Ranks 1-5 (Northrop Grumman through ESCO Technologies)
      guardrails:
        - Top-5 rows carry light BLUE_1 emphasis; the rest are no-fill rule rows. Never use the dark counted-SAM blues here; this is an evidence ledger, not a counted-market exhibit.
        - Values are lifetime cumulative visible subaward $M, parent-normalized; do not relabel as annual.
        - Foreign-incorporated parents (Leonardo SpA rank 2, Rosyth Royal Dockyard rank 11) are foreign by incorporation, not by work location.
        - The right panel ends at rank 25; the trailing left-panel cell (rank 13 row, right half) is blank by design, not missing data.
    render:
      table_skin: rule
      size: 850                  # 8.5pt body (FINEPRINT_8_5PT); 26 data rows across two panels need the compact step
      column_widths:
        mode: ratio
        # Left panel: Rank | Supplier | $M  ||  Right panel: Rank | Supplier | $M
        values: [0.55, 3.55, 0.75, 0.55, 3.55, 0.75]
        builder_resolves_to_emu: true
        sum_to_region_width: true
      col_w_emu_override: []
      aligns: [ctr, l, r, ctr, l, r]
      row_h:
        fn: estimate_row_heights
        size_pt_from: size
        header_size_pt_from: size
      rows:
        - ["Rank", "Supplier (parent legal entity)", "$M", "Rank", "Supplier (parent legal entity)", "$M"]
        - ["1",  "Northrop Grumman Corporation",                  "1,426.6", "14", "W International SC, LLC",                 "74.1"]
        - ["2",  "Leonardo SpA",                                  "490.6",   "15", "Oil States International, Inc.",          "71.5"]
        - ["3",  "Curtiss-Wright Electro-Mechanical Corp.",       "198.0",   "16", "Precision Custom Components, LLC",        "68.8"]
        - ["4",  "Scot Forge Company",                            "197.5",   "17", "Goodrich Corp. (RTX Collins Aerospace)", "64.9"]
        - ["5",  "ESCO Technologies Inc.",                        "188.5",   "18", "Johnson Controls Navy Systems, LLC",     "58.7"]
        - ["6",  "DC Fabricators Inc.",                           "162.9",   "19", "Globe Composite Solutions, LLC",         "57.3"]
        - ["7",  "Rhoads Metal Fabrications, Inc.",               "141.9",   "20", "CIRCOR International, Inc.",              "53.0"]
        - ["8",  "Curtiss-Wright Corporation",                    "110.8",   "21", "L3Harris Technologies, Inc.",            "52.3"]
        - ["9",  "The Graham Corporation",                        "89.1",    "22", "BWX Technologies, Inc.",                 "51.8"]
        - ["10", "Austal USA, LLC",                               "87.6",    "23", "Advance Mfg. Co., Inc.",                 "51.2"]
        - ["11", "Rosyth Royal Dockyard Ltd. (Babcock)",          "84.0",    "24", "Pegasus Steel, LLC",                     "48.9"]
        - ["12", "W International, LLC",                           "82.6",    "25", "Portland Valve LLC",                     "48.1"]
        - ["13", "Curtiss-Wright Flow Control Corp.",             "74.7",    "",   "",                                       ""]
      cell_fills:
        # Header row
        "(0,0)": BLUE_5
        "(0,1)": BLUE_5
        "(0,2)": BLUE_5
        "(0,3)": BLUE_5
        "(0,4)": BLUE_5
        "(0,5)": BLUE_5
        # Top-5 anchor emphasis (left panel, ranks 1-5): light BLUE_1, NOT the counted-SAM dark blues
        "(1,0)": BLUE_1
        "(1,1)": BLUE_1
        "(1,2)": BLUE_1
        "(2,0)": BLUE_1
        "(2,1)": BLUE_1
        "(2,2)": BLUE_1
        "(3,0)": BLUE_1
        "(3,1)": BLUE_1
        "(3,2)": BLUE_1
        "(4,0)": BLUE_1
        "(4,1)": BLUE_1
        "(4,2)": BLUE_1
        "(5,0)": BLUE_1
        "(5,1)": BLUE_1
        "(5,2)": BLUE_1
      cell_bold:
        "(0,0)": true
        "(0,1)": true
        "(0,2)": true
        "(0,3)": true
        "(0,4)": true
        "(0,5)": true
      cell_text_colors:
        "(0,0)": WHITE
        "(0,1)": WHITE
        "(0,2)": WHITE
        "(0,3)": WHITE
        "(0,4)": WHITE
        "(0,5)": WHITE
      footnotes:
        - "Lifetime cumulative FFATA-visible first-tier subaward value, parent-normalized via SAM.gov Entity Management UEIs, FY2016-FY2026 action dates; the three SIB pass-through parents are excluded. Visible filings are a floor, not the full supplier layer."
    columns: []

shapes:
  - id: chip_1
    element: e1
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3            # secondary evidence chip; not a focal frame
    insets: INSETS_EVIDENCE
    text: "150 classified subaward recipients"   # value VALUE_14PT bold DK; qualifier FINEPRINT_8_5PT DK
    meaning: Coverage evidence chip; frames the 25 named rows as the top of a far larger classified set.
  - id: chip_2
    element: e2
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3            # secondary evidence chip; not a focal frame
    insets: INSETS_EVIDENCE
    text: "~$5.46B supplier-addressable visible value"   # value VALUE_14PT bold DK; qualifier FINEPRINT_8_5PT DK
    meaning: Visible supplier-addressable value chip; the named list is a subset of this base.
  - id: note_1
    element: e4
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Visible does not mean complete: FFATA names first-tier filings above the $30,000 per-action threshold and should be treated as a floor, not the full supplier layer. Across the fifteen in-scope new-construction PIIDs there are ~759 FFATA-visible parents; the 25 shown are the largest."   # FINEPRINT_8_5PT
    meaning: Floor-caveat note; keeps the ledger from reading as a complete or target list.

images: []

commentary:
  visible:
    element: e4
    container: table_note
    title:
    bullets:
      - {lead: "Read:", body: "FFATA-visible vendors are a named floor, not the full supplier layer; ~759 parents in total, the top 25 shown."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHAT THIS APPENDIX BACKS. This is the diligence extension of S15 (Visible
      Suppliers), which shows the top 10 on the main deck. It names the top 25
      FFATA-visible first-tier subaward parents and bounds the claim: the visible
      stream is a floor. It pairs with A5 (the bucket crosswalk that uses several of
      these same vendors as NAICS-4 evidence cues); the three SIB pass-throughs that
      would otherwise dominate this list are excluded and detailed on the S16 SIB
      Exclusion slide (no longer a separate appendix).

      WHERE THE 25 ROWS COME FROM. The list is the top 25 FFATA-visible first-tier
      subaward recipients across the fifteen in-scope new-construction PIIDs, summed
      across FY2016-FY2026 action dates, with the three named SIB pass-through parents
      (BlueForge Alliance, Training Modernization Group, Institute for Advanced
      Learning and Research) excluded. Vendors are aggregated to parent legal entity
      by SAM.gov Unique Entity Identifier; subsidiaries are rolled up to the parent
      where the SAM Entity Management API confirms the corporate relationship. The
      top-10 ($M) tie exactly to the S15 chart (Northrop Grumman 1,426.6; Leonardo
      490.6; Curtiss-Wright Electro-Mechanical 198.0; Scot Forge 197.5; ESCO 188.5; DC
      Fabricators 162.9; Rhoads 141.9; Curtiss-Wright Corp. 110.8; Graham 89.1; Austal
      87.6). Ranks 11-25 (left as placeholders in the converted spec because the
      converting agent lacked data) are resolved here from the workbook entity master
      and the vendor-concentration research: Rosyth Royal Dockyard (Babcock) 84.0; W
      International, LLC 82.6; Curtiss-Wright Flow Control 74.7; W International SC, LLC
      74.1; Oil States International 71.5; Precision Custom Components 68.8; Goodrich
      Corp. (RTX Collins) 64.9; Johnson Controls Navy Systems 58.7; Globe Composite
      Solutions 57.3; CIRCOR International 53.0; L3Harris Technologies 52.3; BWX
      Technologies 51.8; Advance Mfg. Co. 51.2; Pegasus Steel 48.9; Portland Valve
      48.1.

      WORK-TYPE READ (cross-reference to A5 buckets). Electrical / power: Northrop
      Grumman (sonar, combat systems, propulsion electronics), Leonardo, Curtiss-Wright
      Electro-Mechanical, L3Harris, BWX. Castings and forgings: Scot Forge, Pegasus
      Steel. Structural fabrication: DC Fabricators, Rhoads, Austal, W International,
      Precision Custom Components. Piping / valves / pumps: Curtiss-Wright Flow Control,
      CIRCOR, Portland Valve, Oil States. HM&E: The Graham Corporation (heat
      exchangers), Johnson Controls Navy Systems (HVAC). Coatings / insulation: Globe
      Composite Solutions. The spread across buckets supports the thesis that the
      supplier layer is real and multi-firm, not a theoretical residual.

      THE CURTISS-WRIGHT FAMILY. Three Curtiss-Wright SAM entities appear (ranks 3, 8,
      13): Electro-Mechanical (nuclear-grade pumps), the Curtiss-Wright Corporation
      parent rollup, and Flow Control (valves). Aggregated, the Curtiss-Wright family
      is ~$383M, the second-largest aggregate FFATA recipient after Northrop Grumman.
      They are kept as separate filer rows here because they file under distinct UEIs.

      FOREIGN ROWS ARE FOREIGN BY INCORPORATION, NOT WORK LOCATION. Leonardo SpA (Italy,
      rank 2, ~$491M) and Rosyth Royal Dockyard Limited (UK, Babcock subsidiary, rank
      11, ~$84M) are foreign by incorporation / registered address; the FFATA geography
      reflects vendor registered address, not where work is performed. Foreign-
      registered vendors are ~3% of total FFATA-visible flow, concentrated on Columbia
      (Babcock Rosyth, APCO Technologies) via the shared UK Dreadnought design lineage.

      THE W INTERNATIONAL DUPLICATE. Two W International filer entities sit at ranks 12
      and 14 (W International, LLC ~$83M; W International SC, LLC ~$74M). They share a
      corporate family; HII acquired W International ~2024-2025 (a documented exception
      to HII CEO Chris Kastner's anti-vertical-integration posture). Because they file
      under distinct UEIs they are kept as separate visible-filer rows and flagged in
      known_caveats rather than silently merged.

      WHY VISIBLE IS A FLOOR (the load-bearing caveat). FAR 52.204-10 requires primes to
      report first-tier subawards above the $30,000 per-action threshold to FSRS,
      surfaced via SAM.gov. The visible stream excludes purchased material booked as
      direct cost, lower-tier subcontracts, indirect / G&A, long-term standing supplier
      agreements, and most of the HII Newport News team-build share (HII-NNS files at
      ~0% against the GDEB primes despite performing roughly half of Virginia by
      workload). Across the fifteen in-scope PIIDs the visible stream captures ~$6.1B
      cumulative across ~759 unique parents (ex-SIB); the supplier-addressable subset is
      ~$5.46B across ~150 classified recipients. The 25 named here are the top of that
      distribution, not the whole of it. NAICS enrichment of the top 150 covers ~93.5%
      of dollar-weighted flow but only ~70% of vendor count (~45 of the top 150 are no
      longer samRegistered=Yes).

      DEMAND BACKDROP (directional, not a sizing input). DoD has invested >$10B in the
      submarine industrial base (GAO-26-109068); the FFATA-visible supplier base
      expanded roughly 30-fold from ~a dozen named parents in FY2016 to 371 in FY2023
      even after the SIB pass-throughs are excluded; HII has guided +30% YoY outsourcing
      hours (HII FY26 Q1). The visible supplier base is expanding for structural reasons.

      DENSITY GUIDANCE. Default is two evidence chips + the two-panel ledger + the floor
      note. To densify, add a work-type tag beside the top names, a third evidence chip
      (~759 broader parents), or a concentration line (Northrop Grumman alone is a large
      share of the ~$5.46B). Keep the floor caveat prominent and never turn the ranking
      into a target list.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 3, safe_containers: [limitation_note, supplier_ledger, evidence_chip_2], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Visible floor:"
        body: "FFATA names first-tier filings above the $30,000 per-action threshold, so the 25 named parents are a floor inside a ~759-parent visible base, not the complete supplier layer."
        evidence: FAR 52.204-10; FFATA-visible subawards (wiki 08)
        safe_container: limitation_note
        density_trigger: Keep visible in all versions; it is the core guardrail.
      - priority: 2
        lead: "Northrop Grumman leads:"
        body: "Northrop Grumman ~$1,427M is the single largest visible recipient, ~2.5x the second-place vendor, on sonar, combat systems, and propulsion electronics."
        evidence: Vendors and concentration (wiki 09); Entity Master
        safe_container: supplier_ledger
        density_trigger: Add as a cell footnote if rank 1 is questioned.
      - priority: 3
        lead: "Curtiss-Wright family:"
        body: "Three Curtiss-Wright filer entities (ranks 3, 8, 13) aggregate to ~$383M, the second-largest corporate family after Northrop Grumman; kept separate because they file under distinct UEIs."
        evidence: Vendors and concentration (wiki 09); SAM.gov Entity Management API
        safe_container: supplier_ledger
        density_trigger: Add if a reader asks why three Curtiss-Wright lines appear.
      - priority: 4
        lead: "Foreign by incorporation:"
        body: "Leonardo SpA (rank 2) and Rosyth Royal Dockyard (rank 11) are foreign by incorporation / registered address, not by work location; FFATA geography is registered address."
        evidence: FFATA-visible subawards (wiki 08; geographic registration); Vendors and concentration (wiki 09)
        safe_container: limitation_note
        density_trigger: Add if a reviewer reads foreign rows as offshore work.
      - priority: 5
        lead: "Work-type spread:"
        body: "The 25 span electrical (Northrop Grumman, Leonardo, L3Harris), structural (DC Fabricators, Rhoads, Austal, W International), castings (Scot Forge, Pegasus), piping (Curtiss-Wright Flow Control, CIRCOR, Portland Valve), and HM&E (Graham, Johnson Controls)."
        evidence: SAM bucket crosswalk (A5); Worktype Evidence
        safe_container: supplier_ledger
        density_trigger: Add a work-type tag column if the ledger widens.
      - priority: 6
        lead: "Coverage context:"
        body: "~759 broader FFATA-visible unique parents back the named 25; the supplier-addressable subset is ~$5.46B across ~150 classified recipients."
        evidence: FFATA-visible subawards (wiki 08); Entity Master
        safe_container: evidence_chip_2
        density_trigger: Add only if the layout can support a third evidence chip.
      - priority: 7
        lead: "Not a target list:"
        body: "The ranking is visible historical subaward flow, not capture probability or a recommended pursuit order; do not sum the rows into a market size."
        evidence: story.do_not_say
        safe_container: limitation_note
        density_trigger: Add if an investor reads the ledger as a pipeline.
      - priority: 8
        lead: "HII Newport News gap:"
        body: "HII-NNS performs roughly half of Virginia by workload yet files at ~0% against the GDEB primes, the single largest omission from the visible stream."
        evidence: HII Newport News gap (wiki 11); HII Form 10-K
        safe_container: limitation_note
        density_trigger: Add when a reviewer asks why a known major builder is absent.
      - priority: 9
        lead: "W International acquisition:"
        body: "Two W International filer entities (ranks 12, 14) share a corporate family; HII acquired W International ~2024-2025, a documented exception to its anti-vertical-integration stance."
        evidence: Vendors and concentration (wiki 09); HII FY24 Q4
        safe_container: supplier_ledger
        density_trigger: Add if a reader asks why two W International lines appear.
      - priority: 10
        lead: "Parent normalization:"
        body: "Subsidiaries are rolled up to parent legal entity via SAM.gov Entity Management UEIs where confirmed; ~45 of the top 150 are not currently samRegistered=Yes."
        evidence: SAM.gov Entity Management API; Entity Master
        safe_container: limitation_note
        density_trigger: Add if a reader questions the normalization basis.
      - priority: 11
        lead: "Base expanded ~30x:"
        body: "The FFATA-visible supplier base grew from ~a dozen named parents in FY2016 to 371 in FY2023 (ex-SIB), a roughly 30-fold expansion."
        evidence: Vendors and concentration (wiki 09; supplier-base size over time)
        safe_container: limitation_note
        density_trigger: Add for an investor audience focused on trajectory.
      - priority: 12
        lead: "Names, not legal caps:"
        body: "Display names are Title Case parent names, not all-caps SAM legal names; no logos in this build."
        evidence: deck convention; story.do_not_say
        safe_container: supplier_ledger
        density_trigger: Build QA only; do not render as a chip.
    do_not_add:
      - company logos
      - target-account, capture %, or win-probability language
      - a summed market total from the 25 rows
      - the three SIB pass-through parents (BlueForge, TMG, IALR) - those are detailed on the S16 SIB Exclusion slide

data_and_calculations:
  data_inputs:
    - {input: Northrop Grumman Corporation,               value: 1426.6, unit: $M, rank: 1,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Leonardo SpA,                               value: 490.6,  unit: $M, rank: 2,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Curtiss-Wright Electro-Mechanical Corp.,    value: 198.0,  unit: $M, rank: 3,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Scot Forge Company,                         value: 197.5,  unit: $M, rank: 4,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: ESCO Technologies Inc.,                     value: 188.5,  unit: $M, rank: 5,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: DC Fabricators Inc.,                        value: 162.9,  unit: $M, rank: 6,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Rhoads Metal Fabrications Inc.,             value: 141.9,  unit: $M, rank: 7,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Curtiss-Wright Corporation,                 value: 110.8,  unit: $M, rank: 8,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: The Graham Corporation,                     value: 89.1,   unit: $M, rank: 9,  tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Austal USA LLC,                             value: 87.6,   unit: $M, rank: 10, tie_out: CD_15_TopVisibleSuppliers / Entity Master, used_in: top25_ledger_1}
    - {input: Rosyth Royal Dockyard Ltd. (Babcock),       value: 84.0,   unit: $M, rank: 11, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: W International LLC,                         value: 82.6,   unit: $M, rank: 12, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Curtiss-Wright Flow Control Corp.,          value: 74.7,   unit: $M, rank: 13, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: W International SC LLC,                      value: 74.1,   unit: $M, rank: 14, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Oil States International Inc.,               value: 71.5,   unit: $M, rank: 15, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Precision Custom Components LLC,             value: 68.8,   unit: $M, rank: 16, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Goodrich Corp. (RTX Collins Aerospace),     value: 64.9,   unit: $M, rank: 17, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Johnson Controls Navy Systems LLC,          value: 58.7,   unit: $M, rank: 18, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Globe Composite Solutions LLC,              value: 57.3,   unit: $M, rank: 19, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: CIRCOR International Inc.,                   value: 53.0,   unit: $M, rank: 20, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: L3Harris Technologies Inc.,                 value: 52.3,   unit: $M, rank: 21, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: BWX Technologies Inc.,                      value: 51.8,   unit: $M, rank: 22, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Advance Mfg. Co. Inc.,                      value: 51.2,   unit: $M, rank: 23, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Pegasus Steel LLC,                          value: 48.9,   unit: $M, rank: 24, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Portland Valve LLC,                         value: 48.1,   unit: $M, rank: 25, tie_out: Entity Master / Vendors (wiki 09), used_in: top25_ledger_1}
    - {input: Classified subaward recipients,             value: 150,    unit: count, tie_out: Entity Master, used_in: chip_1}
    - {input: Supplier-addressable visible value,         value: 5.46,   unit: $B,    tie_out: SAM Build section 3, used_in: chip_2}
    - {input: Broader FFATA-visible unique parents,       value: 759,    unit: count, tie_out: FFATA-visible subawards (wiki 08), used_in: note_1}
  calculations: []
  rounding_rules: Supplier values shown in $M to one decimal as published; visible value rounded to ~$5.46B; counts as published (~150, ~759).
  reconciliation: The 25 named rows are a subset of the ~150 classified recipients and the ~$5.46B supplier-addressable visible value; the named list is not expected to sum to the visible total. Top-10 values tie exactly to the S15 visible_suppliers chart.

qa:
  guardrails:
    - Ranks 1-25 are fully resolved; no WORKBOOK_REQUIRED placeholders remain.
    - Top-10 values match the S15 chart exactly; Northrop Grumman is rank 1 by a wide margin.
    - Top-5 rows use light BLUE_1 emphasis only; never the dark counted-SAM blues. The rest are no-fill rule rows.
    - The slide states FFATA-visible is a floor, not the full supplier layer (~759 parents in total).
    - The ledger is not framed as a capture target list and the rows are not summed into a market size.
    - Foreign rows (Leonardo rank 2, Rosyth rank 11) are foreign by incorporation, not work location.
    - Display names are Title Case parent names, not all-caps SAM legal names; no logos.
  source_checks:
    - Sources are the exact real citations in chrome.sources (SAM.gov FFATA/FSRS, SAM.gov Entity Management API, FAR 52.204-10); no internal docs, workbook tabs, wiki chapters, or CD_ IDs.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - "if a table exists: resolved column widths sum to its region width"
    # no chart on this slide -> chart rId / chart-fit checks do not apply
