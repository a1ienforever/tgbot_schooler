from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def choose_frame_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 корпус", callback_data="frame:1")],
            [InlineKeyboardButton(text="2 корпус", callback_data="frame:2")],
        ]
    )
    return keyboard


def choose_class_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1", callback_data="class:1"),
                InlineKeyboardButton(text="2", callback_data="class:2"),
                InlineKeyboardButton(text="3", callback_data="class:3")
            ],
            [
                InlineKeyboardButton(text="4", callback_data="class:4"),
                InlineKeyboardButton(text="5", callback_data="class:5"),
                InlineKeyboardButton(text="6", callback_data="class:6")
            ],
            [
                InlineKeyboardButton(text="7", callback_data="class:7"),
                InlineKeyboardButton(text="8", callback_data="class:8"),
                InlineKeyboardButton(text="9", callback_data="class:9")
            ],
            [
                InlineKeyboardButton(text="10", callback_data="class:10"),
                InlineKeyboardButton(text="11", callback_data="class:11"),
            ],
        ]
    )
    return keyboard


def choose_letter_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="А", callback_data="letter:А"),
                InlineKeyboardButton(text="Б", callback_data="letter:Б"),
                InlineKeyboardButton(text="В", callback_data="letter:В")
            ],
            [
                InlineKeyboardButton(text="Г", callback_data="letter:Г"),
                InlineKeyboardButton(text="Д", callback_data="letter:Д")
            ],
        ])
    return keyboard
