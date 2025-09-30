import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

#in production 

def _fix(url: str) -> str:
    return url.replace("postgres://", "postgresql://", 1) if url and url.startswith("postgres://") else url

class Config:
    SQLALCHEMY_DATABASE_URI = _fix(os.getenv("DATABASE_URL", "sqlite:///test.db"))  # dev default: SQLite file
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    CALDERA_URL = os.getenv("CALDERA_URL", "http://localhost:8888")
    API_KEY = os.getenv("CALDERA_API_KEY", "ADMIN123")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000/")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")




# This is a temporary database with sql , later will be changed to postgresql when connected to the server 
#SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@server-ip:5432/dbname"

