from .register_handler import router as register_router
from .user_handler import router as user_router
from .admin_handler import router as admin_router
from .incident_handler import router as incident_router
from .incident_form_handler import router as incident_form_router
from .incident_later_handler import router as incident_later_router

routers_list = [
    admin_router,
    register_router,
    # incident_router,
    incident_form_router,
    incident_later_router,
    user_router,
]

__all__ = [
    "routers_list",
]
