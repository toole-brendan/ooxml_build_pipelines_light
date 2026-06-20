#!/bin/bash
# Regenerate every _chart_xml/ data file from the source slides via extract_chart.py.
# Run from _qa/. Records the exact --keepout / --tables args per slide so the static
# chart / verbatim-table dumps can be rebuilt deterministically after a tool change.
# (slide09_chart1.xml is the bundled native chart part and is produced separately.)
set -e
cd "$(dirname "$0")"
OUT=../deck_mro/slides/_chart_xml
X="/usr/bin/python3 extract_chart.py"

# slide : annot keepout (chrome/tables/captions/footers kept as primitives or tables)
$X 4  --keepout 2,4,5            --offset 300 > $OUT/slide04.xml
$X 4  --tables  14              --offset 300 > $OUT/slide04_table.xml
$X 5  --keepout 2,4,7            --offset 300 > $OUT/slide05.xml
$X 5  --tables  3               --offset 300 > $OUT/slide05_table.xml
$X 6  --keepout 448,475,476,477,478,479 --offset 300 > $OUT/slide06.xml
$X 7  --keepout 7,192,193,194,195,197   --offset 300 > $OUT/slide07.xml
$X 8  --keepout 2,5,6,7,9,67     --offset 300 > $OUT/slide08.xml
$X 8  --tables  7               --offset 300 > $OUT/slide08_table.xml
$X 9  --keepout 4,5,6            --offset 300 > $OUT/slide09.xml
$X 10 --keepout 4,5,6            --offset 300 > $OUT/slide10.xml
$X 10 --tables  7               --offset 300 > $OUT/slide10_table.xml
$X 11 --keepout 4,5,6            --offset 300 > $OUT/slide11.xml
$X 12 --keepout 2,3,4,480        --offset 300 > $OUT/slide12.xml
$X 12 --tables  5               --offset 300 > $OUT/slide12_table.xml
$X 13 --keepout 241,242,243,481  --offset 300 > $OUT/slide13.xml
$X 14 --keepout 482             --offset 300 > $OUT/slide14.xml
$X 14 --tables  19              --offset 300 > $OUT/slide14_table.xml
$X 15 --keepout 2,3,4,483        --offset 300 > $OUT/slide15.xml
$X 15 --tables  5               --offset 300 > $OUT/slide15_table.xml
echo "regen complete"
