from aiogram import types
from functools import wraps

from Web.AdminPanel.models import User, TgUser


def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, user: TgUser, *args, **kwargs):

            if not user or user.user.role not in allowed_roles:
                await message.answer(
                    "У вас недостаточно прав для выполнения этой команды."
                )
                return
            return await func(message, user, *args, **kwargs)

        return wrapper

    return decorator
