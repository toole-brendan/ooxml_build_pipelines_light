"""Sourcing-Openings Explainer - plain-language guide to the re-buy signal.

INTENT
    A from-the-top, plain-English explainer of how the analysis finds re-buy
    openings, written for a reader who has never seen the workbook. It opens with
    the basic context — a "jump ball" is a contestable sourcing opening, and the
    analysis screens for three kinds — then focuses on one: the re-buy bucket.
    "Re-buy" now has two subtypes, and the page keeps them distinct throughout:
    PERIODIC lanes buy in clear cycles, so we can estimate a dated next sourcing
    window; CONTINUOUS lanes buy almost non-stop, so the opening is active,
    already-shared supplier access rather than a date. It builds from the basics
    (what a "supplier lane" is) to the shared test, the periodic-vs-continuous
    gate, the next-buy window, whether the waves are the same recurring package,
    and what (if anything) a wave is tied to in the production cycle. Prose-first
    (headings + body + lists + two at-a-glance tables), not a slide mock - so it
    reads as a normal Word document page in portrait. Deliberately NO workbook
    mechanics (dynamic arrays / spills / formulas / XML) - that belongs in build
    notes, not the methodology explainer.

OUTLINE (source-only; not emitted)
    - H1   How We Spot Re-Buy Openings
    - lead what this page is (jump-ball framing + the periodic/continuous split)
    - H2   Three kinds of sourcing opening   <- names all three, points to re-buy
    - H2   Start with the basics: what is a supplier lane?
    - H2   What we look at inside a lane
    - H2   The re-buy idea, in one sentence
    - H2   First test: is the work actually shared?
    - H2   Is the lane even on a rhythm? Periodic vs. continuous   <- the gate
    - H2   When does a periodic lane come up again? The next sourcing window
    - H2   Is it the same kind of buy each time?   <- wave-quality / same-package
    - H2   Can we tell what the wave is tied to?   <- production-cycle confidence
    - H2   Two honest limits
    - Table 1  the sourcing read at a glance
    - H2   What the analysis reads from the data (data fidelity + Table 2)
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

PAGE_TITLE = "Sourcing-Openings Methodology - plain-language explainer"

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


def _body() -> list[str]:
    return [
        _h(1, "How We Spot Re-Buy Openings"),
        paragraph([
            run("In plain terms: ", style=R_STRONG),
            run("a re-buy opening is outsourced work a shipbuilder already buys "
                "from suppliers that may be open to a new entrant. It is one of a "
                "few kinds of contestable sourcing opening — what we loosely call "
                "a “jump ball” — that the analysis screens for. The re-buy idea "
                "splits into two cases: some lanes buy in clear cycles, so we can "
                "estimate a dated periodic sourcing window; others buy almost "
                "continuously, so the opportunity is not a date but an active, "
                "already-shared supplier stream. This page names the three kinds "
                "of opening, then focuses on this one and builds up to both "
                "cases."),
        ]),

        _h(2, "Three kinds of sourcing opening"),
        paragraph(
            "A jump ball is simply a piece of outsourced work a new supplier "
            "could realistically compete for. The analysis looks for three "
            "kinds, each a different shape of opening:"),
        *_list([
            ([run("Periodic / continuous sourcing", style=R_STRONG),
              run(" — this page's focus.")], 0),
            ("Work the shipbuilder already buys from outside suppliers. Some of "
             "it comes in repeatable cycles, where we can estimate a next "
             "sourcing window. Some of it is bought continuously, where the "
             "opening is active supplier access rather than a specific date.", 1),
            ([run("Concentration", style=R_STRONG)], 0),
            ("A lane where one supplier holds most of the recent money; the "
             "opening is unseating an entrenched incumbent.", 1),
            ([run("Source diversification", style=R_STRONG)], 0),
            ("A lane that used to have a single supplier where a credible second "
             "source has recently arrived while the first is still active — a "
             "split already in motion.", 1),
        ]),
        paragraph(
            "The rest of this page is about the first kind. Everything below "
            "builds up to it, starting with the basics."),

        _h(2, "Start with the basics: what is a supplier lane?"),
        paragraph(
            "A prime contractor — here, the shipbuilder — does not make "
            "everything itself. It buys parts and work from outside suppliers. "
            "A supplier lane (we just call it a lane) is one slice of that "
            "buying, pinned down by three things:"),
        *_list([
            ([run("Program", style=R_STRONG),
              run(" — which ship the work is for (Virginia, Columbia, or "
                  "DDG-51).")], 0),
            ([run("Contract", style=R_STRONG),
              run(" — the specific prime contract it sits on (its PIID, the "
                  "contract's ID number).")], 0),
            ([run("Work type", style=R_STRONG),
              run(" — the kind of work it is (piping, machining, electrical, "
                  "castings, and so on).")], 0),
        ]),
        paragraph([
            run("So a lane is simply "),
            run("this program, on this contract, for this type of work",
                style=R_STRONG),
            run(" — for example, Virginia / contract N00024…2100 / piping. "
                "Suppliers compete inside a lane, and the lane is the unit "
                "everything else is measured on."),
        ]),

        _h(2, "What we look at inside a lane"),
        paragraph(
            "For each lane we line up every supplier award it has received over "
            "the years — who won work, how much, and when. From that history we "
            "read a few simple things:"),
        *_list([
            ("How many suppliers are winning recent work.", 0),
            ("How much of the recent money the single biggest supplier holds — "
             "its share.", 0),
            ("The dates of the past awards.", 0),
        ]),

        _h(2, "The re-buy idea, in one sentence"),
        paragraph([
            run("A re-buy opening = ", style=R_STRONG),
            run("shared supplier work where either the next periodic buy window "
                "is coming up, or the lane is already buying continuously enough "
                "to be open now.", style=R_STRONG),
        ]),
        paragraph(
            "That gives us two questions: is the lane genuinely shared, and what "
            "kind of buying pattern does it have — periodic or continuous? We "
            "check the sharing first."),

        _h(2, "First test: is the work actually shared?"),
        paragraph(
            "Before timing matters at all, the lane has to be genuinely "
            "competitive. Two things have to be true:"),
        *_list([
            ("There are at least two suppliers winning recent work in the "
             "lane.", 0),
            ("The top supplier does not hold essentially all of the recent "
             "dollars — a meaningful share is spread across the others. We call "
             "that spread the shared % (it is just 100% minus the top supplier's "
             "share).", 0),
        ]),
        paragraph(
            "If one supplier holds almost everything, the lane is not a re-buy "
            "opening — it is a different kind of opportunity (a concentrated "
            "lane, where the prize is unseating an entrenched incumbent). The "
            "shared % is the dial that tells the two apart."),

        _h(2, "Is the lane even on a rhythm? Periodic vs. continuous"),
        paragraph(
            "Grouping awards into waves only helps if the lane actually buys in "
            "discrete bursts separated by quiet stretches. Many lanes do — but a "
            "large share buy almost continuously, a few awards every month for "
            "years. With no real quiet gap, the 90-day grouping strings all that "
            "activity into one long “wave,” and any cadence read off it is an "
            "artifact, not a real cycle. So before estimating any timing, the "
            "analysis asks whether the lane is genuinely periodic. A lane is "
            "treated as periodic only when:"),
        *_list([
            ("It has at least two distinct waves.", 0),
            ("Its longest wave is short relative to a real cycle — by default no "
             "longer than a year.", 0),
            ("That longest wave is no longer than the spacing between waves; a "
             "“wave” that lasts longer than the cadence is really continuous "
             "activity wearing a wave's clothes.", 0),
        ]),
        paragraph(
            "Lanes that fail this test are not discarded — they are usually the "
            "most active, highest-dollar lanes on the program. They are simply a "
            "different kind of opening: an active continuous sourcing lane. The "
            "question is not “when is the next buy?” (the answer is “constantly”) "
            "but “is the shipbuilder still buying this work, is the work already "
            "split, and could another supplier get in?” Those move to a companion "
            "screen — Continuous Sourcing — which reads them on whether the lane "
            "is still actively buying, the supplier split, and vendor turnover "
            "instead of a date."),

        _h(2, "When does a periodic lane come up again? The next sourcing window"),
        paragraph(
            "For the lanes that are genuinely periodic, we estimate the next buy "
            "from the lane's own rhythm of past awards — not the Navy's contract "
            "schedule. Step by step:"),
        *_olist([
            "List the dates the lane received supplier awards.",
            "Group nearby dates into a single buy wave — awards within about 90 "
            "days of each other count as one event, so a flurry of related "
            "paperwork is not mistaken for many separate buys.",
            "Measure the quiet gap between the end of one wave and the start of "
            "the next, and the typical length of a wave.",
            "Project the next buy as a window: after the last observed award "
            "activity, the model adds a typical quiet gap, then gives the next "
            "wave a typical wave length.",
        ]),
        paragraph([
            run("Why a window, not a single date: ", style=R_STRONG),
            run("a re-buy is itself a burst of awards spread over weeks or months, "
                "not a one-day event. Forecasting the interval the next burst is "
                "likely to fall in is both more honest and far less sensitive to "
                "exactly which past award we anchor on."),
        ]),
        paragraph(
            "A lane needs at least two buy waves for this to work — one wave gives "
            "a date but no spacing. Note too that the cadence reads the lane's "
            "whole award history, while the shared test earlier looks only at "
            "recent money — a periodic lane has to pass both."),
        paragraph(
            "The final “periodic opening due” flag simply asks whether that "
            "projected window overlaps a chosen horizon. By default the horizon "
            "is the twelve months following the as-of date (here, 2026-05-22), "
            "not a moving “today,” so the flag reads the same every time the "
            "workbook is opened — but the workbook can change that horizon. The "
            "horizon length, the periodic-vs-continuous thresholds, and the "
            "shared-test cutoffs are all adjustable controls."),

        _h(2, "Is it the same kind of buy each time?"),
        paragraph(
            "Timing alone is not enough. A lane can have a repeated rhythm but "
            "still be buying different things each time. So the analysis also "
            "checks whether the past waves look similar. It asks:"),
        *_list([
            ("Do the same suppliers show up from one wave to the next?", 0),
            ("Is the dollar split among suppliers similar each time?", 0),
            ("Does the same kind of capability show up in the waves?", 0),
            ("Does the wave count stay roughly the same if the grouping window is "
             "loosened or tightened?", 0),
        ]),
        paragraph(
            "A lane with similar suppliers, similar dollar splits, and similar "
            "capabilities is a cleaner recurring sourcing pattern. A lane where "
            "every wave has a different supplier mix or different capability mix "
            "is still worth watching, but the timing read is less specific."),

        _h(2, "Can we tell what the wave is tied to?"),
        paragraph(
            "Sometimes, but only carefully. The analysis looks for clues: the "
            "lane's work type, the finer capability tags on its suppliers, "
            "whether the same capability repeats across waves, and whether a wave "
            "tends to sit near a prime-contract action. Those clues can suggest a "
            "wave is tied to a recurring package of work. But this is a "
            "confidence read, not a hard label. If the text is vague or the "
            "supplier mix changes a lot, the model should not pretend it knows "
            "the exact part of the ship."),

        _h(2, "Two honest limits"),
        *_list([
            ([run("Timing follows the supplier rhythm, not the Navy's "
                  "prime-contract schedule.", style=R_STRONG)], 0),
            ("We tested whether supplier re-buys line up with the big prime / "
             "block awards and found they do not line up cleanly, so the prime "
             "schedule is shown only as context.", 1),
            ([run("The shared test reads on dollar share, not a head-count of "
                  "suppliers.", style=R_STRONG)], 0),
            ("A lane with five suppliers where one holds 95% still counts as "
             "concentrated, not shared.", 1),
        ]),

        # Caption with a black run override (the Caption style is GRAY_4 italic);
        # built here so table_block emits the table only.
        paragraph([run("Table 1. The sourcing read at a glance", color=BLACK)],
                  style=P_CAPTION, keep_next=True),
        _rule_table(
            ["Piece", "Plain meaning", "Where it comes from"],
            [
                ["Recent active suppliers",
                 "How many real suppliers compete in the lane",
                 "Count of suppliers with recent awards"],
                ["Shared dollar %",
                 "How much of the recent money is spread beyond the top supplier",
                 "100% minus the top supplier's share"],
                ["Sourcing mode",
                 "Whether the lane buys in discrete cycles or continuously",
                 "Read from the wave shape — wave count and longest wave length"],
                ["Award-wave cadence",
                 "A periodic lane's typical spacing between buy waves",
                 "Median gap between past award waves"],
                ["Next periodic sourcing window",
                 "The interval the next buy is likely to fall in",
                 "Last award plus a typical quiet gap, running one typical wave long"],
                ["Periodic opening due",
                 "Whether that window lands soon (periodic lanes only)",
                 "The next-buy window overlaps the horizon after the as-of date"],
                ["Active continuous sourcing opening",
                 "A continuously-bought, already-shared lane to pursue now",
                 "Continuous lane that is still buying recently, has material "
                 "spend, and is not dominated by one supplier (Continuous Sourcing)"],
            ],
        ),

        _h(2, "What the analysis reads from the data"),
        paragraph(
            "Each subaward filing is rich — dozens of fields covering the "
            "supplier, the dollars, the dates, and the parent contract. The "
            "re-buy read leans on only a few of them, and the ones it uses are "
            "well populated:"),
        paragraph([run("Table 2. What the read uses, and how complete it is",
                       color=BLACK)], style=P_CAPTION, keep_next=True),
        _rule_table(
            ["What we read", "What it feeds", "How complete"],
            [
                ["Award date",
                 "Whether an award is recent, and the cadence between buy waves",
                 "On every record"],
                ["Award amount",
                 "Recent dollars and the shared % (top supplier vs. the rest)",
                 "On essentially every record; a few downward corrections are "
                 "netted out"],
                ["Supplier identity",
                 "Who is winning work, the supplier count, and each one's share",
                 "On every record; rolled up to the corporate parent about "
                 "two-thirds of the time"],
                ["Work type",
                 "Which lane the award belongs to",
                 "Set from the supplier's business classification, not the "
                 "award's text"],
                ["Capability tag",
                 "A finer read of what a supplier does, inside a lane",
                 "On about two-thirds of records — a secondary detail, not the "
                 "core signal"],
                ["Award-wave shape",
                 "Periodic vs. continuous classification",
                 "Derived from award dates; stronger when there are several waves"],
                ["Supplier mix by wave",
                 "Whether the same suppliers and dollar split recur",
                 "Derived from supplier identity and award dollars"],
                ["Prime-contract dates",
                 "Context only — not the timing clock",
                 "Available for in-scope PIIDs, but not used as the primary "
                 "timing driver"],
            ],
        ),
        paragraph(
            "The data also carries a free-text description on each line, which "
            "might look like the obvious way to label the kind of work. We do not "
            "use it for that, because it is unreliable."),
        paragraph(
            "On submarine records about three-quarters of those descriptions just "
            "say “see below” or “see remarks,” which point to the report's other "
            "free-text field. Follow the pointer and you usually land not on a "
            "part but on which boat or build year the line sits on (“SSN 792 "
            "construction”), or what kind of administrative change it was (a "
            "billing revision, a subcontracting-plan update) — only occasionally "
            "on the actual component. On DDG records the description is mostly "
            "internal shipyard job codes. Either way it is a contract- or "
            "action-level label repeated across many lines, so we read the kind "
            "of work from the supplier instead."),

        paragraph([run(
            "Plain-language companion to the Award Analysis workbook (Periodic "
            "Sourcing + Continuous Sourcing screens). Basis: FSRS supplier-role "
            "subaward records for Virginia / Columbia / DDG-51, as of 2026-05-22; "
            "exact figures, thresholds, and the live controls live in the "
            "workbook.",
            color=BLACK)], style=P_SOURCE),
    ]


def render() -> PageModuleSpec:
    return PageModuleSpec(body=_body(), page_setup=PAGE_SETUP, title=PAGE_TITLE)
