import csv
import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from tqdm import tqdm

from Web.AdminPanel.models import TgUser, User
from tgbot.decorators.access_rights import role_required
from tgbot.services.db import (
    add_person,
    clear_database_schooler,
    create_notification,
    get_notification,
    get_records,
    get_admins,
)
from tgbot.services.schedule_message import pause_scheduler, resume_scheduler
from tgbot.utils import split_full_name, get_incidents_message

router = Router()


@router.callback_query(
    F.data.startswith("director")
    | F.data.startswith("deputy")
    | F.data.startswith("teacher")
    | F.data.startswith("reject")
)
async def accept_user(call: CallbackQuery, user: TgUser):
    role, user_id = call.data.split(":")
    User.objects.filter(tg_user__telegram_id=user_id).update(role=role)
    if role != "reject":
        await call.message.bot.send_message(
            user_id, text="Вы успешно зарегистрированы."
        )
        await call.message.edit_reply_markup(reply_markup=None)
    else:
        await call.message.bot.send_message(
            user_id, text="Заявка была отклонена. Обратитесь в поддержку."
        )
        await call.message.edit_reply_markup(reply_markup=None)
        User.objects.filter(tg_user__telegram_id=user_id).delete()


async def send_admin(bot: Bot, lesson_num: int):

    today = datetime.date.today()

    records = await get_records(today, lesson_num)

    if not records:
        return

    message_text = f"[{today}] Записи за {lesson_num} урок:\n"
    for record in records:
        message_text += f"Корпус: {record.frame}, Класс: {record.class_num}{record.letter}, Кол-во: {record.count}\n"

    admins = await get_admins()

    for admin in admins:
        notification = await get_notification(today, admin, lesson_num)

        try:
            if notification and notification.lesson_num == lesson_num:
                await bot.edit_message_text(
                    chat_id=admin.telegram_id,
                    message_id=notification.message_id,
                    text=message_text,
                )
            else:
                sent_message = await bot.send_message(
                    chat_id=admin.telegram_id, text=message_text
                )

                await create_notification(today, admin, sent_message, lesson_num)

        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin.telegram_id}: {e}")


async def send_all_admin(bot: Bot, msg):
    admins = await get_admins()
    for admin in admins:
        await bot.send_message(admin.telegram_id, msg)


@router.message(Command("pause"))
@role_required(["director"])
async def pause(message: Message, user: TgUser):
    pause_scheduler()
    msg = "Отправка сообщений по расписанию приостановлена"
    users = User.objects.filter(role="director")
    for user in users:
        await message.bot.send_message(user.tg_user.telegram_id, msg)


@router.message(Command("resume"))
@role_required(["director"])
async def resume(message: Message, user: TgUser):
    resume_scheduler()
    msg = "Отправка сообщений по расписанию возобновлена"
    users = User.objects.filter(role="director")
    for user in users:
        await message.bot.send_message(user.tg_user.telegram_id, msg)


@router.message(Command("test"))
@role_required(["director"])
async def test(message: Message, user: TgUser):
    filename = "C:\\Users\\artyo\\Documents\\ученики.csv"
    clear_database_schooler()
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        total_rows = sum(1 for _ in reader)

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        with tqdm(total=total_rows, desc="Импорт записей", unit=" записей") as pbar:
            for row in reader:
                full_name = row[0]
                class_num = row[1]
                letter = row[2]
                building = row[3]

                last_name, first_name, middle_name = split_full_name(full_name)

                # Добавляем данные в БД
                await add_person(
                    first_name=first_name,
                    last_name=last_name,
                    class_num=class_num,
                    letter=letter,
                    building=building,
                    middle_name=middle_name,
                )

                pbar.update(1)

    await message.answer(f"Импорт завершён. Всего записей: {total_rows}")


@router.message(Command("incidents"))
@role_required(["director", "deputy"])
async def incident_report(message: Message, user: TgUser):
    text, text1 = await get_incidents_message()

    await message.answer(text)
    await message.answer(text1)
