from pathlib import Path

import pytest

from app.services.handwriting import (
    NotebookStyle,
    PageLayout,
    _load_font,
    normalize_text,
    render_pages,
    wrap_text,
)

FONT = Path("assets/fonts/handwriting.ttf")


def test_wrap_respects_width_and_splits_long_words():
    font = _load_font(str(FONT), 46)
    width = PageLayout().text_width
    lines = wrap_text("Salom dunyo " * 50 + "x" * 300, font, width)
    assert all(font.getlength(line) <= width for line in lines)


@pytest.mark.parametrize("style", list(NotebookStyle))
def test_render_returns_jpeg(style):
    pages, truncated = render_pages("Salom, o'zbek!\nIkkinchi qator", style, FONT, 10)
    assert len(pages) == 1 and not truncated
    assert pages[0][:2] == b"\xff\xd8"


def test_render_truncates_to_max_pages():
    pages, truncated = render_pages("qator\n" * 500, NotebookStyle.LINED, FONT, 2)
    assert len(pages) == 2 and truncated


def test_normalize_replaces_uzbek_apostrophes():
    assert normalize_text("O\u02bbzbek g\u02bboya") == "O'zbek g'oya"
