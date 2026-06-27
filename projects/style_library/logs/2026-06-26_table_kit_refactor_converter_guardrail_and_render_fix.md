# Session log & handoff — table-readability kit, converter kit-emission + clobber guardrail, and the LibreOffice empty-cell render fix

**Date:** 2026-06-26 (continues the 2026-06-24/25 docs in this `logs/` folder)
**Project:** `projects/style_library/` — canonical corpus at `library/` (build dir) + `library/library/` (package).
**Engine touched:** `deck_core/primitives.py` (read only — no change needed; `tpara(end_size=)` already existed).
**Converter touched:** `_tools/convert_slide.py` (kit emission + guardrail).
**Slides touched:** all **40** modules got a `# HAND-POLISHED` sentinel; **24** table modules refactored; **2** got the render fix.

Big picture: tables were the one thing the corpus had left **inline + verbatim** (the prior "do-NOT-extract-table-internals" convention). The user rejected that. This session (1) gave every table a per-module **kit** that separates cell CONTENT from MECHANICS, render-identical; (2) updated the **converter** to emit that kit for future slides AND to **refuse to clobber** hand-polished modules; (3) fixed the pre-existing **LibreOffice row-overflow** on the worst converted tables. Build green throughout (40 slides, 22 charts).

---

## 1. The table kit (the spine)

A small **local, per-module** kit, pasted after `CHARTS`, that wraps the low-level primitives. It is
**render-byte-identical** to the raw form (proven, see §2):

```python
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's 60960 cell padding
def edge(color, w=12700): return {"color": color, "width": w}
def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L",L),("R",R),("T",T),("B",B)) if v is not None} or None
def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10), align="l",
         anchor="ctr", span=1, rowspan=1, l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell(text, ..., grid_span=span, row_span=rowspan, font=FONT, l_ins=..., borders=bd(**edges))
def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1, l_ins=45720, ..., **edges):
    return tcell_rich(paras, grid_span=span, row_span=rowspan, anchor=anchor, ..., borders=bd(**edges))
```
**Why it's byte-faithful:** an omitted border edge, `None`, and `"none"` ALL emit `<a:noFill/>`, and the
engine emits sides in fixed L,R,T,B order — so `bd()` naming only the drawn edges (in any order) is
identical to the source's explicit `"T":"none"` noise. `cell`/`rcell` defaults equal the `tcell`/
`tcell_rich` engine defaults, so omitting a kwarg == the default. **Insets:** pass `**PAD` when all four
are 60960, omit when 45720 (default), pass explicit for anything else (e.g. 41564, 37785).

Two more helpers used where they paid off:
- `mt(align="ctr")` — empty matrix-cell paragraph; in the worst sparse matrix it also carries the render
  fix (`end_size=PT(1)`, see §4).
- `r(text, *, b, i, u, color=BLACK, size=PT(N))` — one rich-text run, collapses the repeated
  `size=/color=/font=` on the text-wall slides. The transform was done by `scratchpad/runify.py`
  (regex, **text captured verbatim, never retyped** — the only safe way to touch unicode-heavy prose).

Recipes by table shape: **regular grids** → extract cell content to a module list + comprehension over
`cell()` (key_terms_glossary, coordination_archetypes, assumptions_income_statement_2 OpEx family);
**sparse matrices / hybrids** → keep the row-by-row layout, wrap cells in `cell()`/`rcell()`+`edge()`;
**text walls** (key_findings_*) → `r()` per run, one `tpara` per line; **single-cell labels** → trivial wrap.

---

## 2. Rollout (24 modules) + the render-identity gate

