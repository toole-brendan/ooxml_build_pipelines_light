# Findings — Competable-Work Scorecard (for discussion)

**Date:** 2026-06-11
**Status:** Phases A–E of the handoff executed; slide fill-in (Phase F) gated on this review.
**Artifacts:** `research/extracted/` — `worktype_scorecard.csv`, `vendor_signal_table.csv` (1,411 vendors), `target_list.csv` (113 targets), `entrant_cohorts.csv`, `coverage_by_bucket.csv`, `barrier_scores.csv`, `seeding_evidence.csv`, `window_sensitivity_comparison.csv` (+ `sensitivity_fy20_25/`, `sensitivity_fy19_25/`), `class_cut_scorecard.csv` / `vendor_class_matrix.csv` / `piid_profile.csv` (class & builder cuts). Scripts in `research/scripts/`.

---

## 1. What was built

- **DDG full-history parity (Phase A).** New `projects/ddg/research/sam_subawards_fullhistory/` — all 24 shipbuilder-directed PIIDs (GD-BIW 17 + HII-Ingalls 7), 2008→today, 6,380 published records, $3.6B raw. Validated: zero duplicate `subAwardReportId`s; every windowed-corpus record present (set-coverage). The pull took **24 seconds** — the old 6-hour submarine pull was an IPv6 stall the new script avoids. Full history recovered large pre-FY18 tails (DDG-125: 903 → 2,304 records).
- **Classification coverage (Phase B).** 282 new SAM entity NAICS lookups + 17 firms (36 UEIs) adjudicated into the shared registry (137 → 169 rows; 3 prior low-confidence `residual` placeholders upgraded with evidence — Goodrich EPP→coatings, Hansome→hvac, Hiller→piping). Unbucketed supplier dollars FY22–25: **submarines 12.0% → 3.7%, DDG 19.5% → 3.2%** (target was ≤10%). All three workbooks still build green; registry backup at `vendor_evidence_registry_pre_competability.csv.bak`.
- **Signals 1–4 (Phase C)** computed per vendor and rolled to work types; **barrier & seeding overlay (Phase D)** hand-scored with cited evidence; **target list (Phase E)** gated and ranked.

The corpus basis is **reported first-tier subawards (FSRS floors), FY22–25 by action date**: submarines $4,177M / DDG $1,573M of supplier-addressable dollars. This is *not* the deck's $24.5B outsourced-BC TAM (budget × coefficient); see open item 3.

## 2. The scorecard

| Lane | Pool FY22–25 | Vendors | HHI | Top-1 | Credible entrants | Exits | Cadence | Barrier | **Gate** |
|---|---|---|---|---|---|---|---|---|---|
| **Subs structural** | $794M | 46 | 0.09 | 18% | 13 | 14 | 34d | 3 | **COMPETABLE** |
| **Subs piping** | $798M | 77 | 0.10 | 25% | 29 | 27 | 31d | 4 | **COMPETABLE** |
| **Subs machining** | $138M | 29 | 0.11 | 22% | 15 | 7 | 47d | 3 | **COMPETABLE** |
| **Subs coatings** | $281M | 12 | 0.22 | 35% | 3 | 5 | 52d | 2 | **COMPETABLE** |
| Subs castings | $198M | 9 | 0.56 | 74% | 4 | 0 | 51d | 5 | SEEDED |
| Subs electrical | $1,708M | 28 | 0.52 | 67% | 16 | 10 | 80d | 3 | COMPONENT-TIER |
| Subs hvac | $101M | 5 | 0.36 | 49% | 2 | 2 | 42d | 2 | LOCKED |
| **DDG piping** | $231M | 55 | 0.05 | 8% | 27 | 24 | 65d | 4 | **COMPETABLE** |
| **DDG structural** | $179M | 44 | 0.06 | 16% | 21 | 16 | 79d | 3 | **COMPETABLE** |
| **DDG electrical** | $249M | 26 | 0.15 | 28% | 13 | 11 | 51d | 3 | **COMPETABLE** |
| DDG hvac | $221M | 13 | 0.66 | 81% | 7 | 8 | 26d | 2 | COMPONENT-TIER |
| DDG castings | $49M | 9 | 0.43 | 59% | 5 | 2 | 148d | 5 | SEEDED |
| DDG coatings | $11M | 5 | 0.42 | 60% | 1 | 2 | 92d | 2 | COMPONENT-TIER |
| DDG machining | $585M | 13 | 0.42 | 57% | 2 | 4 | 72d | 3 | LOCKED |

