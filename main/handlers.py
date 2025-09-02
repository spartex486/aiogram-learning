from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from main.states import Sum, Echo
import main.keyboards as kb

router = Router()


# --- START / HELP --- #
@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "Привет! Я твой первый бот. Я умею:\n"
        "/help — показать список команд\n"
        "/echo <текст> — повторить твое сообщение\n"
        "/sum a b — сложить два числа"
    )
    await message.answer(text, reply_markup=kb.start_keyboard)


@router.message(Command("help") | F.text == "Помощь")
async def help_handler(message: Message):
    text = "Список команд: /start, /help, /echo, /sum"
    await message.answer(text)


# --- SUM --- #
@router.message(Command("sum") | F.text == "Сумма")
async def sum_start(message: Message, state: FSMContext):
    await state.set_state(Sum.a)
    await message.answer("Напишите число a")


@router.message(Sum.a)
async def sum_a(message: Message, state: FSMContext):
    try:
        a = int(message.text)
        await state.update_data(a=a)
        await state.set_state(Sum.b)
        await message.answer("Напишите число b")
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


@router.message(Sum.b)
async def sum_b(message: Message, state: FSMContext):
    try:
        b = int(message.text)
        data = await state.get_data()
        result = data["a"] + b
        await message.answer(f"Сумма: {result}")
        await state.clear()
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


# --- ECHO --- #
@router.message(Command("echo") | F.text == "Эхо")
async def echo_start(message: Message, state: FSMContext):
    await state.set_state(Echo.message_echo)
    await message.answer("Напишите что-либо", reply_markup=kb.back_keyboard)


@router.message(F.text == "Назад")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "Привет! Я твой первый бот. Я умею:\n"
        "/help — показать список команд\n"
        "/echo <текст> — повторить твое сообщение\n"
        "/sum a b — сложить два числа"
    )
    await message.answer(text, reply_markup=kb.start_keyboard)


@router.message(Echo.message_echo)
async def echo_message(message: Message, state: FSMContext):
    await message.answer(message.text)
    await state.clear()


# --- SPAM HANDLER --- #
@router.message()
async def spam_handler(message: Message):
    await message.answer("Неизвестная команда")
