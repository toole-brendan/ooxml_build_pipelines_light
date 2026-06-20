"""Outsourcing Ceiling Explainer - plain-language guide to the ceiling estimate.

INTENT
    A from-the-top, plain-English explainer of how the analysis sizes the
    *ceiling* on outsourcing new-construction shipbuilding work — written for a
    reader who has never seen the workbook. It opens by placing the analysis in
    the wider distributed-shipbuilding project, then states the question (how much
    of the build could, in theory, leave the prime yard?), and builds from the
    basics (what "Basic Construction" is) to the two sourced numbers that do the
    work, the core-vs-ceiling idea, and the hours-to-dollars bridge — landing on
    the headline read and what to be careful about. Prose-first (headings + body + lists
    + two at-a-glance tables), not a slide mock - so it reads as a normal Word
    document page in portrait.

OUTLINE (source-only; not emitted)
    - H1   How We Size the Outsourcing Ceiling
    - lead what this page is (the ceiling question, in plain terms)
    - H2   Where this fits in the distributed shipbuilding project
    - H2   The question in one sentence
    - H2   The breakthrough: build the ceiling, don't look it up
    - H2   Start with the basics: what is "Basic Construction"?
    - H2   The two numbers that do the work             <- h and L, sourced
    - H2   The idea in one line: core vs. ceiling
    - H2   From hours to dollars                        <- the bridge + three reads
    - H2   What we found
    - Table 1  core / selected case / ceiling, by program
    - H2   Where the numbers come from (sources + Table 2)
    - H2   What to be careful about                     <- caveats land after sources
    - source line

LOCAL OVERRIDES (inline only; no core edits)
    - No blue font: headings (the named style is BLUE_5) and Caption / Source
      (GRAY_4) get a run-level BLACK override. Heading hierarchy is carried instead
      by a thin gray bottom rule under H1/H2 (_HRULE) plus the size ramp.
    - Lists are drawn inline (_list / _olist), not Word's numbering.xml, to get the
      rendered-markdown glyph hierarchy (• disc / ◦ circle / ▪ square), one indent
      system, and a consistent 6pt breather after each list.
    - Tables paginate cleanly via _rule_table (rows can't split; header repeats).
    - 0.75in left/right margins via a local PageSetup (top/bottom stay 1in).
"""
from __future__ import annotations

import re

from docx_core.primitives import paragraph, run, table_block
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PageSetup
from docx_core.rhythm import PageMargins
from docx_core.style import BLACK
from docx_core.style_ids import (
    R_STRONG, P_SOURCE, P_CAPTION, P_LIST, P_H1, P_H2, P_H3,
)

PAGE_TITLE = "Outsourcing Ceiling - plain-language explainer"

# 0.75in left/right margins (top/bottom stay at the 1in report default). Inline,
# so docx_core's shared presets are untouched.
PAGE_SETUP = PageSetup(margins=PageMargins(left_in=0.75, right_in=0.75))

_HSTYLE = {1: P_H1, 2: P_H2, 3: P_H3}

# Thin gray bottom rule under H1/H2 so sections separate cleanly WITHOUT color
# (the named heading style is blue, but the house ask is no blue font at all). H1
# gets a heavier/darker rule than H2; H3 none. sz is in eighths of a point.
_HRULE = {
    1: '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="2" w:color="7F7F7F"/></w:pBdr>',
    2: '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="BFBFBF"/></w:pBdr>',
}


def _h(level: int, text: str) -> str:
    """Heading: black run override (no blue, per the house ask — the named style is
    blue) plus a thin gray bottom rule under H1/H2, so the hierarchy reads through a
    divider + the size ramp rather than color. Size/bold/air-above/keep-next still
    ride on the named heading style."""
    return paragraph([run(text, color=BLACK)], style=_HSTYLE[level],
                     raw_ppr_extra=_HRULE.get(level, ""))


