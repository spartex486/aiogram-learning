from aiogram.fsm.state import StatesGroup, State


class Sum(StatesGroup):
    a = State()
    b = State()


class Echo(StatesGroup):
    message_echo = State()
