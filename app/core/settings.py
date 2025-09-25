from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Класс для настройки параметров подключения к базе данных."""

    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_echo: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"


class HuggingFaceSettings(BaseSettings):
    hf_token: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


class Settings(BaseSettings):
    """Класс для хранения настроек приложения."""

    db_settings: DBSettings = DBSettings()
    hf_settings: HuggingFaceSettings = HuggingFaceSettings()

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


settings = Settings()
