import os
from pydantic_settings import BaseSettings

# Ye class environment variables ko read karegi
# BaseSettings apne aap .env file dhundta hai agar Config me specify kiya ho
class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        # Taki agar warning aaye extra env variables pe toh wo ignore ho
        extra = "ignore" 

# Ye object settings load karega .env file se
# Isko hum baaki files me import kar sakte hain bina baar baar os.getenv lagaye
settings = Settings()
