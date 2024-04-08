import csv
import json
import os
import shutil
from datetime import date

from fastapi import APIRouter, UploadFile, Depends

from app.hotels.rooms.schemas import RoomWithTotalCostAndLeftsSchema
from app.hotels.rooms.service import RoomService
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter()


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> list[RoomWithTotalCostAndLeftsSchema]:
    return await RoomService.find_all(hotel_id, date_from, date_to)


@router.post("/rooms/add")
async def add_rooms(csv_rooms: UploadFile, user: User = Depends(get_current_user)):
    table_path = "app/statics/csvs/roomscsv.csv"

    with open(table_path, "wb+") as csvfile:
        shutil.copyfileobj(csv_rooms.file, csvfile)

    with open(table_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            row["hotel_id"] = int(row["hotel_id"])
            row["price"] = int(row["price"])
            row["services"] = json.loads(row["services"])
            row["quantity"] = int(row["quantity"])
            row["image_id"] = int(row["image_id"])
            await RoomService.add(**row)

    os.remove(table_path)
