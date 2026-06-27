# 2026-06-24 - Session log (research/wiki - defense-contracting structural reference)

Built a new single-page, Wikipedia-styled HTML wiki under
`projects/awards_methodology/research/wiki/`, modeled on the existing DDG-51
outsourcing wiki generator
(`projects/distributed_shipbuilding/tam/ddg_research/research/wiki`). Source content
was a user-supplied "U.S. Defense Contracting Wiki: Master Map" plus two companion
modules (period-of-performance/scope/small-business/funding-traceability; and
modifications/FSRS-subawards/CLINs/single-vs-sole-source/the submarine example).
Output: `research/wiki/index.html` (~345 KB, ~40k words). Build stayed green
(`python3 build_wiki_html.py` -> 18 chapters, 0 warnings).

---

## What was created

New tree (all untracked in git):

```
awards_methodology/research/wiki/
├── INDEX.md                ← front matter: hatnote, lead, infobox, See also,
│                              References (FAR/DFARS/PGI/SBA/GAO/USAspending bib),
│                              Further reading, External links, Article structure
├── 01..18-*.md             ← 18 chapter files (~40k words total)
├── build_wiki_html.py      ← pipeline adapted from the DDG-51 generator
├── index.html              ← generated artifact (~345 KB)
└── assets/style.css        ← generated artifact (Wikipedia "Vector" styling)
```

1. **Build pipeline** (`build_wiki_html.py`). Copied the DDG-51 generator verbatim
   except for: the `ARTICLES` table (now 18 chapters in 7 category groups), the page
   `<title>`, and the docstring. All machinery unchanged - concatenate INDEX.md +
   numbered chapters into one markdown doc, demote each chapter `# H1` to a slugged
   `##`, render via python-markdown (`extra, attr_list, toc, footnotes`), rewrite
   `[label](NN-file.md)` cross-links to `#anchor`, add `wikitable` class, inject a
   `Citations` heading before the footnotes block, build the sticky sidebar TOC.
   STYLE_CSS and PAGE_TEMPLATE carried over (CSS is generic).

2. **INDEX.md** (front matter). Lead develops the two analytical throughlines from the
   master map - "award amount" is ambiguous (5 distinct numbers; never sum parent
   ceiling + child orders) and "in scope" is necessary but not sufficient. Infobox =
   16 dated rows (thresholds, goals, the FAR Overhaul deviation, data systems).
   References organized by source family with real URLs from the master-map citations.

3. **18 chapters** across 7 parts:
   - I Framework: 01 dimensions, 02 core vocabulary
   - II Awards & money: 03 awards/ceilings/obligations/spending, 04 federal data systems
   - III Instruments: 05 indefinite-delivery (FAR 16.5), 06 IDV/IDIQ/MAC/GWAC/Schedules
   - IV Pricing/options/time: 07 pricing & cost risk, 08 options & award terms, 09 period of performance & scope
   - V Multiyear/production: 10 MYP + major weapon production (Virginia-class case)
   - VI Prime/sub structure: 11 privity & flowdowns, 12 subawards & first-tier reporting, 13 small business
   - VII Structure/authority: 14 modifications, 15 CLINs/SLINs & funding traceability, 16 single-award vs sole-source, 17 contracting authority & award decisions, 18 "not a contract type" traps

## How it was built

- Wrote chapter 01 myself as a **style exemplar**, plus a shared **spec file** in
  scratchpad (format rules, voice rules, the filename list for cross-links, and a
  footnote-URL bank).
- Fanned the remaining **17 chapters out to parallel subagents** (3-6 at a time),
  each pointed at the spec + exemplar + its own source slice, with explicit scope
  boundaries to avoid overlap. Subagents wrote their chapter files directly.
- Hard accuracy rule in the spec: reproduce the master map's figures and citations
  exactly, no outside facts. Preserved the **2026 version discipline** throughout -
  Revolutionary FAR Overhaul / DoD class deviation eff. March 16 2026, FAR 16.507
  (deviation) vs codified 16.505, Oct 1 2025 thresholds ($15K MPT / $350K SAT),
  "as of June 25 2026", and every dollar figure ($7.5M, $35M, $150M, 23.17%/30%,
  the $22.2B Block V modification, GAO 77%/27% findings).

## QA performed

Diffed the rendered `index.html` and fixed every issue before sign-off:

- **0** unrewritten `.md` links; **0** broken `#anchor` targets (after fixes).
- **0** second-person voice leaks (after fixes).
- **83** footnotes, **0** duplicate IDs - achieved via per-chapter footnote label
  prefixes (`[^cNN-...]`), required because all chapters concatenate into one doc
  before the `footnotes` extension runs once (`UNIQUE_IDS: False`).
- 20 tables, 21 worked-example diagrams, 111 subsections, 497 internal cross-links.

Fixes applied this session:
- ch02: orphaned `[^c02-far2101]` definition -> wired an inline reference; deleted an
  orphaned `[^c02-deviation]` definition.
- ch08: deleted an orphaned `[^c08-deviation]` definition.
- ch15: reworded an h3 heading ("...does and does not tell you" -> "...identify") to
  remove second-person voice (it had surfaced twice: body + sidebar TOC).

## Notes / open items

- **Two judgment calls** flagged to the user for confirmation: chapter count set at
  **18** (vs DDG-51's 16) to give each master-map topic room; citation style is
  **inline FAR references + a bibliography in INDEX.md** with sparse footnotes
  (matches the DDG-51 model). Easy to merge/split chapters or change citation style.
- **No visual render performed** - user opens `research/wiki/index.html` in a browser
  for the look-and-feel check (consistent with the deck visual-QA preference: halt,
  don't auto-render).
- The entire `awards_methodology/research/` tree is **untracked in git**.
- Rebuild after edits: `python3 build_wiki_html.py` from the wiki dir (needs
  `markdown`, `pyyaml`). `index.html` and `assets/style.css` are regenerated artifacts.
- Shared chapter spec lives in the session scratchpad (not in the repo).
