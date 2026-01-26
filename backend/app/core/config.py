from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WikiSmart Edu API"
    environment: str = "local"
    debug: bool = True

    # Database
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/wikismart"

    # Auth
    jwt_secret_key: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # LLMs
    groq_api_key: str | None 
    gemini_api_key: str | None 
    # Default to a fast, free Groq model suitable for summaries
    groq_model_name: str = "llama-3.1-8b-instant"
    gemini_model_name_translation: str = "gemini-2.5-flash"
    gemini_model_name_quiz: str = "gemini-2.5-flash"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 1024
    # Safety limit for input size sent to LLMs (approx, in characters)
    llm_max_input_chars: int = 12000

    # Wikipedia
    # Can be overridden by env var WIKIPEDIA_USER_AGENT
    wikipedia_user_agent: str = "WikiSmartEdu/1.0 (contact@example.com)"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
