"""docx_core - shared raw-OOXML WordprocessingML engine + authoring kit.

Stdlib-only. The single source of truth for the Word (.docx) engine, the third
sibling of deck_core (.pptx) and workbook_core (.xlsx). The per-program pipelines
(doc_<program>/) bind output path + docProps and register page modules; they
import docx_core.* directly and never vendor a copy of the engine.

Authoring unit: the PAGE MODULE. A page module's render() returns a
docx_core.specs.PageModuleSpec; the packager (lib.package_docx) concatenates the
module bodies into word/document.xml and owns all OPC plumbing. A page module
normally starts a new Word page and owns that page's setup - but Word repaginates
at render time, so it is not a guarantee that content fits exactly one physical
page; the probe reports what shipped. One source file can register several page
modules via a specs.PageEntry (the workbook_core.SheetEntry analog).

The build is the only strict layer (it rejects anything that would produce broken
or ambiguous OOXML); the guide recommends readable document design; the probe
reports what shipped and never judges.

Import direction (no cycle):
  ooxml
    <- style, units
    <- style_ids, rhythm
    <- styles, numbering, page_setup
    <- specs
    <- primitives
    <- structured_blocks, wireframes
    <- lib

Module roles:
  ooxml.py            XML decl + WordprocessingML/DrawingML namespace constants.
  style.py            pure design tokens (FONT, MONO, palette, type scale, hp()).
  units.py            twips / line / EMU conversions.
  style_ids.py        canonical Word style IDs (P_BODY, R_STRONG, T_RULE, P_CODE,
                      P_BLOCK_HEADING, ...).
  rhythm.py           margins + line/paragraph spacing presets.
  styles.py           build word/styles.xml from the house style manifest.
  numbering.py        build word/numbering.xml (bullet / numbered / outline lists).
  page_setup.py       page setup (<w:sectPr> presets: PAGE_PORTRAIT / PAGE_LANDSCAPE).
  specs.py            PageModuleSpec / PageEntry / DocumentSpec (what render() returns).
  primitives.py       run / paragraph / heading / bullet / table / document builders.
  structured_blocks.py field_block / card_block / checklist_block / definition_list.
  wireframes.py       ASCII / table-grid / DrawingML wireframe + diagram builders.
  lib.py              package_docx() - renders page modules, owns OPC parts, zips .docx.
  doc_probe.py        read-only structural inspector (module + file mode).
  doc_base_template.py / doc_guide.md / doc_snippets.md   authoring kit.

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
