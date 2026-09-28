from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import texts
from app.services.handwriting import NotebookStyle
from app.services.translator import LANGUAGES
from app.services.tts import VOICES


class NotebookCB(CallbackData, prefix="nb"):
    style: NotebookStyle


class VoiceCB(CallbackData, prefix="vc"):
    key: str


class LangCB(CallbackData, prefix="tr"):
    code: str


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_HANDWRITING)],
            [KeyboardButton(text=texts.BTN_TTS)],
            [KeyboardButton(text=texts.BTN_TRANSLATE)],
        ],
        resize_keyboard=True,
    )


def notebook_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for style in NotebookStyle:
        builder.button(text=style.title, callback_data=NotebookCB(style=style))
    builder.adjust(1)
    return builder.as_markup()


def voices_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for voice in VOICES.values():
        builder.button(text=voice.title, callback_data=VoiceCB(key=voice.key))
    builder.adjust(2)
    return builder.as_markup()


def languages_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lang in LANGUAGES.values():
        builder.button(text=lang.label, callback_data=LangCB(code=lang.code))
    builder.adjust(2)
    return builder.as_markup()
