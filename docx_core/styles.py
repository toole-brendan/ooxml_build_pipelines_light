"""docx_core.styles - build word/styles.xml from the house style manifest.

This is the heart of the Word style system and the analog of
workbook_core/styles.py: a manifest of style dataclasses (RunProps / ParaProps
carried by ParagraphStyle / CharacterStyle / TableStyle) plus one generator,
build_styles_xml(), that the packager calls once and writes to word/styles.xml.

Word leans on a native style cascade, so the contract authors use is the
semantic *style ID* (docx_core.style_ids: P_BODY, P_H1, R_STRONG, T_RULE, ...),
not raw run formatting on every paragraph. Spacing/rhythm rides on the paragraph
style (docx_core.rhythm), so normal prose needs no direct spacing XML.

Schema-order discipline (Word "repairs" a file whose children are out of order):
  - <w:rPr>   : rFonts, b, i, caps, color, sz, szCs, u
  - <w:pPr>   : keepNext, keepLines, spacing, jc, outlineLvl
  - <w:style> : name, basedOn, next, uiPriority, qFormat, pPr, rPr
Each is encoded in exactly one to_*_xml() method below.

Adding a style is the workbook 3-step in spirit: add a *_ID to style_ids.py, add
a dataclass entry to the relevant manifest list here, reference it from
primitives. Import direction: ooxml/style/style_ids/rhythm <- styles.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from xml.sax.saxutils import escape as xml_escape

from docx_core.ooxml import XML_DECL, NS_WR
from docx_core.style import (
    FONT, MONO, BLACK, WHITE, BLUE_5, GRAY_4, LINK_BLUE, hp,
    BODY_PT, SMALL_PT, H1_PT, H2_PT, H3_PT, TITLE_PT,
    BLOCK_HEADING_PT, COMPACT_BODY_PT, CODE_PT, CODE_SMALL_PT,
)
from docx_core.style_ids import (
    P_TITLE, P_BODY, P_H1, P_H2, P_H3, P_CAPTION, P_SOURCE, P_LIST,
    R_STRONG, R_EMPH, R_LINK,
    T_RULE, T_DARK_HEADER, T_NO_FORMAT, T_WIREFRAME,
    P_CODE, P_CODE_SMALL,
    P_BLOCK_HEADING, P_FIELD_LABEL, P_COMPACT_BODY,
)
from docx_core.rhythm import (
    ParaRhythm, R_BODY, R_TIGHT, R_LIST, R_H1, R_H2, R_H3, R_TITLE, R_CAPTION,
    R_SOURCE,
)

_NORMAL = "Normal"


# ---------------------------------------------------------------------------
# Manifest dataclasses (schema-ordered serializers)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RunProps:
    font: str | None = None
    size_hp: int | None = None
    bold: bool = False
    italic: bool = False
    color: str | None = None
    caps: bool = False
    underline: bool = False

    def to_rpr_xml(self) -> str:
        bits: list[str] = []
        if self.font:
            bits.append(f'<w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" '
                        f'w:cs="{self.font}"/>')
        if self.bold:
            bits.append("<w:b/>")
        if self.italic:
            bits.append("<w:i/>")
        if self.caps:
            bits.append("<w:caps/>")
        if self.color:
            bits.append(f'<w:color w:val="{self.color}"/>')
        if self.size_hp is not None:
            bits.append(f'<w:sz w:val="{self.size_hp}"/>')
            bits.append(f'<w:szCs w:val="{self.size_hp}"/>')
        if self.underline:
            bits.append('<w:u w:val="single"/>')
        return ("<w:rPr>" + "".join(bits) + "</w:rPr>") if bits else ""


@dataclass(frozen=True)
class ParaProps:
    align: str | None = None            # "left" | "center" | "right" | "both"
    keep_next: bool = False
    keep_lines: bool = False
    outline_level: int | None = None
    rhythm: ParaRhythm | None = None

    def to_ppr_inner(self) -> str:
        bits: list[str] = []
        if self.keep_next:
            bits.append("<w:keepNext/>")
        if self.keep_lines:
            bits.append("<w:keepLines/>")
        if self.rhythm is not None:
            bits.append(self.rhythm.to_spacing_xml())
        if self.align:
            bits.append(f'<w:jc w:val="{self.align}"/>')
        if self.outline_level is not None:
            bits.append(f'<w:outlineLvl w:val="{self.outline_level}"/>')
        return "".join(bits)


@dataclass(frozen=True)
class ParagraphStyle:
    style_id: str
    name: str
    based_on: str | None = None
    next_style: str | None = None
    run: RunProps | None = None
    para: ParaProps | None = None
    quick_format: bool = False
    ui_priority: int | None = None
    default: bool = False               # the one Normal style sets this
    custom: bool = True                 # built-in names (Normal/heading N/Title/caption) -> False

    def to_style_xml(self) -> str:
        attrs = 'w:type="paragraph"'
        if self.default:
            attrs += ' w:default="1"'
        attrs += f' w:styleId="{self.style_id}"'
        if self.custom:
            attrs += ' w:customStyle="1"'
        bits = [f'<w:name w:val="{xml_escape(self.name)}"/>']
        if self.based_on:
            bits.append(f'<w:basedOn w:val="{self.based_on}"/>')
        if self.next_style:
            bits.append(f'<w:next w:val="{self.next_style}"/>')
        if self.ui_priority is not None:
            bits.append(f'<w:uiPriority w:val="{self.ui_priority}"/>')
        if self.quick_format:
            bits.append("<w:qFormat/>")
        if self.para is not None:
            inner = self.para.to_ppr_inner()
            if inner:
                bits.append("<w:pPr>" + inner + "</w:pPr>")
        if self.run is not None:
            bits.append(self.run.to_rpr_xml())
        return f"<w:style {attrs}>" + "".join(bits) + "</w:style>"


@dataclass(frozen=True)
class CharacterStyle:
    style_id: str
    name: str
    run: RunProps
    based_on: str | None = "DefaultParagraphFont"
    ui_priority: int | None = None
    quick_format: bool = False
    custom: bool = False

    def to_style_xml(self) -> str:
        attrs = f'w:type="character" w:styleId="{self.style_id}"'
        if self.custom:
            attrs += ' w:customStyle="1"'
        bits = [f'<w:name w:val="{xml_escape(self.name)}"/>']
        if self.based_on:
            bits.append(f'<w:basedOn w:val="{self.based_on}"/>')
        if self.ui_priority is not None:
            bits.append(f'<w:uiPriority w:val="{self.ui_priority}"/>')
        if self.quick_format:
            bits.append("<w:qFormat/>")
        bits.append(self.run.to_rpr_xml())
        return f"<w:style {attrs}>" + "".join(bits) + "</w:style>"


@dataclass(frozen=True)
class TableStyle:
    style_id: str
    name: str
    inside_h: bool = False              # horizontal rules (top/bottom/insideH), no verticals
    header_fill: str | None = None      # dark-header fill hex (sets a firstRow conditional)
    header_color: str | None = None     # header text color when filled (default WHITE)
    ui_priority: int | None = 59
    custom: bool = True

    def to_style_xml(self) -> str:
        attrs = f'w:type="table" w:styleId="{self.style_id}"'
        if self.custom:
            attrs += ' w:customStyle="1"'
        bits = [f'<w:name w:val="{xml_escape(self.name)}"/>',
                '<w:basedOn w:val="TableNormal"/>']
        if self.ui_priority is not None:
            bits.append(f'<w:uiPriority w:val="{self.ui_priority}"/>')
        # Table-level properties: border posture + cell padding.
        borders = ""
        if self.inside_h:
            rule = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            borders = ("<w:tblBorders>"
                       + rule.format("top") + rule.format("bottom")
                       + rule.format("insideH") + "</w:tblBorders>")
        cell_mar = ('<w:tblCellMar>'
                    '<w:top w:w="60" w:type="dxa"/>'
                    '<w:left w:w="108" w:type="dxa"/>'
                    '<w:bottom w:w="60" w:type="dxa"/>'
                    '<w:right w:w="108" w:type="dxa"/>'
                    '</w:tblCellMar>')
        bits.append(f"<w:tblPr>{borders}{cell_mar}</w:tblPr>")
        # First-row (header) conditional formatting.
        if self.header_fill:
            bits.append(
                '<w:tblStylePr w:type="firstRow">'
                f'<w:rPr><w:b/><w:color w:val="{self.header_color or WHITE}"/></w:rPr>'
                '<w:tcPr>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{self.header_fill}"/>'
                '</w:tcPr>'
                '</w:tblStylePr>'
            )
        elif self.inside_h:
            bits.append(
                '<w:tblStylePr w:type="firstRow">'
                '<w:rPr><w:b/></w:rPr>'
                '<w:tcPr><w:tcBorders>'
                '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="auto"/>'
                '</w:tcBorders></w:tcPr>'
                '</w:tblStylePr>'
            )
        return f"<w:style {attrs}>" + "".join(bits) + "</w:style>"


# ---------------------------------------------------------------------------
# The house manifest
# ---------------------------------------------------------------------------

PARAGRAPH_STYLES: list[ParagraphStyle] = [
    ParagraphStyle(_NORMAL, "Normal", default=True, custom=False, quick_format=True),
    ParagraphStyle(
        P_BODY, "Body", based_on=_NORMAL, next_style=P_BODY, quick_format=True,
        run=RunProps(font=FONT, size_hp=hp(BODY_PT), color=BLACK),
        para=ParaProps(rhythm=R_BODY),
    ),
    ParagraphStyle(
        P_H1, "heading 1", based_on=_NORMAL, next_style=P_BODY, custom=False,
        quick_format=True, ui_priority=9,
        run=RunProps(font=FONT, size_hp=hp(H1_PT), bold=True, color=BLUE_5),
        para=ParaProps(rhythm=R_H1, keep_next=True, outline_level=0),
    ),
    ParagraphStyle(
        P_H2, "heading 2", based_on=_NORMAL, next_style=P_BODY, custom=False,
        quick_format=True, ui_priority=9,
        run=RunProps(font=FONT, size_hp=hp(H2_PT), bold=True, color=BLUE_5),
        para=ParaProps(rhythm=R_H2, keep_next=True, outline_level=1),
    ),
    ParagraphStyle(
        P_H3, "heading 3", based_on=_NORMAL, next_style=P_BODY, custom=False,
        quick_format=True, ui_priority=9,
        run=RunProps(font=FONT, size_hp=hp(H3_PT), bold=True, color=BLUE_5),
        para=ParaProps(rhythm=R_H3, keep_next=True, outline_level=2),
    ),
    ParagraphStyle(
        P_TITLE, "Title", based_on=_NORMAL, next_style=P_BODY, custom=False,
        quick_format=True, ui_priority=10,
        run=RunProps(font=FONT, size_hp=hp(TITLE_PT), bold=True, color=BLACK),
        para=ParaProps(rhythm=R_TITLE),
    ),
    ParagraphStyle(
        P_CAPTION, "caption", based_on=P_BODY, custom=False, ui_priority=35,
        quick_format=True,
        run=RunProps(font=FONT, size_hp=hp(SMALL_PT), italic=True, color=GRAY_4),
        para=ParaProps(rhythm=R_CAPTION),
    ),
    ParagraphStyle(
        P_SOURCE, "Source", based_on=P_BODY,
        run=RunProps(font=FONT, size_hp=hp(SMALL_PT), italic=True, color=GRAY_4),
        para=ParaProps(rhythm=R_SOURCE),
    ),
    # List items (bullet / numbered / outline): body run, tight list rhythm so a
    # list reads as one block instead of inheriting body prose's 6pt-after. The
    # glyph/number + hanging indent come from numbering.xml, not this style.
    ParagraphStyle(
        P_LIST, "List Body", based_on=P_BODY, next_style=P_LIST, ui_priority=34,
        para=ParaProps(rhythm=R_LIST),
    ),
    # Structured-block paragraph styles (generic structured documents).
    ParagraphStyle(
        P_BLOCK_HEADING, "Block Heading", based_on=P_BODY,
        run=RunProps(font=FONT, size_hp=hp(BLOCK_HEADING_PT), bold=True, color=BLUE_5),
        para=ParaProps(rhythm=R_H2, keep_next=True),
    ),
    ParagraphStyle(
        P_FIELD_LABEL, "Field Label", based_on=P_BODY,
        run=RunProps(font=FONT, size_hp=hp(COMPACT_BODY_PT), bold=True),
        para=ParaProps(rhythm=R_TIGHT, keep_next=True),
    ),
    ParagraphStyle(
        P_COMPACT_BODY, "Compact Body", based_on=P_BODY,
        run=RunProps(font=FONT, size_hp=hp(COMPACT_BODY_PT)),
        para=ParaProps(rhythm=R_TIGHT),
    ),
    # Monospace paragraph styles (ASCII wireframes / code blocks).
    ParagraphStyle(
        P_CODE, "Code", based_on=P_BODY,
        run=RunProps(font=MONO, size_hp=hp(CODE_PT), color=BLACK),
        para=ParaProps(rhythm=R_TIGHT),
    ),
    ParagraphStyle(
        P_CODE_SMALL, "Code Small", based_on=P_CODE,
        run=RunProps(font=MONO, size_hp=hp(CODE_SMALL_PT), color=BLACK),
        para=ParaProps(rhythm=R_TIGHT),
    ),
]

CHARACTER_STYLES: list[CharacterStyle] = [
    CharacterStyle(R_STRONG, "Strong", RunProps(bold=True), ui_priority=22, quick_format=True),
    CharacterStyle(R_EMPH, "Emphasis", RunProps(italic=True), ui_priority=20, quick_format=True),
    CharacterStyle(R_LINK, "Hyperlink", RunProps(color=LINK_BLUE, underline=True), ui_priority=99),
]

TABLE_STYLES: list[TableStyle] = [
    TableStyle(T_RULE, "Rule Table", inside_h=True),
    TableStyle(T_DARK_HEADER, "Dark Header Table", inside_h=True,
               header_fill=BLUE_5, header_color=WHITE),
    TableStyle(T_NO_FORMAT, "No Format Table"),
    # Layout grid for table-grid wireframes: no inherent borders/header (the
    # wire_cell helper paints per-cell borders + fills), tight cell margins.
    TableStyle(T_WIREFRAME, "Wireframe Table"),
]


# ---------------------------------------------------------------------------
# Default styles Word expects (one default per style type) + docDefaults
# ---------------------------------------------------------------------------

def _doc_defaults_xml() -> str:
    sz = hp(BODY_PT)
    return (
        "<w:docDefaults>"
        "<w:rPrDefault><w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
        f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        '<w:lang w:val="en-US"/>'
        "</w:rPr></w:rPrDefault>"
        "<w:pPrDefault><w:pPr>"
        + R_BODY.to_spacing_xml() +
        "</w:pPr></w:pPrDefault>"
        "</w:docDefaults>"
    )


_DEFAULT_CHAR_STYLE_XML = (
    '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">'
    '<w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/>'
    '<w:semiHidden/><w:unhideWhenUsed/></w:style>'
)
_DEFAULT_TABLE_STYLE_XML = (
    '<w:style w:type="table" w:default="1" w:styleId="TableNormal">'
    '<w:name w:val="Normal Table"/><w:uiPriority w:val="99"/>'
    '<w:semiHidden/><w:unhideWhenUsed/>'
    '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
    '<w:tblCellMar>'
    '<w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
    '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
    '</w:tblCellMar></w:tblPr></w:style>'
)
_DEFAULT_NUM_STYLE_XML = (
    '<w:style w:type="numbering" w:default="1" w:styleId="NoList">'
    '<w:name w:val="No List"/><w:uiPriority w:val="99"/>'
    '<w:semiHidden/><w:unhideWhenUsed/></w:style>'
)


# ---------------------------------------------------------------------------
# Override merge (data, not edits to the manifest)
# ---------------------------------------------------------------------------

def _resolve_paragraph(styles, overrides):
    """Apply style_overrides {style_id: {"run": {...}, "para": {...}}} to the
    paragraph manifest, returning new frozen instances (never mutates)."""
    if not overrides:
        return styles
    out = []
    for s in styles:
        ov = overrides.get(s.style_id)
        if not ov:
            out.append(s)
            continue
        run = s.run
        if "run" in ov:
            run = replace(run, **ov["run"]) if run is not None else RunProps(**ov["run"])
        para = s.para
        if "para" in ov:
            para = replace(para, **ov["para"]) if para is not None else ParaProps(**ov["para"])
        out.append(replace(s, run=run, para=para))
    return out


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def build_styles_xml(style_overrides: dict | None = None) -> str:
    """Render word/styles.xml from the manifest.

    style_overrides is data, not a manifest edit: {style_id: {"run": {...kwargs},
    "para": {...kwargs}}} re-skins a paragraph style (brand color, heading scale,
    spacing) without touching this module. Emit order: docDefaults, the three
    type defaults (Normal/DefaultParagraphFont/TableNormal/NoList), then the
    paragraph, character, and table manifests.
    """
    paras = _resolve_paragraph(PARAGRAPH_STYLES, style_overrides)
    return (
        XML_DECL
        + f"<w:styles {NS_WR}>"
        + _doc_defaults_xml()
        + _DEFAULT_CHAR_STYLE_XML
        + _DEFAULT_TABLE_STYLE_XML
        + _DEFAULT_NUM_STYLE_XML
        + "".join(s.to_style_xml() for s in paras)
        + "".join(s.to_style_xml() for s in CHARACTER_STYLES)
        + "".join(s.to_style_xml() for s in TABLE_STYLES)
        + "</w:styles>"
    )
