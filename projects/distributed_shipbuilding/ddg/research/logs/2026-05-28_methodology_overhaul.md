# Session Log — destroyer_outsourced_work — 2026-05-28 (methodology overhaul)

**Handoff doc for the next AI agent.** This session diagnosed the destroyer project
against the (newly hardened) submarine methodology, fixed the headline framing,
built the cost funnel as data, integrated the FPDS recovery, cleaned three classes
of scope contamination, and produced the full doc set for a deck overhaul
(`METHODOLOGY.md` → `WORKBOOK_SPEC.md` → `DECK_SPEC_v3.md`).

Read prior logs for pipeline detail:
1. `logs/2026-05-24_session.md` (FPDS/SAM/USAspending pulls + capped-recovery launch)
2. `logs/2026-05-24_dod_announcement_pipeline.md` (DoD POP + the MYP-redaction discovery)
3. `logs/2026-05-24_wiki_ddg_build.md` (16-chapter wiki)
4. `logs/2026-05-25_*` (deck build sessions)
5. This file

**Origin note.** The methodology approach was hardened on the *submarine* project
first this session (a reviewer critique exposed the "visible-subaward-only" framing
gap; we wrote `submarine_outsourced_work/METHODOLOGY.md`). This session ported that
discipline to the destroyer project. The destroyer wiki had already solved the hard
problems conceptually — the work here was making the fixes real in the data, the
docs, and the headline.

---

## 1. TL;DR — the one thing that matters

**Stop headlining "~87% outsourced."** It is a *redaction artifact*: the
outside-yards place-of-performance on the *disclosed-only* DoD corpus, computed with
the FY23-27 MYP master dollars redacted out (so it over-weights GFE, which is
inherently ~100% supplier-performed). The three honest numbers, which must travel
together wherever POP appears:

| Number | What it is | Use |
|---|---|---|
| ~87% | disclosed-corpus outside-yards POP (MYP masters redacted) | **do NOT headline** |
| ~33% | outside-yards POP with the ~$14.58B MYP masters folded back in | geographic lens |
| ~78% | % of total ship cost outsourced (GFE + yard-side) | **the funnel headline** |

The deck, workbook, and README now lead with the **cost funnel**, not the 87%.

---

## 2. What was done (six work items)

### A. `METHODOLOGY.md` (new) — destroyer source of truth
Mirrors the submarine `METHODOLOGY.md`. Codifies: the two-yard competitive structure
(no invisible teaming — an advantage over subs), the **MYP-redaction caveat as a
first-class headline guardrail** (§2a), the four-denominator discipline (§3), the
funnel spine (§4), the WPN/OPN weapons exclusion (§8), the segment-revenue
triangulation for the yard-side band (§9), and a consolidated guardrails list (§12).
Status-tagged [Implemented]/[Planned]/[Guardrail].

### B. `README.md` headline (fixed)
Retired the "~87% outsourced" lead. Now leads with the funnel (~78% of ship cost,
GFE-dominated), reports ~33% outside-yards (MYP-corrected) as the geographic lens, and
explicitly marks 87% as disclosed-corpus-only / redaction-biased.

### C. Cost funnel built as data (new `scripts/build_cost_funnel.py`)
Destroyer analogue of the sub funnel builder. Reads `scn_li_cost_categories.csv`
(single-vintage FY27 PB), decomposes per FY (Total → Plans/GFE/Other → Basic
Construction → outsourced band 35/42/50% of BC), and joins FFATA-visible **split by
yard** (BIW vs Ingalls construction PIIDs, DDG-1000 excluded). Outputs
`extracted/cost_funnel_{summary,per_class}.csv`.

**Validated:** FY24 categories sum exactly to the $5,492.3M Total; yard FFATA-visible
averages ~$296M/yr across FY17–25 — consistent with `outsourcing_assumptions.md`'s
~$286M/yr; GFE (Elec+Ord) runs ~33–42% of total (a lower bound — LM2500 not broken out).

**Carry these caveats** (documented in the script + METHODOLOGY §4): single-vintage
(not multi-vintage reconciled like subs); **HM&E missing in the FY16–FY23 block**;
**FY26 base reads anomalously low** (AP-shifted).

