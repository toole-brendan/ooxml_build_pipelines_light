"""data_worktype_evidence - the "Worktype Evidence" tab (one module = one sheet).

Top vendors per work-type bucket, plus an unbucketed watchlist - all linking back
to Entity Master. Reading evidence for why each bucket's observed share looks the
way it does. Imports Entity Master (row/index helpers, observed bucket $) and the
taxonomy (the bucket list). Pure consumer: it exports no accessors, so the whole
sheet is laid out with one render-local cursor (no hardcoded row anchors - the
former at-a-glance / evidence-base row collision is gone by construction).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines.taxonomy import BUCKETS, UNBUCKETED
from workbook_master_tam.sheets.submarines import data_entity_master as _em
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub Worktype Evidence"
_N_TOP = 3
_N_WATCH = 10
_LETTERS = "abcdefghijklmnop"
_HDR_VENDOR = [S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT]


def _evidence_count(bucket):
    return len(_em.top_vendor_indices(bucket, 10 ** 6))


def _render_worktype_evidence() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("Worktype Evidence", n_cols=5, style=S_TITLE_SHEET)
    c.blank()

    # §1 headline
    c.banner("§1 - Supplier $ + top vendor per bucket", n_cols=5, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Bucket", "Supplier $M", "Top vendor", "Evidence count"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER])
    for key, name, _defn in BUCKETS:
        idxs = _em.top_vendor_indices(key, 1)
        top = f"={_em.ent_row_cell(idxs[0], 'vendor')}" if idxs else "-"
        c.write([name, f"={_em.observed_bucket_dollar_cell(key)}", top, _evidence_count(key)],
                styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT])
    widxs1 = _em.unbucketed_vendor_indices(1)
    utop = f"={_em.ent_row_cell(widxs1[0], 'vendor')}" if widxs1 else "-"
    c.write(["Unbucketed / ambiguous", f"={_em.observed_bucket_dollar_cell(UNBUCKETED)}",
             utop, len(_em.unbucketed_vendor_indices(10 ** 6))],
            styles=[S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT])
    c.blank(2)

    # §2 Top vendors per bucket (links to Entity Master)
    c.banner("§2 - Top vendors per bucket (links to Entity Master)", n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    for bi, (key, name, _defn) in enumerate(BUCKETS):
        c.banner(f"§2{_LETTERS[bi]} - {name} (top {_N_TOP} by subaward $)", n_cols=5,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Rank", "Vendor", "$M", "NAICS desc", "Class rule"], styles=_HDR_VENDOR)
        for j, i in enumerate(_em.top_vendor_indices(key, _N_TOP)):
            c.write([j + 1, f"={_em.ent_row_cell(i, 'vendor')}", f"={_em.ent_row_cell(i, 'dollar')}",
                     f"={_em.ent_row_cell(i, 'naics_desc')}", f"={_em.ent_row_cell(i, 'basis')}"],
                    styles=[S_DEFAULT, S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT], outline_level=1)
        c.blank()

    # §2{last} Unbucketed watchlist
    c.banner(f"§2{_LETTERS[len(BUCKETS)]} - Unbucketed watchlist (top {_N_WATCH} supplier $, no clean bucket)",
             n_cols=5, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Rank", "Vendor", "$M", "NAICS desc", "Why unbucketed"], styles=_HDR_VENDOR)
    for j, i in enumerate(_em.unbucketed_vendor_indices(_N_WATCH)):
        c.write([j + 1, f"={_em.ent_row_cell(i, 'vendor')}", f"={_em.ent_row_cell(i, 'dollar')}",
                 f"={_em.ent_row_cell(i, 'naics_desc')}", f"={_em.ent_row_cell(i, 'basis')}"],
                styles=[S_DEFAULT, S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=[34, 36, 14, 26, 22],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


WORKTYPE_EVIDENCE = SheetEntry(_TAB, _GROUP, _render_worktype_evidence)
