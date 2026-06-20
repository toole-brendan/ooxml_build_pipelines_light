Assumptions
Tab color: B8860B (ochre)  ·  group: Inputs & levers
Module: inputs_assumptions.py

Purpose
The single edit surface: every editable knob the model reads. Nothing is
hardcoded downstream that belongs here. The former Control section of the
composite Assumptions tab; stream toggles relocated here from TAM Build and the bucket-
share Adjustment relocated here from SAM Build. Editable cells carry data validation.

Reads
- none (this is the edit surface itself; values are hardcoded blue inputs, no cross-sheet links)

Feeds
- AP Bridge, POP Corpus, Scenarios, SAM Build, TAM Build, Sensitivity
- Promoted accessors (cell refs into 'Assumptions'!):
  - ap_lltm_base_cell(li, fy)   CY AP base per FY (§3)        -> AP Bridge, TAM Build
  - myp_master_cell(yard)       MYP master $ (§4)             -> TAM Build, POP Corpus
  - myp_pop_cell(yard, class)   reconstructed POP % (§4)      -> TAM Build, POP Corpus
  - ap_ship_construction_share_cell()  non-GFE share (§5)     -> AP Bridge, TAM Build
  - ap_supplier_coeff_cell()    AP/LLTM coeff (§5)            -> AP Bridge, TAM Build
  - include_bc_stream_cell() / include_ap_lltm_stream_cell()  (§2) -> TAM Build
  - bucket_adjustment_cell(bucket)  bucket-share adj (§6)     -> SAM Build
  - selected_scenario_cell()    selected SAM scenario (§1)    -> Scenarios

On the sheet
§1  Run settings
    - Program (DDG-51 Flight III; SCN LI 2122; yards BIW + Ingalls), FY range start
      (default 2022) / end (default 2027), Units (Nominal $M; nominal/real toggle =
      Phase 4), and Selected SAM scenario (default "broad"; dropdown over metal / hme /
      electrical / modular / broad)  [selected_scenario_cell]. List data validation on
      the scenario cell.

§2  Stream toggles (moved here from TAM Build)
    - Include BC stream (default 1; P-5c Basic Construction, GFE-free)  [include_bc_stream_cell]
    - Include AP/LLTM stream (default 1; CY AP x ship-construction share)  [include_ap_lltm_stream_cell]
    - 0/1 whole-number validation; TAM Build multiplies each stream base by these.

§3  AP/LLTM stream ($M, CY advance procurement)
    - DDG-51 (LI 2122) CY AP per FY, FY22-27 (defaults: FY22-24 = 0, FY25 = 83.224,
      FY26 = 1750.0, FY27 = 0)  [ap_lltm_base_cell] -> AP Bridge / TAM Build AP stream base.

§4  MYP master reconstruction (reconstructed POP %)
    - One row per yard - BIW MYP master (PIID N00024-23-C-2305, master default 6400)
      and Ingalls MYP master (PIID N00024-23-C-2307, master default 8180) - with
      reconstructed POP % split across BIW % / Ingalls % / Other-US % / Foreign %
      (BIW row 86/0/12/2; Ingalls row 0/88/10/2)  [myp_master_cell, myp_pop_cell].
      Decimal 0-1 validation on the POP-% block; TAM Build folds these masters back
      to correct the disclosed-only outside-yards artifact.

§5  AP/LLTM classification knobs
    - Ship-construction share of CY AP (default 0.80; non-GFE Ship-Construction-EOQ
      fraction, strips AWS EOQ / Other GFE)  [ap_ship_construction_share_cell]
    - AP/LLTM supplier coefficient (default 0.85; supplier POP share - assumption, no
      DDG AP corpus to SUMPRODUCT over)  [ap_supplier_coeff_cell]. Decimal 0-1 validation.

§6  Bucket adjustments (moved here from SAM Build)
    - One Adjustment +/- per work-type bucket (7 buckets; default 0 each - observed
      share kept unless adjusted)  [bucket_adjustment_cell]. Decimal -1..1 validation;
      SAM Build computes modeled share = observed + this adjustment.

Notes
- Native cell notes: none.
- Note column: none.
