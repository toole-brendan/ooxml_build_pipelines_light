# MRO Deck — Reserve Commentary

Supporting context, sourcing, and citations behind every **body slide** of the MRO deck
(`deck/deck_mro/slides/`). For each slide there is one file holding: the verbatim on-slide
claims, claim-by-claim sourcing, "reserve" facts you can pull onto the slide, quotable stats
with attribution, and caveats/confidence/staleness flags.

These files are **additive notes** — nothing here edits the deck, workbook, or research.

## Files

| File | Slide | Module | What it covers |
|---|---|---|---|
| `03_definitions.md` | 03 | `definitions.py` | Five sizing levels (Total Funding → TAM → SAM → TCV → ACV) |
| `04_bottom_up_approach.md` | 04 | `bottom_up_approach.py` | FPDS PSC filter: 2,539 → ~1,800 → 65 PSCs → $9.0B |
| `05_vessel_taxonomy.md` | 05 | `vessel_taxonomy.py` | Navy + USCG hull taxonomy (SECNAVINST 5030.8D) |
| `06_work_segments.md` | 06 | `work_segments.py` | Six work segments; Depot 53% + Nuclear 21%; $8,971M |
| `07_tam_composition.md` | 07 | `tam_composition.py` | Marimekko, work segment × vessel type |
| `08_topdown_detail.md` | 08 | `topdown_detail.py` | $17.0B top-down budget rollup, line by line |
| `09_topdown_funnel.md` | 09 | `topdown_funnel.py` | $17.0B − $7.49B Public NSY → $9.5B private-addressable |
| `10_reconciliation_bridge.md` | 10 | `reconciliation_bridge.py` | 7-component top-down ↔ bottom-up bridge |
| `11_private_addressable.md` | 11 | `private_addressable.py` | Two pathways converge: $8,971M vs $9,511M (~6%) |
| `12_fleet_structure.md` | 12 | `fleet_structure.py` | Marauder comp-set: 14 hulls, 3 tiers, $758M |
| `13_fleet_mro.md` | 13 | `fleet_mro.py` | Comp-set MRO $758M; 82% depot; per-hull split |
| `14_sam_sizing.md` | 14 | `sam_sizing.py` | TAM → SAM funnel; SAM = $623M (~7% of TAM) |
| `15_contract_vehicles.md` | 15 | `contract_vehicles.py` | MSRA / MAC-MO / SeaPort / FedMall-GSA / USCG-SFLC |

`cover_mro.py` (01) and `overview.py` (02, Context & Objectives) are infrastructure and are
not covered.

---

## Staleness & reconciliation audit (the question: "is the workbook stale?")

**Short answer: No. The workbook is the freshest, authoritative artifact and it ties to the
deck to the dollar. The *stale* material is the April methodology research, which is a layer
behind — but reconciles cleanly.**

### Evidence

| Artifact | Last touched | Headline basis |
|---|---|---|
| Output workbook `20260607_…_vS.xlsx` | **Jun 8 20:40** (today) | `$8,971M` reconciled; `$1,904M` embedded |
| Workbook sheet modules `workbook_mro/sheets/` | **Jun 8** (today) | computes reconciled TAM |
| Deck slide modules `deck_mro/slides/` | **Jun 8** (today) | shows `$8,971M` / `$9.0B` / `$17.0B` |
| `research/psc1905/` (the bridge) | Apr 22 | locks `$1,904M`; defines `$8,971M` |
| `research/award_based/docs/methodology/` | **Apr 15–20** | services-only `$7,067M`; embedded `$1,660M` |

The output workbook was rebuilt the *same minute* as the newest deck edit. It is in lockstep
with the deck.

### Independent tie-out (run against the workbook's own source data)

Summing `Is MRO == TRUE` FY2025 obligations in `workbook/extracted/awards.csv`:

```
Navy        $6,794.2M   (7,241 awards)
Coast Guard   $272.6M   (1,450 awards)
─────────────────────
Services    $7,066.9M  ≈ $7,067M
+ embedded PSC 1905    $1,904M   (model_reconciliation.py → PSC1905_MRO_EMBEDDED)
= Reconciled FPDS TAM  $8,971M
```

`$8,971M` is **exactly** the deck's on-slide total (`work_segments.py` `ChartTotal = "$8,971M"`,
`slide06.xml`, `slide11.xml`). The CG `$272.6M` also matches the deck's USCG bottom-up `$273M`
(`slide10.xml`). The workbook is current and self-consistent.

### Why "$7.1B" and "$9.0B" both appear — they are two layers, not a conflict

```
Services-MRO TAM      $7,067M   (65 J/K/N/M/H/L services PSCs, Navy + USCG, FPDS, post-exclusions)
+ Embedded PSC 1905   $1,904M   (ship MRO booked under shipbuilding PSC 1905 at SUPSHIP yards)
= Reconciled FPDS MRO $8,971M   (the deck's "$9.0B bottom-up")
```

- The **April `methodology/` docs** predate PSC-1905 integration. They anchor on the
  services-only `$7,067M` and an *older* embedded central of **`$1,660M`** (since revised to
  `$1,904M`). Treat their headline TAM as the **services layer**, not the deck total.
- The **`research/psc1905/` folder (Apr 22)** is the bridge that locked `$1,904M` and defined
  the reconciled `$8,971M`. It describes the integration against an *earlier* workbook
  (`build_script_slim/…v4.5.xlsx`) and earlier slide numbers (Target S5/S8/…). That
  integration has **since been implemented** in the current native `workbook_mro/` rewrite —
  so read those docs for the *why*, and read the current workbook modules for the *as-built*
  truth.

### How to use the sources (hierarchy)

1. **As-built / authoritative** — current `workbook_mro/sheets/*.py` accessors and the deck
   slide modules. Use these for any figure you put on a slide.
2. **Current narrative framing** — `research/psc1905/` (reconciled story, per-vessel and
   per-parent embedded attribution, top PIIDs).
3. **Deep methodology + external citations** — `research/award_based/docs/methodology/`,
   `research/budget_method/topdown_gold/`, and workbook `sources_references.py`. Rich for
   reasoning and citations; **layer-correct** any headline number and treat the `$1,660M`
   embedded / services-only `$7,067M`-as-total figures as superseded.

### `[!]` flags appear in the per-slide files wherever an April doc shows a superseded number.

---

## Source-line format

Each per-slide file ends with a **Source line — ready to use** block in the deck's canonical form:

> Sources: (1) …; (2) …; (3) …

- "Sources:" (plural), numbered (1), (2), (3); semicolon-separated.
- No terminal period; no "Note:" caveat; no "Data as of" line.
- Page pins go inside a source entry, e.g. *(p.157)*.
</content>
