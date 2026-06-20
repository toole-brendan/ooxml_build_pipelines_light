# Agent reference cache

Vendored OOXML reference material an agent can grep / Read directly
to answer "what does this element / class / attribute mean?" without
hitting the network. Companion to `deck/_schema/` (the ECMA-376 XSDs).

See **"How to query the cache"** at the bottom for the grep one-liners.

## Contents

```
_docs/
├── open-xml-docs/              # OfficeDev/open-xml-docs markdown (curated)
│   ├── presentation/  (10)         # PresentationML conceptual topics
│   └── general/        (4)         # OPC packaging + markup-compatibility
├── intellisense/
│   └── DocumentFormat.OpenXml.PresentationAndDrawing.xml
│                                   # NuGet intellisense XML, filtered
│                                   # to Presentation + Drawing + Packaging
│                                   # (~3.9 MB, ~11k members)
├── xref/
│   └── element_urls.json           # every <ns:tag> emitted in primitives.py
│                                   # → SDK class FQN + Microsoft Learn URL
└── _build_element_urls.py      # regenerate xref/element_urls.json
                                # (run when primitives.py adds a new emitted tag)
```

The markdown set is **deliberately curated** to the conceptual / structural
files (`structure-of-*.md`, `working-with-*.md`, packaging overviews). The
upstream repo's `how-to-*.md` files are Open XML SDK C# tutorials — useful
to .NET developers but irrelevant to this pipeline, which emits raw OOXML
strings in Python and never instantiates an SDK class. The migration topic
(SDK v2 → v3) is dropped for the same reason. To re-include any of the
dropped topics, add the filename to the `presentation` or `general` curl
loop in the "How the cache was built" section below.

## Provenance

| Source | Origin | Pinned version |
|---|---|---|
| OfficeDev/open-xml-docs markdown | `https://github.com/OfficeDev/open-xml-docs` (raw URLs under `docs/`) | `main` (file list captured 2026-05-25; see "How the cache was built" below) |
| DocumentFormat.OpenXml intellisense | NuGet `DocumentFormat.OpenXml`, `lib/net8.0/DocumentFormat.OpenXml.xml` | `3.5.1` (override with `--nuget-version`) |
| Element → Learn URL map | Generated from intellisense; one entry per `<ns:tag>` emitted in `primitives.py` | — |

ECMA-376 Transitional XSDs live separately in `deck/_schema/` (vendored
from QtExcel/ecma-376-5th `457ce928`; see `_schema/README.md`).

## How the cache was built

The cache content under `open-xml-docs/` and `intellisense/` is vendored.
Refreshes are rare (ECMA-376 is frozen; the SDK ships on a slow cadence;
the conceptual markdown is mostly stable). When you do need to refresh —
bumping the SDK version, pulling new OfficeDev topics, or widening the
namespace filter — run these from the `deck/` directory:

```bash
# 1. Markdown — 14 curated OfficeDev/open-xml-docs topics.
BASE="https://raw.githubusercontent.com/OfficeDev/open-xml-docs/main/docs"
mkdir -p _docs/open-xml-docs/presentation _docs/open-xml-docs/general
for f in overview.md structure-of-a-presentationml-document.md \
         working-with-animation.md working-with-comments.md \
         working-with-handout-master-slides.md working-with-notes-slides.md \
         working-with-presentation-slides.md working-with-presentations.md \
         working-with-slide-layouts.md working-with-slide-masters.md; do
    curl -sfL -o "_docs/open-xml-docs/presentation/$f" "$BASE/presentation/$f"
done
for f in diagnosticids.md features.md \
         introduction-to-markup-compatibility.md overview.md; do
    curl -sfL -o "_docs/open-xml-docs/general/$f" "$BASE/general/$f"
done

# 2. Intellisense — pull the NuGet package, extract the .NET 8 XML doc,
#    filter to the namespaces this pipeline actually uses. Bump VERSION
#    to refresh; widen KEEP if you ever emit Word/Excel content.
VERSION=3.5.1
curl -sL -o /tmp/dox.nupkg \
  "https://api.nuget.org/v3-flatcontainer/documentformat.openxml/${VERSION}/documentformat.openxml.${VERSION}.nupkg"
mkdir -p _docs/intellisense
python3 - <<'PY'
import zipfile, xml.etree.ElementTree as ET
KEEP = ("DocumentFormat.OpenXml.Presentation",
        "DocumentFormat.OpenXml.Drawing",
        "DocumentFormat.OpenXml.Packaging")
with zipfile.ZipFile("/tmp/dox.nupkg") as z:
    raw = z.read("lib/net8.0/DocumentFormat.OpenXml.xml")
root = ET.fromstring(raw)
members = root.find("members")
for m in list(members):
    n = m.get("name", "")
    if len(n) < 2 or n[1] != ":" or not n[2:].startswith(KEEP):
        members.remove(m)
out = "_docs/intellisense/DocumentFormat.OpenXml.PresentationAndDrawing.xml"
ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=True)
print(f"wrote {out}: {sum(1 for _ in members)} members kept")
PY

# 3. Element → Learn URL map — regenerate from intellisense + primitives.py.
python3 _docs/_build_element_urls.py

# 4. Schemas — refresh procedure lives in _schema/README.md (separate vendoring).
```

