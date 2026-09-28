"""Matnni ovozga aylantirish (edge-tts)."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

import edge_tts
from edge_tts.exceptions import NoAudioReceived

from app.services.errors import ServiceError

logger = logging.getLogger(__name__)

_tts_semaphore = asyncio.Semaphore(5)
_TIMEOUT = 60.0
_ATTEMPTS = 2


@dataclass(frozen=True)
class Voice:
    key: str
    title: str
    name: str
    pitch: str = "+0Hz"
    rate: str = "+0%"


VOICES: dict[str, Voice] = {
    v.key: v
    for v in (
        Voice("girl", "Qiz bola 👧", "uz-UZ-MadinaNeural", pitch="+12Hz"),
        Voice("boy", "O'g'il bola 👦", "uz-UZ-SardorNeural", pitch="+25Hz", rate="+5%"),
        Voice("deep", "Yo'g'on ovoz 🧔", "uz-UZ-SardorNeural", pitch="-35Hz", rate="-10%"),
        Voice("indian", "Hind ovozi 🇮🇳", "en-IN-NeerjaNeural"),
    )
}


async def _synthesize_once(text: str, voice: Voice) -> bytes:
    communicate = edge_tts.Communicate(text, voice.name, rate=voice.rate, pitch=voice.pitch)
    buf = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.extend(chunk["data"])
    return bytes(buf)


async def synthesize(text: str, voice: Voice) -> bytes:
    async with _tts_semaphore:
        last_exc: Exception | None = None
        for attempt in range(1, _ATTEMPTS + 1):
            try:
                audio = await asyncio.wait_for(_synthesize_once(text, voice), _TIMEOUT)
                if audio:
                    return audio
            except NoAudioReceived as exc:
                raise ServiceError("Bu matnni ovozga aylantirib bo'lmadi.") from exc
            except Exception as exc:  # tarmoq xatolari va timeout
                last_exc = exc
                logger.warning("TTS urinish %s/%s muvaffaqiyatsiz: %r", attempt, _ATTEMPTS, exc)
                await asyncio.sleep(1)
        logger.error("TTS xatolik: %r", last_exc)
        raise ServiceError("Ovoz tayyorlab bo'lmadi. Keyinroq urinib ko'ring.")
