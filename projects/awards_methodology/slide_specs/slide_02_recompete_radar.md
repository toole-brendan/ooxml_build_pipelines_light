# Slide Spec — Recompete Radar

```text
SLIDE 02 - Recompete Radar
Type: Body

Slide's purpose:
  The payoff: populate the funnel's lower gates with the actual named vehicles. Show
  the forward (and overdue) pipeline of competitor buying vehicles reaching their
  ordering-period end, each with its incumbent, route, and the fact that none was
  advertised on the portal. Carry the honest framing: the close date is certain (an
  FPDS field), the re-buy is inferred, and the order history signals how strong that
  inference is.

TITLE
-----
Copy:
  Recompete Radar | 52 competitor vehicles reach turnover, 12 already overdue, none advertised on SAM.gov Opportunities.

HIGH-LEVEL LAYOUT
-----------------
A thin KPI strip of four readouts across the top, then a full-width table beneath
it (scoreboard over register). The strip is the shape of the pipeline; the table is
the named candidates. No chart.

COMMENTARY COPY
---------------
Commentary 1
  Copy:
    Every vehicle here reaches its ordering-period end with no notice on the portal yet; the route is set by the vehicle, not by us.
    Bid the open ones, get on the multiple-award on-ramps, or sub to a holder on the FAR 16.5 vehicles.
  Text / shape treatment:
    Bold finding strap directly under the table, no fill, full width.

Commentary 2
  Copy:
    Clock = the vehicle's ordering-period end (FPDS lastDateToOrder) - date-certain, and visible 2-6 years before the portal shows anything.
    The re-buy is inferred, strongest where the order history is deep; successor and access are applied per vehicle.
  Text / shape treatment:
    Small italic footnote line at the bottom, no fill, no border - the honesty
    caveat, set quieter than the finding strap.

OTHER VISIBLE COPY
------------------
Copy (KPI strip, four readouts left to right):
  52 vehicles surfaced (>= $5M)
  12 ordering periods already closed (overdue)
  100% with no portal notice
  clock visible 2-6 years before the portal

Text / visual treatment:
  Four no-fill readouts: large value over a small caption, separated by thin
  vertical rules. The strip stays no-fill so the table is the only filled object on
  the slide. Every readout is a count or fact drawn straight from the table below.

TABLE
-----
Copy / rows / columns:
  Columns: Clock | $M | Orders | Incumbent | Tier | Route | Notice
  Representative rows (full set = the 52 on the Recompete Radar tab, soonest clock first):
    2023-09-30 | 117.8 |  8 | Gravois Aluminum Boats | small craft  | holders-only       | NONE
    2023-09-30 |  44.0 | 13 | United States Marine   | small craft  | holders-only       | NONE
    2024-04-03 |  27.5 |  7 | RIBCRAFT USA           | small craft  | holders-only       | NONE
    2026-03-15 |  16.2 |  1 | Silver Ships           | small craft  | open / standalone  | NONE
    2026-10-01 |  55.7 |  8 | Silver Ships           | small craft  | holders-only       | NONE
    2027-01-31 |  98.7 |  1 | NASSCO                 | other small  | open / standalone  | NONE

Purpose:
  Name the addressable candidates and make two things land: every Notice cell is
  NONE (these are competitors' vehicles, none advertised), and the turnover is real
  and dated (clocks in the recent past and near future).

Structure:
  One row per vehicle, ordered by Clock soonest-first so the overdue rows sit on top.
  Clock is the FPDS ordering-period end (lastDateToOrder for an IDV, ultimate
  completion for a standalone). Orders is the re-buy-confidence signal: a deep order
  history (8, 13) is a strong recurring channel; a single order is a softer bet.
  Route is read off the vehicle structure (open / multiple-award / holders-only).

Cell / table treatment:
  Dark header (blue fill, white text) - the one primary table on the slide. Clock,
  $M, and Orders right- or center-aligned; Incumbent, Tier, Route left. The Notice
  column is a single uniform light-gray band (every cell identical "NONE") - the
  rhetorical device. In the Route column, open / standalone cells take a soft-positive
  light-blue fill (reachable now); holders-only cells stay no-fill (gated). Horizontal
  rules only, no vertical borders.

Fit behavior:
  Keep Clock, Incumbent, Route, and Notice visible at all costs - they carry the
  argument. Drop Tier first, then Orders, if width is tight. Do not add an Obligated-
  to-date column or a status column; the strip already carries the totals.

OBJECT NOTES
------------
  - The KPI strip and the table are the same evidence at two grains; the strip floats
    above with whitespace separating it from the table, not a heavy divider.
  - The all-NONE band is the punchline - keep it a single continuous gray, identical
    across rows, so it reads as one block beside named competitors.
  - Keep the dark-header table as the only filled object family; the route soft-blue
    cells are the one accent and must not compete with it for weight.

SOURCES
-------
Copy:
  Sources: USAspending award detail; FPDS per-action records (lastDateToOrder); SAM.gov Contract Opportunities
```
