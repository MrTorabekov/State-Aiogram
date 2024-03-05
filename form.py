from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    username = State()
    password = State()
    finish = State()

# class Login(StatesGroup):
#     username = State()
#     password = State()
#     finish = State()


class facebook(StatesGroup):
    fullname = State()
    phone = State()
    children = State()
    adress = State()
    sinf = State()
    location = State()
    finish = State()

DataUser = {
    "username":"",
    "password":""
}