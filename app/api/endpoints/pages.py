import uuid

from fastapi import APIRouter, Depends, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.schemas import CreateUser
from app.auth.user_service import UserService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Метод загрузки стартовой страницы"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/create_user", response_class=HTMLResponse)
def create_user(request: Request):
    """Метод загрузки страницы создания пользователя"""
    session_uuid = uuid.uuid4()
    return templates.TemplateResponse(
        "create_user.html", {"request": request, "id": session_uuid}
    )


# @router.post("/save_user", response_class=HTMLResponse)
# async def save_user(request: Request, name: str = Form(...),  session_uuid: str = Form(...)):
#     """Метод загрузки страницы сохранения пользователя"""
#     user = UserService(name=name, session_or_telegram_id=session_uuid)
#     await user.create_user()
#     return templates.TemplateResponse("save_user.html",
#                                       {"request": request, "name": name, "id": session_uuid})
@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
    request: Request,
    name: str = Form(...),
    session_uuid: str = Form(...),
    service: UserService = Depends(UserService),
):
    user_data = CreateUser(name=name, session_or_telegram_id=session_uuid)
    await service.create_user(user=user_data)
    return templates.TemplateResponse(
        "save_user.html", {"request": request, "name": name, "id": session_uuid}
    )


# /@router.post("/save_user", response_class=HTMLResponse)
# def save_user(request: Request):
#     """Метод загрузки страницы сохранения пользователя"""
#     return templates.TemplateResponse("save_user.html", {"request": request})


# @router.post("/get_prediction", response_class=HTMLResponse)
# async def get_prediction(response: Response,
#                          session_id: str = Cookie(None),
#                          telegram_user_id: str = None
#                          ):
#     """Метод загрузки страницы с предсказанием"""
#     ident = Identification(user_session=session_id)
#     new_cookie_value = ident.generate_cookie_value(telegram_user_id=telegram_user_id)
#     response.set_cookie(key="session_id", value=new_cookie_value, max_age=86400, httponly=True)
#
#     session_uuid = new_cookie_value.split(":")[0]
#     telegram_user_id = new_cookie_value.split(":")[1]
#     prediction_service = PredictionService(db_session)
#     prediction = await prediction_service.find_prediction_in_db(telegram_user_id=telegram_user_id)
#     if not prediction:
#         predictor = HuggingFacePredictor()
#         response_text = predictor.get_prediction()
#         # await prediction_service.save_prediction_in_db(telegram_user_id=telegram_user_id, main_prediction=response_text)
#     else:
#         response_text = prediction
#     return templates.TemplateResponse(
#         "get_prediction.html", {"request": response, "prediction": response_text}
#     )


@router.post("/questions", response_class=HTMLResponse)
def questions(request: Request):
    """Метод загрузки анкеты пользователя"""
    return templates.TemplateResponse("questions.html", {"request": request})
