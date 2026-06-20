# Faithful Deck Port Methodology — reproducing a real .pptx as native `deck_core` slide modules

> How to take an existing, hand-built (often think-cell-laden) PowerPoint deck and
> re-author it, slide by slide, as native Python modules on the shared `deck_core`
> engine — so the output is a **pixel-faithful reproduction** of the source, not a
> re-skin. Written from the MRO v3.3 → `deck_mro` port (June 2026). Applies to any
> `projects/<name>/deck/` pipeline in `ooxml_build_pipelines_light`.

---

## 0. The one idea

**Drive every slide module from the source slide's actual OOXML — its exact EMU
geometry, fills, fonts, tables, and shapes — and re-emit equivalent OOXML through
`deck_core` primitives.** You are a *transcriber of the shape tree*, not a designer.

The failure mode this avoids: looking at a rendered PNG, inventing a "house-style"
layout that conveys the same content, and shipping something that doesn't look like
the source. That gets rejected ("those slides don't look like the real ones"). The
fix is to stop eyeballing renders and start reading XML.

A faithful port has three properties:
1. **Same coordinates.** Shapes land at the source's `a:off` / `a:ext` (in EMU).
2. **Same styling.** Same fills (resolve theme scheme colors to hex), fonts, sizes,
   borders, bullet levels.
3. **Same structure.** A source table becomes a `table()`; a source ellipse becomes
   `prst="ellipse"`; a source bent connector becomes a `cxnSp`. Like for like.

---

## 1. Mental model & inputs

```
source.pptx ──unzip──▶ src_xml/ (the ground truth)
     │                     │
     │                  dump_slide.py N  ──▶ shape tree: geometry, fills, text, tables
     │                     │
     └──soffice/pdftoppm──▶ src_png/src-NN.png (visual reference for QA diffing)

deck_core (shared engine)  ──primitives/charts──▶  deck_<name>/slides/<slide>.py
                                                          │
                                          build_deck.py ──▶ output.pptx
                                                          │
                                       render.sh N ──▶ _qa/png/slide-N.png  (compare to src-NN)
```

You need three things before writing any module:
- the **source deck** unzipped (`src_xml/`),
- the **`deck_core` API** in your head (see §6 and `deck_core/slide_guide.md`,
  `slide_snippets.md`, `primitives.py`, `charts.py`),
- the **layout map** between the source's layouts and `infra/template`'s (see §4).

---

## 2. One-time setup (per deck port)

Work inside the pipeline's deck dir, e.g. `projects/mro/deck/`. Create a scratch
`_qa/` area (kept out of the build — `build_pptx` only bundles real assets):

```bash
cd projects/<name>/deck
mkdir -p _qa && cd _qa
mkdir -p src_xml && (cd src_xml && unzip -q "/path/to/source.pptx")
```

Then drop in the two tools below.

### 2a. `_qa/dump_slide.py` — the primary instrument

Reads one slide's XML and prints every shape with id/name, preset geometry,
EMU+inch geometry, fill, line, text runs (with size/bold/italic/color), and full
table structure (column widths, per-row heights, per-cell fill + span + text). This
is what you read before building a slide — **not the PNG.**

