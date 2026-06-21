# 2026-06-11 — Competable-work methodology: DDG parity pull, coverage to ~97%, scorecard + target list (phases A–E)

## Goal

Execute the handoff (`projects/consolidated/handoff_competability_methodology_20260611.md`):
within the sized outsourced Basic Construction pool for submarines and DDG-51,
identify which work types are realistically competable for a new entrant and
which incumbent awards are the targets. Five signals per work type (pool size,
concentration, new-entrant rate, cadence & churn, barrier & seeding) computed
per vendor from the SAM.gov FSRS full-history subaward corpora, rolled to the
existing seven-bucket taxonomy. Phase F (filling the v2 flow slide's `$##B`
placeholders) deliberately gated on user review of the findings memo.

## Setup discoveries (before any pull)

- **Two SAM.gov API keys exist.** The newer entity-role key (`SAM-e57b…`,
  1,000 calls/day) lives in `/Users/brendantoole/projects2/distributed_shipbuilding/.env`
  — the file also carries the NEWSAPI/RAPIDAPI keys the ddg scripts use, and
  was modified the night of the successful May submarine full-history pull.
  The older `SAM-106a…` key (in `army_rdte/.env`, `maritime_range…/.env`) is
  the rate-limited one. Copied the newer key to a new repo-root `.env`; all
  new scripts read it there with `os.environ` override.
- **The copied research scripts still hardcode dead projects2 paths**
  (`submarine_outsourced_work`, `destroyer_outsourced_work` are gone). Never
  run them unfixed.

## Phase A — DDG full-history parity (the 6-hour pull that took 24 seconds)

- New `projects/ddg/research/scripts/pull_sam_subawards_fullhistory.py` —
  port of the submarines script, seeded with the 24 shipbuilder-directed
  PIIDs (GD-BIW 17 + HII-Ingalls 7 from `nc_scope_summary.json`; GFE primes
  deliberately excluded per handoff decision 3, appendable later via the
  skip-if-file-exists resume logic).
- **The submarines original lacks the IPv4 `socket.getaddrinfo` monkeypatch**
  (the ddg windowed `pull_sam_subawards.py` has it). That's the whole story
  of the May pull's ~6-hour runtime: macOS urllib tries IPv6 first and stalls
  ~225s/call. With the patch, pages return in 0.1–0.2s; the full 24-PIID
  pull (6,380 published records, $3.6B raw, 2008→today) finished in 0.4 min.
- New `validate_fullhistory_pull.py`. First version failed 4 PIIDs on a
  count-based reconciliation — which exposed an API semantic worth keeping:
  **SAM.gov `fromDate`/`toDate` filter on the FILING date (`submittedDate`),
  not `subAwardDate`** — windowed pulls legitimately contain pre-window
  action dates. Rewrote the check as set-coverage (every windowed
  `subAwardReportId` must appear in fullhistory published ∪ deleted): all 24
  pass, zero duplicate report IDs, zero truly-missing records.
- Full history recovered big pre-FY18 tails: DDG-125 (N0002413C2307)
  903 → 2,304 records. 11 PIIDs legitimately empty (pre-FSRS closeouts;
  N0002423C2305 = BIW FY23 construction still zero — FFATA lag, a floors
  caveat carried through the memo).

## Phase B — classification coverage 12.0%/19.5% → 3.7%/3.2% unbucketed

New cross-program working area `projects/consolidated/research/{scripts,extracted}/`.

- `_corpus.py` — shared loader: loads `_taxonomy.py` via importlib (leaf
  module, no package import), inlines the `_registry.py` parser, replicates
  `data_entity_master.classified_records()` precedence exactly (registry by
  entity UEI then parent UEI → `classify(vendor, naics4)` ladder →
  foreign-flag special case), dedupes on `subAwardReportId`, FY by
  `subAwardDate`. Reads the fullhistory JSONs directly (the workbooks'
  `nc_records_long.csv` predates the fullhistory pulls — windowed basis).
- `measure_classification_coverage.py` → `coverage_by_bucket.csv` +
  `coverage_unclassified_top.csv` (the work queue). Baseline unbucketed
  supplier dollars FY22–25: subs 12.0%, ddg 19.5%.
- `extend_entity_lookups.py` — 282 new SAM Entity API lookups (curl
  subprocess pattern, entity UEI first, parent fallback), cached into each
  program's `sam_entity_lookups/`, appended to the **research-side**
  `entity_naics_lookup.csv` only (workbook copies deliberately untouched —
  open item). NAICS enrichment alone: subs → 8.2%, ddg → 6.1%.
- Registry extension: 17 firms / 36 UEIs adjudicated with web evidence
  (`propose_registry_additions.py` worksheet → `merge_registry_additions.py`
  appends with vocabulary validation + one-time `.bak`). Highlights:
  Goodrich EPP → coatings (sonar-dome elastomers), Hansome → **hvac** not
  electrical (the EB flow is Virginia-class vane-axial fans, $31M NTE award),
  Hiller → piping (shipboard fire-suppression fluid systems), W&O → piping,
  Cleveland-Cliffs → structural (HY plate). Three UEIs hit "already in
  registry" — all prior `residual/low-confidence` placeholders; the merge
  script upgrades exactly that class in place (prior basis preserved in
  notes), never real adjudications. Registry 137 → 169 rows; all three
  workbooks rebuild green.
