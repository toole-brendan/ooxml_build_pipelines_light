"""docx_core.numbering - build word/numbering.xml (bullets, numbers, outline).

Word lists are not just a paragraph style: a list paragraph carries a
<w:numPr><w:ilvl/><w:numId/></w:numPr>, and that numId must resolve through a
<w:num> to a <w:abstractNum> that defines the glyphs, indents and hanging. So
numbering deserves its own module rather than hiding inside paragraph().

This module owns three abstract lists and exposes the author-facing numId
constants the primitives reference:
    NUMID_BULLET    -> bullet glyphs (3 levels)
    NUMID_NUMBERED  -> 1. / a. / i. (decimal, lowerLetter, lowerRoman)
    NUMID_OUTLINE   -> 1 / 1.1 / 1.1.1 (legal multilevel)

Critical ordering (Word repairs otherwise): in word/numbering.xml every
<w:abstractNum> comes before every <w:num>. The NUMID_* constants here MUST match
the emitted <w:num w:numId="..."> values - they are the contract primitives.py
consumes. Imports docx_core.units / docx_core.ooxml only.
"""
from __future__ import annotations

from docx_core.ooxml import XML_DECL, NS_WR
from docx_core.units import twips_from_in

# abstractNumId values (internal) and the author-facing numId values.
_ABSTRACT_BULLET = 0
_ABSTRACT_NUMBERED = 1
_ABSTRACT_OUTLINE = 2

NUMID_BULLET = 1
NUMID_NUMBERED = 2
NUMID_OUTLINE = 3

# Per-level indent geometry. The marker hangs back 0.25in from the text; the
# text itself starts at 0.5in for level 0 and steps 0.25in deeper per level
# (720 / 1080 / 1440 twips). That puts the bullet glyph at 0.25in - clearly
# indented from the parent paragraph at the margin - matching the house
# reference doc (left=720 hanging=360 at the top level), not flush at the margin.
_HANG = twips_from_in(0.25)             # 360 twips: marker hangs back from text
_LEVEL0_LEFT = twips_from_in(0.5)       # 720 twips: text at 0.5in, glyph at 0.25in
_LEVEL_STEP = twips_from_in(0.25)       # 360 twips deeper per nested level


def _ind(level: int) -> str:
    left = _LEVEL0_LEFT + _LEVEL_STEP * level   # 720 / 1080 / 1440
    return f'<w:ind w:left="{left}" w:hanging="{_HANG}"/>'


def _lvl(ilvl: int, num_fmt: str, lvl_text: str, *, font: str | None = None,
         start: int = 1) -> str:
    rpr = (f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:hint="default"/></w:rPr>'
           if font else "")
    return (
        f'<w:lvl w:ilvl="{ilvl}">'
        f'<w:start w:val="{start}"/>'
        f'<w:numFmt w:val="{num_fmt}"/>'
        f'<w:lvlText w:val="{lvl_text}"/>'
        f'<w:lvlJc w:val="left"/>'
        f'<w:pPr>{_ind(ilvl)}</w:pPr>'
        f"{rpr}"
        f"</w:lvl>"
    )


def _abstract_num(aid: int, nsid: str, multilevel_type: str, levels: list[str]) -> str:
    return (
        f'<w:abstractNum w:abstractNumId="{aid}">'
        f'<w:nsid w:val="{nsid}"/>'
        f'<w:multiLevelType w:val="{multilevel_type}"/>'
        + "".join(levels)
        + "</w:abstractNum>"
    )


def _num(numid: int, aid: int) -> str:
    return f'<w:num w:numId="{numid}"><w:abstractNumId w:val="{aid}"/></w:num>'


# Bullet glyphs by level: Symbol bullet, Courier "o", Wingdings square.
_BULLET_LEVELS = [
    _lvl(0, "bullet", "&#xF0B7;", font="Symbol"),
    _lvl(1, "bullet", "o", font="Courier New"),
    _lvl(2, "bullet", "&#xF0A7;", font="Wingdings"),
]
_NUMBERED_LEVELS = [
    _lvl(0, "decimal", "%1."),
    _lvl(1, "lowerLetter", "%2."),
    _lvl(2, "lowerRoman", "%3."),
]
_OUTLINE_LEVELS = [
    _lvl(0, "decimal", "%1"),
    _lvl(1, "decimal", "%1.%2"),
    _lvl(2, "decimal", "%1.%2.%3"),
]


def build_numbering_xml() -> str:
    """Render word/numbering.xml: all abstractNum first, then all num."""
    abstracts = (
        _abstract_num(_ABSTRACT_BULLET, "0A1B2C30", "hybridMultilevel", _BULLET_LEVELS)
        + _abstract_num(_ABSTRACT_NUMBERED, "0A1B2C31", "hybridMultilevel", _NUMBERED_LEVELS)
        + _abstract_num(_ABSTRACT_OUTLINE, "0A1B2C32", "multilevel", _OUTLINE_LEVELS)
    )
    nums = (
        _num(NUMID_BULLET, _ABSTRACT_BULLET)
        + _num(NUMID_NUMBERED, _ABSTRACT_NUMBERED)
        + _num(NUMID_OUTLINE, _ABSTRACT_OUTLINE)
    )
    return XML_DECL + f"<w:numbering {NS_WR}>" + abstracts + nums + "</w:numbering>"
