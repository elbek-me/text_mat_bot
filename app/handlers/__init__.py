from aiogram import Router

from app.handlers import errors, fallback, handwriting, menu, translate, tts


def build_root_router() -> Router:
    """Tartib muhim: menyu birinchi, fallback oxirgi."""
    root = Router(name="root")
    root.include_routers(
        errors.router,
        menu.router,
        handwriting.router,
        tts.router,
        translate.router,
        fallback.router,
    )
    return root
