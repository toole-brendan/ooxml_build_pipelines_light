"""data_notice_links - confirmed pre-award notice <-> contract-family links (analyst).

The evidence-scored bridge between an OPEN SAM notice and the watercraft family it most
likely recompetes, from the durable analyst/notice_family_links.csv. Each row pairs a
notice (notice_id / solicitation) with a family_key, the PSC/NAICS/office match flags that
earned its evidence_score, and the analyst's verdict (analyst_confirmed). The heuristic
proposes; the analyst disposes - analyst_confirmed is the only column the Timing Screen's
"In-market notice" signal trusts, so a same-PSC coincidence never fires that flag.

This replaces the old award_number-keyed in-market signal (which never fired: open notices
carry a solicitation number, not the eventual award number). Rendered faithfully off the
analyst table (like the Customer Map): identifiers + match facts black, the score/deadline
blue source values, analyst_confirmed / notes blue editable judgment.

Promoted accessor: notice_links_cols(header) -> "'Notice Links'!$X$first:$X$last".
"""
from __future__ import annotations

import csv

from workbook_army.sheets import _flat
from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_NOTICE_LINKS
from workbook_army.sheets._widths import contract_width
from workbook_army.sheets._analyst import ANALYST_DIR
from workbook_army.sheets._validate import DV_DATE, dv_list, CONFIRM

# The analyst tables live in workbook/analyst/, not workbook/extracted/. Temporarily point
# the flat builder's loader (bound in _flat's namespace) at the analyst copy for this sheet.
_orig = _flat.load_table


def _load_analyst_csv(name):
    with open(ANALYST_DIR / f"{name}.csv", newline="") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


_flat.load_table = lambda name: (_load_analyst_csv(name) if name == "notice_family_links"
                                 else _orig(name))
try:
    NOTICE_LINKS, notice_links_cols = make_flat_sheet(
        tab=TAB_NOTICE_LINKS, group="data",
        csv_name="notice_family_links", table_name="NoticeLinks",
        banner="§1 - Notice-family review",
        intro="One row per open notice x candidate family. Confirm a real recompete link to "
              "fire the Timing Screen's in-market signal; a same-PSC match alone does not.",
        width_fn=contract_width,
        float_cols=["evidence_score"], date_cols=["response_deadline"],
        input_cols=["evidence_score", "response_deadline", "analyst_confirmed", "notes"],
        validations=[("analyst_confirmed", dv_list(*CONFIRM)),
                     ("response_deadline", DV_DATE)],
    )
finally:
    _flat.load_table = _orig
