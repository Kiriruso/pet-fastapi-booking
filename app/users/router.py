from fastapi import APIRouter, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.schemas import UserAuthSchema
from app.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register")
async def register_user(user: UserAuthSchema):
    is_exist = await UserService.find_one_or_none(email=user.email)
    if is_exist:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user.password)
    await UserService.add(email=user.email, password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user: UserAuthSchema):
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


# @router.get('/me')
# async def get_current_user(user: User = Depends(get_current_user)):
#     return user
#
#
# @router.get('/all')
# async def get_all_users(admin: User = Depends(get_current_admin)) -> list[UserSchema]:
#     return await UserService.find_all()
