from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FitNexa API"
    database_url: str = "sqlite:///./FitNexa.db"
    frontend_origin: str = "http://127.0.0.1:5500"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
