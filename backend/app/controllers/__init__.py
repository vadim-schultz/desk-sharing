from app.controllers.admin import AdminDesksController, AdminRoomsController
from app.controllers.auth import AuthController
from app.controllers.bookings import BookingsController
from app.controllers.health import health_check
from app.controllers.rooms import RoomsController

__all__ = [
    "AdminDesksController",
    "AdminRoomsController",
    "AuthController",
    "BookingsController",
    "RoomsController",
    "health_check",
]
