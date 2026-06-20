"""Dump a source slide's shape tree: geometry (EMU), fill/line, text, tables.
Usage: [SRC=src_xml_v3] python dump_slide.py <slideN>   (SRC defaults to src_xml)"""
import os, sys, re
from xml.etree import ElementTree as ET

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
def q(ns, t): return f'{{{ns}}}{t}'

n = sys.argv[1]
path = f"{os.environ.get('SRC', 'src_xml')}/ppt/slides/slide{n}.xml"
root = ET.parse(path).getroot()

def emu_in(v):
    try: return f"{int(v)/914400:.2f}in"
    except: return v

def fill_of(spPr):
    if spPr is None: return None
    sf = spPr.find(q(A,'solidFill'))
    if sf is not None:
        c = sf.find(q(A,'srgbClr'))
        if c is not None: return f"#{c.get('val')}"
        sc = sf.find(q(A,'schemeClr'))
        if sc is not None: return f"scheme:{sc.get('val')}"
    if spPr.find(q(A,'noFill')) is not None: return "none"
    grad = spPr.find(q(A,'gradFill'))
    if grad is not None: return "gradient"
    return None

def geom_of(spPr):
    if spPr is None: return ("","")
    g = spPr.find(q(A,'prstGeom'))
    prst = g.get('prst') if g is not None else ("custom" if spPr.find(q(A,'custGeom')) is not None else "")
    xfrm = spPr.find(q(A,'xfrm'))
    if xfrm is None: return (prst, "")
    off = xfrm.find(q(A,'off')); ext = xfrm.find(q(A,'ext'))
    g = ""
    if off is not None and ext is not None:
        g = f"x={off.get('x')} y={off.get('y')} ({emu_in(off.get('x'))},{emu_in(off.get('y'))}) cx={ext.get('cx')} cy={ext.get('cy')} ({emu_in(ext.get('cx'))}x{emu_in(ext.get('cy'))})"
    return (prst, g)

def text_of(txBody):
    if txBody is None: return []
    out = []
    for p in txBody.findall(q(A,'p')):
        runs = []
        pPr = p.find(q(A,'pPr'))
        algn = pPr.get('algn') if pPr is not None else None
        lvl = pPr.get('lvl') if pPr is not None else None
        for r in p.findall(q(A,'r')):
            rPr = r.find(q(A,'rPr'))
            t = r.find(q(A,'t'))
            txt = t.text if t is not None else ""
            props = []
            if rPr is not None:
                if rPr.get('sz'): props.append(f"{int(rPr.get('sz'))/100}pt")
                if rPr.get('b')=='1': props.append("b")
                if rPr.get('i')=='1': props.append("i")
                sf = rPr.find(q(A,'solidFill'))
                if sf is not None:
                    c = sf.find(q(A,'srgbClr'))
                    if c is not None: props.append(f"#{c.get('val')}")
            runs.append((txt, ",".join(props)))
        if runs or algn:
            out.append((algn, lvl, runs))
    return out

def walk(sp, depth=0):
    ind = "  "*depth
    tag = sp.tag.split('}')[-1]
    if tag in ('sp','pic','cxnSp','graphicFrame'):
        nv = sp.find('.//'+q(P,'cNvPr'))
        name = nv.get('name') if nv is not None else "?"
        nid = nv.get('id') if nv is not None else "?"
        spPr = sp.find(q(P,'spPr'))
        prst, g = geom_of(spPr)
        fill = fill_of(spPr)
        # placeholder?
        ph = sp.find('.//'+q(P,'ph'))
        phs = f" PH[{ph.get('type')},idx={ph.get('idx')}]" if ph is not None else ""
        # graphicFrame xfrm lives differently
        if tag == 'graphicFrame':
            xfrm = sp.find(q(P,'xfrm'))
            if xfrm is not None:
                off=xfrm.find(q(A,'off')); ext=xfrm.find(q(A,'ext'))
                g = f"x={off.get('x')} y={off.get('y')} cx={ext.get('cx')} cy={ext.get('cy')} ({emu_in(off.get('x'))},{emu_in(off.get('y'))} {emu_in(ext.get('cx'))}x{emu_in(ext.get('cy'))})"
            tbl = sp.find('.//'+q(A,'tbl'))
            graphic = sp.find('.//'+q(A,'graphic'))
            kind = "TABLE" if tbl is not None else "GRAPHIC"
            print(f"{ind}[{tag}:{kind}] id={nid} '{name}'{phs}  {g}")
            if tbl is not None:
                grid = tbl.find(q(A,'tblGrid'))
                cols = [c.get('w') for c in grid.findall(q(A,'gridCol'))]
                print(f"{ind}  cols(EMU)={cols}  ({[emu_in(c) for c in cols]})")
                for ri, tr in enumerate(tbl.findall(q(A,'tr'))):
                    h = tr.get('h')
                    cells=[]
                    for tc in tr.findall(q(A,'tc')):
                        gs = tc.get('gridSpan'); hm = tc.get('hMerge'); rs=tc.get('rowSpan'); vm=tc.get('vMerge')
                        tcPr = tc.find(q(A,'tcPr'))
                        cfill = fill_of(tcPr) if tcPr is not None else None
                        txt = " | ".join("".join(r[0] for r in runs) for _,_,runs in text_of(tc.find(q(A,'txBody'))))
                        meta = ""
                        if gs: meta+=f"span{gs}"
                        if hm: meta+="hM"
                        if rs: meta+=f"rs{rs}"
                        if vm: meta+="vM"
                        cf = f"[{cfill}]" if cfill else ""
                        cells.append(f"{cf}{meta}:{txt}")
                    print(f"{ind}  r{ri}(h={h}): " + " || ".join(cells))
            return
        line = spPr.find(q(A,'ln')) if spPr is not None else None
        lninfo = ""
        if line is not None:
            lw = line.get('w'); lf = fill_of(line)
            lninfo = f" line(w={lw},{lf})"
        print(f"{ind}[{tag}] id={nid} '{name}'{phs} prst={prst} fill={fill}{lninfo}  {g}")
        txt = text_of(sp.find(q(P,'txBody')))
        for algn,lvl,runs in txt:
            rstr = "  ".join(f'"{t}"({p})' if p else f'"{t}"' for t,p in runs)
            a = f"[{algn}]" if algn else ""
            l = f"L{lvl}" if lvl else ""
            if rstr.strip(' "'): print(f"{ind}    {a}{l} {rstr}")
    # recurse into group shapes
    for child in sp:
        if child.tag.split('}')[-1] in ('sp','pic','cxnSp','graphicFrame','grpSp'):
            walk(child, depth+1)

spTree = root.find(q(P,'cSld')+'/'+q(P,'spTree'))
for sp in spTree:
    t = sp.tag.split('}')[-1]
    if t in ('sp','pic','cxnSp','graphicFrame','grpSp'):
        walk(sp)
