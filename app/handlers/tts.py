import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from app import texts
from app.config import Settings
from app.keyboards import VoiceCB
from app.services.errors import ServiceError
from app.services.tts import VOICES, synthesize
from app.states import TTSFlow

logger = logging.getLogger(__name__)
router = Router(name="tts")


@router.callback_query(VoiceCB.filter())
async def choose_voice(cb: CallbackQuery, callback_data: VoiceCB, state: FSMContext) -> None:
    voice = VOICES.get(callback_data.key)
    if voice is None:
        await cb.answer(texts.INVALID_CHOICE, show_alert=True)
        return
    await state.set_state(TTSFlow.waiting_text)
    await state.update_data(voice_key=voice.key)
    if isinstance(cb.message, Message):
        await cb.message.edit_text(texts.VOICE_SELECTED.format(title=voice.title))
    await cb.answer()


@router.message(TTSFlow.waiting_text, F.text)
async def receive_text(message: Message, state: FSMContext, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer(texts.EMPTY_TEXT)
        return
    if len(text) > settings.max_tts_chars:
        await message.answer(
            texts.TEXT_TOO_LONG.format(length=len(text), limit=settings.max_tts_chars)
        )
        return

    data = await state.get_data()
    voice = VOICES.get(data.get("voice_key", ""))
    if voice is None:
        await state.clear()
        await message.answer(texts.CHOOSE_VOICE)
        return

    try:
        async with ChatActionSender.record_voice(bot=message.bot, chat_id=message.chat.id):
            audio = await synthesize(text, voice)
    except ServiceError as exc:
        await message.answer(exc.user_message)
        return

    await message.answer_audio(
        BufferedInputFile(audio, filename="ovoz.mp3"),
        title=voice.title,
        performer="TTS Bot",
    )


@router.message(TTSFlow.waiting_text)
async def not_text(message: Message) -> None:
    await message.answer(texts.SEND_TEXT_ONLY)
