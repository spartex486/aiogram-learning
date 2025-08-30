from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from state import Sum, Echo
import keyboards as kb
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.reply(f'Привет! Я твой первый бот. Я умею:\n/help — показать список команд\n/echo <текст> — повторить твое сообщение\n/sum a b — сложить два числа', reply_markup=kb.start_keyboard)

@router.message(F.text == 'Помощь')
async def help_handler(message: Message):
    await message.reply(f'Список команд: /start, /help, /echo, /sum')

@router.message(F.text == 'Сумма')
async def sum_handler(message: Message, state: FSMContext):
    await state.set_state(Sum.a)
    await message.answer("Напишите число a")
    



@router.message(Sum.a)
async def cmd_sum_a(message: Message, state: FSMContext):
    try:
        a = int(message.text)   # приведение к числу
        await state.update_data(a=a)
        await state.set_state(Sum.b)
        await message.answer("Напишите число b")
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


@router.message(Sum.b)
async def cmd_sum_b(message: Message, state: FSMContext):
    try:
        b = int(message.text)   # приведение к числу
        await state.update_data(b=b)
        data = await state.get_data()
        result = data['a'] + data['b']
        await message.answer(f"Сумма: {result}")
        await state.clear()   # очистим состояние после завершения
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


@router.message(F.text == 'Эхо')
async def echo_handler(message: Message, state: FSMContext):
    await state.set_state(Echo.message_echo)
    await message.answer("Напишите что либо", reply_markup=kb.back_keyboard)


@router.message(F.text == "Назад")
async def back_handler(message: Message):
    await message.answer(f'Привет! Я твой первый бот. Я умею:\n/help — показать список команд\n/echo <текст> — повторить твое сообщение\n/sum a b — сложить два числа', reply_markup=kb.start_keyboard)

@router.message(Echo.message_echo)
async def cmd_echo_message(message: Message, state: FSMContext):
    await state.update_data(message_echo=message.text)
    data = await state.get_data()
    await message.reply(f'{data['message_echo']}')





@router.message(Command('help'))
async def help_handler(message: Message):
    await message.reply(f'Список команд: /start, /help, /echo, /sum')

@router.message(Command('sum'))
async def sum_handler(message: Message, state: FSMContext):
    await state.set_state(Sum.a)
    await message.answer("Напишите число a")


@router.message(Sum.a)
async def cmd_sum_a(message: Message, state: FSMContext):
    try:
        a = int(message.text)   # приведение к числу
        await state.update_data(a=a)
        await state.set_state(Sum.b)
        await message.answer("Напишите число b")
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


@router.message(Sum.b)
async def cmd_sum_b(message: Message, state: FSMContext):
    try:
        b = int(message.text)   # приведение к числу
        await state.update_data(b=b)
        data = await state.get_data()
        result = data['a'] + data['b']
        await message.answer(f"Сумма: {result}")
        await state.clear()   # очистим состояние после завершения
    except ValueError:
        await message.answer("Нужно ввести число, попробуй ещё раз")


@router.message(Command('echo'))
async def echo_handler(message: Message, state: FSMContext):
    await state.set_state(Echo.message_echo)
    await message.answer("Напишите что либо")


@router.message(Echo.message_echo)
async def cmd_echo_message(message: Message, state: FSMContext):
    await state.update_data(message_echo=message.text)
    data = await state.get_data()
    await message.reply(f'{data['message_echo']}')
    
    
@router.message()
async def spam_handler(message: Message):
    await message.answer("Неизвестная команда")    
