# Native, Editable PowerPoint Charts in OOXML

A consolidated reference for generating **bar, grouped (clustered) bar, line, "gap" bar, and waterfall** charts as *native, editable* PowerPoint chart parts — not pasted pictures, not OLE blobs.

The headline: **four of the five are the same element with different attributes; waterfall is a completely different beast** (the "chartex" extended-chart family) that trips most people up. Get the package wiring right once and the classic types are template swaps; waterfall needs its own namespace, part, content type, and data model.

---

## 1. Package architecture (shared by all classic types)

A native chart isn't just XML on the slide — it's a small constellation of parts inside the `.pptx` ZIP, wired by relationships. The key OOXML convention: **the slide owns a chart part, and the chart part owns an embedded XLSX package used as the chart's data.** The XLSX is related *from the chart part*, not directly from the slide.

```text
/ppt/slides/slide1.xml                          ← <p:graphicFrame> references the chart by r:id
/ppt/slides/_rels/slide1.xml.rels               ← rel: slide → chart
/ppt/charts/chart1.xml                          ← the chart definition (c:chartSpace)
/ppt/charts/_rels/chart1.xml.rels               ← rels: chart → embedded xlsx, colors, style
/ppt/charts/colors1.xml                         ← color style (optional, but Office writes it)
/ppt/charts/style1.xml                          ← chart style (optional)
/ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx ← the real backing workbook
[Content_Types].xml                             ← content-type declarations
```

Microsoft's docs state that embedded chart data is stored as an embedded Spreadsheet object, and that the relationship targeted by `externalData/@r:id` is a **package relationship**.

### Relationship types and content types you must get right

| Part | Relationship type | Content type |
|---|---|---|
| chart (classic) | `…/relationships/chart` | `application/vnd.openxmlformats-officedocument.drawingml.chart+xml` |
| chart (waterfall) | `…/relationships/chart` | `application/vnd.ms-office.chartex+xml` |
| embedded xlsx | `…/relationships/package` | `…spreadsheetml.sheet` |
| colors | `…/2011/relationships/chartColorStyle` | `application/vnd.ms-office.chartcolorstyle+xml` |
| style | `…/2011/relationships/chartStyle` | `application/vnd.ms-office.chartstyle+xml` |

> Waterfall also has its own relationship type in the Microsoft 2014 namespace: `http://schemas.microsoft.com/office/2014/relationships/chartEx`.

### The graphic frame on the slide (classic charts)

