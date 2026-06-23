"""market_bridge - reported subawards bridged to an illustrative cumulative co-build scenario.

The program-vendor / Domain Concentration sheets model the OBSERVED reported first-tier
FFATA/FSRS subawards. This sheet is an illustrative cumulative co-build scenario, not a
point-in-time market size: it adds the FFATA-invisible HII-Newport News co-build workshare
(issuer-disclosed; the disclosed ledger + sources are folded into §3) to the observed base and
subtracts the HII-NNS footprint already counted in observed so nothing is double-counted.

Discipline:
  - the bridge math is in ONE unit, nominal $M (observed FY2026$ is shown only as a memo);
  - the co-build Low is the strongest single issuer-disclosed figure (an input cell); Base/High
    are FORMULAS = Low x an explicit, editable scale multiple (blue), never hardcoded magnitudes;
  - the "less reported HII-NNS overlap" lines are LIVE subtractions over both submarine
    transaction sheets keyed on the HII-NNS UEIs, so a future Columbia report cannot be double-counted;
  - the result is labelled a cumulative co-build scenario blending vintages, order-of-magnitude.

`summary` group. Live observed = the program-vendor / transaction sheets; the scenario columns
sum the bridge.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_NUM_INPUT, S_LABEL_INDENT_1,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._tabs import TAB_MARKET_BRIDGE
from workbook_award_classification_refactor.sheets.ddg_program_vendors import ddg_pv_cols
from workbook_award_classification_refactor.sheets.virginia_program_vendors import virginia_pv_cols
from workbook_award_classification_refactor.sheets.columbia_program_vendors import columbia_pv_cols
from workbook_award_classification_refactor.sheets.ddg_subaward_transactions import ddg_tx_cols
from workbook_award_classification_refactor.sheets.virginia_subaward_transactions import virginia_tx_cols
from workbook_award_classification_refactor.sheets.columbia_subaward_transactions import columbia_tx_cols

_GROUP = "summary"
_HEADERS = ["Component", "Basis", "Low $M", "Base $M", "High $M", "Base x", "High x"]
_NCOLS = len(_HEADERS)
_COLS = [36, 34, 12, 12, 12, 9, 9]

# HII-Newport News operating entities used for the live overlap check on each submarine leaf.
# Columbia is currently zero, but it remains formula-driven so a refresh cannot silently double-count.
_HII_NNS_UEIS = ["WMXDDH6HJNA5", "CR39JL3216G7"]   # Huntington Ingalls Inc; Newport News Nuclear

# Observed totals (live). Nominal = sum of the transaction "Subaward Amount $" (raw $) / 1e6;
# FY2026$ memo = sum of the program-vendor "Subaward $M" (already constant FY2026 $M).
_DDG_OBS = f"=SUM({ddg_tx_cols('Subaward Amount $')})/1000000"
_VA_OBS = f"=SUM({virginia_tx_cols('Subaward Amount $')})/1000000"
_COL_OBS = f"=SUM({columbia_tx_cols('Subaward Amount $')})/1000000"
_FY26_MEMO = "=" + "+".join(f"SUM({c('Subaward $M')})"
                            for c in (ddg_pv_cols, virginia_pv_cols, columbia_pv_cols))

def _overlap_formula(txc) -> str:
    amt = txc("Subaward Amount $")
    uei = txc("Subawardee UEI")
    return ("=-(" + "+".join(f'SUMIFS({amt},{uei},"{u}")' for u in _HII_NNS_UEIS)
            + ")/1000000")


_VA_OVERLAP = _overlap_formula(virginia_tx_cols)
_COL_OVERLAP = _overlap_formula(columbia_tx_cols)

INTRO = ("Illustrative bridge from reported subawards to cumulative submarine co-build workshare.")
CAVEAT = ("Not a point-in-time market size. All bridge figures are nominal $M (observed "
          "constant-FY2026$ is a memo). Co-build Low is the strongest single issuer-disclosed "
          "figure (blue input); Base and High are Low times an editable analyst scenario multiple "
          "(blue, not source-derived). Vintages differ, so the scenario is order-of-magnitude and the co-build mass is not "
          "split across capability domains.")

# §3 is the single home of the co-build derivation: the issuer-disclosed ledger that sources the
# §2 Low anchors, the live overlap subtraction, the scenario-multiple caveat, and the sources.
DERIVATION = [
    ("Virginia co-build Low ($10.2B)",
     "HII-NNS Block V cumulative contract value disclosed 2023-05-24 - the strongest single public "
     "Virginia figure (supersedes the $9.8B Mar-2021 option-exercise value and the $1.04B Apr-2019 "
     "AP mod). An issuer disclosure (HII newsroom / SEC), not an FFATA transaction."),
    ("Columbia co-build Low (~$3.4B)",
     "Lineage-summed HII-NNS disclosures: ~$2.2B design + modules for the first two boats (Nov 2020), "
     "$567.6M Build-II LLTM + advance construction (Apr 2023), $197M long-lead (Nov 2018), under the "
     "$468M IPPD ceiling (Dec 2017). Cumulative values are basis-typed and not additive - summed by "
     "lineage, not down a column."),
    ("Less reported HII-NNS overlap",
     "HII-NNS subawards already in observed (UEIs WMXDDH6HJNA5 / CR39JL3216G7) are "
     "subtracted live from both Virginia and Columbia; Columbia currently evaluates to $0."),
    ("Scenario multiples",
     "Base / High scale multiples are editable analyst assumptions, not issuer-disclosed values. "
     "They require an explicit rationale before the bridge is used as a market-sizing output."),
    ("Scope",
     "Co-build figures are not FFATA/FSRS transactions and are excluded from every other "
     "sheet. Edit the blue Low and scale cells to re-scope; the scenario updates live."),
    ("Sources",
     "CRS RL32418 (Virginia) / R41129 (Columbia); DoD/DoW contract announcements (N00024-17-C-2100 "
     "Block V; N00024-17-C-2117 Columbia design); HII issuer disclosures (hii.com newsroom) + SEC "
     "10-K (EDGAR CIK 1501585); GD Electric Boat releases. Mechanism: FAR 52.204-10 first-tier FFATA "
     "reporting - HII characterises these as EB subcontract modifications, so the absence is a "
     "reporting / data-treatment gap, not a clean teaming carve-out."),
]


def _make_market_bridge():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.title(TAB_MARKET_BRIDGE, _NCOLS)
        c.caption(INTRO)
        c.write([CAVEAT], styles=[S_ITALIC])
        c.blank(2)

        c.section("§1 - Observed reported subawards (nominal)", _NCOLS)
        c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 5)
        obs_style = [S_DEFAULT, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT]
        r_ddg = c.write(["DDG-51 observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                         _DDG_OBS, _DDG_OBS, _DDG_OBS, "", ""], styles=obs_style)
        c.write(["Virginia observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                 _VA_OBS, _VA_OBS, _VA_OBS, "", ""], styles=obs_style)
        r_col = c.write(["Columbia observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                         _COL_OBS, _COL_OBS, _COL_OBS, "", ""], styles=obs_style)
        r_obs = c.total(["Observed subtotal (nominal)", "",
                         f"=SUM(D{r_ddg}:D{r_col})", f"=SUM(E{r_ddg}:E{r_col})",
                         f"=SUM(F{r_ddg}:F{r_col})", "", ""],
                        styles=[S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT],
                        n_cols=_NCOLS)
        c.write(["Observed subtotal, constant FY2026$ (memo, not added)",
                 "deflated; for comparison only", _FY26_MEMO, _FY26_MEMO, _FY26_MEMO, "", ""],
                styles=[S_LABEL_INDENT_1, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT])
        c.blank(2)

        c.section("§2 - Co-build adjustment", _NCOLS)
        gross_style = [S_DEFAULT, S_ITALIC, S_NUM_INPUT, S_NUM, S_NUM, S_NUM_INPUT, S_NUM_INPUT]
        live_style = [S_LABEL_INDENT_1, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT]
        r_va_gross = c.write(
            ["Virginia co-build workshare",
             "Low = disclosed $10.2B Block V value (2023); Base/High = analyst scale",
             10200, lambda r: f"=D{r}*G{r}", lambda r: f"=D{r}*H{r}", 1.47, 2.16],
            styles=gross_style)
        c.write(["Less Virginia reported HII-NNS overlap",
                 "HII-NNS subawards already in Virginia observed (live; two UEIs)",
                 _VA_OVERLAP, _VA_OVERLAP, _VA_OVERLAP, "", ""],
                styles=live_style)
        r_col_gross = c.write(["Columbia co-build workshare",
                 "Low = disclosed-scope anchor about $3.4B; Base/High = analyst scale",
                 3400, lambda r: f"=D{r}*G{r}", lambda r: f"=D{r}*H{r}", 1.47, 2.35],
                styles=gross_style)
        r_col_overlap = c.write(["Less Columbia reported HII-NNS overlap",
                 "HII-NNS subawards already in Columbia observed (live; currently $0)",
                 _COL_OVERLAP, _COL_OVERLAP, _COL_OVERLAP, "", ""],
                styles=live_style)
        c.total(["Estimated cumulative outsourced / co-build total (nominal)", "",
                 f"=D{r_obs}+SUM(D{r_va_gross}:D{r_col_overlap})",
                 f"=E{r_obs}+SUM(E{r_va_gross}:E{r_col_overlap})",
                 f"=F{r_obs}+SUM(F{r_va_gross}:F{r_col_overlap})", "", ""],
                styles=[S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT], n_cols=_NCOLS)
        c.blank(2)

        c.section("§3 - Derivation, disclosed ledger & sources", _NCOLS)
        c.write(["Component", "Basis"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
        for comp, basis in DERIVATION:
            c.write([comp, basis], styles=[S_BOLD, S_DEFAULT])

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_MARKET_BRIDGE, _GROUP, render)


MARKET_BRIDGE = _make_market_bridge()
