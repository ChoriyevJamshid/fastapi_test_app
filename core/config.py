import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv



class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent
    secret_key: str = "Jamshid"
    debug: bool = False

    db_url: str = f"sqlite+aiosqlite:///{base_dir}/db.sqlite3"
    db_echo: bool = False

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

