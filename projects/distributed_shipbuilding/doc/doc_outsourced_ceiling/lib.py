"""Outsourcing Ceiling Word pipeline bindings.

The OOXML engine lives in the shared ``docx_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this document
(the output path, the docProps identity) and packages the registered PAGES via the
shared builder ``docx_core.lib.package_docx``.

Page modules import docx_core.* directly; the docx_core import path is set up in
doc_outsourced_ceiling/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from docx_core.lib import package_docx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DOC_DIR = Path(__file__).resolve().parents[1]       # projects/distributed_shipbuilding/doc/
PROJECT_DIR = Path(__file__).resolve().parents[2]   # projects/distributed_shipbuilding/  (build output lands here)

OUT = PROJECT_DIR / "20260616_Outsourcing Ceiling_Methodology_vS.docx"

_TITLE = "Outsourcing Ceiling - Plain-Language Methodology"
_CREATOR = "doc_outsourced_ceiling build_outsourced_ceiling.py"
_APP = "doc_outsourced_ceiling"


def build() -> int:
    """Render every registered page module and package into the output .docx."""
    from doc_outsourced_ceiling.pages import PAGES
    if not PAGES:
        raise SystemExit(
            "doc_outsourced_ceiling/pages/__init__.py PAGES is empty - add a page "
            "module before building."
        )
    return package_docx(OUT, PAGES, title=_TITLE, creator=_CREATOR, app_name=_APP)
