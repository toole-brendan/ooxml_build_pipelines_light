"""docx_core.wireframes - the wireframe / diagram toolkit (three layers).

Lets an author sketch logic and layout inside a Word document. Three layers, in
increasing power and cost (the build never lints or scores - these are pure
builders, like primitives):

  Layer A  ascii_block()         monospace ASCII diagrams - the fastest, most
                                 reliable way to sketch process maps and logic.
  Layer B  wire_table/wire_cell  Word tables used as a layout grid - the default
                                 for stable, editable boxes/lanes/matrices.
  Layer C  shape_box/shape_line/ free-floating DrawingML vector shapes + canvas()
           shape_label/canvas    for polished, free-positioned boxes and arrows.

Guidance (also in doc_guide.md): reach for ASCII first, table-grid for stable
editable diagrams, DrawingML only when the page needs polished free positioning.

To wireframe a real pptx slide, compose those layers with slide_canvas() (a
canvas sized to the deck's 16:9 proportion) and slide_frame() (the slide region
plus a layout/object annotation block), and use the PAGE_SLIDE_16x9_TALL page
setup. See doc_guide.md (Slide mocks) for the convention.

Layer C emits Word DrawingML. A shape is an inline (or anchored) <w:drawing>
wrapped in mc:AlternateContent / mc:Choice Requires="wps" with a minimal VML
mc:Fallback (what real Word writes). Child-element order is load-bearing - Word
"repairs" a file whose drawing children are out of order - so the order is fixed
here once. canvas() groups several shapes with an identity child coordinate
system (chOff=0,0, chExt=w,h), so a child's (x, y, w, h) inches map 1:1 into the
group box. Geometry is EMU (docx_core.units); shape text is real <w:p> built by
primitives, inside wps:txbx / w:txbxContent.

Import direction: ooxml / units / style / style_ids / primitives <- wireframes.
"""
from __future__ import annotations

from dataclasses import dataclass

from docx_core.ooxml import NS_WPS, NS_WPG
from docx_core.units import emu_from_in, emu_from_pt
from docx_core.style import MONO, BLACK, WHITE, hp, CODE_PT, CODE_SMALL_PT
from docx_core.style_ids import (
    P_CODE, P_CODE_SMALL, P_COMPACT_BODY, P_FIELD_LABEL, T_WIREFRAME,
)
from docx_core.primitives import (
    paragraph, run, bullets, table, trow, tcell, xml_attr,
)


# ---------------------------------------------------------------------------
# Unique-id allocation (wp:docPr id / wps:cNvPr id must be unique per document)
# ---------------------------------------------------------------------------

_ID = [0]
_Z = [251658240]            # base relativeHeight for anchored shapes


def _next_id() -> int:
    _ID[0] += 1
    return _ID[0]


def _next_z() -> int:
    _Z[0] += 1
    return _Z[0]


# ---------------------------------------------------------------------------
# Layer A - ASCII wireframes
# ---------------------------------------------------------------------------

def ascii_block(text: str, *, small: bool = False) -> str:
    """A monospace block: one fixed-width line per source line, white space
    preserved. Ideal for early logic sketches, process maps, source->output maps.
    `small=True` uses the denser P_CODE_SMALL style."""
    lines = str(text).rstrip("\n").split("\n")
    runs: list[str] = []
    for i, line in enumerate(lines):
        if i:
            runs.append("<w:r><w:br/></w:r>")
        runs.append(run(line, font=MONO, space_preserve=True))
    return paragraph(runs, style=(P_CODE_SMALL if small else P_CODE))


# ---------------------------------------------------------------------------
# Layer B - table-grid wireframes (Word tables as a stable layout engine)
# ---------------------------------------------------------------------------

_WIRE_BORDER = {"all": {"color": BLACK, "sz": 8}}


def wire_cell(text="", *, fill: str | None = None, grid_span: int = 1,
              bold: bool = False, align: str = "center",
              text_color: str | None = None) -> str:
    """One wireframe cell: bordered box, centered by default, optional fill."""
    body = paragraph([run(text, bold=bold, color=text_color)],
                     style=P_COMPACT_BODY, align=align)
    return tcell(body, fill=fill, grid_span=grid_span, borders=_WIRE_BORDER,
                 v_align="center")


