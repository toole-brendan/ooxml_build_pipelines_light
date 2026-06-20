"""docx_core.style_ids - canonical Word style IDs (the leaf naming module).

The stable authoring language: every w:pStyle / w:rStyle / w:tblStyle reference
and every style *definition* in styles.py uses one of these IDs. Centralizing
them is the Word analog of workbook_core's S_* cellXfs indexes - but because Word
styles are addressable by name and survive user editing, the IDs are semantic
strings, not positional ints.

Leaf module: no dependency on the rest of docx_core. Author modules import the
names they need (P_BODY, R_STRONG, T_RULE, ...) instead of inlining string IDs.

The Heading1/2/3 and Title IDs are deliberate: Word reserves those styleIds for
its built-in heading styles, and the styles.py definitions name them "heading
1/2/3", set custom=False, and emit <w:outlineLvl> so the navigation pane, outline
view, and TOC field treat them as real headings. (No <w:builtinId> is emitted -
the reserved name plus the outline level is what Word keys on.)
"""
from __future__ import annotations

# --- Paragraph styles ------------------------------------------------------
P_TITLE = "Title"            # cover / report title (built-in)
P_BODY = "Body"              # normal prose (the document default, based on Normal)
P_H1 = "Heading1"            # main section heading (built-in, outline level 0)
P_H2 = "Heading2"            # subsection heading (built-in, outline level 1)
P_H3 = "Heading3"            # minor heading (built-in, outline level 2)
P_CAPTION = "Caption"        # figure / table caption (italic, small, gray)
P_SOURCE = "Source"          # source / provenance note (small, gray)

# --- Character (run) styles ------------------------------------------------
R_STRONG = "Strong"          # bold emphasis / lead phrase
R_EMPH = "Emphasis"          # italic qualifier
R_LINK = "Hyperlink"         # external / internal link (Office built-in name)

# --- Table styles ----------------------------------------------------------
T_RULE = "RuleTable"             # default evidence table: horizontal rules, no vertical grid
T_DARK_HEADER = "DarkHeaderTable"  # primary table: dark header row, white text
T_NO_FORMAT = "NoFormatTable"      # native-table behavior with no visible styling (escape hatch)
T_WIREFRAME = "WireframeTable"     # table used as a layout grid for table-grid wireframes

# --- Monospace paragraph styles (ASCII wireframes / code) ------------------
P_CODE = "Code"                  # monospace block (ASCII diagrams, code, fixed-width sketches)
P_CODE_SMALL = "CodeSmall"       # smaller monospace block (denser ASCII diagrams)

# --- List paragraph style --------------------------------------------------
# Lists are real Word numbering (the w:numId values live in docx_core/numbering.py
# as NUMID_*), but the *spacing* of list items rides on a paragraph style like
# everything else. P_LIST is that style: a tight list rhythm (single line, small
# after) so bullet/numbered/outline items don't inherit body prose's 6pt-after and
# 1.15 line. The glyph/number + hanging indent come from numbering.py; P_LIST only
# carries the rhythm (and the body run, via based_on Body).
P_LIST = "ListBody"

# --- Structured-block paragraph styles (generic structured documents) ------
P_BLOCK_HEADING = "BlockHeading"        # a structured-block heading (card title, register entry)
P_FIELD_LABEL = "FieldLabel"            # a bold field label ("Purpose", "Owner", ...)
P_COMPACT_BODY = "CompactBody"          # tight body copy under a label (no extra after-space)
