from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from Web.AdminPanel.models import TgUser, User


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user, _ = await TgUser.objects.aget_or_create(
            telegram_id=event.from_user.id,
            username=event.from_user.username,
            tg_fullname=event.from_user.full_name,
        )

        data["user"] = user
        result = await handler(event, data)
        return result