```python
"""Dump a source slide's shape tree. Usage: python dump_slide.py <N>"""
import sys
from xml.etree import ElementTree as ET
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
def q(ns, t): return f'{{{ns}}}{t}'
n = sys.argv[1]
root = ET.parse(f"src_xml/ppt/slides/slide{n}.xml").getroot()
def emu_in(v):
    try: return f"{int(v)/914400:.2f}in"
    except Exception: return v
def fill_of(spPr):
    if spPr is None: return None
    sf = spPr.find(q(A,'solidFill'))
    if sf is not None:
        c = sf.find(q(A,'srgbClr'));  sc = sf.find(q(A,'schemeClr'))
        if c is not None: return f"#{c.get('val')}"
        if sc is not None: return f"scheme:{sc.get('val')}"
    if spPr.find(q(A,'noFill')) is not None: return "none"
    if spPr.find(q(A,'gradFill')) is not None: return "gradient"
    return None
def geom_of(spPr):
    if spPr is None: return ("","")
    g = spPr.find(q(A,'prstGeom'))
    prst = g.get('prst') if g is not None else ("custom" if spPr.find(q(A,'custGeom')) is not None else "")
    xf = spPr.find(q(A,'xfrm'))
    if xf is None: return (prst, "")
    off, ext = xf.find(q(A,'off')), xf.find(q(A,'ext'))
    if off is None or ext is None: return (prst, "")
    return (prst, f"off=({off.get('x')},{off.get('y')}) ext=({ext.get('cx')},{ext.get('cy')}) "
                  f"[{emu_in(off.get('x'))},{emu_in(off.get('y'))} {emu_in(ext.get('cx'))}x{emu_in(ext.get('cy'))}]")
def text_of(txBody):
    out = []
    if txBody is None: return out
    for p in txBody.findall(q(A,'p')):
        pPr = p.find(q(A,'pPr')); algn = pPr.get('algn') if pPr is not None else None
        lvl = pPr.get('lvl') if pPr is not None else None
        runs = []
        for r in p.findall(q(A,'r')):
            rPr, t = r.find(q(A,'rPr')), r.find(q(A,'t'))
            txt = t.text if t is not None else ""
            props = []
            if rPr is not None:
                if rPr.get('sz'): props.append(f"{int(rPr.get('sz'))/100}pt")
                if rPr.get('b') == '1': props.append("b")
                if rPr.get('i') == '1': props.append("i")
                sf = rPr.find(q(A,'solidFill'))
                if sf is not None:
                    c = sf.find(q(A,'srgbClr'))
                    if c is not None: props.append(f"#{c.get('val')}")
            runs.append((txt, ",".join(props)))
        if runs or algn: out.append((algn, lvl, runs))
    return out
def walk(sp, depth=0):
    ind = "  " * depth
    tag = sp.tag.split('}')[-1]
    if tag in ('sp','pic','cxnSp','graphicFrame'):
        nv = sp.find('.//'+q(P,'cNvPr'))
        name = nv.get('name') if nv is not None else "?"; nid = nv.get('id') if nv is not None else "?"
        spPr = sp.find(q(P,'spPr')); prst, g = geom_of(spPr); fill = fill_of(spPr)
        ph = sp.find('.//'+q(P,'ph')); phs = f" PH[{ph.get('type')},idx={ph.get('idx')}]" if ph is not None else ""
        if tag == 'graphicFrame':
            xf = sp.find(q(P,'xfrm'))
            if xf is not None:
                off, ext = xf.find(q(A,'off')), xf.find(q(A,'ext'))
                g = f"off=({off.get('x')},{off.get('y')}) ext=({ext.get('cx')},{ext.get('cy')})"
            tbl = sp.find('.//'+q(A,'tbl'))
            print(f"{ind}[{tag}:{'TABLE' if tbl is not None else 'GRAPHIC'}] id={nid} '{name}'{phs} {g}")
            if tbl is not None:
                grid = tbl.find(q(A,'tblGrid'))
                cols = [c.get('w') for c in grid.findall(q(A,'gridCol'))]
                print(f"{ind}  cols={cols} ({[emu_in(c) for c in cols]})")
                for ri, tr in enumerate(tbl.findall(q(A,'tr'))):
                    cells = []
                    for tc in tr.findall(q(A,'tc')):
                        gs, hm, rs, vm = tc.get('gridSpan'), tc.get('hMerge'), tc.get('rowSpan'), tc.get('vMerge')
                        tcPr = tc.find(q(A,'tcPr')); cf = fill_of(tcPr) if tcPr is not None else None
                        txt = " | ".join("".join(r[0] for r in runs) for _,_,runs in text_of(tc.find(q(A,'txBody'))))
                        meta = "".join(x for x in [f"span{gs}" if gs else "", "hM" if hm else "",
                               f"rs{rs}" if rs else "", "vM" if vm else ""])
                        cells.append(f"{('['+cf+']') if cf else ''}{meta}:{txt}")
                    print(f"{ind}  r{ri}(h={tr.get('h')}): " + " || ".join(cells))
            return
        ln = spPr.find(q(A,'ln')) if spPr is not None else None
        lninfo = f" line(w={ln.get('w')},{fill_of(ln)})" if ln is not None else ""
        print(f"{ind}[{tag}] id={nid} '{name}'{phs} prst={prst} fill={fill}{lninfo} {g}")
        for algn, lvl, runs in text_of(sp.find(q(P,'txBody'))):
            rstr = "  ".join(f'"{t}"({p})' if p else f'"{t}"' for t, p in runs)
            if rstr.strip(' "'):
                print(f"{ind}    {('['+algn+']') if algn else ''}{('L'+lvl) if lvl else ''} {rstr}")
    for child in sp:
        if child.tag.split('}')[-1] in ('sp','pic','cxnSp','graphicFrame','grpSp'):
            walk(child, depth+1)
spTree = root.find(q(P,'cSld')+'/'+q(P,'spTree'))
for sp in spTree:
    if sp.tag.split('}')[-1] in ('sp','pic','cxnSp','graphicFrame','grpSp'):
        walk(sp)
```

