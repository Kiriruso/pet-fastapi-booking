from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("room.id"))
    user_id = Column(ForeignKey("user.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_days = Column(Integer, Computed("date_to - date_from"))
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))

    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")

    # def __str__(self) -> str:
    #     return f'booking #{self.id}'
