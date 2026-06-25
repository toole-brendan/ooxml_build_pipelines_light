"""deck_commercial_strategy - reference-port pipeline for the Commercial Strategy
Market Analysis deck.

Single slides ported 1:1 from the source deck onto the shared ``deck_core``
engine (docs/faithful_deck_port_methodology.md), to act as a reference corpus an
AI agent can study when authoring custom slide modules. Each module is emitted by
_tools/convert_slide.py: surrounding shapes become idiomatic deck_core primitive
calls (text_box / connector / graphic_frame), and native <c:chart> exhibits are
bundled verbatim with their .xlsb via editable_bundled_chart (byte-exact, still
"Edit Data"-editable). think-cell OLE frames + their EMF previews are dropped.

Thin per-deck package: binds the output path, the shared template + brand assets,
and the docProps identity (lib.py), and registers the slide modules (slides/).
The raw-OOXML engine is the canonical ``deck_core`` package at the workspace
root; the slide modules import ``deck_core.*`` directly. No vendored engine copy.

Two dirs go on sys.path so both packages resolve regardless of entry point:
  - the build dir (this package's parent) so ``deck_commercial_strategy`` resolves;
  - the workspace root (four levels up) so ``deck_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_BUILD_DIR = str(_HERE.parents[1])   # projects/style_library/deck_commercial_strategy/
_CORE_DIR = str(_HERE.parents[4])    # workspace root (holds deck_core + infra)

for _p in (_BUILD_DIR, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
