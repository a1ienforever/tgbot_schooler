from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Web.AdminPanel.models import User


scheduler = AsyncIOScheduler()


# TODO подключить Redis
async def schedule_messages(bot: Bot, storage):
    users = User.objects.all()
    from tgbot.handlers.user_handler import choose_start

    for user in users:
        await choose_start(user.tg_user.telegram_id, bot)


def start_scheduler(bot: Bot, storage):
    scheduler.add_job(
        schedule_messages, "cron", hour=12, minute=35, args=[bot, storage]
    )
    scheduler.add_job(schedule_messages, "cron", hour=9, minute=25, args=[bot, storage])
    scheduler.add_job(
        schedule_messages, "cron", hour=10, minute=30, args=[bot, storage]
    )  # Запуск каждый день в 12:00
    scheduler.add_job(
        schedule_messages, "cron", hour=11, minute=30, args=[bot, storage]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=12, minute=30, args=[bot, storage]
    )
    scheduler.add_job(
        schedule_messages, "cron", hour=13, minute=35, args=[bot, storage]
    )
    scheduler.start()

