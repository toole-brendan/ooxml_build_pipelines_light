"""docx_core.specs - the declarative objects a page module returns.

The DOCX analog of workbook_core's WorksheetSpec and the deck's <p:sld> string.
A page module's render() returns a PageModuleSpec: the ordered block XML for one
page module plus its optional page setup. The packager concatenates page-module
bodies into word/document.xml and owns where each module's <w:sectPr> lands.

The authoring unit is the PAGE MODULE - it normally starts a new Word page and
owns that page's setup. It is not a hard guarantee that the content fits on
exactly one physical page; Word repaginates at render time and the probe reports
what shipped.

PageEntry is the workbook_core.SheetEntry analog: it lets ONE source file
register MULTIPLE page modules (the packager accepts either a bare module or a
PageEntry). The common case stays one file per page module.

Kept deliberately thin and free of any primitives import, so it sits low in the
import graph (the packager imports it; primitives do not). Authors build the
`body` list with docx_core.primitives builders.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:                       # avoid an import cycle at runtime
    from docx_core.page_setup import PageSetup


@dataclass
class PageModuleSpec:
    """What a page module's render() returns.

    body:        ordered block XML strings (paragraphs, tables, wireframes) - the
                 page-module content, in paint/reading order.
    page_setup:  page size/orientation/margins/columns for this module; None
                 inherits the document default (PAGE_PORTRAIT). When two adjacent
                 modules differ, the packager inserts a section break between them.
    title:       optional module label (used for docProps/app TitlesOfParts and
                 the probe); not emitted into the body.
    """
    body: list[str]
    page_setup: "PageSetup | None" = None
    title: str | None = None


@dataclass(frozen=True)
class PageEntry:
    """A page module to register, decoupled from the one-file-per-module layout.

    Lets ONE source file register MULTIPLE page modules. The packager
    (lib.package_docx) accepts either a page *module* (reads PAGE_TITLE / render())
    OR a PageEntry, normalizing both to a (title, render) pair - so the two styles
    coexist and a pipeline can group page code by responsibility rather than one
    module per page.

    title:  module label (docProps TitlesOfParts / probe); not emitted.
    render: zero-arg callable returning this module's PageModuleSpec.
    """
    title: str
    render: Callable[[], "PageModuleSpec"]


@dataclass
class DocumentSpec:
    """Aggregate of an ordered page-module list. The packager assembles this from
    the rendered modules; exposed for callers that want to build a document in
    memory rather than from a module registry."""
    pages: list[PageModuleSpec] = field(default_factory=list)
