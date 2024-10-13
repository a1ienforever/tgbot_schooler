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
        schedule_messages, "cron", hour=15, minute=28, args=[bot, storage, 1]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=15, minute=17, args=[bot, storage, 1]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=15, minute=19, args=[bot, storage, 2]
    )  # Запуск каждый день в 12:00
    scheduler.add_job(
        schedule_messages, "cron", hour=15, minute=21, args=[bot, storage, 2]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=14, minute=10, args=[bot, storage, 5]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=19, minute=31, args=[bot, storage, 6]
    )
    scheduler.start()