def _rule_table(headers: list[str], rows: list[list[str]]) -> str:
    """A rule table that paginates cleanly. Every row carries <w:cantSplit/> so a
    tall row never breaks mid-cell across a page (the first render showed exactly
    that). The header row already repeats on continuation (the primitive sets
    <w:tblHeader/>), so when a table crosses a page boundary it picks up its header
    again rather than stranding a bare row — and the table fills the page instead
    of jumping whole and leaving a big gap. Paired with a keep_next caption so the
    caption never strands above a break. Done inline because the shared table
    primitive doesn't expose cantSplit and core stays untouched."""
    tbl = table_block(headers, rows)[0]            # single table string (no caption)
    def _cant_split(m: re.Match) -> str:
        tr = m.group(0)
        if tr.startswith("<w:tr><w:trPr>"):         # header row already has a trPr
            return tr.replace("<w:tr><w:trPr>", "<w:tr><w:trPr><w:cantSplit/>", 1)
        return tr.replace("<w:tr>", "<w:tr><w:trPr><w:cantSplit/></w:trPr>", 1)
    return re.sub(r"<w:tr>.*?</w:tr>", _cant_split, tbl, flags=re.S)


# --- markdown-clean list hierarchy (inline; core's numbering.xml untouched) -----
# Real Word lists give • / o (Courier) / ▪ and no after-block breather. To get the
# rendered-markdown look (disc -> circle -> square) with one consistent indent and
# a gap after each list, markers are drawn by hand: a glyph/number run + <w:tab/>,
# a per-level hanging indent matching the workbook's list geometry (glyph at
# 0.25/0.5/0.75in, text 0.25in further), tight rhythm between items, and a wider
# gap after the last item so a list never collides with the next paragraph.
_BULLET = {0: "&#x2022;", 1: "&#x25E6;", 2: "&#x25AA;"}   # • disc · ◦ circle · ▪ square
_LIST_LEFT = {0: 720, 1: 1080, 2: 1440}                    # text indent, twips
_LIST_HANG = 360                                           # marker hangs back 0.25in
_LIST_AFTER = 40                                           # 2pt between items
_LIST_AFTER_LAST = 120                                     # 6pt breather after the list


def _list_para(marker: str, content, level: int, after: int) -> str:
    left = _LIST_LEFT[level]
    ppr = (f'<w:tabs><w:tab w:val="left" w:pos="{left}"/></w:tabs>'
           f'<w:spacing w:after="{after}" w:line="240" w:lineRule="auto"/>'
           f'<w:ind w:left="{left}" w:hanging="{_LIST_HANG}"/>')
    runs = [f'<w:r><w:t xml:space="preserve">{marker}</w:t><w:tab/></w:r>']
    runs += list(content) if isinstance(content, list) else [run(content)]
    return paragraph(runs, style=P_LIST, raw_ppr_extra=ppr)


def _list(rows) -> list[str]:
    """Markdown-clean bullets. rows = list of (content, level); content is a plain
    string or a list of run() strings. Glyph by depth; 6pt breather after the last."""
    n = len(rows)
    return [_list_para(_BULLET[lvl], c, lvl,
                       _LIST_AFTER_LAST if i == n - 1 else _LIST_AFTER)
            for i, (c, lvl) in enumerate(rows)]


def _olist(items) -> list[str]:
    """Numbered steps (1. 2. 3.) sharing the bullet geometry + after-block breather,
    so the spacing contract stays uniform across list types (numbers are static)."""
    n = len(items)
    return [_list_para(f"{i + 1}.", t, 0,
                       _LIST_AFTER_LAST if i == n - 1 else _LIST_AFTER)
            for i, t in enumerate(items)]


# At-a-glance figures for the two body tables, pulled out so the headline read lives
# in one place. This page mirrors the workbook headline (it is not wired to it); if
# the workbook headline moves, update these rows. _body() feeds them to _rule_table.
RESULT_HEADERS = ["Program", "Must stay (core)", "Selected case (p=50%)",
                  "Ceiling (p=100%)", "vs. today"]
RESULT_ROWS = [
    ["Virginia", "25%", "50%", "75%", "about 2.2x"],
    ["Columbia", "25%", "50%", "75%", "about 3.4x"],
    ["DDG-51", "20%", "52%", "80%", "about 6.1x"],
    ["Portfolio", "24%", "51%", "76%", "about 3.0x"],
]

