"""Page registry - ONE module per page; PAGES order = document order.

Each entry is a page module exposing render() -> docx_core.specs.PageModuleSpec
(or a docx_core.specs.PageEntry when one file registers several pages). The
packager (docx_core.lib.package_docx) concatenates the page-module bodies into
word/document.xml and inserts a section break between modules.

To add a page:
  1. Copy docx_core/doc_base_template.py to doc_outsourced_ceiling/pages/<name>.py.
  2. Write INTENT, set PAGE_TITLE, build _body() (primitives / structured_blocks /
     wireframes).
  3. Import the module here and append it to PAGES, in document order.
"""
from __future__ import annotations

from . import ceiling_methodology_explainer

PAGES = [
    ceiling_methodology_explainer,  # Outsourcing ceiling: plain-language prose explainer (portrait)
]
