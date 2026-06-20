"""Distributed Shipbuilding Word pipeline bindings.

The OOXML engine lives in the shared ``docx_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this document
(the output path, the docProps identity) and packages the registered PAGES
via the shared builder ``docx_core.lib.package_docx``.

Page modules import docx_core.* directly; the docx_core import path is set up
in doc_distributed_shipbuilding/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from docx_core.lib import package_docx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DOC_DIR = Path(__file__).resolve().parents[1]       # projects/distributed_shipbuilding/doc/
PROJECT_DIR = Path(__file__).resolve().parents[2]   # projects/distributed_shipbuilding/  (build output lands here)

OUT = PROJECT_DIR / "20260616_Distributed Shipbuilding_Sourcing-Openings Methodology_vS.docx"

_TITLE = "Distributed Shipbuilding - Sourcing-Openings Methodology"
_CREATOR = "doc_distributed_shipbuilding build_doc.py"
_APP = "doc_distributed_shipbuilding"


def build() -> int:
    """Render every registered page module and package into the output .docx."""
    from doc_distributed_shipbuilding.pages import PAGES
    if not PAGES:
        raise SystemExit(
            "doc_distributed_shipbuilding/pages/__init__.py PAGES is empty - add a "
            "page module before building. Start by copying "
            "docx_core/doc_base_template.py to "
            "doc_distributed_shipbuilding/pages/overview.py, then register it in "
            "doc_distributed_shipbuilding/pages/__init__.py."
        )
    return package_docx(OUT, PAGES, title=_TITLE, creator=_CREATOR, app_name=_APP)
