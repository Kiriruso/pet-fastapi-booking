from fastapi import HTTPException, status


class BookingException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail)


class RoomCannotBeBooked(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT, "Не осталось свободных комнат")


class BookingDateExceptiom(BookingException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST, "Некорректный диапазон дат для бронирования"
        )


class UserAlreadyExistsException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT, "Такой пользователь уже существует")


class IncorrectEmailOrPasswordException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Неверная почта или пароль")


class IncorrectTokenFormatException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Неверный формат токена")


class TokenExpiredException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Токен доступа истек")


class TokenAbsentException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Нет токена доступа")


class UserIsNotPresentException(BookingException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED)
