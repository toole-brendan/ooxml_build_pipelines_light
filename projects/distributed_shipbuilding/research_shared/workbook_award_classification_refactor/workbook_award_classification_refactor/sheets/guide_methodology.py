"""guide_methodology - the "Methodology" tab (guide group; one module = one sheet).

The classification-method sheet, structured to match the DDG/submarine Methodology
tabs: definitions, the classification unit & grain, the three axes and how they
relate, evidence precedence, the assignment rule, the program asymmetry, scope
hygiene, and coverage reporting. Table-first, minimal prose.

This workbook classifies suppliers (it carries no TAM/SAM market-sizing model), so
the sheet is self-contained - no live cross-sheet coefficient links. The axis
VOCABULARY (the legends, lattice, assignment rule) lives in the ``_taxonomy`` leaf
and is presented in full on the Taxonomy tab; this sheet renders the shared
constants it needs and otherwise points there for code-level definitions. Pure
consumer (no accessors).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._tabs import TAB_METHODOLOGY
from workbook_award_classification_refactor.sheets._taxonomy import (
    AXES, ROLE_OUTPUT_LATTICE, LATTICE_NOTE, ASSIGNMENT_RULE,
    DOMAIN_TIEBREAKS, OUTPUT_BOUNDARIES,
    SWBS_MAPPING_METHOD, SWBS_GUARDRAILS,
)

_GROUP = "guide"
_NCOLS = 4
#       B term/label | C definition | D treatment | E (note anchor / spare)
_COLS = [26, 46, 40, 20]


def _render_methodology() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(TAB_METHODOLOGY, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["How the classification is produced - unit, grain, the three axes, "
             "evidence precedence, and the assignment rule."], styles=[S_ITALIC])
    c.blank(2)

    # §1 - Definitions
    c.banner("§1 - Definitions", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Term", "Definition", "Treatment"], styles=S_HEADER_LEFT)
    _dn = {}
    for term, defn, treat in [
        ("Classification unit", "the supplier operating entity (UEI), taken per program",
         "UEI x Program; the same UEI may differ across DDG-51 / Virginia / Columbia"),
        ("Capability Domain", "the technical ship area the entity is competent in",
         "published axis - D1-D11 (D11 = Services & non-material support), D0 unresolved"),
        ("Operating Role", "the value-chain responsibility the entity owns",
         "internal validation layer - R1-R5, R0; not published"),
        ("Primary Output", "the physical form / integration level of what is delivered",
         "published axis - P1-P6, P0 unresolved"),
        ("Canonical universe", "the post-filtered new-construction subaward base",
         "~$12.49B; hull-builder (Basic Construction) prime only - subs = GDEB, GFE primes (BPMI/LM/BAE/RR) and MIB pass-throughs removed"),
        ("Assignment basis", "the method that set the archetype label (not the result)",
         "Research override (researched prose, takes precedence) or NAICS-6 map; blank = not yet classified. Unresolved is a code (D0/P0), not a basis."),
        ("Confidence", "strength of the entity evidence behind the label",
         "A specific NAICS, B corroborated secondary, C curated, U unresolved"),
        ("SWBS / subsystem", "the ship system worked on, from the observed SWBS code",
         "transaction-level; HII-DDG only; never compared across programs"),
        ("scope_status", "relevance-to-new-construction hygiene tag",
         "quarantine-and-report; totals still tie to $13.1B"),
    ]:
        _dn[term] = c.write([term, defn, treat], styles=[S_BOLD, S_DEFAULT, S_DEFAULT],
                            outline_level=1)
    c.blank(2)

    # §2 - Classification unit & grain
    c.banner("§2 - Classification unit & grain", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    for txt in [
        "The primary unit is the supplier operating entity (UEI), taken per program - not the corporate parent, and not the subaward transaction.",
        "A subaward transaction carries no NAICS/PSC of its own; NAICS is an entity-level, self-reported attribute. So entity labels describe what the company makes or does, and a UEI's subaward dollars inherit its labels (join on entity_uei x program), preserving the $13.1B total.",
        "Grain is UEI x Program: the same UEI may receive different Domain / Role / Output values across DDG-51, Virginia, and Columbia (e.g. communications on one program, electric propulsion on another).",
        "The one record-level exception is the SWBS / subsystem dimension, carried on the HII-DDG transaction itself and reconciled at the subaward join.",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 - The three classification axes
    c.banner("§3 - The three classification axes", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Axis", "Question it answers", "Status"], styles=S_HEADER_LEFT)
    for axis, question, status in AXES:
        c.write([axis, question, status], styles=[S_BOLD, S_DEFAULT, S_DEFAULT],
                outline_level=1)
    c.write(["Each axis answers exactly one question and is kept independent of the others; every UEI x Program gets exactly one label on each axis (MECE), with a forced catch-all (D0 / R0 / P0)."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["Capability Domain and Primary Output are published; Operating Role is internal - it bounds and validates the Output assignment (see lattice), then drops out of the deliverable. Output is assigned from its own physical-form evidence; Role checks it is in-bounds, it does not generate it. That discipline keeps role/activity reasoning off the Domain and Output axes - the reason the schema is split three ways."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§3a - Role -> Output validation lattice", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Code", "Operating Role", "Expected Primary Output"], styles=S_HEADER_LEFT)
    for code, short, expected in ROLE_OUTPUT_LATTICE:
        c.write([code, short, expected], styles=[S_BOLD, S_DEFAULT, S_DEFAULT],
                outline_level=1)
    c.write([LATTICE_NOTE], styles=[S_DEFAULT], outline_level=1)
    c.write(["Full code-level definitions and the axis legends live on the Taxonomy tab; the assignment rule and boundary rules are in §5."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 - Evidence & precedence
    c.banner("§4 - Evidence & precedence", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Priority", "Source", "Treatment"], styles=S_HEADER_LEFT)
    for pri, source, treat in [
        ("1", "Curated vendor registry (operating-entity, hand-verified)",
         "authoritative; highest precedence - the highest-dollar UEIs researched first"),
        ("2", "NAICS-6 entity default",
         "the granular NAICS-6 -> archetype mapping for the long tail"),
        ("3", "Unresolved",
         "when evidence is insufficient; still exactly one label per axis - nothing silently dropped"),
    ]:
        c.write([pri, source, treat], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Positive entity evidence beats the mechanical NAICS default (a desalination UEI maps to fluid systems, not the generic machinery code)."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["Primary Output is positive-evidence-only: integration-suggestive NAICS sets a candidate flag, never an automatic high-integration (P4 / P5) assignment."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 - Assignment rule & boundary rules
    c.banner("§5 - Assignment rule & boundary rules", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["One label per UEI x Program, per axis:"], styles=[S_BOLD], outline_level=1)
    c.write([ASSIGNMENT_RULE], styles=[S_DEFAULT], outline_level=1)
    c.write(["Off-lattice Role x Output combinations are review flags, not errors - they trigger a second look, not a correction (see §3a)."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§5a - Capability Domain tie-breaks", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Situation", "Tie-break rule"], styles=S_HEADER_LEFT)
    for situation, rule in DOMAIN_TIEBREAKS:
        c.write([situation, rule], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§5b - Primary Output boundary tests", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Boundary", "Test"], styles=S_HEADER_LEFT)
    for pair, test in OUTPUT_BOUNDARIES:
        c.write([pair, test], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §6 - HII-DDG vs submarine
    c.banner("§6 - HII-DDG vs submarine evidence", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Program", "Entity axes (Domain / Role / Output)", "Subsystem (SWBS)"],
            styles=S_HEADER_LEFT)
    for prog, axes_basis, swbs in [
        ("HII-DDG", "from the entity (registry / NAICS)", "SWBS present -> subsystem populated"),
        ("Virginia / Columbia", "from the entity only",
         "no SWBS equivalent; the ~half-present GDEB code reflects order details, not work type - not used"),
    ]:
        c.write([prog, axes_basis, swbs], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Never compare subsystem mix across programs - SWBS exists only for HII-DDG, so any cross-program system comparison would be a data artifact."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §7 - Scope hygiene (scope_status)
    c.banner("§7 - Scope hygiene (scope_status)", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    for txt in [
        "scope_status is a hygiene tag applied at the end, once the full mapping and registry are complete, independent of the three axes.",
        "It flags residuals that should have been excluded upstream - e.g. workforce/training, GFE, prime-owned in-house work (illustrative, not exhaustive).",
        "Quarantine-and-report, not purge: residuals are shown separately and retained so totals still tie to $13.1B; the corpus is not re-baselined.",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §8 - Coverage reporting
    c.banner("§8 - Coverage reporting", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Coverage is always reported segmented by assignment basis (Research override / NAICS-6 map / unclassified) and by confidence."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["Confidence", "Meaning"], styles=S_HEADER_LEFT)
    for conf, mean in [
        ("A", "specific primary NAICS"),
        ("B", "corroborated process / secondary signal"),
        ("C", "curated entity evidence"),
        ("U", "unresolved"),
    ]:
        c.write([conf, mean], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §9 - Ship-System Application (SWBS), transaction-level
    c.banner("§9 - Ship-System Application (SWBS), transaction-level", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["A transaction-level companion to the three entity axes (not a fourth supplier archetype): the SWBS code on each HII-DDG subaward says where in the ship's functional architecture the work lands. Each HII-DDG transaction inherits the vendor's DDG-51 Domain / Role / Output; its SWBS application can vary transaction by transaction. Full legend: Taxonomy §5."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§9a - SWBS mapping method", n_cols=_NCOLS, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Method", "Definition"], styles=S_HEADER_LEFT)
    for code, method in SWBS_MAPPING_METHOD:
        c.write([code, method], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.write(["Each mapping also carries an swbs_mapping_confidence (High / Medium / Low); coverage is reported segmented by method and confidence alongside mapped-dollar %."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§9b - Standing rules", n_cols=_NCOLS, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    c.blank()
    for txt in SWBS_GUARDRAILS:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # Native Excel Notes: one concise hover per load-bearing definition, on the
    # Treatment column (D) of §1 - matching the DDG/submarine Methodology pattern.
    notes = [
        ExcelNote(f"D{_dn['Classification unit']}",
                  "Entity-level, not transaction-level: a subaward carries no NAICS/PSC, so "
                  "all of a UEI's dollars inherit its entity labels via entity_uei x program. "
                  "Preserves the $13.1B total."),
        ExcelNote(f"D{_dn['Operating Role']}",
                  "Scaffolding, not output: Role bounds and validates the published Primary "
                  "Output (R1->P1/P2, R2->P2/P3, R3->P4, R4->P5, R5->P6) and is dropped from "
                  "the deliverable. Off-lattice cells are review flags."),
        ExcelNote(f"D{_dn['Canonical universe']}",
                  "Source is the program-split corpus ($13.1B, MIB-excluded), not the SAM "
                  "entity-enrichment profiles. Always the post-filtered base; raw per-PIID "
                  "pulls are not classified directly."),
    ]
    ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, notes=notes)


METHODOLOGY = SheetEntry(TAB_METHODOLOGY, _GROUP, _render_methodology)