def wire_table(rows, *, col_widths_twips, width_pct: int = 100) -> str:
    """A table-grid wireframe. `rows` is a list of rows; each row is a list of
    wire_cell() strings (or plain text, wrapped as plain cells). Pass
    col_widths_twips to fix the column geometry (1 in = 1440 twips)."""
    trows = [trow(r) for r in rows]
    return table(trows, style=T_WIREFRAME, col_widths_twips=list(col_widths_twips),
                 width_pct=width_pct)


# ---------------------------------------------------------------------------
# Layer C - DrawingML shapes (low-level XML builders)
# ---------------------------------------------------------------------------

def _fill_xml(fill) -> str:
    """None -> omit (lines); "none" -> <a:noFill/>; hex -> solid fill."""
    if fill is None:
        return ""
    if fill == "none":
        return "<a:noFill/>"
    return f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'


def _ln_xml(line, line_emu, *, dashed=False, head=False, arrow=False) -> str:
    """None -> omit; "none" -> a line with no paint; hex -> stroke (+optional
    dash / arrow ends). a:ln child order: fill, prstDash, headEnd, tailEnd."""
    if line is None:
        return ""
    if line == "none":
        return "<a:ln><a:noFill/></a:ln>"
    bits = [f'<a:solidFill><a:srgbClr val="{line}"/></a:solidFill>']
    if dashed:
        bits.append('<a:prstDash val="dash"/>')
    if head:
        bits.append('<a:headEnd type="triangle" w="med" len="med"/>')
    if arrow:
        bits.append('<a:tailEnd type="triangle" w="med" len="med"/>')
    return f'<a:ln w="{line_emu}">{"".join(bits)}</a:ln>'


def _txbx_xml(text, *, color=BLACK, size_pt=11.0, align="center") -> str:
    """A wps:txbx holding real <w:p> paragraphs (Word, not PowerPoint a:p)."""
    paras = [
        paragraph([run(line, color=color, size_hp=hp(size_pt))],
                  style=P_COMPACT_BODY, align=align)
        for line in str(text).split("\n")
    ]
    return f'<wps:txbx><w:txbxContent>{"".join(paras)}</w:txbxContent></wps:txbx>'


def _wsp(off_x, off_y, cx, cy, *, prst="rect", fill=WHITE, line=BLACK,
         line_emu=12700, flip="", txbx_xml="", with_text=False, is_line=False,
         dashed=False, head=False, arrow=False,
         cnv_id=None, cnv_name=None) -> str:
    """One shape (<wps:wsp>). Child order: cNvPr?, cNvSpPr, spPr, txbx?, bodyPr.
    spPr order: xfrm(off->ext), prstGeom, fill, ln. cnv_id/cnv_name emit a
    wps:cNvPr - used for GROUP CHILDREN (a top-level shape's id lives on
    wp:docPr instead)."""
    nv = (f'<wps:cNvPr id="{cnv_id}" name="{xml_attr(cnv_name or "Shape")}"/>'
          if cnv_id is not None else "")
    sppr = (
        "<wps:spPr>"
        f'<a:xfrm{flip}><a:off x="{off_x}" y="{off_y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
        f'{_fill_xml(None if is_line else fill)}'
        f'{_ln_xml(line, line_emu, dashed=dashed, head=head, arrow=arrow)}'
        "</wps:spPr>"
    )
    if with_text:
        bodypr = ('<wps:bodyPr rot="0" anchor="ctr" lIns="91440" tIns="45720" '
                  'rIns="91440" bIns="45720"><a:noAutofit/></wps:bodyPr>')
    else:
        bodypr = "<wps:bodyPr/>"
    return f"<wps:wsp>{nv}<wps:cNvSpPr/>{sppr}{txbx_xml}{bodypr}</wps:wsp>"


def _graphic(uri: str, inner: str) -> str:
    return f'<a:graphic><a:graphicData uri="{uri}">{inner}</a:graphicData></a:graphic>'


