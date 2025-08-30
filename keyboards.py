from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Эхо")],
        [KeyboardButton(text="Сумма")]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Назад')]
        
    ], resize_keyboard=True
    
)