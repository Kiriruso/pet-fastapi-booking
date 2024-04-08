import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.bookings.models import Booking
from app.database import Base, async_engine, async_session_maker
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.main import app as fastapi_app
from app.settings import app_settings
from app.users.auth import get_password_hash
from app.users.models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert app_settings.mode == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app\\tests\\mock_{model}.json", "r") as data:
            return json.load(data)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for user in users:
        user["password"] = get_password_hash(user["password"])

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotel).values(hotels)
        add_rooms = insert(Room).values(rooms)
        add_users = insert(User).values(users)
        add_bookings = insert(Booking).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/auth/login", json={"email": "test_1@test.com", "password": "qwerty_1"}
        )
        assert ac.cookies.get("booking_access_token") is not None
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
