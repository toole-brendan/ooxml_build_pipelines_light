# 2026-06-03 — light workspace flatten + standardize: projects/, infra/, appendix renames, co-located specs

## Scope

End-to-end cleanup of the **light** staging workspace (`ooxml_build_pipelines_light`).
Started from the `AI_AGENT_FLATTEN_STANDARDIZE_HANDOFF.txt` intent (flatten, standardize
names, validate with the build commands) and went further per live direction:

1. Group the two pipelines under a `projects/` tree; move build outputs to each project root.
2. Declutter the shared cores to **code-only** and move build chrome + reference into a new
   top-level `infra/` (matching the `core_pipeline` + `infra` split in the reference repo
   `ooxml_pptx_build_pipeline`).
3. Replace the three duplicate readmes with one generalized top-level `README.md`.
4. Standardize output filenames to the `_vS` suffix.
5. Prefix appendix **slide modules** with `appendix_`.
6. Bring the detailed text **slide specs** in from `../d2/` as co-located, name-aligned
   `slide_specs/`, and stand up the equivalent `sheet_specs/` infra on the workbook side.

Workspace is **not** under git — all moves were `mv`/`rm` with a full build re-run after each
major step. All four builds are green at every checkpoint.

---

## 1. `projects/` grouping + outputs at the project root

- `ddg/` and `submarines/` moved into `projects/`.
- Deck `.pptx` and workbook `.xlsx` now build to the **project root** (`projects/<proj>/`)
  rather than one level down in `deck/` / `workbook/`.
- `OUT` rebound in each `lib.py` to the project dir; `extracted/` (workbook input) and
  `images/` (deck input) stay in their subdirs.

## 2. Cores decluttered → `infra/`

`deck_core/` and `workbook_core/` are now **code-only** (engine modules + guides + the probe),
keeping their package names and `__init__.py` (80+ modules import `deck_core.lib` etc., and the
engine modules cross-import absolutely — so the packages could be *decluttered* but not renamed
or sub-packaged). Moved out to a new top-level `infra/`:

```
infra/
  template/            ← was deck_core/template   (build chrome)
  assets/              ← was deck_core/assets
  ooxml_reference/
    ooxml_cheat_sheet_pptx.md   ← was deck_core/
    ooxml_cheat_sheet_xlsx.md   ← was workbook_core/
    schema/                     ← was deck_core/_schema
    openxml_docs/               ← was deck_core/_docs
    prompt.txt                  ← was deck_core/
```

Probes flattened to the core top level to match the reference set:
`deck_core/tools/slide_probe.py` → `deck_core/slide_probe.py`,
`workbook_core/tools/sheet_probe.py` → `workbook_core/sheet_probe.py`; the `tools/` packages
removed. `_build_element_urls.py`'s `primitives.py` path was repointed to `deck_core/`.

## 3. Single generalized `README.md`

New top-level `README.md` covers **both** pipelines and **any** project (overview, layout, how a
project plugs into a core, the 4 build/validate commands, authoring model, locked-core rule).
Deleted `README.txt`, `deck_core/README_deck_core.txt`, and the byte-identical `deck_core/readme.txt`.

## 4. Path-math rewiring + probe fixes

After `projects/` everything is one level deeper:

- Each core-resolving `__init__.py` (4): `_CORE_DIR` `parents[3]` → `parents[4]`; `_PROJECT_ROOT`
  (`parents[1]`) unchanged.
- Each `lib.py` (4): `OUT` → project dir (`parents[2]`); deck `TEMPLATE`/`ASSETS` → `infra/`
  (`parents[4]/infra/...`); workbook `EXTRACTED` stays in `workbook/`.
- `validate_workbook.py`: fixed `OUT` filename (was a non-existent legacy name) — `parent.parent`
  now correctly resolves to the project root where the xlsx lands.
- **Functional probe fixes** from the `tools/` flatten:
  - `slide_probe.py`: `_CORE_ROOT` `parents[2]` → `parents[1]` (was a real break — it pointed
    above the workspace).
  - `sheet_probe.py`: added the `sys.path` bootstrap it never had, so it now runs as a direct
    script (parity with `slide_probe`).

## 5. Deletions / standardization

- Deleted the scratch draft-preview pipeline: `build_draft.py`, `draft_slides/`, the DRAFT preview
  `.pptx`.
- Deleted dead, singular-named `deck_submarines/submarine_market_primer.py` (not imported).
- Swept stale prose (comments/docstrings only): old `core/` layout, `deck_sub`/`workbook_sub`
  names, wrong `Output:` lines, moved-reference-file pointers (now under `infra/ooxml_reference/`),
  `tools/*probe` locations. Probe CLI `default_package` defaults updated `deck_sub`/`workbook_sub`
  → `deck_ddg`/`workbook_ddg` (the old defaults named nonexistent packages).
- Removed stray `.DS_Store` files.

## 6. Output filenames → `_vS`

The deck outputs already ended `_vS.pptx`; the **workbook** outputs ended `_v1.0.xlsx`. Renamed
both `OUT` filenames to `_vS.xlsx` (+ `build_workbook.py` docstrings, `validate_workbook.py`, README
examples), rebuilt, removed the stale `_v1.0` artifacts. Historical `_v1.0` mentions in `logs/`
were left untouched. Final outputs:

