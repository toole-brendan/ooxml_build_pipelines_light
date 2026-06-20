"""_widths - standardized column widths + header-alignment helper.

Local non-sheet helper (like _layout / _cuts). Centralizes the column-width
vocabulary so every sheet sizes a given column TYPE the same way instead of
hand-picking a number per sheet - the workbook reads as one ruled system. Widths
are Excel character units (the `cols=[...]` values passed to worksheet()); the
~1.5-char gutter is prepended by worksheet(with_gutter=True), so these map to
content columns starting at column B.

These raw data sheets carry long free-text columns (requirement descriptions,
account titles, office names). The workbook standard is no wrapped text, so a prose
column is sized wide enough to read the opening clause; the rest overflows into
neighbouring blank cells / is reached by widening or via the formula bar. Identifier
and numeric columns stay compact.

contract_width(header) maps a contract CSV column name to its width, so a raw data
sheet auto-sizes every column from its header without a hand-counted widths list
(make_flat_sheet(width_fn=contract_width)). header_styles() encodes the
header-alignment rule: every header left-aligned EXCEPT numeric columns named in
center_headers, which are centered.
"""
from __future__ import annotations

from workbook_core.styles import S_HEADER_LEFT, S_HEADER_CENTER

# ---------------------------------------------------------------------------
# Column widths by semantic type (Excel character units)
# ---------------------------------------------------------------------------
W_UEI        = 14    # vendor UEI
W_CODE       = 10    # short code (PSC, agency id)
W_NAICS      = 11    # NAICS code
W_DATE       = 14    # ISO date (real date serial)
W_FY         = 10    # federal fiscal year
W_PIID       = 22    # prime contract PIID
W_AWARDID    = 30    # USAspending generated award id (CONT_AWD_...)
W_VENDOR     = 34    # recipient / vendor / office name
W_AMOUNT     = 16    # raw dollar amount
W_COUNT      = 13    # record / offer count
W_CONF       = 15    # flag / TAS / set-aside
W_CATEGORY   = 28    # categorical description label
W_NAICS_DESC = 34    # NAICS / account-title description
W_TEXT       = 46    # general prose (requirement description, title)

# ---------------------------------------------------------------------------
# Contract-column -> width map (the faithful raw-pull columns)
# ---------------------------------------------------------------------------
_CONTRACT_W = {
    # identifiers
    "award_id": W_AWARDID, "piid": W_PIID, "parent_idv_piid": W_PIID,
    "prime_piid": W_PIID, "prime_referenced_idv_piid": W_PIID,
    "sub_award_number": 18, "sub_award_report_id": 16, "mod_number": 12,
    "solicitation_number": 20, "notice_id": 20, "award_number": W_PIID,
    # entities
    "recipient_uei": W_UEI, "sub_entity_uei": W_UEI, "sub_parent_uei": W_UEI,
    "recipient_name": W_VENDOR, "parent_recipient_name": W_VENDOR,
    "prime_recipient": W_VENDOR, "sub_entity_name": W_VENDOR,
    "sub_parent_name": W_VENDOR, "contracting_office": 30, "funding_office": 30,
    # money
    "obligation_amount": W_AMOUNT, "current_value": W_AMOUNT,
    "ceiling_value": W_AMOUNT, "total_outlay": W_AMOUNT,
    "total_subaward_amount": W_AMOUNT, "amount": W_AMOUNT,
    # counts
    "subaward_count": W_COUNT, "number_of_offers": W_COUNT, "fiscal_year": W_FY,
    # codes / keys
    "naics_code": W_NAICS, "prime_naics": W_NAICS, "psc_code": W_CODE,
    "prime_agency_id": W_CODE, "funding_tas": W_CONF, "set_aside": W_CONF,
    "matched_axes": W_CATEGORY,
    # categoricals
    "idv_type": 12, "single_or_multiple_award": 14, "award_type": 12,
    "category": 16, "extent_competed": 16, "fair_opportunity_limited": 16,
    "has_tas": 9, "actions_source": 14, "amount_type": 14, "dollars_basis": 14,
    "pricing_type": 18, "action_type": 22, "notice_type": 18, "base_type": 16,
    "department": 22, "matched_term": 16,
    # descriptions / prose
    "award_type_description": W_CATEGORY, "extent_competed_description": 26,
    "solicitation_procedures": 26, "naics_description": W_NAICS_DESC,
    "psc_description": W_CATEGORY, "funding_account_titles": W_NAICS_DESC,
    "description": W_TEXT, "sub_description": W_TEXT, "title": W_TEXT,
    # dates
    "date_signed": W_DATE, "pop_start_date": W_DATE, "pop_current_end_date": W_DATE,
    "pop_potential_end_date": W_DATE, "first_action_date": W_DATE,
    "last_action_date": W_DATE, "action_date": W_DATE, "sub_action_date": W_DATE,
    "submitted_date": W_DATE, "posted_date": W_DATE, "response_deadline": W_DATE,
    # analyst bridges (blank in the raw pull)
    "program": 14, "capability_node": 16,
    # provenance
    "source_system": 14, "source_id": 22, "extract_run_id": 34, "row_hash": 16,
}


def contract_width(header: str) -> int:
    """Width for a contract CSV column. Explicit map first, then suffix rules,
    then a safe default - so an unmapped column still sizes sensibly."""
    if header in _CONTRACT_W:
        return _CONTRACT_W[header]
    h = header.lower()
    if h.endswith(("_date", "_deadline")):
        return W_DATE
    if h.endswith("_uei"):
        return W_UEI
    if h.endswith(("_amount", "_value")):
        return W_AMOUNT
    if h.endswith(("_name", "_titles")) or "recipient" in h:
        return W_VENDOR
    if "description" in h or h == "title":
        return W_TEXT
    return 18


# ---------------------------------------------------------------------------
# Header alignment
# ---------------------------------------------------------------------------

def header_styles(headers: list[str], center_headers=()) -> list[int]:
    """Header-row styles: left-align text headers; center any numeric columns
    named in `center_headers`. Pass the same header strings used in the header
    write_row plus the subset that are numeric, e.g.

        c.write(HEADERS, styles=header_styles(HEADERS, center_headers=NUMERIC))
    """
    centered = set(center_headers)
    return [S_HEADER_CENTER if h in centered else S_HEADER_LEFT for h in headers]
