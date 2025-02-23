import os
from dotenv import load_dotenv
load_dotenv("./app/.env", override=True)

def get_project_id() -> str:
    return os.getenv("PROJECT_ID", "hackfest-vertex-ai")