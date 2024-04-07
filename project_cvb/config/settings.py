
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  ENVIRONMENT: str
  GEMINI_API_KEY: str

  class Config:
    env_file = ".env"
