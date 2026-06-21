#!/usr/bin/env python3
"""
Mine the existing HII + GD earnings transcripts for direct executive quotes about
outsourcing, supplier content, vertical integration, supplier spend, etc.

We have 23 HII transcripts (FY19-FY26) and 22 GD transcripts (FY20-FY26).

Output: extracted/exec_quotes_outsourcing.csv  — one row per matching snippet
       + extracted/exec_quotes_outsourcing.md  — human-readable digest, top hits
"""
import csv
import re
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "extracted"

# Keyword PATTERNS — anything an exec might say about supplier content / outsourcing
KEYWORD_PATTERNS = [
    # Most direct
    ("outsource_pct", re.compile(r"outsourc[a-z]*[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    ("supplier_pct",  re.compile(r"\b(?:supplier|suppliers|supply chain|sub[-]?tier|subcontract|subcontractor)[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    ("pct_outsource", re.compile(r"\d+\s*(?:percent|%)[^.]{0,80}(?:outsourc|supplier|supply chain|subcontract|vendors?)", re.I)),
    # Vertical integration
    ("vertical_integration", re.compile(r"vertical[a-z]* integration", re.I)),
    ("in_house_pct",  re.compile(r"in[- ]house[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    # Specific supplier spend disclosures
    ("supplier_spend", re.compile(r"(?:supplier|supply chain|subcontract|vendor)[^.]{0,150}\$\s*[\d,\.]+\s*(?:billion|million|B|M)\b", re.I)),
    ("spend_with_suppliers", re.compile(r"\$\s*[\d,\.]+\s*(?:billion|million|B|M)[^.]{0,80}(?:supplier|supply chain|vendors?)", re.I)),
    # Materials content
    ("material_content", re.compile(r"(?:material|materials)\s+(?:content|cost|spend)[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    # Direct statements about labor share
    ("labor_pct",     re.compile(r"(?:labor|workforce|in[- ]house)\s+(?:cost|content|share|portion)[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    # Supplier development / industrial base
    ("industrial_base", re.compile(r"industrial base[^.]{0,200}\$\s*[\d,\.]+\s*(?:billion|million|B|M)\b", re.I)),
    # Less specific but maybe useful
    ("our_suppliers", re.compile(r"\bour\s+(?:supplier|suppliers|supply chain|vendors?)\b[^.]{0,200}", re.I)),
    ("our_outsource", re.compile(r"\bour\s+outsourc", re.I)),
]


def extract_context(text, m, before=200, after=400):
    """Extract a clean sentence-bounded context around a regex match."""
    start = max(0, m.start() - before)
    end = min(len(text), m.end() + after)
    ctx = text[start:end]
    # Trim to nearest sentence at start (remove leading partial sentence)
    first_period = ctx.find(". ")
    if 0 < first_period < before - 50:
        ctx = ctx[first_period + 2:]
    # Trim trailing partial sentence
    last_period = ctx.rfind(".")
    if last_period > 0 and last_period > len(ctx) - 50:
        ctx = ctx[:last_period + 1]
    return ctx.strip()


def speaker_attribution(text, m, window=300):
    """Try to find the speaker name/role preceding the match. Speakers in MF
    transcripts are typically formatted 'Name -- Role -- Company'. We look for
    the nearest such pattern before the match."""
    start = max(0, m.start() - window)
    pre = text[start:m.start()]
    # Look for "Name -- Role" lines or "Name:" prefixes
    speakers = re.findall(r"\n([A-Z][a-zA-Z'\-]+ [A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)?)\s*--", pre)
    if speakers:
        return speakers[-1]
    # Try "Name:" pattern
    speakers2 = re.findall(r"\n([A-Z][a-zA-Z'\-]+ [A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)?):", pre)
    if speakers2:
        return speakers2[-1]
    return ""


def main():
    matches = []
    transcript_dirs = [
        ("HII", REPO / "hii_earnings_transcripts"),
        ("GD",  REPO / "gd_earnings_transcripts"),
    ]
    for company, d in transcript_dirs:
        for p in sorted(d.glob("FY*.txt")):
            if p.name.startswith("_"): continue
            text = p.read_text(errors="replace")
            fy_match = re.match(r"FY(\d{4})_Q(\d+)_(\w+)", p.stem)
            if not fy_match: continue
            fy = int(fy_match.group(1))
            q = int(fy_match.group(2))
            for cat, pat in KEYWORD_PATTERNS:
                for m in pat.finditer(text):
                    ctx = extract_context(text, m)
                    speaker = speaker_attribution(text, m)
                    matches.append({
                        "company": company,
                        "fy": fy, "quarter": q,
                        "file": p.name,
                        "category": cat,
                        "speaker": speaker,
                        "matched_phrase": m.group(0)[:200],
                        "context": ctx[:1200],
                    })

    # De-dup by (company, fy, quarter, first 100 chars of context)
    seen = set()
    dedup = []
    for r in matches:
        k = (r["company"], r["fy"], r["quarter"], r["context"][:100])
        if k in seen: continue
        seen.add(k)
        dedup.append(r)

    # Write CSV
    csv_path = OUT / "exec_quotes_outsourcing.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "company", "fy", "quarter", "file", "category", "speaker",
            "matched_phrase", "context"
        ])
        w.writeheader()
        for r in dedup:
            w.writerow(r)
    print(f"Wrote {csv_path}  ({len(dedup)} unique matches)")

    # Categorized digest — focus on the MOST RELEVANT categories first
    md = ["# Executive Quotes on DDG Outsourcing / Supplier Content\n\n"]
    md.append("Auto-mined from HII + GD earnings transcripts (FY19-FY26).\n\n")
    HIGH_VALUE = ("supplier_pct", "outsource_pct", "pct_outsource", "in_house_pct",
                  "labor_pct", "material_content", "supplier_spend",
                  "spend_with_suppliers", "industrial_base", "vertical_integration")
    LOW_VALUE = ("our_suppliers", "our_outsource")

    md.append("## High-signal matches (direct % / $ disclosures)\n\n")
    high_hits = [r for r in dedup if r["category"] in HIGH_VALUE]
    md.append(f"({len(high_hits)} hits)\n\n")
    for r in high_hits:
        md.append(f"### {r['company']} FY{r['fy']} Q{r['quarter']} — {r['category']}\n")
        md.append(f"**Speaker:** {r['speaker'] or '(unknown)'}\n\n")
        md.append(f"> {r['context']}\n\n")
        md.append(f"*Matched phrase: `{r['matched_phrase']}`*\n\n---\n\n")

    md.append("## Lower-signal matches (general supplier/outsource mentions)\n\n")
    low_hits = [r for r in dedup if r["category"] in LOW_VALUE]
    md.append(f"({len(low_hits)} hits — not enumerated here; see CSV)\n\n")

    md_path = OUT / "exec_quotes_outsourcing.md"
    md_path.write_text("".join(md))
    print(f"Wrote {md_path}")

    # Quick stats
    from collections import Counter
    by_cat = Counter(r["category"] for r in dedup)
    by_co  = Counter(r["company"] for r in dedup)
    print(f"\nBy category: {dict(by_cat.most_common())}")
    print(f"By company: {dict(by_co)}")
    print(f"\nHIGH-VALUE hits by company:")
    high_by_co = Counter(r["company"] for r in dedup if r["category"] in HIGH_VALUE)
    print(f"  {dict(high_by_co)}")


if __name__ == "__main__":
    main()
