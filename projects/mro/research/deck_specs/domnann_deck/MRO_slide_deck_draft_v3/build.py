"""Concat src/shell.html + src/slides/*.html -> MRO Deck.html.

CSS lives in src/deck.css and is referenced by <link> from the shell, so
edits to deck.css take effect on browser reload with no rebuild needed.
Only structural HTML changes (shell or slide partials) require running this.

Slides are included in numeric filename order (01-*.html, 02-*.html, ...).
Usage:
    python3 build.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC_DIR = HERE / "src"
SHELL = SRC_DIR / "shell.html"
SLIDES_DIR = SRC_DIR / "slides"
OUT = HERE / "MRO Deck.html"
MARKER = "{{SLIDES}}"


def main() -> int:
    if not SHELL.exists():
        print(f"missing {SHELL}", file=sys.stderr)
        return 1

    slide_files = sorted(SLIDES_DIR.glob("*.html"))
    if not slide_files:
        print(f"no slides found in {SLIDES_DIR}", file=sys.stderr)
        return 1

    shell = SHELL.read_text(encoding="utf-8")
    if MARKER not in shell:
        print(f"{SHELL} missing {MARKER} placeholder", file=sys.stderr)
        return 1

    parts = []
    for path in slide_files:
        body = path.read_text(encoding="utf-8").rstrip("\n")
        parts.append(body)
    slides_blob = "\n\n".join(parts)

    out = shell.replace(MARKER, slides_blob)
    OUT.write_text(out, encoding="utf-8")

    total = sum(p.stat().st_size for p in slide_files)
    print(
        f"wrote {OUT.name}: {len(slide_files)} slides "
        f"({total:,} bytes) + shell ({SHELL.stat().st_size:,} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
