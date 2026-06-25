# Capability Domain shares are real but contract-concentrated — read before quoting them

**One-line caveat:** Several of the largest Capability Domain (D) shares in the
`award_classification_refactor` workbook are driven by **one or two contracts**, not a broad
field of suppliers. The shares are correct; they are just concentrated. Never quote a domain %
as "the supplier base" without naming what's inside it.

Scope of these figures: **hull-builder-only** universe (subs = GDEB Basic Construction; GFE
primes excluded), **post-MECE** D taxonomy, **nominal** dollars. As of 2026-06-20.

> **2026-06-21 UPDATE — several recommendations below are now DONE; some numbers here are stale.**
> Path 3 (complete the EB denominator) executed: **N00024-20-C-2120 "Lead Yard Support" added to
> scope** (Virginia new construction, verified by DoD announcement + place-of-performance), adding
> 670 subs / $1,018M and **recovering the ~$14M EB→HII subaward slice** this doc predicted (7 recs /
> $14.37M — the HII re-test over the *completed* EB prime set confirms this doc's forensics; HII is
> still structurally absent at scale). **Virginia headline figures shifted:** D2 Propulsion is now
> **37% / $2,280M (NG 73%)**, not the 40.2% / $2,053M below (denominator grew). Paths 1–2 + 5
> (reframe, derived memo, CRS cite) and the concentration axis are now built into the workbook as the
> **Domain Concentration** sheet (live size×contestability "where to play" view) and the **HII
> Co-Build Workshare** sheet (issuer-disclosed ledger incl. Block V ≈ $10.2B). Also fixed: the SAM
> subaward API `piid` casing flipped to UPPERCASE (see `SAM_GOV_HOWTO.md`). Full detail:
> `sam/logs/2026-06-21_eb_denominator_completion_and_where_to_play_layer.md`.

---

## The headline

| Program | Domain | Share | What's actually inside it |
|---|---|--:|---|
| **Virginia** | **D2 Propulsion** | **40.2% ($2,053M)** | Northrop Grumman $1,471M (72%) + BAE Land & Armaments $333M (16%) + Scot Forge $176M (9%) — **top 3 = 96% of the domain** |
| **Columbia** | **D6 Mission/Combat** | **24.5% ($922M)** | Northrop Grumman (CMC missile-compartment launcher) $530M (58%) + Babcock Marine Rosyth $241M + Rosyth Royal Dockyard $84M — **top 2 = 84%** |
| **Columbia** | **D2 Propulsion** | **18.6% ($702M)** | DRS Naval Power ~$439M (63%, across two UEIs) + Scot Forge $177M — **top 2 = 83%** |
| **DDG** | **D2 Propulsion** | **30.4% ($1,094M)** | Rolls-Royce $460M + GE $333M + Timken $169M — top 2 = 72% (more spread, but still 3 firms) |
| **DDG** | **D5 Thermal/HVAC** | **15.6% ($564M)** | York $192M + Johnson Controls $180M — top 2 = 66% (an HVAC duopoly) |

**Virginia's "propulsion" is essentially the Northrop Grumman electric-drive contract.** One
UEI (`LCV2N9FVV739`, $1.47B) is 72% of the largest domain in the largest submarine program — and
it only became D2 in the 2026-06-20 MECE pass (it was previously buried in D0). Quoting "Virginia
propulsion = 40%" without that context overstates the breadth of the propulsion supplier base.

## Why this is real, not an artifact

These are genuine, large, single contracts — the concentration is a true property of submarine/
destroyer outsourcing, not a classification error:

- Submarine **electric propulsion and power** is a sole-/few-source area (NG/DRS) — consistent
  with the CRS finding that ~70% of critical submarine suppliers are sole-source.
- The Columbia **D6** mass is the Common Missile Compartment launcher (NG) plus the UK Rosyth
  CMC work (shared US/UK Columbia–Dreadnought build) — a handful of named programs, by design.
- DDG **D2/D5** reflect the LM2500/propulsor (Rolls-Royce, GE, Timken) and the HVAC duopoly
  (York, Johnson Controls) the two shipyards actually buy from.

So the right framing is *"this domain is dominated by these named primes,"* not *"this is a deep
competitive field."*

## How to quote a domain share responsibly

1. **Pair the % with its top 1–2 firms.** "Virginia D2 is 40%, but 72% of that is one NG
   contract" is honest; "Virginia D2 is 40%" alone is misleading.
2. **Distinguish breadth from magnitude.** A high share with top-2 ≥ ~80% is a *concentration*
   signal (few suppliers), not a *broad-base* signal. Low-concentration domains (e.g. Virginia
   D4 Fluid/piping, top-2 = 36%; Columbia D4, top-2 = 28%; DDG D4, top-2 = 16%) are the genuinely
   broad supplier fields.
