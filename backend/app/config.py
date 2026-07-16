from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Google Gemini
    google_api_key: str
    gemini_embedding_model: str = "models/gemini-embedding-001"
    gemini_generation_model: str = "gemini-2.0-flash"

    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "startup_navigator"
    rag_top_k: int = 5

    # App
    app_name: str = "Startup Navigator"
    frontend_url: str = "http://localhost:3000"
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
