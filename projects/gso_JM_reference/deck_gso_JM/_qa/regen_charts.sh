#!/bin/bash
# Regenerate every _chart_xml/ data file for the GS&O style-guide port from the
# source slides. Run from _qa/. Records the exact extraction args per slide so
# the static-shape / verbatim-table / verbatim-pic / native-chart dumps rebuild
# deterministically after a tool change.
#
# Source: src_xml/ (20260615_GS&O_Strategy Materials Style Guide.pptx). Theme is
# byte-identical to infra/template, so schemeClr accentN refs resolve to the same
# hexes (verified). Each slide carries floating purple `JM:` reviewer callouts;
# their cNvPr ids are --keepout here (and captured in JM_style_notes.md).
#
# Charts are REAL native <c:chart> parts bundled verbatim with <c:externalData>
# stripped; the modules re-add it via editable_bundled_chart, reattaching the
# original binary .xlsb so PowerPoint "Edit Data" works. The OLE data frames
# ("think-cell data - do not delete", + their EMF fallback image1.emf) are
# dropped by extract_chart (chart mode drops every graphicFrame). Real top-level
# pics (logos / flags / wordmarks) are transcribed verbatim by extract_pics with
# their r:embed remapped to controlled rIds (preserving drop shadows).
set -e
cd "$(dirname "$0")"
OUT=../deck_gso_JM/slides/_chart_xml
IMG=../deck_gso_JM/slides/images
X="python3 extract_chart.py"
XP="python3 extract_pics.py"
mkdir -p "$OUT" "$IMG"

# ---- slide 1 — Bridge Charts (1/2): chart1 + table 331 + US-flag pic 56 ----
# JM callouts: 9,10,11,12,13,14,17,19,21,22,30,31,32,35 ; pic 56 (-> extract_pics)
$X 1 --keepout 9,10,11,12,13,14,17,19,21,22,30,31,32,35,56 --offset 300 > $OUT/slide01.xml
$X 1 --tables 331 --offset 300 > $OUT/slide01_tables.xml
$XP 1 --ids 56 --embeds rId3 --offset 300 > $OUT/slide01_pics.xml

# ---- slide 2 — Bridge Charts (2/2): chart2 + chart3 + 4 company logos ----
# JM callouts: 9,11,12,13,14,15,16,18,19,20 ; logo pics 2052,2054,2058,2060
$X 2 --keepout 9,11,12,13,14,15,16,18,19,20,2052,2054,2058,2060 --offset 300 > $OUT/slide02.xml
$XP 2 --ids 2052,2054,2058,2060 --embeds rId4,rId5,rId6,rId7 --offset 300 > $OUT/slide02_pics.xml

# ---- slide 3 — Bar Charts: chart4 + SHIPS Act table 11 (no real pics) ----
# JM callouts: 3,7,9
$X 3 --keepout 3,7,9 --offset 300 > $OUT/slide03.xml
$X 3 --tables 11 --offset 300 > $OUT/slide03_tables.xml

# ---- slide 4 — Tables: opex table 155 + 4 wordmark/badge pics (no chart) ----
# JM callouts: 8,9,10,11,12,13,14,15,16,17 ; pics 269,271,273,279
$X 4 --keepout 8,9,10,11,12,13,14,15,16,17,269,271,273,279 --offset 300 > $OUT/slide04.xml
$X 4 --tables 155 --offset 300 > $OUT/slide04_tables.xml
$XP 4 --ids 269,271,273,279 --embeds rId2,rId3,rId4,rId5 --offset 300 > $OUT/slide04_pics.xml

# ---- slide 5 — Flow Charts: flow diagram + 1 China + 3 US flags (no chart) ----
# JM callouts: 3,5,8,11 ; flag pics 35,36,60,61
$X 5 --keepout 3,5,8,11,35,36,60,61 --offset 300 > $OUT/slide05.xml
$XP 5 --ids 35,36,60,61 --embeds rId2,rId3,rId4,rId5 --offset 300 > $OUT/slide05_pics.xml

# native chart parts: verbatim, externalData stripped (editable_bundled_chart
# re-adds externalData + the .xlsb rel at build).
python3 - <<'EOF'
import re
# (slide, chartfile, xlsb) — chart<-xlsb verified from charts/_rels/chartN.xml.rels
plan = [(1, "chart1", "Microsoft_Excel_Binary_Worksheet.xlsb"),
        (2, "chart2", "Microsoft_Excel_Binary_Worksheet1.xlsb"),
        (2, "chart3", "Microsoft_Excel_Binary_Worksheet2.xlsb"),
        (3, "chart4", "Microsoft_Excel_Binary_Worksheet3.xlsb")]
OUT = "../deck_gso_JM/slides/_chart_xml"
for slide, chart, xlsb in plan:
    x = open(f"src_xml/ppt/charts/{chart}.xml", encoding="utf-8").read()
    x = re.sub(r'<c:externalData\b[^>]*>.*?</c:externalData>', '', x, flags=re.S)
    assert 'r:id=' not in x, f"{chart}: dangling rel"
    open(f"{OUT}/slide{slide:02d}_{chart}.xml", "w", encoding="utf-8").write(x)
    import shutil
    shutil.copyfile(f"src_xml/ppt/embeddings/{xlsb}", f"{OUT}/slide{slide:02d}_{chart}.xlsb")
    print(f"{chart} -> slide{slide:02d}_{chart}.xml ({len(x)} bytes) + .xlsb")
EOF

echo "regen complete"
