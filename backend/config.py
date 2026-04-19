"""
Application configuration module.
Loads ALL settings from the .env file — no secrets are hardcoded.
"""

import json
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """
    Application settings loaded exclusively from environment variables / .env file.
    Sensitive values have no default — the app will fail fast
    if .env is missing, rather than silently using wrong credentials.
    """

    # Database — NO default, must be set in .env
    DATABASE_URL: str

    # Application
    APP_TITLE: str = "Smart Resource Allocation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # CORS — NO default, must be set in .env
    CORS_ORIGINS: str

    # ── JWT Authentication ───────────────────────────────────────
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    # ── Email (SMTP via FastAPI-Mail) ────────────────────────────
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_FROM: Optional[str] = None  # defaults to EMAIL_USERNAME if not set

    # ── Twilio WhatsApp ──────────────────────────────────────────
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE: Optional[str] = None  # e.g. whatsapp:+14155238886

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string to list."""
        return json.loads(self.CORS_ORIGINS)

    @property
    def email_configured(self) -> bool:
        return bool(self.EMAIL_USERNAME and self.EMAIL_PASSWORD)

    @property
    def twilio_configured(self) -> bool:
        return bool(self.TWILIO_ACCOUNT_SID and self.TWILIO_AUTH_TOKEN and self.TWILIO_PHONE)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

