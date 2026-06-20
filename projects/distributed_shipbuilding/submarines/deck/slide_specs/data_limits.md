# SlideSpec - submarines `data_limits` (deck slide 17)
# Shape-built visibility ledger: a left "visible and measured" panel vs a right
# "unseen or under-observed" panel, a four-chip model-guardrail strip, and a
# one-line interpretation note. The slide's job is credibility before
# implications - it makes the FFATA visibility boundary explicit rather than
# burying it in footnotes.

meta:
  slide_id: subs-s17
  slide_order: 17
  module_name: data_limits.py
  slide_type: body
  section: Interpretation
  archetype: visibility_ledger_with_guardrail_strip
  story_role: Increase credibility before implications by distinguishing the FFATA-visible named-vendor floor (~$1.0-1.5B/yr) from the larger under-observed outsourced layer (~$5-7B/yr implied).
  inputs:
    - POP Source Audit (confirmation coverage, unparsed share)
    - SAM Build residual checks (unbucketed residual discipline)
    - QA Reconciliation (guardrail anchors)
    - Source Index / References
    - Unseen layer (wiki 12); Data sources and limitations (wiki 16); HII Newport News gap (wiki 11)
  related_appendix: []

chrome:
  section: Market sizing
  breadcrumb_topic: Data limits
  title_topic: Data Limits
  title_finding: FFATA captures a visible floor, not the full supplier layer
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - FAR 52.204-10
    - SAM.gov FFATA and FSRS records
    - General Dynamics and HII Form 10-K filings
  source_line_exact: "Sources: (1) FAR 52.204-10; (2) SAM.gov FFATA and FSRS records; (3) General Dynamics and HII Form 10-K filings"

story:
  objective: Make the data limitations explicit and credible before closing with market-priority implications - what is measured, what is under-observed, and how the model guards against overstatement.
  do_not_say:
    - Do not treat FFATA-visible records as the full supplier layer.
    - Do not imply unobserved means nonexistent or non-addressable.
    - Do not introduce SOM, capture probability, qualification haircut, or pricing realization.
    - Do not present the slide as a wall of caveats; it is a balanced ledger.
  known_caveats:
    - FFATA-visible suppliers are used for named-vendor and work-type evidence, not as a complete supplier-spend total.
    - Reporting lag is especially relevant in FY2025 and FY2026 records; recent visible flow is biased downward.
    - The visible-vs-unseen split is directional; the unseen-layer dollar magnitudes are not separately measurable from public data.

regions:
  coord_basis: BODY
  layout_pattern: visibility_ledger_with_guardrail_strip
  # Two ledger panels side by side across the upper BODY, a centered one-line
  # interpretation note beneath them, then a full-width four-chip guardrail strip
  # pinned near the bottom of BODY.
  visible_panel: {x: 0%, y: 0%, w: 49%, h: 62%}
  unseen_panel:  {x: right_of(visible_panel) + GAP, y: align_top(visible_panel), w: remaining, h: 62%}
  interp_note:   {x: 0%, y: 66%, w: 100%, h: fit_content}
  guardrail:     {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1, type: diagram,  region: visible_panel, prominence: primary,   paint_order: 1, content: visible and measured public-data layer (left ledger panel)}
  - {id: e2, type: diagram,  region: unseen_panel,  prominence: primary,   paint_order: 2, content: unseen or under-observed supplier layer (right ledger panel)}
  - {id: e3, type: note,     region: interp_note,   prominence: secondary, paint_order: 3, content: one-line visible-floor interpretation note}
  - {id: e4, type: chip_row, region: guardrail,     prominence: secondary, paint_order: 4, content: four model-guardrail chips (SOM, double-count check, dollar basis, supplier visibility)}


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
      - role: card cap/header
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
        note: Use ALL CAPS only where the visible text already uses it.
      - role: card body/bullets
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e2:
      text_runs:
      - role: card cap/header
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
        note: Use ALL CAPS only where the visible text already uses it.
      - role: card body/bullets
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: visible-floor lead
        size: MESSAGE_11PT
        color: DK
        font: FONT
        bold: true
      - role: visible-floor body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: chip label
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        bold: true
      - role: chip body
        size: DENSE_BODY_10PT
        color: DK
        font: FONT
        bold: true
  render_notes: []

charts: []                # NONE on this slide -> no rId / chart-fit checks apply
tables: []                # NONE on this slide -> no table-fit / col-width checks apply