def _vml_fallback(w_in: float, h_in: float, fill) -> str:
    """A crude VML rectangle so non-wps readers still see a box. Real Word writes
    a fallback; it only renders where the wps Choice can't."""
    w_pt = round(w_in * 72, 1)
    h_pt = round(h_in * 72, 1)
    paint = f' fillcolor="#{fill}"' if (fill and fill != "none") else ' filled="f"'
    return ('<mc:Fallback><w:pict>'
            '<v:rect xmlns:v="urn:schemas-microsoft-com:vml" '
            f'style="width:{w_pt}pt;height:{h_pt}pt"{paint} stroked="t"/>'
            '</w:pict></mc:Fallback>')


def _wrap_inline(cx, cy, sid, name, graphic, fallback_xml) -> str:
    """A <w:p> holding an inline drawing. wp:inline child order: extent,
    effectExtent, docPr, cNvGraphicFramePr, graphic."""
    alt = (
        '<mc:AlternateContent><mc:Choice Requires="wps">'
        '<w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{sid}" name="{xml_attr(name)}"/>'
        '<wp:cNvGraphicFramePr/>'
        f'{graphic}'
        '</wp:inline>'
        '</w:drawing>'
        '</mc:Choice>'
        f'{fallback_xml}'
        '</mc:AlternateContent>'
    )
    return f"<w:p><w:r>{alt}</w:r></w:p>"


def _wrap_anchor(cx, cy, x, y, sid, name, graphic, fallback_xml, z) -> str:
    """A <w:p> holding an anchored (free-positioned) drawing. wp:anchor child
    order: simplePos, positionH, positionV, extent, effectExtent, wrap, docPr,
    cNvGraphicFramePr, graphic."""
    anchor = (
        '<wp:anchor distT="0" distB="0" distL="114300" distR="114300" '
        f'simplePos="0" relativeHeight="{z}" behindDoc="0" locked="0" '
        'layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="column">'
        f'<wp:posOffset>{x}</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="paragraph">'
        f'<wp:posOffset>{y}</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:wrapNone/>'
        f'<wp:docPr id="{sid}" name="{xml_attr(name)}"/>'
        '<wp:cNvGraphicFramePr/>'
        f'{graphic}'
        '</wp:anchor>'
    )
    alt = (
        '<mc:AlternateContent><mc:Choice Requires="wps">'
        f'<w:drawing>{anchor}</w:drawing>'
        '</mc:Choice>'
        f'{fallback_xml}'
        '</mc:AlternateContent>'
    )
    return f"<w:p><w:r>{alt}</w:r></w:p>"


# ---------------------------------------------------------------------------
# Layer C - public shape builders
# ---------------------------------------------------------------------------

def shape_box(text="", *, w_in: float, h_in: float,
              x_in: float | None = None, y_in: float | None = None,
              fill: str = WHITE, line: str = BLACK, line_pt: float = 1.0,
              text_color: str = BLACK, text_size_pt: float = 11.0,
              align: str = "center", name: str = "Box",
              fallback: bool = True) -> str:
    """A rectangle, optionally with centered text. Inline when x_in/y_in are
    None; anchored (free X/Y from the column/paragraph) when both are given."""
    cx, cy = emu_from_in(w_in), emu_from_in(h_in)
    with_text = bool(str(text).strip())
    txbx = (_txbx_xml(text, color=text_color, size_pt=text_size_pt, align=align)
            if with_text else "")
    wsp = _wsp(0, 0, cx, cy, prst="rect", fill=fill, line=line,
               line_emu=emu_from_pt(line_pt), txbx_xml=txbx, with_text=with_text)
    graphic = _graphic(NS_WPS, wsp)
    fb = _vml_fallback(w_in, h_in, fill) if fallback else ""
    sid = _next_id()
    if x_in is None or y_in is None:
        return _wrap_inline(cx, cy, sid, name, graphic, fb)
    return _wrap_anchor(cx, cy, emu_from_in(x_in), emu_from_in(y_in),
                        sid, name, graphic, fb, _next_z())


