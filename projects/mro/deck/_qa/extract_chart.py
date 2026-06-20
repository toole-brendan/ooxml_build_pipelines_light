"""Extract a slide's think-cell-emitted chart shapes as cleaned STATIC OOXML.

think-cell draws its charts as ordinary native shapes (accent-filled rectangles
for the bar segments, <p:cxnSp> connectors for the axes, text placeholders whose
labels live in <a:fld> fields) alongside an opaque OLE blob named
"think-cell data - do not delete". This tool keeps the *visual* shapes and drops
the OLE, producing a faithful, fully static reproduction of the chart that no
longer depends on the think-cell add-in.

Usage:
    python extract_chart.py <N> --keepout 2,5,6,7,9,67 [--offset 300] > out.xml

--keepout : cNvPr ids you rebuild as deck_core primitives instead (chrome /
            table / caption / footer) -- these are skipped here.
--offset  : added to every cNvPr id so the chart shapes can't collide with the
            chrome ids (breadcrumb=2, title=3, prelim=4, sources=9999) or the
            module's own primitive ids.

Per shape the cleaner: strips think-cell custData / creationId / hiddenFill
extLst and the bulky inherited <a:lstStyle>; rewrites every <a:fld> (a bogus
type="datetime..." field holding cached label text) into a plain static <a:r>
run so PowerPoint can never refresh it to today's date; renumbers the cNvPr id.
The source theme is byte-identical to infra/template, so schemeClr accentN refs
are kept as-is (they resolve to the same hexes).
"""
import colorsys
import re
import sys
from xml.etree import ElementTree as ET

# Source theme1.xml clrScheme resolved through the master clrMap
# (tx1->dk1, bg1->lt1, tx2->dk2, bg2->lt2). Theme is byte-identical to
# infra/template, so these hexes are authoritative for both decks.
_THEME = {
    'dk1': '162029', 'lt1': 'FFFFFF', 'dk2': '44505C', 'lt2': 'F2F6FA',
    'tx1': '162029', 'bg1': 'FFFFFF', 'tx2': '44505C', 'bg2': 'F2F6FA',
    'accent1': '79838F', 'accent2': '1D4D68', 'accent3': '486D82',
    'accent4': '89A2B0', 'accent5': 'AFC2CC', 'accent6': 'D8E3EB',
    'hlink': '1D4D68', 'folHlink': '89A2B0',
}

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
SHAPE_TAGS = ('sp', 'cxnSp', 'pic', 'grpSp')
# Built-in "No Style, No Grid" table style (same GUID deck_core.table() uses): a
# verbatim source table keeps its explicit per-cell fills/borders but picks up no
# theme grid lines, and needs no tableStyles.xml entry to resolve.
NO_STYLE_NO_GRID = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def find_close(s, start, tag):
    """Index just past the </p:tag> matching the <p:tag> at `start`, counting
    nested same-tag opens. Self-closing shape containers don't occur here."""
    open_tok, close_tok = f'<p:{tag}', f'</p:{tag}>'
    depth, i = 0, start
    while i < len(s):
        if s.startswith(close_tok, i):
            depth -= 1
            i += len(close_tok)
            if depth == 0:
                return i
        elif s.startswith(open_tok, i) and not s[i + len(open_tok)].isalnum():
            depth += 1
            i += len(open_tok)
        else:
            i += 1
    return i


def top_shapes(inner):
    """Yield (tag, raw_xml) for each top-level child of the spTree."""
    i, n = 0, len(inner)
    while i < n:
        if inner[i] != '<':
            i += 1
            continue
        m = re.match(r'<p:(\w+)', inner[i:])
        if not m:
            i += 1
            continue
        tag = m.group(1)
        end = find_close(inner, i, tag)
        yield tag, inner[i:end]
        i = end


def _fld_to_run(m):
    inner = m.group(1)
    rm = (re.search(r'<a:rPr\b[^>]*?>.*?</a:rPr>', inner, re.S)
          or re.search(r'<a:rPr\b[^>]*?/>', inner))
    tm = re.search(r'<a:t>.*?</a:t>', inner, re.S)
    rpr = rm.group(0) if rm else '<a:rPr lang="en-US"/>'
    t = tm.group(0) if tm else '<a:t></a:t>'
    return f'<a:r>{rpr}{t}</a:r>'


def _renumber(xml, offset):
    return re.sub(r'(<p:cNvPr id=")(\d+)(")',
                  lambda m: f'{m.group(1)}{int(m.group(2)) + offset}{m.group(3)}', xml)


def _apply_lum(hex6, lummod, lumoff):
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.0, min(1.0, l * lummod + lumoff))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))


def _resolve_scheme_lum(xml):
    """Flatten <a:schemeClr val="X"><a:lumMod/><a:lumOff/></a:schemeClr> to a
    literal <a:srgbClr val="HEX"/>. soffice mis-renders schemeClr+lumOff (it
    darkens instead of lightening), and the result is renderer-dependent; baking
    the HLS lum transform into an explicit hex makes the fill render identically in
    soffice and PowerPoint. Only schemeClr carrying lumMod/lumOff is touched -
    plain schemeClr refs (theme-identical) and shade/tint in <p:style> are left."""
    def repl(m):
        val, inner = m.group(1), m.group(2)
        if 'lumMod' not in inner and 'lumOff' not in inner:
            return m.group(0)
        base = _THEME.get(val)
        if not base:
            return m.group(0)
        lm = re.search(r'<a:lumMod val="(\d+)"/>', inner)
        lo = re.search(r'<a:lumOff val="(\d+)"/>', inner)
        lummod = int(lm.group(1)) / 100000 if lm else 1.0
        lumoff = int(lo.group(1)) / 100000 if lo else 0.0
        return f'<a:srgbClr val="{_apply_lum(base, lummod, lumoff)}"/>'
    return re.sub(r'<a:schemeClr val="([^"]+)">((?:(?!</a:schemeClr>).)*)</a:schemeClr>',
                  repl, xml, flags=re.S)


