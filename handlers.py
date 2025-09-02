from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states import Sum, Echo
import keyboards as kb

router = Router()


# --- START ---
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "Привет! Я твой бот:\n"
        "/help — показать команды\n"
        "/echo <текст> — повторить сообщение\n"
        "/sum a b — сложить числа"
    )
    await message.answer(text, reply_markup=kb.start_keyboard)


# --- HELP ---
@router.message(Command("help"))
@router.message(F.text == "Помощь")
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    text = "Список команд: /start, /help, /echo, /sum"
    await message.answer(text)


# --- SUM ---
@router.message(Command("sum"))
@router.message(F.text == "Сумма")
async def sum_start(message: Message, state: FSMContext):
    await state.set_state(Sum.a)
    await message.answer("Напишите число a", reply_markup=kb.back_keyboard)


@router.message(Sum.a)
async def sum_a(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.clear()
        await start_handler(message, state)
        return

    try:
        a = int(message.text)
        await state.update_data(a=a)
        await state.set_state(Sum.b)
        await message.answer("Напишите число b", reply_markup=kb.back_keyboard)
    except ValueError:
        await message.answer("Нужно ввести число")


@router.message(Sum.b)
async def sum_b(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.clear()
        await start_handler(message, state)
        return

    try:
        b = int(message.text)
        data = await state.get_data()
        result = data["a"] + b
        await message.answer(f"Сумма: {result}")
        await state.clear()
    except ValueError:
        await message.answer("Нужно ввести число")


# --- ECHO ---
@router.message(Command("echo"))
@router.message(F.text == "Эхо")
async def echo_start(message: Message, state: FSMContext):
    await state.set_state(Echo.message_echo)
    await message.answer("Напишите что-либо", reply_markup=kb.back_keyboard)


@router.message(Echo.message_echo)
async def echo_message(message: Message, state: FSMContext):
    # Выход из состояния
    if message.text.lower() == "назад":
        await state.clear()
        await start_handler(message, state)
        return

    # Просто повторяем текст пользователя
    await message.answer(message.text, reply_markup=kb.back_keyboard)

# --- BACK ---
@router.message(F.text == "Назад")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await start_handler(message, state)


# --- SPAM ---
@router.message()
async def spam_handler(message: Message):
    await message.answer("Неизвестная команда")
