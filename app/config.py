import os
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: int  # Assuming port is an integer
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")
   

settings = Settings()

