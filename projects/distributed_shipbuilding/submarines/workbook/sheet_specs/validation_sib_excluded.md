SIB Excluded
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_sib_excluded.py

Purpose
The SIB (Submarine Industrial Base) exclusion trail: BlueForge Alliance, Training
Modernization Group, and the Institute for Advanced Learning and Research are capacity
grants / workforce support, NOT construction outsourcing, so their subaward $ is excluded
from the SAM (Sec. 8 guardrail). Only outsourced new-construction supplier work counts in
TAM. Earlier source files use MIB / Maritime Industrial Base; visible text says SIB.

Source
extracted/sam_subaward_top_parents.csv - the three SIB parents' total $M + action count
  (filtered by UEI: F8PEZKXES8B1, QLJZVM6XKR71, TCM3R4JPRKY4).
extracted/nc_scope_summary.json - key dollars_excluded_mib_$M, the SIB exclusion anchor;
  the third entity's $ is back-solved as sib_total - BlueForge - TMG.

Reads
- none (standalone leaf; loads its own CSV/JSON, links no sibling sheet)

Feeds
- Methodology (SIB glossary note), z_ChartData (CD_16), Figure Register (DO-08),
  QA Reconciliation (QA-09, anchor $4,251.8M)
- Accessors: sib_total_cell() -> 'SIB Excluded'!D<total row>; mib_total_cell (alias);
  sib_entity_dollar_cell(i) -> i-th entity $ cell (z_ChartData); SIB_ENTITY_NAMES

On the sheet
(Layout note: §2 detail is built first so sib_total_cell is promoted before §1.)

§1  At a glance: SIB exclusion
    - Total SIB exclusion $M <- §2 total row (sib_total_cell)  (excluded from the SAM)
    - Number of SIB entities = 3  (largest: BlueForge Alliance)
    - Cell note: the three entities are capacity-development pass-throughs (shipyard
      capacity, workforce/training, industrial-base R&D), not construction subawards.

§2  SIB exclusion (capacity grants, not construction outsourcing)
    - One input row per UEI (UEI, Display name, Total $M, Action count, % of SIB total):
        - BlueForge Alliance (F8PEZKXES8B1)                     <- CSV total_$M / action_count
        - Training Modernization Group, Inc. (QLJZVM6XKR71)     <- CSV total_$M / action_count
        - Institute for Advanced Learning and Research (TCM3R4JPRKY4)
            Total $M = sib_total (nc_scope_summary.json) - BlueForge - TMG; action_count = 1
    - % of SIB total = D<row> / D<total row>
    - Total (SIB exclusion) row = SUM of the entity Total $M / action / % columns; the
      Total $M cell is sib_total_cell (= nc_scope_summary.dollars_excluded_mib_$M, anchor
      $4,251.8M checked in QA Reconciliation QA-09).

Notes
- Native cell notes: 1 -
    §1 (C): BlueForge Alliance, Training Modernization Group, and the Institute for Advanced Learning are the removed SIB entities
- Note column: none.
