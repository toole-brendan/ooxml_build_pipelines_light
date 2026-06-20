# Excel OOXML Conventions Field Guide

A consolidated reference for understanding and generating Excel .xlsx SpreadsheetML

Consolidated from the provided Excel OOXML notes

May 28, 2026

# Contents

- Scope and reading notes
- Core mental model
- Package anatomy
- Relationships and content types
- Workbook-level XML
- Worksheet XML
- Cells and values
- Strings and escaping
- Dates, times, and number formats
- Styles and differential styles
- Formulas and recalculation
- Defined names
- Tables
- Conditional formatting
- Data validation
- Modern extensions and compatibility
- Generator-safe checklists
- Recipes: what files must I touch?
- Appendix A: compact element glossary
- Appendix B: worksheet order quick reference
- Appendix C: selected references from the source notes
# Scope and reading notes

This guide assumes the normal Excel-compatible **Transitional**** ****.xlsx** dialect unless a section explicitly says otherwise. Transitional SpreadsheetML commonly uses these namespace families:

```
xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
```

Strict OOXML uses different purl.oclc.org/ooxml/... relationship and content-type URIs. Most hand-authored or generator-authored Excel files target Transitional because it is what Excel writes most often and what most tools expect.

Use this guide as a field reference when generating, inspecting, or editing .xlsx files. It emphasizes conventions that avoid Excel repair dialogs: package integrity, relationship integrity, worksheet element order, correct indexes, and preserving modern extension blocks.

Core conventions used throughout:

- A normal .xlsx is a ZIP/OPC package, not one XML document.
- Formula text is normally stored **without** a leading =.
- Many indexes are zero-based: shared strings, cell styles, differential styles, fonts, fills, borders, and workbook sheet positions used by localSheetId.
- Relationships are local to the owning .rels file. The same rId1 can exist in different relationship files and mean different things.
- Content types declare what each package part is.
- Preserve unfamiliar extLst, mc:Ignorable, x14:*, x14ac:*, xm:*, and xda:* content when editing existing Excel-authored files.
# Core mental model

A useful mental model is:

**workbook = index and relationships; worksheet = sparse grid; sharedStrings = text dictionary; styles = formatting dictionary; rels = pointers; content types = MIME registry.**

An Excel .xlsx package is a set of parts. Some parts contain content, such as worksheet cells or style records. Other parts tell the reader how to locate and interpret those content parts.

Typical package shape:

```
[Content_Types].xml
_rels/.rels

docProps/core.xml
docProps/app.xml

xl/workbook.xml
xl/_rels/workbook.xml.rels
xl/worksheets/sheet1.xml
xl/worksheets/sheet2.xml
xl/styles.xml
xl/sharedStrings.xml
xl/theme/theme1.xml
xl/calcChain.xml          optional
xl/tables/table1.xml      optional
xl/drawings/drawing1.xml  optional
```

Common object roles:

| Object | Role |
|---|---|
| [Content_Types].xml | Declares MIME/content types for package parts. |
| _rels/.rels | Points from the package root to the main workbook part and properties. |
| xl/workbook.xml | Names and orders sheets; holds workbook-level settings, defined names, and external references. |
| xl/_rels/workbook.xml.rels | Maps workbook r:id values to worksheets, styles, shared strings, theme, calculation chain, etc. |
| xl/worksheets/sheetN.xml | Stores sparse rows, cells, formulas, and many sheet-level features. |
| xl/styles.xml | Stores reusable fonts, fills, borders, number formats, cell styles, and differential styles. |
| xl/sharedStrings.xml | Stores workbook-wide string table entries used by t="s" cells. |
| xl/tables/tableN.xml | Stores table metadata; actual table values remain in worksheet cells. |

# Package anatomy

## Minimum valid workbook

A minimal workbook that should open without repair can be as small as:

```
[Content_Types].xml
_rels/.rels
xl/workbook.xml
xl/_rels/workbook.xml.rels
xl/worksheets/sheet1.xml
```

### [Content_Types].xml

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels"
           ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"
           ContentType="application/xml"/>

  <Override PartName="/xl/workbook.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml"
            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
```

### _rels/.rels

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="xl/workbook.xml"/>
</Relationships>
```

### xl/workbook.xml

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
```

### xl/_rels/workbook.xml.rels

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
    Target="worksheets/sheet1.xml"/>
</Relationships>
```

### xl/worksheets/sheet1.xml

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData/>
</worksheet>
```

## Common real-world workbook layout

A more Excel-like package may include many optional parts. Only include parts that are actually referenced.

```
[Content_Types].xml
_rels/.rels

docProps/core.xml
docProps/app.xml
docProps/custom.xml

xl/workbook.xml
xl/_rels/workbook.xml.rels

xl/worksheets/sheet1.xml
xl/worksheets/sheet2.xml
xl/worksheets/_rels/sheet1.xml.rels

xl/styles.xml
xl/sharedStrings.xml
xl/theme/theme1.xml
xl/calcChain.xml
xl/metadata.xml
xl/volatileDependencies.xml

xl/tables/table1.xml
xl/queryTables/queryTable1.xml

xl/drawings/drawing1.xml
xl/drawings/_rels/drawing1.xml.rels
xl/drawings/vmlDrawing1.vml

xl/charts/chart1.xml
xl/charts/_rels/chart1.xml.rels

xl/comments1.xml
xl/threadedComments/threadedComment1.xml

xl/media/image1.png
xl/media/image2.jpeg

xl/pivotTables/pivotTable1.xml
xl/pivotCache/pivotCacheDefinition1.xml
xl/pivotCache/pivotCacheRecords1.xml

xl/externalLinks/externalLink1.xml
xl/externalLinks/_rels/externalLink1.xml.rels

xl/connections.xml
xl/printerSettings/printerSettings1.bin

xl/vbaProject.bin       macro-enabled .xlsm only
```

## Macro-enabled files

For macro-enabled workbooks:

- Use file extension .xlsm, not .xlsx.
- Include xl/vbaProject.bin.
- Add a workbook relationship with type http://schemas.microsoft.com/office/2006/relationships/vbaProject.
- Change the workbook content type from ordinary workbook main type to:
```
application/vnd.ms-excel.sheet.macroEnabled.main+xml
```

# Relationships and content types

## Relationship indirection

OOXML rarely points directly to another package part from ordinary XML. Instead, an element carries a relationship ID, and a .rels file maps that ID to a target.

In xl/workbook.xml:

```
<workbook
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
```

In xl/_rels/workbook.xml.rels:

```
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship
    Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
    Target="worksheets/sheet1.xml"/>
</Relationships>
```

sheetId is a workbook sheet identifier. r:id points through the workbook relationship file to the actual worksheet part.

## Relationship locality

Relationship IDs are local to the .rels file that owns them. This means:

```
/_rels/.rels                         rId1 can mean xl/workbook.xml
xl/_rels/workbook.xml.rels           rId1 can mean worksheets/sheet1.xml
xl/worksheets/_rels/sheet1.xml.rels  rId1 can mean ../tables/table1.xml
```

Never assume an r:id is globally meaningful. Resolve it from the relationship part associated with the XML part that contains the r:id.

## Useful URI prefixes

```
odRel = http://schemas.openxmlformats.org/officeDocument/2006/relationships/
pkgRel = http://schemas.openxmlformats.org/package/2006/relationships/
msRel = http://schemas.microsoft.com/office/2006/relationships/
```

## Common relationships and content types

Relationship parts themselves do **not** get content-type overrides. They are covered by the default:

```
<Default Extension="rels"
         ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
```

XML content parts normally need an override unless covered by a default:

```
<Override PartName="/xl/styles.xml"
          ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
