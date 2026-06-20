"""Extract named top-level <p:pic> shapes from a source slide, verbatim but
made self-contained: strip extLst (creationId), remap each blip r:embed to a
controlled slide rId, renumber the cNvPr id (+offset). Preserves the source
geometry AND effects (drop shadow, etc.) that picture() would not reproduce.

Usage:
    python extract_pics.py <N> --ids 56 --embeds rId3 [--offset 300] > out.xml
    # ids and embeds are parallel comma lists (id[i] gets embeds[i]).

Pair with a module IMAGES = [{"rId": "rIdN", "file": "<media name>"}, ...] whose
rIds match --embeds; build_pptx wires the per-slide image rel + copies the bytes.
"""
import os
import re
import sys

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'


def find_close(s, start, tag):
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


def main():
    n = sys.argv[1]
    ids, embeds, offset = [], [], 300
    for i, a in enumerate(sys.argv):
        if a == '--ids':
            ids = [int(x) for x in sys.argv[i + 1].split(',') if x.strip()]
        elif a == '--embeds':
            embeds = [x for x in sys.argv[i + 1].split(',') if x.strip()]
        elif a == '--offset':
            offset = int(sys.argv[i + 1])
    assert len(ids) == len(embeds), "ids and embeds must be parallel"
    want = dict(zip(ids, embeds))
    src = os.environ.get('SRC', 'src_xml')
    raw = open(f'{src}/ppt/slides/slide{n}.xml', encoding='utf-8').read()
    inner = re.search(r'<p:spTree>(.*)</p:spTree>', raw, re.S).group(1)

    out = []
    i, m = 0, len(inner)
    while i < m:
        if inner.startswith('<p:pic', i) and not inner[i + 6].isalnum():
            end = find_close(inner, i, 'pic')
            pic = inner[i:end]
            sid = int(re.search(r'<p:cNvPr id="(\d+)"', pic).group(1))
            if sid in want:
                pic = re.sub(r'<a:extLst>.*?</a:extLst>', '', pic, flags=re.S)
                pic = re.sub(r'(<a:blip[^>]*r:embed=")[^"]+(")',
                             lambda mm: f'{mm.group(1)}{want[sid]}{mm.group(2)}', pic)
                pic = re.sub(r'(<p:cNvPr id=")(\d+)(")',
                             lambda mm: f'{mm.group(1)}{int(mm.group(2)) + offset}{mm.group(3)}', pic)
                out.append(pic)
            i = end
        else:
            i += 1
    sys.stderr.write(f"slide{n}: extracted {len(out)}/{len(want)} pics; "
                     f"remaining src embeds: {len(re.findall(r'r:embed', ''.join(out)))}\n")
    sys.stdout.write(''.join(out))


if __name__ == "__main__":
    main()
