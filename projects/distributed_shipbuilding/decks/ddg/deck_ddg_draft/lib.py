"""DRAFT Distributed Shipbuilding Destroyers deck pipeline bindings.

Sibling of ``deck_ddg/lib.py``: same shared ``deck_core`` engine, same template +
brand assets under ``infra/``, but it renders the reviewed DRAFT slide modules
registered in ``deck_ddg_draft/slides_draft/`` and writes to a distinct
``..._DDG_DRAFT_vS.pptx`` so it never overwrites the real deck output.

Slide modules import deck_core.* directly; the deck_core import path is set up in
deck_ddg_draft/__init__.py.
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

OUT = PROJECT_DIR / "20260602_Distributed Shipbuilding DDG_DRAFT_vS.pptx"

# Shared build chrome lives once under infra/ (not vendored per program).
TEMPLATE = ROOT / "infra" / "template"   # unzipped pptx template (layouts/master/theme)
ASSETS = ROOT / "infra" / "assets"       # brand media/ + embeddings/
IMAGES = DECK_DIR / "images"             # optional per-deck pictures (draft slots); created on demand

_TITLE = "Distributed Shipbuilding Destroyers - Outsourced Construction TAM & SAM (DRAFT)"
_CREATOR = "deck_ddg_draft build_drafts.py"
_APP = "deck_ddg_draft"


def build() -> int:
    """Render every registered DRAFT slide and package into the output .pptx."""
    from deck_ddg_draft.slides_draft import SLIDE_RENDERS
    if not SLIDE_RENDERS:
        raise SystemExit(
            "deck_ddg_draft/slides_draft/__init__.py SLIDE_RENDERS is empty - add "
            "a slide module before building."
        )
    images = IMAGES if IMAGES.is_dir() else None
    build_pptx(SLIDE_RENDERS, out=OUT, extracted=TEMPLATE, assets=ASSETS,
               title=_TITLE, creator=_CREATOR, app=_APP, images=images)
    return 0
