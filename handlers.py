from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
router = Router()

@router.message()
async def start_handler(message: Message):
    await message.reply(f'Вот ваше сообщение {message.text}')
