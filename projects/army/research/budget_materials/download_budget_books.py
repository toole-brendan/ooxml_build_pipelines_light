#!/usr/bin/env python3
"""Download Army budget justification books for the autonomous-watercraft market study.

Scope (the "Recommended corpus"):
  Tier 1 - OPA Other Procurement, Army (watercraft procurement):                FY22-FY27
           * BA1 - Tactical & Support Vehicles: carries the appropriation-wide P-1 index only.
           * BA3&4 (Vol 3) - Other Support Equipment & Spares: the actual watercraft line-item
             DETAIL (Army Watercraft Esp 3569M11101, MSV 8211R01001, Float/Rail <$5M) lives here.
  Tier 2 - RDT&E volumes carrying autonomy / prototyping / contested logistics:
           Budget Activities 3, 4A, 4B, 5A, 5D, 7.                                FY22-FY27
  Tier 3 - OMA Volume 1 (Operating Forces): watercraft sustainment + Composite
           Watercraft Company stand-up.                                          FY25-FY27
  Index  - DoD-wide consolidated P-1 / R-1 / O-1 from OSD Comptroller.           FY27 only

The asafm.army.mil host sits behind Akamai bot management: bare requests 403, a full
browser header set passes. Filenames drift year to year, so each book carries several
candidate URLs (incl. volume-number fallbacks); the first that returns a real PDF wins.
Misses are logged to _manifest.csv with status=MISS for manual follow-up.
"""
import csv, hashlib, os, subprocess, time
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(ROOT, "pdf_originals")   # downloaded PDFs live here
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
ASAFM = "https://www.asafm.army.mil/Portals/72/Documents/BudgetMaterial"
DELAY = 0.5  # politeness between requests to a .mil host

# ---- per-year RDT&E location/naming -----------------------------------------
# folder under {year}/, rdte subdir, and a filename formatter taking (vol, ba)
RDTE = {
    2027: ("Discretionary%20Budget", "rdte",  lambda v, ba: f"RDTE%20-%20Vol%20{v}%20-%20Budget%20Activity%20{ba}.pdf"),
    2026: ("Discretionary%20Budget", "rdte",  lambda v, ba: f"RDTE%20-%20Vol%20{v}%20-%20Budget%20Activity%20{ba}.pdf"),
    2025: ("Base%20Budget", "Research,%20Development,%20Test%20and%20Evaluation",
                                              lambda v, ba: f"RDTE%20-%20Vol%20{v}%20-%20Budget%20Activity%20{ba}.pdf"),
    2024: ("Base%20Budget", "rdte",          lambda v, ba: f"RDTE-Vol%20{v}-Budget%20Activity%20{ba}.pdf"),
    2023: ("Base%20Budget", "rdte",          lambda v, ba: f"vol_{v}-Budget_Activity_{ba}.pdf"),
    2022: ("Base%20Budget", "rdte",          lambda v, ba: f"RDTE_BA_{ba}_FY_2022_PB.pdf"),
}
def rdte_urls(year, ba):
    folder, sub, fmt = RDTE[year]
    if year == 2022:
        return [f"{ASAFM}/{year}/{folder}/{sub}/{fmt(0, ba)}"]
    # volume number is unstable across years -> try 1..4
    return [f"{ASAFM}/{year}/{folder}/{sub}/{fmt(v, ba)}" for v in (1, 2, 3, 4)]

# ---- per-year OPA BA1 (watercraft procurement) ------------------------------
OPA = {
    2027: [f"{ASAFM}/2027/Discretionary%20Budget/Procurement/Other%20Procurement%20-%20BA1%20-%20Tactical%20&%20Support%20Vehicles.pdf",
           f"{ASAFM}/2027/Discretionary%20Budget/Procurement/Other_Procurement%20-%20BA1%20-%20Tactical%20&%20Support%20Vehicles.pdf"],
    2026: [f"{ASAFM}/2026/Discretionary%20Budget/Procurement/Other%20Procurement%20-%20BA1%20-%20Tactical%20&%20Support%20Vehicles.pdf"],
    2025: [f"{ASAFM}/2025/Base%20Budget/Procurement/Other%20Procurement%20-%20BA%201%20-%20Tactical%20&%20Support%20Vehicles.pdf",
           f"{ASAFM}/2025/Base%20Budget/Procurement/Other%20Procurement%20-%20BA1%20-%20Tactical%20&%20Support%20Vehicles.pdf"],
    2024: [f"{ASAFM}/2024/Base%20Budget/Procurement/Other%20Procurement%20-%20BA%201%20-%20Tactical%20&%20Support%20Vehicles.pdf"],
    2023: [f"{ASAFM}/2023/Base%20Budget/Procurement/OPA_BA1_Tactical_Support_Vehicles.pdf"],
    2022: [f"{ASAFM}/2022/Base%20Budget/Procurement/OPA_BA_1_FY_2022_PB_Other_Procurement_BA1_Tactical_and_Support_Vehicles.pdf"],
}

