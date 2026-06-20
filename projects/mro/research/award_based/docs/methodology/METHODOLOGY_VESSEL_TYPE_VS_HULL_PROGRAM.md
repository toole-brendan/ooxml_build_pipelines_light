# Methodology: Why the Hull Program Tables Show More Unclassified Dollars Than the Vessel Type Table

**Purpose**: explain the apparent inconsistency between the "Vessel Type" (supergroup) cross-tab at the top of the Services sheet and the "Hull Program" cross-tabs that follow it. A reviewer looking at the Services sheet will see ~1.9% Unclassified in the Vessel Type view and ~30% Unclassified in the Hull Program view. This is by design, not a bug.

---

## What you'll see in the workbook

As of v2.48, Navy Services TAM is $6.79B. The three cross-tabs display:

| Table | "Unclassified" column $ | As % of TAM |
|---|---:|---:|
| U.S. Navy + Coast Guard by Vessel Type (combined) | $128M | ~1.9% |
| U.S. Navy by Hull Program | ~$1,900M + $128M | ~29.8% |
| U.S. Coast Guard by Hull Program | ~$31M | ~11.5% |

The Vessel Type table looks nearly fully classified. The Hull Program tables look like they've lost a third of the dollars to "Unclassified." A first-time reviewer will reasonably ask: "Where did the $1.9B go between those two tables?"

It didn't go anywhere. It's classified — just not down to the level of specificity that a Hull Program column requires.

---

## How the classification cascade assigns rows

Every row in the `Awards By Hull` data sheet has two classification fields driving the Services sheet cross-tabs:

- `vessel_supergroup` — broad category like "Surface Combatants", "Submarines", "Aircraft Carriers", "Amphibious Warfare Ships". 15 possible values, per the Vessel Taxonomy sheet.
- `hull_program` — specific hull family like "DDG", "CVN", "SSN", "SSBN", "LPD", "LCS". Approximately 30-50 possible values across Navy + CG.

The `vessel_supergroup` is always a rollup of `hull_program` — e.g., DDG + CG + FFG + LCS + Zumwalt all roll up to "Surface Combatants."

The classification cascade runs through six tiers per FPDS mod, in priority order:

| Tier | Name | What it sets |
|---|---|---|
| -1 | FPDS MOD 0 SOW override + LLM override | Varies - often supergroup only |
| 0 | Wikipedia proper-name lookup (USS / USNS / CGC names) | Both (class known -> hull known) |
| 0b | Hull-number regex (DDG 75, CVN 78, etc.) | Both |
| 0c | DoD Acquisition Program (DAP) lookup | Both |
| 1, 2 | VESSEL_DESC_PATTERNS regex on mod / IDV | Both (class known -> hull known) |
| 3, 4 | SUPERGROUP_DESC_PATTERNS regex on mod / IDV | **Supergroup only** |
| 5 | Recipient prior (contractor-specific) | **Supergroup only** |

Tiers 3, 4, and 5 can only ever set the supergroup. That's not a limitation we could code around - it's the nature of the evidence. If a mod description says "LCS EMERGENT MAINTENANCE" with no hull number, we know it's a Surface Combatant but not whether it's USS Freedom LCS-1 or USS Cincinnati LCS-20 or USS Minneapolis-St. Paul LCS-21. Forcing a specific hull assignment would be fabrication.

---

## How the cross-tabs render

Both cross-tabs use SUMIFS formulas against the `AwardsByHull` Excel table.

**Vessel Type cross-tab**:
```
=SUMIFS(AwardsByHull[FY2025 Obligation], AwardsByHull[PSC], "J998", AwardsByHull[Vessel Type], "Surface Combatants")
```
This sums any row whose `vessel_supergroup` is populated with "Surface Combatants", regardless of whether `hull_program` is filled in. A Tier 3 / 4 / 5 row with only supergroup classification shows up here.

**Hull Program cross-tab**:
```
=SUMIFS(AwardsByHull[FY2025 Obligation], AwardsByHull[PSC], "J998", AwardsByHull[Hull Program], "DDG")
```
This sums only rows whose `hull_program` is exactly "DDG". A Tier 3 / 4 / 5 row with empty `hull_program` does not match any specific-hull column and falls into the Hull Program cross-tab's "Unclassified" column.

Different filters, same underlying data. The Hull Program view is a stricter filter.

---

## Breakdown of the "missing" $1.9B (Navy Services)

Where the $1.9B that shows up in Vessel Type but rolls to Unclassified in Hull Program actually comes from:

| Cascade tier | $M | Description |
|---|---:|---|
| `residual_override` (LLM + FPDS MOD 0) | $1,100 | LLM classified to supergroup without claiming a specific vessel class |
| `supergroup_idv` (Tier 4) | $308 | IDV description regex matched a supergroup keyword (e.g. "SURFACE COMBATANT", "CVN") without naming a hull |
| `supergroup_mod` (Tier 3) | $289 | Per-mod description regex matched a supergroup keyword without naming a hull |
| `recipient_prior` (Tier 5) | $202 | Contractor's vessel-type specialization (e.g. Bath Iron Works -> Surface Combatants, Electric Boat -> Submarines) |
| **TOTAL** | **$1,899** | |

