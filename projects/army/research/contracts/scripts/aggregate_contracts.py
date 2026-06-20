#!/usr/bin/env python3
"""AGGREGATE — flatten the raw contract pulls into the four tidy workbook CSVs,
following the funding-layer invariants (amount_type money discipline; per-row
provenance: source_system / source_id / extract_run_id / row_hash). Writes to
projects/army/workbook/extracted/ alongside the budget_* facts.

Four tables (the money-discipline boundary is the whole point):
  contract_awards.csv         one row per award (PIID/IDV/TO). Value columns are
                              DISTINCT amount_types (obligation / current_value /
                              ceiling) — never sum across them; this is a register,
                              not a fact table.
  contract_award_actions.csv  one row per modification — THE ONLY SUM-ABLE TABLE.
                              amount_type=obligation, per-mod dollars. Reconciled:
                              FPDS per-mod obligatedAmount WINS; USAspending
                              transactions fill awards FPDS didn't return.
  contract_subawards.csv      first-tier FFATA subs (SAM Stage 4). amount_type=
                              subaward — a SEPARATE money universe; never summed
                              with prime award/budget dollars.
  contract_pipeline_events.csv  pre-award notices (SAM Stage 5). No dollars; the
                              forward half of the recompete radar.

Tie-back hooks (left for the analyst bridges, not guessed here):
  * funding_tas on awards -> appropriation/PE/BLI via the budget line_item keys.
  * capability_node + program columns are emitted BLANK — the capability bridge
    (workbook/analyst/capability_nodes.csv) and the program attribution bridge fill
    them; keeping judgment out of the mechanical aggregate is invariant #2.

Run after Stages 2 (+3 for authoritative actions; 4/5 optional). Idempotent.
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = Path(__file__).resolve().parents[1]                 # research/contracts/
EXTRACT = ROOT / "extracted"
USASPENDING_RAW = ROOT / "usaspending_raw"
FPDS_RAW = ROOT / "fpds_raw"
SAM_SUB = ROOT / "sam_subawards"
OUT = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/army/workbook/extracted")
RUN_ID = "army-contracts-aggregate-2026-06-20"
DOLLARS_BASIS = "then_year"


def safe(gid: str) -> str:
    return "".join(c if (c.isalnum() or c in "._-") else "_" for c in gid)


def rhash(*parts) -> str:
    return hashlib.blake2b("|".join("" if p is None else str(p) for p in parts).encode(),
                           digest_size=8).hexdigest()


def dod_fy(date_str):
    if not date_str or len(date_str) < 7:
        return None
    try:
        y, m = int(date_str[:4]), int(date_str[5:7])
    except ValueError:
        return None
    return y + 1 if m >= 10 else y


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ---------- load FPDS per-mod actions, keyed by (piid, referenced_idv_piid) ----------
def load_fpds_actions():
    by_key = {}
    for fp in glob.glob(str(FPDS_RAW / "*.json")):
        if Path(fp).name.startswith("_"):
            continue
        try:
            doc = json.loads(Path(fp).read_text())
        except Exception:
            continue
        for r in doc.get("records", []):
            key = (r.get("piid"), r.get("referenced_idv_piid") or None)
            by_key.setdefault(key, []).append(r)
    return by_key


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = json.loads((EXTRACT / "_detail_index.json").read_text())
    fpds = load_fpds_actions()

    award_rows, action_rows = [], []
    n_fpds_awards = n_usasp_awards = 0

    for e in index:
        gid = e["generated_internal_id"]
        piid = e.get("piid")
        parent_idv = e.get("parent_idv_piid")
        # FPDS match key: task orders carry the parent IDV as referenced_idv_piid.
        fpds_recs = fpds.get((piid, parent_idv)) or fpds.get((piid, None)) or []

        # ---- awards register row (distinct amount_types as columns) ----
        award_rows.append({
            "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
            "idv_type": e.get("idv_type_description"),
            "single_or_multiple_award": e.get("single_or_multiple_award"),
            "award_type": e.get("award_type"),
            "award_type_description": e.get("award_type_description"),
            "category": e.get("category"),
            "recipient_name": e.get("recipient_name"),
            "recipient_uei": e.get("recipient_uei"),
            "parent_recipient_name": e.get("parent_recipient_name"),
            "obligation_amount": e.get("total_obligation"),       # amount_type=obligation
            "current_value": e.get("base_exercised_options"),     # amount_type=current_value
            "ceiling_value": e.get("base_and_all_options"),       # amount_type=ceiling
            "total_outlay": e.get("total_outlay"),
            "subaward_count": e.get("subaward_count"),
            "total_subaward_amount": e.get("total_subaward_amount"),
            "date_signed": e.get("date_signed"),
            "pop_start_date": e.get("pop_start_date"),
            "pop_current_end_date": e.get("pop_current_end_date"),
            "pop_potential_end_date": e.get("pop_potential_end_date"),
            "first_action_date": e.get("first_action_date"),
            "last_action_date": e.get("last_action_date"),
            "extent_competed": e.get("extent_competed"),
            "extent_competed_description": e.get("extent_competed_description"),
            "solicitation_procedures": e.get("solicitation_procedures_description"),
            "fair_opportunity_limited": e.get("fair_opportunity_limited"),
            "number_of_offers": e.get("number_of_offers_received"),
            "naics_code": e.get("naics_code"), "naics_description": e.get("naics_description"),
            "psc_code": e.get("psc_code"), "psc_description": e.get("psc_description"),
            "funding_tas": "; ".join(e.get("funding_federal_accounts") or []),
            "funding_account_titles": "; ".join(e.get("funding_account_titles") or []),
            "has_tas": e.get("has_tas"),
            "matched_axes": e.get("matched_axes"),
            "actions_source": "fpds" if fpds_recs else "usaspending",
            "program": "",          # <- program attribution bridge fills
            "capability_node": "",  # <- capability bridge fills (Platform/Sensors/Effectors/C2)
            "dollars_basis": DOLLARS_BASIS,
            "source_system": "usaspending+fpds",
            "source_id": "USASP-AWARD-DETAIL",
            "extract_run_id": RUN_ID,
            "row_hash": rhash(gid, e.get("total_obligation"), e.get("pop_current_end_date")),
        })

        # ---- award_actions (THE sum-able table): FPDS wins, USAspending fills ----
        if fpds_recs:
            n_fpds_awards += 1
            for r in fpds_recs:
                ad = r.get("signed_date")
                action_rows.append({
                    "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
                    "mod_number": r.get("mod_number"),
                    "recipient_name": r.get("vendor_name") or e.get("recipient_name"),
                    "recipient_uei": r.get("vendor_uei") or e.get("recipient_uei"),
                    "action_date": ad, "fiscal_year": dod_fy(ad),
                    "amount_type": "obligation", "amount": fnum(r.get("this_obligated")),
                    "dollars_basis": DOLLARS_BASIS,
                    "action_type": r.get("contract_action_type"),
                    "pricing_type": r.get("pricing_type"),
                    "extent_competed": r.get("extent_competed"),
                    "contracting_office": r.get("contracting_office"),
                    "funding_office": r.get("funding_office"),
                    "psc_code": r.get("psc"), "naics_code": r.get("naics"),
                    "description": (r.get("description") or "")[:300],
                    "source_system": "fpds", "source_id": "FPDS-ATOM",
                    "extract_run_id": RUN_ID,
                    "row_hash": rhash(gid, r.get("mod_number"), ad, r.get("this_obligated")),
                })
        else:
            n_usasp_awards += 1
            tpath = USASPENDING_RAW / "transactions" / f"{safe(gid)}.json"
            txns = []
            if tpath.exists():
                try:
                    txns = json.loads(tpath.read_text()).get("results", [])
                except Exception:
                    txns = []
            for t in txns:
                ad = t.get("action_date")
                action_rows.append({
                    "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
                    "mod_number": t.get("modification_number"),
                    "recipient_name": e.get("recipient_name"),
                    "recipient_uei": e.get("recipient_uei"),
                    "action_date": ad, "fiscal_year": dod_fy(ad),
                    "amount_type": "obligation", "amount": fnum(t.get("federal_action_obligation")),
                    "dollars_basis": DOLLARS_BASIS,
                    "action_type": t.get("action_type_description"),
                    "pricing_type": None, "extent_competed": None,
                    "contracting_office": None, "funding_office": None,
                    "psc_code": e.get("psc_code"), "naics_code": e.get("naics_code"),
                    "description": (t.get("description") or "")[:300],
                    "source_system": "usaspending", "source_id": "USASP-TXN",
                    "extract_run_id": RUN_ID,
                    "row_hash": rhash(gid, t.get("modification_number"), ad, t.get("federal_action_obligation")),
                })

    # ---- subawards (SAM Stage 4) ----
    sub_rows = []
    for fp in glob.glob(str(SAM_SUB / "*.json")):
        try:
            doc = json.loads(Path(fp).read_text())
        except Exception:
            continue
        for s in doc.get("published", []):
            ad = s.get("subAwardDate")
            sub_rows.append({
                "prime_piid": doc.get("piid"), "prime_agency_id": doc.get("agency_id"),
                "prime_referenced_idv_piid": doc.get("referenced_idv_piid"),
                "prime_recipient": doc.get("recipient"),
                "sub_award_report_id": s.get("subAwardReportId"),
                "sub_award_number": s.get("subAwardNumber"),
                "amount_type": "subaward", "amount": fnum(s.get("subAwardAmount")),
                "dollars_basis": DOLLARS_BASIS,
                "sub_action_date": ad, "fiscal_year": dod_fy(ad),
                "submitted_date": s.get("submittedDate"),
                "sub_entity_name": s.get("subEntityLegalBusinessName"),
                "sub_entity_uei": s.get("subEntityUei"),
                "sub_parent_uei": s.get("subParentUei"),
                "sub_parent_name": s.get("subEntityParentLegalBusinessName"),
                "sub_description": (s.get("subawardDescription") or "")[:300],
                "prime_naics": (s.get("primeNaics") or {}).get("code") if isinstance(s.get("primeNaics"), dict) else None,
                "capability_node": "",
                "source_system": "sam_subaward", "source_id": "SAM-SUBAWARD",
                "extract_run_id": RUN_ID,
                "row_hash": rhash(s.get("subAwardReportId"), s.get("subAwardAmount")),
            })

    # ---- pipeline_events (SAM Stage 5) ----
    pipe_rows = []
    oidx = EXTRACT / "_opportunities_index.json"
    if oidx.exists():
        for o in json.loads(oidx.read_text()):
            pipe_rows.append({
                "notice_id": o.get("notice_id"), "title": o.get("title"),
                "solicitation_number": o.get("solicitation_number"),
                "notice_type": o.get("type"), "base_type": o.get("base_type"),
                "posted_date": o.get("posted_date"), "fiscal_year": dod_fy(o.get("posted_date")),
                "response_deadline": o.get("response_deadline"),
                "naics_code": o.get("naics"), "psc_code": o.get("psc"),
                "set_aside": o.get("set_aside"), "department": o.get("department"),
                "award_number": o.get("award_number"), "matched_term": o.get("matched_term"),
                "capability_node": "",
                "source_system": "sam_opportunities", "source_id": "SAM-OPPORTUNITY",
                "extract_run_id": RUN_ID,
                "row_hash": rhash(o.get("notice_id")),
            })

    # ---- write ----
    award_cols = list(award_rows[0].keys()) if award_rows else []
    action_cols = ["award_id", "piid", "parent_idv_piid", "mod_number", "recipient_name",
                   "recipient_uei", "action_date", "fiscal_year", "amount_type", "amount",
                   "dollars_basis", "action_type", "pricing_type", "extent_competed",
                   "contracting_office", "funding_office", "psc_code", "naics_code",
                   "description", "source_system", "source_id", "extract_run_id", "row_hash"]
    sub_cols = list(sub_rows[0].keys()) if sub_rows else [
        "prime_piid", "amount_type", "amount", "sub_entity_name", "source_system",
        "extract_run_id", "row_hash"]
    pipe_cols = list(pipe_rows[0].keys()) if pipe_rows else [
        "notice_id", "title", "posted_date", "source_system", "extract_run_id", "row_hash"]

    write_csv(OUT / "contract_awards.csv", award_cols, award_rows)
    write_csv(OUT / "contract_award_actions.csv", action_cols, action_rows)
    write_csv(OUT / "contract_subawards.csv", sub_cols, sub_rows)
    write_csv(OUT / "contract_pipeline_events.csv", pipe_cols, pipe_rows)

    # ---- reconciliation report ----
    sum_actions = sum(a["amount"] or 0 for a in action_rows)
    sum_oblig_awards = sum((a["obligation_amount"] or 0) for a in award_rows)
    print(f"=== aggregate_contracts {RUN_ID}")
    print(f"  contract_awards.csv          {len(award_rows):>6} awards "
          f"(actions source: {n_fpds_awards} FPDS / {n_usasp_awards} USAspending)")
    print(f"  contract_award_actions.csv   {len(action_rows):>6} mod actions  "
          f"sum(amount)=${sum_actions/1e6:,.1f}M   [THE sum-able table]")
    print(f"     cross-check awards.obligation sum = ${sum_oblig_awards/1e6:,.1f}M "
          f"(per-mod vs award-level differ by deobligations / FPDS-wins reconciliation)")
    print(f"  contract_subawards.csv       {len(sub_rows):>6} first-tier subs   "
          f"sum=${sum(s['amount'] or 0 for s in sub_rows)/1e6:,.1f}M")
    print(f"  contract_pipeline_events.csv {len(pipe_rows):>6} pre-award notices")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
