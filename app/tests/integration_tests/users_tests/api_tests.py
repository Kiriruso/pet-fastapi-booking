import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("exist@exist.com", "exist", 200),
        ("exist@exist.com", "other_exist", 409),
        ("new_user@new.com", "new", 200),
        ("incorrect_email", "err", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test_1@test.com", "qwerty_1", 200),
        ("test_1@test.com", "incorrect", 401),
        ("test_2@test.com", "qwerty_2", 200),
        ("test_3@test.com", "qwerty_3", 200),
        ("test_4@test.com", "qwerty_4", 200),
        ("test_5@test.com", "qwerty_5", 200),
        ("notexist@test.com", "some_pass", 401),
        ("incorrect_email", "some_pass", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        })

    assert response.status_code == status_code