3. **Watch the D2 inflation from the MECE pass.** Pushing forged-shaft firms (Scot Forge, Erie)
   into D2 deliberately concentrated D2 further; that was the right call for classification but
   compounds the single-contract dominance above.

## The deeper caveat: the largest co-builder (HII Newport News) is absent from this universe entirely

Concentration is the *second*-order problem. The first-order problem is that the single
largest construction participant on both submarine programs — **HII Newport News Shipbuilding**,
the Navy-designated co-builder — is **almost entirely missing from the subaward population these
shares are computed over.** Established 2026-06-21 via a nine-method investigation (below); the
result is not a search error.

**What the public award data actually contains for HII NNS on these programs:**

| Program | HII in the FSRS/SAM subaward universe | True HII role (CRS) |
|---|--:|---|
| **Virginia** | **~$75–90M** — three EB purchase orders (`SND034=058` ~$44.9M on N0002417C2100; `SNC179=014` ~$18.6M on N0002416C2111; ~$14M on N0002420C2120) + ~$0.3M of Newport News Nuclear GFE/property items | **~50% co-builder** — fabricates/outfits major hull modules, joins pressure-hull sections, delivers assigned boats |
| **Columbia** | **$0.00** — no HII record on either Columbia prime | **~22–23%** — stern, bow, habitability/aux-machinery, torpedo room, command-and-control modules |

So the reported HII footprint is **well under $100M on Virginia and exactly zero on Columbia**,
against a true co-build workshare that runs to **tens of billions** across the in-scope boats.

**Why it's missing (mechanism — revised 2026-06-21).** The build runs under a Navy-directed
**teaming / co-production arrangement** with GDEB as sole prime, and the original prime
announcements name HII Newport News as the *major subcontractor* (Block V) and co-designer
(Columbia) — so the workshare unambiguously exists contractually. **Be careful not to overstate the
explanation, though:** a teaming agreement does not by itself make those subcontracts
non-reportable. HII *itself* describes these as **contracts and subcontract modifications received
from Electric Boat**, and FAR 52.204-10 defines a first-tier subcontract broadly and normally
requires the amount, date, description, subcontract number, and prime PIID to be reported (it
permits Contracting-Officer direction and excludes classified information, but a teaming structure
alone is not a stated exemption). The honest characterization is an **unexplained reporting /
data-treatment gap — not proof that no reportable subcontract existed.** What *is* certain is that
the gap is real and systemic: on the **same Columbia prime (N0002417C2117)** where HII is absent,
EB reports **$7.75B** of subawards (BlueForge $1.5B+, Northrop Grumman, DRS Naval Power, Precision
Custom Components, UK Rosyth) — EB reports subs *diligently*; only the HII workshare is missing.

**Nine methods, one conclusion.** (1) SAM/FSRS raw scan of 17 sub primes incl. the **deleted**
arrays — 1 deleted record total, not HII; (2) USAspending cross-prime subaward search by
recipient; (3) USAspending direct-prime by primary UEI; (4) direct-prime by the other HII UEIs;
(5)+(6) FPDS vendor-name sweeps ("Newport News Shipbuilding" and pre-2011 "Northrop Grumman
Shipbuilding") + Navy + dollar floor; (7) FPDS PIID-direct description checks; (8) **recipient-
agnostic FPDS NAICS-336611 megaprime sweep — every submarine construction megaprime since 2012
belongs to Electric Boat; HII holds only carriers, DDG-51s, and amphibs**; (9) SAM Entity API
enumeration of all six HII registrations (incl. a previously-unsearched `P3FPNF7WGWL8` → 0 awards,
0 subs). HII's *direct* Navy work is carriers ($51.8B) + submarine **maintenance/overhaul** ($4.2B,
e.g. USS Columbus EOH, USS Boise planning) — **not** Virginia/Columbia new construction.

**Consequence for every share in this workbook.** All domain (D) percentages here are
**"% of GDEB-reported first-tier subcontracted scope," not "% of total boat construction."** The
denominator omits the #1 (Virginia) / #2 (Columbia) single builder by value. This is the most
extreme form of the concentration caveat above: not merely "concentrated in a few firms," but
"the largest builder is structurally invisible." Never present a domain share as "the submarine
supplier base" without stating that the EB↔HII co-build workshare is excluded by reporting
structure.

## Recommended paths forward

1. **Reframe the shares (do first, zero new data).** Re-label every domain % as *"share of
   GDEB-reported first-tier subcontracted scope (hull-builder-only universe) — excludes the HII
   Newport News co-build workshare, which is not FFATA-reported."* One sentence; makes every
   downstream quote honest.
