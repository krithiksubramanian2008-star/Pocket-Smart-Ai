import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "PocketSmart AI")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
    CORS_ORIGINS = [x.strip() for x in os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000"
    ).split(",") if x.strip()]

settings = Settings()
