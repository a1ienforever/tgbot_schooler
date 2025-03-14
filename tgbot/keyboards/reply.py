from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def menu_kb():

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Опоздавший")],
            [KeyboardButton(text="Без формы")],
            [KeyboardButton(text="Сигнал")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    return keyboard


