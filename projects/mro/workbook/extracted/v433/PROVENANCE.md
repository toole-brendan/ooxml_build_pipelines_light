# extracted/v433 — read-only provenance (NOT a build input)

These JSON files are the pristine extracted grid of the original v4.33 Excel model. They
were the source from which the MRO workbook was ported during the native rewrite
(Phases 0–4). **They are no longer read by the build.** Every formula sheet is now a
hand-authored `RowCursor` builder under `workbook_mro/sheets/`, the data tabs load the
CSVs in `extracted/` (`awards.csv`, `j998_j999.csv`, `psc_1905_classified.csv`), and the
workbook ships **zero defined names** (cross-sheet coupling is via import-time closure
accessors).

What still touches this directory, and only read-only:

- `qa/inspect_v433.py` — a structural browser for eyeballing the original grid.
- `qa/verify_crosstab.py` — proves the native Services §1/§2/§3 cross-tab loops reproduce
  the extracted `Services.json` formula strings byte-for-byte (a fast, soffice-free gate).
- `_defined_names.json` — the 88 v4.33 defined names. These were frozen into
  `qa/gold/baseline.json["defined_names"]` as the tie-out oracle (Invariant B). The
  workbook itself no longer declares them; `qa/name_map.py` maps each to its producer
  accessor cell so the tie-out validates the model figures by recompute.

Do not edit. Do not wire into the build. Treat as historical record.
