import logging

from aiogram import Router
from aiogram.types import ErrorEvent

from app import texts

logger = logging.getLogger(__name__)
router = Router(name="errors")


@router.errors()
async def on_error(event: ErrorEvent) -> bool:
    logger.exception("Ishlanmagan xatolik: %s", event.exception, exc_info=event.exception)
    update = event.update
    try:
        if update.message:
            await update.message.answer(texts.UNEXPECTED_ERROR)
        elif update.callback_query:
            await update.callback_query.answer(texts.UNEXPECTED_ERROR, show_alert=True)
    except Exception:  # foydalanuvchiga xabar yuborib bo'lmasa ham bot ishlashda davom etsin
        logger.debug("Xatolik haqida xabar yuborib bo'lmadi", exc_info=True)
    return True
