#!/usr/bin/env python3
"""Download the FY2027 (PB-2027) Department of the Navy budget justification books.

Source: Navy Office of Budget (FMB)  ->  https://www.secnav.navy.mil/fmc/fmb/Documents/27pres/

The FMB listing page (Fiscal-Year-2027.aspx) sits behind a JavaScript bot-management
interstitial that a plain curl cannot clear, but the static PDFs under Documents/27pres/
are directly fetchable with a full browser header set. Rapid-fire requests trip a
connection-reset throttle, so we pace requests (DELAY) and back off on resets.

Exact filenames were confirmed by direct probe + web search (Jun 2026). A few long-tail
books (Marine Corps O&M, the four military-personnel books, Family Housing, NWCF) publish
every year but were not yet search-indexed for FY27; they are listed as candidates and the
download run is the source of truth -- a miss is logged to _manifest_navy_fy27.csv, not fatal.
SCN is already on disk from an earlier pull and is skipped.

Local files follow the existing SCN convention in this folder:  <navy stem>_FY27.pdf
(e.g. SCN_Book.pdf -> SCN_Book_FY27.pdf) plus a layout-preserving .txt sibling
(pdftotext -layout, form-feed page breaks) exactly like SCN_Book_FY27.txt.
"""
import csv, hashlib, os, subprocess, time

ROOT = os.path.dirname(os.path.abspath(__file__))     # the budget_books/ folder (flat)
BASE = "https://www.secnav.navy.mil/fmc/fmb/Documents/27pres"
REFERER = "https://www.secnav.navy.mil/fmc/fmb/Pages/Fiscal-Year-2027.aspx"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
DELAY = 3.0          # polite spacing between books (the host resets on rapid fire)
RETRIES = 3          # per-URL attempts, with linear backoff, on connection reset / 000

# ---- the book list ----------------------------------------------------------
# (tier, appropriation, [candidate navy stems])  -- first candidate names the local file;
# extra candidates cover naming drift (e.g. MCON vs MILCON, FHN vs FH).
BOOKS = [
    # ---- Procurement ----
    ("Procurement", "APN",   ["APN_BA1-4_Book"]),     # Aircraft Procurement, Navy  (BA01-04: combat/airlift/trainer/other)
    ("Procurement", "APN",   ["APN_BA5_Book"]),       #   (BA05: modification of aircraft)
    ("Procurement", "APN",   ["APN_BA6-7_Book"]),      #   (BA06-07: spares & repair parts; support equip & facilities)
    ("Procurement", "WPN",   ["WPN_Book"]),           # Weapons Procurement, Navy
    ("Procurement", "PANMC", ["PANMC_Book"]),         # Procurement of Ammunition, Navy & Marine Corps
    ("Procurement", "SCN",   ["SCN_Book"]),           # Shipbuilding & Conversion, Navy  (already on disk)
    ("Procurement", "OPN",   ["OPN_BA1_Book"]),       # Other Procurement, Navy  (BA1 ships support)
    ("Procurement", "OPN",   ["OPN_BA2_Book"]),       #   (BA2 comms & electronics)
    ("Procurement", "OPN",   ["OPN_BA3_Book"]),       #   (BA3 aviation support)
    ("Procurement", "OPN",   ["OPN_BA4_Book"]),       #   (BA4 ordnance support)
    ("Procurement", "OPN",   ["OPN_BA5-8_Book"]),     #   (BA5-8: personnel/command support + spares & repair parts, one volume)
    ("Procurement", "PMC",   ["PMC_Book"]),           # Procurement, Marine Corps
    # ---- RDT&E, Navy ----
    ("RDT&E", "RDTEN", ["RDTEN_BA1-3_Book"]),         # Research, Development, Test & Evaluation, Navy
    ("RDT&E", "RDTEN", ["RDTEN_BA4_Book"]),
    ("RDT&E", "RDTEN", ["RDTEN_BA5_Book"]),
    ("RDT&E", "RDTEN", ["RDTEN_BA6_Book"]),
    ("RDT&E", "RDTEN", ["RDTEN_BA7-8_Book"]),
    # ---- Operation & Maintenance ----
    ("O&M", "OMN",   ["OMN_Book"]),                   # Operation & Maintenance, Navy  (Vol 1)
    ("O&M", "OMN",   ["OMN_Vol2_Book"]),              #   (Vol 2: BA4 admin & servicewide)
    ("O&M", "OMNR",  ["OMNR_Book"]),                  # O&M, Navy Reserve
    ("O&M", "OMMC",  ["OMMC_Book"]),                  # O&M, Marine Corps          (candidate)
    ("O&M", "OMMCR", ["OMMCR_Book"]),                 # O&M, Marine Corps Reserve  (candidate)
    # ---- Military Personnel ----
    ("MilPers", "MPN",  ["MPN_Book"]),                # Military Personnel, Navy          (candidate)
    ("MilPers", "RPN",  ["RPN_Book"]),                # Reserve Personnel, Navy           (candidate)
    ("MilPers", "MPMC", ["MPMC_Book"]),               # Military Personnel, Marine Corps  (candidate)
    ("MilPers", "RPMC", ["RPMC_Book"]),               # Reserve Personnel, Marine Corps   (candidate)
    # ---- Military Construction / Family Housing ----
    # Navy has no standalone Family Housing book for FY27 -- "Part 4: Family Housing" is
    # bound inside MCON_Book (verified). MCON_Book covers Military Construction + Family Housing.
    ("MilCon", "MCON", ["MCON_Book", "MILCON_Book"]),   # Military Construction & Family Housing, Navy
    # ---- Working Capital Fund ----
    ("WCF", "NWCF", ["NWCF_Book"]),                   # Navy Working Capital Fund (candidate)
    # ---- Department-level overview ----
    ("Overview", "Highlights", ["Highlights_Book"]),  # DON budget Highlights book
    ("Overview", "PressBrief", ["DON_Press_Brief"]),  # DON press brief deck
]

