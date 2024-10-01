from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://root:root@localhost:5432/url_shortener"
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    OTP_EXPIRATION_MIN: int = int(os.getenv("OTP_EXPIRATION_MIN", 5))

    class Config:
        env_file = ".env"


settings = Settings()
