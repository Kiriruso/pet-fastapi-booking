from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO"]
    SENTRY_DSN: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )


class ServiceAuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="AUTH_", extra="ignore"
    )


class ServicePostgresSettings(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DB_NAME: str = Field(alias="DB_NAME")

    TEST_HOST: str
    TEST_PORT: int
    TEST_USERNAME: str
    TEST_PASSWORD: str
    TEST_DB_NAME: str = Field(alias="DB_TEST_NAME")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

    @property
    def postgresql_url(self):
        return (
            f"postgresql+asyncpg"
            f"://{self.USERNAME}"
            f":{self.PASSWORD}"
            f"@{self.HOST}"
            f":{self.PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def test_postgresql_url(self):
        return (
            f"postgresql+asyncpg"
            f"://{self.TEST_USERNAME}"
            f":{self.TEST_PASSWORD}"
            f"@{self.TEST_HOST}"
            f":{self.TEST_PORT}"
            f"/{self.TEST_DB_NAME}"
        )


class ServiceRedisSettings(BaseSettings):
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="REDIS_", extra="ignore"
    )

    @property
    def redis_url(self):
        return f"redis://{self.HOST}:{self.PORT}"


class ServiceGoogleSettings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    APP_SECRET: str = Field(alias="GOOGLE_APP_SECRET")

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="GMAIL_", extra="ignore"
    )


app_settings = AppSettings()
service_auth_settings = ServiceAuthSettings()
service_postgres_settings = ServicePostgresSettings()
service_redis_settings = ServiceRedisSettings()
service_google_settings = ServiceGoogleSettings()
