from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.redis import RedisStorage  # или MemoryStorage


from Web.AdminPanel.models import User
from tgbot.keyboards.inline import choose_frame_kb
from tgbot.misc.states import SchoolerCounter


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


# async def send_scheduled_message(user_id: int, bot: Bot, state: FSMContext):
#     current_state = await state.get_state()  # Получаем текущее состояние
#
#     # Если необходимо, обрабатываем предыдущее состояние
#     if current_state is not None:
#         # Например, можно записать его в логи или обработать
#         print(f"Current state before sending new message: {current_state}")
#     await bot.send_message(
#         user_id,
#         "Пожалуйста выберите корпус учащихся",
#         reply_markup=choose_frame_kb(),
#     )
#
#     await state.set_state(SchoolerCounter.frame)
#     print(f"State set to: {SchoolerCounter.frame} for user {user_id}")