```

Image parts are usually covered by defaults:

```
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
```

Compact lookup:

| Owner | Relationship type | Typical target | Content type rule |
|---|---|---|---|
| /_rels/.rels | odRel + officeDocument | /xl/workbook.xml | workbook main override |
| /_rels/.rels | pkgRel + metadata/core-properties | /docProps/core.xml | core properties override |
| /_rels/.rels | odRel + extended-properties | /docProps/app.xml | extended properties override |
| xl/_rels/workbook.xml.rels | odRel + worksheet | worksheets/sheet1.xml | worksheet override |
| xl/_rels/workbook.xml.rels | odRel + styles | styles.xml | styles override |
| xl/_rels/workbook.xml.rels | odRel + sharedStrings | sharedStrings.xml | shared strings override |
| xl/_rels/workbook.xml.rels | odRel + theme | theme/theme1.xml | theme override |
| xl/_rels/workbook.xml.rels | odRel + calcChain | calcChain.xml | calculation chain override |
| xl/_rels/workbook.xml.rels | odRel + externalLink | externalLinks/externalLink1.xml | external link override |
| xl/_rels/workbook.xml.rels | odRel + connections | connections.xml | connections override |
| xl/worksheets/_rels/sheet1.xml.rels | odRel + table | ../tables/table1.xml | table override |
| xl/worksheets/_rels/sheet1.xml.rels | odRel + drawing | ../drawings/drawing1.xml | drawing override |
| xl/worksheets/_rels/sheet1.xml.rels | odRel + comments | ../comments1.xml | comments override |
| xl/worksheets/_rels/sheet1.xml.rels | odRel + hyperlink | external URL | no content type; TargetMode="External" |
| xl/drawings/_rels/drawing1.xml.rels | odRel + chart | ../charts/chart1.xml | chart override |
| xl/drawings/_rels/drawing1.xml.rels | odRel + image | ../media/image1.png | image default |
| xl/externalLinks/_rels/externalLink1.xml.rels | odRel + externalLinkPath | external workbook path | no content type; TargetMode="External" |

# Workbook-level XML

xl/workbook.xml is the workbook index. It usually contains sheet listings, workbook properties, calculation properties, defined names, and external reference declarations.

## Sheets, sheetId, and r:id

```
<workbook
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Jan" sheetId="7" r:id="rId1"/>
    <sheet name="Feb" sheetId="42" r:id="rId2"/>
  </sheets>
</workbook>
```

Important distinctions:

| Concept | Meaning |
|---|---|
| <sheet name="..."> | Display name shown in Excel. |
| sheetId | Workbook sheet identifier. It must be unique, but does not have to equal order. |
| r:id | Relationship ID resolved in xl/_rels/workbook.xml.rels. |
| sheet position | The zero-based order of <sheet> elements. Used by localSheetId in defined names. |

## Workbook properties and date system

The workbook can opt into the 1904 date system:

```
<workbookPr date1904="1"/>
```

Omit date1904, or use date1904="0", for the normal 1900 system. The date system matters because Excel date serials differ by 1,462 days between 1900 and 1904 systems.

## Calculation properties

When generating or editing formulas, it is often safest to remove stale calculation chain data and force recalculation:

```
<calcPr calcId="0" fullCalcOnLoad="1" forceFullCalc="1"/>
```

calcPr lives in workbook.xml. The calcChain.xml part, if present, records the last calculation chain and can become stale after formula edits.

## Defined names overview

Defined names live under <definedNames> in workbook.xml:

```
<definedNames>
  <definedName name="TaxRate">0.0825</definedName>
  <definedName name="SalesData">'Jan'!$A$1:$D$100</definedName>
  <definedName name="CompanyName">&quot;Acme Corp&quot;</definedName>
</definedNames>
```

Defined-name text is formula-like and normally has no leading =.

# Worksheet XML

Worksheets are sparse grids. The main cell data lives in <sheetData>. Empty/default rows and cells are normally omitted.

```
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="s"><v>0</v></c>
      <c r="B1"><v>42</v></c>
      <c r="C1" s="2"><f>B1*2</f><v>84</v></c>
      <c r="D1" t="b"><v>1</v></c>
    </row>
  </sheetData>
</worksheet>
```

## Sparse grid rules

- A missing <c> element means the cell is blank/default, not that later cells shift left.
- Use explicit r="A1" cell references for robust output.
- Write rows in ascending row order.
- Write cells in ascending column order inside each row.
- Use the r attribute as the source of truth for position.
## Required child order inside <worksheet>

<worksheet> is schema-ordered. Wrong order is one of the most common causes of Excel “repaired records.” The practical order is:

```
worksheet
  sheetPr?
  dimension?
  sheetViews?
  sheetFormatPr?
  cols*
  sheetData                       required
  sheetCalcPr?
  sheetProtection?
  protectedRanges?
  scenarios?
  autoFilter?
  sortState?
  dataConsolidate?
  customSheetViews?
  mergeCells?
  phoneticPr?
  conditionalFormatting*
  dataValidations?
  hyperlinks?
  printOptions?
  pageMargins?
  pageSetup?
  headerFooter?
  rowBreaks?
  colBreaks?
  customProperties?
  cellWatches?
  ignoredErrors?
  smartTags?
  drawing?
  legacyDrawing?
  legacyDrawingHF?
  picture?
  oleObjects?
  controls?
  webPublishItems?
  tableParts?
  extLst?
```

Placement examples:

| Feature | Worksheet element | Placement reminder |
|---|---|---|
| Core cells | <sheetData> | Required. |
| Merged cells | <mergeCells> | After customSheetViews, before phoneticPr. |
| Conditional formatting | <conditionalFormatting> | After phoneticPr, before dataValidations. |
| Data validation | <dataValidations> | After conditional formatting. |
| Hyperlinks | <hyperlinks> | After data validations. |
| Drawing | <drawing> | Late in the worksheet, before table parts. |
| Tables | <tableParts> | Near the end, before extLst. |
| Modern extensions | <extLst> | Last. |

# Cells and values

A cell is a <c> element inside a <row> inside <sheetData>. Important attributes and children:

| Syntax | Meaning |
|---|---|
| <c r="B3"> | Cell at B3. |
| s="4" | Style index 4 in styles.xml / cellXfs. |
| t="s" | Shared-string cell. <v> is an index into sharedStrings.xml. |
| t="inlineStr" | Inline string. Uses <is>, not <v>. |
| <v> | Cell value or cached formula result. |
| <f> | Formula text, normally without leading =. |

## Cell type variants

| Cell kind | Encoding | Notes |
|---|---|---|
| Number | <c r="A1"><v>123.45</v></c> | t="n" is optional. Use invariant decimal text, not localized commas. |
| Shared string | <c r="A1" t="s"><v>0</v></c> | <v> is a zero-based shared-string index. |
| Formula string result | <c r="A1" t="str"><f>TEXT(B1,&quot;0&quot;)</f><v>abc</v></c> | str is mainly for formula results, not ordinary text literals. |
| Boolean | <c r="A1" t="b"><v>1</v></c> | 1 = TRUE, 0 = FALSE. |
| Error | <c r="A1" t="e"><v>#DIV/0!</v></c> | Common values: #NULL!, #DIV/0!, #VALUE!, #REF!, #NAME?, #NUM!, #N/A. |
| Inline string | <c r="A1" t="inlineStr"><is><t>Hello</t></is></c> | Do not use <v> for inline strings. |
| Date/time | <c r="A1" s="3"><v>45352.5</v></c> | Stored as a number plus date/time style. |

## Empty/default cells

Empty/default cells are normally omitted:

```
<row r="1">
  <c r="A1"><v>1</v></c>
  <c r="D1"><v>4</v></c>
