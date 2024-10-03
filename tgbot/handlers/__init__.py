from .register import register_router
from .user import user_router
from .schedule_msg import scheduler_router

routers_list = [
    register_router,
    user_router,
    scheduler_router
]


__all__ = [
    "routers_list",
]
