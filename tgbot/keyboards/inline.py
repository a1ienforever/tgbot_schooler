from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Web.Schooler.models import Person
from tgbot.misc.callback import (
    FrameCallback,
    ClassCallback,
    LetterCallback,
    PersonCallback,
)


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
            [
                InlineKeyboardButton(
                    text="Директор", callback_data=f"director:{user_id}"
                )
            ],
            [InlineKeyboardButton(text="Завуч", callback_data=f"deputy:{user_id}")],
            [InlineKeyboardButton(text="Учитель", callback_data=f"teacher:{user_id}")],
            [InlineKeyboardButton(text="Отклонить", callback_data=f"reject:{user_id}")],
        ]
    )
    return keyboard


def choose_frame_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 корпус",
                    callback_data=FrameCallback(
                        type_report=type_report, lesson_num=lesson_num, frame=1
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="4 корпус",
                    callback_data=FrameCallback(
                        type_report=type_report, lesson_num=lesson_num, frame=4
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def second_frame_class_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=1
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="2",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=2
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="3",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=3
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="4",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=4
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="5",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=5
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="6",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=6
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="7",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=7
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="8",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=8
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="9",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=9
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="10",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=10
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="11",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=11
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=100
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_eab_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Э",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="З"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="А",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="А"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Б",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Б"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_a_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="А"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_ea_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="А"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Э",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="З"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_ab_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="А"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Б",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Б"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_gnste_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Г",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Г"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Н",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Н"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="С",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="С"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Т",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Т"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Э",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="З"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_gnte_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Г",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Г"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Н",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Н"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Т",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Т"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Э",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="З"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def generate_npt_kb(type_report, lesson_num=None):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Н",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Н"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="П",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="П"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Т",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Т"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def first_frame_class_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=1
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="2",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=2
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="3",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=3
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="4",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=4
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="5",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=5
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="6",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=6
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="7",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=7
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=ClassCallback(
                        type_report=type_report, lesson_num=lesson_num, class_num=100
                    ).pack(),
                )
            ],
        ]
    )
    return keyboard


def first_frame_letter_kb(type_report, lesson_num):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="А"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Б",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="Б"
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="В",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="В"
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=LetterCallback(
                        type_report=type_report, lesson_num=lesson_num, letter="back"
                    ).pack(),
                )
            ],
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


def generate_inline_keyboard(state: dict, type_report):
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
        builder.button(
            text=name,
            callback_data=PersonCallback(type_report=type_report, person_id=person.id),
        )
    builder.button(
        text="Назад",
        callback_data=PersonCallback(type_report=type_report, person_id=-1),
    )

    builder.adjust(2)

    return builder
