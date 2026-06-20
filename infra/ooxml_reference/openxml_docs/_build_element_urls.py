"""Regenerate xref/element_urls.json from deck_core/primitives.py + the
filtered intellisense XML.

For every `<ns:tag>` pattern emitted in deck_core/primitives.py, find the
DocumentFormat.OpenXml SDK class whose intellisense docstring contains
"qualified name is <ns>:<tag>" and emit the corresponding learn.microsoft.com
URL. Tags with multiple matching SDK classes (e.g., a:xfrm appears for
Transform2D / TransformEffect / TransformGroup) keep all candidates.

Re-run whenever deck_core/primitives.py adds a new emitted tag. The script
prints any unmapped tags so a missing entry is easy to spot.

This is a manual dev/reference tool (lives under infra/ooxml_reference/), not
part of any build. Run it from this directory:
    python3 _build_element_urls.py
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent       # infra/ooxml_reference/openxml_docs/
WORKSPACE_ROOT = THIS_DIR.parents[2]             # repo root (holds deck_core/)

INTELLISENSE = THIS_DIR / "intellisense" / "DocumentFormat.OpenXml.PresentationAndDrawing.xml"
PRIMITIVES = WORKSPACE_ROOT / "deck_core" / "primitives.py"
OUT_PATH = THIS_DIR / "xref" / "element_urls.json"

QNAME_RE = re.compile(r"qualified name is ([ap]):([A-Za-z][A-Za-z0-9]*)")
TAG_RE = re.compile(r'<(?:/)?([ap]):([A-Za-z][A-Za-z0-9]*)')


def main() -> int:
    if not INTELLISENSE.is_file():
        print(f"missing {INTELLISENSE} — rebuild the cache first (see README.md)", file=sys.stderr)
        return 1

    root = ET.parse(INTELLISENSE).getroot()
    members = root.find("members")
    qname_to_fqns: dict[str, list[str]] = {}
    for m in members:
        name_attr = m.get("name", "")
        if not name_attr.startswith("T:"):
            continue
        fqn = name_attr[2:]
        text = " ".join(m.itertext())
        for ns, tag in QNAME_RE.findall(text):
            qname_to_fqns.setdefault(f"{ns}:{tag}", []).append(fqn)

    primitives_src = PRIMITIVES.read_text()
    tags = {f"{ns}:{tag}" for ns, tag in TAG_RE.findall(primitives_src)}

    result: dict[str, dict] = {}
    unmapped: list[str] = []
    for tag in sorted(tags):
        fqns = qname_to_fqns.get(tag, [])
        if not fqns:
            unmapped.append(tag)
            continue
        entries = [
            {
                "sdk_fqn": fqn,
                "learn_url": f"https://learn.microsoft.com/en-us/dotnet/api/{fqn.lower()}",
            }
            for fqn in fqns
        ]
        result[tag] = entries[0] if len(entries) == 1 else {"candidates": entries}

    out = {
        "_meta": {
            "source": "Generated from infra/ooxml_reference/openxml_docs/intellisense/DocumentFormat.OpenXml.PresentationAndDrawing.xml",
            "pattern": "<ns>:<tag>  ->  DocumentFormat.OpenXml.<Class>  ->  learn.microsoft.com/.../<class_lower>",
            "regenerate": "python3 _build_element_urls.py",
            "covers": "every <ns:tag> emitted in deck_core/primitives.py",
        },
        "elements": result,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2) + "\n")

    print(f"primitives.py tags: {len(tags)}")
    print(f"mapped:             {len(result)}")
    print(f"unmapped:           {unmapped or 'none'}")
    print(f"wrote {OUT_PATH.relative_to(DECK_DIR)}")
    return 1 if unmapped else 0


if __name__ == "__main__":
    sys.exit(main())