def _strip_hlinks(xml):
    """Drop hyperlink refs. <a:hlinkClick>/<a:hlinkHover> anchor to a slide rel by
    r:id we don't carry over; the run's own rPr fill already fixes the visible
    color, so removing the link leaves the text identical but self-contained."""
    xml = re.sub(r'<a:hlinkClick\b[^>]*/>', '', xml)
    xml = re.sub(r'<a:hlinkClick\b[^>]*>.*?</a:hlinkClick>', '', xml, flags=re.S)
    xml = re.sub(r'<a:hlinkHover\b[^>]*/>', '', xml)
    return xml


def clean(xml, offset):
    xml = re.sub(r'<a:extLst>.*?</a:extLst>', '', xml, flags=re.S)
    xml = re.sub(r'<p:custDataLst>.*?</p:custDataLst>', '', xml, flags=re.S)
    xml = re.sub(r'<a:lstStyle>.*?</a:lstStyle>', '', xml, flags=re.S)
    xml = re.sub(r'<a:fld\b[^>]*>(.*?)</a:fld>', _fld_to_run, xml, flags=re.S)
    # Drop connector glue: stCxn/endCxn anchor a cxnSp to other shapes BY ID, but
    # we renumber ids (+offset) so the glue would dangle. Stripping it makes the
    # connector render statically from its own xfrm (off/ext/rot/flip), which is
    # exact. (cxnSpLocks left as-is; harmless.)
    xml = re.sub(r'<a:stCxn\b[^>]*/>', '', xml)
    xml = re.sub(r'<a:endCxn\b[^>]*/>', '', xml)
    return _renumber(_strip_hlinks(_resolve_scheme_lum(xml)), offset)


def clean_table(xml, offset):
    """A source <a:tbl> graphicFrame, made static + self-contained: strip the
    dsbld cellmeta / creationId extLst and any custData, and swap the source's
    custom tableStyleId for the built-in no-grid style so it renders with only
    its explicit per-cell borders (no missing-style fallback grid)."""
    xml = re.sub(r'<a:extLst>.*?</a:extLst>', '', xml, flags=re.S)
    xml = re.sub(r'<p:extLst>.*?</p:extLst>', '', xml, flags=re.S)
    xml = re.sub(r'<p:custDataLst>.*?</p:custDataLst>', '', xml, flags=re.S)
    xml = re.sub(r'<a:tableStyleId>[^<]*</a:tableStyleId>',
                 f'<a:tableStyleId>{NO_STYLE_NO_GRID}</a:tableStyleId>', xml)
    return _renumber(_strip_hlinks(_resolve_scheme_lum(xml)), offset)


def cnvpr_id(xml):
    m = re.search(r'<p:cNvPr id="(\d+)"', xml)
    return int(m.group(1)) if m else None


def main():
    n = sys.argv[1]
    keepout, tables, offset = set(), set(), 300
    for i, a in enumerate(sys.argv):
        if a == '--keepout':
            keepout = {int(x) for x in sys.argv[i + 1].split(',') if x.strip()}
        elif a == '--tables':
            tables = {int(x) for x in sys.argv[i + 1].split(',') if x.strip()}
        elif a == '--offset':
            offset = int(sys.argv[i + 1])
    raw = open(f'src_xml/ppt/slides/slide{n}.xml', encoding='utf-8').read()
    mt = re.search(r'<p:spTree>(.*)</p:spTree>', raw, re.S)
    inner = mt.group(1)

    # --tables mode: emit ONLY the named table graphicFrame(s), verbatim+cleaned.
    # Default mode: emit the chart shapes (sp/cxnSp/pic/grpSp), dropping the OLE
    # graphicFrame and the keep-out (chrome/table/caption/footer) shapes.
    out, kept = [], 0
    for tag, xml in top_shapes(inner):
        sid = cnvpr_id(xml)
        if tables:
            if tag == 'graphicFrame' and sid in tables:
                out.append(clean_table(xml, offset))
                kept += 1
            continue
        if tag not in SHAPE_TAGS or sid in keepout:
            continue
        out.append(clean(xml, offset))
        kept += 1
    result = "".join(out)

    # validate: must parse, and must carry no dangling rels refs or live fields
    test = (f'<root xmlns:a="{A}" xmlns:p="{P}" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'{result}</root>')
    ET.fromstring(test)
    leftover_rid = len(re.findall(r'r:(id|embed)=', result))
    leftover_fld = len(re.findall(r'<a:fld\b', result))

    sys.stderr.write(f"kept {kept} chart shapes; r:id/embed refs={leftover_rid}; "
                     f"live <a:fld>={leftover_fld}\n")
    if leftover_rid or leftover_fld:
        sys.stderr.write("WARNING: dangling rels ref or live field remains\n")
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
