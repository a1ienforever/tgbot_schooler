import re

from aiogram.fsm.context import FSMContext

from Web.AdminPanel.models import TgUser, User


def get_name(input_str: str):
    pattern = r"Фамилия:\s*(\S+)\nИмя:\s*(\S+)\nОтчество:\s*(\S+)"

    # Поиск данных
    match = re.search(pattern, input_str)

    # Извлечение данных
    if match:
        surname = match.group(1)
        name = match.group(2)
        patronymic = match.group(3)

        # Вывод
        print(f"Фамилия: {surname}\nИмя: {name}\nОтчество: {patronymic}")
        return surname, name, patronymic
    else:
        return "Данные не найдены", None, None


async def get_user_data(user: TgUser):
    return User.objects.filter(tg_user__telegram_id=user.telegram_id).get()


async def get_state_data(state: FSMContext):
    data = await state.get_data()
    return {
        "frame": data.get("frame"),
        "class_num": data.get("class_num"),
        "letter": data.get("letter"),
        "count": data.get("count"),
        "lesson_num": data.get("lesson_number"),
    }


async def format_message(user, frame, class_num, letter, count, lesson_num):
    return (
        f"{user.name} {user.patronymic}, проверьте запись: на {lesson_num} уроке в {frame} корпусе "
        f"{class_num}{letter} - {count} человек"
    )
