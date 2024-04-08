from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Booking
from app.database import async_session_maker
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.hotels.schemas import HotelWithLeftRoomsSchema
from app.service import BaseService


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def find_with_location(
        cls, location: str, date_from: date, date_to: date
    ) -> list[HotelWithLeftRoomsSchema]:
        async with async_session_maker() as session:
            booked_rooms = (
                select(Booking, Room.hotel_id)
                .join(Room, Room.id == Booking.room_id)
                .where(
                    or_(
                        and_(
                            Booking.date_from >= date_from, Booking.date_from < date_to
                        ),
                        and_(
                            Booking.date_from <= date_from, Booking.date_to > date_from
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_hotels = (
                select(
                    Hotel.__table__.columns,
                    (Hotel.rooms_quantity - func.count(booked_rooms.c.id)).label(
                        "left_rooms"
                    ),
                )
                .join(booked_rooms, booked_rooms.c.hotel_id == Hotel.id, isouter=True)
                .where(Hotel.__table__.c.location == location)
                .group_by(Hotel.id)
            )

            hotels = await session.execute(get_hotels)

        return hotels.mappings().all()
