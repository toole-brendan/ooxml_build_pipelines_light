# 2026-06-22 — AP/LLTM/EOQ scope treatment audit (DDG vs submarines)

User concern: *"AP/LLTM/EOQ for DDG does not fall under Basic Construction, while for
submarines it does fall under Basic Construction PIIDs. We are interested in non-nuclear
AP/LLTM/EOQ (the $ outsourced from prime shipbuilders during new construction) — did I
treat them appropriately?"* Audit of the `award_classification_refactor` workbook scope
against the DDG and Virginia/Columbia research wikis.

## Verdict

The contracting facts in the user's intuition are **correct**, and the dollar treatment is
**substantially right** — non-nuclear AP/LLTM/EOQ *is* captured for submarines (the intent),
and DDG's analogous long-lead is *correctly* excluded as GFE. The real defects are **not**
mis-bucketed dollars; they are (1) a **scope-rule wording** that contradicts what the build
actually does, and (2) a **missing cross-program comparability caveat**. One inference is
worth a confirming check (DDG EOQ capture under the MYP PIIDs).

## Evidence

### Submarines — AP/LLTM/EOQ IS in the base, correctly
The in-scope GDEB PIIDs *are* the long-lead contracts (from `extracted/prime_awards.csv`,
USAspending award detail — descriptions far more informative than the internal labels):

| In-scope PIID | Internal label | USAspending description | FY22-25 subaward $M |
|---|---|---|---|
| `N0002417C2100` | Va Block V/VI master | **SSN 802 AND 803 LONG LEAD TIME MATERIAL** | 1,373.9 |
| `N0002412C2115` | Va Block IV MYP | **SSN 792 LONG LEAD TIME MATERIAL** | 0.0 |
| `N0002424C2110` | Va Block VI LLTM | **SSN 814 & SSN 815 LONG LEAD TIME MATERIAL** | 399.8 |
| `N0002417C2117` | Col Build I/II master | COLUMBIA CLASS DESIGN COMPLETION | 2,405.1 |

GDEB reports its non-nuclear shipbuilder-procured LLTM/EOQ subawards under these *same*
master/LLTM PIIDs, commingled with Basic Construction. Top work types on the dedicated LLTM
PIID `N0002424C2110` are piping $121.4M / electrical $103.7M — i.e. non-nuclear HM&E/outfitting
material, exactly the "shipbuilder-procured LLTM" the submarine wiki ch.5 calls the *"most
directly addressable bucket"* (~$2.0-2.5B/yr combined, growing).

Nuclear LLTM is **correctly dropped**: the `bgroup=="GDEB"` filter removes the BPMI naval-reactor
PIIDs (`N0002419C2114` Naval Reactor Components, `N0002419C2115`, `N0002424C2114` S9G).
Net: non-nuclear in, nuclear out. ✓ matches intent.

### DDG — the analogous long-lead is GFE, so it is correctly NOT in the hull-builder base
DDG wiki ch.1 GFE/CFE table is explicit: propulsion (LM2500 turbines, **main reduction gears**)
and combat systems are **GFE** — the Navy buys them on *separate* prime contracts (GE `N00019…`,
LM-Aegis, Raytheon, BAE), not from BIW/Ingalls. DDG wiki ch.2 confirms the budget structure:
P-40 carves advance procurement and EOQ out *separately* from Basic Construction/Conversion.

All DDG in-scope PIIDs are pure construction (`prime_awards.csv`): `N0002413C2305` "FY13-FY17
DDG 51 CLASS SHIP CONSTRUCTION", `N0002418C2305` "FY18-FY22…", `N0002423C2307` "…FY23-27", etc.
There is **no AP/LLTM/EOQ PIID for BIW/Ingalls** in the corpus — because DDG's big-ticket
long-lead never flows through the yard. Excluding it is the *same GFE rule* used to drop BPMI
nuclear for subs — so the two programs are treated consistently at the rule level.

Tell-tale wiki asymmetry: the submarine wiki has a dedicated ch.5 "Long-lead and advance
procurement"; the DDG wiki has **none** (ch.3 → ch.4), with MYP handled in ch.12. The DDG
program simply has no large shipbuilder-procured AP/LLTM layer to chapter.

### DDG exclusions are not mis-dropped AP/LLTM
Checked the three dollar-bearing DDG `include=N` rows in `prime_contract_scope.csv`:
`N0002419C4452` (Provisioned Items Orders = in-service spares, $24.6M), `N0002414C4313`
(PIO/de-ob, $0), `N0002419C2322` (DDG-1000 planning yard, $18.2M). None are new-construction
AP/LLTM/EOQ. Correctly excluded.

## Defects found

### 1. Scope-rule wording contradicts the build (the real "messed up")
`workbook_award_classification_refactor/.../sheets/guide_methodology.py:51`:
> *"Only Basic Construction prime contracts are included…"*

But the submarine in-scope PIIDs are titled **LONG LEAD TIME MATERIAL**, not Basic Construction.
A reader taking the sentence literally concludes AP/LLTM/EOQ was *excluded* — the opposite of
the truth. The keyword classifier `_scope_type()` in `scripts/build_prime_scope_manifest.py`
keeps those LLTM PIIDs only because "LLTM" is absent from its exclude-keyword list, so the
(correct) inclusion is **semi-accidental and fragile** — anyone who "tightens" the rule to
honor the stated wording would delete the submarine LLTM base.

