# SECTION 1: Imports
from pydantic_settings import BaseSettings, SettingsConfigDict


# SECTION 2: Application Settings
class Settings(BaseSettings):
    app_name: str = "AISP Baseball Analytics Engine"
    database_url: str = "sqlite:///./data/warehouse/aisp_baseball.db"
    mlb_api_base_url: str = "https://statsapi.mlb.com/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# SECTION 3: Shared Settings Instance
settings = Settings()
