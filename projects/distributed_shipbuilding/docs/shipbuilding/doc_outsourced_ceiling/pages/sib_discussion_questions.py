"""SIB Slack handoff - two ready-to-send Slack drafts + the SIB question set.

INTENT
    A copy-ready draft of the two Slack messages around the SIB handoff: (1) a
    short 1:1 reply to Danielle (DR) agreeing to move the sync to Friday and
    flagging that the questions will land in a separate channel, and (2) the
    message for the new channel (Danielle + JM) - a light intro followed by the
    question set we'd like her to raise with SIB. Plain-English; the questions are
    organized by topic (A-D) with continuously numbered questions (1-6) so the
    topic labels never collide with the question numbers. The two H1s are draft
    labels for the reader, not text to paste.

OUTLINE (source-only; not emitted)
    - H1   Message 1 - direct reply to Danielle (reschedule to Friday)
    - body two short lines (warm thanks + heads-up on the separate channel)
    - H1   Message 2 - new channel (Danielle + JM)
    - lead light intro ("cover a few of these, no pressure")
    - H2  A. Outsourcing ceiling and ramp              <- Q1-Q2 (Q2 sub-bullet: ramp constraints)
    - H2  B. Components, systems, and modules          <- Q3 (sub-bullet: new-entrant fit)
    - H2  C. Electric Boat and Newport News workshare  <- Q4-Q5 (Q5 sub-bullet: data caveat)
    - H2  D. Turning work into dollars                 <- Q6 (sub-bullet: benchmarks / data sources)

LOCAL OVERRIDES (inline only; no core edits)
    - No blue font: headings (the named style is BLUE_5) get a run-level BLACK
      override; the hierarchy is carried instead by a thin gray bottom rule under
      H1/H2 (_HRULE) plus the size ramp.
    - Numbered questions are drawn inline (_qlist), not Word's numbering.xml, so
      the count continues across topic sections (1..8) and the marker geometry +
      after-block breather match the house list look.
    - 0.75in left/right margins via a local PageSetup (top/bottom stay 1in).
"""
from __future__ import annotations

from docx_core.primitives import paragraph, run
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PageSetup
from docx_core.rhythm import PageMargins
from docx_core.style import BLACK
from docx_core.style_ids import P_LIST, P_H1, P_H2, P_H3

PAGE_TITLE = "SIB Slack handoff (messages + questions)"

# 0.75in left/right margins (top/bottom stay at the 1in report default). Inline,
# so docx_core's shared presets are untouched.
PAGE_SETUP = PageSetup(margins=PageMargins(left_in=0.75, right_in=0.75))

_HSTYLE = {1: P_H1, 2: P_H2, 3: P_H3}

# Thin gray bottom rule under H1/H2 so sections separate cleanly WITHOUT color
# (the named heading style is blue, but the house ask is no blue font at all). H1
# gets a heavier/darker rule than H2. sz is in eighths of a point.
_HRULE = {
    1: '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="2" w:color="7F7F7F"/></w:pBdr>',
    2: '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="BFBFBF"/></w:pBdr>',
}


def _h(level: int, text: str) -> str:
    """Heading: black run override (no blue, per the house ask - the named style is
    blue) plus a thin gray bottom rule under H1/H2, so the hierarchy reads through a
    divider + the size ramp rather than color."""
    return paragraph([run(text, color=BLACK)], style=_HSTYLE[level],
                     raw_ppr_extra=_HRULE.get(level, ""))


# --- inline numbered questions + sub-bullets (core's numbering.xml untouched) --
# Numbers are drawn by hand so the count continues across topic sections (Q1..Q8)
# rather than restarting per list. Each question is a hanging-indent paragraph
# (number run + <w:tab/>, so wrapped lines align under the text). A question may
# carry sub-bullets (•) one level in - for its context note, or to split a
# multi-part ask into readable pieces. Spacing stays tight between a question and
# its sub-bullets, with the wider breather only after a section's last paragraph.
_LIST_LEFT = 720          # question text indent, twips (0.5in)
_LIST_HANG = 360          # number hangs back 0.25in
_SUB_LEFT = 1080          # sub-bullet text indent (0.75in); glyph sits at 0.5in
_SUB_HANG = 360
_TIGHT = 40               # ~2pt: question-to-sub-bullet, and between sub-bullets
_LIST_AFTER = 80          # ~4pt between questions
_LIST_AFTER_LAST = 160    # ~8pt breather after a section's last paragraph


def _q_para(number: int, content, after: int) -> str:
    ppr = (f'<w:tabs><w:tab w:val="left" w:pos="{_LIST_LEFT}"/></w:tabs>'
           f'<w:spacing w:after="{after}" w:line="240" w:lineRule="auto"/>'
           f'<w:ind w:left="{_LIST_LEFT}" w:hanging="{_LIST_HANG}"/>')
    runs = [f'<w:r><w:t xml:space="preserve">{number}.</w:t><w:tab/></w:r>']
    runs += list(content) if isinstance(content, list) else [run(content)]
    return paragraph(runs, style=P_LIST, raw_ppr_extra=ppr)


