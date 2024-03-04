import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from form import Form, Login, facebook, DataUser
from aiogram.fsm.context import FSMContext
from buttons import keyboard, key, check, keyboard1
from config import TOKEN, data_group
from db import Database

db = Database("database.db")

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Assalomu alekum! {message.from_user.full_name} botni ishlatish uchun pastdagi kanalga obuna bo'ling",
        reply_markup=check)
    print(message.from_user.full_name)
    # db.add_user(message.from_user.id, message.from_user.full_name)


@dp.callback_query(F.data == "submit")
async def callback_submit(call: CallbackQuery, bot: Bot):
    user_status = await bot.get_chat_member(chat_id=data_group, user_id=call.from_user.id)

    if user_status.status != "left":
        await bot.send_message(
            call.from_user.id, "✅"
        )
        await call.message.answer("Login or Register", reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text="Siz kanalga obuna bulmagansiz!", reply_markup=check)
        text = ("Kanalga obuna bo'lmagansiz ⚠️"
                )
        show_alert = True
        await call.answer(text, show_alert=show_alert)

    @dp.message()
    async def reg(message: Message, state: FSMContext):
        if message.text == "Register":
            await state.set_state(Form.name)
            await message.answer("Ismingizni kiriting:")


@dp.message(Form.name)
async def usernames(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.username)
    await message.answer("Username ni kiritng")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("parolingizni kirting:")


@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Muvaffaqiyatli amalga oshirildi",
    )
    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    matn = f"🧑‍💻 Name: {name}\n⚡️ Username: {username}\n🔐 Password: {password}"
    await message.answer(text=matn, reply_markup=key)
    db.add_user(name, username, password)
    print(matn)

    DataUser["username"] = username
    DataUser["password"] = password


@dp.message(F.text == "Login")
async def start(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Login.username)
    await message.answer("Tepada yozgan username ni kiriting:")
    print(message.from_user.full_name)


@dp.message(Login.username)
async def username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Login.password)
    await message.answer("Tepada yozgan parolingizni kiriting:")
    print(message.from_user.full_name)


@dp.message(Login.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Login.finish)
    userdata = await state.get_data()
    await state.clear()
    username = userdata.get("username", "Unknown")
    password = userdata.get("password", "Unknown")
    print(username, password)
    print(message.from_user.full_name)

    if username == DataUser["username"] and password == DataUser["password"]:
        await message.answer("Muvaffaqiyatli amalga oshirildi")
        print("Successful")
    else:
        await message.answer("Wrong username or password")
        print("username yoki parol notog'ri")


@dp.message(F.text == "Ariza to'ldirish")
async def fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(facebook.fullname)
    await message.answer("To'liq ism familiyangizni kiriting:")


@dp.message(facebook.fullname)
async def phone(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(facebook.phone)
    await message.answer("Telefon raqamingizni kiriting:")


@dp.message(facebook.phone)
async def phone(message: Message, state: FSMContext):
    if message.text[0:4] == "+998":
        if message.text[4:10]:
            await state.update_data(phone=message.text)
            await state.set_state(facebook.children)
            await message.answer("Bolangizni ismi")
        else:
            await message.answer("Telefon raqam 11 sondan iborat boshlanishi kerak")
    else:
        await message.answer("raqam +998 nilan boshlanishi kerak")


@dp.message(facebook.children)
async def sinf(message: Message, state: FSMContext):
    await state.update_data(children=message.text)
    await state.set_state(facebook.adress)
    await message.answer("adressingizni yozing:")


@dp.message(facebook.adress)
async def adress(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    await state.set_state(facebook.sinf)
    await message.answer("bolangiz nechinchi sinfda o'qimoqchi")


@dp.message(facebook.sinf)
async def sinf(message: Message, state: FSMContext):
    await state.update_data(sinf=message.text)
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
        "You have successfully",
    )
    fullname = data2.get("fullname", "Unknown")
    phone = data2.get("phone", "Unknown")
    children = data2.get("children", "Unknown")
    adress = data2.get("adress", "Unknown")
    sinf = data2.get("sinf", "Unknown")
    location1 = data2.get("location1", "Unknown")
    location2 = data2.get("location2", "Unknown")

    await bot.send_message(data_group,
                           text=f"Murojat qilgan shaxs {message.from_user.full_name}\n\n🧑‍💻Ism va Familiya: {fullname}\n📱Telefon raqam: {phone}\n👦🏻farzandini ismi: {children}\n🟤Turar joylari: {adress}\n🔢Farzandini sinfi: {sinf}")
    await bot.send_location(data_group, latitude=location1, longitude=location2)  # noqa
    await message.answer(
        f"🧑‍💻 fullname: {fullname}\n📱phone number: {phone}\n👦🏻child's name: {children}\n🟤adress: {adress}\n🔢sinf number: {sinf}")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