```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>…</p:nvGraphicFramePr>
  <p:xfrm><a:off x="838200" y="365125"/><a:ext cx="7772400" cy="4525963"/></p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
      <c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
               r:id="rId2"/>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

---

## 2. Two non-negotiable conventions

**1. Cache everything.** Every data reference is a *pair*: a formula `<c:f>Sheet1!$B$2:$B$5</c:f>` **and** a cached copy (`<c:numCache>` / `<c:strCache>`). PowerPoint renders from the cache; the formula only matters when the user clicks "Edit Data." Omit the cache and many renderers show an empty or broken chart until refreshed. The cache must mirror the workbook, or you get stale display.

**2. Element order is law.** Every `CT_*` type is an XSD `<sequence>`. Emit children out of order and PowerPoint declares the file corrupt and offers to "repair" it (i.e., strip your chart). The orderings below are correct as written.

---

## 3. Bar / column — `c:barChart`

The confusing vocabulary: **`barDir` controls orientation, not the element name.**

- `<c:barDir val="col"/>` → vertical columns (what the PowerPoint UI calls "Column")
- `<c:barDir val="bar"/>` → horizontal bars (what the UI calls "Bar")

Here's a complete, valid `chartSpace` for a single-series column chart. The other classic types below only swap out the `<c:barChart>`/`<c:lineChart>` block, so **this is your template:**

```xml
<c:chartSpace
    xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <c:chart>
    <c:autoTitleDeleted val="1"/>
    <c:plotArea>
      <c:layout/>
      <c:barChart>
        <c:barDir val="col"/>
        <c:grouping val="clustered"/>
        <c:varyColors val="0"/>
        <c:ser>
          <c:idx val="0"/>
          <c:order val="0"/>
          <c:tx>
            <c:strRef>
              <c:f>Sheet1!$B$1</c:f>
              <c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>Revenue</c:v></c:pt></c:strCache>
            </c:strRef>
          </c:tx>
          <c:cat>
            <c:strRef>
              <c:f>Sheet1!$A$2:$A$5</c:f>
              <c:strCache>
                <c:ptCount val="4"/>
                <c:pt idx="0"><c:v>Q1</c:v></c:pt>
                <c:pt idx="1"><c:v>Q2</c:v></c:pt>
                <c:pt idx="2"><c:v>Q3</c:v></c:pt>
                <c:pt idx="3"><c:v>Q4</c:v></c:pt>
              </c:strCache>
            </c:strRef>
          </c:cat>
          <c:val>
            <c:numRef>
              <c:f>Sheet1!$B$2:$B$5</c:f>
              <c:numCache>
                <c:formatCode>General</c:formatCode>
                <c:ptCount val="4"/>
                <c:pt idx="0"><c:v>120</c:v></c:pt>
                <c:pt idx="1"><c:v>150</c:v></c:pt>
                <c:pt idx="2"><c:v>180</c:v></c:pt>
                <c:pt idx="3"><c:v>210</c:v></c:pt>
              </c:numCache>
            </c:numRef>
          </c:val>
        </c:ser>
        <c:gapWidth val="150"/>
        <c:overlap val="-27"/>
        <c:axId val="111111111"/>
        <c:axId val="222222222"/>
      </c:barChart>
      <c:catAx>
        <c:axId val="111111111"/>
        <c:scaling><c:orientation val="minMax"/></c:scaling>
        <c:delete val="0"/>
        <c:axPos val="b"/>
        <c:crossAx val="222222222"/>
      </c:catAx>
      <c:valAx>
        <c:axId val="222222222"/>
        <c:scaling><c:orientation val="minMax"/></c:scaling>
        <c:delete val="0"/>
        <c:axPos val="l"/>
        <c:crossAx val="111111111"/>
      </c:valAx>
    </c:plotArea>
    <c:plotVisOnly val="1"/>
    <c:dispBlanksAs val="gap"/>
  </c:chart>
  <c:externalData r:id="rId3">
    <c:autoUpdate val="0"/>
  </c:externalData>
</c:chartSpace>
```

**Axis wiring:** the two `<c:axId>` in the chart must match the two axis IDs, and each axis points back at the other via `<c:crossAx>`. If you flip to `barDir="bar"`, also flip the axis positions (`catAx` → `axPos="l"`, `valAx` → `axPos="b"`).

**`<c:ser>` child order** (this bites people): `idx, order, tx, spPr?, invertIfNegative?, dPt*, dLbls?, …, cat, val`. **Categories before values, always.**

---

## 4. Grouped (clustered) bar — same element, multiple series

"Grouped bar" = `<c:grouping val="clustered"/>` with **more than one `<c:ser>`**. Add a second series with `idx`/`order` of `1`, and keep `overlap` negative or zero so the bars sit side-by-side:

```xml
<c:barChart>
  <c:barDir val="col"/>
  <c:grouping val="clustered"/>
  <c:varyColors val="0"/>
  <c:ser><c:idx val="0"/><c:order val="0"/> … series 1 … </c:ser>
  <c:ser><c:idx val="1"/><c:order val="1"/> … series 2 … </c:ser>
  <c:gapWidth val="150"/>
  <c:overlap val="-27"/>   <!-- side-by-side; use 100 for stacked -->
  <c:axId val="111111111"/>
  <c:axId val="222222222"/>
</c:barChart>
```

Valid `grouping` values for `barChart` are exactly **`clustered`, `stacked`, `percentStacked`** (there's no `standard` for bars — that's a line-chart value, a common mistake).

| Variant | `grouping` | `overlap` |
|---|---|---|
| Clustered (side-by-side) | `clustered` | `-27` (or any ≤ 0) |
| Stacked | `stacked` | `100` |
| 100% stacked | `percentStacked` | `100` |

---

## 5. "Gap bar" — not standard OOXML terminology, so two readings

There's no `gapBarChart` in the schema. Two things people mean:

### Reading A — tuning the spacing

Two knobs on `c:barChart`:

- `<c:gapWidth val="N"/>` — space *between* bars/clusters as a percentage of bar width, range **0–500**, default `150`. Large values (e.g. `300`) give the thin-bars-with-big-gaps look.
- `<c:overlap val="N"/>` — how much series within a cluster overlap, `-100` (gap between them) to `100` (fully stacked).

```xml
<c:barChart>
  <c:barDir val="col"/>
  <c:grouping val="clustered"/>
  <c:ser>…</c:ser>
  <c:gapWidth val="300"/>   <!-- wide gaps -->
  <c:overlap val="-50"/>    <!-- extra gap between series in a cluster -->
  <c:axId val="111111111"/>
  <c:axId val="222222222"/>
