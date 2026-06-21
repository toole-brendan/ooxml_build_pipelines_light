#!/usr/bin/env python3
"""
Mine the 23 HII earnings call transcripts for high-signal quotes.

Pulls quote candidates that match topic categories, then ranks by signal strength:
  - Outsourcing strategy / supplier capacity / MIB
  - Program status ($ figures + program names: Virginia / Columbia / CVN)
  - Forward-looking guidance / backlog
  - Performance issues (cumulative catch-up adjustments)

Outputs:
  extracted/hii_curated_quotes.csv  (top 30-50 quotes for the workbook)
  extracted/hii_all_quote_candidates.csv  (everything for audit)
"""
import csv
import glob
import re
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
TRANSCRIPTS = REPO / "hii_earnings_transcripts"
OUT = REPO / "extracted"


# Topic categories with their keyword patterns
TOPICS = {
    "Outsourcing / Supplier capacity / MIB": [
        r"\boutsourc\w*\b",
        r"\bsuppl\w+ (?:base|capacity|network|chain)\b",
        r"\bindustrial base\b",
        r"\bBlueForge\b",
        r"\bMaritime Industrial Base\b",
        r"\bMIB\b",
        r"\bsupplier development\b",
        r"\bvendor base\b",
        r"\bthroughput\b",
    ],
    "Virginia program status": [
        r"\bVirginia (?:class|program|submarines?)\b",
        r"\bSSN 774\b",
        r"\bBlock IV\b",
        r"\bBlock V\b",
        r"\bBlock VI\b",
    ],
    "Columbia program status": [
        r"\bColumbia (?:class|program|submarines?)\b",
        r"\bSSBN 826\b",
    ],
    "Aircraft carrier / RCOH": [
        r"\bCVN \d+\b",
        r"\bRCOH\b",
        r"\baircraft carrier\b",
    ],
    "Performance / catch-up adjustments": [
        r"\bcatch[- ]up\b",
        r"\bunfavorable adjustment\b",
        r"\bcost growth\b",
        r"\bschedule (?:delay|slippage|performance)\b",
        r"\bproductivity\b",
    ],
    "Backlog / forward visibility": [
        r"\bbacklog\b",
        r"\bcontract award\b",
        r"\bawards\b",
        r"\bguidance\b",
    ],
    "Teaming agreement / GDEB relationship": [
        r"\bteaming (?:agreement|arrangement|partner)\b",
        r"\bElectric Boat\b",
        r"\bgeneral dynamics\b",
    ],
}

# Speakers we want to attribute quotes to (CEO/CFO/NNS lead)
KEY_SPEAKERS = [
    "Chris Kastner", "Christopher Kastner", "Chris  Kastner",
    "Tom Stiehle", "Thomas Stiehle", "Thomas E. Stiehle",
    "Kari Wilkinson",
    "Mike Petters",  # former CEO
    "Mike  Petters",
]


def split_into_paragraphs(text):
    """Split transcript into speaker-tagged paragraphs."""
    # Transcripts use patterns like "Name Surname:" or "Name:" at start of paragraph
    # Each paragraph is up to the next speaker or until empty line
    paragraphs = []
    lines = text.split("\n")
    current = []
    current_speaker = None
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                paragraphs.append((current_speaker, " ".join(current)))
                current = []
            continue
        # Speaker line: typical formats
        # "Christopher Kastner: ..."
        # "Christopher Kastner -- President: ..."
        m = re.match(r"^([A-Z][A-Za-z\. ]{2,40}?)\s*(?:--[^:]*)?:\s*(.*)$", line)
        if m and len(m.group(1).split()) <= 4 and not any(
            w in m.group(1).lower() for w in ("the", "and", "this", "that")
        ):
            if current:
                paragraphs.append((current_speaker, " ".join(current)))
            current_speaker = m.group(1).strip()
            rest = m.group(2).strip()
            current = [rest] if rest else []
        else:
            current.append(line)
    if current:
        paragraphs.append((current_speaker, " ".join(current)))
    return paragraphs


def score_quote(quote, topic_patterns):
    """Score a quote on signal strength for a topic.
    Bonus for:
      - $ figure
      - Specific numbers (boats, percentages, dates)
      - Forward-looking words (expect, plan, going to, will, target)
    """
    score = 0
    # Topic hit
    for pat in topic_patterns:
        n = len(re.findall(pat, quote, re.I))
        score += n * 5
    # Dollar figures
    score += 3 * len(re.findall(r"\$\s*[\d,\.]+\s*(?:billion|million|B|M)", quote, re.I))
    # Percentages
    score += 2 * len(re.findall(r"\d+(?:\.\d+)?\s*%", quote))
    # Concrete numbers (e.g., "two boats", "ten submarines")
    score += 1 * len(re.findall(r"\b\d+\s+(?:boats?|submarines?|ships?|carriers?)\b", quote, re.I))
    # Forward-looking
    score += 1 * len(re.findall(r"\b(?:expect|plan|target|will|going to|forecast|outlook)\b", quote, re.I))
    return score


