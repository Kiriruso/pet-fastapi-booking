from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.settings import service_auth_settings
from app.users.service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(
        to_encode, service_auth_settings.SECRET_KEY, service_auth_settings.ALGORITHM
    )
    return jwt_token


async def authenticate_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if user is not None and not verify_password(password, user.password):
        return None
    return user