Gates: **COMPETABLE** = HHI < 0.15, or credible entrant flow > 3% of lane dollars in an unconcentrated lane. **SEEDED** = locked incumbents but barrier-5 lanes under active Navy/BFA seeding (castings: "the kink in the garden hose", $605M FY24 supplemental for supplier development) — long qualification path, not a closed door. **COMPONENT-TIER** = top tier locked (NG turbine-generators at 67% of subs electrical; JCI at 81% of DDG hvac) but the component tier shows real entry. **LOCKED** = DDG machining is main-reduction-gear country (Timken/Philadelphia Gear, GE, Rolls-Royce); subs hvac is a 5-vendor lane with no entry.

## 3. Headline reads

1. **Structural fabrication and piping/fluid handling are the entry lanes, on both programs.** Fragmented (HHI ≤ 0.10), fast re-buy cadence (~monthly), heavy two-way churn, and the biggest competable pools ($1.6B subs, $410M DDG over FY22–25).
2. **The marquee proof of entry is Austal USA**: first submarine-module subawards FY22, $88M by FY25 — third-largest vendor in subs structural within three years. (The signal table's $25M credibility cap auto-labels it "reported-entrant"; it is in fact the known real entry — see caveat 2.)
3. **Named churn targets exist.** Globe Composite ($54M FY22–25, subs coatings) silent since Nov 2023; Air & Liquid Systems ($13.5M, DDG piping) silent since Oct 2024; Lake Shore Systems' deck-machinery scope re-emerging under new entities. Each `target_list.csv` row carries the incumbent's PIIDs — the named competable awards.
4. **Castings is the seeded lane, not the open lane.** Scot Forge holds 74% of subs castings with zero exits; entry happens via Navy/BFA qualification money (Lehigh Heavy Forge and PRL both first-report FY22).
5. **BWXT validation passes, with a recast.** The handoff's PIID-level expectation is unobservable (N0002410C2118 has zero FSRS records — pre-FSRS award). At vendor level the episode is fully visible: BWXT $342M of subawards 2016 → Dec 2021, then silence (including a −$1.0M FY21 de-obligation), with Babcock Marine Rosyth (UK) appearing 2019–21 as the second-sourced tube fabricator. Both sit outside the supplier scorecard by intended role (gfe_sib / foreign_fms) — the detection mechanics work; the episode itself is Navy-directed scope.

## 3a. Class and builder cuts (added 2026-06-12)

Descriptive cuts of the same corpus — vessel class for submarines (Virginia / Columbia via the scope JSON's `class` field), builder group for DDG (single-class DDG-51, so GD-BIW vs HII-Ingalls is the analog). Gates stay program-level per the handoff's unit-of-analysis rule; these are pools / concentration / overlap only (`compute_class_cut.py` → the three CSVs above; per-cut pools reconcile to the program scorecard to the dollar).

1. **Columbia is now the larger submarine supplier pool**: $2,405M vs Virginia $1,773M FY22–25. The entry lanes hold on *both* classes — structural, piping, and machining all sit at HHI 0.10–0.14 per class — so the program-level COMPETABLE reads aren't an artifact of blending classes.
2. **Subs electrical splits sharply by class.** Virginia electrical is near-single-source (HHI 0.88, top-1 at 94% of $574M) while Columbia electrical is $1,135M at HHI 0.44 (top-1 54%). The program lane's COMPONENT-TIER read lives mostly on Columbia; Virginia's top tier is effectively closed.
3. **Columbia opened doors.** Of 551 window-active submarine supplier vendors, 234 work both classes, but **182 are Columbia-only ($246M)** vs 135 Virginia-only — Graham Corp ($82M, piping) is the headline Columbia-only name, with Caterpillar, Plainville Electrical, and General Atomics behind it. Caveat: Columbia lanes have shallower pre-window history (pre-window record shares 0.21–0.51 vs Virginia's 0.47–0.68), so class-level *entrant-rate* claims would be censoring-weak — one more reason gates stay program-level.
4. **The DDG scorecard is effectively an Ingalls-visibility scorecard.** HII-Ingalls carries $1,470M (93%) of the FY22–25 DDG supplier pool vs GD-BIW's $102M; six of seven BIW lanes are thin (<5 vendors or <$20M), and BIW's FY23 construction PIID (`N0002423C2305`) still has zero FSRS records. DDG lane reads should be voiced as "at Ingalls" where precision matters.
5. **Per-hull cuts are viable only at Ingalls.** `piid_profile.csv` (39 in-corpus PIIDs) shows 17 with zero FSRS records. The hull-readable PIIDs: DDG 128 (`N0002418C2307`, $372M window), the FY23 construction award (`N0002423C2307`, $1,070M — carries the GE machining reporting onset), DDG 125 (`N0002413C2307`, robust history but only $28M window — winding down). For submarines the PIID cut collapses into the class cut: the two master contracts hold ~85% of all records.

## 4. Assumptions and caveats (documented in code)

1. **Entrant left-censoring.** "First-ever award" is dated within each program's FSRS corpus (subs usable from ~2016, DDG ~2013 but thin). A vendor first *reported* in FY22 may be a long-time supplier newly reported. Mitigations: the $25M credibility cap (GE "entering" DDG machining at $333M is a reporting onset; Timken Gears & Services is Philadelphia Gear renamed) and a pre-FY22 history-depth check per lane.
2. **The cap cuts both ways.** It mislabels Austal USA (real entry, large dollars) as "reported-entrant". Status labels in `target_list.csv` are a screen, not a verdict — top targets deserve the qualitative check the handoff prescribed.
3. **Exit = last award ≥18 months before corpus end** (subs corpus ends 2025-10, DDG 2026-05) with ≥2 lifetime awards. FFATA lag (6–18 months) means recent "exits" can be reporting lag.
4. **Levels are floors.** FSRS undercounts; `N0002423C2305` (BIW FY23 DDG) still has zero subaward records. Structure signals (concentration, entry, cadence) are the load-bearing reads, per the handoff.
5. **Full-history basis ≠ deck basis.** The deck's work-type chart derives from the older windowed corpus; this analysis re-pulled full history, so per-lane dollars differ slightly (upward). Goodrich's $62M moving into subs coatings (my registry adjudication) is the largest single classification change vs the deck's mix.
6. **Window sensitivity (added 2026-06-12).** The FY22–25 window was inherited from the deck, so the gates were re-run at FY20–25 and FY19–25 (`COMP_WINDOW`/`COMP_OUTDIR` overrides; outputs in `sensitivity_fy20_25/`, `sensitivity_fy19_25/`; per-lane grid in `window_sensitivity_comparison.csv` via `compare_window_sensitivity.py`). **13 of 14 lane gates are unchanged across all three windows.** The one mover is DDG castings — SEEDED at FY22–25 *and* FY19–25 but COMPETABLE at FY20–25, where lane HHI lands at 0.296, a hair under the 0.30 cutoff that lets the entrant arm fire (HHI is 0.43 / 0.34 in the other two windows). The non-monotonic flip is a threshold artifact, not a market-structure change: the lane carries barrier 5 with active seeding in every window, so SEEDED is the robust reading. Note also that widening the window backward *weakens* the entrant signal rather than strengthening it — first-award censoring needs deep pre-window history, and 54–58% of corpus records sit pre-FY22 today. FY22–25 stays the headline basis.

## 5. Open items for discussion

1. **Gate thresholds** (HHI 0.15/0.30, credible-entrant 3%, $25M cap, 18-month exit window) are explicit constants in `build_target_list.py` / `compute_competability_signals.py` — adjust and re-run takes seconds. The window-sensitivity check (caveat 6) shows the only gate that moves under a ±3-year window change is DDG castings, and only via the HHI 0.30 cutoff.
2. **Subs electrical framing.** $1.7B pool reads COMPONENT-TIER because NG turbine-generators dominate; if the deck should treat the NG scope as effectively Navy-locked (like GFE), the lane could be split rather than gated whole.
3. **Phase F slide numbers.** The v2 flow slide's lane `$##B` placeholders can carry (a) raw FSRS floor dollars (defensible, smaller, basis-consistent with this memo) or (b) the deck's outsourced-BC TAM allocated by corpus lane shares (consistent with the deck's existing work-type chart idiom). Recommend (b) for the deck, with the floors kept in the workbook; your call before I fill the slide.
4. **Program-workbook refresh.** The registry additions slightly improve the live workbooks' bucket coverage (they rebuild green). The workbook `extracted/entity_naics_lookup.csv` copies were deliberately *not* refreshed with the 282 new lookups — say the word and I'll sync them so Entity Master picks up the new NAICS enrichment too.
