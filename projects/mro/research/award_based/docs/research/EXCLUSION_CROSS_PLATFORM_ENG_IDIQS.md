# Exclusion: Cross-Platform Engineering IDIQs from Services TAM

## Why

The Services residual surfaced a pattern: ~$400M of "unclassified" FY25 task-order dollars are coming from **cross-platform engineering / IT IDIQ contract vehicles** that happen to carry service-type PSCs (J998, J059, K058, etc.) but whose scope is not ship maintenance, repair, or overhaul. These contracts pass through Navy contracting but deliver DoD-wide engineering services, cyber work, training-system integration, or air-traffic control — none of which belong in a Navy/USCG ship-MRO market size.

Until now the model assumed that any contract with an MRO PSC and a Navy/USCG agency is ship MRO. PSC-based classification is necessary but not sufficient: the task-order scope also has to be ship MRO.

## What the patterns look like in the residual

Top IDV descriptions in residual (after all other tiers):

| IDV pattern | Residual $ | TOs | Typical recipients |
|---|---|---|---|
| `SEAPORT-NXG` | $291M | 49 | SAIC, Serco, KBR Wyle, TriStar, HII TS, Chugach |
| `CYBER MISSION ENGINEERING` | $72M | 6 | Scientific Research Corp |
| `COMBAT ENVIRONMENT INSTRUMENTATION SYSTEMS` | $41M | 11 | EWA Triad |
| `ATC PLATFORM INTEGRATION` | $5M | 3 | BAE Tech Solutions & Services |
| **Subtotal (safe-exclude)** | **~$409M** | **69** | |

These are the contracts being proposed for exclusion.

## What each one is

**SEAPORT-NXG** (Navy Seaport-NxG) — a Navy-wide Multi-Agency Contract (MAC) IDIQ for professional engineering, program management, and financial/cost analysis support services. Task orders span every Navy program, not just ship MRO. It is the Navy's go-to umbrella vehicle for engineering labor. Recipients in our residual (SAIC, Serco, KBR Wyle, TriStar, HII Technical Solutions, Chugach, Vector, MIL Corp) are staffing-services firms, not shipyards. By definition the SEAPORT-NXG task orders that are still residual after every text / DAP / hull-number / recipient tier are ones whose text doesn't reference a ship — they are generic engineering-labor task orders, not ship repair.

**Cyber Mission Engineering** — cyber work for Navy command systems. Hits J058/J059 PSC codes (maintenance of electronic / comm equipment) because the deliverable involves electronic systems, but the work is offensive/defensive cyber, not ship repair.

**Combat Environment Instrumentation Systems** — test and training-range instrumentation systems (e.g. NWTRC, NUWC ranges). Hits K058 (modification of communications / detection equipment). Training-range hardware, not shipboard equipment.

**ATC Platform Integration** — Air Traffic Control (aviation/airfield) systems. Hits J-PSCs as electronic-equipment maintenance. Aviation-adjacent, parallel to J016/J028/J069 aviation PSCs that were already excluded in session 2026-04-16_ii.

## Why these are *not* ship MRO

Three reasons the existing cascade fails to classify them:

1. **No ship-specific text anywhere.** All seven classification tiers (proper name, hull number, DAP, vessel regex, supergroup regex, recipient prior) rely on either the mod / IDV / award text or the recipient identity containing a ship signal. These IDIQs deliver engineering labor by skill category, not by ship. The SOW describes capabilities (systems engineering, cyber analysis, program management), not platforms. Therefore the cascade correctly returns "no match" — but for a reason the market-sizing model doesn't handle: the work isn't a ship at all.

2. **The vendors are staffing / engineering firms, not shipyards.** The SEAPORT-NXG recipients above are bodies-in-seats professional-services contractors. They don't hold maintenance availability contracts or hull-cleaning contracts. They aren't in the ship-repair supply chain.

3. **Contract vehicle scope is explicit.** Seaport-NxG's published scope (NAVSEA solicitation N00178-19-R-7000) is Navy-wide engineering services across 23 functional areas including cybersecurity, training, and program management — not ship maintenance.

## What we are *not* excluding (and why)

Some adjacent patterns look similar but are kept because they do map to ship systems:

- **ISEA SUPPORT SERVICES ($47M)** — In-Service Engineering Agent. ISEAs support specific ship combat systems (AN/SLQ-32 EW, Aegis, SPY radars). The work is ship-system-focused even if the ship isn't named. Residual here should eventually get classified via better DAP / system-code coverage, not excluded.
- **SOCS SATCOM ($37M)** — Ship-borne SATCOM. Cross-class but shipboard.
- **Depot Systems Support ($34M)** — broad, but likely includes shipboard systems. Not cleanly excludable.
- **Husbanding Support Services ($57M, 379 TOs)** — port-visit support for Navy ships. This IS ship-related (services rendered to ships during port calls) and should classify, not exclude. Mostly M2xx PSCs already.

## Estimated impact

Before this exclusion:
- Navy services in: $7.97B
- Already-excluded (shore/base + Marine Corps + Army + FMS): $558M
- Residual: $2.23B (~29% of net services $)

After this exclusion (estimated):
- Additional exclusions: ~$409M
- Residual: ~$1.82B
- Residual as % of net services: ~25%

Combined with the remaining tier-5 lift already applied, the total residual would be ~$1.8B / ~$7.28B net = **~25%**.

## What this does NOT achieve

The original goal was 10% residual. These exclusions plus the earlier regex / DAP / recipient-prior tiers only get us to ~25%. The residual gap to 10% is genuinely ambiguous "SHIP REPAIR" text on Navy ship-repair contracts at generic yards without hull identification. Closing that gap requires either:

1. LLM classification pass over the remaining residual (~$1.8B, ~3,500 PIIDs) using Claude Haiku with a constrained schema. Estimated $1-5 to run.
2. Manual PIID-to-hull map for the top 200 residual PIIDs. High quality, several hours of external research.

Neither is in scope for this exclusion decision, but both are the logical next steps if 10% is a hard target.

## Implementation

Add to `sheets/services.py::SHORE_BASE_IDV_PATTERNS`:

```python
re.compile(r"\bSEAPORT[\s-]?N(?:X|EXT)G\b", re.I),
re.compile(r"\bCYBER\s+MISSION\s+ENGINEERING\b", re.I),
re.compile(r"\bCOMBAT\s+ENVIRONMENT\s+INSTRUMENTATION\b", re.I),
re.compile(r"\bATC\s+PLATFORM\s+INTEGRATION\b", re.I),
```

And rename the helper from `is_shore_base_excluded` to something broader since the set of exclusions now includes:
- Shore/base infrastructure (ATFP, NAVFAC facilities)
- Ground weapons (Marine Corps M67854)
- Army watercraft / USACE dredge (W912CH, W9127N)
- Foreign Military Sales (Egyptian / Iraqi navies, etc.)
- Cross-platform engineering MACs (SEAPORT-NXG, Cyber Mission Eng, etc.) — **this addition**

A name like `is_non_ship_mro_excluded` or `is_out_of_scope_for_services_tam` would be more accurate, but renaming can wait — the current function name is an artifact of when shore/base was the only exclusion category.

## Audit trail

If the workbook reviewer disagrees with any one of these IDV patterns, each pattern is a single regex that can be removed independently. The exclusion count is logged per-run in the build output (`[excluded N shore/base awards ($X)]`) so the $ impact of the rule stays visible.
