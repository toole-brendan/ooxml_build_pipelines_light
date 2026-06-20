AP Bridge
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_ap_bridge.py

Purpose
Derives the AP/LLTM stream base and classifies P-10 lines as supplier-addressable
or excluded, feeding the second TAM stream.

Source
extracted/scn_li_resource_summary.csv (LI 2122 rows) - the SCN P-1/P-10 resource summary.

Reads
- Assumptions   CY AP base per FY [ap_lltm_base_cell], ship-construction share, AP/LLTM
           supplier coeff

Feeds
- QA Reconciliation (reconciliation)
- Producer cells: cy_ap_gross, eoq_gross, cy_ap_inwindow, ap_tam (AP/LLTM stream TAM)

On the sheet
§1  Resource summary ($M, FY27 PB; P-1/P-10 view)
    - CSV-loaded input rows for LI 2122: Gross/Weapon System Cost, Plus CY AP, Plus EOQ,
      Less PY AP, Less EOQ, Net Procurement (P-1), Total Obligation Authority.
    - Period columns: Prior Years, FY25-FY31, To Complete, Total (gross all-periods).

§2  TAM-base derivation (CY AP x ship-construction share x supplier coeff)
    - CY AP in-window      = sum of Assumptions CY AP, FY22-27 (FY22-24 lump into "Prior Years",
                             so this is a lower bound)
    - x ship-constr share  = non-GFE AP base   (Assumptions knob, default 0.80; strips AWS EOQ /
                             Other GFE)
    - x AP/LLTM coeff      = AP/LLTM stream TAM (Assumptions knob, default 0.85)  [feeds QA Reconciliation]

§3  Line-level classification (DDG P-10 structure)
    INCLUDE / EXCLUDE table by AP/EOQ line:
    - Ship Construction EOQ            INCLUDE        new-construction supplier material
    - AWS EOQ (Aegis Weapon System)    EXCLUDE        GFE-controlled combat system
    - Other GFE / CBSP AP              EXCLUDE        Navy-furnished equipment
    - VLS / weapons / ordnance AP      EXCLUDE        WPN/OPN appropriation, not SCN
    - Power Conversion Modules         IN BC ALREADY  moved GFE -> BC in FY23 (no re-add)

§4  Caveats
    - Ship-Construction vs AWS/Other-GFE split is an editable Assumptions knob (P-10 doesn't
      parse cleanly).
    - No double-count: P-5c BC is net of prior-yr AP, so CY AP is additive (PY-AP credit = 0).

Notes
- Native cell notes: 3 -
    §2 (C): ship-construction share knob (default 0.80) strips AWS EOQ / Other GFE from CY AP
    §2 (C): AP/LLTM stream TAM = in-window CY AP x ship share x AP/LLTM coeff (an additive stream)
    §4 (C): no double-count - P-5c BC is already net of prior-yr AP, so CY AP is additive (PY-AP credit 0)
- Note column: none.
