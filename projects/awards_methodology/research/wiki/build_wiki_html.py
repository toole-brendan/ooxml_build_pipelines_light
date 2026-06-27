"""Build the U.S. Defense Contracting structural-reference single-page article.

Adapted from the DDG-51 destroyer-outsourcing wiki generator, which was in
turn adapted from the submarine wiki generator. INDEX.md supplies the lead,
infobox, see-also, references, further reading, and external links. Each
numbered file in this directory becomes one H2 section.

Run:
    pip install markdown pyyaml
    python build_wiki_html.py
"""

from __future__ import annotations

import html as html_lib
import re
import sys
from pathlib import Path

try:
    import markdown
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency. Install with: python -m pip install markdown pyyaml"
    ) from exc

ROOT = Path(__file__).parent
WIKI = ROOT / "wiki"
if not WIKI.exists() and (ROOT / "INDEX.md").exists():
    WIKI = ROOT
OUT_DIR = ROOT
ASSETS_DIR = OUT_DIR / "assets"


ARTICLES: list[tuple[str, str, str]] = [
    ("01-dimensions-of-a-federal-contract.md", "The classification framework", "The dimensions of a federal contract"),
    ("02-core-vocabulary.md", "The classification framework", "The core vocabulary"),
    ("03-awards-ceilings-obligations-spending.md", "Awards and money", "Awards, ceilings, obligations, and spending"),
    ("04-contract-data-systems.md", "Awards and money", "How awards appear in federal data"),
    ("05-recompetes-and-opportunity-intelligence.md", "Awards and money", "Recompetes and opportunity intelligence from awards data"),
    ("06-indefinite-delivery-contracts.md", "Instruments and vehicles", "Indefinite-delivery contracts (FAR 16.5)"),
    ("07-idv-idiq-mac-gwac-schedules.md", "Instruments and vehicles", "IDV, IDIQ, MAC, GWAC, and Schedules"),
    ("08-pricing-types-and-cost-risk.md", "Pricing, options, and time", "Pricing, commerciality, and cost risk"),
    ("09-options-and-award-terms.md", "Pricing, options, and time", "Options and award terms"),
    ("10-period-of-performance-and-scope.md", "Pricing, options, and time", "Period of performance and scope"),
    ("11-multiyear-procurement-and-production.md", "Multiyear and major production", "Multiyear procurement and major weapon production"),
    ("12-prime-contracting-subcontracting-teaming.md", "Prime and subcontracting structure", "Prime contracting, subcontracting, teaming, and first-tier reporting"),
    ("13-small-business.md", "Prime and subcontracting structure", "Small business in defense contracting"),
    ("14-contract-modifications.md", "Structure, traceability, and authority", "Post-award administration, modifications, and closeout"),
    ("15-clins-slins-and-funding-traceability.md", "Structure, traceability, and authority", "CLINs, funding traceability, and program transition"),
    ("16-single-award-and-sole-source.md", "Structure, traceability, and authority", "Single-award, single-source, and sole-source"),
    ("17-contracting-authority-and-award-decisions.md", "Structure, traceability, and authority", "The acquisition lifecycle, source selection, and contracting authority"),
    ("18-not-a-contract-type-traps.md", "Structure, traceability, and authority", "Alternative acquisition pathways and “not a contract type” traps"),
]


def slug_for(rel_path: str) -> str:
    return Path(rel_path).stem.lower().lstrip("0123456789-")


SLUG_LOOKUP: dict[str, str] = {}
LABEL_FOR_SLUG: dict[str, str] = {}
for rel, _cat, label in ARTICLES:
    s = slug_for(rel)
    SLUG_LOOKUP[rel] = s
    SLUG_LOOKUP[Path(rel).name] = s
    LABEL_FOR_SLUG[s] = label
SLUG_LOOKUP["INDEX.md"] = "top"
SLUG_LOOKUP["index.md"] = "top"
LABEL_FOR_SLUG["top"] = "Top of article"


def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("﻿"):
        text = text[1:]
    if not text.startswith("---"):
        return {}, text
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return {}, text
    fm = yaml.safe_load(text[3:end]) or {}
    body = text[end + 4:].lstrip("\n")
    return fm, body


_LIST_LINE = re.compile(r"^\s*([-*+] |\d+\. )")


