# SlideSpec - submarines `demand_backdrop` (deck slide 5)
# Horizontal-timeline body slide: a single time-axis connector carrying five real
# tick glyphs, with five dated milestone cards hung beneath it, then three NO-FILL
# theme rails (supplier-base constraint, policy investment, prime behavior) that
# group the events, closed by a no-fill interpretation note. The theme rails are
# thin-rule / no-fill rails (not filled cards) so the page reads as a timeline plus
# grouping rails, not a multi-card grid. Shape-built only: no chart, table, photo,
# seal, or logo. Every figure here is DIRECTIONAL demand-backdrop context, not a
# FY2022-FY2027 sizing input.

meta:
  slide_id: subs-s5
  slide_order: 5
  module_name: demand_backdrop.py
  slide_type: body
  section: TAM Build
  archetype: horizontal_timeline_plus_evidence_themes
  story_role: Ground the supplier opportunity in oversight, Navy policy, and prime-contractor behavior before the model defends individual inputs, so the TAM build reads as a response to a documented structural shift, not spreadsheet arithmetic.
  inputs:
    - Demand-backdrop timeline (deck spec slide 5)
    - Wiki 06 Outsourced layer within Basic Construction
    - Wiki 10 Maritime Industrial Base layer
    - Wiki 13 Executive commentary
    - Wiki 14 Navy and OSD industrial-base policy
    - Wiki 15 Prime financials
  related_appendix: []

chrome:
  section: TAM Build
  breadcrumb_topic: Demand backdrop
  title_topic: Demand Backdrop
  title_finding: Policy and prime behavior point toward distributed supplier capacity
  layout: slideLayout4          # -> module-level LAYOUT
  sources:
    - U.S. GAO, GAO-21-257, GAO-24-107732, GAO-25-106286, and GAO-26-109068
    - CRS RL32418 and U.S. Navy FY2027 30-Year Shipbuilding Plan
    - HII and General Dynamics SEC 10-K filings and earnings calls
  source_line_exact: "Sources: (1) U.S. GAO, GAO-21-257, GAO-24-107732, GAO-25-106286, and GAO-26-109068; (2) CRS RL32418 and U.S. Navy FY2027 30-Year Shipbuilding Plan; (3) HII and General Dynamics SEC 10-K filings and earnings calls"

story:
  objective: "Establish that the market opportunity has an operational backdrop: government oversight, Navy policy, and prime behavior all point toward a broader distributed supplier base, so the modeled supplier TAM is grounded in a documented direction of travel."
  do_not_say:
    - Do not imply the Navy 10 percent to 50 percent distributed-sites target is submarine-specific; it is Navy-wide policy context.
    - Do not imply every supplier-capacity dollar is immediately addressable to new entrants.
    - Do not overload the timeline cards with direct quotes; paraphrase on slide.
    - Avoid photos, seals, logos, or external images.
  known_caveats:
    - The 1.3 per year current delivery rate is from trade-press commentary, not from CRS or the Navy plan directly; the 2.0-then-2.33 per year requirement is from CRS RL32418.
    - The 10 percent to 50 percent distributed-shipbuilding target is Navy-wide; the Navy has not published a submarine-specific figure beneath it.
    - SIB terminology is used in visible copy; older source files use MIB, reconciled only in the explicit policy-rail note.
    - Prime commentary and policy confirm direction of travel but do not change the FY2022-FY2027 sizing math.

