import os
import csv
import json
import shutil

from datetime import date, datetime
from fastapi import APIRouter, Query, UploadFile, Depends
from fastapi_cache.decorator import cache

from app.exceptions import BookingDateExceptiom
from app.hotels.rooms.router import router as rooms_router
from app.hotels.schemas import HotelSchema, HotelWithLeftRoomsSchema
from app.hotels.service import HotelService
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/hotels", tags=["Отели"])
router.include_router(rooms_router)


@router.get("")
@cache(expire=10)
async def get_hotels() -> list[HotelSchema]:
    return await HotelService.find_all()


@router.get("/{location}")
async def get_hotels_with_location(
    location: str,
    date_from: date = Query(..., description=f"Например: {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например: {datetime.now().date()}"),
) -> list[HotelWithLeftRoomsSchema]:
    if date_from >= date_to:
        raise BookingDateExceptiom

    if (date_to - date_from).days > 30:
        raise BookingDateExceptiom

    hotels = await HotelService.find_with_location(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> HotelSchema:
    return await HotelService.find_by_id(hotel_id)


@router.post("/add")
async def add_hotels(csv_hotels: UploadFile, user: User = Depends(get_current_user)):
    table_path = "app/statics/csvs/hotelscsv.csv"

    with open(table_path, "wb+") as csvfile:
        shutil.copyfileobj(csv_hotels.file, csvfile)

    with open(table_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            row["services"] = json.loads(row["services"])
            row["rooms_quantity"] = int(row["rooms_quantity"])
            row["image_id"] = int(row["image_id"])
            await HotelService.add(**row)

    os.remove(table_path)
