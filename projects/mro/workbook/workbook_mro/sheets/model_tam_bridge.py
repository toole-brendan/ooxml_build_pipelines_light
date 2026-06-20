"""TAM Bridge

INTENT
    Reconciliation between the top-down budget-anchored MRO funding pot (~$17.0B: OP-5
    availability categories + MSC + SCN + USCG + OPN; WPN excluded as a memo) and the
    bottom-up Reconciled FPDS-visible MRO TAM (~$9.0B: services 65-PSC + embedded PSC
    1905). Per-component top-down cells pull the producer accessors; per-component
    bottom-up cells are live FPDS SUMIFS; the bottom-up TOTAL is reconciled_mro_tam_cell()
    so the bridge ties to the deck (16,996 / 8,971 / +8,025). The Gap column is intra-sheet
    =D{r}-E{r}. A scaled pull (accessor/1000) is a derived value (black S_NUM); only a bare
    =accessor() link is green.

LAYOUT
    row 2 : title
    B..F  : #, Bridge Component, Top-Down ($M), Bottom-Up ($M), Gap ($M, TD-BU)
    §1 top-down vs bottom-up bridge (components, grand total, private-addressable drop-through)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_NUM_INPUT, S_LINK_NUM,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import sumifs_award, sumifs_psc1905
from workbook_mro.sheets.model_op5_navy_topdown import (
    op5_private_cell, op5_public_nsy_cell,
)
from workbook_mro.sheets.model_msc_scn_uscg_topdown import (
    msc_mr_fy25_transfer_cell, scn_cvn_rcoh_li2086_cell, opn_li1000_cell,
    uscg_isvs_floor_cell,
)
from workbook_mro.sheets.model_services import cg_tam_svc_cell
from workbook_mro.sheets.model_reconciliation import reconciled_mro_tam_cell
from workbook_mro.sheets.inputs_assumptions import wpn_estimate_cell

_GROUP = "model"
_TAB = "TAM Bridge"
_NCOLS = 5                      # B..F
_COLS = [5, 40, 14, 14, 14]
_HEADERS = ["#", "Bridge Component", "Top-Down ($M)", "Bottom-Up ($M)", "Gap ($M)"]
_HSTYLE = [S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER,
           S_HEADER_CENTER]

# Bottom-up FPDS RMC universe for Row 1 (the 7 canonical RMC / FDNF buyers) - sum of
# per-office SUMIFS (one term per contracting office).
_RMC_OFFICES = ["SWRMC", "MARMC", "SERMC", "NW RMC / Puget Sound", "Pearl Harbor RMC",
                "SRF-JRMC Yokosuka", "FDRMC Naples"]
_RMC_SUMIFS = "+".join(
    f'{sumifs_award("FY2025 Obligation", ("Is MRO", "Y"), ("Canonical Office", off))}/1000000'
    for off in _RMC_OFFICES)


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _row(key, num, comp, td, td_style, bu, bu_style, *, gap=True):
        gap_val = (lambda r: f"=D{r}-E{r}") if gap else None
        # Per-row Gap is intra-sheet arithmetic, not a total - plain S_NUM (the §2
        # grand-total row below is the only one that gets the c.total() divider).
        r = c.write([num, comp, td, bu, gap_val],
                    styles=[S_DEFAULT, S_DEFAULT, td_style, bu_style, S_NUM],
                    outline_level=1)
        P[key] = r
        return r

    # §1 Top-down vs bottom-up bridge
    c.banner("§1 - Top-down vs bottom-up bridge", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(_HEADERS, styles=_HSTYLE, outline_level=1)

    _row("navpriv", 1, "Navy private-yard ship maintenance (1B4B non-NSY)",
         f"={op5_private_cell()}/1000", S_NUM, f"={_RMC_SUMIFS}", S_NUM)
    _row("pubnsy", 2, "Navy Public NSY (NNSY/PNSY/PSNSY/PHNSY)",
         f"={op5_public_nsy_cell()}/1000", S_NUM, 0, S_NUM_INPUT)
    _row("msc", 3, "MSC M&R (FY25 1B1B transfer-out; FY26 -> 1B4B)",
         f"={msc_mr_fy25_transfer_cell()}/1000", S_NUM,
         f'={sumifs_award("FY2025 Obligation", ("Is MRO", "Y"), ("Canonical Office", "MSC HQ"))}/1000000',
         S_NUM)
    _row("fdnf", 4, "FDNF private MSRA (Yokosuka / Rota / Bahrain / Sigonella)",
         None, S_DEFAULT, None, S_DEFAULT, gap=False)
    _row("scn", 5, "SCN CVN RCOH (LI 2086) + embedded complex OH",
         f"={scn_cvn_rcoh_li2086_cell(2025)}/1000", S_NUM,
         f'={sumifs_psc1905("FY2025 Obligation", ("Bucket", "MRO*"))}/1000000', S_NUM)
    _row("opn", 6, "OPN LI 1000 ship maintenance (private contracted)",
         f"={opn_li1000_cell(2025)}/1000", S_NUM, 0, S_NUM_INPUT)
    _row("uscg", 7, "USCG cutter MRO",
         f"={uscg_isvs_floor_cell()}/1000", S_NUM, f"={cg_tam_svc_cell()}", S_LINK_NUM)

    # Grand total + non-public-NSY drop-through (the bridge's concluding lines, kept
    # inside §1 rather than as two single-row sections). WPN is a combat-systems plug,
    # not an MRO bridge component, so it is a memo line below the total (excluded), and
    # the bottom-up total is the Reconciled FPDS-visible MRO TAM (services + embedded).
    _td_rows = [P[k] for k in ("navpriv", "pubnsy", "msc", "scn", "opn", "uscg")]
    P["total"] = c.total(
        ["T", "TOTAL TOP-DOWN",
         "=" + "+".join(f"D{r}" for r in _td_rows),
         f"={reconciled_mro_tam_cell()}",
         lambda r: f"=D{r}-E{r}"],
        styles=[S_BOLD, S_BOLD, S_NUM, S_NUM, S_NUM],
        n_cols=_NCOLS, outline_level=1)
    c.write(
        [None, "Top-down minus Public NSY (non-public-NSY funding cross-check)",
         f"=D{P['total']}-{op5_public_nsy_cell()}/1000", None, None],
        styles=[S_DEFAULT, S_BOLD, S_NUM, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(
        [None, "memo: WPN combat-systems sustainment (excluded from total)",
         f"={wpn_estimate_cell()}", None, None],
        styles=[S_DEFAULT, S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    # accessors (load-bearing §2 grand-total cells; consumed by Figure Register)
    def topdown_total_cell() -> str: return f"'{_TAB}'!D{P['total']}"
    def bottomup_total_cell() -> str: return f"'{_TAB}'!E{P['total']}"
    def bridge_gap_cell() -> str: return f"'{_TAB}'!F{P['total']}"

    accessors = dict(topdown_total_cell=topdown_total_cell,
                     bottomup_total_cell=bottomup_total_cell,
                     bridge_gap_cell=bridge_gap_cell)
    return SheetEntry(_TAB, _GROUP, render), accessors


TAM_BRIDGE, _ACC = _make()

topdown_total_cell = _ACC["topdown_total_cell"]
bottomup_total_cell = _ACC["bottomup_total_cell"]
bridge_gap_cell = _ACC["bridge_gap_cell"]
