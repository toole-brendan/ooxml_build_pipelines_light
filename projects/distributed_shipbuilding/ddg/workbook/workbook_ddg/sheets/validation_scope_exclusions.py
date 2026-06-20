"""validation_scope_exclusions - the "Scope Exclusions" tab (DDG, validation group).

Scope cleanup + excluded-PIID evidence. Data-driven from nc_scope_summary.json and
_discovered_piids.csv (no cross-sheet dependencies; exports nothing).
"""
from __future__ import annotations

import csv
import json

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.lib import EXTRACTED
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "Scope Exclusions"
_NCOLS = 3


def _make_scope_exclusions():
    def _classify(reason):
        if "IVECO" in reason or "Marine Corps" in reason:
            return "IVECO"
        if "WPN/OPN" in reason:
            return "WPN/OPN weapons"
        return "DDG-1000 / Zumwalt"

    _BLOCK_ORDER = ["IVECO", "DDG-1000 / Zumwalt", "WPN/OPN weapons"]
    _BLOCK_TITLE = {
        "IVECO": "IVECO - Marine Corps Mk110 gun (not DDG)",
        "DDG-1000 / Zumwalt": "DDG-1000 / Zumwalt - out of class (LI 2119, closed)",
        "WPN/OPN weapons": "WPN/OPN weapons - ESSM + CIWS, different appropriation",
    }

    def render() -> WorksheetSpec:
        with (EXTRACTED / "nc_scope_summary.json").open(encoding="utf-8") as fh:
            summ = json.load(fh)
        oos = summ["out_of_scope_piids"]
        blocks = {b: [] for b in _BLOCK_ORDER}
        for piid, reason in oos.items():
            reason = reason.replace(" — ", " - ").replace("—", "-")
            blocks[_classify(reason)].append((piid, reason))
        for b in blocks:
            blocks[b].sort(key=lambda t: t[0])
        fpds = {}
        with (EXTRACTED / "_discovered_piids.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                piid = (r.get("piid") or "").strip()
                try:
                    v = float(r.get("total_obligated_M", "") or 0)
                except ValueError:
                    v = 0.0
                if piid:
                    fpds[piid] = max(fpds.get(piid, 0.0), v)

        c = RowCursor(2)
        c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.blank()

        # §1 Cleanup summary
        c.banner("§1 - Cleanup summary (after removing 16 contaminant PIIDs)", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        kept = summ["records_kept"]
        excl = summ["records_excluded_out_of_scope_piids"]
        r_kept = c.write(["Records kept (in-scope)", kept],
                         styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
        r_excl = c.write(["Records excluded (out-of-scope PIIDs)", excl],
                         styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
        c.write(["Records pre-clean (kept + excluded)", f"=C{r_kept}+C{r_excl}"],
                styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
        c.write(["In-scope dollars ($M)", round(summ["total_dollars_in_scope_$M"], 1)],
                styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
        c.write(["Unique in-scope parent UEIs", summ["unique_parent_ueis_in_scope"]],
                styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
        c.blank(2)

        # §2 Excluded PIIDs by class
        c.banner("§2 - Excluded PIIDs by class (FPDS obligated $M = size indicator)", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        for n, block in enumerate(_BLOCK_ORDER):
            entries = blocks[block]
            letter = chr(ord("a") + n)
            c.banner(f"§2{letter} - {_BLOCK_TITLE[block]} ({len(entries)})", n_cols=_NCOLS,
                     style=S_TITLE_SUBSECTION, mark_collapsible=True)
            c.blank()
            c.write(["PIID", "Reason", "FPDS obligated $M"],
                    styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER])
            block_first = c.at()
            for piid, reason in entries:
                c.write([piid, reason, fpds.get(piid)],
                        styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT], outline_level=1)
            block_last = c.at() - 1
            c.total(["", f"Subtotal - {block}", f"=SUM(D{block_first}:D{block_last})"],
                    styles=[S_DEFAULT, S_BOLD, S_NUM], n_cols=3)
            c.blank(2)
        return WorksheetSpec(worksheet(c.rows, cols=[24, 40, 16],
                             tab_color=group_color(_GROUP), with_gutter=True))

    return SheetEntry(_TAB, _GROUP, render)


SCOPE_EXCLUSIONS = _make_scope_exclusions()
