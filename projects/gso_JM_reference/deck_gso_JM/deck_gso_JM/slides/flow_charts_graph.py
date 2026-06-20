"""flow_charts_graph - a hybrid semantic-graph + pinned-renderer flow chart.

Built so an AI agent can read the TOPOLOGY (which box connects to which) while
the slide still renders the SHIPS Act flow exactly like the faithful versions.
The trick: a "gold" edge keeps its src/dst for meaning AND pins the original
PowerPoint connector geometry, instead of asking a router to re-derive it.

  flow_charts.py          verbatim PowerPoint XML export (opaque, faithful)
  flow_charts_rebuilt.py  data tables of shapes with pinned connector coords
  flow_charts_graph.py    THIS - semantic graph; gold edges pinned, new edges routed

Why hybrid: PowerPoint draws connectors with rotated/flipped PRESET geometry
(bentConnector3/2, straightConnector1 + rot/flipH/flipV/adj1). A generic router
can't reproduce that exact look, and it shouldn't have to. So every edge in the
gold SHIPS chart carries a `conn={...}` (the exact transform) and a
`label_box={...}` (the exact white-chip rectangle). Edges authored later for a
NEW chart just omit `conn` and fall back to the orthogonal router below.

────────────────────────────────────────────────────────────────────────────
EDGE — required: src, dst (node ids; arrow points src -> dst).
  GOLD (pinned, faithful) fields:
    conn      = dict(prst=, x=, y=, cx=, cy=, rot=0, flipH=False, flipV=False,
                     adj1=None)   exact <p:cxnSp> preset-connector transform (EMU)
    label     text for the white chip
    label_box = dict(x=, y=, w=, h=)   exact chip rectangle (EMU)
    label_z   paint order among labels (source stacking order)
    dashed / arrow   line style (default solid, arrow at dst)
  NEW (routed, no conn) fields - the router computes the path:
    src_side/dst_side ("top"|"bottom"|"left"|"right"), src_pos/dst_pos (0..1),
    mid (0..1 bend), via ([(x,y),...] explicit waypoints), straight, dashed,
    arrow, label_w.   See _route() / _edge() fallback.

NODE — one entry in NODES: x, y, w, h (EMU; 914400=1in), fill (hex or None),
  para (_t("Label","FFFFFF") simple, or _p(_r(...)) multi-run), border.
"""
from __future__ import annotations

from xml.sax.saxutils import escape as _esc

from deck_core.primitives import slide

LAYOUT = "slideLayout4"

_ID = [2000]
def _nid() -> int:
    _ID[0] += 1
    return _ID[0]


# ── OOXML run / paragraph / box helpers (self-contained) ─────────────────────
def _r(t, *, sz=1000, b=False, i=False, u=False, color="000000"):
    a = f' sz="{sz}"' + (' b="1"' if b else '') + (' i="1"' if i else '') + (' u="sng"' if u else '')
    return (f'<a:r><a:rPr lang="en-US"{a}><a:solidFill><a:srgbClr val="{color}"/>'
            f'</a:solidFill></a:rPr><a:t>{_esc(t)}</a:t></a:r>')

def _brk(*, b=False, color="000000"):
    a = ' sz="1000"' + (' b="1"' if b else '')
    return f'<a:br><a:rPr lang="en-US"{a}><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr></a:br>'

def _p(*runs, algn="ctr"):
    pPr = f'<a:pPr algn="{algn}"/>' if algn else ''
    return f'<a:p>{pPr}{"".join(runs)}</a:p>'

def _t(text, fg, sz=1000):                       # simple bold centered label
    return _p(_r(text, sz=sz, b=True, color=fg))

