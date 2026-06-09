import os
from pathlib import Path
from dotenv import load_dotenv

# try finding .env via absolute path mapping
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # search system environment / standard directory lookups
    load_dotenv()

class Settings:
    # Read the connection string directly from your file
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
