# Open Question: How much of PSC 1905 is actually MRO?

**Status:** Partial answer in workbook (Sub & Carrier Coverage sheet) as a range with residual uncertainty. Single defensible number still requires an additional data pull + classification pass.

## The question

PSC 1905 is the federal Product Service Code for **"Combat Ships and Landing Vessels"** — i.e., the shipbuilding PSC. FY2025 Navy + USCG obligations on PSC 1905 are `$38.1B` across 201 PIIDs. On its face, this is all newbuild: Columbia SSBN construction, Virginia SSN construction, CVN-80/81, DDG-51 Flight III, Constellation FFG, etc.

**But a non-trivial slice is actually MRO.** NAVSEA's Supervisor of Shipbuilding, Conversion, and Repair (SUPSHIP) administers **both construction AND major overhaul work at the same builder yards — Electric Boat, HII Newport News, HII Ingalls — under one PSC set.** So an Engineered Overhaul of a Los Angeles-class submarine at Newport News is coded PSC 1905 (shipbuilding), not J998 (non-nuclear ship repair), even though it's unambiguously depot maintenance work.

**The question this session is trying to answer:**

> For FY2025 PSC 1905 obligations (`$38.1B` Navy + USCG), what dollar amount is actually MRO/depot work bundled under the shipbuilding PSC — and how does that split across submarines vs. aircraft carriers vs. other platforms?

## Why this matters for the project

The project sizes **U.S. Navy + Coast Guard MRO TAM/SAM** as its core deliverable. The current workbook's Services MRO TAM is `$7,067M` (post-exclusion, FY25), built bottom-up from 68 J/K/N/M/H/L services PSCs. That `$7.07B` explicitly does **not** include any PSC 1905 dollars because PSC 1905 is classified as newbuild (Product Procurement sheet).

**If we don't account for the embedded MRO in PSC 1905, we structurally undercount the addressable market for submarine and carrier maintenance:**

| Platform | Services TAM (current) | + PSC 1905 Embedded MRO | Complete FPDS picture |
|---|---:|---:|---:|
| Submarines | `~$838M` | `+ $1,255M` | `~$2.1B` (2.5x uplift) |
| Aircraft Carriers | `~$422M` | `+ $319M` | `~$741M` (1.8x uplift) |

*Figures from [specs/psc_1905_mro_share.md](specs/psc_1905_mro_share.md) Central bound.*

Undercounting submarine MRO by a factor of 2.5x is a material error for any investor or strategic read of the market. The embedded `$1.5-2.0B` of PSC 1905 MRO is the single largest source of systematic undercounting in the current TAM methodology.

This is also independent of the **public naval shipyard labor** undercount (Portsmouth / Puget Sound / Pearl Harbor, funded through NWCF reimbursement, `~$3-4B` outside FPDS entirely). That's a separate issue already partially addressed via Budget Anchors.

## Current state of the answer

[specs/psc_1905_mro_share.md](specs/psc_1905_mro_share.md) applied a 3-tier heuristic cascade (keyword matching + POP-length tiebreaker + newbuild-hull override) across the 201 PSC 1905 PIIDs and produced a **range**:

| Bound | Method | $M |
|---|---|---:|
| Conservative | Strong MRO keyword only | `$1,565M` |
| Central | Strong + soft-keyword + short POP | `$1,660M` |
| Upper | + POP-only (no keyword) | `$1,949M` |

This is now reproducible in the workbook — [build_script/psc_1905_classifier.py](build_script/psc_1905_classifier.py) + new "Embedded MRO inside PSC 1905" section on Sub & Carrier Coverage. Our build matches the spec within ~1-2%: `$1,553M / $1,647M / $1,912M`. Top PIIDs correctly identified: Electric Boat Seam Split Repairs `$831M`, USS Boise SSN-764 Engineered Overhaul `$424M`.

**Why bounds and not a single number:** the classifier is heuristic. Some PSC 1905 PIIDs are genuinely ambiguous (admin modifications on newbuild base contracts that fund emergent repair work, hull-treatment material procurements that could be either construction or repair, etc.). The `$150-400M` gap between Conservative and Upper is the real residual uncertainty of keyword-based classification.

**Residual uncertainty:** roughly `±$150-200M` on the Central estimate.

## Likely path to a single defensible answer

The single-number answer exists — it just requires signals that aren't in the current Awards pipeline. Path in increasing confidence / increasing effort:

### Path 1: TAS-based classification (best signal-for-effort)

