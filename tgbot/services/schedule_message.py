from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from Web.AdminPanel.models import User
from tgbot.services.db import get_admins
from tgbot.utils import get_incidents_message

scheduler = AsyncIOScheduler()


async def schedule_messages(bot: Bot, lesson_number: int):
    users = User.objects.all().filter(tg_user__is_admin=False)
    from tgbot.handlers.user_handler import choose_start

    for user in users:
        await choose_start(user.tg_user.telegram_id, bot, lesson_number)


async def send_all_admin(bot: Bot, msg):
    admins = await User.objects.filter(is_superuser=True, tg_user__is_admin=True)
    for admin in admins:
        await bot.send_message(admin.telegram_id, msg)


def start_scheduler(bot: Bot):
    scheduler.add_job(schedule_messages, "cron", hour=8, minute=30, args=[bot, 1])
    scheduler.add_job(schedule_messages, "cron", hour=9, minute=25, args=[bot, 2])
    scheduler.add_job(schedule_messages, "cron", hour=10, minute=35, args=[bot, 3])
    scheduler.add_job(schedule_messages, "cron", hour=11, minute=30, args=[bot, 4])
    scheduler.add_job(schedule_messages, "cron", hour=12, minute=30, args=[bot, 5])
    scheduler.add_job(schedule_messages, "cron", hour=13, minute=35, args=[bot, 6])
    scheduler.add_job(schedule_messages, "cron", hour=14, minute=30, args=[bot, 7])
    scheduler.add_job(schedule_messages, "cron", hour=15, minute=48, args=[bot, 8])
    scheduler.add_job(schedule_messages, "cron", hour=16, minute=20, args=[bot, 9])
    scheduler.add_job(
        send_all_admin,
        CronTrigger(day_of_week="fri", hour=10, minute=0),
        args=[bot, get_incidents_message()],
    )

    scheduler.start()


def pause_scheduler():
    scheduler.pause()


def resume_scheduler():
    scheduler.resume()
