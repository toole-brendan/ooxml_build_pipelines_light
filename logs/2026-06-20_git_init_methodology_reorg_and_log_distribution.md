# 2026-06-20 — Git init, distributed_shipbuilding methodology-first reorg, log distribution

Workspace-wide session. Lives in the root `logs/` because the work spans the whole repo
(version control, a cross-project structural reorg, and redistributing every project's logs) —
not any single sub-project. Sits alongside the other workspace-restructure logs here
(`core_tree_restructure`, `light_workspace_flatten_standardize`, `overview_restructure`).

Logging convention going forward (established this session):
- **workspace-wide** (git, cross-project structure, repo conventions) → root `logs/`
- **distributed_shipbuilding cross-cutting** (spans tam+sam+decks) → `projects/distributed_shipbuilding/logs/`
- **sub-project specific** → that sub-project's own `logs/` (e.g. `tam/ddg/logs/`, `sam/award_classification/logs/`);
  note workbook/build logs go in `<subproject>/logs/`, research-session logs in `<subproject>/research/logs/`.

---

## 1. Git — workspace put under version control + pushed

Repo was NOT a git repo at session start. Now it is, and it's backed up to a private GitHub repo.

- `git init` at repo root → **full snapshot** commit `93effc84` (everything except secrets + junk).
- **`.gitignore` rewritten**: secrets (`.env*`) + junk (`__pycache__`, `.DS_Store`, venvs, tool caches).
  The pre-existing `.gitignore` did **not** exclude `.env` (holds `SAM_API_KEY`) and blanket-ignored
  `research/` (which would have dropped the corpus code) — both fixed. `.env` is gitignored and was
  never committed.
- **Pushed** to `https://github.com/toole-brendan/ooxml_build_pipelines_light` (**PRIVATE**), `master`
  tracks `origin/master`. Auth via `gh` (account `toole-brendan`).
- **GitHub 100 MB blocker**: two `mro` QA fixtures (`mro/workbook/qa/{gold,new}/probe/09_Awards.json`,
  103 MB each) exceeded the hard limit. Per user: deleted. Because they were in the snapshot commit,
  purged from ALL history via `git filter-branch` (commit hashes rebased), then gitignored. (This is
  why hashes below differ from the original snapshot's `a6bd7cd`.)

## 2. distributed_shipbuilding → methodology-first (commit `cf9d71bb`)

Re-architected so TAM vs SAM is the top-level split and the former sibling `research_shared` moved in.

Target layout: `tam/` + `sam/` + `research_shared/` + `decks/` + `docs/`.
- TAM workbooks → `tam/{submarines,ddg,consolidated,outsourcing_ceiling}` (collapsed the `workbook/` level)
- SAM `award_analysis` → `sam/award_analysis`
- `projects/research_shared` (sibling) → `distributed_shipbuilding/research_shared`; its `corpus` (= the old
  `distributed_shipbuilding/research/`, holding `_corpus.py`) → `research_shared/corpus`
- decks → `decks/{submarines,ddg,consolidated,primary}`; docs → `docs/{submarines,shipbuilding}`
- dropped stray duplicate `ddg/workbook_submarines`

**Path mechanics (the load-bearing part).** Packages find the shared engines
(`workbook_core`/`deck_core`/`docx_core` at repo root) via `Path(__file__).resolve().parents[N]`.
- The single dangerous edit: `PROJECT_DIR = parents[2]` (where output is written) → `parents[1]` for every
  moved workbook/deck/doc, else all outputs would silently collide in the methodology bucket. (SAM refactor
  is the exception — keeps `parents[2]`.)
- Flat-origin packages (`parents[4]`) that gained a level bumped engine N `4→5`; nested-origin (`parents[5]`)
  stayed. Path-literal repaths done globally (slash + `os.path.join` token forms) with assert-once edits.
- No symlinks exist under the tree (the rumored ddg→sub research symlink is false). `projects2/...` paths in
  research scripts are pre-existing dead refs, left untouched.

## 3. research_shared dissolved (commit `e8bd10fe`)

Per user revision: `research_shared` should not survive as a unit.
- whole `research_shared` → `sam/award_classification` (the refactor pipeline + corpus + supplier_bucketing +
  taxonomy_* + sam_entity_enrichment + worklists + vendor_research + caveats + the .xlsx)
- `budget_books` pulled out → `tam/shared/budget_books` (budget materials = TAM)
- per-ship research merged: `submarines/research` → `tam/submarines/research`, `ddg/research` → `tam/ddg/research`;
  empty `submarines/`+`ddg/` shells removed
- depth fixes: refactor package `parents[5]→[6]`; the 5 per-ship research scripts that walk to repo root got
  one extra `..` (research moved a level deeper under `tam/`)
- `_corpus.py` repathed (absolute `REPO`, so only its relative literals changed): `REGISTRY_CSV`,
  `EXTRACTED`, and the per-ship `fullhistory`/`naics` inputs

## 4. Deletions
- 5 stale loose planning `.md` at ds root (commit `70112303`)
- 2 unattributed legacy `.pptx` at ds root (commit `777ad675`) — no build produces them
- 2 oversized mro QA fixtures (above)
- **All 21 auto-memories** (incl. `MEMORY.md`) deleted at user request — nothing auto-loads now.

## 5. Logs distributed (commit `3eb1091e`)
The root `logs/` had 116 pre-per-project session logs. Routed 113 to their relevant projects; 3 workspace-wide
stayed at root (this file makes 4). mro (18), sea_range_telemetry (2), gso_JM_reference (1), core libs
(workbook_core 4 / docx_core 4 / deck_core 3) → own `logs/`; the 81 distributed_shipbuilding logs split
fine-grained across `tam/sam/decks/docs` sub-projects with 12 genuinely cross-cutting ones in
`distributed_shipbuilding/logs/`.

## Verification
Every structural change was checked by rebuilding **all 12 pipelines** (6 workbooks + 4 decks + 2 docs) from
their new locations against a pre-reorg baseline — all green, every sheet/slide/page count matched, outputs
landed in the new folders. Corpus import, `extract_workbook_cuts.py`, `build_ceiling_base.py`, the SAM
`build_program_vendors.py`, and the 4 validators (`0 XML errors`) all pass from the new paths.

## Commit trail (HEAD = `777ad675`)
```
777ad675 Delete 2 unattributed legacy .pptx
3eb1091e Distribute root logs/ into per-project logs/
89625d61 Drop 2 oversized mro QA fixtures (>100MB) + gitignore
e8bd10fe Dissolve research_shared into sam/ + tam/
70112303 Delete stale loose planning docs
cf9d71bb Reorg distributed_shipbuilding -> methodology-first
93effc84 Initial snapshot (pre-reorg)
```

## Open / not done
- Migration scripts were one-shot in `/tmp` (`reorg_migrate.py`, `reorg_migrate2.py`, `route_logs.py`) — not kept in-repo.
- A few log-routing calls were judgment (cross-cutting → `distributed_shipbuilding/logs/`); trivially `git mv`-able if any are misfiled.
- `tam/shared` currently holds only `budget_books`; `supplier_bucketing`/`corpus`/`reference_prior_analysis` went to `sam/award_classification` (the dismissed-question default — flip-able if wanted).
