import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config import get_settings
from app.handlers import build_root_router
from app.logger import setup_logging
from app.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_dir)

    if not settings.font_path.exists():
        logger.warning(
            "Shrift topilmadi: %s. Oddiy shrift ishlatiladi (assets/fonts/README.md ga qarang).",
            settings.font_path,
        )

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # Production uchun RedisStorage ishlating: aiogram.fsm.storage.redis.RedisStorage
    dp = Dispatcher(storage=MemoryStorage(), settings=settings)

    throttling = ThrottlingMiddleware(settings.throttle_seconds)
    dp.message.outer_middleware(throttling)
    dp.callback_query.outer_middleware(throttling)
    dp.include_router(build_root_router())

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Bosh menyu"),
            BotCommand(command="help", description="Yordam"),
            BotCommand(command="cancel", description="Amalni bekor qilish"),
        ]
    )

    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s", me.username)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
