SLIDE 01 - Vendor Archetypes (Capability Domain and Primary Output)
Type: Body (methodology)

Slide's purpose:
  Establish the two PUBLISHED classification axes that define a supplier archetype:
  Capability Domain (what technical ship area the vendor supports) and Primary Output
  (what physically leaves the vendor, on a maturity ladder). Show the grain (one label
  per UEI x Program), that each axis is MECE with a forced catch-all (D0 / P0), and how a
  label is assigned (NAICS-6 archetype-map default, then entity-level override). The third
  axis, Operating Role, is named once as an internal validation layer only - it is not
  published, which is why this slide carries two axes, not three.

TITLE
-----
Copy:
  Vendor Archetypes | Two published axes classify every supplier by ship area and delivered form.

HIGH-LEVEL LAYOUT
-----------------
Two-axis methodology slide, definitional (tables are the exhibit, not a chart).
  - Title band, then a one-line concept caption directly under it (full width).
  - Left column (~58% width): Capability Domain (D) reference table, 12 rows.
  - Right column (~42% width), stacked top-to-bottom:
      top    = Primary Output (P) rendered as an ASCENDING maturity ladder (P1 -> P5),
               with P6 and P0 set off-ladder below it;
      bottom = three assignment-method badges + one worked-example chip.
  - An italic Operating-Role caveat line sits above the source note.
The Capability Domain table is the primary object (dark header). The method badges and
ladder rungs are the only filled object family; both tables use horizontal rules only, so
heavy fills/borders never collide. Generous gutter between the two columns.

COMMENTARY COPY, IF NEEDED
--------------------------
Minimal by design - this table is definitional, not a sizing exhibit, so no interpretive
rail. The only "commentary" is the concept caption under the title; the method content
lives in the badges (see OTHER VISIBLE COPY).

Commentary 1 (concept caption under title)
  Copy:
    Archetype = one Capability Domain (ship area) and one Primary Output (delivered form),
    assigned to every UEI x Program. Each axis is MECE: exactly one label, with D0 and P0
    as forced catch-alls so coverage is complete.
  Text / shape treatment:
    No-fill, no-border caption directly beneath the title, full width. 10 pt italic, black.
    This is framing, not a finding - keep it to two lines.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Assignment-method badges (3), read left-to-right or top-to-bottom in the lower-right block:

    1. DEFAULT, THEN OVERRIDE
       The NAICS-6 archetype map sets a default (D, R, P) per industry code; an entity-level
       (Program, UEI) override replaces it when work-text evidence warrants. A Resolution flag
       marks codes the industry code alone cannot decide (Partial / Unresolved).

    2. ASSIGNMENT RULE
       Classify the most representative recurring output crossing the vendor's contractual
       boundary, not the most sophisticated item in its portfolio. Take the highest integration
       level only when the items ship as one configured system.

    3. ONE LABEL PER AXIS (MECE)
       Exactly one Capability Domain and one Primary Output per UEI x Program. D0 and P0 absorb
       the indeterminate, so every supplier is placed.

  Worked-example chip (anchors the method in one real row):
    Motor-and-generator OEM (NAICS 335312)  ->  D3 Electrical Power  x  P3 Functional Equipment

  Operating-Role caveat (italic line above the source):
    A third axis, Operating Role (R1-R5, R0), validates the Primary Output assignment internally
    and is not published; Capability Domain and Primary Output are the two published axes.

Text / visual treatment:
  - Method badges: filled cards, each a 12 pt bold ALL-CAPS cap + 9 pt regular body, 1 pt black
    border. Fill ramps lightest-to-darkest across the three (E2E9EF -> B6C8D8 -> 6E91B1) to read
    as a 1-2-3 sequence; the third badge (6E91B1) flips to white text. If a flat treatment is
    preferred, fill all three F2F2F2 (gray) instead - do not mix.
  - Worked-example chip: single pale-blue chip (E2E9EF, 1 pt black border), 8.5 pt. The "->" and
    "x" are allowed here as a label-flow / formula, not as sentence shorthand.
  - Operating-Role caveat: 8.5 pt italic, no fill, no border.

CHART, IF NEEDED
----------------
None. The maturity ordering of Primary Output is carried by the ladder exhibit described in
TABLE B (rendered as fills, not a plotted chart).

