"""Award Classification Refactor pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data dir, the docProps identity),
exposes a load_extracted_csv wrapper bound to this pipeline's data dir, and
packages the SHEETS module list via the shared packager.

The extracted/ dir holds the per-sheet raw CSVs written verbatim from the manual
workbook by ``extract_classification_cuts.py`` (re-run only if the manual source
changes). Cell values are stored as strings so identifiers keep their exact form
(Work-type ID "01", CAGE "90099"); the sheet modules cast the numeric columns.

The build always writes the canonical ``award_classification_refactor.xlsx`` at the
project root.
"""
from __future__ import annotations

from pathlib import Path

from workbook_core.lib import (
    package_workbook,
    load_extracted_csv as _core_load_extracted_csv,
)
from workbook_core.primitives import set_normalize_dashes

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/
PROJECT_DIR = Path(__file__).resolve().parents[2]    # projects/distributed_shipbuilding/sam/award_classification/   (build output lands here)
REPO_ROOT = Path(__file__).resolve().parents[6]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "award_classification_refactor.xlsx"
EXTRACTED = WORKBOOK_DIR / "extracted"

_TITLE = "Award Classification Refactor - New-Construction Subaward Vendor Classification"
_CREATOR = "workbook_award_classification_refactor build_workbook.py"
_APP = "workbook_award_classification_refactor"


def load_extracted_csv(name: str) -> tuple[list[str], list[list]]:
    """Load extracted/<name>.csv from this pipeline's data dir (numeric-coerced)."""
    return _core_load_extracted_csv(name, EXTRACTED)


def build() -> int:
    """Render every registered sheet and package into the output xlsx.

    normalize_dashes is ON: visible literal em/en dashes render as hyphens so the
    workbook reads in one ASCII-clean dash convention (formulas bypass this branch,
    so any dash in a formula string must be fixed at the source - see the style
    audit in tools/style_audit.py).
    """
    # The flat sheets build their cell XML eagerly at import (make_flat_sheet runs at
    # module top level), so the dash-normalization switch must be ON *before* the sheet
    # modules are imported, not just when package_workbook renders the deferred sheets.
    set_normalize_dashes(True)
    from workbook_award_classification_refactor.sheets import SHEETS
    from workbook_award_classification_refactor.sheets._integrity import (
        assert_universes_aligned,
        assert_piids_in_manifest,
        assert_duplicate_audit_recorded,
        assert_archetype_codes_valid,
        assert_naics_rationale_aligned,
    )
    # Build-stopping guards (fail loudly before anything is packaged):
    #  - every transaction prime PIID is in the versioned scope manifest as include=Y, and
    #    no out-of-scope (include=N) prime leaked through;
    #  - program-vendor / transaction / dimension CSVs agree on the (Program x UEI) universe,
    #    or a stale pull would silently drop rows to dash / D0 / P0;
    #  - semantic duplicate-report candidates are accounted for by the adjudication log.
    assert_piids_in_manifest()
    assert_universes_aligned()
    assert_duplicate_audit_recorded()
    assert_archetype_codes_valid()
    assert_naics_rationale_aligned()
    return package_workbook(OUT, SHEETS, title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=True)
