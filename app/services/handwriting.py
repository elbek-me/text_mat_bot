"""Matnni qo'lyozma daftar sahifasiga aylantirish (Pillow)."""
from __future__ import annotations

import asyncio
import io
import logging
import random
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.services.errors import ServiceError

logger = logging.getLogger(__name__)

_render_semaphore = asyncio.Semaphore(3)  # bir vaqtda 3 tadan ortiq render qilinmasin


# Shriftda bo'lmasligi mumkin bo'lgan apostrof turlari (o', g' harflari uchun)
_APOSTROPHES = str.maketrans(
    {
        "\u02bb": "'",  # ʻ
        "\u02bc": "'",  # ʼ
        "\u2019": "'",  # ’
        "\u0060": "'",  # `
        "\u00b4": "'",  # ´
    }
)


def normalize_text(text: str) -> str:
    return text.translate(_APOSTROPHES)


class NotebookStyle(str, Enum):
    LINED = "lined"
    GRID = "grid"

    @property
    def title(self) -> str:
        return {
            NotebookStyle.LINED: "📏 Yo'l-yo'l chiziqli daftar",
            NotebookStyle.GRID: "🔲 Katakli (shaxmat) daftar",
        }[self]


@dataclass(frozen=True)
class PageLayout:
    width: int = 1240
    height: int = 1754
    line_height: int = 64
    margin_left: int = 150
    margin_right: int = 80
    margin_top: int = 180
    margin_bottom: int = 100
    font_size: int = 46
    grid_step: int = 32
    paper: tuple[int, int, int] = (253, 253, 248)
    rule_color: tuple[int, int, int] = (170, 200, 230)
    margin_color: tuple[int, int, int] = (230, 120, 120)
    ink: tuple[int, int, int] = (25, 40, 110)

    @property
    def lines_per_page(self) -> int:
        return (self.height - self.margin_top - self.margin_bottom) // self.line_height + 1

    @property
    def text_width(self) -> int:
        return self.width - self.margin_left - self.margin_right


@lru_cache(maxsize=8)
def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (path, "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    logger.warning("Qo'lyozma shrifti topilmadi (%s). Standart shrift ishlatiladi.", path)
    return ImageFont.load_default(size)


def wrap_text(text: str, font, max_width: int) -> list[str]:
    """Matnni piksel kengligiga qarab qatorlarga bo'ladi (uzun so'zlarni ham)."""
    lines: list[str] = []
    for paragraph in text.replace("\r\n", "\n").split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        current = ""
        for word in paragraph.split():
            candidate = f"{current} {word}".strip()
            if font.getlength(candidate) <= max_width:
                current = candidate
                continue
            if current:
                lines.append(current)
                current = ""
            while font.getlength(word) > max_width:
                cut = len(word)
                while cut > 1 and font.getlength(word[:cut]) > max_width:
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            current = word
        lines.append(current)
    return lines


def _draw_paper(draw: ImageDraw.ImageDraw, style: NotebookStyle, lay: PageLayout) -> None:
    if style is NotebookStyle.LINED:
        y = lay.margin_top
        while y < lay.height - 60:
            draw.line([(0, y), (lay.width, y)], fill=lay.rule_color, width=2)
            y += lay.line_height
    else:
        step = lay.grid_step
        for y in range(lay.margin_top % step, lay.height, step):
            draw.line([(0, y), (lay.width, y)], fill=lay.rule_color, width=1)
        for x in range(0, lay.width, step):
            draw.line([(x, 0), (x, lay.height)], fill=lay.rule_color, width=1)
    x = lay.margin_left - 30
    draw.line([(x, 0), (x, lay.height)], fill=lay.margin_color, width=3)


def render_pages(
    text: str,
    style: NotebookStyle,
    font_path: Path,
    max_pages: int,
    layout: PageLayout | None = None,
) -> tuple[list[bytes], bool]:
    """Sahifalar (JPEG baytlar) va matn qisqartirilgani haqida belgini qaytaradi."""
    lay = layout or PageLayout()
    font = _load_font(str(font_path), lay.font_size)
    lines = wrap_text(normalize_text(text), font, lay.text_width)

    per_page = lay.lines_per_page
    pages_lines = [lines[i : i + per_page] for i in range(0, len(lines), per_page)] or [[""]]
    truncated = len(pages_lines) > max_pages
    rng = random.Random()

    result: list[bytes] = []
    for page_lines in pages_lines[:max_pages]:
        img = Image.new("RGB", (lay.width, lay.height), lay.paper)
        draw = ImageDraw.Draw(img)
        _draw_paper(draw, style, lay)
        for i, line in enumerate(page_lines):
            if not line:
                continue
            baseline = lay.margin_top + i * lay.line_height - 8 + rng.randint(-2, 2)
            x = lay.margin_left + rng.randint(-3, 3)
            draw.text((x, baseline), line, font=font, fill=lay.ink, anchor="ls")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=92)
        result.append(buf.getvalue())
    return result, truncated


async def render_pages_async(
    text: str, style: NotebookStyle, font_path: Path, max_pages: int
) -> tuple[list[bytes], bool]:
    async with _render_semaphore:
        try:
            return await asyncio.to_thread(render_pages, text, style, font_path, max_pages)
        except Exception as exc:
            logger.exception("Daftar rasmini yaratishda xatolik")
            raise ServiceError("Rasm yaratib bo'lmadi. Keyinroq urinib ko'ring.") from exc
