from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from typing import Optional
import os


class Settings(BaseSettings):
    DATABASE_URI: PostgresDsn

    # well here optional really needs Optional!!
    SERVICE_NAME: Optional[str] = None
    SERVICE_VERSION: Optional[str] = "0.0.1"


class DevSettings(Settings):
    model_config = SettingsConfigDict(env_file="config/dev.env", extra="ignore")


class ProdSettings(Settings):
    # it reads from envvar!
    ...


def find_which_config():
    if os.getenv("ENV"):  # there is DOMAIN name provided
        return ProdSettings()
    else:
        return DevSettings()


configurations = find_which_config()


if __name__ == "__main__":
    s = ProdSettings()
    s = DevSettings()
    print(s.SERVICE_NAME)
    print(s.SERVICE_VERSION)
    print(s.DATABASE_URI)