def _sub_para(content, after: int) -> str:
    ppr = (f'<w:tabs><w:tab w:val="left" w:pos="{_SUB_LEFT}"/></w:tabs>'
           f'<w:spacing w:after="{after}" w:line="240" w:lineRule="auto"/>'
           f'<w:ind w:left="{_SUB_LEFT}" w:hanging="{_SUB_HANG}"/>')
    runs = ['<w:r><w:t xml:space="preserve">&#x2022;</w:t><w:tab/></w:r>']
    runs += list(content) if isinstance(content, list) else [run(content)]
    return paragraph(runs, style=P_LIST, raw_ppr_extra=ppr)


def _qlist(items, start: int) -> list[str]:
    """Numbered questions starting at `start`. Each item is either the question
    content (a plain string or a list of run() strings) or a (content, [subs])
    tuple whose sub-bullets render one level in; each sub is itself a plain
    string or a list of run() strings. The section's last paragraph gets the
    wider after-block breather; everything else stays tight."""
    out: list[str] = []
    n = len(items)
    for i, item in enumerate(items):
        last_q = i == n - 1
        content, subs = item if isinstance(item, tuple) else (item, [])
        out.append(_q_para(start + i, content,
                           _TIGHT if subs
                           else (_LIST_AFTER_LAST if last_q else _LIST_AFTER)))
        for j, sub in enumerate(subs):
            last_sub = j == len(subs) - 1
            out.append(_sub_para(
                sub,
                (_LIST_AFTER_LAST if last_q else _LIST_AFTER) if last_sub
                else _TIGHT))
    return out


def _body() -> list[str]:
    return [
        # ---- Message 1: direct reply to Danielle (reschedule) -------------
        _h(1, "Message 1: direct reply to Danielle (reschedule)"),
        paragraph(
            "Wow, thank you Danielle! Hope you guys had a great weekend too!"),
        paragraph(
            "Yes, Friday works! And that's awesome you're seeing SIB Thursday. JM "
            "asked me to send a few questions/topics to raise with SIB if there's "
            "time, so I'll send them over in the other channel now!"),

        # ---- Message 2: new channel (you, Danielle, JM) -------------------
        _h(1, "Message 2: new channel with Danielle and JM (SIB questions)"),
        paragraph(
            "Hey Danielle, JM and I were hoping you might be able to cover a few of "
            "these points in your SIB meeting on Thursday. No pressure if you're "
            "not able to, but any insight would be a big help. Looking forward to "
            "our sync on Friday!"),

        _h(2, "A. Outsourcing ceiling and ramp"),
        *_qlist([
            "We assume most new-construction work could be outsourced except "
            "final assembly, integration, test, and anything that must stay in "
            "the nuclear-qualified yards. Is that a fair assumption?",
            ("Are you seeing a surge of interest in outsourced work on your end? "
             "If so, how fast could it expand, and roughly where is it now, in 3 "
             "to 5 years, and at the ceiling?",
             ["What most constrains the ramp: trained labor, facilities, "
              "nuclear quality, design maturity, or the primes' capacity to "
              "manage more suppliers?"]),
        ], start=1),

        _h(2, "B. Components, systems, and modules"),
        *_qlist([
            ("Is \"component vs. module\" the right way to slice outsourced "
             "work, or does the industry use a more granular, standard breakdown "
             "(kits, parts/equipment, systems/shipsets, structural/outfitted "
             "modules)?",
             ["Which types can new entrants realistically take on?"]),
        ], start=3),

        _h(2, "C. Electric Boat and Newport News workshare"),
        *_qlist([
            "What's the most accurate way to describe Newport News on Virginia "
            "and Columbia: co-builder, co-prime, or major subcontractor to "
            "Electric Boat? Does it differ by class?",
            ("Roughly how is the build split between EB and Newport News (% of "
             "cost or hours), and how much does NNS subcontract down to outside "
             "suppliers?",
             [[run("Context for Danielle: NNS's subawards are completely absent "
                   "from our data pulls, and we're trying to understand why.",
                   italic=True)]]),
        ], start=4),

        _h(2, "D. Turning work into dollars"),
        *_qlist([
            ("Is the roughly 40% shipyard-labor share of construction cost "
             "about right, and what makes up the rest (material, "
             "vendor-furnished equipment, overhead)?",
             ["Does SIB maintain (or know who does) benchmarks for outsourced "
              "hours, supplier capacity targets, or qualification timelines by "
              "work type?"]),
        ], start=6),
    ]


def render() -> PageModuleSpec:
    return PageModuleSpec(body=_body(), page_setup=PAGE_SETUP, title=PAGE_TITLE)
