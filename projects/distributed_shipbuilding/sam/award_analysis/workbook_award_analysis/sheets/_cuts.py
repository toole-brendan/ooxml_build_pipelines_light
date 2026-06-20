"""_cuts - shared access to the wb_*.csv data-cut extracts.

Local non-sheet helper (like _layout / _taxonomy / _registry): the data-cut
sheets all read the wide FY-columned CSVs that
projects/distributed_shipbuilding/sam/award_classification/corpus/scripts/extract_workbook_cuts.py regenerates
into this pipeline's extracted/ dir. This module centralizes the FY-column
vocabulary and display-name maps so the FY span lives in exactly one place on
the workbook side.
"""
from __future__ import annotations

from datetime import date

from workbook_award_analysis.lib import load_extracted_csv
from workbook_award_analysis.sheets._taxonomy import BUCKETS, UNBUCKETED

_EPOCH = date(1899, 12, 30)         # Excel date serial day 0


def date_serial(s):
    """ISO date text -> Excel date serial (None for blank). Date cells are
    written as real serials (S_DATE_INPUT / S_DATE_LINK) so MINIFS/MAXIFS
    can aggregate them."""
    if not s:
        return None
    y, m, d = (int(p) for p in str(s)[:10].split("-"))
    return (date(y, m, d) - _EPOCH).days

FY_KEYS = ["le_fy12"] + [f"fy{y}" for y in range(2013, 2027)]
VAL_KEYS = FY_KEYS + ["total"]
VAL_LABELS = ["≤FY12"] + [f"FY{y % 100}" for y in range(2013, 2027)] + ["Total"]
FY_LABELS = VAL_LABELS[:-1]                 # the 15 FY labels (no "Total")
N_VALS = len(VAL_KEYS)                      # 15 FY columns + Total
N_FY_KEYS = [f"n_{k}" for k in FY_KEYS]     # record-count columns (n_-prefixed)

# Jump-ball windows partition FY_KEYS into "prior" and "recent". Recent runs
# FY22 -> present (incl. the partial latest FY) so the newest second sources are
# caught - the jump-ball lens is about emerging entrants, not the scorecard's
# FY22-25 concentration snapshot (FY26 is partial; flagged on the tabs).
RECENT_FY_KEYS = [f"fy{y}" for y in range(2022, 2027)]            # fy2022..fy2026
PRIOR_FY_KEYS = ["le_fy12"] + [f"fy{y}" for y in range(2013, 2022)]
N_PRIOR = len(PRIOR_FY_KEYS)                # 10 prior FY columns; 5 recent

PROGRAMS = [("virginia", "Virginia"), ("columbia", "Columbia"),
            ("ddg", "DDG-51")]
_PROGRAM_LABEL = dict(PROGRAMS)


def program_label(key: str) -> str:
    """Display name for a program key. The leaf tables store the raw key
    (virginia / columbia / ddg) but the MODEL tabs show the display name
    (Virginia / Columbia / DDG-51) in their Program column, so any COUNTIFS
    that filters a model-tab Program column must match on the label, not the
    key (otherwise it counts nothing)."""
    return _PROGRAM_LABEL[key]

BUCKET_NAME = {k: name for k, name, _ in BUCKETS}
BUCKET_NAME[UNBUCKETED] = "Unbucketed / ambiguous"

ROLE_NAME = {
    "supplier": "Supplier",
    "prime": "Prime (shipbuilder)",
    "co_prime": "Co-prime",
    "gfe_sib": "GFE / SIB pass-through",
    "mission_systems": "Mission systems",
    "foreign_fms": "Foreign / FMS",
    "service": "Services",
    "holding": "Holding company",
}


def load(name: str):
    """(column-index map, rows) for extracted/<name>.csv."""
    headers, rows = load_extracted_csv(name)
    return {h: n for n, h in enumerate(headers)}, rows


def fy_vals(i: dict, row: list) -> list:
    """The 15 FY values from a wide row (None -> 0). The extracted `total`
    column is deliberately NOT returned: per-row Totals are written as live
    =SUM formulas (house rule: blue hardcoded inputs, black derived formulas;
    the CSV total stays for script-side reconciliation only)."""
    return [row[i[k]] if row[i[k]] is not None else 0 for k in FY_KEYS]


def n_fy_vals(i: dict, row: list) -> list:
    """The 15 FY record counts from a wide row's n_-prefixed columns
    (None -> 0); same live-Total rule as fy_vals (n_total stays in the CSV
    for script-side reconciliation only)."""
    return [row[i[k]] if row[i[k]] is not None else 0 for k in N_FY_KEYS]


def row_sum(c0: str, c1: str):
    """A live per-row Total formula (=SUM(c0{r}:c1{r})). Pass the callable in
    a RowCursor values list; the cursor resolves it against the row it writes."""
    return lambda r: f"=SUM({c0}{r}:{c1}{r})"
