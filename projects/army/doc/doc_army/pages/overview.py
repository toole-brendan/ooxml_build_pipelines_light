"""overview - SCAFFOLD PLACEHOLDER: proves the doc pipeline emits a valid page.

This is the seed module from the new-project scaffold. It renders a heading + a
lead paragraph so ``build_doc.py`` produces a valid 1-page .docx immediately.
Replace it with real page modules per docx_core/doc_guide.md: copy
docx_core/doc_base_template.py to a new pages/<name>.py, build _body(), and
register it in pages/__init__.py.

INTENT
    Placeholder overview page; carries no load-bearing content.

OUTLINE
    - H1:   page heading
    - lead: one placeholder paragraph
"""
from __future__ import annotations

from docx_core.primitives import heading, paragraph, run
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_PORTRAIT
from docx_core.style_ids import R_STRONG

PAGE_TITLE = "Overview"
PAGE_SETUP = PAGE_PORTRAIT


def _body() -> list[str]:
    return [
        heading(1, "U.S. Army - Market Mapping"),
        paragraph([
            run("Scaffold placeholder: ", style=R_STRONG),
            run("replace this page with the first real content module."),
        ]),
    ]


def render() -> PageModuleSpec:
    """Render this page module. Wrap the block list in a PageModuleSpec."""
    return PageModuleSpec(body=_body(), page_setup=PAGE_SETUP, title=PAGE_TITLE)
