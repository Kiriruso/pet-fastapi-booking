from email.message import EmailMessage

from pydantic import EmailStr

from app.settings import service_google_settings


def create_booking_confirmation_template(
    booking: dict, recipient: EmailStr
) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = service_google_settings.smtp_username
    email["To"] = recipient

    email.set_content(
        f"""
        <h1>Подвердите бронирование<h1>
        Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        """,
        subtype="html",
    )
    return email
