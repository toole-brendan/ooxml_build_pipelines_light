# 2026-06-24 — Session log (wiki restructure: recompete + lifecycle fold-in)

Folded a large, operator-facing research spec (two ChatGPT passes; the second
superseded the first) into the existing 18-chapter defense-contracting wiki at
`projects/awards_methodology/research/wiki/`, plus one factual correction —
keeping the chapter count at **18** (net-zero). Build stayed green
(`python3 build_wiki_html.py` → 18 chapters, 0 warnings). Page grew from ~40k to
**~52.7k words** (`index.html` ~345 KB → ~469 KB).

Input spec lives in `logs/2026-06-24_session_log.md` (the prior build log) plus the
user's pasted critique; plan saved to
`~/.claude/plans/please-read-projects-awards-methodology-misty-wilkinson.md`
(detailed structural sub-plan alongside it with an `-agent-…` suffix).

---

## Decisions (confirmed with the user before executing)

- **Scope:** full fold-in in one pass (not phased).
- **Voice:** strictly neutral encyclopedic third person — recast every
  startup/second-person framing ("can this startup win", "what must you build")
  into neutral named actors ("a prospective offeror", "a non-incumbent", "an
  analyst"); scoring tables and the 2×2 presented as analysis, not advice.
- **Safety net:** none — no git snapshot taken (tree is untracked). Mitigated by
  doing targeted per-file edits / single-pass transforms instead of blind `sed`.

## Structure change (18 → 18)

- **NEW ch05** `05-recompetes-and-opportunity-intelligence.md` — the one genuinely
  new chapter (inferred-event framing; opportunity-unit + transaction-class +
  demand-signal + false-positive-trap tables; the two-axis event-probability /
  addressability weight tables; three `text` worked-example diagrams: award-family
  tree, clock band, 2×2 action matrix).
- **MERGE** old `11-prime-subcontracting-and-privity.md` +
  `12-subawards-and-ffata-reporting.md` → `12-prime-contracting-subcontracting-teaming.md`
  ("Prime contracting, subcontracting, teaming, and first-tier reporting"),
  deduped + two new sections (Government rights in technical data/software; entry
  choices for a non-holder).
- **RENUMBER** old 05–10 → 06–11 (filenames, footnote prefixes, cross-links).
- **RETITLES** (filenames unchanged): ch08 → "Pricing, commerciality, and cost
  risk"; ch14 → "Post-award administration, modifications, and closeout"; ch15 →
  "CLINs, funding traceability, and program transition"; ch17 → "The acquisition
  lifecycle, source selection, and contracting authority"; ch18 → "Alternative
  acquisition pathways and 'not a contract type' traps".

## The factual correction

ch03 (and the mirror in ch04) no longer call **current value** a "committed-to-date"
amount. Both now state current value is a *contract-value* field that may differ
from obligations and is **not a spending measure**, and name SAM/FPDS's three
distinct concepts: action/total **obligations** (the only commitment),
base-and-exercised-options value (current), base-and-all-options value (potential).

## Content folds (section-level additions)

- **ch04:** mirror correction + new "public-data reporting delay" (~90-day DoD lag)
  + "period-of-performance fields and ordering periods" (IDV last-date-to-order).
- **ch07:** "Vehicle on-ramps, off-ramps, and access".
- **ch08:** price vs cost analysis; commercial-item pricing; indirect/wrap rates;
  cost-type timekeeping & accounting systems; truthful cost-or-pricing data; CAS/
  DCAA/business systems.
- **ch12:** data rights + non-holder entry choices (above).
- **ch14:** kickoff; PCO/ACO/COR/DCMA roles table; CDRLs; inspection/acceptance;
  WAWF/PIEE invoicing; CPARS (controlled/non-public); constructive changes; claims/
  REAs; termination & closeout.
- **ch15:** purpose/time/amount; bona fide need; severable vs nonseverable; expired
  vs cancelled funds; CRs; color-of-money & RDT&E→procurement/O&M transition (+ diagram).
- **ch17:** pre-award lifecycle (need→award→protest, + diagram); "five conditions an
  award must satisfy"; what public data does/doesn't show (forecasts nonbinding;
  CPARS controlled).
