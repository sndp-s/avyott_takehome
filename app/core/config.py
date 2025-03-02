"""
Application config
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Library API"
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    db_port: str
    minconn: int = 1
    maxconn: int = 10

    api_key: str

settings = Settings()
