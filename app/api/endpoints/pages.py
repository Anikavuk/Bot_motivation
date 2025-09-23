
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, PlainTextResponse

from app.services.motivational_ai import OllamaMotivator

router = APIRouter()


@router.get("/")
def index():
    """Метод загрузки стартовой страницы"""
    return FileResponse("app/templates/index.html")


@router.post("/get_prediction")
def get_prediction(request: Request):
    """Метод загрузки страницы с предсказанием"""
    prediction_class = OllamaMotivator()
    prediction_text = prediction_class.get_motivational_support()
    return PlainTextResponse(content=prediction_text)


@router.post("/questions")
def questions():
    """Метод загрузки анкеты пользователя"""
    return FileResponse("app/templates/questions.html")