TABLE, IF NEEDED
----------------
TABLE A - Capability Domain (D), the "what ship area" axis (PRIMARY table on the page)

Copy / rows / columns:
  Columns: Code | Domain | Scope (fragment)
    D1  | Hull, Structures & Marine Fabrication        | Hull, superstructure, decks, weldments, foundations, structural units.
    D2  | Propulsion & Power-Transmission Machinery    | Prime movers and drive: turbines, diesels, motors, reduction gears, shafting, propulsors.
    D3  | Electrical Power (Gen, Conv & Dist)          | Generates, converts, distributes ship-service power: gensets, switchboards, transformers, switchgear.
    D4  | Fluid, Pressure & Piping Systems             | Valves, pumps, actuators, compressors, HP air, piping, seals, filtration.
    D5  | Thermal, HVAC & Life-Support                 | Chillers, HVAC and refrigeration, heat exchangers, ventilation, atmosphere and life-support.
    D6  | Mission, Combat & Communications Systems     | Sonar, radar, EW, comms, fire-control, masts, and ordnance (guns, launchers, handling).
    D7  | Electronic Components, Interconnect & Cable  | Penetrators, connectors, feedthroughs, cable and harness, circuit cards, instrumentation.
    D8  | Mechanical Handling & Deck Machinery         | Davits, cranes, hoists, winches, elevators, weapons-handling, access doors.
    D9  | Specialty Materials & Precision Processes    | Forging, casting, machining, composites, elastomers, signature treatments (ship use unknown).
    D10 | Interiors, Habitability & Outfitting         | Joinery, galley and berthing outfit, insulation, deck covering, habitability and egress gear.
    D11 | Services & Non-Material Support              | Engineering, test/R&D, install/field service, repair/overhaul, logistics, software/IT, training.
    D0  | Unresolved / Insufficient Evidence           | No single defensible domain: multi-domain firm or thin evidence; still gets one label.

Purpose:
  Document the full, MECE set of technical ship areas a supplier can be placed in. A pure
  technical-area axis - no role or production-mode meaning.

Structure:
  Code-ordered (D1..D11, then D0 last as the catch-all). Three columns; the Domain column is the
  scan column. Fragments only in Scope - no sentences.

Cell / table treatment:
  - Header: dark fill 263746, white 9 pt bold text, left-aligned.
  - Code column: 9 pt bold, centered, ~0.5 in wide (row-identity feel).
  - Domain column: 9 pt regular, left, the widest column.
  - Scope column: 8.5 pt regular, left, wraps to two lines max.
  - D0 row: light-gray fill F2F2F2 across the row to mark it as the catch-all.
  - Rules only: 1.5 pt under the header, 1 pt under each body row, none under the last row.
    No vertical borders, no interior grid.
  - Size rows to content so the 12 rows read even, not ragged.

Fit behavior:
  Shorten the Scope fragments first. All 12 codes must stay visible (dropping any breaks MECE).
  Do not add Operating Role or SWBS columns here.

----

TABLE B - Primary Output (P), the "what physically ships" axis, rendered as a maturity ladder

Copy / rows / columns:
  Columns: Code | Output | What ships (fragment)
  Ladder rungs, HIGHEST maturity at top:
    P5 | Outfitted Structures & Ship Modules        | Major structural section or outfitted module, moved as a shipbuilding unit.
    P4 | Integrated Systems & Configured Shipsets    | Multiple interdependent elements delivered as one configured, integrated system.
    P3 | Functional Equipment & Machinery            | Acceptance-testable unit that performs a function once installed (engine, pump, switchboard).
    P2 | Finished Parts & Fabricated Components       | Fit-ready parts that install into a larger item (machined parts, fittings, spools, harnesses).
    P1 | Materials, Stock & Bulk Inputs              | Material needing downstream work, or consumed in process (plate, forgings, coatings, consumables).
  Off-ladder (below a thin divider):
    P6 | Services & Technical Work Products          | Labor-led or intangible handoff (engineering, test, install, repair, software, data).
    P0 | Unresolved / Attribution-Only              | No defensible output; parent, investor, or holding-company attribution.

Purpose:
  Show that Primary Output is a deliverable-maturity ladder (P1 lowest to P5 highest), with P6
  for labor-led handoffs and P0 for attribution-only - so "delivered form" is ordered, not a flat
  list. This is why it is a ladder, not a second plain table.