</c:barChart>
```

This is **not a separate chart type** — just attribute tuning on a normal bar chart.

### Reading B — floating / "gapped" / Gantt-style bars

If you mean bars that don't start at zero (a Gantt look, or a hand-rolled waterfall), the convention is a **stacked bar with an invisible base series**: series 1 is the "gap" (offset/spacer) made transparent, series 2 is the visible value stacked on top. This is how people faked waterfalls before chartex existed, and the normal native way to make editable Gantt/range bars.

```xml
<c:barChart>
  <c:barDir val="bar"/>
  <c:grouping val="stacked"/>
  <c:overlap val="100"/>

  <!-- spacer / start-offset series: invisible -->
  <c:ser>
    …
    <c:spPr>
      <a:noFill/>
      <a:ln><a:noFill/></a:ln>
    </c:spPr>
    …
  </c:ser>

  <!-- visible duration/value series stacked on top -->
  <c:ser>…</c:ser>

  <c:gapWidth val="50"/>
  <c:axId val="111111111"/>
  <c:axId val="222222222"/>
</c:barChart>
```

---

## 6. Line — `c:lineChart`

Structurally identical to bar minus orientation. Note `grouping` here is **`standard`** (not `clustered`), and the per-series child order puts `marker` before `cat`/`val` and `smooth` after:

```xml
<c:lineChart>
  <c:grouping val="standard"/>
  <c:varyColors val="0"/>
  <c:ser>
    <c:idx val="0"/>
    <c:order val="0"/>
    <c:tx>…</c:tx>
    <c:marker><c:symbol val="none"/></c:marker>   <!-- or "circle", etc. -->
    <c:cat>…</c:cat>
    <c:val>…</c:val>
    <c:smooth val="0"/>
  </c:ser>
  <c:marker val="1"/>
  <c:axId val="111111111"/>
  <c:axId val="222222222"/>
</c:lineChart>
```

Everything else (axes, `externalData`, the `chartSpace` wrapper) is the same as the bar template.

---

## 7. Waterfall — the part that's actually different (chartex)

Waterfall is **not** a `c:` chart at all. It's part of the **"extended charts" (chartex)** family Microsoft added in Office 2016 — alongside treemap, sunburst, histogram/pareto, box & whisker, and funnel. Everything changes:

- **New namespace:** `xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"`
- **New part,** conventionally `/ppt/charts/chartEx1.xml`, content type `application/vnd.ms-office.chartex+xml`
- **Root is `<cx:chartSpace>`,** not `<c:chartSpace>`
- The slide's `graphicData uri` becomes `http://schemas.microsoft.com/office/drawing/2014/chartex`, wrapping `<cx:chart r:id="…"/>`
- **`externalData` is an attribute** (`cx:autoUpdate="0"`), not a child element like in classic
- The **data model is dimensions** (`cx:strDim`/`cx:numDim`), not `cat`/`val`

### Slide reference pattern

```xml
<a:graphicData uri="http://schemas.microsoft.com/office/drawing/2014/chartex">
  <cx:chart
      xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
      r:id="rIdChartEx1"/>
</a:graphicData>
```

### ChartEx part (full waterfall example)

