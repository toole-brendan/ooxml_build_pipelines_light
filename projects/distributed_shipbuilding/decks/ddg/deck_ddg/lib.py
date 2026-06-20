"""Distributed Shipbuilding Destroyers deck pipeline bindings.

The OOXML engine lives in the shared ``deck_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this deck (the
output path, the shared template + brand assets under ``infra/``, the docProps
identity) and packages the registered SLIDE_RENDERS via the shared builder
``deck_core.lib.build_pptx``.

Slide modules import deck_core.* directly; the deck_core import path is set up in
deck_ddg/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.lib import build_pptx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DECK_DIR = Path(__file__).resolve().parents[1]      # projects/distributed_shipbuilding/ddg/deck/
PROJECT_DIR = Path(__file__).resolve().parents[1]   # projects/distributed_shipbuilding/ddg/   (build output lands here)
ROOT = Path(__file__).resolve().parents[5]          # workspace root (holds deck_core/ + infra/)

OUT = PROJECT_DIR / "20260602_Distributed Shipbuilding DDG_vS.pptx"

# Shared build chrome lives once under infra/ (not vendored per program).
TEMPLATE = ROOT / "infra" / "template"   # unzipped pptx template (layouts/master/theme)
ASSETS = ROOT / "infra" / "assets"       # brand media/ + embeddings/
IMAGES = DECK_DIR / "images"             # optional per-deck pictures (draft slots); created on demand

_TITLE = "Distributed Shipbuilding Destroyers - Outsourced Construction TAM & SAM"
_CREATOR = "deck_ddg build_deck.py"
_APP = "deck_ddg"


def build() -> int:
    """Render every registered slide and package into the output .pptx."""
    from deck_ddg.slides import SLIDE_RENDERS
    if not SLIDE_RENDERS:
        raise SystemExit(
            "deck_ddg/slides/__init__.py SLIDE_RENDERS is empty - add a slide "
            "module before building. Start by copying "
            "deck_core/slide_base_template.py to deck_ddg/slides/cover.py, then "
            "register it in deck_ddg/slides/__init__.py."
        )
    images = IMAGES if IMAGES.is_dir() else None
    build_pptx(SLIDE_RENDERS, out=OUT, extracted=TEMPLATE, assets=ASSETS,
               title=_TITLE, creator=_CREATOR, app=_APP, images=images)
    return 0