def insert_blank_lines_before_lists(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        is_list = bool(_LIST_LINE.match(line))
        if is_list and i > 0:
            prev = lines[i - 1]
            if prev.strip() and not _LIST_LINE.match(prev):
                out.append("")
        out.append(line)
    return "\n".join(out)


def attach_slug_to_h1(md_text: str, slug: str) -> str:
    def repl(m: re.Match) -> str:
        title = m.group(1).strip()
        return f"## {title} " + "{#" + slug + "}"
    return re.sub(r"^#\s+(.+)$", repl, md_text, count=1, flags=re.MULTILINE)


def demote_remaining_headings(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        m = re.match(r"^(#{2,5})(\s)", line)
        if m and "{#" not in line:
            out.append("#" + line)
        else:
            out.append(line)
    return "\n".join(out)


def _split_by_h2(body: str) -> list[tuple[str | None, list[str]]]:
    lines = body.split("\n")
    sections: list[tuple[str | None, list[str]]] = []
    current: str | None = None
    buf: list[str] = []
    for line in lines:
        if line.startswith("## "):
            sections.append((current, buf))
            current = line[3:].strip()
            buf = [line]
        else:
            buf.append(line)
    sections.append((current, buf))
    return sections


def _parse_infobox_block(block_lines: list[str]) -> tuple[str, str, str, str, list[tuple[str, str]]]:
    title = ""
    subtitle = ""
    image = ""
    image_caption = ""
    rows: list[tuple[str, str]] = []
    for raw in block_lines:
        line = raw.rstrip()
        if line.startswith("## "):
            continue
        if not line.strip():
            continue
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
            continue
        if line.lower().startswith("subtitle:"):
            subtitle = line.split(":", 1)[1].strip()
            continue
        if line.lower().startswith("image:"):
            image = line.split(":", 1)[1].strip()
            continue
        if line.lower().startswith("image_caption:"):
            image_caption = line.split(":", 1)[1].strip()
            continue
        m = re.match(r"^\s*[-*+]\s+(.+?)\s*\|\s*(.+)$", line)
        if m:
            rows.append((m.group(1).strip(), m.group(2).strip()))
    return title, subtitle, image, image_caption, rows


def render_infobox(title: str, subtitle: str, image: str, image_caption: str, rows: list[tuple[str, str]]) -> str:
    out: list[str] = []
    out.append('<table class="infobox">')
    if title:
        out.append(f'<caption class="infobox-title">{html_lib.escape(title)}</caption>')
    if image:
        cap_html = ""
        if image_caption:
            cap_html = f'<div class="infobox-image-caption">{html_lib.escape(image_caption)}</div>'
        out.append(
            '<tr><td colspan="2" class="infobox-image-cell">'
            f'<img src="{html_lib.escape(image)}" alt="{html_lib.escape(image_caption or title)}" class="infobox-image">'
            f'{cap_html}</td></tr>'
        )
    if subtitle:
        out.append(
            '<tr><td colspan="2" class="infobox-subtitle">'
            f'{html_lib.escape(subtitle)}</td></tr>'
        )
    for key, val in rows:
        val_html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html_lib.escape(val))
        val_html = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", val_html)
        out.append(
            "<tr>"
            f'<th scope="row">{html_lib.escape(key)}</th>'
            f"<td>{val_html}</td>"
            "</tr>"
        )
    out.append("</table>")
    return "".join(out)


def extract_index_pieces(index_md: str) -> dict:
    _fm, body = split_frontmatter(index_md)
    body = insert_blank_lines_before_lists(body)
    sections = _split_by_h2(body)

    pre_h2_lines: list[str] = []
    infobox_lines: list[str] = []
    see_also_lines: list[str] = []
    references_lines: list[str] = []
    further_reading_lines: list[str] = []
    external_links_lines: list[str] = []
    for heading, blk in sections:
        if heading is None:
            pre_h2_lines = blk
        elif heading.lower().startswith("infobox"):
            infobox_lines = blk
        elif heading.lower().startswith("see also"):
            see_also_lines = blk
        elif heading.lower().startswith("references"):
            references_lines = blk
        elif heading.lower().startswith("further reading"):
            further_reading_lines = blk
        elif heading.lower().startswith("external links"):
            external_links_lines = blk

    hatnote = ""
    cleaned_pre: list[str] = []
    seen_h1 = False
    for line in pre_h2_lines:
        if not seen_h1 and re.match(r"^\s*\*[^*].+[^*]\*\s*$", line):
            hatnote = line.strip().strip("*").strip()
            continue
        if line.startswith("# "):
            seen_h1 = True
            cleaned_pre.append(line)
            continue
        cleaned_pre.append(line)

    lead_md = "\n".join(cleaned_pre).strip() + "\n"

    title, subtitle, image, image_caption, rows = _parse_infobox_block(infobox_lines)
    infobox_html = render_infobox(title, subtitle, image, image_caption, rows) if rows else ""

    def pack(blk: list[str], heading_id: str) -> str:
        if not blk:
            return ""
        text = "\n".join(blk).strip() + "\n"
        if f"{{#{heading_id}}}" not in text:
            text = re.sub(
                r"^##\s+([^\n]+)\s*$",
                r"## \1 {#" + heading_id + "}",
                text, count=1, flags=re.MULTILINE,
            )
        return text

    return {
        "lead_md": lead_md,
        "hatnote": hatnote,
        "infobox_html": infobox_html,
        "see_also_md": pack(see_also_lines, "see-also"),
        "references_md": pack(references_lines, "references"),
        "further_reading_md": pack(further_reading_lines, "further-reading"),
        "external_links_md": pack(external_links_lines, "external-links"),
    }


_HREF_MD = re.compile(r'href="([^"#]+\.md)(#[^"]*)?"')


def rewrite_cross_links(html_text: str) -> str:
    def repl(m: re.Match) -> str:
        href = m.group(1)
        fragment = m.group(2) or ""
        if href.startswith("../"):
            return m.group(0)
        posix = href.replace("\\", "/").lstrip("./")
        slug = SLUG_LOOKUP.get(posix) or SLUG_LOOKUP.get(Path(posix).name)
        if not slug:
            return m.group(0)
        if fragment:
            return f'href="{fragment}"'
        return f'href="#{slug}"'
    return _HREF_MD.sub(repl, html_text)


def add_wikitable_class(html_text: str) -> str:
    return re.sub(r"<table(?![^>]*class=)", '<table class="wikitable"', html_text)


def preprocess_math_tags(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    counter = [0]

    def make_key() -> str:
        counter[0] += 1
        return f"MATHPLACEHOLDER{counter[0]:05d}MATHEND"

    def replace_block(m: re.Match) -> str:
        key = make_key()
        placeholders[key] = "\\[" + m.group(1).strip() + "\\]"
        return key

    def replace_inline(m: re.Match) -> str:
        key = make_key()
        placeholders[key] = "\\(" + m.group(1).strip() + "\\)"
        return key

    text = re.sub(
        r'<math\s+display="block"\s*>(.*?)</math>',
        replace_block,
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'<math\s*>(.*?)</math>',
        replace_inline,
        text,
        flags=re.DOTALL,
    )
    return text, placeholders


def postprocess_math_tags(html: str, placeholders: dict[str, str]) -> str:
    for key, value in placeholders.items():
        html = html.replace(key, value)
    return html


_HEADING_RE = re.compile(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def extract_sections(html_body: str) -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    current_h2: str | None = None
    for m in _HEADING_RE.finditer(html_body):
        level = m.group(1)
        hid = m.group(2)
        text = _TAG_RE.sub("", m.group(3)).strip()
        if level == "2":
            current_h2 = hid
            out.setdefault(current_h2, [])
        elif level == "3" and current_h2 is not None:
            out[current_h2].append((hid, text))
    return out


def build_sidebar(sections: dict[str, list[tuple[str, str]]]) -> str:
    out: list[str] = []
    out.append('<aside class="sidebar" aria-label="Contents">')
    out.append('<h2 class="sidebar-title">Contents</h2>')
    out.append('<nav class="sidebar-nav">')

    out.append('<ul class="nav-list nav-list-top">')
    out.append('<li><a href="#top">Top of article</a></li>')
    out.append('</ul>')

    def render_h3s(h2_id: str) -> str:
        children = sections.get(h2_id, [])
        if not children:
            return ""
        parts: list[str] = ['<ul class="nav-sublist">']
        for cid, ctext in children:
            parts.append(
                f'<li><a href="#{cid}">{html_lib.escape(ctext)}</a></li>'
            )
        parts.append("</ul>")
        return "".join(parts)

    last_cat: str | None = None
    for rel, cat, label in ARTICLES:
        if cat != last_cat:
            if last_cat is not None:
                out.append("</ul>")
            out.append(f'<h3 class="nav-heading">{html_lib.escape(cat)}</h3>')
            out.append('<ul class="nav-list">')
            last_cat = cat
        s = slug_for(rel)
        out.append(
            f'<li><a href="#{s}">{html_lib.escape(label)}</a>{render_h3s(s)}</li>'
        )
    if last_cat is not None:
        out.append("</ul>")

    out.append('<ul class="nav-list nav-list-tail">')
    for tail_id, tail_label in [
        ("see-also", "See also"),
        ("references", "References"),
        ("further-reading", "Further reading"),
        ("external-links", "External links"),
        ("citations", "Citations"),
    ]:
        out.append(f'<li><a href="#{tail_id}">{tail_label}</a></li>')
    out.append("</ul>")
    out.append("</nav>")
    out.append("</aside>")
    return "".join(out)


STYLE_CSS = """\
:root {
  --text: #202122;
  --muted: #54595d;
  --link: #36c;
  --visited: #6a60b0;
  --border: #a2a9b1;
  --border-light: #c8ccd1;
  --bg-subtle: #f8f9fa;
  --bg-page: #fff;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; scroll-padding-top: 64px; }

body {
  margin: 0;
  background: var(--bg-page);
  color: var(--text);
  font-family: sans-serif;
  font-size: 16px;
  line-height: 1.6;
}

a { color: var(--link); text-decoration: none; }
a:visited { color: var(--visited); }
a:hover { text-decoration: underline; }

.topbar {
  border-bottom: 1px solid var(--border-light);
  min-height: 50px;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1.5rem;
  font-size: 0.875rem;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 5;
}

.site-title {
  font-family: 'Linux Libertine', Georgia, Times, 'Source Serif 4', serif;
  font-size: 1.35rem;
  letter-spacing: 0.01em;
}

.topnav a { margin-right: 0.5rem; }

.search {
  margin-left: auto;
  min-width: 280px;
  border: 1px solid var(--border);
  padding: 0.35rem 0.5rem;
  font: inherit;
}

.page {
  display: grid;
  grid-template-columns: 16rem minmax(0, 60rem);
  gap: 2.5rem;
  max-width: 100rem;
  margin: 0 auto;
  padding: 1.25rem 1.5rem 4rem;
}

.sidebar {
  font-size: 0.875rem;
  color: var(--muted);
  position: sticky;
  top: 4rem;
  align-self: start;
  max-height: calc(100vh - 5rem);
  overflow-y: auto;
  padding-right: 0.5rem;
}

.sidebar-title {
  font-family: sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin: 0 0 0.5rem;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid var(--border-light);
  border: 0;
}

.nav-heading {
  font-family: sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  margin: 1rem 0 0.25rem;
  border: 0;
  padding: 0;
}

.nav-list {
  list-style: none;
  margin: 0 0 0.25rem;
  padding: 0;
}

.nav-list li { margin: 0.1rem 0; }

.nav-list a {
  display: block;
  padding: 0.18rem 0.5rem;
  border-radius: 2px;
  color: var(--link);
  line-height: 1.35;
}

.nav-list a:hover {
  background: var(--bg-subtle);
  text-decoration: none;
}

.nav-list-top a,
.nav-list-tail a { font-weight: 600; }

.nav-sublist {
  list-style: none;
  margin: 0.1rem 0 0.2rem;
  padding: 0;
  border-left: 1px solid var(--border-light);
  margin-left: 0.5rem;
}

.nav-sublist li { margin: 0.05rem 0; }

.nav-sublist a {
  display: block;
  padding: 0.12rem 0.5rem 0.12rem 0.75rem;
  border-radius: 2px;
  color: var(--link);
  font-size: 0.82rem;
  line-height: 1.3;
}

.nav-sublist a:hover {
  background: var(--bg-subtle);
  text-decoration: none;
}

.content { min-width: 0; }

.page-subtitle {
  color: var(--muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}

h1, h2, h3 {
  font-family: 'Linux Libertine', Georgia, Times, 'Source Serif 4', serif;
  font-weight: 400;
  line-height: 1.3;
}

h1 {
  font-size: 1.95rem;
  margin: 0 0 0.5rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.25rem;
}

h2 {
  font-size: 1.55rem;
  margin: 1.75rem 0 0.4rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.15rem;
}

h3 {
  font-size: 1.25rem;
  margin: 1.25rem 0 0.3rem;
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 0.1rem;
}

h4 {
  font-size: 1.05rem;
  margin: 1rem 0 0.25rem;
  font-family: sans-serif;
  font-weight: 700;
}

h5 {
  font-size: 0.95rem;
  margin: 0.8rem 0 0.25rem;
  font-family: sans-serif;
  font-weight: 700;
}

p { margin: 0.5rem 0 1rem; }

ul, ol { margin: 0.4rem 0 0.8rem; padding-left: 1.4rem; }
li { margin: 0.2rem 0; }

code {
  font-family: Menlo, Consolas, 'DejaVu Sans Mono', monospace;
  font-size: 0.875em;
  background: var(--bg-subtle);
  padding: 0.05em 0.3em;
  border: 1px solid var(--border-light);
  border-radius: 2px;
}

pre {
  background: var(--bg-subtle);
  border: 1px solid var(--border-light);
  padding: 0.75rem 1rem;
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.5;
}

pre code { background: transparent; border: 0; padding: 0; }

blockquote {
  border-left: 4px solid var(--border-light);
  margin: 0.75rem 0;
  padding: 0.1rem 0.9rem;
  color: var(--muted);
  background: var(--bg-subtle);
}

hr {
  border: 0;
  border-top: 1px solid var(--border-light);
  margin: 1.5rem 0;
}

.article-tabs {
  border-bottom: 1px solid var(--border-light);
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.8rem;
  margin: 0.25rem 0 1rem;
  padding-bottom: 0.35rem;
  color: var(--muted);
}

.tab-active { color: var(--text); font-weight: 600; }

.wikitable {
  border-collapse: collapse;
  background: var(--bg-subtle);
  color: var(--text);
  margin: 1em 0;
  font-size: 95%;
}

.wikitable th,
.wikitable td {
  border: 1px solid var(--border);
  padding: 0.35em 0.55em;
  vertical-align: top;
}

.wikitable th {
  background: #eaecf0;
  text-align: center;
  font-weight: 700;
}

.infobox {
  float: right;
  clear: right;
  width: 22em;
  margin: 0.5em 0 1em 1.25em;
  border: 1px solid var(--border);
  background: var(--bg-subtle);
  color: #000;
  padding: 0.2em;
  font-size: 88%;
  line-height: 1.5;
  border-spacing: 3px;
  border-collapse: separate;
}

.infobox-title {
  font-size: 125%;
  font-weight: bold;
  text-align: center;
  padding: 0.3em 0.2em;
}

.infobox-subtitle {
  text-align: center;
  font-style: italic;
  padding: 0 0.2em 0.4em;
  color: var(--muted);
}

.infobox th[scope="row"] {
  text-align: left;
  vertical-align: top;
  padding: 0.25em 0.4em;
  background: transparent;
  font-weight: 700;
  width: 9em;
}

.infobox td {
  vertical-align: top;
  padding: 0.25em 0.4em;
}

.hatnote {
  font-style: italic;
  color: var(--muted);
  margin: 0.25rem 0 1rem;
  padding-left: 1.6em;
  border-left: 0;
}

.references-list { font-size: 90%; }

sup.footnote-ref {
  font-size: 0.75em;
  line-height: 1;
  vertical-align: super;
}

sup.footnote-ref a { text-decoration: none; }
sup.footnote-ref a::before { content: "["; }
sup.footnote-ref a::after { content: "]"; }

div.footnote {
  font-size: 0.875em;
  margin-top: 2rem;
  border-top: 1px solid var(--border-light);
  padding-top: 1rem;
}

div.footnote ol { padding-left: 1.5rem; }
div.footnote li { margin: 0.4rem 0; }

a.footnote-backref {
  text-decoration: none;
  margin-left: 0.4em;
}

@media (max-width: 900px) {
  .page {
    display: block;
    padding: 1rem;
  }
  .sidebar {
    position: static;
    max-height: none;
    overflow: visible;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
  }
  .infobox {
    float: none;
    width: 100%;
    margin: 1rem 0;
  }
  .search { display: none; }
  .topbar { flex-wrap: wrap; gap: 0.5rem; }
  .float-right { float: none; max-width: 100%; margin: 1rem 0; }
  .hero-image { max-height: 280px; }
}

/* Image styling */
.infobox-image-cell {
  padding: 0.4rem 0.5rem !important;
  text-align: center;
}
.infobox-image {
  display: block;
  width: 100%;
  height: auto;
  max-height: 220px;
  object-fit: cover;
  margin: 0 auto;
}
.infobox-image-caption {
  font-size: 0.78rem;
  color: #555;
  font-style: italic;
  margin-top: 0.35rem;
  line-height: 1.3;
  text-align: left;
}
.float-right {
  float: right;
  max-width: 320px;
  margin: 0.3rem 0 1rem 1.5rem;
  clear: right;
}
.float-right img {
  display: block;
  width: 100%;
  height: auto;
  border: 1px solid var(--border-light);
}
.float-right figcaption {
  font-size: 0.82rem;
  color: #666;
  font-style: italic;
  padding: 0.35rem 0.2rem 0;
  line-height: 1.35;
}
.logo-inline {
  height: 48px;
  width: auto;
  vertical-align: middle;
  margin: 0 0.5rem 0.3rem 0;
}
.logo-thumb {
  height: 24px;
  width: auto;
  vertical-align: middle;
  margin-right: 0.4rem;
}
.dod-seal-header {
  float: right;
  height: 110px;
  width: auto;
  margin: 0 0 1rem 1.5rem;
}
"""


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>U.S. Defense Contracting: A Structural Reference</title>
<link rel="stylesheet" href="assets/style.css">
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['\\\\(', '\\\\)']],
    displayMath: [['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }}
}};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body id="top">
<div class="page">
{sidebar}

<main class="content">
  <div class="page-subtitle">Encyclopedic overview</div>
{body}
</main>

</div>
</body>
</html>
"""


def main() -> int:
    index_md = (WIKI / "INDEX.md").read_text(encoding="utf-8-sig")
    pieces = extract_index_pieces(index_md)

    tabs_block = (
        '<div class="article-tabs">'
        '<span class="tab-active">Article</span>'
        '<span>Talk</span>'
        '<span>Read</span>'
        '<span>Edit</span>'
        '<span>View history</span>'
        '</div>'
    )

    parts: list[str] = []
    parts.append(pieces["lead_md"])
    parts.append("")

    for rel, _cat, _label in ARTICLES:
        p = WIKI / rel
        if not p.exists():
            print(f"  WARN missing: {rel}", file=sys.stderr)
            continue
        text = p.read_text(encoding="utf-8-sig")
        _fm, body = split_frontmatter(text)
        body = insert_blank_lines_before_lists(body)
        body = demote_remaining_headings(body)
        body = attach_slug_to_h1(body, slug_for(rel))
        parts.append(body)
        parts.append("")

    if pieces["see_also_md"]:
        parts.append(pieces["see_also_md"])
    if pieces["references_md"]:
        parts.append(pieces["references_md"])
    if pieces["further_reading_md"]:
        parts.append(pieces["further_reading_md"])
    if pieces["external_links_md"]:
        parts.append(pieces["external_links_md"])

    combined_md = "\n".join(parts)
    combined_md, math_placeholders = preprocess_math_tags(combined_md)

    md = markdown.Markdown(
        extensions=["extra", "attr_list", "toc", "footnotes"],
        extension_configs={
            "toc": {"permalink": False, "anchorlink": False},
            "footnotes": {"UNIQUE_IDS": False, "BACKLINK_TEXT": "↩"},
        },
        output_format="html5",
    )
    html_body = md.convert(combined_md)
    html_body = postprocess_math_tags(html_body, math_placeholders)

    after_h1_blocks: list[str] = [tabs_block]
    if pieces["hatnote"]:
        after_h1_blocks.append(
            f'<p class="hatnote">{pieces["hatnote"]}</p>'
        )
    if pieces["infobox_html"]:
        after_h1_blocks.append(pieces["infobox_html"])

    html_body = html_body.replace(
        "</h1>",
        "</h1>\n" + "\n".join(after_h1_blocks),
        1,
    )

    html_body = rewrite_cross_links(html_body)
    html_body = add_wikitable_class(html_body)
    html_body = html_body.replace(
        '<div class="footnote">',
        '<h2 id="citations">Citations</h2>\n<div class="footnote">',
        1,
    )

    sections = extract_sections(html_body)
    sidebar = build_sidebar(sections)
    final_html = PAGE_TEMPLATE.format(sidebar=sidebar, body=html_body)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (OUT_DIR / "index.html").write_text(final_html, encoding="utf-8")

    print(f"Wrote {OUT_DIR / 'index.html'}")
    print(f"  size: {(OUT_DIR / 'index.html').stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
