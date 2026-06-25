"""model_piid_worktype - the "Supplier Lanes" tab.

One filterable native table: supplier subaward record counts by (PIID, work type)
lane x subaward FY, per program, with a leading Program column - plus lane $M
(full history), lane timing (first/last award), vendor repetition (unique vendor
count, repeat-award share, shared-vendor pct and its fleet variant), and three
live lane flags mirroring the Indicators criteria (Multi-source / Concentration /
New 2nd source). Fully DERIVED: the FY count grid is black SUMIFS over
Lane Detail, first/last award are green links to the Lane Detail row, and $M /
Vendors / Repeat % / Shared % / the 3 flags are live COUNTIFS / SUMIFS / MAXIFS
against the Lane Vendors and Lane Vendor FY leaves - everything keyed on the row's
own PIID + Work Type cells, using the LIVE Assumptions controls. The bottom Totals Row
is filter-aware SUBTOTAL. Zero-record PIIDs have no lanes and are omitted - the
Market Views PIID section carries the full scope.

Seven header cells carry native Excel hover notes (one-line definitions of the
metric / flag columns).

Promoted accessors - program-keyed SUMIFS over the leaves (full history):
  pw_records_total_cell(program) - full-history record count (Lane Detail).
  pw_dollar_total_cell(program)  - full-history lane $M (Lane Vendors).
  pw_multi_count(program)        - lanes with >= the Assumptions vendor minimum.
  pw_single_count(program)       - lanes with a single vendor (Vendors = 1).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_BOLD, S_DATE_LINK, S_DEFAULT, S_INT, S_NUM, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry, ExcelTable
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, N_VALS, PROGRAMS, VAL_LABELS, load, program_label, row_sum,
)
from workbook_award_analysis.sheets.data_lane_vendors import vl_cols
from workbook_award_analysis.sheets.data_lane_detail import ld_cols, ld_date_refs
from workbook_award_analysis.sheets.data_lane_vendor_fy import lvf_cols
from workbook_award_analysis.sheets.summary_inputs import (
    input_multisource_cell, input_conc_threshold_cell,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_DATE, W_DOLLAR, W_COUNT, W_PCT, W_FY_N,
    W_STATUS, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_SUPPLIER_LANES
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "model"
_TAB = TAB_SUPPLIER_LANES
_META = ["Program", "PIID", "Work Type", "First Award", "Last Award",
         "$M (hist)", "Vendors", "Repeat %", "Shared %", "Shared % fleet",
         "Multi-source", "Concentration", "New 2nd source"]
_HEADERS = _META + VAL_LABELS
_CENTER_HDRS = set(VAL_LABELS)                          # center the FY grid
_NCOLS = len(_HEADERS)                                  # 13 + 16 = 29
_VCOL = [col_letter(1 + len(_META) + j) for j in range(N_VALS)]   # O..AD
_DOL_COL = col_letter(6)                                # G ($M)
_VEND_COL = col_letter(7)                               # H (Vendors)
# the 3 live lane flags appended after the metrics; the FY grid follows at _VCOL.
# Each is labelled for what it actually computes off the Lane Vendor FY leaf
# (mirroring the matching Indicators screen's criteria).
_MULTI_COL = col_letter(11)                             # L (recent multi-source)
_CONC_COL = col_letter(12)                              # M (top-1 >= cutoff)
_NEW2ND_COL = col_letter(13)                            # N (prior single -> recent multi)
_DATE_HDRS = {"First Award", "Last Award"}
# header-cell hover notes: {column letter -> one-line definition}.
_NOTE_COLS = {
    _VEND_COL:      "Unique suppliers in the lane.",
    col_letter(8):  "Share of records from repeat suppliers.",
    col_letter(9):  "Share of suppliers also on another PIID in the program.",
    col_letter(10): "Share of suppliers also on another PIID in the fleet.",
    _MULTI_COL:     "Recent multi-source lane (active vendors ≥ Assumptions min).",
    _CONC_COL:      "Top supplier share ≥ the Assumptions cutoff.",
    _NEW2ND_COL:    "Prior single-source lane, now recent multi-source.",
}


def _make_piid_worktype():
    i, rows = load("wb_piid_worktype")
    V = vl_cols()
    L = ld_cols()
    LV = lvf_cols()
    # Per-lane "incumbent still active" signal (wb_lane_signals) keyed on the raw
    # (PIID, work_type) - not derivable from the lvf leaf, so it gates the live
    # New 2nd source flag below (harmonizing it with the Source diversification
    # screen's count). Lanes with no signal row read as not-active (blank flag).
    j, sig_rows = load("wb_lane_signals")
    sig_incumbent = {(s[j["piid"]], s[j["work_type"]]): s[j["incumbent_still_active"]]
                     for s in sig_rows}

    def n_cell(rng: str):
        return lambda r: f"=SUMIFS({rng},{L['piid']},C{r},{L['wt']},D{r})"

    def _lane(r: int) -> str:
        """COUNTIFS/SUMIFS criteria pairs keyed on this row's own lane."""
        return f"{V['piid']},C{r},{V['wt']},D{r}"

    def vendors_f(r: int) -> str:
        return f"=COUNTIFS({_lane(r)})"

    def repeat_f(r: int) -> str:
        return (f'=SUMIFS({V["rec"]},{_lane(r)},{V["rec"]},">1")'
                f"/SUMIFS({V['rec']},{_lane(r)})")

    def shared_f(r: int) -> str:
        return (f'=COUNTIFS({_lane(r)},{V["np"]},">1")'
                f"/COUNTIFS({_lane(r)})")

    def shared_fam_f(r: int) -> str:
        return (f'=COUNTIFS({_lane(r)},{V["npf"]},">1")'
                f"/COUNTIFS({_lane(r)})")

    def dollars_f(r: int) -> str:
        return f"=SUMIFS({V['dol']},{_lane(r)})"

    # --- the 3 live indicator flags (mirror each Indicators screen's headline
    # condition over the Lane Vendor FY leaf, keyed on this row's PIID + Work Type,
    # using the LIVE Assumptions controls) ---
    def _lvf_crit(r: int) -> str:
        return f'{LV["piid"]},C{r},{LV["wt"]},D{r}'

    def multisource_flag(r: int) -> str:
        return (f'=IF(COUNTIFS({_lvf_crit(r)},{LV["rec_recent"]},">0")'
                f'>={input_multisource_cell()},"Y","N")')

    def concentration_flag(r: int) -> str:
        # blank (not "N") when there is no recent $ - concentration is undefined.
        rc = f'SUMIFS({LV["dol_recent"]},{_lvf_crit(r)})'
        return (f'=IF({rc}=0,"",IF(_xlfn.MAXIFS({LV["dol_recent"]},'
                f'{_lvf_crit(r)})/{rc}>={input_conc_threshold_cell()},"Y","N"))')

    def sourcediv_flag(incumbent_active: bool):
        """New 2nd source = a prior single-source lane (live prior active = 1) now
        recently multi-source (live recent active >= 2) AND whose incumbent is
        still active (a split, not a swap). The incumbent fact is a wb_lane_signals
        value, not derivable from the lvf leaf, so it gates the live formula as a
        static per-row boolean - lanes with no signal row read as not-active and
        stay blank. Harmonized with Source diversification's sc_emerging_count
        (prior=1, recent>=2, incumbent yes)."""
        if not incumbent_active:
            return ""                          # no incumbent -> blank, not "N"
        return lambda r: (
            f'=IF(AND(COUNTIFS({_lvf_crit(r)},{LV["rec_prior"]},">0")=1,'
            f'COUNTIFS({_lvf_crit(r)},{LV["rec_recent"]},">0")>=2),"Y","N")')

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Supplier lanes (PIID x work type)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS,
                  styles=header_styles(_HEADERS, _DATE_HDRS, center_headers=_CENTER_HDRS))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        for idx, row in enumerate(rows):
            if row[i["program"]] != prog:
                continue
            fa_ref, la_ref = ld_date_refs(idx)
            incumbent_active = (
                sig_incumbent.get((row[i["piid"]], row[i["work_type"]])) == "yes")
            last = c.write(
                [pname, row[i["piid"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 f"={fa_ref}", f"={la_ref}",
                 dollars_f, vendors_f, repeat_f, shared_f, shared_fam_f,
                 multisource_flag, concentration_flag,
                 sourcediv_flag(incumbent_active)]
                + [n_cell(rng) for rng in L["nfy"]]
                + [row_sum(_VCOL[0], _VCOL[-2])],
                styles=[S_DEFAULT] * 3 + [S_DATE_LINK] * 2
                       + [S_NUM, S_INT] + [S_PCT] * 3 + [S_CENTER] * 3
                       + [S_INT] * N_VALS,
                outline_level=1)
    table_ref = f"B{hdr}:{_VCOL[-1]}{last}"
    c.total(
        ["Total", None, None, None, None,
         f"=SUBTOTAL(109,{_DOL_COL}{f}:{_DOL_COL}{last})",
         f"=SUBTOTAL(109,{_VEND_COL}{f}:{_VEND_COL}{last})",
         None, None, None, None, None, None]
        + [f"=SUBTOTAL(109,{col}{f}:{col}{last})" for col in _VCOL],
        styles=[S_BOLD] + [S_DEFAULT] * 4 + [S_NUM, S_INT] + [S_DEFAULT] * 6
               + [S_INT] * N_VALS, n_cols=_NCOLS)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows,
                       cols=[W_PROGRAM, W_PIID, W_WORKTYPE, W_DATE, W_DATE,
                             W_DOLLAR, W_COUNT, W_PCT, W_PCT, W_PCT,
                             W_STATUS, W_STATUS, W_STATUS]
                            + [W_FY_N] * N_VALS,
                       tab_color=group_color(_GROUP), with_gutter=True)
        notes = [ExcelNote(ref=f"{col}{hdr}", text=text, author="Model")
                 for col, text in _NOTE_COLS.items()]
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="PIIDxWorkType", ref=table_ref, headers=_HEADERS),
        ], notes=notes)

    def pw_records_total_cell(program: str) -> str:
        return f'SUMIFS({L["ntot"]},{L["prog"]},"{program}")'

    def pw_dollar_total_cell(program: str) -> str:
        return f'SUMIFS({V["dol"]},{V["prog"]},"{program}")'

    def pw_cols() -> dict:
        # table body only (f..last), Program (B) + the live Vendors count (H)
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${last}"
        return {"prog": rng(col_letter(1)), "vendors": rng(_VEND_COL)}

    def pw_multi_count(program: str) -> str:
        # Multi-source = unique vendors (H) >= the LIVE Assumptions vendor minimum.
        P = pw_cols()
        return (f'COUNTIFS({P["prog"]},"{program_label(program)}",'
                f'{P["vendors"]},">="&{input_multisource_cell()})')

    def pw_single_count(program: str) -> str:
        # Single-source is a fixed definition (exactly one vendor), not a knob.
        P = pw_cols()
        return f'COUNTIFS({P["prog"]},"{program_label(program)}",{P["vendors"]},"=1")'

    return (SheetEntry(_TAB, _GROUP, render), pw_records_total_cell,
            pw_dollar_total_cell, pw_multi_count, pw_single_count)


(PIID_WORKTYPE, pw_records_total_cell, pw_dollar_total_cell,
 pw_multi_count, pw_single_count) = _make_piid_worktype()