When the table branch hides run-level detail (cell colors, bullet levels, multi-run
formatting) or you need connector `flipH/flipV/rot`/`avLst`, write a 15-line inline
`ElementTree` snippet for that specific question — don't over-build the dumper.

### 2b. `_qa/render.sh` — build-deck → PNG for QA

```bash
#!/bin/bash
set -e
PPTX="/abs/path/to/projects/<name>/<output>.pptx"
OUT="$(dirname "$0")/png"; mkdir -p "$OUT"
soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
if [ -n "$1" ]; then pdftoppm -png -r 96 -f "$1" -l "${2:-$1}" "$PDF" "$OUT/slide"
else pdftoppm -png -r 96 "$PDF" "$OUT/slide"; fi
```

Render the **source** deck once the same way into `_qa/src_png/src-NN.png` — those
are your visual diff targets. (`soffice`, `pdftoppm`, `rsvg-convert` are all
expected to be installed; see the `deck-image-pipeline` memory.)

### 2c. `_qa/extract_chart.py` — the static-chart / verbatim-table instrument

The third tool turns a slide's think-cell chart (and, in `--tables` mode, a dense
native table) into cleaned, fully static OOXML you read into the module. It's the
heart of §7 — see there for usage, the `<a:fld>`→`<a:r>` freeze, and the cleaning
rules. Full source lives next to `dump_slide.py`.

---

## 3. Per-slide workflow (the loop)

For each source slide N:

1. **`python _qa/dump_slide.py N`** — read the shape tree. Identify:
   - the **chrome** (breadcrumb / title / Preliminary chip / sources) — usually
     reproducible 1:1 with `deck_core` builders (see §5);
   - the **layout** the source slide uses (`slideN.xml.rels`) → map to
     `infra/template` (see §4);
   - the **body objects**: tables, shape diagrams, connectors, text blocks;
   - any **think-cell / OLE chart** region (see §7) → decide reproduce vs. blank.
2. **Pull extra detail** as needed (run colors, bullet `marL`/`lvl`, connector
   `rot`/`flip`, theme scheme colors → §8) with inline snippets.
3. **Write `deck_<name>/slides/<descriptive_name>.py`** — set `LAYOUT`, the chrome
   constants, and build `_body()` from `deck_core` primitives at the **exact source
   EMU coordinates**. Keep the source's text verbatim (apply only the agreed content
   decisions — see §9).
4. **Register** the module in `deck_<name>/slides/__init__.py` `SLIDE_RENDERS`, in
   slide order.
5. **`python build_deck.py`** — must stay green (`wrote … N slides`).
6. **`_qa/render.sh N N`** then **Read `_qa/png/slide-N.png`** side-by-side with
   `_qa/src_png/src-NN.png`. Fix coordinates/colors/sizes until they match.
7. Move to N+1.

Work in deck order; render in small batches (2–3 slides) to amortize the soffice
startup. Checkpoint progress to `logs/` + a `project`-type memory every few slides
(this work is long and context-heavy — see §11).

