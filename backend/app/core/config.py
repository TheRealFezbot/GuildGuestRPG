from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    frontend_url: str = "http://localhost:5173"
    email_sender: str = "onboarding@resend.dev"
    cors_origins: list[str] = ["http://localhost:5173"]
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    resend_api_key: str
    environment: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()