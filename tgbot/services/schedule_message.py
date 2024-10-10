from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Web.AdminPanel.models import User


scheduler = AsyncIOScheduler()


# TODO подключить Redis
async def schedule_messages(bot: Bot, storage, lesson_number):
    users = User.objects.all()
    from tgbot.handlers.user_handler import choose_start

    for user in users:
        await choose_start(user.tg_user.telegram_id, bot, lesson_number)


def start_scheduler(bot: Bot, storage):
    scheduler.add_job(
        schedule_messages, "cron", hour=1, minute=1, args=[bot, storage, 1]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=0, minute=53, args=[bot, storage, 2]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=0, minute=54, args=[bot, storage, 3]
    )  # Запуск каждый день в 12:00
    scheduler.add_job(
        schedule_messages, "cron", hour=0, minute=9, args=[bot, storage, 4]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=0, minute=10, args=[bot, storage, 5]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=0, minute=11, args=[bot, storage, 6]
    )
    scheduler.start()