```
projects/ddg/20260602_Distributed Shipbuilding DDG_vS.pptx
projects/ddg/20260601_Distributed Shipbuilding DDG_vS.xlsx
projects/submarines/20260602_Distributed Shipbuilding Submarines_vS.pptx
projects/submarines/20260601_Distributed Shipbuilding Submarines_vS.xlsx
```

## 7. Appendix slide-module renames

Using each deck's `slides/__init__.py` registry (both have explicit appendix markers) as the source
of truth, the appendix slide modules were prefixed `appendix_`:

- **DDG (6):** `definitions_scope`, `tam_calculation`, `myp_correction`, `ap_lltm_sensitivity`,
  `ffata_limitations`, `bucket_rules_supplier_evidence`.
- **Submarines (9):** the A1–A9 set (`definitions_and_scope`, `model_map_and_figure_register`,
  `ap_and_lltm_detail`, `coefficient_sensitivity`, `sam_bucket_crosswalk`, `top_25_visible_suppliers`,
  `data_limitations_and_unseen_layer`, `sib_exclusion_detail`, `qa_reconciliation`).

Both registries' import blocks + `SLIDE_RENDERS` tuples updated. No inter-slide imports existed, so
only the registries referenced these names. Body slide `ap_and_lltm` (vs appendix `ap_and_lltm_detail`)
correctly stayed unprefixed. Slide counts unchanged (DDG 16, Submarines 25).

## 8. Slide specs → co-located `slide_specs/` (+ `sheet_specs/` infra)

Source: `../d2/ddg_slides` and `../d2/submarine_slides` (detailed plain-text wireframes). Confirmed
these were byte-identical to the old `projects/<proj>/docs/specs/slides/` for DDG, and a superset for
submarines (the d2 set adds the `enhanced_appendix_*` specs the docs copy lacked) — so the d2 set is
canonical and the docs copies were pure duplication.

- Imported into co-located `projects/<proj>/deck/slide_specs/`, each file renamed **1:1 to its module
  stem** as `.md` (ordering prefixes dropped — order lives in the registry, like the modules; appendix
  → `appendix_*`; `_optional` dropped; `bucket_rules` → `bucket_rules_supplier_evidence`; the stale
  submarines `a1–a10` numbering resolved by matching module stems).
- Verified alignment: **every content module has exactly one matching spec.** Only the submarines
  cover + 4 dividers have no spec (structural — expected).
- Deleted the old `projects/<proj>/docs/specs/slides/` (kept `submarines/docs/specs/deck_spec.txt` +
  `docs/logs/`; DDG's `docs/` held nothing else and was removed).
- Stood up empty `projects/<proj>/workbook/sheet_specs/` as equivalent infra (no sheet specs exist yet).
- README layout + a short descriptive note updated for `slide_specs/` / `sheet_specs/` — deliberately
  **no** rule that specs must track the registry.

**Design-only specs kept** (specced but never built as modules), as the backlog:
- DDG (5): `implications`, `market_direction`, `sam_scenarios`, `supplier_landscape`, `ffata_visibility_gap`.
- Submarines (6): `work_type_taxonomy`, `bucket_tam`, `sam_scenarios`, `visible_suppliers`,
  `sib_exclusion`, `appendix_basic_construction_backup`.

---

## Final top-level layout

```
ooxml_build_pipelines_light/
  README.md
  deck_core/        workbook_core/        ← code-only engines (+ guides + probe)
  infra/            template/ assets/ ooxml_reference/
  projects/
    ddg/         <pptx> <xlsx>  deck/(deck_ddg/, slide_specs/)  workbook/(workbook_ddg/, extracted/, sheet_specs/)
    submarines/  <pptx> <xlsx>  deck/(deck_submarines/, slide_specs/)  workbook/(…, sheet_specs/)  docs/(deck_spec.txt, logs/)
  docs/  logs/      ← shared workspace history
```

## Verification

All four builds re-run green at the final state:

| Build | Result |
|---|---|
| ddg deck | exit 0 — 16 slides, 7 charts → `projects/ddg/…_vS.pptx` |
| ddg workbook | exit 0 — 24 sheets → `projects/ddg/…_vS.xlsx` |
| submarines deck | exit 0 — 25 slides, 5 charts → `projects/submarines/…_vS.pptx` |
| submarines workbook | exit 0 — 21 sheets → `projects/submarines/…_vS.xlsx` |

Both probes run as direct scripts (file-mode end-to-end checked). Stale-reference greps clean
(`deck_sub`/`workbook_sub`, old `core/` layout, `parents[3]`, `tools/*probe`, deleted spec paths).

## Open items / follow-ups

- **Submarines `slides/__init__.py` docstring** — tidied: the stale `draft_slides/` + `build_draft.py`
  reference now points at the deck's `slide_specs/` (where the un-promoted S12–S16 section is specced),
  and the opening "A1-A10 appendix" was corrected to "A1-A9" (A3 was removed). The "KNOWN GAP" prose
  (Divider 3 omitted, `divider_sam_supplier` insert point) remains accurate.
- **`../d2/` source folders** (`ddg_slides`, `submarine_slides`) are now imported but still exist
  outside the workspace as the staging area; left untouched.
- **Design-only specs** retained as backlog (see §8). If `slide_specs/` should mirror only active
  modules, the 11 listed can be dropped (originals remain in `../d2/`).
- **`sheet_specs/`** are empty placeholders awaiting hand-authored sheet specs.