</row>
```

This means B1 and C1 are blank/default. It does not mean D1 should be interpreted as B1.

# Strings and escaping

Excel commonly uses xl/sharedStrings.xml to store repeated strings once, then cells point to the string by index. Shared strings are common but not required. Inline strings are valid SpreadsheetML too.

## Shared string table

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
     count="3"
     uniqueCount="2">
  <si>
    <t>Hello</t>
  </si>
  <si>
    <t>World</t>
  </si>
</sst>
```

Cells:

```
<c r="A1" t="s"><v>0</v></c>
<c r="A2" t="s"><v>1</v></c>
<c r="A3" t="s"><v>0</v></c>
```

Here count="3" because three cells refer to shared strings, and uniqueCount="2" because there are two <si> entries.

## Shared string terms

| Element/attribute | Meaning |
|---|---|
| <sst> | Shared string table root. |
| count | Total number of shared-string cell references. |
| uniqueCount | Number of unique <si> entries. |
| <si> | One shared string item. |
| <t> | Plain text. |
| <r> | Rich text run. |
| <rPr> | Rich text run properties. |

## Rich text shared strings

```
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
     count="1"
     uniqueCount="1">
  <si>
    <r>
      <rPr>
        <b/>
        <color rgb="FFFF0000"/>
      </rPr>
      <t>Red bold</t>
    </r>
    <r>
      <t xml:space="preserve"> normal</t>
    </r>
  </si>
</sst>
```

## Inline strings

Inline strings are stored directly in the worksheet:

```
<c r="A1" t="inlineStr">
  <is>
    <t>Hello</t>
  </is>
</c>
```

Rich inline string:

```
<c r="A1" t="inlineStr">
  <is>
    <r>
      <rPr><b/></rPr>
      <t>Bold</t>
    </r>
    <r>
      <t xml:space="preserve"> text</t>
    </r>
  </is>
</c>
```

Important distinction:

```
t="s"         uses <v> as a shared-string index
t="inlineStr" uses <is>, not <v>
```

## xml:space="preserve"

Use xml:space="preserve" on <t> when leading or trailing whitespace matters:

```
<t xml:space="preserve"> leading and trailing </t>
```

Also use it for rich text runs that begin or end with significant spaces:

```
<r><t>Hello</t></r>
<r><t xml:space="preserve"> world</t></r>
```

## XML escaping

Ordinary XML escaping applies:

```
<t>Tom &amp; Jerry</t>
<t>5 &lt; 10</t>
```

In XML attributes, quotes must be escaped:

```
<numFmt formatCode="&quot;Total:&quot; #,##0"/>
```

Formula text is also XML text:

```
<f>A1&lt;10</f>
<f>AND(A1&gt;0,B1&lt;5)</f>
<f>&quot;A&quot;&amp;&quot;B&quot;</f>
```

## SpreadsheetML _xHHHH_ escapes

SpreadsheetML has a second escaping convention for characters that are not valid XML characters:

```
_xHHHH_
```

HHHH is a four-digit hexadecimal Unicode code point. For example:

```
_x0008_
```

The serialized syntax has no braces:

```
correct:   _x0008_
incorrect: _x{0008}_
```

If a literal string should contain text that looks like an escape sequence, escape the underscore itself:

```
literal desired text:  _x0041_
serialized text:       _x005F_x0041_
```

# Dates, times, and number formats

Excel dates are usually numbers plus display formats. The cell value stores the serial; the style determines whether it displays as a date, time, currency, percentage, etc.

## Date serials

```
<c r="A2" s="1">
  <v>45352</v>
</c>
```

The style might point to a custom date format:

```
<numFmts count="1">
  <numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
</numFmts>

<cellXfs count="2">
  <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
  <xf numFmtId="164" fontId="0" fillId="0" borderId="0"
      xfId="0" applyNumberFormat="1"/>
</cellXfs>
```

Practical date rule:

```
Store date/time values as numbers.
Apply a date/time number format through styles.xml.
Do not store ordinary dates as t="s" or t="str".
```

## 1900 vs 1904 date systems

The workbook-level switch is:

```
<workbookPr date1904="1"/>
```

Time is the fractional part of the serial number:

```
45352.0   midnight
45352.5   noon
45352.75  6:00 PM
```

## Number formats

A number format is either a built-in numFmtId or a custom <numFmt> in styles.xml.

```
<numFmts count="1">
  <numFmt numFmtId="164" formatCode="#,##0.0,,&quot;M&quot;"/>
</numFmts>
```

A cell format references it:

```
<xf numFmtId="164" fontId="0" fillId="0" borderId="0"
    xfId="0" applyNumberFormat="1"/>
```

Custom IDs should normally start at 164:

```
<numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
<numFmt numFmtId="165" formatCode="#,##0.0,,&quot;M&quot;"/>
```

## Format sections

Format codes can have up to four semicolon-separated sections:

```
positive;negative;zero;text
```

Rules:

```
one section:   all numeric values
two sections:  positive and zero ; negative
three sections: positive ; negative ; zero
four sections:  positive ; negative ; zero ; text
```

If a text section exists, it must be last, and @ is the placeholder for text.

## Core format tokens

| Token | Meaning |
|---|---|
| 0 | Required digit placeholder. |
| # | Optional digit placeholder. |
| ? | Optional digit placeholder that leaves alignment space. |
| . | Decimal point in the format code. |
| , | Thousands separator or scaling by 1,000 when trailing. |
| % | Multiply by 100 and display percent sign. |
| E+00 / E-00 | Scientific notation. |
| "text" | Literal text; in XML attributes use &quot;. |
| \x | Escape and display the next character. |
| _x | Leave space equal to width of character x. |
| *x | Repeat character x to fill column width. |
| @ | Text placeholder in the fourth section. |
| [Red] | Color modifier. |
| [>=1000] | Numeric condition for that section. |
| m, d, y, h, s, AM/PM | Date/time display tokens. |

## Built-in numFmtId values 0-49

Built-in formats are referenced by ID and are not written as <numFmt> entries. Date and currency built-ins can display differently by locale, so custom numFmtId >= 164 is safer for stable display.

