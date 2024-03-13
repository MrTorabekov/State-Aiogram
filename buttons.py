from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

kb = [[KeyboardButton(text="Register")]]

keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Choose Button")

ke = [[types.KeyboardButton(text="Ariza to'ldirish")]]

key = types.ReplyKeyboardMarkup(keyboard=ke, resize_keyboard=True, one_time_keyboard=True)

check = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="Obuna bo'ling", url="https://t.me/+A3sk-slXf7RmNjIy")],
    [InlineKeyboardButton(text="Tasdiqlash", callback_data="submit")]
])

get = [
    [types.KeyboardButton(text="Get id")]
]
get_id = types.ReplyKeyboardMarkup(keyboard=get, resize_keyboard=True)

kb1 = [

    [types.KeyboardButton(text="Lokatsiya yuborish", request_location=True)]
]

keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb1, resize_keyboard=True, input_field_placeholder="Word"
                                      )

number = [
    [KeyboardButton(text="Kontactni yuborish", request_contact=True)]
]
number1 = types.ReplyKeyboardMarkup(keyboard=number, resize_keyboard=True)
