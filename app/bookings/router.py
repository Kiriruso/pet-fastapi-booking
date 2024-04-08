from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.schemas import (
    BookingDeletedSchema,
    BookingSchema,
    BookingWithRoomDetailSchema,
)
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import User
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    user: User = Depends(get_current_user)
) -> list[BookingWithRoomDetailSchema]:
    return await BookingService.find_all(user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date, user: User = Depends(get_current_user)
) -> BookingSchema:
    booking = await BookingService.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked

    booking_dict = {
        "date_from": booking.date_from,
        "date_to": booking.date_to
    }
    send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int, user: User = Depends(get_current_user)
) -> BookingDeletedSchema:
    return await BookingService.delete(booking_id, user.id)
