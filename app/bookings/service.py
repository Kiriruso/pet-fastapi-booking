from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Booking
from app.bookings.schemas import (
    BookingDeletedSchema,
    BookingSchema,
    BookingWithRoomDetailSchema,
)
from app.database import async_session_maker
from app.hotels.rooms.models import Room
from app.logger import logger
from app.service import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def find_all(cls, user_id: int) -> list[BookingWithRoomDetailSchema]:
        async with async_session_maker() as session:
            get_bookings = (
                select(
                    Booking.__table__.columns,
                    Room.__table__.c.image_id,
                    Room.__table__.c.name,
                    Room.__table__.c.description,
                    Room.__table__.c.services,
                )
                .select_from(Booking)
                .join(Room, Room.id == Booking.room_id, isouter=True)
                .where(Booking.user_id == user_id)
            )

            bookings = await session.execute(get_bookings)
            return bookings.mappings()

    @classmethod
    async def add(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ) -> BookingSchema | None:
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Booking)
                    .where(
                        and_(
                            Booking.room_id == room_id,
                            or_(
                                and_(
                                    Booking.date_from >= date_from,
                                    Booking.date_from < date_to,
                                ),
                                and_(
                                    Booking.date_from <= date_from,
                                    Booking.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Room.quantity - func.count(booked_rooms.c.room_id)).label(
                            "available rooms"
                        )
                    )
                    .select_from(Room)
                    .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                    .where(Room.__table__.c.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar_one_or_none()

                if rooms_left is None or rooms_left <= 0:
                    return None

                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()

                add_booking = (
                    insert(Booking)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Booking)
                )

                booking = await session.execute(add_booking)
                await session.commit()

                return booking.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database"
            else:
                msg = "Unknown"
            msg = f"{msg} Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)

            return None

    @classmethod
    async def delete(cls, booking_id: int, user_id: int) -> BookingDeletedSchema:
        query = (
            delete(Booking)
            .where(and_(Booking.id == booking_id, Booking.user_id == user_id))
            .returning(Booking.id, Booking.room_id, Booking.user_id)
        )
        async with async_session_maker() as session:
            deleted = await session.execute(query)
            await session.commit()
        return deleted.one_or_none()
