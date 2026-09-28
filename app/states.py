from aiogram.fsm.state import State, StatesGroup


class HandwritingFlow(StatesGroup):
    waiting_text = State()


class TTSFlow(StatesGroup):
    waiting_text = State()


class TranslateFlow(StatesGroup):
    waiting_text = State()
