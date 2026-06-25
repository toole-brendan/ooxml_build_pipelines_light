#!/usr/bin/env python3
"""convert_slide.py - convert one source-.pptx slide into an idiomatic deck_core module.

Reads a single slide from a source PowerPoint file and emits a Python slide module
that rebuilds it through deck_core primitives. The aim is a module that (a) renders
faithfully and (b) reads like a hand-authored deck_core slide, so an AI agent can
study it as a worked example.

Pipeline: parse every shape into a record -> detect roles/structure -> emit.

  - native <c:chart> graphicFrame -> graphic_frame(rId="rId2") + the chart part and
    its .xlsb copied into _src/. Its data caches are read into a _DATA dict literal and
    CHARTS = [styled_chart(_CHART_TPL, _DATA, _XLSB)]: the source part is the exact
    STYLE template (look byte-identical), the values live in Python, and "Edit Data"
    still works. Style-dense charts a factory can't rebuild (bar+line combos, pattern
    fills) come through faithfully; the chart is NEVER rebuilt by a factory. Falls back
    to editable_bundled_chart when the data or .xlsb can't be recovered.
  - <p:pic> images -> picture() + an IMAGES entry; the media bytes are copied into the
    deck's slides/images/ under a content-addressed name (identical media dedupes, names
    never collide across source decks). An .emf pic over a bundled native chart is that
    chart's think-cell vector PREVIEW and is dropped; a think-cell OLE data frame ("... do
    not delete") is dropped too.
  - <a:fld> labels (think-cell) -> FROZEN to static run()s from their cached text.
  - colour: schemeClr (lumMod/lumOff/shade/tint baked) -> hex; an exact deck_core
    token match is emitted as the token. Borders inherited from a <p:style><a:lnRef>
    (think-cell's callouts) are resolved too.
  - STANDARD CHROME (breadcrumb / title / Preliminary chip / sources) is recognised by
    placeholder + text + position and emitted via the house builders -- but only when
    the source sits within tolerance of the house position; otherwise it's kept as a
    verbatim shape so nothing moves.
  - STRUCTURE: shapes that share a style (>=3 of them) are collapsed into a module-level
    data table + a loop (the year axis, on-bar values, legend swatches/labels, callouts),
    instead of N near-identical calls.
  - anything exotic (custGeom, gradient/pattern/picture fill, a placeholder with no
    geometry) -> emitted as a RAW verbatim OOXML string (cruft stripped, id renumbered).

Usage:
    python convert_slide.py SOURCE.pptx N \\
        --out  ../deck_<name>/slides/<name>.py \\
        --src-dir ../deck_<name>/slides/_src \\
        --module-name <name> [--layout slideLayout4]

Stdlib only, so it can be copied next to any deck pipeline.
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

for _pfx, _uri in (("a", A), ("p", P), ("c", C), ("r", R)):
    ET.register_namespace(_pfx, _uri)


def q(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


# hex (upper) -> deck_core.style token name. Exact matches only (no nearest-snap, which
# would shift a brand colour). Brand accents stay literal hex on purpose.
TOKENS = {
    "000000": "BLACK", "FFFFFF": "WHITE", "162029": "DK",
    "44505C": "BREADCRUMB", "FFFFCC": "PRELIM",
    "E2E9EF": "BLUE_1", "B6C8D8": "BLUE_2", "6E91B1": "BLUE_3",
    "3D5972": "BLUE_4", "263746": "BLUE_5",
    "F2F2F2": "GRAY_1", "D9D9D9": "GRAY_2", "BFBFBF": "GRAY_3",
    "7F7F7F": "GRAY_4", "646464": "GRAY_5",
}

# House chrome positions (deck_core.style) + tolerance, for chrome detection. A
# detected chrome shape becomes a builder only when its source position is within
# TOL of the house position; otherwise it stays a verbatim shape so nothing moves.
LEFT_MARGIN = 453079
HOUSE_POS = {
    "breadcrumb": (LEFT_MARGIN, 263452),
    "title": (LEFT_MARGIN, 554500),
    "prelim": (10267829, 111556),
    "sources": (LEFT_MARGIN, 5930000),
}
TOL = 91440   # 0.1 in

# fields a same-style cluster is allowed to vary on, in tuple order
VARYING_ORDER = ["x", "y", "cx", "cy", "fill", "line_color", "text", "geom_adj"]
VAR_NAMES = {"x": "_x", "y": "_y", "cx": "_cx", "cy": "_cy", "fill": "_fill",
             "line_color": "_lc", "text": "_t", "geom_adj": "_ga"}
FIELD_LABEL = {"x": "x", "y": "y", "cx": "cx", "cy": "cy", "fill": "fill",
               "line_color": "line", "text": "label", "geom_adj": "tail"}
DIM = {"x": "X", "y": "Y", "cx": "W", "cy": "H"}   # coordinate -> anchor-name dimension
MIN_CLUSTER = 3
SHARED_ANCHOR_MIN = 4   # a coord value repeated >= this across standalone shapes is hoisted

# coordinate units in the emitted module. "inches" -> every coord becomes IN(<inches>)
# (deck_core.style.IN converts back to EMU at build); "emu" -> raw EMU ints. Inch
# values use 3 decimals: visually exact (sub-0.05 px) but not byte-exact.
_UNITS = "inches"


def _inch(emu):
    return f"{emu / 914400:.3f}".rstrip("0").rstrip(".") or "0"


def coordlit(emu):
    """Inline coordinate literal: IN(<inches>) in inch mode, else the raw EMU int."""
    return f"IN({_inch(emu)})" if (_UNITS == "inches" and isinstance(emu, int)) else str(emu)


def coordfloat(emu):
    """Bare coordinate value for a data-table cell (the loop wraps it in IN())."""
    return _inch(emu) if (_UNITS == "inches" and isinstance(emu, int)) else str(emu)


def sizelit(sz):
    """Font size literal: PT(<points>) in inch/human mode, else the raw 1/100-pt int."""
    return f"PT({sz / 100:g})" if (_UNITS == "inches" and isinstance(sz, int)) else str(sz)


# ── colour resolution ────────────────────────────────────────────────────────
def build_theme_map(z: zipfile.ZipFile) -> dict:
    root = ET.fromstring(z.read("ppt/theme/theme1.xml"))
    scheme = root.find(".//" + q(A, "clrScheme"))
    m: dict[str, str] = {}
    for child in scheme:
        name = child.tag.split("}")[-1]
        srgb = child.find(q(A, "srgbClr"))
        sysc = child.find(q(A, "sysClr"))
        if srgb is not None:
            m[name] = srgb.get("val", "000000").upper()
        elif sysc is not None:
            m[name] = sysc.get("lastClr", "000000").upper()
    m["tx1"], m["bg1"] = m.get("dk1", "000000"), m.get("lt1", "FFFFFF")
    m["tx2"], m["bg2"] = m.get("dk2", "000000"), m.get("lt2", "FFFFFF")
    # theme line-style list (1-based) -> width, for borders inherited via <a:lnRef idx>
    lnlst = root.find(".//" + q(A, "lnStyleLst"))
    m["__lnw__"] = {}
    if lnlst is not None:
        for idx, ln in enumerate(lnlst.findall(q(A, "ln")), 1):
            if ln.get("w"):
                m["__lnw__"][idx] = int(ln.get("w"))
    return m


def _bake_lum(hex6: str, lummod, lumoff) -> str:
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if lummod is not None:
        l *= lummod
    if lumoff is not None:
        l += lumoff
    l = max(0.0, min(1.0, l))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"


def _apply_shade_tint(hex6: str, shade, tint) -> str:
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    if shade is not None:
        r, g, b = r * shade, g * shade, b * shade
    if tint is not None:
        r = r * tint + 255 * (1 - tint)
        g = g * tint + 255 * (1 - tint)
        b = b * tint + 255 * (1 - tint)
    return f"{round(r):02X}{round(g):02X}{round(b):02X}"


def color_hex(clr, theme: dict):
    """An <a:srgbClr>/<a:schemeClr> element -> resolved 6-char hex (lum/shade/tint baked)."""
    if clr is None:
        return None
    tag = clr.tag.split("}")[-1]
    if tag == "srgbClr":
        base = clr.get("val", "000000").upper()
    elif tag == "schemeClr":
        base = theme.get(clr.get("val"), "000000")
    else:
        return None
    lm, lo = clr.find(q(A, "lumMod")), clr.find(q(A, "lumOff"))
    lummod = int(lm.get("val")) / 100000 if lm is not None else None
    lumoff = int(lo.get("val")) / 100000 if lo is not None else None
    if lummod is not None or lumoff is not None:
        base = _bake_lum(base, lummod, lumoff)
    sh, ti = clr.find(q(A, "shade")), clr.find(q(A, "tint"))
    if sh is not None or ti is not None:
        base = _apply_shade_tint(base,
                                 int(sh.get("val")) / 100000 if sh is not None else None,
                                 int(ti.get("val")) / 100000 if ti is not None else None)
    return base


def color_lit(hex6):
    """hex -> Python literal: a token name where it matches exactly, else a quoted hex."""
    if hex6 is None:
        return None
    return TOKENS.get(hex6.upper(), f'"{hex6.upper()}"')


def _solid_child(parent):
    sf = parent.find(q(A, "solidFill"))
    if sf is None:
        return None
    s = sf.find(q(A, "srgbClr"))
    return s if s is not None else sf.find(q(A, "schemeClr"))


def _lnref_color(el, theme):
    """Border colour inherited from a shape's <p:style><a:lnRef> (schemeClr/srgbClr)."""
    style = el.find(q(P, "style"))
    lnRef = style.find(q(A, "lnRef")) if style is not None else None
    if lnRef is None:
        return None
    ref = lnRef.find(q(A, "schemeClr"))
    if ref is None:
        ref = lnRef.find(q(A, "srgbClr"))
    return color_lit(color_hex(ref, theme))


