"""scope_assumptions - scope, money discipline + method (the read-me-first guide).

A compact, structured statement of what this workbook is, what is in/out of scope, the money
rules it must obey, how the sizes are built, and where each rule is enforced - so a reader
trusts the numbers and does not misuse them. No data; a short Topic / Rule / Where table per
section rather than single-cell essays (narrow columns, no wrap).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import S_DEFAULT, S_TITLE_SECTION, S_TITLE_SHEET
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_SCOPE

_GROUP = "guide"
_TAB = TAB_SCOPE
_NCOLS = 3
_COLS = [22, 46, 24]                                # Topic | Rule | Where enforced
_HEAD = ["Topic", "Rule", "Where enforced"]

# (section banner, header?, rows). A header of None makes the section narrative (col B only).
_SECTIONS = [
    ("§1 - Purpose", None, [
        ["Where-to-play market map for Saronic in Army autonomous surface vessels."],
        ["Chain: mission -> user -> requirement -> funding -> contract -> timing -> route."],
    ]),
    ("§2 - Scope", _HEAD, [
        ["In scope", "U.S. Army + USACE/ERDC watercraft", "Contract Families"],
        ["Relevance", "PSC 19xx, NAICS 33661x, vessel terms, primes", "Contract Families"],
        ["Out of scope", "Navy / USMC (dropped at discovery)", "-"],
        ["Segments", "Army ops vs USACE vs MRO vs RDT&E", "Timing Screen"],
        ["Materiality", "Selected measure >= $1.0M", "Timing Screen"],
    ]),
    ("§3 - Money discipline", _HEAD, [
        ["Amount types", "Never sum different money types", "Budget Facts"],
        ["Request", "Use request_total, not base+oco+total", "Budget Market"],
        ["Budget vs contracts", "Separate lenses - never added", "QA"],
        ["Obligations", "Evidence of spend, not TAM/SAM", "QA"],
        ["Selected measure", "One per family (action, else award)", "Contract Families"],
    ]),
    ("§4 - Market sizing", _HEAD, [
        ["Gross funded", "FY27-31 spine (request + outyears, PB2027)", "Budget Market"],
        ["Addressable", "Gross x addressable %", "Market Size"],
        ["Serviceable (SAM)", "Addressable x Saronic fit %", "Market Size"],
        ["Weighted (SOM)", "Serviceable x timing x access x win", "Market Size"],
        ["Knobs", "Seed until independently sourced", "Market Assumptions"],
    ]),
    ("§5 - Lineage & pipeline", _HEAD, [
        ["Lineage", "Evidence-scored; Superseded only if confirmed", "Timing Screen"],
        ["Pipeline", "One row per solicitation lifecycle", "Pipeline Events"],
        ["Notice links", "Confirmed link fires it; same-PSC doesn't", "Notice Links"],
        ["Decision dates", "PoP-end proxies; Notice-by = 90-day est.", "Timing Screen"],
    ]),
    ("§6 - Sources & freshness", _HEAD, [
        ["Freshness", "Per-source data-through dates + lag", "Data Freshness"],
        ["SAM CA", "Revealed-only; DoD < 90 days excluded", "Data Freshness"],
        ["Citations", "Cited budget books + pull dates", "Source Log"],
        ["Analyst layer", "Durable record; survives rebuild", "Inputs tabs"],
    ]),
]


def _make_scope():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Scope, money discipline, and how the market sizes are built."],
            styles=[S_ITALIC])
    c.blank(2)
    for title, header, rows in _SECTIONS:
        c.banner(title, n_cols=_NCOLS, style=S_TITLE_SECTION)
        c.blank()
        if header:
            c.write(header, styles=header_styles(header))
        for row in rows:
            c.write(row, styles=[S_DEFAULT] * len(row))
        c.blank(2)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SCOPE_ASSUMPTIONS = _make_scope()
