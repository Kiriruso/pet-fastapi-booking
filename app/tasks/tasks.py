import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.settings import service_google_settings as google
from app.tasks.celeryconfig import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(rf"app\statics\images\resized_1000_500_{im_path.name}")
    im_resized_200_100.save(rf"app\statics\images\resized_200_100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(booking: dict, recipient: EmailStr):
    msg_content = create_booking_confirmation_template(booking, recipient)
    with smtplib.SMTP_SSL(google.SMTP_HOST, google.SMTP_PORT) as server:
        server.login(google.SMTP_USERNAME, google.APP_SECRET)
        server.send_message(msg_content)
