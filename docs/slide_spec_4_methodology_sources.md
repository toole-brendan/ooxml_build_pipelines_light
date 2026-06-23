# Slide Spec — 04 · Methodology & Sources (How We Source Federal Award Intelligence)

```text
SLIDE 04 - METHODOLOGY & SOURCES: HOW WE SOURCE FEDERAL AWARD INTELLIGENCE
Type: Body

Slide's purpose:
  The broad, defensible map of where the data comes from and why it can be trusted: four free
  government API families covering the full contract lifecycle, the triangulation rule that
  resolves disagreements, the quota constraints that govern collection, and the honest limits
  (subaward blindness, reporting lag, operational gotchas). This is the credibility slide -
  it answers "can we trust this?" before the analytical slides.

TITLE
-----
Copy:
  How we source it | Four free federal APIs, triangulated, with FPDS as ground truth.

HIGH-LEVEL LAYOUT
-----------------
  Lifecycle swim-lane across the top (Pre-award -> Prime award -> Sub-tier -> Entity), each
  lane mapped to its API(s). An API-at-a-glance table fills the middle. A triangulation +
  honest-limits rail runs along the bottom, with operational-gotcha chips.

COMMENTARY COPY, IF NEEDED
--------------------------
Commentary 1
  Copy:
    Triangulate; FPDS wins ties.
    FPDS is the authoritative prime-award record; USAspending is derived from it (so when the
    two disagree, FPDS is ground truth); subawards lag primes 6-18 months and have compliance
    gaps; SAM Opportunities covers what has not been awarded yet. The SAM Contract Awards API
    (2025) is the modern structured replacement for the FPDS Atom feed.
  Text / shape treatment:
    Bold finding; no-fill rail beneath the swim-lane.

Commentary 2
  Copy:
    A prime feed cannot expose subaward gaps.
    First-tier subcontracts are a separate, lagging universe - multi-billion workshare can be
    structurally invisible in prime data (the HII <-> GDEB submarine co-build is the canonical
    case). Recover it via FFATA subawards + issuer disclosures, not the prime feeds.
  Text / shape treatment:
    Filled caution card, lower-left; this is the most important limitation to state out loud.

Commentary 3
  Copy:
    Keep the money universes separate.
    Prime obligations, funded budget demand, and subawards are distinct money universes;
    within contracts, obligation / current value / ceiling are distinct measures. Never sum
    across them - the discipline that holds Slides 2 and 3 together.
  Text / shape treatment:
    Below-exhibit note; muted; ties back to the prior slides.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Swim-lane labels and their APIs:
    Pre-award (pipeline) -> SAM Opportunities.
    Prime award actions -> FPDS Atom (authoritative) · SAM Contract Awards API (modern) ·
      USAspending (enriched).
    Sub-tier -> SAM Subaward Reporting (FFATA) · USAspending subawards.
    Entity resolution -> SAM Entity Management (UEI -> NAICS / CAGE).
  Operational-gotcha chips:
    "PIID = UPPERCASE, no dashes (reversed 2026-06-21; lowercase silently returns 0 records)."
    "Sum per-mod obligations, never cumulative totals."
    "Subaward reporting lags 6-18 months."

Text / visual treatment:
  Swim-lane as four left-to-right lanes with the API names as chips inside each lane; FPDS
  chip marked "authoritative." Gotcha chips small, monospace, along the very bottom - present
  but visually subordinate (operational footnotes, not headline).

CHART, IF NEEDED
----------------
  None - the swim-lane is an object/lane treatment, not a data chart.

TABLE, IF NEEDED
----------------
Copy / rows / columns:
  API-at-a-glance. Columns: API | What it gives you | API key? | Daily quota | Best for.
  Row 1: FPDS Atom feed | Authoritative prime award actions (XML, per mod) | No | - |
    Ground-truth obligations; discovery by NAICS / PSC / vendor.
  Row 2: USAspending | Enriched awards, transactions, funding accounts (JSON) | No | - |
    FY breakdowns; funding TAS; PIID lookups.
  Row 3: SAM Contract Awards API | Modern structured prime + IDV awards (JSON / CSV) | Yes |
    10 / 1,000 / 10,000 by account tier | Vehicle ceiling + ordering-period; bulk extracts.
  Row 4: SAM Subaward Reporting | First-tier subcontracts, FFATA (per prime) | Yes | (same
    tiers) | The supplier layer under a prime.
  Row 5: SAM Opportunities | Solicitations / pre-award notices | Yes | (same tiers) | The
    not-yet-awarded pipeline.
  Row 6: SAM Entity Management | UEI -> NAICS / CAGE / registration | Yes | (same tiers) |
    Enriching / resolving top vendors.
  Purpose:
    One scannable register of every source, what it is good for, and what it costs to pull.
  Structure:
    Six rows, lifecycle order (prime feeds, then sub-tier, then pipeline, then entity). "API
    key?" and "Daily quota" are narrow scan columns. Quota tiers = personal / entity-role /
    federal.
  Cell / table treatment:
    API column bold. "API key?" centered Yes/No (No tinted as the low-friction case). Quota
    cell small. FPDS row given a subtle emphasis fill (it is ground truth). Header underlined;
    light rules.
  Fit behavior:
    Shorten "What it gives you" first; "Best for" and the quota column must remain. Do not add
    endpoint URLs or query syntax (that is the reference doc, not the slide).

OBJECT NOTES, IF NEEDED
-----------------------
  - Reading order: swim-lane (top) -> API table (middle) -> triangulation/limits rail
    (bottom).
  - The swim-lane lane that contains FPDS, SAM Contract Awards, and USAspending should align
    above their corresponding table rows so the lifecycle map and the register read as one.
  - Optional source-freshness chips (data-through dates) may pin under the swim-lane: budget
    PB2022-2027; USAspending ~1-2 wk lag; subawards 6-18 mo; SAM Contract Awards excludes DoD
    actions signed < 90 days (revealed-only).
  - Do not add: per-API gotcha detail beyond the three bottom chips; endpoint specs.

Do not repeat:
  - Title copy.
  - Commentary copy or treatment.
  - Table copy, data, or cell treatment.
  - Source note.

SOURCES
-------
Copy:
  API documentation: open.gsa.gov/api (SAM.gov Contract Awards, Subawards, Opportunities,
  Entity), api.usaspending.gov/docs, fpds.gov (Atom feed). Quota tiers and freshness /
  reporting-lag notes: internal Army Market Mapping workbook (source clocks). Methodology
  reference: Federal Award API Research Methodology (internal).
```
