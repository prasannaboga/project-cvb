from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  environment: str
  gemini_api_key: str
  open_ai_api_key: str

  class Config:
    env_file = ".env"
