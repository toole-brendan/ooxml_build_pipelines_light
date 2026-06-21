# Deck pipeline enhancements — 2026-05-25

Parallel-track session to the deck-content work in
`deck_build_session_2026-05-25_pt3.md`. This session touched the
**build infrastructure** under `deck/` — schema validation, OOXML
reference cache, and the agent-facing surface around both. No slide
modules were authored or edited; the existing slide pipeline kept
building cleanly throughout.

## Context at session start

- `deck/` pipeline emits raw OOXML strings via `primitives.py` →
  `builder.py` → `build.py`. Schema-order traps were documented only
  in comments (e.g., `primitives.py:114` notes the required
  `lnSpc → spcBef → spcAft → bu*` ordering inside `<a:pPr>`).
- `lxml` was imported in `build.py:42` but only used for the
  `strip_all_shadows` post-process.
- No tests, no dependency manifest, no validation layer.
- `build.py` registered `s06_visibility_gap` but the file was missing
  from `slides/` at first read; the slides directory grew during the
  session to 10 files including `s08_divider_layers.py` and
  `s09_aegis_spy6.py` (those are the content-track session's work).
- The user's stated goal: make the pipeline more robust and give an
  AI agent better local access to OOXML reference material.

## Work completed

### 1. ECMA-376 XSD schema validation

Added a validation step that runs against every rendered slide body
before packing. Catches schema-order errors at build time instead of
having PowerPoint open with a "Repair" dialog or silently drop
content.

**Source choice.** Vendored the Transitional XSD set from
`QtExcel/ecma-376-5th` commit `457ce928a15b2ccda8ffbd7f6fc4e828113c6290`
(2019-02-16; repo archived, content frozen). Not Strict — the Saronic
chrome and authored slides both use the 2006 transitional namespaces.

**Files staged.** Full 26-file Transitional set into
`deck/_schema/` (~960 KB):

- `pml.xsd` (root)
- 8× `dml-*.xsd`
- 9× `shared-*.xsd`
- `wml.xsd`, `sml.xsd` (transitively imported)
- 5× `vml-*.xsd`

Flat directory because the `<xs:import schemaLocation="..."/>` paths
in QtExcel are relative siblings. Confirmed closure with one
`lxml.etree.XMLSchema(parse(pml.xsd))` call — ~10 ms cold load,
sub-ms per-slide validation.

**Module: `deck/validate.py`** (new).

- `SlideValidationError(RuntimeError)` — raised on schema or XML
  syntax failure.
- `validate_slide_xml(xml, *, slide_name="")` — parses with
  `lxml.etree.fromstring`, runs `schema.validate(...)`, formats a
  multi-line error: slide name, line/column, source line sliced
  out of `xml.splitlines()` with a caret, optional hint from a small
  lookup dict keyed on the most common offending tag (`lnSpc`,
  `spcAft`, `solidFill`, `prstDash`, `tailEnd`, `xfrm`, etc.), and
  the raw lxml message as fallback.
- `_get_schema()` — lazy module-level singleton; compiles `pml.xsd`
  once and caches.

Top-of-file comment block restates the trust boundary: only
authored slide bodies are validated. Chrome under `_extracted/` and
packaging XML (`[Content_Types].xml`, rels, `presentation.xml`,
`docProps/*`) are trusted and out of scope.

**Integration: `deck/build.py`.**

- Added `from validate import SlideValidationError, validate_slide_xml`
  near the top.
- Wrapped the render loop (~line 389) so each `mod.render(...)` is
  validated immediately; first violation aborts with `SystemExit(1)`
  and no partial `.pptx` is written.
- Replaced `if __name__ == "__main__": build()` with an `argparse`
  block exposing `--no-validate` (default off; bypass is debug-only).
- New keyword arg: `build(deck_title=..., *, validate=True)`.

**Verification.**

- **Positive.** `python3 build.py` on the 8 registered slides exits
  0. Same `out/destroyer_deck.pptx` size as `--no-validate`.
- **Negative (synthetic).** Hand-built a minimal `<p:sld>` with
  reversed `<a:pPr>` child order (`spcAft` before `lnSpc`); validator
  raised `SlideValidationError` with all the formatted parts —
  slide name, line/col, source caret, hint dict match on `lnSpc`,
  raw lxml message.
- **Negative (end-to-end).** Transiently injected a forced
  `<a:spcAft>` emission before `<a:lnSpc>` in
  `primitives.py:paragraph()`; ran `build.py`; got exit 1,
  `slide1 (slides.s00_cover)` named, ordering hint shown, +2 silent
  follow-on violations counted but not spammed. Reverted.

**Documentation.** Added `deck/_schema/README.md` (provenance, file
list, refresh procedure) and a "Schema validation" subsection in
`deck/README.md` explaining the trust boundary and the
`--no-validate` escape.

### 2. OOXML reference cache (initial build)

Goal: give an AI agent authoring slide modules fast local access to
OOXML element / attribute / SDK class info, without web-fetching
Microsoft Learn pages every time.

User research surfaced four candidate sources: ECMA-376 XSDs
(already done), OfficeDev/open-xml-docs markdown, the
DocumentFormat.OpenXml NuGet intellisense XML, and the dotnet
xrefmap. After verification work — the actual repo is
`OfficeDev/open-xml-docs` (not `MicrosoftDocs/office-developer-docs`),
the dotnet xrefmap is 270 MB and contains *zero*
`DocumentFormat.OpenXml.*` entries, the NuGet intellisense XML is
14 MB uncompressed — settled the design via `AskUserQuestion`:

- Scope: Presentation + Drawing only.
- Wrap with a small CLI (initially; later removed — see §4).
- Skip the bulk xrefmap; handwrite a small element→URL JSON.

**Files initially shipped (later trimmed):**

```
deck/_docs/
├── _refresh.py                 # fetcher (later removed — see §5)
├── _build_element_urls.py      # element→URL map generator
├── open-xml-docs/
│   ├── presentation/  (29)         # later curated to 10 — see §3
│   ├── general/       (12)         # later curated to 4
│   └── migration/      (1)         # later removed
├── intellisense/
│   └── DocumentFormat.OpenXml.PresentationAndDrawing.xml  # 3.86 MB
└── xref/
    └── element_urls.json       # 78 entries, one per primitives.py tag
```

The intellisense filter is the only non-trivial transform: kept
`<member name="X">` entries where `X[2:]` starts with
`DocumentFormat.OpenXml.{Presentation,Drawing,Packaging}`. Drops the
14 MB whole-package XML to 3.86 MB / 11,456 members. Wordprocessing
and Spreadsheet absent (confirmed by inspection).

**Element→URL map.** `_build_element_urls.py` extracts every
`<ns:tag>` literal emitted in `primitives.py` (78 distinct pairs),
finds the SDK class via the intellisense's "qualified name is
{ns}:{tag}" pattern, and emits
`https://learn.microsoft.com/en-us/dotnet/api/{fqn.lower()}`. Tags
with multiple matching classes (e.g., `a:xfrm` →
`Transform2D`/`TransformEffect`/`TransformGroup`) keep all
candidates. All 78 mapped on first run, no manual curation needed.

**Initial CLI: `deck/ooxml_lookup.py`** (~300 lines, later removed —
see §4). Single Bash call dispatched to four sections (XSD, MD, SDK,
URL) with query normalization (local name, ns-qualified, SDK FQN,
bare SDK class) and `--source` filter. Two refinements landed before
the CLI was scrapped: namespace-aware XSD search (so `a:pPr` doesn't
return `wml.xsd` matches) and SDK-FQN reverse resolution to qname.

### 3. Curation: markdown corpus

After surveying the OfficeDev/open-xml-docs content, the
`how-to-*.md` files turned out to be Open XML SDK C# tutorials —
useful to .NET developers, useless to a pipeline that emits raw XML
in Python and never instantiates an SDK class. Code-block-to-prose
ratio was actually low (9–19%), but the prose IS procedural
SDK-usage, not OOXML structure.

**Dropped (29 → 14 files, 311 KB → 204 KB).**

- All 19 `presentation/how-to-*.md`.
- 8 of 12 `general/how-to-*.md` (the SDK-procedure ones).
- Entire `migration/` directory (v2 → v3 SDK migration).

**Kept** — the conceptual / structural files:

- `presentation/structure-of-a-presentationml-document.md` (40 KB —
  the gem; pure schema/package overview)
- 8× `presentation/working-with-*.md` (slide masters, layouts,
  notes, comments, animation, etc.)
- `presentation/overview.md`
- `general/{overview,features,diagnosticids,introduction-to-markup-compatibility}.md`

`introduction-to-markup-compatibility.md` is the one that explains
`mc:AlternateContent` / `mc:Choice` / `mc:Fallback` — relevant to
the markup-compatibility risk noted in the validation plan.

### 4. CLI removal (`ooxml_lookup.py`)

After user pushed back on whether the CLI was necessary, agreed it
was a thin convenience wrapper over `grep` and `Read` operations
the agent could do directly. The value-adds (namespace-aware XSD
filtering, SDK-FQN reverse resolution, multi-source dispatch) didn't
justify the ~300 lines of Python and the maintenance surface as
`primitives.py` grows.

**Removed `deck/ooxml_lookup.py`.** Updated 5+ references across
`deck/README.md`, `_docs/README.md`, `_docs/_refresh.py`,
`_docs/_build_element_urls.py` so nothing pointed at the deleted
file.

**Replaced with "How to query the cache" section** in
`_docs/README.md`: grep one-liners for each source plus a
"which source for which question" table. The new section is the
agent-facing documentation that replaced the CLI's `--help`.

### 5. Refresh script removal (`_refresh.py`)

Same minimalism argument applied recursively: the refresh script
ran rarely (NuGet version bumps, OfficeDev updates — maybe once a
year given ECMA-376 is frozen and the SDK is on a slow cadence),
and most of what it did was either a curl loop (markdown fetch) or
a one-time download (nupkg). Only the intellisense filter was
non-trivial.

**Removed `deck/_docs/_refresh.py`** (~200 lines).

**Replaced with "How the cache was built"** section in
`_docs/README.md`. Self-contained shell snippet:

1. Curl loop over the 14 curated markdown filenames.
2. Curl the nupkg, then a `python3 - <<'PY' ... PY` heredoc with
   the ~20-line intellisense filter (the one load-bearing
   transformation, preserved verbatim).
3. Pointer to `_build_element_urls.py` for the URL map step.
4. Cross-reference to `_schema/README.md` for the XSD refresh.

`KEEP` tuple inlined in the heredoc so widening to Word/Excel later
is a one-line edit.

**Kept `_build_element_urls.py`.** Different cadence — runs whenever
`primitives.py` adds a new emitted tag (potentially every few weeks
as content slides grow), and the logic (parse intellisense, regex
"qualified name is X", match against primitives.py tags) is more
complex than a curl snippet. Updated its missing-intellisense error
message to point at `_docs/README.md` instead of the deleted
`_refresh.py`.

## Final state

```
deck/
├── _extracted/                    # Saronic chrome (verbatim, untouched)
├── _schema/                       # 26 ECMA-376 Transitional XSDs (vendored)
│   └── README.md                      # QtExcel provenance + refresh procedure
├── _docs/                         # agent reference cache
│   ├── README.md                      # provenance + rebuild snippet + grep recipes
│   ├── _build_element_urls.py         # kept — element→URL map regenerator
│   ├── intellisense/
│   │   └── DocumentFormat.OpenXml.PresentationAndDrawing.xml  (3.86 MB)
│   ├── open-xml-docs/
│   │   ├── presentation/  (10 conceptual files)
│   │   └── general/        (4 conceptual files)
│   └── xref/
│       └── element_urls.json          # 78 element→Learn URL entries
├── assets_deck/                   # unchanged
├── build.py                       # MODIFIED — validate import, render-loop call, --no-validate
├── primitives.py                  # untouched (negative-test injection reverted)
├── builder.py                     # untouched
├── validate.py                    # NEW
├── style.py                       # untouched
├── slides/                        # untouched
└── README.md                      # MODIFIED — _schema/_docs in workspace tree + schema-validation subsection + agent-reference-cache subsection
```

Net code added: `validate.py` (~115 lines), `_docs/_build_element_urls.py`
(~70 lines). Net code removed: `ooxml_lookup.py` (~300 lines),
`_refresh.py` (~200 lines). About 315 lines of Python net deleted,
plus ~1 MB of vendored XSDs, ~3.9 MB of filtered intellisense, and
~210 KB of curated markdown gained.

`python3 build.py` exits 0 with validation on. All 8 currently-registered
slides validate cleanly; `_build_element_urls.py` re-runs idempotently
(78/78 mapped, none unmapped).

## Decisions / patterns worth keeping

- **Vendor (commit) for hermetic builds, document the refresh
  procedure rather than scripting it.** Holds for both `_schema/`
  (frozen ECMA spec) and `_docs/` (slow-moving SDK / docs). Scripts
  earned their keep only when they did something genuinely
  non-trivial (the intellisense namespace filter — preserved as a
  ~20-line heredoc in the README).
- **Trust boundary as a first-class concept.** Validation only
  covers authored slide bodies; chrome and packaging XML are
  trusted. Documented in `validate.py`'s top docstring, both
  READMEs, and the plan file. Prevents scope creep.
- **Hint dict over schema parsing for ordering errors.** Six or
  eight hand-curated entries keyed on the element lxml reports as
  unexpected, with the raw lxml message as fallback. Cheap to
  maintain, surfaces the right fix for the cases that actually
  bite.
- **Cache is the asset, not the wrapper.** Two iterations of
  "delete the thin wrapper, let the agent grep the cache files
  directly." Held for both `ooxml_lookup.py` and `_refresh.py`.
  The remaining `_build_element_urls.py` survives only because its
  job (parse intellisense XML for SDK-class qnames, match to
  primitives.py emitted tags) genuinely isn't a one-liner.
- **`AskUserQuestion` for forks that matter, defaults for forks
  that don't.** Used it for the cache scope (Presentation+Drawing
  vs everything), the CLI-vs-files decision, and the xrefmap
  handling — three real architectural choices. Didn't use it for
  filenames, hint-dict entries, or grep-recipe wording where the
  reasonable default is obvious.
- **Plan-mode iteration.** Two planning rounds (validation, then
  reference cache) each followed the Explore → Plan-agent → Write
  plan → Exit flow. Both plans approved on first pass and shipped
  on the same day.

## Open follow-ups (not done in this session)

- **Package/relationship model.** `build.py` still hand-emits
  `[Content_Types].xml`, rels, `presentation.xml.rels`, per-slide
  rels by string concatenation. The largest remaining "silent
  PowerPoint Repair" risk surface. Discussed in the third-agent
  review at the end of the session; deferred.
- **Layout registry.** Parsing `_extracted/slideLayout*.xml` into a
  structured registry (placeholder positions, default roles) would
  replace the "open the XML and squint" workflow when binding new
  slides to layouts. Deferred.
- **Office extension specs.** MS-PPTX / MS-OE376 / MS-ODRAWXML
  coverage is zero. Only matters when the deck explicitly touches
  `p14`/`a14`/`p15` namespaces, which it currently doesn't. Deferred.
- **Element→URL map drift assertion.** The map is generated and the
  generator prints unmapped tags, but nothing in the build pipeline
  fails when `primitives.py` adds a tag without a corresponding
  entry. Could be wired into `build.py` as a soft-warning at startup.
