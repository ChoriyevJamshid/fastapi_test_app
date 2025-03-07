from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR: Path = Path(__file__).resolve().parent.parent

class DbConfig(BaseModel):
    url: str
    echo: bool = False

class Settings(BaseSettings):
    secret_key: str | None = None
    debug: bool = False

    db: DbConfig

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="_",
        case_sensitive=False
    )


settings = Settings()