The upstream pipeline already has `data_pull/output/fpds/approp_rollup_imputed.json` — this maps FPDS PIIDs to Treasury Account Symbols (TAS), which in turn map to specific budget line items. A PSC 1905 PIID funded from:

- **SCN LI 2086 "CVN Refueling Overhauls"** → definitively MRO (carrier RCOH)
- **SCN LI 1045 Columbia Class** → definitively Newbuild
- **SCN LI 2013 Virginia Class** → definitively Newbuild (construction funding)
- **OMN SAG 1B4B Ship Maintenance** → definitively MRO
- **OPN BA-01 LI 1000 CNO availabilities** → definitively MRO

For any PIID with a **direct TAS attribution** (not imputed), this is gold-standard classification — independent of contract description keywords. Referenced in [specs/METHODOLOGY_AVAILABILITY_FUNDING_APPROPRIATIONS.md](specs/METHODOLOGY_AVAILABILITY_FUNDING_APPROPRIATIONS.md).

**Effort:** Pull `approp_rollup_imputed.json` from the other machine; join to the PSC 1905 PIID list; flag each PIID by its TAS → line item → MRO/Newbuild. Probably classifies 60-80% of dollars cleanly.

### Path 2: Mod-level LLM review (for residual)

The current `data/base_data.xlsx` collapses all mods of a PIID into a single description string, so a PIID with 10 mods — some clearly "FY25 RCOH Phase 2 growth work" and some "administrative funding action" — gets flattened to one description (typically the base-award text). The richness at **mod level** is lost downstream.

The raw FPDS JSONs on the other machine (`navy_awards_master.json`, `cg_awards_master.json`) preserve per-mod descriptions, per-mod obligations, and `base_award_description` separately. For the ambiguous PSC 1905 PIIDs that TAS doesn't cleanly classify, re-exploding to mod level and classifying each mod individually (via LLM, using the same infrastructure as [build_script/sheets/services.py](build_script/sheets/services.py)'s `llm_exclusions.json` pipeline) captures the MRO/newbuild intent mod-by-mod.

**Effort:** Copy raw JSONs; explode ~200 PSC 1905 PIIDs to probably ~1,000-2,000 mods; run LLM over mod descriptions; aggregate dollars by mod classification. Couple hundred mods × one LLM call = minutes of compute. Pipeline is already mostly built; needs a new harness + prompt.

### Path 3: Manual review (fallback / validation)

201 PIIDs is small enough to human-review in 2-3 hours. Sort by $M descending, read each description + parent IDV description + hull program, classify MRO / Newbuild / Ambiguous. Not scalable to future years but definitive for FY25. Useful as validation layer over the LLM pass.

### Recommended sequence

1. **TAS-first pass** (Path 1) — lands most of the `$38.1B` in known buckets cleanly. 1-2 hours once JSONs are on this machine.
2. **Mod-level LLM pass** (Path 2) for residual `$2-5B` that TAS doesn't cleanly classify. 1 day of work.
3. **Reconcile** — TAS answer should match LLM answer for dollars where both fire; differences get flagged for human review (Path 3 as spot-check).

End result: a single defensible "`PSC 1905 embedded MRO = $X.XM`" number per vessel supergroup, derived from independent methods, ready to fold into the Services TAM as an additive correction.

## What's blocking it right now

Three JSON files from the other machine:

- `data_pull/output/fpds/navy_awards_master.json`
- `data_pull/output/fpds/cg_awards_master.json`
- `data_pull/output/fpds/approp_rollup_imputed.json`

Once those arrive at `data_pull/output/fpds/` on this machine, the work is mostly infrastructure extension, not new research.

## Related artifacts in this session

- [build_script/psc_1905_classifier.py](build_script/psc_1905_classifier.py) — 3-tier cascade, ready to extend with TAS / mod-level signals
- [build_script/sheets/sub_carrier_coverage.py](build_script/sheets/sub_carrier_coverage.py) — new "Embedded MRO inside PSC 1905" section (bounds, supergroup share, top PIIDs, bucket census)
- [specs/psc_1905_mro_share.md](specs/psc_1905_mro_share.md) — source methodology
- [logs/2026-04-21_psc_1905_embedded_mro_section.md](logs/2026-04-21_psc_1905_embedded_mro_section.md) — session log for the workbook work
- Current workbook output: `build_script/output/08APR2028_Newbuild_and_MRO_Spend_v3.13.xlsx` (built + warmed this session)