```xml
<cx:chartSpace
    xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <cx:chartData>
    <cx:externalData r:id="rId3" cx:autoUpdate="0"/>
    <cx:data id="0">
      <cx:strDim type="cat">
        <cx:f>Sheet1!$A$2:$A$7</cx:f>
        <cx:lvl ptCount="6">
          <cx:pt idx="0">Start</cx:pt>
          <cx:pt idx="1">Sales</cx:pt>
          <cx:pt idx="2">Returns</cx:pt>
          <cx:pt idx="3">Costs</cx:pt>
          <cx:pt idx="4">Tax</cx:pt>
          <cx:pt idx="5">End</cx:pt>
        </cx:lvl>
      </cx:strDim>
      <cx:numDim type="val">
        <cx:f>Sheet1!$B$2:$B$7</cx:f>
        <cx:lvl ptCount="6" formatCode="General">
          <cx:pt idx="0">100</cx:pt>
          <cx:pt idx="1">80</cx:pt>
          <cx:pt idx="2">-20</cx:pt>
          <cx:pt idx="3">-30</cx:pt>
          <cx:pt idx="4">-10</cx:pt>
          <cx:pt idx="5">120</cx:pt>
        </cx:lvl>
      </cx:numDim>
    </cx:data>
  </cx:chartData>
  <cx:chart>
    <cx:plotArea>
      <cx:plotAreaRegion>
        <cx:series layoutId="waterfall" uniqueId="{00000000-0000-0000-0000-000000000001}">
          <cx:tx>
            <cx:txData><cx:f>Sheet1!$B$1</cx:f><cx:v>Net</cx:v></cx:txData>
          </cx:tx>
          <cx:dataId val="0"/>
          <cx:layoutPr>
            <cx:visibility connectorLines="1"/>
            <cx:subtotals>
              <cx:idx val="0"/>
              <cx:idx val="5"/>
            </cx:subtotals>
          </cx:layoutPr>
        </cx:series>
      </cx:plotAreaRegion>
      <cx:axis id="0"><cx:catScaling gapWidth="150"/><cx:tickLabels/></cx:axis>
      <cx:axis id="1"><cx:valScaling/><cx:majorGridlines/><cx:tickLabels/></cx:axis>
    </cx:plotArea>
  </cx:chart>
</cx:chartSpace>
```

### The two things that *define* a waterfall here

- **`layoutId="waterfall"`** on the series — this selects waterfall vs. funnel vs. treemap, since they all share `cx:series`. (`waterfall` is a valid `ST_SeriesLayout` value.)
- **`<cx:subtotals>`** with a `<cx:idx>` per data point that should be drawn as a **total/subtotal** column (anchored to the baseline). In the example, index 0 (Start) and 5 (End) are totals; the points between float as increments/decrements. **This is the single most important and most-forgotten element.** `<cx:visibility connectorLines="1"/>` draws the connecting lines.

> **`gapWidth` moves.** In chartex it lives on `<cx:catScaling>`, not on the series — so the "gap" knob is in a different place when you're in waterfall land.

### Backward-compatibility wrinkle

PowerPoint 2013 and earlier can't render chartex. When Office writes a waterfall it wraps the `graphicFrame` in an `mc:AlternateContent`, with the chartex in `<mc:Choice Requires="…chartex…">` and a static picture in `<mc:Fallback>`. Optional if you only target modern Office, but recommended for portability.

---

## 8. Chart-type mapping (quick reference)

| Requested chart | OOXML convention |
|---|---|
| **Bar** | `<c:barChart>`. Horizontal → `<c:barDir val="bar"/>`; vertical columns → `<c:barDir val="col"/>`. |
| **Grouped bar** | `<c:barChart>` with `<c:grouping val="clustered"/>` and multiple `<c:ser>`. |
| **Line** | `<c:lineChart>`, usually `<c:grouping val="standard"/>`. |
| **Gap bar** (wider/narrower spacing) | `<c:barChart>` with `<c:gapWidth val="…"/>`. Not a separate type. |
| **Gap bar** (floating / Gantt / range) | Stacked bar: invisible offset/spacer series + visible duration series. |
| **Waterfall** | **ChartEx** (`cx:` namespace, `layoutId="waterfall"`), not classic `<c:barChart>` — unless deliberately faking with stacked bars. |

---

## 9. Landmines, consolidated

- **Element ordering** — follow the XSD `<sequence>` exactly or the file gets "repaired." Validate against the chart schemas if you can.
- **Cache + formula** — always write both; the cache is what renders.
- **The embedded xlsx must be a complete, valid spreadsheet package** (`[Content_Types].xml`, `_rels/.rels`, `xl/workbook.xml` + its rels, `xl/worksheets/sheet1.xml`), and every `<c:f>`/`<cx:f>` range must actually resolve inside it.
- **Unique, cross-referenced `axId`s** for classic charts; the chart's two `<c:axId>` must match real `<c:catAx>`/`<c:valAx>` elements, each pointing at the other via `<c:crossAx>`.
- **`barDir` (col vs bar)** and **`overlap` (100 stacked, ≤ 0 clustered)** — easy to get backwards.
- **Waterfall ≠ classic** — different namespace, part, content type, `graphicData uri`, `externalData` form (attribute, not element), and the `subtotals` indices.
- **Generate unique shape IDs and relationship IDs** throughout.
- **Don't use `/ppt/embeddings/oleObject*.bin`** if the requirement is a native editable chart — that's an OLE blob, not chart data.
- **Keep workbook cells, chart formulas, and chart caches synchronized.**

