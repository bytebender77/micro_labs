"""Configuration settings for HealthGuide backend"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    openai_api_key: str = ""
    gemini_api_key: str = ""
    maps_api_key: str = ""
    database_url: str = "sqlite:///./healthguide.db"
    llm_provider: str = "openai"  # openai or gemini
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        # Look for .env file in the backend directory
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

# Debug: Print API key status (without showing actual keys)
if settings.debug:
    print(f"🔑 API Key Status:")
    print(f"   OpenAI: {'✅ Configured' if settings.openai_api_key and settings.openai_api_key not in ['', 'your_key_here', 'your-api-key'] else '❌ Not configured'}")
    print(f"   Gemini: {'✅ Configured' if settings.gemini_api_key and settings.gemini_api_key not in ['', 'your_key_here', 'your-api-key'] else '❌ Not configured'}")
    print(f"   .env file location: {os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')}")

