"""docx_core.ooxml - shared OOXML package plumbing (XML decl + namespaces).

The leaf module of the Word engine: the XML declaration, the WordprocessingML
namespace URIs, the assembled root-namespace attribute strings, and the parser
namespace map. Everything else in docx_core imports these from here, so the URIs
live in exactly one place. Mirrors workbook_core/ooxml.py and deck_core/ooxml.py.

No dependency on the rest of docx_core (import is cheap and cycle-free).
"""
from __future__ import annotations

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

# OpenXML namespace URIs.
NS_W   = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"          # w:  main schema
NS_R   = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"   # r:  part relationships
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"          # the xmlns on every *.rels
NS_MC  = "http://schemas.openxmlformats.org/markup-compatibility/2006"           # mc: markup compatibility
NS_W14 = "http://schemas.microsoft.com/office/word/2010/wordml"                  # w14: Word 2010 extensions

# DrawingML (the wireframe shape layer). NS_A is shared with deck_core; wp/wps/wpg
# are the WordprocessingML drawing wrappers a free-floating shape needs.
NS_WP  = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" # wp:  inline / anchor
NS_A   = "http://schemas.openxmlformats.org/drawingml/2006/main"                  # a:   DrawingML geometry/fill/text
NS_WPS = "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"      # wps: a shape inside a drawing
NS_WPG = "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"      # wpg: a shape group (canvas)

# Assembled xmlns attribute string for the <w:document> root. mc:Ignorable="w14"
# keeps the root forward-compatible with the w14:* attrs Word writes, without
# forcing us to emit them. wp/a/wps/wpg are declared here (where real Word puts
# them) so wireframe shapes need no local xmlns; they are NOT in mc:Ignorable -
# they carry the shape content (ignoring them would drop the drawing). The
# mc:AlternateContent + Choice Requires="wps" wrapper is what lets non-wps readers
# fall back gracefully.
NS_DOCUMENT = (f'xmlns:w="{NS_W}" '
               f'xmlns:r="{NS_R}" '
               f'xmlns:mc="{NS_MC}" '
               f'xmlns:w14="{NS_W14}" '
               f'xmlns:wp="{NS_WP}" '
               f'xmlns:a="{NS_A}" '
               f'xmlns:wps="{NS_WPS}" '
               f'xmlns:wpg="{NS_WPG}" '
               f'mc:Ignorable="w14"')

# Bare w+r xmlns string for the styles / numbering / settings / fontTable roots.
NS_WR = f'xmlns:w="{NS_W}" xmlns:r="{NS_R}"'

# Parser namespace map (ElementTree): the WordprocessingML main schema under "w"
# plus the DrawingML wrappers the probe inspects.
NS_MAP = {"w": NS_W, "r": NS_R, "mc": NS_MC, "w14": NS_W14,
          "wp": NS_WP, "a": NS_A, "wps": NS_WPS, "wpg": NS_WPG}
