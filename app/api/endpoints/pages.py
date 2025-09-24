
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, PlainTextResponse

from app.services.motivation_ai import HuggingFacePredictor

router = APIRouter()


@router.get("/")
def index():
    """Метод загрузки стартовой страницы"""
    return FileResponse("app/templates/index.html")


@router.post("/get_prediction")
def get_prediction(request: Request):
    """Метод загрузки страницы с предсказанием"""
    predictor = HuggingFacePredictor()
    response = predictor.get_prediction()
    return PlainTextResponse(content=response)


@router.post("/questions")
def questions():
    """Метод загрузки анкеты пользователя"""
    return FileResponse("app/templates/questions.html")
