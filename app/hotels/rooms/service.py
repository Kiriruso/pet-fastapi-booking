from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Booking
from app.database import async_session_maker
from app.hotels.rooms.models import Room
from app.hotels.rooms.schemas import RoomWithTotalCostAndLeftsSchema
from app.service import BaseService


class RoomService(BaseService):
    model = Room

    @classmethod
    async def find_all(
        cls, hotel_id: int, date_from: date, date_to: date
    ) -> list[RoomWithTotalCostAndLeftsSchema]:
        booked_rooms = (
            select(Booking)
            .join(Room, Room.id == Booking.room_id)
            .where(
                or_(
                    and_(Booking.date_from >= date_from, Booking.date_from < date_to),
                    and_(Booking.date_from <= date_from, Booking.date_to > date_from),
                )
            )
            .cte("booked_rooms")
        )

        get_rooms = (
            select(
                Room.__table__.columns,
                (Room.__table__.c.price * (date_to - date_from).days).label(
                    "total_cost"
                ),
                (Room.__table__.c.quantity - func.count(booked_rooms.c.id)).label(
                    "left_rooms"
                ),
            )
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .where(Room.hotel_id == hotel_id)
            .group_by(Room.id)
        )

        async with async_session_maker() as session:
            rooms = await session.execute(get_rooms)
        return rooms.mappings()
