import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from form import Form, facebook, DataUser
from aiogram.fsm.context import FSMContext
from buttons import keyboard, key, check, keyboard1, number1, get_id
from config import TOKEN, data_group, admin,Ahmad_group
from db import Database, Database1
from aiogram.utils.markdown import hbold
from aiogram.types import ReplyKeyboardRemove

ariza = Database1("database.db")

db = Database("database.db")

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(photo="https://view.genial.ly/65ee8a9f8282920014c2bfa8/interactive-content-first-proekt",
                               caption=f"Assalomu Alekum! {(hbold(message.from_user.full_name))}\n\nbotni ishlatish uchun pastdagi kanalga obuna bo'ling",
                               reply_markup=check, parse_mode="HTML")
    print(datetime.now())
    print(message.from_user.full_name)
    db.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)


@dp.callback_query(F.data == "submit")
async def callback_submit(call: CallbackQuery, bot: Bot):
    user_status = await bot.get_chat_member(chat_id=Ahmad_group, user_id=call.from_user.id)

    if user_status.status != "left":
        await bot.send_message(
            call.from_user.id,
            "<b>Muvaffaqiyatli O'tdingiz endi registerdan o'tishingiz mumkun✅!</b>", reply_markup=key,
            parse_mode="HTML")

    else:
        text = ("Kanalga obuna bo'lmagansiz ⚠️"
                )
        await call.answer(text, show_alert=True)




@dp.message(F.text == "Ariza qoldirish")
async def fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(facebook.fullname)
    await message.answer("To'liq ism familiyangizni kiriting:")


@dp.message(facebook.fullname)
async def phone(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text.title())
    await state.set_state(facebook.phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=number1)


@dp.message(facebook.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(facebook.children)
    await message.answer("Bolangizning ismi:",reply_markup=ReplyKeyboardRemove())


@dp.message(facebook.children)
async def phone(message: Message, state: FSMContext):
    await state.update_data(children=message.text.capitalize())
    await state.set_state(facebook.sinf)
    await message.answer("bolangiz nechinchi sinfda o'qimoqchi:")


@dp.message(facebook.sinf)
async def sinf(message: Message, state: FSMContext):
    if 5 <= int(message.text) <= 11:
        await state.update_data(sinf=message.text)
        await state.set_state(facebook.adress)
        await message.answer("Adresingizni yozma holatda kiriting:")
    else:
        await message.answer("5-11 bo'lgan sinflar kiritishingiz zarur")


@dp.message(facebook.adress)
async def adress(message: Message, state: FSMContext):
    await state.update_data(adress=message.text.title())
    await state.set_state(facebook.location)
    await message.answer("Lokatsiyani yuboring:", reply_markup=keyboard1)


@dp.message(facebook.location and F.location)
async def location(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(location1=message.location.latitude)
    await state.update_data(location2=message.location.longitude)
    await state.set_state(facebook.finish)
    data2 = await state.get_data()
    await state.clear()
    await message.answer(
        "Arizangiz qabul qilindi tez orada ko'rib chiqamiz✅", reply_markup=ReplyKeyboardRemove()
    )
    fullname = data2.get("fullname", "Unknown")
    phone = data2.get("phone", "Unknown")
    children = data2.get("children", "Unknown")
    adress = data2.get("adress", "Unknown")
    sinf = data2.get("sinf", "Unknown")
    location1 = data2.get("location1", "Unknown")
    location2 = data2.get("location2", "Unknown")

    await bot.send_message(data_group,
                           text=f"Murojat qilgan shaxs {message.from_user.full_name}\n⏱Ariza tashalgan vaqt: {datetime.now()}\n\n🧑‍💻Ism va Familiya: {fullname}\n📱Telefon raqam: {phone}\n👦🏻farzandini ismi: {children}\n🟤Turar joylari: {adress}\n🔢Farzandini sinfi: {sinf}")
    await bot.send_location(data_group, latitude=location1, longitude=location2)  # noqa
    # await message.answer(
    #     f"Murojat qilgan shaxs {message.from_user.full_name}\n⏱Ariza tashalgan vaqt: {datetime.now()}\n\n🧑‍💻Ism va Familiya: {fullname}\n📱Telefon raqam: {phone}\n👦🏻farzandini ismi: {children}\n🟤Turar joylari: {adress}\n🔢Farzandini sinfi: {sinf}")

    ariza.add_user(fullname, phone, children, adress, sinf, location1, location2, datetime.now())


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
