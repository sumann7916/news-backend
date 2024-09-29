from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    model_config = SettingsConfigDict(env_file=".env")


class SettingsManager:
    # mypy: ignore
    _instance = None

    @classmethod
    def get_settings(cls) -> Settings:
        if cls._instance is None:
            cls._instance = Settings()  # Read from .env only once
        return cls._instance
