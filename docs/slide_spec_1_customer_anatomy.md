# Slide Spec — 01 · The Federal Customer (Who Funds / Who Buys / Who Uses)

```text
SLIDE 01 - THE FEDERAL CUSTOMER: WHO FUNDS, WHO BUYS, WHO USES
Type: Body

Slide's purpose:
  Orient the audience that in federal / defense markets the organization that HOLDS THE
  MONEY, the organization that RUNS THE COMPETITION AND AWARDS, and the organization that
  ACTUALLY USES the capability are usually three different organizations. Establish this
  triad as the lens for the rest of the deck (Slide 2 details "who funds"; Slide 3 details
  "who buys, and when") and set honest expectations about how reliably each of the three is
  recoverable from awards data.

TITLE
-----
Copy:
  The federal customer is three customers | Money, decision authority, and end-user rarely
  sit in one organization.

HIGH-LEVEL LAYOUT
-----------------
  Three-column "customer anatomy." A thin left-to-right relationship band runs across the
  top showing the org chain (operational user -> requirement / experimentation -> program /
  acquisition -> contracting). Beneath it, three labeled columns - WHO FUNDS / WHO BUYS /
  WHO USES - each anchored by the Army watercraft worked example. A data-visibility rail
  sits below (or down the right) rating how recoverable each role is from awards data. The
  triad mapping itself is carried by the TABLE; the columns are its visual framing.

COMMENTARY COPY, IF NEEDED
--------------------------
Commentary 1
  Copy:
    Payer is not buyer is not user.
    Conflating the three is the classic market-mapping error: the appropriation that funds
    a program, the contracting office that awards it, and the unit that fields it answer to
    different commands and live in different places.
  Text / shape treatment:
    Lead finding as a bold one-liner above the three columns; no-fill text rail.

Commentary 2
  Copy:
    Each "who" is a different door for business development.
    Shape the requirement with the user / requirements side (theater command, Futures
    Command CFTs); win the award through the contracting office (and watch its OTA / CSO
    pathways); confirm the money exists in the program office's budget lines.
  Text / shape treatment:
    Filled card, lower-left, beneath the WHO USES / WHO BUYS columns.

Commentary 3
  Copy:
    The three are not equally observable in the data.
    The BUYER falls straight out of the contract number; the PAYER is recoverable to the
    appropriation account via the Treasury Account Symbol; the END-USER usually is NOT in
    contract data at all and must be sourced externally (open program reporting, demos,
    requirements docs).
  Text / shape treatment:
    Side annotation tied to the data-visibility rail; muted box, smaller type.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Relationship-band labels (left -> right): Operational user -> Requirement /
  experimentation -> Program / acquisition -> Contracting.
  Column kicker chips: "WHO FUNDS - the money", "WHO BUYS - the decision", "WHO USES - the
  capability".

Text / visual treatment:
  Band rendered as four connected nodes with arrows; the three triad columns visually align
  under the band node(s) they map to (Program/acquisition spans funds+buys). Chips colored
  per column; arrows muted so the three role columns dominate.

CHART, IF NEEDED
----------------
  None - the relationship band is an object/connector treatment (see OBJECT NOTES), not a
  data chart.

TABLE, IF NEEDED
----------------
Copy / rows / columns:
  Columns: Role | What it is (DoD) | Army watercraft example | Awards-data visibility |
  Where we get it.
  Row 1 - WHO FUNDS: Appropriation + color of money + program element / budget line item;
    the program office owns it in programming terms | OPA line 8211R01001 (MSV(L)) and RDT&E
    PE 0603804A-526, programmed by PM Transportation Systems under CPE Combat Sustainment |
    MEDIUM - funding_tas resolves the appropriation account, not the PE/BLI | USAspending
    funding endpoint (TAS); President's Budget P-1 / R-1.
  Row 2 - WHO BUYS: Contracting office (DODAAC) plus the milestone / source-selection
    authority | ACC-Detroit Arsenal (DODAAC W56HZV) runs and awards; ASA(ALT) is the
    milestone decision authority | HIGH - DODAAC = first 6 characters of the PIID;
    contracting agency / office are native fields | FPDS / SAM Contract Awards / USAspending
    awarding-office fields.
  Row 3 - WHO USES: The operational command or unit that fields the capability | USARPAC /
    8th Theater Sustainment Command / 569th Dive Detachment (INDOPACOM) | LOW - place of
    performance and requiring activity are weak hints | Sourced externally (2025 autonomous
    ship-to-shore demo), NOT the contract APIs.

Purpose:
  Make the abstract triad concrete and immediately show the visibility asymmetry that the
  rest of the methodology has to work around.

Structure:
  Three rows, one per role, in funds -> buys -> uses order. "Awards-data visibility" is the
  scan column. Width priority: "Army watercraft example" and "Where we get it" widest; the
  visibility column narrow but bold.

Cell / table treatment:
  Role column bold. Visibility cells are emphasis cells - color-graded High (green) /
  Medium (amber) / Low (red), centered, single word. Body cells left-aligned, regular
  weight, wrap allowed. Header row underlined; no heavy gridlines.

Fit behavior:
  Shorten "What it is (DoD)" first. The Army example, the visibility rating, and the
  source-of-record must remain. Do not add a fourth role or per-org rows - the org detail
  lives in the workbook Customer Map, not on this slide.

OBJECT NOTES, IF NEEDED
-----------------------
  - Reading order: relationship band (top) is read first, then the three columns top-to-
    bottom, then the visibility rail.
  - Connector behavior: the WHO FUNDS and WHO BUYS columns both connect up to the "Program /
    acquisition" + "Contracting" band nodes; WHO USES connects to "Operational user". Keep
    connectors thin and behind the columns.
  - Alignment: the three triad columns share a common top and baseline; the worked-example
    line in each column sits at the same vertical position for left-to-right scanning.
  - Do not add: an org-by-org hierarchy chart (that is the workbook Customer Map, ~13 orgs);
    this slide is the 3-role abstraction only.

Do not repeat:
  - Title copy.
  - Commentary copy or treatment.
  - Table copy, data, or cell treatment.
  - Source note.

SOURCES
-------
Copy:
  Buyer/payer fields: FPDS, SAM.gov Contract Awards API, USAspending (awarding office +
  funding TAS). Entity resolution: SAM.gov Entity Management. End-user: external program
  reporting (not contract APIs). Worked example: internal Army Market Mapping workbook
  (Customer Map - operational user -> requirement -> program/acquisition -> contracting,
  with a live count of screened vehicles per contracting office).
```
