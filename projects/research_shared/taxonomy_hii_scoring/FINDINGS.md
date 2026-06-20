# Taxonomy × HII-DDG scoring — findings (2026-06-18)

Grades agent A's NAICS-6 → work-type taxonomy (`taxonomy_design_output/`) against the
HII-Ingalls DDG ground truth (observed SWBS ship-system per subaward) in the canonical
$13.1B bundle. Referee = **HII-DDG only ≈ $3.5B, one builder, one program, a *system* axis**
— used to *calibrate/validate*, never to redefine categories. Script: `score_taxonomy_vs_hii.py`.

## Coverage of the referee
- HII-DDG total **$3,547.3M**; SWBS group resolved on **$1,967.9M (55.5%)**; component text on ~37%.
- **0% join gap** — every HII vendor is in the 1,203-entity profile.

## How the NAICS map classifies HII dollars
| Outcome | $M | % of HII |
|---|--:|--:|
| Resolved to a real category by primary NAICS | 2,502.6 | **70.6%** |
| In profile but **no primary NAICS** | 884.3 | 24.9% |
| In profile, NAICS maps to **99** (weak/generic) | 160.4 | 4.5% |

The 24.9% no-primary mass is **concentrated in registry-covered vendors** — Rolls-Royce
Marine (~$439M), York International (~$192M), SOCAIL ($151M), Power Paragon, Howden — so
the registry override (agent B) resolves almost all of it. NAICS alone gets 70.6%; registry
closes most of the rest.

## System categories — SWBS agreement (share of HII$ landing on the expected ship system)
| Cat | Work type | HII$ w/SWBS | Agreement | Read |
|---|---|--:|--:|---|
| 01 | Electrical power | $235.1M | **1.00** | clean |
| 02 | Propulsion & mech. transmission | $529.7M | **0.986** | clean |
| 03 | Fluid systems / piping | $95.4M | **0.907** | clean |
| 04 | Thermal / HVAC | $259.0M | 0.669 | thermal↔fluid boundary (heat exchangers/boilers/heaters land in piping) |
| 11 | Industrial machinery / handling | $37.4M | 0.231 | small; galley/service machinery lands in HVAC |

Weighted agreement across 01–04 ≈ **0.91**. The clean trio (01/02/03 ≈ 0.98) is strong
independent validation that those NAICS→category mappings are correct.

## System categories whose home is NOT observable in HII (agreement N/A — data artifact, not a fault)
- **10 Sensors/controls ($110.5M)** — combat/C4ISR (SWBS 4xx) is GFE and excluded upstream;
  only residual ship-control/instrument work remains (e.g. Northrop Grumman submarine steering,
  SWBS 561). Do **not** read low SWBS agreement here as a taxonomy problem.
- **05 Structural ($23.1M)** — hull structure (1xx) is fabricated in-house by Ingalls;
  subcontracted structural metal shows up as foundations/tanks/uptakes coded to the system it
  serves (2xx/5xx), not 1xx.

## Process-only categories — not SWBS-gradable (they scatter across ship systems by design)
Assessed by component_text coverage + NAICS-internal purity instead:
06 forgings/castings **0.96**, 14 engineering 0.75, 13 shipyard 0.74, 07 machining 0.69,
15 install/repair 0.62, 16 distribution 0.53, 17 workforce 0.41, 09 electronic 0.41,
08 polymers/coatings 0.23. (99 unresolved 0.42.)

## Low-purity flags → enrichment / registry-research queue (`low_purity_flags.csv`)
5 NAICS with ≥$5M HII that scatter or whose observed SWBS implies a different category:
1. **336611 Ship Building (cat 13, $36.6M)** — scattered (modal one-digit share 0.65) → confirms
   the taxonomy's decision to make 336611 a *review trigger*, not auto-assign to 13.
2. **333310 Commercial/Service Machinery (cat 11, $28.7M)** — work lands in HVAC; likely galley/
   laundry/refrigeration equipment.
3. **332410 Boiler & Heat Exchanger (cat 04, $26.4M)** — lands in fluid/piping; thermal↔fluid boundary.
4. **332420 Metal Tank (cat 05, $11.2M)** — scattered.
5. **333414 Heating Equipment (cat 04, $9.4M)** — low agreement; thermal↔fluid boundary.

The other half of the research queue is the **no-primary-NAICS $884M**, resolved by registry
override rather than NAICS research (mostly already covered by the top-50 registry).

## Bottom line
The process taxonomy is **well-validated where HII can see it**: 01/02/03 ≈ 0.98, 04 ≈ 0.67
(explained by a genuine thermal/fluid adjacency). The two "failing" system categories (05, 10)
fail for structural data reasons, not taxonomy reasons. Forgings/castings — the process-only
category with no SWBS home — is corroborated independently by 96% component-text coverage.
Net: adopt the NAICS map as the baseline, apply the registry override for the no-primary mass,
and treat the 5 flagged NAICS + the thermal/fluid boundary as the targeted-research list.

## Outputs
- `naics6_hii_purity.csv` — per primary NAICS-6: HII$, modal SWBS, concentration/entropy, agreement, mismatch.
- `category_hii_agreement.csv` — per category: HII$, SWBS agreement or not-observable note, component_text coverage.
- `low_purity_flags.csv` — the enrichment queue above.