def shape_label(text, *, w_in: float, h_in: float,
                x_in: float | None = None, y_in: float | None = None,
                color: str = BLACK, size_pt: float = 11.0,
                align: str = "center", name: str = "Label",
                fallback: bool = True) -> str:
    """A text-only shape (no fill, no border) - a free-positioned label."""
    return shape_box(text, w_in=w_in, h_in=h_in, x_in=x_in, y_in=y_in,
                     fill="none", line="none", text_color=color,
                     text_size_pt=size_pt, align=align, name=name, fallback=fallback)


def shape_line(*, dx_in: float, dy_in: float, color: str = BLACK,
               line_pt: float = 1.0, dashed: bool = False, arrow: bool = True,
               head: bool = False, name: str = "Line",
               fallback: bool = True) -> str:
    """A straight inline line/arrow drawn across a |dx_in| x |dy_in| box; negative
    components flip direction (deck_core rule). For connectors between specific
    boxes, prefer canvas() with CanvasLine (absolute coordinates)."""
    cx, cy = emu_from_in(abs(dx_in)), emu_from_in(abs(dy_in))
    flip = (' flipH="1"' if dx_in < 0 else "") + (' flipV="1"' if dy_in < 0 else "")
    wsp = _wsp(0, 0, cx, cy, prst="line", fill=None, line=color,
               line_emu=emu_from_pt(line_pt), flip=flip, is_line=True,
               dashed=dashed, head=head, arrow=arrow)
    graphic = _graphic(NS_WPS, wsp)
    fb = _vml_fallback(abs(dx_in) or 0.05, abs(dy_in) or 0.05, "none") if fallback else ""
    return _wrap_inline(cx, cy, _next_id(), name, graphic, fb)


# ---------------------------------------------------------------------------
# Layer C - canvas (a group of shapes on one logical drawing)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CanvasBox:
    """A box positioned in the canvas's inch coordinate system (origin top-left)."""
    x_in: float
    y_in: float
    w_in: float
    h_in: float
    text: str = ""
    fill: str = WHITE
    line: str = BLACK
    line_pt: float = 1.0
    text_color: str = BLACK
    text_size_pt: float = 10.0
    align: str = "center"
    name: str = "Box"


@dataclass(frozen=True)
class CanvasLine:
    """A line/arrow from (x_in, y_in) by vector (dx_in, dy_in), canvas inches."""
    x_in: float
    y_in: float
    dx_in: float
    dy_in: float
    color: str = BLACK
    line_pt: float = 1.0
    dashed: bool = False
    arrow: bool = True
    head: bool = False
    name: str = "Line"


def _canvas_child(ch) -> str:
    if isinstance(ch, CanvasBox):
        with_text = bool(str(ch.text).strip())
        txbx = (_txbx_xml(ch.text, color=ch.text_color, size_pt=ch.text_size_pt,
                          align=ch.align) if with_text else "")
        return _wsp(emu_from_in(ch.x_in), emu_from_in(ch.y_in),
                    emu_from_in(ch.w_in), emu_from_in(ch.h_in),
                    prst="rect", fill=ch.fill, line=ch.line,
                    line_emu=emu_from_pt(ch.line_pt), txbx_xml=txbx,
                    with_text=with_text, cnv_id=_next_id(), cnv_name=ch.name)
    if isinstance(ch, CanvasLine):
        ox_in, oy_in = ch.x_in, ch.y_in
        if ch.dx_in < 0:
            ox_in = ch.x_in + ch.dx_in
        if ch.dy_in < 0:
            oy_in = ch.y_in + ch.dy_in
        flip = (' flipH="1"' if ch.dx_in < 0 else "") + (' flipV="1"' if ch.dy_in < 0 else "")
        return _wsp(emu_from_in(ox_in), emu_from_in(oy_in),
                    emu_from_in(abs(ch.dx_in)), emu_from_in(abs(ch.dy_in)),
                    prst="line", fill=None, line=ch.color,
                    line_emu=emu_from_pt(ch.line_pt), flip=flip, is_line=True,
                    dashed=ch.dashed, head=ch.head, arrow=ch.arrow,
                    cnv_id=_next_id(), cnv_name=ch.name)
    raise TypeError(f"canvas children must be CanvasBox/CanvasLine, "
                    f"got {type(ch).__name__!r}")


