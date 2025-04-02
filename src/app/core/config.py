import os
from dotenv import load_dotenv

load_dotenv("./app/.env", override=True)

PROJECT_ID = os.getenv("PROJECT_ID", "hackfest-vertex-ai")

# Database Settings
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "10.121.75.46")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hansel_test")

# API Keys
GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "app/secrets/service-account.json")

# TTS Settings
TTS_LANGUAGE_CODE = os.getenv("TTS_LANGUAGE_CODE", "id-ID")
TTS_SPEAKING_RATE: float = os.getenv("TTS_SPEAKING_RATE", 1.2)
TTS_PITCH : float = os.getenv("TTS_PITCH", 3.0)
TTS_GENDER: str = os.getenv("TTS_GENDER", "FEMALE")

# DIFY Settings
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", "")
DIFY_DATASET_PROMO_API_KEY = os.getenv("DIFY_DATASET_PROMO_API_KEY", "")
DIFT_WORKFLOW_API_KEY = os.getenv("DIFT_WORKFLOW_API_KEY", "")