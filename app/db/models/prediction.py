from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.db.models import Base


class Prediction(Base):
    """
    Класс для предсказаний.

    """

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    main_prediction: Mapped[str] = mapped_column(Text)
    user = relationship("User", back_populates="prediction")
