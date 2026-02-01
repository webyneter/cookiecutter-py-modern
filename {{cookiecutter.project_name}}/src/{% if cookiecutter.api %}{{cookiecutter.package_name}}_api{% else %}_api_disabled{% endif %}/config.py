"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    debug: bool = Field(default=False, description="Enable debug mode")
    environment: str = Field(default="development", description="Environment name")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")  # noqa: S104
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(default=True, description="Allow credentials")
    {%- if cookiecutter.api_auth %}

    # JWT Authentication
    jwt_secret_key: str = Field(
        default="change-me-in-production",
        description="Secret key for JWT encoding",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration in minutes",
    )
    {%- endif %}
    {%- if cookiecutter.api_lambda %}

    # AWS Lambda / Powertools
    powertools_service_name: str = Field(
        default="{{cookiecutter.package_name}}_api",
        validation_alias="POWERTOOLS_SERVICE_NAME",
        description="Service name for Powertools logging and tracing",
    )
    powertools_log_level: str = Field(
        default="INFO",
        validation_alias="POWERTOOLS_LOG_LEVEL",
        description="Log level for Powertools logger",
    )
    {%- if cookiecutter.api_lambda_powertools_metrics %}
    powertools_metrics_namespace: str = Field(
        default="{{cookiecutter.friendly_name}}",
        validation_alias="POWERTOOLS_METRICS_NAMESPACE",
        description="CloudWatch metrics namespace",
    )
    {%- endif %}
    {%- endif %}


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Application settings.
    """
    return Settings()


settings = get_settings()
