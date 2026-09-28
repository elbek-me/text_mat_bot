import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject

from app import texts


class ThrottlingMiddleware(BaseMiddleware):
    """Bir foydalanuvchining juda tez-tez so'rov yuborishini cheklaydi."""

    def __init__(self, delay: float) -> None:
        self.delay = delay
        self._last_seen: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is not None and self.delay > 0:
            now = time.monotonic()
            if now - self._last_seen.get(user.id, 0.0) < self.delay:
                if isinstance(event, CallbackQuery):
                    await event.answer(texts.SLOW_DOWN)
                return None
            self._last_seen[user.id] = now
            if len(self._last_seen) > 5000:
                self._cleanup(now)
        return await handler(event, data)

    def _cleanup(self, now: float) -> None:
        self._last_seen = {uid: t for uid, t in self._last_seen.items() if now - t < 60}