- **ch18:** operationalized SBIR/STTR, OT, BAA, CSO (entry → instrument → follow-on →
  re-compete? → public-data footprint) + end-to-end pathway diagram; prototype-OT
  and Phase III follow-ons as lawful closed competitions.
- **INDEX:** article-structure outline renumbered/retitled (Part II/VI/VII
  descriptions updated); bibliography gained SAM Contract Awards + Get Opportunities
  APIs, the fedspendingtransparency PoP whitepaper, DoD forecasts/FAR 5.404, and the
  new FAR/DFARS/statutory authorities (FAR 7/10/12/15.201/15.403/15.404-1/15.506/
  31.203/42.15/46/49/35.016; DFARS 227.71-72/206.001-70/252.242-7006/252.232-7003;
  10 U.S.C. 4021/4022/3458; 15 U.S.C. 638; 31 U.S.C. 1301/1341/1502/1552-1553).

## How it was built

- **Phase 1 — mechanical skeleton, then verified green.** Renamed shifted files
  high-to-low; deleted the two merge sources; created stub ch05/ch12. One **single-pass
  Python transform** repointed all 87 cross-link occurrences (regex over original
  text → dict map, avoiding the ascending `05→06`/`06→07` re-hit trap) and bumped
  footnote prefixes per renamed file (each file holds only its own prefix). Rewrote
  the `ARTICLES` list in `build_wiki_html.py` (new ch05 folded into "Awards and
  money"; merged ch12 keeps "Prime and subcontracting structure"). Rewrote the INDEX
  "Article structure" tail in Python. Skeleton built clean (74 footnotes, 0 dup/dead/
  broken) before any content authoring.
- **Phase 2 — content.** Authored ch03/ch04 corrections, the full new ch05, and the
  merged ch12 myself (the footnote-delicate merge: kept ch12's richer `fsrs`
  definition, dropped ch11's; collapsed the FAR 44.101 / 52.204-10 near-duplicate
  citation pairs; unified surviving notes to `[^c12-…]`). Fanned ch07+08, ch14, ch15,
  ch17, ch18 out to **5 background subagents**, each given the strict voice rule, a
  style exemplar, its footnote prefix, the post-renumber filename list, and a precise
  section spec. All returned clean.
- **Phase 3 — rebuild + QA.**

## QA performed

- Build: exit 0, **0 WARN**, 18 chapters; `index.html` ~469 KB.
- **0** unrewritten `.md` links; **0** broken `#anchor` targets.
- **121** footnote defs, **0** duplicate IDs, **0** orphan refs, **0** defs without a
  ref (every footnote resolves both ways).
- **0** second-person leaks and **0** prescriptive/advice-tone hits across all 18
  chapters (the "strictly neutral" rule held, including in delegated chapters).
- Structural: exactly one H1 per file; all `text` fences balanced (ch05 = 3 diagrams,
  ch12 = 5); footnotes contiguous at the bottom of every file.
- Spot-read ch17 (largest delegated chapter) end-to-end — high quality, well
  integrated, existing authority content preserved.

## Notes / open items

- **No git snapshot taken** (user's choice); `research/` tree remains untracked.
  Restructure is reversible only from this session's history — consider committing
  after the visual pass.
- **No visual render performed** — user opens `research/wiki/index.html` in a browser
  for the look-and-feel check (consistent with the wiki/deck visual-QA preference:
  halt, don't auto-render).
- One cosmetic non-issue: ch18's sidebar label uses curly quotes while its H1 uses
  straight quotes — the same pre-existing convention the original shipped.
- Rebuild after edits: `python3 build_wiki_html.py` from the wiki dir (needs
  `markdown`, `pyyaml`); `index.html` and `assets/style.css` are regenerated artifacts.