2. **Add a derived HII co-builder memo line.** Apply the documented CRS workshare split
   (~50% Virginia, ~22–23% Columbia) to the EB prime obligations already in the workbook to
   produce a parenthetical "co-builder workshare (not in subaward data) ≈ $X" so readers see the
   true scale. Mark it clearly as *derived*, not transactional.
3. **Complete the EB-reported denominator.** Add the EB primes the current pull is missing —
   confirmed: **N0002420C2120** ("Lead Yard Support," $4.3B, NAICS 336611, ~$14M of EB→HII subs);
   verify Block VI / AP coverage — so the reported-subaward base is at least complete *for EB*.
4. **Bound it with HII SEC 10-K segment data.** Newport News segment revenue with submarine vs.
   carrier split is the best *public, hard* quantification of HII submarine revenue; use it to
   sanity-check the path-2 estimate.
5. **Corroborate the split + structure with CRS/GAO.** O'Rourke, *Navy Virginia-Class Submarine
   Program* (RL32418) and *Columbia-Class* (R41129) document both the workshare percentages and
   the teaming arrangement; cite them for the reframing and the estimate.
6. **(Government-side only) NAVSEA FOIA / PIEE-EDA** for the workshare schedules under the
   specific PIIDs — the only place exact HII dollars exist; flag as not publicly retrievable.
7. **Methodology hygiene.** When deriving any "supplier base" share from subaward data, check for
   structurally-absent teaming partners first — the EB↔HII co-build is the canonical case. (Pull
   note: SAM Entity lookups must use `_common.py`'s IPv4 patch, query by `ueiSAM`, and cap
   `size`≤10; name searches do a full-dataset scan and hang.)

## Preferred path for headline HII numbers: an issuer-disclosed subcontract ledger

The data-forensics avenues are now **exhausted** — additional UEIs, deleted records, and
USAspending variants have all been tested and the core HII workshare is simply not in the FFATA
feed. Stop spending time there. The recoverable signal is **HII's own disclosures**, which name
actual award dollars (not CRS-derived estimates). Build a second, clearly-labeled primary-source
table from them; leave the federal transactional data untouched.

**HII-disclosed actual award amounts** (issuer announcements + SEC filings):

| Program | Date | HII-disclosed amount | How to treat it |
|---|---|---|---|
| Columbia | Dec 2017 | up to **$468M** — integrated product & process development | ceiling / "up-to"; not necessarily funded |
| Columbia | Nov 2018 | **$197M** mod — long-lead material + advance construction | mod; check if inside the 2017 ceiling |
| Columbia | Nov 2020 | ~**$2.2B** mod — design support + modules, first two boats | actual announced mod |
| Columbia | Apr 2023 | **$567.6M** subcontract mod — Build II LLTM + advance construction | actual announced mod |
| Virginia Block V | Apr 2019 | **$727.4M** mod → AP contract to **$1.04B** | action + cumulative both disclosed |
| Virginia Block V | Mar 2021 | option → **total NN contract value $9.8B** | cumulative; do **not** re-add earlier actions |
| Virginia Block V | May 2023 | **$305.2M** mod → overall value **$10.2B** | action + updated cumulative |

> **Strongest public Virginia figure: HII Newport News Block V contract value ≈ $10.2B as of
> 2023-05-24** — an actual disclosed contract value. For headline Virginia numbers, prefer this
> over the looser "~50%" CRS framing in the table above (the Block V prime announcement allocates
> ~25% place-of-performance to Newport News; the Columbia design award, 12.7%). Label each figure
> by basis — never mix them.

> **Columbia caution:** do **not** sum $468M + $197M + $2.2B + $567.6M. The 2017 amount is an
> "up-to" ceiling that later mods may exercise/overlap; HII has not publicly isolated the dollar
> value of the 2025 (boats 11–12) or Block VI AP actions. Build the Columbia ledger row-by-row with
> lineage, not by addition.

**1. Add an `issuer-disclosed subcontract awards` table** (separate from the FSRS transactional
data), with an explicit amount-basis so cumulative and incremental figures never get summed:

```
subcontractor_name · subcontractor_uei · parent_prime · parent_piid · program ·
award_announcement_date · effective_award_date · announced_action_amount ·
cumulative_contract_value · amount_basis · scope · subcontract_number ·
source_type · source_document
amount_basis ∈ { INCREMENTAL_MODIFICATION, CUMULATIVE_CONTRACT_VALUE,
                 UP_TO_CEILING, TEAM_PRIME_VALUE, AMOUNT_NOT_DISCLOSED }
```
Parent crosswalk: Virginia Block V = `N00024-17-C-2100`; Columbia design/construction begins at
`N00024-17-C-2117`.

