"""docx_core.doc_probe - read-only inspector for Word page modules and .docx files.

Reports what the emitted WordprocessingML actually says. Like sheet_probe and
slide_probe, it never builds, repairs, or judges - it is a pure inventory of the
artifact, not a linter or a pass/fail.

Two modes (auto-detected from the target):
  module mode: a dotted module path (doc_consolidated.pages.overview) or a .py
               file - import it, run render(), wrap the PageModuleSpec body in a
               document(), and inspect the emitted XML.
  file mode:   a built .docx - open the zip and parse word/document.xml.

It reports: paragraphs (with w:pStyle resolved back to its style_ids name), runs
(text + props), tables (style, rows/cols), list paragraphs (numId/ilvl),
bookmarks, drawings (kind/name/extent), the page setups, and rollups (heading
outline, source lines, structured-block headings, ASCII/wireframe-table counts).
Markdown + JSON, written to the out dir (replacing, never stacking).

Usage:
    python docx_core/doc_probe.py <target> [--json] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Make the workspace root importable (for docx_core.*) and the current working
# directory importable (for a doc_<program> package run from its build dir).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.getcwd())

from docx_core.ooxml import NS_W, NS_WP, NS_MC         # noqa: E402
from docx_core.specs import PageModuleSpec             # noqa: E402
from docx_core.page_setup import PAGE_PORTRAIT         # noqa: E402
from docx_core.primitives import document              # noqa: E402
import docx_core.style_ids as _sid                     # noqa: E402

_W = f"{{{NS_W}}}"
_WP = f"{{{NS_WP}}}"
_MC = f"{{{NS_MC}}}"
# Reverse map: styleId value -> constant name (P_BODY, T_RULE, ...).
_ID_TO_NAME = {v: k for k, v in vars(_sid).items()
               if isinstance(v, str) and not k.startswith("_")}


def _q(tag: str) -> str:
    return _W + tag


def _style_name(style_id: str | None) -> str:
    if not style_id:
        return "(none)"
    return f"{style_id} [{_ID_TO_NAME.get(style_id, '?')}]"


# ---------------------------------------------------------------------------
# Target resolution
# ---------------------------------------------------------------------------

def _load_module(target: str):
    """Import a page module from a dotted path or a .py file."""
    if target.endswith(".py"):
        import importlib.util
        path = Path(target).resolve()
        sys.path.insert(0, str(path.parent))
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, path.stem
    import importlib
    mod = importlib.import_module(target)
    return mod, target.rsplit(".", 1)[-1]


def _render_module(mod):
    """Run a module's render() (lenient: accept PageModuleSpec, list, or str)."""
    fn = getattr(mod, "render", None)
    if not callable(fn):
        stem = mod.__name__.rsplit(".", 1)[-1]
        fn = getattr(mod, f"render_{stem}", None)
    if not callable(fn):
        raise AttributeError(f"{mod.__name__} exposes no render()/render_<stem>()")
    out = fn()
    if isinstance(out, PageModuleSpec):
        body, props = out.body, out.page_setup
    elif isinstance(out, list):
        body, props = out, None
    else:
        body, props = [str(out)], None
    sect = (props or PAGE_PORTRAIT).to_sectpr_xml()
    return document("".join(body), sect_pr=sect)


def _document_xml(target: str) -> tuple[str, str]:
    """Return (document_xml, report_name) for either a .docx or a module."""
    if target.endswith(".docx"):
        with zipfile.ZipFile(target) as z:
            return z.read("word/document.xml").decode("utf-8"), Path(target).stem
    mod, name = _load_module(target)
    return _render_module(mod), name


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------

def _run_facts(r) -> dict:
    rpr = r.find(_q("rPr"))
    text = "".join(t.text or "" for t in r.iter(_q("t")))
    facts = {"text": text}
    if rpr is not None:
        rstyle = rpr.find(_q("rStyle"))
        if rstyle is not None:
            facts["rStyle"] = rstyle.get(f"{_W}val")
        if rpr.find(_q("b")) is not None:
            facts["bold"] = True
        if rpr.find(_q("i")) is not None:
            facts["italic"] = True
        color = rpr.find(_q("color"))
        if color is not None:
            facts["color"] = color.get(f"{_W}val")
        sz = rpr.find(_q("sz"))
        if sz is not None:
            facts["sz_hp"] = sz.get(f"{_W}val")
    return facts


