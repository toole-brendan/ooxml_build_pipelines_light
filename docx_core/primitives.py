"""docx_core.primitives - WordprocessingML block/run builders.

The raw-OOXML string builders a section module composes, analogous to the deck's
run/paragraph/text_box builders and the workbook's cell/row/worksheet builders.
Styles-first: a paragraph/run names a style ID (docx_core.style_ids) and the look
comes from word/styles.xml; local overrides are allowed; passing raw OOXML is the
escape hatch when a primitive is not enough.

Surface:
  run / paragraph / heading                 - text
  bullet / bullets / numbered / outline_item - lists (numId from numbering.py)
  caption / page_break / bookmark_start/end  - structure
  tcell / trow / table / table_block         - tables (rule-table default)
  document                                   - the <w:document><w:body> wrapper

Two correctness rules are baked in so authors can't trip them: <w:pPr> is always
emitted before runs, and every <w:tc> carries at least one <w:p>. Import
direction: ooxml / style_ids / numbering <- primitives.
"""
from __future__ import annotations

import re
from xml.sax.saxutils import escape as xml_escape

from docx_core.ooxml import XML_DECL, NS_DOCUMENT
from docx_core.style_ids import (
    P_BODY, P_H1, P_H2, P_H3, P_CAPTION, P_LIST, T_RULE, T_DARK_HEADER,
)
from docx_core.numbering import NUMID_BULLET, NUMID_NUMBERED, NUMID_OUTLINE

_HEADING_STYLE = {1: P_H1, 2: P_H2, 3: P_H3}

# Default usable text width on Letter with 1in margins (8.5 - 2 = 6.5in -> twips).
_DEFAULT_TABLE_TWIPS = 9360


# ---------------------------------------------------------------------------
# Escaping
# ---------------------------------------------------------------------------

def xml_text(s) -> str:
    """Escape for element text content (& < >)."""
    return xml_escape(str(s))


def xml_attr(s) -> str:
    """Escape for attribute values (& < > plus quotes)."""
    return xml_escape(str(s), {'"': "&quot;", "'": "&apos;"})


# ---------------------------------------------------------------------------
# Runs and paragraphs
# ---------------------------------------------------------------------------

def run(text, *, style: str | None = None, bold: bool = False, italic: bool = False,
        caps: bool = False, color: str | None = None, size_hp: int | None = None,
        font: str | None = None, space_preserve: bool = True) -> str:
    """A single run. `style` is a character-style ID (e.g. R_STRONG); the other
    args are direct overrides. rPr child order: rStyle, rFonts, b, i, caps, color,
    sz, szCs, u."""
    bits: list[str] = []
    if style:
        bits.append(f'<w:rStyle w:val="{style}"/>')
    if font:
        bits.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>')
    if bold:
        bits.append("<w:b/>")
    if italic:
        bits.append("<w:i/>")
    if caps:
        bits.append("<w:caps/>")
    if color:
        bits.append(f'<w:color w:val="{color}"/>')
    if size_hp is not None:
        bits.append(f'<w:sz w:val="{size_hp}"/><w:szCs w:val="{size_hp}"/>')
    rpr = ("<w:rPr>" + "".join(bits) + "</w:rPr>") if bits else ""
    sp = ' xml:space="preserve"' if space_preserve else ""
    return f"<w:r>{rpr}<w:t{sp}>{xml_text(text)}</w:t></w:r>"


def _runs_xml(content) -> str:
    """Normalize paragraph content to run XML. A plain string becomes one
    auto-run; a string already starting with '<w:' is used verbatim; a list mixes
    both (plain items auto-run)."""
    if content is None or content == "":
        return ""
    if isinstance(content, str):
        return content if content[:3] == "<w:" else run(content)
    out = []
    for c in content:
        out.append(c if (isinstance(c, str) and c[:3] == "<w:") else run(c))
    return "".join(out)


