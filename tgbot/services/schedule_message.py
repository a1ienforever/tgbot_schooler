from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db.models import Q

from Web.AdminPanel.models import User
from tgbot.middlewares.schedule import work_day
from tgbot.services.broadcaster import broadcast

from tgbot.utils import get_incidents_message

scheduler = AsyncIOScheduler()


async def schedule_messages(bot: Bot, lesson_number: int, dp: Dispatcher):
    if not work_day():
        return
    users = User.objects.all().filter(Q(role="teacher") | Q(role="deputy"))
    from tgbot.handlers.user_handler import choose_start

    for user in users:
        state = dp.fsm.get_context(
            bot, int(user.tg_user.telegram_id), int(user.tg_user.telegram_id)
        )

        await choose_start(user.tg_user.telegram_id, bot, lesson_number, state)


async def send_all_admin(bot: Bot, msg):
    admins = list(User.objects.filter(is_superuser=True, tg_user__is_admin=True).values_list('tg_user__telegram_id', flat=True))
    await broadcast(bot=bot, text=msg, users=admins)


async def start_scheduler(bot: Bot, dp: Dispatcher):
    scheduler.add_job(schedule_messages, "cron", hour=8, minute=30, args=[bot, 1, dp])
    scheduler.add_job(schedule_messages, "cron", hour=9, minute=25, args=[bot, 2, dp])
    scheduler.add_job(schedule_messages, "cron", hour=10, minute=30, args=[bot, 3, dp])
    scheduler.add_job(schedule_messages, "cron", hour=11, minute=30, args=[bot, 4, dp])
    scheduler.add_job(schedule_messages, "cron", hour=12, minute=30, args=[bot, 5, dp])
    scheduler.add_job(schedule_messages, "cron", hour=13, minute=35, args=[bot, 6, dp])
    scheduler.add_job(schedule_messages, "cron", hour=14, minute=30, args=[bot, 7, dp])
    scheduler.add_job(schedule_messages, "cron", hour=15, minute=25, args=[bot, 8, dp])
    scheduler.add_job(schedule_messages, "cron", hour=16, minute=45, args=[bot, 9, dp])
    scheduler.add_job(
        send_all_admin,
        CronTrigger(day_of_week="fri", hour=10, minute=0),
        args=[bot, await get_incidents_message()],
    )

    scheduler.start()


def pause_scheduler():
    scheduler.pause()


def resume_scheduler():
    scheduler.resume()
