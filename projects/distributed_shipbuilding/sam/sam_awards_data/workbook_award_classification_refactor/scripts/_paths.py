"""_paths - project path anchors, derived from this file's location.

Single source of truth for the repo-root / project paths the build scripts need, so
no script hardcodes an absolute machine path. Import the anchors you need, e.g.

    from _paths import REPO, REFACTOR, EXTRACTED, AC, CORPUS_SCRIPTS

A script run as `python3 scripts/<name>.py` (or from within scripts/) has this
directory on sys.path[0], so a bare `import _paths` resolves before any sys.path
manipulation. Every anchor is computed from __file__, so moving the checkout (or
running on another machine) needs no edits.
"""
from __future__ import annotations

from pathlib import Path

SCRIPTS        = Path(__file__).resolve().parent          # .../workbook_award_classification_refactor/scripts
REFACTOR       = SCRIPTS.parent                            # .../workbook_award_classification_refactor
AC             = REFACTOR.parent                           # .../award_classification
SAM            = AC.parent                                 # .../sam
REPO           = SAM.parents[2]                            # .../ooxml_build_pipelines_light  (sam -> distributed_shipbuilding -> projects -> repo)
REPO_ROOT      = REPO                                      # alias
EXTRACTED      = REFACTOR / "extracted"                    # generated-artifact dir the workbook packages
CORPUS_SCRIPTS = AC / "corpus" / "scripts"                # shared corpus loader (_corpus.py)

# Sanity: the anchors must resolve to a real checkout (fail loud if the depth assumption breaks).
assert (REPO / "workbook_core").is_dir(), f"REPO anchor wrong: {REPO}"
assert EXTRACTED.is_dir(), f"EXTRACTED anchor wrong: {EXTRACTED}"
