from aiogram.fsm.state import State, StatesGroup
class Sum(StatesGroup):
    a = State()
    b = State()

class Echo(StatesGroup):
    message_echo = State()