| ID | Typical built-in format |
|---|---|
| 0 | General |
| 1 | 0 |
| 2 | 0.00 |
| 3 | #,##0 |
| 4 | #,##0.00 |
| 5 | $#,##0_);($#,##0) |
| 6 | $#,##0_);[Red]($#,##0) |
| 7 | $#,##0.00_);($#,##0.00) |
| 8 | $#,##0.00_);[Red]($#,##0.00) |
| 9 | 0% |
| 10 | 0.00% |
| 11 | 0.00E+00 |
| 12 | # ?/? |
| 13 | # ??/?? |
| 14 | mm-dd-yy |
| 15 | d-mmm-yy |
| 16 | d-mmm |
| 17 | mmm-yy |
| 18 | h:mm AM/PM |
| 19 | h:mm:ss AM/PM |
| 20 | h:mm |
| 21 | h:mm:ss |
| 22 | m/d/yy h:mm |
| 23-36 | Reserved / international / locale-dependent. |
| 37 | #,##0 ;(#,##0) |
| 38 | #,##0 ;[Red](#,##0) |
| 39 | #,##0.00;(#,##0.00) |
| 40 | #,##0.00;[Red](#,##0.00) |
| 41 | _(* #,##0_);_(* (#,##0);_(* "-"_);_(@_) |
| 42 | _($* #,##0_);_($* (#,##0);_($* "-"_);_(@_) |
| 43 | _(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_) |
| 44 | _($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_) |
| 45 | mm:ss |
| 46 | [h]:mm:ss |
| 47 | mmss.0 |
| 48 | ##0.0E+0 |
| 49 | @ |

## Common number-format recipes

| Goal | Format code |
|---|---|
| Integer with thousands | #,##0 |
| Two decimals | #,##0.00 |
| Negative in parentheses | #,##0;(#,##0);- |
| Negative red in parentheses | #,##0;[Red](#,##0);- |
| Accounting, no decimals | _($* #,##0_);_($* (#,##0);_($* "-"_);_(@_) |
| Accounting, two decimals | _($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_) |
| Percent, one decimal | 0.0% |
| Date ISO-like | yyyy-mm-dd |
| Date/time | yyyy-mm-dd h:mm |
| Thousands as K | #,##0.0,"K" |
| Millions as M | #,##0.0,,"M" |
| Billions as B | #,##0.0,,,"B" |
| Conditional color | [Green]#,##0;[Red](#,##0);[Blue]-;@ |
| Threshold sections | [>=1000000]#,##0.0,,"M";[>=1000]#,##0.0,"K";0 |
| Stored bps value | 0 "bps" |
| Text prefix | "ID-"@ |

Basis-points gotcha: Excel number formats can scale with % and trailing commas, but they do not provide a clean arbitrary “multiply by 10,000 and append bps” operator. If the stored value is 123, format as 0 "bps". If the stored value is a rate like 0.0123, use a helper formula/value rate*10000, then format that result as 0 "bps".

# Styles and differential styles

Formatting is centralized in xl/styles.xml. A cell’s s="N" is a zero-based index into <cellXfs>. If s is omitted, treat it like style index 0.

```
<c r="A1" s="2">
  <v>123</v>
</c>
```

Resolution path:

```
cell @s="2"
  -> styles.xml / styleSheet / cellXfs / xf[2]
      -> numFmtId
      -> fontId
      -> fillId
      -> borderId
      -> alignment/protection children
      -> xfId, a base-style index into cellStyleXfs
```

Practical writer rule: put the complete intended formatting directly into the cellXfs record and use xfId="0" unless you specifically need named-style inheritance.

## Minimal usable styles.xml

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">

  <numFmts count="1">
    <numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
  </numFmts>

  <fonts count="2">
    <font>
      <sz val="11"/>
      <color theme="1"/>
      <name val="Calibri"/>
      <family val="2"/>
      <scheme val="minor"/>
    </font>
    <font>
      <b/>
      <sz val="11"/>
      <color rgb="FF000000"/>
      <name val="Calibri"/>
    </font>
  </fonts>

  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill>
      <patternFill patternType="solid">
        <fgColor rgb="FFFFF2CC"/>
        <bgColor indexed="64"/>
      </patternFill>
    </fill>
  </fills>

  <borders count="2">
    <border>
      <left/><right/><top/><bottom/><diagonal/>
    </border>
    <border>
      <left style="thin"><color rgb="FF000000"/></left>
      <right style="thin"><color rgb="FF000000"/></right>
      <top style="thin"><color rgb="FF000000"/></top>
      <bottom style="thin"><color rgb="FF000000"/></bottom>
      <diagonal/>
    </border>
  </borders>

  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>

  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="0"
        xfId="0" applyNumberFormat="1"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1"
        xfId="0"
        applyFont="1"
        applyFill="1"
        applyBorder="1"
        applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
  </cellXfs>

  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>

  <dxfs count="0"/>

  <tableStyles count="0"
               defaultTableStyle="TableStyleMedium2"
               defaultPivotStyle="PivotStyleLight16"/>
</styleSheet>
```

## apply* flags

Practical writer rule:

```
If you set non-default numFmtId -> add applyNumberFormat="1"
If you set non-default fontId   -> add applyFont="1"
If you set non-default fillId   -> add applyFill="1"
If you set non-default borderId -> add applyBorder="1"
If you include <alignment>      -> add applyAlignment="1"
If you include <protection>     -> add applyProtection="1"
```

Excel often tolerates missing apply* flags, but explicit apply*="1" avoids ambiguous inheritance behavior. Avoid writing applyFill="0" unless you deliberately want to suppress that formatting aspect.

## Fonts

```
<font>
  <b/>
  <i/>
  <u/>
  <sz val="11"/>
  <color rgb="FF000000"/>
  <name val="Calibri"/>
  <family val="2"/>
  <scheme val="minor"/>
</font>
```

Common font children include b, i, u, strike, sz, color, name, family, scheme, and vertical alignment. Colors can be rgb="AARRGGBB", theme="N", indexed="N", or auto="1".

## Fills

For a solid fill, the visible fill color is usually fgColor, not bgColor:

```
<fill>
  <patternFill patternType="solid">
    <fgColor rgb="FFFFFF00"/>
    <bgColor indexed="64"/>
  </patternFill>
</fill>
```

For simple “make the cell yellow,” use solid + fgColor.

## Borders

```
<border>
  <left style="thin"><color rgb="FF000000"/></left>
  <right style="thin"><color rgb="FF000000"/></right>
  <top style="thin"><color rgb="FF000000"/></top>
  <bottom style="thin"><color rgb="FF000000"/></bottom>
  <diagonal/>
</border>
```

Common styles: thin, medium, thick, dashed, dotted, double, hair, dashDot, dashDotDot, mediumDashed, mediumDashDot, mediumDashDashDot, and slantDashDot.

## Alignment

Alignment is a child of an <xf> in cellXfs, not a top-level indexed collection:

```
<xf numFmtId="0" fontId="0" fillId="0" borderId="0"
    xfId="0" applyAlignment="1">
  <alignment horizontal="center"
             vertical="center"
             wrapText="1"
             shrinkToFit="0"
             textRotation="0"/>
</xf>
```

## Differential formats: <dxfs> and <dxf>

<dxf> records are used by conditional formatting and similar features. They are not normal cell styles; they are differential formats applied on top of existing formatting.

```
<dxfs count="1">
  <dxf>
    <font>
      <color rgb="FF9C0006"/>
    </font>
    <fill>
      <patternFill patternType="solid">
        <fgColor rgb="FFFFC7CE"/>
        <bgColor indexed="64"/>
      </patternFill>
    </fill>
  </dxf>
</dxfs>
```

Conditional formatting references a dxf by zero-based dxfId:

```
<conditionalFormatting sqref="A1:A10">
  <cfRule type="cellIs" priority="1" operator="greaterThan" dxfId="0">
    <formula>100</formula>
  </cfRule>
</conditionalFormatting>
```

# Formulas and recalculation

All normal formulas use the cell’s <f> child. Formula text is stored without a leading =. The <v> child is the cached result from the last calculation and may be omitted if the reader recalculates.

## Basic formula

```
<c r="C2">
  <f>A2+B2</f>
  <v>30</v>
</c>
```

If the cached formula result is text, Boolean, or error, the cell’s t may reflect that:

```
<c r="A1" t="str">
  <f>TEXT(B1,&quot;0&quot;)</f>
  <v>123</v>
</c>

<c r="A2" t="b">
  <f>B2&gt;0</f>
  <v>1</v>
</c>

<c r="A3" t="e">
  <f>1/0</f>
  <v>#DIV/0!</v>
</c>
```

## Shared formulas

Shared formulas reduce repeated formula text. The master cell has t="shared", a shared group index si, a ref range, and formula text. Dependent cells use the same si and usually omit formula text.

```
<!-- Master -->
<c r="C2">
  <f t="shared" ref="C2:C100" si="0">A2+B2</f>
  <v>30</v>
</c>

<!-- Dependents -->
<c r="C3">
  <f t="shared" si="0"/>
  <v>45</v>
</c>

<c r="C4">
  <f t="shared" si="0"/>
  <v>51</v>
</c>
```

In this example, dependent formulas are interpreted relative to the master. C3 behaves like A3+B3; C4 behaves like A4+B4.

## Legacy array formulas

Legacy Ctrl+Shift+Enter-style array formulas use t="array" and a ref range on the master formula cell.

```
<c r="D1">
  <f t="array" ref="D1:F1">TRANSPOSE(A1:A3)</f>
  <v>1</v>
</c>
<c r="E1"><v>2</v></c>
<c r="F1"><v>3</v></c>
```

Optional array attributes include aca="1" for always-calculate-array and ca="1" for calculate-cell.

## Dynamic-array spills

Dynamic arrays are not the same as legacy t="array" formulas. Modern Excel formula anchors still use <f>...</f> in the top-left spill cell, while dynamic-array metadata is stored in extension metadata, including xda:dynamicArrayProperties.

Typical anchor shape:

```
<c r="E2" cm="1">
  <f>_xlfn.UNIQUE(A2:A10)</f>
  <v>Alpha</v>
</c>
```

Metadata extension shape:

```
<ext uri="{bdbb8cdc-fa1e-496e-a857-3c3f30c029c3}">
  <xda:dynamicArrayProperties
    xmlns:xda="http://schemas.microsoft.com/office/spreadsheetml/2017/dynamicarray"
    fDynamic="1"
    fCollapsed="0"/>
</ext>
```

Practical writer rule: if Excel 365 can calculate the workbook, write the anchor formula, omit stale spill caches, delete calcChain.xml, and force recalculation. When preserving Excel-authored workbooks, preserve xl/metadata.xml, cell metadata indexes such as cm, and extension lists.

## Cross-sheet formulas

Cross-sheet references are formula grammar, not separate package relationships:

```
<c r="A1">
  <f>Sheet2!A1</f>
  <v>10</v>
</c>
```

Quote sheet names containing spaces, punctuation, or special characters:

```
<f>'Sales Q1'!$A$1</f>
```

If a sheet name contains an apostrophe, double it:

```
<f>'Bob''s Sheet'!A1</f>
```

## 3D references

```
<f>SUM(Sheet1:Sheet3!A1)</f>
```

With quoted sheet names:

```
<f>SUM('Jan 2026:Mar 2026'!A1)</f>
```

## External workbook references

External workbook links require both formula syntax and package metadata.

In xl/workbook.xml:

```
<externalReferences>
  <externalReference r:id="rId5"/>
</externalReferences>
```

In xl/_rels/workbook.xml.rels:

```
<Relationship Id="rId5"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLink"
  Target="externalLinks/externalLink1.xml"/>
```

In xl/externalLinks/externalLink1.xml:

```
<externalLink
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <externalBook r:id="rId1">
    <sheetNames>
      <sheetName val="Sheet1"/>
    </sheetNames>
  </externalBook>
</externalLink>
```

In xl/externalLinks/_rels/externalLink1.xml.rels:

```
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLinkPath"
    Target="file:///C:/work/Budget.xlsx"
    TargetMode="External"/>
</Relationships>
```

Formula text may appear as an external-book-index reference:

```
<c r="A1">
  <f>[1]Sheet1!$A$1</f>
  <v>123</v>
</c>
```

## Structured references

Structured references are formula text, but they require the table definition to exist.

Inside a table row:

```
<c r="D2">
  <f>Table1[@Amount]*Table1[@Rate]</f>
  <v>12.5</v>
</c>
```

Same-row table syntax:

```
<c r="D2">
  <f>[@Amount]*[@Rate]</f>
  <v>12.5</v>
</c>
```

Outside the table:

```
<c r="G1">
  <f>SUM(Table1[Amount])</f>
  <v>1000</v>
</c>
```

## Recalculation strategy

If you generate or modify formulas, the safest approach is usually:

```
1. Omit or delete xl/calcChain.xml.
2. Do not rely on stale cached <v> values.
3. Set workbook calculation properties to force recalculation if needed.
```

Example:

```
<calcPr calcId="0" fullCalcOnLoad="1" forceFullCalc="1"/>
```

# Defined names

Defined names live in xl/workbook.xml, under <definedNames>. Their text content is formula-like: a reference, constant, or formula expression, normally without a leading =.

```
<workbook
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <sheets>
    <sheet name="Jan" sheetId="7" r:id="rId1"/>
    <sheet name="Feb" sheetId="42" r:id="rId2"/>
  </sheets>

  <definedNames>
    <definedName name="TaxRate">0.0825</definedName>
    <definedName name="SalesData">'Jan'!$A$1:$D$100</definedName>
    <definedName name="CompanyName">&quot;Acme Corp&quot;</definedName>

    <definedName name="LocalRate" localSheetId="1">'Feb'!$B$2</definedName>

    <definedName name="_xlnm.Print_Area" localSheetId="0">
      'Jan'!$A$1:$H$50
    </definedName>
  </definedNames>
</workbook>
```

## Workbook vs sheet scope

```
<!-- Global name: visible from any sheet -->
<definedName name="Revenue">Summary!$B$2</definedName>

<!-- Sheet-local name: only local to sheet at position 0 -->
<definedName name="Revenue" localSheetId="0">'Jan'!$B$2</definedName>

<!-- Same visible name can exist on a different sheet -->
<definedName name="Revenue" localSheetId="1">'Feb'!$B$2</definedName>
```

| Scope | Encoding | Uniqueness |
|---|---|---|
| Workbook/global | no localSheetId | Name must be unique among global names. |
| Sheet-local | localSheetId="N" | Name must be unique for that sheet index. |
| Built-in sheet features | often _xlnm.* with localSheetId | Usually sheet-local. |

## localSheetId trap

localSheetId is the zero-based position of the sheet in <sheets>, not the <sheet sheetId="..."> value. In this example, Feb has sheetId="42" but localSheetId="1" because it is the second <sheet> element.

## Built-in _xlnm.* names

Reserved built-in names include:

```
_xlnm.Print_Area
_xlnm.Print_Titles
_xlnm.Criteria
_xlnm._FilterDatabase
_xlnm.Extract
_xlnm.Consolidate_Area
_xlnm.Database
_xlnm.Sheet_Title
```

Common examples:

```
<definedName name="_xlnm.Print_Area" localSheetId="0">
  'Sheet1'!$A$1:$G$50
</definedName>

<definedName name="_xlnm.Print_Titles" localSheetId="0">
  'Sheet1'!$1:$1
</definedName>

<definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">
  'Sheet1'!$A$1:$G$50
</definedName>
```

## Name character rules

Safe generator pattern:

```
[A-Za-z_][A-Za-z0-9_.]*
```

Avoid backslash or question mark even though the grammar allows them in some positions. They are not worth the compatibility risk.

Forbidden or unsafe in ordinary defined names:

```
space, tab, newline, :, ;, ,, !, ', ", [, ], {, }, (, ), +, -, *, /,
^, &, =, <, >, %, $, #, @
```

Also avoid names that look like cell references, Booleans, function names, or reserved names:

```
A1
R1C1
XFD1048576
C
R
TRUE
FALSE
SUM
FILTER
```

The _xlnm. prefix is reserved for built-ins. Avoid generating user names beginning _xl unless preserving Excel-authored content.

# Tables

A table’s data is **not** stored in xl/tables/table1.xml. Actual cell values remain in xl/worksheets/sheetN.xml; the table part stores identity, range, columns, calculated/totals metadata, filters, and style.

## Minimum table part

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
       id="1"
       name="Table1"
       displayName="Table1"
       ref="A1:C4"
       totalsRowShown="0">
  <autoFilter ref="A1:C4"/>
  <tableColumns count="3">
    <tableColumn id="1" name="Item"/>
    <tableColumn id="2" name="Amount"/>
    <tableColumn id="3" name="Rate"/>
  </tableColumns>
  <tableStyleInfo name="TableStyleMedium2"
                  showFirstColumn="0"
                  showLastColumn="0"
                  showRowStripes="1"
                  showColumnStripes="0"/>
</table>
```

Absolute minimum can omit <autoFilter> and <tableStyleInfo>, but <tableColumns> is the important required structure. The table id and name must be unique across table parts; displayName must be unique across tables and defined names; ref covers the whole table range including the header row.

## Wiring a table to a sheet

In [Content_Types].xml:

```
<Override PartName="/xl/tables/table1.xml"
          ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
```

In xl/worksheets/sheet1.xml:

```
<worksheet
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <sheetData>
    ...
  </sheetData>

  <tableParts count="1">
    <tablePart r:id="rIdTable1"/>
  </tableParts>
</worksheet>
```

In xl/worksheets/_rels/sheet1.xml.rels:

```
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdTable1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table"
    Target="../tables/table1.xml"/>
</Relationships>
```

## Built-in table style names

Safe built-in ranges:

```
TableStyleLight1   through TableStyleLight21
TableStyleMedium1  through TableStyleMedium28
TableStyleDark1    through TableStyleDark11
```

Example:

```
<tableStyleInfo name="TableStyleMedium9"
                showFirstColumn="0"
                showLastColumn="0"
                showRowStripes="1"
                showColumnStripes="0"/>
```

## Calculated columns

```
<tableColumn id="4" name="Total">
  <calculatedColumnFormula>[@Amount]*[@Rate]</calculatedColumnFormula>
</tableColumn>
```

For compatibility, Excel-authored files usually also have corresponding formulas and cached values in worksheet cells:

```
<c r="D2">
  <f>Table1[@Amount]*Table1[@Rate]</f>
  <v>12.5</v>
</c>
```

## Totals rows

At table level:

```
<table id="1"
       name="Table1"
       displayName="Table1"
       ref="A1:D11"
       totalsRowShown="1"
       totalsRowCount="1">
```

At column level:

```
<tableColumns count="4">
  <tableColumn id="1" name="Item"
               totalsRowFunction="none"
               totalsRowLabel="Total"/>
  <tableColumn id="2" name="Amount"
               totalsRowFunction="sum"/>
  <tableColumn id="3" name="Rate"
               totalsRowFunction="average"/>
  <tableColumn id="4" name="Total"
               totalsRowFunction="sum"/>
</tableColumns>
```

Custom totals formula:

```
<tableColumn id="4" name="Total" totalsRowFunction="custom">
  <totalsRowFormula>SUBTOTAL(109,[Total])</totalsRowFormula>
</tableColumn>
```

Totals-row function values:

```
none
sum
min
max
average
count
countNums
stdDev
var
custom
```

## Merged cells are forbidden inside a table

A worksheet can contain <mergeCells> elsewhere, but a <mergeCell ref="..."> that intersects the table ref breaks the table model. Sorting, filtering, structured references, calculated columns, and totals depend on one header cell per column and one data cell per row/column intersection. Generator rule: reject any merge range that intersects a table range.

# Conditional formatting

Conditional formatting is stored at worksheet level. A <conditionalFormatting> element has an sqref range, and each <cfRule> describes one rule. Rules that apply reusable formatting generally reference a differential style in styles.xml using dxfId.

## Basic dxfId pattern

In xl/styles.xml:

```
<dxfs count="1">
  <dxf>
    <font>
      <color rgb="FF9C0006"/>
    </font>
    <fill>
      <patternFill patternType="solid">
        <fgColor rgb="FFFFC7CE"/>
        <bgColor indexed="64"/>
      </patternFill>
    </fill>
  </dxf>
</dxfs>
```

In xl/worksheets/sheet1.xml:

```
<conditionalFormatting sqref="A2:A100">
  <cfRule type="cellIs"
          operator="greaterThan"
          dxfId="0"
          priority="1">
    <formula>100</formula>
  </cfRule>
</conditionalFormatting>
```

dxfId="0" means the first <dxf> under <dxfs>. Lower priority numbers are evaluated first. stopIfTrue="1" can stop lower-priority rules.

## cfRule types

```
expression
cellIs
colorScale
dataBar
iconSet
top10
uniqueValues
duplicateValues
containsText
notContainsText
beginsWith
endsWith
containsBlanks
notContainsBlanks
containsErrors
notContainsErrors
timePeriod
aboveAverage
```

| Type | Main attributes / children | Usually uses dxfId? |
|---|---|---|
| expression | one formula returning TRUE/FALSE | yes |
| cellIs | operator, one or two formulas | yes |
| colorScale | <colorScale> child | no, uses child colors |
| dataBar | <dataBar> child | no, uses child color |
| iconSet | <iconSet> child | no, uses child definition |
| top10 | rank, percent, bottom | yes |
| uniqueValues | no formula usually | yes |
| duplicateValues | no formula usually | yes |
| text rules | text, formula pattern | yes |
| blank/error rules | optional formula | yes |
| timePeriod | timePeriod attribute | yes |
| aboveAverage | aboveAverage, equalAverage, stdDev | yes |

## Operators

```
lessThan
lessThanOrEqual
equal
notEqual
greaterThanOrEqual
greaterThan
between
notBetween
containsText
notContains
beginsWith
endsWith
```

Numeric cellIs rule:

```
<cfRule type="cellIs" operator="between" dxfId="0" priority="1">
  <formula>10</formula>
  <formula>20</formula>
</cfRule>
```

Text rule example:

```
<conditionalFormatting sqref="A2:A100">
  <cfRule type="containsText"
          operator="containsText"
          text="urgent"
          dxfId="0"
          priority="1">
    <formula>NOT(ISERROR(SEARCH(&quot;urgent&quot;,A2)))</formula>
  </cfRule>
</conditionalFormatting>
```

## Color scales

```
<conditionalFormatting sqref="B2:B100">
  <cfRule type="colorScale" priority="2">
    <colorScale>
      <cfvo type="min"/>
      <cfvo type="percentile" val="50"/>
      <cfvo type="max"/>
      <color rgb="FFF8696B"/>
      <color rgb="FFFFEB84"/>
      <color rgb="FF63BE7B"/>
    </colorScale>
  </cfRule>
</conditionalFormatting>
```

Common <cfvo type="..."> values:

```
min
max
num
percent
percentile
formula
```

Excel extension rules also use values such as autoMin and autoMax.

## Data bars

```
<conditionalFormatting sqref="C2:C100">
  <cfRule type="dataBar" priority="3">
    <dataBar showValue="1" minLength="10" maxLength="90">
      <cfvo type="min"/>
      <cfvo type="max"/>
      <color rgb="FF638EC6"/>
    </dataBar>
  </cfRule>
</conditionalFormatting>
```

Standard data bars are limited compared with modern Excel UI features. Negative-bar color, axis options, gradient toggles, and border options are usually stored in x14: extensions.

## Icon sets

```
<conditionalFormatting sqref="D2:D100">
  <cfRule type="iconSet" priority="4">
    <iconSet iconSet="3TrafficLights1"
             showValue="1"
             percent="1"
             reverse="0">
      <cfvo type="percent" val="0"/>
      <cfvo type="percent" val="33"/>
      <cfvo type="percent" val="67"/>
    </iconSet>
  </cfRule>
</conditionalFormatting>
```

Common standard icon-set names:

```
3Arrows
3ArrowsGray
3Flags
3TrafficLights1
3TrafficLights2
3Signs
3Symbols
3Symbols2
4Arrows
4ArrowsGray
4RedToBlack
4Rating
4TrafficLights
5Arrows
5ArrowsGray
5Rating
5Quarters
```

## timePeriod values

```
today
yesterday
tomorrow
last7Days
thisMonth
lastMonth
nextMonth
thisWeek
lastWeek
nextWeek
```

Example:

```
<conditionalFormatting sqref="A2:A100">
  <cfRule type="timePeriod"
          timePeriod="last7Days"
          dxfId="0"
          priority="5">
    <formula>AND(TODAY()-FLOOR(A2,1)&lt;=6,FLOOR(A2,1)&lt;=TODAY())</formula>
  </cfRule>
</conditionalFormatting>
```

## x14: extension rules

Modern Excel conditional-formatting features can live under worksheet <extLst> using the Office 2010+ x14 namespace:

```
<worksheet
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"
  xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main"
  mc:Ignorable="x14">

  ...

  <extLst>
    <ext uri="{78C0D931-6437-407d-A8EE-F0AAD7539E65}"
         xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main">
      <x14:conditionalFormattings>
        <x14:conditionalFormatting>
          <x14:cfRule type="dataBar" priority="1"
            id="{01234567-89AB-CDEF-0123-456789ABCDEF}">
            <x14:dataBar minLength="0" maxLength="100"
                         border="1"
                         gradient="0"
                         negativeBarColorSameAsPositive="0">
              <x14:cfvo type="autoMin"/>
              <x14:cfvo type="autoMax"/>
              <x14:fillColor rgb="FF638EC6"/>
              <x14:borderColor rgb="FF638EC6"/>
              <x14:negativeFillColor rgb="FFFF0000"/>
              <x14:axisColor rgb="FF000000"/>
            </x14:dataBar>
          </x14:cfRule>
          <xm:sqref>C2:C100</xm:sqref>
        </x14:conditionalFormatting>
      </x14:conditionalFormattings>
    </ext>
  </extLst>
</worksheet>
```

Preserve Excel-authored x14: blocks when editing existing files.

# Data validation

Data validations live in the worksheet, usually after conditional formatting and before hyperlinks/page setup in schema order.

```
<dataValidations count="1">
  <dataValidation type="whole"
                  operator="between"
                  allowBlank="1"
                  showInputMessage="1"
                  promptTitle="Allowed"
                  prompt="Enter a whole number from 1 to 10."
                  showErrorMessage="1"
                  errorStyle="stop"
                  errorTitle="Invalid value"
                  error="Use a whole number from 1 to 10."
                  sqref="A2:A100">
    <formula1>1</formula1>
    <formula2>10</formula2>
  </dataValidation>
</dataValidations>
```

formula1 and formula2 contain the criteria. For between and notBetween, both formulas represent lower and upper bounds. For most other operators, only formula1 is used. For list and custom validations, formula1 holds the list source or custom formula.

## Validation types

```
none
whole
decimal
list
date
time
textLength
custom
```

Examples:

```
<dataValidation type="decimal" operator="greaterThan" sqref="B2:B100">
  <formula1>0</formula1>
</dataValidation>

<dataValidation type="date" operator="between" sqref="C2:C100">
  <formula1>DATE(2026,1,1)</formula1>
  <formula2>DATE(2026,12,31)</formula2>
</dataValidation>

<dataValidation type="textLength" operator="lessThanOrEqual" sqref="D2:D100">
  <formula1>20</formula1>
</dataValidation>

<dataValidation type="custom" sqref="E2:E100">
  <formula1>ISNUMBER(E2)</formula1>
</dataValidation>
```

## Operators

```
between
notBetween
equal
notEqual
lessThan
lessThanOrEqual
greaterThan
greaterThanOrEqual
```

## Inline-list dropdown

```
<dataValidations count="1">
  <dataValidation type="list"
                  allowBlank="1"
                  showErrorMessage="1"
                  sqref="A2:A100">
    <formula1>&quot;Red,Green,Blue&quot;</formula1>
  </dataValidation>
</dataValidations>
```

For values containing commas, long lists, dynamic lists, or translated workbooks, use a range instead.

## Same-sheet range dropdown

```
<dataValidation type="list"
                allowBlank="1"
                showErrorMessage="1"
                sqref="B2:B100">
  <formula1>$H$2:$H$20</formula1>
</dataValidation>
```

## Cross-sheet dropdown through a defined name

Most compatible approach: define a name in workbook.xml:

```
<definedNames>
  <definedName name="StatusList">'Lists'!$A$2:$A$20</definedName>
</definedNames>
```

Then use the name in validation:

```
<dataValidation type="list"
                allowBlank="1"
                showErrorMessage="1"
                sqref="C2:C100">
  <formula1>StatusList</formula1>
</dataValidation>
```

## Cascading dropdowns with INDIRECT

Suppose C2 contains a category such as Fruit, and there is a defined name Fruit pointing to a list:

```
<dataValidation type="list"
                allowBlank="1"
                showErrorMessage="1"
                sqref="D2:D100">
  <formula1>INDIRECT($C2)</formula1>
</dataValidation>
```

If category labels contain spaces, use sanitized defined names and transform the selected value:

```
<dataValidation type="list"
                allowBlank="1"
                showErrorMessage="1"
                sqref="D2:D100">
  <formula1>INDIRECT(SUBSTITUTE($C2,&quot; &quot;,&quot;_&quot;))</formula1>
</dataValidation>
```

Validation formulas are evaluated relative to the top-left cell of sqref, so $C2 naturally adjusts by row for D2:D100.

## Prompt and error messages

```
<dataValidation type="whole"
                operator="between"
                allowBlank="1"
                showInputMessage="1"
                promptTitle="Quantity"
                prompt="Enter 1 through 100."
                showErrorMessage="1"
                errorStyle="warning"
                errorTitle="Check quantity"
                error="The value should be between 1 and 100."
                sqref="A2:A100">
  <formula1>1</formula1>
  <formula2>100</formula2>
</dataValidation>
```

errorStyle values:

```
stop
warning
information
```

## showDropDown gotcha

For normal .xlsx generation, omit showDropDown or write showDropDown="0" when you want the dropdown arrow to appear. Despite the name, many Excel-compatible libraries document that showDropDown="1" means the in-cell dropdown arrow is hidden/suppressed in Excel and LibreOffice. Preserve Excel-authored values rather than normalizing this flag blindly.

## x14: data validations

Modern Excel can store data validations in worksheet <extLst> using x14:dataValidations:

```
<worksheet
  xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"
  xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main"
  mc:Ignorable="x14">

  ...

  <extLst>
    <ext uri="{CCE6A557-97BC-4b89-ADB6-D9C93CAAB3DF}"
         xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main">
      <x14:dataValidations count="1"
          xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main">
        <x14:dataValidation type="list"
                            allowBlank="1"
                            showErrorMessage="1">
          <x14:formula1>
            <xm:f>Lists!$A$2:$A$20</xm:f>
          </x14:formula1>
          <xm:sqref>C2:C100</xm:sqref>
        </x14:dataValidation>
      </x14:dataValidations>
    </ext>
  </extLst>
</worksheet>
```

Preserve x14:dataValidations blocks when editing existing files.

# Modern extensions and compatibility

Modern Excel files often contain extension and compatibility constructs:

```
xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main"
xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"
xmlns:xm="http://schemas.microsoft.com/office/excel/2006/main"
xmlns:xda="http://schemas.microsoft.com/office/spreadsheetml/2017/dynamicarray"
mc:Ignorable="x14 x14ac"
```

Practical preservation rule:

```
When editing an Excel-authored file, preserve unfamiliar extension blocks unless you intentionally understand and rewrite them.
```

Common extension-bearing features:

| Feature | Common extension area |
|---|---|
| Modern conditional formatting | worksheet <extLst> with x14:conditionalFormattings |
| Modern data validation | worksheet <extLst> with x14:dataValidations |
| Dynamic arrays | xl/metadata.xml, cell metadata indexes, and xda:* extensions |
| Row/column compatibility hints | x14ac:* namespaces and attributes |
| Future functions | formula prefixes such as _xlfn. |

# Generator-safe checklists

## Package checklist

```
[Content_Types].xml has Default rels.
[Content_Types].xml has Overrides for XML parts that require them.
Every relationship target exists.
Every r:id used in XML exists in the correct local .rels file.
No stale relationship points to a missing part.
Do not include parts that are not referenced unless intentionally preserving them.
```

## Workbook checklist

```
workbook.xml has <sheets>/<sheet> entries.
Each sheet has a unique sheetId.
Each sheet r:id points to a worksheet/chartsheet/dialogsheet part.
sharedStrings relationship exists if any cell uses t="s".
styles relationship exists if any cell uses non-default s or date formatting.
localSheetId values are zero-based sheet positions, not sheetId values.
```

## Worksheet checklist

```
<worksheet> children are in schema order.
<sheetData> exists.
Rows and cells are written in ascending order.
Cell r attributes are correct.
inlineStr cells use <is>, not <v>.
shared-string cells use zero-based indexes into sharedStrings.xml.
Date cells are numeric values plus date styles.
<tableParts> appears near the end, before extLst.
```

## Styles checklist

```
Cell s indexes are valid indexes into cellXfs.
fontId/fillId/borderId indexes exist.
Custom numFmtId values are defined under numFmts and usually start at 164.
Solid fills use fgColor.
dxfId values reference dxfs, not cellXfs.
count attributes match actual child counts, or omit counts.
```

## Formula checklist

```
<f> has no leading "=".
XML-sensitive formula characters are escaped.
Shared formulas have a master with ref+si.
Array formulas have t="array" and ref on the master.
External formulas have externalLink parts/relationships if preserving links.
Delete stale calcChain.xml after formula edits.
Set calcPr fullCalcOnLoad/forceFullCalc if recalculation is desired.
```

## Feature checklists

Defined names:

```
Use workbook.xml / definedNames.
Omit localSheetId for global names.
Use zero-based sheet position for localSheetId.
Avoid custom names beginning _xl or _xlnm.
Use simple ASCII names that do not look like cell references.
```

Tables:

```
Keep table data in worksheet cells.
Add table part, content type, worksheet relationship, and tableParts entry.
Keep table ref rectangular and unmerged.
Use built-in TableStyleLight/Medium/Dark names unless preserving custom styles.
Put calculated/totals metadata in tableColumn.
```

Conditional formatting:

```
Put reusable formatting in styles.xml / dxfs.
Reference dxfs with zero-based dxfId.
Use child structures for colorScale, dataBar, and iconSet.
Preserve x14 extLst rules.
```

Data validation:

```
Use formula1/formula2 with no leading equals.
Use defined names for cross-sheet list sources when compatibility matters.
Omit showDropDown unless intentionally preserving existing behavior.
Preserve x14:dataValidations blocks.
```

Shared strings:

```
t="s" means <v> is a zero-based shared-string index.
inlineStr uses <is>, not <v>.
Keep count and uniqueCount correct.
Use xml:space="preserve" for significant leading/trailing spaces.
Use _xHHHH_ only for illegal XML characters or literal escape disambiguation.
```

# Recipes: what files must I touch?

Use these recipe cards as a quick implementation checklist.

## Add plain numbers

```
Parts:          xl/worksheets/sheetN.xml
Relationships:  No
Content type:   No
Gotcha:         Use invariant decimal text, not localized commas.
```

## Add inline strings

```
Parts:          xl/worksheets/sheetN.xml
Relationships:  No
Content type:   No
Gotcha:         inlineStr uses <is>, not <v>.
```

## Add shared strings

```
Parts:          worksheet + xl/sharedStrings.xml
Relationships:  Add workbook relationship if sharedStrings.xml is new.
Content type:   Add sharedStrings override if new.
Gotcha:         t="s" index must exist in sharedStrings.xml.
```

## Add styles

```
Parts:          worksheet + xl/styles.xml
Relationships:  Add workbook relationship if styles.xml is new.
Content type:   Add styles override if new.
Gotcha:         Cell s is a zero-based cellXfs index.
```

## Add dates

```
Parts:          worksheet + xl/styles.xml
Relationships:  Add styles relationship if styles.xml is new.
Content type:   Add styles override if new.
Gotcha:         Date/time is a numeric serial plus a date/time style.
```

## Add formulas

```
Parts:          worksheet, and maybe workbook calcPr
Relationships:  Usually no
Content type:   Usually no
Gotcha:         No leading =. Cached <v> may be stale.
```

## Add a table

```
Parts:          worksheet + sheet rels + xl/tables/tableN.xml
Relationships:  Yes, worksheet relationship to the table part.
Content type:   Yes, table part override.
Gotcha:         Actual data remains in worksheet cells.
```

## Add data validation

```
Parts:          worksheet
Relationships:  No
Content type:   No
Gotcha:         showDropDown="1" hides the dropdown arrow.
```

## Add conditional formatting

```
Parts:          worksheet + styles.xml dxfs when reusable formatting is needed
Relationships:  Maybe styles relationship if styles.xml is new.
Content type:   Maybe styles override if styles.xml is new.
Gotcha:         dxfId indexes dxfs, not cellXfs.
```

## Add a defined name

```
Parts:          xl/workbook.xml
Relationships:  No
Content type:   No
Gotcha:         localSheetId is zero-based sheet position, not sheetId.
```

## Add an external workbook link

```
Parts:          workbook.xml + workbook rels + externalLink part + externalLink rels
Relationships:  Yes
Content type:   Yes
Gotcha:         Formula syntax and package metadata both matter.
```

## Add an image

```
Parts:          worksheet + drawing part + drawing rels + media
Relationships:  Yes
Content type:   Usually image default; drawing part needs its content type.
Gotcha:         Requires drawing anchors, not just a media file.
```

# Appendix A: compact element glossary

| Pattern | Meaning |
|---|---|
| <sheetData> | Worksheet cell table. |
| <row r="3"> | Row 3. |
| <c r="B3"> | Cell B3. |
| <v> | Cell value or cached formula result. |
| <f> | Formula text. |
| t="s" | Shared-string cell. |
| t="n" or no t | Number. |
| t="b" | Boolean. |
| t="inlineStr" | Inline string. |
| s="4" | Style index 4. |
| <sst> | Shared string table. |
| <si> | Shared string item. |
| <xf> | Style/format record. |
| <dxf> | Differential formatting record. |
| <cfRule> | Conditional-formatting rule. |
| <dataValidation> | Data-validation rule. |
| <tableParts> | Worksheet references to table parts. |

# Appendix B: worksheet order quick reference

```
sheetPr, dimension, sheetViews, sheetFormatPr, cols, sheetData,
sheetCalcPr, sheetProtection, protectedRanges, scenarios, autoFilter,
sortState, dataConsolidate, customSheetViews, mergeCells, phoneticPr,
conditionalFormatting, dataValidations, hyperlinks, printOptions,
pageMargins, pageSetup, headerFooter, rowBreaks, colBreaks,
customProperties, cellWatches, ignoredErrors, smartTags, drawing,
legacyDrawing, legacyDrawingHF, picture, oleObjects, controls,
webPublishItems, tableParts, extLst
```

# Appendix C: selected references from the source notes

The source notes referenced these standards, documentation pages, and implementation notes:

- ECMA-376 Office Open XML standard:
- Microsoft Learn: Structure of a SpreadsheetML document:
- Microsoft Learn: Working with sheets:
- Microsoft Learn: Working with formulas:
- Microsoft Learn: Working with the shared string table:
- Microsoft Learn: Working with SpreadsheetML tables:
- Microsoft Learn: Working with conditional formatting:
- Microsoft Support: Date systems in Excel:
- Microsoft Support: Structured references with Excel tables:
- OOXML Info part summary:
- OOXML Info external workbook references:
- Datypic worksheet schema reference:
- Datypic cell type reference:
- c-rex definedName reference:
- c-rex escaped string reference:
- Eric White: Dates in SpreadsheetML:
- Eric White: Force recalculation of workbook/worksheet:
- ClosedXML cell-format notes:
- EPPlus data validation list notes:
