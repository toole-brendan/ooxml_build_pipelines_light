# Capability Domain shares are real but contract-concentrated — read before quoting them

**One-line caveat:** Several of the largest Capability Domain (D) shares in the
`award_classification_refactor` workbook are driven by **one or two contracts**, not a broad
field of suppliers. The shares are correct; they are just concentrated. Never quote a domain %
as "the supplier base" without naming what's inside it.

Scope of these figures: **hull-builder-only** universe (subs = GDEB Basic Construction; GFE
primes excluded), **post-MECE** D taxonomy, **nominal** dollars. As of 2026-06-20.

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
