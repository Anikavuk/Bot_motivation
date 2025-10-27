from .base import Base
from .users import User
from .prediction import Prediction

# эта строчка для алембика, для корректной работы алембика
__all__ = ("Base", "User", "Prediction")
