# 2026-06-20 - Archetype MECE revision (D axis)

Second session of the day (after `2026-06-20_hull_builder_only_scope_standardization.md`).
Made the **Capability Domain (D) axis MECE**; the Primary Output (P) axis was already a clean
maturity ladder and was left unchanged. Build green throughout (12 sheets, 10 tables, 6 note
parts, 0 XML errors, 0 error-literal cells, no repair).

## Diagnosis (why D was not MECE)

The crosswalk failed to place **36% of observed NAICS on D (->D0)** vs only 14% on P (->P0),
because the D axis mixed three logics: (1) ship-system domains D1-D8/D10, (2) a process/material
fallback D9 on a *different* axis (overlaps every functional domain), and (3) an overloaded D0
that conflated genuine-no-evidence + services + un-domainable equipment. D0 was $3.03B (24% of
the hull-builder universe). The single largest item: **Northrop Grumman `LCV2N9FVV739` ($2.0B,
NAICS 335312 Motor & Generator) deliberately overridden to D0** because motors->D2 and
generators->D3 and the taxonomy had no bridge (the D2/D3 "crack"). That one entity was 80% of
Virginia D0 and 60% of Columbia D0.

## The five fixes

1. **D2/D3 electric-power crack.** Added a tie-break (_taxonomy.DOMAIN_TIEBREAKS): a firm spanning
   propulsion motors/drives (D2) and power generation/conversion/distribution (D3) is assigned by
   dollar-dominant ship function, NEVER D0. Crosswalk `335312`->D3 (generic) and `333611` turbines
   ->D2. **NG re-adjudicated program-specifically from its own basis notes**: Virginia (main-
   propulsion machinery) -> **D2**; Columbia (Common Missile Compartment launcher) -> **D6** (it is
   not even electrical on Columbia). Edited the override source `{virginia,columbia}_archetype_
   results.csv` with a `[MECE 2026-06-20...]` marker.
2. **New D11 "Services & Non-Material Support"** (domain-axis counterpart of P6): engineering/
   test, install/repair, logistics, software, training, facilities. Reverses the old "there is no
   services domain" rule. 38 service NAICS remapped D0->D11 via `scripts/apply_mece_remap.py`.
   Distributors deliberately NOT moved here (they take the material's domain, or D0 - a role, not
   a service).
3. **D9 reframed** "Specialty Materials & Precision **Processes**" - explicitly an application-
   agnostic process/material fallback (assign a functional domain D1-D8 when the ship application
   IS known), not a peer ship-system domain.
4. **Catch-alls tightened + ordnance decided.** D8 -> "Mechanical Handling & Deck Machinery"
   (dropped the vague "mechanical auxiliaries"; general fluid/thermal/electrical machinery routes
   to D4/D5/D3). D10 -> "Interiors, Habitability & Outfitting" (no longer a residual for
   "manufactured goods not captured above"). D6 sharpened; **ordnance stays in D6** (no separate
   domain - under the hull-builder scope the weapons GFE primes are out of scope, so standalone
   ordnance is sparse) - documented as a tie-break.
5. **P axis unchanged** - it is a genuine P1->P5 maturity ladder + P6 services + P0; only the
   inherent P2/P3 boundary is fuzzy and the boundary test handles it.

## Files changed

- `extracted/naics6_archetype_map.csv` - 40 D0 rows remapped (38->D11, 335312->D3, 333611->D2).
  Original preserved as `naics6_archetype_map.pre_mece.csv`.
- `scripts/apply_mece_remap.py` - NEW, the auditable, idempotent remap (rule set + change report).
- `extracted/{virginia,columbia}_archetype_results.csv` - NG `LCV2N9FVV739` D0->D2 / D0->D6.
- `sheets/_taxonomy.py` - D6 def sharpened; D8/D10 bounded; D9 reframed; **D11 added** (before D0);
  DOMAIN_TIEBREAKS += D2/D3-electric, Ordnance; "Service firms" tie-break rewritten for D11.
- `sheets/guide_methodology.py` - "D1-D10"->"D1-D11"; canonical-universe row -> ~$12.49B hull-builder.
- Rebuilt overrides (287 rows) + workbook; re-cut validated via `/tmp/recut_dp.py` (now incl D11).

## Impact (hull-builder-only universe; pooled where noted)

D0 collapsed from **24% -> ~7%** (now just the honest no-evidence floor):

| Program  | D0 before  | D0 after   | biggest moves out of D0                              |
|----------|-----------:|-----------:|-----------------------------------------------------|
| DDG      | $304M 8.4% | $277M 7.7% | services -> D11 (24 vend / $25M)                    |
| Virginia | $1,841M 36%| $319M 6.2% | NG $1,471M -> D2; services -> D11 (44 vend / $37M)  |
| Columbia | $931M 21%  | $286M 7.6% | NG $530M -> D6; services -> D11 (60 vend / $55M)    |

Consequences worth noting: Virginia **D2 now 36%** ($1,840M) - ~80% of it is the single NG
electric-drive/propulsion contract; Columbia **D6 now 24.5%** ($922M) - ~58% is the NG CMC
launcher. Legitimate single-contract concentrations, not errors. D11 is small by $ (services are
low-dollar) but meaningful by count (24/44/60 vendors left D0).

## Addendum - D9 functional-domain push (same day, user-approved Tier A + mis-bins)

Audited the 127 D9 firms ($1,446M); dollars sit in 33 hand-researched firms (other 94 = no-prose
long-tail). Pushed ONLY firms whose ship application is named in the research prose; kept the
genuine material/acoustic specialists (Globe $218M, Oil States $103M, Hutchinson, Metaltek) and
all indeterminate firms as D9. 7 firms, via firm-level overrides in `{program}_archetype_results.csv`
(backups `*.pre_d9mece.csv`):

| Firm | UEI | -> | basis |
|---|---|---|---|
| Scot Forge | N1PJDANWUJ61 | D2 | submarine/ship shaft forgings |
| Erie Forge & Steel | WUDSRNBSYC17 | D2 | marine propulsion/stern shafting |
| American Tank & Fab | PUG1H9MFJD63 | D2 | Virginia propulsor forward assembly (Columbia row flipped D1->D2 for firm consistency) |
| Ranor | MF1LU8RPCMB8 | D2 | BAE Virginia propulsor assemblies |
| Goodrich | CBMZJ3Z5SC89 | D1 | composite sail cusp / structures |
| D.W. Clark | MKDGDE6K34N5 | D4 | seawater pump/valve castings |
| Industrial Corrosion Control | DQ35GXAUTW61 | D11 | coating/blasting service, not a material (mis-bin) |

Set consistently across each firm's programs (4 tail rows ADDED where a program was map-resolved
D9). Overrides 287 -> 291 rows. Impact: pooled D9 $1,446M -> $926M (~$520M moved: ~$440M into D2,
~$58M D1, ~$12M D4, ~$11M D11). D9 now reads as the application-agnostic material/acoustic base.
**Watch:** this further concentrates D2 - Virginia D2 now 40.2% ($2,053M; ~NG $1,471M + Scot $176M),
Columbia D2 18.6%.

## Open / not done

- Constant-FY2026 dollars (prior handoff §8) - still on hold.
- D9 Tier B (Ellwood Forge, Lehigh Heavy Forge, Seemann bow domes - application likely but exact
  part unconfirmed) deliberately left as D9; push later if desired.
- Big remaining D0 buckets are genuine-indeterminate generic codes (336611 shipbuilding $1.2B,
  332999 misc-fab-metal $0.5B) - firm-level overrides only, not NAICS rules.
