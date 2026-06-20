"""inspect_v433 - compact structural dump of an extracted v4.33 sheet JSON. Read-only
provenance browser for the original grid (the native sheets are now hand-authored, no
longer reflowed): per row, the col-0 label (style + text), cell count, formula flag, and
any S_PASTE_*/S_TITLE_* styles in the row.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "extracted" / "v433"


def main(slug: str) -> int:
    data = json.loads((HERE / f"{slug}.json").read_text(encoding="utf-8"))
    cells = data["cells"]
    print(f"# {slug}  sheet={data.get('sheet')!r}")
    print(f"cols ({len(data.get('cols') or [])}): {data.get('cols')}")
    print(f"tables: {[(t['name'], t['ref']) for t in data.get('tables', [])]}")
    by_row = {}
    for c in cells:
        by_row.setdefault(c["r"], []).append(c)
    for r in sorted(by_row):
        row = by_row[r]
        c0 = next((c for c in row if c["c"] == 0), None)
        styles = sorted({c["s"] for c in row})
        special = [s for s in styles if "TITLE" in s or "PASTE" in s or "HEADER" in s]
        nf = sum(1 for c in row if c["k"] == "f")
        txt = ""
        if c0 is not None:
            p = c0["p"]
            txt = (str(p)[:70] + "…") if isinstance(p, str) and len(str(p)) > 70 else p
        tag = f"  [{','.join(special)}]" if special else ""
        fflag = f" f={nf}" if nf else ""
        print(f"  r{r:<3} c0={c0['s'] if c0 else '-':18} n={len(row):2}{fflag}{tag}  {txt!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
