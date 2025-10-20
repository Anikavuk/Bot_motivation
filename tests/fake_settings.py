from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class FakeDBSettings(BaseSettings):
    db_name: str = "test_db"
    db_user: str = "test_user"
    db_password: SecretStr = SecretStr("test_password")
    db_host: str = "localhost"
    db_port: int = 5432
    db_echo: bool = False

    model_config = SettingsConfigDict(extra="ignore")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"


# Фейковый класс для HuggingFaceSettings
class FakeHuggingFaceSettings(BaseSettings):
    hf_token: SecretStr = SecretStr("fake_hf_token")

    model_config = SettingsConfigDict(extra="ignore")


# Фейковый класс для BotSettings
class FakeBotSettings(BaseSettings):
    bot_token: SecretStr = SecretStr("fake_bot_token")
    admin_id: int = 123456789

    model_config = SettingsConfigDict(extra="ignore")


# Основной фейковый класс Settings
class FakeSettings(BaseSettings):
    db_settings: FakeDBSettings = FakeDBSettings()
    hf_settings: FakeHuggingFaceSettings = FakeHuggingFaceSettings()
    bot_settings: FakeBotSettings = FakeBotSettings()

    model_config = SettingsConfigDict(extra="ignore")


fake_settings = FakeSettings()