def extract_candidates_from_transcript(fy, q, source, text):
    """Walk through every speaker paragraph, classify by topic, score, and return candidates."""
    paragraphs = split_into_paragraphs(text)
    candidates = []
    for speaker, para in paragraphs:
        if not speaker or len(para) < 80 or len(para) > 1200:
            continue
        # Only include quotes from key speakers (CEO/CFO/NNS)
        speaker_clean = re.sub(r"\s+", " ", speaker).strip()
        is_key = any(ks.lower() in speaker_clean.lower() for ks in KEY_SPEAKERS)
        if not is_key:
            continue
        # Score for each topic
        for topic, patterns in TOPICS.items():
            score = score_quote(para, patterns)
            if score >= 8:  # threshold for "interesting"
                candidates.append({
                    "fy": fy,
                    "quarter": q,
                    "source": source,
                    "speaker": speaker_clean,
                    "topic": topic,
                    "score": score,
                    "quote": para.strip(),
                    "quote_length": len(para),
                })
    return candidates


def main():
    all_candidates = []
    transcript_files = sorted(TRANSCRIPTS.glob("*.txt"))
    transcript_files = [f for f in transcript_files if "README" not in f.name]
    print(f"Mining {len(transcript_files)} transcripts…\n")
    for f in transcript_files:
        # Parse filename: FY2026_Q1_fool.txt
        m = re.match(r"FY(\d{4})_Q(\d)_(.+)", f.stem)
        if not m:
            continue
        fy, q, source = int(m.group(1)), int(m.group(2)), m.group(3)
        text = f.read_text()
        cands = extract_candidates_from_transcript(fy, q, source, text)
        all_candidates.extend(cands)
        print(f"  {f.name}: {len(cands)} candidates")

    print(f"\nTotal candidates: {len(all_candidates):,}")

    # Dedup near-duplicates (same quote across fool+IM mirror)
    seen_sigs = set()
    deduped = []
    for c in all_candidates:
        sig = (c["fy"], c["quarter"], c["speaker"][:20], c["quote"][:120].lower())
        if sig in seen_sigs:
            continue
        seen_sigs.add(sig)
        deduped.append(c)
    print(f"After dedup: {len(deduped):,}")

    # Write all candidates (audit)
    fields = ["fy", "quarter", "source", "speaker", "topic", "score",
              "quote_length", "quote"]
    with open(OUT / "hii_all_quote_candidates.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for c in sorted(deduped, key=lambda x: (x["topic"], -x["score"])):
            w.writerow({k: c[k] for k in fields})
    print(f"Wrote {OUT/'hii_all_quote_candidates.csv'} ({len(deduped)} rows)")

    # Curated: top N per topic, avoiding duplicate FYs unless score is much higher
    curated = []
    for topic in TOPICS:
        topic_cands = sorted(
            [c for c in deduped if c["topic"] == topic],
            key=lambda x: -x["score"]
        )
        # Take up to 6 per topic, prefer chronological diversity
        seen_fys = set()
        topic_picks = []
        for c in topic_cands:
            if len(topic_picks) >= 6:
                break
            fy_q = (c["fy"], c["quarter"])
            if fy_q in seen_fys and c["score"] < (topic_picks[0]["score"] * 0.8 if topic_picks else 0):
                continue
            seen_fys.add(fy_q)
            topic_picks.append(c)
        curated.extend(topic_picks)

    with open(OUT / "hii_curated_quotes.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for c in sorted(curated, key=lambda x: (x["topic"], x["fy"], x["quarter"])):
            w.writerow({k: c[k] for k in fields})
    print(f"Wrote {OUT/'hii_curated_quotes.csv'} ({len(curated)} curated quotes)")

    # Print preview
    print()
    print("=== Sample curated quotes by topic ===")
    for topic in TOPICS:
        topic_q = [c for c in curated if c["topic"] == topic]
        if not topic_q:
            continue
        print(f"\n--- {topic} ({len(topic_q)} quotes) ---")
        for c in topic_q[:2]:
            print(f"  FY{c['fy']} Q{c['quarter']} {c['speaker']}: "
                  f"{c['quote'][:250]}...")


if __name__ == "__main__":
    main()
