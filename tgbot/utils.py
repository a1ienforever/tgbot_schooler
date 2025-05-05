import asyncio
import re
from collections import defaultdict

from aiogram.fsm.context import FSMContext
from icecream import ic

from Web.AdminPanel.models import TgUser, User
from Web.Record.models import IncidentRecord
from tgbot.services.db import get_incidents

WITHOUT_FORM = 'form'
SIGNAL = 'signal'
LATE = 'late'

STATUS_INCIDENTS = {
    WITHOUT_FORM: IncidentRecord.WITHOUT_UNIFORM,
    SIGNAL: IncidentRecord.SIGNAL,
    LATE: IncidentRecord.LATE
}


async def delete_message_later(bot, chat_id: int, message_id: int, delay: int):
    """Удаляет сообщение через заданное время."""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass  # Игнорируем ошибки, если сообщение уже удалено или недоступно


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
    return await User.objects.filter(tg_user__telegram_id=user.telegram_id).aget()


async def get_state_data(state: FSMContext):
    data = await state.get_data()
    return {
        "frame": data.get("frame"),
        "class_num": data.get("class_num"),
        "letter": data.get("letter"),
        "count": data.get("count"),
        "lesson_num": data.get("lesson_number"),
        "message_type": data.get("message_type"),
    }


async def format_message(user, frame, class_num, letter, count, lesson_num):
    return (
        f"{user.name} {user.patronymic}, проверьте запись: на {lesson_num} уроке в {frame} корпусе "
        f"{class_num}{letter} - {count} человек"
    )


def split_full_name(full_name):
    parts = full_name.split()

    # Фамилия всегда будет первой
    last_name = parts[0]

    # Имя всегда второй частью
    first_name = parts[1]

    # Проверяем, есть ли отчество
    middle_name = " ".join(parts[2:]) if len(parts) > 2 else None

    return last_name, first_name, middle_name



async def get_incidents_message(status):
    records = await get_incidents(status)

    msg = "Отчет за последние 7 дней\n" f"{status}:\n"

    # Группируем по signal.msg
    grouped = defaultdict(list)
    for record in records:
        key = record.signal.msg if status == IncidentRecord.SIGNAL else "default"
        grouped[key].append(record)

    for signal_msg, group in grouped.items():
        for person in group:
            msg += (
                f"{person.person_id.last_name} "
                f"{person.person_id.first_name} "
                f"{person.person_id.class_assigned}\n"
            )

        if status == IncidentRecord.SIGNAL and signal_msg:
            msg += f"{signal_msg}\n"

        msg += "\n"  # разделение между группами

    return msg

