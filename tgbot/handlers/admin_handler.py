import datetime

from asgiref.sync import sync_to_async
from django.db import transaction
from aiogram import Router, F, Bot

from aiogram.types import CallbackQuery
from Web.AdminPanel.models import TgUser, User, AdminNotification, RecordDate, Record

router = Router()


@router.callback_query(F.data.startswith("accept"))
async def accept_user(call: CallbackQuery, user: TgUser):
    user_id = call.data.split(":")[1]
    User.objects.filter(tg_user__telegram_id=user_id).update(is_accept=True)
    await call.message.bot.send_message(user_id, text="Вы успешно зарегистрированы.")
    await call.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("nonaccept"))
async def reject_user(call: CallbackQuery, user: TgUser):
    user_id = call.data.split(":")[1]
    await call.message.bot.send_message(
        user_id, text="Заявка была отклонена. Обратитесь в поддержку."
    )
    await call.message.edit_reply_markup(reply_markup=None)


@sync_to_async
def get_records(today, lesson_num):
    return Record.objects.filter(date__date=today, lesson_num=lesson_num).order_by(
        "frame", "class_num"
    )


@sync_to_async
def get_admins():
    return TgUser.objects.filter(is_admin=True)


@sync_to_async
def get_notification(today, admin, lesson_num):
    return AdminNotification.objects.filter(
        date=today, admin_id=admin.telegram_id, lesson_num=lesson_num
    ).first()


@sync_to_async
def create_notification(today, admin, sent_message, lesson_num):
    with transaction.atomic():
        return AdminNotification.objects.create(
            date=today,
            admin_id=admin.telegram_id,
            message_id=sent_message.message_id,
            lesson_num=lesson_num,
        )


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


async def create_record(
    frame,
    class_num,
    letter,
    count,
    lesson_num,
    record_date=None,
):

    if record_date is None:
        record_date = datetime.date.today()

    record_date_obj, created = await RecordDate.objects.aget_or_create(date=record_date)

    new_record = Record.objects.create(
        frame=frame,
        class_num=class_num,
        letter=letter,
        count=count,
        date=record_date_obj,
        lesson_num=lesson_num,
    )

    return new_record
