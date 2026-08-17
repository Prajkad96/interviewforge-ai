import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "interviewforge-secret-key-super-secure-2026")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "interviewforge.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max payload
