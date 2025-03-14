from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from Web.AdminPanel.models import TgUser


class DatabaseMiddleware(BaseMiddleware):

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
        return await handler(event, data)