- Left unbucketed on purpose: L3Harris (taxonomy pins it), ESI Acquisition
  (machinery wholesaler, work type unidentifiable), HTP Meds, SGL Automation,
  J.F. Lehman (PE parent, operating entity unidentified).
- Final coverage: **subs 3.7% / ddg 3.2% unbucketed** (target was ≤10%).

## Phase C — signals + the two honesty fixes

`compute_competability_signals.py` → `vendor_signal_table.csv` (1,411
vendors), `worktype_scorecard.csv`, `entrant_cohorts.csv`. Pools tie to
coverage to the dollar (subs $4,177M / ddg $1,573M FY22–25 supplier).

Two artifacts had to be engineered out of the entrant signal:

1. **Left-censoring**: per-lane `pre_fy22_record_share` diagnostic — thin
   pre-window history means "first award FY22–25" can't be dated.
2. **Reporting onsets / renames**: GE "enters" DDG machining FY22 at $333M;
   Timken Gears & Services is Philadelphia Gear renamed (2014 acquisition) —
   the FPDS novation trap, FSRS edition. Added
   `ENTRANT_CREDIBILITY_CAP_M = 25.0`: first-reporters above $25M window
   dollars count as `reported-entrant (likely incumbent)`, and the scorecard
   carries a separate `credible_entrant_rate` the gates use. Disclosed cost:
   it mislabels Austal USA, the marquee REAL entry ($88M of sub modules
   since FY22) — status labels are a screen, not a verdict.

**BWXT validation recast and passed.** The handoff expected churn "in the VPM
tube PIIDs N0002410C2118 / N0002416C2111" — unobservable: N0002410C2118
predates FSRS (zero records). Vendor level tells the whole story: BWXT $342M
2016 → Dec 2021 then silence (incl. a −$1.0M FY21 de-obligation), with
Babcock Marine Rosyth (UK) entering 2019–21 as the second-sourced fabricator.
Both sit outside the supplier scorecard by intended role (gfe_sib /
foreign_fms) — `validate_bwxt_churn.py` asserts the mechanics and the roles.

## Phases D + E — overlay, gates, targets, memo

- `barrier_scores.csv` (8 lanes, cert regimes + rationale) and
  `seeding_evidence.csv` (8 cited items: castings "kink in the garden hose",
  $605M FY24 supplemental, BFA CNC recruiting, HII CEO 30% quotes from
  `exec_commentary_makebuy.csv`, etc.) join into the scorecard as signal 5.
- `build_target_list.py` gates lanes with explicit ordered rules
  (COMPETABLE: HHI<0.15 or credible-entrant>3% in an unconcentrated lane;
  SEEDED: barrier-5 + active seeding; COMPONENT-TIER: top tier locked,
  component tier moving; concentrated lanes never read plain COMPETABLE off
  the entrant arm alone). → `target_list.csv`, 113 ranked vendors across 12
  gated lanes, PIIDs per row = the named competable awards.
- Gate readings: subs structural/piping/machining/coatings COMPETABLE,
  castings SEEDED (Scot Forge 74%, zero exits), electrical COMPONENT-TIER
  (NG turbine generators 67% of $1.7B), hvac LOCKED. DDG piping/structural/
  electrical COMPETABLE, castings SEEDED, hvac COMPONENT-TIER (JCI 81%),
  machining LOCKED (MRG country), coatings COMPONENT-TIER (tiny pool).
- Named churn targets: Globe Composite ($54M subs coatings, silent since
  2023-11), Air & Liquid Systems ($13.5M ddg piping, silent since 2024-10).
- Findings memo for the user discussion:
  `projects/consolidated/findings_competability_scorecard.md` (scorecard
  table, headline reads, caveats, open items).

## State / open items (memo §5)

- Phase F (slide `$##B` fill) NOT done — gated on user review. Key open
  choice: lanes carry raw FSRS floors vs deck TAM allocated by corpus shares
  (recommended the latter, matches the deck's work-type chart idiom).
- Gate thresholds are explicit constants; re-run takes seconds.
- Workbook `extracted/entity_naics_lookup.csv` copies not yet synced with
  the 282 new lookups (would further improve Entity Master coverage).
- Registry backup: `vendor_evidence_registry_pre_competability.csv.bak`.

## Files

New: `projects/ddg/research/scripts/pull_sam_subawards_fullhistory.py`,
`…/validate_fullhistory_pull.py`, `projects/ddg/research/sam_subawards_fullhistory/`
(24 JSONs + `_summary/_progress/_validation`),
`projects/consolidated/research/scripts/{_corpus,measure_classification_coverage,extend_entity_lookups,propose_registry_additions,merge_registry_additions,compute_competability_signals,validate_bwxt_churn,build_target_list}.py`,
`projects/consolidated/research/extracted/{coverage_by_bucket,coverage_unclassified_top,registry_additions_worksheet,vendor_signal_table,worktype_scorecard,entrant_cohorts,barrier_scores,seeding_evidence,target_list}.csv`,
`projects/consolidated/findings_competability_scorecard.md`, repo-root `.env`.
Modified: `projects/research_shared/supplier_bucketing/vendor_evidence_registry.csv`
(137→169 rows + 3 in-place upgrades),
`projects/{submarines,ddg}/research/extracted/entity_naics_lookup.csv` (+141 rows each),
`projects/{submarines,ddg}/research/sam_entity_lookups/` (+282 cache files).
