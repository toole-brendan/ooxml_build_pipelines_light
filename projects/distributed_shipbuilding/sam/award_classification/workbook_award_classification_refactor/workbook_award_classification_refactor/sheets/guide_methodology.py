"""guide_methodology - the "Methodology" tab (guide group; one module = one sheet).

The classification-method sheet, in six compact sections: scope and grain, the
three classification axes, the evidence hierarchy, the assignment rules, SWBS
treatment, and coverage / QA. Table-first, minimal prose - the current rules a
reader needs to interpret the figures, not how the pipeline implements them.

This workbook classifies suppliers (it carries no TAM/SAM market-sizing model), so
the sheet is self-contained - no live cross-sheet coefficient links. The axis
VOCABULARY (the legends, lattice, assignment rule) lives in the ``_taxonomy`` leaf
and is presented in full on the Taxonomy tab; this sheet renders the shared
constants it needs and otherwise points there for code-level definitions.
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
_COLS = [24, 40, 32, 16]


def _render_methodology() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(TAB_METHODOLOGY, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Scope, classification grain, evidence hierarchy and assignment rules."],
            styles=[S_ITALIC])
    c.blank(2)

    # §1 - Scope and grain
    c.banner("§1 - Scope and grain", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    for txt in [
        "Only Basic Construction prime contracts are included. Design, lead-yard support, ship "
        "alteration, planning-yard work, government-furnished-equipment (GFE) primes, and "
        "MIB / BlueForge pass-throughs are excluded.",
        "The classification unit is the supplier operating entity (UEI), taken per program - not the "
        "corporate parent and not the subaward transaction. Grain is UEI x Program: the same UEI may "
        "carry different Domain / Output values across DDG-51, Virginia and Columbia.",
        "A subaward transaction carries no NAICS of its own; NAICS is a self-reported entity "
        "attribute. So entity labels describe what the firm makes or does, and a UEI's subaward "
        "dollars inherit its labels (joined on entity UEI x program), preserving the reported total.",
        "The one transaction-level dimension is Ship-System Application (SWBS), carried on the "
        "HII-DDG subaward itself (see §5).",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.write(["Term", "Definition", "Treatment"], styles=S_HEADER_LEFT)
    _dn = {}
    for term, defn, treat in [
        ("Capability Domain (D)", "the technical ship area the entity is competent in",
         "published axis; D1-D11 (D11 = Services), D0 unresolved"),
        ("Operating Role (R)", "the value-chain responsibility the entity owns",
         "internal validation axis; R1-R5, R0; not published"),
        ("Primary Output (P)", "the physical form / integration level of what is delivered",
         "published axis; P1-P6, P0 unresolved"),
        ("Assignment basis", "the method that set the label, not the result",
         "research override or NAICS-6 map; blank = not yet classified"),
        ("Confidence", "strength of the entity evidence behind the label",
         "A specific NAICS, B corroborated secondary, C curated, U unresolved"),
        ("SWBS / subsystem", "the ship system worked on, from the observed SWBS code",
         "transaction-level; HII-DDG only; never compared across programs"),
    ]:
        _dn[term] = c.write([term, defn, treat],
                            styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 - Classification axes
    c.banner("§2 - Classification axes", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Axis", "Question it answers", "Status"], styles=S_HEADER_LEFT)
    for axis, question, status in AXES:
        c.write([axis, question, status], styles=[S_BOLD, S_DEFAULT, S_DEFAULT],
                outline_level=1)
    c.write(["Each axis answers one question and stays independent; every UEI x Program gets exactly "
             "one label per axis (MECE), with a forced catch-all (D0 / R0 / P0)."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["Capability Domain and Primary Output are published; Operating Role is internal - it "
             "bounds and validates the Output assignment, then drops out of the deliverable. Output "
             "is assigned from its own physical-form evidence; Role only checks that it is in-bounds."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2a - Role and Output validation lattice", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Code", "Operating Role", "Expected Primary Output"], styles=S_HEADER_LEFT)
    for code, short, expected in ROLE_OUTPUT_LATTICE:
        c.write([code, short, expected], styles=[S_BOLD, S_DEFAULT, S_DEFAULT],
                outline_level=1)
    c.write([LATTICE_NOTE], styles=[S_DEFAULT], outline_level=1)
    c.write(["Full code-level definitions and the axis legends are on the Taxonomy tab."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 - Evidence hierarchy
    c.banner("§3 - Evidence hierarchy", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Priority", "Source", "Treatment"], styles=S_HEADER_LEFT)
    for pri, source, treat in [
        ("1", "Curated vendor registry (operating-entity, hand-verified)",
         "authoritative; highest precedence - the highest-dollar UEIs researched first"),
        ("2", "NAICS-6 entity default",
         "the granular NAICS-6 to archetype mapping for the long tail"),
        ("3", "Unresolved",
         "when evidence is insufficient; still exactly one label per axis - nothing dropped"),
    ]:
        c.write([pri, source, treat], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Positive entity evidence beats the mechanical NAICS default (a desalination UEI maps "
             "to fluid systems, not the generic machinery code)."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["Primary Output is positive-evidence-only: an integration-suggestive NAICS sets a "
             "candidate flag, never an automatic high-integration (P4 / P5) assignment."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 - Assignment rules
    c.banner("§4 - Assignment rules", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["One label per UEI x Program, per axis:"], styles=[S_BOLD], outline_level=1)
    c.write([ASSIGNMENT_RULE], styles=[S_DEFAULT], outline_level=1)
    c.write(["Off-lattice Role x Output combinations are review flags, not errors (see §2a)."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4a - Capability Domain tie-breaks", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Situation", "Tie-break rule"], styles=S_HEADER_LEFT)
    for situation, rule in DOMAIN_TIEBREAKS:
        c.write([situation, rule], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4b - Primary Output boundary tests", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Boundary", "Test"], styles=S_HEADER_LEFT)
    for pair, test in OUTPUT_BOUNDARIES:
        c.write([pair, test], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 - SWBS treatment
    c.banner("§5 - SWBS treatment", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Ship-System Application (SWBS) is a transaction-level companion to the three entity "
             "axes, not a fourth supplier archetype: the SWBS code on each HII-DDG subaward says "
             "where in the ship the work lands. It is HII-DDG only - submarine subawards carry no "
             "SWBS equivalent - and is never compared across programs. Legend: Taxonomy §4."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§5a - SWBS mapping method", n_cols=_NCOLS, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Method", "Definition"], styles=S_HEADER_LEFT)
    for code, method in SWBS_MAPPING_METHOD:
        c.write([code, method], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.write(["Each mapping carries a confidence (High / Medium / Low); coverage is reported by "
             "method and confidence alongside mapped-dollar %."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§5b - Standing rules", n_cols=_NCOLS, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    c.blank()
    for txt in SWBS_GUARDRAILS:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §6 - Coverage and QA
    c.banner("§6 - Coverage and QA", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Coverage is always reported segmented by assignment basis (research override / "
             "NAICS-6 map / unclassified) and by confidence."],
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

    # Native Excel Notes: one concise hover on a load-bearing definition's Treatment
    # column (D) of §1 - matching the DDG/submarine Methodology pattern.
    notes = [
        ExcelNote(f"D{_dn['Operating Role (R)']}",
                  "Scaffolding, not output: Role bounds and validates the published Primary "
                  "Output (R1 covers P1/P2, R2 covers P2/P3, R3 covers P4, R4 covers P5, R5 "
                  "covers P6) and is dropped from the deliverable. Off-lattice cells are review flags."),
        ExcelNote(f"D{_dn['SWBS / subsystem']}",
                  "SWBS exists only for HII-DDG, so any cross-program subsystem comparison would "
                  "be a data artifact. It validates the entity tags; it does not overwrite them."),
    ]
    ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                   with_gutter=True, show_outline_symbols=True)
    return WorksheetSpec(ws, notes=notes)


METHODOLOGY = SheetEntry(TAB_METHODOLOGY, _GROUP, _render_methodology)
