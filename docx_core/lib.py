"""Word engine - the packager that turns a list of page modules into a .docx.

Stdlib-only, no python-docx. This module owns the package-level XML (everything
that is not page-module body): [Content_Types].xml, the relationship files,
styles.xml, numbering.xml, settings.xml, fontTable.xml, docProps, and the zip
packaging. The page-module bodies come from author modules: each exposes a
render() (or render_<stem>()) returning a docx_core.specs.PageModuleSpec, OR is
registered via a PageEntry. Block/run string building lives in primitives.py;
styling in styles.py; numbering in numbering.py.

Mirrors workbook_core.lib.package_workbook (module resolution, strict spec
coercion, ValueError-on-collision, named package builders, [Content_Types].xml
written first) and ports deck_core.lib's OPC guard (every packaged part must have
a declared content type, else the build raises before the file is written).

Import direction (no cycle): ooxml <- ... <- specs <- primitives <- lib.

docx archive layout produced by package_docx():
  [Content_Types].xml
  _rels/.rels
  docProps/core.xml
  docProps/app.xml
  word/document.xml
  word/_rels/document.xml.rels
  word/styles.xml
  word/numbering.xml
  word/settings.xml
  word/fontTable.xml
"""
from __future__ import annotations

import datetime as dt
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from docx_core.ooxml import XML_DECL, NS_W, NS_WR
from docx_core.primitives import document
from docx_core.specs import PageModuleSpec, PageEntry
from docx_core.page_setup import PAGE_PORTRAIT


# ---------------------------------------------------------------------------
# Page-module resolution (module-first registry; PageEntry is the multi-page
# escape hatch, mirroring workbook_core.SheetEntry)
# ---------------------------------------------------------------------------

def _module_stem(mod) -> str:
    return mod.__name__.rsplit(".", 1)[-1]


def _is_entry(item) -> bool:
    return isinstance(item, PageEntry)


def _render_fn(mod):
    """Find a module's render callable: render() or render_<stem>()."""
    fn = getattr(mod, "render", None)
    if callable(fn):
        return fn
    stem = _module_stem(mod)
    fn = getattr(mod, f"render_{stem}", None)
    if callable(fn):
        return fn
    raise AttributeError(f"{mod.__name__} must expose render() or render_{stem}()")


def _item_label(item) -> str:
    """Identifier for error messages (PageEntry title / module name)."""
    if _is_entry(item):
        return f"PageEntry({item.title!r})"
    return getattr(item, "__name__", repr(item))


def _item_render(item):
    """Zero-arg render callable returning a PageModuleSpec - PageEntry.render or a
    module's render()/render_<stem>()."""
    if _is_entry(item):
        if not callable(item.render):
            raise AttributeError(f"{_item_label(item)} render is not callable")
        return item.render
    return _render_fn(item)


def _coerce_spec(rendered, label: str) -> PageModuleSpec:
    """Require render() to return a PageModuleSpec (the build is strict; the probe
    is lenient)."""
    if isinstance(rendered, PageModuleSpec):
        return rendered
    raise TypeError(
        f"{label}: render() must return a PageModuleSpec, got "
        f"{type(rendered).__name__!r}. Wrap a block list: PageModuleSpec(body=[...])."
    )


def _page_title(item, spec: PageModuleSpec) -> str:
    if _is_entry(item):
        return spec.title or item.title
    return (spec.title
            or getattr(item, "PAGE_TITLE", None)
            or _module_stem(item).replace("_", " ").title())


# ---------------------------------------------------------------------------
# Package-level XML
# ---------------------------------------------------------------------------

_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml."


