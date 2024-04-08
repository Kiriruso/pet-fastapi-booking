from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.users.router import router as users_router

all_routers = [
    bookings_router,
    hotels_router,
    users_router,
    pages_router,
    images_router,
]