### 2. DDG and submarine bases are not like-for-like; not disclosed
Subs capture a large shipbuilder-procured AP/LLTM/EOQ stream; DDG cannot (its equivalent is
GFE). Any direct DDG-vs-sub "outsourced $" / make-buy comparison tilts toward subs
**structurally, not by error**. Needs an explicit caveat.

## Confirmed — DDG EOQ rides the MYP construction PIIDs (2026-06-22, SAM Contract Awards API)
The "to confirm" inference is now **verified against the prime universe**, not just `nc_scope_summary.json`.
Method: SAM.gov Contract Awards API (`api.sam.gov/contract-awards/v1/search`), enumerated EVERY prime
award to each DDG shipbuilder by **exact awardee UEI** (the verified `awardeeUniqueEntityId` filter;
`cageCode` is not a valid param), FY2005-2026:
- **Bath Iron Works** (UEI `FREEMCLKFXE3`, CAGE 70876, parent General Dynamics): 28 base PIIDs / 11,875 mods.
- **Huntington Ingalls** (UEI `C3NLZNSMU254`, CAGE 34293): 27 base PIIDs / 10,812 mods.

**Finding: neither yard holds a separate DDG-51 advance-procurement / EOQ / LLTM prime.** Every large
DDG-51 (NAICS 336611, PSC 1905) definitive contract is a construction MYP vehicle already in scope —
BIW `N0002413C2305` / `N0002418C2305` / `N0002423C2305` ("CONSTRUCTION OF DDG 51 SHIP" / "DDG 51 CHANGES")
and Ingalls `N0002413C2307` / `N0002418C2307` / `N0002423C2307` ("CONSTRUCTION OF DDG 51 SHIP"), each flagged
`multiyearContract=YES`. Everything else is DDG-1000 (Zumwalt), LPD/LHA (Ingalls' other programs),
ship-alteration / PIO spares (`C42xx`/`C43xx`/`C44xx`), design (`C2313`/`C2318`), or ~$0 purchase orders/BOAs.

**Tell-tale that makes this conclusive:** the ONLY long-lead-labeled prime across either yard is BIW
`N0002424C2331` "**DDG 1000** PY LLTM" — a *Zumwalt* contract. When the Navy carves out a separate yard
long-lead vehicle, the description says so explicitly; DDG-51 has none, so its yard EOQ rides the MYP
construction contract. (Contrast: the submarine GDEB master/LLTM PIIDs — in scope per fix #1 — are the
case where a separate yard long-lead vehicle DOES exist.) Prior caveat stands: BIW under-reports FFATA
(FY23-27 master `N0002423C2305` has zero filings), so DDG dollar capture is effectively Ingalls-only —
but that is a reporting-compliance gap, not a missing AP contract.

**Incidental finding (cosmetic, zero dollar impact):** BIW `N0002406C2303` ($3.31B, "CONSTRUCTION", SAM
program "DDG 1000", PSC 1903) and `N0002411C2306` ($2.55B, "COSAL WAREHOUSING", "DDG 1000") are tagged
DDG-1000 by SAM yet carried in `prime_contract_scope.csv` as DDG-51 `include=Y` (new-construction-admin).
Both return **zero subawards** (already in the build's "10 include=Y zero-subaward" note), so no analysis
dollars depend on them — but they are Zumwalt contracts mislabeled DDG-51 in the manifest. Optional cleanup.

## Recommended fixes (not yet applied — dollar logic untouched, it is correct)
1. Reword the methodology scope line (and mirror to the manifest rationale +
   `CLASSIFICATION_METHODOLOGY_OVERVIEW.md`) to state honestly:
   > In-scope = hull-builder new-construction contracts, including shipbuilder-procured
   > non-nuclear long-lead/EOQ material (carried on the GDEB master/LLTM PIIDs for submarines).
   > Excluded: nuclear-reactor LLTM (BPMI), GFE/component-prime advance procurement (GE
   > propulsion, Aegis, etc.), design/lead-yard/ship-alteration/planning-yard work, and
   > MIB/BlueForge pass-throughs.
2. Add a cross-program caveat: DDG long-lead is predominantly GFE, so the DDG base captures
   less AP/LLTM than the submarine base — not a like-for-like make/buy comparison.
3. ~~(Optional) Confirm the DDG-EOQ-under-MYP inference~~ — **DONE 2026-06-22**, confirmed via SAM
   Contract Awards API prime enumeration of both yards (see "Confirmed" section above): no separate
   DDG-51 AP/EOQ prime exists; EOQ rides the MYP construction PIIDs.

## Files reviewed
- `workbook_award_classification_refactor/prime_contract_scope.csv`,
  `scripts/build_prime_scope_manifest.py`, `scripts/pull_prime_awards.py`,
  `extracted/prime_awards.csv`, `sheets/guide_methodology.py`
- `corpus/extracted/piid_profile.csv`;
  `tam/{ddg_research,virginia_columbia_research}/extracted/nc_scope_summary.json`
- Wikis: subs ch.4 (Basic Construction), ch.5 (Long-lead & AP), ch.1 (scope/funnel);
  DDG ch.1 (scope/funnel), ch.2 (cost/production), ch.12 (MYP redaction & unseen layer)
- Prior logs: `award_classification/logs/2026-06-10_worktype_shares…`,
  `workbook_…/logs/2026-06-20_hull_builder_only_scope_standardization.md`,
  `logs/2026-06-21_award_classification_style_audit_fixes.md`
