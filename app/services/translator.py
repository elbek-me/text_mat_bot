"""Tarjima xizmati (deep-translator, Google Translate)."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from deep_translator import GoogleTranslator

from app.services.errors import ServiceError

logger = logging.getLogger(__name__)

_TIMEOUT = 30.0


@dataclass(frozen=True)
class Language:
    code: str
    label: str


LANGUAGES: dict[str, Language] = {
    lang.code: lang
    for lang in (
        Language("uz", "🇺🇿 O'zbekcha"),
        Language("en", "🇬🇧 Inglizcha"),
        Language("ru", "🇷🇺 Ruscha"),
        Language("tr", "🇹🇷 Turkcha"),
        Language("ar", "🇸🇦 Arabcha"),
        Language("ko", "🇰🇷 Koreyscha"),
        Language("de", "🇩🇪 Nemischa"),
        Language("fr", "🇫🇷 Fransuzcha"),
        Language("zh-CN", "🇨🇳 Xitoycha"),
        Language("es", "🇪🇸 Ispancha"),
    )
}


def _translate_sync(text: str, target: str) -> str:
    return GoogleTranslator(source="auto", target=target).translate(text)


async def translate(text: str, target: str) -> str:
    try:
        result = await asyncio.wait_for(asyncio.to_thread(_translate_sync, text, target), _TIMEOUT)
    except Exception as exc:
        logger.warning("Tarjima xatoligi: %r", exc)
        raise ServiceError("Tarjima qilib bo'lmadi. Keyinroq urinib ko'ring.") from exc
    if not result:
        raise ServiceError("Tarjima natijasi bo'sh. Boshqa matn bilan urinib ko'ring.")
    return result
