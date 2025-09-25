from datetime import datetime
from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db.mixins.id_mixins import UuidMixin
from app.db.models import Base


class User(UuidMixin, Base):
    """
    Класс User представляет пользователя в системе.

    """

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=True)
    zodiac_sign: Mapped[str] = mapped_column(Text, nullable=True)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    date_prediction: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    prediction_table = relationship(
        "Prediction", back_populates="user", cascade="all, delete-orphan"
    )
