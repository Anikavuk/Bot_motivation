from datetime import datetime
from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db.models import Base


class User(Base):
    """
    Класс User представляет пользователя в системе.

    """

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=True)
    date_prediction: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    uuid: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    prediction = relationship(
        "Prediction", back_populates="user", cascade="all, delete-orphan"
    )
