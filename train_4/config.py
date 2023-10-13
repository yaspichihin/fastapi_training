from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# __file__ текущее положение файла, parent указатель на родителя
# В данном случае создаст БД в папке train_3
BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_name: str
    db_echo: bool

    @property
    def db_url(self) -> str:
        return f"sqlite+aiosqlite:///{BASE_DIR}/{self.db_name}"


settings = Settings()
