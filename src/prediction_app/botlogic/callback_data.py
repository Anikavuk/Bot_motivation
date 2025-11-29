from aiogram.filters.callback_data import CallbackData


class PredictionBase(CallbackData, prefix="pred"):  # type: ignore[call-arg]
    start_message_id: int
    user_id: int


class SweetPrediction(PredictionBase, prefix="sweet"):  # type: ignore[call-arg]
    pass


class StrictPrediction(PredictionBase, prefix="strict"):  # type: ignore[call-arg]
    pass
