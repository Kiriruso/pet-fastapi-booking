import pytest

from app.users.models import User
from app.users.service import UserService


@pytest.mark.parametrize(
    "user_id, user_email, is_exist",
    [
        (1, "test_1@test.com", True),
        (2, "test_2@test.com", True),
        (3, "test_3@test.com", True),
        (4, "test_4@test.com", True),
        (5, "test_5@test.com", True),
        (100, "random_1@test.com", False),
        (200, "random_2@test.com", False),
    ],
)
async def test_find_user_by_id(user_id, user_email, is_exist):
    user: User = await UserService.find_by_id(user_id)

    if is_exist:
        assert user
        assert user.id == user_id
        assert user.email == user_email
    else:
        assert not user