def paragraph(content="", *, style: str = P_BODY, align: str | None = None,
              num: tuple[int, int] | None = None, keep_next: bool = False,
              raw_ppr_extra: str = "") -> str:
    """A paragraph. `content` is plain text, one run() string, or a list of runs.
    `num=(numId, ilvl)` joins a list. pPr child order: pStyle, keepNext, numPr,
    jc."""
    ppr: list[str] = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        ppr.append("<w:keepNext/>")
    if num is not None:
        numid, ilvl = num
        ppr.append(f'<w:numPr><w:ilvl w:val="{ilvl}"/>'
                   f'<w:numId w:val="{numid}"/></w:numPr>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if raw_ppr_extra:
        ppr.append(raw_ppr_extra)
    ppr_xml = ("<w:pPr>" + "".join(ppr) + "</w:pPr>") if ppr else ""
    return f"<w:p>{ppr_xml}{_runs_xml(content)}</w:p>"


def heading(level: int, text) -> str:
    """A heading paragraph; level 1/2/3 -> P_H1/H2/H3."""
    return paragraph(text, style=_HEADING_STYLE[level])


def caption(text) -> str:
    return paragraph(text, style=P_CAPTION)


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------

def bullet(text, *, level: int = 0) -> str:
    return paragraph(text, style=P_LIST, num=(NUMID_BULLET, level))


def bullets(items, *, level: int = 0) -> list[str]:
    return [bullet(it, level=level) for it in items]


def numbered(items, *, level: int = 0) -> list[str]:
    return [paragraph(it, style=P_LIST, num=(NUMID_NUMBERED, level)) for it in items]


def outline_item(text, *, level: int = 0) -> str:
    return paragraph(text, style=P_LIST, num=(NUMID_OUTLINE, level))


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def bookmark_start(name: str, bid: int) -> str:
    return f'<w:bookmarkStart w:id="{bid}" w:name="{xml_attr(name)}"/>'


def bookmark_end(bid: int) -> str:
    return f'<w:bookmarkEnd w:id="{bid}"/>'


# ---------------------------------------------------------------------------
# Tables (rule-table default posture)
# ---------------------------------------------------------------------------

def _cell_blocks(content) -> str:
    """A <w:tc> needs >=1 <w:p>. Normalize text/blocks; empty -> a single
    empty paragraph."""
    if content is None or content == "":
        return "<w:p/>"
    if isinstance(content, str):
        s = content.lstrip()
        return content if s.startswith(("<w:p", "<w:tbl")) else paragraph(content)
    blocks = []
    for c in content:
        s = c.lstrip() if isinstance(c, str) else ""
        blocks.append(c if s.startswith(("<w:p", "<w:tbl")) else paragraph(c))
    return "".join(blocks) if blocks else "<w:p/>"


def _tc_borders_xml(borders) -> str:
    """Render <w:tcBorders> from a dict. `borders` is {"all": SIDE} to set all four
    edges, and/or per-side keys "top"/"left"/"bottom"/"right" -> SIDE. A SIDE spec
    is {"val": "single", "sz": 4, "color": "auto"} ("size" is accepted for "sz").
    Side order is locked: top, left, bottom, right."""
    if not borders:
        return ""
    spec = dict(borders)
    if "all" in spec:
        allspec = spec.pop("all")
        for s in ("top", "left", "bottom", "right"):
            spec.setdefault(s, allspec)
    bits = []
    for s in ("top", "left", "bottom", "right"):
        if s in spec:
            b = spec[s] or {}
            val = b.get("val", "single")
            sz = b.get("sz", b.get("size", 4))
            color = b.get("color", "auto")
            bits.append(f'<w:{s} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>')
    return f"<w:tcBorders>{''.join(bits)}</w:tcBorders>" if bits else ""


def tcell(content="", *, width_twips: int | None = None, fill: str | None = None,
          vmerge: str | None = None, grid_span: int = 1, borders=None,
          v_align: str | None = None) -> str:
    """One table cell. `vmerge` is "restart" to begin a vertical merge or
    "continue" to extend it; `grid_span` makes the cell span N grid columns;
    `borders` paints per-cell rules (see _tc_borders_xml); `v_align` is
    "top"/"center"/"bottom". tcPr child order is locked: tcW, gridSpan, vMerge,
    tcBorders, shd, vAlign."""
    tcpr: list[str] = []
    if width_twips is not None:
        tcpr.append(f'<w:tcW w:w="{width_twips}" w:type="dxa"/>')
    else:
        tcpr.append('<w:tcW w:w="0" w:type="auto"/>')
    if grid_span and grid_span > 1:
        tcpr.append(f'<w:gridSpan w:val="{grid_span}"/>')
    if vmerge:
        tcpr.append(f'<w:vMerge w:val="{vmerge}"/>')
    tcpr.append(_tc_borders_xml(borders))
    if fill:
        tcpr.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>')
    if v_align:
        tcpr.append(f'<w:vAlign w:val="{v_align}"/>')
    return f"<w:tc><w:tcPr>{''.join(tcpr)}</w:tcPr>{_cell_blocks(content)}</w:tc>"


def trow(cells, *, header: bool = False) -> str:
    """One table row. Items already built by tcell() pass through; anything else
    is wrapped as a cell. `header=True` marks the row to repeat on page breaks."""
    tcs = []
    for c in cells:
        tcs.append(c if (isinstance(c, str) and c.lstrip().startswith("<w:tc"))
                   else tcell(c))
    trpr = "<w:trPr><w:tblHeader/></w:trPr>" if header else ""
    return f"<w:tr>{trpr}{''.join(tcs)}</w:tr>"


def _even_grid(n_cols: int, total_twips: int, col_widths_twips):
    if col_widths_twips:
        return list(col_widths_twips)
    if n_cols <= 0:
        return []
    base = total_twips // n_cols
    widths = [base] * n_cols
    widths[-1] += total_twips - base * n_cols          # remainder on the last col
    return widths


# Logical grid-column counting (gridSpan-aware). Assumes non-nested rows: a cell
# holding a nested <w:tbl> would confuse the non-greedy cell regex below.
_TC_RE = re.compile(r"<w:tc\b.*?</w:tc>", re.S)
_GRIDSPAN_RE = re.compile(r'<w:gridSpan\s+w:val="(\d+)"')


def _row_grid_cols(row_xml: str) -> int:
    n = 0
    for tc_xml in _TC_RE.findall(row_xml):
        m = _GRIDSPAN_RE.search(tc_xml)
        n += int(m.group(1)) if m else 1
    return n


def _table_grid_cols(rows) -> int:
    """The grid column count = the widest row's logical column total (so a row that
    opens with a spanning cell can't undercount the <w:tblGrid>)."""
    return max((_row_grid_cols(r) for r in rows), default=0)


def table(rows, *, style: str = T_RULE, col_widths_twips=None,
          width_pct: int = 100) -> str:
    """The low-level table engine. `rows` are trow() strings. `style` is a table
    style ID; the firstRow conditional (bold/dark header) applies via tblLook. The
    grid is sized from the widest row's logical column count (honoring gridSpan)."""
    rows = list(rows)
    n_cols = _table_grid_cols(rows)
    if col_widths_twips is not None:
        widths = list(col_widths_twips)
        if len(widths) < n_cols:
            raise ValueError(
                f"col_widths_twips has {len(widths)} columns but the rows need at "
                f"least {n_cols} logical columns after gridSpan.")
    else:
        widths = _even_grid(n_cols, _DEFAULT_TABLE_TWIPS, None)
    tblpr = [f'<w:tblStyle w:val="{style}"/>']
    if width_pct is not None:
        tblpr.append(f'<w:tblW w:w="{int(width_pct * 50)}" w:type="pct"/>')
    else:
        tblpr.append('<w:tblW w:w="0" w:type="auto"/>')
    tblpr.append('<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
                 'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>')
    grid = ("<w:tblGrid>"
            + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
            + "</w:tblGrid>") if widths else ""
    return (f"<w:tbl><w:tblPr>{''.join(tblpr)}</w:tblPr>{grid}"
            + "".join(rows) + "</w:tbl>")


def table_block(headers, data, *, style: str = T_RULE, dark_header: bool = False,
                col_widths_twips=None, caption_text: str | None = None) -> list[str]:
    """The house "rule table" convenience: optional caption + a header row + body
    rows. Returns a list of block strings (caption paragraph, then the table)."""
    out: list[str] = []
    if caption_text:
        out.append(caption(caption_text))
    tstyle = T_DARK_HEADER if dark_header else style
    rows = [trow(headers, header=True)]
    rows.extend(trow(r) for r in data)
    out.append(table(rows, style=tstyle, col_widths_twips=col_widths_twips))
    return out


# ---------------------------------------------------------------------------
# Document wrapper
# ---------------------------------------------------------------------------

def document(body_xml: str, *, sect_pr: str = "") -> str:
    """Wrap concatenated block XML in <w:document><w:body>. `sect_pr` is the
    final, body-level <w:sectPr> and must be the LAST child of <w:body> - the
    packager passes it; authors never place it."""
    return (XML_DECL
            + f"<w:document {NS_DOCUMENT}><w:body>"
            + body_xml + sect_pr
            + "</w:body></w:document>")
