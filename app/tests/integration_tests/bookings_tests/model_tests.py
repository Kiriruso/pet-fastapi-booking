from datetime import datetime

import pytest

from app.bookings.service import BookingService


@pytest.mark.parametrize(
    "user_id, room_id, date_from, date_to",
    [
        (2, 2, "2023-05-10", "2023-05-15"),
        (1, 3, "2023-02-19", "2023-02-21"),
    ],
)
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    booking = await BookingService.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime(date_from, "%Y-%m-%d"),
        date_to=datetime.strptime(date_to, "%Y-%m-%d"),
    )

    assert booking.user_id == user_id
    assert booking.room_id == room_id

    booking = await BookingService.find_by_id(booking.id)

    assert booking is not None


@pytest.mark.parametrize(
    "user_id, room_id, date_from, date_to",
    [
        (2, 2, "2023-05-10", "2023-05-15"),
        (1, 3, "2023-02-19", "2023-02-21"),
        # multiply booking
        (1, 3, "2023-02-19", "2023-02-21"),
        (1, 3, "2023-02-19", "2023-02-21"),
        (1, 3, "2023-02-19", "2023-02-21"),
        # not existed room
        # (1, 11, '2023-02-19', '2023-02-21'),
        # not existed user
        # (6, 3, '2023-02-19', '2023-02-21'),
    ],
)
async def test_add_get_delete_booking(user_id, room_id, date_from, date_to):
    booking = await BookingService.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime(date_from, "%Y-%m-%d"),
        date_to=datetime.strptime(date_to, "%Y-%m-%d"),
    )
    assert booking.user_id == user_id
    assert booking.room_id == room_id

    new_booking_id = booking.id
    booking = await BookingService.find_by_id(booking.id)
    assert booking.id == new_booking_id

    deleted_booking = await BookingService.delete(booking.id, booking.user_id)
    assert deleted_booking.id == new_booking_id
    assert deleted_booking.user_id == user_id
    assert deleted_booking.room_id == room_id

    booking = await BookingService.find_by_id(booking.id)
    assert booking is None