Every dollar in this $1.9B has a defensible supergroup attribution. None of it has strong enough evidence to identify a specific hull family.

---

## Why the LLM layer is the biggest contributor ($1.1B)

The LLM classifier (`llm_classify_residual.py`) evaluates the top-N residual PIIDs that survive all the regex/name/hull/DAP/recipient tiers. For each PIID it reads the base-award SOW, parent IDV description, deduped top-25 mod descriptions, recipient, PSC, and DAP; then returns a classification with `supergroup`, optional `vessel_class`, and confidence.

Of the 403 LLM overrides currently in play, **only 10 have `vessel_class` populated**. The remaining 393 return supergroup-only. This is not an LLM error - the prompt explicitly instructs:

> vessel_class values must match the taxonomy labels in the examples ("DDG-51 Arleigh Burke", "CVN-68/78 Carrier", "Virginia (SSN-774)", ...). If you can't match one of these, leave vessel_class null.

The LLM is being conservative by design. If a PIID's SOW says "SWFTS submarine combat systems support," the model correctly answers `supergroup=Submarines, vessel_class=null` - because it genuinely cannot tell whether the Virginia-class, Los Angeles-class, or Columbia-class submarines are being supported. Forcing it to guess a specific class would move money into a hull column where it doesn't belong.

---

## Why this is the right methodology

The alternative would be to either:

1. **Dishonestly attribute supergroup-only rows to an arbitrary hull class.** E.g., assign all "Submarines" residual to Virginia-class because Virginia is the most common. This would contaminate the Hull Program view with fake precision.

2. **Exclude supergroup-only rows from the TAM entirely.** This would understate the TAM by ~$1.9B on the Navy side - most of which is legitimate ship MRO work whose hull specificity just can't be recovered from the available text.

The current approach keeps the work in the TAM, credits it to the right supergroup, and is transparent about the limit of what we can say. The Vessel Type cross-tab is the apples-to-apples market-size view across service branches and PSC families. The Hull Program cross-tab is the more granular view that naturally shows honest uncertainty when we can't get below the supergroup level.

---

## Reconciliation guidance for readers

If you're presenting this model to an audience that asks "why is there so much unclassified in the Hull Program tables but not the Vessel Type table?" - here is the response:

> The Vessel Type view rolls dollars to 15 broad ship categories. The Hull Program views roll to ~30-50 specific hull families. Every dollar in Vessel Type has a supergroup attribution. Not every dollar has a specific hull - roughly 28% of Navy Services dollars are classified to supergroup only (we can tell it's a Surface Combatant but not which class, because the contract text doesn't name one). The Vessel Type view is the market-sizing view; the Hull Program view surfaces that residual uncertainty honestly rather than hiding it. Both views use the same source data; they differ only in the strictness of the filter.

This framing makes the cross-tabs defensible to a technically literate buy-side audience: the model doesn't pretend to have hull-level specificity it doesn't have, and the $1.9B difference is not "missing" dollars - it's disclosed uncertainty.

---

## Possible enhancement: LLM hull-family field

The conservatism described above is a workable floor. It is possible to push the Hull Program classification rate up without losing honesty by extending the LLM output schema:

- Add a new output field `hull_program` distinct from `vessel_class`. The LLM can set `hull_program = "SSN"` when it can tell submarine-family but can't pick between Virginia / Los Angeles / Seawolf. Same idea for `hull_program = "DDG"` when it sees Aegis signal without a class indicator, or `hull_program = "CVN"` when it sees carrier work without a Nimitz/Ford flag.
- Update the prompt to give the LLM permission to commit to a hull family when it's confident - even if not to a class.
- Re-run on the top ~100 residual PIIDs. Cost: ~$0.40. Expected lift: convert maybe $300-600M of the $1.1B LLM residual_override supergroup-only into Hull Program attribution.

This would reduce the Hull Program "Unclassified" column to a range closer to 10-15% without inventing specificity the underlying text doesn't support. The trade-off is that the LLM now has a middle tier of confidence it can express, which requires more prompt-engineering care to avoid drift.

Not implemented as of v2.48 - current methodology is the conservative floor described above. Revisit if a deeper Hull Program breakout becomes required for investor / buy-side conversations.

---

## Sources and precedents

- `data_pull/vessel_explode_v2.py` - classification cascade source of truth
- `data_pull/llm_classify_residual.py` - LLM classifier, current prompt, output schema
- `sheets/services.py` - Services sheet cross-tab layout
- `sheets/product_procurement.py::_write_crosstab` - SUMIFS formula construction
- `SESSION_2026-04-16_iii_llm_override_guide.md` - original LLM layer design and trade-offs
- `METHODOLOGY_CVN_SSN_COVERAGE.md` - adjacent methodology note on public-yard labor outside the TAM
