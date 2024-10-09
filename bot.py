import asyncio
import logging
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config, Config

from tgbot.middlewares.config import ConfigMiddleware


async def on_startup(bot: Bot, admin_ids: list[int]):
    from tgbot.services import broadcaster, schedule_message
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен")
    config = load_config(".env")
    schedule_message.start_scheduler(bot, get_storage(config))



def register_global_middlewares(dp: Dispatcher, config: Config):
    from tgbot.middlewares.database import DatabaseMiddleware

    middleware_types = [ConfigMiddleware(config), DatabaseMiddleware()]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(filename)s - LINE:%(lineno)d] %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    setup_logging()
    config = load_config(".env")
    storage = get_storage(config)
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    os.environ["DJANGO_SETTINGS_MODULE"] = "Web.Web.settings"
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})

    django.setup()
    from tgbot.handlers import routers_list

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")
