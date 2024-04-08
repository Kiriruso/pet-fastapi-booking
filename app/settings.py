from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    mode: Literal["DEV", "TEST", "PROD"]
    log_level: Literal["DEBUG", "INFO"]

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="app_", extra="ignore"
    )


class ServiceAuthSettings(BaseSettings):
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="auth_", extra="ignore"
    )


class ServicePostgresSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    db_name: str = Field(alias="db_name")

    test_host: str
    test_port: int
    test_username: str
    test_password: str
    test_db_name: str = Field(alias="db_test_name")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="db_", extra="ignore")

    @property
    def postgresql_url(self):
        return (
            f"postgresql+asyncpg"
            f"://{self.username}"
            f":{self.password}"
            f"@{self.host}"
            f":{self.port}"
            f"/{self.db_name}"
        )

    @property
    def test_postgresql_url(self):
        return (
            f"postgresql+asyncpg"
            f"://{self.test_username}"
            f":{self.test_password}"
            f"@{self.test_host}"
            f":{self.test_port}"
            f"/{self.test_db_name}"
        )


class ServiceRedisSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="redis_", extra="ignore"
    )

    @property
    def redis_url(self):
        return f"redis://{self.host}:{self.port}"


class ServiceGoogleSettings(BaseSettings):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    app_secret: str = Field(alias="google_app_secret")

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="gmail_", extra="ignore"
    )


app_settings = AppSettings()
service_auth_settings = ServiceAuthSettings()
service_postgres_settings = ServicePostgresSettings()
service_redis_settings = ServiceRedisSettings()
service_google_settings = ServiceGoogleSettings()