def _para_facts(p) -> dict:
    ppr = p.find(_q("pPr"))
    style = None
    num = None
    if ppr is not None:
        ps = ppr.find(_q("pStyle"))
        if ps is not None:
            style = ps.get(f"{_W}val")
        numpr = ppr.find(_q("numPr"))
        if numpr is not None:
            ilvl = numpr.find(_q("ilvl"))
            numid = numpr.find(_q("numId"))
            num = {"numId": numid.get(f"{_W}val") if numid is not None else None,
                   "ilvl": ilvl.get(f"{_W}val") if ilvl is not None else "0"}
    runs = [_run_facts(r) for r in p.findall(_q("r"))]
    text = "".join(r["text"] for r in runs)
    return {"kind": "paragraph", "style": style, "num": num,
            "text": text, "runs": runs}


def _table_facts(tbl) -> dict:
    tblpr = tbl.find(_q("tblPr"))
    style = None
    if tblpr is not None:
        ts = tblpr.find(_q("tblStyle"))
        if ts is not None:
            style = ts.get(f"{_W}val")
    rows = tbl.findall(_q("tr"))
    grid = []
    for tr in rows:
        cells = []
        for tc in tr.findall(_q("tc")):
            txt = "".join(t.text or "" for t in tc.iter(_q("t")))
            cells.append(txt)
        grid.append(cells)
    n_cols = len(grid[0]) if grid else 0
    return {"kind": "table", "style": style, "rows": len(rows),
            "cols": n_cols, "grid": grid}


def _sect_facts(sectpr) -> dict:
    out = {}
    pgsz = sectpr.find(_q("pgSz"))
    if pgsz is not None:
        out["page_w"] = pgsz.get(f"{_W}w")
        out["page_h"] = pgsz.get(f"{_W}h")
        out["orient"] = pgsz.get(f"{_W}orient", "portrait")
    pgmar = sectpr.find(_q("pgMar"))
    if pgmar is not None:
        out["margins"] = {k: pgmar.get(f"{_W}{k}")
                          for k in ("top", "right", "bottom", "left")}
    return out


def _drawing_facts(el) -> list[dict]:
    """Factual inventory of every <w:drawing> reachable from `el`: kind (inline vs
    anchor), name (wp:docPr@name), extent (wp:extent cx/cy). Scope to mc:Choice
    (skip mc:Fallback) so the VML fallback is never double-counted; bare drawings
    with no AlternateContent fall back to scanning `el` directly. docPr/extent
    attributes are unprefixed. Pure inventory - no judgment."""
    choices = [c for ac in el.iter(_MC + "AlternateContent")
               for c in ac if c.tag == _MC + "Choice"]
    scopes = choices if choices else [el]
    out: list[dict] = []
    for scope in scopes:
        for kind in ("inline", "anchor"):
            for node in scope.iter(_WP + kind):
                docpr = node.find(_WP + "docPr")
                ext = node.find(_WP + "extent")
                out.append({
                    "drawing_kind": kind,
                    "name": docpr.get("name") if docpr is not None else None,
                    "cx": ext.get("cx") if ext is not None else None,
                    "cy": ext.get("cy") if ext is not None else None,
                })
    return out


