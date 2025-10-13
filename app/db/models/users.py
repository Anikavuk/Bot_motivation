from datetime import datetime
from typing import Dict
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
    user_timezone: Mapped[str] = mapped_column(Text, nullable=True)
    uuid: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    prediction = relationship(
        "Prediction", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name if self.name else None,
            "uuid": self.uuid,
            "date_prediction": self.date_prediction.isoformat()
            if self.date_prediction
            else None,
            "user_timezone": self.user_timezone,
        }
