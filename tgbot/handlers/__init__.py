from .register_handler import router as register_router
from .user_handler import router as user_router
from .admin_handler import router as admin_router

routers_list = [
    admin_router,
    register_router,
    user_router,
]


__all__ = [
    "routers_list",
]