def inspect(document_xml: str) -> dict:
    root = ET.fromstring(document_xml)
    body = root.find(_q("body"))
    blocks: list[dict] = []
    bookmarks: list[str] = []
    page_setups: list[dict] = []
    drawings: list[dict] = []
    for el in list(body):
        tag = el.tag
        if tag == _q("p"):
            # bookmarks may be inline children of the paragraph
            for bm in el.findall(_q("bookmarkStart")):
                bookmarks.append(bm.get(f"{_W}name"))
            # a paragraph whose pPr holds a sectPr is a section break
            ppr = el.find(_q("pPr"))
            if ppr is not None and ppr.find(_q("sectPr")) is not None:
                page_setups.append(_sect_facts(ppr.find(_q("sectPr"))))
            drawings.extend(_drawing_facts(el))
            blocks.append(_para_facts(el))
        elif tag == _q("tbl"):
            drawings.extend(_drawing_facts(el))
            blocks.append(_table_facts(el))
        elif tag == _q("bookmarkStart"):
            bookmarks.append(el.get(f"{_W}name"))
        elif tag == _q("sectPr"):
            page_setups.append(_sect_facts(el))

    paras = [b for b in blocks if b["kind"] == "paragraph"]
    tables = [b for b in blocks if b["kind"] == "table"]
    style_counts: dict[str, int] = {}
    for p in paras:
        style_counts[p["style"] or "(none)"] = style_counts.get(p["style"] or "(none)", 0) + 1
    headings = [{"level": p["style"], "text": p["text"]}
                for p in paras if (p["style"] or "").startswith("Heading")]
    sources = [p["text"] for p in paras if p["style"] == _sid.P_SOURCE]
    structured_heads = [p["text"] for p in paras if p["style"] == _sid.P_BLOCK_HEADING]
    ascii_blocks = [p for p in paras if p["style"] in (_sid.P_CODE, _sid.P_CODE_SMALL)]
    wire_tables = [t for t in tables if t["style"] == _sid.T_WIREFRAME]
    lists = [p for p in paras if p["num"]]
    return {
        "summary": {
            "paragraphs": len(paras),
            "tables": len(tables),
            "list_paragraphs": len(lists),
            "bookmarks": len(bookmarks),
            "page_setups": len(page_setups),
            "drawings": len(drawings),
            "ascii_blocks": len(ascii_blocks),
            "wire_tables": len(wire_tables),
            "style_counts": style_counts,
        },
        "headings": headings,
        "sources": sources,
        "structured_blocks": structured_heads,
        "bookmarks": bookmarks,
        "page_setups": page_setups,
        "drawings": drawings,
        "tables": tables,
        "blocks": blocks,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def to_markdown(name: str, facts: dict) -> str:
    s = facts["summary"]
    out = [f"# doc_probe - {name}", ""]
    out.append("## Summary")
    out.append(f"- paragraphs: {s['paragraphs']}")
    out.append(f"- tables: {s['tables']}")
    out.append(f"- list paragraphs: {s['list_paragraphs']}")
    out.append(f"- bookmarks: {s['bookmarks']}")
    out.append(f"- page setups: {s['page_setups']}")
    out.append(f"- drawings: {s['drawings']}")
    out.append(f"- ASCII blocks: {s['ascii_blocks']}")
    out.append(f"- wireframe tables: {s['wire_tables']}")
    out.append("")
    out.append("## Paragraph styles")
    for st, c in sorted(s["style_counts"].items(), key=lambda kv: -kv[1]):
        out.append(f"- {_style_name(st if st != '(none)' else None)}: {c}")
    out.append("")
    if facts["headings"]:
        out.append("## Heading outline")
        for h in facts["headings"]:
            out.append(f"- {h['level']}: {h['text']}")
        out.append("")
    if facts["structured_blocks"]:
        out.append("## Structured block headings")
        for t in facts["structured_blocks"]:
            out.append(f"- {t}")
        out.append("")
    if facts["sources"]:
        out.append("## Source lines")
        for t in facts["sources"]:
            out.append(f"- {t}")
        out.append("")
    if facts["bookmarks"]:
        out.append("## Bookmarks")
        for b in facts["bookmarks"]:
            out.append(f"- {b}")
        out.append("")
    if facts["tables"]:
        out.append("## Tables")
        for i, t in enumerate(facts["tables"], 1):
            out.append(f"- table {i}: style {_style_name(t['style'])}, "
                       f"{t['rows']} rows x {t['cols']} cols; "
                       f"header: {t['grid'][0] if t['grid'] else []}")
        out.append("")
    if facts["drawings"]:
        out.append("## Drawings")
        for i, d in enumerate(facts["drawings"], 1):
            out.append(f"- drawing {i}: {d['drawing_kind']}, name {d['name']!r}, "
                       f"extent {d['cx']} x {d['cy']} EMU")
        out.append("")
    if facts["page_setups"]:
        out.append("## Page setups")
        for i, sec in enumerate(facts["page_setups"], 1):
            out.append(f"- page setup {i}: {sec}")
        out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Read-only Word page-module/.docx inspector.")
    ap.add_argument("target", help="dotted module path, a .py file, or a .docx file")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    ap.add_argument("--out-dir", default="reports/doc_probe",
                    help="output directory (default: reports/doc_probe)")
    args = ap.parse_args(argv)

    document_xml, name = _document_xml(args.target)
    facts = inspect(document_xml)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")
    if not args.json:
        md = to_markdown(name, facts)
        (out_dir / f"{name}.md").write_text(md, encoding="utf-8")
        print(md)
    else:
        print(json.dumps(facts["summary"], indent=2))
    print(f"\n[doc_probe] wrote {out_dir / name}.json"
          + ("" if args.json else f" + {out_dir / name}.md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
