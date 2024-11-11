from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Web.Schooler.models import Person


def start_cb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
        ],
    )
    return keyboard


def cancel_cb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]],
    )
    return keyboard


def accept_cb(user_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Accept", callback_data=f"accept:{user_id}")],
            [InlineKeyboardButton(text="reject", callback_data=f"reject:{user_id}")],
        ]
    )
    return keyboard


def choose_frame_kb(lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 корпус", callback_data=f"frame:1:{lesson_num}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="4 корпус", callback_data=f"frame:4:{lesson_num}"
                )
            ],
        ]
    )
    return keyboard


def second_frame_class_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data="class:1"),
                InlineKeyboardButton(text="2", callback_data="class:2"),
                InlineKeyboardButton(text="3", callback_data="class:3"),
            ],
            [
                InlineKeyboardButton(text="4", callback_data="class:4"),
                InlineKeyboardButton(text="5", callback_data="class:5"),
                InlineKeyboardButton(text="6", callback_data="class:6"),
            ],
            [
                InlineKeyboardButton(text="7", callback_data="class:7"),
                InlineKeyboardButton(text="8", callback_data="class:8"),
                InlineKeyboardButton(text="9", callback_data="class:9"),
            ],
            [
                InlineKeyboardButton(text="10", callback_data="class:10"),
                InlineKeyboardButton(text="11", callback_data="class:11"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="class:back")],
        ]
    )
    return keyboard


def generate_eab_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Э", callback_data="letter:Э"),
                InlineKeyboardButton(text="А", callback_data="letter:А"),
                InlineKeyboardButton(text="Б", callback_data="letter:Б"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_a_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="А", callback_data="letter:А"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_ea_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="А", callback_data="letter:А"),
                InlineKeyboardButton(text="Э", callback_data="letter:Э"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_ab_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="А", callback_data="letter:А"),
                InlineKeyboardButton(text="Б", callback_data="letter:Б"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_gnste_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Г", callback_data="letter:Г"),
                InlineKeyboardButton(text="Н", callback_data="letter:Н"),
                InlineKeyboardButton(text="С", callback_data="letter:С"),
                InlineKeyboardButton(text="Т", callback_data="letter:Т"),
                InlineKeyboardButton(text="Э", callback_data="letter:Э"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_gnte_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Г", callback_data="letter:Г"),
                InlineKeyboardButton(text="Н", callback_data="letter:Н"),
                InlineKeyboardButton(text="Т", callback_data="letter:Т"),
                InlineKeyboardButton(text="Э", callback_data="letter:Э"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def generate_npt_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Н", callback_data="letter:Н"),
                InlineKeyboardButton(text="П", callback_data="letter:П"),
                InlineKeyboardButton(text="Т", callback_data="letter:Т"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def first_frame_class_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data="class:1"),
                InlineKeyboardButton(text="2", callback_data="class:2"),
                InlineKeyboardButton(text="3", callback_data="class:3"),
            ],
            [
                InlineKeyboardButton(text="4", callback_data="class:4"),
                InlineKeyboardButton(text="5", callback_data="class:5"),
                InlineKeyboardButton(text="6", callback_data="class:6"),
            ],
            [
                InlineKeyboardButton(text="7", callback_data="class:7"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="class:back")],
        ]
    )
    return keyboard


def first_frame_letter_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="А", callback_data="letter:А"),
                InlineKeyboardButton(text="Б", callback_data="letter:Б"),
                InlineKeyboardButton(text="В", callback_data="letter:В"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="letter:back")],
        ]
    )
    return keyboard


def accept_record_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправить", callback_data="check:accept")],
            [InlineKeyboardButton(text="Заново", callback_data="check:restart")],
        ]
    )
    return keyboard


def accept_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправить", callback_data=f"send")],
            [InlineKeyboardButton(text="Заново", callback_data="repeat")],
        ]
    )
    return keyboard


def generate_inline_keyboard(state: dict):
    builder = InlineKeyboardBuilder()

    persons = (
        Person.objects.select_related("class_assigned__building")
        .filter(
            class_assigned__grade=state["class_num"],
            class_assigned__letter=state["letter"],
            class_assigned__building__number=state["frame"],
        )
        .order_by("last_name")
    )

    for person in persons:
        name = f"{person.last_name} {person.first_name}"
        builder.button(text=name, callback_data=f"person:{person.id}")

    builder.adjust(2)

    return builder