def _box(x, y, w, h, para, *, fill=None, border=True, lw=12700):
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    ln_xml = (f'<a:ln w="{lw}"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln>'
              if border else '<a:ln w="12700"><a:noFill/></a:ln>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_nid()}" name="box"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{fill_xml}{ln_xml}</p:spPr>'
            f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/>{para}</p:txBody></p:sp>')


# ════════════════════════════════════════════════════════════════════════════
# NODES — the single source of geometry.
# ════════════════════════════════════════════════════════════════════════════
NODES = {
    # actor column (left) -----------------------------------------------------
    "shipbuilders": dict(x=1062038, y=1296511, w=1371600, h=1097280, fill="223E59", para=_t("US Shipbuilders", "FFFFFF", 1200)),
    "owners":       dict(x=1062038, y=2623983, w=1371600, h=1097280, fill="447BB2", para=_t("US-Built, US-Flagged Vessel Owners / Operators", "FFFFFF", 1200)),
    "govt":         dict(x=1062038, y=3951455, w=1371600, h=1097280, fill="99B9D8", para=_t("US Government", "000000", 1200)),
    "foreign":      dict(x=1062038, y=5278928, w=1371600, h=1097280, fill="808080", para=_t("Foreign Vessel Owners / Operators", "FFFFFF", 1200)),
    # entity boxes ------------------------------------------------------------
    "us_built_ships":     dict(x=2509211, y=2623983, w=2251075, h=293688, fill="447BB2", para=_t("US Built Ships", "FFFFFF")),
    "capital_subsidies":  dict(x=4835398, y=3951455, w=2249488, h=293688, fill="3D9970", para=_t("Capital Subsidies", "FFFFFF")),
    "operating_subsidies":dict(x=7160458, y=3951455, w=2249488, h=293688, fill="6DCF9E", para=_t("Operating Subsidies", "000000")),
    "penalties":          dict(x=2509210, y=5271939, w=5488616, h=293688, fill="C00000", para=_t("Penalties", "FFFFFF")),
    "prc_owned":          dict(x=2509210, y=6082520, w=1737360, h=293688, fill="A6A6A6", para=_t("PRC owned/operated", "FFFFFF")),
    "orderbook50":        dict(x=4384838, y=6082520, w=1737360, h=293688, fill="BFBFBF", para=_t("50% of orderbook / fleet from PRC", "000000")),
    "orderbook25":        dict(x=6260466, y=6082520, w=1737360, h=293688, fill="D9D9D9", para=_t("25-49% of orderbook at PRC", "000000")),
    "other_foreign":      dict(x=8039100, y=6082520, w=1828800, h=293688, fill="F2F2F2", para=_t("Other foreign ship operators", "000000")),
    # rich (multi-run) boxes --------------------------------------------------
    "trust_fund": dict(x=2509211, y=4755047, w=9227946, h=293688, fill="1B4332",
                       para=_p(_r("Maritime Security Trust Fund ", b=True, color="FFFFFF"),
                               _r("($20B cap, appropriations specified from FY26-FY35)", i=True, color="FFFFFF"))),
    "scf": dict(x=7997826, y=2134266, w=3738024, h=749241, fill="0E1924",
                para=_p(_r("Strategic Commercial Fleet (SCF)", b=True, color="FFFFFF"), _brk(b=True, color="FFFFFF"),
                        _r("(250 commercial ships for foreign trade only; ", i=True, color="FFFFFF"),
                        _r("permanently ineligible for coastwise trade i.e., Jones Act", b=True, i=True, u=True, color="FFFFFF"),
                        _r(")", i=True, color="FFFFFF"))),
    "reg_tonnage": dict(x=8038692, y=5271939, w=1828800, h=293688, fill="FFC000",
                        para=_p(_r("Regular Tonnage Taxes ", b=True), _brk(b=True), _r("(Subject to exemptions)", i=True))),
    "cargo_fees": dict(x=9908357, y=5271939, w=1828800, h=293688, fill="FB6B3C",
                       para=_p(_r("Cargo Fees ($0.01+ / kg)", b=True, color="FFFFFF"), _brk(b=True, color="FFFFFF"),
                               _r("SHIPS Act “Plus” only", i=True, color="FFFFFF"))),
}

# ════════════════════════════════════════════════════════════════════════════
# EDGES — gold SHIPS chart: semantic src/dst + pinned PowerPoint connector geom.
# Arrow points src -> dst (verified against the export's tailEnd direction).
# ════════════════════════════════════════════════════════════════════════════
EDGES = [
    dict(src="shipbuilders", dst="us_built_ships", label="Sells", label_z=1,
         conn=dict(prst="bentConnector2", x=2433638, y=1845151, cx=1201111, cy=778832),
         label_box=dict(x=2719942, y=1762261, w=552929, h=165779)),
    dict(src="owners", dst="shipbuilders", label="Buys", label_z=5,
         conn=dict(prst="straightConnector1", x=1747838, y=2393791, cx=0, cy=230192, flipV=True),
         label_box=dict(x=1878596, y=2423463, w=552929, h=165779)),
    dict(src="us_built_ships", dst="scf", label="Placed into service ", label_z=4,
         conn=dict(prst="bentConnector3", x=4760286, y=2508887, cx=3237540, cy=261940, flipV=True, adj1=50000),
         label_box=dict(x=5749236, y=2548269, w=1320347, h=180640)),
    dict(src="capital_subsidies", dst="us_built_ships",
         label="Paid to US vessel owner / operators for each ship in SCF", label_z=2,
         conn=dict(prst="bentConnector3", x=4280554, y=2271866, cx=1033784, cy=2325393, rot=16200000, flipV=True, adj1=50000),
         label_box=dict(x=4834835, y=3554575, w=4575112, h=166688)),
    dict(src="operating_subsidies", dst="us_built_ships",
         conn=dict(prst="bentConnector3", x=5443084, y=1109336, cx=1033784, cy=4650453, rot=16200000, flipV=True, adj1=50000)),
    dict(src="trust_fund", dst="capital_subsidies", label="Disburses", label_z=3,
         conn=dict(prst="bentConnector3", x=6286711, y=3918574, cx=509904, cy=1163042, rot=16200000, flipV=True, adj1=50000),
         label_box=dict(x=5998440, y=4538341, w=2249488, h=166688)),
    dict(src="trust_fund", dst="operating_subsidies",
         conn=dict(prst="bentConnector3", x=7449241, y=3919086, cx=509904, cy=1162018, rot=5400000, flipH=True, flipV=True, adj1=50000)),
    dict(src="penalties", dst="trust_fund",
         conn=dict(prst="bentConnector3", x=6076749, y=4225504, cx=223204, cy=1869666, rot=5400000, flipH=True, flipV=True, adj1=50000)),
    dict(src="reg_tonnage", dst="trust_fund",
         conn=dict(prst="bentConnector3", x=7926536, y=4245383, cx=223204, cy=1829908, rot=16200000, flipV=True, adj1=50000)),
    dict(src="cargo_fees", dst="trust_fund",
         conn=dict(prst="bentConnector3", x=8861369, y=3310550, cx=223204, cy=3699573, rot=16200000, flipV=True, adj1=50000)),
    dict(src="prc_owned", dst="penalties",
         conn=dict(prst="bentConnector3", x=4057258, y=4886260, cx=516893, cy=1875628, rot=5400000, flipH=True, flipV=True)),
    dict(src="orderbook25", dst="penalties",
         conn=dict(prst="bentConnector3", x=5932886, y=4886260, cx=516893, cy=1875628, rot=16200000, flipV=True, adj1=50000)),
    dict(src="orderbook50", dst="penalties", label="Pays", label_z=6,
         conn=dict(prst="straightConnector1", x=5253518, y=5565627, cx=0, cy=516893, flipV=True),
         label_box=dict(x=4972501, y=5746212, w=562035, h=166688)),
    dict(src="other_foreign", dst="reg_tonnage", label="Pays", label_z=7,
         conn=dict(prst="straightConnector1", x=8953092, y=5565627, cx=408, cy=516893, flipH=True, flipV=True),
         label_box=dict(x=8672075, y=5746212, w=562035, h=166688)),
    dict(src="other_foreign", dst="cargo_fees", label="Pays", label_z=8,
         conn=dict(prst="bentConnector2", x=9908357, y=5565627, cx=914400, cy=639903, flipV=True),
         label_box=dict(x=10496020, y=5740729, w=562035, h=166688)),
]


# ════════════════════════════════════════════════════════════════════════════
# PINNED RENDERER — exact PowerPoint preset connector (gold edges)
# ════════════════════════════════════════════════════════════════════════════
def _conn(*, prst, x, y, cx, cy, rot=0, flipH=False, flipV=False, adj1=None,
          w=12700, dashed=False, arrow=True):
    """A <p:cxnSp> preset connector with the export's exact transform."""
    xf = '<a:xfrm'
    if rot: xf += f' rot="{rot}"'
    if flipH: xf += ' flipH="1"'
    if flipV: xf += ' flipV="1"'
    xf += f'><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
    av = f'<a:gd name="adj1" fmla="val {adj1}"/>' if adj1 is not None else ''
    dash = '<a:prstDash val="dash"/>' if dashed else ''
    tail = '<a:tailEnd type="triangle"/>' if arrow else ''
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{_nid()}" name="conn"/>'
            f'<p:cNvCxnSpPr><a:cxnSpLocks/></p:cNvCxnSpPr><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr>{xf}<a:prstGeom prst="{prst}"><a:avLst>{av}</a:avLst></a:prstGeom>'
            f'<a:ln w="{w}"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
            f'{dash}{tail}</a:ln></p:spPr></p:cxnSp>')

