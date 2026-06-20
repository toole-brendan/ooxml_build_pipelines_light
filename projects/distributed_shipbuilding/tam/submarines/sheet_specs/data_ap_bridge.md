AP Bridge
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_ap_bridge.py

Purpose
The P-10 advance-procurement bucket grids (Virginia + Columbia), the P-10 -> TAM
treatment crosswalk, and the central reconciliation bridge that confirms the AP/LLTM
additive base nets to $0 (supplier LLTM is already inside P-5c Basic Construction, so
wiring P-10 AP as a separate stream would double-count the BC TAM). This bridge is the
producer block for the Executive Summary's AP/LLTM bridge.

Source
extracted/scn_p10_ap_buckets.csv - per (LI, Bucket, FY) "Best Value $M" rows; redacted
cells parse to blank. LI 2013 = Virginia, LI 1045 = Columbia.

Reads
- Assumptions   ap_gross_cell(li, fy) - the authoritative P-10 gross AP
                           top-line per ship/FY (the §5 gross row sums N(...) of these
                           over LI 2013/1045 x FY22-27)

Feeds
- z_ChartData, Figure Register, Slide Data, Executive Summary (AP/LLTM bridge),
  QA Reconciliation (holds the official base = 0 gate)
- Producer cells / accessors (all C-column of the §5 bridge):
  ap_bridge_gross_cell, ap_bridge_gfe_removed_cell, ap_bridge_in_bc_removed_cell,
  ap_bridge_residual_cell, ap_bridge_base_cell (= confirmed $0)

On the sheet
§1  At a glance: P-10 -> TAM bridge ($M, FY22-27)
    - Same-sheet echo of the §5 bridge producer cells: gross AP top-line, less GFE /
      design / weapons, less already inside P-5c BC, less un-itemized overlap, AP/LLTM
      additive base (= confirmed $0). Notes flag the gross as non-additive (overlaps BC).

§2  Virginia (LI 2013) P-10 AP buckets ($M, FY20-31)
    - Grid: 10 buckets (Plans/SIB, EOQ, Nuclear plant LLTM, Propulsor LLTM, Electronics
      LLTM, HM&E LLTM, Ordnance LLTM, Missile compartment LLTM, Shipbuilder-procured
      LLTM, Shipbuilder-procured LLTM (CFE)) x FY2020-2031, $-input cells from the CSV.
        per-bucket Total = SUM(FY20:FY31 of that row)
        Class total row  = SUM down each FY column + SUM of the totals.

§3  Columbia (LI 1045) P-10 AP buckets ($M, FY20-31)
    - Same 10-bucket x FY grid and Class-total logic as §2, for LI 1045.

§4  P-10 bucket -> TAM treatment (AP/LLTM base = 0)
    - Crosswalk table (bucket, TAM treatment, basis), one row per reconciliation entry:
        EXCL GFE  - Nuclear plant LLTM (BPMI naval reactor), Electronics LLTM
                    (Navy-furnished), Missile compartment LLTM (CMC / tubes)
        EXCL wpn  - Ordnance LLTM (WPN/OPN, not SCN)
        EXCL des  - Plans / SIB (lead-yard design - Plan Costs)
        IN BC     - Shipbuilder-procured (+CFE), EOQ, HM&E / Propulsor LLTM (inside BC)

§5  P-10 -> TAM reconciliation bridge ($M, FY22-27)  - the producer block
    - Walk from gross to a $0 additive base over FY22-27, Virginia + Columbia:
        gross AP top-line  = SUM of N(ap_gross_cell(li, fy)) over LI x FY22-27
                             <- Assumptions  [ap_bridge_gross]
        less GFE / design / weapons  = -(SUM FY22-27 of the EXCLUDE buckets:
                             Nuclear + Electronics + Ordnance + Missile + Plans, both LIs)
                             [ap_bridge_gfe_removed]
        less already inside P-5c BC  = -(SUM FY22-27 of the IN-BC buckets:
                             Propulsor + HM&E + Shipbuilder-procured + CFE + EOQ, both LIs)
                             [ap_bridge_in_bc_removed]
        less un-itemized overlap     = -(gross + GFE-removed + in-BC-removed)
                             (early-Va top-line over named detail)  [ap_bridge_residual]
        = AP/LLTM additive base = 0  = gross + all three removals  [ap_bridge_base]

§6  Reconciliation checks
    - Bridge nets to the additive base = IF(|base - (gross + gfe + in_bc + residual)|
      < 0.5, "OK", "FAIL").
    - AP/LLTM additive base = 0 = IF(|base| < 0.5, "OK", "FAIL")  (QA Reconciliation
      holds the official gate).

Notes
- Native cell notes: 2 -
    §1 (C): P-10 gross AP is the authoritative top-line but overlaps Basic Construction (non-additive)
    §1 (C): after removing GFE / design / weapons and the portion already inside BC, the AP/LLTM base nets to $0
- Note column: none.
