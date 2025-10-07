from dataclasses import dataclass

from aiogram import Bot


@dataclass
class Secrets:
    token: str = "7675393103:AAGWRyLzrNaC1GR6RpcGmFX8i0Kp0p13Ll8"
    admin_id: int = 1469740145


bot = Bot(token=Secrets.token)
