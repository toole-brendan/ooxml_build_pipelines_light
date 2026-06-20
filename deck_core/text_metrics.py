"""Deterministic text / table-row sizing for hand-built slides.

Native PowerPoint tables do NOT autofit, and `<a:tr h="…">` is only a MINIMUM
row height: a cell whose wrapped text needs more vertical space makes the row
grow at render time. So a single scalar row height produces ragged rows and a
graphic-frame whose authored `cy` understates the real table height — which an
AI agent (who cannot see the render) has no way to notice.

This module is the pre-made tool that closes that gap: estimate how many lines
each cell wraps to, size each row to its tallest cell, and hand back explicit
per-row heights the agent passes straight into `house_table(row_h=[…])`. The author
stays in control of the numbers; nothing is auto-resized behind their back.

The character-width model (`AVG_CHAR_WIDTH_RATIO` + greedy word wrap) is the
same one `slide_probe.py --text-estimate` uses, so the probe report and
this estimator always agree. Estimates are intentionally slightly generous
(see `LINE_HEIGHT_FACTOR`) — better a hair tall than clipped.

Units: font sizes are in POINTS (e.g. 10.0). Note `house_table`'s `size=` argument
is the OOXML hundredths-of-a-point form (sz="1000" == 10pt), so a row-height call
uses `size_pt=10.0` while the matching `house_table(..., size=DENSE_BODY_10PT)` uses
1000. Dense tables may still pass a smaller size (size_pt=9.5 or 8.5) explicitly.
"""
from __future__ import annotations

EMU_PER_INCH = 914_400
EMU_PER_POINT = 12_700

# Arial approximate average-char-width / font-size. Matches slide_probe.
AVG_CHAR_WIDTH_RATIO = 0.50
# Rendered line pitch / font size for Arial single spacing (glyph box + leading).
# Keeps row estimates a touch generous so wrapped text is never clipped.
LINE_HEIGHT_FACTOR = 1.2
# House table-cell vertical inset (top AND bottom) — matches the canonical
# house_table cell inset. A row must clear its text plus this padding top and bottom.
DEFAULT_CELL_INSET_V = 45_720   # 0.05 in
DEFAULT_CELL_INSET_H = 45_720   # 0.05 in
# Floor so a one-line row still reads with breathing room (~0.3 in).
DEFAULT_MIN_ROW_H = 274_320


def avg_char_width_emu(size_pt: float) -> float:
    """Approximate average Arial glyph advance at `size_pt`, in EMU."""
    return size_pt * AVG_CHAR_WIDTH_RATIO * EMU_PER_POINT


def line_height_emu(size_pt: float) -> int:
    """Rendered single-spaced line pitch at `size_pt`, in EMU."""
    return int(size_pt * LINE_HEIGHT_FACTOR * EMU_PER_POINT)


def greedy_wrap(text: str, avail_w_emu: float, avg_char_w_emu: float) -> list[str]:
    """Greedy word wrap by character count — the shared slide_probe model.
    Returns the list of lines `text` occupies in `avail_w_emu` of width."""
    if not text:
        return [""]
    if avg_char_w_emu <= 0:
        return [text]
    words = text.split()
    if not words:
        return [""]
    max_chars = max(1, int(avail_w_emu / avg_char_w_emu))
    lines: list[str] = []
    current: list[str] = []
    cur_len = 0
    for w in words:
        wlen = len(w)
        if not current:
            current = [w]
            cur_len = wlen
            continue
        if cur_len + 1 + wlen <= max_chars:
            current.append(w)
            cur_len += 1 + wlen
        else:
            lines.append(" ".join(current))
            current = [w]
            cur_len = wlen
    if current:
        lines.append(" ".join(current))
    return lines


def wrapped_line_count(text: str, usable_width_emu: float, *, size_pt: float) -> int:
    """Number of lines `text` wraps to in `usable_width_emu` at `size_pt`
    (usable width = column width minus left+right insets). Minimum 1."""
    if usable_width_emu <= 0:
        return 1
    return max(1, len(greedy_wrap(str(text), usable_width_emu,
                                  avg_char_width_emu(size_pt))))


def estimate_row_heights(
    rows: list[list[str]],
    col_w: list[int],
    *,
    size_pt: float = 10.0,
    header_size_pt: float | None = None,
    inset_v: int = DEFAULT_CELL_INSET_V,
    inset_h: int = DEFAULT_CELL_INSET_H,
    min_row_h: int = DEFAULT_MIN_ROW_H,
) -> list[int]:
    """Per-row EMU heights sized so every cell's wrapped text fits.

    rows[0] is the header (uses `header_size_pt`, default = `size_pt`). For each
    row the height is `max(min_row_h, max_cell_lines * line_pitch + 2*inset_v)`,
    where a cell's usable text width is its column width minus `2*inset_h`.

    Pass the result straight to the canonical `house_table(..., row_h=[…])`; the
    table's frame height is then `sum(...)`, so authored geometry matches the
    render. `size_pt` here mirrors `house_table`'s `size` (sz="1000" -> size_pt=10.0).
    """
    if any(len(r) != len(col_w) for r in rows):
        raise ValueError(
            f"every row must have {len(col_w)} cells (got widths "
            f"{[len(r) for r in rows]})"
        )
    header_size_pt = header_size_pt if header_size_pt is not None else size_pt
    heights: list[int] = []
    for ri, row in enumerate(rows):
        sz = header_size_pt if ri == 0 else size_pt
        max_lines = 1
        for ci, cell in enumerate(row):
            usable = col_w[ci] - 2 * inset_h
            max_lines = max(max_lines, wrapped_line_count(cell, usable, size_pt=sz))
        heights.append(max(min_row_h, max_lines * line_height_emu(sz) + 2 * inset_v))
    return heights


def table_height(rows: list[list[str]], col_w: list[int], **kw) -> int:
    """Honest total table height in EMU = sum of `estimate_row_heights(...)`."""
    return sum(estimate_row_heights(rows, col_w, **kw))
