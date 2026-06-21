#!/usr/bin/env python3
"""
Re-process the existing HII earnings transcript text files with DDG/Ingalls-focused
keyword analysis. No re-fetching needed — the .txt files are already symlinked from
submarine_outsourced_work/hii_earnings_transcripts/.

Outputs to hii_earnings_transcripts/:
  _ddg_keyword_counts.csv    Per-transcript counts of DDG-relevant keywords
  _ddg_dollar_snippets.csv   Dollar-figure snippets near DDG / destroyer / Ingalls
"""
import csv
import re
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "hii_earnings_transcripts"

KEYWORDS = ("DDG", "destroyer", "Arleigh", "Flight III", "Aegis", "SPY-6",
            "Ingalls", "Pascagoula", "LHA", "LPD", "NSC",
            "Newport News", "submarine", "Virginia", "Columbia",
            "backlog", "multi-year", "MYP")


def main():
    txts = sorted([p for p in OUT.glob("FY*.txt") if not p.name.startswith("_")])
    if not txts:
        print("No HII transcript .txt files found in", OUT)
        return

    print(f"Re-analyzing {len(txts)} HII transcripts for DDG keywords...\n")

    count_rows = []
    snippet_rows = []
    for p in txts:
        text = p.read_text(errors="replace")
        fy_match = re.match(r"FY(\d{4})_Q(\d+)_(\w+)", p.stem)
        if not fy_match:
            continue
        fy, q, source = int(fy_match.group(1)), int(fy_match.group(2)), fy_match.group(3)

        counts = {kw: len(re.findall(r"\b" + re.escape(kw) + r"\b", text, re.I)) for kw in KEYWORDS}
        row = {"fy": fy, "quarter": q, "source": source, "file": p.name, "chars": len(text)}
        row.update({f"n_{kw}": c for kw, c in counts.items()})
        count_rows.append(row)

        # Pull dollar-near-keyword snippets
        for kw in ("DDG", "destroyer", "Ingalls", "Arleigh", "Aegis", "Flight III"):
            for m in re.finditer(re.escape(kw) + r"[^.]{0,120}\$[\d,\.]+\s*(?:billion|million|B|M)\b", text, re.I):
                snippet_rows.append({
                    "fy": fy, "quarter": q, "source": source, "keyword": kw,
                    "snippet": m.group(0)[:300],
                })
            # Also reverse direction: $ amount followed by keyword
            for m in re.finditer(r"\$[\d,\.]+\s*(?:billion|million|B|M)\b[^.]{0,120}" + re.escape(kw), text, re.I):
                snippet_rows.append({
                    "fy": fy, "quarter": q, "source": source, "keyword": kw + " (reverse)",
                    "snippet": m.group(0)[:300],
                })

        # Print quick summary per transcript
        d, dest, ing = counts.get("DDG",0), counts.get("destroyer",0), counts.get("Ingalls",0)
        sub, nns = counts.get("submarine",0), counts.get("Newport News",0)
        print(f"  FY{fy} Q{q}: DDG={d}  destroyer={dest}  Ingalls={ing}  | submarine={sub}  NNS={nns}")

    # Write counts CSV
    count_path = OUT / "_ddg_keyword_counts.csv"
    if count_rows:
        keys = sorted({k for r in count_rows for k in r.keys()})
        front = ["fy", "quarter", "source", "file", "chars"]
        keys = front + [k for k in keys if k not in front]
        with open(count_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for r in count_rows:
                w.writerow({k: r.get(k, 0) for k in keys})
        print(f"\nWrote {count_path}  ({len(count_rows)} transcripts)")

    # Write snippets CSV
    snippet_path = OUT / "_ddg_dollar_snippets.csv"
    if snippet_rows:
        with open(snippet_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["fy", "quarter", "source", "keyword", "snippet"])
            w.writeheader()
            for r in snippet_rows:
                w.writerow(r)
        print(f"Wrote {snippet_path}  ({len(snippet_rows)} dollar snippets)")

    # Aggregate DDG-mention totals across all transcripts
    print("\nAggregate DDG mentions across all HII transcripts:")
    agg = {kw: sum(r.get(f"n_{kw}", 0) for r in count_rows) for kw in KEYWORDS}
    for kw, n in sorted(agg.items(), key=lambda x: -x[1]):
        if n > 0:
            print(f"  {kw:>20s}: {n}")


if __name__ == "__main__":
    main()
