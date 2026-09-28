"""Hech qanday holatda bo'lmagan foydalanuvchi xabarlari."""
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from app import texts
from app.keyboards import main_menu

router = Router(name="fallback")


@router.message(StateFilter(None))
async def unknown_message(message: Message) -> None:
    await message.answer(texts.USE_MENU, reply_markup=main_menu())