### D. FPDS recovery integrated (`aggregate_annual_outsourcing.py` edited)
The `fpds_raw_v2/` capped-recovery (BIW 30,236 records; RR 3,562) had completed but
was never consumed. Pointed the FPDS aggregator at **both** `fpds_raw` + `fpds_raw_v2`
(dedup by (piid,mod,signed_date) unions them). First run produced
`extracted/fpds_annual_by_prime.csv`: de-capped **BIW prime obligations ≈ $13,574.9M**,
Rolls-Royce ≈ $4,896.3M. The FY23-27 MYP master `N0002423C2305` shows **$5,027.5M**,
matching wiki ch12.

**Key judgment — no subaward re-pull fired.** Checked the de-capped top BIW DDG PIIDs
against the in-scope set: every high-$ DDG-51 construction PIID is *already in scope*;
the only newly-visible ones are correctly out-of-scope (DDG-1000, DDG(X), FFG(X),
ceiling-holders). So the recovery's value was completing the BIW prime-obligation
*total*, not expanding the subaward universe. No network pull needed.

### E. Scope contamination cleaned (3 aggregators edited)
Found **three** contaminant classes in the 89-PIID in-scope set (not just IVECO):
- **IVECO** `M6785416C0006` — Marine Corps (MARCORSYSCOM) Mk110 gun; phantom $707M vendor.
- **DDG-1000 Zumwalt** (6 PIIDs) — out of class.
- **WPN/OPN weapons** (9 PIIDs: ESSM ×4, CIWS ×5) — different appropriation; double-counts.
  Includes `N0002415C5420`, the Thales $4.2B artifact PIID.

Defined all 16 in `OUT_OF_SCOPE_PIIDS` in `aggregate_new_construction.py` (single
source of truth, with per-PIID reasons), enforced there, and imported into
`aggregate_sam_subawards.py` + `aggregate_annual_outsourcing.py`. Re-ran all three.

**Impact:** in-scope subawards **$13,836.7M → $11,201.9M**; records 22,235 → 15,720;
unique parent UEIs **1,954 → 1,554**. IVECO gone from `sam_subaward_top_parents.csv`;
the top-vendor list now reads as real DDG suppliers (DRS, Maine Machine, Rolls-Royce
Marine, GE, Johnson Controls, Timken, Major Tool). Raw pulls untouched on disk —
only the aggregations exclude.

### F. Doc set for the deck overhaul (new)
- **`DECK_SPEC_v3.md`** — overhaul spec replacing `deck_v2/`. ~13-slide arc
  (Cover → funnel-first Exec answer → Frame[scope/denominators/funnel] →
  Size[GFE/POP-with-correction/FFATA/hidden-yard/two-yard] → Outlook[direction/where-to-play]
  → Method). Cardinal guardrails baked in. Maps each slide to a methodology section +
  data artifact.
- **`WORKBOOK_SPEC.md`** — 13-sheet plan (sub's 12 pattern + DDG swaps: LLTM_AP→Production,
  MIB_Excluded→Scope_Excluded, +FPDS_Primes). `Inputs`→`Funnel` ripple; `DoD_POP` carries
  the 87→33→78 reconciliation in cells. **Workbook itself not built yet.**

### G. Transfer package
`/Users/brendantoole/projects2/destroyer_outsourced_work_transfer.tar.gz` (**88M**,
self-contained: symlinks dereferenced so budget_books + DoD cache are real files;
`.env` excluded). Rebuilt twice as new docs landed. **Point-in-time snapshot — rebuild
after any further edits before uploading.**

---

## 3. Files created / modified

**Created:** `METHODOLOGY.md`, `DECK_SPEC_v3.md`, `WORKBOOK_SPEC.md`,
`scripts/build_cost_funnel.py`, `extracted/cost_funnel_summary.csv`,
`extracted/cost_funnel_per_class.csv`, this log.

**Modified:** `README.md` (headline), `scripts/aggregate_new_construction.py`
(OUT_OF_SCOPE_PIIDS + enforcement), `scripts/aggregate_sam_subawards.py` (import +
skip), `scripts/aggregate_annual_outsourcing.py` (fpds_raw_v2 + exclusion).

**Regenerated by re-running aggregators:** `extracted/nc_annual_by_piid.csv`,
`nc_annual_by_vendor.csv`, `nc_lifetime_vendors.csv`, `nc_records_long.csv`,
`nc_scope_summary.json` (all cleaned), `sam_subaward_*.csv` (cleaned),
`fpds_annual_by_prime.csv` (new, de-capped), `subaward_annual_by_prime.csv`,
`subaward_top_recipients.csv`.

