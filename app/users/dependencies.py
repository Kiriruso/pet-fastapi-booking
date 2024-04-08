from datetime import datetime

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.settings import service_auth_settings
from app.users.models import User
from app.users.service import UserService


def get_jwt_token(request: Request):
    jwt_token = request.cookies.get("booking_access_token")
    if not jwt_token:
        raise TokenAbsentException()
    return jwt_token


async def get_current_user(jwt_token: str = Depends(get_jwt_token)) -> User:
    try:
        payload = jwt.decode(
            jwt_token, service_auth_settings.secret_key, service_auth_settings.algorithm
        )
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except JWTError:
        raise IncorrectTokenFormatException()

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException()

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException()

    user: User = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException()

    return user


async def get_current_admin(admin: User = Depends(get_current_user)) -> User:
    # Здесь должна быть проверка на администратора исходя из ролей
    # if admin.role != 'admin':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return admin
