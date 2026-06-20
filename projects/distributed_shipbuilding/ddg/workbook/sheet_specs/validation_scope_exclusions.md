Scope Exclusions
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_scope_exclusions.py

Purpose
The cleanup trail: contaminant PIIDs removed and out-of-scope PIIDs grouped by
class, with FPDS obligated $M as a size indicator (audit only). Data-driven from
nc_scope_summary.json and _discovered_piids.csv.

Source
extracted/nc_scope_summary.json (records kept/excluded, in-scope dollars, parent UEIs,
the out-of-scope PIID -> reason map) and extracted/_discovered_piids.csv (FPDS
obligated $M per PIID, kept as the max seen per PIID).

Reads
- none (standalone scope arbiter; no cross-sheet dependencies)

Feeds
- none (exports nothing; producer: SCOPE_EXCLUSIONS SheetEntry)

On the sheet
§1  Cleanup summary (after removing 16 contaminant PIIDs)
    - Records kept (in-scope)              <- JSON records_kept
    - Records excluded (out-of-scope PIIDs) <- JSON records_excluded_out_of_scope_piids
    - Records pre-clean (kept + excluded)  = C{kept} + C{excluded}  (derived)
    - In-scope dollars ($M)                <- JSON total_dollars_in_scope_$M (rounded 1dp)
    - Unique in-scope parent UEIs          <- JSON unique_parent_ueis_in_scope

§2  Excluded PIIDs by class (FPDS obligated $M = size indicator)
    Each out-of-scope PIID is classified by its reason text into one of three blocks,
    sorted by PIID; FPDS obligated $M pulled from _discovered_piids.csv per PIID.
    §2a IVECO - Marine Corps Mk110 gun (not DDG)        (reason contains "IVECO" / "Marine Corps")
    §2b DDG-1000 / Zumwalt - out of class (LI 2119, closed)  (default class)
    §2c WPN/OPN weapons - ESSM + CIWS, different appropriation  (reason contains "WPN/OPN")
    - Each block: PIID / Reason / FPDS obligated $M rows, then a
      Subtotal - <block> = SUM(D{first}:D{last}) total row.

Notes
- Native cell notes: none.
- Note column: none.