---

## 10. Tooling

Waterfall is the dividing line.

- **python-pptx** generates the chart part, embedded xlsx, and rels for you for all the *classic* types (`XL_CHART_TYPE.COLUMN_CLUSTERED`, `BAR_CLUSTERED`, `LINE`, etc.). It has **no chartex support** — for waterfall you build the `cx` XML by hand and inject the part + relationship + embedding into the package yourself.
- **Open XML SDK (C#)** gives full control: classic types under `DocumentFormat.OpenXml.Drawing.Charts` (`BarChart` = `c:barChart`, `LineChart` = `c:lineChart`, with children `barDir`, `grouping`, `ser`, `gapWidth`, `overlap`, axis IDs); chartex under the Office2016 chart classes (`cx:chart`), so you can construct waterfall properly without raw string XML.
- **Raw XML / templating** — most control, most footguns; exactly the conventions above.

### Open XML SDK generation flow (classic charts)

```csharp
// 1. Add chart part to the slide.
ChartPart chartPart = slidePart.AddNewPart<ChartPart>("rIdChart1");

// 2. Add embedded workbook package to the chart part.
EmbeddedPackagePart workbookPart =
    chartPart.AddEmbeddedPackagePart(EmbeddedPackagePartType.Xlsx, "rIdWorkbook1");

// 3. Write XLSX bytes into workbookPart.

// 4. Generate c:chartSpace and set c:externalData r:id="rIdWorkbook1".
chartPart.ChartSpace = BuildChartSpace(...);

// 5. Add a p:graphicFrame on the slide containing c:chart r:id="rIdChart1".
```

For **ChartEx/waterfall**, the pragmatic approach is to **template it**: build one correct PowerPoint waterfall manually, unzip it, inspect the `chartEx` part, then programmatically clone and update that structure. ChartEx is far less forgiving than classic `c:barChart`, and PowerPoint will repair or discard small mistakes.

### Practical rules that avoid most corrupt / non-editable decks

1. Keep workbook cells, chart formulas, and chart caches synchronized.
2. Use `c:externalData` / `cx:externalData` pointing to the embedded XLSX relationship.
3. Do **not** use `/ppt/embeddings/oleObject*.bin` if the requirement is a native editable chart.
4. Generate unique shape IDs, relationship IDs, and axis IDs.
5. For classic charts, make `c:barChart` / `c:lineChart` axis IDs match real `c:catAx` / `c:valAx` elements.
6. For waterfall, use ChartEx or clone a known-good ChartEx template.
7. Validate with Open XML SDK validation, then open/resave in PowerPoint as the final compatibility test.

> **The key split:** bar, line, grouped bar, and gap-width bar are classic `c:*Chart` parts; **waterfall is ChartEx** unless you are intentionally approximating it with stacked bars.

---

## References

- [ChartReference Class — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.chartreference?view=openxml-3.0.1)
- [ChartPart.AddEmbeddedPackagePart Method — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packaging.chartpart.addembeddedpackagepart?view=openxml-2.20.0)
- [BarChart Class — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.barchart?view=openxml-3.0.1)
- [BarDirection Class — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.bardirection?view=openxml-3.0.1)
- [ST_BarGrouping (Bar Grouping) — c-rex.net](https://c-rex.net/samples/ooxml/e1/Part4/OOXML_P4_DOCX_ST_BarGrouping_topic_ID0ETSPRB.html)
- [gapWidth (Gap Width) — c-rex.net](https://c-rex.net/samples/ooxml/e1/Part4/OOXML_P4_DOCX_gapWidth_topic_ID0EFVEQB.html)
- [[MS-ODRAWXML]: ChartEx — Microsoft Learn](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-odrawxml/5d0d453e-adac-43be-a797-59b9916593dd)
- [Chart Class (Office2016.Drawing.ChartDrawing) — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.office2016.drawing.chartdrawing.chart?view=openxml-3.0.1)
- [[MS-ODRAWXML]: chartex Schema — Microsoft Learn](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-odrawxml/e2723b0a-9120-42a5-bd11-c252ccb13c1e)
