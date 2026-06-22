"""market_bridge - reported subawards bridged to an illustrative cumulative co-build scenario.

The program-vendor / Domain Concentration sheets model the OBSERVED reported first-tier
FFATA/FSRS subawards. This sheet is an illustrative cumulative co-build scenario, not a
point-in-time market size: it adds the FFATA-invisible HII-Newport News co-build workshare
(issuer-disclosed; see HII Co-Build) to the observed base and subtracts the HII-NNS footprint
already counted in observed so nothing is double-counted.

Discipline:
  - the bridge math is in ONE unit, nominal $M (observed FY2026$ is shown only as a memo);
  - the co-build Low is the strongest single issuer-disclosed figure (an input cell); Base/High
    are FORMULAS = Low x an explicit, editable scale multiple (blue), never hardcoded magnitudes;
  - the "less reported HII-NNS overlap" line is a LIVE subtraction over the Virginia transaction
    sheet keyed on the HII-NNS UEIs, so it reconciles to the data and updates on refresh;
  - the result is labelled a cumulative co-build scenario blending vintages, order-of-magnitude.

`summary` group. Live observed = the program-vendor / transaction sheets; the scenario columns
sum the bridge.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION, S_NUM, S_NUM_INPUT, S_LABEL_INDENT_1,
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

# HII-Newport News operating entities visible in the Virginia subaward data (subawardee UEIs).
# The "less reported overlap" line sums these so the co-build add-on is net of what observed
# already counts. (Columbia retains no HII-NNS subaward after the scope exclusions -> $0.)
_HII_NNS_UEIS = ["WMXDDH6HJNA5", "CR39JL3216G7"]   # Huntington Ingalls Inc; Newport News Nuclear

# Observed totals (live). Nominal = sum of the transaction "Subaward Amount $" (raw $) / 1e6;
# FY2026$ memo = sum of the program-vendor "Subaward $M" (already constant FY2026 $M).
_DDG_OBS = f"=SUM({ddg_tx_cols('Subaward Amount $')})/1000000"
_VA_OBS = f"=SUM({virginia_tx_cols('Subaward Amount $')})/1000000"
_COL_OBS = f"=SUM({columbia_tx_cols('Subaward Amount $')})/1000000"
_FY26_MEMO = "=" + "+".join(f"SUM({c('Subaward $M')})"
                            for c in (ddg_pv_cols, virginia_pv_cols, columbia_pv_cols))

_VA_AMT = virginia_tx_cols("Subaward Amount $")
_VA_UEI = virginia_tx_cols("Subawardee UEI")
_VA_OVERLAP = ("=-(" + "+".join(f'SUMIFS({_VA_AMT},{_VA_UEI},"{u}")' for u in _HII_NNS_UEIS)
               + ")/1000000")

INTRO = ("Illustrative bridge from reported subawards to cumulative submarine co-build workshare.")
CAVEAT = ("Not a point-in-time market size. All bridge figures are nominal $M (observed "
          "constant-FY2026$ is a memo). Co-build Low is the strongest single issuer-disclosed "
          "figure (blue input); Base and High are Low times an editable scale multiple (blue). "
          "Vintages differ, so the scenario is order-of-magnitude and the co-build mass is not "
          "split across capability domains.")

# §3 derivation, as a compact (component, basis) table instead of a prose block.
DERIVATION = [
    ("Virginia co-build Low",
     "$10,200M - HII-NNS Block V contract value as of 2023-05-24 (disclosed cumulative value)."),
    ("Virginia Base / High",
     "Low times scale (earlier blocks + CRS about 25% place-of-performance to about 50% "
     "co-builder workshare, RL32418); judgment, order-of-magnitude."),
    ("Columbia co-build Low",
     "about $3,400M - lineage-summed disclosed mods ($2.2B 2020 modules + $567.6M 2023 + "
     "$197M 2018 + $468M 2017 ceiling; cumulative values not also added)."),
    ("Columbia Base / High",
     "Low times scale (CRS about 22-23% workshare, R41129)."),
    ("Less reported HII-NNS overlap",
     "HII-NNS subawards already in observed (Virginia UEIs WMXDDH6HJNA5 / CR39JL3216G7), "
     "subtracted live. Columbia overlap = $0."),
    ("Scope",
     "Co-build figures are not FFATA/FSRS transactions and are excluded from every other "
     "sheet. Edit the blue Low and scale cells to re-scope; the scenario updates live."),
]


def _make_market_bridge():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(TAB_MARKET_BRIDGE, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.write([INTRO], styles=[S_ITALIC])
        c.write([CAVEAT], styles=[S_ITALIC])
        c.blank(2)

        c.banner("§1 - Observed reported subawards (nominal)", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 5)
        obs_style = [S_DEFAULT, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT]
        r_ddg = c.write(["DDG-51 observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                         _DDG_OBS, _DDG_OBS, _DDG_OBS, "", ""], styles=obs_style, outline_level=1)
        c.write(["Virginia observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                 _VA_OBS, _VA_OBS, _VA_OBS, "", ""], styles=obs_style, outline_level=1)
        r_col = c.write(["Columbia observed subawards", "reported first-tier FFATA/FSRS, nominal $",
                         _COL_OBS, _COL_OBS, _COL_OBS, "", ""], styles=obs_style, outline_level=1)
        r_obs = c.total(["Observed subtotal (nominal)", "",
                         f"=SUM(D{r_ddg}:D{r_col})", f"=SUM(E{r_ddg}:E{r_col})",
                         f"=SUM(F{r_ddg}:F{r_col})", "", ""],
                        styles=[S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT],
                        n_cols=_NCOLS)
        c.write(["Observed subtotal, constant FY2026$ (memo, not added)",
                 "deflated; for comparison only", _FY26_MEMO, _FY26_MEMO, _FY26_MEMO, "", ""],
                styles=[S_LABEL_INDENT_1, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT],
                outline_level=1)
        c.blank(2)

        c.banner("§2 - Co-build adjustment", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        gross_style = [S_DEFAULT, S_ITALIC, S_NUM_INPUT, S_NUM, S_NUM, S_NUM_INPUT, S_NUM_INPUT]
        live_style = [S_LABEL_INDENT_1, S_ITALIC, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT]
        r_va_gross = c.write(
            ["Virginia co-build workshare",
             "Low = disclosed $10.2B Block V value (2023); Base/High = Low x scale",
             10200, lambda r: f"=D{r}*G{r}", lambda r: f"=D{r}*H{r}", 1.47, 2.16],
            styles=gross_style, outline_level=1)
        c.write(["Less reported HII-NNS overlap",
                 "HII-NNS subawards already in observed (live; UEIs WMXDDH6HJNA5/CR39JL3216G7)",
                 _VA_OVERLAP, _VA_OVERLAP, _VA_OVERLAP, "", ""],
                styles=live_style, outline_level=1)
        r_col_gross = c.write(["Columbia co-build workshare",
                 "Low = disclosed lineage-summed mods about $3.4B; Base/High = Low x scale",
                 3400, lambda r: f"=D{r}*G{r}", lambda r: f"=D{r}*H{r}", 1.47, 2.35],
                styles=gross_style, outline_level=1)
        c.total(["Estimated cumulative outsourced / co-build total (nominal)", "",
                 f"=D{r_obs}+SUM(D{r_va_gross}:D{r_col_gross})",
                 f"=E{r_obs}+SUM(E{r_va_gross}:E{r_col_gross})",
                 f"=F{r_obs}+SUM(F{r_va_gross}:F{r_col_gross})", "", ""],
                styles=[S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT], n_cols=_NCOLS)
        c.blank(2)

        c.banner("§3 - Derivation & basis", n_cols=_NCOLS, style=S_TITLE_SECTION,
                 mark_collapsible=True)
        c.write(["Component", "Basis"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
        for comp, basis in DERIVATION:
            c.write([comp, basis], styles=[S_BOLD, S_DEFAULT], outline_level=1)

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_MARKET_BRIDGE, _GROUP, render)


MARKET_BRIDGE = _make_market_bridge()