# ---- per-year OPA BA3&4 (watercraft procurement DETAIL: P-40/P-5) ------------
# OPA is published in 3 volumes: Vol 1 = BA1 (above, has only the appropriation-
# wide P-1 index), Vol 2 = BA2 Comms/Electronics, Vol 3 = BA3 & 4 "Other Support
# Equipment & Spares". The watercraft procurement line items (Army Watercraft Esp
# 3569M11101, MSV 8211R01001, Float/Rail <$5M 9552ML5355 - all BA03, BSA 55
# "Rail Float Containerization Equipment") carry their funding tables / narrative
# HERE, not in BA1. Filename drifts hard year to year (and FY25's title literally
# reads "Other Support Vehicles" - an Army typo, but it is the real URL); first
# valid PDF wins. URLs confirmed via asafm.army.mil search, Jun 2026.
OPA3 = {
    2027: [f"{ASAFM}/2027/Discretionary%20Budget/Procurement/Other%20Procurement%20-%20BA3%20&%204%20-%20Other%20Support%20Equipment%20&%20Initial%20Spares.pdf"],
    2026: [f"{ASAFM}/2026/Discretionary%20Budget/Procurement/Other%20Procurement%20-%20BA%203,%204%20&%206%20-%20Other%20Support%20Equipment,%20Initial%20Spares%20and%20Agile%20Portfolio%20Management.pdf"],
    2025: [f"{ASAFM}/2025/Base%20Budget/Procurement/Other%20Procurement%20-%20BA%203%20&%204%20-%20Other%20Support%20Vehicles.pdf",
           f"{ASAFM}/2025/Base%20Budget/Procurement/Other%20Procurement%20-%20BA%203%20&%204%20-%20Other%20Support%20Equipment.pdf"],
    2024: [f"{ASAFM}/2024/Base%20Budget/Procurement/Other%20Procurement%20-%20BA%203%20&%204%20-%20Other%20Support%20Equipment.pdf"],
    2023: [f"{ASAFM}/2023/Base%20Budget/Procurement/OPA_BA3_4_Other_Support_Equipment.pdf"],
    2022: [f"{ASAFM}/2022/Base%20Budget/Procurement/OPA_BA_34_FY_2022_PB_Other_Procurement_BA3&4_Other_Support_Equipment.pdf"],
}

# ---- per-year OMA Vol 1 (Operating Forces) ----------------------------------
OMA = {
    2027: [f"{ASAFM}/2027/Discretionary%20Budget/Operation%20and%20Maintenance/Regular%20Army%20Operation%20and%20Maintenance%20Volume-1.pdf",
           f"{ASAFM}/2027/Discretionary%20Budget/Operation%20and%20Maintenance/Regular%20Army%20Operation%20and%20Maintenance%20Volume%201.pdf"],
    2026: [f"{ASAFM}/2026/Discretionary%20Budget/Operation%20and%20Maintenance/Regular%20Army%20Operation%20and%20Maintenance%20Volume-1.pdf"],
    2025: [f"{ASAFM}/2025/Base%20Budget/Operation%20and%20Maintenance/Regular%20Army%20Operation%20and%20Maintenance%20Volume%201.pdf"],
}

# ---- DoD-wide consolidated indices (OSD Comptroller), FY27 ------------------
def osd(stub):
    return [f"https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2027/FY2027_{stub}.pdf",
            f"https://comptroller.defense.gov/Portals/45/Documents/defbudget/FY2027/FY2027_{stub}.pdf"]

