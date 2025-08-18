from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def index_page():
    return FileResponse("app/templates/index.html")


@router.get("/get_prediction")
def get_prediction_page():
    return FileResponse("app/templates/get_prediction.html")


@router.get("/questions")
def questions_page():
    return FileResponse("app/templates/questions.html")