The gate is `scratchpad/render_one.py`: import a module **standalone** (NOT through the slides registry,
so concurrent edits to siblings can't interfere) and diff `render()` vs a baseline snapshot
(`scratchpad/baseline/NN_module.xml`, captured before any edits). Race-free → **parallel subagents were
safe**: I did the hardest matrix (approach_unit_economics) + the two text-walls myself, then fanned out
the other 18 modules across 4 subagents and the 3 bordered+bulleted hybrids to a 5th, each gated on
`check.sh <module> → IDENTICAL`. I then re-verified all 21 subagent modules myself, and a **full
40-slide diff was 0/40**. Build green. (One transcription slip on the matrix — a stray `B=edge(WHITE)` —
was caught by the per-cell diff and fixed; that's the gate working.)

---

## 3. Converter: emit the kit + clobber guardrail (`convert_slide.py`)

**Kit emission (future slides).** `render_cell`/`render_table` now emit `cell()`/`rcell()`/`edge()`/
`**PAD` (helpers `_edge_lit`/`_border_kw`/`_inset_kw`), dropping `"none"` edges; `build_module_text`
injects the `_TABLE_KIT` block when `stats["table"]`; `_imports` still imports tcell/tcell_rich/PT/
BLACK/FONT (used only inside the kit) by scanning the kit text appended to `all_text`. Verified by
**round-tripping a slide out of `library.pptx`** → emitted module uses the kit, compiles, and its
`<a:tbl>` renders byte-identical.

**Guardrail (the user's hard ask — never re-convert these by hand).** `convert()` now, before any work:
if `out_path` exists and contains `HANDPOLISH_MARKER` ("HAND-POLISHED") → **refuse even with `--force`**;
else if it exists and no `--force` → refuse. `main()` gained `--force`. Tested all four cases. Every one
of the **40** library modules carries a top-of-file `# HAND-POLISHED — do not regenerate…` sentinel, so
the whole curated corpus is protected, not just the 24 tables.

---

## 4. Render fix — LibreOffice empty-cell 18pt overflow (intentional render change)

The user noticed `approach_unit_economics` (slide 24) renders badly in LibreOffice: the table balloons
and bottom rows run off-slide. Root cause: an **empty cell** (`tpara([])` with no `end_size`) emits a
bare `<a:endParaRPr lang="en-US"/>`; LibreOffice floors it at ~18pt. A row's height = max over its cells,
so **one** naked empty cell floors the whole row at ~18pt. PowerPoint renders the same XML compactly —
it's a LibreOffice divergence. Fix = think-cell's own trick: `end_size=PT(1)` on empty cells. Decided to
keep the readability refactor render-preserving and do this as a **separate pass** (user's choice).

Diagnosis tool: count REAL naked empty cells per table — `<a:tc>` with `<a:endParaRPr lang="en-US"/>`,
no `<a:t>`, **excluding `hMerge`/`vMerge` placeholders** (those carry a bare endParaRPr too but don't
drive row height — the main false positive; they made slide 24 look unfixed until excluded).

Fixed (verified by LibreOffice PDF render, before/after):
- **slide 24 approach_unit_economics** — `mt()` → `end_size=PT(1)` (108 empties); table now fits.
- **slide 23 assumptions_income_statement_2** — empty Category cells → `end_size=PT(1)` (11); last row
  ("Insurance") no longer overlaps the footer.

Both changes are surgical: normalizing `sz="100"`→naked makes the render **identical to baseline except
the empty-cell sizes** (108 / 11 additions, everything else byte-equal).

Checked, **left as-is**: `comparison_vs_ddgs` (38, renders fine — big merged cells dominate),
`assumptions_income_statement_1` (22, fine), `key_findings_what_must_be_true` (5, content-dense/tight
but the 2 naked cells aren't the constraint), `key_inputs` (28, genuinely content-dense / 0 naked cells
— fills the page; the user deferred this; needs smaller font/padding, not the end_size lever).

See [[libreoffice-empty-table-cell-18pt-overflow]].

---

## 5. State & for the next agent

- **24 table modules** now use the kit; **all 40** carry the `HAND-POLISHED` sentinel; build green
  (40 slides, 22 charts). Render is byte-identical to the pre-session baseline on **38** slides; slides
  **23 & 24** differ ONLY by empty-cell `end_size` (the intentional render fix).
- **Do NOT re-run the converter on any `library/library/slides/*.py`** — it now refuses (sentinel hard-
  stop). The converter is for NEW slides; it emits the kit + `local_meaning: TODO` stubs.
- **Open render candidates the user may still want addressed:** `key_inputs` (28) and
  `key_findings_what_must_be_true` (5) are content-dense and fill/tighten to the slide bottom — NOT the
  empty-cell bug; fixing needs a font/padding judgment call on the deck.
- **Scratchpad tools (reusable):** `render_one.py` + `check.sh` (per-module byte gate), `dump_renders.py`
  (all-40 snapshot), `runify.py` (trun→r, text-preserving), `estimate_overflow.py` + the naked-empty
  counter (overflow triage), `kit_proof.py`/`cell_proof.py` (the render-identity proofs).
- **Memory:** updated [[pptx-to-idiomatic-module-workflow]]; added [[libreoffice-empty-table-cell-18pt-overflow]].
  Older `logs/` path references predate the `library/` rename (map `schematics_curated/schematics` → `library/library`).
