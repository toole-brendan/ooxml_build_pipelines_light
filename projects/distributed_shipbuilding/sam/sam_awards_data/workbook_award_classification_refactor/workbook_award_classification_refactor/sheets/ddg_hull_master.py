"""ddg_hull_master - one row per DDG-51 hull (the hull dimension).

The hull reference dimension: builder, prime PIID, contract block / MYP, Flight, and award FY for
each in-scope hull, with a confidence grade and the supporting public source folded into a hover
Note. It supplies the row spine + builder label for the hull roll-ups (DDG Hull Spend Summary,
DDG Hull x SWBS) the way the Supplier Master supplies the program-vendor sheets.

Lifecycle milestone dates (steel-cut / keel / launch / delivery / commissioning) and the derived
lifecycle-stage attribution are a deliberately deferred later phase; this dimension carries only
the procurement identity today. Built by hand (HII supplier PDFs, SAR / MSAR, USNI); NOT regenerated.
Award FY is approximate for the MYP hulls (the row Confidence grades the hull->builder identity, not
the exact procurement year).

Promoted accessor: hull_master_cols(header) -> "'DDG Hull Master'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_HULL_MASTER
from workbook_award_classification_refactor.sheets._widths import (
    W_SHORT_FLAG, W_SUPTYPE, W_PIID, W_STATUS, W_CLASS, W_FY,
)

# Hull | Builder | Prime PIID | Contract Block / MYP | Flight | Award FY | Confidence
# (Source URL is dropped into a hover Note on the Hull cell.)
_WIDTHS = [W_SHORT_FLAG, W_SUPTYPE, W_PIID, W_STATUS, W_CLASS, W_FY, W_CLASS]

DDG_HULL_MASTER, hull_master_cols = make_flat_sheet(
    tab=TAB_HULL_MASTER, group="inputs",
    csv_name="ddg_hull_master", table_name="DdgHullMaster",
    banner="§1 - DDG-51 hull master",
    intro="One row per hull: builder, prime contract, block / MYP, Flight, award FY (approximate).",
    widths=_WIDTHS,
    int_cols=["Award FY"],
    input_cols=["Hull"], input_fill=True,
    # the public source for each hull folds into a hover Note on the Hull cell.
    note_from={"Hull": "Source URL"},
    display_headers={"Contract Block / MYP": "Block / MYP"},
)
