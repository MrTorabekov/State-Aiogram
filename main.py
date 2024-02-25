import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from buttons import keyboard


class Form(StatesGroup):
    name = State()
    username = State()
    password = State()
    finish = State()



dp = Dispatcher()
TOKEN = "7163530590:AAEQ_e86WsCKTgOxPtRdY2Vw81-n0MTFCyk"


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Assalomu alekum! {message.from_user.full_name}")
    await message.answer("Login or Register", reply_markup=keyboard)

    @dp.message()
    async def reg(message: Message, state: FSMContext):
        if message.text == "Register":
            await state.set_state(Form.name)
            await message.answer("Enter name")


@dp.message(Form.name)
async def usernames(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.username)
    await message.answer("Enter username")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("Enter password")


@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "You have successfully",
    )
    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    matn = f"🧑‍💻 Name: {name}\n⚡️ Username: {username}\n🔐 Password: {password}"
    await message.answer(text=matn)
    print(matn)


class Form(StatesGroup):
    gmail = State()
    pasword = State()
    finish = State()

    @dp.message(F.text == "Login")
    async def login(message: Message, state: FSMContext):
        await state.set_state(Form.gmail)
        await message.answer("Enter gmail")


@dp.message(Form.gmail)
async def paswords(message: Message, state: FSMContext):
    await state.update_data(gmail=message.text)
    await state.set_state(Form.pasword)
    await message.answer("Enter pasword")


@dp.message(Form.pasword)
async def Finish(message: Message, state: FSMContext):
    await state.update_data(pasword=message.text)
    await state.set_state(Form.finish)
    dataa = await state.get_data()
    await state.clear()
    await message.answer(
        "You have successfully",
    )
    gmail = dataa.get("gmail", "Unknown")
    pasword = dataa.get("pasword", "Unknown")

    matnn = f"🧑‍💻 Gmail: {gmail}\n🔐 Password: {pasword}"
    await message.answer(text=matnn)
    print(matnn)


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