shapes:
  - id: visible_1
    element: e1
    factory: text_box
    fill: BLUE_1               # counted-data styling: same family as the measured TAM layer
    line_color: GRAY_3        # primary ledger panel: hairline border
    insets: INSETS_CARD
    text: |
      VISIBLE AND MEASURED LAYER
      FFATA-visible first-tier subawards
      Named vendors and parent entities
      SAM.gov Entity NAICS enrichment
      DoD Contracts POP evidence
      SCN P-5c and P-10 budget exhibits
    meaning: Left side of the ledger; data used directly or as triangulation evidence. Header CAP_12PT bold; bullets DENSE_BODY_10PT.
  - id: unseen_1
    element: e2
    factory: text_box
    fill: GRAY_1              # under-observed styling: gray, not the counted blues
    line_color: GRAY_3       # primary ledger panel: hairline border
    insets: INSETS_CARD
    text: |
      UNSEEN OR UNDER-OBSERVED LAYER
      Purchased material booked as direct material
      Lower-tier subcontracts
      HII Newport News visibility gap
      Standing supplier agreements
      Reporting lag
      Unparsed single-site POP rows
    meaning: Right side of the ledger; public-data blind spots. Header CAP_12PT bold; bullets DENSE_BODY_10PT.
  - id: note_1
    element: e3
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Visible data is strong enough to classify and triangulate, not complete enough to equal the whole supplier layer."   # lead-in MESSAGE_11PT bold, remainder DENSE_BODY_10PT, centered
    meaning: One-line interpretation note bridging the two panels; the slide's plain-language takeaway.
  - id: guardrail_chips
    element: e4
    factory: chip_row
    layout: even_row          # four equal compact chips spanning the guardrail strip, left to right
    insets: INSETS_MICRO_CAP
    chips:
      - id: chip_som
        fill: GRAY_2
        line_color: GRAY_3    # secondary chip: hairline border
        label: "MODEL GUARDRAIL"
        body: "No SOM or capture modeled"
      - id: chip_doublecount
        fill: GRAY_2
        line_color: GRAY_3    # secondary chip: hairline border
        label: "DOUBLE-COUNT CHECK"
        body: "AP and LLTM additive base = $0"
      - id: chip_dollarbasis
        fill: GRAY_2
        line_color: GRAY_3    # secondary chip: hairline border
        label: "DOLLAR BASIS"
        body: "Nominal then-year dollars"
      - id: chip_visibility
        fill: BLUE_1          # FFATA-floor chip ties to the visible (counted-data) layer
        line_color: GRAY_3    # secondary chip: hairline border
        label: "SUPPLIER VISIBILITY"
        body: "FFATA-visible = named floor"
    meaning: Quick-scan model guardrails rendered as four labeled chips (MODEL GUARDRAIL / DOUBLE-COUNT CHECK / DOLLAR BASIS / SUPPLIER VISIBILITY). Chip labels FINEPRINT_8_5PT bold; chip bodies DENSE_BODY_10PT bold. The supplier-visibility chip uses BLUE_1 to tie to the visible layer; the other three use GRAY_2.

