"""data_worktype_evidence - the "Worktype Evidence" tab (DDG, data group; one module = one sheet).

Evidence support for the seven work-type buckets. The former Buckets section of the
composite Suppliers tab (buried at the bottom), now its own tab. The bucket map +
the top vendors per bucket (linked from Entities). Conceptually linked to
Methodology, but it does not duplicate the long taxonomy prose.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, build_table
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_TITLE_SHEET,
    S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets._taxonomy import BUCKETS
from workbook_ddg.sheets.data_entity_master import top_vendor_indices, ent_row_cell
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "Worktype Evidence"
_NCOLS = 4
_WT_NTOP = 3


def _make_bucket_evidence():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Bucket map
    c.banner("§1 - Bucket map", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    map_rows = [[name, defn, "", ""] for _k, name, defn in BUCKETS]
    blk, nxt = build_table(c.at(), headers=["Bucket", "Definition", "", ""], data_rows=map_rows,
                           header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(blk, nxt)
    c.blank(2)

    # §2 Top vendors by bucket (linked from Entities)
    c.banner("§2 - Top vendors by bucket (from Entities)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    for n, (key, name, _defn) in enumerate(BUCKETS):
        letter = chr(ord("a") + n)
        c.banner(f"§2{letter} - {name} (top {_WT_NTOP} by subaward $)", n_cols=_NCOLS,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Rank", "Vendor", "$M", "NAICS desc"],
                styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
        for j, i in enumerate(top_vendor_indices(key, _WT_NTOP)):
            c.write([j + 1, f"={ent_row_cell(i, 'vendor')}", f"={ent_row_cell(i, 'dollar')}",
                     f"={ent_row_cell(i, 'naics_desc')}"],
                    styles=[S_DEFAULT, S_DEFAULT, S_LINK_NUM, S_DEFAULT], outline_level=1)
        c.blank(2)

    # §3 Classification evidence
    c.banner("§3 - Classification evidence", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    ce, nxt = build_table(
        c.at(), headers=["Arbiter", "How it assigns role + bucket", "", ""],
        data_rows=[
            ["Evidence registry (primary)", "operating-entity UEI -> role + bucket (SAM-resolved NAICS)", "", ""],
            ["Vendor-name override", "known specialty vendors mapped directly (e.g. Curtiss-Wright -> piping)", "", ""],
            ["NAICS-4 fallback", "vendor NAICS-4 -> bucket for entities not in the registry (e.g. 3329 -> piping)", "", ""],
        ],
        header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(ce, nxt)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[10, 44, 12, 30],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


WORKTYPE_EVIDENCE = _make_bucket_evidence()
