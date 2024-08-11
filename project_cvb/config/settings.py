from pydantic_settings import BaseSettings, SettingsConfigDict, PyprojectTomlConfigSettingsSource


class Settings(BaseSettings):
  environment: str
  gemini_api_key: str
  open_ai_api_key: str

  class Config:
    env_file = ".env"


class CustomSettings(Settings):

  model_config = SettingsConfigDict(
      pyproject_toml_table_header=("tool.custom_settings"),
  )
