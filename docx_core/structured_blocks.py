"""docx_core.structured_blocks - generic structured-document writing blocks.

The recommended style for structured documents - build registers, requirement
lists, definition sheets, field/value forms - WITHOUT committing to any specific
template vocabulary. These are conveniences over primitives + the structured
paragraph styles (P_BLOCK_HEADING / P_FIELD_LABEL / P_COMPACT_BODY); an author may
always compose primitives directly when that reads better.

Each builder returns a LIST of block XML strings, so a page module splices them
into its body with `*`:

    body = [
        heading(1, "Build register"),
        *card_block("Ingest", ["Pulls the source extracts.", "Owner: data team."]),
        *field_block("Status", "Green"),
    ]

Import direction: primitives / style_ids <- structured_blocks.
"""
from __future__ import annotations

from docx_core.primitives import paragraph, run, bullets
from docx_core.style_ids import (
    P_BLOCK_HEADING, P_FIELD_LABEL, P_COMPACT_BODY, R_STRONG,
)


def _as_lines(value) -> list[str]:
    """Normalize a field to a list of non-empty lines (split a str on newlines;
    pass a list/tuple through, stripping blanks)."""
    items = list(value) if isinstance(value, (list, tuple)) else str(value).split("\n")
    return [s for s in (str(x).strip() for x in items) if s]


def field_block(label: str, value) -> list[str]:
    """A bold field label over its (possibly multi-line) value:

        Purpose
        Allocate portfolio TAM across work-type buckets.

    Empty values render the label only. `value` is a string (newline-split) or a
    list of lines."""
    out = [paragraph(label, style=P_FIELD_LABEL)]
    out.extend(paragraph(ln, style=P_COMPACT_BODY) for ln in _as_lines(value))
    return out


def card_block(title: str, lines=()) -> list[str]:
    """A block heading + compact body lines - a titled card:

        Ingest
        Pulls the source extracts nightly.
        Owner: data team."""
    out = [paragraph(title, style=P_BLOCK_HEADING)]
    out.extend(paragraph(ln, style=P_COMPACT_BODY) for ln in _as_lines(lines))
    return out


def checklist_block(items, *, label: str | None = None) -> list[str]:
    """An optional bold label over a bulleted list (acceptance criteria, checks)."""
    out: list[str] = []
    if label:
        out.append(paragraph(label, style=P_FIELD_LABEL))
    out.extend(bullets(_as_lines(items)))
    return out


def definition_list(pairs) -> list[str]:
    """Inline bold-term + definition lines; each pair is (term, definition):

        Term - definition text."""
    out: list[str] = []
    for term, definition in pairs:
        out.append(paragraph(
            [run(f"{term} ", style=R_STRONG), run(f"- {definition}")],
            style=P_COMPACT_BODY,
        ))
    return out
