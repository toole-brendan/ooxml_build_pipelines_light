# DDG HII-Ingalls subaward package — SWBS / work-item codes by UEI

Purpose: provide the raw FFATA/FSRS subaward records for DDG-51 awards where **HII-Ingalls
is the prime** on the parent PIID, together with the two lookup tables needed to decode the
code(s) embedded in each subaward's description field. No analysis or conclusions are
included here — only the records and the conversion tables.

All three CSVs are verbatim copies. Originals (not modified) live at:
`projects/research_shared/taxonomy_design_input_canonical/`

## How the subaward `description` field is coded

For HII-Ingalls DDG subawards, the description (`raw_description`) can carry up to two codes:

1. **HII work-item code** — format `NNNNN-NN` (e.g. `03013-01`). The contractor's internal
   build code. Decoded in `hii_ddg_code_dictionary.csv` → its observed SWBS subsystem and
   the component wording that appears with it. It is finer than SWBS: one SWBS subsystem
   maps to several HII codes.
2. **SWBS subsystem** — 3-digit Navy code (e.g. `234`). Sometimes written explicitly in the
   description; otherwise it is the value associated with the HII code. Decoded in
   `swbs_hierarchy.csv`. Convert a 3-digit group `NNN` by looking up `eswbs_code = NNN + "00"`
   (e.g. `234` → `23400` → "Propulsion Plant / PROPULSION GAS TURBINES").

To see which UEIs appear against a given code or SWBS subsystem, filter / group
`hii_ddg_record_components.csv` (one row per subaward) on `code` or `swbs_group` and read
`vendor_uei` + `vendor_name`.

## Files

### hii_ddg_record_components.csv — raw subaward records (one row per subaward)
5,900 rows, all `builder == 'HII-Ingalls'`. (This copy was filtered to HII-Ingalls only; the
421 GD-BIW rows present in the source bundle were dropped — no other change.) Of these, 4,318
carry a value in `code` and/or `swbs_group`; 381 distinct `vendor_uei`; FY 2013–2026.
HII-Ingalls parent PIIDs (6): N0002411C2307, N0002411C2309, N0002412C2312, N0002413C2307,
N0002418C2307, N0002423C2307.

Columns:
- `piid` — parent contract PIID (the HII prime award).
- `builder` — HII-Ingalls (this copy contains HII-Ingalls only).
- `sub_report_id` — FSRS subaward report id (dedup key; one row per id).
- `sub_date` — subaward action date.
- `fy` — fiscal year.
- `amount_usd` — subaward amount.
- `vendor_uei` — subawardee UEI.
- `parent_uei` — subawardee's reported corporate parent UEI (blank where not reported).
- `vendor_name` — subawardee name as reported.
- `raw_description` — the subaward description text as pulled (source of the codes below).
- `code` — HII work-item code (`NNNNN-NN`) parsed from `raw_description`; blank if none.
- `swbs_group` — 3-digit SWBS subsystem associated with the record; blank if none.
- `hull` — hull number parsed from the description where present.
- `component_text` — component free-text token(s) parsed from the description.
- `n_component_words` — count of component words parsed.

### hii_ddg_code_dictionary.csv — decode table for the HII work-item code
365 rows (one per distinct `code`). All values are computed from the records above.
- `code` — HII work-item code.
- `n_subawards` — number of subawards carrying that code.
- `total_usd` — sum of `amount_usd` for that code.
- `modal_swbs_group` — most frequent `swbs_group` observed with that code (blank if none observed).
- `top_components` — most frequent component string(s) seen with that code; these are taken
  verbatim from the subaward descriptions (every value here is present in the raw text).

### swbs_hierarchy.csv — Navy SWBS/ESWBS codebook (reference)
1,888 rows. Standard Navy reference, not derived from the subawards.
- `eswbs_code` — SWBS/ESWBS code (3–5 digit).
- `one_digit_group` — top group 1–9.
- `group_name` — name of the 1-digit group.
- `nomenclature` — code description.
- `remarks` — codebook remarks.

## Truly-raw upstream sources (not copied here; pointers only)
- Parsed pull incl. a 2-digit `family` column: `projects/distributed_shipbuilding/ddg/research/ingalls_subaward_components.csv`
- Unparsed SAM/FSRS JSON pulls per PIID: `projects/distributed_shipbuilding/ddg/research/sam_subawards/`,
  `.../sam_subawards_fullhistory/`, `.../usaspending_subawards/`
