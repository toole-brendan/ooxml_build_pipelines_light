# PowerPoint OOXML Conventions: Consolidated Reference

_Last consolidated: 2026-05-28_

This file consolidates the uploaded PowerPoint OOXML notes into one structured reference. It is organized around how a `.pptx` actually works: package parts and relationships first, then presentation-level structure, inheritance and themes, slide objects, formatting primitives, charts, dynamic features, and practical editing workflows.

---

## Table of Contents

1. [Core mental model](#1-core-mental-model)
2. [Namespaces and common prefixes](#2-namespaces-and-common-prefixes)
3. [Package anatomy: parts, relationships, and content types](#3-package-anatomy-parts-relationships-and-content-types)
4. [ID taxonomy: not all IDs are the same](#4-id-taxonomy-not-all-ids-are-the-same)
5. [Units and coordinate conventions](#5-units-and-coordinate-conventions)
6. [Presentation-level structure](#6-presentation-level-structure)
7. [Masters, layouts, placeholders, and inheritance](#7-masters-layouts-placeholders-and-inheritance)
8. [Themes, color maps, and effective formatting](#8-themes-color-maps-and-effective-formatting)
9. [Slide skeleton and the shape tree](#9-slide-skeleton-and-the-shape-tree)
10. [Shared object anatomy](#10-shared-object-anatomy)
11. [Shapes and text boxes](#11-shapes-and-text-boxes)
12. [Text, paragraphs, runs, bullets, and list styles](#12-text-paragraphs-runs-bullets-and-list-styles)
13. [Fills, lines, borders, padding, and alignment](#13-fills-lines-borders-padding-and-alignment)
14. [Pictures and image fills](#14-pictures-and-image-fills)
15. [Tables](#15-tables)
16. [Connectors and arrowheads](#16-connectors-and-arrowheads)
17. [Group shapes](#17-group-shapes)
18. [Custom geometry and freeform paths](#18-custom-geometry-and-freeform-paths)
19. [Hyperlinks](#19-hyperlinks)
20. [Charts: architecture and data model](#20-charts-architecture-and-data-model)
21. [Standard `c:*` charts](#21-standard-c-charts)
22. [ChartEx `cx:*` charts and waterfall charts](#22-chartex-cx-charts-and-waterfall-charts)
23. [Detailed chart formatting](#23-detailed-chart-formatting)
24. [Slide numbers, dates, and footers](#24-slide-numbers-dates-and-footers)
25. [Practical workflows](#25-practical-workflows)
26. [What must be updated together](#26-what-must-be-updated-together)
27. [Common gotchas](#27-common-gotchas)
28. [Appendices](#28-appendices)

---

## 1. Core mental model

PowerPoint OOXML is not one XML file. A `.pptx` is an OPC/ZIP package made of XML parts, relationship parts, binary assets, embedded workbooks, themes, media, charts, and content-type declarations.

The most important operating rule is:

```text
current XML part
  contains an r:id
    resolved in that current part's local _rels/*.rels file
      target part contains the real payload
```

Examples:

```text
slideN.xml
  contains <c:chart r:id="rId5"/>
  slideN.xml.rels maps rId5 -> ../charts/chart1.xml

chart1.xml
  contains <c:externalData r:id="rId1"/>
  chart1.xml.rels maps rId1 -> ../embeddings/Microsoft_Excel_Worksheet1.xlsx

slideN.xml
  contains <a:blip r:embed="rId7"/>
  slideN.xml.rels maps rId7 -> ../media/image1.png
```

A second important rule is that the visible XML on a slide often does not contain all final formatting. Final appearance may be resolved through:

```text
direct formatting
  -> shape style references
  -> placeholder/layout/master formatting
  -> color map
  -> theme color/font/format scheme
```

A third important rule is that visible slide objects normally live under:

```text
p:sld / p:cSld / p:spTree
```

with one of these object wrappers:

```text
p:sp             shapes, text boxes, placeholders
p:pic            inserted pictures
p:graphicFrame   charts, tables, diagrams, SmartArt-like framed objects
p:cxnSp          connectors
p:grpSp          group shapes
```

When reading or generating PowerPoint OOXML, always ask:

```text
1. Is this value direct, inherited, or theme-derived?
2. Is this element the real payload or only a reference via r:id?
3. Which .rels file owns that r:id?
4. Is this color an absolute RGB color or a scheme color that needs a color map/theme?
5. Is this a standalone object or a placeholder inheriting from a layout/master?
```

---

## 2. Namespaces and common prefixes

Common prefixes:

```xml
p   = http://schemas.openxmlformats.org/presentationml/2006/main
a   = http://schemas.openxmlformats.org/drawingml/2006/main
r   = http://schemas.openxmlformats.org/officeDocument/2006/relationships
c   = http://schemas.openxmlformats.org/drawingml/2006/chart
cx  = http://schemas.microsoft.com/office/drawing/2014/chartex
p14 = http://schemas.microsoft.com/office/powerpoint/2010/main
```

Conceptual split:

```text
p:*     PresentationML: slides, shapes, placeholders, masters, layouts
a:*     DrawingML: geometry, transforms, fills, lines, text, tables
r:*     relationship attributes, most commonly r:id
c:*     standard DrawingML charts
cx:*    Office 2014+ ChartEx charts, such as waterfall, treemap, sunburst
p14:*   PowerPoint 2010+ extensions, including sections
```

Common full namespace set for a slide object example:

```xml
xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
```

Common chart namespace set:

```xml
xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
```

Common ChartEx namespace set:

```xml
xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
```

---

## 3. Package anatomy: parts, relationships, and content types

A typical `.pptx` contains parts like:

```text
[Content_Types].xml
_rels/.rels
docProps/
ppt/presentation.xml
ppt/_rels/presentation.xml.rels
ppt/slides/slide1.xml
ppt/slides/_rels/slide1.xml.rels
ppt/slideLayouts/slideLayout1.xml
ppt/slideLayouts/_rels/slideLayout1.xml.rels
ppt/slideMasters/slideMaster1.xml
ppt/slideMasters/_rels/slideMaster1.xml.rels
ppt/theme/theme1.xml
ppt/media/image1.png
ppt/charts/chart1.xml
ppt/charts/chartEx1.xml
ppt/charts/_rels/chart1.xml.rels
ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx
ppt/tableStyles.xml
```

### 3.1 Relationship files are local

`rId5` in `slide1.xml` is not the same as `rId5` in `chart1.xml`.

For example, on a slide:

```xml
<c:chart r:id="rId5"/>
```

is resolved by:

```text
ppt/slides/_rels/slide1.xml.rels
```

not by `ppt/_rels/presentation.xml.rels` and not by the chart part's `.rels`.

Example slide relationship:

```xml
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId5"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart"
    Target="../charts/chart1.xml"/>
</Relationships>
```

Example chart relationship to embedded workbook:

```xml
<!-- ppt/charts/_rels/chart1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package"
    Target="../embeddings/Microsoft_Excel_Worksheet1.xlsx"/>
</Relationships>
```

Example image relationship:

```xml
<!-- ppt/slides/_rels/slide1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId7"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="../media/image1.png"/>
</Relationships>
```

Example external hyperlink relationship:

```xml
<Relationship Id="rId5"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
  Target="https://example.com/"
  TargetMode="External"/>
```

### 3.2 Content types

`[Content_Types].xml` declares what package parts are. Some parts use `<Default>` by extension, while XML parts usually use `<Override>` by part name.

Common image defaults:

```xml
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
```

Common overrides:

```xml
<!-- standard chart -->
<Override PartName="/ppt/charts/chart1.xml"
  ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>

<!-- Office extended ChartEx chart -->
<Override PartName="/ppt/charts/chartEx1.xml"
  ContentType="application/vnd.ms-office.chartex+xml"/>

<!-- embedded workbook -->
<Override PartName="/ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx"
  ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/>

<!-- table styles -->
<Override PartName="/ppt/tableStyles.xml"
  ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
```

When creating a new part, update all of:

```text
1. The referring XML element.
2. The referring part's .rels file.
3. The target part payload.
4. The target part's own .rels file, if it has dependencies.
5. [Content_Types].xml.
```

---

## 4. ID taxonomy: not all IDs are the same

Many PowerPoint bugs come from confusing ID scopes.

| ID form | Scope | Meaning |
|---|---|---|
| `r:id="rId5"` | Local to the current part's `.rels` file | Relationship pointer to another package part or external target |
| `p:cNvPr/@id` | Local drawing object ID within a slide/layout/master shape tree | Identifies shapes/pictures/graphic frames/connectors for drawing operations |
| `p:sldId/@id` | Presentation-level stable slide ID | Used by `presentation.xml`, sections, custom shows |
| `p:sldId/@r:id` | Relationship from `presentation.xml` | Points to the slide part |
| `p:ph/@idx` | Placeholder matching key | Connects slide placeholders to layout placeholders |
| `c:axId` | Chart-local axis ID | Connects chart types to axes |
| `p14:sldId/@id` | Presentation slide ID reference | Refers to `p:sldId/@id`, not `r:id` |

Examples:

```xml
<!-- Drawing object ID -->
<p:cNvPr id="4" name="Chart 3"/>

<!-- Relationship ID -->
<c:chart r:id="rId5"/>

<!-- Presentation slide ID plus relationship ID -->
<p:sldId id="256" r:id="rId2"/>

<!-- Section references p:sldId/@id -->
<p14:sldId id="256"/>

<!-- Placeholder matching key -->
<p:ph type="body" idx="1"/>

<!-- Connector target references p:cNvPr/@id, not r:id -->
<a:stCxn id="2" idx="3"/>
<a:endCxn id="5" idx="1"/>

<!-- Chart axis IDs -->
<c:axId val="123456"/>
<c:crossAx val="123457"/>
```

Practical rule:

```text
r:id resolves package relationships.
p:cNvPr/@id identifies drawing objects.
p:ph/@idx matches placeholders.
p:sldId/@id identifies slides at the presentation level.
c:axId wires chart types and axes.
```

---

## 5. Units and coordinate conventions

PowerPoint DrawingML geometry normally uses EMUs.

### 5.1 EMU conversions

| Unit | EMU conversion |
|---|---:|
| 1 inch | `914400` EMU |
| 1 cm | `360000` EMU |
| 1 point | `12700` EMU |
| 1 twip | `635` EMU |
| 1 px at 96 DPI | `9525` EMU |

Python helpers:

```python
EMU_PER_INCH = 914400
EMU_PER_CM = 360000
EMU_PER_PT = 12700

def inches_to_emu(x: float) -> int:
    return round(x * EMU_PER_INCH)

def emu_to_inches(x: int) -> float:
    return x / EMU_PER_INCH

def cm_to_emu(x: float) -> int:
    return round(x * EMU_PER_CM)

def pt_to_emu(x: float) -> int:
    return round(x * EMU_PER_PT)

def px_to_emu(px: float, dpi: float = 96) -> int:
    return round(px * EMU_PER_INCH / dpi)
```

Examples:

```xml
<p:sldSz cx="9144000" cy="6858000"/>
```

means:

```text
cx = 9144000 / 914400 = 10 inches
cy = 6858000 / 914400 = 7.5 inches
```

This transform:

```xml
<a:xfrm>
  <a:off x="914400" y="457200"/>
  <a:ext cx="1828800" cy="914400"/>
</a:xfrm>
```

means:

```text
position = 1.0 in, 0.5 in
size     = 2.0 in x 1.0 in
```

### 5.2 Other numeric conventions

| Feature | Convention |
|---|---|
| Rotation | `rot` is in 60,000ths of a degree |
| Text size | `sz` is in hundredths of a point |
| Percentage values | Often `100000 = 100%` |
| Line width | Usually EMUs; `12700 = 1 pt` |
| `a:srcRect` image crop | Percent offsets; `100000 = 100%` |

Examples:

```xml
<!-- 90 degrees -->
<a:xfrm rot="5400000"/>

<!-- 10 pt text -->
<a:rPr sz="1000"/>

<!-- 25% bullet size? No: 100000 = 100%, so 75000 = 75% -->
<a:buSzPct val="100000"/>

<!-- 1 pt line -->
<a:ln w="12700"/>

<!-- crop 10% left/right, 5% top/bottom -->
<a:srcRect l="10000" r="10000" t="5000" b="5000"/>
```

---

## 6. Presentation-level structure

The main presentation part is:

```text
ppt/presentation.xml
```

Typical skeleton:

```xml
<p:presentation
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  saveSubsetFonts="1">

  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>

  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
    <p:sldId id="257" r:id="rId3"/>
    <p:sldId id="258" r:id="rId4"/>
  </p:sldIdLst>

  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>

  <p:embeddedFontLst>
    <p:embeddedFont>...</p:embeddedFont>
  </p:embeddedFontLst>

  <p:defaultTextStyle>
    ...
  </p:defaultTextStyle>

  <p:extLst>
    ...
  </p:extLst>
</p:presentation>
```

Key conventions:

```text
p:sldIdLst
  Authoritative slide order. The order of p:sldId entries is the presentation order.

p:sldId/@id
  Stable numeric slide identifier. This is not a relationship ID.

p:sldId/@r:id
  Relationship from ppt/presentation.xml to ppt/slides/slideN.xml.

p:sldMasterIdLst
  List of slide master parts available to the presentation.

p:sldSz/@cx and @cy
  Slide dimensions in EMUs.

p:sldSz/@type
  Preset/target slide size label.

p:notesSz
  Notes/handout surface size.

p:defaultTextStyle
  Fallback text style if no master/layout/shape text style supplies one.

p:embeddedFontLst
  List of fonts embedded in the presentation.
```

Common slide size examples:

```xml
<!-- 4:3, 10 in x 7.5 in -->
<p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>

<!-- 16:9, 13.333... in x 7.5 in -->
<p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
```

Common `p:sldSz/@type` values:

```text
screen4x3
screen16x9
screen16x10
letter
A4
35mm
overhead
banner
custom
ledger
A3
B4ISO
B5ISO
B4JIS
B5JIS
hagakiCard
```

### 6.1 PowerPoint sections

PowerPoint sections are stored as a PowerPoint extension under `presentation.xml`:

```text
p:presentation
  p:extLst
    p:ext uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}"
      p14:sectionLst
```

Example:

```xml
<p:presentation
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">

  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
    <p:sldId id="257" r:id="rId3"/>
    <p:sldId id="258" r:id="rId4"/>
  </p:sldIdLst>

  <p:extLst>
    <p:ext uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}">
      <p14:sectionLst>
        <p14:section
          name="Introduction"
          id="{01F07B81-39E6-4BBB-9B89-66EA253FBD29}">
          <p14:sldIdLst>
            <p14:sldId id="256"/>
          </p14:sldIdLst>
        </p14:section>

        <p14:section
          name="Main Content"
          id="{1FEF2C88-0CF2-4176-BA81-0DE6FD9D1274}">
          <p14:sldIdLst>
            <p14:sldId id="257"/>
            <p14:sldId id="258"/>
          </p14:sldIdLst>
        </p14:section>
      </p14:sectionLst>
    </p:ext>
  </p:extLst>
</p:presentation>
```

Important details:

```text
p14:section/@name
  Display name in the PowerPoint section pane.

p14:section/@id
  GUID uniquely identifying the section.

p14:sldId/@id
  Refers to p:presentation/p:sldIdLst/p:sldId/@id.

It does not use r:id.
It does not point directly to slide1.xml.
```

Generator convention:

```text
Keep p14:sldId entries in the same order as the main p:sldIdLst.
```

---

## 7. Masters, layouts, placeholders, and inheritance

The hierarchy is:

```text
presentation.xml
  -> slideMaster1.xml
       -> slideLayout1.xml
       -> slideLayout2.xml
  -> slides/slide1.xml
       -> slideLayoutX.xml
```

### 7.1 Slide master

A slide master part root is usually:

```xml
<p:sldMaster>
  <p:cSld>...</p:cSld>
  <p:clrMap .../>
  <p:sldLayoutIdLst>...</p:sldLayoutIdLst>
  <p:txStyles>...</p:txStyles>
</p:sldMaster>
```

Master responsibilities:

```text
shared background
theme color map
default text styles
placeholder prototypes
header/footer placeholders
common shapes/logos
layout list
```

### 7.2 Slide layout

A layout part root is usually:

```xml
<p:sldLayout type="titleAndContent">
  <p:cSld>...</p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sldLayout>
```

Layout responsibilities:

```text
slide arrangement
placeholder geometry
layout-specific formatting
layout-specific background or objects
mapping between slide placeholder content and master placeholder defaults
```

### 7.3 Slide

A slide part root is usually:

```xml
<p:sld>
  <p:cSld>
    <p:spTree>
      ...
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>
```

Slide responsibilities:

```text
actual content
direct overrides
sparse placeholders
relationships to charts/images/hyperlinks
notes/timing/transition if present
```

### 7.4 Placeholders

A placeholder is usually not a separate object class. It is a normal shape, picture, or graphic frame whose nonvisual properties contain `p:ph`.

Example placeholder shape:

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Title 1"/>
    <p:cNvSpPr/>
    <p:nvPr>
      <p:ph type="title" idx="0"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr/>
  <p:txBody>...</p:txBody>
</p:sp>
```

A slide placeholder can be very sparse:

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="5" name="Content Placeholder 4"/>
    <p:cNvSpPr/>
    <p:nvPr>
      <p:ph idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr/>
  <p:txBody>...</p:txBody>
</p:sp>
```

Its geometry, default text style, bullet style, fill, line, and other defaults can come from the matching layout placeholder with `idx="1"` and then from the master/theme chain.

Key placeholder attributes:

```text
p:ph/@type
  Placeholder role: title, body, obj, chart, pic, tbl, dt, ftr, sldNum, etc.

p:ph/@idx
  Placeholder matching/inheritance key.

p:ph/@sz
  Size hint.

p:ph/@orient
  Orientation hint.
```

Important distinction:

```text
p:cNvPr/@id = local drawing object ID
p:ph/@idx   = logical placeholder matching key
```

Common placeholder types:

```text
title
ctrTitle
subTitle
body
obj
chart
tbl
clipArt
dgm
media
pic
dt
ftr
sldNum
```

Practical rules:

```text
Use p:ph/@idx to match slide placeholders to layout placeholders.
Do not use p:cNvPr/@id as the placeholder inheritance key.
When changing layouts, preserve placeholder idx values where possible.
Use direct formatting only when you want to override the layout/master inheritance chain.
```

---

## 8. Themes, color maps, and effective formatting

Theme files are usually stored under:

```text
ppt/theme/theme1.xml
```

A typical theme part:

```xml
<a:theme name="Office Theme">
  <a:themeElements>
    <a:clrScheme name="Office">...</a:clrScheme>
    <a:fontScheme name="Office">...</a:fontScheme>
    <a:fmtScheme name="Office">...</a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/>
  <a:extraClrSchemeLst/>
</a:theme>
```

### 8.1 Color scheme

`a:clrScheme` has twelve main slots:

```xml
<a:clrScheme name="Office">
  <a:dk1>...</a:dk1>
  <a:lt1>...</a:lt1>
  <a:dk2>...</a:dk2>
  <a:lt2>...</a:lt2>
  <a:accent1>...</a:accent1>
  <a:accent2>...</a:accent2>
  <a:accent3>...</a:accent3>
  <a:accent4>...</a:accent4>
  <a:accent5>...</a:accent5>
  <a:accent6>...</a:accent6>
  <a:hlink>...</a:hlink>
  <a:folHlink>...</a:folHlink>
</a:clrScheme>
```

Each slot often contains:

```xml
<a:srgbClr val="1F497D"/>
```

or:

```xml
<a:sysClr val="windowText" lastClr="000000"/>
```

### 8.2 Color maps

Slide/master XML often refers to semantic names like:

```text
bg1, tx1, bg2, tx2, accent1 ... accent6, hlink, folHlink
```

The master color map maps these names to theme slots:

```xml
<p:clrMap
  bg1="lt1"
  tx1="dk1"
  bg2="lt2"
  tx2="dk2"
  accent1="accent1"
  accent2="accent2"
  accent3="accent3"
  accent4="accent4"
  accent5="accent5"
  accent6="accent6"
  hlink="hlink"
  folHlink="folHlink"/>
```

Resolution example:

```xml
<a:solidFill>
  <a:schemeClr val="tx1"/>
</a:solidFill>
```

with the map above resolves as:

```text
tx1 -> dk1 -> theme clrScheme/dk1 -> actual RGB/system color
```

A slide or layout can use the master mapping:

```xml
<p:clrMapOvr>
  <a:masterClrMapping/>
</p:clrMapOvr>
```

or override it:

```xml
<p:clrMapOvr>
  <a:overrideClrMapping
    bg1="dk1"
    tx1="lt1"
    accent1="accent3"/>
</p:clrMapOvr>
```

### 8.3 Font scheme

The font scheme has major and minor fonts:

```xml
<a:fontScheme name="Office">
  <a:majorFont>
    <a:latin typeface="Aptos Display"/>
    <a:ea typeface=""/>
    <a:cs typeface=""/>
    <a:font script="Jpan" typeface="Yu Gothic"/>
  </a:majorFont>

  <a:minorFont>
    <a:latin typeface="Aptos"/>
    <a:ea typeface=""/>
    <a:cs typeface=""/>
    <a:font script="Jpan" typeface="Yu Gothic"/>
  </a:minorFont>
</a:fontScheme>
```

Theme font references:

```text
+mj-lt = major Latin font
+mn-lt = minor Latin font
+mj-ea = major East Asian font
+mn-ea = minor East Asian font
+mj-cs = major complex-script font
+mn-cs = minor complex-script font
```

Example:

```xml
<a:rPr sz="2400">
  <a:latin typeface="+mn-lt"/>
</a:rPr>
```

### 8.4 Format scheme

The format scheme is the theme's style matrix:

```xml
<a:fmtScheme name="Office">
  <a:fillStyleLst>...</a:fillStyleLst>
  <a:lnStyleLst>...</a:lnStyleLst>
  <a:effectStyleLst>...</a:effectStyleLst>
  <a:bgFillStyleLst>...</a:bgFillStyleLst>
</a:fmtScheme>
```

Shapes refer to these matrix entries through style refs:

```xml
<a:style>
  <a:lnRef idx="1">
    <a:schemeClr val="accent1"/>
  </a:lnRef>
  <a:fillRef idx="3">
    <a:schemeClr val="accent1"/>
  </a:fillRef>
  <a:effectRef idx="2">
    <a:schemeClr val="accent1"/>
  </a:effectRef>
  <a:fontRef idx="minor">
    <a:schemeClr val="lt1"/>
  </a:fontRef>
</a:style>
```

Effective formatting resolution:

```text
direct shape formatting
  -> shape style refs
  -> placeholder/layout/master formatting
  -> color map
  -> theme color scheme, font scheme, format scheme
```

---

## 9. Slide skeleton and the shape tree

Common slide body pattern:

```xml
<p:sld>
  <p:cSld>
    <p:spTree>
      <!-- shapes, pictures, tables, charts, connectors, groups -->
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>
```

Most visible objects appear as children of `p:spTree`:

```xml
<p:sp>...</p:sp>
<p:pic>...</p:pic>
<p:graphicFrame>...</p:graphicFrame>
<p:cxnSp>...</p:cxnSp>
<p:grpSp>...</p:grpSp>
```

Object map:

| PowerPoint object | Main XML |
|---|---|
| Text box | `p:sp` with `p:txBody` |
| AutoShape | `p:sp` with `p:spPr/a:prstGeom` |
| Placeholder | Usually `p:sp`, `p:pic`, or `p:graphicFrame` with `p:nvPr/p:ph` |
| Picture | `p:pic` |
| Table | `p:graphicFrame` + `a:graphicData` + `a:tbl` |
| Standard chart | `p:graphicFrame` + `c:chart r:id` |
| ChartEx chart | `p:graphicFrame` + `cx:chart r:id` |
| Connector | `p:cxnSp` |
| Group | `p:grpSp` |

---

## 10. Shared object anatomy

Many slide objects have the same broad anatomy:

```text
nonvisual properties
transform/position
object-specific properties
style/direct formatting
text body if applicable
```

### 10.1 Nonvisual properties

Shapes:

```xml
<p:nvSpPr>
  <p:cNvPr id="2" name="Rectangle 1" descr="Alt text"/>
  <p:cNvSpPr/>
  <p:nvPr/>
</p:nvSpPr>
```

Pictures:

```xml
<p:nvPicPr>
  <p:cNvPr id="5" name="Picture 4" descr="Alt text"/>
  <p:cNvPicPr>
    <a:picLocks noChangeAspect="1"/>
  </p:cNvPicPr>
  <p:nvPr/>
</p:nvPicPr>
```

Graphic frames:

```xml
<p:nvGraphicFramePr>
  <p:cNvPr id="7" name="Table 6"/>
  <p:cNvGraphicFramePr/>
  <p:nvPr/>
</p:nvGraphicFramePr>
```

Connectors:

```xml
<p:nvCxnSpPr>
  <p:cNvPr id="7" name="Connector 6"/>
  <p:cNvCxnSpPr/>
  <p:nvPr/>
</p:nvCxnSpPr>
```

Common details:

```text
p:cNvPr/@id      local drawing object ID
p:cNvPr/@name    UI-ish object name
p:cNvPr/@descr   alt text / accessibility description
p:nvPr/p:ph      placeholder metadata
p:cNvPr/a:hlinkClick whole-shape hyperlink
```

### 10.2 Transform and position

For most shapes/pictures:

```xml
<a:xfrm>
  <a:off x="914400" y="914400"/>
  <a:ext cx="3657600" cy="2743200"/>
</a:xfrm>
```

For `p:graphicFrame`, PowerPoint commonly uses:

```xml
<p:xfrm>
  <a:off x="914400" y="914400"/>
  <a:ext cx="7315200" cy="4114800"/>
</p:xfrm>
```

For group shapes, see [Group shapes](#17-group-shapes), because `a:xfrm` has `chOff` and `chExt` too.

### 10.3 Shape properties

Common `p:spPr` structure:

```xml
<p:spPr>
  <a:xfrm>...</a:xfrm>
  <a:prstGeom prst="roundRect">
    <a:avLst/>
  </a:prstGeom>

  <a:solidFill>
    <a:srgbClr val="FFFFFF"/>
  </a:solidFill>

  <a:ln w="12700">
    <a:solidFill>
      <a:srgbClr val="4472C4"/>
    </a:solidFill>
  </a:ln>
</p:spPr>
```

### 10.4 Text body

Shape text uses:

```xml
<p:txBody>
  <a:bodyPr/>
  <a:lstStyle/>
  <a:p>
    <a:r>
      <a:rPr sz="1800" b="1"/>
      <a:t>Hello</a:t>
    </a:r>
  </a:p>
</p:txBody>
```

Table cell text uses the same DrawingML text model but under `a:txBody`:

```xml
<a:tc>
  <a:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:t>Cell text</a:t>
      </a:r>
    </a:p>
  </a:txBody>
  <a:tcPr/>
</a:tc>
```

---

## 11. Shapes and text boxes

A normal shape/text box is `p:sp`.

Minimal useful shape:

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Rectangle 1"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>

  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>
      <a:ext cx="3657600" cy="914400"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="4472C4"/>
    </a:solidFill>
    <a:ln w="12700">
      <a:solidFill>
        <a:srgbClr val="FFFFFF"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>

  <p:txBody>
    <a:bodyPr lIns="91440" rIns="91440" tIns="45720" bIns="45720"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="en-US" sz="1800" b="1">
          <a:solidFill>
            <a:srgbClr val="FFFFFF"/>
          </a:solidFill>
        </a:rPr>
        <a:t>Hello</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Shape checklist:

```text
1. Set a unique p:cNvPr/@id within the slide shape tree.
2. Set p:cNvPr/@name for readability.
3. Use a:xfrm for position/size.
4. Use a:prstGeom or a:custGeom for geometry.
5. Put fill/line in p:spPr.
6. Put text in p:txBody.
7. Use p:nvPr/p:ph only if the shape is a placeholder.
```

---

## 12. Text, paragraphs, runs, bullets, and list styles

### 12.1 Text body model

PowerPoint text generally follows:

```xml
<p:txBody>
  <a:bodyPr/>
  <a:lstStyle/>
  <a:p>
    <a:pPr/>
    <a:r>
      <a:rPr/>
      <a:t>Text</a:t>
    </a:r>
    <a:endParaRPr/>
  </a:p>
</p:txBody>
```

Elements:

```text
a:bodyPr       text box layout: padding, wrap, columns, vertical alignment
a:lstStyle     local list/level styles
a:p            paragraph
a:pPr          paragraph properties: horizontal alignment, margins, bullets, level
a:r            text run
a:rPr          run properties: font, size, bold, italic, color, hyperlink
a:t            text
a:endParaRPr   end paragraph run defaults
```

### 12.2 Text sizes and font references

Text size:

```xml
<a:rPr sz="2400"/>
```

means 24 pt.

Theme font references:

```xml
<a:latin typeface="+mn-lt"/>
```

Common:

```text
+mn-lt = minor Latin font
+mj-lt = major Latin font
```

### 12.3 Paragraph horizontal alignment

Horizontal alignment is paragraph-level:

```xml
<a:p>
  <a:pPr algn="ctr"/>
  <a:r>
    <a:t>Centered text</a:t>
  </a:r>
</a:p>
```

Common `algn` values:

```text
l
ctr
r
just
```

### 12.4 Bullets

Direct paragraph bullet:

```xml
<a:p>
  <a:pPr lvl="0" marL="342900" indent="-171450">
    <a:buFont typeface="Arial"/>
    <a:buClr>
      <a:schemeClr val="tx1"/>
    </a:buClr>
    <a:buSzPct val="100000"/>
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>Bullet text</a:t>
  </a:r>
</a:p>
```

Key bullet elements:

```xml
<a:buChar char="•"/>                    <!-- symbol bullet -->
<a:buAutoNum type="arabicPeriod" startAt="1"/>  <!-- numbered bullet -->
<a:buNone/>                             <!-- explicitly no bullet -->
<a:buClr><a:srgbClr val="FFFF00"/></a:buClr>    <!-- bullet color -->
<a:buFont typeface="Wingdings"/>         <!-- bullet font -->
<a:buSzPct val="100000"/>                <!-- bullet size; 100000 = 100% -->
<a:buClrTx/>                             <!-- bullet color follows text -->
<a:buFontTx/>                            <!-- bullet font follows text -->
<a:buSzTx/>                              <!-- bullet size follows text -->
```

Important level convention:

```text
a:pPr/@lvl="0" -> uses a:lvl1pPr
a:pPr/@lvl="1" -> uses a:lvl2pPr
...
a:pPr/@lvl="8" -> uses a:lvl9pPr
```

The paragraph `lvl` attribute is zero-based, but the list-style element names are one-based.

### 12.5 List styles

A text body can define local list styles:

```xml
<p:txBody>
  <a:bodyPr/>
  <a:lstStyle>
    <a:lvl1pPr marL="342900" indent="-171450">
      <a:buChar char="•"/>
      <a:defRPr sz="2400"/>
    </a:lvl1pPr>

    <a:lvl2pPr marL="685800" indent="-171450">
      <a:buChar char="–"/>
      <a:defRPr sz="2200"/>
    </a:lvl2pPr>
  </a:lstStyle>

  <a:p>
    <a:pPr lvl="0"/>
    <a:r><a:t>Level 1</a:t></a:r>
  </a:p>

  <a:p>
    <a:pPr lvl="1"/>
    <a:r><a:t>Level 2</a:t></a:r>
  </a:p>
</p:txBody>
```

Master text styles often appear as:

```xml
<p:txStyles>
  <p:titleStyle>
    <a:lvl1pPr algn="ctr">
      <a:defRPr sz="4400"/>
    </a:lvl1pPr>
  </p:titleStyle>

  <p:bodyStyle>
    <a:lvl1pPr marL="342900" indent="-171450">
      <a:buChar char="•"/>
      <a:defRPr sz="2800"/>
    </a:lvl1pPr>
    <a:lvl2pPr marL="685800" indent="-171450">
      <a:buChar char="–"/>
      <a:defRPr sz="2400"/>
    </a:lvl2pPr>
  </p:bodyStyle>

  <p:otherStyle>...</p:otherStyle>
</p:txStyles>
```

Bullet cascade for placeholder text:

```text
1. Direct paragraph properties on the slide:
   a:p/a:pPr

2. Shape-local text body list style:
   p:txBody/a:lstStyle/a:lvlNpPr

3. Matching placeholder on the slide layout:
   same p:ph/@idx

4. Matching/default placeholder style on the slide master:
   master placeholder p:txBody/a:lstStyle
   and/or p:sldMaster/p:txStyles

5. Presentation default text style:
   p:presentation/p:defaultTextStyle

6. Theme font/color defaults:
   theme1.xml
```

Practical bullet-writing rules:

```text
Use a:buNone when you must stop inherited bullets.
Use a:buChar for symbol bullets.
Use a:buAutoNum for numbered lists.
Set marL and indent together for hanging bullets.
Use layout/master styles instead of repeating bullet formatting on every slide when possible.
Preserve schema order when writing bullet children.
```

Hanging-indent convention:

```xml
<a:lvl1pPr marL="342900" indent="-171450">
```

Interpretation:

```text
marL   = left margin / text start
indent = first-line offset relative to marL
negative indent = bullet hangs to the left of the text
```

---

## 13. Fills, lines, borders, padding, and alignment

### 13.1 Fills

Common fill elements:

```xml
<a:noFill/>
<a:solidFill>...</a:solidFill>
<a:gradFill>...</a:gradFill>
<a:pattFill>...</a:pattFill>
<a:blipFill>...</a:blipFill>
```

Absolute color:

```xml
<a:solidFill>
  <a:srgbClr val="4472C4"/>
</a:solidFill>
```

Theme color:

```xml
<a:solidFill>
  <a:schemeClr val="accent1"/>
</a:solidFill>
```

Where fills appear:

```text
shape fill:       p:spPr / a:solidFill
table cell fill:  a:tcPr / a:solidFill
chart series:     c:ser / c:spPr / a:solidFill
picture fill:     p:blipFill
image-as-fill:    a:blipFill inside shape/table/cell properties
```

### 13.2 Shape outlines and lines

Shape border/outline:

```xml
<p:spPr>
  <a:prstGeom prst="roundRect">
    <a:avLst/>
  </a:prstGeom>

  <a:solidFill>
    <a:srgbClr val="FFFFFF"/>
  </a:solidFill>

  <a:ln w="12700" cap="flat" cmpd="sng" algn="ctr">
    <a:solidFill>
      <a:srgbClr val="4472C4"/>
    </a:solidFill>
    <a:prstDash val="solid"/>
    <a:round/>
  </a:ln>
</p:spPr>
```

Line attributes:

```xml
<a:ln
  w="12700"      <!-- line width; 12700 = 1 pt -->
  cap="flat"    <!-- flat, rnd, sq -->
  cmpd="sng"    <!-- sng, dbl, thickThin, thinThick, tri -->
  algn="ctr">   <!-- ctr or in -->
```

Useful line widths:

| Points | EMUs |
|---:|---:|
| 0.75 pt | `9525` |
| 1 pt | `12700` |
| 1.5 pt | `19050` |
| 2 pt | `25400` |
| 3 pt | `38100` |

Remove a shape border explicitly:

```xml
<a:ln>
  <a:noFill/>
</a:ln>
```

If `a:ln` is omitted, the shape may inherit its line from a style ref or theme.

Dash examples:

```xml
<a:prstDash val="solid"/>
<a:prstDash val="dot"/>
<a:prstDash val="dash"/>
<a:prstDash val="lgDash"/>
<a:prstDash val="dashDot"/>
<a:prstDash val="lgDashDot"/>
<a:prstDash val="lgDashDotDot"/>
<a:prstDash val="sysDash"/>
<a:prstDash val="sysDot"/>
<a:prstDash val="sysDashDot"/>
<a:prstDash val="sysDashDotDot"/>
```

Decorated line:

```xml
<a:ln w="25400" cap="rnd" cmpd="sng" algn="ctr">
  <a:solidFill>
    <a:schemeClr val="accent1"/>
  </a:solidFill>

  <a:prstDash val="dashDot"/>

  <a:round/>
  <!-- or <a:bevel/> -->
  <!-- or <a:miter lim="800000"/> -->
</a:ln>
```

### 13.3 Table borders

PowerPoint table cell borders are usually stored per cell in `a:tcPr` as separate line elements:

```xml
<a:tcPr marL="91440" marR="91440" marT="45720" marB="45720" anchor="ctr">
  <a:lnL w="12700">
    <a:solidFill><a:srgbClr val="D9E2F3"/></a:solidFill>
  </a:lnL>

  <a:lnR w="12700">
    <a:solidFill><a:srgbClr val="D9E2F3"/></a:solidFill>
  </a:lnR>

  <a:lnT w="12700">
    <a:solidFill><a:srgbClr val="D9E2F3"/></a:solidFill>
  </a:lnT>

  <a:lnB w="12700">
    <a:solidFill><a:srgbClr val="D9E2F3"/></a:solidFill>
  </a:lnB>

  <a:solidFill>
    <a:srgbClr val="FFFFFF"/>
  </a:solidFill>
</a:tcPr>
```

Diagonal borders:

```xml
<a:tcPr>
  <a:lnTlToBr w="12700">
    <a:solidFill>
      <a:srgbClr val="808080"/>
    </a:solidFill>
  </a:lnTlToBr>

  <a:lnBlToTr w="12700">
    <a:solidFill>
      <a:srgbClr val="808080"/>
    </a:solidFill>
  </a:lnBlToTr>
</a:tcPr>
```

Suppress a table border explicitly:

```xml
<a:lnB>
  <a:noFill/>
</a:lnB>
```

Practical table-border gotcha:

```text
Internal borders are visually shared, but XML can store both sides:
right border of cell A and left border of adjacent cell B.
For predictable output, set both sides consistently.
```

### 13.4 Padding and vertical alignment in shapes

Shape text padding is on `a:bodyPr`:

```xml
<p:txBody>
  <a:bodyPr
    lIns="91440"
    rIns="91440"
    tIns="45720"
    bIns="45720"
    anchor="ctr"
    wrap="square"/>

  <a:lstStyle/>

  <a:p>
    <a:pPr algn="ctr"/>
    <a:r>
      <a:t>Centered text</a:t>
    </a:r>
  </a:p>
</p:txBody>
```

Shape text layout:

```text
Shape internal padding:       a:bodyPr @lIns/@rIns/@tIns/@bIns
Shape vertical alignment:     a:bodyPr @anchor
Paragraph horizontal align:   a:p/a:pPr @algn
Paragraph indent/margins:     a:p/a:pPr @marL/@marR/@indent
```

Common `anchor` values:

```text
t    top
ctr  middle
b    bottom
```

### 13.5 Padding and vertical alignment in table cells

Table cell padding is on `a:tcPr`, not `a:bodyPr`:

```xml
<a:tc>
  <a:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>
      <a:r>
        <a:t>42%</a:t>
      </a:r>
    </a:p>
  </a:txBody>

  <a:tcPr
    marL="91440"
    marR="91440"
    marT="45720"
    marB="45720"
    anchor="ctr"/>
</a:tc>
```

Table cell text layout:

```text
Table cell padding:           a:tcPr @marL/@marR/@marT/@marB
Table cell vertical align:    a:tcPr @anchor
Cell paragraph horizontal:    a:txBody/a:p/a:pPr @algn
```

---

## 14. Pictures and image fills

### 14.1 Normal inserted pictures

A normal inserted picture is a `p:pic` element under `p:spTree`.

Example:

```xml
<p:pic
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <p:nvPicPr>
    <p:cNvPr id="5" name="Picture 4" descr="Alt text for accessibility"/>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>

  <p:blipFill>
    <a:blip r:embed="rId7" cstate="print"/>
    <a:srcRect/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>

  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>
      <a:ext cx="3657600" cy="2743200"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

The relationship lives in the slide's `.rels` file:

```xml
<!-- ppt/slides/_rels/slide1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId7"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="../media/image1.png"/>
</Relationships>
```

And `[Content_Types].xml` needs image defaults:

```xml
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
```

### 14.2 Embedded vs linked images

Embedded image:

```xml
<a:blip r:embed="rId7"/>
```

Linked image:

```xml
<a:blip r:link="rId8"/>
```

Linked image relationship:

```xml
<Relationship Id="rId8"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
  Target="https://example.com/image.png"
  TargetMode="External"/>
```

### 14.3 Cropping

Cropping is stored in `a:srcRect`, not by editing the underlying image file:

```xml
<!-- Crop 10% from left and right; 5% from top and bottom -->
<a:srcRect l="10000" r="10000" t="5000" b="5000"/>
```

Remember:

```text
100000 = 100%
10000  = 10%
5000   = 5%
```

### 14.4 Image fills inside shapes, tables, and cells

Not every image appears as `p:pic`. Images can also be fills.

Table cell image fill:

```xml
<a:tcPr>
  <a:blipFill>
    <a:blip r:embed="rId9"/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </a:blipFill>
</a:tcPr>
```

In that case:

```text
The image still needs a relationship from the part that contains the a:blip.
For a table on a slide, that usually means ppt/slides/_rels/slideN.xml.rels.
```

Picture creation checklist:

```text
1. Add binary image to /ppt/media/.
2. Add image relationship from slide part.
3. Set a:blip r:embed to that relationship ID.
4. Add or confirm image content type in [Content_Types].xml.
5. Size picture with p:spPr/a:xfrm.
6. Use a:srcRect for crop.
7. Use p:cNvPr/@descr for alt text.
```

---

## 15. Tables

A native editable PowerPoint table is usually inline in the slide XML. It is normally not a separate `/ppt/tables/table1.xml` part.

Main structure:

```xml
<p:graphicFrame
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">

  <p:nvGraphicFramePr>
    <p:cNvPr id="7" name="Table 6"/>
    <p:cNvGraphicFramePr/>
    <p:nvPr/>
  </p:nvGraphicFramePr>

  <p:xfrm>
    <a:off x="914400" y="914400"/>
    <a:ext cx="6400800" cy="2286000"/>
  </p:xfrm>

  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
      <a:tbl>
        <a:tblPr firstRow="1" bandRow="1">
          <a:tableStyleId>{TABLE-STYLE-GUID}</a:tableStyleId>
        </a:tblPr>

        <a:tblGrid>
          <a:gridCol w="2133600"/>
          <a:gridCol w="2133600"/>
          <a:gridCol w="2133600"/>
        </a:tblGrid>

        <a:tr h="762000">
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:rPr lang="en-US" sz="1400" b="1"/>
                  <a:t>Header 1</a:t>
                </a:r>
              </a:p>
            </a:txBody>
            <a:tcPr/>
          </a:tc>

          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:rPr lang="en-US" sz="1400" b="1"/>
                  <a:t>Header 2</a:t>
                </a:r>
              </a:p>
            </a:txBody>
            <a:tcPr/>
          </a:tc>

          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:rPr lang="en-US" sz="1400" b="1"/>
                  <a:t>Header 3</a:t>
                </a:r>
              </a:p>
            </a:txBody>
            <a:tcPr/>
          </a:tc>
        </a:tr>
      </a:tbl>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

Important children:

```text
a:tblPr     whole-table properties and style flags
a:tblGrid   logical column grid
a:gridCol   one per logical column, width in EMUs
a:tr        row, height in EMUs
a:tc        table cell
a:txBody    cell text body
a:tcPr      cell formatting: fills, borders, margins, vertical alignment
```

### 15.1 Table properties and styles

Whole-table formatting starts in `a:tblPr`:

```xml
<a:tblPr firstRow="1" bandRow="1" firstCol="0" bandCol="0">
  <a:tableStyleId>{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}</a:tableStyleId>
</a:tblPr>
```

Common flags:

```text
firstRow
lastRow
firstCol
lastCol
bandRow
bandCol
```

Custom table styles can require:

```text
ppt/tableStyles.xml
ppt/_rels/presentation.xml.rels relationship to tableStyles.xml
[Content_Types].xml override for /ppt/tableStyles.xml
```

Relationship:

```xml
<!-- ppt/_rels/presentation.xml.rels -->
<Relationship Id="rIdTableStyles"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles"
  Target="tableStyles.xml"/>
```

Content type:

```xml
<Override PartName="/ppt/tableStyles.xml"
  ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
```

### 15.2 Cell formatting

Example formatted cell:

```xml
<a:tc>
  <a:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:rPr sz="1400" b="1">
          <a:solidFill>
            <a:srgbClr val="FFFFFF"/>
          </a:solidFill>
        </a:rPr>
        <a:t>Total</a:t>
      </a:r>
    </a:p>
  </a:txBody>

  <a:tcPr marL="45720" marR="45720" marT="22860" marB="22860" anchor="ctr">
    <a:lnL w="12700">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    </a:lnL>
    <a:lnR w="12700">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    </a:lnR>
    <a:lnT w="12700">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    </a:lnT>
    <a:lnB w="12700">
      <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
    </a:lnB>

    <a:solidFill>
      <a:srgbClr val="4472C4"/>
    </a:solidFill>
  </a:tcPr>
</a:tc>
```

### 15.3 Merged cells

Horizontal merge:

```xml
<a:tc gridSpan="3">
  ...
</a:tc>
<a:tc hMerge="1">
  ...
</a:tc>
<a:tc hMerge="1">
  ...
</a:tc>
```

Vertical merge:

```xml
<a:tc rowSpan="3">
  ...
</a:tc>
<a:tc vMerge="1">
  ...
</a:tc>
<a:tc vMerge="1">
  ...
</a:tc>
```

Table editing checklist:

```text
1. Create or clone the whole p:graphicFrame.
2. Keep a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table".
3. Update p:cNvPr/@id and name.
4. Keep a:tblGrid aligned with the logical column count.
5. Keep a:tr heights and a:gridCol widths consistent with the frame size.
6. Put text in a:txBody.
7. Put fills, borders, and cell layout in a:tcPr.
8. Preserve ppt/tableStyles.xml if the table depends on custom styles.
9. Be careful with element order.
```

---

## 16. Connectors and arrowheads

A real PowerPoint connector is usually `p:cxnSp`, not a normal `p:sp`.

Example connector:

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="7" name="Connector 6"/>

    <p:cNvCxnSpPr>
      <a:stCxn id="2" idx="3"/>
      <a:endCxn id="5" idx="1"/>
    </p:cNvCxnSpPr>

    <p:nvPr/>
  </p:nvCxnSpPr>

  <p:spPr>
    <a:xfrm>
      <a:off x="1828800" y="1371600"/>
      <a:ext cx="2743200" cy="1828800"/>
    </a:xfrm>

    <a:prstGeom prst="straightConnector1">
      <a:avLst/>
    </a:prstGeom>

    <a:ln w="19050" cap="flat" cmpd="sng" algn="ctr">
      <a:solidFill>
        <a:srgbClr val="4472C4"/>
      </a:solidFill>
      <a:prstDash val="solid"/>
      <a:headEnd type="none" w="med" len="med"/>
      <a:tailEnd type="triangle" w="med" len="med"/>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

Important rule:

```text
a:stCxn/@id and a:endCxn/@id point to target shape p:cNvPr/@id values.
They are not r:id relationship IDs.
```

Connector mapping:

```text
Object type:          p:cxnSp
Target shapes:        p:cNvCxnSpPr/a:stCxn and a:endCxn
Visual stroke:        p:spPr/a:ln
Arrowheads:           a:ln/a:headEnd and a:ln/a:tailEnd
Connector family:     a:prstGeom @prst
Bend tuning:          a:prstGeom/a:avLst/a:gd, when present
Bounding box:         p:spPr/a:xfrm
Exact auto-route:     application-determined when connected
```

### 16.1 Arrowheads

Arrowheads are children of `a:ln`:

```xml
<a:ln w="19050">
  <a:solidFill>
    <a:srgbClr val="C00000"/>
  </a:solidFill>

  <a:headEnd type="oval" w="sm" len="sm"/>
  <a:tailEnd type="triangle" w="lg" len="lg"/>
</a:ln>
```

Common `type` values:

```text
none
triangle
stealth
diamond
oval
arrow
```

Common `w` and `len` values:

```text
sm
med
lg
```

PowerPoint UI mapping:

```text
Begin Arrow type     -> a:headEnd/@type
Begin Arrow size     -> a:headEnd/@w and @len
End Arrow type       -> a:tailEnd/@type
End Arrow size       -> a:tailEnd/@w and @len
Line dash            -> a:prstDash/@val
Line weight          -> a:ln/@w
Line color           -> a:ln/a:solidFill
```

### 16.2 Elbow and curved connectors

Common preset geometries:

```xml
<a:prstGeom prst="straightConnector1"/>
<a:prstGeom prst="bentConnector2"/>
<a:prstGeom prst="bentConnector3"/>
<a:prstGeom prst="bentConnector4"/>
<a:prstGeom prst="bentConnector5"/>
<a:prstGeom prst="curvedConnector2"/>
<a:prstGeom prst="curvedConnector3"/>
<a:prstGeom prst="curvedConnector4"/>
<a:prstGeom prst="curvedConnector5"/>
```

Some elbow connectors include adjustment guides:

```xml
<a:prstGeom prst="bentConnector3">
  <a:avLst>
    <a:gd name="adj1" fmla="val 50000"/>
  </a:avLst>
</a:prstGeom>
```

Important gotcha:

```text
A connected connector's visible route is not always fully encoded as absolute bend-point coordinates.
PowerPoint can reroute it based on connection sites, nearby shapes, and its own routing algorithm.
```

If you need a real connector:

```text
Use p:cxnSp with a:stCxn and a:endCxn.
Accept possible PowerPoint rerouting.
```

If you need a fixed polyline-looking object:

```text
Use an unconnected connector, custom geometry shape, or grouped line segments.
It will not behave like a true connector when target shapes move.
```

Unconnected elbow example:

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="9" name="Elbow Connector 8"/>
    <p:cNvCxnSpPr/>
    <p:nvPr/>
  </p:nvCxnSpPr>

  <p:spPr>
    <a:xfrm flipH="0" flipV="0">
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="1200000"/>
    </a:xfrm>

    <a:prstGeom prst="bentConnector3">
      <a:avLst>
        <a:gd name="adj1" fmla="val 45000"/>
      </a:avLst>
    </a:prstGeom>

    <a:ln w="12700">
      <a:solidFill>
        <a:srgbClr val="000000"/>
      </a:solidFill>
      <a:tailEnd type="triangle" w="med" len="med"/>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

---

## 17. Group shapes

A group shape is `p:grpSp`. It is a container of shapes, pictures, graphic frames, connectors, and nested groups.

Typical structure:

```xml
<p:grpSp>
  <p:nvGrpSpPr>
    <p:cNvPr id="10" name="Group 9"/>
    <p:cNvGrpSpPr/>
    <p:nvPr/>
  </p:nvGrpSpPr>

  <p:grpSpPr>
    <a:xfrm>
      <a:off   x="1000000" y="1000000"/>
      <a:ext   cx="4000000" cy="2000000"/>
      <a:chOff x="0"       y="0"/>
      <a:chExt cx="2000000" cy="1000000"/>
    </a:xfrm>
  </p:grpSpPr>

  <p:sp>...</p:sp>
  <p:pic>...</p:pic>
  <p:graphicFrame>...</p:graphicFrame>
  <p:grpSp>...</p:grpSp>
</p:grpSp>
```

Group transform has two rectangles:

```text
off/ext      = where the group appears in the parent coordinate system
chOff/chExt  = the internal child-coordinate rectangle
```

Mapping:

```text
scaleX = ext.cx / chExt.cx
scaleY = ext.cy / chExt.cy

parentX  = off.x + (childX  - chOff.x) * scaleX
parentY  = off.y + (childY  - chOff.y) * scaleY
parentCx = childCx * scaleX
parentCy = childCy * scaleY
```

Example:

```xml
<a:off   x="1000000" y="1000000"/>
<a:ext   cx="4000000" cy="2000000"/>
<a:chOff x="0"       y="0"/>
<a:chExt cx="2000000" cy="1000000"/>
```

Child:

```xml
<a:off x="500000" y="250000"/>
<a:ext cx="1000000" cy="500000"/>
```

Mapping:

```text
scaleX = 4000000 / 2000000 = 2
scaleY = 2000000 / 1000000 = 2

parent x  = 1000000 + (500000 - 0) * 2 = 2000000
parent y  = 1000000 + (250000 - 0) * 2 = 1500000
parent cx = 1000000 * 2 = 2000000
parent cy = 500000 * 2 = 1000000
```

If all four values match:

```xml
<a:off   x="838200" y="990600"/>
<a:ext   cx="2426208" cy="978408"/>
<a:chOff x="838200" y="990600"/>
<a:chExt cx="2426208" cy="978408"/>
```

then child coordinates are effectively already in the parent coordinate system.

Group transforms can also have:

```xml
<a:xfrm rot="5400000" flipH="1">
  ...
</a:xfrm>
```

Remember:

```text
rot="5400000" = 90 degrees
```

For nested groups, apply mappings recursively from inner group to outer group to slide.

---

## 18. Custom geometry and freeform paths

Custom geometry uses `a:custGeom` inside `p:spPr` instead of a preset geometry.

Example:

```xml
<p:sp>
  <p:nvSpPr>...</p:nvSpPr>

  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>
      <a:ext cx="3657600" cy="1828800"/>
    </a:xfrm>

    <a:custGeom>
      <a:avLst/>
      <a:gdLst/>
      <a:ahLst/>
      <a:cxnLst/>
      <a:rect l="0" t="0" r="21600" b="21600"/>

      <a:pathLst>
        <a:path w="21600" h="21600" fill="norm" stroke="1">
          <a:moveTo>
            <a:pt x="0" y="21600"/>
          </a:moveTo>

          <a:lnTo>
            <a:pt x="10800" y="0"/>
          </a:lnTo>

          <a:quadBezTo>
            <a:pt x="16200" y="0"/>
            <a:pt x="21600" y="10800"/>
          </a:quadBezTo>

          <a:cubicBezTo>
            <a:pt x="21600" y="16200"/>
            <a:pt x="16200" y="21600"/>
            <a:pt x="10800" y="21600"/>
          </a:cubicBezTo>

          <a:close/>
        </a:path>
      </a:pathLst>
    </a:custGeom>
  </p:spPr>
</p:sp>
```

The `a:path` element defines a path coordinate system:

```xml
<a:path w="21600" h="21600">
```

The shape's displayed EMU box is controlled by `a:xfrm`:

```xml
<a:off x="914400" y="914400"/>
<a:ext cx="3657600" cy="1828800"/>
```

Path-to-shape scaling:

```text
shapeX = shapeOff.x + pathX * shapeExt.cx / path@w
shapeY = shapeOff.y + pathY * shapeExt.cy / path@h
```

Common path commands:

```text
a:moveTo       move pen without drawing
a:lnTo         line to point
a:quadBezTo    quadratic Bezier: control point + endpoint
a:cubicBezTo   cubic Bezier: control1 + control2 + endpoint
a:arcTo        elliptical arc using radii and angles
a:close        close current subpath
```

`a:arcTo` attributes include:

```text
wR
hR
stAng
swAng
```

Arc angles use the same 60,000ths-of-a-degree convention.

Practical convention:

```text
Normalize generated freeforms to a 21600 x 21600 path box when possible.
PowerPoint may also write path coordinates in a larger internal box.
Both are valid if path@w/h and a:xfrm/a:ext agree.
```

---

## 19. Hyperlinks

PowerPoint uses `a:hlinkClick` in different locations.

### 19.1 Shape-level hyperlink

For a whole shape, the hyperlink is under `p:cNvPr`:

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="4" name="Rectangle 3">
      <a:hlinkClick r:id="rId7" tooltip="Open website"/>
    </p:cNvPr>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  ...
</p:sp>
```

This makes the entire shape clickable.

### 19.2 Text-run hyperlink

For only part of text, the hyperlink is under run properties:

```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US">
      <a:hlinkClick r:id="rId5" tooltip="Details"/>
    </a:rPr>
    <a:t>Details</a:t>
  </a:r>
</a:p>
```

### 19.3 External URL

In slide XML:

```xml
<a:hlinkClick r:id="rId5"/>
```

In `ppt/slides/_rels/slide1.xml.rels`:

```xml
<Relationship
  Id="rId5"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
  Target="https://example.com/"
  TargetMode="External"/>
```

### 19.4 Slide-to-slide jump

In slide XML:

```xml
<a:hlinkClick
  r:id="rId6"
  action="ppaction://hlinksldjump"/>
```

In `slide1.xml.rels`:

```xml
<Relationship
  Id="rId6"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
  Target="slide2.xml"/>
```

### 19.5 Navigation actions

For next/previous/first/last slide, PowerPoint may encode behavior mostly in the `action` attribute:

```xml
<a:hlinkClick action="ppaction://hlinkshowjump?jump=nextslide"/>
```

Practical distinction:

```text
External URL/file:
  relationship type = hyperlink
  TargetMode         = External
  Target             = URL or file path

Specific slide in same deck:
  action             = ppaction://hlinksldjump
  relationship type = slide
  TargetMode         = usually internal / omitted
  Target             = another slide part

Navigation jump:
  action             = ppaction://hlinkshowjump?jump=nextslide, etc.
  relationship       = often not needed
```

---

## 20. Charts: architecture and data model

A native editable chart normally has three layers:

```text
slideN.xml
  -> relationship to chartN.xml or chartExN.xml
       -> relationship to embedded workbook .xlsx
```

For standard charts:

```text
slideN.xml
  p:graphicFrame
    a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart"
      c:chart r:id="rId5"

slideN.xml.rels
  rId5 -> ../charts/chart1.xml

ppt/charts/chart1.xml
  c:chartSpace

ppt/charts/_rels/chart1.xml.rels
  rId1 -> ../embeddings/Microsoft_Excel_Worksheet1.xlsx

ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx
  editable data workbook
```

For ChartEx charts:

```text
slideN.xml
  p:graphicFrame
    a:graphicData uri="http://schemas.microsoft.com/office/drawing/2014/chartex"
      cx:chart r:id="rId6"

slideN.xml.rels
  rId6 -> ../charts/chartEx1.xml

ppt/charts/chartEx1.xml
  cx:chartSpace

ppt/charts/_rels/chartEx1.xml.rels
  rId1 -> ../embeddings/Microsoft_Excel_Worksheet2.xlsx
```

### 20.1 Standard chart frame on a slide

```xml
<p:graphicFrame xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:nvGraphicFramePr>
    <p:cNvPr id="4" name="Chart 3"/>
    <p:cNvGraphicFramePr/>
    <p:nvPr/>
  </p:nvGraphicFramePr>

  <p:xfrm>
    <a:off x="914400" y="914400"/>
    <a:ext cx="7315200" cy="4114800"/>
  </p:xfrm>

  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
      <c:chart r:id="rId5"/>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

Slide relationship:

```xml
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId5"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart"
    Target="../charts/chart1.xml"/>
</Relationships>
```

### 20.2 Standard chart part

```xml
<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <c:lang val="en-US"/>

  <c:chart>
    <c:plotArea>
      ...
    </c:plotArea>
  </c:chart>

  <c:externalData r:id="rId1">
    <c:autoUpdate val="0"/>
  </c:externalData>
</c:chartSpace>
```

Chart relationship to embedded workbook:

```xml
<!-- ppt/charts/_rels/chart1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package"
    Target="../embeddings/Microsoft_Excel_Worksheet1.xlsx"/>
</Relationships>
```

### 20.3 Workbook plus chart cache

PowerPoint-generated charts usually duplicate data:

```text
1. Embedded workbook in ppt/embeddings/*.xlsx
   Opens when the user chooses "Edit Data."

2. Cached chart data inside chart XML
   Used by renderers and often shown even before workbook refresh.
```

Example cache:

```xml
<c:ser>
  <c:idx val="0"/>
  <c:order val="0"/>

  <c:tx>
    <c:strRef>
      <c:f>Sheet1!$B$1</c:f>
      <c:strCache>
        <c:ptCount val="1"/>
        <c:pt idx="0"><c:v>Revenue</c:v></c:pt>
      </c:strCache>
    </c:strRef>
  </c:tx>

  <c:cat>
    <c:strRef>
      <c:f>Sheet1!$A$2:$A$4</c:f>
      <c:strCache>...</c:strCache>
    </c:strRef>
  </c:cat>

  <c:val>
    <c:numRef>
      <c:f>Sheet1!$B$2:$B$4</c:f>
      <c:numCache>...</c:numCache>
    </c:numRef>
  </c:val>
</c:ser>
```

Practical rule:

```text
For reliable generated decks, update both the embedded workbook and chart XML caches/formulas.
```

### 20.4 Embedded workbook patterns by chart type

The embedding mechanism is mostly the same across chart types:

```text
slide -> chart part -> optional embedded workbook part
```

What changes is the chart-type XML inside `c:plotArea`.

| Chart type | Main XML | Data references |
|---|---|---|
| Column/bar/line/area | `c:barChart`, `c:lineChart`, etc. | Series usually have `c:cat` and `c:val` |
| Pie/doughnut | `c:pieChart`, `c:doughnutChart` | Series have categories/values, usually no axes |
| Scatter | `c:scatterChart` | Series use `c:xVal` and `c:yVal` |
| Bubble | `c:bubbleChart` | Uses `c:xVal`, `c:yVal`, and `c:bubbleSize` |
| Combo | Multiple chart-type siblings in one `c:plotArea` | Series split across chart-type elements, often sharing axes |

Simple category workbook layout:

```text
       A        B        C
1               Sales    Profit
2   Q1          10       3
3   Q2          12       4
4   Q3          9        2
```

Corresponding formulas:

```xml
<c:f>Sheet1!$A$2:$A$4</c:f>  <!-- categories -->
<c:f>Sheet1!$B$2:$B$4</c:f>  <!-- first series values -->
<c:f>Sheet1!$C$2:$C$4</c:f>  <!-- second series values -->
```

---

## 21. Standard `c:*` charts

Standard charts use:

```text
c:chartSpace
  c:chart
    c:plotArea
      c:barChart / c:lineChart / c:pieChart / ...
      c:catAx / c:valAx / ...
```

Common standard chart elements:

```text
c:barChart
c:lineChart
c:areaChart
c:pieChart
c:doughnutChart
c:scatterChart
c:bubbleChart
c:ser
c:cat
c:val
c:xVal
c:yVal
c:bubbleSize
c:axId
c:catAx
c:valAx
c:dateAx
c:serAx
```

### 21.1 Stacked column chart

A stacked column chart is a standard `c:barChart`.

Key switch:

```xml
<c:barChart>
  <c:barDir val="col"/>
  <c:grouping val="stacked"/>
  ...
</c:barChart>
```

`barDir`:

```text
col = vertical columns
bar = horizontal bars
```

`grouping` examples:

```text
clustered
stacked
percentStacked
standard
```

Minimal stacked column skeleton:

```xml
<c:chartSpace
  xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <c:lang val="en-US"/>

  <c:chart>
    <c:title>
      <c:tx>
        <c:rich>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:t>Stacked column example</a:t>
            </a:r>
          </a:p>
        </c:rich>
      </c:tx>
      <c:overlay val="0"/>
    </c:title>

    <c:plotArea>
      <c:layout/>

      <c:barChart>
        <c:barDir val="col"/>
        <c:grouping val="stacked"/>
        <c:varyColors val="0"/>

        <c:ser>
          <c:idx val="0"/>
          <c:order val="0"/>
          <c:tx>
            <c:strRef>
              <c:f>Sheet1!$B$1</c:f>
              <c:strCache>
                <c:ptCount val="1"/>
                <c:pt idx="0"><c:v>Product A</c:v></c:pt>
              </c:strCache>
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
                <c:pt idx="0"><c:v>10</c:v></c:pt>
                <c:pt idx="1"><c:v>15</c:v></c:pt>
                <c:pt idx="2"><c:v>18</c:v></c:pt>
                <c:pt idx="3"><c:v>20</c:v></c:pt>
              </c:numCache>
            </c:numRef>
          </c:val>
        </c:ser>

        <c:gapWidth val="150"/>
        <c:overlap val="100"/>
        <c:axId val="123456"/>
        <c:axId val="123457"/>
      </c:barChart>

      <c:catAx>
        <c:axId val="123456"/>
        <c:scaling><c:orientation val="minMax"/></c:scaling>
        <c:axPos val="b"/>
        <c:tickLblPos val="nextTo"/>
        <c:crossAx val="123457"/>
        <c:crosses val="autoZero"/>
        <c:auto val="1"/>
        <c:lblAlgn val="ctr"/>
        <c:lblOffset val="100"/>
      </c:catAx>

      <c:valAx>
        <c:axId val="123457"/>
        <c:scaling><c:orientation val="minMax"/></c:scaling>
        <c:axPos val="l"/>
        <c:majorGridlines/>
        <c:numFmt formatCode="General" sourceLinked="1"/>
        <c:tickLblPos val="nextTo"/>
        <c:crossAx val="123456"/>
        <c:crosses val="autoZero"/>
      </c:valAx>
    </c:plotArea>

    <c:legend>
      <c:legendPos val="r"/>
      <c:overlay val="0"/>
    </c:legend>

    <c:plotVisOnly val="1"/>
  </c:chart>

  <c:externalData r:id="rId1">
    <c:autoUpdate val="0"/>
  </c:externalData>
</c:chartSpace>
```

Element order matters in chart XML. A reliable strategy is to clone a PowerPoint-authored chart of the target type and modify the values, relationships, workbook, and caches.

---

## 22. ChartEx `cx:*` charts and waterfall charts

Native Office waterfall charts are usually ChartEx charts, not standard `c:barChart` charts.

Key differences:

| Feature | Standard chart | ChartEx chart |
|---|---|---|
| Main namespace | `c` | `cx` |
| Slide graphicData URI | `http://schemas.openxmlformats.org/drawingml/2006/chart` | `http://schemas.microsoft.com/office/drawing/2014/chartex` |
| Slide reference | `c:chart r:id="..."` | `cx:chart r:id="..."` |
| Relationship type | `.../officeDocument/2006/relationships/chart` | `http://schemas.microsoft.com/office/2014/relationships/chartEx` |
| Part root | `c:chartSpace` | `cx:chartSpace` |
| Content type | `application/vnd.openxmlformats-officedocument.drawingml.chart+xml` | `application/vnd.ms-office.chartex+xml` |

### 22.1 ChartEx frame on slide

```xml
<p:graphicFrame xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:nvGraphicFramePr>
    <p:cNvPr id="5" name="Waterfall Chart 4"/>
    <p:cNvGraphicFramePr/>
    <p:nvPr/>
  </p:nvGraphicFramePr>

  <p:xfrm>
    <a:off x="914400" y="914400"/>
    <a:ext cx="7315200" cy="4114800"/>
  </p:xfrm>

  <a:graphic>
    <a:graphicData uri="http://schemas.microsoft.com/office/drawing/2014/chartex">
      <cx:chart r:id="rId6"/>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

Slide relationship:

```xml
<!-- ppt/slides/_rels/slide1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId6"
    Type="http://schemas.microsoft.com/office/2014/relationships/chartEx"
    Target="../charts/chartEx1.xml"/>
</Relationships>
```

### 22.2 Waterfall ChartEx skeleton

The key waterfall marker is:

```xml
<cx:series layoutId="waterfall">
```

Example:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cx:chartSpace
  xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <cx:chartData>
    <cx:externalData r:id="rId1" autoUpdate="0"/>

    <cx:data id="0">
      <cx:strDim type="cat">
        <cx:f>Sheet1!$A$2:$A$7</cx:f>
        <cx:lvl ptCount="6">
          <cx:pt idx="0">Start</cx:pt>
          <cx:pt idx="1">Revenue</cx:pt>
          <cx:pt idx="2">COGS</cx:pt>
          <cx:pt idx="3">Operating expense</cx:pt>
          <cx:pt idx="4">Tax</cx:pt>
          <cx:pt idx="5">End</cx:pt>
        </cx:lvl>
      </cx:strDim>

      <cx:numDim type="val">
        <cx:f>Sheet1!$B$2:$B$7</cx:f>
        <cx:lvl ptCount="6" formatCode="General">
          <cx:pt idx="0">100</cx:pt>
          <cx:pt idx="1">40</cx:pt>
          <cx:pt idx="2">-30</cx:pt>
          <cx:pt idx="3">-20</cx:pt>
          <cx:pt idx="4">-10</cx:pt>
          <cx:pt idx="5">80</cx:pt>
        </cx:lvl>
      </cx:numDim>
    </cx:data>
  </cx:chartData>

  <cx:chart>
    <cx:title pos="t" align="ctr" overlay="0">
      <cx:tx>
        <cx:txData>
          <cx:v>Waterfall example</cx:v>
        </cx:txData>
      </cx:tx>
    </cx:title>

    <cx:plotArea>
      <cx:plotAreaRegion>
        <cx:series layoutId="waterfall" formatIdx="0">
          <cx:tx>
            <cx:txData>
              <cx:v>Bridge</cx:v>
            </cx:txData>
          </cx:tx>

          <cx:dataId val="0"/>

          <cx:layoutPr>
            <cx:visibility connectorLines="1"/>
            <cx:subtotals>
              <cx:idx val="0"/>
              <cx:idx val="5"/>
            </cx:subtotals>
          </cx:layoutPr>

          <cx:axisId>1001</cx:axisId>
          <cx:axisId>1002</cx:axisId>
        </cx:series>
      </cx:plotAreaRegion>

      <cx:axis id="1001">
        <cx:catScaling gapWidth="0.7"/>
        <cx:tickLabels/>
      </cx:axis>

      <cx:axis id="1002">
        <cx:valScaling/>
        <cx:majorGridlines/>
        <cx:tickLabels/>
      </cx:axis>
    </cx:plotArea>

    <cx:legend pos="r" align="ctr" overlay="0"/>
  </cx:chart>
</cx:chartSpace>
```

ChartEx relationship to embedded workbook:

```xml
<!-- ppt/charts/_rels/chartEx1.xml.rels -->
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package"
    Target="../embeddings/Microsoft_Excel_Worksheet2.xlsx"/>
</Relationships>
```

Content types:

```xml
<Override PartName="/ppt/charts/chartEx1.xml"
  ContentType="application/vnd.ms-office.chartex+xml"/>

<Override PartName="/ppt/embeddings/Microsoft_Excel_Worksheet2.xlsx"
  ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/>
```

Practical ChartEx rule:

```text
Do not try to make native waterfall by setting c:barChart options.
Clone a PowerPoint-authored ChartEx waterfall and modify cx:data, embedded workbook, and caches.
```

---

## 23. Detailed chart formatting

Chart formatting is usually attached at the most specific available level:

```text
data point formatting
  overrides series formatting
    overrides chart-type/chart/theme defaults
```

### 23.1 Data labels

Chart-type-wide or series-wide labels use `c:dLbls`:

```xml
<c:barChart>
  ...

  <c:dLbls>
    <c:numFmt formatCode="#,##0" sourceLinked="0"/>

    <c:txPr>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr>
          <a:defRPr sz="900">
            <a:solidFill>
              <a:schemeClr val="tx1"/>
            </a:solidFill>
            <a:latin typeface="+mn-lt"/>
          </a:defRPr>
        </a:pPr>
      </a:p>
    </c:txPr>

    <c:dLblPos val="outEnd"/>
    <c:showVal val="1"/>
    <c:showCatName val="0"/>
    <c:showSerName val="0"/>
    <c:showLegendKey val="0"/>
  </c:dLbls>
</c:barChart>
```

Individual data-label override:

```xml
<c:dLbls>
  <c:dLbl>
    <c:idx val="2"/>
    <c:numFmt formatCode="0.0%" sourceLinked="0"/>
    <c:dLblPos val="ctr"/>
    <c:showVal val="1"/>
    <c:showCatName val="1"/>
  </c:dLbl>
</c:dLbls>
```

Common `c:dLblPos` values:

```text
bestFit
b
ctr
inBase
inEnd
l
outEnd
r
t
```

### 23.2 Axis and label text formatting

Chart text formatting uses `c:txPr`, containing DrawingML text-body pieces:

```xml
<c:catAx>
  <c:axId val="100"/>
  ...

  <c:txPr>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:pPr>
        <a:defRPr sz="1000">
          <a:solidFill>
            <a:schemeClr val="tx1"/>
          </a:solidFill>
          <a:latin typeface="+mn-lt"/>
        </a:defRPr>
      </a:pPr>
    </a:p>
  </c:txPr>
</c:catAx>
```

Remember:

```text
sz="1000" = 10 pt
```

### 23.3 Series fill and outline

Series formatting:

```xml
<c:ser>
  <c:idx val="0"/>
  <c:order val="0"/>

  <c:spPr>
    <a:solidFill>
      <a:schemeClr val="accent1"/>
    </a:solidFill>

    <a:ln w="12700">
      <a:solidFill>
        <a:schemeClr val="accent1"/>
      </a:solidFill>
    </a:ln>
  </c:spPr>

  ...
</c:ser>
```

For bar/column charts, this is usually bar fill/outline.

For line charts, the important part is usually the line:

```xml
<c:spPr>
  <a:ln w="25400">
    <a:solidFill>
      <a:schemeClr val="accent2"/>
    </a:solidFill>
  </a:ln>
</c:spPr>
```

### 23.4 Per-data-point formatting

A single data point override uses `c:dPt` under `c:ser`:

```xml
<c:ser>
  <c:idx val="0"/>
  <c:order val="0"/>

  <c:spPr>
    <a:solidFill>
      <a:schemeClr val="accent1"/>
    </a:solidFill>
  </c:spPr>

  <c:dPt>
    <c:idx val="2"/>
    <c:spPr>
      <a:solidFill>
        <a:srgbClr val="FF0000"/>
      </a:solidFill>
      <a:ln>
        <a:solidFill>
          <a:srgbClr val="990000"/>
        </a:solidFill>
      </a:ln>
    </c:spPr>
  </c:dPt>
</c:ser>
```

Specificity:

```text
point formatting:   c:ser/c:dPt/c:spPr
overrides
series formatting:  c:ser/c:spPr
overrides
chart/theme defaults
```

### 23.5 Combo charts

A combo chart is usually multiple chart-type siblings in one `c:plotArea`, sharing one or more axes.

Clustered column + line:

```xml
<c:plotArea>
  <c:barChart>
    <c:barDir val="col"/>
    <c:grouping val="clustered"/>
    <c:ser>...</c:ser>
    <c:axId val="100"/>
    <c:axId val="200"/>
  </c:barChart>

  <c:lineChart>
    <c:grouping val="standard"/>
    <c:ser>...</c:ser>
    <c:axId val="100"/>
    <c:axId val="200"/>
  </c:lineChart>

  <c:catAx>
    <c:axId val="100"/>
    <c:crossAx val="200"/>
  </c:catAx>

  <c:valAx>
    <c:axId val="200"/>
    <c:crossAx val="100"/>
  </c:valAx>
</c:plotArea>
```

Secondary-axis combo:

```xml
<c:barChart>
  ...
  <c:axId val="100"/>  <!-- category axis -->
  <c:axId val="200"/>  <!-- primary value axis -->
</c:barChart>

<c:lineChart>
  ...
  <c:axId val="100"/>  <!-- same category axis -->
  <c:axId val="300"/>  <!-- secondary value axis -->
</c:lineChart>

<c:valAx>
  <c:axId val="200"/>
  <c:crossAx val="100"/>
</c:valAx>

<c:valAx>
  <c:axId val="300"/>
  <c:crossAx val="100"/>
</c:valAx>
```

Convention:

```text
Chart-type siblings share axes by repeating the same c:axId values.
```

---

## 24. Slide numbers, dates, and footers

Three separate concepts work together:

```text
1. p:hf flags
   Enable or disable date/footer/slide-number placeholders.

2. Placeholder shapes
   p:ph type="sldNum", type="dt", or type="ftr".

3. Dynamic text fields
   a:fld type="slidenum" or type="datetime..."
```

### 24.1 Header/footer flags

`p:hf` appears on slide masters/layouts, notes masters, and handout masters:

```xml
<p:hf dt="1" ftr="1" sldNum="1"/>
```

Attributes:

```text
dt      = date/time placeholder enabled
ftr     = footer placeholder enabled
hdr     = header placeholder enabled; mainly notes/handouts
sldNum  = slide number placeholder enabled
```

To explicitly hide slide numbers:

```xml
<p:hf sldNum="0"/>
```

### 24.2 Placeholder shapes

Slide number placeholder example:

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="6" name="Slide Number Placeholder 5"/>
    <p:cNvSpPr/>
    <p:nvPr>
      <p:ph type="sldNum" idx="12"/>
    </p:nvPr>
  </p:nvSpPr>

  <p:spPr>
    <a:xfrm>
      <a:off x="11000000" y="6500000"/>
      <a:ext cx="800000" cy="300000"/>
    </a:xfrm>
  </p:spPr>

  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:fld id="{424CEEAC-8F67-4238-9622-1B74DC6E8318}" type="slidenum">
        <a:rPr lang="en-US"/>
        <a:pPr/>
        <a:t>3</a:t>
      </a:fld>
      <a:endParaRPr lang="en-US"/>
    </a:p>
  </p:txBody>
</p:sp>
```

Placeholder roles:

```xml
<p:ph type="sldNum"/>  <!-- slide number -->
<p:ph type="dt"/>      <!-- date/time -->
<p:ph type="ftr"/>     <!-- footer -->
```

### 24.3 Dynamic fields

Slide number field:

```xml
<a:fld id="{424CEEAC-8F67-4238-9622-1B74DC6E8318}" type="slidenum">
  <a:rPr lang="en-US"/>
  <a:pPr/>
  <a:t>3</a:t>
</a:fld>
```

Date/time field:

```xml
<a:fld id="{B2D8D8B9-8048-46F4-9E7A-6D1B7C55D8D3}" type="datetime1">
  <a:rPr lang="en-US"/>
  <a:t>05/28/2026</a:t>
</a:fld>
```

Footer text is often normal text inside a footer placeholder:

```xml
<p:ph type="ftr" idx="11"/>
...
<a:r>
  <a:rPr lang="en-US"/>
  <a:t>Confidential</a:t>
</a:r>
```

Field cached value rule:

```text
a:t stores the last cached visible text.
PowerPoint or another renderer can update it from a:fld/@type.
```

Rendering chain:

```text
p:hf says whether the placeholder kind is enabled
  +
p:ph type says this shape is the date/footer/slide-number placeholder
  +
a:fld type tells PowerPoint what dynamic value to render
  +
a:t stores the last cached value
```

Common field types include:

```text
slidenum
datetime
datetime1
datetime2
...
datetime13
```

---

## 25. Practical workflows

### 25.1 How to inspect a `.pptx`

```text
1. Duplicate the .pptx.
2. Rename .pptx to .zip or unzip it.
3. Start at ppt/presentation.xml.
4. Use ppt/_rels/presentation.xml.rels to map slide/master IDs to files.
5. Open ppt/slides/slideN.xml for visible slide objects.
6. Open ppt/slides/_rels/slideN.xml.rels for charts, images, hyperlinks, and layouts.
7. For charts, inspect ppt/charts/chartN.xml or chartExN.xml.
8. For chart workbooks, inspect ppt/charts/_rels/chartN.xml.rels and ppt/embeddings/*.xlsx.
9. For theme resolution, inspect ppt/theme/themeN.xml and p:clrMap/p:clrMapOvr.
10. For placeholders, inspect slide -> layout -> master by p:ph/@idx.
11. Check [Content_Types].xml for required overrides/defaults.
12. Open in PowerPoint and compare after save/normalization.
```

### 25.2 How to clone a shape

```text
1. Clone the whole p:sp.
2. Assign a new unique p:cNvPr/@id.
3. Change p:cNvPr/@name as needed.
4. Update a:xfrm position/size.
5. If it contains hyperlinks, clone/update the slide relationships.
6. If it is a placeholder, be careful with p:ph/@idx.
7. Preserve element order.
```

### 25.3 How to clone a picture

```text
1. Clone p:pic.
2. Assign a new p:cNvPr/@id.
3. Copy or reuse the image part in /ppt/media/.
4. Add an image relationship from the slide part.
5. Set a:blip r:embed to the new relationship ID.
6. Confirm image content type default in [Content_Types].xml.
7. Update a:xfrm and a:srcRect if needed.
8. Update p:cNvPr/@descr for alt text.
```

### 25.4 How to clone a table

```text
1. Clone the p:graphicFrame containing a:tbl.
2. Assign a new p:cNvPr/@id.
3. Update p:xfrm position/size.
4. Update a:tblGrid column widths and a:tr heights if resizing structurally.
5. Update cell text in a:txBody.
6. Update cell fills/borders/margins in a:tcPr.
7. Preserve custom table styles if used.
```

### 25.5 How to clone a standard chart

```text
1. Clone the slide p:graphicFrame.
2. Assign a new p:cNvPr/@id.
3. Create a new slide relationship to a new chart part.
4. Copy ppt/charts/chartN.xml to a new chart file.
5. Copy ppt/charts/_rels/chartN.xml.rels.
6. Copy the embedded workbook to a new file in ppt/embeddings/.
7. Update chart part relationship to the new workbook.
8. Update [Content_Types].xml overrides for chart and workbook.
9. Update workbook cell values.
10. Update chart XML formulas and caches.
11. Update c:axId values if needed to avoid accidental collisions in the same chart context.
12. Open in PowerPoint and verify/normalize.
```

### 25.6 How to clone a ChartEx waterfall chart

```text
1. Clone a PowerPoint-authored waterfall chart.
2. Clone the slide p:graphicFrame with cx:chart r:id.
3. Add a chartEx relationship from the slide.
4. Copy chartExN.xml.
5. Copy chartExN.xml.rels.
6. Copy the embedded workbook.
7. Update cx:externalData relationship.
8. Update cx:chartData/cx:data values and formulas.
9. Update cx:series layoutId="waterfall" subtotals if needed.
10. Update content type override for chartEx.
11. Open in PowerPoint and validate.
```

### 25.7 How to clone a slide

```text
1. Copy the slide XML part.
2. Copy the slide .rels file.
3. Copy or reuse all referenced parts: charts, images, media, hyperlinks, embedded workbooks.
4. Add a new relationship from presentation.xml.rels to the new slide part.
5. Add a new p:sldId entry to p:sldIdLst with a unique p:sldId/@id.
6. If using sections, add the new p:sldId/@id to p14:sectionLst.
7. Confirm content types for the new slide and dependent parts.
8. Be careful with duplicate chart part names and embedded workbook names.
```

---

## 26. What must be updated together

| Feature | Must update together |
|---|---|
| Picture | `p:pic`, slide image relationship, `/ppt/media/*`, image content type default |
| Image fill | `a:blipFill`, relationship from containing part, `/ppt/media/*`, content type |
| Standard chart | slide `p:graphicFrame`, slide chart relationship, `chartN.xml`, chart relationship, embedded workbook, content type overrides |
| ChartEx waterfall | slide `cx:chart`, `chartEx` relationship, `chartExN.xml`, ChartEx relationship, embedded workbook, ChartEx content type |
| Chart data | embedded workbook cells, chart formulas, chart caches |
| Table with custom style | inline `a:tbl`, `ppt/tableStyles.xml`, presentation relationship, content type override |
| Slide section | `p14:sectionLst` and matching `p:sldId/@id` values |
| Placeholder inheritance | slide placeholder `p:ph/@idx` and matching layout placeholder |
| Connector | `p:cxnSp`, target shapes' `p:cNvPr/@id`, `a:stCxn/@id`, `a:endCxn/@id` |
| Hyperlink | `a:hlinkClick`, slide relationship, `TargetMode` if external |
| Slide jump | `a:hlinkClick action`, relationship to target slide if specific slide |
| Slide number/date/footer | `p:hf`, `p:ph` placeholder, `a:fld`, cached `a:t` |
| Group shape | `p:grpSpPr/a:xfrm` `off/ext/chOff/chExt`, child transforms |
| Theme color | `a:schemeClr`, `p:clrMap`/`p:clrMapOvr`, `theme1.xml` |

---

## 27. Common gotchas

```text
r:id is local to the current part's .rels file.
```

```text
p:cNvPr/@id is not r:id.
```

```text
p:ph/@idx is the placeholder inheritance key.
```

```text
p14:section/p14:sldId/@id refers to p:sldId/@id, not r:id and not slide1.xml.
```

```text
Element order matters in OOXML. Clone PowerPoint-authored samples or use typed SDK classes when possible.
```

```text
Omitted formatting may inherit from theme/layout/master.
```

```text
A chart's visible data may come from XML cache even if the workbook exists.
```

```text
Waterfall is usually ChartEx, not standard c:barChart.
```

```text
Native tables are usually inline a:tbl objects, not separate table parts.
```

```text
Pictures can be p:pic or a:blipFill inside shape/table/cell properties.
```

```text
Connector routing can be recalculated by PowerPoint.
```

```text
Slide number/date fields have cached text in a:t.
```

```text
Horizontal alignment is usually a:pPr/@algn, not bodyPr or tcPr.
```

```text
Shape padding and table-cell padding use different attributes:
shape = a:bodyPr @lIns/@rIns/@tIns/@bIns
cell  = a:tcPr @marL/@marR/@marT/@marB
```

```text
Internal table borders may need both adjacent cell sides set consistently.
```

```text
Text size sz uses hundredths of a point; line width w uses EMUs.
```

```text
Rotation uses 60,000ths of a degree.
```

```text
Percentage values often use 100000 = 100%.
```

---

## 28. Appendices

### Appendix A: UI feature to XML location

| PowerPoint feature | Main XML location |
|---|---|
| Slide order | `ppt/presentation.xml / p:sldIdLst` |
| Slide size | `ppt/presentation.xml / p:sldSz` |
| Notes size | `ppt/presentation.xml / p:notesSz` |
| Sections | `presentation.xml / p:extLst / p14:sectionLst` |
| Slide master list | `presentation.xml / p:sldMasterIdLst` |
| Slide content | `slideN.xml / p:cSld / p:spTree` |
| Shape | `slideN.xml / p:spTree / p:sp` |
| Text box | `p:sp / p:txBody` |
| Picture | `slideN.xml / p:spTree / p:pic` |
| Image file | `/ppt/media/imageN.*` + slide relationship |
| Table | `p:graphicFrame / a:graphicData / a:tbl` |
| Standard chart | `p:graphicFrame / c:chart r:id` + `ppt/charts/chartN.xml` |
| Waterfall chart | `p:graphicFrame / cx:chart r:id` + `ppt/charts/chartExN.xml` |
| Embedded chart workbook | `ppt/embeddings/Microsoft_Excel_WorksheetN.xlsx` |
| Shape hyperlink | `p:cNvPr / a:hlinkClick` |
| Text hyperlink | `a:rPr / a:hlinkClick` |
| Connector | `p:cxnSp` |
| Group | `p:grpSp` |
| Custom geometry | `p:spPr / a:custGeom` |
| Slide number | `p:ph type="sldNum"` + `a:fld type="slidenum"` |
| Date field | `p:ph type="dt"` + `a:fld type="datetime..."` |
| Footer | `p:ph type="ftr"` |
| Theme colors/fonts | `ppt/theme/themeN.xml` |
| Color map | `p:sldMaster / p:clrMap` or `p:clrMapOvr` |
| Table styles | `ppt/tableStyles.xml` |

### Appendix B: Relationship types

| Relationship purpose | Type |
|---|---|
| Presentation to slide | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide` |
| Presentation to slide master | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster` |
| Slide to layout | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout` |
| Master/layout to theme | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme` |
| Slide to image | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/image` |
| Slide to standard chart | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart` |
| Slide to ChartEx chart | `http://schemas.microsoft.com/office/2014/relationships/chartEx` |
| Chart to embedded workbook | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/package` |
| Slide to external hyperlink | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink` |
| Presentation to table styles | `http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles` |

### Appendix C: Content types

| Part | Content type |
|---|---|
| Standard chart | `application/vnd.openxmlformats-officedocument.drawingml.chart+xml` |
| ChartEx | `application/vnd.ms-office.chartex+xml` |
| Embedded xlsx | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Table styles | `application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml` |
| PNG | `image/png` |
| JPEG | `image/jpeg` |

Common overrides:

```xml
<Override PartName="/ppt/charts/chart1.xml"
  ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>

<Override PartName="/ppt/charts/chartEx1.xml"
  ContentType="application/vnd.ms-office.chartex+xml"/>

<Override PartName="/ppt/embeddings/Microsoft_Excel_Worksheet1.xlsx"
  ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/>

<Override PartName="/ppt/tableStyles.xml"
  ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
```

### Appendix D: Unit conversion table

| Meaning | Value |
|---|---:|
| 1 inch | `914400` EMU |
| 1 cm | `360000` EMU |
| 1 point | `12700` EMU |
| 1 px at 96 DPI | `9525` EMU |
| 1 degree rotation | `60000` |
| 10 pt text size | `sz="1000"` |
| 100% percentage | `100000` |

### Appendix E: Element index

| Element | Meaning / common location |
|---|---|
| `a:bodyPr` | Text body layout, padding, wrap, vertical anchor |
| `a:blip` | Image reference container, often with `r:embed` or `r:link` |
| `a:blipFill` | Image fill |
| `a:buAutoNum` | Automatic numbered bullet |
| `a:buChar` | Character bullet |
| `a:buNone` | Explicitly no bullet |
| `a:custGeom` | Custom/freeform geometry |
| `a:fld` | Dynamic text field, such as slide number/date |
| `a:graphicData` | Payload wrapper inside `a:graphic`, differentiated by URI |
| `a:ln` | General line/outline properties |
| `a:lnL`, `a:lnR`, `a:lnT`, `a:lnB` | Table cell border lines |
| `a:p` | Paragraph |
| `a:pPr` | Paragraph properties |
| `a:path` | Custom geometry path |
| `a:prstGeom` | Preset shape geometry |
| `a:r` | Text run |
| `a:rPr` | Text run properties |
| `a:solidFill` | Solid fill |
| `a:srcRect` | Image crop rectangle |
| `a:t` | Text value |
| `a:tbl` | DrawingML table |
| `a:tc` | Table cell |
| `a:tcPr` | Table cell properties |
| `a:txBody` | DrawingML text body, especially in table cells |
| `c:axId` | Chart axis ID |
| `c:barChart` | Standard bar/column chart |
| `c:cat` | Standard chart category data |
| `c:catAx` | Category axis |
| `c:chart` | Standard chart reference or chart container depending context |
| `c:chartSpace` | Standard chart part root |
| `c:dLbls` | Data labels |
| `c:dPt` | Individual data point |
| `c:externalData` | Standard chart external/embedded workbook reference |
| `c:numCache` | Numeric chart cache |
| `c:ser` | Standard chart series |
| `c:spPr` | Chart shape properties |
| `c:strCache` | String chart cache |
| `c:txPr` | Chart text properties |
| `c:val` | Standard chart value data |
| `c:valAx` | Value axis |
| `cx:chart` | ChartEx slide reference or chart container depending context |
| `cx:chartData` | ChartEx data container |
| `cx:chartSpace` | ChartEx chart part root |
| `cx:data` | ChartEx data block |
| `cx:externalData` | ChartEx workbook reference |
| `cx:series` | ChartEx series, e.g. `layoutId="waterfall"` |
| `p:cNvPr` | Nonvisual drawing properties, including local drawing ID/name/descr |
| `p:clrMap` | Master color mapping |
| `p:clrMapOvr` | Layout/slide color-map override |
| `p:cSld` | Common slide data |
| `p:cxnSp` | Connector shape |
| `p:graphicFrame` | Frame for charts/tables/diagrams |
| `p:grpSp` | Group shape |
| `p:hf` | Header/footer flags |
| `p:ph` | Placeholder marker |
| `p:pic` | Picture object |
| `p:presentation` | Presentation root |
| `p:sld` | Slide root |
| `p:sldId` | Presentation-level slide entry |
| `p:sldMaster` | Slide master root |
| `p:sldLayout` | Slide layout root |
| `p:sp` | Shape/text box |
| `p:spPr` | Shape properties |
| `p:spTree` | Slide shape tree |
| `p:txBody` | Shape text body |
| `p14:sectionLst` | PowerPoint sections list |

### Appendix F: Minimal object skeletons

#### Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Shape 1"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="0" y="0"/>
      <a:ext cx="1000000" cy="1000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p/>
  </p:txBody>
</p:sp>
```

#### Picture

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="3" name="Picture 1" descr="Alt text"/>
    <p:cNvPicPr/>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rIdImage"/>
    <a:stretch><a:fillRect/></a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="0" y="0"/>
      <a:ext cx="1000000" cy="1000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
</p:pic>
```

#### Standard chart frame

```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="4" name="Chart 1"/>
    <p:cNvGraphicFramePr/>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm>
    <a:off x="0" y="0"/>
    <a:ext cx="6000000" cy="4000000"/>
  </p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
      <c:chart r:id="rIdChart"/>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

#### ChartEx frame

```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="5" name="Waterfall 1"/>
    <p:cNvGraphicFramePr/>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm>
    <a:off x="0" y="0"/>
    <a:ext cx="6000000" cy="4000000"/>
  </p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.microsoft.com/office/drawing/2014/chartex">
      <cx:chart r:id="rIdChartEx"/>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

#### Connector

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="6" name="Connector 1"/>
    <p:cNvCxnSpPr>
      <a:stCxn id="2" idx="3"/>
      <a:endCxn id="5" idx="1"/>
    </p:cNvCxnSpPr>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="0" y="0"/>
      <a:ext cx="1000000" cy="1000000"/>
    </a:xfrm>
    <a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>
    <a:ln w="12700">
      <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
      <a:tailEnd type="triangle" w="med" len="med"/>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

---

## External reference URLs preserved from source notes

These were referenced throughout the original notes and are useful for deeper schema checks.

```text
https://learn.microsoft.com/en-us/office/open-xml/presentation/structure-of-a-presentationml-document
https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-presentations
https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-slide-masters
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.presentation
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.picture
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.groupshape
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.connectionshape
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.placeholdershape
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.headerfooter
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.table
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.tablecellproperties
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.bodyproperties
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.outline
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.customgeometry
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.path
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.hyperlinkonclick
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.field
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.chartspace
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.barchart
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.externaldata
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.datalabels
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.datapoint
https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.plotarea
https://learn.microsoft.com/en-us/openspecs/office_standards/ms-odrawxml/5d0d453e-adac-43be-a797-59b9916593dd
https://learn.microsoft.com/en-us/openspecs/office_standards/ms-odrawxml/e2723b0a-9120-42a5-bd11-c252ccb13c1e
https://learn.microsoft.com/en-us/openspecs/office_standards/ms-pptx/1f21a089-944d-410b-bd47-4f5e692c2532
https://ooxml.info/
https://c-rex.net/
```
