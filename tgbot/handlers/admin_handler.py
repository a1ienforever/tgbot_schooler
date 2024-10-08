import datetime

from aiogram import Router, F, Bot

from aiogram.types import Message, CallbackQuery
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


async def send_admin(bot: Bot):

    today = datetime.date.today()

    records = Record.objects.filter(date__date=today).order_by("frame", "class_num")
    if not records.exists():
        return

    message_text = "Записи за сегодня:\n"
    for record in records:
        message_text += f"Корпус: {record.frame}, Класс: {record.class_num}{record.letter}, Количество: {record.count}\n"

    for admin in TgUser.objects.filter(is_admin=True):
        notification = AdminNotification.objects.filter(
            date=today, admin_id=admin.telegram_id
        ).first()

        if notification:

            await bot.edit_message_text(
                chat_id=admin.telegram_id,
                message_id=notification.message_id,
                text=message_text,
            )
        else:

            sent_message = await bot.send_message(
                chat_id=admin.telegram_id, text=message_text
            )

            AdminNotification.objects.create(
                date=today,
                admin_id=admin.telegram_id,
                message_id=sent_message.message_id,
            )


async def create_record(frame, class_num, letter, count, record_date=None):

    if record_date is None:
        record_date = datetime.date.today()

    record_date_obj, created = await RecordDate.objects.aget_or_create(date=record_date)

    new_record = Record.objects.create(
        frame=frame,
        class_num=class_num,
        letter=letter,
        count=count,
        date=record_date_obj,
    )

    return new_record
