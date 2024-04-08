import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels")
async def add_hotel_image(name: int, img_file: UploadFile):
    im_path = f"app/statics/images/{name}.webp"
    with open(im_path, "wb+") as img:
        shutil.copyfileobj(img_file.file, img)
    process_pic.delay(im_path)