---

## 4. Layout discovery & mapping

The source deck and `infra/template` are usually the **same brand template** but
with **different layout numbering**. Never assume `slideLayout4` means the same
thing in both. Discover it:

```bash
# which layout each source slide uses
for i in $(seq 1 N); do
  echo "slide$i -> $(grep -o 'slideLayout[0-9]*\.xml' src_xml/ppt/slides/_rels/slide$i.xml.rels | head -1)"
done
# source layout names
for f in src_xml/ppt/slideLayouts/slideLayout*.xml; do
  echo "$(basename $f): $(grep -o '<p:cSld name=\"[^\"]*\"' $f | head -1)"; done
# infra/template layout names (the ones you actually set LAYOUT= to)
for f in ../../../infra/template/ppt/slideLayouts/slideLayout*.xml; do
  echo "$(basename $f): $(grep -o '<p:cSld name=\"[^\"]*\"' $f | head -1)"; done
```

Match by **layout name**, not number. (MRO example: source `Light Blank`=layout13
maps to template `slideLayout4`; source `50% Block + Title`=layout12 maps to
template `slideLayout3`.) Set `LAYOUT = "slideLayoutK"` on the module to the
*template's* number. **Background panels come from the layout** — e.g. the dark-left
half of a "50% Block" slide is painted by the layout, so you place only the
foreground shapes, never the panel.

---

## 5. Chrome — usually free

For "content" slides, these `deck_core` builders reproduce the standard chrome
(verify once against a `src_png` and then trust it):

```python
breadcrumb(SECTION, TOPIC)            # "TAM / Definitions" (bold section + " / " + topic)
prelim_chip()                         # the "Preliminary" yellow box, top-right
title_placeholder(TOPIC, TAKEAWAY)    # "Topic | Finding." 20pt
sources_line(text)                    # bottom source line — pass the source's own string
```

A well-built source deck already writes titles as `Topic | Finding.` and headers as
`Section / Topic` — so the mapping is literally copy the strings out of the dump.
Slides on a special layout (cover, section divider, a 50%-block intro) skip these
and place their own title/labels at the dumped coordinates.

> Footnote vs. sources line: if the source has a custom full-width footer at its own
> `y` (e.g. an 8pt "Note: … Source: …"), reproduce it as a `text_box` at those exact
> coords rather than `sources_line()` (which sits at the standard `SOURCES_Y`).

---

## 6. Reproduction cookbook (source shape → `deck_core`)

| Source shape (in the dump) | Reproduce with |
|---|---|
| `[sp] prst=rect fill=#hex` text | `text_box(id,name,x,y,cx,cy,[paragraph([run(...)])], fill=hex, ...)` at source coords |
| `[sp] prst=ellipse` (rings) | `text_box(..., prst="ellipse", fill=BLUE_n, line_color="C0C0C0", line_width=3175, [paragraph([])])` |
| `[sp] prst=wedgeRectCallout` | `text_box(..., prst="wedgeRectCallout", fill=..., ...)` |
| `[cxnSp] prst=straightConnector1 ... tail=triangle` | `connector(id,name,x,y,cx,cy, color=BLACK, arrow=True)` |
| `[cxnSp] prst=bentConnector3 rot=... ` (think-cell elbow) | **raw `<p:cxnSp>`** with the exact `xfrm rot/off/ext` + `prstGeom bentConnector3` + `<a:ln>… <a:tailEnd type="triangle"/>` (see below) |
| `[graphicFrame:TABLE]` no merges | `house_table(id,name,x,y,col_w,rows, row_h=[...per source...], table_skin="rule"/"dark"/"light", aligns=[...])` |
| `[graphicFrame:TABLE]` with `spanN`/`rs`/`vM` | low-level `table()/trow()/tcell(grid_span=, row_span=)` — the engine synthesizes hMerge/vMerge fillers; provide only the spanning cell |
| greyed / highlighted cells | `house_table(..., cell_fills={(r,c):GRAY_1}, cell_text_colors={(r,c):GRAY_4}, cell_bold={...})` |
| rotated label in a thin table column | overlay a `text_box(..., rot=16200000)` (270°) over the column band; size `cx=band_len, cy=col_w` centered on the band |
| bulleted body with indent levels | `paragraph(runs, bullet=True, mar_l=<source marL>, indent=-<hang>)` for L0; manual `"–  "` prefix + `mar_l=<deeper>` (no bullet) for the dash sub-bullets |
| image / logo / photo | `picture()` + a module-level `IMAGES=[{"rId":"rId2","file":...}]` (see `deck-image-pipeline` memory) |

