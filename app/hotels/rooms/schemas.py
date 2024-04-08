from pydantic import BaseModel, JsonValue


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None
    price: int
    services: JsonValue | None
    quantity: int
    image_id: int

    class ConfigDict:
        from_attributes = True


class RoomWithTotalCostAndLeftsSchema(RoomSchema):
    total_cost: int
    left_rooms: int
