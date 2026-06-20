# OOXML documentation audit + pipeline fixes — 2026-05-25

Short follow-on session to `2026-05-25_deck_pipeline_enhancements.md`.
Used the cached OpenXML documentation (`deck/_docs/open-xml-docs`,
`deck/_schema/` ECMA-376 Transitional XSDs, `deck/_docs/intellisense/
DocumentFormat.OpenXml.PresentationAndDrawing.xml`) to audit the deck
pipeline and apply targeted hardening fixes. Schema validation kept
passing throughout.

## Context at session start

- The OOXML doc cache landed in the prior pipeline-enhancements
  session (see that log). It hadn't been used yet for a code review
  pass over the deck modules — only as a build-time validation
  dependency.
- User asked, in two passes:
  1. Audit `deck/slides/*.py` against OOXML docs — anything to update?
  2. Audit `deck/{build,builder,style,validate,primitives}.py` against
     OOXML docs — anything to update?
- Pre-session verification (separate exchange) confirmed the external
  sources the cache was built from are still live and agent-fetchable:
  - `OfficeDev/open-xml-docs` repo + `/docs/presentation` tree (DocFX
    front-matter, `<xref:DocumentFormat.OpenXml...>` cross-refs).
  - `QtExcel/ecma-376-5th` Transitional XSDs (raw fetch returns real
    `xsd:schema` content, `purl.oclc.org/ooxml/...` namespaces).
  - `exceljs/ooxml-xsd` mirror.
  - **Correction noted:** `dotnet/Open-XML-SDK/tree/main/src/
    DocumentFormat.OpenXml/Presentation` is a 404 — that subfolder
    does not exist; per-class definitions are code-generated, so the
    practical lookup path for class/property metadata stays the NuGet
    intellisense XML.

## Audit findings

### Pass 1 — `deck/slides/*.py`

Reviewed all 11 slide modules (`s00`..`s11`). **No OOXML-driven
updates required at the slide layer.** The slide modules are
consumers of the `SlideBuilder` / `primitives` API — they call
`s.text(...)`, `s.connector(...)`, etc. They do not emit raw OOXML
themselves, so any spec-driven correction would land in
`primitives.py` or `builder.py`.

Indirect output cross-checked against ECMA-376 (Transitional set in
`deck/_schema/`):

- `<a:pPr>` child order (`lnSpc → spcBef → spcAft → bu*`) — primitives
  cites and follows the schema order (`primitives.py:113-114, 539-540`).
- `<p:sld> / <p:cSld> / <p:spTree>` ordering — correct.
- `<a:tcPr>` borders-before-fill — correct (CT_TableCellProperties).
- `<a:ln>` children (`solidFill → prstDash → tailEnd`) — correct
  (CT_LineProperties).
- Table style id `{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}` — documented
  "No Style, No Grid" GUID.
- `<a:endParaRPr>` placement — used only when paragraph has no runs,
  matches CT_TextParagraph.
- Bullet PANOSE `020B0604020202020204` for "Arial" — historically
  correct Arial PANOSE.

Non-OOXML observations surfaced incidentally and reported in chat
only (not fixed this session — content/structure, not spec):

