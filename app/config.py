import os
from dotenv import load_dotenv
#/ye command .env file ko load karti hai taake os.getenv() usko read kar sake/
load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AI Document Intelligence System")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))


settings = Settings()