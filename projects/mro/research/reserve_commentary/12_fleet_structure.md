# Slide 12 — Fleet Structure / Marauder-Like Comp-Set (module: `fleet_structure.py`)

> Breadcrumb: SAM › Fleet Structure · tier-roster table + criteria callout · `_chart_xml/slide12_table.xml` + `slide12.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Marauder-like comp-set spans **14 hull programs** across **3 mission-fit tiers**
  and anchors the SAM vessel universe inside TAM."
- **Caption:** "FY2025 Marauder-Like Comp-Set by Mission-Fit Tier ($M)."
- **Tier roster:**
  | Tier | Hulls | FY25 $M |
  |---|---|---:|
  | 1 — Combat Logistics & MSC | T-AKE, T-AO, T-EPF, ESB, T-ESB, T-AK, T-AKR, T-ESD | **$715M** |
  | 2 — Amphibious connectors | LSM, T-LSM, LCU | **$0M** |
  | 3 — USCG size-class | FRC, WPC, WLB | **$43M** |
  | **Comp-set total** | **14 hull programs across 3 tiers** | **$758M** |
- Tier-1 role text: "Containerized logistics and at-sea payload hosting mirror Marauder's
  **180-foot ASV with 150MT modular deck**. MSC-operated scheduled availabilities book under
  J998/J999." Segment mix: **Depot 82%, Port & Technical 14%, HM&E 4%**, Combat/Electronics/
  Nuclear near 0%.
- **Inclusion criteria callout:** Availability pipeline = MSC scheduled ROH / mid-term
  availabilities at MSRA yards (not NAVSEA combatant overhauls); Crewing = civilian mariners,
  commercial-style sustainment (parallel to Marauder's ASV concept); Yard pool = pierside and
  MSRA yards (not the four public shipyards).
- **Note:** "Tier 2 FY2025 total is $0M because LSM, T-LSM, and LCU programs are early in the
  procurement cycle and not yet material in obligations." Source: FPDS FY2025 obligations, MSC
  fleet disposition, USCG Cutter Fleet inventory, Marauder ASV design envelope.

## Claim-by-claim sourcing

| Claim | Source |
|---|---|
| 14-hull comp-set (the exact set) | `workbook_mro/sheets/taxonomy_mro.py` `target_hull` scenario hull list |
| Comp-set total **$758M**; tier totals $715M / $0M / $43M | `model_sam_build.py` `target_hull` SAM via SUMPRODUCT over TAM atoms |
| "Marauder = 180-ft ASV, 150MT modular deck" | Saronic Marauder design envelope (deck source line) |
| Selection logic (MSC auxiliaries / MSRA yards) | `research/psc1905/TARGET_deck_structure.md`; `sam_methodology.md`; memory `tam-sam-methodology` |

- The 14 hulls = Tier 1 (8): T-AKE, T-AO, T-EPF, ESB, T-ESB, T-AK, T-AKR, T-ESD · Tier 2 (3):
  LSM, T-LSM, LCU · Tier 3 (3): FRC, WPC, WLB. This is the `target_hull` atom-flag set in the
  workbook's SAM engine (see memory `mro-sam-atom-engine`).

## Reserve facts (could be added)

- **The comp-set is forward-looking.** Today's $758M is concentrated in **Tier 1 ($715M)**;
  Tier 2 ($0M) is the *future* contested-littoral connector fleet (LSM/T-LSM/LCU still early in
  procurement), and Tier 3 ($43M) is just **WPC + WLB** (the only USCG cutters with material
  FY25 MRO spend, slide 13). The thesis: the addressable set grows as Tier 2 matures.
- **Why these hulls and not DDG/SSN:** the addressability test is structural — MSC-operated,
  civilian-crewed auxiliaries that book scheduled ROH / mid-term availabilities at **MSRA yards
  under J998/J999**, *not* NAVSEA combatant overhauls at the four public shipyards. That mirrors
  Marauder's commercial-style sustainment model.
- **$758M = 8% of the $8,971M TAM** (slide 14); the depot subset of it (**$623M**) is the SAM.
- Segment mix (Depot 82% / Port & Tech 14% / HM&E 4%) is the slide-13 breakdown in one line.

## Quotable stats & attributions

- "Marauder-like comp-set = **14 hull programs**, **3 tiers**, **$758M** FY2025 MRO — 8% of the
  $9B TAM." (deck, slide 12)
- "Comp-set hulls mirror Marauder's **180-ft / 150MT** profile and book availabilities at MSRA
  yards, not the four public shipyards." (deck)
- "**WPC and WLB are the only USCG cutters with material FY2025 MRO spend** ($43M)." (deck)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations; (2) MSC fleet disposition; (3) USCG Cutter Fleet inventory; (4) Marauder ASV design envelope

## Caveats / confidence / staleness flags

- **Confidence: high** on the dollar totals ($758M / $715M / $43M, from the SAM build);
  the **comp-set definition itself is an analyst judgment** (Marauder design envelope), not an
  official Navy taxonomy — the inclusion criteria are stated on-slide for defensibility.
- `[!]` **Tier 2 = $0M** — the comp-set deliberately includes programs with no FY25 spend yet
  (LSM/T-LSM/LCU). Don't read $758M as the ceiling; it's today's realized slice of a growing set.
- `[!]` Minor internal cross-ref: the note says "See slide 11 for per-hull split," but the
  per-hull Marimekko is **slide 13**. Slide-number callouts in the notes are approximate.
- PSC 1905 embedded MRO does **not** touch this comp-set (no MSC auxiliaries / USCG cutters in
  the embedded set) — so the $1,904M reconciliation has no effect here.
</content>
