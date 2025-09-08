
from datetime import datetime
from sqlalchemy import Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


from app.db.mixins.id_mixins import Uuid_Mixin
from app.db.models import Base


class User(Uuid_Mixin, Base):
    """
    Класс User представляет пользователя в системе.

    """
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    zodiac_sign: Mapped[str] = mapped_column(Text, nullable=True)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    date_prediction: Mapped[datetime] = mapped_column( DateTime(timezone=True),nullable=True)
    prediction_table = relationship("Prediction_Table", back_populates="user", cascade="all, delete-orphan")


class Prediction_Table(Base):
    """
    Класс для предсказаний.

    """
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    main_prediction: Mapped[str] = mapped_column(Text)
    extended_prediction: Mapped[str] = mapped_column(Text)
    user = relationship("User", back_populates="prediction_table")
