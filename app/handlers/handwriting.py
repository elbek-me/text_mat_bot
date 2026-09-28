import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.media_group import MediaGroupBuilder

from app import texts
from app.config import Settings
from app.keyboards import NotebookCB
from app.services.errors import ServiceError
from app.services.handwriting import NotebookStyle, render_pages_async
from app.states import HandwritingFlow

logger = logging.getLogger(__name__)
router = Router(name="handwriting")


@router.callback_query(NotebookCB.filter())
async def choose_notebook(cb: CallbackQuery, callback_data: NotebookCB, state: FSMContext) -> None:
    style = callback_data.style
    await state.set_state(HandwritingFlow.waiting_text)
    await state.update_data(style=style.value)
    if isinstance(cb.message, Message):
        await cb.message.edit_text(texts.NOTEBOOK_SELECTED.format(title=style.title))
    await cb.answer()


@router.message(HandwritingFlow.waiting_text, F.text)
async def receive_text(message: Message, state: FSMContext, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer(texts.EMPTY_TEXT)
        return
    if len(text) > settings.max_handwriting_chars:
        await message.answer(
            texts.TEXT_TOO_LONG.format(length=len(text), limit=settings.max_handwriting_chars)
        )
        return

    data = await state.get_data()
    style = NotebookStyle(data.get("style", NotebookStyle.LINED.value))

    try:
        async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
            pages, truncated = await render_pages_async(
                text, style, settings.font_path, settings.max_pages
            )
    except ServiceError as exc:
        await message.answer(exc.user_message)
        return

    if len(pages) == 1:
        await message.answer_photo(BufferedInputFile(pages[0], filename="daftar.jpg"))
    else:
        album = MediaGroupBuilder()
        for i, page in enumerate(pages, 1):
            album.add_photo(media=BufferedInputFile(page, filename=f"daftar_{i}.jpg"))
        await message.answer_media_group(album.build())

    if truncated:
        await message.answer(texts.HANDWRITING_TRUNCATED.format(pages=settings.max_pages))
    await message.answer(texts.HANDWRITING_MORE)


@router.message(HandwritingFlow.waiting_text)
async def not_text(message: Message) -> None:
    await message.answer(texts.SEND_TEXT_ONLY)