SOURCE_HEADERS = ["Number", "What it means", "Where it comes from"]
SOURCE_ROWS = [
    ["Movable hours (about 50%)",
     "The share of submarine labor hours that can be done outside the "
     "prime yard",
     "Navy submarine program executive, press interview (2022) — the "
     "two-to-five-million supplier-hours ramp"],
    ["Labor share (about 40%)",
     "Labor as a share of a ship's total cost; re-based higher onto "
     "Basic Construction",
     "Congressional Research Service testimony (2025), cross-checked "
     "against an independent cost index (2024)"],
    ["One build line",
     "Confirms there is no published split of assembly vs. outsourceable "
     "work to read off",
     "Pentagon budget-rules exhibit, plus the shipbuilders' annual "
     "reports"],
    ["Today's off-yard share (the floor)",
     "Virginia 34%, Columbia 22%, DDG-51 about 13% — the starting point "
     "the ceiling is measured against",
     "Announced place-of-performance shares for each program"],
]


def _body() -> list[str]:
    return [
        _h(1, "How We Size the Outsourcing Ceiling"),
        paragraph([
            run("In plain terms: ", style=R_STRONG),
            run("the ceiling is the most of a ship's new-construction work that "
                "could, in theory, be bought from outside suppliers instead of "
                "done inside the prime shipyard — if the only work that truly has "
                "to stay in the yard is final assembly, integration, and test. "
                "This page explains, from the top, how we put a number on that "
                "ceiling, why we had to build it up from two sourced figures "
                "rather than read it off a budget line, and what it comes out to."),
        ]),

        _h(2, "Where this fits in the distributed shipbuilding project"),
        paragraph(
            "The wider project asks one question: how much of the work of building "
            "the Navy's warships is moving away from the prime shipyards and out to "
            "a distributed base of suppliers — and how big an opening that creates "
            "for a new entrant. The work splits in two:"),
        *_list([
            ([run("Looking back — what is already outsourced.", style=R_STRONG),
              run(" A separate Award Analysis workbook reads the supplier records "
                  "to map the work the shipbuilders already buy from outside: who "
                  "wins it, how concentrated it is, and when it comes up to be "
                  "bought again.")], 0),
            ([run("Looking forward — how much more could move.", style=R_STRONG),
              run(" That is this workbook. It puts an upper bound on outsourcing — "
                  "the largest share of a ship's build that could, in principle, "
                  "leave the prime yard.")], 0),
        ]),
        paragraph(
            "The two meet at this page's headline read: the opening is the gap "
            "between what is distributed today — the share already built away from "
            "the prime yard — and the structural ceiling above it. This workbook "
            "sizes that ceiling, and so the headroom still on the table."),

        _h(2, "The question in one sentence"),
        paragraph([
            run("How much higher could outsourcing go? ", style=R_STRONG),
            run("Today a known share of each ship's build already happens away "
                "from the prime yard. The question is not what that share is now — "
                "it is how high it could climb before it runs into the work that "
                "physically cannot leave the yard."),
        ]),

        _h(2, "The breakthrough: build the ceiling, don't look it up"),
        paragraph(
            "The obvious move would be to find an official figure for "
            "“assembly work that must stay” versus “work that could "
            "be outsourced.” Two facts forced a different approach:"),
        *_list([
            ([run("The clean line does not exist.", style=R_STRONG),
              run(" The budget lumps the whole hull-and-structure build into one "
                  "line; it never splits labor from materials, or "
                  "“assembly” from “parts you could buy elsewhere.” "
                  "The Pentagon's own budget rules and the shipbuilders' annual "
                  "reports confirm the split simply is not published.")], 0),
            ([run("Today's number is the floor, not the ceiling.", style=R_STRONG),
              run(" The share already performed away from the prime yard "
                  "(Virginia 34%, Columbia 22%, DDG-51 about 13%) is the announced "
                  "place of performance — where the work happens today, which is "
                  "not the same as work contracted out to suppliers. Using it as "
                  "the ceiling would assume away the very growth we are trying to "
                  "size — so it becomes the starting floor, and the ceiling has to "
                  "come from somewhere else.")], 0),
        ]),
        paragraph([
            run("So instead of looking the ceiling up, we ", style=None),
            run("build it", style=R_STRONG),
            run(" from two numbers that "),
            run("are", style=R_STRONG),
            run(" published and citable. The rest of this page is those two "
                "numbers and the simple arithmetic that turns them into a "
                "ceiling."),
        ]),

        _h(2, "Start with the basics: what is “Basic Construction”?"),
        paragraph(
            "When the Navy buys a ship, the largest single piece of the price is a "
            "budget line usually called Basic Construction — the shipbuilder-side "
            "labor and the material the yard itself buys to build and assemble the "
            "ship. It does not include government-furnished gear like the combat "
            "system or, on the submarines, the reactor; those are bought "
            "separately. Everything in this analysis is measured as a share of that "
            "Basic Construction line — not of the ship's total cost — because that "
            "is the work a shipbuilder can choose to do in-house or send out."),

        _h(2, "The two numbers that do the work"),
        paragraph(
            "The whole estimate rests on two sourced figures. Both describe the "
            "build as shares, so they travel across programs and dollar years:"),
        *_list([
            ([run("How much labor can leave the yard (we call it h).",
                  style=R_STRONG),
              run(" The Navy's submarine program executive has said roughly half "
                  "the labor hours to build a Virginia-class boat can be done "
                  "outside the prime yard — the planned ramp from about two million "
                  "to five million supplier hours a year. So about 50% of the "
                  "labor hours are movable.")], 0),
            ([run("How much of the build is labor in the first place (we call it L).",
                  style=R_STRONG),
              run(" Congressional Research Service testimony puts shipyard labor at "
                  "roughly 40% of a ship's total cost, and an independent cost "
                  "index puts it in the same 40-to-48% range. Because that 40% is "
                  "measured against the ship's whole price — including the "
                  "government-furnished gear — labor's share of just the Basic "
                  "Construction line is higher. Basic Construction is about 65% of "
                  "total ship cost across the portfolio, so if all of that 40% sat "
                  "inside it labor would be about 61% of Basic Construction — which "
                  "we haircut to about 50% for the submarines and 45% for the "
                  "destroyer.")], 0),
        ]),
        paragraph([
            run("Why this matters: ", style=R_STRONG),
            run("the planned five-million supplier hours are about half the Virginia "
                "labor base, which puts today's roughly two-million supplier hours at "
                "about a fifth of it. That is the capacity-relief story in one line — "
                "supplier labor moving from about 20% toward about 50% of the hours, "
                "a jump of roughly two-and-a-half times."),
        ]),

        _h(2, "The idea in one line: core vs. ceiling"),
        paragraph(
            "Picture the Basic Construction build as a whole. Part of it is work "
            "that has to stay in the prime yard no matter what — final assembly, "
            "integration, and test. Call that the core. The ceiling is simply "
            "everything that is not core:"),
        *_list([
            ([run("Core", style=R_STRONG),
              run(" = the labor share that stays put = "),
              run("labor share × the part of labor that cannot leave",
                  style=R_STRONG),
              run(".")], 0),
            ([run("Ceiling", style=R_STRONG),
              run(" = everything else = "),
              run("100% minus the core", style=R_STRONG),
              run(".")], 0),
        ]),
        paragraph(
            "That is the entire model. Two sourced numbers go in; a core and a "
            "ceiling come out, for each ship class and for the portfolio as a "
            "whole."),

        _h(2, "From hours to dollars"),
        paragraph(
            "The two numbers above are about hours, but the answer people want is "
            "in dollars. The bridge adds the materials side back in. Outsourced "
            "dollars are the sum of two flows:"),
        *_olist([
            "The prime-yard labor that relocates to suppliers — the movable hours "
            "turned into dollars.",
            "The parts and materials bought from outside — a share of the "
            "non-labor half of the build, set by how much of that material is "
            "genuinely up for grabs rather than locked to a single source.",
        ]),
        paragraph(
            "That second flow is a dial. Turned all the way up — every outsourced "
            "package carrying its own material — it gives the headline ceiling, "
            "about three-quarters of the build. Turned off, it gives the labor-only "
            "reading, about a quarter. The working case sets it about halfway, which "
            "lands the outsourced share near half of Basic Construction. The ceiling "
            "on this page is the dial-all-the-way-up number, because for sizing a "
            "supplier opportunity the bought-in material is part of the prize."),
        paragraph([
            run("Put precisely, that dial — call it ", style=None),
            run("p", style=R_STRONG),
            run(", the share of an outsourced package's material that travels out "
                "with the work — gives three reads of the same build, not one:"),
        ]),
        *_list([
            ([run("Labor-only (p = 0). ", style=R_STRONG),
              run("Only the movable labor counts, so the outsourced share is "
                  "h × L — about a quarter of Basic Construction.")], 0),
            ([run("Selected case (p ≈ 50%). ", style=R_STRONG),
              run("The packages also carry about half of their own material, so "
                  "the share is h × L + p × (1 - L) — about half the build.")], 0),
            ([run("Structural ceiling (p = 100%). ", style=R_STRONG),
              run("The packages carry all of their non-labor content, so the share "
                  "is 1 - L × (1 - h) — the headline ceiling, about "
                  "three-quarters.")], 0),
        ]),
        paragraph(
            "The reason 50% of movable hours does not mean 50% of dollars is in "
            "that second term: hours and materials enter the total separately, so "
            "the dollar share tracks p, not the hours figure alone. Either way, the "
            "ceiling on this page is the p = 100% upper bound, while the p ≈ 50% "
            "selected case is the more conservative working number."),

        _h(2, "What we found"),
        paragraph(
            "Run the two sourced numbers through the model and the ceiling lands "
            "near three-quarters of Basic Construction on every program — roughly "
            "three times today's outsourced share, with the selected working case "
            "near half:"),
        paragraph([run("Table 1. The core, the selected case, and the ceiling, "
                       "by program", color=BLACK)],
                  style=P_CAPTION, keep_next=True),
        _rule_table(RESULT_HEADERS, RESULT_ROWS),
        paragraph([
            run("The punchline: ", style=R_STRONG),
            run("the nuclear submarines carry the bigger must-stay core (25% vs. "
                "the destroyer's 20%) — the nuclear integration and test work keeps "
                "more locked inside the yard — yet even they could roughly double "
                "or triple what they outsource today."),
        ]),

        _h(2, "Where the numbers come from"),
        paragraph(
            "Only a handful of figures drive the whole estimate, and each traces "
            "to a named, public source. The rest of the workbook is arithmetic on "
            "top of these:"),
        paragraph([run("Table 2. The sourced inputs, and where each comes from",
                       color=BLACK)], style=P_CAPTION, keep_next=True),
        _rule_table(SOURCE_HEADERS, SOURCE_ROWS),

        _h(2, "What to be careful about"),
        *_list([
            ([run("The ceiling is an upper bound, not the working case.",
                  style=R_STRONG)], 0),
            ("The p = 100% ceiling assumes every outsourced package carries its "
             "full non-labor content. The selected p = 50% case in Table 1 is the "
             "more conservative working read — closer to half of Basic "
             "Construction.", 1),
            ([run("The destroyer's two numbers are analyst judgment.",
                  style=R_STRONG)], 0),
            ("There is no surface-ship equivalent of the submarine "
             "half-the-hours figure, so we set the destroyer's movable-hours and "
             "labor shares by reasoning (no reactor, so a smaller locked core) "
             "rather than a direct quote. They are meant to be adjusted.", 1),
            ([run("The 40% labor figure is of the whole ship, not just the build.",
                  style=R_STRONG)], 0),
            ("Re-basing it onto just the Basic Construction line is a judgment "
             "call (we used about 50% for subs, 45% for the destroyer), so the "
             "workbook lets you sweep it.", 1),
            ([run("The dollars are illustrative; the shares are the answer.",
                  style=R_STRONG)], 0),
            ("Figures are in as-reported (then-year) dollars to show magnitude. "
             "The ratios — core, ceiling, and the multiple over today — are what "
             "the analysis stands on, and they do not depend on the dollar year.", 1),
        ]),

        paragraph([run(
            "Plain-language companion to the Outsourcing Ceiling workbook. Basis: "
            "FY22-27 Basic Construction for Virginia / Columbia / DDG-51, with the "
            "movable-hours and labor-share inputs sourced as above; exact figures, "
            "thresholds, and the live controls live in the workbook.",
            color=BLACK)], style=P_SOURCE),
    ]


def render() -> PageModuleSpec:
    return PageModuleSpec(body=_body(), page_setup=PAGE_SETUP, title=PAGE_TITLE)
