# Note: PSC count in deck footers is stale (68 -> 65)

Deck materials cite "68 services PSCs, post-exclusions" in slide footers
and source lines. The live `sheets/services.py::MRO_PSCS` list now has
**65 PSCs**.

## Cause

Commit `b1aa621` ("Scale workbook values to $M, drop nuclear PSCs,
retire temp SAM sheet") removed the three nuclear PSCs -- **J044
(Maint), K044 (Mod), N044 (Install)** -- from `MRO_PSCS`. Rationale
in the code comment: nuclear reactor work bundles under ship-level
shipbuilding PSCs (1905, 4470) at HII NNS, Fluor Marine, Bechtel, so
J044/K044/N044 contain ~$0 in FPDS and were pruned to keep the scope
honest.

68 - 3 = 65.

## Stale files (deck-facing)

- `deck/DECK.md` (6 references in slide footers + Slide 1 filter funnel)
- `deck/SLIDE5_APPROPRIATION_SOURCING_MOCKUP.md` (source line)
- `deck/SLIDE7_SUB_CARRIER_SCOPE_MOCKUP.md` (source line)
- `docs/research/WHY_PSC_DATA.md` (2 references)

Session logs that cite 68 are dated snapshots and not stale by
definition -- they were correct at the time of writing.

## Action

None taken yet. Before the next deck redraw, sync the footer PSC count
to **65** across the 4 files above to match the code. The TAM value
($7.1B) does not change -- nuclear PSCs contributed ~$0 to the Services
TAM so removing them from the list does not move the bottom-up total.
