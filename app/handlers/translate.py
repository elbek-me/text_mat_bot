import html
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from app import texts
from app.config import Settings
from app.keyboards import LangCB, languages_keyboard
from app.services.errors import ServiceError
from app.services.translator import LANGUAGES, translate
from app.states import TranslateFlow
from app.utils import split_message

logger = logging.getLogger(__name__)
router = Router(name="translate")


@router.message(TranslateFlow.waiting_text, F.text)
async def receive_text(message: Message, state: FSMContext, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer(texts.EMPTY_TEXT)
        return
    if len(text) > settings.max_translate_chars:
        await message.answer(
            texts.TEXT_TOO_LONG.format(length=len(text), limit=settings.max_translate_chars)
        )
        return
    await state.update_data(source_text=text)
    await message.answer(texts.CHOOSE_LANGUAGE, reply_markup=languages_keyboard())


@router.message(TranslateFlow.waiting_text)
async def not_text(message: Message) -> None:
    await message.answer(texts.SEND_TEXT_ONLY)


@router.callback_query(LangCB.filter())
async def choose_language(cb: CallbackQuery, callback_data: LangCB, state: FSMContext) -> None:
    data = await state.get_data()
    source = data.get("source_text")
    if not source:
        await cb.answer(texts.SEND_TEXT_FIRST, show_alert=True)
        return
    lang = LANGUAGES.get(callback_data.code)
    if lang is None:
        await cb.answer(texts.INVALID_CHOICE, show_alert=True)
        return
    if not isinstance(cb.message, Message):
        await cb.answer()
        return

    await cb.answer(texts.TRANSLATING)
    try:
        async with ChatActionSender.typing(bot=cb.bot, chat_id=cb.message.chat.id):
            result = await translate(source, lang.code)
    except ServiceError as exc:
        await cb.message.answer(exc.user_message)
        return

    for i, chunk in enumerate(split_message(result)):
        prefix = f"<b>{lang.label}</b>\n\n" if i == 0 else ""
        await cb.message.answer(prefix + html.escape(chunk))