The intellisense filter is the only non-trivial step; everything else is
plain curl / `_build_element_urls.py`. Drop in a new namespace prefix
(e.g., `"DocumentFormat.OpenXml.Wordprocessing"`) to widen coverage.

## What's NOT in this cache (deliberately)

- **WordprocessingML / SpreadsheetML topics.** The deck pipeline only
  emits PresentationML and DrawingML; the intellisense filter drops
  Word + Excel namespaces. If you ever extend the pipeline, widen the
  `KEEP` tuple in the rebuild snippet above.
- **Full `learn.microsoft.com/.xrefmap.json` (270 MB).** Verified to
  contain zero `DocumentFormat.OpenXml.*` entries — the OpenXml docs
  live in a separate docset that isn't part of that map. The handwritten
  `xref/element_urls.json` covers what we actually need.
- **ECMA-376 spec PDFs.** The XSDs in `_schema/` cover the structural
  content; markdown + intellisense cover the prose. The full PDF is
  better fetched on demand if a question truly can't be answered
  locally.
- **Live xref-query API integration.** `https://xref.docs.microsoft.com/query`
  exists but is per-call and requires careful header handling; the
  generated URL map covers every element `primitives.py` actually emits.

## How to query the cache

Run these from the `deck/` directory. Each one-liner targets a single
source; combine when you want the full picture on an element.

```bash
# XSD definitions — scope to DrawingML + PresentationML to skip wml/sml noise.
grep -n 'name="lnSpc"' _schema/dml-*.xsd _schema/pml.xsd

# Allowed children of a complex type (read the surrounding block).
grep -n -A 20 'complexType name="CT_TextParagraphProperties"' _schema/dml-main.xsd

# Conceptual prose — works on local names, namespaced names, and SDK classes.
grep -rn 'a:lnSpc\|SlidePart\|<p:sld>' _docs/open-xml-docs/

# SDK class for a qname (intellisense embeds "qualified name is a:lnSpc").
grep -B1 -A3 'qualified name is a:lnSpc' _docs/intellisense/*.xml

# Class summary by FQN.
grep -A2 'name="T:DocumentFormat.OpenXml.Drawing.LineSpacing"' _docs/intellisense/*.xml

# Microsoft Learn URL for an emitted element.
python3 -c "import json; print(json.load(open('_docs/xref/element_urls.json'))['elements']['a:lnSpc'])"

# Chart XSD — complex types for bar/line/doughnut and their parents.
grep -n 'complexType name="CT_BarChart"\|complexType name="CT_BarSer"\|complexType name="CT_CatAx"\|complexType name="CT_ValAx"\|complexType name="CT_Chart"' _schema/dml-chart.xsd

# Children of a chart complex type (read the surrounding block — useful when
# debugging the "Element X is not expected" schema errors that
# validate_chart_xml raises against deck/charts.py output).
grep -n -A 30 'complexType name="CT_BarChart"' _schema/dml-chart.xsd

# Chart-related conceptual / SDK lookups.
grep -B1 -A3 'qualified name is c:barChart' _docs/intellisense/*.xml
```

## Which source for which question

| Question | Source |
|---|---|
| "What are the valid children of `<a:pPr>`?" | XSD (`_schema/dml-main.xsd`) |
| "How do slide layouts inherit from masters?" | markdown (`_docs/open-xml-docs/presentation/working-with-slide-layouts.md`) |
| "What is `DocumentFormat.OpenXml.Drawing.LineSpacing`?" | intellisense (`_docs/intellisense/*.xml`) |
| "What's the Microsoft Learn URL for `<a:lnSpc>`?" | URL map (`_docs/xref/element_urls.json`) |
| "What does `mc:AlternateContent` mean?" | markdown (`_docs/open-xml-docs/general/introduction-to-markup-compatibility.md`) |
| "What's the child order of `<c:catAx>` / `<c:valAx>` / `<c:ser>`?" | chart XSD (`_schema/dml-chart.xsd`) — load `complexType name="CT_CatAx"` etc. |
| "Which chart types ship in `deck/charts.py`?" | source (`deck/charts.py` — stacked column, ranked column, waterfall) + README "Native OOXML charts" section in `deck/README.md` |