commentary:
  visible:
    element: e4
    container: method_note     # the guardrail strip is the visible method commentary
    title:
    bullets:
      - {lead: "Guardrail:", body: "FFATA is a named first-tier floor; the model uses strict coefficients and an explicit residual rather than treating visible subawards as total spend."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. It is the credibility slide right before implications.
      The deck relies on public records, but public records do not show the full
      submarine supplier base cleanly. This slide raises trust by making the data
      boundary visible rather than burying it in notes, and by showing the model's
      guardrails against overstatement.

      THE CORE LIMITATION (verified, wiki 12 + wiki 16). The FFATA-visible first-tier
      subaward stream captures roughly $1.0 to $1.5 billion per fiscal year of
      named-vendor subaward flow against the in-scope new-construction PIIDs at recent
      rates. The cost-funnel framework sizes the actual outsourced layer within Basic
      Construction at roughly $5 to $7 billion per fiscal year. The cleanest single
      statement: FFATA-visible first-tier filings capture approximately 10 to 20
      percent of the actual outsourced layer; the remaining 80 to 90 percent is unseen
      at the named-vendor first-tier level. (The FY2025 FFATA figure is ~$758M,
      reporting-lag-depressed; it will revise upward.)

      VISIBLE AND MEASURED LAYER (left panel). FFATA-visible first-tier subawards above
      the $30,000 reporting threshold; named vendors and parent-normalized entities;
      SAM.gov Entity Management NAICS-informed work-type mapping; DoD daily Contracts
      place-of-performance percentages for high-dollar actions; and SCN P-5c and P-10
      budget exhibits for base and timing evidence. This layer is strong enough to
      classify suppliers and triangulate a coefficient, not complete enough to equal
      total supplier spend.

      UNSEEN OR UNDER-OBSERVED LAYER (right panel). The gap between the ~$1-1.5B visible
      and the ~$5-7B implied outsourced layer falls into categories from wiki 12:
      (a) purchased material booked as direct material cost (structurally the largest,
      ~$3-4B/yr by industry-typical decomposition) - FAR 52.204-10 reaches subcontracts
      but not material purchases; (b) lower-tier subcontracts beneath the first tier
      (~20-40% of outsourced material flow), not reportable to FSRS; (c) the HII Newport
      News team-build share (~$1.5-2.0B/yr) that flows through GDEB's prime contracts
      but appears FFATA-visible at essentially zero (wiki 11); (d) long-term standing
      supplier agreements that pre-date the prime contract and are FAR-excluded;
      (e) reporting lag (6-18 months; depresses FY2025-FY2026); and (f) unparsed
      single-site POP rows where place-of-performance percentages are not explicit.
      Categorically excluded by the article's scope (not "missing," excluded by design):
      classified payload modules, Trident SWS, and federal naval shipyard depot work.

      MODEL RESPONSE. The deck does NOT treat FFATA as the full outsourced layer. FFATA
      is used for named-vendor evidence and work-type allocation. The TAM coefficient is
      triangulated with DoD Contracts POP evidence and external policy and oversight
      context. The strict applied ~35% supplier coefficient (BPMI naval-nuclear excluded;
      the BPMI-included sensitivity coefficient is ~75.7% and is NOT applied) and the
      explicit unbucketed residual are intentional safeguards against overstating
      precision. POP confirmation coverage is high (target ~90%+ of in-scope dollars).

      WHAT THE DECK DOES NOT DO. No SOM, capture share, win probability, qualification
      haircut, pricing realization, or inflation normalization. The AP and LLTM additive
      base is $0 (it overlaps Basic Construction and is not additive to TAM). Dollar
      figures are nominal then-year dollars.

      DENSITY GUIDANCE. Default is two ledger panels + interpretation note + four-chip
      guardrail strip. To densify, add sub-bullets inside either panel or expand the
      interpretation note to two lines. Keep the visible panel in the counted-data blue
      family and the unseen panel in gray at any density; never let it read as a caveat
      wall.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4]}
      dense:  {add_bullets: 4, safe_containers: [visible_panel, unseen_panel, interp_note, guardrail], allowed_font_step_down: ["LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Capture rate:"
        body: "FFATA-visible first-tier filings capture roughly 10 to 20 percent of the actual outsourced layer (~$1.0-1.5B/yr visible vs ~$5-7B/yr implied)."
        evidence: Unseen layer (wiki 12); Data sources and limitations (wiki 16); FAR 52.204-10
        safe_container: interp_note
        density_trigger: Add as a second interpretation line when the note can expand.
      - priority: 2
        lead: "Purchased material:"
        body: "The single largest unseen category, ~$3-4B/yr, is purchased material booked as direct material cost - FFATA reaches subcontracts, not material purchases."
        evidence: Unseen layer (wiki 12); GD and HII Form 10-K filings
        safe_container: unseen_panel
        density_trigger: Add as a sub-bullet when the unseen panel has room.
      - priority: 3
        lead: "HII team-build gap:"
        body: "HII Newport News submarine workshare (~$1.5-2.0B/yr) flows through GDEB's primes but appears FFATA-visible at essentially zero, a 100x to 10,000x gap by year."
        evidence: HII Newport News gap (wiki 11); HII and GD Form 10-K filings
        safe_container: unseen_panel
        density_trigger: Add for shipyard-savvy audiences.
      - priority: 4
        lead: "Lower tiers:"
        body: "Tier-2 and below subcontracts (~20-40% of outsourced material flow) are not reportable to FSRS and stay under-observed in first-tier records."
        evidence: Unseen layer (wiki 12); FAR 52.204-10
        safe_container: unseen_panel
        density_trigger: Add if a reader expects a complete vendor roll-up.
      - priority: 5
        lead: "Reporting lag:"
        body: "FFATA carries a 6 to 18 month filing lag; FY2025 (~$758M reported) and FY2026 are depressed and will revise upward, so recent visible flow is biased downward."
        evidence: Unseen layer (wiki 12); SAM.gov FFATA and FSRS records
        safe_container: unseen_panel
        density_trigger: Add if a reviewer asks about recent years.
      - priority: 6
        lead: "Strict coefficient:"
        body: "The applied ~35% supplier coefficient excludes BPMI naval-nuclear; the BPMI-included sensitivity coefficient is ~75.7% and is not applied - a deliberate conservatism."
        evidence: Sensitivity (coefficient ladder); QA Reconciliation
        safe_container: guardrail
        density_trigger: Use in a methodology-heavy variant.
      - priority: 7
        lead: "Residual discipline:"
        body: "An unbucketed residual is kept rather than forcing ambiguous dollars into a named bucket; it stays in TAM but out of broad component SAM."
        evidence: SAM Build residual checks
        safe_container: guardrail
        density_trigger: Add if the residual has been challenged.
      - priority: 8
        lead: "No SOM:"
        body: "No capture share, win probability, qualification haircut, or pricing realization is modeled; the deck stops at TAM and scenario SAM."
        evidence: Deck guardrails; QA Reconciliation
        safe_container: guardrail
        density_trigger: Always safe when excerpted.
      - priority: 9
        lead: "AP and LLTM base = $0:"
        body: "Advance procurement and LLTM overlap Basic Construction; the additive base is set to $0 (QA-12) so the bridge cannot double-count it into TAM."
        evidence: QA Reconciliation (QA-12); AP bridge
        safe_container: guardrail
        density_trigger: Add for an audience focused on double-counting risk.
      - priority: 10
        lead: "POP triangulation:"
        body: "DoD Contracts place-of-performance percentages support coefficient triangulation rather than replacing FFATA vendor evidence; confirmation coverage targets ~90%+ of in-scope dollars."
        evidence: POP Source Audit
        safe_container: visible_panel
        density_trigger: Use in a methodology-heavy variant.
      - priority: 11
        lead: "Categorically excluded:"
        body: "Classified payload modules, the Trident strategic weapon system, and federal naval-shipyard depot work are excluded by scope, not missing data."
        evidence: Unseen layer (wiki 12)
        safe_container: unseen_panel
        density_trigger: Add if a reviewer asks why certain large dollars are absent.
      - priority: 12
        lead: "Nominal dollars:"
        body: "Dollar figures are nominal then-year dollars; the model does not inflation-normalize except where a cross-vintage comparison explicitly notes it."
        evidence: Data sources and limitations (wiki 16)
        safe_container: guardrail
        density_trigger: Add for a finance audience asking about real-vs-nominal basis.
    do_not_add:
      - any claim that FFATA equals the whole supplier layer
      - internal workbook tab names, wiki chapters, or chart IDs in rendered fields
      - capture probability, SOM, qualification-haircut, or pricing-realization language
      - the unseen panel rendered in the counted-data blue family (keep it gray + separate)

data_and_calculations:
  data_inputs:
    - {input: FFATA-visible first-tier flow, value: "1.0-1.5", unit: $B/yr, year: recent FY, tie_out: "Unseen layer (wiki 12) ch.8; SAM.gov FFATA", used_in: visible_1}
    - {input: Implied outsourced layer in Basic Construction, value: "5-7", unit: $B/yr, year: recent FY, tie_out: "Unseen layer (wiki 12) ch.6 cost-funnel band", used_in: note_1}
    - {input: FFATA capture share of outsourced layer, value: "10-20", unit: "%", year: recent FY, tie_out: "Unseen layer (wiki 12)", used_in: note_1}
    - {input: HII Newport News implied submarine workshare, value: "1.5-2.0", unit: $B/yr, year: recent FY, tie_out: "HII Newport News gap (wiki 11); HII 10-K", used_in: unseen_1}
    - {input: FY2025 FFATA-visible flow (reporting-lag depressed), value: 758, unit: $M, year: FY2025, tie_out: "Data sources and limitations (wiki 16)", used_in: unseen_1}
    - {input: AP and LLTM additive base, value: 0, unit: $B, year: FY2022-FY2027, tie_out: "QA Reconciliation QA-12", used_in: guardrail_chips}
  rounding_rules: Ranges quoted as in source (whole $B/yr or $M); no derived rounding on this slide.
  reconciliation: This is a limitations ledger; it classifies evidence and blind spots rather than deriving a new number. The ~10-20% capture share reconciles ~$1-1.5B visible against the ~$5-7B cost-funnel-band outsourced layer.

qa:
  guardrails:
    - Slide explicitly says FFATA is a floor, not the full supplier layer.
    - HII visibility gap, purchased material, lower-tier subs, standing agreements, reporting lag, and unparsed single-site POP are all in the unseen panel.
    - No SOM and AP and LLTM additive base = $0 are shown as guardrails; the AP and LLTM base = $0 ties to QA-12.
    - Visible panel uses the counted-data blue family; unseen panel uses gray - never the reverse.
    - Capture-rate claims stay in the wiki's "approximately 10 to 20 percent" / "~$1-1.5B vs ~$5-7B" envelope; not a precise single number.
  source_checks:
    - Sources are the exact real citations in chrome.sources (FAR 52.204-10, SAM.gov FFATA and FSRS records, GD and HII Form 10-K); no internal docs, workbook tabs, wiki chapters, or chart IDs in rendered fields.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    # no charts or tables on this slide -> rId and table-fit checks do not apply
