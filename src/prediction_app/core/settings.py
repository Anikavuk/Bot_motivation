from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.templating import Jinja2Templates


class DBSettings(BaseSettings):
    """Класс для настройки параметров подключения к базе данных."""

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    db_host: str
    db_port: int
    db_echo: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.postgres_db}"


class HuggingFaceSettings(BaseSettings):
    hf_token: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


class BotSettings(BaseSettings):
    bot_token: SecretStr
    admin_id: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


class Settings(BaseSettings):
    """Класс для хранения настроек приложения."""

    db_settings: DBSettings
    hf_settings: HuggingFaceSettings
    bot_settings: BotSettings
    session_secret: SecretStr
    templates_dir: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def templates(self) -> Jinja2Templates:
        return Jinja2Templates(directory=self.templates_dir)


def get_settings():
    return Settings(
        db_settings=DBSettings(),
        hf_settings=HuggingFaceSettings(),
        bot_settings=BotSettings(),
    )


def get_templates() -> Jinja2Templates:
    return get_settings().templates


#
# settings = Settings()
