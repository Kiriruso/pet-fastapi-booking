from pydantic import BaseModel, JsonValue


class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: JsonValue
    rooms_quantity: int
    image_id: int

    class ConfigDict:
        from_attributes = True


class HotelWithLeftRoomsSchema(HotelSchema):
    left_rooms: int