def py_str(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


# ── parse: source element -> record dict ──────────────────────────────────────
def parse_run(rPr, text, theme):
    d = {"text": text or "", "size": None, "bold": False, "italic": False, "color": None}
    if rPr is not None:
        if rPr.get("sz"):
            d["size"] = int(rPr.get("sz"))
        d["bold"] = rPr.get("b") == "1"
        d["italic"] = rPr.get("i") == "1"
        d["color"] = color_lit(color_hex(_solid_child(rPr), theme))
    return d


def parse_para(p, theme):
    runs = []
    for ch in p:
        tag = ch.tag.split("}")[-1]
        if tag in ("r", "fld"):    # <a:fld> = think-cell label, frozen by reading its cache
            t = ch.find(q(A, "t"))
            runs.append(parse_run(ch.find(q(A, "rPr")), t.text if t is not None else "", theme))
        elif tag == "br":          # explicit in-paragraph line break (think-cell wraps tight labels)
            runs.append({"break": True})
    pPr = p.find(q(A, "pPr"))
    pa = {"align": None, "level": 0, "marL": None, "indent": None,
          "space_after": None, "line_spacing": None, "bullet": False,
          "end_size": None, "runs": runs}
    # <a:endParaRPr> drives an EMPTY paragraph's height. think-cell collapses
    # spacer rows/cols by giving their empty cells a tiny font (e.g. sz=100 = 1pt);
    # capture it so empty cells reproduce that height instead of the 10pt default.
    epr = p.find(q(A, "endParaRPr"))
    if epr is not None and epr.get("sz"):
        pa["end_size"] = int(epr.get("sz"))
    if pPr is not None:
        pa["align"] = pPr.get("algn")
        pa["level"] = int(pPr.get("lvl")) if pPr.get("lvl") else 0
        pa["marL"] = int(pPr.get("marL")) if pPr.get("marL") is not None else None
        pa["indent"] = int(pPr.get("indent")) if pPr.get("indent") is not None else None
        sa = pPr.find(q(A, "spcAft") + "/" + q(A, "spcPts"))
        pa["space_after"] = int(sa.get("val")) if sa is not None else None
        ls = pPr.find(q(A, "lnSpc") + "/" + q(A, "spcPct"))
        pa["line_spacing"] = int(ls.get("val")) if ls is not None else None
        pa["bullet"] = pPr.find(q(A, "buChar")) is not None
    return pa


def parse_sp(el, theme):
    spPr = el.find(q(P, "spPr"))
    nv = el.find(".//" + q(P, "cNvPr"))
    rec = {"type": "sp", "el": el, "name": nv.get("name", "Shape") if nv is not None else "Shape",
           "raw": None, "role": None}
    ph = el.find(".//" + q(P, "ph"))
    rec["ph"] = (ph.get("type"), ph.get("idx")) if ph is not None else None
    xfrm = spPr.find(q(A, "xfrm")) if spPr is not None else None
    if xfrm is None:
        rec["raw"] = "no explicit xfrm (layout placeholder)"
        return rec
    for exotic in ("gradFill", "pattFill", "blipFill"):
        if spPr.find(q(A, exotic)) is not None:
            rec["raw"] = exotic
            return rec
    if spPr.find(q(A, "custGeom")) is not None:
        rec["raw"] = "custGeom"
        return rec
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    rec["x"], rec["y"] = int(off.get("x")), int(off.get("y"))
    rec["cx"], rec["cy"] = int(ext.get("cx")), int(ext.get("cy"))
    rec["rot"] = int(xfrm.get("rot")) if xfrm.get("rot") else 0
    pg = spPr.find(q(A, "prstGeom"))
    rec["prst"] = pg.get("prst") if pg is not None else "rect"
    rec["geom_adj"] = ({gd.get("name"): gd.get("fmla") for gd in pg.findall(q(A, "avLst") + "/" + q(A, "gd"))}
                       if pg is not None else {})
    rec["fill"] = "None" if spPr.find(q(A, "noFill")) is not None \
        else (color_lit(color_hex(_solid_child(spPr), theme)) or "None")
    # border: explicit ln colour, else inherit from <p:style><a:lnRef> (think-cell callouts)
    rec["line_color"], rec["line_width"], rec["dashed"] = '"none"', None, False
    ln = spPr.find(q(A, "ln"))
    if ln is not None and ln.find(q(A, "noFill")) is None:
        lc = color_lit(color_hex(_solid_child(ln), theme))
        if lc is None:
            lc = _lnref_color(el, theme)   # <a:ln w=..> with no fill inherits colour from the style
        if lc is not None:
            rec["line_color"] = lc
            w = ln.get("w")
            rec["line_width"] = int(w) if w else None
            d = ln.find(q(A, "prstDash"))
            rec["dashed"] = d is not None and d.get("val") not in (None, "solid")
    elif ln is None:
        # No <a:ln> at all: the border (if any) comes entirely from the shape's
        # <p:style><a:lnRef idx=N> - colour from the ref, width from the theme's
        # line-style list at idx (idx 0 = no line). think-cell's Preliminary chip
        # relies on this; soffice/PowerPoint render it but a naive parse drops it.
        style = el.find(q(P, "style"))
        lnRef = style.find(q(A, "lnRef")) if style is not None else None
        if lnRef is not None and lnRef.get("idx") not in (None, "0"):
            lc = _lnref_color(el, theme)
            if lc is not None:
                rec["line_color"] = lc
                rec["line_width"] = theme.get("__lnw__", {}).get(int(lnRef.get("idx")))
    txBody = el.find(q(P, "txBody"))
    bodyPr = txBody.find(q(A, "bodyPr")) if txBody is not None else None
    rec["anchor"], rec["wrap"], rec["ins"] = "t", "square", {}
    if bodyPr is not None:
        rec["anchor"] = bodyPr.get("anchor", "t")
        rec["wrap"] = bodyPr.get("wrap", "square")
        for attr, kw in (("lIns", "l_ins"), ("tIns", "t_ins"), ("rIns", "r_ins"), ("bIns", "b_ins")):
            if bodyPr.get(attr) is not None:
                rec["ins"][kw] = int(bodyPr.get(attr))
    rec["paras"] = [parse_para(p, theme) for p in txBody.findall(q(A, "p"))] if txBody is not None else []
    return rec


def parse_cxn(el, theme):
    spPr = el.find(q(P, "spPr"))
    nv = el.find(".//" + q(P, "cNvPr"))
    rec = {"type": "cxn", "el": el, "name": nv.get("name", "Connector") if nv is not None else "Connector",
           "raw": None, "role": None}
    xfrm = spPr.find(q(A, "xfrm"))
    if xfrm is None:
        rec["raw"] = "connector w/o xfrm"
        return rec
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    rec["x"], rec["y"] = int(off.get("x")), int(off.get("y"))
    # Keep the source's positive bounding box + orientation EXPLICIT (flip/rot)
    # rather than folding flip into a signed cx/cy: the signed-vector trick shifts
    # the box, which silently mis-routes flipped/rotated elbows (rot was dropped
    # entirely, so a 90/270-deg elbow rendered unrotated and shot off-slide).
    rec["cx"], rec["cy"] = int(ext.get("cx")), int(ext.get("cy"))
    rec["flip_h"] = xfrm.get("flipH") == "1"
    rec["flip_v"] = xfrm.get("flipV") == "1"
    rec["rot"] = int(xfrm.get("rot") or 0)
    pg = spPr.find(q(A, "prstGeom"))
    rec["prst"] = pg.get("prst") if pg is not None else "line"
    rec["adj"] = {}
    av = pg.find(q(A, "avLst")) if pg is not None else None
    if av is not None:
        for gd in av.findall(q(A, "gd")):
            if (gd.get("name"), gd.get("fmla")) != ("adj1", "val 50000"):  # 50% = elbow default
                rec["adj"][gd.get("name")] = gd.get("fmla")
    rec["color"], rec["width"], rec["dashed"], rec["arrow"] = "BLACK", 12700, False, False
    ln = spPr.find(q(A, "ln"))
    if ln is not None:
        w = ln.get("w")
        rec["width"] = int(w) if w else 12700
        lc = color_lit(color_hex(_solid_child(ln), theme))
        if lc is not None:
            rec["color"] = lc
        rec["dashed"] = ln.find(q(A, "prstDash")) is not None
        rec["arrow"] = ln.find(q(A, "tailEnd")) is not None or ln.find(q(A, "headEnd")) is not None
    return rec


def parse_table(el, theme):
    """A <p:graphicFrame> wrapping an <a:tbl> -> table record. Merge-filler cells
    (hMerge/vMerge) are dropped; the engine re-synthesizes them from the anchor
    cell's grid_span/row_span. Per-cell fill / borders / insets / anchor are kept."""
    nv = el.find(".//" + q(P, "cNvPr"))
    xfrm = el.find(q(P, "xfrm"))
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    tbl = el.find(".//" + q(A, "tbl"))
    grid = tbl.find(q(A, "tblGrid"))
    cols = [int(c.get("w")) for c in grid.findall(q(A, "gridCol"))]
    rows = []
    for tr in tbl.findall(q(A, "tr")):
        cells = []
        for tc in tr.findall(q(A, "tc")):
            if tc.get("hMerge") == "1" or tc.get("vMerge") == "1":
                continue
            tcPr = tc.find(q(A, "tcPr"))
            cell = {"grid_span": int(tc.get("gridSpan") or 1),
                    "row_span": int(tc.get("rowSpan") or 1),
                    "fill": None, "anchor": "ctr", "l_ins": None, "r_ins": None,
                    "t_ins": None, "b_ins": None, "borders": {}}
            if tcPr is not None:
                if tcPr.find(q(A, "solidFill")) is not None:
                    cell["fill"] = color_lit(color_hex(_solid_child(tcPr), theme))
                cell["anchor"] = tcPr.get("anchor", "ctr")
                if tcPr.get("marL") is not None:
                    cell["l_ins"] = int(tcPr.get("marL"))
                if tcPr.get("marR") is not None:
                    cell["r_ins"] = int(tcPr.get("marR"))
                if tcPr.get("marT") is not None:
                    cell["t_ins"] = int(tcPr.get("marT"))
                if tcPr.get("marB") is not None:
                    cell["b_ins"] = int(tcPr.get("marB"))
                for side, key in (("lnL", "L"), ("lnR", "R"), ("lnT", "T"), ("lnB", "B")):
                    ln = tcPr.find(q(A, side))
                    if ln is None:
                        continue
                    if ln.find(q(A, "noFill")) is not None:
                        cell["borders"][key] = "none"
                    elif ln.find(q(A, "solidFill")) is not None:
                        cell["borders"][key] = {"color": color_hex(_solid_child(ln), theme),
                                                "width": int(ln.get("w") or 12700)}
            txBody = tc.find(q(A, "txBody"))
            cell["paras"] = [parse_para(p, theme) for p in txBody.findall(q(A, "p"))] if txBody is not None else []
            cells.append(cell)
        rows.append({"h": int(tr.get("h") or 0), "cells": cells})
    return {"type": "table", "el": el, "raw": None, "role": None,
            "name": nv.get("name", "Table") if nv is not None else "Table",
            "x": int(off.get("x")), "y": int(off.get("y")),
            "cx": int(ext.get("cx")), "cy": int(ext.get("cy")), "cols": cols, "rows": rows}


# ── render: record -> Python call string ──────────────────────────────────────
def render_run(d, text_override=None):
    if d.get("break"):
        return "line_break()"
    parts = [text_override if text_override is not None else f'"{py_str(d["text"])}"']
    if d["size"] is not None:
        parts.append(f"size={sizelit(d['size'])}")
    if d["bold"]:
        parts.append("bold=True")
    if d["italic"]:
        parts.append("italic=True")
    if d["color"] is not None:
        parts.append(f"color={d['color']}")
    parts.append("font=FONT")
    return f"run({', '.join(parts)})"


def render_para(pa, text_override=None):
    if pa["runs"]:
        if text_override is not None and len(pa["runs"]) == 1:
            runs = [render_run(pa["runs"][0], text_override)]
        else:
            runs = [render_run(r) for r in pa["runs"]]
        runs_str = "[" + ", ".join(runs) + "]"
    else:
        runs_str = "[]"
    kw = []
    if pa["align"]:
        kw.append(f'align="{pa["align"]}"')
    if pa["level"]:
        kw.append(f"level={pa['level']}")
    if pa["marL"] is not None:
        kw.append(f"mar_l={pa['marL']}")
    if pa["indent"] is not None:
        kw.append(f"indent={pa['indent']}")
    if pa["space_after"] is not None:
        kw.append(f"space_after={pa['space_after']}")
    # deck_core paragraph() defaults to 115% (LNSPC_BODY house style); a ported text
    # box with no explicit lnSpc renders at the 100% default. Emit the source's
    # effective spacing so deck_core's 115% doesn't inflate a tight box (overflow).
    ls = pa["line_spacing"] if pa["line_spacing"] is not None else 100000
    if ls != 115000:
        kw.append(f"line_spacing={ls}")
    if pa["bullet"]:
        kw.append("bullet=True")
    return f"paragraph({runs_str}{(', ' + ', '.join(kw)) if kw else ''})"


def render_sp(rec, id_expr, varmap=None):
    """Render a text_box() call. varmap maps a varying field -> a loop-variable name
    (used inside a cluster loop); fields absent from varmap use the record's literal."""
    varmap = varmap or {}

    def v(field, lit):
        return varmap[field] if field in varmap else lit

    if "text" in varmap and len(rec["paras"]) == 1:
        paras_str = "[" + render_para(rec["paras"][0], varmap["text"]) + "]"
    elif rec["paras"]:
        paras_str = "[" + ", ".join(render_para(p) for p in rec["paras"]) + "]"
    else:
        paras_str = "[paragraph([])]"
    args = [id_expr, f'"{py_str(rec["name"])}"',
            v("x", coordlit(rec["x"])), v("y", coordlit(rec["y"])),
            v("cx", coordlit(rec["cx"])), v("cy", coordlit(rec["cy"])), paras_str]
    kw = [f"fill={v('fill', rec['fill'])}", f"line_color={v('line_color', rec['line_color'])}"]
    if rec["line_width"] is not None and rec["line_width"] != 12700:
        kw.append(f"line_width={rec['line_width']}")
    if rec["dashed"]:
        kw.append("dashed_line=True")
    if rec["prst"] != "rect":
        kw.append(f'prst="{rec["prst"]}"')
    if "geom_adj" in varmap:
        kw.append(f"geom_adj={varmap['geom_adj']}")
    elif rec["geom_adj"]:
        kw.append("geom_adj={" + ", ".join(f'"{k}": "{val}"' for k, val in rec["geom_adj"].items()) + "}")
    if rec["anchor"] != "t":
        kw.append(f'anchor="{rec["anchor"]}"')
    if rec["wrap"] != "square":
        kw.append(f'wrap="{rec["wrap"]}"')
    for k, val in rec["ins"].items():
        kw.append(f"{k}={val}")
    if rec.get("rot"):
        kw.append(f"rot={rec['rot']}")
    return f"text_box({', '.join(args)}, {', '.join(kw)})"


def render_cxn(rec, id_expr, coords=None):
    coords = coords or {}

    def c(field):
        return coords.get(field, coordlit(rec[field]))

    kw = [f"color={rec['color']}", f"width={rec['width']}"]
    if rec["dashed"]:
        kw.append("dashed=True")
    if rec["arrow"]:
        kw.append("arrow=True")
    if rec["prst"] not in ("line", "straightConnector1"):
        kw.append(f'prst="{rec["prst"]}"')
    if rec.get("flip_h"):
        kw.append("flip_h=True")
    if rec.get("flip_v"):
        kw.append("flip_v=True")
    if rec.get("rot"):
        kw.append(f"rot={rec['rot']}")
    if rec.get("adj"):
        kw.append("adj={" + ", ".join(f'"{k}": "{v}"' for k, v in rec["adj"].items()) + "}")
    return (f'connector({id_expr}, "{py_str(rec["name"])}", '
            f'{c("x")}, {c("y")}, {c("cx")}, {c("cy")}, {", ".join(kw)})')


def render_chrome(rec):
    role, data = rec["role"]
    if role == "breadcrumb":
        return f'breadcrumb("{py_str(data[0])}", "{py_str(data[1])}")'
    if role == "title":
        return f'title_placeholder("{py_str(data[0])}", "{py_str(data[1])}")'
    if role == "prelim":
        return "prelim_chip()" if data is None else f'prelim_chip(text="{py_str(data)}")'
    if role == "sources":
        return f'sources_line("{py_str(data)}")'
    return ""


def render_trun(r):
    if r.get("break"):
        return "tbreak()"
    a = [f'"{py_str(r["text"])}"']
    if r["size"] is not None:
        a.append(f"size={sizelit(r['size'])}")
    if r["bold"]:
        a.append("bold=True")
    if r["italic"]:
        a.append("italic=True")
    if r["color"] is not None:
        a.append(f"color={r['color']}")
    a.append("font=FONT")
    return f"trun({', '.join(a)})"


def render_tpara(p):
    runs = ", ".join(render_trun(r) for r in p["runs"])
    al = f', align="{p["align"]}"' if p["align"] and p["align"] != "l" else ""
    return f"tpara([{runs}]{al})"


def _border_lit(b):
    if b == "none":
        return '"none"'
    return '{"color": ' + color_lit(b["color"]) + f', "width": {b["width"]}' + "}"


def render_cell(c):
    kw = []
    if c["fill"] and c["fill"] != "None":
        kw.append(f"fill={c['fill']}")
    if c["grid_span"] > 1:
        kw.append(f"grid_span={c['grid_span']}")
    if c["row_span"] > 1:
        kw.append(f"row_span={c['row_span']}")
    if c["anchor"] and c["anchor"] != "ctr":
        kw.append(f'anchor="{c["anchor"]}"')
    if c["l_ins"] is not None and c["l_ins"] != 45720:
        kw.append(f"l_ins={c['l_ins']}")
    if c["r_ins"] is not None and c["r_ins"] != 45720:
        kw.append(f"r_ins={c['r_ins']}")
    if c.get("t_ins") is not None and c["t_ins"] != 45720:
        kw.append(f"t_ins={c['t_ins']}")
    if c.get("b_ins") is not None and c["b_ins"] != 45720:
        kw.append(f"b_ins={c['b_ins']}")
    if c["borders"]:
        kw.append("borders={" + ", ".join(f'"{k}": {_border_lit(v)}' for k, v in c["borders"].items()) + "}")
    paras = c["paras"]
    if len(paras) <= 1 and (not paras or len(paras[0]["runs"]) <= 1):   # tcell shortcut
        run = paras[0]["runs"][0] if (paras and paras[0]["runs"]) else None
        a = [f'"{py_str(run["text"]) if run else ""}"']
        if run:
            if run["size"] is not None:
                a.append(f"size={sizelit(run['size'])}")
            if run["bold"]:
                a.append("bold=True")
            if run["italic"]:
                a.append("italic=True")
            if run["color"] is not None:
                a.append(f"color={run['color']}")
        elif paras and paras[0].get("end_size") is not None:
            # empty cell: keep its <a:endParaRPr> font size so spacer rows/cols
            # stay collapsed (think-cell uses a 1pt font; the 10pt default bloats them)
            a.append(f"size={sizelit(paras[0]['end_size'])}")
        if paras and paras[0]["align"] and paras[0]["align"] != "l":
            a.append(f'align="{paras[0]["align"]}"')
        return f"tcell({', '.join(a + kw)})"
    paras_str = ", ".join(render_tpara(p) for p in paras)
    return f"tcell_rich([{paras_str}]{(', ' + ', '.join(kw)) if kw else ''})"


def render_table(rec, id_expr):
    cols = ", ".join(coordlit(w) for w in rec["cols"])
    rowlines = [f"        trow([{', '.join(render_cell(c) for c in r['cells'])}], h={coordlit(r['h'])}),"
                for r in rec["rows"]]
    return (f'table({id_expr}, "{py_str(rec["name"])}", {coordlit(rec["x"])}, {coordlit(rec["y"])}, '
            f'{coordlit(rec["cx"])}, {coordlit(rec["cy"])}, col_widths=[{cols}], rows=[\n'
            + "\n".join(rowlines) + "\n    ])")


# ── raw fallback ─────────────────────────────────────────────────────────────
_CRUFT = {q(P, "custDataLst"), q(P, "extLst"), q(A, "extLst"),
          q(A, "hlinkClick"), q(A, "hlinkHover")}


def _strip_cruft(elem):
    for child in list(elem):
        if child.tag in _CRUFT:
            elem.remove(child)
        else:
            _strip_cruft(child)
    return elem


def raw_literal(elem, new_id: int) -> str:
    _strip_cruft(elem)
    nv = elem.find(".//" + q(P, "cNvPr"))
    if nv is not None:
        nv.set("id", str(new_id))
    xml = ET.tostring(elem, encoding="unicode")
    for decl in (f' xmlns:a="{A}"', f' xmlns:p="{P}"', f' xmlns:r="{R}"', f' xmlns:c="{C}"'):
        xml = xml.replace(decl, "")
    return '"' + xml.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ── detection ────────────────────────────────────────────────────────────────
def rec_text(rec):
    return "".join(r.get("text", "") for p in rec["paras"] for r in p["runs"])


def rec_first_bold(rec):
    for p in rec["paras"]:
        for r in p["runs"]:
            return r["bold"]
    return False


def _near(x, y, kind):
    hx, hy = HOUSE_POS[kind]
    return abs(x - hx) <= TOL and abs(y - hy) <= TOL


def detect_chrome(items):
    """Tag records that are standard chrome AND sit within tolerance of the house
    position (so swapping in the builder doesn't move them). Returns a list of
    (kind, moved) notes for divergent chrome left verbatim."""
    notes = []
    for rec in items:
        if rec["type"] != "sp" or rec["raw"]:
            continue
        text = rec_text(rec).strip()
        ph = rec.get("ph")
        x, y = rec["x"], rec["y"]
        if text == "Preliminary":
            if _near(x, y, "prelim"):
                rec["role"] = ("prelim", None)
            else:
                notes.append("Preliminary chip off house position - kept verbatim")
            continue
        if y < 400000 and "/" in text and rec_first_bold(rec):
            if _near(x, y, "breadcrumb"):
                sec, _, top = text.partition("/")
                rec["role"] = ("breadcrumb", (sec.strip(), top.strip()))
            else:
                notes.append("breadcrumb-like shape off house position - kept verbatim")
            continue
        if text.startswith(("Note:", "Source:", "Sources:")):   # before title: a footnote may contain " | "
            if _near(x, y, "sources"):
                rec["role"] = ("sources", text)
            else:
                notes.append("Note/Source line off house position - kept verbatim")
            continue
        if (ph and ph[0] == "title") or " | " in text:
            if (ph and ph[0] == "title") or _near(x, y, "title"):
                topic, _, takeaway = text.partition(" | ")
                rec["role"] = ("title", (topic.strip(), takeaway.strip()))
            else:
                notes.append("title-like shape off house position - kept verbatim")
            continue
    return notes


def is_simple(rec):
    return (rec["type"] == "sp" and not rec["raw"] and not rec["role"]
            and len(rec["paras"]) <= 1
            and (not rec["paras"] or len(rec["paras"][0]["runs"]) <= 1))


def const_key(rec):
    p = rec["paras"][0] if rec["paras"] else None
    r = next((x for x in p["runs"] if not x.get("break")), None) if p else None
    return (rec["prst"], rec["line_width"], rec["dashed"], rec["anchor"], rec["wrap"],
            tuple(sorted(rec["ins"].items())), rec.get("rot", 0),
            tuple(sorted(rec["geom_adj"].keys())),
            p["align"] if p else None, p["level"] if p else 0,
            p["marL"] if p else None, p["indent"] if p else None,
            p["space_after"] if p else None, p["line_spacing"] if p else None,
            p["bullet"] if p else False,
            r["size"] if r else None, r["bold"] if r else False,
            r["italic"] if r else False, r["color"] if r else None, r is not None)


def _member_text(rec):
    return rec["paras"][0]["runs"][0].get("text", "") if (rec["paras"] and rec["paras"][0]["runs"]) else ""


def detect_clusters(items):
    groups = {}
    for i, rec in enumerate(items):
        if is_simple(rec):
            groups.setdefault(const_key(rec), []).append(i)
    clusters = []
    for idxs in groups.values():
        if len(idxs) < MIN_CLUSTER:
            continue
        varying = []
        for field in ("x", "y", "cx", "cy", "fill", "line_color"):
            if len({items[i][field] for i in idxs}) > 1:
                varying.append(field)
        if len({_member_text(items[i]) for i in idxs}) > 1:
            varying.append("text")
        if any(items[i]["geom_adj"] for i in idxs):
            if len({tuple(sorted(items[i]["geom_adj"].items())) for i in idxs}) > 1:
                varying.append("geom_adj")
        varying = [f for f in VARYING_ORDER if f in varying]
        clusters.append({"idxs": idxs, "varying": varying, "leader": idxs[0]})
    return clusters


def cluster_identity(items, cl, used):
    """Infer a cluster's role -> (data-table name, const-anchor prefix, shape name)."""
    texts = [_member_text(items[i]) for i in cl["idxs"]]
    lead = items[cl["leader"]]
    if lead["prst"] == "wedgeRectCallout":
        base, pfx, sn = "_CALLOUTS", "CALLOUT", "Callout"
    elif all(re.fullmatch(r"(19|20)\d\d", (t or "").strip()) for t in texts):
        base, pfx, sn = "_AXIS_YEARS", "AXIS", "YearLabel"
    elif all((t or "").strip() == "" for t in texts) and lead["fill"] != "None":
        base, pfx, sn = "_LEGEND_SWATCHES", "SW", "LegendSwatch"
    elif all(re.fullmatch(r"~?\d{1,3}%?", (t or "").strip()) for t in texts if t):
        base, pfx, sn = "_VALUE_LABELS", "VAL", "ValueLabel"
    elif all((t or "").strip() for t in texts):
        base, pfx, sn = "_LABELS", "LBL", "Label"
    else:
        base, pfx, sn = "_GROUP", "G", "Shape"
    name, k = base, 2
    while name in used:
        name, k = f"{base}{k}", k + 1
    used.add(name)
    pfx += name[len(base):]   # keep the const prefix unique in lockstep with the table name
    return name, pfx, sn


def render_value(rec, field):
    if field in ("x", "y", "cx", "cy"):
        return coordfloat(rec[field])
    if field == "fill":
        return rec["fill"]
    if field == "line_color":
        return rec["line_color"]
    if field == "text":
        return f'"{py_str(_member_text(rec))}"'
    if field == "geom_adj":
        return "{" + ", ".join(f'"{k}": "{v}"' for k, v in rec["geom_adj"].items()) + "}"
    return "None"


# ── chart rels ───────────────────────────────────────────────────────────────
def slide_rels(z, slide_no):
    root = ET.fromstring(z.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels"))
    return {r.get("Id"): r.get("Target") for r in root}


def chart_xlsb(z, chart_target):
    chart_path = "ppt/" + chart_target.split("../", 1)[-1]
    chart_no = "".join(c for c in chart_path.rsplit("/", 1)[-1] if c.isdigit())
    chart_xml = z.read(chart_path).decode("utf-8")
    rels = ET.fromstring(z.read(f"ppt/charts/_rels/chart{chart_no}.xml.rels"))
    xlsb = None
    for r in rels:
        if r.get("Target").lower().endswith((".xlsb", ".xlsx")):
            xlsb = z.read("ppt/" + r.get("Target").split("../", 1)[-1])
    return chart_xml, xlsb, chart_no


# ── chart data extraction (for styled_chart, data-over-template) ───────────────
# Mirrors deck_core.charts.extract_chart_data but stdlib-only and trimmed to the
# fields the emitted _DATA literal needs (categories + per-series name/values),
# keeping this tool copy-next-to-any-pipeline. Series come out in document order
# across every chart-type container (barChart then lineChart, ...) — the order
# styled_chart rewrites — so the round-trip reproduces the source, combos included.
def _chart_series_els(root):
    chart = root.find(q(C, "chart"))
    plot = (chart.find(q(C, "plotArea")) if chart is not None
            else root.find(".//" + q(C, "plotArea")))
    if plot is None:
        return []
    out = []
    for cont in list(plot):
        if cont.tag.split("}")[-1].endswith("Chart"):
            out.extend(cont.findall(q(C, "ser")))
    return out


def _cache_list(parent, *, numeric):
    """Ordered values from a <c:cat>/<c:val>/<c:tx> cache (None at blanks), or
    None when the parent/cache is absent."""
    if parent is None:
        return None
    node = None
    for kind in ("numCache", "strCache", "numLit", "strLit"):
        node = parent.find(".//" + q(C, kind))
        if node is not None:
            break
    if node is None:
        return None
    by_idx = {}
    for pt in node.findall(q(C, "pt")):
        v = pt.find(q(C, "v"))
        by_idx[int(pt.get("idx"))] = v.text if v is not None else None
    pc = node.find(q(C, "ptCount"))
    n = int(pc.get("val")) if pc is not None else 0
    n = max(n, (max(by_idx) + 1) if by_idx else 0)
    out = [by_idx.get(i) for i in range(n)]
    if numeric:
        out = [None if x in (None, "") else round(float(x), 4) for x in out]
    return out


def extract_chart_data(chart_xml):
    """Chart part -> {categories, series:[{name, values}]} for a styled_chart
    _DATA literal. categories / name come back None when the chart omits them
    (think-cell draws those as separate slide shapes)."""
    root = ET.fromstring(chart_xml)
    series, categories = [], None
    for ser in _chart_series_els(root):
        if categories is None:
            categories = _cache_list(ser.find(q(C, "cat")), numeric=False)
        tx = ser.find(q(C, "tx"))
        name = None
        if tx is not None:
            nm = _cache_list(tx, numeric=False)
            if nm:
                name = next((x for x in nm if x), None)
            elif tx.find(q(C, "v")) is not None:
                name = tx.find(q(C, "v")).text
        series.append({"name": name,
                       "values": _cache_list(ser.find(q(C, "val")), numeric=True) or []})
    return {"categories": categories, "series": series}


# ── main ─────────────────────────────────────────────────────────────────────
def _pic_record(el, rels):
    """Parse a <p:pic> into a 'pic' item (or a 'drop' if it lacks media/geometry).
    Coordinates are the element's own; flatten_group re-maps them into slide space."""
    blip = el.find(".//" + q(A, "blip"))
    tgt = rels.get(blip.get(q(R, "embed")), "") if blip is not None else ""
    xfrm = el.find(".//" + q(A, "xfrm"))
    off = xfrm.find(q(A, "off")) if xfrm is not None else None
    ext = xfrm.find(q(A, "ext")) if xfrm is not None else None
    cNvPr = el.find(".//" + q(P, "cNvPr"))
    nm = (cNvPr.get("name") if cNvPr is not None else "") or "Picture"
    if not tgt or off is None or ext is None:
        return {"type": "drop",
                "comment": f"DROPPED <p:pic> {(tgt.rsplit('/', 1)[-1] or '?')} (no media target or geometry)"}
    # <a:srcRect> crops the source image (l/r/t/b, 1/1000 %). Source decks crop a
    # logo strip out of a square canvas; keep it or the logo stretches to a sliver.
    sr = el.find(".//" + q(A, "srcRect"))
    src_rect = {k: int(v) for k, v in sr.attrib.items()} if (sr is not None and sr.attrib) else None
    return {"type": "pic", "name": nm, "target": tgt,
            "is_emf": tgt.lower().endswith(".emf"), "src_rect": src_rect,
            "x": int(off.get("x")), "y": int(off.get("y")),
            "cx": int(ext.get("cx")), "cy": int(ext.get("cy"))}


def flatten_group(grp, theme, rels, notes, parent_tx=None):
    """Flatten a <p:grpSp> into item records mapped into slide (parent) space.

    A group nests a child coordinate system: a child at (x, y) maps to
    off + (x - chOff) * (ext / chExt). Nested groups compose by threading the outer
    transform. Group rotation/flip is NOT applied to children (the schematic icon
    groups carry none); a rotated group is noted so the omission isn't silent."""
    xf = grp.find(q(P, "grpSpPr") + "/" + q(A, "xfrm"))
    nm = grp.find(".//" + q(P, "cNvPr"))
    gname = nm.get("name") if nm is not None else "Group"
    if xf is None:
        notes.append(f"group {gname!r} has no xfrm - skipped")
        return []
    if xf.get("rot") or xf.get("flipH") or xf.get("flipV"):
        notes.append(f"group {gname!r} is rotated/flipped - children placed without that transform")
    off, ext = xf.find(q(A, "off")), xf.find(q(A, "ext"))
    chOff, chExt = xf.find(q(A, "chOff")), xf.find(q(A, "chExt"))
    ox, oy = int(off.get("x")), int(off.get("y"))
    chx, chy = (int(chOff.get("x")), int(chOff.get("y"))) if chOff is not None else (0, 0)
    sx = int(ext.get("cx")) / int(chExt.get("cx")) if (chExt is not None and int(chExt.get("cx"))) else 1.0
    sy = int(ext.get("cy")) / int(chExt.get("cy")) if (chExt is not None and int(chExt.get("cy"))) else 1.0

    def tx(x, y, cx, cy):
        lx, ly, lcx, lcy = ox + (x - chx) * sx, oy + (y - chy) * sy, cx * sx, cy * sy
        return parent_tx(lx, ly, lcx, lcy) if parent_tx else (lx, ly, lcx, lcy)

    out = []
    for el in grp:
        tag = el.tag.split("}")[-1]
        if tag in ("nvGrpSpPr", "grpSpPr"):
            continue
        if tag == "grpSp":
            out.extend(flatten_group(el, theme, rels, notes, parent_tx=tx))
            continue
        if tag == "pic":
            rec = _pic_record(el, rels)
        elif tag == "cxnSp":
            rec = parse_cxn(el, theme)
        elif tag == "sp":
            rec = parse_sp(el, theme)
        elif tag == "graphicFrame":
            notes.append(f"group {gname!r} contains a graphicFrame (table/chart) - skipped")
            continue
        else:
            continue
        if not rec.get("raw") and all(k in rec for k in ("x", "y", "cx", "cy")):
            x, y, cx, cy = tx(rec["x"], rec["y"], rec["cx"], rec["cy"])
            rec["x"], rec["y"], rec["cx"], rec["cy"] = round(x), round(y), round(cx), round(cy)
        elif rec.get("raw"):
            notes.append(f"group {gname!r} child kept raw ({rec['raw']}) - not re-positioned")
        out.append(rec)
    return out


def convert(src_pptx, slide_no, out_path, src_dir, module_name, layout, units="inches",
            images_dir=None):
    global _UNITS
    _UNITS = units
    out_path, src_dir = Path(out_path), Path(src_dir)
    src_dir.mkdir(parents=True, exist_ok=True)
    images_dir = Path(images_dir) if images_dir else out_path.parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src_pptx) as z:
        theme = build_theme_map(z)
        rels = slide_rels(z, slide_no)
        root = ET.fromstring(z.read(f"ppt/slides/slide{slide_no}.xml"))
        spTree = root.find(q(P, "cSld") + "/" + q(P, "spTree"))

        items = []
        chart_assets = []
        group_notes = []
        for el in spTree:
            tag = el.tag.split("}")[-1]
            if tag == "graphicFrame":
                chart = el.find(".//" + q(C, "chart"))
                nm = (el.find(".//" + q(P, "cNvPr")).get("name", "") or "").lower()
                if chart is not None:
                    cx_xml, xlsb, cno = chart_xlsb(z, rels[chart.get(q(R, "id"))])
                    cfile, xfile = f"slide{slide_no}_chart{cno}.xml", f"slide{slide_no}_chart{cno}.xlsb"
                    (src_dir / cfile).write_text(cx_xml, encoding="utf-8")
                    if xlsb is not None:
                        (src_dir / xfile).write_bytes(xlsb)
                    try:
                        cdata = extract_chart_data(cx_xml)
                    except Exception:
                        cdata = None   # fall back to a verbatim bundle
                    chart_assets.append((cfile, xfile if xlsb is not None else None, cdata))
                    xf = el.find(q(P, "xfrm"))
                    off, ext = xf.find(q(A, "off")), xf.find(q(A, "ext"))
                    items.append({"type": "chart", "x": int(off.get("x")), "y": int(off.get("y")),
                                  "cx": int(ext.get("cx")), "cy": int(ext.get("cy")),
                                  "rId": f"rId{len(chart_assets) + 1}"})
                elif el.find(".//" + q(A, "tbl")) is not None:
                    items.append(parse_table(el, theme))
                else:
                    items.append({"type": "drop", "comment": f"DROPPED graphicFrame ('{nm}') - think-cell OLE"})
            elif tag == "pic":
                items.append(_pic_record(el, rels))
            elif tag == "grpSp":
                items.extend(flatten_group(el, theme, rels, group_notes))
            elif tag == "cxnSp":
                items.append(parse_cxn(el, theme))
            elif tag == "sp":
                items.append(parse_sp(el, theme))

        # ── finalize <p:pic> images: EMF-preview gating, media copy, rId assignment ──
        # An .emf pic over a bundled native chart is the think-cell vector PREVIEW of
        # that chart -> drop it (the chart renders itself). With no native chart on the
        # slide the .emf IS the content (icon / vector graphic) -> keep it. Kept images
        # become picture() + an IMAGES entry; bytes are copied into images_dir under a
        # content-addressed name so identical media dedupes and names never collide
        # across source decks. Image rIds continue after the layout (rId1) and any chart
        # rIds, so the first image is rId{len(charts)+2} (matches deck_core.lib).
        has_native_chart = any(r.get("type") == "chart" for r in items)
        images = []                       # [{"rId","file"}] -> the module IMAGES block
        tgt_to_img = {}                   # source media target -> (rId, copied filename)
        img_rid_base = len(chart_assets) + 2
        for rec in items:
            if rec.get("type") != "pic":
                continue
            if rec["is_emf"] and has_native_chart:
                rec["type"], rec["comment"] = "drop", (
                    f"DROPPED <p:pic> {rec['target'].rsplit('/', 1)[-1]} "
                    f"(EMF think-cell preview of a bundled chart)")
                continue
            tgt = rec["target"]
            if tgt not in tgt_to_img:
                fname_src = tgt.rsplit("/", 1)[-1]
                zip_path = "ppt/media/" + fname_src
                if zip_path not in z.namelist():
                    rec["type"], rec["comment"] = "drop", (
                        f"DROPPED <p:pic> {fname_src} (media part missing from source)")
                    continue
                data = z.read(zip_path)
                stem, _, ext = fname_src.rpartition(".")
                digest = hashlib.sha1(data).hexdigest()[:8]
                new_name = f"{stem or fname_src}_{digest}" + (f".{ext}" if ext else "")
                (images_dir / new_name).write_bytes(data)
                rid = f"rId{img_rid_base + len(tgt_to_img)}"
                tgt_to_img[tgt] = (rid, new_name)
                images.append({"rId": rid, "file": new_name})
            rec["rId"], rec["file"] = tgt_to_img[tgt]

        notes = group_notes + detect_chrome(items)
        clusters = detect_clusters(items)

    leader_of = {cl["leader"]: cl for cl in clusters}
    member_set = {i for cl in clusters for i in cl["idxs"]}

    # cluster identity (data-table name / const-anchor prefix / shape name)
    used_names = set()
    for cl in clusters:
        cl["table"], cl["prefix"], cl["shape_name"] = cluster_identity(items, cl, used_names)

    # ── coordinate hoisting: name the structural anchors, keep per-shape coords raw ──
    anchor_defs = []   # module-level "layout anchor" constant lines (faithful: same values)
    # (a) each cluster's CONSTANT coords -> role-named anchors (_AXIS_Y, _SW_X, ...)
    for cl in clusters:
        amap, triples = {}, []
        for f in ("x", "y", "cx", "cy"):
            if f not in cl["varying"]:
                cname = f"_{cl['prefix']}_{DIM[f]}"
                amap[f] = cname
                triples.append((cname, items[cl["leader"]][f]))
        cl["coord_alias"] = amap
        if triples:
            vals = ", ".join(coordlit(v) for _, v in triples)
            cmt = "" if _UNITS == "inches" else \
                f"   # {', '.join(f'{v / 914400:.2f}in' for _, v in triples)}"
            anchor_defs.append(f"{', '.join(c for c, _ in triples)} = {vals}{cmt}")
    # (b) coords repeated across standalone shapes/connectors -> shared anchors (_Y1, _X1, ...)
    standalone = [i for i, rec in enumerate(items)
                  if i not in member_set and i not in leader_of and rec["type"] in ("sp", "cxn")
                  and not rec.get("role") and not rec.get("raw")]
    freq = {}
    for i in standalone:
        for f in ("x", "y", "cx", "cy"):
            v = items[i].get(f)
            if isinstance(v, int) and v > 0:
                freq[v] = freq.get(v, 0) + 1
    global_alias, dimk = {}, {"X": 0, "Y": 0, "W": 0, "H": 0}
    for i in standalone:
        for f in ("x", "y", "cx", "cy"):
            v = items[i].get(f)
            if isinstance(v, int) and v > 0 and freq[v] >= SHARED_ANCHOR_MIN and v not in global_alias:
                dimk[DIM[f]] += 1
                global_alias[v] = f"_{DIM[f]}{dimk[DIM[f]]}"
                anchor_defs.append(f"{global_alias[v]} = {coordlit(v)}   # shared x{freq[v]}")

    def coord_map_for(rec):
        return {f: global_alias[rec[f]] for f in ("x", "y", "cx", "cy")
                if isinstance(rec.get(f), int) and rec[f] in global_alias}

    data_defs, body = [], []
    stats = {"text_box": 0, "connector": 0, "chart": 0, "table": 0, "picture": 0, "raw": 0,
             "dropped": 0, "fld": 0, "clusters": 0, "chrome": 0, "looped": 0}
    raw_id = 2000
    for i, rec in enumerate(items):
        if i in leader_of:
            cl = leader_of[i]
            fields = cl["varying"]
            stats["clusters"] += 1
            stats["looped"] += len(cl["idxs"])
            stats["fld"] += sum(len(items[j]["el"].findall(".//" + q(A, "fld"))) for j in cl["idxs"])
            keycmt = ", ".join(FIELD_LABEL[f] for f in fields)
            data_defs.append(f"{cl['table']} = [    # ({keycmt}) x{len(cl['idxs'])}")
            for j in cl["idxs"]:
                vals = ", ".join(render_value(items[j], f) for f in fields)
                data_defs.append(f"    ({vals})," if len(fields) != 1 else f"    {vals},")
            data_defs.append("]")
            data_defs.append("")
            varmap = {}
            for f in fields:
                vn = VAR_NAMES[f]
                varmap[f] = (f"IN({vn})" if _UNITS == "inches" and f in ("x", "y", "cx", "cy") else vn)
            varmap.update(cl["coord_alias"])   # constant coords -> role-named anchors (already EMU)
            rec["name"] = cl["shape_name"]      # role-based shape name
            unpack = ", ".join(VAR_NAMES[f] for f in fields)
            body.append(f"    for {unpack} in {cl['table']}:")
            body.append(f"        out.append({render_sp(rec, 'n()', varmap)})")
            continue
        if i in member_set:
            continue
        if rec["type"] == "drop":
            body.append(f"    # {rec['comment']}")
            stats["dropped"] += 1
        elif rec["type"] == "table":
            body.append('    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)')
            body.append(f"    out.append({render_table(rec, 'n()')})")
            stats["table"] += 1
        elif rec["type"] == "chart":
            body.append('    # native chart, bundled verbatim + .xlsb ("Edit Data" works)')
            body.append(f'    out.append(graphic_frame(sp_id=n(), name="Chart", '
                        f'x={coordlit(rec["x"])}, y={coordlit(rec["y"])}, '
                        f'cx={coordlit(rec["cx"])}, cy={coordlit(rec["cy"])}, rId="{rec["rId"]}"))')
            stats["chart"] += 1
        elif rec["type"] == "pic":
            sr = rec.get("src_rect")
            sr_arg = f", src_rect={sr!r}" if sr else ""
            body.append('    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)')
            body.append(f'    out.append(picture(n(), "{py_str(rec["name"])}", "{rec["rId"]}", '
                        f'{coordlit(rec["x"])}, {coordlit(rec["y"])}, '
                        f'{coordlit(rec["cx"])}, {coordlit(rec["cy"])}{sr_arg}))')
            stats["picture"] += 1
        elif rec.get("role"):
            body.append(f"    out.append({render_chrome(rec)})")
            stats["chrome"] += 1
        elif rec["type"] == "cxn":
            if rec["raw"]:
                body.append(f"    out.append({raw_literal(rec['el'], raw_id)})")
                raw_id += 1
                stats["raw"] += 1
            else:
                body.append(f"    out.append({render_cxn(rec, 'n()', coord_map_for(rec))})")
                stats["connector"] += 1
        elif rec["type"] == "sp":
            stats["fld"] += len(rec["el"].findall(".//" + q(A, "fld")))
            if rec["raw"]:
                body.append(f"    # RAW verbatim ({rec['raw']}):")
                body.append(f"    out.append({raw_literal(rec['el'], raw_id)})")
                raw_id += 1
                stats["raw"] += 1
            else:
                body.append(f"    out.append({render_sp(rec, 'n()', coord_map_for(rec))})")
                stats["text_box"] += 1

    module = build_module_text(module_name, slide_no, layout, chart_assets, images,
                               anchor_defs, data_defs, body, stats, notes)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(module, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"  text_box={stats['text_box']} connector={stats['connector']} chart={stats['chart']} "
          f"table={stats['table']} picture={stats['picture']} raw={stats['raw']} dropped={stats['dropped']} frozen_fields={stats['fld']}")
    print(f"  chrome builders={stats['chrome']} | clusters={stats['clusters']} "
          f"collapsing {stats['looped']} shapes into loops")
    for nt in notes:
        print(f"  note: {nt}")


def _imports(text, chart_syms=()):
    prims = ["slide"]
    for nm in ("run", "paragraph", "text_box", "connector", "picture", "line_break",
               "table", "trow", "tcell", "tcell_rich", "tpara", "trun", "tbreak"):
        if re.search(rf"\b{nm}\(", text):
            prims.append(nm)
    chrome = [nm for nm in ("breadcrumb", "title_placeholder", "prelim_chip", "sources_line")
              if re.search(rf"\b{nm}\(", text)]
    toks = [t for t in dict.fromkeys(TOKENS.values()) if re.search(rf"\b{t}\b", text)]
    if "FONT" not in toks:
        toks.append("FONT")
    if re.search(r"\bPT\(", text):
        toks = ["PT"] + toks
    if re.search(r"\bIN\(", text):
        toks = ["IN"] + toks
    prim_line = "from deck_core.primitives import " + ", ".join(prims + chrome)
    if len(prim_line) > 95:
        prim_line = ("from deck_core.primitives import (\n    "
                     + ", ".join(prims + chrome) + ",\n)")
    lines = [prim_line]
    chart_imports = [s for s in ("graphic_frame", "styled_chart", "editable_bundled_chart")
                     if s in chart_syms]
    if chart_imports:
        lines.append("from deck_core.charts import " + ", ".join(chart_imports))
    lines.append("from deck_core.style import " + ", ".join(toks))
    return "\n".join(lines)


def _fmt_num_literal(v):
    """A number for a _DATA literal: None stays None, int-valued floats lose the
    '.0' (42.0 -> 42), everything else is repr (shortest round-trip)."""
    if v is None:
        return "None"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return repr(v)


def _format_chart_data(var, data):
    """Emit a readable _DATA literal: categories + one {name?, values} per series."""
    out = [f"{var} = {{"]
    cats = data.get("categories")
    if cats is None:
        out.append('    "categories": None,')
    else:
        out.append('    "categories": [' + ", ".join(repr(c) for c in cats) + "],")
    out.append('    "series": [')
    for s in data["series"]:
        vals = "[" + ", ".join(_fmt_num_literal(v) for v in s["values"]) + "]"
        if s.get("name") is not None:
            out.append(f'        {{"name": {s["name"]!r}, "values": {vals}}},')
        else:
            out.append(f'        {{"values": {vals}}},')
    out += ["    ],", "}"]
    return "\n".join(out)


def build_module_text(module_name, slide_no, layout, chart_assets, images, anchor_defs, data_defs, body, stats, notes):
    chart_reads, data_literals, charts, chart_syms = [], [], [], set()
    for i, (cfile, xfile, cdata) in enumerate(chart_assets):
        # styled_chart (data-over-template) when we recovered both the .xlsb and
        # the series data; else fall back to a verbatim editable/raw bundle.
        if xfile and cdata and cdata.get("series"):
            chart_reads.append(f'_CHART{i}_TPL = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            chart_reads.append(f'_XLSB{i} = (_SRC / "{xfile}").read_bytes()')
            data_literals.append(_format_chart_data(f"_CHART{i}_DATA", cdata))
            charts.append(f"styled_chart(_CHART{i}_TPL, _CHART{i}_DATA, _XLSB{i})")
            chart_syms.add("styled_chart")
        elif xfile:
            chart_reads.append(f'_CHART{i} = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            chart_reads.append(f'_XLSB{i} = (_SRC / "{xfile}").read_bytes()')
            charts.append(f"editable_bundled_chart(_CHART{i}, _XLSB{i})")
            chart_syms.add("editable_bundled_chart")
        else:
            chart_reads.append(f'_CHART{i} = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            charts.append(f'{{"chart_xml": _CHART{i}}}')
    if chart_assets:
        chart_syms.add("graphic_frame")
        blocks = ["\n".join(chart_reads)]
        blocks += data_literals
        blocks.append("CHARTS = [" + ", ".join(charts) + "]")
        chart_block = "\n\n".join(blocks)
    else:
        chart_block = "CHARTS: list = []"
    if images:
        img_lines = ["IMAGES = ["]
        for im in images:
            img_lines.append(f'    {{"rId": "{im["rId"]}", "file": "{im["file"]}"}},')
        img_lines.append("]")
        images_block = "\n" + "\n".join(img_lines)
    else:
        images_block = ""
    all_text = "\n".join(anchor_defs + data_defs + body)
    has_styled = any(xfile and cdata and cdata.get("series")
                     for (_, xfile, cdata) in chart_assets)
    if has_styled:
        chart_doc = ('The native <c:chart> exhibit is a data-over-template styled_chart: the\n'
                     'source chart part is the exact STYLE template and its values live in the\n'
                     '_CHART*_DATA literal (look byte-identical, "Edit Data" still works).')
    elif chart_assets:
        chart_doc = ('The native <c:chart> exhibit is bundled verbatim with its .xlsb\n'
                     '(byte-exact, still "Edit Data"-editable).')
    else:
        chart_doc = 'Shapes are rebuilt through deck_core primitives.'
    notes_doc = ("\n\nConverter notes:\n  - " + "\n  - ".join(notes)) if notes else ""
    data_section = ""
    if anchor_defs:
        data_section += ("# ── layout anchors (shared coordinates) ──\n"
                         + "\n".join(anchor_defs) + "\n\n")
    if data_defs:
        data_section += ("# ── repeated-shape data tables (each drives a loop in _body) ──\n"
                         + "\n".join(data_defs) + "\n")
    return f'''"""{module_name} - Commercial Strategy deck, source slide {slide_no}.

Auto-converted from the source .pptx by _tools/convert_slide.py.
{chart_doc}
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box={stats['text_box']}, connector={stats['connector']}, chart={stats['chart']}, \
table={stats['table']}, picture={stats['picture']}, chrome_builders={stats['chrome']}, clusters={stats['clusters']} (covering {stats['looped']} shapes), \
raw_verbatim={stats['raw']}, dropped={stats['dropped']}, frozen_fields={stats['fld']}.{notes_doc}
"""
from __future__ import annotations

from pathlib import Path

{_imports(all_text, chart_syms)}

LAYOUT = "{layout}"

_SRC = Path(__file__).parent / "_src"
{chart_block}{images_block}


{data_section}def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
{chr(10).join(body)}
    return "".join(out)


def render() -> str:
    return slide(_body())
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source")
    ap.add_argument("slide", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--src-dir", required=True)
    ap.add_argument("--module-name", required=True)
    ap.add_argument("--layout", default="slideLayout4")
    ap.add_argument("--units", choices=("inches", "emu"), default="inches",
                    help="coordinate units in the emitted module (default inches via IN())")
    ap.add_argument("--images-dir", default=None,
                    help="dir to copy <p:pic> media into (default: <out>/../images, "
                         "i.e. the slides/images/ the build packs into ppt/media/)")
    a = ap.parse_args()
    convert(a.source, a.slide, a.out, a.src_dir, a.module_name, a.layout, a.units,
            a.images_dir)


if __name__ == "__main__":
    main()