# ---- assemble the book list -------------------------------------------------
RDTE_BAS_NEW = ["3", "4A", "4B", "5A", "5D", "7"]   # FY24-FY27 (BA4/BA5 split A/B/D)
RDTE_BAS_23  = ["3", "4", "5A", "5D", "7"]          # FY23 (BA4 single, BA5 split)
RDTE_BAS_22  = ["3", "4", "5A", "7"]                # FY22 (no A/B split)

def rdte_bas(fy):
    return {2022: RDTE_BAS_22, 2023: RDTE_BAS_23}.get(fy, RDTE_BAS_NEW)

books = []
def add(fy, tier, approp, book_id, subdir, urls):
    books.append(dict(fy=fy, tier=tier, approp=approp, book_id=book_id, subdir=subdir, urls=urls))

for fy in (2027, 2026, 2025, 2024, 2023, 2022):
    add(fy, "1", "OPA", "OPA_BA1_Tactical_Support_Vehicles", "procurement", OPA[fy])
    add(fy, "1", "OPA", "OPA_BA34_Other_Support_Equipment", "procurement", OPA3[fy])
    for ba in rdte_bas(fy):
        add(fy, "2", "RDTE", f"RDTE_BA{ba}", "rdte", rdte_urls(fy, ba))
for fy in (2027, 2026, 2025):
    add(fy, "3", "OMA", "OMA_Vol1_Operating_Forces", "om", OMA[fy])
add(2027, "I", "OSD", "P1_Procurement_Programs", "summary", osd("p1"))
add(2027, "I", "OSD", "R1_RDTE_Programs", "summary", osd("r1"))
add(2027, "I", "OSD", "O1_OM_Programs", "summary", osd("o1"))

# ---- fetch ------------------------------------------------------------------
def referer(url):
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/"

def curl(url, dest_tmp):
    cmd = ["curl", "-sS", "-L", "--compressed", "-A", UA,
           "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
           "-H", "Accept-Language: en-US,en;q=0.9",
           "-H", f"Referer: {referer(url)}",
           "-H", "Sec-Fetch-Dest: document", "-H", "Sec-Fetch-Mode: navigate",
           "-H", "Sec-Fetch-Site: same-origin", "-H", "Upgrade-Insecure-Requests: 1",
           "--max-time", "120", "-o", dest_tmp,
           "-w", "%{http_code} %{size_download}", url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180).stdout.strip()
        code, size = out.split()
        return int(code), int(size)
    except Exception as e:
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

rows = []
hits = misses = skipped = 0
for b in books:
    d = os.path.join(PDF_DIR, f"FY{b['fy']}", b["subdir"])
    os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, b["book_id"] + ".pdf")
    rel = os.path.relpath(dest, ROOT)
    if os.path.exists(dest) and is_pdf(dest):
        skipped += 1
        rows.append([b["fy"], b["tier"], b["approp"], b["book_id"], "HAVE",
                     "", os.path.getsize(dest), pages(dest), sha256(dest), rel, "", "already on disk"])
        print(f"  skip  FY{b['fy']} {b['book_id']} (already have)")
        continue
    got = None
    for url in b["urls"]:
        tmp = dest + ".part"
        code, size = curl(url, tmp)
        time.sleep(DELAY)
        if code == 200 and is_pdf(tmp) and size > 8000:
            os.replace(tmp, dest)
            got = url
            break
        if os.path.exists(tmp):
            os.remove(tmp)
    if got:
        hits += 1
        print(f"  OK    FY{b['fy']} {b['book_id']:38s} {os.path.getsize(dest)//1024:>6d} KB")
        rows.append([b["fy"], b["tier"], b["approp"], b["book_id"], "OK",
                     200, os.path.getsize(dest), pages(dest), sha256(dest), rel, got, ""])
    else:
        misses += 1
        print(f"  MISS  FY{b['fy']} {b['book_id']:38s} tried {len(b['urls'])} url(s)")
        rows.append([b["fy"], b["tier"], b["approp"], b["book_id"], "MISS",
                     "", "", "", "", rel, " | ".join(b["urls"]), "no candidate returned a PDF"])

with open(os.path.join(ROOT, "_manifest.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["fy", "tier", "appropriation", "book_id", "status", "http", "bytes",
                "pages", "sha256_16", "rel_path", "source_url", "note"])
    w.writerows(sorted(rows, key=lambda r: (-int(str(r[0])), r[1], r[3])))

print(f"\nDONE  hits={hits}  misses={misses}  already_had={skipped}  total={len(books)}")