# ---- fetch helpers ----------------------------------------------------------
def curl(url, dest_tmp):
    cmd = ["curl", "-sS", "-L", "--compressed", "-A", UA,
           "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
           "-H", "Accept-Language: en-US,en;q=0.9",
           "-H", f"Referer: {REFERER}",
           "-H", "Sec-Fetch-Dest: document", "-H", "Sec-Fetch-Mode: navigate",
           "-H", "Sec-Fetch-Site: same-origin", "-H", "Upgrade-Insecure-Requests: 1",
           "--max-time", "180", "-o", dest_tmp,
           "-w", "%{http_code} %{size_download}", url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=240).stdout.strip()
        code, size = out.split()
        return int(code), int(size)
    except Exception:
        return -1, 0

def is_pdf(path):
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False

def pages(path):
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True, timeout=30).stdout
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1])
    except Exception:
        pass
    return ""

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]

def to_txt(pdf_path):
    """Layout-preserving .txt mirror (form-feed page breaks), matching SCN_Book_FY27.txt."""
    txt_path = pdf_path[:-4] + ".txt"
    subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", "-eol", "unix", pdf_path, txt_path],
                   capture_output=True, timeout=300)
    return txt_path

# ---- run --------------------------------------------------------------------
rows = []
hits = misses = skipped = 0
for tier, approp, cands in BOOKS:
    primary = cands[0]
    dest = os.path.join(ROOT, primary + "_FY27.pdf")
    if os.path.exists(dest) and is_pdf(dest):
        skipped += 1
        rows.append([tier, approp, primary, "HAVE", "", os.path.getsize(dest), pages(dest),
                     sha256(dest), os.path.basename(dest), os.path.basename(dest)[:-4] + ".txt",
                     "already on disk"])
        print(f"  skip  {primary:22s} (already have)")
        continue

    got = got_stem = None
    for stem in cands:
        url = f"{BASE}/{stem}.pdf"
        tmp = os.path.join(ROOT, stem + "_FY27.pdf.part")
        for attempt in range(1, RETRIES + 1):
            code, size = curl(url, tmp)
            if code == 200 and is_pdf(tmp) and size > 50000:
                got, got_stem = url, stem
                break
            if os.path.exists(tmp):
                os.remove(tmp)
            if code in (-1, 0):                      # connection reset / throttle -> back off
                time.sleep(DELAY * attempt * 2)
            else:
                break                                # a real 200-HTML / 404 -> next candidate
        if got:
            break
        time.sleep(DELAY)

    if got:
        final = os.path.join(ROOT, got_stem + "_FY27.pdf")
        os.replace(os.path.join(ROOT, got_stem + "_FY27.pdf.part"), final)
        txt = to_txt(final)
        hits += 1
        print(f"  OK    {got_stem + '_FY27.pdf':30s} {os.path.getsize(final)//1024:>6d} KB  "
              f"{pages(final)} pp  -> {os.path.basename(txt)}")
        rows.append([tier, approp, got_stem, "OK", 200, os.path.getsize(final), pages(final),
                     sha256(final), os.path.basename(final), os.path.basename(txt), got])
    else:
        misses += 1
        print(f"  MISS  {approp:6s} {primary:22s} tried {', '.join(cands)}")
        rows.append([tier, approp, primary, "MISS", "", "", "", "", "", "",
                     " | ".join(f"{BASE}/{s}.pdf" for s in cands)])
    time.sleep(DELAY)

with open(os.path.join(ROOT, "_manifest_navy_fy27.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tier", "appropriation", "book_id", "status", "http", "bytes",
                "pages", "sha256_16", "pdf_file", "txt_file", "source_url"])
    w.writerows(rows)

print(f"\nDONE  hits={hits}  misses={misses}  already_had={skipped}  total={len(BOOKS)}")