def _edge_label_box(text, box):
    """White relationship chip at an exact pinned rectangle."""
    return _box(box["x"], box["y"], box["w"], box["h"], _p(_r(text, i=True)),
                fill="FFFFFF", border=False)


# ════════════════════════════════════════════════════════════════════════════
# ROUTER — fallback for NEW edges authored without pinned `conn` geometry
# ════════════════════════════════════════════════════════════════════════════
def _center(n):
    return (n["x"] + n["w"] // 2, n["y"] + n["h"] // 2)

def _anchor(n, side, pos=0.5):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    if side == "left":   return (x,                  y + int(h * pos))
    if side == "right":  return (x + w,              y + int(h * pos))
    if side == "top":    return (x + int(w * pos),   y)
    return                      (x + int(w * pos),   y + h)            # bottom

def _default_sides(src, dst):
    s_top, s_bot = src["y"], src["y"] + src["h"]
    d_top, d_bot = dst["y"], dst["y"] + dst["h"]
    if d_top >= s_bot:
        return ("bottom", "top")
    if d_bot <= s_top:
        return ("top", "bottom")
    return ("right", "left") if _center(dst)[0] >= _center(src)[0] else ("left", "right")

def _dedupe(pts):
    out = [pts[0]]
    for p in pts[1:]:
        if p != out[-1]:
            out.append(p)
    return out

def _route(p0, s0, p1, s1, mid=0.5):
    x0, y0 = p0; x1, y1 = p1
    if x0 == x1 or y0 == y1:
        return [(x0, y0), (x1, y1)]
    v0 = s0 in ("top", "bottom"); v1 = s1 in ("top", "bottom")
    if v0 and v1:
        ym = y0 + int((y1 - y0) * mid)
        return _dedupe([(x0, y0), (x0, ym), (x1, ym), (x1, y1)])
    if not v0 and not v1:
        xm = x0 + int((x1 - x0) * mid)
        return _dedupe([(x0, y0), (xm, y0), (xm, y1), (x1, y1)])
    if v0:
        return _dedupe([(x0, y0), (x0, y1), (x1, y1)])
    return _dedupe([(x0, y0), (x1, y0), (x1, y1)])

def _edge_conn(pts, *, w=12700, dashed=False, arrow=True):
    """Open-path custGeom LINE SHAPE for a routed (non-pinned) edge."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    mnx, mny = min(xs), min(ys)
    W = max(max(xs) - mnx, 1); H = max(max(ys) - mny, 1)
    move = f'<a:moveTo><a:pt x="{pts[0][0]-mnx}" y="{pts[0][1]-mny}"/></a:moveTo>'
    lns = "".join(f'<a:lnTo><a:pt x="{x-mnx}" y="{y-mny}"/></a:lnTo>' for x, y in pts[1:])
    dash = '<a:prstDash val="dash"/>' if dashed else ''
    tail = '<a:tailEnd type="triangle"/>' if arrow else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_nid()}" name="edge"/><p:cNvSpPr/><p:nvPr/>'
            f'</p:nvSpPr><p:spPr>'
            f'<a:xfrm><a:off x="{mnx}" y="{mny}"/><a:ext cx="{W}" cy="{H}"/></a:xfrm>'
            f'<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/>'
            f'<a:rect l="0" t="0" r="0" b="0"/>'
            f'<a:pathLst><a:path w="{W}" h="{H}" fill="none">{move}{lns}</a:path></a:pathLst>'
            f'</a:custGeom><a:noFill/>'
            f'<a:ln w="{w}"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>{dash}{tail}</a:ln>'
            f'</p:spPr><p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/><a:p/></p:txBody></p:sp>')

def _longest_mid(pts):
    best, blen = pts[0], -1
    for a, b in zip(pts, pts[1:]):
        L = abs(b[0] - a[0]) + abs(b[1] - a[1])
        if L > blen:
            blen = L; best = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
    return best

def _edge_label(text, at, label_w=None):
    w = label_w or min(max(len(text) * 68000 + 120000, 480000), 4800000)
    h = 175000
    cx, cy = at
    return _box(cx - w // 2, cy - h // 2, w, h, _p(_r(text, i=True)), fill="FFFFFF", border=False)


def _edge(e):
    """Returns (connector_xml, label_xml, label_z). Pinned when the edge carries
    a `conn`; otherwise routed by the fallback orthogonal router."""
    if "conn" in e:                                          # GOLD: pinned geometry
        conn = _conn(**e["conn"], dashed=e.get("dashed", False), arrow=e.get("arrow", True))
        if e.get("label") and e.get("label_box"):
            label = _edge_label_box(e["label"], e["label_box"])
        elif e.get("label"):                                 # pinned conn, auto chip
            c = e["conn"]; at = (c["x"] + c["cx"] // 2, c["y"] + c["cy"] // 2)
            label = _edge_label(e["label"], at, e.get("label_w"))
        else:
            label = ""
        return conn, label, e.get("label_z", 0)
    # NEW: route from src/dst with the fallback router
    src, dst = NODES[e["src"]], NODES[e["dst"]]
    ds, dd = _default_sides(src, dst)
    s0 = e.get("src_side", ds); s1 = e.get("dst_side", dd)
    p0 = _anchor(src, s0, e.get("src_pos", 0.5))
    p1 = _anchor(dst, s1, e.get("dst_pos", 0.5))
    if e.get("via"):
        pts = _dedupe([p0] + [tuple(v) for v in e["via"]] + [p1])
    elif e.get("straight"):
        pts = [p0, p1]
    else:
        pts = _route(p0, s0, p1, s1, e.get("mid", 0.5))
    conn = _edge_conn(pts, dashed=e.get("dashed", False), arrow=e.get("arrow", True))
    label = _edge_label(e["label"], _longest_mid(pts), e.get("label_w")) if e.get("label") else ""
    return conn, label, e.get("label_z", 0)


# ── static chrome / annotations (not part of the node/edge graph) ────────────
_TITLE_PH = ('<p:sp><p:nvSpPr><p:cNvPr id="304" name="Title 3"/>'
             '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/></p:nvPr>'
             '</p:nvSpPr><p:spPr><a:xfrm><a:off x="452437" y="566399"/>'
             '<a:ext cx="11283696" cy="640080"/></a:xfrm></p:spPr><p:txBody>'
             '<a:bodyPr vert="horz" rIns="0"/><a:lstStyle/><a:p><a:pPr marL="0"/>'
             '<a:r><a:rPr lang="en-US" b="1" dirty="0"><a:solidFill><a:srgbClr val="000000"/>'
             '</a:solidFill></a:rPr><a:t>Flow Charts</a:t></a:r></a:p></p:txBody></p:sp>')

_TEXT_PH = ('<p:sp><p:nvSpPr><p:cNvPr id="310" name="Text Placeholder 1"/>'
            '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="body" sz="quarter" idx="10"/></p:nvPr></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="452701" y="263452"/><a:ext cx="5394960" cy="155448"/>'
            '</a:xfrm></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p>'
            '<a:r><a:rPr lang="en-US" b="1"/><a:t>Strategy Materials Style Guide</a:t></a:r>'
            '</a:p></p:txBody></p:sp>')

def _band():    # pale band behind the bottom PRC-tier row
    return _box(2480928, 5978984, 7427429, 453091, '<a:p><a:pPr algn="ctr"/></a:p>', fill="DFE7EB")

def _notes():
    return (_box(158654, 6082520, 756272, 293688, _p(_r("+ ROW", b=True)), fill=None, border=False)
            + _box(127318, 1024477, 2816720, 224437, _p(_r("Chart reads from bottom to top", i=True), algn=None),
                   fill=None, border=False))

_FLAGS = [
    dict(x=262470, y=5644688, w=548640, h=365760),
    dict(x=189481, y=1662271, w=694619, h=365760),
    dict(x=189481, y=2989743, w=694619, h=365760),
    dict(x=189481, y=4317215, w=694619, h=365760),
]

def _annotations() -> str:
    outline = _box(8919131, 1296511, 2816720, 544068,
                   _p(_r("Vessel and Shipyard Investment Tax Credits (40% and 25%, respectively) "
                         "from Building Ships in America Act not shown", i=True)),
                   fill=None, border=True)
    callout = (f'<p:sp><p:nvSpPr><p:cNvPr id="{_nid()}" name="callout"/><p:cNvSpPr/><p:nvPr/>'
               f'</p:nvSpPr><p:spPr><a:xfrm><a:off x="4215618" y="1986880"/>'
               f'<a:ext cx="1790366" cy="466140"/></a:xfrm>'
               f'<a:prstGeom prst="wedgeRectCallout"><a:avLst>'
               f'<a:gd name="adj1" fmla="val 41650"/><a:gd name="adj2" fmla="val 74944"/></a:avLst>'
               f'</a:prstGeom><a:noFill/><a:ln w="12700"><a:solidFill><a:srgbClr val="000000"/>'
               f'</a:solidFill></a:ln></p:spPr><p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/>'
               f'<a:lstStyle/>{_p(_r("US crew required to participate in SCF, which states vessels will be crewed IAW 46 USC 8103 ", sz=800, i=True))}'
               f'</p:txBody></p:sp>')
    flags = "".join(_box(f["x"], f["y"], f["w"], f["h"], _p(_r("flag", sz=800, i=True, color="7F7F7F")),
                         fill="F2F2F2", border=True) for f in _FLAGS)
    return outline + callout + flags


def _body() -> str:
    boxes = "".join(_box(n["x"], n["y"], n["w"], n["h"], n["para"], fill=n["fill"]) for n in NODES.values())
    conns, labels = [], []
    for e in EDGES:
        c, l, z = _edge(e)
        conns.append(c)
        if l:
            labels.append((z, l))
    labels.sort(key=lambda t: t[0])                          # source stacking order
    # paint order: chrome -> band -> boxes -> connectors -> labels (mask lines)
    #              -> notes -> static annotations + flags
    return (_TITLE_PH + _TEXT_PH + _band() + boxes
            + "".join(conns) + "".join(l for _, l in labels) + _notes() + _annotations())


def render() -> str:
    return slide(_body())
