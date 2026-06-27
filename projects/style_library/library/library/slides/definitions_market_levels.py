"""definitions_market_levels — Navy market-sizing deck (20251120), source slide 16.

EXHIBIT — "Definitions | Sizing breaks the market down into five levels": a
left-side nested-funnel diagram paired with a right-side definitions table. The
funnel is five concentric circles (largest → smallest, BLUE_1 → BLUE_5) keyed by
five level tags that overlay them top-to-bottom: Total Funding · TAM · SAM ·
Company TCV · Company ACV — each successive level a narrower slice of the one
above. The table (right) restates the same five levels in a Level / Definition
two-column layout, e.g. Total Funding = "All appropriations for relevant
platforms, regardless of mission" down to Company ACV = "Portion of TCV exercised
through Growth and Programs action".

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • _LAYER_SHAPES .. the 5 nested background layers (prst="ellipse"), drawn
                       largest-first so each smaller level sits on top → loop;
                       converter named them the generic "LegendSwatch"
  • chrome ........... breadcrumb() (Market Sizing · Navy (Surface incl. MDA))
  • title ............ RAW-verbatim title placeholder (no explicit xfrm); see Residue
  • table ............ Level / Definition definitions table (low-level
                       table()/trow()/tcell()/tcell_rich(); merges via borders)
  • Total Funding / TAM tags . Rectangle 27/28 = the top two level tags (black text)
  • _LAYER_LABELS ... the labels over the lower three layers (SAM / Company TCV / Company ACV,
                       white text on BLUE_3/4/5) that overlay the funnel → loop
  • logo ............. picture() top-right (IMAGES rId2, image8_3071a231.jpeg)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=2, table=1, picture=1, chrome_builders=1,
clusters=2 (covering 8 shapes), raw_verbatim=1, dropped=1 (think-cell OLE frame).
Residue: the title is a RAW-verbatim <p:sp> string (layout placeholder, no explicit
xfrm) — kept byte-for-byte rather than rebuilt through title_placeholder().
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, picture, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def edge(color, w=12700):
    """One cell-border edge (default 1pt rule)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass **PAD for the source's 60960 padding; omit for the 45720 default."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich counterpart of cell(); keep the tpara()/trun() paras as-is."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_LEVEL_LBL_X, _LEVEL_LBL_W, _LEVEL_LBL_H = IN(2.352), IN(1.949), IN(0.386)  # level-tag box [x3]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the five nested background layers, largest to smallest (Total Funding ->
#   Company ACV), forming the market-levels funnel.
_LAYER_SHAPES = [    # (x, y, cx, cy, fill) x5 — nested background layers, largest→smallest (Total Funding→Company ACV)
    (0.477, 1.307, 5.7, 5.7, BLUE_1),   # E2E9EF pale blue
    (0.927, 2.207, 4.8, 4.8, BLUE_2),   # B6C8D8 light blue
    (1.377, 3.107, 3.9, 3.9, BLUE_3),   # 6E91B1 blue
    (1.777, 4.007, 3.1, 3, BLUE_4),   # 3D5972 dark blue
    (2.277, 4.907, 2.1, 2.1, BLUE_5),   # 263746 navy
]

# local_meaning: the labels over the lower three funnel layers (the market-level tags).
_LAYER_LABELS = [    # (y, fill, label) x3 — labels over the lower three layers overlaying the funnel
    (3.457, BLUE_3, "SAM"),   # 6E91B1 blue
    (4.45, BLUE_4, "Company TCV"),   # 3D5972 dark blue
    (5.8, BLUE_5, "Company ACV"),   # 263746 navy
]

# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── layered diagram: 5 nested background shapes, largest first so each level sits on top ──
    for _x, _y, _cx, _cy, _fill in _LAYER_SHAPES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="202223", line_width=3175, prst="ellipse"))
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Title 3\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" /><a:lstStyle /><a:p><a:pPr marL=\"0\" /><a:r><a:rPr lang=\"en-US\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:rPr><a:t>Definitions | Sizing breaks the market down into five levels </a:t></a:r></a:p></p:txBody></p:sp>")
    # ── definitions table — Level / Definition ──
    # col_widths and trow(h=...) set column geometry / row minima. The repeated
    # 60,960-EMU cell insets form a row/column padding convention; anchor is
    # vertical alignment and tpara align/mar_l/indent controls text margins.
    # palette — text: 000000 black; rules: 162029 dark navy (section dividers); cell fills: none.
    out.append(table(n(), "Table 13", IN(6.577), IN(1.408), IN(6.257), IN(5.711), col_widths=[IN(1.749), IN(4.509)], rows=[
        trow([
            cell("Level", size=PT(14), bold=True, anchor="b", **PAD, B=edge(DK)),
            cell("Definition", size=PT(14), bold=True, anchor="b", **PAD, B=edge(DK)),
        ], h=IN(0.359)),
        trow([
            cell("Total Funding", size=PT(14), **PAD, T=edge(DK), B=edge(DK, 6350)),
            rcell([tpara([trun("All appropriations for relevant platforms, ", size=PT(14), color=BLACK, font=FONT), trun("regardless of mission", size=PT(14), color=BLACK, font=FONT)])], **PAD, T=edge(DK), B=edge(DK, 6350)),
        ], h=IN(0.956)),
        trow([
            rcell([tpara([trun("Total Addressable Market (TAM)", size=PT(14), color=BLACK, font=FONT), tbreak(), tbreak()])], **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
            rcell([tpara([trun("Funding for missions that ", size=PT(14), color=BLACK, font=FONT), trun("could", size=PT(14), color=BLACK, font=FONT), trun(" ", size=PT(14), color=BLACK, font=FONT), trun("be performed by unmanned platforms", size=PT(14), color=BLACK, font=FONT), tbreak(), tbreak(), trun("Portion of Total Funding for platforms ", size=PT(14), color=BLACK, font=FONT), trun("allocated to specific missions", size=PT(14), color=BLACK, font=FONT)])], **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
        ], h=IN(1.272)),
        trow([
            rcell([tpara([trun("Serviceable Addressable Market (SAM)", size=PT(14), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
            rcell([tpara([trun("Funding for missions ", size=PT(14), color=BLACK, font=FONT), trun("performed", size=PT(14), color=BLACK, font=FONT), trun(" ", size=PT(14), color=BLACK, font=FONT), trun("by unmanned platforms (i.e., adoption)", size=PT(14), color=BLACK, font=FONT), tbreak()]), tpara([trun("Portion of TAM that USVs can likely ", size=PT(14), color=BLACK, font=FONT), trun("penetrate", size=PT(14), color=BLACK, font=FONT)])], **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
        ], h=IN(1.044)),
        trow([
            cell("Company TCV", size=PT(14), **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
            rcell([tpara([trun("Funding for ", size=PT(14), color=BLACK, font=FONT), trun("Saronic", size=PT(14), color=BLACK, font=FONT), trun(" ", size=PT(14), color=BLACK, font=FONT), trun("unmanned platforms (i.e., market share)", size=PT(14), color=BLACK, font=FONT)]), tpara([]), tpara([trun("Share of SAM that Saronic can likely ", size=PT(14), color=BLACK, font=FONT), trun("capture", size=PT(14), color=BLACK, font=FONT)])], **PAD, T=edge(DK, 6350), B=edge(DK, 6350)),
        ], h=IN(0.956)),
        trow([
            cell("Company ACV", size=PT(14), **PAD, T=edge(DK, 6350)),
            cell("Portion of TCV exercised through Growth and Programs action", size=PT(14), **PAD, T=edge(DK, 6350)),
        ], h=IN(0.956)),
    ]))
    # ── level tags overlaying the funnel — top two (black text); the lower three loop below ──
    out.append(text_box(n(), "Rectangle 27", IN(2.352), IN(1.564), IN(1.949), IN(0.386), [paragraph([run("Total Funding", bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_1, line_color="none", anchor="ctr"))   # E2E9EF pale blue
    out.append(text_box(n(), "Rectangle 28", IN(2.352), IN(2.464), IN(1.949), IN(0.386), [paragraph([run("TAM", bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_2, line_color="none", anchor="ctr"))   # B6C8D8 light blue
    for _y, _fill, _t in _LAYER_LABELS:
        out.append(text_box(n(), "Label", _LEVEL_LBL_X, IN(_y), _LEVEL_LBL_W, _LEVEL_LBL_H, [paragraph([run(_t, bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # ── logo (top-right; <p:pic> bytes copied into slides/images/, wired via IMAGES) ──
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
