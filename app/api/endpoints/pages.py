from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def index():
    """Метод загрузки стартовой страницы"""
    return FileResponse("app/templates/index.html")


@router.post("/get_prediction")
def get_prediction():
    """Метод загрузки страницы с предсказанием"""
    return FileResponse("app/templates/get_prediction.html")


@router.post("/questions")
def questions():
    """Метод загрузки анкеты пользователя"""
    return FileResponse("app/templates/questions.html")
