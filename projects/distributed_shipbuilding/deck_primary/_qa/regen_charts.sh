#!/bin/bash
# Regenerate every _chart_xml/ data file from the source slides.
# Run from _qa/. Records the exact extraction args per slide so the static
# shape / verbatim-table / native-chart dumps rebuild deterministically.
#
# TWO sources:
#  - src_xml_v3/ - the v3 working deck (20260605_Defense Demand Drivers New
#    Construction_v3.pptx): the v2-built deck re-edited by hand in PowerPoint
#    (with think-cell), re-exported. Slides 1-3 are ported from it 1:1 - all
#    the former module-level patches (separator move, callout shifts, manager
#    ledger edits, strip remaps, ...) are baked into its XML, so the modules
#    are pure verbatim reads again.
#  - src_xml/ - the v2.0 deck, still the source for slides 4-6 (whose modules
#    have since diverged from it by design: penetration_outlook was realized
#    from the placeholder spec, slides 7-8 are new-built).
#
# The think-cell charts are REAL native <c:chart> parts, bundled verbatim with
# <c:externalData> stripped here; the modules re-add it via
# editable_bundled_chart, which reattaches the ORIGINAL binary .xlsb (copied
# below) so PowerPoint's "Edit Data" works. The OLE data frame and its tags
# are dropped by extract_chart. All non-frame shapes (chrome included) are
# transcribed verbatim - no keepout anywhere.
set -e
cd "$(dirname "$0")"
OUT=../deck_primary/slides/_chart_xml
X="/usr/bin/python3 extract_chart.py"
mkdir -p $OUT

# ---- slides 1-3: from the v3 deck (SRC env var switches the source tree) ----
SRC=src_xml_v3 $X 1 --offset 300 > $OUT/slide01.xml
SRC=src_xml_v3 $X 1 --tables 14,50 --offset 300 > $OUT/slide01_tables.xml
SRC=src_xml_v3 $X 2 --offset 300 > $OUT/slide02.xml
SRC=src_xml_v3 $X 2 --tables 6,53,54 --offset 300 > $OUT/slide02_tables.xml
SRC=src_xml_v3 $X 3 --offset 300 > $OUT/slide03.xml
SRC=src_xml_v3 $X 3 --tables 52 --offset 300 > $OUT/slide03_tables.xml

# ---- slides 4-6: from the v2.0 deck (unchanged) ----
$X 4 --offset 300 > $OUT/slide04.xml
$X 5 --offset 300 > $OUT/slide05.xml
$X 6 --offset 300 > $OUT/slide06.xml
$X 6 --tables 13 --offset 300 > $OUT/slide06_tables.xml

# native chart parts: verbatim, externalData stripped (no rels needed at this
# layer; editable_bundled_chart re-adds externalData + the .xlsb rel at build)
/usr/bin/python3 - <<'EOF'
import re
for src, plan in (("src_xml_v3", ((1, (1, 2)), (2, (3,)), (3, (4,)))),
                  ("src_xml",    ((5, (5,)),))):
    for slide, charts in plan:
        for k in charts:
            x = open(f"{src}/ppt/charts/chart{k}.xml", encoding="utf-8").read()
            x = re.sub(r'<c:externalData\b[^>]*>.*?</c:externalData>', '', x, flags=re.S)
            assert 'r:id=' not in x, f"chart{k}: dangling rel"
            out = f"../deck_primary/slides/_chart_xml/slide{slide:02d}_chart{k}.xml"
            open(out, "w", encoding="utf-8").write(x)
            print(f"{src}/chart{k} -> slide{slide:02d}_chart{k}.xml ({len(x)} bytes)")
EOF

# original binary workbooks for slides 1-3 (v3; chart rels verified:
# chart1<-Worksheet.xlsb, chart2<-Worksheet1.xlsb, chart3<-Worksheet2.xlsb,
# chart4<-Worksheet3.xlsb). Slide 5's slide05_chart5.xlsb stays the v2.0 copy.
E=src_xml_v3/ppt/embeddings
cp "$E/Microsoft_Excel_Binary_Worksheet.xlsb"  $OUT/slide01_chart1.xlsb
cp "$E/Microsoft_Excel_Binary_Worksheet1.xlsb" $OUT/slide01_chart2.xlsb
cp "$E/Microsoft_Excel_Binary_Worksheet2.xlsb" $OUT/slide02_chart3.xlsb
cp "$E/Microsoft_Excel_Binary_Worksheet3.xlsb" $OUT/slide03_chart4.xlsb

echo "regen complete"