**Untouched:** all raw pulls (`sam_subawards/`, `usaspending_subawards/`, `fpds_raw/`,
`fpds_raw_v2/`, transcripts, `edgar_research/`), `.env`, `deck_v2/`, `deck/`, `wiki_ddg/`.

---

## 4. Things to NOT do

- **Don't headline the ~87% figure.** It's a redaction artifact. Lead with the funnel
  (~78% of ship cost); show 87/33/78 together wherever POP appears.
- **Don't re-add the 16 contaminants.** They live in `OUT_OF_SCOPE_PIIDS`
  (`aggregate_new_construction.py`, single source of truth). The ESSM/CIWS are WPN/OPN
  (different appropriation); DDG-1000 is out of class; IVECO is Marine Corps.
- **Don't re-pull subawards for the FPDS recovery.** Confirmed no new in-scope DDG
  PIIDs surfaced; a re-pull would burn API time for nothing.
- **Don't treat the funnel as fully reconciled.** Single-vintage; HM&E blank pre-FY24;
  FY26 base AP-shifted. These are [Planned] fixes, not done.
- **Don't forget to rebuild the transfer tarball** after edits — it's a snapshot.
- **Don't edit `deck_v2/` slides as the overhaul** — `DECK_SPEC_v3.md` is the plan;
  the new deck should be built fresh from it (engine in `deck_v2/` is reusable).

---

## 5. Open items / next steps (in order of value)

1. **Build the workbook** from `WORKBOOK_SPEC.md` (copy sub's `lib.py`/`styles.py`,
   author the 13 sheets). This is the numeric layer the deck needs.
2. **Refresh stale figures in the wiki + `outsourcing_assumptions.md`.** They still
   cite the pre-cleanup **$13.8B / 89 PIIDs / 1,954 UEIs**; current is **$11.2B / 73
   PIIDs / 1,554 UEIs**. `wiki_ddg/01-scope-and-funnel-framework.md` is the main one.
3. **Fix `deck_v2/slides/dod_pop.py` (and `deck/slides/s05_dod_pop.py`)** — they still
   visually anchor on a 72pt "~87%". Pair with the ~33% corrected number, or re-anchor.
4. **SCN multi-vintage reconciliation + HM&E backfill** (METHODOLOGY §4 [Planned]) —
   re-extract earlier PB vintages so the funnel isn't single-vintage with the HM&E gap.
5. **Build the deck** from `DECK_SPEC_v3.md` (needs #1 first, plus the client capability
   profile for the slide-11 addressability heat map).

---

## 6. Quick orientation for next agent

- **"What's the outsourcing number?"** → the funnel: ~78% of total ship cost (GFE +
  yard-side); FFATA-visible is the ~15% floor of the yard-side piece (~$296M/yr avg vs
  ~$1.8B/yr modeled). NOT 87% (that's geography on a redacted corpus → ~33% corrected).
- **"Where's the method?"** → `METHODOLOGY.md` (don't re-derive; it cross-refs `wiki_ddg/`).
- **"Where's the funnel data?"** → `extracted/cost_funnel_summary.csv` (built by
  `scripts/build_cost_funnel.py`).
- **"Why did the in-scope total drop?"** → 16 contaminants removed (IVECO + DDG-1000 +
  WPN/OPN weapons); audit trail in `OUT_OF_SCOPE_PIIDS` + (planned) the workbook's
  Scope_Excluded sheet.
- **"Is BIW data complete now?"** → yes, `fpds_annual_by_prime.csv` reads the de-capped
  `fpds_raw_v2`; BIW ≈ $13.57B prime obligations.
- **"What's the deck plan?"** → `DECK_SPEC_v3.md`. **Workbook plan?** → `WORKBOOK_SPEC.md`.
  Neither the new deck nor the workbook is built yet.
- **"Where's the transfer package?"** →
  `/Users/brendantoole/projects2/destroyer_outsourced_work_transfer.tar.gz` (88M;
  rebuild after edits).

## 7. Memory
No cross-session memory entries written for the destroyer project this session — all
context is in this log + the three spec docs. (The submarine project's memory was
updated separately with its own METHODOLOGY.md pointer.)