**Raw elbow connector** (faithful think-cell down-flow). The source uses
`rot="5400000"` and shape-anchored endpoints (`stCxn`/`endCxn`); strip the anchors
so it renders statically from the `xfrm` alone:

```python
def _elbow(sp_id, x, y, cx, cy):
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sp_id}" name="Elbow{sp_id}"/>'
            '<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>'
            f'<a:xfrm rot="5400000"><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="bentConnector3"><a:avLst/></a:prstGeom>'
            f'<a:ln><a:solidFill><a:srgbClr val="{DK}"/></a:solidFill>'
            '<a:tailEnd type="triangle"/></a:ln></p:spPr></p:cxnSp>')
```

Raw OOXML is fully allowed in `_body()` — `deck_core.slide()` declares the `a:`/`p:`
namespaces, so any `<p:sp>` / `<p:cxnSp>` / `<p:graphicFrame>` string drops straight
in. Use it whenever a primitive doesn't fit; prefer copying the source element
verbatim (renumber the `id`) for exotic geometry.

**Low-level merged table** essentials (`from deck_core.primitives import table, trow,
tcell, tcell_rich, tpara, trun`):
- `tcell(text, grid_span=N)` spans N columns; **omit** the covered cells in that row.
- `tcell(..., row_span=N)` spans N rows; **omit** the covered cell in the next row(s).
- multi-paragraph cell → `tcell_rich([tpara([trun(line, size=...)]) for line in lines], anchor="t")`.
- pass per-source `row_h` list; `table(... , cx=sum(col_w), cy=sum(row_h))`.

---

## 7. think-cell / OLE charts — reproduce them STATICALLY by transcription

The source's stacked bars, Marimekkos, funnels, and waterfalls are **think-cell
OLE embeds**. The load-bearing fact: think-cell *also emits the rendered chart as
ordinary native shapes* right next to the OLE blob. The bar segments are plain
`<p:sp>` rectangles with `fill=scheme:accentN`; the axes are `<p:cxnSp>`
connectors; every data / axis / legend label is a "Text Placeholder" whose text
lives in an `<a:fld>` field. So you do **not** rebuild the chart from its data —
you **transcribe the shapes think-cell already drew**, drop the OLE, and freeze
the fields. The result is a pixel-faithful, fully static chart with no think-cell
dependency. (This supersedes the deck's earlier "leave the chart area blank"
decision — the MRO user asked for the chart reproduced statically.)

Identify a think-cell chart in the dump by: a `graphicFrame` named `think-cell
data - do not delete` (the OLE — discard it), plus a cluster of
`fill=scheme:accentN` rectangles, `prst=line` connectors, and many `Text
Placeholder 25` shapes whose text the `[sp]` dump shows as *empty* (because it's
in `<a:fld>`, not `<a:r>` — the dumper only reads runs).

### The tool — `_qa/extract_chart.py` (full source committed beside `dump_slide.py`)

Two modes, both run from `_qa/` and writing to the slides package:

```bash
# chart mode: emit the bar/axis/label shapes (drops OLE + the keep-out shapes)
python extract_chart.py <N> --keepout 2,5,6,7,9,67 --offset 300 \
    > ../deck_<name>/slides/_chart_xml/slideNN.xml
# table mode: emit ONLY the named <a:tbl> graphicFrame(s), verbatim + cleaned
python extract_chart.py <N> --tables 7 --offset 300 \
    > ../deck_<name>/slides/_chart_xml/slideNN_table.xml
```