regions:
  coord_basis: BODY
  layout_pattern: horizontal_timeline_plus_evidence_themes
  # Top band: a shared horizontal time axis with five dated milestone cards hung
  # beneath it. Lower band: three theme rails grouping the events, then a pinned
  # interpretation note.
  timeline_axis:     {x: 0%, y: 6%,  w: 100%, h: 10%}
  event_2021:        {x: 0%,  y: 18%, w: 17%, h: 23%}
  event_2024_2025:   {x: 19%, y: 18%, w: 20%, h: 23%}
  event_jan_2026:    {x: 41%, y: 18%, w: 18%, h: 23%}
  event_jan_apr_2026: {x: 61%, y: 18%, w: 18%, h: 23%}
  event_apr_may_2026: {x: 81%, y: 18%, w: 19%, h: 23%}
  constraint_theme:  {x: 0%, y: 51%, w: 31%, h: 34%}
  policy_theme:      {x: right_of(constraint_theme) + GAP, y: align_top(constraint_theme), w: 31%, h: 34%}
  prime_theme:       {x: right_of(policy_theme) + GAP, y: align_top(constraint_theme), w: remaining, h: 34%}
  note_strip:        {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:
  - {id: e1,  type: connector, region: timeline_axis,      prominence: tertiary,  paint_order: 1,  content: horizontal time-axis connector line (no ticks; ticks are e11)}
  - {id: e2,  type: diagram,   region: event_2021,         prominence: secondary, paint_order: 3,  content: Jan 2021 GAO supplier-base atrophy milestone}
  - {id: e3,  type: diagram,   region: event_2024_2025,    prominence: secondary, paint_order: 4,  content: 2024-2025 SIB institutionalization and yard-space outsourcing milestone}
  - {id: e4,  type: diagram,   region: event_jan_2026,     prominence: secondary, paint_order: 5,  content: Jan 2026 CRS structure and AUKUS demand milestone}
  - {id: e5,  type: diagram,   region: event_jan_apr_2026, prominence: secondary, paint_order: 6,  content: Jan-Apr 2026 General Dynamics supply-chain gating milestone}
  - {id: e6,  type: diagram,   region: event_apr_may_2026, prominence: secondary, paint_order: 7,  content: Apr-May 2026 GAO and Navy plus HII distributed-shipbuilding milestone}
  - {id: e7,  type: rail,      region: constraint_theme,   prominence: secondary, paint_order: 8,  content: supplier-base constraint no-fill theme rail}
  - {id: e8,  type: rail,      region: policy_theme,       prominence: secondary, paint_order: 9,  content: policy investment no-fill theme rail}
  - {id: e9,  type: rail,      region: prime_theme,        prominence: secondary, paint_order: 10, content: prime behavior no-fill theme rail}
  - {id: e10, type: note,      region: note_strip,         prominence: tertiary,  paint_order: 11, content: interpretation note guarding against over-claiming addressability}
  - {id: e11, type: glyph_set, region: timeline_axis,      prominence: tertiary,  paint_order: 2,  content: five tick glyphs marking the five milestone dates on the axis}


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
      connector_text: none
    e11:
      text_runs:
      - role: tick date label
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
    e2:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e3:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e4:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e5:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e6:
      text_runs:
      - role: map/flow title
        size: LABEL_9PT
        color: DK
        font: FONT
        bold: true
      - role: map/flow body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
    e7:
      text_runs:
      - role: theme rail cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: theme rail bullets
        size: LABEL_9PT
        color: DK
        font: FONT
    e8:
      text_runs:
      - role: theme rail cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: theme rail bullets
        size: LABEL_9PT
        color: DK
        font: FONT
    e9:
      text_runs:
      - role: theme rail cap
        size: CAP_12PT
        color: DK
        font: FONT
        bold: true
      - role: theme rail bullets
        size: LABEL_9PT
        color: DK
        font: FONT
    e10:
      text_runs:
      - role: note/body
        size: FINEPRINT_8_5PT
        color: DK
        font: FONT
        italic: true
  note: Event cards are dense; use LABEL_9PT bold date/source lead plus FINEPRINT_8_5PT body if DENSE_BODY_10PT overflows.
  render_notes: []

charts: []
tables: []
images: []

shapes:
  - id: timeline_axis_1
    element: e1
    factory: connector
    fill: null
    line_color: GRAY_4        # connector(): color=GRAY_4, width 12700 (1pt), arrow=False
    insets: INSETS_NONE
    meaning: Shared horizontal time-axis line only; builder draws a 1pt GRAY_4 connector. No-fill connector (line_color GRAY_4, no fill). The five tick glyphs and their date labels are the separate tick_marks object (e11).
  - id: tick_marks
    element: e11
    factory: glyph_set
    fill: null
    line_color: null
    insets: INSETS_NONE
    children:
      - {tick: t1, x_on_axis: 8%,  label: "2021",         glyph: vertical_tick}
      - {tick: t2, x_on_axis: 29%, label: "2024-2025",    glyph: vertical_tick}
      - {tick: t3, x_on_axis: 50%, label: "Jan 2026",     glyph: vertical_tick}
      - {tick: t4, x_on_axis: 70%, label: "Jan-Apr 2026", glyph: vertical_tick}
      - {tick: t5, x_on_axis: 90%, label: "Apr-May 2026", glyph: vertical_tick}
    meaning: Five real tick glyphs sitting on the axis line, one per milestone, each a short GRAY_4 vertical tick mark with its date labeled above (LABEL_9PT). No-fill glyph set (no fill, no border); the ticks themselves are the marks. Enumerates exactly five tick glyphs.
  - id: event_2021_card
    element: e2
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Jan 2021\nGAO-21-257: Columbia relies on a supplier base roughly 70% smaller than prior shipbuilding booms; outsourcing raises supplier-quality oversight need."   # DENSE_BODY_10PT
    meaning: Oversight baseline for the supplier-base constraint.
  - id: event_2024_2025_card
    element: e3
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "2024-2025\nSIB program office stood up (Sep 2024); GAO-25-106286 documents two shipbuilders already outsourcing yard work due to constrained physical space."   # DENSE_BODY_10PT
    meaning: Policy and operating context for moving work beyond legacy yard space.
  - id: event_crs_card
    element: e4
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Jan 2026\nCRS RL32418: about 16,000 suppliers in all 50 states; about 70% of critical suppliers sole-source; AUKUS lifts the rate requirement toward 2.33 Virginia per year."   # DENSE_BODY_10PT
    meaning: Industrial-base structure and AUKUS demand pressure.
  - id: event_gd_card
    element: e5
    factory: text_box
    fill: GRAY_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Jan-Apr 2026\nGeneral Dynamics: supply chain remains the gating item; complex, sole-source components are the bottleneck; capex up 79% YoY to over $900M, half at Electric Boat."   # DENSE_BODY_10PT
    meaning: Prime confirmation that bottlenecks are supplier-side, with own-yard capital response.
  - id: event_gao_hii_card
    element: e6
    factory: text_box
    fill: BLUE_1
    line_color: GRAY_3
    insets: INSETS_CARD
    text: "Apr-May 2026\nGAO-26-109068: more than $10B already invested in the submarine industrial base; Navy FY2027 plan targets distributed shipbuilding; HII guides to plus 30% YoY outsourcing hours."   # DENSE_BODY_10PT
    meaning: Recent policy and prime evidence confirming the distributed-capacity direction.
  - id: constraint_theme_rail
    element: e7
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_CARD
    paragraphs:
      - runs:
          - {text: "CONSTRAINT SIGNAL", size: CAP_12PT, bold: true, color: DK, font: FONT}
      - runs:
          - {text: "Supplier base about 70% smaller than prior booms", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "About 70% of critical suppliers sole-source", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "AUKUS adds demand toward 2.33 Virginia per year", size: LABEL_9PT, color: DK, font: FONT}
    text: "CONSTRAINT SIGNAL\nSupplier base about 70% smaller than prior booms\nAbout 70% of critical suppliers sole-source\nAUKUS adds demand toward 2.33 Virginia per year"
    meaning: No-fill theme rail (no fill, no border, intentionally borderless) grouping the timeline into the supplier-base constraint documented by GAO and CRS; keeps the bold CAP lead-in plus bullet paragraphs but reads as a rule-grouped rail, not a filled card.
  - id: policy_theme_rail
    element: e8
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_CARD
    paragraphs:
      - runs:
          - {text: "POLICY SIGNAL", size: CAP_12PT, bold: true, color: DK, font: FONT}
      - runs:
          - {text: "More than $10B DoD submarine industrial-base investment", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "SIB program office institutionalizes oversight (MIB in source docs)", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "Navy distributed-shipbuilding policy context", size: LABEL_9PT, color: DK, font: FONT}
    text: "POLICY SIGNAL\nMore than $10B DoD submarine industrial-base investment\nSIB program office institutionalizes oversight (MIB in source docs)\nNavy distributed-shipbuilding policy context"
    meaning: No-fill theme rail (no fill, no border, intentionally borderless) grouping the timeline into the formalized policy response; carries the only explicit SIB/MIB reconciliation note on the slide; keeps the bold CAP lead-in plus bullet paragraphs as a rule-grouped rail, not a filled card.
  - id: prime_theme_rail
    element: e9
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_CARD
    paragraphs:
      - runs:
          - {text: "PRIME BEHAVIOR SIGNAL", size: CAP_12PT, bold: true, color: DK, font: FONT}
      - runs:
          - {text: "HII guides to plus 30% YoY outsourcing hours", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "GD: supply chain is the gating item", size: LABEL_9PT, color: DK, font: FONT}
      - runs:
          - {text: "Electric Boat capex and throughput focus", size: LABEL_9PT, color: DK, font: FONT}
    text: "PRIME BEHAVIOR SIGNAL\nHII guides to plus 30% YoY outsourcing hours\nGD: supply chain is the gating item\nElectric Boat capex and throughput focus"
    meaning: No-fill theme rail (no fill, no border, intentionally borderless) grouping the timeline into operating confirmation from the two primes; keeps the bold CAP lead-in plus bullet paragraphs as a rule-grouped rail, not a filled card.
  - id: note_strip_1
    element: e10
    factory: text_box
    fill: null
    line_color: null
    insets: INSETS_NONE
    text: "Read: the direction of travel is visible in oversight, Navy policy, and prime behavior; it is not a claim that every dollar is immediately addressable, and these signals do not change the FY2022-FY2027 sizing math."   # FINEPRINT_8_5PT italic
    meaning: Keeps the slide from over-claiming addressability and separates directional context from the sizing model.

commentary:
  visible:
    element: e10
    container: method_note
    title:
    bullets:
      - {lead: "Read:", body: "oversight, Navy policy, and prime behavior all point toward broader distributed supplier capacity."}
    body_size: LABEL_9PT
  reserve:
    purpose: Approved extra material for denser future versions of this slide.
    context: |
      WHERE THIS SLIDE SITS. This is the opening slide of the TAM Build section. It
      bridges the market map (Market and Scope) to the model: the modeled supplier
      opportunity only matters if there is an operational reason for more submarine
      work to move to the supplier base. The documents provide that reason from three
      independent directions - government oversight, Navy and OSD policy, and prime-
      contractor behavior - and the slide's job is to show those three signals moving
      the same way without converting any of them into a sizing input.

      THE OVERSIGHT BASELINE (GAO). GAO-21-257 (Jan 2021) found the Columbia program
      relies on a supplier base "roughly 70 percent smaller than in previous
      shipbuilding booms," and warned that quality-assurance oversight at supplier
      facilities becomes critical as shipbuilders expand outsourcing. GAO-24-107732
      (Sep 2024) found SUPSHIP Groton and Newport News "not well positioned to conduct
      quality-assurance oversight for the significant amount of Columbia work being
      outsourced" - a direct statement that work is being outsourced. GAO-25-106286
      (Feb 2025) is the most direct operational statement: "Two of the shipbuilders we
      spoke with are already outsourcing work that would normally be done at their
      shipyards to their suppliers to overcome constrained physical space, with plans
      to expand the volume of material they are outsourcing." The two shipbuilders are
      GDEB and HII.

      THE STRUCTURE (CRS). CRS RL32418 (Jan 26, 2026) supplies the structure: beyond
      GD/EB and HII/NNS, "the submarine construction industrial base includes about
      16,000 suppliers in all 50 states," and "about 70 percent of the critical
      suppliers for the construction of submarines are sole-source suppliers." The same
      report frames AUKUS Pillar 1 demand: the Virginia-class rate must rise to 2.0 per
      year and "subsequently to 2.33 boats per year" to cover the two-per-year U.S.
      requirement plus replacement of the three to five Virginia hulls to be sold to
      Australia. Trade-press commentary (Breaking Defense op-ed, Apr 2024) notes that
      against the two-per-year target the program is "currently only on pace to deliver
      1.3" - this 1.3 figure is commentary, not a CRS or Navy figure, and is tagged as
      such.

      THE POLICY RESPONSE (Navy / OSD). The Navy established a Maritime Industrial Base
      (MIB) Program Office by June 2024 memorandum, operating from September 2024; in
      visible copy this is rendered as the SIB program office, with the MIB term
      reconciled only in the policy rail. GAO-26-109068 (Apr 22, 2026) documents that
      "DOD does not know how much funding it expects to need - beyond the more than $10
      billion DOD already invested - to solve submarine industrial base challenges." The
      Navy's FY2027 30-Year Shipbuilding Plan (the "Golden Fleet" plan, Apr-May 2026)
      states: "Currently only 10% of shipbuilding occurs at distributed sites. The Navy
      aims to increase this to 50%." This 10-to-50 target is Navy-wide, not submarine-
      specific, and must be treated as policy context. The plan also allocates about
      $6.2B specifically to the submarine industrial base.

      THE PRIME CONFIRMATION (HII and GD). HII's May 5, 2026 FY26 Q1 guidance: "We are
      on track to grow our outsourcing hours year-over-year by 30%." This 30 percent is
      the single most authoritative dated quantitative statement on HII's outsourcing
      magnitude; it is a growth rate, not an absolute share (HII does not disclose the
      base). Kastner also adopted "distributed shipbuilding strategy" as HII's corporate
      term and stated "I really don't want to vertically integrate" - an unusual posture
      that means HII responds to capacity constraint by expanding the supplier base
      rather than acquiring it. (Note: an analyst referenced "35%" in May 2025; official
      guidance settled at 30 percent, so the slide uses 30 percent.) General Dynamics
      took the complementary path: Novakovic (Jan 28, 2026) called the supply chain "the
      gating item" with "sole source suppliers where they are bottlenecks," and guided
      capex up 79 percent YoY to over $900M with "half at least... at Electric Boat"
      (about $450-500M). Danny Deep (Apr 29, 2026) reported Electric Boat Columbia hours
      earned up 29 percent and sequence-critical material receipts up 52 percent YoY.

      WHY THIS IS NOT A SIZING INPUT. The intended takeaway is not that every dollar
      becomes addressable to new entrants immediately. It is that the direction of
      travel is not speculative: it is visible in government oversight, budget policy,
      and public company commentary. None of these figures - the >$10B, the 10-to-50
      target, the +30% outsourcing hours, the 2.33-per-year requirement - enters the
      FY2022-FY2027 TAM math, which is built bottom-up from the SCN Basic Construction
      base and the strict 35.0 percent supplier coefficient.

      DENSITY GUIDANCE. Default is the five-card timeline plus three theme rails plus
      the interpretation note. To densify, add a fourth line to a theme rail or expand
      the note strip; keep direct quotes off the slide (paraphrase only) and keep the
      three rails so the page does not collapse into a disconnected list of events.
    density_modes:
      normal: {visible_bullets: 1, keep: [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]}
      dense: {add_bullets: 3, safe_containers: [constraint_theme, policy_theme, prime_theme, note_strip], allowed_font_step_down: ["DENSE_BODY_10PT -> LABEL_9PT", "LABEL_9PT -> FINEPRINT_8_5PT"]}
    approved_extra_points:
      - priority: 1
        lead: "Constraint is supplier-side:"
        body: "The binding problem is no longer only yard throughput; supplier capacity and supplier qualification are the documented constraints."
        evidence: GAO-21-257; GAO-25-106286; CRS RL32418 (wiki 06)
        safe_container: constraint_theme
        density_trigger: Add if the constraint theme needs a stronger lead-in line.
      - priority: 2
        lead: "Sole-source concentration:"
        body: "About 70% of critical submarine suppliers are sole-source, making qualification and capacity expansion the central levers."
        evidence: CRS RL32418 (wiki 06)
        safe_container: constraint_theme
        density_trigger: Add if one statistic needs to stand out.
      - priority: 3
        lead: "AUKUS demand pressure:"
        body: "AUKUS lifts the Virginia-class requirement toward 2.33 boats per year, structurally larger than the U.S. Navy requirement alone."
        evidence: CRS RL32418 (wiki 14)
        safe_container: constraint_theme
        density_trigger: Add if international demand is discussed.
      - priority: 4
        lead: "Policy response:"
        body: "More than $10B of DoD submarine industrial-base investment and distributed-shipbuilding language formalize the response to supplier-base limits."
        evidence: GAO-26-109068; U.S. Navy FY2027 30-Year Shipbuilding Plan (wiki 14)
        safe_container: policy_theme
        density_trigger: Add for a policy-heavy audience.
      - priority: 5
        lead: "Investment is context, not TAM:"
        body: "The more than $10B industrial-base investment supports the policy signal but is not itself counted as component TAM in the model."
        evidence: GAO-26-109068; wiki 10
        safe_container: policy_theme
        density_trigger: Add when connecting back to the sizing-boundary slide.
      - priority: 6
        lead: "Physical-space mechanism:"
        body: "GAO documents shipbuilders outsourcing work normally done at yards because constrained physical space forces distributed work."
        evidence: GAO-25-106286 (wiki 06)
        safe_container: policy_theme
        density_trigger: Add if the outsourcing mechanism is unclear.
      - priority: 7
        lead: "HII prime confirmation:"
        body: "HII guides to plus 30% YoY outsourcing hours and prefers arms-length partners over vertical integration, expanding the supplier base by design."
        evidence: HII FY26 Q1 earnings call, May 5, 2026 (wiki 13)
        safe_container: prime_theme
        density_trigger: Add if the audience wants company evidence.
      - priority: 8
        lead: "GD prime confirmation:"
        body: "General Dynamics calls the supply chain the gating item and is raising capex 79% YoY to over $900M, about half at Electric Boat."
        evidence: GD FY25 Q4 and FY26 Q1 earnings calls; GD SEC 10-K (wiki 13, wiki 15)
        safe_container: prime_theme
        density_trigger: Add when contrasting the two primes' strategies.
      - priority: 9
        lead: "Margin signal in the financials:"
        body: "Both primes show about 200 basis points of segment-margin compression in FY2023-FY2024, consistent with the acknowledged outsourcing cost premium."
        evidence: HII and GD SEC 10-K filings (wiki 15)
        safe_container: note_strip
        density_trigger: Add for an investor audience focused on prime economics.
      - priority: 10
        lead: "Navy-wide caution:"
        body: "Treat the 10 percent to 50 percent distributed-sites target as Navy-wide policy context unless a source explicitly ties a target to submarine construction."
        evidence: U.S. Navy FY2027 30-Year Shipbuilding Plan (wiki 14)
        safe_container: note_strip
        density_trigger: Add if the slide risks over-claiming the 10-to-50 target as submarine-specific.
      - priority: 11
        lead: "Delivery-rate caveat:"
        body: "The 1.3 per year current delivery figure is trade-press commentary, not a CRS or Navy figure; the 2.0-then-2.33 requirement is the CRS-sourced number."
        evidence: CRS RL32418; Breaking Defense op-ed (wiki 14)
        safe_container: note_strip
        density_trigger: Add if a reviewer questions the delivery-rate gap.
      - priority: 12
        lead: "Three independent axes:"
        body: "Oversight, policy, and prime behavior are independent signals; their concurrence, not their sum, is what makes the direction of travel credible."
        evidence: GAO; U.S. Navy FY2027 plan; HII and GD earnings calls (wiki 14)
        safe_container: note_strip
        density_trigger: Add when summarizing why the backdrop matters.
    do_not_add:
      - logos, seals, photography, or external imagery
      - a claim that the 10 percent to 50 percent distributed-sites target is submarine-specific unless backed by a specific source
      - any numerical change to TAM based on demand-backdrop signals
      - direct multi-sentence executive quotes on the slide face (keep paraphrase; quotes belong in speaker notes or appendix)

qa:
  guardrails:
    - Slide shows all three support types: oversight (GAO), policy (Navy/OSD), and prime behavior (HII/GD).
    - Navy-wide distributed-shipbuilding targets are treated as policy context, not submarine-specific proof.
    - Visible wording uses SIB; MIB appears only in the explicit SIB/MIB reconciliation note in the policy rail.
    - The 1.3 per year delivery figure is flagged as commentary; 2.0-then-2.33 per year is CRS-sourced.
    - Timeline cards stay short and paraphrased; no direct quotes on the slide face.
    - No "+" or "/" in visible copy except canonical percentages; "plus 30%" is spelled out.
  source_checks:
    - Sources are real external citations only: GAO reports, CRS RL32418, U.S. Navy FY2027 plan, and HII/GD SEC filings and earnings calls.
    - No workbook tabs, wiki chapters, slide-data IDs, or chart IDs appear in chrome.sources.
    - The Navy FY2027 plan is in the footer because distributed-capacity language appears on the slide.
  engine_checks:
    - all body objects within BODY
    - title <= 2 lines
    - no chart rIds because charts is empty
    - no table-fit check because tables is empty
