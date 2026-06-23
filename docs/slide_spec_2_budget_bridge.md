# Slide Spec — 02 · From Appropriation to Obligation (Contracts ↔ Budget)

```text
SLIDE 02 - FROM APPROPRIATION TO OBLIGATION: ALIGNING CONTRACTS TO THE BUDGET
Type: Body

Slide's purpose:
  Show how contract awards (the demand signal - who got money, for what) connect to
  appropriations (the authority - what Congress funded). Be honest that the join is clean at
  the appropriation-account + color-of-money + fiscal-year level and lossy below it, and
  that durable program-level alignment runs through a curated "opportunity" bridge, not an
  automatic Treasury-Account-Symbol-to-line-item key join. This is the "who funds" role from
  Slide 1, in depth.

TITLE
-----
Copy:
  Aligning contracts to the budget | The join is clean at the account; the program-level
  bridge is curated, not automatic.

HIGH-LEVEL LAYOUT
-----------------
  Left-to-right bridge diagram across the upper two-thirds: BUDGET AUTHORITY (left) ->
  TREASURY ACCOUNT SYMBOL (center connector) -> OBLIGATION ON A CONTRACT (right). The left
  node expands into the budget hierarchy (account -> budget activity -> line item / program
  element); the center shows the analyst opportunity-attribution bridge; the right shows
  contract families. A method / caveat rail runs along the bottom. The funded-demand funnel
  is a small inset, lower-right.

COMMENTARY COPY, IF NEEDED
--------------------------
Commentary 1
  Copy:
    The only valid join keys are agency, Treasury Account Symbol, and fiscal year.
    Budget is not organized by NAICS or PSC, so contract codes do not bridge. What the
    appropriation does tell you is "color of money" - RDT&E (development), Procurement /
    OPA (production), O&M (sustainment) - which reads as a program's lifecycle stage.
  Text / shape treatment:
    Bold finding line; no-fill text rail above the bridge.

Commentary 2
  Copy:
    The hard part: the TAS resolves the account, not the program.
    A contract's funding_tas lands it in "Other Procurement, Army, FY-XX" - but not in a
    specific line item or program element. We therefore bridge budget and contracts through
    an analyst-curated OPPORTUNITY that both a budget line and a contract family attribute
    to. The TAS is captured as the mechanical hook; the semantic alignment is deliberate.
  Text / shape treatment:
    Filled card centered under the TAS connector - this is the slide's key insight; give it
    the most visual weight of the three commentaries.

Commentary 3
  Copy:
    Funded demand and historical obligations are separate lenses - never summed.
    The forward budget spine sizes the market (Gross funded -> Addressable -> Serviceable ->
    Weighted pursuit); contract obligations measure what has already flowed. Keep them apart.
  Text / shape treatment:
    Below-exhibit note tied to the funnel inset; muted.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Bridge node labels: "Appropriation account -> Budget activity -> Line item (P-1) / Program
  element (R-1)" | "Treasury Account Symbol (captured on award)" | "Contract family
  (PIID / IDV)".
  Money-type discipline chip: "PY actual -> CY enacted -> BY request -> outyears; request =
  request_total only; never summed across types."

Text / visual treatment:
  Three bridge nodes equal height; the center TAS node visually narrower (it is a connector,
  not a destination). Color the left node by "color of money" swatches; keep the right node
  neutral.

CHART, IF NEEDED
----------------
Copy / data / labels / chips:
  Inset funnel, units caption "Forward FY27-31, then-year $M". Tiers top-to-bottom: Gross
  funded -> Addressable (x addressable %) -> Saronic-serviceable (x fit %) -> Weighted
  pursuit (x timing x access x win). Data labels illustrative.
  Purpose:
    Show that the budget spine - not contract obligations - is what the market sizing sits
    on, reinforcing Commentary 3.
  Structure:
    Four-tier descending funnel; each tier a fraction of the one above; multipliers labeled
    on the step.
  Text / visual treatment:
    Muted relative to the main bridge; it is supporting, not the hero exhibit.
  Fit behavior:
    If space is tight, drop to the funnel's two endpoints (Gross funded -> Weighted pursuit)
    with the multiplier chain as a caption. The bridge diagram must remain dominant.

TABLE, IF NEEDED
----------------
Copy / rows / columns:
  Small worked-example table beneath the bridge. Columns: Program | Line item / PE | Approp
  (color) | Bridged opportunity.
  Row 1: MSV(L) - Maneuver Support Vessel (Light) | BLI 8211R01001 | OPA (Procurement) |
    OPP-MSVL.
  Row 2: Army Watercraft ESP (SLEP) | BLI 3569M11101 | OPA (Procurement) | OPP-ESP.
  Row 3: Project 526 - Marine S&T (autonomy / C2) | PE 0603804A-526 | RDT&E | OPP-AWS-
    AUTONOMY.
  Purpose:
    Make the budget side concrete - real PB2027 lines, the two colors of money, and the
    opportunity each attributes to.
  Structure:
    Three rows; "Approp (color)" is the scan column. PB2027 vintage only (single vintage, no
    cross-year blending).
  Cell / table treatment:
    Program bold; color-of-money cell tinted by appropriation type; opportunity column
    monospace IDs. Header underlined.
  Fit behavior:
    Drop the "Bridged opportunity" column first if needed; the line item + color must stay.

OBJECT NOTES, IF NEEDED
-----------------------
  - Reading order: bridge left-to-right first, then the key card under the TAS connector,
    then the worked-example table, then the funnel inset.
  - The TAS connector should visually "pinch" between the two large nodes to read as the
    single thread that ties budget to contract.
  - Do not add: a literal TAS-to-PE crosswalk arrow (it does not auto-join - that is the
    whole point); the opportunity bridge is the only connector between budget and contract.

Do not repeat:
  - Title copy.
  - Commentary copy or treatment.
  - Chart copy, data, labels, or treatment.
  - Table copy, data, or cell treatment.
  - Source note.

SOURCES
-------
Copy:
  Appropriations / budget lines: President's Budget P-1 (procurement) and R-1 (RDT&E),
  PB2027 vintage. Funding linkage: USAspending funding endpoint (Treasury Account Symbol per
  transaction). Worked example and the opportunity-attribution bridge: internal Army Market
  Mapping workbook (Budget Facts; budget_opportunity_attribution + award_opportunity_
  attribution). Then-year dollars.
```