`--keepout` = the source cNvPr ids you rebuild as deck_core primitives instead
(chrome / table / caption / footer); they're skipped. `--offset` is added to every
`cNvPr id`. It does a balanced top-level scan of the `spTree` (handles nested
`grpSp`), so it never needs an XML parse that would mangle namespace prefixes.

**What the cleaner does, and why each step matters:**
- **Freeze every `<a:fld>` → `<a:r>`.** think-cell stores each label in a field
  with a *bogus* `type="datetime…"` attribute holding the cached text (`100%`,
  `$16,996M`, `USCG ISVS`). Real PowerPoint can **refresh** a datetime field to
  today's date and destroy the label, so each field is rewritten to a plain static
  run (its `rPr` + cached `<a:t>`, inner `<a:pPr>` dropped). This is *the* reason
  "static" is more than cosmetic — verify the tool reports `live <a:fld>=0`.
- **Strip cruft:** think-cell `<p:custDataLst>` tags, the `a16:creationId` /
  `a14:hiddenFill` / dsbld `cellmeta` `<a:extLst>` (and the `<p:extLst>` modId on a
  table frame), and the bulky inherited `<a:lstStyle>` on each label (its default
  sizes are overridden by the run, so it's dead weight).
- **Strip connector glue.** `<a:stCxn>`/`<a:endCxn>` anchor a `<p:cxnSp>` to other
  shapes *by id* — but we renumber ids, so the glue would dangle and the renderer
  may drop the connector to the origin. Removing it makes the connector render
  statically from its own `xfrm` (off/ext/rot/flip), which is exact (same idea as
  the §6 raw-elbow recipe, applied to every transcribed connector).
- **Strip hyperlinks.** `<a:hlinkClick>`/`<a:hlinkHover>` reference a slide rel by
  `r:id` we don't carry; the run's own `rPr` fill already fixes the visible color,
  so dropping the link leaves the text identical but self-contained (no dangling
  rel → no PowerPoint repair).
- **Resolve `schemeClr` + `lumMod`/`lumOff` → literal `<a:srgbClr>`.** A *plain*
  `schemeClr accentN/tx1/...` is kept as-is (theme is byte-identical to
  `infra/template` — verify once, §8 — so it resolves to the same hex). But a
  `schemeClr` carrying `lumMod`/`lumOff` (the trick a source uses to make a
  light/medium/dark ramp from one theme color) is **baked to an explicit hex** via
  the HLS lum transform, because **soffice mis-renders `schemeClr`+`lumOff`** (it
  darkens instead of lightening, so e.g. a `tx1`+`lumMod10`+`lumOff90` light-navy
  box comes out near-black). Baking it makes the fill render identically in soffice
  and PowerPoint. (`lumMod`-only, no `lumOff`, happens to render fine — but it's
  resolved too for consistency.) This was the fix for slide 4's wrong box fills.
- **Renumber `cNvPr id += offset`** (default +300) so chart ids can't collide with
  chrome (breadcrumb=2, title=3, prelim=4, sources=9999) or the module's own
  primitive ids. The tool also asserts no `r:id`/`r:embed` survives (so no slide
  rels are needed).

The same cleaning runs in `--tables` mode (a verbatim `<a:tbl>` also gets its
hyperlinks stripped and its `lumMod`/`lumOff` cell fills baked). `_qa/regen_charts.sh`
records the exact `--keepout`/`--tables` args per slide, so every `_chart_xml/`
file can be rebuilt deterministically after a tool change — re-run it, rebuild,
re-render. **Watch the render cache:** `render.sh` reuses a stale PDF if one is
present; `rm _qa/png/*.pdf` before re-rendering after a rebuild.

### Wiring it into the slide module

The cleaned dumps are large (tens of KB of *real source XML*), so store them as
package data beside the slides and read them at render time — NOT inlined, and NOT
an OPC part, so `build_pptx` won't try to bundle them:

```python
_XML = Path(__file__).parent / "_chart_xml"
_CHART = (_XML / "slideNN.xml").read_text(encoding="utf-8")          # static bars+labels
_TABLE = (_XML / "slideNN_table.xml").read_text(encoding="utf-8")    # verbatim <a:tbl>
...
def _body() -> str:
    return caption + _TABLE + footer + _CHART   # _CHART last: labels paint over bars
```

Each chart shape carries its own `xfrm`, so the block drops in with no coordinate
work; source z-order (bars → connectors → labels) is preserved by the tool, so put
`_CHART` after anything it must overlay.

### Dense source tables → transcribe verbatim too (`--tables`)

A deck_core `table()` is great for ≤ a handful of rows, but `_emit_cell` hardcodes
`marT/marB=45720` and paragraphs default to 115% line spacing — a per-row tax that
**overflows the slide** on a dense (~20-row) source table whose cells use
`marT/marB=0` at 100% spacing. Don't fight it: transcribe the native `<a:tbl>`
verbatim with `--tables <id>`. The cleaner swaps the source's custom
`tableStyleId` for the built-in **No Style, No Grid** GUID
(`{2D5ABB26-0587-4C30-8999-92F81FD0307C}`, the same one `deck_core.table()` uses)
so the table keeps its explicit per-cell fills/borders (e.g. a `bg1`+`lumMod50`
grey total row) and picks up no fallback grid lines — and needs no `tableStyles.xml`
entry. Read it like `_TABLE` above. Reserve the primitive `table()`/`house_table()`
for tables you're authoring fresh or that are short enough not to overflow.

> Still on the table: if you ever DO want a *live, editable* chart instead, rebuild
> as a native `deck_core` chart (`column_chart(mode="stacked")`, `marimekko_chart`,
> `waterfall_chart`) via a module-level `CHARTS=[...]` + `graphic_frame(rId=...)`
> (see `charts.py`). That's much more work and changes the data-provenance story —
> the verbatim-shape transcription above is the faithful-port default.

---

## 8. Resolving colors

Source fills come in three forms in the dump:
- `fill=#223E59` — literal hex, use as-is (`fill="223E59"`).
- `fill=scheme:tx1` / `scheme:bg2` — a **theme** color; resolve it once from
  `src_xml/ppt/theme/theme1.xml`'s `<a:clrScheme>`. PowerPoint maps `tx1→dk1`,
  `bg1→lt1`, `tx2→dk2`, `bg2→lt2`. (MRO theme: dk1=`162029`, lt1=`FFFFFF`,
  dk2=`44505C`, lt2=`F2F6FA`; accents 1-6 = `79838F/1D4D68/486D82/89A2B0/AFC2CC/D8E3EB`.)
- the `deck_core.style` ramps line up with common brand hexes — know these by heart:
  `BLUE_1..5 = E2E9EF / B6C8D8 / 6E91B1 / 3D5972 / 263746`;
  `GRAY_1..5 = F2F2F2 / D9D9D9 / BFBFBF / 7F7F7F / 646464`; `DK = 162029`,
  `WHITE = FFFFFF`, `PRELIM = FFFFCC`. So `#F2F2F2`→`GRAY_1`, `#7F7F7F`→`GRAY_4`,
  `#162029`→`DK`, etc. Prefer the token; fall back to a literal hex for off-ramp
  colors like `#99B9D8`, `#F2F6FA`, `#223E59`.

---

## 9. Content decisions (lock these with the user up front)

These recur and change text on most slides — agree once, apply everywhere:
- **De-identification / renaming** (e.g. a placeholder "BuildCo" → the real client
  "Saronic"). Apply consistently; fix lone source inconsistencies.
- **Working-session artifacts** (e.g. yellow "DISCUSS:" analyst-question callouts) —
  usually **drop** for a clean deliverable.
- **think-cell charts** — **reproduce statically** by transcribing the emitted
  shapes (§7); the old "leave blank" default was superseded mid-port.
- Otherwise keep the source text **verbatim**, including its own wording choices
  ("USN / USCG", "$9.0B", footnote "Note: …") — faithfulness beats house-style copy
  edits in a *port*.

---

## 10. QA / done-ness bar

A slide is done when `_qa/png/slide-N.png` and `_qa/src_png/src-NN.png` are visually
indistinguishable at the structural level: same blocks in the same places, same
fills, same text, same table shape. Small wrap/round-off differences are fine; moved
blocks, wrong fills, or invented layouts are not. The build must be green and the
deck must open in PowerPoint without "Repair" (the `build_pptx` OPC guard enforces
declared content types — keep only real assets in `images/`).

Useful checks:
- `slide_probe` (`deck_core/slide_probe.py`) dumps the geometry of YOUR built slide
  from its emitted XML — a programmatic cross-check of fills/borders/anchors/tables.
- Re-render at `-r 150` and crop with Pillow to inspect a dense region (tiny table
  text, rotated labels).

---

## 11. Resume / extend (long-running port hygiene)

This is multi-session work. Protect it:
- After every few slides, append to `logs/<date>_<deck>_native_port.md`: what's done,
  what's left, and **per-remaining-slide source notes** (object inventory + which
  regions are think-cell-blank). Keep a `project` memory pointing at the log.
