"""U.S. Army Market Mapping Word pipeline bindings.

The OOXML engine lives in the shared ``docx_core`` package at the workspace root.
This module is intentionally thin: it binds the things specific to this document
(the output path, the docProps identity) and packages the registered PAGES
via the shared builder ``docx_core.lib.package_docx``.

Page modules import docx_core.* directly; the docx_core import path is set up
in doc_army/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from docx_core.lib import package_docx

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

DOC_DIR = Path(__file__).resolve().parents[1]       # projects/army/doc/
PROJECT_DIR = Path(__file__).resolve().parents[2]   # projects/army/  (build output lands here)

OUT = PROJECT_DIR / "20260620_US Army Market Mapping_vS.docx"

_TITLE = "U.S. Army - Market Mapping"
_CREATOR = "doc_army build_doc.py"
_APP = "doc_army"


def build() -> int:
    """Render every registered page module and package into the output .docx."""
    from doc_army.pages import PAGES
    if not PAGES:
        raise SystemExit(
            "doc_army/pages/__init__.py PAGES is empty - add a "
            "page module before building. Start by copying "
            "docx_core/doc_base_template.py to "
            "doc_army/pages/overview.py, then register it in "
            "doc_army/pages/__init__.py."
        )
    return package_docx(OUT, PAGES, title=_TITLE, creator=_CREATOR, app_name=_APP)