def canvas(children, *, w_in: float, h_in: float,
           x_in: float | None = None, y_in: float | None = None,
           name: str = "Canvas", fallback: bool = True) -> str:
    """Group CanvasBox / CanvasLine children into ONE drawing (a wpg:wgp group
    with an identity child coordinate system, so child inches map 1:1 into the
    w_in x h_in box). Inline when x_in/y_in are None; anchored when both given.
    Returns one <w:p> block - the recommended primitive for box-and-arrow
    diagrams."""
    cx, cy = emu_from_in(w_in), emu_from_in(h_in)
    parts = "".join(_canvas_child(ch) for ch in children)
    grp = (
        "<wpg:wgp>"
        "<wpg:cNvGrpSpPr/>"
        "<wpg:grpSpPr>"
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/>'
        f'<a:chOff x="0" y="0"/><a:chExt cx="{cx}" cy="{cy}"/></a:xfrm>'
        "</wpg:grpSpPr>"
        f"{parts}"
        "</wpg:wgp>"
    )
    graphic = _graphic(NS_WPG, grp)
    fb = _vml_fallback(w_in, h_in, "none") if fallback else ""
    sid = _next_id()
    if x_in is None or y_in is None:
        return _wrap_inline(cx, cy, sid, name, graphic, fb)
    return _wrap_anchor(cx, cy, emu_from_in(x_in), emu_from_in(y_in),
                        sid, name, graphic, fb, _next_z())


# ---------------------------------------------------------------------------
# Slide mock - wireframe a real pptx slide (16:9), with a layout/object footer
# ---------------------------------------------------------------------------

# Height multiplier per slide aspect ratio (h_in = w_in * mult). The deck is
# 16:9 (deck_core SLIDE_W/SLIDE_H = 13.333 x 7.5 in); 4:3 is parameterized for
# reuse but the live deck never uses it.
_SLIDE_RATIOS = {"16:9": 9 / 16, "4:3": 3 / 4}


def slide_canvas(children, *, ratio: str = "16:9", w_in: float = 12.5,
                 x_in: float | None = None, y_in: float | None = None,
                 name: str = "Slide", fallback: bool = True) -> str:
    """A canvas() sized to a slide aspect ratio. Derives h_in from w_in so the
    region stays proportion-correct (16:9 by default), with child inches mapping
    1:1 into the w_in x h_in box - draw the slide's title/exhibits/commentary as
    CanvasBox / CanvasLine children. w_in defaults to the usable width of a
    PAGE_SLIDE_16x9_TALL page; pass the page's usable width to fill it."""
    try:
        mult = _SLIDE_RATIOS[ratio]
    except KeyError:
        raise ValueError(f"ratio must be one of {sorted(_SLIDE_RATIOS)}, "
                         f"got {ratio!r}")
    return canvas(children, w_in=w_in, h_in=round(w_in * mult, 3),
                  x_in=x_in, y_in=y_in, name=name, fallback=fallback)


def slide_frame(slide, *, layout, objects, layout_label: str = "Layout",
                objects_label: str = "Objects") -> list[str]:
    """Compose a slide-mock page body: the slide wireframe on top, then a
    subordinate annotation block - the layout/grid first, then the object
    inventory - as concise bullets. `slide` is one wireframe block (slide_canvas /
    wire_table / ascii_block) or a list of blocks; `layout` and `objects` are
    lists of strings. Returns a list of block XML strings - splice into a
    PageModuleSpec body with `*` and pair with PAGE_SLIDE_16x9_TALL so the slide
    keeps the deck's 13.333in width and the annotation rides below on one page.

    The annotation is descriptive (what regions exist, what sits in each), not a
    re-transcription of the slide copy - the slide region already carries every
    planned word (see doc_guide.md, Slide mocks)."""
    out = list(slide) if isinstance(slide, (list, tuple)) else [slide]
    out.append(paragraph(layout_label, style=P_FIELD_LABEL))
    out.extend(bullets(layout))
    out.append(paragraph(objects_label, style=P_FIELD_LABEL))
    out.extend(bullets(objects))
    return out
