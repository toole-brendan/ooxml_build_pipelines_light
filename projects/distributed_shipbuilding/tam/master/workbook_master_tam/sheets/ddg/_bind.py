"""DDG sub-package data binding.

Points EXTRACTED / load_extracted_csv at this program's namespaced slice of the
master extracted root. The relocated DDG sheet modules import these three names
(formerly from ``workbook_ddg.lib``).
"""
from __future__ import annotations

from workbook_core.lib import load_extracted_csv as _core_load_extracted_csv
from workbook_master_tam.lib import EXTRACTED as _ROOT, REGISTRY_CSV  # noqa: F401 (re-exported)

EXTRACTED = _ROOT / "ddg"


def load_extracted_csv(name: str):
    """Load extracted/ddg/<name>.csv."""
    return _core_load_extracted_csv(name, EXTRACTED)
