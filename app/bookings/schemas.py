from datetime import date

from pydantic import BaseModel, JsonValue


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int

    class ConfigDict:
        from_attributes = True


class BookingWithRoomDetailSchema(BookingSchema):
    image_id: int
    name: str
    description: str | None
    services: JsonValue | None


class BookingDeletedSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
