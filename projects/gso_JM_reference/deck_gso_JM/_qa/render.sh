#!/bin/bash
# Render the built GS&O style-guide deck to per-slide PNGs for visual QA.
# Usage: _qa/render.sh [first] [last]   (default: all slides)
set -e
PPTX="/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/gso_JM_reference/20260615_GSO_Strategy Materials Style Guide_vS.pptx"
OUT="/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/gso_JM_reference/deck_gso_JM/_qa/png"
mkdir -p "$OUT"
rm -f "$OUT"/*.pdf   # never reuse a stale PDF after a rebuild
soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
if [ -n "$1" ]; then
  pdftoppm -png -r 96 -f "$1" -l "${2:-$1}" "$PDF" "$OUT/slide"
else
  pdftoppm -png -r 96 "$PDF" "$OUT/slide"
fi
echo "rendered -> $OUT"
ls "$OUT"/slide*.png 2>/dev/null