1. Section dividers `s08_divider_layers.py` and
   `s11_divider_direction.py` promise downstream content (s10 "other
   GFE"; s12/s13) that is missing from `slides/`. They were added
   subsequently to support `build.py` registration —
   `s10_other_gfe.py`, `s12_hii_outsourcing.py`, `s13_navy_50pct.py`,
   `s14_method_sources.py` all now exist (visible in the SLIDES list
   in `build.py`).
2. `s07_top_vendors.py:62` title says "absorb most of the visible
   flow"; caption math computes ~41%. Substantial share, not "most" —
   wording-only inconsistency.

### Pass 2 — `deck/{build,builder,style,validate,primitives}.py`

Five findings worth acting on, four small enough to fix in this
session:

1. **`build.py` `core_xml()` doesn't escape `<dc:title>`**
   (was `build.py:255`). XML-injection latent: if `deck_title`
   ever contains `<`, `>`, `&`, `"`, or `'`, the literal
   interpolation breaks the XML and PowerPoint refuses to open.
   Dormant today (only caller passes the default literal).

2. **`build.py` `<p:sldSz>` omits the `type` attribute**
   (was `build.py:305`). Per CT_SlideSize, `type` defaults to
   `"custom"`. For a 16:9 widescreen canvas the semantic value is
   `"screen16x9"`; some renderers (Keynote, older LibreOffice)
   handle the explicit value more uniformly.

3. **`primitives.py` `<a:fld>` uses a hard-coded GUID**
   (was `primitives.py:605`). The literal was
   `id="{{{{00000000-0000-0000-0000-000000000000}}}}"` in the
   f-string — this had two bugs at once:
   - f-string `{{{{...}}}}` resolves to `{{...}}` (double braces)
     in the rendered XML, but OOXML expects single braces
     `id="{GUID}"`.
   - Even with single braces, all fields sharing the same GUID
     causes PowerPoint to coalesce field values per the OpenXML
     SDK `Field.Id` docs.
   Latent — `run()`'s public signature does not expose a `field`
   parameter, so no slide module currently triggers this path.

4. **`validate.py` `_HINTS`** does not cover two common ordering
   errors that show up in hand-written PPTX:
   - `<a:endParaRPr>` must be the last child of `<a:p>`.
   - `<a:lstStyle>` must sit between `<a:bodyPr>` and the first
     `<a:p>` inside `<p:txBody>`.

5. **`primitives.py` has no `<a:br>` support and `picture()` only
   handles `r:embed` (not `r:link`).** Both are feature omissions,
   not bugs. Not currently needed by any slide. Left as-is.

`builder.py` and `style.py` had no spec-driven items — `builder.py`
is a bounds/fill/sp_id checker over primitives (doesn't emit XML
itself); `style.py` is design tokens only and its unit comments are
accurate.

## Fixes applied

### 1. `build.py` — escape `<dc:title>` content

`build.py:37` — added stdlib import:
```python
from xml.sax.saxutils import escape as xml_escape
```

`build.py:256` — wrapped interpolation:
```diff
- f'<dc:title>{title}</dc:title>'
+ f'<dc:title>{xml_escape(title)}</dc:title>'
```

### 2. `build.py` — `<p:sldSz type="screen16x9"/>`

`build.py:305`:
```diff
- f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}"/>'
+ f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>'
```

Verified in build output:
```
<p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
```

### 3. `primitives.py` — unique `<a:fld>` GUIDs + brace fix

`primitives.py:23-24` — added stdlib import:
```python
import uuid
```

`primitives.py:605-613` — rewrite the field branch:
```diff
  if "field" in r:
+     # Each <a:fld> needs a unique GUID per ECMA-376 / OpenXML SDK
+     # Field.Id docs; PowerPoint coalesces fields that share an id.
+     field_id = r.get("field_id") or uuid.uuid4()
      return (
-         f'<a:fld id="{{{{00000000-0000-0000-0000-000000000000}}}}" type="{r["field"]}">'
+         f'<a:fld id="{{{field_id}}}" type="{r["field"]}">'
          f'{rpr}<a:t>{esc(text)}</a:t></a:fld>'
      )
```

The `field_id` override (`r.get("field_id")`) lets a caller pass a
deterministic id if needed; default is a fresh `uuid.uuid4()` per
field. The f-string now renders single braces, matching what
PowerPoint expects.

### 4. `validate.py` — two more hint entries

`validate.py:57-58` — appended to `_HINTS`:
```python
"endParaRPr": "<a:endParaRPr> must be the last child of <a:p>, "
              "after all <a:r>/<a:br>/<a:fld> children.",
"lstStyle":   "<p:txBody> requires <a:lstStyle> between <a:bodyPr> "
              "and the first <a:p>: bodyPr, lstStyle, then p+.",
```

These now print author-facing fix instructions when an lxml schema
violation reports those element names as unexpected — same pattern
as the existing entries for `spcAft`, `solidFill`, `prstDash`, etc.

## Verification

`python3 build.py` ran cleanly with schema validation on (default).
Wrote `out/destroyer_deck.pptx`. Spot-checked the two `build.py`
fixes against the packed output:

```
sldSz: <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
title: <dc:title>Destroyer Outsourced Construction</dc:title>
```

(Title shown unescaped because the default has no special chars; the
`xml_escape` path is exercised on any title with `<>&"'`.)

The `<a:fld>` fix is dormant — no slide module currently emits a
field — but the brace-count bug is gone and the next field-bearing
run will get a unique GUID.

## Files touched

```
deck/build.py        — 2 edits  (xml_escape import; dc:title; sldSz type)
deck/primitives.py   — 2 edits  (uuid import; <a:fld> GUID logic)
deck/validate.py     — 1 edit   (_HINTS for endParaRPr, lstStyle)
```

No slide modules changed. No new files. No dependency changes.

## Notes for next session

- If field-bearing runs ever get used (page numbers, dates), expose
  `field=` and optionally `field_id=` on the `run()` public signature
  — currently `_emit_run` checks `r["field"]` but `run()` doesn't
  accept it as a kwarg.
- The `validate.py` `_HINTS` dict is a low-friction place to add
  more rules as new schema-order traps surface during build.
- Title-Case structural gaps in the deck (missing s10/s12/s13 at the
  time of audit, plus the s07 "most" wording) were noted in chat but
  not in scope for this session. The content-track session
  (`deck_build_session_2026-05-25_pt3.md`) is the right venue.
