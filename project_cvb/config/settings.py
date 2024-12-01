from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  ENVIRONMENT: str
  gemini_api_key: str
  open_ai_api_key: str
  MONGODB_URI: str

  class Config:
    env_file = ".env"
