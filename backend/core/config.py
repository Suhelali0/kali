import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    ENV = os.getenv("ENV", "development")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
