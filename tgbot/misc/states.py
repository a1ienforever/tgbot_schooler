from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()


class Incident(StatesGroup):
    frame = State()
    class_num = State()
    letter = State()


class SchoolerCounter(StatesGroup, Incident):
    count = State()
    lesson_number = State()


class InputFile(StatesGroup):
    call = State()
    input = State()


class IncidentLater(StatesGroup, Incident):
    person = State()


class IncidentForm(StatesGroup, Incident):
    person = State()
