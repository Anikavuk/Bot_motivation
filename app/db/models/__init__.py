from app.db.models.base import Base
from app.db.models.users import User
from app.db.models.users import Prediction_Table

# эта строчка для алембика, для корректной работы алембика
__all__ = ("Base", "User", "Prediction_Table")
