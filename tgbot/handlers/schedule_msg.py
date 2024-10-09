from aiogram import Router, Bot
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from Web.AdminPanel.models import TgUser, User
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.inline import choose_frame_kb
from tgbot.misc.states import SchoolerCounter

# Создаём роутер
scheduler_router = Router()


# Функция для отправки сообщения всем пользователям
async def send_message_to_all_users(bot: Bot):
    # Получаем всех пользователей из базы данных
    users = User.objects.all()

    for user in users:
        try:
            # Отправляем сообщение каждому пользователю
            await bot.send_message(chat_id=user.tg_user.telegram_id, text="Hello",
                                   reply_markup=choose_frame_kb())

        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user.tg_user.telegram_id}: {e}")


# Функция для планирования задачи отправки сообщений
# async def schedule_broadcast(bot: Bot, message, send_time: datetime, state: FSMContext):
#     # Инициализируем планировщик
#     scheduler = AsyncIOScheduler()
#
#     # Планируем задачу на определённое время
#     scheduler.add_job(
#         send_message_to_all_users,
#         trigger="date",
#         run_date=send_time,
#         kwargs={'bot': bot,
#                 'message': message}
#     )
#
#     # Запускаем планировщик
#     scheduler.start()


