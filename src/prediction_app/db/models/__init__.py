from prediction_app.db.models.base import Base
from prediction_app.db.models.prediction import Prediction
from prediction_app.db.models.users import User


# эта строчка для алембика, для корректной работы алембика
__all__ = ("Base", "User", "Prediction")
