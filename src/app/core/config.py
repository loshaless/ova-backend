import os
from dotenv import load_dotenv
load_dotenv("./app/.env", override=True)

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "10.121.75.46")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hansel_test")

def get_project_id() -> str:
    return os.getenv("PROJECT_ID", "hackfest-vertex-ai")