def build_content_types() -> str:
    return (
        XML_DECL
        + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f'<Override PartName="/word/document.xml" ContentType="{_CT}document.main+xml"/>'
        f'<Override PartName="/word/styles.xml" ContentType="{_CT}styles+xml"/>'
        f'<Override PartName="/word/numbering.xml" ContentType="{_CT}numbering+xml"/>'
        f'<Override PartName="/word/settings.xml" ContentType="{_CT}settings+xml"/>'
        f'<Override PartName="/word/fontTable.xml" ContentType="{_CT}fontTable+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    )


def build_root_rels() -> str:
    return (
        XML_DECL
        + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )


def build_document_rels() -> str:
    rt = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
    return (
        XML_DECL
        + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + f'<Relationship Id="rId1" Type="{rt}styles" Target="styles.xml"/>'
        + f'<Relationship Id="rId2" Type="{rt}numbering" Target="numbering.xml"/>'
        + f'<Relationship Id="rId3" Type="{rt}settings" Target="settings.xml"/>'
        + f'<Relationship Id="rId4" Type="{rt}fontTable" Target="fontTable.xml"/>'
        + '</Relationships>'
    )


def build_settings_xml() -> str:
    # NOTE: no <w:updateFields/> - the MVP emits no fields (TOC/PAGEREF/REF), and
    # that flag makes Word prompt "update the fields…" on every open for nothing.
    # When the later fields phase lands, set it only on documents that have fields.
    return (
        XML_DECL
        + f'<w:settings {NS_WR}>'
        + '<w:defaultTabStop w:val="720"/>'
        + '<w:characterSpacingControl w:val="doNotCompress"/>'
        + '<w:compat>'
        '<w:compatSetting w:name="compatibilityMode" '
        'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
        '</w:compat>'
        + '</w:settings>'
    )


def build_font_table_xml() -> str:
    def _font(name: str, family: str) -> str:
        return (f'<w:font w:name="{name}"><w:charset w:val="00"/>'
                f'<w:family w:val="{family}"/><w:pitch w:val="variable"/></w:font>')
    return (
        XML_DECL
        + f'<w:fonts {NS_WR}>'
        + _font("Arial", "swiss")
        + _font("Symbol", "roman")
        + _font("Courier New", "modern")
        + _font("Wingdings", "auto")
        + '</w:fonts>'
    )


def build_core_props(title: str, creator: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        XML_DECL
        + '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f'<dc:title>{xml_escape(title)}</dc:title>'
        f'<dc:creator>{xml_escape(creator)}</dc:creator>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        '</cp:coreProperties>'
    )


def build_app_props(app_name: str, page_titles: list[str]) -> str:
    n = len(page_titles)
    titles = "".join(f"<vt:lpstr>{xml_escape(t)}</vt:lpstr>" for t in page_titles)
    return (
        XML_DECL
        + '<Properties '
        'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        f'<Application>{xml_escape(app_name)}</Application>'
        '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
        '<HeadingPairs><vt:vector size="2" baseType="variant">'
        '<vt:variant><vt:lpstr>Page modules</vt:lpstr></vt:variant>'
        f'<vt:variant><vt:i4>{n}</vt:i4></vt:variant>'
        '</vt:vector></HeadingPairs>'
        f'<TitlesOfParts><vt:vector size="{n}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>'
        '<Company></Company><LinksUpToDate>false</LinksUpToDate>'
        '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
        '<AppVersion>16.0000</AppVersion>'
        '</Properties>'
    )


# ---------------------------------------------------------------------------
# Body assembly + OPC guard
# ---------------------------------------------------------------------------

def _assemble_document_xml(rendered: list[tuple[str, PageModuleSpec]]) -> str:
    """Concatenate page-module bodies into <w:body>. Each module but the last ends
    in a section-break paragraph carrying that module's <w:sectPr>; the last
    module's <w:sectPr> is the final, body-level child (the critical Word rule)."""
    n = len(rendered)
    parts: list[str] = []
    final_sectpr = (rendered[-1][1].page_setup or PAGE_PORTRAIT).to_sectpr_xml()
    for i, (_title, spec) in enumerate(rendered):
        parts.append("".join(spec.body))
        if i < n - 1:
            props = spec.page_setup or PAGE_PORTRAIT
            parts.append(f"<w:p><w:pPr>{props.to_sectpr_xml()}</w:pPr></w:p>")
    return document("".join(parts), sect_pr=final_sectpr)


def _assert_unique_bookmarks(body_xml: str) -> None:
    names = re.findall(r'<w:bookmarkStart[^>]*\bw:name="([^"]*)"', body_xml)
    seen: set[str] = set()
    for nm in names:
        if nm in seen:
            raise ValueError(
                f"Duplicate bookmark name {nm!r}. Bookmark names are load-bearing "
                f"(cross-references resolve by value) and are never auto-renamed; "
                f"give the colliding bookmark a distinct name."
            )
        seen.add(nm)


def _opc_guard(parts: dict[str, str], content_types_xml: str) -> None:
    """Every packaged part must have a declared content type - a Default for its
    extension or an Override for its part name (ported from deck_core.lib)."""
    defaults = {e.lower() for e in re.findall(r'<Default Extension="([^"]+)"', content_types_xml)}
    overrides = set(re.findall(r'<Override PartName="([^"]+)"', content_types_xml))
    for name in parts:
        if name == "[Content_Types].xml":
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        if ext in defaults or ("/" + name) in overrides:
            continue
        raise ValueError(
            f"OPC: packaged part {name!r} has no declared content type "
            f"(no Default for .{ext} and no Override for /{name})."
        )


# ---------------------------------------------------------------------------
# Build entry point
# ---------------------------------------------------------------------------

def package_docx(out_path, page_modules, *, title: str, creator: str,
                 app_name: str, style_overrides: dict | None = None) -> int:
    """Render every page module and package into the output .docx.

    page_modules: the pipeline's PAGES list. Each item is either a page *module*
      exposing render()/render_<stem>() returning a PageModuleSpec (it may set
      PAGE_TITLE; else the title is the filename stem in Title Case), OR a
      PageEntry(title, render) when one source file registers several modules.
      render() MUST return a PageModuleSpec - a bare block list/string is rejected
      here (wrap it: PageModuleSpec(body=[...])).
    style_overrides: optional {style_id: {"run": {...}, "para": {...}}} re-skin
      data passed to build_styles_xml (brand color, heading scale, ...).
    out_path / title / creator / app_name: per-pipeline bindings.

    Raises ValueError on a duplicate bookmark name (load-bearing; never renamed)
    or any packaged part lacking a declared content type (the OPC guard).
    """
    out_path = Path(out_path)
    if not page_modules:
        raise ValueError("page_modules is empty - register at least one "
                         "page module before building.")

    # Render every page module to a PageModuleSpec.
    rendered: list[tuple[str, PageModuleSpec]] = []
    for item in page_modules:
        label = _item_label(item)
        spec = _coerce_spec(_item_render(item)(), label)
        rendered.append((_page_title(item, spec), spec))
    page_titles = [t for t, _ in rendered]

    document_xml = _assemble_document_xml(rendered)
    _assert_unique_bookmarks(document_xml)

    # build_styles_xml / build_numbering_xml imported lazily so a pipeline can
    # override styling without a hard dependency-direction issue (mirrors workbook).
    from docx_core.styles import build_styles_xml
    from docx_core.numbering import build_numbering_xml

    content_types = build_content_types()
    parts: dict[str, str] = {
        "[Content_Types].xml": content_types,
        "_rels/.rels": build_root_rels(),
        "docProps/core.xml": build_core_props(title, creator),
        "docProps/app.xml": build_app_props(app_name, page_titles),
        "word/document.xml": document_xml,
        "word/_rels/document.xml.rels": build_document_rels(),
        "word/styles.xml": build_styles_xml(style_overrides),
        "word/numbering.xml": build_numbering_xml(),
        "word/settings.xml": build_settings_xml(),
        "word/fontTable.xml": build_font_table_xml(),
    }
    _opc_guard(parts, content_types)

    n = len(rendered)
    print(f"Building {out_path.name} with {n} page(s) …")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # [Content_Types].xml first; the rest in a stable, readable order.
    order = [
        "[Content_Types].xml", "_rels/.rels",
        "docProps/core.xml", "docProps/app.xml",
        "word/document.xml", "word/_rels/document.xml.rels",
        "word/styles.xml", "word/numbering.xml",
        "word/settings.xml", "word/fontTable.xml",
    ]
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in order:
            zf.writestr(name, parts[name])
    for i, (t, _spec) in enumerate(rendered, start=1):
        print(f"  page {i}: {t}")
    print(f"Wrote {out_path}")
    print(f"  size: {out_path.stat().st_size:,} bytes  ·  document.xml: "
          f"{len(document_xml):,} bytes")
    return 0