Structure:
  Five stacked rungs P1->P5 (ascending), then a divider, then P6 and P0 as off-ladder rows. Each
  rung is a full-width filled bar; the ramp encodes the ordering.

Cell / table treatment:
  - Ramp fill rises P1 -> P5: E2E9EF, B6C8D8, 6E91B1, 3D5972, 263746.
  - Text flips to WHITE at the third step (6E91B1) and darker: P3, P4, P5 white text; P1, P2 black.
  - Off-ladder rows in gray: P6 = F2F2F2, P0 = D9D9D9, both black text.
  - Every filled rung carries a 1 pt black border.
  - In-rung layout: Code 11 pt bold + Output name 11 pt bold on the left; What-ships fragment
    8.5 pt regular on the right (or as a subline). A small "maturity" arrow on the left edge
    (P1 bottom -> P5 top) is optional.

Fit behavior:
  Keep all 7 codes. Shorten the What-ships fragments before anything else. Do not re-order the
  rungs (the ascending order is the message).

OBJECT NOTES, IF NEEDED
-----------------------
  - Reading order: Capability Domain table (left) is read first as the primary exhibit; the
    Primary Output ladder (right) second; method badges last.
  - The two columns should top-align; the ladder + badge stack on the right should bottom-align
    with the 12-row table so the slide reads balanced (the badges fill the right column's lower
    third because the ladder is shorter than the 12-row table).
  - Keep the one divider line (between P5 and P6) thin; do not add other dividers.
  - Do not add a third-axis (Operating Role) table or a SWBS table - they belong on the Taxonomy
    tab / a separate slide.

TYPOGRAPHY HIERARCHY (Arial throughout)
---------------------------------------
  - Title "Topic | Finding.": 20 pt. Topic ("Vendor Archetypes") bold; pipe and Finding in
    regular weight, sentence case, ending in a period.
  - Concept caption (under title): 10 pt italic, black - framing/qualifier register.
  - Table A header row: 9 pt bold, white on the dark header.
  - Table A Code cells: 9 pt bold; Domain cells: 9 pt regular; Scope fragments: 8.5 pt regular.
  - Ladder rung cap (code + output name): 11 pt bold; rung fragment / subline: 8.5 pt regular.
  - Method-badge cap: 12 pt bold ALL CAPS; badge body: 9 pt regular.
  - Worked-example chip: 8.5 pt regular (the "->" / "x" read as a formula flow, allowed).
  - Operating-Role caveat: 8.5 pt italic.
  - Source note: 8 pt.
  Hierarchy logic: bold carries structure (codes, caps, ladder rungs); italic marks the
  caption and the role caveat; size separates the title (20) from exhibit text (8.5-11). No
  size larger than the 20 pt title appears on this slide - it is reference, not a KPI slide.

BACKGROUND / FILL COLOR
-----------------------
  - Slide background: white (FFFFFF), no fill.
  - Capability Domain table: no-fill body rows (white) carried by horizontal rules; dark header
    263746 with white text; D0 catch-all row filled light-gray F2F2F2. This is the one dark
    header on the slide (the primary table).
  - Primary Output ladder: blue ramp by maturity - P1 E2E9EF, P2 B6C8D8, P3 6E91B1, P4 3D5972,
    P5 263746; white text from P3 up. Off-ladder P6 F2F2F2, P0 D9D9D9 (black text). 1 pt black
    border on every filled rung.
  - Method badges: blue ramp E2E9EF -> B6C8D8 -> 6E91B1 (white text on the third), or flat F2F2F2
    if a non-sequenced look is wanted; 1 pt black border on each.
  - Worked-example chip: pale-blue E2E9EF fill, 1 pt black border.
  - No-fill, no-border for all interpretive text: concept caption, role caveat, source.
  - Fill rule honored: only objects with semantic weight (axis codes, method steps, the example)
    carry fill; definitions and captions stay no-fill. Dark fills always take white text.
  - No pale-yellow placeholder (FFFFCC) is needed - every object has real content.

SOURCES
-------
Copy:
  SAM.gov and USAspending prime and subaward records; NAICS-6 archetype map with entity-level
  (Program, UEI) overrides. Classification vocabulary (Capability Domain, Primary Output) per the
  workbook taxonomy. Grain: one label per UEI x Program.
