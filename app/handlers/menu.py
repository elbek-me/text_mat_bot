"""Bosh menyu, /start, /help, /cancel va bo'limlarga kirish tugmalari.

Bu router birinchi ulanadi, shuning uchun menyu tugmalari har qanday holatda ishlaydi.
"""
import html

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import texts
from app.keyboards import main_menu, notebook_keyboard, voices_keyboard
from app.states import TranslateFlow

router = Router(name="menu")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    name = html.escape(message.from_user.first_name) if message.from_user else "do'st"
    await message.answer(texts.WELCOME.format(name=name), reply_markup=main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(texts.HELP, reply_markup=main_menu())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=main_menu())


@router.message(F.text == texts.BTN_HANDWRITING)
async def open_handwriting(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.CHOOSE_NOTEBOOK, reply_markup=notebook_keyboard())


@router.message(F.text == texts.BTN_TTS)
async def open_tts(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.CHOOSE_VOICE, reply_markup=voices_keyboard())


@router.message(F.text == texts.BTN_TRANSLATE)
async def open_translate(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(TranslateFlow.waiting_text)
    await message.answer(texts.ASK_TRANSLATE_TEXT)