- The registry (`SLIDE_RENDERS`) is the source of truth for order and progress — a
  slide is "in" the deck once registered.
- To continue: read the log, `dump_slide.py` the next slide, build, render, compare,
  register, repeat.

---

## 12. Worked references (MRO port)

- `deck_mro/slides/overview.py` — special `slideLayout3` (50% dark-left from the
  layout); light-on-dark / dark-on-white columns; L0 • + L1 en-dash bullets; yellow
  prelim note. *No* breadcrumb/title chrome.
- `deck_mro/slides/definitions.py` — 5 concentric `prst="ellipse"` rings (exact
  blue-ramp + `C0C0C0` borders) + centered labels + a `house_table` with greyed
  future-effort rows.
- `deck_mro/slides/bottom_up_approach.py` — 3-row Input→Filter→Output grid: light /
  dark boxes, `connector(arrow=True)` straight arrows, raw `bentConnector3` elbows,
  italic column headers + rules, left-column step descriptions.
- `deck_mro/slides/vessel_taxonomy.py` — one big low-level `table()` with gridSpan
  header band, per-cell category fills, multi-paragraph classification cells, and
  rotated (`rot=16200000`) column labels overlaid on a thin first column.
- `deck_mro/slides/topdown_detail.py` (slide 8) — **the canonical static-chart +
  verbatim-table slide** (§7): reads `_chart_xml/slide08.xml` (the frozen
  think-cell stacked bar) and `_chart_xml/slide08_table.xml` (the verbatim 20-row
  rollup `<a:tbl>`); only the caption + footer are deck_core primitives.
