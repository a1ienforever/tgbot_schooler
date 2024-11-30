from .register_handler import router as register_router
from .user_handler import router as user_router
from .admin_handler import router as admin_router
from .incident_form_handler import router as incident_router
from .incident_later_handler import router as incident_later_router

routers_list = [
    admin_router,
    register_router,
    user_router,
    incident_later_router,
    incident_router,
]


__all__ = [
    "routers_list",
]
