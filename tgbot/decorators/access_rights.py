from functools import wraps
from aiogram import types
from aiogram.types import Message

from Web.AdminPanel.models import TgUser


def is_superuser(func):
    @wraps(func)
    async def wrapper(message: Message, user: TgUser, *args, **kwargs):
        if not user.user.is_superuser:
            await message.answer("Вы не можете воспользоваться данной команды")
            return
        return await func(message, *args, **kwargs)

    return wrapper


def is_admin(func):
    @wraps(func)
    async def wrapper(message: Message, user: TgUser, *args, **kwargs):
        if not user.is_admin:
            await message.answer("Вы не можете воспользоваться данной команды")
            return
        return await func(message, *args, **kwargs)

    return wrapper
