from app.auth.user_service import UserService
from app.core.db_dependency import DBDependency

db = DBDependency()


async def checking_time() -> bool:
    user_service = UserService(db=db)
    # prediction_service = PredictionService(db=db)
    users = await user_service.get_all_users()  # <app.db.models.users.User object at 0x000001D5179D8C80>, <app.db.models.users.User object at 0x000001D516772E10>
    users_as_dicts = [
        user.to_dict() for user in users
    ]  # [{'id': 47, 'name': 'Usla', 'uuid': 'e3a7cc59-cbf5-48d1-b746-4f5a4b22316b', 'date_prediction': '2025-10-06T16:25:42.648657+00:00', 'user_timezone': 'Europe/Moscow'},
    print(users_as_dicts)
    # now_utc = datetime.now(ZoneInfo("UTC"))
    # utc_time = datetime.fromisoformat(user.date_prediction)
    # user_tz= user.user_timezone
    # local_dt = utc_time.replace(tzinfo=user_tz)
    # next_midnight_local = (local_dt + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # next_midnight_utc = next_midnight_local.astimezone(ZoneInfo('UTC'))
    # if now_utc >= next_midnight_utc:
    #     return True


# def deleted_prediction():
#     users = user_service.get_all_users()
#     now_utc = datetime.now(timezone.utc)
#     today_date = now_utc.date()
#     print(users)
#     print(now_utc)
#     print(today_date)
#
