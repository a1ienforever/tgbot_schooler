from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()


class SchoolerCounter(StatesGroup):
    name = State()
    message_type = State()
    frame = State()
    class_num = State()
    letter = State()
    count = State()
    lesson_number = State()
