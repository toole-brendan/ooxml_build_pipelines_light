#!/bin/bash
# Render the built Awards Methodology deck to per-slide PNGs for visual QA.
# Usage: _qa/render.sh [first] [last]   (default: all slides)
set -e
PPTX="/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/other/awards_methodology/20260622_Awards Methodology_vS.pptx"
OUT="/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/other/awards_methodology/_qa/png"
mkdir -p "$OUT"
soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
if [ -n "$1" ]; then
  pdftoppm -png -r 96 -f "$1" -l "${2:-$1}" "$PDF" "$OUT/slide"
else
  pdftoppm -png -r 96 "$PDF" "$OUT/slide"
fi
echo "rendered -> $OUT"
ls "$OUT"/slide*.png 2>/dev/null
