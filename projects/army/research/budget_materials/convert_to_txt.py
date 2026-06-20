#!/usr/bin/env python3
"""Convert every PDF under pdf_originals/ to a layout-preserving .txt mirror under txt_versions/.

Settings chosen for these budget exhibits (mixed prose + dense funding tables):
  pdftotext -layout   keep physical column geometry so a line item's label stays on the
                      same line as its P-1 line number, quantity and dollar figures.
  -enc UTF-8          clean em-dashes / special glyphs for AI ingestion.
  -eol unix           consistent line endings.
Form-feed page breaks (emitted by pdftotext) are converted into explicit
"===== PAGE N =====" markers (N = physical PDF page) so an agent can cite an exact page
without reopening the PDF. The book's own printed "Volume X - NNN" labels remain inline.

Also augments _manifest.csv with txt_path / txt_bytes / txt_pages columns.
"""
import csv, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(ROOT, "pdf_originals")
TXT_DIR = os.path.join(ROOT, "txt_versions")
MANIFEST = os.path.join(ROOT, "_manifest.csv")

def convert(pdf_path):
    """Return (text_with_markers, n_pages)."""
    out = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", "-eol", "unix", pdf_path, "-"],
        capture_output=True, timeout=300)
    raw = out.stdout.decode("utf-8", "replace")
    pages = raw.split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]                      # drop trailing empty chunk after final \f
    chunks = []
    for i, p in enumerate(pages, 1):
        chunks.append(f"===== PAGE {i} =====\n{p.rstrip(chr(10))}\n")
    return "\n".join(chunks), len(pages)

# ---- convert all ------------------------------------------------------------
txt_info = {}   # pdf_rel -> (txt_rel, txt_bytes, n_pages)
n = empties = 0
for dirpath, _, files in os.walk(PDF_DIR):
    for fn in sorted(files):
        if not fn.lower().endswith(".pdf"):
            continue
        pdf_path = os.path.join(dirpath, fn)
        pdf_rel = os.path.relpath(pdf_path, ROOT)
        txt_rel = pdf_rel.replace("pdf_originals/", "txt_versions/", 1)[:-4] + ".txt"
        txt_path = os.path.join(ROOT, txt_rel)
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        text, pages = convert(pdf_path)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        sz = os.path.getsize(txt_path)
        txt_info[pdf_rel] = (txt_rel, sz, pages)
        if sz < 500:
            empties += 1
            print(f"  WARN empty-ish  {txt_rel}  ({sz} B)")
        n += 1
        print(f"  ok  {txt_rel:54s} {pages:>4d} pp  {sz//1024:>6d} KB")

# ---- augment manifest -------------------------------------------------------
with open(MANIFEST, newline="") as f:
    rows = list(csv.reader(f))
header, data = rows[0], rows[1:]
rp_i = header.index("rel_path")
for col in ("txt_path", "txt_bytes", "txt_pages"):
    if col not in header:
        header.append(col)
tp_i, tb_i, tg_i = (header.index(c) for c in ("txt_path", "txt_bytes", "txt_pages"))
for r in data:
    while len(r) < len(header):
        r.append("")
    info = txt_info.get(r[rp_i])
    if info:
        r[tp_i], r[tb_i], r[tg_i] = info[0], info[1], info[2]
with open(MANIFEST, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(data)

print(f"\nDONE  converted={n}  empty_warnings={empties}  txt_versions/ ready")
