from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    google_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Check if API key is available
if not settings.google_api_key:
    print("⚠️  Warning: Google API key not found!")
    print("Please create a .env file with your google_api_key")
    print("You can get your API key from: https://makersuite.google.com/app/apikey")
    print("Example .env file content:")
    print("google_api_key=your_actual_api_key_here")