- `deck_mro/slides/work_segments.py` / `tam_composition.py` / `fleet_mro.py` — side
  table / commentary reproduced as primitives, with the think-cell stacked bar /
  Marimekko read in statically the same way as slide 8.
- `deck_mro/slides/topdown_funnel.py` (slide 9) — **the native-chart path**: the
  source funnel is a real `<c:chart>` part (not think-cell shapes), so chart1.xml is
  bundled verbatim via `CHARTS=[{"chart_xml": ...}]` (its `<c:externalData>` stripped)
  and placed with `graphic_frame(rId="rId2", ...)`; the neck connectors / labels /
  commentary are transcribed.
- `deck_mro/slides/private_addressable.py` / `reconciliation_bridge.py` /
  `fleet_structure.py` / `contract_vehicles.py` — chrome via builders, then verbatim
  transcription of every BLD-authored shape (tiles / callouts / numbered ovals) and
  `--tables` for the dense tables; analyst "DISCUSS" review-stickies dropped via
  `--keepout`.
- `deck_mro/slides/sam_sizing.py` (slide 14) — the "Blank" layout (`slideLayout5`)
  case: chrome is transcribed verbatim with the body (no placeholder-bound builders).

Status: MRO port COMPLETE — all 15 slides ported & visually verified faithful; build
green (15 slides, 1 native chart); deck round-trips through soffice without repair; no
live `<a:fld>` / dangling rels / think-cell residue anywhere. Memory:
`mro-deck-native-port`.
