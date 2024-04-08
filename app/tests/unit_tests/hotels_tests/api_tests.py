import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        # Correct tests
        ("Moscow, st. Sinichkina 1", "2024-04-03", "2024-04-13", 200),
        ("Saint Petersburg, st. Nevsky 10", "2024-04-03", "2024-04-13", 200),
        ("Kazan, st. Bauman 7", "2024-04-03", "2024-04-13", 200),
        # Undefined location test
        ("Undefined Location", "2024-04-03", "2024-04-13", 200),
        # Incorrect dates
        # date_from == date_to
        ("Kazan, st. Bauman 7", "2024-04-03", "2024-04-03", 400),
        # date_from > date_to
        ("Kazan, st. Bauman 7", "2024-04-13", "2024-04-03", 400),
        # incorrect format dates
        ("Kazan, st. Bauman 7", "2024-13-04", "2024-03-04", 422),
    ],
)
async def test_get_hotels_with_location(
    location: str, date_from: str, date_to: str, status_code: int, ac: AsyncClient
):
    response = await ac.get(
        f"/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
