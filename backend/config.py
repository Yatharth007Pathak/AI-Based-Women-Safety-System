import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Basic App Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # MySQL Database Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "yourpassword")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "women_safety_db")

    # Twilio SMS Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Email (SMTP) Configuration
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

    # AI Model Paths
    EMOTION_MODEL_PATH = os.getenv(
        "EMOTION_MODEL_PATH",
        "../ai_models/emotion/emotion_model.h5"
    )

    SOUND_MODEL_PATH = os.getenv(
        "SOUND_MODEL_PATH",
        "../ai_models/sound/sound_model.pkl"
    )

    # Geo-Fencing Configuration
    RISK_RADIUS_KM = float(os.getenv("RISK_RADIUS_KM", 0.5))

    # App Behavior
    DEBUG = os.getenv("DEBUG", "True") == "True"