"""<Page Module Name> - ONE-SENTENCE INTENT: the question this page answers.

INTENT
    One short paragraph: what this page module contributes to the document and
    who reads it. Answer-first prose works well - a claim-bearing heading + the
    finding, then evidence, then method/sources - but the engine is general:
    compose any mix of prose, tables, structured_blocks, and wireframes.

OUTLINE
    Top-to-bottom block map (this is a SOURCE-ONLY note; it is NOT emitted):
        - H1:    page heading (a claim, not a label)
        - lead:  the finding paragraph (bold lead phrase allowed)
        - bullets: the supporting evidence
        - table: an evidence/rule table with a caption + source line

To use:
  1. Copy to doc_<program>/pages/<name>.py.
  2. Write the one-sentence INTENT above and set PAGE_TITLE.
  3. Build _body() from the imported builders (primitives / structured_blocks /
     wireframes); render() returns a PageModuleSpec.
  4. Register the module in doc_<program>/pages/__init__.py PAGES.
  5. Inspect with: python docx_core/doc_probe.py doc_<program>.pages.<name>
"""
from __future__ import annotations

from docx_core.primitives import (
    heading, paragraph, run, bullets, table_block, caption,
)
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_PORTRAIT
from docx_core.style_ids import R_STRONG, P_SOURCE

# Metadata (read by the packager / probe; not emitted into the document).
PAGE_TITLE = "Page Module Name"
PAGE_SETUP = PAGE_PORTRAIT               # page setup for this module


def _body() -> list[str]:
    """Return the ordered block XML for this page module. Replace the example."""
    return [
        heading(1, "Claim-bearing page heading"),
        paragraph([
            run("Finding: ", style=R_STRONG),
            run("state the answer in one sentence; evidence follows."),
        ]),
        *bullets([
            "First supporting point.",
            "Second supporting point.",
        ]),
        *table_block(
            ["Category", "Value", "Basis"],
            [["Addressable", "$1.8B", "FY2026 run-rate"]],
            caption_text="Table 1. Evidence bridge",
        ),
        paragraph("Sources: ...", style=P_SOURCE),
    ]


def render() -> PageModuleSpec:
    """Render this page module. Wrap the block list in a PageModuleSpec; set
    page_setup only when this module needs non-default page setup."""
    return PageModuleSpec(body=_body(), page_setup=PAGE_SETUP, title=PAGE_TITLE)
