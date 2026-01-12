from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    # Proxy Settings
    INITIAL_SCORE: int = 10
    MAX_SCORE: int = 100
    MIN_SCORE: int = 0
    SCORE_DECREMENT: int = 20
    SCORE_INCREMENT: int = 10

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