**2. Source hierarchy for this relationship** (label HII-sourced rows as *issuer-disclosed
subcontract award data*, not FSRS transactions): (1) HII award announcement / SEC filing →
(2) NAVSEA/DoD prime-contract announcement → (3) FPDS/SAM/USAspending prime action →
(4) SAM/FSRS subaward record, when one exists.

**3. File two narrowly targeted NAVSEA FOIA requests** — one each for `N00024-17-C-2100` and
`N00024-17-C-2117` (NAVSEA FOIA portal / FOIA.gov). Request, for any GDEB→HII (UEI
`WMXDDH6HJNA5`) subcontract or modification: subcontract number, initial award + modification
dates, per-action amount, current cumulative subcontract value, work description, and the
associated prime mod; plus, if held, consent-to-subcontract requests/approvals, subcontract
price-analysis summaries, and workshare / make-or-buy schedules. Explicitly disclaim classified
technical data, proprietary labor rates, detailed cost build-ups, and specifications (ask only for
segregable award-identification and dollar fields). **Add the key question:** *"any Contracting
Officer direction, determination, or correspondence concerning whether these GDEB-to-HII
subcontracts were required to be reported under FAR 52.204-10."* That last item is what may
actually explain the FFATA gap.

**4. Use PIEE/EDA where government-authorized access exists.** Search the GDEB prime PIIDs and
inspect the modification packages (esp. Sections B and J + attachments). EDA likely won't hold the
private GDEB–HII subcontract itself, but may contain pricing memoranda identifying the HII
component, negotiated workshare schedules, consent records, prime-mod attachments allocating
major-yard work, or references to the HII subcontract number.

**Practical conclusion.** For historical **Block V, use the HII-disclosed ~$10.2B cumulative
contract value**, not a CRS percentage. For Columbia and newer Virginia actions, build the public
ledger from HII disclosures and pursue NAVSEA records / EDA for the missing subcontract numbers,
modification lineage, and cumulative values. No other public federal transactional database will
expose the complete GDEB→HII ledger — the remaining exact data lives in **HII disclosures, EDA
contract files, or NAVSEA contract-administration records, not another UEI search.**

*Sources for this section: HII award announcements (hii.com newsroom) + SEC 10-K (EDGAR CIK
1501585); DoD/DoW contract announcements 2017-09-21 (Columbia design, `N00024-17-C-2117`, 12.7%
NN PoP) and 2019-12-02 (Block V, `N00024-17-C-2100`, GDEB prime / HII major subcontractor, ~25% NN
PoP); FAR 52.204-10, 15.404-3, 44.201-1 (acquisition.gov); NAVSEA FOIA; PIEE/EDA.*

## Two items to verify if these shares get published

- **BAE Systems Land & Armaments in Virginia D2 ($333M)** — confirm this entity's propulsion
  attribution; "Land & Armaments" reads more like ordnance/structures than propulsion machinery.
- **DRS Naval Power Systems appears under two UEIs** ($403M + $36M) in Columbia D2 — same firm,
  consider consolidating for any headline "top supplier" claim.

---

*Source: `award_classification_refactor.xlsx` D/P resolution (override → NAICS-6 crosswalk →
unresolved), re-cut over the hull-builder-only vendor population. See
`workbook_award_classification_refactor/logs/2026-06-20_archetype_mece_revision.md` and
`..._hull_builder_only_scope_standardization.md` for the scope and taxonomy basis.*

*2026-06-21 addition (HII co-builder absence + recommended paths forward): established by a
nine-method FPDS / USAspending / SAM investigation over the GDEB Virginia/Columbia primes,
cross-checking the published+deleted SAM subaward arrays in
`submarine_subaward_code_package/raw_json/`, recipient/UEI searches across all six HII
registrations, and a recipient-agnostic NAICS-336611 megaprime sweep. Conclusion: HII NNS
new-construction workshare is ~$75–90M (Virginia) / $0 (Columbia) in the public subaward universe
vs. a true co-build workshare in the tens of billions; the build runs under a Navy-directed
teaming/co-production arrangement with GDEB as sole prime.*

*2026-06-21 second-opinion addition (issuer-disclosed ledger path + mechanism revision): a review
flagged that a teaming agreement alone does not exempt a subcontract from FAR 52.204-10 (HII calls
these EB subcontract modifications), so the FFATA absence is reframed as an unexplained
reporting/data-treatment gap rather than a clean carve-out. Added the "issuer-disclosed subcontract
ledger" path: HII-announced/SEC award amounts (Block V cumulative ≈ $10.2B as of 2023-05-24;
itemized Columbia mods), a separate amount-basis-typed table schema, the source hierarchy, two
targeted NAVSEA FOIA requests (incl. the FAR 52.204-10 CO-direction question), and PIEE/EDA. Data
forensics (extra UEIs, deleted records, USAspending variants) declared exhausted — do not re-run.*
