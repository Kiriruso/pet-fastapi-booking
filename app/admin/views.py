from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.password]
    column_details_exclude_list = [User.password]

    can_delete = False


class HotelAdmin(ModelView, model=Hotel):
    column_list = "__all__"


class RoomAdmin(ModelView, model=Room):
    column_list = "__all__"


class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"


all_views = [UserAdmin, HotelAdmin, RoomAdmin, BookingAdmin]
