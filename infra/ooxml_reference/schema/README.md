# ECMA-376 Transitional XSDs

Vendored schemas used by `deck/validate.py` to check every rendered slide
body against ECMA-376 Transitional before it's packed into a `.pptx`.

## Provenance

Source: [QtExcel/ecma-376-5th](https://github.com/QtExcel/ecma-376-5th),
path `ECMA-376/OfficeOpenXML-XMLSchema-Transitional/`.

- Commit: `457ce928a15b2ccda8ffbd7f6fc4e828113c6290` (2019-02-16)
- Repo status: archived (read-only since Sep 2019). ECMA-376 5th edition
  is frozen, so the schema content is stable.
- Upstream license: ECMA-376 is published by ECMA International under
  terms permitting redistribution for implementation purposes; see the
  ECMA-376 standard for full terms.

The Transitional set (not Strict) is used because the Saronic chrome and
our authored slides both declare the 2006 namespaces, e.g.,
`xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"`. Real-
world `.pptx` files almost universally use Transitional.

## What's vendored

The complete Transitional set — 26 files, ~960 KB:

- `pml.xsd` — PresentationML (root for `<p:sld>`)
- `dml-main.xsd`, `dml-chart.xsd`, `dml-chartDrawing.xsd`,
  `dml-diagram.xsd`, `dml-lockedCanvas.xsd`, `dml-picture.xsd`,
  `dml-spreadsheetDrawing.xsd`, `dml-wordprocessingDrawing.xsd`
- `shared-additionalCharacteristics.xsd`, `shared-bibliography.xsd`,
  `shared-commonSimpleTypes.xsd`, `shared-customXmlDataProperties.xsd`,
  `shared-customXmlSchemaProperties.xsd`,
  `shared-documentPropertiesCustom.xsd`,
  `shared-documentPropertiesExtended.xsd`,
  `shared-documentPropertiesVariantTypes.xsd`, `shared-math.xsd`,
  `shared-relationshipReference.xsd`
- `wml.xsd`, `sml.xsd` (transitively imported by DrawingML)
- `vml-main.xsd`, `vml-officeDrawing.xsd`, `vml-presentationDrawing.xsd`,
  `vml-spreadsheetDrawing.xsd`, `vml-wordprocessingDrawing.xsd`

All files must remain in this directory (flat layout) — the
`<xs:import schemaLocation="..."/>` paths reference siblings by relative
filename.

## Refresh procedure

If a future ECMA edition or a QtExcel fix needs to be pulled in:

```bash
cd deck/_schema
BASE="https://raw.githubusercontent.com/QtExcel/ecma-376-5th/master/ECMA-376/OfficeOpenXML-XMLSchema-Transitional"
for f in *.xsd; do curl -sfO "$BASE/$f"; done
# Confirm closure (no unresolved imports):
cd .. && python3 -c "from validate import _get_schema; _get_schema(); print('OK')"
```

Bump the commit SHA above. Re-run `python3 build.py` to confirm all
currently-registered slides still validate.
