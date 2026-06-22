"""duplicate_audit - the "Duplicate-Report Audit" tab (reviewer finding #2).

USAspending warns that the same first-tier subcontract action is sometimes reported more
than once (distinct Subaward Report IDs, identical on every other field), inflating totals;
FAR 52.204-10 says continued reporting of the same subcontract is not required unless a
reported element changes. The base model already dedupes on Subaward Report ID; this sheet
surfaces the residual SEMANTIC duplicates - rows identical on ALL non-report-ID fields.

These are duplicate CANDIDATES, not confirmed duplicates: only the prime can say whether two
reports are distinct actions, so nothing is removed from the model. The headline stays the
GROSS reported total; this sheet shows the candidate count/$ and the illustrative NET-of-
candidates total per program. The per-row adjudication log is extracted/duplicate_candidates.csv.

Values are computed at build time by scripts/build_program_transactions.py
(extracted/duplicate_audit.csv); nominal dollars.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_DUP_AUDIT
from workbook_award_classification_refactor.sheets._widths import W_NAME, W_DOLLAR, W_FY

# Program | Gross Rows | Gross Nominal $M | Candidate Rows | Candidate Nominal $M
#         | Net Rows | Net Nominal $M | Candidate % of Gross
_WIDTHS = [W_NAME, W_FY, W_DOLLAR, W_FY, W_DOLLAR, W_FY, W_DOLLAR, W_FY]

_INT_COLS = ["Gross Rows", "Duplicate-Candidate Rows", "Net Rows"]
_FLOAT_COLS = ["Gross Nominal $M", "Duplicate-Candidate Nominal $M", "Net Nominal $M"]

DUPLICATE_AUDIT, duplicate_audit_cols = make_flat_sheet(
    tab=TAB_DUP_AUDIT, group="validation",
    csv_name="duplicate_audit", table_name="DuplicateReportAudit",
    banner="§1 - Potential duplicate reports",
    intro="Potential duplicate reports share all fields except report ID. Totals remain gross; "
          "net values are sensitivity only.",
    widths=_WIDTHS,
    int_cols=_INT_COLS, float_cols=_FLOAT_COLS,
)
