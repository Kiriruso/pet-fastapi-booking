from datetime import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, booked_rooms",
    [
        (10, "2025-11-20", "2025-11-25", 200, 4),
        (10, "2025-11-20", "2025-11-25", 200, 5),
        (10, "2025-11-20", "2025-11-25", 200, 6),
        (10, "2025-11-20", "2025-11-25", 409, 6),
        (10, "2025-11-20", "2025-11-25", 409, 6),
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
            "date_to": datetime.strptime(date_to, "%Y-%m-%d"),
        },
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms


@pytest.mark.parametrize(
    "email, password, auth_status, get_status, delete_status",
    [
        ("test_1@test.com", "qwerty_1", 200, 200, 200),
        ("test_2@test.com", "qwerty_2", 200, 200, 200),
        ("test_3@test.com", "qwerty_3", 200, 200, 200),
        ("test_4@test.com", "qwerty_4", 200, 200, 200),
        ("test_5@test.com", "qwerty_5", 200, 200, 200),
        ("test_1@test.com", "incorrect", 401, 401, 422),
        ("undefined", "aboba", 422, 401, 422),
    ],
)
async def test_get_delete_bookings(
    email: str,
    password: str,
    auth_status: int,
    get_status: int,
    delete_status: int,
    ac: AsyncClient,
):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    response_auth_status = response.status_code
    assert response_auth_status == auth_status

    response = await ac.get("/bookings")
    assert response.status_code == get_status
    bookings = response.json()

    if "detail" in bookings and bookings["detail"] == "Нет токена доступа":
        return

    for booking in bookings:
        response = await ac.delete(f'/bookings/{booking["id"]}')
        assert response.status_code == delete_status

    response = await ac.get("/bookings")
    assert response.status_code == get_status
    bookings = response.json()

    assert len(bookings) == 0
